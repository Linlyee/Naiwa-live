# -*- coding: utf-8 -*-
"""
抖音互动直播间 · 全功能 WebSocket & HTTP 核心桥接网关 (Port 12393)
集成 Antigravity 本地 Gemini 智能回复核 (gemini-3.5-flash-lite)
打通：
1. 本地直播网页 (http://localhost:8088/index.html) 的实时 WebSocket 联动
2. Antigravity 管理器本地代理 API (http://127.0.0.1:8045/v1/chat/completions)
3. 抖音弹幕智能问答、官方礼物动效与点歌系统
"""

import sys
import os
import re
import json
import asyncio
from typing import Set, Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import aiohttp
from loguru import logger

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

app = FastAPI(title="Douyin Live Bridge Gateway", version="2.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 活跃客户端连接池
connected_websockets: Set[WebSocket] = set()

# Antigravity 本地管理器 API 配置
ANTIGRAVITY_BASE_URL = os.environ.get("ANTIGRAVITY_PROXY_URL", "http://127.0.0.1:8045")
ANTIGRAVITY_API_KEY = os.environ.get("ANTIGRAVITY_API_KEY", "sk-your-antigravity-api-key")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")

# 官方主流常驻礼物别名兼容字典
GIFT_ALIASES = {
    '小心心': '小心心', '心心': '小心心', '爱心': '小心心', '心动': '小心心',
    '粉丝团灯牌': '粉丝团灯牌', '灯牌': '粉丝团灯牌', '粉丝团': '粉丝团灯牌', '加入粉丝团': '粉丝团灯牌',
    '鲜花': '鲜花', '玫瑰花': '鲜花', '玫瑰': '鲜花', '小花花': '鲜花',
    '棒棒糖': '棒棒糖',
    '荧光棒': '荧光棒', '打call': '荧光棒', '加油鸭': '荧光棒', '人气票': '荧光棒',
    '墨镜': '墨镜', '酷炫墨镜': '墨镜', '黑超': '墨镜', '好看': '墨镜', '你最好看': '墨镜',
    '比心': '比心', '手势比心': '比心', '为你点亮': '为你点亮', '点亮': '为你点亮',
    '热气球': '热气球', '气球': '热气球', '嘉年华': '热气球',
    '大啤酒': '鲜花', '啤酒': '鲜花', '保时捷': '热气球', '跑车': '热气球', '甜甜圈': '棒棒糖'
}

def parse_gift_text(content_str: str, default_user: str = "热心观众"):
    """
    智能解析弹幕/聊天流中的送礼文本
    支持格式示例：
    - "Linly 送给主播 心动到-1"
    - "Linly 送给主播 心动到-10"
    - "小明 送给主播 小心心 x5"
    - "送出 棒棒糖 x2"
    - "[送出 为你点亮 x1]"
    - "王五 送了 鲜花 10个"
    """
    t = content_str.strip()
    is_gift_indicator = any(kw in t for kw in ['送给主播', '送给', '送出', '送了', '赠送', '赠给']) or t.startswith('[')
    
    # 查找匹配的礼物（长词优先匹配）
    matched_gift = None
    sorted_keys = sorted(GIFT_ALIASES.keys(), key=lambda x: len(x), reverse=True)
    for g in sorted_keys:
        if g in t:
            matched_gift = GIFT_ALIASES[g]
            break
            
    if not matched_gift:
        return None
        
    # 如果有礼物词，但没有任何送礼动作词，且文本较长（如普通闲聊：“我比心心给你看”），排除误判
    if not is_gift_indicator and len(t) > len(matched_gift) + 4:
        return None
        
    # 提取送礼数量（支持 x1, *1, -1, 到-1, 1个）
    cnt = 1
    m_cnt = re.search(r'(?:[xX*×\-:]|到-?)\s*(\d+)', t) or re.search(r'(\d+)\s*(?:个|支|朵|束|份|把)', t)
    if m_cnt:
        try:
            cnt = max(1, int(m_cnt.group(1)))
        except Exception:
            cnt = 1
            
    # 提取送礼人
    user = default_user
    m_user = re.match(r'^(.*?)\s*(?:送给主播|送给|送出|送了|赠送)', t)
    if m_user:
        extracted_user = m_user.group(1).strip(' [【(（')
        if extracted_user and len(extracted_user) <= 25:
            user = extracted_user
            
    return user, matched_gift, cnt

async def broadcast_event(payload: Dict[str, Any]):
    """向所有连接的直播间前端广播事件"""
    if not connected_websockets:
        logger.warning(f"广播跳过（暂无前端页面连接）: {payload}")
        return
    
    msg_str = json.dumps(payload, ensure_ascii=False)
    dead_sockets = set()
    for ws in list(connected_websockets):
        try:
            await ws.send_text(msg_str)
        except Exception:
            dead_sockets.add(ws)
    
    for ws in dead_sockets:
        connected_websockets.discard(ws)
    
    logger.success(f"已向 {len(connected_websockets)} 个直播前端广播事件: {payload.get('type') or 'danmaku'} - {payload}")

def start_antigravity_tools_process():
    """在后台静默启动 antigravity-tools.exe 代理核"""
    import subprocess
    try:
        for d in os.listdir('D:/'):
            p = os.path.join('D:/', d, 'antigravity', 'Antigravity Tools', 'antigravity-tools.exe')
            if os.path.exists(p):
                logger.info(f"正在自动拉起 Antigravity Tools 后台核心: {p}")
                flags = subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                subprocess.Popen([p], cwd=os.path.dirname(p), creationflags=flags)
                return True
    except Exception as e:
        logger.warning(f"拉起 Antigravity Tools 异常: {e}")
    return False

async def ensure_gemini_proxy_running():
    """确保 Antigravity 管理器的代理服务处于开启状态"""
    try:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    f"{ANTIGRAVITY_BASE_URL}/api/proxy/status",
                    headers={"Authorization": f"Bearer {ANTIGRAVITY_API_KEY}"},
                    timeout=aiohttp.ClientTimeout(total=2)
                ) as resp:
                    if resp.status == 200:
                        st = await resp.json()
                        if not st.get("running"):
                            logger.info("Antigravity 代理处于关闭状态，正在自动启动...")
                            async with session.post(
                                f"{ANTIGRAVITY_BASE_URL}/api/proxy/start",
                                headers={"Authorization": f"Bearer {ANTIGRAVITY_API_KEY}", "Content-Type": "application/json"},
                                json={},
                                timeout=aiohttp.ClientTimeout(total=3)
                            ) as start_resp:
                                logger.info(f"Antigravity 代理启动结果: {start_resp.status}")
            except Exception as ex:
                logger.debug(f"8045 服务未就绪，自动拉起 antigravity-tools 进程: {ex}")
                if start_antigravity_tools_process():
                    await asyncio.sleep(2.5)
    except Exception as e:
        logger.warning(f"自动维持 Gemini 代理异常: {e}")

