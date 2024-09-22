from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pymongo
from pymongo.server_api import ServerApi

uri = "mongodb+srv://victoria91718:white0718@poxa.1j2eh.mongodb.net/?retryWrites=true&w=majority&appName=poxa"
client = pymongo.MongoClient(uri)

mydb = client["WebInformation"] # Test
mycol = mydb["synonyms"] # info

t_voc = "dReg"
voc = "調頻服務"

data = {
        "term": t_voc,
        "vocabulary": voc
    }

if data:
    mycol.insert_one(data)
    print("Inserted new data into the database.")
else:
    print("No new data to insert.")
