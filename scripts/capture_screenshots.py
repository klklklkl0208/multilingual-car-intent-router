# -*- coding: utf-8 -*-
"""
Demo 截图脚本
=============
启动 Streamlit -> 用 Playwright 模拟操作 -> 截三张图存到 docs/screenshots/

用途: 给 README 顶部使用，让招聘官 30 秒看懂项目价值。
本脚本只在准备 README 资源时用一次，不参与正常运行。
"""

import asyncio
import os
import subprocess
import time
from pathlib import Path

from playwright.async_api import async_playwright

BASE_URL = "http://localhost:8599"
OUT_DIR = Path("docs/screenshots")
OUT_DIR.mkdir(parents=True, exist_ok=True)


async def capture():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome")  # 用系统 Chrome 跳过 Chromium 下载
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()
        await page.goto(BASE_URL, wait_until="networkidle")
        # 等 Streamlit 完成首屏渲染
        await page.wait_for_selector("text=多语种车载意图路由器", timeout=20000)
        await page.wait_for_timeout(1500)

        # ---- Tab 1: 实时路由 ----
        # 默认就在 Tab1，且输入框已预填示例。直接点"识别"。
        await page.get_by_role("button", name="识别").click()
        await page.wait_for_selector("text=识别功能", timeout=15000)
        await page.wait_for_timeout(800)
        await page.screenshot(path=str(OUT_DIR / "01_realtime_route.png"), full_page=True)
        print("✓ 01 realtime route")

        # ---- Tab 2: 质量看板 ----
        await page.get_by_role("tab", name="📊 质量看板").click()
        await page.wait_for_timeout(500)
        await page.get_by_role("button", name="▶️ 跑评测集").click()
        # 等汇总表渲染
        await page.wait_for_selector("text=汇总", timeout=60000)
        await page.wait_for_timeout(1500)
        await page.screenshot(path=str(OUT_DIR / "02_quality_dashboard.png"), full_page=True)
        print("✓ 02 quality dashboard")

        # ---- Tab 3: 功能集 ----
        await page.get_by_role("tab", name="📖 功能集").click()
        await page.wait_for_timeout(800)
        await page.screenshot(path=str(OUT_DIR / "03_intent_schema.png"), full_page=True)
        print("✓ 03 intent schema")

        await browser.close()


def main():
    # 先启动 Streamlit
    proc = subprocess.Popen(
        ["streamlit", "run", "app.py",
         "--server.headless", "true",
         "--server.port", "8599",
         "--browser.gatherUsageStats", "false"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        # 等服务起来
        for _ in range(30):
            time.sleep(1)
            try:
                import urllib.request
                urllib.request.urlopen(BASE_URL, timeout=1)
                break
            except Exception:
                continue
        asyncio.run(capture())
    finally:
        proc.terminate()
        proc.wait(timeout=5)


if __name__ == "__main__":
    main()
