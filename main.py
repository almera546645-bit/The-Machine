import telebot

# Вставь сюда токен своего бота вместо текста ниже
BOT_TOKEN = '8983463329:AAG8LuVFvDO9xtz0LnWiuzgyGaxNF3JMWFY' 
bot = telebot.TeleBot(BOT_TOKEN)

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

@bot.message_handler(commands=['start', 'status'])
def send_status(message):
    report = "🟢 **Машина-Радар в боевом режиме!**\n\n"
    report += "📍 **Регионы поиска:** Крым + Краснодарский край\n\n"
    report += "🎯 **Мониторинг цен:**\n"
    for target, price in TARGETS.items():
        report += f"- {target}: до {price} ₽\n"
    bot.reply_to(message, report, parse_mode='Markdown')

if __name__ == '__main__':
    print("Робот запущен...")
    bot.infinity_polling()
