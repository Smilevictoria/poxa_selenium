import pymongo
from pymongo.server_api import ServerApi
import json

uri = "mongodb+srv://victoria91718:white0718@poxa.1j2eh.mongodb.net/?retryWrites=true&w=majority&appName=poxa"
client = pymongo.MongoClient(uri)

mydb = client["WebInformation"] # Test
mycol = mydb["article"] # info

# with open('GetchUp_data.json', 'r', encoding='utf-8') as f:
#             existing_data = json.load(f)

# x = mycol.insert_many(existing_data)
# print("finsh~")

# Can use in "title/content"
# find_result1 = list(mycol.find({'name': 'Victoria'}))
# print(find_result1[0]['id'])

# Can use in "labels/subtitle/subcontent" // get all article with '市場資訊' of labels
# find_result2 = list(mycol.find({}))
# for document in find_result2:
#     labels = document.get('labels', {})
#     if '市場資訊' in labels.values():
#         print(document['title'])

# Can use in "section" // [2 for loops] get all article with '颱風' of section
find_result3 = list(mycol.find({}))
for document in find_result3:
    section = document.get('section', {})
    # Iterate over all sections
    for key, value in section.items():
        # Check if 'sReg價金' is in the sectionContent
        if 'sReg價金' in value.get('sectionContent', ''):
            print(document.get('title', 'No title'))
            break

