import telebot
from user import User
from shape_func import no_member, poorly, usrname_to_id
from parametrs import TOKEN, CREATOR, TESTER, WARN_TO_MUTE
from event import Event
import datetime

bot = telebot.TeleBot(TOKEN)

USERS = {CREATOR: User(2), TESTER: User(2)}
EVENTS = []


@bot.message_handler(commands=['help'])
def command_list(message):
    """
    Prints command list
    :param message:
    :return:
    """
    bot.send_message(message.chat.id, "Привет, меня зовут Генадий Брат. Я буду вашим новым другом.")
    bot.send_message(message.chat.id, "Мои комманды:\n" +
                                      "/start - вступить в ряды пользователей Генадия\n" +
                                      "/help - список команд\n" +
                                      "/info - информация\n" +
                                      "/all - тэгнуть всех в чате\nУроыень доступа 1\n" +
                                      "/event - создать событие\n<describtion> <dd.mm.yyyy>\nУровень доступа 1\n"
                                      "/deadline - вывести список всех дедлайнов\n" +
                                      "/kill - завершить работу бота\nУровень доступа 2\n" +
                                      "/mafia - начать игру мафия\n" +
                                      "/coins - начать игру казино\n" +
                                      "/warn - кинуть пред\n<user>\nУровень доступа 1\n" +
                                      "/mute - кинуть в мут\n<user>\nУровень доступа 1\n" +
                                      "/pardon - снять мут\n<user>\nУровень доступа 1\n" +
                                      "/give_admin - выдать права администратора\n<user>\nУровень доступа 2\n" +
                                      "/demote - понизить уровень доступа\n<user>\nУровень доступа 2\n" +
                                      "/event_list - вывести список событий\nУровень доступа 1\n")


@bot.message_handler(commands=['start'])
def start(message):
    """
    signing in community
    :param message:
    :return:
    """
    bot.send_message(message.chat.id, "Привет, меня зовут Генадий Брат. Я буду вашим новым другом.\n" +
                                      "Чтобы посмотреть список команд введите /help")
    if USERS.get(message.from_user.id) is None:
        USERS[message.from_user.id] = User(0)
        bot.send_message(message.chat.id, message.from_user.first_name + ", теперь вы можете меня использовать.")
    else:
        bot.send_message(message.chat.id, message.from_user.first_name + ", вы уже являетесь частью сообщества" +
                                                                         " пользователей Генадия Брата")


@bot.message_handler(commands=['info'])
def info(message):
    """
    information about creator
    :param message:
    :return:
    """
    bot.send_message(message.chat.id, 'Создатель: @YamSuf\nНа кофе: 4817760342918145')


@bot.message_handler(commands=['all'])
def tag_all(message):
    """
    tags all of users
    :param message:
    :return:
    """
    if USERS.get(message.from_user.id) is None:
        no_member(bot, message)
        return
    if USERS[message.from_user.id].right > 0:
        user_list = list(USERS.keys())
        for usr in user_list:
            bot.send_message(usr, "Посмотри чат группы, там прислали что то важное")
        return
    poorly(bot, message, 'all')


@bot.message_handler(commands=['kill'])
def kill(message):
    """
    stops bot with delay
    :param message:
    :return:
    """
    if USERS.get(message.from_user.id) is None:
        no_member(bot, message)
        return
    if USERS[message.from_user.id].right >= 2:
        bot.send_message(message.chat.id, "Пока!")
        bot.stop_bot()
        return
    poorly(bot, message, 'kill')


@bot.message_handler(commands=['give_admin'])
def give(message):
    """
    gives admin rights
    :param message:
    :return:
    """
    if USERS.get(message.from_user.id) is None:
        # catching exception not member type
        no_member(bot, message)
        # return message
        return
    arg = message.text.split()[1:]
    if len(arg) != 1:
        bot.send_message(message.chat.id, message.from_user.first_name + ", неверное число аргументов")
        return
    arg = usrname_to_id(arg[0])
    if USERS.get(arg) is None:
        no_member(bot, message, arg)
        return
    if USERS[message.from_user.id].right < 2:
        poorly(bot, message, 'give_admin')
        return
    USERS[arg].right = 1


@bot.message_handler(commands=['demote'])
def demote(message):
    """
    demotion in rights
    :param message:
    :return:
    """
    if USERS.get(message.from_user.id) is None:
        no_member(bot, message)
        return
    arg = message.text.split()[1:]
    if len(arg) != 1:
        bot.send_message(message.chat.id, message.from_user.first_name + ", неверное число аргументов")
        return
    arg = usrname_to_id(arg[0])
    if USERS.get(arg) is None:
        no_member(bot, message, arg)
        return
    if USERS[message.from_user.id].right < 2:
        poorly(bot, message, 'demote')
        return
    USERS[arg].right = 0


