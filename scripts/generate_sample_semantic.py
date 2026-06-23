#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成样例功能协议表

结构对齐真实车企交互文档:
含「项目三级功能点 / 项目四级功能点」中文功能名列 + service / operation / semantic。
这样公开 demo 里模糊匹配("打开车窗""氛围灯"等)能直接命中。
"""
import pandas as pd
import json


def sem(name, **extra):
    """生成 semantic JSON 字符串,格式: {"slots":{"name":...}, ...}"""
    body = {"slots": {"name": name}}
    body.update(extra)
    return json.dumps(body, ensure_ascii=False)


# 样例功能协议数据 —— 三级(英文)/四级(中文)功能点 + 协议三列
data = [
    {"项目三级功能点": "Roll Down the Window", "项目四级功能点": "打开车窗",
     "service": "carControl", "operation": "OPEN", "semantic": sem("car_window", action="open")},
    {"项目三级功能点": "Roll Up the Window", "项目四级功能点": "关闭车窗",
     "service": "carControl", "operation": "CLOSE", "semantic": sem("car_window", action="close")},
    {"项目三级功能点": "Ambient Light", "项目四级功能点": "打开氛围灯",
     "service": "lightControl", "operation": "ON", "semantic": sem("ambient_light", action="on")},
    {"项目三级功能点": "Set Temperature", "项目四级功能点": "设置空调温度",
     "service": "hvacControl", "operation": "SET_TEMP", "semantic": sem("temperature", unit="celsius")},
    {"项目三级功能点": "Toggle AC", "项目四级功能点": "开关空调",
     "service": "hvacControl", "operation": "TOGGLE", "semantic": sem("ac_power")},
    {"项目三级功能点": "Play Music", "项目四级功能点": "播放音乐",
     "service": "mediaControl", "operation": "PLAY", "semantic": sem("media_query")},
    {"项目三级功能点": "Adjust Volume", "项目四级功能点": "调节音量",
     "service": "audioControl", "operation": "SET_VOLUME", "semantic": sem("volume_level")},
    {"项目三级功能点": "Navigate To", "项目四级功能点": "导航",
     "service": "naviControl", "operation": "SET_DEST", "semantic": sem("poi_name")},
    {"项目三级功能点": "Seat Heating", "项目四级功能点": "座椅加热",
     "service": "seatControl", "operation": "HEAT", "semantic": sem("seat_zone")},
    {"项目三级功能点": "Make a Call", "项目四级功能点": "拨打电话",
     "service": "phoneControl", "operation": "DIAL", "semantic": sem("contact_name")},
]

df = pd.DataFrame(data)
df.to_excel("docs/功能协议表_样例.xlsx", index=False, engine="openpyxl")
print(f"✅ 样例功能协议表已生成: docs/功能协议表_样例.xlsx")
print(f"   共 {len(df)} 条协议")
print("\n列名:", list(df.columns))
print("\n前3行:")
print(df.head(3).to_string(index=False))
