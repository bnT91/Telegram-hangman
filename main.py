import telebot

bot = telebot.TeleBot("6698814211:AAHG1nGyvkAgIqJBvrvo7cOXQhW5avf8V44")


with open("words.txt", "r", encoding="utf-8") as f:
    words = list()
    for line in f:
        line = line.rstrip()
        words.append(line)


@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(msg.chat.id, "Привет! Этот бот создан для игры в виселицу. Правила просты: гадывай буквы, "
                                  "отправляй твои догадки боту. Есть 3 уровня сложности, на сложном "
                                  "тебе даётся 7 жизней, на среднем - 10, а на сложном - 15. Наслаждайся игрой!")


print(words)
