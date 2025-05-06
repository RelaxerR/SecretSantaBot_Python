from os import name
import telebot
from random import shuffle
from random import randint

datapath = "C:/Projects/Python/SecretSanta/data.txt"
idpath = "C:/Projects/Python/SecretSanta/ids.txt"
moneypath = "C:/Projects/Python/SecretSanta/money.txt"
wishpath = "C:/Projects/Python/SecretSanta/wish.txt"

api = ""
bot = telebot.TeleBot(api)

adminId = ""

def GetPresents ():
    ids = LoadIds ()
    names = LoadNames ()
    moneys = LoadMoney ()
    wishs = LoadWish ()

    avgm = getSum ()
 
    txt = ""

    for i in range (len (names)):
        if i < len (names) - 1:
            txt = "Вы (" + str (names[i]) + ") дарите для " + str (names [i + 1] + ".\nОн хочет следующее: " + str (wishs[i + 1]) + ".\nИтоговый средний бюджет: " + str (avgm) + " Рублей.")
        else:
            txt = "Вы (" + str (names[i]) + ") дарите для " + str (names [0])
        Send (ids[i], txt)

def Send (userId, text): # Отправка сообщений. Использование: Send (message, ТЕКСТ)
    try:
        bot.send_message(userId, text)
    except:
        print ("long msg")
    print ("Сообщение отправлено для " + str (userId) + ":\n" + text)

def Save (names, ids, moneys, wishs):
    print ("data saved")
    with open(datapath, 'w') as f:
        for s in names:
            f.write(str(s) + '\n')
    with open(idpath, 'w') as f:
        for s in ids:
            f.write(str(s) + '\n')
    with open(moneypath, 'w') as f:
        for s in moneys:
            f.write(str(s) + '\n')
    with open(wishpath, 'w') as f:
        for s in wishs:
            f.write(str(s) + '\n')

def LoadNames ():
    try:
        with open(datapath, 'r') as f:
            score = [line.rstrip('\n') for line in f]
            print ("names data loaded")
            print (score)
            return score
    except:
        print ("Name Data is no loaded")
def LoadIds ():
    try:
        with open(idpath, 'r') as f:
            score = [line.rstrip('\n') for line in f]
            print ("ids data loaded")
            print (score)
            return score
    except:
        print ("Ids Data is no loaded")
        return False
def LoadMoney ():
    try:
        with open(moneypath, 'r') as f:
            score = [line.rstrip('\n') for line in f]
            print ("money data loaded")
            print (score)
            return score
    except:
        print ("Money Data is no loaded")
def LoadWish ():
    try:
        with open(wishpath, 'r') as f:
            score = [line.rstrip('\n') for line in f]
            print ("wish data loaded")
            print (score)
            return score
    except:
        print ("Wish Data is no loaded")

def AddName (name, myid, money, wish):
    ids = []
    names = []
    moneys = []
    wishs = []

    if not (LoadIds () == False):
        ids = LoadIds ()
        names = LoadNames ()
        moneys = LoadMoney ()
        wishs = LoadWish ()

    print ("adding name and id: " + str (name) + " | " + str (myid))

    if not str (myid) in ids:
        ids.append (myid)
        names.append (name)
        moneys.append (money)
        wishs.append (wish)
        Save (names, ids, moneys, wishs)
        return True
    else:
        return False

def ShuffleNames ():
    names = LoadNames ()
    ids = LoadIds ()
    moneys = LoadMoney ()
    wishs = LoadWish ()

    for i in range (len (names)):
        newid = randint (0, len (names) - 1)

        tmpname = names[newid]
        tmpid = ids[newid]
        tmpmoney = moneys[newid]
        tmpwish = wishs[newid]

        names[newid] = names[i]
        ids[newid] = ids[i]
        moneys[newid] = moneys[i]
        wishs[newid] = wishs[i]

        names[i] = tmpname
        ids[i] = tmpid
        moneys[i] = tmpmoney
        wishs[i] = tmpwish
    Save (names, ids, moneys, wishs)

def getSum ():
    monyes = LoadMoney ()

    try:
        m = 0
        i = 0
        for money in monyes:
            try:
                m += int (money)
                i += 1
            except:
                m += 0

        avgm = round (m / i)
        return avgm
    except:
        Send (adminId, "Ошибка при расчёте средней суммы! " + str (monyes))
        return 0

@bot.message_handler(commands=["start"])
def start(message):
    f_name = message.from_user.first_name # Имя пользователя
    user_id = message.from_user.id
    
    txt = "Привет, " + str (f_name) + "!\nДля регистрации в Тайном Санте осталось совсем немного!\nНапиши о себе в таком формате: Reg_Сумма, которую ты готов(а) потратить_Что ты хочешь в качестве подарка\n\nПри распределении будет посчитана средняя сумма, чтобы тебе было понятно, какой бюджет нужно отложить. Сейчас средняя сумма: " + str (getSum ()) + " рублей"

    Send (user_id, txt)

