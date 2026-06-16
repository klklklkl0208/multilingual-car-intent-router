# -*- coding: utf-8 -*-
"""
评测引擎 (Evaluator)
====================
拿 eval_set 跑一遍 router，按语言维度(zh/en/mixed)汇总准确率。
产出的 DataFrame 直接喂给 UI 的"质量看板"。

这是项目里最像 PM 交付物的部分：把"多语种交互好不好"变成可量化、
可对比、可按市场切分的指标，而不是凭感觉。
"""

import pandas as pd

from router import route
from eval_set import EVAL_SET


def run_eval(prefer_llm: bool = True) -> pd.DataFrame:
    """逐条跑评测，返回明细 DataFrame。"""
    rows = []
    for text, expected, lang in EVAL_SET:
        r = route(text, prefer_llm=prefer_llm)
        rows.append({
            "指令": text,
            "语言": lang,
            "期望意图": expected,
            "预测意图": r.intent,
            "是否正确": r.intent == expected,
            "置信度": round(r.confidence, 2),
            "引擎": r.engine,
        })
    return pd.DataFrame(rows)


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    """按语言维度汇总准确率，外加一行总计。"""
    g = df.groupby("语言")["是否正确"].agg(["sum", "count"])
    g["准确率"] = (g["sum"] / g["count"] * 100).round(1)
    g = g.rename(columns={"sum": "正确数", "count": "样本数"})

    total = pd.DataFrame({
        "正确数": [df["是否正确"].sum()],
        "样本数": [len(df)],
        "准确率": [round(df["是否正确"].mean() * 100, 1)],
    }, index=["总计"])

    return pd.concat([g, total])
