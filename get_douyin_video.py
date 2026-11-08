import asyncio
from playwright.async_api import async_playwright
import urllib.request
import os

target_url = "https://v.douyin.com/_kOP85GOIr4/"
media_urls = []

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        async def handle_response(response):
            u = response.url
            ct = response.headers.get("content-type", "")
            if "video" in ct or "douyinvod" in u or ".mp4" in u or "bytevc" in u:
                print(f"[Captured Media] URL: {u[:100]} | Type: {ct}")
                media_urls.append(u)

        page.on("response", handle_response)

        print(f"Navigating to {target_url}...")
        try:
            await page.goto(target_url, wait_until="networkidle", timeout=20000)
        except Exception as e:
            print("Navigation finished/timeout:", e)

        await asyncio.sleep(4)

        video_src = await page.evaluate('''() => {
            const v = document.querySelector('video');
            return v ? (v.src || (v.querySelector('source') ? v.querySelector('source').src : null)) : null;
        }''')
        if video_src:
            print("DOM Video src:", video_src[:100])
            media_urls.append(video_src)

        await browser.close()

asyncio.run(run())

if media_urls:
    print(f"Found {len(media_urls)} media URLs. Downloading best one...")
    chosen = media_urls[0]
    out_path = "douyin_laugh_belly_leak.mp4"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.douyin.com/"
    }
    req = urllib.request.Request(chosen, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            with open(out_path, "wb") as f:
                f.write(data)
            print(f"Successfully downloaded {out_path} ({len(data)} bytes)!")
    except Exception as e:
        print("Download error:", e)
else:
    print("No media URL captured!")
