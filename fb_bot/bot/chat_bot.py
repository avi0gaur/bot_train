import json
import random

from adapt.engine import IntentDeterminationEngine
from adapt.intent import IntentBuilder

from textblob import TextBlob

from chat_logger import BotLogger
from Corpus import BotNextCorpus

__author__ = 'avi0gaur'


class CrmnextChatBot:

    def __init__(self):
        """
        Init for logger Intent engine Corpus
        """
        self.engine = IntentDeterminationEngine()
        self.bot = BotLogger()
        self.cr = BotNextCorpus()
        self.first_time = True
        self.intent = []
        self.train_intent()

    def train_intent(self):
        """
        Training intent engine to classify text intent
        :return:
        """
        for k in self.cr.train_intent_list.keys():
            for w in self.cr.train_intent_list[k]:
                self.engine.register_entity(w, k)

        for w in self.cr.train_intent.keys():
            self.intent.append(IntentBuilder(w) \
                    .require(self.cr.train_intent[w]) \
                    .build())
        for obj in self.intent:
            self.engine.register_intent_parser(obj)

    def run_bot(self, conv):
        """
        Thread starts from here.
        :return:
        """
        self.bot.log_debug("Received Json in run_bot: {}".format(conv))
        msg = conv["user_text"]
        isFirst = conv["re_connect"]

        if self.sent(msg):
            if isFirst:
                try:
                    intent = json.loads(self.intent_parser(msg))
                except Exception:
                    intent = {
                            "intent_type": "",
                            "Card": "",
                            "CardLost": "",
                            "target": "",
                            "confidence": 0.0
                            }
                conv["intent_type"] = intent["intent_type"]
                return self.p_flow(self.cr.chat_data, conv)
            else:
                return self.p_flow(self.cr.chat_data, conv)
        else:
            return self.neg_res(self.cr.chat_data, conv)

    def intent_parser(self, conv):
        """
        Method to get intent of user text.
        :param conv: user data
        :return:
        """
        for intent in self.engine.determine_intent(conv):
            if intent.get('confidence') > 0:
                return json.dumps(intent, indent=4)
            else:
                pass

    def p_flow(self, corpus, ud):
        """
        Method to implement process for user.
        :param corpus: It provides data for chatbot
        :param ud: User related data.
        :return: response
        """
        response = dict(type="text", response_text="Sorry Not able to understand", senderId="1234", userintent="")
        self.bot.log_debug("User Data: {}".format(ud))
        p_data = corpus[ud['intent_type']][ud['user_stage']]
        
        if ud['user_text'].lower() in p_data['user_text']:
            response = self.update_res(response, p_data)
        return response

    def update_res(self, response, p_data):
        """
        :param response:
        :param p_data:
        :return:
        """
        response['response_text'] = random.choice(p_data['response'])
        return response

    def neg_res(self, cr_data, conv):
        """
        Generate response if sentiment is -ve
        :param cr_data:
        :param conv:
        :return:
        """
        neg_data = cr_data["neg_sent"][0]
        return dict(userId=conv["userId"], user_intent=neg_data["intent_type"], response_text=random.choice(neg_data["response"]),
                    card_type=neg_data["card_type"],user_stage=0)

    def sent(self, conv):
        """
        Polarity is considered pos if > -0.2 (for tuning our scenario)
        :param conv:
        :return:
        """
        t = TextBlob(conv)
        return True if t.polarity > - 0.2 else False

