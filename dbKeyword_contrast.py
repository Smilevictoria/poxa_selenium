import pymongo
from pymongo.server_api import ServerApi
from openai import OpenAI

uri = "mongodb+srv://victoria91718:white0718@poxa.1j2eh.mongodb.net/?retryWrites=true&w=majority&appName=poxa"
client = pymongo.MongoClient(uri)

mydb = client["WebInformation"] # Test
mycol = mydb["article"] # info

# api_key = '?????'
# client = OpenAI(api_key = api_key)

unique_keywords = set()

documents = list(mycol.find({}))
for doc in documents:
        doc_keywords_dict = doc.get('keywords', {})
        for keyword in doc_keywords_dict.values():
            unique_keywords.add(keyword)

unique_keywords_list = list(unique_keywords)

print(unique_keywords_list)