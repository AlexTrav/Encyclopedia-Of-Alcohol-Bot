import datetime as dt
import telebot as tb
from random import choice
from database.db_command import DataBase

bot = tb.TeleBot('5381314744:AAE1H24pXros7KCVNVJiS8e4a607I32U6WM')

db = DataBase()

last_command = ['', '', '']
login_as_admin = 0

insert_values, update_values = [''], ['']

request_values = ['']

is_category_random, is_subcategory_random = [''], ['']

user_name = ''


@bot.message_handler(commands=['start'])
def start(message):
    global user_name
    user_name = str(message.from_user.username)
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
        markup.add(btnSuggestEntry, btnLogInAsAdmin)
    if user_condition == 1:
        btnSuggestedEntries = tb.types.InlineKeyboardButton(text='Предложенные записи', callback_data='suggested_entries')
        btnExit = tb.types.InlineKeyboardButton(text='Выйти из аккаунта', callback_data='exit')
        markup.add(btnSuggestedEntries, btnExit)
    bot.send_message(message.chat.id, mess, reply_markup=markup)
    db.open_connect()
    now = dt.datetime.now()
    db.insert_table('logs', ('user_name', 'action', 'performed_time'), (user_name, message.text, now.strftime('%d-%m-%Y %H:%M:%S')))
    db.close_connect()


@bot.message_handler(commands=['help'])
def help_bot(message):
    global user_name
    user_name = str(message.from_user.username)
    mess = 'Проект Encyclopedia Of Alcohol Bot был разработан в целях выполнения задания поставленного преподавателем колледжа.' + '\n'
    markup = tb.types.InlineKeyboardMarkup()
    bot.send_message(message.chat.id, mess)
    mess = 'Связь c разработчиком:'
    btn = tb.types.InlineKeyboardButton('Мой telegram', url='https://t.me/Alex_codov')
    markup.add(btn)
    bot.send_message(message.chat.id, mess, reply_markup=markup)
    db.open_connect()
    now = dt.datetime.now()
    db.insert_table('logs', ('user_name', 'action', 'performed_time'), (user_name, message.text, now.strftime('%d-%m-%Y %H:%M:%S')))
    db.close_connect()


