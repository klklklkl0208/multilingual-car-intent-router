# -*- coding: utf-8 -*-
"""
车载意图测试集 (Evaluation Set)
================================
这是项目的核心产品资产：一套带"标准答案"的多语种指令集，
用来量化路由器在不同语言上的表现。

每条 = (指令文本, 期望 intent, 语言标签)
语言标签: zh / en / mixed(中英混说) —— 评测看板按这个维度切分。

设计要点(PM 视角)：
- 故意包含大量 mixed 样本，因为这是现有车机最容易漏的真实场景。
- 覆盖每个车控功能，避免评测出现盲区。
- 真实项目里这套集合会扩到几千条并按市场分语种维护；这里给一个可演示的种子集。
"""

EVAL_SET = [
    # --- 中文 ---
    ("把温度调到 22 度", "climate.set_temperature", "zh"),
    ("打开空调", "climate.ac_toggle", "zh"),
    ("空调关掉", "climate.ac_toggle", "zh"),
    ("声音大一点", "media.volume", "zh"),
    ("放周杰伦的歌", "media.play", "zh"),
    ("导航去机场", "navigation.navigate", "zh"),
    ("打开车窗", "window.control", "zh"),
    ("打开座椅加热", "seat.heating", "zh"),
    ("打电话给老婆", "phone.call", "zh"),
    ("今天天气怎么样", "system.unknown", "zh"),

    # --- 英文 ---
    ("set temperature to 70 fahrenheit", "climate.set_temperature", "en"),
    ("turn off the AC", "climate.ac_toggle", "en"),
    ("turn it down", "media.volume", "en"),
    ("play some jazz", "media.play", "en"),
    ("navigate to the nearest charging station", "navigation.navigate", "en"),
    ("close the windows", "window.control", "en"),
    ("turn on seat heating", "seat.heating", "en"),
    ("call mom", "phone.call", "en"),
    ("tell me a joke", "system.unknown", "en"),

    # --- 中英混说 (code-switching) —— 现有车机最易掉链子的场景 ---
    ("把 air conditioning 调到 20 度", "climate.set_temperature", "mixed"),
    ("把 AC 关掉", "climate.ac_toggle", "mixed"),
    ("把音量调 louder", "media.volume", "mixed"),
    ("放点 relaxing music", "media.play", "mixed"),
    ("带我去 the office", "navigation.navigate", "mixed"),
    ("把 driver window 打开", "window.control", "mixed"),
    ("把副驾的 seat heater 开开", "seat.heating", "mixed"),
    ("给 David 打个电话", "phone.call", "mixed"),
]
