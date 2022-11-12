import telebot as tb
from database.db_command import DataBase

bot = tb.TeleBot('5381314744:AAE1H24pXros7KCVNVJiS8e4a607I32U6WM')

db = DataBase()

last_command = ['', '', '']
login_as_admin = 0

insert_values = ['', '', '', '', '', '', '']


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


@bot.message_handler(commands=['help'])
def help_bot(message):
    mess = 'Проект Encyclopedia Of Alcohol Bot был разработан в целях выполнения задания поставленного преподавателем колледжа.' + '\n'
    markup = tb.types.InlineKeyboardMarkup()
    bot.send_message(message.chat.id, mess)
    mess = 'Связь c разработчиком:'
    btn = tb.types.InlineKeyboardButton('Мой telegram', url='https://t.me/Alex_codov')
    markup.add(btn)
    bot.send_message(message.chat.id, mess, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def text(message):
    global last_command, login_as_admin, insert_values
    markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
    db.open_connect()
    user_condition = db.select_table('admin', 1, 0, ('user_condition',), ('id',), ('1',))[0][0]
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
        if user_condition == 1:
            btnAddCategories = tb.types.KeyboardButton('Добавить категорию')
            markup.add(btnAddCategories)
        btnStart = tb.types.KeyboardButton('/start')
        markup.add(btnStart)
        bot.send_message(message.chat.id, mess, reply_markup=markup)

    if message.text in str(categories[:]):
        mess = 'Выберите нужную подкатегорию алкогольных напитков:'
        db.open_connect()
        category_id = db.select_table('category_alcohol', 1, 0, ('id',), ('category',), (f'{message.text}', ''))[0][0]
        db.close_connect()
        for i in range(len(categories_ids)):
            if categories_ids[i][0] == category_id:
                btn = tb.types.KeyboardButton(names_of_alcohols[i][0])
                markup.add(btn)
        if user_condition == 1:
            btnAddCategories = tb.types.KeyboardButton('Добавить подкатегорию')
            markup.add(btnAddCategories)
        btn_back = tb.types.KeyboardButton('Категории')
        last_command[0] = categories[category_id - 1][0]
        markup.add(btn_back)
        bot.send_message(message.chat.id, mess, reply_markup=markup)

    # Подкатегории
    if message.text in str(names_of_alcohols[:]):
        sub_id = names_of_alcohols.index((f'{message.text}',))
        mess = f'{str(names_of_alcohols[sub_id][0])}:'
        for i in range(len(sub_categories_ids)):
            if sub_categories_ids[i][0] == sub_id + 1:
                btn = tb.types.KeyboardButton(names_of_drinks[i][0])
                markup.add(btn)
        if user_condition == 1:
            btnAddCategories = tb.types.KeyboardButton('Добавить алкогольный напиток')
            markup.add(btnAddCategories)
        btn_back = tb.types.KeyboardButton(last_command[0])
        markup.add(btn_back)
        last_command[1] = message.text
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

    # Добавить категорию
    if message.text == 'Добавить категорию' and user_condition == 1:
        mess = 'Введите название новой категорию:'
        markupInline = tb.types.InlineKeyboardMarkup(row_width=1)
        btnInsert = tb.types.InlineKeyboardButton(text='Добавить категорию', callback_data='insert_categories')
        markupInline.add(btnInsert)
        bot.send_message(message.chat.id, mess, reply_markup=markupInline)
    else:
        insert_values[0] = str(message.text)

    # Добавить подкатегорию
    if message.text == 'Добавить подкатегорию' and user_condition == 1:
        mess = 'Введите ключ категории и название новой подкатегории, через *:'
        markupInline = tb.types.InlineKeyboardMarkup(row_width=1)
        btnInsert = tb.types.InlineKeyboardButton(text='Добавить подкатегорию', callback_data='insert_subcategories')
        markupInline.add(btnInsert)
        bot.send_message(message.chat.id, mess, reply_markup=markupInline)
    else:
        insert_values = str(message.text).split('*')
        pass

    # Добавить название
    if message.text == 'Добавить алкогольный напиток' and user_condition == 1:
        mess = 'Введите ключ категории, ключ подкатегории, название напитка, количество алкоголя, описание, фото (ссылка) и цену, через *'
        markupInline = tb.types.InlineKeyboardMarkup(row_width=1)
        btnInsert = tb.types.InlineKeyboardButton(text='Добавить напиток', callback_data='insert_alcohol_drink')
        markupInline.add(btnInsert)
        bot.send_message(message.chat.id, mess, reply_markup=markupInline)
    else:
        insert_values = str(message.text).split('*')
        pass


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global login_as_admin, insert_values
    db.open_connect()
    user_condition = db.select_table('admin', 1, 0, ('user_condition',), ('id',), ('1',))[0][0]
    db.close_connect()
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
            if user_condition == 1:
                btnAddCategories = tb.types.KeyboardButton('Добавить категорию')
                markup.add(btnAddCategories)
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

        if call.data == 'insert_categories':
            db.open_connect()
            db.insert_table('category_alcohol', ('category',), (insert_values[0],))
            db.close_connect()
            mess = 'Запись успешно добавлена'
            markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btnStart = tb.types.KeyboardButton('/start')
            markup.add(btnStart)
            bot.send_message(call.message.chat.id, mess, reply_markup=markup)

        if call.data == 'insert_subcategories':
            db.open_connect()
            db.insert_table('subcategories_of_alcohol', ('category_id', 'name_of_alcohol',), (insert_values[0], insert_values[1],))
            db.close_connect()
            mess = 'Запись успешно добавлена'
            markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btnStart = tb.types.KeyboardButton('/start')
            markup.add(btnStart)
            bot.send_message(call.message.chat.id, mess, reply_markup=markup)

        if call.data == 'insert_alcohol_drink':
            db.open_connect()
            db.insert_table('alcohol', ('category_id', 'subcategories_id', 'name_of_drink', 'alcohol_content', 'description', 'photo', 'price',),
                            (insert_values[0], insert_values[1], insert_values[2], insert_values[3], insert_values[4], insert_values[5], insert_values[6]))
            db.close_connect()
            mess = 'Запись успешно добавлена'
            markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btnStart = tb.types.KeyboardButton('/start')
            markup.add(btnStart)
            bot.send_message(call.message.chat.id, mess, reply_markup=markup)


bot.polling(none_stop=True)
