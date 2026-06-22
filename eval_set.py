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
- 每个车控功能覆盖多种表达(正式/口语/带槽位/省略主语)，避免评测出现盲区。
- 包含易混淆边界样本(如"声音"既可能指音量也可能指别的)，压测路由器的区分力。
- 真实项目里这套集合会扩到每市场几千条并从车机日志回流；这里给一个可演示的种子集。
"""

EVAL_SET = [
    # ======================= 中文 (zh) =======================
    # -- climate.set_temperature --
    ("把温度调到 22 度", "climate.set_temperature", "zh"),
    ("空调温度调高一点", "climate.set_temperature", "zh"),
    ("有点冷，温度升到 26 度", "climate.set_temperature", "zh"),
    ("把副驾这边温度设成 24 度", "climate.set_temperature", "zh"),
    # -- climate.ac_toggle --
    ("打开空调", "climate.ac_toggle", "zh"),
    ("空调关掉", "climate.ac_toggle", "zh"),
    ("把冷气开一下", "climate.ac_toggle", "zh"),
    # -- media.volume --
    ("声音大一点", "media.volume", "zh"),
    ("太吵了，把声音调小", "media.volume", "zh"),
    ("音量调到 50", "media.volume", "zh"),
    # -- media.play --
    ("放周杰伦的歌", "media.play", "zh"),
    ("随便放点音乐", "media.play", "zh"),
    ("来首轻松点的歌", "media.play", "zh"),
    # -- navigation.navigate --
    ("导航去机场", "navigation.navigate", "zh"),
    ("带我回家", "navigation.navigate", "zh"),
    ("去最近的充电站", "navigation.navigate", "zh"),
    # -- window.control --
    ("打开车窗", "window.control", "zh"),
    ("把所有车窗关上", "window.control", "zh"),
    # -- seat.heating --
    ("打开座椅加热", "seat.heating", "zh"),
    ("把主驾座椅加热关了", "seat.heating", "zh"),
    # -- phone.call --
    ("打电话给老婆", "phone.call", "zh"),
    ("拨打 110", "phone.call", "zh"),
    # -- system.unknown --
    ("今天天气怎么样", "system.unknown", "zh"),
    ("讲个笑话听听", "system.unknown", "zh"),
    ("现在几点了", "system.unknown", "zh"),

    # ======================= 英文 (en) =======================
    # -- climate.set_temperature --
    ("set temperature to 70 fahrenheit", "climate.set_temperature", "en"),
    ("make it warmer in here", "climate.set_temperature", "en"),
    ("lower the temperature to 21 degrees", "climate.set_temperature", "en"),
    ("set the passenger side to 24", "climate.set_temperature", "en"),
    # -- climate.ac_toggle --
    ("turn off the AC", "climate.ac_toggle", "en"),
    ("turn on the air conditioning", "climate.ac_toggle", "en"),
    ("switch the AC off", "climate.ac_toggle", "en"),
    # -- media.volume --
    ("turn it down", "media.volume", "en"),
    ("turn the volume up please", "media.volume", "en"),
    ("set volume to 30", "media.volume", "en"),
    # -- media.play --
    ("play some jazz", "media.play", "en"),
    ("play music", "media.play", "en"),
    ("put on some relaxing songs", "media.play", "en"),
    # -- navigation.navigate --
    ("navigate to the nearest charging station", "navigation.navigate", "en"),
    ("take me home", "navigation.navigate", "en"),
    ("drive to the airport", "navigation.navigate", "en"),
    # -- window.control --
    ("close the windows", "window.control", "en"),
    ("open the driver window", "window.control", "en"),
    # -- seat.heating --
    ("turn on seat heating", "seat.heating", "en"),
    ("turn off the passenger seat heater", "seat.heating", "en"),
    # -- phone.call --
    ("call mom", "phone.call", "en"),
    ("dial 911", "phone.call", "en"),
    # -- system.unknown --
    ("tell me a joke", "system.unknown", "en"),
    ("what's the weather like today", "system.unknown", "en"),
    ("how are you doing", "system.unknown", "en"),

    # ============ 中英混说 (mixed / code-switching) ============
    # 现有车机最易掉链子的场景：一句话里中英混用功能词
    # -- climate.set_temperature --
    ("把 air conditioning 调到 20 度", "climate.set_temperature", "mixed"),
    ("temperature 调到 23 度", "climate.set_temperature", "mixed"),
    ("有点热，把 temp 降到 21", "climate.set_temperature", "mixed"),
    # -- climate.ac_toggle --
    ("把 AC 关掉", "climate.ac_toggle", "mixed"),
    ("帮我 turn on 空调", "climate.ac_toggle", "mixed"),
    # -- media.volume --
    ("把音量调 louder", "media.volume", "mixed"),
    ("声音 turn down 一点", "media.volume", "mixed"),
    ("volume 调到 40", "media.volume", "mixed"),
    # -- media.play --
    ("放点 relaxing music", "media.play", "mixed"),
    ("play 一首周杰伦的歌", "media.play", "mixed"),
    # -- navigation.navigate --
    ("带我去 the office", "navigation.navigate", "mixed"),
    ("navigate 去最近的加油站", "navigation.navigate", "mixed"),
    ("帮我 set 一个去机场的路线", "navigation.navigate", "mixed"),
    # -- window.control --
    ("把 driver window 打开", "window.control", "mixed"),
    ("close 一下后面的车窗", "window.control", "mixed"),
    # -- seat.heating --
    ("把副驾的 seat heater 开开", "seat.heating", "mixed"),
    ("turn on 座椅加热", "seat.heating", "mixed"),
    # -- phone.call --
    ("给 David 打个电话", "phone.call", "mixed"),
    ("call 一下我老婆", "phone.call", "mixed"),
    # -- system.unknown --
    ("今天 weather 怎么样", "system.unknown", "mixed"),
    ("讲个 joke 来听听", "system.unknown", "mixed"),
]
