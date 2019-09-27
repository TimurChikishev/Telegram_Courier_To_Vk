import telebot
import config
import vk_api
import re
import time
import random
from vk_api.longpoll import VkLongPoll
from vk_api.bot_longpoll import VkBotLongPoll

# подключение вк
vk_session = vk_api.VkApi(token=config.token_vk)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

# подключение телеграма 
bot = telebot.TeleBot(config.token_telegram)

# для упрощения кода (постоянно не писать всякие индетификатор для id и прочего.....)
def send_msg(id_group, message):
    vk_session.method('messages.send', 
                     {'chat_id': config.groups[id_group], # получаф по ключу, например 352, 351.... 
                     'message': f' {id_group} Важное сообщение от: {message}', # id_group 352, 351.... message: сообщение пользователя
                     'random_id': 0}) # просто необходимо после абгрейда до версии longpool - 0.50 

@bot.message_handler(content_types=['text']) 
def echo_msg(message): 
    for group in config.groups: # идет по dict() вида {'352' : 1, '351' : 2}
        if group in message.text: # проверяет есть ли в сообщении 352, 351....
            # простое упрощение для последуйщего написания кода + скипаем необходимый слэш 
            send_msg(group, message.text[message.text.find('/')+1:]) 

if __name__ == "__main__":  
    while True: # если срабатывает except, то заного 
        try:
            bot.polling(none_stop=True) # постоянно слушает группу в телеграм
        except TimeoutError:
            print('Error') 
            time.sleep(20)