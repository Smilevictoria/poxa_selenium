from openai import OpenAI
from selenium_Demo import get_data_from_web
import pymongo
from pymongo.server_api import ServerApi
import re

uri = "mongodb+srv://victoria91718:white0718@poxa.1j2eh.mongodb.net/?retryWrites=true&w=majority&appName=poxa"
client = pymongo.MongoClient(uri)

mydb = client["WebInformation"] # Test
mycol = mydb["article"] # info

api_key = '??????'
client = OpenAI(api_key = api_key)

def generate_keywords(section_text):
    conversation = [
        {"role": "system", "content": "你是一個專業的關鍵字分析師，會根據所得到的內容進行分析"},
        {"role": "user", "content": f"為以下內容產生10個關鍵字，只輸出繁體關鍵字，使用逗號分隔: {section_text}"}
    ]
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=conversation
    )
    keywords = response.choices[0].message.content.strip()
    keywords_cleaned = re.sub(r'\s*[,\n]+\s*', ',', keywords) 
    keywords_neat = [keyword.strip() for keyword in keywords_cleaned.split(',') if keyword.strip()]
    # transfer list
    keyword_list = {str(index): keyword for index, keyword in enumerate(keywords_neat)}
    return keyword_list

# Get all data
all_data = mycol.find()

for data in all_data:
    section_text = data.get("section", "")
    existing_keywords = data.get("keywords", None)

    if section_text and not existing_keywords:
        keyword_list = generate_keywords(section_text)
        # 更新
        mycol.update_one({"_id": data["_id"]}, {"$set": {"keywords": keyword_list}})
        print(f"存入資料 : {keyword_list}")

print("All keywords generated and stored in the database.")

# conversation = [
#     {"role": "assistant", "content": "你是一個專業的關鍵字分析師，會根據這16類對問題進行分析，16類有:用電大戶、光儲合一、市場資訊、E-dReg、sReg、dReg、即時備轉、補充備轉、創新能源技術、電價方案、再生能源、台電說明會、規範解析和台電供需資訊。請根據問題分析該問題符合這16類中的哪幾類，並使用繁體中文回覆。除此之外，請回覆問題中涉及的時間關鍵字，例如：本週、今天。如果問題符合多個類別，請列出所有相關的類別關鍵字。"},
#     {"role": "user", "content": "本週市場情況摘要？"}, # 跟我介紹一下E-dReg的規範？光儲的參與資格是？ 幫我說明目前sReg價金的計算方式？
#     {"role": "assistant", "content": "市場資訊,本週"},
#     {"role": "user", "content": "幫我說明目前sReg價金的計算方式？"},
#     {"role": "assistant", "content": "sReg,規範解析,目前"},
#     {"role": "user", "content": "光儲的參與資格是？"},
#     {"role": "assistant", "content": "光儲合一,規範解析"}
# ]

# # 將新提問加到對話歷史
# new_user_input = "本週頻率變化？" # 本週頻率變化？本週市場情況摘要？本週是否有台電新的公告？目前E-dReg的投報率如何？你建議投資嗎？
# conversation.append({"role": "user", "content": new_user_input})

# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=conversation
# )

# new_answer = completion.choices[0].message.content
# print(new_answer)

# data_list = get_data_from_web(new_answer)
# summarys = []
# for data in data_list:
#     subtitles = "\n".join([f"{key}: {value}" for key, value in data["subtitle"].items()])
#     subcontents = "\n".join([f"{key}: {value}" for key, value in data["subcontent"].items()])
#     sections = "\n".join([f"{key}: {', '.join(section)}" for key, section in data["section"].items()])
    
#     data_text = f"""
#     Title: {data['title']}
#     Content: {data['content']}
#     Labels: {', '.join(data['labels'].values())}
#     Subtitles: {subtitles}
#     Subcontents: {subcontents}
#     Sections: {sections}
#     """

#     data_conversation = [
#         {"role": "system", "content": "你是一個專業的文章摘要助手，會根據輸入的文本生成250字的摘要。請使用繁體中文回覆。"},
#         {"role": "user", "content": f"請幫根據{new_user_input}從{data_text}總結內容"}
#     ]

#     completion = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=data_conversation
#     )

#     summary = completion.choices[0].message.content
#     summarys.append(summary)

# if len(data_list) > 1:
#     combined_summaries = "\n\n".join(summarys)
#     final_conversation = [
#         {"role": "system", "content": "你是一個專業的文章摘要助手，會根據輸入的文本生成250字的摘要。請使用繁體中文回覆。"},
#         {"role": "user", "content": f"請幫我根據{new_user_input}總結以下多篇文章的摘要:\n\n{combined_summaries}"}
#     ]

#     completion = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=final_conversation
#     )

#     final_summary = completion.choices[0].message.content
#     print(final_summary)
# else:
#     print(summarys[0])