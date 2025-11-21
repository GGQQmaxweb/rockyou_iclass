import ssl
import aiohttp
import asyncio
import json
import logging
from api.http_headers import number_rollcall_headers

if not logging.getLogger().hasHandlers():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

logger = logging.getLogger(__name__)


async def try_code(session, url, headers, code):
    data = {"deviceId": "7eba2081f77e5527", "numberCode": code}
    async with session.put(url, headers=headers, data=json.dumps(data)) as resp:
        text = await resp.text()
        logger.info("Trying %s: %s - %s", code, resp.status, text)
        if resp.status == 200 and "on_call" in text.lower():
            logger.info("✅ Correct code found: %s", code)
            return True
    logger.error("can't find correct code, try again")
    return False


async def answer_rollcall_number_async(session, rollcall_id):
    url = f"https://iclass.tku.edu.tw/api/rollcall/{rollcall_id}/answer_number_rollcall"

    headers = number_rollcall_headers()

    # 🔐 Disable SSL verification
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    cookie_dict = session.cookies.get_dict()
    # 🔄 Use the connector with disabled SSL
    async with aiohttp.ClientSession(
        cookies=cookie_dict, connector=connector
    ) as session:
        for i in range(0, 10000, 100):
            tasks = []
            for j in range(i, min(i + 100, 10000)):
                code = f"{j:04d}"
                tasks.append(try_code(session, url, headers, code))
            results = await asyncio.gather(*tasks)
            if any(results):
                break  # Stop on success
