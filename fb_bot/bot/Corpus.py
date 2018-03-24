from state_db import mdb
''' Chat corpus to handle request from the user and to generate appropriate response from the bot '''

__author__ = 'avi0gaur'


class BotNextCorpus:

    def __init__(self):
        """
        Init db and load required data
        """
        db = mdb()
        dic = db.get_corpus("bot_data")[0]
        self.chat_data = dic["chat_data"]
        self.train_intent = dic['train_data']['intents']
        self.train_intent_list = dic['train_data']['intent_list']
