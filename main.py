
import os
import time
import requests
import threading
from flask import Flask

app = Flask(__name__)

# Берём токены из настроек Render
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Наш чёрный список (стоп-слова)
STOP_WORDS = [
    "на запчасти", "не включается", "ремонт", "артефакты", "греется", 
    "шумит", "глючит", "сгорел", "мастер", "бан", "banned", 
    "заблокирован", "нет сети", "аренда", "прокат", "посуточно", 
    "trade-in", "трейд ин", "магазин", "куплю", "обмен", "ищу", 
    "без геймпада", "без джойстика"
]

# Наш список охоты: что ищем и максимальная цена
HUNT_LIST = [
    {"query": "Xbox Series S", "max_price": 13000},
    {"query": "PS4 Slim", "max_price": 11000},
    {"query": "PS4 Pro", "max_price": 14000},
    {"query": "Xbox One X", "max_price": 10000},
    {"query": "iPad 9", "max_price": 16000},
    {"query": "iPad 10", "max_price": 16000},
    {"query": "iPad Air", "max_price": 19000},
    {"query": "Apple Watch SE", "max_price": 12000},
    {"query": "Apple Watch 6", "max_price": 12000},
    {"query": "Apple Watch 7", "max_price": 12000},
    {"query": "Apple Watch 10 46mm Rose", "max_price": 29000},
    {"query": "Коляска Anex", "max_price": 12000},
    {"query": "Коляска Cybex", "max_price": 12000}
]

@app.route('/')
def health():
    return "Машина работает", 200

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})
    except Exception as e:
        print(f"Ошибка отправки сообщения: {e}")

def check_avito():
    for item in HUNT_LIST:
        try:
            pass
        except Exception as e:
            print(f"Ошибка при поиске {item['query']}: {e}")
        time.sleep(5)

def bot_worker():
    time.sleep(10)
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/setWebhook", json={"url": ""})
    except:
        pass
    send_telegram_message("🚀 *Машина успешно обновлена!* \nРадар по Крыму и Краснодарскому краю запущен.\n\nИщу: гейм-боксы, айпады, Apple Watch и премиум-коляски.")
    
    while True:
        check_avito()
        time.sleep(300)

# Запуск фонового радара
threading.Thread(target=bot_worker, daemon=True).start()

# Вот эта заветная строчка, которую я забыл!
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