@bot.message_handler(commands=['pardon'])
def unmute(message):
    """
    delete muting from user
    :param message:
    :return:
    """
    if USERS.get(message.from_user.id) is None:
        no_member(bot, message)
        return
    arg = message.text.split()[1:]
    if len(arg) != 1:
        bot.send_message(message.chat.id, message.from_user.first_name + ", неверное число аргументов")
        return
    arg = usrname_to_id(arg[0])
    if USERS.get(arg) is None:
        no_member(bot, message, arg)
        return
    if USERS[message.from_user.id].right < 2:
        poorly(bot, message, 'pardon')
        return
    USERS[arg].warn_count = 0
    USERS[arg].is_mute = False


@bot.message_handler(commands=['mute'])
def mute(message):
    """
    mute user
    :param message:
    :return:
    """
    if USERS.get(message.from_user.id) is None:
        no_member(bot, message)
        return
    arg = message.text.split()[1:]
    if len(arg) != 1:
        bot.send_message(message.chat.id, message.from_user.first_name + ", неверное число аргументов")
        return
    arg = usrname_to_id(arg[0])
    if USERS.get(arg) is None:
        no_member(bot, message, arg)
        return
    if USERS[message.from_user.id].right < 2:
        poorly(bot, message, 'mute')
        return
    USERS[arg].warn_count = 0
    USERS[arg].is_mute = True


@bot.message_handler(commands=['warn'])
def warn(message):
    """
    drop warning for user
    :param message:
    :return:
    """
    if USERS.get(message.from_user.id) is None:
        no_member(bot, message)
        return
    arg = message.text.split()[1:]
    if len(arg) != 1:
        bot.send_message(message.from_user.id, message.from_user.first_name + ", неверное число аргументов")
        return
    arg = usrname_to_id(arg[0])
    if USERS.get(arg) is None:
        no_member(bot, message, arg)
        return
    if USERS[message.from_user.id].right < 2:
        poorly(bot, message, 'warn')
        return
    USERS[arg].warn_count += 1
    bot.send_message(message.chat.id, "Предупреждение!!!")
    if USERS[arg].warn_count > WARN_TO_MUTE:
        USERS[arg].warn_count = 0
        USERS[arg].is_mute = True
        bot.send_message(message.chat.id, "Отлетаем в мут")


@bot.message_handler(commands=['event'])
def create_event(message):
    """
    create Event type object in event list
    :param message:
    :return:
    """
    if USERS.get(message.from_user.id) is None:
        no_member(bot, message)
        return
    arg = message.text.split()[1:]
    if len(arg) < 2:
        bot.send_message(message.from_user.id, message.from_user.first_name + ", неверное число аргументов")
        return
    date = arg[len(arg) - 1].split('.')
    if len(date) < 3:
        bot.send_message(message.from_user.id, message.from_user.first_name + ", неверный формат даты")
        return
    date = list(map(int, date))
    date = datetime.date(date[2], date[1], date[0])
    arg = arg[:len(arg) - 1]
    describtion = ' '.join(arg)
    EVENTS.append(Event(describtion, date))
    if USERS[message.from_user.id].right < 1:
        poorly(bot, message, 'event')
        return


@bot.message_handler(commands=['deadline'])
def deadline(message):
    """
    display deadlines
    :param message:
    :return:
    """
    if USERS.get(message.from_user.id) is None:
        no_member(bot, message)
        return
    flag = False
    for event in EVENTS:
        if event.date == datetime.date.today():
            bot.send_message(message.chat.id, event.describtion)
            flag = True
    if not flag:
        bot.send_message(message.chat.id, "Расчилься, сегодня ничего нет")


@bot.message_handler(commands=['event_list'])
def deadline_list(message):
    """
    display deadline list
    :param message:
    :return:
    """
    if USERS.get(message.from_user.id) is None:
        no_member(bot, message)
        return

    flag = False
    for event in EVENTS:
        bot.send_message(message.chat.id, event.describtion + ' ' + str(event.date))
        flag = True
    if not flag:
        bot.send_message(message.chat.id, "Ничего нет")


@bot.message_handler(commands=['coins', 'mafia'])
def in_dev(message):
    """
    in developing
    :param message:
    :return:
    """
    bot.send_message(message.chat.id, "Эта команда ещё в разработке")


@bot.message_handler()
def delete_from_muted(message):
    """
    processing muting
    :param message:
    :return:
    """
    if USERS.get(message.from_user.id) is None:
        return
    if USERS[message.from_user.id].is_mute:
        bot.delete_message(message.chat.id, message.id)


bot.polling(none_stop=True)
