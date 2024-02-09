import telebot
import random

started = False
clues = list("?" for _ in range(5))
guessed = list()
lives = 10

bot = telebot.TeleBot("6698814211:AAHG1nGyvkAgIqJBvrvo7cOXQhW5avf8V44")


with open("words.txt", "r", encoding="utf-8") as f:
    words = list()
    for line in f:
        line = line.rstrip()
        words.append(line)

word = random.choice(words)


@bot.message_handler(commands=["start"])
def start(msg):
    global started, clues, word, guessed, lives
    started = True
    clues = list("?" for _ in range(5))
    guessed.clear()
    lives = 10

    word = random.choice(words)

    bot.send_message(msg.chat.id, "Привет! Я создан для игры в упрощённую виселицу. Правила просты: отгадывай буквы, "
                                  "отправляй свои догадки мне. У тебя 10 жизней, и если догадка неверна, ты теряешь одну. Наслаждайся игрой!")
    bot.send_message(msg.chat.id, f"Я загадал слово из пяти букв. Пока тебе не известно не одной его буквы: {clues}")
    bot.send_message(msg.chat.id, "Попробуй отгадать букву (в любой момент игры ты можешь ввести целое слово, если ты уверен в ответе)")


@bot.message_handler(content_types=["text"])
def handle_msg(msg):
    global clues, guessed, started, lives
    if not started:
        bot.send_message(msg.chat.id, "Для начала игры введи /start.")
    if len(msg.text) == 1:
        guessed.append(msg.text)
        if msg.text.lower() in word:
            for ltr in range(len(word)):
                if word[ltr] == msg.text.lower():
                    clues[ltr] = msg.text.lower()
            if clues == [i for i in word]:
                bot.send_message(msg.chat.id, "Поздравляю! Ты угадал слово! Хочешь сыграть ещё раз? Вводи /start.")
                started = False
            bot.send_message(msg.chat.id,
                             f"Ты угадал букву {msg.text}!")
        else:
            lives -= 1
            bot.send_message(msg.chat.id, "Упс! Ты теряешь жизнь(")
            if lives == 0:
                started = False
                bot.send_message(msg.chat.id, "К сожалению, "
                                              "игра окончена, ведь у тебя не осталось жизней. Удачи в следующий раз!")

        bot.send_message(msg.chat.id, f"Загаданное слово: {clues}, твои догадки: {', '.join(guessed)}, осталось жизней: {lives}.")
    else:
        if msg.text.lower() == word:
            bot.send_message(msg.chat.id, "Поздравляю! Ты угадал слово! Хочешь сыграть ещё раз? Вводи /start.")
            started = False
        else:
            lives -= 1
            bot.send_message(msg.chat.id, "Это не загаданное слово. Ты теряешь одну жизнь.")
            if lives == 0:
                started = False
                bot.send_message(msg.chat.id, "К сожалению, "
                                              "игра окончена, ведь у тебя не осталось жизней. Удачи в следующий раз!")


bot.polling(non_stop=True)
