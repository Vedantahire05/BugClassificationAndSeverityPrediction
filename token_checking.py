from dotenv import load_dotenv
import os, requests

load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")
r = requests.get("https://api.github.com/user", headers={"Authorization": f"token {TOKEN}"})
print(r.json())
