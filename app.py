# -*- coding: utf-8 -*-
"""
多语种车载意图路由器 - Web Demo
================================
运行: streamlit run app.py

两个 Tab:
1) 实时路由: 输入任意语言/中英混说的指令，看它被映射到哪个车控功能。
2) 质量看板: 跑评测集，按语言维度看准确率 —— 体现"混说场景更难"的产品洞察。

没配 API key 也能运行（自动降级到规则引擎），保证随时可演示。
"""

import os
import streamlit as st
import pandas as pd

from router import route
from intents import INTENTS
from evaluator import run_eval, summarize
from style import apply_custom_style
from icons import icon_html, get_icon_svg

# 应用自定义紫色系样式
apply_custom_style()


def lookup_semantic(intent_id, semantic_table):
    """
    从上传的功能协议表里查找 semantic

    匹配逻辑:
    - intent_id 如 "window.control"
    - 在表格里找 domain="carControl" 或类似的行
    - 返回该行的 service, operation, semantic 等字段
    """
    if semantic_table is None or semantic_table.empty:
        return None

    # 简单模糊匹配: intent_id 的前缀 (如 window) 匹配 domain
    # 真实项目应该有更精确的映射规则
    prefix = intent_id.split(".")[0]  # window
    action = intent_id.split(".")[-1]  # control

    # 尝试在表格里找匹配行
    for _, row in semantic_table.iterrows():
        domain_lower = str(row.get('domain', '')).lower()
        intent_lower = str(row.get('intent', '')).lower()
        operation_lower = str(row.get('operation', '')).lower()

        # 模糊匹配: domain 包含 prefix 或 intent/operation 包含 action 关键词
        if (prefix in domain_lower or
            'window' in operation_lower or
            'open' in operation_lower and 'window' in str(row.get('slot', '')).lower()):
            return {
                'domain': row.get('domain'),
                'service': row.get('service'),
                'operation': row.get('operation'),
                'intent': row.get('intent'),
                'slot': row.get('slot'),
                'semantic': row.get('semantic'),
                'source': 'uploaded_table'
            }

    return None


def lookup_from_uploaded_spec(user_text, intent_id, spec_table):
    """
    从上传的功能协议表里查找对应功能的 service, operation, semantic

    通用模糊匹配策略 (方案 B):
    1. 把用户输入与每一行的功能点列做相似度计算
    2. 中英文都支持
    3. 返回相似度最高且超过阈值的行
    """
    if spec_table is None or spec_table.empty:
        return None

    import pandas as pd
    from difflib import SequenceMatcher

    user_clean = user_text.lower().replace(' ', '').strip()

    # 找出"功能点"相关的列(用于匹配的文本列)
    function_cols = [c for c in spec_table.columns
                     if '功能点' in str(c) or 'function' in str(c).lower()
                     or '功能' in str(c) or 'name' in str(c).lower()]
    # 如果没找到功能点列,用所有非协议列
    if not function_cols:
        function_cols = [c for c in spec_table.columns
                         if str(c).lower() not in ['service', 'operation', 'semantic']]

    best_row = None
    best_score = 0.0

    for idx, row in spec_table.iterrows():
        # 收集这一行所有功能点列的文本
        candidates = []
        for col in function_cols:
            val = row.get(col)
            if pd.notna(val) and str(val).strip():
                candidates.append(str(val).lower().replace(' ', ''))

        # 对每个候选文本计算相似度
        for cand in candidates:
            if not cand:
                continue
            if user_clean == cand:
                # 完全相同 -> 满分
                score = 1.0
            elif user_clean in cand or cand in user_clean:
                # 包含关系: 用长度比例衡量"包含的充分性"
                # 避免"打开"这种短通用词成为"打开车窗"的高分误匹配
                shorter = min(len(user_clean), len(cand))
                longer = max(len(user_clean), len(cand))
                score = 0.55 + 0.45 * (shorter / longer)  # 0.55 ~ 1.0
            else:
                # 序列相似度
                seq = SequenceMatcher(None, user_clean, cand).ratio()
                # 关键字符重叠(中文场景),权重压低,避免共享字干扰
                common = set(user_clean) & set(cand)
                overlap = len(common) / len(set(user_clean)) if user_clean else 0
                score = max(seq, overlap * 0.6)

            if score > best_score:
                # 检查这一行有 service 或 semantic
                result = extract_semantic_info(row)
                if result['service'] != 'N/A' or result['semantic'] != 'N/A':
                    best_score = score
                    best_row = result

    # 阈值: 相似度需 > 0.5 才算匹配
    if best_row and best_score >= 0.5:
        best_row['match_score'] = round(best_score, 2)
        return best_row

    return None


