import os
from dotenv import load_dotenv
load_dotenv()
from google import genai
client = genai.Client()
for m in client.models.list():
    if "embed" in m.name.lower():
        print(f"{m.name}")
