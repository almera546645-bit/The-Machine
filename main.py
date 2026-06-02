import os
import time
import requests
import threading
from flask import Flask

app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
PROXY_URL = os.environ.get("PROXY_URL")

HUNT_LIST = [
    {"query": "Xbox Series S", "max_price": 13000},
    {"query": "Apple Watch SE", "max_price": 12000},
    {"query": "iPad 9", "max_price": 16000}
]

@app.route('/')
def health():
    return "Машина работает", 200

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})
    except Exception as e:
        print(f"Ошибка ТГ: {e}")

def check_avito():
    if not PROXY_URL:
        send_telegram_message("⚠️ *Ошибка:* PROXY_URL не найден в настройках Render!")
        return

    proxies = {"http": PROXY_URL, "https": PROXY_URL}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    item = HUNT_LIST[0]
    search_url = f"https://www.avito.ru/krym_i_krasnodarskiy_kray?q={item['query']}"
    
    try:
        # Делаем реальный проверочный запрос через Билайн-прокси
        response = requests.get(search_url, headers=headers, proxies=proxies, timeout=20)
        
        if response.status_code == 200:
            send_telegram_message(f"✅ *Проверка реальности:* Прокси работает! Защита Авито успешно пробита, код ответа 200. Мы внутри системы!")
        else:
            send_telegram_message(f"⚠️ *Затык:* Авито ответил кодом {response.status_code}. Мобильный IP определен, но доступ ограничен.")
            
    except Exception as e:
        send_telegram_message(f"❌ *Ошибка сети через прокси:* {str(e)}")

def bot_worker():
    time.sleep(10)
    send_telegram_message("🚀 *Машина запущена с московским прокси Билайн.* Тестирую первый реальный прорыв к Авито...")
    check_avito()

threading.Thread(target=bot_worker, daemon=True).start()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
