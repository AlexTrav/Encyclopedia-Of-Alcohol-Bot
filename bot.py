import telebot as tb
from database.db_command import DataBase

bot = tb.TeleBot('5381314744:AAE1H24pXros7KCVNVJiS8e4a607I32U6WM')

db = DataBase()

last_command = ['', '', '']
login_as_admin = 0


@bot.message_handler(commands=['start'])
def start(message):
    db.open_connect()
    user_condition = db.select_table('admin', 1, 0, ('user_condition',), ('id',), ('1',))[0][0]
    db.close_connect()
    mess = f'{message.from_user.first_name} {message.from_user.last_name} добро пожаловать в энциклопедию алкоголя!' + '\n'
    mess += 'Выберите нужное действие:'
    markup = tb.types.InlineKeyboardMarkup(row_width=1)
    btnCategories = tb.types.InlineKeyboardButton(text='Категории алкоголя', callback_data='categories')
    markup.add(btnCategories)
    if user_condition == 0:
        btnLogInAsAdmin = tb.types.InlineKeyboardButton(text='Войти как админ', callback_data='login_as_admin')
        btnSuggestEntry = tb.types.InlineKeyboardButton(text='Предложить запись', callback_data='suggest_entry')
        markup.add(btnLogInAsAdmin, btnSuggestEntry)
    if user_condition == 1:
        btnSuggestedEntries = tb.types.InlineKeyboardButton(text='Предложенные записи', callback_data='suggested_entries')
        btnExit = tb.types.InlineKeyboardButton(text='Выйти из аккаунта', callback_data='exit')
        markup.add(btnSuggestedEntries, btnExit)
    bot.send_message(message.chat.id, mess, reply_markup=markup)


# @bot.message_handler(commands=['help'])
# def help_bot(message):
#     pass


