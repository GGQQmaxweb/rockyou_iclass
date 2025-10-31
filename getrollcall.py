import time
import requests

def wait_for_rollcall(session: requests.Session,sec:int=10) -> tuple[int, str]:
    """
    Polls the iClass rollcall API until the specified rollcall_id is found.
    
    Args:
        session (requests.Session): The session with proper headers set.
        target_rollcall_id (int): The rollcall_id to wait for.
    
    Returns:
        tuple: (rollcall_id, source) when found.
    """
    url = 'https://iclass.tku.edu.tw/api/radar/rollcalls?api_version=1.1.0'
    while True:
        try:
            response = session.get(url)
            response.raise_for_status()
            data = response.json()
            rollcall_id = ""
            rollcalls = data.get('rollcalls', [])
            for rollcall in rollcalls:
                if rollcall.get('rollcall_id'):
                    print(f"Found rollcall: ID = {rollcall['rollcall_id']}, Source = {rollcall['source']}")
                    return rollcall['rollcall_id'],rollcall['source']

            print(f"Rollcall not found yet. Waiting {sec} seconds...")
            time.sleep(sec)

        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(5)
