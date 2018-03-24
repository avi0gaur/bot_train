import os
import json
import requests
from flask import Flask, request
from chat_bot import CrmnextChatBot
from Custompayload import send_message

app = Flask(__name__)

bot = CrmnextChatBot()

app = Flask(__name__, static_url_path='')


@app.route('/privacypolicy')
def privacypolicy():
    return app.send_static_file('privacypolicy.html')

@app.route('/termofservice')
def termofservice():
    return app.send_static_file('termofservice.html')

@app.route('/', methods=['POST'])
def fb_webhook():
    """
    To get data from  the user and reponse back
    :return:
    """
    data = request.get_json()
    if data["object"] == "page":
        for entry in data["entry"]:
            for msg in entry["messaging"]:
                if msg.get("message"):
                        sender_id = msg["sender"]["id"]
                        message_text = msg["message"]["text"]

                        data = {'userId': '123', 'intent_type': '', 'user_text': message_text, 'user_name': 'Avinash Gaur',
                                'contactNumber': '89892398128', 'user_stage': 0, 're_connect': True}

                        res = bot.run_bot(data)
                        print("res",res)
                        send_message(sender_id, res['response_text'])

    return "ok", 200


@app.route('/', methods=['GET'])
def v():
    return request.args["hub.challenge"], 200


if __name__ == '__main__':
    app.run(debug=True)