def extract_semantic_info(row):
    """从表格行中提取 service, operation, semantic"""
    import pandas as pd

    # 尝试多种可能的列名
    service = None
    operation = None
    semantic = None

    # 查找 service (可能的列名: service, Service, 服务等)
    for col in row.index:
        col_lower = str(col).lower()
        if 'service' in col_lower or '服务' in col_lower:
            service = row[col]
            break

    # 查找 operation (可能的列名: operation, Operation, 操作等)
    for col in row.index:
        col_lower = str(col).lower()
        if 'operation' in col_lower or '操作' in col_lower:
            operation = row[col]
            break

    # 查找 semantic (可能的列名: semantic, Semantic, 语义等)
    for col in row.index:
        col_lower = str(col).lower()
        if 'semantic' in col_lower or '语义' in col_lower:
            semantic = row[col]
            break

    # 如果直接有这些列名
    if service is None:
        service = row.get('service', row.get('Service', 'N/A'))
    if operation is None:
        operation = row.get('operation', row.get('Operation', 'N/A'))
    if semantic is None:
        semantic = row.get('semantic', row.get('Semantic', 'N/A'))

    # 查找功能名称
    function_name = 'N/A'
    for col in row.index:
        if '功能点' in str(col) or 'function' in str(col).lower():
            fn = row[col]
            if pd.notna(fn) and str(fn).strip():
                function_name = str(fn)
                break

    return {
        'service': str(service) if pd.notna(service) else 'N/A',
        'operation': str(operation) if pd.notna(operation) else 'N/A',
        'semantic': str(semantic) if pd.notna(semantic) else 'N/A',
        'function_name': function_name,
        'source': 'uploaded_spec'
    }

st.set_page_config(page_title="多语种车载意图路由器", page_icon="⚡", layout="wide")

# ---- 顶部说明 ----
st.markdown(f"""
<h1 style='display: flex; align-items: center; gap: 12px; font-family: "Space Grotesk", sans-serif; font-weight: 600; color: #0F172A; margin-bottom: 0;'>
    {icon_html('zap', 36, '#7C3AED', inline=False)}
    <span>多语种车载意图路由器</span>
</h1>
""", unsafe_allow_html=True)
st.caption(
    "把任意语言、甚至中英混说的语音指令，映射到固定的车控功能集。"
    "聚焦现有车机最易漏的 code-switching（混说）场景。"
)

