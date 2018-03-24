import os
import json
import requests

from bot_conf import PAGE_TOKEN
class CustomPayload:

    def __init__(self):
        pass

    def quick_reply(self,senderId, res):
        botRes = res["response_text"]
        listOfReply = res["recommendation"]
        quickReply = []


        for qrly in listOfReply:
            temp = {
                "content_type": "text",
                "title": "",
                "payload": ""
            }
            temp["title"] = qrly
            temp["payload"] = qrly
            quickReply.append(temp)

        msg = {
            "text": botRes,
            "quick_replies": quickReply
        }

        self.send(senderId, msg)


    def normalReply(self, senderId, msg):
        temp = {
            "text": msg
        }

        self.send(senderId, temp)


    def send(self, recipient_id, message_text):

        params = {
            "access_token": PAGE_TOKEN
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient": {
                    "id": recipient_id
            },
            "message": message_text
        })
        return requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers,
                                     data=data)

    def payloadManager(self, senderId, res):
        return self.normalReply(senderId, res)

p = CustomPayload()
def send_message(senderId, msg):
    return p.payloadManager(senderId, msg)