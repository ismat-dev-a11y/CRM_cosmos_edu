import os
import sys
import threading
import time
import ngrok

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  

import django
from django.core.management.commands.runserver import Command as Runserver

def start_django_server():
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'runserver', '8000', '--noreload'])

server_thread = threading.Thread(target=start_django_server, daemon=True)
server_thread.start()

time.sleep(3)  

try:
    listener = ngrok.forward(8000, authtoken="36axo14pVmoZFWrOF3w6CgfjHVa_6xZZCxjUvid3CMYyFFe9U")
    
    print("=" * 50)
    print(f"Mahalliy manzil: http://localhost:8000")
    print(f"Internet manzil: {listener.url()}")
    print("=" * 50)
    print("CTRL+C tugmalarini bosib to'xtating")

    while True:
        time.sleep(1)
        
except KeyboardInterrupt:
    print("\nDastur to'xtatildi")
except Exception as e:
    print(f"Xato: {e}")
    sys.exit(1)