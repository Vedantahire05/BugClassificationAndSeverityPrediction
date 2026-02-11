import time
import requests

def check_rate_limit(headers):
    r = requests.get("https://api.github.com/rate_limit", headers=headers)
    data = r.json()
    remaining = data['rate']['remaining']
    reset_time = data['rate']['reset']
    
    if remaining == 0:
        sleep_time = int(reset_time - time.time())
        if sleep_time > 0:
            print(f"Rate limit exceeded. Sleeping for {sleep_time} seconds...")
            time.sleep(sleep_time)