# ---- 侧边栏：引擎状态 ----
with st.sidebar:
    st.markdown(f"""
    <h2 style='display: flex; align-items: center; gap: 8px; font-family: "Space Grotesk", sans-serif; font-weight: 600; color: #FFFFFF; font-size: 1.25rem;'>
        {icon_html('settings', 22, '#FFFFFF', inline=False)}
        <span>引擎设置</span>
    </h2>
    """, unsafe_allow_html=True)
    from router import _get_config
    has_key = bool(_get_config("LLM_API_KEY"))
    if has_key:
        st.success(f"LLM 已启用\n\n模型: {_get_config('LLM_MODEL') or 'gpt-4o-mini'}")
    else:
        st.warning("未检测到 LLM_API_KEY\n\n当前使用规则兜底引擎（准确率有限，仅供演示流程）")
    prefer_llm = st.toggle("优先使用 LLM", value=has_key)

    st.divider()

    # 上传功能协议表
    st.markdown("### 📋 功能协议表")

    # 初始化状态
    if 'semantic_file_uploaded' not in st.session_state:
        st.session_state.semantic_file_uploaded = False
        st.session_state.semantic_file_name = None

    # 显示当前状态
    if st.session_state.semantic_file_uploaded and st.session_state.semantic_file_name:
        st.success(f"✅ 已加载: {st.session_state.semantic_file_name}")
        if st.button("🗑️ 清除功能协议表", key="clear_semantic"):
            st.session_state.semantic_table = None
            st.session_state.semantic_file_uploaded = False
            st.session_state.semantic_file_name = None
            st.rerun()

    semantic_file = st.file_uploader(
        "上传功能协议表 (.xlsx)",
        type=["xlsx"],
        help="需含列: service | operation | semantic",
        key="semantic_upload"
    )

    # 加载功能协议表到 session_state
    if semantic_file and not st.session_state.semantic_file_uploaded:
        import tempfile
        import pandas as pd
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            tmp.write(semantic_file.read())
            tmp_path = tmp.name

            try:
                # 读取所有 sheet,找到包含 service, semantic 列的那个
                xl = pd.ExcelFile(tmp_path)
                found_sheet = None
                for sheet_name in xl.sheet_names:
                    df = pd.read_excel(xl, sheet_name=sheet_name)
                    cols_lower = [str(c).lower() for c in df.columns]
                    if 'service' in cols_lower and 'semantic' in cols_lower:
                        found_sheet = sheet_name
                        st.session_state.semantic_table = df
                        st.session_state.semantic_file_uploaded = True
                        st.session_state.semantic_file_name = semantic_file.name
                        st.success(f"✅ 已加载 {len(df)} 条协议 (sheet: {sheet_name})")
                        break

                if not found_sheet:
                    st.warning(f"⚠️ 未找到包含 service/semantic 列的 sheet。文件有 {len(xl.sheet_names)} 个 sheet")
                    st.session_state.semantic_table = None
            except Exception as e:
                st.error(f"加载失败: {e}")
                st.session_state.semantic_table = None
    elif not semantic_file and not st.session_state.semantic_file_uploaded:
        st.session_state.semantic_table = None
        st.info("未上传协议表,将使用内置定义")

    st.divider()
    st.markdown(
        "**如何接入 LLM**\n\n"
        "```bash\n"
        "export LLM_API_KEY=你的key\n"
        "# 千问/DeepSeek 等填各自地址:\n"
        "export LLM_BASE_URL=...\n"
        "export LLM_MODEL=...\n"
        "```"
    )

tab1, tab2, tab3, tab4 = st.tabs([
    "⚡ 实时路由",
    "📊 质量看板",
    "🎯 功能集",
    "🔍 交互文档查询"
])