@bot.message_handler(content_types=['text'])
def text(message):
    global last_command, login_as_admin, insert_values, update_values, request_values, is_category_random, user_name
    user_name = str(message.from_user.username)
    markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
    db.open_connect()

    # admin
    user_condition = db.select_table('admin', 1, 0, ('user_condition',), ('id',), ('1',))[0][0]
    logins = db.select_table('admin', 0, 0, ('login',), '', '', '')
    passwords = db.select_table('admin', 0, 0, ('password',), '', '', '')

    # category_alcohol
    categories = db.select_table('category_alcohol', 0, 0, ('category',), '', '', '')
    is_visible_c = db.select_table('category_alcohol', 0, 0, ('is_visible',), '', '', '')

    # subcategories_alcohol
    categories_ids = db.select_table('subcategories_of_alcohol', 0, 0, ('category_id',), '', '', '')
    names_of_alcohols = db.select_table('subcategories_of_alcohol', 0, 0, ('name_of_alcohol',), '', '', '')
    is_visible_s = db.select_table('subcategories_of_alcohol', 0, 0, ('is_visible',), '', '', '')

    # alcohol
    sub_categories_ids = db.select_table('alcohol', 0, 0, ('subcategories_id',), '', '', '')
    names_of_drinks = db.select_table('alcohol', 0, 0, ('name_of_drink',), '', '', '')
    alcohols_contents = db.select_table('alcohol', 0, 0, ('alcohol_content',), '', '', '')
    descriptions = db.select_table('alcohol', 0, 0, ('description',), '', '', '')
    photos = db.select_table('alcohol', 0, 0, ('photo',), '', '', '')
    price = db.select_table('alcohol', 0, 0, ('price',), '', '', '')
    is_visible_a = db.select_table('alcohol', 0, 0, ('is_visible',), '', '', '')

    db.close_connect()

    # Категории
    if message.text == 'Категории':
        mess = 'Выберите категорию алкоголя:'
        markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in range(len(categories)):
            if is_visible_c[i][0] == 1:
                btn = tb.types.KeyboardButton(categories[i][0])
                markup.add(btn)
        btnRandom = tb.types.KeyboardButton('Полный рандом!')
        markup.add(btnRandom)
        if user_condition == 1:
            btnAddCategories = tb.types.KeyboardButton('Добавить категорию')
            btnUpdateCategories = tb.types.KeyboardButton('Обновить категорию')
            btnDeleteCategories = tb.types.KeyboardButton('Удалить категорию')
            markup.add(btnAddCategories, btnUpdateCategories)
            markup.add(btnDeleteCategories)
        btnStart = tb.types.KeyboardButton('/start')
        markup.add(btnStart)
        bot.send_message(message.chat.id, mess, reply_markup=markup)

    if message.text in str(categories[:]):
        mess = 'Выберите нужную подкатегорию алкогольных напитков:'
        db.open_connect()
        category_id = db.select_table('category_alcohol', 1, 0, ('id',), ('category',), (f'{message.text}', ''))[0][0]
        db.close_connect()
        for i in range(len(categories_ids)):
            if is_visible_s[i][0] == 1:
                if categories_ids[i][0] == category_id:
                    btn = tb.types.KeyboardButton(names_of_alcohols[i][0])
                    markup.add(btn)
        btnRandom = tb.types.KeyboardButton('Рандом категории!')
        markup.add(btnRandom)
        if user_condition == 1:
            btnAddCategories = tb.types.KeyboardButton('Добавить подкатегорию')
            btnUpdateSubcategories = tb.types.KeyboardButton('Обновить подкатегорию')
            btnDeleteCategories = tb.types.KeyboardButton('Удалить подкатегорию')
            markup.add(btnAddCategories, btnUpdateSubcategories)
            markup.add(btnDeleteCategories)
        btn_back = tb.types.KeyboardButton('Категории')
        last_command[0] = categories[category_id][0]
        markup.add(btn_back)
        is_category_random[0] = message.text
        bot.send_message(message.chat.id, mess, reply_markup=markup)

    # Подкатегории
    if message.text in str(names_of_alcohols[:]):
        db.open_connect()
        sub_id_subcategory = db.select_table('subcategories_of_alcohol', 1, 0, ('id',), ('name_of_alcohol',), (str(message.text),))[0][0]
        sub_id = names_of_alcohols.index((f'{message.text}',))
        db.close_connect()
        mess = f'{str(names_of_alcohols[sub_id][0])}:'
        for i in range(len(sub_categories_ids)):
            if is_visible_a[i][0] == 1:
                if sub_categories_ids[i][0] == sub_id_subcategory:
                    btn = tb.types.KeyboardButton(names_of_drinks[i][0])
                    markup.add(btn)
        btnRandom = tb.types.KeyboardButton('Рандом подкатегории!')
        markup.add(btnRandom)
        if user_condition == 1:
            btnAddCategories = tb.types.KeyboardButton('Добавить алкогольный напиток')
            btnUpdateDrink = tb.types.KeyboardButton('Обновить алкогольный напиток')
            btnDeleteCategories = tb.types.KeyboardButton('Удалить алкогольный напиток')
            markup.add(btnAddCategories, btnUpdateDrink)
            markup.add(btnDeleteCategories)
        btn_back = tb.types.KeyboardButton(last_command[0])
        markup.add(btn_back)
        last_command[1] = message.text
        is_subcategory_random[0] = message.text
        bot.send_message(message.chat.id, mess, reply_markup=markup)

    # Названия
    if message.text in str(names_of_drinks[:]) and not str(message.text).isdigit():

        # db.open_connect()
        # name_of_alcohol_id = db.select_table('alcohol', 1, 0, ('subcategories_id',), ('name_of_drink',), (f'{message.text}',), '')
        # db.close_connect()

        names_of_alcohols_list = []

        for x in range(len(names_of_alcohols)):
            for y in range(len(names_of_alcohols[x])):
                names_of_alcohols_list.append(names_of_alcohols[x][y])

        sub_id = names_of_alcohols_list.index(last_command[1])

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

    # [0]:
    # Добавить категорию
    if message.text == 'Добавить категорию' and user_condition == 1:
        mess = 'Введите название новой категорию:'
        markupInline = tb.types.InlineKeyboardMarkup(row_width=1)
        btnInsert = tb.types.InlineKeyboardButton(text='Добавить категорию', callback_data='insert_categories')
        markupInline.add(btnInsert)
        bot.send_message(message.chat.id, mess, reply_markup=markupInline)
    else:
        insert_values[0] = str(message.text)

    # Удалить категорию
    if message.text == 'Удалить категорию' and user_condition == 1:
        mess = 'Введите ключ категории:'
        markupInline = tb.types.InlineKeyboardMarkup(row_width=1)
        btnInsert = tb.types.InlineKeyboardButton(text='Удалить категорию', callback_data='delete_category')
        markupInline.add(btnInsert)
        bot.send_message(message.chat.id, mess, reply_markup=markupInline)
    else:
        update_values[0] = message.text

    # Удалить подкатегорию
    if message.text == 'Удалить подкатегорию' and user_condition == 1:
        mess = 'Введите ключ подкатегории:'
        markupInline = tb.types.InlineKeyboardMarkup(row_width=1)
        btnInsert = tb.types.InlineKeyboardButton(text='Удалить подкатегорию', callback_data='delete_subcategory')
        markupInline.add(btnInsert)
        bot.send_message(message.chat.id, mess, reply_markup=markupInline)
    else:
        update_values[0] = message.text

    # Удалить алкогольный напиток
    if message.text == 'Удалить алкогольный напиток' and user_condition == 1:
        mess = 'Введите ключ алкогольного напитка:'
        markupInline = tb.types.InlineKeyboardMarkup(row_width=1)
        btnInsert = tb.types.InlineKeyboardButton(text='Удалить алкогольный напиток', callback_data='delete_alcohol_drink')
        markupInline.add(btnInsert)
        bot.send_message(message.chat.id, mess, reply_markup=markupInline)
    else:
        update_values[0] = message.text

    # Предложить запись
    # Категорию
    if message.text == 'Предложить категорию':
        mess = 'Введите название новой категории:'
        markupInline = tb.types.InlineKeyboardMarkup(row_width=1)
        btnRequestCategoryInline = tb.types.InlineKeyboardButton(text='Предложить категорию', callback_data='request_category')
        markupInline.add(btnRequestCategoryInline)
        bot.send_message(message.chat.id, mess, reply_markup=markupInline)
    else:
        request_values[0] = message.text

    # Посмотреть предложеные записи
    # Категории
    if message.text == 'Посмотреть предложенные категории' and user_condition == 1:
        mess = 'Всего предложенных категорий: '
        db.open_connect()
        request_id = db.select_table('category_alcohol', 1, 0, ('id',), ('is_visible',), (0,), '')
        request_categories = db.select_table('category_alcohol', 1, 0, ('category',), ('is_visible',), (0,), '')
        db.close_connect()
        if len(request_id) > 0:
            mess += str(len(request_categories)) + '\n'
            markupInline = tb.types.InlineKeyboardMarkup(row_width=2)
            for i in range(len(request_id)):
                mess += 'id -> ' + str(request_id[i][0]) + '||' + 'category -> ' + str(request_categories[i][0]) + '\n'
            mess += 'Введите id и нажмите одну из кнопок.'
            btnAllow = tb.types.InlineKeyboardButton(text='Добавить запись', callback_data='insert_allow_category')
            btnBan = tb.types.InlineKeyboardButton(text='Удалить запись', callback_data='delete_ban_category')
            markupInline.add(btnAllow, btnBan)
            bot.send_message(message.chat.id, mess, reply_markup=markupInline)
        else:
            mess += 'К сожалению предложенных записей нет, увы!'
            bot.send_message(message.chat.id, mess)
    else:
        request_values[0] = message.text

    # Подкатегории
    if message.text == 'Посмотреть предложенные подкатегории' and user_condition == 1:
        mess = 'Всего предложенных подкатегорий: '
        db.open_connect()
        request_id = db.select_table('subcategories_of_alcohol', 1, 0, ('id',), ('is_visible',), (0,), '')
        request_categories_id = db.select_table('subcategories_of_alcohol', 1, 0, ('category_id',), ('is_visible',), (0,), '')
        request_subcategories = db.select_table('subcategories_of_alcohol', 1, 0, ('name_of_alcohol',), ('is_visible',), (0,), '')
        db.close_connect()
        if len(request_id) > 0:
            mess += str(len(request_subcategories)) + '\n'
            markupInline = tb.types.InlineKeyboardMarkup(row_width=2)
            for i in range(len(request_id)):
                mess += 'id -> ' + str(request_id[i][0]) + '|| category_id -> ' + str(request_categories_id[i][0]) + '|| name_of_alcohol -> ' + str(request_subcategories[i][0]) + '\n'
            mess += 'Введите id и нажмите одну из кнопок.'
            btnAllow = tb.types.InlineKeyboardButton(text='Добавить запись', callback_data='insert_allow_subcategory')
            btnBan = tb.types.InlineKeyboardButton(text='Удалить запись', callback_data='delete_ban_subcategory')
            markupInline.add(btnAllow, btnBan)
            bot.send_message(message.chat.id, mess, reply_markup=markupInline)
        else:
            mess += 'К сожалению предложенных записей нет, увы!'
            bot.send_message(message.chat.id, mess)
    else:
        request_values[0] = message.text

    # Напитки
    if message.text == 'Посмотреть предложенные алкогольные напитки' and user_condition == 1:
        mess = 'Всего предложенных алкогольных напитков: '
        db.open_connect()
        request_id = db.select_table('alcohol', 1, 0, ('id',), ('is_visible',), (0,), '')
        request_categories_id = db.select_table('alcohol', 1, 0, ('category_id',), ('is_visible',), (0,), '')
        request_subcategories_id = db.select_table('alcohol', 1, 0, ('subcategories_id',), ('is_visible',), (0,), '')
        request_name_of_drink = db.select_table('alcohol', 1, 0, ('name_of_drink',), ('is_visible',), (0,), '')
        request_alcohol_content = db.select_table('alcohol', 1, 0, ('alcohol_content',), ('is_visible',), (0,), '')
        request_description = db.select_table('alcohol', 1, 0, ('description',), ('is_visible',), (0,), '')
        request_photo = db.select_table('alcohol', 1, 0, ('photo',), ('is_visible',), (0,), '')
        request_price = db.select_table('alcohol', 1, 0, ('price',), ('is_visible',), (0,), '')
        db.close_connect()
        if len(request_id) > 0:
            mess += str(len(request_name_of_drink)) + '\n'
            markupInline = tb.types.InlineKeyboardMarkup(row_width=2)
            for i in range(len(request_id)):
                mess += f'id -> {str(request_id[i][0])}' + f'|| category_id -> {str(request_categories_id[i][0])}' + \
                        f'|| subcategory_id -> {str(request_subcategories_id[i][0])}' + f'|| name_of_alcohol -> {str(request_name_of_drink[i][0])}' + \
                        f'|| alcohol_content -> {str(request_alcohol_content[i][0])}' + f'|| description -> {str(request_description[i][0])}' + \
                        f'|| photo -> {str(request_photo[i][0])}' + f'|| price -> {str(request_price[i][0])}' + '\n'
            mess += 'Введите id и нажмите одну из кнопок.'
            btnAllow = tb.types.InlineKeyboardButton(text='Добавить запись', callback_data='insert_allow_alcohol_drink')
            btnBan = tb.types.InlineKeyboardButton(text='Удалить запись', callback_data='delete_ban_alcohol_drink')
            markupInline.add(btnAllow, btnBan)
            bot.send_message(message.chat.id, mess, reply_markup=markupInline)
        else:
            mess += 'К сожалению предложенных записей нет, увы!'
            bot.send_message(message.chat.id, mess)
    else:
        request_values[0] = message.text

    # Полный рандом
    if message.text == 'Полный рандом!':
        db.open_connect()
        random_alcohol_drink = choice(db.select_table('alcohol', 0, 1))
        db.close_connect()
        markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        mess = f'Ваш напиток: {random_alcohol_drink[3]} {random_alcohol_drink[4]}' + '\n'
        mess += f'Стоимость: {random_alcohol_drink[7]}' + '\n'
        mess += f'Описание: {random_alcohol_drink[5]}' + '\n'
        btn_again = tb.types.KeyboardButton('Полный рандом!')
        btn_start = tb.types.KeyboardButton('/start')
        markup.add(btn_again, btn_start)
        mess += 'Фото:'
        bot.send_message(message.chat.id, mess, reply_markup=markup)
        bot.send_photo(message.chat.id, str(random_alcohol_drink[6]))

    # Рандом категории!
    if message.text == 'Рандом категории!':
        db.open_connect()
        category_value = db.select_table('category_alcohol', 1, 0, ('id', 'category'), ('is_visible',), (1,))
        category_id = 0
        for i in range(len(category_value)):
            if category_value[i][1] == is_category_random[0]:
                category_id = category_value[i][0]
                break
        random_alcohol_drink_category = choice(db.select_table('alcohol', 1, 1, '', ('category_id',), (category_id,)))
        db.close_connect()
        markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        mess = f'Ваш напиток: {random_alcohol_drink_category[3]} {random_alcohol_drink_category[4]}' + '\n'
        mess += f'Стоимость: {random_alcohol_drink_category[7]}' + '\n'
        mess += f'Описание: {random_alcohol_drink_category[5]}' + '\n'
        btn_again = tb.types.KeyboardButton('Рандом категории!')
        btn_start = tb.types.KeyboardButton('/start')
        markup.add(btn_again, btn_start)
        mess += 'Фото:'
        bot.send_message(message.chat.id, mess, reply_markup=markup)
        bot.send_photo(message.chat.id, str(random_alcohol_drink_category[6]))

    # Рандом подкатегории!
    if message.text == 'Рандом подкатегории!':
        db.open_connect()
        category_value = db.select_table('category_alcohol', 1, 0, ('id', 'category'), ('is_visible',), (1,))
        subcategory_value = db.select_table('subcategories_of_alcohol', 1, 0, ('id', 'name_of_alcohol'), ('is_visible',), (1,))
        category_id = 0
        subcategory_id = 0
        for i in range(len(category_value)):
            if category_value[i][1] == is_category_random[0]:
                category_id = category_value[i][0]
                break
        for j in range(len(subcategory_value)):
            if subcategory_value[j][1] == is_subcategory_random[0]:
                subcategory_id = subcategory_value[j][0]
                break
        random_alcohol_drink_subcategory = choice(db.select_table('alcohol', 1, 1, '', ('category_id', 'subcategories_id'), (category_id, subcategory_id), ' AND '))
        db.close_connect()
        markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        mess = f'Ваш напиток: {random_alcohol_drink_subcategory[3]} {random_alcohol_drink_subcategory[4]}' + '\n'
        mess += f'Стоимость: {random_alcohol_drink_subcategory[7]}' + '\n'
        mess += f'Описание: {random_alcohol_drink_subcategory[5]}' + '\n'
        btn_again = tb.types.KeyboardButton('Рандом подкатегории!')
        btn_start = tb.types.KeyboardButton('/start')
        markup.add(btn_again, btn_start)
        mess += 'Фото:'
        bot.send_message(message.chat.id, mess, reply_markup=markup)
        bot.send_photo(message.chat.id, str(random_alcohol_drink_subcategory[6]))

    # split():
    # Добавить подкатегорию
    if message.text == 'Добавить подкатегорию' and user_condition == 1:
        mess = 'Введите ключ категории и название новой подкатегории, через  ||:'
        markupInline = tb.types.InlineKeyboardMarkup(row_width=1)
        btnInsert = tb.types.InlineKeyboardButton(text='Добавить подкатегорию', callback_data='insert_subcategories')
        markupInline.add(btnInsert)
        bot.send_message(message.chat.id, mess, reply_markup=markupInline)
    else:
        insert_values = str(message.text).split('||')
        pass

    # Добавить название
    if message.text == 'Добавить алкогольный напиток' and user_condition == 1:
        mess = 'Введите ключ категории, ключ подкатегории, название напитка, количество алкоголя, описание, фото (ссылка) и цену, через ||'
        markupInline = tb.types.InlineKeyboardMarkup(row_width=1)
        btnInsert = tb.types.InlineKeyboardButton(text='Добавить напиток', callback_data='insert_alcohol_drink')
        markupInline.add(btnInsert)
        bot.send_message(message.chat.id, mess, reply_markup=markupInline)
    else:
        insert_values = str(message.text).split('||')
        pass

    # Подкатегорию
    if message.text == 'Предложить подкатегорию':
        mess = 'Введите ключ категории и название новой подкатегории, через ||:'
        markupInline = tb.types.InlineKeyboardMarkup(row_width=1)
        btnRequestSubcategoryInline = tb.types.InlineKeyboardButton(text='Предложить подкатегорию',
                                                                    callback_data='request_subcategory')
        markupInline.add(btnRequestSubcategoryInline)
        bot.send_message(message.chat.id, mess, reply_markup=markupInline)
    else:
        request_values = message.text.split('||')
        print()

    # Напитки
    if message.text == 'Предложить алкогольный напиток':
        mess = 'Введите ключ категории, ключ подкатегории, название алкогольного напитка, количество алкоголя, описание, фото (ссылкой) и примерную цену, через ||:'
        markupInline = tb.types.InlineKeyboardMarkup(row_width=1)
        btnRequestAlcoholDrinkInline = tb.types.InlineKeyboardButton(text='Предложить алкогольный напиток',
                                                                     callback_data='request_alcohol_drink')
        markupInline.add(btnRequestAlcoholDrinkInline)
        bot.send_message(message.chat.id, mess, reply_markup=markupInline)
    else:
        request_values = str(message.text).split('||')

    # Обновить категорию
    if message.text == 'Обновить категорию' and user_condition == 1:
        mess = 'Введите ключ категории и новое название категории, через ||:'
        markupInline = tb.types.InlineKeyboardMarkup(row_width=1)
        btnInsert = tb.types.InlineKeyboardButton(text='Обновить категорию', callback_data='update_category')
        markupInline.add(btnInsert)
        bot.send_message(message.chat.id, mess, reply_markup=markupInline)
    else:
        update_values = str(message.text).split('||')

    # Обновить подкатегорию
    if message.text == 'Обновить подкатегорию' and user_condition == 1:
        mess = 'Введите ключ подкатегории, новый ключ категории и новое название подкатегории, через ||:'
        markupInline = tb.types.InlineKeyboardMarkup(row_width=1)
        btnInsert = tb.types.InlineKeyboardButton(text='Обновить подкатегорию', callback_data='update_subcategory')
        markupInline.add(btnInsert)
        bot.send_message(message.chat.id, mess, reply_markup=markupInline)
    else:
        update_values = str(message.text).split('||')

    # Обновить алкогольный напиток
    if message.text == 'Обновить алкогольный напиток' and user_condition == 1:
        mess = 'Введите ключ алкогольного напитка, новый ключ категории, новый ключ подкатегории,' \
               ' новое название, новое количество алкоголя, новое описание, новое фото (ссылкой), новую примерную цену, через ||:'
        markupInline = tb.types.InlineKeyboardMarkup(row_width=1)
        btnInsert = tb.types.InlineKeyboardButton(text='Обновить алкогольный напиток',
                                                  callback_data='update_alcohol_drink')
        markupInline.add(btnInsert)
        bot.send_message(message.chat.id, mess, reply_markup=markupInline)
    else:
        update_values = str(message.text).split('||')

    db.open_connect()
    now = dt.datetime.now()
    db.insert_table('logs', ('user_name', 'action', 'performed_time'), (user_name, message.text, now.strftime('%d-%m-%Y %H:%M:%S')))
    db.close_connect()


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global login_as_admin, insert_values, request_values, user_name
    db.open_connect()
    user_condition = db.select_table('admin', 1, 0, ('user_condition',), ('id',), ('1',))[0][0]
    is_visible_c = db.select_table('category_alcohol', 0, 0, ('is_visible',), '', '', '')
    db.close_connect()
    if call.message:
        # Категории
        if call.data == 'categories':
            db.open_connect()
            category_alcohol = db.select_table('category_alcohol', 0, 0, ('category',), '', '', '')
            db.close_connect()
            mess = 'Выберите категорию алкоголя:'
            markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
            for i in range(len(category_alcohol)):
                if is_visible_c[i][0] == 1:
                    btn = tb.types.KeyboardButton(category_alcohol[i][0])
                    markup.add(btn)
            btnRandom = tb.types.KeyboardButton('Полный рандом!')
            markup.add(btnRandom)
            if user_condition == 1:
                btnAddCategories = tb.types.KeyboardButton('Добавить категорию')
                btnUpdateCategories = tb.types.KeyboardButton('Обновить категорию')
                btnDeleteCategories = tb.types.KeyboardButton('Удалить категорию')
                markup.add(btnAddCategories, btnUpdateCategories)
                markup.add(btnDeleteCategories)
            btnStart = tb.types.KeyboardButton('/start')
            markup.add(btnStart)
            bot.send_message(call.message.chat.id, mess, reply_markup=markup)

        # Предложить запись
        if call.data == 'suggest_entry':
            mess = 'Выберите нужное действие:'
            markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btnRequestCategory = tb.types.KeyboardButton('Предложить категорию')
            btnRequestSubcategory = tb.types.KeyboardButton('Предложить подкатегорию')
            btnRequestAlcoholDrink = tb.types.KeyboardButton('Предложить алкогольный напиток')
            btnStart = tb.types.KeyboardButton('/start')
            markup.add(btnRequestCategory, btnRequestSubcategory, btnRequestAlcoholDrink, btnStart)
            bot.send_message(call.message.chat.id, mess, reply_markup=markup)

        # Предложенные записи
        if call.data == 'suggested_entries':
            mess = 'Выберите нужное действие:'
            markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btnRequestCategory = tb.types.KeyboardButton('Посмотреть предложенные категории')
            btnRequestSubcategory = tb.types.KeyboardButton('Посмотреть предложенные подкатегории')
            btnRequestAlcoholDrink = tb.types.KeyboardButton('Посмотреть предложенные алкогольные напитки')
            btnStart = tb.types.KeyboardButton('/start')
            markup.add(btnRequestCategory, btnRequestSubcategory, btnRequestAlcoholDrink, btnStart)
            bot.send_message(call.message.chat.id, mess, reply_markup=markup)

        # Авторизация
        if call.data == 'login_as_admin':
            login_as_admin = 1
            mess = 'Введите логин:'
            bot.send_message(call.message.chat.id, mess)

        # Выход
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

        # Добавить категорию
        if call.data == 'insert_categories' and user_condition == 1:
            db.open_connect()
            db.insert_table('category_alcohol', ('category', 'is_visible',), (insert_values[0], '1',))
            db.close_connect()
            mess = 'Запись успешно добавлена'
            markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btnStart = tb.types.KeyboardButton('/start')
            markup.add(btnStart)
            bot.send_message(call.message.chat.id, mess, reply_markup=markup)

        # Добавить подкатегорию
        if call.data == 'insert_subcategories' and user_condition == 1:
            db.open_connect()
            db.insert_table('subcategories_of_alcohol', ('category_id', 'name_of_alcohol', 'is_visible',), (insert_values[0], insert_values[1], '1',))
            db.close_connect()
            mess = 'Запись успешно добавлена'
            markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btnStart = tb.types.KeyboardButton('/start')
            markup.add(btnStart)
            bot.send_message(call.message.chat.id, mess, reply_markup=markup)

        # Добавить название
        if call.data == 'insert_alcohol_drink' and user_condition == 1:
            db.open_connect()
            db.insert_table('alcohol', ('category_id', 'subcategories_id', 'name_of_drink', 'alcohol_content', 'description', 'photo', 'price', 'is_visible',),
                            (insert_values[0], insert_values[1], insert_values[2], insert_values[3], insert_values[4], insert_values[5], insert_values[6], '1',))
            db.close_connect()
            mess = 'Запись успешно добавлена'
            markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btnStart = tb.types.KeyboardButton('/start')
            markup.add(btnStart)
            bot.send_message(call.message.chat.id, mess, reply_markup=markup)

        # Обновить категорию
        if call.data == 'update_category' and user_condition == 1:
            db.open_connect()
            db.update_table('category_alcohol', ('category',), (update_values[1],), ('id',), (update_values[0],), '')
            db.close_connect()
            mess = 'Запись успешно обновлена'
            markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btnStart = tb.types.KeyboardButton('/start')
            markup.add(btnStart)
            bot.send_message(call.message.chat.id, mess, reply_markup=markup)

        # Обновить подкатегорию
        if call.data == 'update_subcategory' and user_condition == 1:
            db.open_connect()
            db.update_table('subcategories_of_alcohol', ('category_id', 'name_of_alcohol',), (update_values[1], update_values[2]), ('id',), (update_values[0],), '')
            db.close_connect()
            mess = 'Запись успешно обновлена'
            markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btnStart = tb.types.KeyboardButton('/start')
            markup.add(btnStart)
            bot.send_message(call.message.chat.id, mess, reply_markup=markup)

        # Обновить алкогольный напиток
        if call.data == 'update_alcohol_drink' and user_condition == 1:
            db.open_connect()
            db.update_table('alcohol', ('category_id', 'subcategories_id', 'name_of_drink', 'alcohol_content', 'description', 'photo', 'price'),
                            (update_values[1], update_values[2], update_values[3], update_values[4], update_values[5], update_values[6], update_values[7]),
                            ('id',), (update_values[0],), '')
            db.close_connect()
            mess = 'Запись успешно обновлена'
            markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btnStart = tb.types.KeyboardButton('/start')
            markup.add(btnStart)
            bot.send_message(call.message.chat.id, mess, reply_markup=markup)

        # Удалить категорию
        if call.data == 'delete_category' and user_condition == 1:
            db.open_connect()
            db.update_table('category_alcohol', ('is_visible',), (0,), ('id',), (update_values[0],), '')
            db.close_connect()
            mess = 'Запись успешно удалена'
            markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btnStart = tb.types.KeyboardButton('/start')
            markup.add(btnStart)
            bot.send_message(call.message.chat.id, mess, reply_markup=markup)

        # Удалить подкатегорию
        if call.data == 'delete_subcategory' and user_condition == 1:
            db.open_connect()
            db.update_table('subcategories_of_alcohol', ('is_visible',), (0,), ('id',), (update_values[0],), '')
            db.close_connect()
            mess = 'Запись успешно удалена'
            markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btnStart = tb.types.KeyboardButton('/start')
            markup.add(btnStart)
            bot.send_message(call.message.chat.id, mess, reply_markup=markup)

        # Удалить алкогольный напиток
        if call.data == 'delete_alcohol_drink' and user_condition == 1:
            db.open_connect()
            db.update_table('alcohol', ('is_visible',), (0,), ('id',), (update_values[0],), '')
            db.close_connect()
            mess = 'Запись успешно удалена'
            markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btnStart = tb.types.KeyboardButton('/start')
            markup.add(btnStart)
            bot.send_message(call.message.chat.id, mess, reply_markup=markup)

        # <- от Предложить запись
        # Выполнить insert для категорий от пользователя
        if call.data == 'request_category':
            db.open_connect()
            db.insert_table('category_alcohol', ('category',), (request_values[0],))
            db.close_connect()
            mess = 'Запись успешно предложена'
            markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btnStart = tb.types.KeyboardButton('/start')
            markup.add(btnStart)
            bot.send_message(call.message.chat.id, mess, reply_markup=markup)

        # Выполнить insert для подкатегорий от пользователя
        if call.data == 'request_subcategory':
            db.open_connect()
            db.insert_table('subcategories_of_alcohol', ('category_id', 'name_of_alcohol'), (request_values[0], request_values[1]))
            db.close_connect()
            mess = 'Запись успешно предложена'
            markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btnStart = tb.types.KeyboardButton('/start')
            markup.add(btnStart)
            bot.send_message(call.message.chat.id, mess, reply_markup=markup)

        # Выполнить insert для алкогольных напитков от пользователя
        if call.data == 'request_alcohol_drink':
            db.open_connect()
            db.insert_table('alcohol', ('category_id', 'subcategories_id', 'name_of_drink', 'alcohol_content', 'description', 'photo', 'price'),
                            (request_values[0], request_values[1], request_values[2], request_values[3], request_values[4], request_values[5], request_values[6]))
            db.close_connect()
            mess = 'Запись успешно предложена'
            markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btnStart = tb.types.KeyboardButton('/start')
            markup.add(btnStart)
            bot.send_message(call.message.chat.id, mess, reply_markup=markup)

        # <- от Предложенные записи
        # Категории
        # Разрешить категорию
        if call.data == 'insert_allow_category':
            db.open_connect()
            db.update_table('category_alcohol', ('is_visible',), (1,), ('id',), (request_values[0],), '')
            db.close_connect()
            mess = 'Запись успешно разрешена'
            markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btnStart = tb.types.KeyboardButton('/start')
            markup.add(btnStart)
            bot.send_message(call.message.chat.id, mess, reply_markup=markup)
        # Запретить категорию
        if call.data == 'delete_ban_category':
            db.open_connect()
            db.delete_table('category_alcohol', request_values[0])
            db.close_connect()
            mess = 'Запись успешно удалена из таблицы'
            markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btnStart = tb.types.KeyboardButton('/start')
            markup.add(btnStart)
            bot.send_message(call.message.chat.id, mess, reply_markup=markup)

        # Подкатегории
        # Разрешить подкатегорию
        if call.data == 'insert_allow_subcategory':
            db.open_connect()
            db.update_table('subcategories_of_alcohol', ('is_visible',), (1,), ('id',), (request_values[0],), '')
            db.close_connect()
            mess = 'Запись успешно разрешена'
            markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btnStart = tb.types.KeyboardButton('/start')
            markup.add(btnStart)
            bot.send_message(call.message.chat.id, mess, reply_markup=markup)
        # Запретить подкатегорию
        if call.data == 'delete_ban_subcategory':
            db.open_connect()
            db.delete_table('subcategories_of_alcohol', request_values[0])
            db.close_connect()
            mess = 'Запись успешно удалена из таблицы'
            markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btnStart = tb.types.KeyboardButton('/start')
            markup.add(btnStart)
            bot.send_message(call.message.chat.id, mess, reply_markup=markup)

        # Алкогольные напитки
        # Разрешить напиток
        if call.data == 'insert_allow_alcohol_drink':
            db.open_connect()
            db.update_table('alcohol', ('is_visible',), (1,), ('id',), (request_values[0],), '')
            db.close_connect()
            mess = 'Запись успешно разрешена'
            markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btnStart = tb.types.KeyboardButton('/start')
            markup.add(btnStart)
            bot.send_message(call.message.chat.id, mess, reply_markup=markup)
        # Запретить напиток
        if call.data == 'delete_ban_alcohol_drink':
            db.open_connect()
            db.delete_table('alcohol', request_values[0])
            db.close_connect()
            mess = 'Запись успешно удалена из таблицы'
            markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btnStart = tb.types.KeyboardButton('/start')
            markup.add(btnStart)
            bot.send_message(call.message.chat.id, mess, reply_markup=markup)

    db.open_connect()
    now = dt.datetime.now()
    db.insert_table('logs', ('user_name', 'action', 'performed_time'), (user_name, str(call.data), now.strftime('%d-%m-%Y %H:%M:%S')))
    db.close_connect()


bot.polling(none_stop=True)
