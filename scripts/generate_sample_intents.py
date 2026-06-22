#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成样例功能集 xlsx"""
import pandas as pd
from intents import INTENTS

rows = []
for intent_id, spec in INTENTS.items():
    rows.append({
        "intent_id": intent_id,
        "功能名称": spec["desc"],
        "槽位": ", ".join(spec["slots"].keys()) if spec["slots"] else "无",
        "示例": " / ".join(spec["examples"][:5]),  # 取前5条示例
    })

df = pd.DataFrame(rows)
df.to_excel("docs/功能集_样例.xlsx", index=False, engine="openpyxl")
print(f"✅ 样例功能集已生成: docs/功能集_样例.xlsx")
print(f"   共 {len(df)} 个功能")
