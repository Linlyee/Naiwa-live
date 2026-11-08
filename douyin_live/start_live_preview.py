import http.server
import socketserver
import os
import sys
import webbrowser
import urllib.parse
import urllib.request
import hashlib
import subprocess
import json
import re
import random
import anyio
import base64
import uuid
import qqmusic_api
from qqmusic_api import Credential
from qqmusic_api.modules.song import SongFileInfo
from qqmusic_api.modules.login import QRLoginType, QRCodeLoginEvents

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PORT = 8088
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(DIRECTORY)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
CACHE_DIR = os.path.join(DIRECTORY, 'assets', 'tts_cache')
MUSIC_CACHE_DIR = os.path.join(DIRECTORY, 'assets', 'music_cache')
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(MUSIC_CACHE_DIR, exist_ok=True)

# 强制原唱过滤：坚决剔除一切翻唱、伴奏、Remix、DJ、慢放、片段等非原唱杂质
# 过滤非正统音源（伴奏、DJ、慢摇、变奏、剪辑片段等）
DISQUALIFY_PATTERNS = [
    r'伴奏', r'instrumental', r'remix', r'dj', r'慢摇', r'电音',
    r'纯音乐', r'片段', r'剪辑', r'降调', r'升调', r'变奏',
    r'烟嗓', r'戏腔', r'铃声', r'8d', r'加快', r'减速', r'消音',
    r'卡拉ok', r'ktv', r'karaoke', r'粗口版'
]

# 严格过滤翻唱关键字（仅在未指定歌手时启用）
COVER_PATTERNS = [
    r'翻唱', r'cover', r'翻', r'女生版', r'男声版', r'童声版',
    r'热播版', r'live合唱', r'翻自'
]

# 权威原唱对照映射表（保障未指定歌手时 100% 锁定官方原唱）
CANONICAL_ORIGINALS = {
    'hello': 'Adele',
    'rolling in the deep': 'Adele',
    'someone like you': 'Adele',
    'easy on me': 'Adele',
    '晴天': '周杰伦',
    '七里香': '周杰伦',
    '稻香': '周杰伦',
    '青花瓷': '周杰伦',
    '夜曲': '周杰伦',
    '告白气球': '周杰伦',
    '花海': '周杰伦',
    '枫': '周杰伦',
    '一路向北': '周杰伦',
    '安静': '周杰伦',
    '不能说的秘密': '周杰伦',
    '孤勇者': '陈奕迅',
    '富士山下': '陈奕迅',
    '爱情转移': '陈奕迅',
    '十年': '陈奕迅',
    '浮夸': '陈奕迅',
    '好久不见': '陈奕迅',
    '红豆': '王菲',
    '匆匆那年': '王菲',
    '传奇': '王菲',
    '乌梅子酱': '李荣浩',
    '年少有为': '李荣浩',
    '李白': '李荣浩',
    '模特': '李荣浩',
    '老街': '李荣浩',
    '戒烟': '李荣浩',
    '起风了': '买辣椒也用券',
    '大鱼': '周深',
    '消愁': '毛不易',
    '像我这样的人': '毛不易',
    '平凡的一天': '毛不易',
    '不染': '毛不易',
    '泡沫': '邓紫棋',
    '光年之外': '邓紫棋',
    '来自天堂的魔鬼': '邓紫棋',
    '倒数': '邓紫棋',
    '句号': '邓紫棋',
    '多远都要在一起': '邓紫棋',
    '我的秘密': '邓紫棋',
    '演员': '薛之谦',
    '认真的雪': '薛之谦',
    '绅士': '薛之谦',
    '方圆几里': '薛之谦',
    '体面': '于文文',
    '后来': '刘若英',
    '成全': '刘若英',
    '慢慢喜欢你': '莫文蔚',
    '阴天': '莫文蔚',
    '盛夏的果实': '莫文蔚',
    '红色高跟鞋': '蔡健雅',
    '达尔文': '蔡健雅',
    '江南': '林俊杰',
    '一千年以后': '林俊杰',
    '修炼爱情': '林俊杰',
    '可惜没如果': '林俊杰',
    '不为谁而作的歌': '林俊杰',
    'Shape of You': 'Ed Sheeran',
    'Perfect': 'Ed Sheeran',
    'Bad Habits': 'Ed Sheeran',
    'See You Again': 'Wiz Khalifa',
    'Faded': 'Alan Walker',
    'Stay': 'The Kid LAROI',
    'As It Was': 'Harry Styles'
}