# ---- Tab 1: 实时路由 ----
with tab1:
    st.subheader("输入一条指令")

    # 初始化 session state
    if 'input_text' not in st.session_state:
        st.session_state.input_text = "把 air conditioning 调到 20 度"

    examples = [
        "把 air conditioning 调到 20 度",
        "把音量调 louder",
        "navigate to the nearest charging station",
        "给 David 打个电话",
        "打开车窗",
    ]

    col_in, col_ex = st.columns([3, 2])
    with col_in:
        text = st.text_input("指令", value=st.session_state.input_text, label_visibility="collapsed")
        st.session_state.input_text = text
        go = st.button("识别", type="primary")
    with col_ex:
        st.caption("点击试试这些混说示例：")
        for ex in examples:
            if st.button(ex, key=f"ex_{ex}"):
                st.session_state.input_text = ex
                st.rerun()

    if go and st.session_state.input_text.strip():
        r = route(st.session_state.input_text, prefer_llm=prefer_llm)
        spec = INTENTS.get(r.intent, {})

        # metric 在窄列里会截断长 intent id, 改用普通文本展示
        c1, c2, c3 = st.columns(3)
        with c1:
            st.caption("识别功能")
            st.markdown(f"### `{r.intent}`")
        with c2:
            st.caption("置信度")
            st.markdown(f"### {r.confidence:.0%}")
        with c3:
            st.caption("引擎")
            st.markdown(f"### {'LLM' if r.engine == 'llm' else '规则兜底'}")

        st.write(f"**功能说明**：{spec.get('desc', '—')}")

        # 功能协议 (Semantic) - 优先从侧边栏上传的功能协议表查询
        semantic_from_uploaded = None
        no_match_table = None  # 记录"已上传但没匹配上"的表,供展开调试

        # 1. 优先: 侧边栏上传的功能协议表
        if 'semantic_table' in st.session_state and st.session_state.semantic_table is not None:
            semantic_from_uploaded = lookup_from_uploaded_spec(
                st.session_state.input_text,
                r.intent,
                st.session_state.semantic_table
            )
            if not semantic_from_uploaded:
                no_match_table = st.session_state.semantic_table

        # 2. 降级: Tab4 上传的交互文档表
        if not semantic_from_uploaded and 'uploaded_spec_table' in st.session_state and st.session_state.uploaded_spec_table is not None:
            semantic_from_uploaded = lookup_from_uploaded_spec(
                st.session_state.input_text,
                r.intent,
                st.session_state.uploaded_spec_table
            )
            if not semantic_from_uploaded and no_match_table is None:
                no_match_table = st.session_state.uploaded_spec_table

        semantic_builtin = spec.get('semantic')

        if semantic_from_uploaded:
            # 使用上传表格里的 semantic
            st.divider()
            st.markdown("### 🔗 功能协议 (Semantic)")
            score = semantic_from_uploaded.get('match_score')
            st.caption(f"📋 *来源: 上传的功能协议表*" + (f" · 匹配度 {score:.0%}" if score else ""))

            # 显示功能名称(如果有)
            if fn := semantic_from_uploaded.get('function_name'):
                st.write(f"**功能**: {fn}")

            col1, col2 = st.columns(2)
            with col1:
                st.caption("**Service (服务)**")
                st.code(semantic_from_uploaded.get('service', 'N/A'), language="")
            with col2:
                st.caption("**Operation (操作)**")
                st.code(semantic_from_uploaded.get('operation', 'N/A'), language="")

            st.caption("**Semantic (语义定义)**")
            # 解析 JSON 并格式化显示
            semantic_data = semantic_from_uploaded.get('semantic', 'N/A')
            if isinstance(semantic_data, str) and semantic_data.startswith('{'):
                try:
                    import json
                    semantic_json = json.loads(semantic_data)
                    st.json(semantic_json)
                except:
                    st.code(semantic_data, language="json")
            else:
                st.code(str(semantic_data), language="")

        elif semantic_builtin:
            # 降级到内置 semantic
            st.divider()
            st.markdown("### 🔗 功能协议 (Semantic)")
            if no_match_table is not None:
                st.caption("⚙️ *来源: 内置定义（上传的表格里没找到匹配行）*")
                with st.expander("📋 没匹配上？点开看表格结构"):
                    st.write("表格列名:", list(no_match_table.columns))
                    st.dataframe(no_match_table.head(5))
            else:
                st.caption("⚙️ *来源: 内置定义*")

            col1, col2 = st.columns([1, 3])
            with col1:
                st.caption("**协议类型**")
                protocol_color = "#10B981" if semantic_builtin['protocol'] == "API" else "#7C3AED"
                st.markdown(f"<span style='background: {protocol_color}; color: white; padding: 4px 12px; border-radius: 6px; font-weight: 600;'>{semantic_builtin['protocol']}</span>", unsafe_allow_html=True)
            with col2:
                st.caption("**指令名称**")
                st.code(semantic_builtin['command'], language="")

            st.caption("**协议描述**")
            st.info(semantic_builtin['description'])

            st.caption("**参数定义**")
            params_display = {}
            for key, value in semantic_builtin['parameters'].items():
                # 替换槽位变量为实际值
                if value.startswith("${") and value.endswith("}"):
                    slot_name = value[2:-1]
                    params_display[key] = f"{value} → {r.slots.get(slot_name, 'N/A')}"
                else:
                    params_display[key] = value
            st.json(params_display)

        langs = "、".join(r.detected_languages)
        if len(r.detected_languages) > 1:
            st.info(f"🔀 检测到混说：{langs}")
        else:
            st.write(f"**检测语言**：{langs}")

        if r.slots:
            st.write("**抽取的槽位**：")
            st.json(r.slots)

        if r.raw:
            with st.expander("查看引擎原始返回（调试）"):
                st.code(r.raw, language="json")


