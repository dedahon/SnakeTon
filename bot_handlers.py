import time
from telebot import types
from translations import translations
from bot_helpers import is_user_subscribed, add_user_to_subscribed_list

class BotHandlers:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        self.correct_answers_count = 0
        self.marked_users_quiz = {}

    def register_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.start_message(message)

        @self.bot.callback_query_handler(func=lambda call: call.data == 'prof')
        def profile(call):
            self.handle_profile(call)

        @self.bot.callback_query_handler(func=lambda call: call.data == 'back')
        def back_callback(call):
            self.handle_back(call)

        @self.bot.callback_query_handler(func=lambda call: call.data == 'canal')
        def canal(call):
            self.handle_canal(call)

        @self.bot.callback_query_handler(func=lambda call: call.data == 'check')
        def check_subscription(call):
            self.handle_check_subscription(call)

        @self.bot.callback_query_handler(func=lambda call: call.data == 'zadanie')
        def zadanie(call):
            self.handle_zadanie(call)

        @self.bot.callback_query_handler(func=lambda call: call.data == 'quiz')
        def quiz(call):
            self.handle_quiz(call)

        @self.bot.callback_query_handler(func=lambda call: call.data == 'start_game')
        def start_game(call):
            self.handle_start_game(call)

        @self.bot.callback_query_handler(func=lambda call: call.data.startswith('answer_'))
        def handle_quiz_reply(call):
            self.handle_quiz_reply(call)

        @self.bot.callback_query_handler(func=lambda call: call.data == 'druz')
        def friends(call):
            self.handle_friends(call)

        @self.bot.callback_query_handler(func=lambda call: call.data == 'soc')
        def social_networks(call):
            self.handle_social_networks(call)

        @self.bot.callback_query_handler(func=lambda call: call.data == 'smena')
        def change_language(call):
            self.handle_change_language(call)

        @self.bot.callback_query_handler(func=lambda call: call.data == 'confirm_language_change')
        def confirm_language_change(call):
            self.handle_confirm_language_change(call)

        @self.bot.callback_query_handler(func=lambda call: call.data == 'doska')
        def doska_pocheta(call):
            self.handle_doska_pocheta(call)

    def start_message(self, message, language=None):
        user_id = message.from_user.id
        if language is None:
            result = self.db.execute_query('SELECT language FROM users_points WHERE user_id = ?', (user_id,))
            current_language = result[0][0] if result else 'ru'
        else:
            current_language = language

        users_count = self.db.execute_query('SELECT COUNT(user_id) FROM users_points')[0][0]

        tr = translations[current_language]
        markup = types.InlineKeyboardMarkup()
        bt1 = types.InlineKeyboardButton(tr['profile'], callback_data='prof')
        bt2 = types.InlineKeyboardButton(tr['tasks'], callback_data='zadanie')
        bt3 = types.InlineKeyboardButton(tr['leaderboard'], callback_data='doska')
        bt4 = types.InlineKeyboardButton(tr['friends'], callback_data='druz')
        bt5 = types.InlineKeyboardButton(tr['social_networks'], callback_data='soc')
        bt6 = types.InlineKeyboardButton(tr['change_language'], callback_data='smena')
        markup.row(bt1, bt2)
        markup.row(bt3, bt4)
        markup.row(bt5)
        markup.row(bt6)

        photo_start = 'https://ibb.co/n7z5Tfs'
        self.bot.send_photo(message.chat.id, photo_start, tr['welcome'] + str(users_count), reply_markup=markup, parse_mode='Markdown')

    def handle_profile(self, call):
        self.bot.delete_message(call.message.chat.id, call.message.message_id)
        result = self.db.execute_query('SELECT points, language FROM users_points WHERE user_id = ?', (call.message.chat.id,))
        points_text = str(result[0][0]) if result and result[0][0] else translations[result[0][1]]['not_working']
        current_language = result[0][1]

        tr = translations[current_language]

        markup = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton(tr['back'], callback_data='back')
        markup.row(back_button)
        photo_profile = 'https://ibb.co/19Lttzb'
        self.bot.send_photo(call.message.chat.id, photo_profile, tr['nest'].format(points_text=points_text), reply_markup=markup)

    def handle_back(self, call):
        user_id = call.from_user.id
        result = self.db.execute_query('SELECT language FROM users_points WHERE user_id = ?', (user_id,))
        current_language = result[0][0]

        self.bot.delete_message(call.message.chat.id, call.message.message_id)
        self.start_message(call.message, language=current_language)

    def handle_canal(self, call):
        user_id = call.from_user.id
        username = call.from_user.username
        result = self.db.execute_query('SELECT language FROM users_points WHERE user_id = ?', (user_id,))
        current_language = result[0][0]

        tr = translations[current_language]

        if is_user_subscribed(user_id, '@ggttgem'):
            add_user_to_subscribed_list(user_id, username, self.db)
            message = tr['subscribed']
            markup = types.InlineKeyboardMarkup()
            back_button = types.InlineKeyboardButton(tr['back'], callback_data='back')
            markup.row(back_button)
        else:
            result = self.db.execute_query("SELECT invited_by FROM users_points WHERE user_id = ?", (user_id,))
            referrer_id = result[0][0]

            if referrer_id:
                self.db.execute_update("UPDATE users_points SET points = points + 1000 WHERE user_id = ?", (referrer_id,))

            message = tr['join_channel']
            markup = types.InlineKeyboardMarkup()
            check_button = types.InlineKeyboardButton(tr['verify'], callback_data='check')
            back_button = types.InlineKeyboardButton(tr['back'], callback_data='back')
            markup.row(check_button)
            markup.row(back_button)

        self.bot.send_message(call.message.chat.id, message, reply_markup=markup, parse_mode='HTML')

    def handle_check_subscription(self, call):
        user_id = call.from_user.id
        chat_id = call.message.chat.id
        username = call.from_user.username
        result = self.db.execute_query('SELECT language FROM users_points WHERE user_id = ?', (user_id,))
        current_language = result[0][0]

        tr = translations[current_language]

        if is_user_subscribed(user_id, '@ggttgem'):
            add_user_to_subscribed_list(user_id, username, self.db)
            message = tr['subscribed']
            self.bot.delete_message(chat_id, call.message.message_id)
            markup = types.InlineKeyboardMarkup()
            back_button = types.InlineKeyboardButton(tr['back'], callback_data='back')
            markup.row(back_button)
            self.bot.send_message(chat_id, message, reply_markup=markup)
        else:
            message = tr['not_subscribed']
            self.bot.answer_callback_query(call.id, text=message)

    def handle_zadanie(self, call):
        user_id = call.from_user.id
        result = self.db.execute_query('SELECT tasks_completed, language FROM users_points WHERE user_id = ?', (user_id,))
        tasks_completed = result[0][0] if result and result[0][0] else ''
        current_language = result[0][1]

        tr = translations[current_language]

        markup = types.InlineKeyboardMarkup()

        if 'canal' not in tasks_completed:
            canal_button = types.InlineKeyboardButton(tr['join_family'], callback_data='canal')
            markup.row(canal_button)

        if 'quiz' not in tasks_completed:
            quiz_button = types.InlineKeyboardButton(tr['prove'], callback_data='quiz')
            markup.row(quiz_button)

        back_button = types.InlineKeyboardButton(tr['back'], callback_data='back')
        markup.row(back_button)
        
        photo_zadaniya = 'https://ibb.co/wg5gDzd'
        self.bot.send_photo(call.message.chat.id, photo_zadaniya, tr['tasks_intro'], reply_markup=markup)

    def handle_quiz(self, call):
        user_id = call.from_user.id
        self.marked_users_quiz[user_id] = True
        result = self.db.execute_query('SELECT language FROM users_points WHERE user_id = ?', (user_id,))
        current_language = result[0][0]

        tr = translations[current_language]

        markup = types.InlineKeyboardMarkup()
        start_button = types.InlineKeyboardButton(tr['start_game'], callback_data='start_game')
        back_button = types.InlineKeyboardButton(tr['back'], callback_data='back')
        markup.row(start_button)
        markup.row(back_button)

        self.bot.send_message(call.message.chat.id, tr['quiz_message'], reply_markup=markup)

    def handle_start_game(self, call):
        self.correct_answers_count = 0
        self.bot.delete_message(call.message.chat.id, call.message.message_id)
        self.send_next_question(call.message.chat.id, 1)

    def send_next_question(self, chat_id, question_number):
        result = self.db.execute_query('SELECT language FROM users_points WHERE user_id = ?', (chat_id,))
        current_language = result[0][0]

        tr = translations[current_language]
        question_data = tr['questions'].get(question_number)
        if not question_data:
            return

        markup = types.InlineKeyboardMarkup()
        for option in question_data['options']:
            callback_data = f"answer_{question_number}_{option}"
            markup.add(types.InlineKeyboardButton(option, callback_data=callback_data))

        self.bot.send_message(chat_id, tr['question_number'].format(question_number=question_number, question=question_data['question']), reply_markup=markup)

    def handle_quiz_reply(self, call):
        user_id = call.from_user.id
        data = call.data.split('_')
        question_number = int(data[1])
        answer = data[2]

        result = self.db.execute_query('SELECT language FROM users_points WHERE user_id = ?', (user_id,))
        current_language = result[0][0]

        tr = translations[current_language]

        question_data = tr['questions'].get(question_number)
        if question_data and answer == question_data['correct_answer']:
            self.correct_answers_count += 1

        self.bot.delete_message(call.message.chat.id, call.message.message_id)

        if question_number < len(tr['questions']):
            self.send_next_question(call.message.chat.id, question_number + 1)
        else:
            points_earned = self.correct_answers_count * 100
            self.update_user_score(user_id, points_earned)
            self.mark_quiz_completed(user_id)
            markup = types.InlineKeyboardMarkup()
            back_button = types.InlineKeyboardButton(tr['back'], callback_data='back')
            markup.row(back_button)
            self.bot.send_message(call.message.chat.id, tr['quiz_completed'].format(correct_answers=self.correct_answers_count, points_earned=points_earned), reply_markup=markup)

    def update_user_score(self, user_id, score):
        self.db.execute_update("UPDATE users_points SET points = points + ? WHERE user_id = ?", (score, user_id))

    def mark_quiz_completed(self, user_id):
        result = self.db.execute_query("SELECT tasks_completed FROM users_points WHERE user_id = ?", (user_id,))
        tasks_completed = result[0][0] if result and result[0][0] else ''
        new_tasks_completed = tasks_completed + ',quiz' if tasks_completed else 'quiz'
        self.db.execute_update("UPDATE users_points SET tasks_completed = ? WHERE user_id = ?", (new_tasks_completed, user_id))

    def handle_friends(self, call):
        user_id = call.from_user.id
        result = self.db.execute_query('SELECT friends, language FROM users_points WHERE user_id = ?', (user_id,))
        friends_ids = result[0][0].split(',') if result and result[0][0] else []
        current_language = result[0][1]
        friends_list = []

        for friend_id in friends_ids:
            friend_name = self.db.execute_query('SELECT username FROM users_points WHERE user_id = ?', (friend_id,))
            if friend_name:
                friends_list.append(friend_name[0][0])

        result = self.db.execute_query('SELECT invited_by FROM users_points WHERE user_id = ?', (user_id,))
        invited_by_id = result[0][0] if result and result[0][0] else None
        invited_by_name = None

        if invited_by_id:
            result = self.db.execute_query('SELECT username FROM users_points WHERE user_id = ?', (invited_by_id,))
            invited_by_name = result[0][0] if result and result[0][0] else None

        tr = translations[current_language]

        friends_text = '\n'.join(friends_list) if friends_list else tr['no_friends']
        invited_by_text = tr['invited_by'].format(username=invited_by_name) if invited_by_name else tr['not_invited']
        ref_link = f"https://t.me/TowerhihiBot?start={user_id}"
        
        markup = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton(tr['back'], callback_data='back')
        markup.row(back_button)
        
        self.bot.send_message(call.message.chat.id, tr['friends_list'].format(friends=friends_text, invited_by=invited_by_text, ref_link=ref_link), reply_markup=markup, parse_mode='Markdown')

    def handle_social_networks(self, call):
        user_id = call.from_user.id
        result = self.db.execute_query('SELECT language FROM users_points WHERE user_id = ?', (user_id,))
        current_language = result[0][0]

        tr = translations[current_language]

        markup = types.InlineKeyboardMarkup()
        twitter_button = types.InlineKeyboardButton("💎 Twitter", url='https://x.com/okpebenbela')
        vk_button = types.InlineKeyboardButton("📘 VK", url='https://vk.com/id474732093')
        back_button = types.InlineKeyboardButton(tr['back'], callback_data='back')
        markup.row(twitter_button, vk_button)
        markup.row(back_button)

        self.bot.send_message(call.message.chat.id, tr['social_networks'], reply_markup=markup)

    def handle_change_language(self, call):
        user_id = call.from_user.id
        result = self.db.execute_query('SELECT language FROM users_points WHERE user_id = ?', (user_id,))
        current_language = result[0][0]

        tr = translations[current_language]

        if current_language == 'ru':
            new_language_text = "English"
            change_language_button_text = "Change to English"
        else:
            new_language_text = "Русский"
            change_language_button_text = "Сменить на Русский"

        markup = types.InlineKeyboardMarkup()
        confirm_button = types.InlineKeyboardButton(change_language_button_text, callback_data='confirm_language_change')
        back_button = types.InlineKeyboardButton(tr['back'], callback_data='back')
        markup.row(confirm_button)
        markup.row(back_button)

        self.bot.send_message(call.message.chat.id, f"{tr['change_language_message']}", reply_markup=markup)

    def handle_confirm_language_change(self, call):
        user_id = call.from_user.id
        result = self.db.execute_query('SELECT language FROM users_points WHERE user_id = ?', (user_id,))
        current_language = result[0][0] if result else 'ru'

        if current_language == 'ru':
            new_language = 'en'
            language_changed_message = translations['en']['language_changed']
        else:
            new_language = 'ru'
            language_changed_message = translations['ru']['language_changed']

        self.db.execute_update('UPDATE users_points SET language = ? WHERE user_id = ?', (new_language, user_id))

        self.bot.send_message(call.message.chat.id, language_changed_message)
        self.start_message(call.message, language=new_language)

    def handle_doska_pocheta(self, call):
        user_id = call.from_user.id
        result = self.db.execute_query('SELECT language FROM users_points WHERE user_id = ?', (user_id,))
        current_language = result[0][0]

        current_date = time.strftime("%Y-%m-%d")
        result = self.db.execute_query('SELECT leaders FROM leaderboard WHERE date = ?', (current_date,))
        leaders_text = result[0][0] if result else translations[current_language]['no_leaders']

        tr = translations[current_language]

        markup = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton(tr['back'], callback_data='back')
        markup.row(back_button)

        self.bot.send_message(call.message.chat.id, tr['leaderboard_message'].format(leaders=leaders_text), reply_markup=markup, parse_mode='Markdown')

