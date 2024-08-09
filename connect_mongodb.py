import pymongo
from pymongo.server_api import ServerApi

uri = "mongodb+srv://victoria91718:white0718@poxa.1j2eh.mongodb.net/?retryWrites=true&w=majority&appName=poxa"
client = pymongo.MongoClient(uri)
# client = pymongo.MongoClient(uri, server_api=ServerApi('1'))

mydb = client["WebInformation"]
mycol = mydb["article"]

#印出所有DB的名稱
#print("目前存在的DB有 ",mydb,"目前存在的Collection是 ",mycol)

mydict = {"_id": 123, "name": "Google", "address": "Google 搜索"}
x = mycol.insert_one(mydict)
print(x.inserted_id)