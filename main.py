import telebot
import random

started = False
clues = list("?" for _ in range(5))
guessed = list()
lives = 10
initial_lives = 10

bot = telebot.TeleBot("6698814211:AAHG1nGyvkAgIqJBvrvo7cOXQhW5avf8V44")


with open("words.txt", "r", encoding="utf-8") as f:
    words = list()
    for line in f:
        line = line.rstrip()
        words.append(line)

word = random.choice(words)


@bot.message_handler(commands=["start"])
def start(msg):
    global started, clues, word, guessed, lives, initial_lives
    started = True
    clues = list("?" for _ in range(5))
    guessed.clear()
    lives, initial_lives = 10, 10

    word = random.choice(words)

    bot.send_message(msg.chat.id, "Привет! Я создан для игры в упрощённую виселицу. Правила просты: отгадывай буквы, "
                                  "отправляй свои догадки мне. У тебя 10 жизней (ты можешь изменить сложность командой "
                                  "/difficulty), и если догадка неверна, ты теряешь одну. Наслаждайся игрой!")
    bot.send_message(msg.chat.id, f"Я загадал слово из пяти букв. Пока тебе не известно не одной его буквы: {clues}")
    bot.send_message(msg.chat.id, "Попробуй отгадать букву (в любой момент игры ты можешь ввести целое слово, если уверен в ответе)")


@bot.message_handler(commands=["stop"])
def stop(msg):
    global started
    bot.send_message(msg.chat.id, "Игра остановлена")
    started = False


@bot.message_handler(commands=["difficulty"])
def difficulty(msg):
    if lives == initial_lives:
        bot.send_message(msg.chat.id, "Измени сложность (на лёгкую, среднюю или сложную: отправь 1, 2 или 3)")
        bot.register_next_step_handler(msg, setdifficulty)
    else:
        bot.send_message(msg.chat.id, "Ты можешь изменить сложность только перед началом игры.")


def setdifficulty(msg):
    global lives, initial_lives
    if msg.text[0] == "1":
        lives, initial_lives = 15, 15
    elif msg.text[0] == "2":
        lives, initial_lives = 10, 10
    else:
        lives, initial_lives = 7, 7

    bot.send_message(msg.chat.id, f"Установлено количество жизней: {initial_lives}")


@bot.message_handler(content_types=["text"])
def handle_msg(msg):
    global clues, guessed, started, lives
    if not started:
        bot.send_message(msg.chat.id, "Для начала игры введи /start.")
        return
    if len(msg.text) == 1:
        if msg.text.lower() in guessed:
            bot.send_message(msg.chat.id, "Ты уже отправлял эту букву, попробуй ввести другую. ")
            return
        guessed.append(msg.text.lower())
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
                bot.send_message(msg.chat.id, f"К сожалению, "
                                              f"игра окончена, ведь у тебя не осталось жизней. Удачи в следующий раз! Я загадал слово <b>{word}</b>.",
                                 "html")

        bot.send_message(msg.chat.id, f"Загаданное слово: {clues}, твои догадки: {', '.join(guessed)}, осталось жизней: {lives}.")
    else:
        if msg.text.lower() == word:
            bot.send_message(msg.chat.id, "Мои поздравления! Ты угадал слово! Хочешь сыграть ещё раз? Вводи /start.")
            started = False
        else:
            lives -= 1
            bot.send_message(msg.chat.id, "Это не загаданное слово. Ты теряешь одну жизнь.")
            if lives == 0:
                started = False
                bot.send_message(msg.chat.id, "К сожалению, "
                                              "игра окончена, ведь у тебя не осталось жизней. Удачи в следующий раз!")


bot.polling(non_stop=True)
