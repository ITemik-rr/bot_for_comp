# импорт
import telebot, psutil, os, time
from config import *

# Вставка токена
bot = telebot.TeleBot(TOKEN)
# для последней комманды
def bytes2human(n):
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        prefix = {}
        for i, s in enumerate(symbols):
            prefix[s] = 1 << (i + 1) * 10
        for s in reversed(symbols):
            if abs(n) >= prefix[s]:
                value = float(n) / prefix[s]
                return '%.1f%s' % (value, s)
        return "%sB" % n

# Обработка '/start' и '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """\
Привет, человек. Я бот, который помогает тебе с мониторингом твоего компутатора. Напиши /help и я скажу, что я умею делать быстрее чем ты.\
""")

@bot.message_handler(commands=['help'])
def send_help(message):
        bot.reply_to(message, """\
Так вот, человек, я умею мониторить память твоего компутатора (/memory), показывать количество логических и физических поцессоров (/processors) и 
про твою загрузку CPU рассказывать (/cpu), а также посчитать количество места в диске (/bite). \
""")
        
# монитор памяти компьютера
@bot.message_handler(commands=['memory'])
def send_memory(message):
    mem2 = psutil.virtual_memory().percent
    mem = f' Память твоего компутатора равна {mem2}.' 
    if mem2 <= 60:
         mem +=  'OK'
    else:
         mem +=  'Не экономишь ты память'
    bot.reply_to(message, mem)

# показ количество логических и физических поцессоров
@bot.message_handler(commands=['processors'])
def send_processors(message):
    log  = psutil.cpu_count(logical=True)
    phs = psutil.cpu_count(logical=False)
    ans = f' Логические процессоры {log}. Физические {phs}.' 
    bot.reply_to(message, ans)

# CPU
@bot.message_handler(commands=['cpu'])
def send_cpu(message):
    cp = psutil.cpu_percent(interval = 1)
    answer = f' Твой CPU равен {cp}.' 
    bot.reply_to(message, answer)

# Память в дисках
@bot.message_handler(commands=['bite'])
def send_bite(message):
    paths = []
    if os.name == 'nt':
        for drive in ['C:\\', 'D:\\']:
            try:
                psutil.disk_usage(drive)
                paths.append(drive)
            except Exception:
                continue
        if not paths:
            paths = ['C:\\']  
    else:
        paths = ['/']

    lines = ["💾 Диски:"]
    for path in paths:
        try:
            usage = psutil.disk_usage(path)
            total_human = bytes2human(usage.total)
            free_human = bytes2human(usage.free)
            lines.append(
                f"- {path}:\n"
                f"    Всего: {total_human}\n"
                f"    Свободно: {free_human} ({usage.percent}% занято)"
            )
        except Exception as e:
            lines.append(f"- {path}: ❌ нет доступа ({e})")

    text = "\n".join(lines)
    bot.reply_to(message, text)


bot.infinity_polling()