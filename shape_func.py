def no_member(tg_bot, message, name="Вы"):
    tg_bot.send_message(message.chat.id, name + " не являетесь зарегистрированным пользователем бота Генадия\n" +
                        "Чтобы пользоваться его возможностями пропишите /start")


def poorly(tg_bot, message, command):
    tg_bot.send_message(message.chat.id,
                        message.from_user.first_name +
                        ", у вас недостаточно прав для использования /" +
                        command)


def usrname_to_id(username):
    return int(username)