COMMON_SINGERS = {
    '周杰伦', '陈奕迅', '林俊杰', '周深', '毛不易', '薛之谦', '李荣浩', '邓紫棋',
    '王菲', '张学友', '刘德华', '张国荣', '孙燕姿', '梁静茹', '蔡依林', '田馥甄',
    '莫文蔚', '张韶涵', '杨宗纬', '萧敬腾', '汪苏泷', '许嵩', '陶喆', '王力宏',
    '华晨宇', '张杰', '朴树', '李健', '郁可唯', '买辣椒也用券', '单依纯', '周笔畅',
    'adele', 'taylor swift', 'ed sheeran', 'justin bieber', 'rihanna', 'bruno mars',
    'coldplay', 'maroon 5', 'billie eilish', 'charlie puth', 'katy perry', 'sia',
    '刘若英', '于文文', '蔡健雅', '五月天', '苏打绿', '逃跑计划', '新裤子'
}

def parse_song_and_artist(raw_kw):
    """
    点歌解析器：
    规则：默认原唱，除非硬在歌名后面备注歌手
    返回: (song_name, target_artist, is_user_specified)
    """
    s = raw_kw.strip()
    
    # 1. 括号语法：起风了(周深) 或 晴天（蔡依林）
    m = re.search(r'[\(（]([^\)）]+)[\)）]', s)
    if m:
        candidate_artist = m.group(1).strip()
        song_part = re.sub(r'[\(（][^\)）]+[\)）]', '', s).strip()
        if song_part and candidate_artist:
            return song_part, candidate_artist, True

    # 2. 分隔符 / 空格切割：起风了 周深 或 周杰伦 晴天
    parts = re.split(r'[\-\_\/\—\～\~\|\s]+', s)
    if len(parts) >= 2:
        p0, p1 = parts[0].strip(), parts[1].strip()
        if p0.lower() in [x.lower() for x in COMMON_SINGERS]:
            return p1, p0, True
        else:
            return p0, p1, True

    # 3. 单纯歌名（未备注歌手）：默认原唱
    song_name = s
    canonical = None
    for k, v in CANONICAL_ORIGINALS.items():
        if k.lower() == song_name.lower():
            canonical = v
            break
    return song_name, canonical, False

