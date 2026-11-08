import asyncio
from playwright.async_api import async_playwright
import json

target_url = "https://v.douyin.com/_kOP85GOIr4/"

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        captured = []
        async def on_resp(resp):
            u = resp.url
            ct = resp.headers.get("content-type", "")
            if "audio" in ct or "video" in ct or "douyinvod" in u:
                captured.append({"url": u, "ct": ct, "status": resp.status})

        page.on("response", on_resp)
        await page.goto(target_url, wait_until="domcontentloaded")
        await asyncio.sleep(5)

        # Get audio and video element details from page
        media_info = await page.evaluate('''() => {
            const res = [];
            document.querySelectorAll('video, audio').forEach(el => {
                res.push({
                    tag: el.tagName,
                    src: el.src || el.currentSrc,
                    duration: el.duration,
                    paused: el.paused,
                    muted: el.muted,
                    volume: el.volume
                });
            });
            // Also look for window._SSR_DATA or render_data
            let title = document.title;
            return { elements: res, title: title };
        }''')
        print("Page media info:", json.dumps(media_info, ensure_ascii=False))

        # Also get all network requests captured
        print("Captured responses:", len(captured))
        for c in captured:
            print(c)

        # If audio element or audio response found, fetch it inside browser context!
        # Because inside browser context, cookies/headers are valid!
        for c in captured:
            if "douyinvod" in c["url"]:
                # Fetch buffer using page.evaluate fetch
                data_b64 = await page.evaluate('''async (url) => {
                    const r = await fetch(url);
                    const buf = await r.arrayBuffer();
                    let binary = '';
                    const bytes = new Uint8Array(buf);
                    const len = bytes.byteLength;
                    for (let i = 0; i < len; i++) {
                        binary += String.fromCharCode(bytes[i]);
                    }
                    return btoa(binary);
                }''', c["url"])
                import base64
                data = base64.b64decode(data_b64)
                fn = f"stream_{len(data)}.bin"
                with open(fn, "wb") as f:
                    f.write(data)
                print(f"Downloaded {fn} ({len(data)} bytes)")

        await browser.close()

asyncio.run(run())
