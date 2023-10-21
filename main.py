import config
import random

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

import requests
from bs4 import BeautifulSoup

from pyrogram import Client
import time

api_id = 28639961
api_hash = "bc72e8794b9069f1ec89fa9b8e8e5d93"
chat_id = -1001879606431
app = Client("ParserGPT", api_id, api_hash)

TG_API = "6683690512:AAFXQZpeKOdZfOPI9rhExAKwaLpdY73SecQ"
token = "vk1.a.JUsxF96n75AgNnsks_423GLynhKYneVDoF7xXk3A9hsJH7gb7NhMnDlIZj3CrPS0VoodJV8K3FGA7soRYDkRBN3Odgr6gTcl3wfRDD97CQHdy01HVYGS-jffbo1FN2msfyOmxo7WbU7SensyDtdmK0yiVoy_jRSl05iHtPgNCUy2QEk5JhrIo31EoPe2g8dOTS9oXhR5gFNsRCtQDKMXEA"
session = vk_api.VkApi(token=token)
session_api = session.get_api()
longpoll = VkBotLongPoll(session, 222855908)

starts = ["!", "/", "энди", "эн"]
admins_id = []
response_list = []

class Bot:
    class Functions: 
        def __init__(self, ConversationItems):
            self.ConversationItems = ConversationItems

        @staticmethod
        def sender(chat_id, text):  
            session_api.messages.send(chat_id=chat_id, message=text, random_id=0)

        @staticmethod
        def kicker_from_msg(chat_id, member_id):  
            session_api.messages.removeChatUser(
                chat_id=chat_id,
                member_id=member_id,
            )

        @staticmethod
        def parser_jocks():  
            headers = {
                'user-agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari 537.36 OPR/84.0.4316.52'
            }
            url = 'https://www.anekdot.ru/random/anekdot/'
            r = requests.get(url=url, headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            anecdot = soup.find_all('div', class_="text")
            
            for article in anecdot:
                article_title = article.text.strip()

            return article_title

        def get_admin_id_list(self):  
            for member in self.ConversationItems:
                try:
                    if member["is_admin"]:
                        admins_id.append(member["member_id"])
                except Exception as E:
                    print("Err: " + str(E))
        
        def parserGPT(msg):
            def send_message(chat_id, message):
                with app:
                    app.send_message(chat_id, message)

            def get_last_response(chat_id):
                with app:
                    while True:
                        messages = app.get_chat_history(chat_id, limit=1)
                        messages = list(messages)
                        last_message = messages[0] if messages else None
                        last_message = last_message.text
                        if last_message == "Обрабатываем ваш вопрос...":
                            time.sleep(0.5)
                        else:
                            break

                    return last_message

            send_message(chat_id, f"/ask {msg}")
            response = get_last_response(chat_id)
            response_list.append(response)
            print(response_list)

            app.stop()

    @staticmethod
    def process():
        for event in longpoll.listen():  
            try:
                if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
                    msg = event.object['text'].lower()     
                    print(msg)
                    chat_id = event.chat_id
                    member_id = event.object['from_id']

                    print(f"Member id from chat message: {member_id}")

                    ConversationItems = session_api.messages.getConversationMembers(peer_id=event.object.peer_id, chat_id=chat_id)["items"]
                    user = session_api.users.get(user_ids=member_id)

                    try:
                        if event.object.action['type'] == 'chat_invite_user':
                            Bot.Functions.sender(chat_id, "Привет, я Энди, помощник первой школы.✌️) Напишите команду \"помощь\" для ознакомления.")
                    except:
                        pass

                    try:
                        if event.object.action['type'] == 'chat_invite_user_by_link':
                            Bot.Functions.sender(chat_id, "Привет, я Энди, помощник первой школы.✌️) Напишите команду \"помощь\" для ознакомления.")
                    except:
                        pass

                    try:
                        if event.object.action['type'] == 'chat_kick_user':
                            Bot.Functions.sender(chat_id, "Пока, пока!🖐️")
                    except:
                        pass

                    if int(msg.find("даун")) >= 0 or int(msg.find("далбаеб")) >= 0 or int(msg.find("дибил")) >= 0 or int(msg.find("еблан")) >= 0 or int(msg.find("конченный")) >= 0:
                        Bot.Functions.sender(chat_id, f"@id{member_id} (Не оскорбляйте никого! Если вы продолжите, то можете быть иключены из беседы!)")

                    elif msg.startswith(tuple(starts)):
                        msg = msg.split(" ")
                        try:
                            if msg[1] in ["кик", "исключить", "убрать"]: 
                                Bot.Functions(ConversationItems).get_admin_id_list()
                                if member_id in admins_id:
                                    Bot.Functions.kicker_from_msg(chat_id=chat_id, member_id=event.object.reply_message['from_id'])
                                else:
                                    Bot.Functions.sender(chat_id, f"@id{member_id} (Вы не являетесь администратором.)")

                            elif msg[1] == "правила":
                                Bot.Functions.sender(chat_id, "📋Правила общения в беседе: \n1. Токсичное поведение запрещено. К токсичному поведению относится: использование большого количества мата в сообщениях, оскорбление и унижение других, регулярные ссоры и провокации. \n2. Распространение некорректных материалов запрещено. К таким относятся: порнография, физическое насилие, пропаганда курения или алкоголизма. \n3. Ответственность за вашу речь, выражения и высказывания лежит только на вас. \n4. Администраторы беседы не могут разглашать что-либо за пределы беседы. ")

                            elif msg[1] == "монетка":
                                numbers = [0, 1]
                                if random.choice(numbers) == 0:
                                    Bot.Functions.sender(chat_id, "Выпала решка!")
                                else:
                                    Bot.Functions.sender(chat_id, "Выпал орел!")

                            elif msg[1] in ["камень", "ножницы", "бумага"]:
                                numbers = ["камень", "ножницы", "бумага"]
                                randome = random.choice(numbers)
                                if randome == msg[1]:
                                    Bot.Functions.sender(chat_id, randome)
                                    Bot.Functions.sender(chat_id, "Упс! Ничья!")
                                elif (randome == "камень" and msg[1] == "бумага") or (randome == "бумага" and msg[1] == "ножницы") or (randome == "ножницы" and msg[1] == "камень"):
                                    Bot.Functions.sender(chat_id, randome)
                                    Bot.Functions.sender(chat_id, f"@id{member_id} (Похоже, что вы выиграли.😅))")
                                else:
                                    Bot.Functions.sender(chat_id, randome)
                                    Bot.Functions.sender(chat_id, "Ура, ура, я выиграл!😎)")

                            elif msg[1] in ["подкати", "запикапь", "подкат"]:
                                Bot.Functions.sender(chat_id, f"@id{member_id} ({random.choice(config.pikap)})")

                            elif msg[1] in ["шутка", "прикол", "анекдот", "смешнявка"]:
                                Bot.Functions.sender(chat_id, Bot.Functions.parser_jocks())

                            elif msg[1] in ["помощь", "помоги", "хелп"]:
                                Bot.Functions.sender(chat_id, "🚦Основные команды:\n1. С помощью команды \"помощь\" я покажу вам список команд.\n2. С помощью команды \"правила\" вы можете узнать о правилах беседы.\n \n🎮Игровые команды:\n1. Орел или решка. Напишите команду \"монетка\" и я кину монетку. Вероятность выпадения орла и решки одинакова, 50 на 50.\n2. Камень, ножницы, бумага. Напишите мне: \"Энди {камень, ножницы или бумага}\" и я сыграю с вами!\n \n🤣Развлекательные команды:\n1. С помощью команды \"шутка\" я расскажу вам анекдот.\n2. С помощью команды \"подкат\" я очень круто к вам подкачу.\n \n👮Для администраторов:\n1. Команда \"кик\" исключает человека в ответ на сообщение.\n \n❗Чтобы использовать эти команды вам требуется перед их выполнением обратиться ко мне. Пример:\nВы: Энди бумага\nЯ: Ножницы!\nЯ: Ура, ура, я выиграл!😎)")

                            else:
                                Bot.Functions.sender(chat_id, "Думаю...🤔")
                                response_list.clear()
                                try:
                                    Bot.Functions.parserGPT(" ".join(msg[1:]))
                                    Bot.Functions.sender(chat_id, f"@id{member_id} ({response_list[0]})")
                                except:
                                    Bot.Functions.sender(chat_id, f"@id{member_id} ({response_list[0]})")

                        except IndexError:
                            Bot.Functions.sender(chat_id, "Привет, я Энди, помощник первой школы.✌️) Напишите команду \"помощь\" для ознакомления.")

            except Exception as e:
                Bot.Functions.sender(chat_id, f"Сообщение для моего папы: {e}")

if __name__ == '__main__':
    Bot.process()