def search_kuwo_strict(song_name, target_artist=None, is_specified=False):
    try:
        query = f"{song_name} {target_artist}" if target_artist else song_name
        url = f"http://search.kuwo.cn/r.s?client=kt&all={urllib.parse.quote(query)}&pn=0&rn=15&vipver=1&ft=music&encoding=utf8&rformat=json"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=4) as resp:
            text = resp.read().decode('utf-8', errors='ignore')
        data = json.loads(text.replace("'", '"'))
        abslist = data.get('abslist', [])
        if not abslist:
            return None

        # 未硬指定歌手时，若无预设则取首个结果歌手作为权威参考
        canonical_singer = target_artist or abslist[0].get('ARTIST', '').replace('&nbsp;', ' ').strip()

        for s in abslist:
            sname = s.get('SONGNAME', '').replace('&nbsp;', ' ').strip()
            singer = s.get('ARTIST', '').replace('&nbsp;', ' ').strip()
            rid = s.get('MUSICRID', '').replace('MUSIC_', '').strip()
            if not rid:
                continue

            comb = f"{sname} {singer}".lower()
            if any(re.search(p, comb, re.IGNORECASE) for p in DISQUALIFY_PATTERNS):
                continue

            if not is_specified:
                # 默认原唱模式：必须杜绝翻唱
                if any(re.search(p, comb, re.IGNORECASE) for p in COVER_PATTERNS):
                    continue
                if canonical_singer and (canonical_singer.lower() not in singer.lower() and singer.lower() not in canonical_singer.lower()):
                    continue
            else:
                # 用户硬在歌名后备注了歌手：必须严格命中该歌手
                if target_artist and (target_artist.lower() not in singer.lower() and singer.lower() not in target_artist.lower()):
                    continue

            p_url = f"http://antiserver.kuwo.cn/anti.s?type=convert_url&rid={rid}&format=mp3&response=url"
            with urllib.request.urlopen(urllib.request.Request(p_url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=3) as p:
                real_url = p.read().decode().strip()
                if real_url.startswith('http'):
                    return {
                        'success': True,
                        'title': sname,
                        'artist': singer,
                        'url': real_url,
                        'is_original': not is_specified,
                        'mode': f"指定歌手 · {singer}" if is_specified else "官方原唱母带",
                        'engine': 'Kuwo Master'
                    }
    except Exception:
        pass
    return None

def search_kugou_strict(song_name, target_artist=None, is_specified=False):
    try:
        query = f"{song_name} {target_artist}" if target_artist else song_name
        url = f"http://mobilecdn.kugou.com/api/v3/search/song?format=json&keyword={urllib.parse.quote(query)}&page=1&pagesize=20"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        info = data.get('data', {}).get('info', [])
        if not info:
            return None

        canonical_singer = target_artist or info[0].get('singername', '').strip()

        for item in info:
            sname = item.get('songname', '').strip()
            singer = item.get('singername', '').strip()
            dur = item.get('duration', 0)
            h = item.get('hash', '')
            if not h or dur < 120:
                continue

            comb = f"{sname} {singer}".lower()
            if any(re.search(p, comb, re.IGNORECASE) for p in DISQUALIFY_PATTERNS):
                continue

            if not is_specified:
                if any(re.search(p, comb, re.IGNORECASE) for p in COVER_PATTERNS):
                    continue
                if canonical_singer and (canonical_singer.lower() not in singer.lower() and singer.lower() not in canonical_singer.lower()):
                    continue
            else:
                if target_artist and (target_artist.lower() not in singer.lower() and singer.lower() not in target_artist.lower()):
                    continue

            p_url = f"https://m.kugou.com/app/i/getSongInfo.php?cmd=playInfo&hash={h}"
            with urllib.request.urlopen(urllib.request.Request(p_url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=3) as p:
                pdata = json.loads(p.read().decode('utf-8'))
                # 严格拦截所有需要付费、VIP、以及截断试听片段
                if pdata.get('status') == 0 or '付费' in str(pdata) or 'vip' in str(pdata).lower():
                    continue
                if dur < 100: # 剔除 30s/60s 试听片段，只取全长完整版
                    continue
                song_url = pdata.get('url') or (pdata.get('backup_url') and pdata.get('backup_url')[0])
                if song_url and song_url.startswith('http'):
                    return {
                        'success': True,
                        'title': sname,
                        'artist': singer,
                        'url': song_url,
                        'duration': dur,
                        'is_original': not is_specified,
                        'mode': f"指定歌手 · {singer}" if is_specified else "官方原唱母带",
                        'engine': 'KuGou Free Master'
                    }
    except Exception:
        pass
    return None


QR_SESSIONS = {}

def get_qqmusic_credential():
    for p in [
        os.path.join(DIRECTORY, "qqmusic_credential.json"),
        os.path.join(os.path.dirname(DIRECTORY), "qqmusic_credential.json")
    ]:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    cred = Credential.model_validate_json(f.read())
                    if not cred.is_expired():
                        return cred
            except Exception as e:
                print("[QQMusic Credential Error]", e)
    return None

def search_qqmusic_strict(song_name, target_artist=None, is_specified=False):
    cred = get_qqmusic_credential()
    query = f"{song_name} {target_artist}".strip() if target_artist else song_name

    async def _do():
        async with qqmusic_api.Client(credential=cred) as client:
            res = await client.search.search_by_type(query)
            if not res or not res.song:
                return None
            
            canonical_singer = target_artist or (res.song[0].singer[0].name if res.song[0].singer else "")
            
            for s in res.song:
                sname = s.name.strip()
                singers = [sg.name.strip() for sg in s.singer]
                singer_str = "/".join(singers)
                
                comb = f"{sname} {singer_str}".lower()
                if any(re.search(p, comb, re.IGNORECASE) for p in DISQUALIFY_PATTERNS):
                    continue
                
                if not is_specified:
                    # 默认原唱模式：必须杜绝翻唱
                    if any(re.search(p, comb, re.IGNORECASE) for p in COVER_PATTERNS):
                        continue
                    if canonical_singer and not any(canonical_singer.lower() in sg.lower() or sg.lower() in canonical_singer.lower() for sg in singers):
                        continue
                else:
                    # 用户指定了歌手：必须严格匹配该歌手
                    if target_artist and not any(target_artist.lower() in sg.lower() or sg.lower() in target_artist.lower() for sg in singers):
                        continue
                
                media_mid = s.file.media_mid if (s.file and s.file.media_mid) else s.mid
                sinfo = SongFileInfo(mid=s.mid, media_mid=media_mid)
                try:
                    urls_res = await client.song.get_song_urls([sinfo])
                    if urls_res and urls_res.data:
                        item = urls_res.data[0]
                        if item.purl:
                            full_url = f"https://isure6.stream.qqmusic.qq.com/{item.purl}"
                            return {
                                "success": True,
                                "title": sname,
                                "artist": singer_str,
                                "url": full_url,
                                "duration": s.interval,
                                "is_original": not is_specified,
                                "mode": f"指定歌手 · {singer_str}" if is_specified else "QQ音乐官方原唱母带",
                                "engine": "QQ Music VIP" if (cred and not cred.is_expired()) else "QQ Music"
                            }
                except Exception as e:
                    print("[QQMusic Url Extract Error]", e)
            return None

    try:
        return anyio.run(_do)
    except Exception as e:
        print("[QQMusic Search Exception]", e)
        return None
def search_mandatory_original(keyword):
    """
    点歌引擎：优先使用 QQ 音乐 (支持用户绿钻/VIP账号原唱母带)
    """
    kw = keyword.strip()
    if not kw:
        return None

    song_name, target_artist, is_specified = parse_song_and_artist(kw)

    # 1. 第一优先级：QQ 音乐 (支持用户 VIP 完整原唱母带与海量曲库)
    res = search_qqmusic_strict(song_name, target_artist, is_specified)
    if res and res.get('success'):
        return res

    # 2. 备选：Kuwo 母带库
    res = search_kuwo_strict(song_name, target_artist, is_specified)
    if res and res.get('success'):
        return res

    # 3. 备选：KuGou 免费曲库
    res = search_kugou_strict(song_name, target_artist, is_specified)
    if res and res.get('success'):
        return res

    # 4. 容错重试：如果指定歌手未搜到，回退为纯歌名搜官方原唱
    if is_specified:
        res = search_qqmusic_strict(song_name, target_artist=None, is_specified=False)
        if res and res.get('success'):
            return res
        res = search_kuwo_strict(song_name, target_artist=None, is_specified=False)
        if res and res.get('success'):
            return res
        res = search_kugou_strict(song_name, target_artist=None, is_specified=False)
        if res and res.get('success'):
            return res

    return None


# 华语大热门流行金曲池（空闲时自动高保真随机轮播，绝不放软糖华尔兹）
HOT_POPULAR_SONGS = [
    ("晴天", "周杰伦"),
    ("告白气球", "周杰伦"),
    ("稻香", "周杰伦"),
    ("七里香", "周杰伦"),
    ("青花瓷", "周杰伦"),
    ("花海", "周杰伦"),
    ("一路向北", "周杰伦"),
    ("起风了", "买辣椒也用券"),
    ("孤勇者", "陈奕迅"),
    ("爱情转移", "陈奕迅"),
    ("富士山下", "陈奕迅"),
    ("十年", "陈奕迅"),
    ("大鱼", "周深"),
    ("乌梅子酱", "李荣浩"),
    ("年少有为", "李荣浩"),
    ("李白", "李荣浩"),
    ("消愁", "毛不易"),
    ("像我这样的人", "毛不易"),
    ("光年之外", "邓紫棋"),
    ("来自天堂的魔鬼", "邓紫棋"),
    ("泡沫", "邓紫棋"),
    ("倒数", "邓紫棋"),
    ("演员", "薛之谦"),
    ("绅士", "薛之谦"),
    ("认真的雪", "薛之谦"),
    ("红色高跟鞋", "蔡健雅"),
    ("后来", "刘若英"),
    ("成全", "刘若英"),
    ("慢慢喜欢你", "莫文蔚"),
    ("阴天", "莫文蔚"),
    ("Hello", "Adele"),
    ("Rolling in the Deep", "Adele"),
    ("Someone Like You", "Adele"),
    ("Shape of You", "Ed Sheeran"),
    ("Perfect", "Ed Sheeran")
]

HOT_SONG_CACHE = {}

def get_random_hot_song():
    """获取全网大热门流行歌曲原唱完整版直链"""
    shuffled = list(HOT_POPULAR_SONGS)
    random.shuffle(shuffled)
    for s, a in shuffled:
        cache_key = f"{s} {a}"
        if cache_key in HOT_SONG_CACHE:
            return HOT_SONG_CACHE[cache_key]
        
        # 优先使用爬虫无损库获取
        res = search_kuwo_strict(s, target_artist=a, is_specified=False)
        if res and res.get('url'):
            HOT_SONG_CACHE[cache_key] = res
            return res
        
        res = search_kugou_strict(s, target_artist=a, is_specified=False)
        if res and res.get('url'):
            HOT_SONG_CACHE[cache_key] = res
            return res

    return None

class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        
        # 1. 严格原唱点歌检索接口
        if parsed.path == '/api/random_hot_song':
            result = get_random_hot_song()
            if not result:
                result = {
                    'success': True,
                    'title': '晴天',
                    'artist': '周杰伦',
                    'url': 'https://kw-bj.kuwo.cn/d89888ee0bbdd24e8d9ed99825e01cb4/6aed91d8/nf/resource/n1/69/32/588957081.mp3',
                    'is_original': True,
                    'is_hot_rotation': True
                }
            resp_body = json.dumps(result, ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(resp_body)))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(resp_body)
            return

        if parsed.path == '/api/qqmusic_status':
            cred = get_qqmusic_credential()
            status = {
                'logged_in': cred is not None,
                'is_expired': cred.is_expired() if cred else True,
                'musicid': cred.str_musicid if cred else '',
                'login_type': getattr(cred, 'login_type', '') if cred else ''
            }
            resp_body = json.dumps(status, ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(resp_body)
            return
        
        if parsed.path == '/api/qqmusic_qr':
            query = urllib.parse.parse_qs(parsed.query)
            qtype = query.get('type', ['wx'])[0].lower()
            login_type = QRLoginType.WX if qtype == 'wx' else QRLoginType.QQ
            
            async def _get_qr():
                async with qqmusic_api.Client() as client:
                    return await client.login.get_qrcode(login_type)
            
            try:
                qr = anyio.run(_get_qr)
                session_id = str(uuid.uuid4())
                QR_SESSIONS[session_id] = qr
                b64 = base64.b64encode(qr.data).decode('utf-8')
                result = {
                    'success': True,
                    'session_id': session_id,
                    'type': qtype,
                    'image': f"data:{qr.mimetype};base64,{b64}"
                }
            except Exception as e:
                result = {'success': False, 'error': str(e)}
        
            resp_body = json.dumps(result, ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(resp_body)
            return
        
        if parsed.path == '/api/qqmusic_check_qr':
            query = urllib.parse.parse_qs(parsed.query)
            session_id = query.get('session_id', [''])[0]
            qr = QR_SESSIONS.get(session_id)
            if not qr:
                result = {'status': 'expired', 'msg': '会话已过期，请重新获取二维码'}
            else:
                async def _check():
                    async with qqmusic_api.Client() as client:
                        return await client.login.check_qrcode(qr)
                try:
                    res = anyio.run(_check)
                    if res.event == QRCodeLoginEvents.DONE:
                        cred = res.credential
                        save_p = os.path.join(os.path.dirname(DIRECTORY), 'qqmusic_credential.json')
                        with open(save_p, 'w', encoding='utf-8') as f:
                            f.write(cred.model_dump_json())
                        with open(os.path.join(DIRECTORY, 'qqmusic_credential.json'), 'w', encoding='utf-8') as f:
                            f.write(cred.model_dump_json())
                        QR_SESSIONS.pop(session_id, None)
                        result = {'status': 'done', 'msg': 'VIP 会员登录成功！专属曲库已激活！'}
                    elif res.event == QRCodeLoginEvents.CONF:
                        result = {'status': 'scanned', 'msg': '已扫码，请在手机上点击确认授权登录'}
                    elif res.event == QRCodeLoginEvents.SCAN:
                        result = {'status': 'waiting', 'msg': '请使用手机微信/QQ扫码'}
                    elif res.event == QRCodeLoginEvents.TIMEOUT:
                        QR_SESSIONS.pop(session_id, None)
                        result = {'status': 'timeout', 'msg': '二维码已过期，请刷新'}
                    elif res.event == QRCodeLoginEvents.REFUSE:
                        QR_SESSIONS.pop(session_id, None)
                        result = {'status': 'refused', 'msg': '手机端已拒绝授权'}
                    else:
                        result = {'status': 'waiting', 'msg': '等待扫码中...'}
                except Exception as e:
                    result = {'status': 'error', 'msg': str(e)}
        
            resp_body = json.dumps(result, ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(resp_body)
            return
        
        if parsed.path == '/api/music_search':
            query = urllib.parse.parse_qs(parsed.query)
            kw = query.get('keyword', [''])[0].strip()
            if not kw:
                self.send_error(400, "Missing keyword parameter")
                return
            
            result = search_mandatory_original(kw)
            if not result:
                result = {
                    'success': False,
                    'error': f'未找到符合【强制原唱】条件的《{kw}》音源，已为您自动过滤掉非原唱翻唱与改编',
                    'title': kw,
                    'artist': '官方伴奏'
                }
            
            resp_body = json.dumps(result, ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(resp_body)))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(resp_body)
            return

        # 2. 实时奶娃 TTS 语音生成接口 (极速直出 + 100% 坚固智能回退，杜绝无声)
        if parsed.path == '/api/tts':
            query = urllib.parse.parse_qs(parsed.query)
            text = query.get('text', [''])[0].strip()
            if not text:
                text = "奶娃在呢"

            text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
            out_wav = os.path.join(CACHE_DIR, f"{text_hash}.mp3")

            # 1. 若无缓存，优先进程内直接调用 SiliconFlow 毫秒级生成 MP3
            if not os.path.exists(out_wav) or os.path.getsize(out_wav) < 100:
                try:
                    from single_tts import generate_speech
                    ok = generate_speech(text, out_wav, timeout=8)
                    if ok:
                        print(f"[TTS Success] In-process generated: {out_wav} ({os.path.getsize(out_wav)} bytes)")
                    else:
                        print(f"[TTS Warning] In-process failed, fallback needed for: {text}")
                except Exception as ex:
                    print(f"[TTS Exception] {ex}")

            # 2. 决定最终输出音频 (若合成成功则播放合成音；若网络慢/失败则无缝回退官方原声切片，确保绝对有声音)
            audio_file_to_serve = None
            if os.path.exists(out_wav) and os.path.getsize(out_wav) > 100:
                audio_file_to_serve = out_wav
            else:
                t_lower = text.lower()
                voice_dir = os.path.join(DIRECTORY, 'assets', 'voice', 'nailong_official')
                if any(k in t_lower for k in ['吃', '饭', '饿', '饱']):
                    audio_file_to_serve = os.path.join(voice_dir, 'hungry.mp3')
                elif any(k in t_lower for k in ['肚', '胖', '帅', '酷', '美', '夸']):
                    audio_file_to_serve = os.path.join(voice_dir, 'belly.mp3')
                elif any(k in t_lower for k in ['跳', '666', '赢', '棒', '赞']):
                    audio_file_to_serve = os.path.join(voice_dir, 'boing.mp3')
                elif any(k in t_lower for k in ['怕', '吓', '坏', '哭']):
                    audio_file_to_serve = os.path.join(voice_dir, 'shiver.mp3')
                else:
                    audio_file_to_serve = os.path.join(voice_dir, 'intro.mp3')

                if not os.path.exists(audio_file_to_serve):
                    audio_file_to_serve = os.path.join(DIRECTORY, 'assets', 'voice', 'intro.mp3')

            try:
                with open(audio_file_to_serve, 'rb') as f:
                    data = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'audio/mpeg')
                self.send_header('Content-Length', str(len(data)))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Cache-Control', 'public, max-age=86400')
                self.end_headers()
                self.wfile.write(data)
                return
            except Exception as e:
                print(f"[Serve Audio Error] {e}")
                return

        super().do_GET()

def run():
    os.chdir(DIRECTORY)
    with ThreadingHTTPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}/index.html"
        print("=" * 60)
        print("[OK] Douyin AI Live Room Started with Mandatory Original Singer Jukebox!")
        print(f"Browser URL: {url}")
        print("=" * 60)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")

if __name__ == '__main__':
    run()
