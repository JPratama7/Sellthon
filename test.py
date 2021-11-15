import telebot
from telebot import types
from dataclasses import dataclass, astuple
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('API')

bot = telebot.TeleBot(API_TOKEN)

user_dict = {}

@dataclass
class User:
    name = str
    age = int
    sex = str

    def getastuple(self):
        name = self.name
        age = self.age
        sex = self.sex
        result = (name,age,sex)
        return result

# Handle '/start' and '/help'
# @bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Hi there, I am Example bot.
What's your name?
""")
    bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    print(message)
    try:
        chat_id = message.chat.id
        name = message.text
        user = User()
        user.name = name
        user_dict[chat_id] = user
        msg = bot.reply_to(message, 'How old are you?')
        bot.register_next_step_handler(msg, process_age_step)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'oooops')


def process_age_step(message):
    print(message)
    try:
        chat_id = message.chat.id
        age = message.text
        if not age.isdigit():
            msg = bot.reply_to(message, 'Age should be a number. How old are you?')
            bot.register_next_step_handler(msg, process_age_step)
            return
        user = user_dict[chat_id]
        user.age = age
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Male', 'Female')
        msg = bot.reply_to(message, 'What is your gender', reply_markup=markup)
        bot.register_next_step_handler(msg, process_sex_step)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'oooops')


def process_sex_step(message):
    print(message)
    try:
        chat_id = message.chat.id
        sex = message.text
        user = user_dict[chat_id]
        if (sex == u'Male') or (sex == u'Female'):
            user.sex = sex
        else:
            raise Exception("Unknown sex")
        bot.send_message(chat_id, 'Nice to meet you ' + user.name + '\n Age:' + str(user.age) + '\n Sex:' + user.sex)
        # Clearing user_dict
        user_dict.clear()
    except Exception as e:
        print(e)
        bot.reply_to(message, 'oooops')


class Test_handler:
    def send_welcome(self, message):
        msg = bot.reply_to(message, """\
    Hi there, I am Example bot.
    What's your name?
    """)
        bot.register_next_step_handler(msg, self.process_name_step)


    def process_name_step(self, message):
        try:
            chat_id = message.chat.id
            name = message.text
            user = User()
            user.name = name
            user_dict[chat_id] = user
            msg = bot.reply_to(message, 'How old are you?')
            bot.register_next_step_handler(msg, self.process_age_step)
        except Exception as e:
            print(e)
            bot.reply_to(message, 'oooops')


    def process_age_step(self, message):
        try:
            chat_id = message.chat.id
            age = message.text
            if not age.isdigit():
                msg = bot.reply_to(message, 'Age should be a number. How old are you?')
                bot.register_next_step_handler(msg, self.process_age_step)
            else:
                user = user_dict[chat_id]
                user.age = age
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                markup.add('Male', 'Female')
                msg = bot.reply_to(message, 'What is your gender', reply_markup=markup)
                bot.register_next_step_handler(msg, self.process_sex_step)
        except Exception as e:
            print(e)
            bot.reply_to(message, 'oooops')


    def process_sex_step(self, message):
        try:
            chat_id = message.chat.id
            sex = message.text
            user = user_dict[chat_id]
            if (sex == u'Male') or (sex == u'Female'):
                user.sex = sex
            else:
                raise Exception("Unknown sex")
            bot.send_message(chat_id, 'Nice to meet you ' + user.name + '\n Age:' + str(user.age) + '\n Sex:' + user.sex)
            # Clearing user_dict
            print(user.getastuple())
            del user_dict[chat_id]
            print(user_dict)
        except Exception as e:
            print(e)
            bot.reply_to(message, 'oooops')

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
# bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
# bot.load_next_step_handlers()
test_handler = Test_handler()

bot.register_message_handler(test_handler.send_welcome, commands=['start'])

print("bot is run")
bot.infinity_polling()