@bot.message_handler(content_types=['text'])
def text(message):
    global last_command, login_as_admin
    markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
    db.open_connect()
    categories = db.select_table('category_alcohol', 0, 0, ('category',), '', '', '')
    categories_ids = db.select_table('subcategories_of_alcohol', 0, 0, ('category_id',), '', '', '')
    names_of_alcohols = db.select_table('subcategories_of_alcohol', 0, 0, ('name_of_alcohol',), '', '', '')
    sub_categories_ids = db.select_table('alcohol', 0, 0, ('subcategories_id',), '', '', '')
    names_of_drinks = db.select_table('alcohol', 0, 0, ('name_of_drink',), '', '', '')
    alcohols_contents = db.select_table('alcohol', 0, 0, ('alcohol_content',), '', '', '')
    descriptions = db.select_table('alcohol', 0, 0, ('description',), '', '', '')
    photos = db.select_table('alcohol', 0, 0, ('photo',), '', '', '')
    price = db.select_table('alcohol', 0, 0, ('price',), '', '', '')
    logins = db.select_table('admin', 0, 0, ('login',), '', '', '')
    passwords = db.select_table('admin', 0, 0, ('password',), '', '', '')
    db.close_connect()

    # Категории
    if message.text == 'Категории':
        mess = 'Выберите категорию алкоголя:'
        markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in range(len(categories)):
            btn = tb.types.KeyboardButton(categories[i][0])
            markup.add(btn)
        btnStart = tb.types.KeyboardButton('/start')
        markup.add(btnStart)
        bot.send_message(message.chat.id, mess, reply_markup=markup)

    if message.text in str(categories[:]):
        if message.text == categories[0][0]:
            mess = 'Выберите подкатегорию крепких алкогольных напитков:'
            count_names = categories_ids.count((1,))
            f_index = categories_ids.index((1,))
            l_index = 0
            c = 0
            for j in range(len(categories_ids)):
                if categories_ids[j][0] == 1:
                    c += 1
                    if c == count_names:
                        l_index = j
                        break
            for i in range(f_index, l_index + 1):
                btn = tb.types.KeyboardButton(names_of_alcohols[i][0])
                markup.add(btn)
            btn_back = tb.types.KeyboardButton('Категории')
            last_command[0] = 'Крепкие алкогольные напитки'
            markup.add(btn_back)
            bot.send_message(message.chat.id, mess, reply_markup=markup)

        if message.text == categories[1][0]:
            mess = 'Выберите подкатегорию среднеалкогольных напитков:'
            count_names = categories_ids.count((2,))
            f_index = categories_ids.index((2,))
            l_index = 0
            c = 0
            for j in range(len(categories_ids)):
                if categories_ids[j][0] == 2:
                    c += 1
                    if c == count_names:
                        l_index = j
                        break
            for i in range(f_index, l_index + 1):
                btn = tb.types.KeyboardButton(names_of_alcohols[i][0])
                markup.add(btn)
            btn_back = tb.types.KeyboardButton('Категории')
            last_command[0] = 'Среднеалкогольные напитки'
            markup.add(btn_back)
            bot.send_message(message.chat.id, mess, reply_markup=markup)

        if message.text == categories[2][0]:
            mess = 'Выберите подкатегорию слабоалкогольных напитков:'
            count_names = categories_ids.count((3,))
            f_index = categories_ids.index((3,))
            l_index = 0
            c = 0
            for j in range(len(categories_ids)):
                if categories_ids[j][0] == 3:
                    c += 1
                    if c == count_names:
                        l_index = j
                        break
            for i in range(f_index, l_index + 1):
                btn = tb.types.KeyboardButton(names_of_alcohols[i][0])
                markup.add(btn)
            btn_back = tb.types.KeyboardButton('Категории')
            last_command[0] = 'Слабоалкогольные напитки'
            markup.add(btn_back)
            bot.send_message(message.chat.id, mess, reply_markup=markup)

    # Подкатегории
    if message.text in str(names_of_alcohols[:]):
        sub_id = names_of_alcohols.index((f'{message.text}',))
        mess = f'{str(names_of_alcohols[sub_id][0])}:'
        count_names_alc = sub_categories_ids.count((sub_id + 1,))
        f_index = sub_categories_ids.index((sub_id + 1,))
        l_index = 0
        c = 0
        for j in range(len(sub_categories_ids)):
            if sub_categories_ids[j][0] == sub_id + 1:
                c += 1
                if c == count_names_alc:
                    l_index = j
                    break
        for i in range(f_index, l_index + 1):
            tmp = names_of_drinks[i][0]
            btn = tb.types.KeyboardButton(tmp)
            markup.add(btn)
        # last_command = message.text ---> Разобраться
        btn_back = tb.types.KeyboardButton(last_command[0])
        last_command[1] = message.text
        markup.add(btn_back)
        bot.send_message(message.chat.id, mess, reply_markup=markup)

    # Названия
    if message.text in str(names_of_drinks[:]):
        db.open_connect()
        name_of_alcohol_id = db.select_table('alcohol', 1, 0, ('subcategories_id',), ('name_of_drink',),
                                             (f'{message.text}',), '')
        db.close_connect()
        names_of_alcohols_list = []
        for x in range(len(names_of_alcohols)):
            for y in range(len(names_of_alcohols[x])):
                names_of_alcohols_list.append(names_of_alcohols[x][y])
        sub_id = names_of_alcohols_list.index(f'{names_of_alcohols[name_of_alcohol_id[0][0] - 1][0]}')
        index_drink = names_of_drinks.index((f'{message.text}',))
        mess = f'{str(names_of_alcohols[sub_id][0])}: ' + str(
            names_of_drinks[index_drink][0]) + f' {str(alcohols_contents[index_drink][0])}' + '\n'
        mess += f'Стоимость ' + str(price[index_drink][0]) + '\n'
        bot.send_photo(message.chat.id, str(photos[index_drink][0]))
        mess += 'Описание: ' + str(descriptions[index_drink][0])
        btn_back = tb.types.KeyboardButton(last_command[1])
        last_command[2] = ''
        markup.add(btn_back)
        bot.send_message(message.chat.id, mess, reply_markup=markup)

    # Авторизация
    if message.text == logins[0][0]:
        if message.text in str(logins) and login_as_admin == 1:
            for i in range(len(logins)):
                if message.text == logins[i][0]:
                    mess = 'Отлично! А теперь введите пароль:'
                    bot.send_message(message.chat.id, mess)
                    break
        else:
            mess = 'К сожалению, такого логина нет!'
            btnStart = tb.types.KeyboardButton('/start')
            markup.add(btnStart)
            bot.send_message(message.chat.id, mess, reply_markup=markup)
            login_as_admin = 0

    if message.text == passwords[0][0]:
        if message.text in str(passwords) and login_as_admin == 1:
            for i in range(len(passwords)):
                if message.text == passwords[i][0]:
                    mess = 'Отлично! Вы успешно авторизировались как админ'
                    bot.send_message(message.chat.id, mess)
                    db.open_connect()
                    db.update_table('admin', ('user_condition',), ('1',), ('id',), ('1',),)
                    db.close_connect()
                    start(message)
                    break
        else:
            mess = 'К сожалению, пароль неверный!'
            btnStart = tb.types.KeyboardButton('/start')
            markup.add(btnStart)
            bot.send_message(message.chat.id, mess, reply_markup=markup)
            login_as_admin = 0


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global login_as_admin
    if call.message:
        if call.data == 'categories':
            db.open_connect()
            category_alcohol = db.select_table('category_alcohol', 0, 0, ('category',), '', '', '')
            db.close_connect()
            mess = 'Выберите категорию алкоголя:'
            markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
            for i in range(len(category_alcohol)):
                btn = tb.types.KeyboardButton(category_alcohol[i][0])
                markup.add(btn)
            btnStart = tb.types.KeyboardButton('/start')
            markup.add(btnStart)
            bot.send_message(call.message.chat.id, mess, reply_markup=markup)

        if call.data == 'suggest_entry':
            pass

        if call.data == 'login_as_admin':
            login_as_admin = 1
            mess = 'Введите логин:'
            bot.send_message(call.message.chat.id, mess)

        if call.data == 'exit':
            login_as_admin = 0
            db.open_connect()
            db.update_table('admin', ('user_condition',), ('0',), ('id',), ('1',), )
            db.close_connect()
            mess = 'Выход произведён'
            markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btnStart = tb.types.KeyboardButton('/start')
            markup.add(btnStart)
            bot.send_message(call.message.chat.id, mess, reply_markup=markup)


bot.polling(none_stop=True)
