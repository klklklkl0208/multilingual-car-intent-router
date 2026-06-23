# -*- coding: utf-8 -*-
"""
UI 样式配置 - 基于 UI/UX Pro Max 设计系统
===========================================
风格: AI-Native UI (对话式、极简、科技感)
配色: AI 紫 (#7C3AED) + 生成粉 (#EC4899)
字体: Space Grotesk + DM Sans
"""

# 导入 Google Fonts
FONT_IMPORT = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
"""

# AI-Native UI 样式系统
CUSTOM_CSS = """
<style>
/* Design System Variables */
:root {
    /* Colors - AI 紫 + 生成粉 */
    --color-primary: #7C3AED;
    --color-on-primary: #FFFFFF;
    --color-secondary: #6366F1;
    --color-accent: #EC4899;
    --color-background: #FAF5FF;
    --color-foreground: #0F172A;
    --color-muted: #F7F3FD;
    --color-border: #EFE7FC;
    --color-destructive: #DC2626;
    --color-ring: #7C3AED;

    /* Typography */
    --font-heading: 'Space Grotesk', sans-serif;
    --font-body: 'DM Sans', sans-serif;

    /* Spacing (4pt system) */
    --space-xs: 4px;
    --space-sm: 8px;
    --space-md: 16px;
    --space-lg: 24px;
    --space-xl: 32px;

    /* Effects */
    --radius: 12px;
    --shadow-sm: 0 2px 8px rgba(124, 58, 237, 0.12);
    --shadow-md: 0 4px 16px rgba(124, 58, 237, 0.16);
    --shadow-lg: 0 8px 24px rgba(124, 58, 237, 0.2);

    /* Animation */
    --duration-fast: 150ms;
    --duration-base: 250ms;
    --duration-slow: 350ms;
    --ease-smooth: cubic-bezier(0.4, 0, 0.2, 1);
}

/* Global Typography */
* {
    font-family: var(--font-body);
}

h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-heading);
    font-weight: 600;
    color: var(--color-foreground);
    letter-spacing: -0.02em;
}

/* App Background - Minimal Chrome */
.stApp {
    background: var(--color-background);
}

/* Sidebar - AI Conversational Style */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--color-primary) 0%, #5B21B6 100%);
    border-right: 1px solid var(--color-border);
}

section[data-testid="stSidebar"] * {
    color: var(--color-on-primary) !important;
}

section[data-testid="stSidebar"] .stMarkdown {
    color: var(--color-on-primary) !important;
}

section[data-testid="stSidebar"] h2 {
    color: var(--color-on-primary) !important;
}

/* Buttons - High Contrast CTA */
.stButton > button {
    background: linear-gradient(135deg, var(--color-accent) 0%, var(--color-primary) 100%);
    color: var(--color-on-primary);
    border: none;
    border-radius: var(--radius);
    padding: 0.75rem 1.5rem;
    font-family: var(--font-heading);
    font-weight: 600;
    font-size: 0.95rem;
    transition: all var(--duration-base) var(--ease-smooth);
    box-shadow: var(--shadow-md);
    cursor: pointer;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

.stButton > button:active {
    transform: translateY(0);
}

/* Tabs - Minimal Chrome */
.stTabs [data-baseweb="tab-list"] {
    gap: var(--space-sm);
    background: transparent;
    border-bottom: 2px solid var(--color-border);
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: var(--radius) var(--radius) 0 0;
    padding: var(--space-md) var(--space-lg);
    border: none;
    color: var(--color-foreground);
    font-family: var(--font-heading);
    font-weight: 500;
    transition: all var(--duration-fast) var(--ease-smooth);
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(180deg, var(--color-primary) 0%, var(--color-secondary) 100%);
    color: var(--color-on-primary);
    box-shadow: var(--shadow-sm);
}

/* Input Fields - Conversational Style */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    border: 2px solid var(--color-border);
    border-radius: var(--radius);
    padding: var(--space-md);
    font-family: var(--font-body);
    background: white;
    transition: all var(--duration-base) var(--ease-smooth);
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--color-primary);
    box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
    outline: none;
}

/* File Upload - AI Context Card Style */
.stFileUploader {
    background: white;
    border: 2px dashed var(--color-border);
    border-radius: var(--radius);
    padding: var(--space-lg);
    transition: all var(--duration-base) var(--ease-smooth);
}

.stFileUploader:hover {
    border-color: var(--color-primary);
    background: var(--color-muted);
}

/* Data Tables - Clean Presentation */
.stDataFrame {
    border-radius: var(--radius);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--color-border);
}

/* Metrics - Bold Display */
[data-testid="stMetricValue"] {
    font-size: 2.5rem;
    font-weight: 700;
    font-family: var(--font-heading);
    color: var(--color-primary);
}

/* Alert Messages - Context Cards */
.stAlert {
    border-radius: var(--radius);
    border: none;
    box-shadow: var(--shadow-sm);
    padding: var(--space-md) var(--space-lg);
}

.stInfo {
    background: linear-gradient(135deg, #EBF5FF 0%, #F0F9FF 100%);
    border-left: 4px solid var(--color-secondary);
}

.stSuccess {
    background: linear-gradient(135deg, #ECFDF5 0%, #F0FDF4 100%);
    border-left: 4px solid #10B981;
}

.stWarning {
    background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
    border-left: 4px solid #F59E0B;
}

.stError {
    background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
    border-left: 4px solid var(--color-destructive);
}

/* Divider - Subtle */
hr {
    border: none;
    height: 1px;
    background: var(--color-border);
    margin: var(--space-xl) 0;
}

/* Code Blocks */
code {
    background: var(--color-muted);
    color: var(--color-primary);
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 0.9em;
}

/* Expander - Context Card */
.streamlit-expanderHeader {
    background: white;
    border-radius: var(--radius);
    border: 1px solid var(--color-border);
    padding: var(--space-md);
    font-family: var(--font-heading);
    font-weight: 500;
    transition: all var(--duration-fast) var(--ease-smooth);
}

.streamlit-expanderHeader:hover {
    border-color: var(--color-primary);
    box-shadow: var(--shadow-sm);
}

/* Spinner - AI Typing Indicator Style */
.stSpinner > div {
    border-top-color: var(--color-accent) !important;
    border-right-color: var(--color-primary) !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--color-muted);
}

::-webkit-scrollbar-thumb {
    background: var(--color-border);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--color-primary);
}

/* Accessibility - Focus States */
button:focus-visible,
input:focus-visible,
textarea:focus-visible,
a:focus-visible {
    outline: 2px solid var(--color-ring);
    outline-offset: 2px;
}

/* Reduced Motion Support */
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

/* Responsive Typography */
@media (max-width: 768px) {
    h1 { font-size: 1.75rem; }
    h2 { font-size: 1.5rem; }
    h3 { font-size: 1.25rem; }
}

/* Dark Mode Support (if enabled) */
@media (prefers-color-scheme: dark) {
    :root {
        --color-background: #0F0A1A;
        --color-foreground: #F8FAFC;
        --color-muted: #1E1433;
        --color-border: #2D2047;
    }
}
</style>
"""


def apply_custom_style():
    """应用基于 UI/UX Pro Max 的 AI-Native 设计系统"""
    import streamlit as st
    st.markdown(FONT_IMPORT, unsafe_allow_html=True)
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
