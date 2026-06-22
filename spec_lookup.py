# -*- coding: utf-8 -*-
"""
交互文档查询 (Spec Lookup)
===========================
PM 日常痛点工具：给定一条缺陷描述或功能咨询,自动:
1. 分类到意图(复用 router)
2. 在交互文档里查找对应功能
3. 判定"在不在文档里 / 定义全不全"

输入: 缺陷文本 + 交互文档 xlsx
输出: 意图 + 匹配到的文档行 + 覆盖度判定(完整定义/部分定义/未定义)
"""

import pandas as pd
from dataclasses import dataclass
from typing import List, Optional, Dict
from router import route

@dataclass
class SpecMatch:
    """文档匹配结果"""
    found: bool                  # 是否找到对应功能
    sheet_name: str             # 所在 sheet(模块名)
    row_index: int              # 行号(从 0 开始)
    function_id: str            # 功能ID
    function_name: str          # 功能名称
    voice_examples: str         # 语音指令示例
    behavior: str               # 响应行为
    exception: str              # 异常处理
    coverage: str               # 覆盖度: "完整" / "部分" / "未定义"
    coverage_note: str          # 覆盖度说明


def load_spec(xlsx_path: str) -> dict:
    """加载交互文档,返回 {sheet_name: DataFrame}"""
    xl = pd.ExcelFile(xlsx_path)
    return {name: pd.read_excel(xl, name) for name in xl.sheet_names}


def load_intents_from_xlsx(xlsx_path: str) -> Dict[str, str]:
    """
    从上传的功能集 xlsx 加载 intent_id -> 模块名 的映射。
    xlsx 格式: intent_id | 功能名称 | 槽位 | 示例

    返回: {"climate": "空调", "media": "媒体", ...}
    策略: intent_id 前缀(如 climate.set_temperature 的 climate) -> 从功能名称推断模块名
    """
    df = pd.read_excel(xlsx_path)
    if "intent_id" not in df.columns:
        raise ValueError("功能集 xlsx 必须包含 intent_id 列")

    # 简化策略:从 intent_id 前缀推断模块
    # 真实项目应该让用户在 xlsx 里显式指定模块名
    mapping = {}
    for intent_id in df["intent_id"]:
        prefix = str(intent_id).split(".")[0]
        # 硬编码映射(和交互文档的 sheet 名对应)
        MODULE_MAP = {
            "climate": "空调",
            "media": "媒体",
            "navigation": "导航",
            "window": "车窗",
            "seat": "座椅",
            "phone": "电话",
        }
        if prefix in MODULE_MAP:
            mapping[prefix] = MODULE_MAP[prefix]
    return mapping


def search_spec(intent_id: str, user_text: str, spec: dict, intent_to_module: Optional[Dict[str, str]] = None) -> Optional[SpecMatch]:
    """
    在文档里搜索与 intent_id 匹配的功能。

    策略:
    - intent_id 形如 "climate.set_temperature",取前缀 "climate" 对应文档里的"空调"模块
    - 在该模块的 sheet 里,模糊匹配"语音指令示例"列
    - 判定覆盖度:
      - 用户文本能在示例里找到类似说法 → "完整"
      - 意图对,但示例里没覆盖这种说法 → "部分(示例不全)"
      - 完全找不到 → "未定义"
    """
    # intent 映射到文档模块名(默认使用内置映射)
    if intent_to_module is None:
        intent_to_module = {
            "climate": "空调",
            "media": "媒体",
            "navigation": "导航",
            "window": "车窗",
            "seat": "座椅",
            "phone": "电话",
        }
    prefix = intent_id.split(".")[0]
    module = intent_to_module.get(prefix)
    if not module or module not in spec:
        return None  # 文档里没这个模块

    df = spec[module]
    # 假设列名是: 功能ID, 功能名称, 语音指令示例, 响应行为, 异常处理
    # 实际项目中要做更健壮的列名检测
    if "语音指令示例" not in df.columns:
        return None

    # 简单策略:遍历该模块所有行,找第一个语音指令示例包含 intent 关键词的
    # 真实场景应该用向量相似度或 LLM,这里先用关键词粗匹配演示
    for idx, row in df.iterrows():
        examples = str(row.get("语音指令示例", ""))
        # 判定:用户文本里的关键词在示例里出现 → 覆盖度完整
        # 这里简化为:只要 intent 对上就算找到,覆盖度按文本相似度粗判
        # TODO: 真实版本这里应该调 LLM 做语义匹配
        coverage = "部分(示例不全)"
        note = f"文档定义了该功能,但示例未明确覆盖用户的说法:'{user_text}'"

        # 粗略判断:用户文本和示例有重叠词 → 完整
        user_words = set(user_text.replace(" ", ""))
        example_words = set(examples.replace(" ", "").replace("/", ""))
        if len(user_words & example_words) > 3:  # 有 3 个字重叠就算覆盖
            coverage = "完整"
            note = "文档已明确定义该功能和语音指令"

        return SpecMatch(
            found=True,
            sheet_name=module,
            row_index=int(idx),
            function_id=str(row.get("功能ID", "")),
            function_name=str(row.get("功能名称", "")),
            voice_examples=examples,
            behavior=str(row.get("响应行为", "")),
            exception=str(row.get("异常处理", "")),
            coverage=coverage,
            coverage_note=note,
        )

    return None  # 该模块里没找到匹配功能


def query_spec(user_input: str, spec_xlsx_path: str, prefer_llm: bool = True, intents_xlsx_path: Optional[str] = None):
    """
    完整查询流程。

    Args:
        user_input: 用户输入文本
        spec_xlsx_path: 交互文档 xlsx 路径
        prefer_llm: 是否优先使用 LLM 路由
        intents_xlsx_path: 可选,功能集 xlsx 路径。不传则使用内置功能集。

    返回: (RouteResult, SpecMatch | None)
    """
    # 1. 路由到意图
    route_result = route(user_input, prefer_llm=prefer_llm)

    # 2. 加载文档并搜索
    spec = load_spec(spec_xlsx_path)

    # 3. 如果上传了功能集,加载映射关系
    intent_mapping = None
    if intents_xlsx_path:
        try:
            intent_mapping = load_intents_from_xlsx(intents_xlsx_path)
        except Exception as e:
            # 功能集加载失败,降级到内置映射
            print(f"⚠️ 功能集加载失败: {e},使用内置映射")

    match = search_spec(route_result.intent, user_input, spec, intent_mapping) if route_result else None

    return route_result, match
