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

st.set_page_config(page_title="多语种车载意图路由器", page_icon="🚗", layout="wide")

# ---- 顶部说明 ----
st.title("🚗 多语种车载意图路由器")
st.caption(
    "把任意语言、甚至中英混说的语音指令，映射到固定的车控功能集。"
    "聚焦现有车机最易漏的 code-switching（混说）场景。"
)

# ---- 侧边栏：引擎状态 ----
with st.sidebar:
    st.header("⚙️ 引擎设置")
    from router import _get_config
    has_key = bool(_get_config("LLM_API_KEY"))
    if has_key:
        st.success(f"LLM 已启用\n\n模型: {_get_config('LLM_MODEL') or 'gpt-4o-mini'}")
    else:
        st.warning("未检测到 LLM_API_KEY\n\n当前使用规则兜底引擎（准确率有限，仅供演示流程）")
    prefer_llm = st.toggle("优先使用 LLM", value=has_key)

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

tab1, tab2, tab3, tab4 = st.tabs(["🎙️ 实时路由", "📊 质量看板", "📖 功能集", "📑 交互文档查询"])

# ---- Tab 1: 实时路由 ----
with tab1:
    st.subheader("输入一条指令")
    examples = [
        "把 air conditioning 调到 20 度",
        "把音量调 louder",
        "navigate to the nearest charging station",
        "给 David 打个电话",
    ]
    col_in, col_ex = st.columns([3, 2])
    with col_in:
        text = st.text_input("指令", value=examples[0], label_visibility="collapsed")
        go = st.button("识别", type="primary")
    with col_ex:
        st.caption("点击试试这些混说示例：")
        for ex in examples:
            if st.button(ex, key=f"ex_{ex}"):
                text = ex
                go = True

    if go and text.strip():
        r = route(text, prefer_llm=prefer_llm)
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
    st.subheader("📑 交互文档查询")
    st.markdown(
        "PM 日常工具：输入缺陷描述或功能咨询,自动分类意图并在交互文档里查找对应功能,判定是否在规格里、定义是否完整。"
    )

    # 上传交互文档
    spec_file = st.file_uploader(
        "上传交互文档 (.xlsx)",
        type=["xlsx"],
        help="按模块分 sheet,每行一个功能,需含:功能ID / 功能名称 / 语音指令示例 / 响应行为 / 异常处理",
        key="spec_file"
    )
    if not spec_file:
        st.info("未上传交互文档,使用内置样例(通用车机交互文档)")
        spec_path = "docs/交互文档_样例.xlsx"
    else:
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            tmp.write(spec_file.read())
            spec_path = tmp.name

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

    if st.button("🔍 查询"):
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
