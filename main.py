import asyncio
import requests
from api.auth_module import Authenticator
from getrollcall import wait_for_rollcall
from sendRadar import answer_rollcall_Radar
from sendNum import answer_rollcall_number_async

async def main():
    print("🔐 Logging in...")
    auth = Authenticator()
    session = auth.perform_auth()

    session.headers.update({
        'sec-ch-ua-platform': '"Android"',
        'accept-language': 'zh-Hant',
        'sec-ch-ua': '"Android WebView";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?1',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Linux; Android 14; SM-A146P Build/UP1A.231005.007; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/135.0.7049.111 Mobile Safari/537.36 TronClass/googleplay',
        'accept': 'application/json, text/plain, */*',
        'origin': 'http://localhost',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'priority': 'u=1, i'
    })

    rollcall_id, source = wait_for_rollcall(session)
    print(f"Returned: rollcall_id={rollcall_id}, source={source}")

    if source == "number":
        data = await answer_rollcall_number_async(session, rollcall_id)
        print(data)

    elif source == "radar":
        print(answer_rollcall_Radar(session, rollcall_id).text)

if __name__ == "__main__":
    asyncio.run(main())

