# -*- coding: utf-8 -*-
"""
现代图标系统 - Lucide Icons
===========================
使用 SVG 矢量图标替代 emoji,支持主题色自定义
"""

def get_icon_svg(name, size=24, color="currentColor", stroke_width=2):
    """
    获取 Lucide 风格的 SVG 图标

    Args:
        name: 图标名称
        size: 尺寸(px)
        color: 颜色(支持 CSS 颜色值)
        stroke_width: 描边粗细
    """
    icons = {
        # 主图标 - 闪电/能量
        "zap": f'''
            <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24"
                 fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
            </svg>
        ''',

        # 实时路由 - 活动/脉冲
        "activity": f'''
            <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24"
                 fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
            </svg>
        ''',

        # 质量看板 - 柱状图
        "bar-chart": f'''
            <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24"
                 fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="20" x2="12" y2="10"/>
                <line x1="18" y1="20" x2="18" y2="4"/>
                <line x1="6" y1="20" x2="6" y2="16"/>
            </svg>
        ''',

        # 功能集 - 靶心/目标
        "target": f'''
            <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24"
                 fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/>
                <circle cx="12" cy="12" r="6"/>
                <circle cx="12" cy="12" r="2"/>
            </svg>
        ''',

        # 交互文档查询 - 搜索
        "search": f'''
            <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24"
                 fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"/>
                <path d="m21 21-4.35-4.35"/>
            </svg>
        ''',

        # 设置 - 齿轮
        "settings": f'''
            <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24"
                 fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="3"/>
                <path d="M12 1v6m0 6v6m5.196-15.196l-4.243 4.243m-6.364 0l4.243 4.243m4.243 4.243l-4.243 4.243m-6.364 0l4.243-4.243"/>
            </svg>
        ''',

        # 查询按钮 - 星星/魔法
        "sparkles": f'''
            <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24"
                 fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
                <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>
                <path d="M5 3v4"/>
                <path d="M19 17v4"/>
                <path d="M3 5h4"/>
                <path d="M17 19h4"/>
            </svg>
        ''',

        # CPU/处理器 - 备选主图标
        "cpu": f'''
            <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24"
                 fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
                <rect x="4" y="4" width="16" height="16" rx="2"/>
                <rect x="9" y="9" width="6" height="6"/>
                <path d="M15 2v2m0 16v2M2 15h2m16 0h2M2 9h2m16 0h2M9 2v2m0 16v2"/>
            </svg>
        ''',

        # 大脑 - AI 智能
        "brain": f'''
            <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24"
                 fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
                <path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 1.98-3A2.5 2.5 0 0 1 9.5 2Z"/>
                <path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-1.98-3A2.5 2.5 0 0 0 14.5 2Z"/>
            </svg>
        ''',
    }

    return icons.get(name, icons["zap"])  # 默认返回闪电图标


def icon_html(name, size=20, color="#7C3AED", inline=True):
    """
    生成可直接嵌入 Streamlit 的图标 HTML

    Args:
        name: 图标名称
        size: 尺寸
        color: 颜色
        inline: 是否内联显示
    """
    svg = get_icon_svg(name, size, color)
    display = "inline-block" if inline else "block"
    return f'<span style="display: {display}; vertical-align: middle; margin-right: 8px;">{svg}</span>'
