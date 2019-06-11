import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import logging 
import time
import os
import telegram

import dialogflow_tools
from dialogflow_tools import MyLogsHandler

def echo(event, vk_api):
    user_id = event.user_id
    user_message = event.text
    project_id = os.environ['project_id']
    message = dialogflow_tools.detect_intent_texts(project_id, event.user_id, user_message, 'ru-RU')
    if message:
        vk_api.messages.send(
            user_id=event.user_id,
            message=message,
            random_id=random.randint(1,1000000000)
        )

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(MyLogsHandler())
    logger.info("Бот для общения в ВКонтакте запущен")
    
    try:
        vk_community_token = os.environ['vk_community_token']
        vk_session = vk_api.VkApi(token=vk_community_token)
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                echo(event, vk_api)
                
    except Exception:
        logger.exception('Возникла ошибка в боте для общения в ВКонтакте ↓')