# ---- Tab 2: 质量看板 ----
with tab2:
    st.subheader("按语言维度的识别准确率")
    st.caption(
        "核心洞察：混说（mixed）样本通常比单语种更难，规则引擎在此尤其吃力。"
        "这正是为什么多语市场需要 LLM 路由 + 专门评测。"
    )
    if st.button("▶️ 跑评测集", type="primary"):
        with st.spinner("逐条识别中…"):
            df = run_eval(prefer_llm=prefer_llm)
            summary = summarize(df)

        st.write("### 汇总")
        st.dataframe(
            summary.style.format({"准确率": "{:.1f}%"}),
            use_container_width=True,
        )
        # 用柱状图直观对比各语言准确率（排除"总计"行）
        chart_data = summary.drop(index="总计")[["准确率"]]
        st.bar_chart(chart_data)

        st.write("### 明细")
        st.dataframe(
            df.style.apply(
                lambda row: ["background-color: #ffe6e6" if not row["是否正确"] else "" for _ in row],
                axis=1,
            ),
            use_container_width=True,
        )
    else:
        st.info("点上方按钮运行评测。无 LLM 时跑的是规则引擎，正好能看出混说场景掉分。")


# ---- Tab 3: 功能集 ----
with tab3:
    st.subheader("车机支持的固定功能集")
    st.caption("不管用户怎么说，最终都要落到这些功能之一。新增功能只需改 intents.py。")
    rows = []
    for iid, spec in INTENTS.items():
        rows.append({
            "Intent ID": iid,
            "功能": spec["desc"],
            "槽位": ", ".join(spec["slots"].keys()) or "—",
            "示例": " / ".join(spec["examples"][:3]),
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ---- Tab 4: 交互文档查询 ----
with tab4:
    st.subheader("🔍 交互文档查询")
    st.markdown(
        "PM 日常工具：输入缺陷描述或功能咨询,自动分类意图并在交互文档里查找对应功能,判定是否在规格里、定义是否完整。"
    )

    # 初始化 session state
    if 'spec_file_uploaded' not in st.session_state:
        st.session_state.spec_file_uploaded = False
        st.session_state.spec_file_name = None

    # 上传交互文档
    spec_file = st.file_uploader(
        "上传交互文档 (.xlsx)",
        type=["xlsx"],
        help="需含: service | operation | semantic 等列",
        key="spec_file"
    )

    # 显示当前已加载的文件状态
    if st.session_state.spec_file_uploaded and st.session_state.spec_file_name:
        st.info(f"📁 当前已加载: {st.session_state.spec_file_name}")
        if st.button("🗑️ 清除已上传的文件"):
            st.session_state.uploaded_spec_table = None
            st.session_state.spec_file_uploaded = False
            st.session_state.spec_file_name = None
            st.rerun()

    if spec_file and not st.session_state.spec_file_uploaded:
        import tempfile
        import pandas as pd
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            tmp.write(spec_file.read())
            spec_path = tmp.name
            # 读取所有 sheet,找到包含 service, operation, semantic 列的那个
            try:
                xl = pd.ExcelFile(spec_path)
                found_sheet = None
                for sheet_name in xl.sheet_names:
                    df = pd.read_excel(xl, sheet_name=sheet_name)
                    # 检查是否包含必需的列
                    cols_lower = [str(c).lower() for c in df.columns]
                    if 'service' in cols_lower and 'semantic' in cols_lower:
                        found_sheet = sheet_name
                        st.session_state.uploaded_spec_table = df
                        st.session_state.spec_file_uploaded = True
                        st.session_state.spec_file_name = spec_file.name
                        st.success(f"✅ 已加载功能协议表(sheet: {sheet_name}),共 {len(df)} 行")
                        break

                if not found_sheet:
                    st.warning(f"⚠️ 未找到包含 service/semantic 列的 sheet。文件有 {len(xl.sheet_names)} 个 sheet: {', '.join(xl.sheet_names)}")
                    st.session_state.uploaded_spec_table = None
            except Exception as e:
                st.error(f"表格读取失败: {e}")
                st.session_state.uploaded_spec_table = None
    elif not spec_file and not st.session_state.spec_file_uploaded:
        st.info("未上传文档,使用内置样例(通用车机交互文档)")
        spec_path = "docs/交互文档_样例.xlsx"
        st.session_state.uploaded_spec_table = None
    else:
        # 已经上传过,使用缓存的数据
        spec_path = None

    # 上传功能集
    intents_file = st.file_uploader(
        "上传功能集 (.xlsx,可选)",
        type=["xlsx"],
        help="列名: intent_id | 功能名称 | 槽位 | 示例。不传则使用内置功能集(8 类车控功能)",
        key="intents_file"
    )
    if intents_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            tmp.write(intents_file.read())
            intents_path = tmp.name
        st.success("✅ 已加载自定义功能集")
    else:
        intents_path = None
        st.info("未上传功能集,使用内置 8 类车控功能(空调/媒体/导航/车窗/座椅/电话等)")

    st.divider()

    # 输入缺陷描述
    defect_input = st.text_area(
        "输入缺陷描述或功能咨询:",
        value="用户说'把 air conditioning 调到 20 度',车机没反应",
        height=100,
    )

    if st.button("✨ 查询"):
        with st.spinner("路由中..."):
            from spec_lookup import query_spec
            route_res, match = query_spec(defect_input, spec_path, prefer_llm, intents_path)

        # 路由结果
        st.markdown("### 🎯 路由结果")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.caption("识别功能")
            st.markdown(f"### `{route_res.intent}`")
        with c2:
            st.caption("置信度")
            st.markdown(f"### {route_res.confidence:.0%}")
        with c3:
            st.caption("引擎")
            st.markdown(f"### {'LLM' if route_res.engine == 'llm' else '规则兜底'}")

        if route_res.detected_languages:
            st.caption(f"检测到语言: {', '.join(route_res.detected_languages)}")

        st.divider()

        # 文档匹配结果
        st.markdown("### 📄 文档中的对应功能")
        if not match:
            st.error("❌ 未在交互文档中找到对应功能\n\n可能原因:\n- 该模块未在文档里定义\n- 意图识别错误")
        else:
            st.success(f"✅ 找到匹配功能: **{match.function_name}** ({match.function_id})")
            st.markdown(f"**所在模块**: {match.sheet_name} (第 {match.row_index + 2} 行)")  # +2 因为 header 占 1 行,idx 从 0 开始

            with st.expander("📋 功能详情", expanded=True):
                st.markdown(f"**语音指令示例**:\n```\n{match.voice_examples}\n```")
                st.markdown(f"**响应行为**: {match.behavior}")
                st.markdown(f"**异常处理**: {match.exception}")

            # 覆盖度判定
            st.divider()
            st.markdown("### 🔍 覆盖度判定")
            if match.coverage == "完整":
                st.success(f"✅ **{match.coverage}**")
                st.markdown(match.coverage_note)
            else:
                st.warning(f"⚠️ **{match.coverage}**")
                st.markdown(match.coverage_note)
                st.info(
                    "**建议**: 这可能是产品规格的盲点(文档定义不全)而非开发 bug。\n\n"
                    "可将此场景补充进交互文档的语音指令示例,避免后续测试误报。"
                )