session_tokens_total: int = 0

async def ask_gemini_naiwa(user: str, message: str) -> tuple[str, int]:
    """调用 Antigravity 本地 Gemini 模型生成软萌奶娃回复，并返回回复文本及消耗的 Token"""
    global session_tokens_total
    await ensure_gemini_proxy_running()

    sys_prompt = (
        "你是抖音互动直播间的软萌小主播【奶娃】（三岁半）。自称奶娃，叫观众哥哥姐姐。"
        "性格天真烂漫、活泼软萌，喜欢用叠词（如饭饭、肚肚、水水、抱抱、duang~），语调甜甜的。"
        "现在你在直播间看弹幕跟观众互动。必须用奶娃的语气在1-2句话内甜甜地回复观众，字数在30字以内，一定要口语化、软萌、有爱心！"
    )

    payload = {
        "model": GEMINI_MODEL,
        "messages": [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": f"观众【{user}】发来弹幕说：“{message}”"}
        ],
        "temperature": 0.8,
        "max_tokens": 80
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{ANTIGRAVITY_BASE_URL}/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {ANTIGRAVITY_API_KEY}",
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status == 200:
                    res = await resp.json()
                    reply = res["choices"][0]["message"]["content"].strip()
                    usage = res.get("usage", {})
                    tokens = usage.get("total_tokens", len(reply) + len(message) + 40)
                    session_tokens_total += tokens
                    logger.success(f"🤖 Gemini ({GEMINI_MODEL}) 回复 [{user}]: {reply} | Token消耗: {tokens} (本场累计: {session_tokens_total})")
                    return reply, tokens
                else:
                    err = await resp.text()
                    logger.error(f"Gemini API 错误 {resp.status}: {err}")
                    return "", 0
    except Exception as e:
        logger.error(f"Gemini 生成异常: {e}")
        return "", 0

async def handle_llm_reply_task(user: str, danmaku: str):
    """异步任务：生成 Gemini 回复并推送给直播间前端"""
    t = danmaku.strip()
    # 仅过滤以“点歌”开头的指令或单纯动作指令，其他所有弹幕均自动智能回复
    if t.startswith('点歌') or t in ['蹦跳', '吐泡泡', '睡觉', '插队点歌']:
        return
    
    logger.info(f"正在为观众【{user}】的弹幕「{danmaku}」生成 Gemini AI 语音回复...")
    # 稍作等待，让观众弹幕先推上公屏
    await asyncio.sleep(0.3)
    reply, tokens = await ask_gemini_naiwa(user, danmaku)
    if reply:
        logger.success(f"已广播 Gemini AI 回复: {reply}")
        await broadcast_event({
            "type": "llm_reply",
            "user": user,
            "question": danmaku,
            "reply": reply,
            "tokens_used": tokens,
            "session_tokens": session_tokens_total
        })

@app.websocket("/client-ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_websockets.add(websocket)
    logger.info(f"直播前端已上线连接！当前连接总数: {len(connected_websockets)}")
    
    # 发送握手成功报文
    await websocket.send_text(json.dumps({
        "type": "connected",
        "message": "抖音互动直播核心网关连接成功！AI 智能回复已就绪。"
    }, ensure_ascii=False))

    try:
        while True:
            text = await websocket.receive_text()
            try:
                data = json.loads(text)
                logger.info(f"收到客户端消息: {data}")
                await broadcast_event(data)
            except json.JSONDecodeError:
                pass
    except WebSocketDisconnect:
        connected_websockets.discard(websocket)
        logger.info(f"客户端断开连接，当前剩余连接数: {len(connected_websockets)}")
    except Exception as e:
        connected_websockets.discard(websocket)
        logger.warning(f"WebSocket 异常断开: {e}")

@app.get("/")
async def index_status():
    return HTMLResponse(content=f"""
    <html>
        <head><title>抖音直播间桥接网关</title></head>
        <body style="font-family: sans-serif; padding: 30px; background: #121214; color: #fff;">
            <h2>🚀 抖音互动直播间 · 核心网关已启动 (Port 12393)</h2>
            <p>前端 WebSocket 连接状态: <b style="color: #38ef7d;">{len(connected_websockets)} 个活跃客户端连接</b></p>
            <p>Gemini AI 状态: <b style="color: #60a5fa;">已接入 Antigravity 管理器 ({GEMINI_MODEL})</b></p>
            <hr style="border-color: #333;" />
            <h3>📡 接口指南：</h3>
            <ul>
                <li><b>WebSocket 接口</b>: <code>ws://localhost:12393/client-ws</code> (已打通)</li>
                <li><b>发送送礼事件 (POST)</b>: <code>/api/gift</code> (JSON: <code>{{"user": "小可爱", "gift": "为你点亮", "count": 1}}</code>)</li>
                <li><b>发送弹幕事件 (POST)</b>: <code>/api/danmaku</code> (JSON: <code>{{"user": "观众", "danmaku": "奶娃你今天吃饱饭了吗？"}}</code>)</li>
                <li><b>测试直接 AI 对话 (POST)</b>: <code>/api/chat</code> (JSON: <code>{{"user": "观众", "message": "你好呀"}}</code>)</li>
                <li><b>适配各类抖音弹幕抓手 (POST)</b>: <code>/barrage</code> (兼容 BarrageGrab 格式)</li>
            </ul>
        </body>
    </html>
    """)

@app.post("/api/gift")
async def trigger_gift_api(req: Request):
    """供外部爬虫或测试工具调用的送礼 HTTP 接口"""
    data = await req.json()
    user = data.get("user") or "热心观众"
    gift = data.get("gift") or "小心心"
    count = int(data.get("count", 1))

    std_gift = GIFT_ALIASES.get(gift, gift)
    payload = {
        "type": "gift",
        "user": user,
        "gift": std_gift,
        "count": count
    }
    await broadcast_event(payload)
    return JSONResponse({"status": "success", "event": payload})

@app.post("/api/danmaku")
async def trigger_danmaku_api(req: Request):
    """供外部爬虫或测试工具调用的弹幕 HTTP 接口"""
    data = await req.json()
    user = data.get("user") or "热心观众"
    danmaku = data.get("danmaku") or data.get("text") or "奶娃今天开心吗？"

    # 先检查是否包含文本送礼指令
    parsed = parse_gift_text(str(danmaku), user)
    if parsed:
        g_user, g_gift, g_count = parsed
        payload = {
            "type": "gift",
            "user": g_user,
            "gift": g_gift,
            "count": g_count
        }
        await broadcast_event(payload)
        return JSONResponse({"status": "success", "event": payload, "parsed_as": "gift"})

    payload = {
        "type": "danmaku",
        "user": user,
        "danmaku": danmaku
    }
    # 1. 广播用户弹幕至公屏
    await broadcast_event(payload)
    
    # 2. 异步触发 Gemini AI 智能回复
    asyncio.create_task(handle_llm_reply_task(user, danmaku))
    
    return JSONResponse({"status": "success", "event": payload})

@app.post("/api/chat")
async def direct_chat_api(req: Request):
    """直接测试 Gemini 奶娃对话"""
    data = await req.json()
    user = data.get("user") or "观众"
    message = data.get("message") or data.get("text") or "你好呀奶娃"
    reply, tokens = await ask_gemini_naiwa(user, message)
    if reply:
        await broadcast_event({
            "type": "llm_reply",
            "user": user,
            "question": message,
            "reply": reply,
            "tokens_used": tokens,
            "session_tokens": session_tokens_total
        })
    return JSONResponse({"user": user, "message": message, "reply": reply, "tokens_used": tokens, "session_tokens": session_tokens_total})

@app.post("/api/stats/reset")
async def reset_stats_api():
    """开播数据清零接口"""
    global session_tokens_total
    session_tokens_total = 0
    await broadcast_event({
        "type": "reset_stats",
        "message": "开播数据已清零"
    })
    return JSONResponse({"status": "success", "session_tokens": 0})

@app.post("/api/reload")
async def reload_frontend_api():
    """通知所有直播前端页面热重载最新代码"""
    await broadcast_event({"type": "reload"})
    return JSONResponse({"status": "success", "message": "已向前端广播热重载指令"})

async def process_barrage_payload(data: dict):
    """通用弹幕/礼物/进房消息处理器 (同时兼容 BarrageGrab Webhook 与 WebSocket 格式)"""
    try:
        raw_type = data.get("Type") or data.get("MsgType") or data.get("type")
        # 兼容两种结构：平铺结构或包裹在 Data 字段中
        body = data.get("Data") if isinstance(data.get("Data"), dict) else data

        # 提取用户昵称
        user_info = body.get("User") or body.get("user") or {}
        if isinstance(user_info, dict):
            user = user_info.get("NickName") or user_info.get("Nickname") or user_info.get("name") or "热心观众"
        else:
            user = str(user_info) if user_info else "热心观众"

        content = body.get("Content") or body.get("content") or body.get("danmaku") or body.get("text")
        gift_info = body.get("Gift") if isinstance(body.get("Gift"), dict) else {}
        gift_name = body.get("GiftName") or body.get("gift_name") or body.get("gift") or gift_info.get("Name") or gift_info.get("name")

        # 1. 结构化原生礼物识别 (Type 5 或 Type 2 或 包含 GiftName)
        if gift_name or str(raw_type) in ["5", "2", "gift", "Gift"]:
            if gift_name:
                count = int(body.get("GiftCount") or body.get("Count") or body.get("count") or gift_info.get("Count") or 1)
                std_gift = GIFT_ALIASES.get(gift_name, gift_name)
                logger.success(f"[抓手送礼(原生)] 观众【{user}】送出【{std_gift} x{count}】")
                await broadcast_event({
                    "type": "gift",
                    "user": user,
                    "gift": std_gift,
                    "count": count
                })
                return

        # 2. 文本送礼识别 (针对聊天流/弹幕流推送的互动送礼，如 "Linly 送给主播 心动到-1")
        if content:
            content_str = str(content).strip()
            parsed = parse_gift_text(content_str, user)
            if parsed:
                g_user, g_gift, g_count = parsed
                logger.success(f"[抓手送礼(文本解析)] 观众【{g_user}】送出【{g_gift} x{g_count}】 (原消息: {content_str})")
                await broadcast_event({
                    "type": "gift",
                    "user": g_user,
                    "gift": g_gift,
                    "count": g_count
                })
                return

        # 3. 普通弹幕消息识别 (Type 3 或 Type 1 或 包含 Content)
        if content or str(raw_type) in ["3", "1", "chat", "danmaku"]:
            if content:
                content_str = str(content).strip()
                logger.info(f"[抓手弹幕] 观众【{user}】：{content_str}")
                await broadcast_event({
                    "type": "danmaku",
                    "user": user,
                    "danmaku": content_str
                })
                # 异步生成 Gemini 回复
                asyncio.create_task(handle_llm_reply_task(user, content_str))
                return

        # 4. 进房欢迎识别 (Type 1 且包含 MemberCount 或 Type 3)
        if str(raw_type) in ["1", "3"] and ("MemberCount" in body or "member_count" in body):
            logger.info(f"[抓手进房] 欢迎【{user}】进入直播间")
            await broadcast_event({
                "type": "welcome",
                "user": user
            })
            return

    except Exception as e:
        logger.error(f"处理弹幕抓手异常: {e}")

@app.post("/barrage")
async def barrage_grab_adapter(req: Request):
    """通用抖音弹幕抓手 (BarrageGrab / dy-barrage) 自动适配接口 (HTTP WebPush)"""
    try:
        data = await req.json()
        logger.info(f"收到弹幕抓手 Webhook 推送: {data}")
        await process_barrage_payload(data)
        return JSONResponse({"code": 0, "msg": "ok"})
    except Exception as e:
        logger.error(f"处理弹幕抓手 Webhook 异常: {e}")
        return JSONResponse({"code": 500, "error": str(e)})

async def barrage_grab_ws_listener():
    """后台静默守护协程：自动探测并直连 BarrageGrab 本地 WebSocket 服务 (ws://127.0.0.1:8888)"""
    import websockets
    logger.info("BarrageGrab WebSocket 自动探测守护已就绪 (目标: ws://127.0.0.1:8888)...")
    while True:
        try:
            async with websockets.connect("ws://127.0.0.1:8888", ping_interval=20) as ws:
                logger.success("★ [抓手直连成功] 已连接 BarrageGrab 8888 服务！真实弹幕/礼物通道已开启！")
                async for message in ws:
                    try:
                        data = json.loads(message)
                        await process_barrage_payload(data)
                    except Exception as err:
                        logger.debug(f"BarrageGrab 消息解析: {err}")
        except Exception:
            # 静默等待 BarrageGrab 打开，每 3 秒探活一次
            await asyncio.sleep(3)

@app.on_event("startup")
async def on_startup():
    asyncio.create_task(barrage_grab_ws_listener())

@app.get("/api/test/{action_name}")
async def quick_test(action_name: str):
    """浏览器地址栏快速测试各种礼物动作"""
    action_to_gift = {
        'blush': '小心心',
        'dengpai': '粉丝团灯牌',
        'rose': '鲜花',
        'belly_laugh': '棒棒糖',
        'praise': '荧光棒',
        'mojing': '墨镜',
        'vip_song': '比心',
        'balloon': '热气球'
    }
    gift = action_to_gift.get(action_name, action_name)
    await broadcast_event({
        "type": "gift",
        "user": f"测试小助手_{action_name}",
        "gift": gift,
        "count": 1
    })
    return JSONResponse({"message": f"已触发测试送礼: {gift}"})

if __name__ == "__main__":
    logger.info("正在启动抖音直播核心网关 (0.0.0.0:12393) · 已接入 Antigravity Gemini AI...")
    uvicorn.run(app, host="0.0.0.0", port=12393, log_level="info")
