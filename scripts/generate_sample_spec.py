#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成样例交互文档 xlsx"""
import pandas as pd

sheets = {}

# -- 空调模块 --
sheets["空调"] = pd.DataFrame([
    {
        "功能ID": "HVAC-001",
        "功能名称": "空调温度设置",
        "语音指令示例": "把温度调到 X 度 / 调高温度 / set temperature to X",
        "响应行为": "将空调温度设为用户指定值，语音播报'已设置温度为 X 度'",
        "异常处理": "温度超出范围(16-30°C)时提示'温度设置超出范围'"
    },
    {
        "功能ID": "HVAC-002",
        "功能名称": "空调开关",
        "语音指令示例": "打开空调 / 关闭空调 / turn on AC / turn off AC",
        "响应行为": "切换空调开关状态，语音播报'空调已打开/关闭'",
        "异常处理": "引擎熄火时空调自动关闭"
    },
])

# -- 媒体模块 --
sheets["媒体"] = pd.DataFrame([
    {
        "功能ID": "MEDIA-001",
        "功能名称": "音量调节",
        "语音指令示例": "声音大一点 / 音量调到 X / turn it up / volume down",
        "响应行为": "调整媒体音量，屏幕显示当前音量值",
        "异常处理": "静音状态下调节音量自动取消静音"
    },
    {
        "功能ID": "MEDIA-002",
        "功能名称": "播放音乐",
        "语音指令示例": "放周杰伦的歌 / 随便放点音乐 / play some jazz",
        "响应行为": "从音乐库检索并播放，语音播报'正在播放 XXX'",
        "异常处理": "未找到内容时播报'未找到相关音乐'"
    },
])

# -- 导航模块 --
sheets["导航"] = pd.DataFrame([
    {
        "功能ID": "NAV-001",
        "功能名称": "目的地导航",
        "语音指令示例": "导航去机场 / 带我回家 / navigate to X / take me to the office",
        "响应行为": "检索目的地并规划路线，语音播报预计到达时间",
        "异常处理": "未找到目的地时弹出列表让用户选择"
    },
])

# -- 车窗/座椅/电话 --
sheets["车窗"] = pd.DataFrame([
    {
        "功能ID": "WINDOW-001",
        "功能名称": "车窗控制",
        "语音指令示例": "打开车窗 / 关闭所有车窗 / open driver window",
        "响应行为": "控制指定车窗升降，语音播报'车窗已打开/关闭'",
        "异常处理": "行驶中禁止打开后排车窗(儿童锁开启时)"
    },
])

sheets["座椅"] = pd.DataFrame([
    {
        "功能ID": "SEAT-001",
        "功能名称": "座椅加热",
        "语音指令示例": "打开座椅加热 / turn on seat heating",
        "响应行为": "启动座椅加热，屏幕显示加热图标",
        "异常处理": "电池电量低于 15% 时禁用"
    },
])

sheets["电话"] = pd.DataFrame([
    {
        "功能ID": "PHONE-001",
        "功能名称": "拨打电话",
        "语音指令示例": "打电话给 X / 拨打 XXX / call mom",
        "响应行为": "从通讯录检索联系人并拨号，语音播报'正在呼叫 XXX'",
        "异常处理": "未连接手机时提示'请先连接蓝牙'"
    },
])

with pd.ExcelWriter("docs/交互文档_样例.xlsx", engine="openpyxl") as writer:
    for name, df in sheets.items():
        df.to_excel(writer, sheet_name=name, index=False)

print(f"✅ 样例交互文档已生成: docs/交互文档_样例.xlsx")
print(f"   共 {len(sheets)} 个模块, {sum(len(df) for df in sheets.values())} 条功能")
