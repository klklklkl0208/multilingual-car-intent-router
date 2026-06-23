# -*- coding: utf-8 -*-
"""
车载功能意图集 (Intent Schema)
================================
这是整个系统的"产品定义层"：车机能响应的功能是固定的、可枚举的。
不管用户用什么语言、怎么混说，最终都要落到这里的某一个 intent 上。

每个 intent 包含：
- desc:   功能说明（给 LLM 看，也给看代码的人看）
- slots:  这个功能需要的参数（槽位）
- examples: 多语种示例，既喂给 LLM 当 few-shot，也方便人理解

要新增一个车控功能，只需在这里加一项 —— 路由逻辑无需改动。
"""

# 固定功能集。key 是 intent id，会贯穿整个系统。
INTENTS = {
    "climate.set_temperature": {
        "desc": "设置空调温度",
        "slots": {"value": "数字，目标温度", "zone": "区域: driver/passenger/all"},
        "semantic": {
            "protocol": "CAN",
            "command": "HVAC_SET_TEMP",
            "parameters": {
                "temperature": "${value}",
                "zone": "${zone}",
                "unit": "celsius"
            },
            "description": "通过 CAN 总线向 HVAC 控制器发送温度设置指令"
        },
        "examples": [
            "把温度调到 22 度",
            "set temperature to 70 fahrenheit",
            "把 air conditioning 调到 20 度",  # 中英混说
        ],
    },
    "climate.ac_toggle": {
        "desc": "开关空调",
        "slots": {"state": "on / off"},
        "semantic": {
            "protocol": "CAN",
            "command": "HVAC_POWER_TOGGLE",
            "parameters": {
                "state": "${state}"
            },
            "description": "控制空调主电源开关"
        },
        "examples": ["打开空调", "turn off the AC", "把 AC 关掉"],
    },
    "media.play": {
        "desc": "播放音乐/电台/某首歌",
        "slots": {"query": "歌名/歌手/电台，可为空表示随便放"},
        "semantic": {
            "protocol": "API",
            "command": "MEDIA_PLAY",
            "parameters": {
                "query": "${query}",
                "source": "auto"
            },
            "description": "调用多媒体系统播放接口,支持音乐库/电台/流媒体"
        },
        "examples": ["放周杰伦的歌", "play some jazz", "放点 relaxing music"],
    },
    "media.volume": {
        "desc": "调节音量",
        "slots": {"direction": "up / down / set", "value": "set 时的目标值 0-100"},
        "semantic": {
            "protocol": "API",
            "command": "MEDIA_VOLUME_CONTROL",
            "parameters": {
                "action": "${direction}",
                "level": "${value}"
            },
            "description": "控制多媒体音量,支持相对调节和绝对设置"
        },
        "examples": ["声音大一点", "turn it down", "把音量调 louder", "volume 50"],
    },
    "navigation.navigate": {
        "desc": "导航到某地",
        "slots": {"destination": "目的地名称"},
        "semantic": {
            "protocol": "API",
            "command": "NAV_SET_DESTINATION",
            "parameters": {
                "destination": "${destination}",
                "mode": "fastest"
            },
            "description": "设置导航目的地并规划路线"
        },
        "examples": ["导航去机场", "navigate to the nearest charging station", "带我去 the office"],
    },
    "window.control": {
        "desc": "开关车窗",
        "slots": {"action": "open / close", "position": "driver/passenger/all"},
        "semantic": {
            "protocol": "CAN",
            "command": "WINDOW_CONTROL",
            "parameters": {
                "action": "${action}",
                "window": "${position}"
            },
            "description": "通过车身控制器操作车窗升降"
        },
        "examples": ["打开车窗", "close the windows", "把 driver window 打开"],
    },
    "seat.heating": {
        "desc": "座椅加热开关",
        "slots": {"state": "on / off", "zone": "driver/passenger"},
        "semantic": {
            "protocol": "CAN",
            "command": "SEAT_HEATING_CONTROL",
            "parameters": {
                "state": "${state}",
                "seat": "${zone}"
            },
            "description": "控制座椅加热功能开关"
        },
        "examples": ["打开座椅加热", "turn on seat heating", "把副驾的 seat heater 开开"],
    },
    "phone.call": {
        "desc": "拨打电话",
        "slots": {"contact": "联系人姓名或号码"},
        "semantic": {
            "protocol": "API",
            "command": "PHONE_DIAL",
            "parameters": {
                "contact": "${contact}",
                "type": "voice"
            },
            "description": "通过蓝牙连接手机发起通话"
        },
        "examples": ["打电话给老婆", "call mom", "给 David 打个电话"],
    },
    "system.unknown": {
        "desc": "无法识别为以上任何车控功能时的兜底",
        "slots": {},
        "examples": ["今天天气怎么样", "讲个笑话"],
    },
}

# 给 LLM 用的合法 intent id 列表
INTENT_IDS = list(INTENTS.keys())


def intents_for_prompt() -> str:
    """把意图集格式化成喂给 LLM 的说明文本。"""
    lines = []
    for iid, spec in INTENTS.items():
        slot_str = ", ".join(f"{k}({v})" for k, v in spec["slots"].items()) or "无"
        lines.append(f"- {iid}: {spec['desc']}. 槽位: {slot_str}")
    return "\n".join(lines)
