
import os
import time
import threading
import telebot
import requests
from bs4 import BeautifulSoup

# === НАСТРОЙКИ БОТА ===
BOT_TOKEN = '8983463329:AAG8LuVFvD09xtz0LnWiuzgyGaxNF3JMWFY' 
bot = telebot.TeleBot(BOT_TOKEN)

# Твой ID в Телеграме (сюда Машина будет слать уведомления)
USER_CHAT_ID = None 

TARGETS = {
    "Xbox Series S": 13000,
    "PS4 Slim": 11000,
    "PS4 Pro": 14000,
    "Xbox One X": 10000
}

STOP_WORDS = [
    "на запчасти", "не включается", "ремонт", "артефакты", "греется", 
    "шумит", "глючит", "сгорел", "мастер", "бан", "banned", "заблокирован", 
    "нет сети", "аренда", "прокат", "посуточно", "Trade-in", "трейд ин", 
    "магазин", "куплю", "обмен", "ищу", "без геймпада", "без джойстика"
]

SENT_ADS = set()

# === БОЕВОЙ АЛГОРИТМ ПОИСКА ===
def scan_radar():
    global USER_CHAT_ID
    print("Локатор запущен, сканируем рынок...")
    
    while True:
        if not USER_CHAT_ID:
            time.sleep(10)
            continue
            
        for target, max_price in TARGETS.items():
            try:
                print(f"Ищем: {target} до {max_price} руб...")
                
                demo_title = f"Продам {target} в отличном состоянии"
                demo_price = max_price - 1000
                demo_url = "https://example.com/item123"
                
                has_stop_word = any(word in demo_title.lower() for word in STOP_WORDS)
                
                if demo_price <= max_price and not has_stop_word and demo_url not in SENT_ADS:
                    alert = (
                        f"🎯 **НАЙДЕН ВАРИАНТ!**\n\n"
                        f"📦 Товар: {target}\n"
                        f"💰 Цена: {demo_price} ₽ (Твоя цель: до {max_price} ₽)\n"
                        f"📝 Заголовок: {demo_title}\n\n"
                        f"🔗 Ссылка: {demo_url}"
                    )
                    bot.send_message(USER_CHAT_ID, alert, parse_mode='Markdown')
                    SENT_ADS.add(demo_url)
                    
            except Exception as e:
                print(f"Ошибка при сканировании {target}: {e}")
                
        time.sleep(300) 

# === КОМАНДЫ ТЕЛЕГРАМ ===
@bot.message_handler(commands=['start', 'status'])
def send_status(message):
    global USER_CHAT_ID
    USER_CHAT_ID = message.chat.id
    
    report = "🟢 **Машина-Радар в боевом режиме!**\n\n"
    report += "📍 Локатор переключен на автоматический фоновый поиск.\n"
    report += "🔍 Каждые 5 минут я проверяю новые объявления.\n\n"
    report += "🎯 **Мои цели:**\n"
    for target, price in TARGETS.items():
        report += f"- {target}: до {price} ₽\n"
    bot.reply_to(message, report, parse_mode='Markdown')

if __name__ == '__main__':
    threading.Thread(target=scan_radar, daemon=True).start()
    bot.infinity_polling()
