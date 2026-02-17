import os
import time
import threading
from pyngrok import ngrok

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


def start_django():
    os.system("python manage.py runserver 8000 --noreload")


# Django serverni ishga tushiramiz
threading.Thread(target=start_django, daemon=True).start()

# Django to‘liq ishga tushishini kutamiz
time.sleep(8)

# ngrok token (IMPORTANT: keyni keyinchalik yangilagin)
ngrok.set_auth_token("36axo14pVmoZFWrOF3w6CgfjHVa_6xZZCxjUvid3CMYyFFe9U")

# tunnel ochish
public_url = ngrok.connect(8000)

print("=" * 50)
print("Local:", "http://127.0.0.1:8000")
print("Public:", public_url)
print("=" * 50)

# programmani alive ushlab turish
while True:
    time.sleep(1)