def DeleteUser (userid):
    names = LoadNames ()
    ids = LoadIds ()
    moneys = LoadMoney ()
    wishs = LoadWish ()

    did = -1
    if userid in ids:
        did = ids.index (str (userid))
        try:
            names.pop (did)
        except:
            print ("DATA ERROR")
        try:
            ids.pop (did)
        except:
            print ("DATA ERROR")
        try:
            moneys.pop (did)
        except:
            print ("DATA ERROR")
        try:
            wishs.pop (did)
        except:
            print ("DATA ERROR")

        Save (names, ids, moneys, wishs)

        return True

    # try:
    #     did = -1
    #     if userid in ids:
    #         did = ids.index (str (userid))
    #         names.pop (did)
    #         ids.pop (did)
    #         moneys.pop (did)
    #         wishs.pop (did)

    #         Save (names, ids, moneys, wishs)

    #         return True
    # except:
    #     return False

@bot.message_handler(content_types=['text'])
def text(message):
    username = message.from_user.username
    user_id = message.from_user.id
    msg = message.text

    commands = msg.split ('_')
    command = commands[0]

    if (command == "Shuffle"):
        ShuffleNames ()
        Send (user_id, "Список имён перемешан!")
    elif (command == "Change"):
        Send (adminId, "Пользователь @" + str (username) + "Хочет удалить анкету!")
    elif command == "Delete":
        if (str (user_id) == str (adminId)):
            print (commands[1])
            p = ""
            try:
                p = commands[2]
            except:
                p = "-"
            if DeleteUser (commands[1]):
                Send (user_id, "Анкета удалена")
                Send (commands[1], "Ваша анкета удалена\nПричина удаления: " + str (p))
            else:
                Send (user_id, "Не удалось удалить анкету")
        else:
            if DeleteUser (user_id):
                Send (user_id, "Анкета удалена")
            else:
                Send (user_id, "Не удалось удалить анкету. Запрос на удаление отправлен для @Relaxerrkis")
                Send (adminId, "Пользователь не смог удалить анкету")
                Send (adminId, str (user_id))
    elif commands[0] == "Show":
        names = LoadNames ()
        ids = LoadIds ()
        moneys = LoadMoney ()
        wishs = LoadWish ()

        txt = ""
        for i in range (len (ids)):
            txt += str (names[i]) + "\nid: " + str (ids[i])
            if (len (commands) > 1):
                try:
                    if (str (user_id) == str (adminId)):
                        txt += f"\nmoney: {moneys[i]}\nwish: {wishs[i]}"
                except:
                    print ("CRITICAL DATA ERROR!")
            txt += "\n\n"

        Send (user_id, txt)
    elif command == "Send":
        if (str (user_id) == adminId):
            GetPresents ()
        else:
            Send (user_id, "Вы должны быть Администратором, чтобы использовать эту команду")
    elif command == "Reg":
        # name = message.from_user.first_name
        # money = commands[0]
        # wish = commands[1]

        # AddName (name, user_id, money, wish)
        try:
            name = message.from_user.first_name + " (@" + str (username) + ")"
            money = commands[1]
            tmp = int (money)
            if int (tmp) > 2000:
                raise Exception ("so much")
            wish = commands[2]

            r = AddName (name, user_id, money, wish)
            if r:
                Send (user_id, "Отлично! Твои данные сохранены!\nИмя: " + str (name) + "; Деньги: " + str (money) + "; Желание: " + str (wish))
            else:
                Send (user_id, "Ты уже зарегистрирован(а) в Тайном Санте, твоя анкета:\nИмя: " + str (name) + "; Деньги" + str (money) + "; Желание: " + str (wish) + "\n\nЕсли ты хочешь удалить\поменять анкету, напиши Change")
        except:
            Send (user_id, "Ошибка добавления. Попробуйте ещё раз, напрмер:\nReg_500_Машина, квартира\n\nPS. Вводи сумму не более 2000")
    else:
        Send (user_id, "Неизвестная команда! Список доступных команд:\nDelete - удаляет твою анкету\nReg_твой бюджет_твои пожелания - регистрирует анкету\nShuffle - перемешивает список анкет\nSend - распределяет участников и отправляет каждому, кому он(а) дарит подарок\nShow - показываает список участников\nShow All - показывает список участников с пожеланиями каждого\n\nЧтобы отправить команду, просто напиши ключевое слово из списка доступных\nЕсли нужна помощь, пиши мне: @Relaxerrkis")

bot.polling(none_stop=True, interval=0)