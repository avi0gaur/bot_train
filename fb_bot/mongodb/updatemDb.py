from pymongo import MongoClient
import json

mdb_pass = ""
mdb_user = ""
client = MongoClient("mongodb://{}:{}@ds027295.mlab.com:27295/chatbot".format(mdb_user, mdb_pass))
db = client.chatbot


def insert(cr):
    delete_col()
    try:
        db.chatbot.insert_one(
                cr
               )
        print('\nInserted data successfully\n')
    except Exception as e:
        print(e)

def read_data():
    with open('user_data.json') as data_file:
        data = json.load(data_file)
    return data

def delete_col():

    try:
        db.chatbot.delete_many({})
    except Exception as e:
        print(e)

insert(read_data())