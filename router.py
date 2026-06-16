# -*- coding: utf-8 -*-
"""
意图路由核心 (Intent Router)
=============================
输入: 任意语言 / 中英混说的自然语言指令
输出: 结构化结果 { intent, slots, confidence, detected_languages, engine }

两条路径：
1) LLM 路径 (主):  调用 OpenAI 兼容接口(千问/DeepSeek/OpenAI 均可)，
   用 few-shot + 强制 JSON 输出，把指令映射到 intents.py 里的固定功能集。
2) 规则路径 (兜底): 没配 API key、或 LLM 调用失败时，用关键词匹配兜底。
   保证 demo 在任何环境下都能跑、能演示。

这样设计的产品考量：车机对"可用性"的要求极高，云端不可用时必须有本地降级。
"""

import os
import re
import json
from dataclasses import dataclass, field, asdict
from typing import Optional

from intents import INTENT_IDS, intents_for_prompt


@dataclass
class RouteResult:
    intent: str
    slots: dict = field(default_factory=dict)
    confidence: float = 0.0
    detected_languages: list = field(default_factory=list)
    engine: str = "rule"          # "llm" 或 "rule"，方便在 UI 上标注来源
    raw: str = ""                 # LLM 原始返回，便于调试展示

    def to_dict(self):
        return asdict(self)


# ---------------------------------------------------------------------------
# 规则兜底引擎：关键词 -> 意图。覆盖中/英及常见混说写法。
# 这不是为了"做得多准"，而是保证无网络/无 key 时 demo 仍可运行。
# ---------------------------------------------------------------------------
_RULES = [
    ("climate.set_temperature", [r"温度", r"调到.*度", r"temperature", r"度"]),
    ("climate.ac_toggle",       [r"空调", r"\bac\b", r"air ?condition"]),
    ("media.volume",            [r"音量", r"声音", r"volume", r"louder", r"turn it (up|down)"]),
    ("media.play",              [r"放.*歌", r"播放", r"play ", r"music", r"音乐"]),
    ("navigation.navigate",     [r"导航", r"带我去", r"navigate", r"go to", r"去"]),
    ("window.control",          [r"车窗", r"window"]),
    ("seat.heating",            [r"座椅加热", r"seat heat"]),
    ("phone.call",              [r"打电话", r"call ", r"拨打"]),
]


def _detect_languages(text: str) -> list:
    """极简语种探测：是否含 CJK、是否含拉丁字母。用于演示'混说检测'。"""
    langs = []
    if re.search(r"[一-鿿]", text):
        langs.append("zh")
    if re.search(r"[a-zA-Z]", text):
        langs.append("en")
    return langs or ["unknown"]


def route_by_rule(text: str) -> RouteResult:
    low = text.lower()
    for intent, patterns in _RULES:
        for p in patterns:
            if re.search(p, low):
                return RouteResult(
                    intent=intent,
                    slots={},
                    confidence=0.4,           # 规则匹配置信度固定给低分，提示"非精确"
                    detected_languages=_detect_languages(text),
                    engine="rule",
                )
    return RouteResult(
        intent="system.unknown",
        confidence=0.2,
        detected_languages=_detect_languages(text),
        engine="rule",
    )


# ---------------------------------------------------------------------------
# LLM 引擎
# ---------------------------------------------------------------------------
_SYSTEM_PROMPT = """你是车载语音助手的意图路由器。用户可能用任意语言，或在一句话里混用多种语言(code-switching)。
你的任务：把用户指令映射到下面固定的车控功能之一，并抽取槽位。

可用功能集：
{intents}

要求：
1. 只能从上面的 intent id 里选一个，选不出就用 system.unknown。
2. confidence 是 0~1 的浮点数，表示你的把握。
3. detected_languages 列出指令里实际出现的语言代码(如 ["zh","en"])。
4. 严格只输出 JSON，不要任何额外文字。格式：
{{"intent": "...", "slots": {{...}}, "confidence": 0.0, "detected_languages": ["..."]}}"""


def _get_config(key: str) -> Optional[str]:
    """读取配置，优先级：环境变量(本地) > Streamlit secrets(云端部署)。
    这样本地 export 和 Streamlit Cloud 的 Secrets 面板两种方式都能用。
    """
    val = os.getenv(key)
    if val:
        return val
    try:
        import streamlit as st
        return st.secrets.get(key)  # 云端在 App settings -> Secrets 配置
    except Exception:
        return None


def _build_client():
    """构造 OpenAI 兼容 client。通过环境变量切换不同厂商。
    需要的环境变量：
      LLM_API_KEY   (必填才走 LLM)
      LLM_BASE_URL  (可选，默认 OpenAI；千问/DeepSeek 填各自地址)
      LLM_MODEL     (可选，默认 gpt-4o-mini)
    """
    api_key = _get_config("LLM_API_KEY")
    if not api_key:
        return None, None
    try:
        from openai import OpenAI
    except ImportError:
        return None, None
    base_url = _get_config("LLM_BASE_URL")  # None -> 官方默认
    model = _get_config("LLM_MODEL") or "gpt-4o-mini"
    client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
    return client, model


def route_by_llm(text: str) -> Optional[RouteResult]:
    client, model = _build_client()
    if client is None:
        return None
    prompt = _SYSTEM_PROMPT.format(intents=intents_for_prompt())
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text},
            ],
            temperature=0,
            response_format={"type": "json_object"},
        )
        raw = resp.choices[0].message.content
        data = json.loads(raw)
        intent = data.get("intent", "system.unknown")
        if intent not in INTENT_IDS:        # LLM 偶尔会编一个不存在的 id
            intent = "system.unknown"
        return RouteResult(
            intent=intent,
            slots=data.get("slots", {}) or {},
            confidence=float(data.get("confidence", 0.0)),
            detected_languages=data.get("detected_languages", []) or _detect_languages(text),
            engine="llm",
            raw=raw,
        )
    except Exception as e:
        # LLM 任何异常都不让 demo 崩，记录到 raw 里方便排查
        return RouteResult(
            intent="system.unknown", confidence=0.0,
            detected_languages=_detect_languages(text),
            engine="llm", raw=f"[LLM error] {e}",
        )


def route(text: str, prefer_llm: bool = True) -> RouteResult:
    """对外统一入口：优先 LLM，失败/无 key 时自动降级规则。"""
    if prefer_llm:
        r = route_by_llm(text)
        if r is not None and r.engine == "llm" and not r.raw.startswith("[LLM error]"):
            return r
        if r is not None and r.raw.startswith("[LLM error]"):
            # LLM 报错 -> 降级规则，但保留错误信息
            fallback = route_by_rule(text)
            fallback.raw = r.raw
            return fallback
    return route_by_rule(text)
