
import os
import time
import threading
import telebot
import requests
from bs4 import BeautifulSoup
from http.server import BaseHTTPRequestHandler, HTTPServer

# === ФЕЙКОВЫЙ ВЕБ-СЕРВЕР ДЛЯ ОБМАНА RENDER ===
class RenderHealthServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Machine is running perfectly!")

# === НАСТРОЙКИ БОТА ===
BOT_TOKEN = '8983463329:AAG8LuVFvDO9xtz0LnWiuzgyGaxNF3JMWFY' 
bot = telebot.TeleBot(BOT_TOKEN)

USER_CHAT_ID = None 

TARGETS = {
    "xbox series s": 13000,
    "ps4 slim": 11000,
    "ps4 pro": 14000,
    "xbox one x": 10000
}

STOP_WORDS = [
    "на запчасти", "не включается", "ремонт", "артефакты", "греется", 
    "шумит", "глючит", "сгорел", "мастер", "бан", "banned", "заблокирован", 
    "нет сети", "аренда", "прокат", "посуточно", "trade-in", "трейд ин", 
    "магазин", "куплю", "обмен", "ищу", "без геймпада", "без джойстика"
]

SENT_ADS = set()
REGIONS = ["krym", "krasnodarskiy_kray"]

# === БОЕВОЙ АЛГОРИТМ ПОИСКА ===
def scan_radar():
    global USER_CHAT_ID
    print("Боевой локатор Авито запущен...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "ru-RU,ru;q=0.9"
    }
    
    while True:
        if not USER_CHAT_ID:
            time.sleep(5)
            continue
            
        for target, max_price in TARGETS.items():
            for region in REGIONS:
                try:
                    search_url = f"https://www.avito.ru/{region}/igrovye_pristavki_igry_i_programmy?q={target.replace(' ', '+')}&s=104"
                    print(f"Сканируем Авито ({region}) для: {target}...")
                    
                    response = requests.get(search_url, headers=headers, timeout=10)
                    if response.status_code != 200:
                        continue
                        
                    soup = BeautifulSoup(response.text, 'html.parser')
                    items = soup.find_all('div', {'data-marker': 'item'})
                    
                    for item in items:
                        try:
                            title_element = item.find('h3', {'itemprop': 'name'})
                            if not title_element:
                                continue
                            title = title_element.text.strip()
                            
                            link_element = item.find('a', {'itemprop': 'url'})
                            if not link_element:
                                continue
                            url = "https://www.avito.ru" + link_element['href']
                            
                            if url in SENT_ADS:
                                continue
                                
                            price_element = item.find('meta', {'itemprop': 'price'})
                            if price_element:
                                price = int(price_element['content'])
                            else:
                                price_text = item.find('span', {'data-marker': 'item-price'})
                                if price_text:
                                    price = int(''.join(filter(str.isdigit, price_text.text)))
                                else:
                                    continue
                            
                            has_stop_word = any(word in title.lower() for word in STOP_WORDS)
                            
                            if price <= max_price and not has_stop_word:
                                alert = (
                                    f"🎯 **НАЙДЕНО НА АВИТО!**\n\n"
                                    f"📦 Товар: {target.upper()}\n"
                                    f"💰 Цена: {price} ₽ (Твоя цель: до {max_price} ₽)\n"
                                    f"📝 Заголовок: {title}\n\n"
                                    f"🔗 Ссылка:\n{url}"
                                )
                                bot.send_message(USER_CHAT_ID, alert, parse_mode='Markdown')
                                SENT_ADS.add(url)
                                time.sleep(2) 
                                
                        except Exception:
                            continue
                            
                except Exception as e:
                    print(f"Ошибка сканирования: {e}")
                
                time.sleep(20)
        time.sleep(600)

# === КОМАНДЫ ТЕЛЕГРАМ ===
@bot.message_handler(commands=['start', 'status'])
def send_status(message):
    global USER_CHAT_ID
    USER_CHAT_ID = message.chat.id
    
    report = "🟢 **Машина-Радар переведена в БОЕВОЙ режим Авито!**\n\n"
    report += "📍 **Регионы поиска:** Крым + Краснодарский край\n"
    report += "🔍 Проверка объявлений запущена в фоновом режиме.\n\n"
    report += "🎯 **Мои цели:**\n"
    for target, price in TARGETS.items():
        report += f"- {target.upper()}: до {price} ₽\n"
    bot.reply_to(message, report, parse_mode='Markdown')

if __name__ == '__main__':
    # 1. Запускаем локатор в фоновом потоке
    threading.Thread(target=scan_radar, daemon=True).start()
    
    # 2. Запускаем Телеграм-бота в фоновом потоке
    threading.Thread(target=bot.infinity_polling, daemon=True).start()
    
    # 3. Запускаем веб-сервер на ОСНОВНОМ потоке (Рендер будет видеть его в первую очередь)
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), RenderHealthServer)
    print(f"Веб-сервер запущен на порту {port}")
    server.serve_forever()
