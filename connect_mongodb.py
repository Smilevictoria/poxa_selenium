import pymongo
import json
from pymongo.server_api import ServerApi

uri = "mongodb+srv://victoria91718:white0718@poxa.1j2eh.mongodb.net/?retryWrites=true&w=majority&appName=poxa"
client = pymongo.MongoClient(uri)
# client = pymongo.MongoClient(uri, server_api=ServerApi('1'))

mydb = client["WebInformation"]
mycol = mydb["article"]

with open('GetchUp_data.json', 'r', encoding='utf-8') as f:
            existing_data = json.load(f)

x = mycol.insert_many(existing_data)
print("finsh~")