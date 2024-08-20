import pymongo
from pymongo.server_api import ServerApi
from openai import OpenAI
import re, opencc

uri = "mongodb+srv://victoria91718:white0718@poxa.1j2eh.mongodb.net/?retryWrites=true&w=majority&appName=poxa"
client = pymongo.MongoClient(uri)

mydb = client["WebInformation"] # Test
mycol = mydb["article"] # info

api_key = '??????'
client = OpenAI(api_key = api_key)

def choose_appropriate_keywords(user_input):
    conversation = [
        {"role": "assistant", "content": "你是一個專業的關鍵字分析師，會根據問題進行分析並選出五個關鍵字，且確保這五個關鍵字能準確反映問題的核心內容。"},
        {"role": "user", "content": f"為以下問題從下列關鍵字列表中選擇5個關鍵字:{user_input}。用繁體中文回答關鍵字，使用逗號分隔: \n\n" + "\n\n".join(unique_keywords_list) + "\n\n"}
    ]

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )

    suited_keywords = completion.choices[0].message.content.strip()
    keywords_cleaned = re.sub(r'\s*[,\n]+\s*', ',', suited_keywords) 
    keywords_neat = [keyword.strip() for keyword in keywords_cleaned.split(',') if keyword.strip()]
    keyword_list = {str(index): keyword for index, keyword in enumerate(keywords_neat)}
    return keyword_list

def generate_keywords(user_inputQA):
    conversation = [
        {"role": "assistant", "content": "你是一個專業的關鍵字分析師，會根據問題進行分析並產生三個關鍵字，且確保這三個關鍵字能準確反映問題的核心內容，只用繁體中文回答。"},
        {"role": "user", "content": f"為以下內容產生3個關鍵字，用繁體中文回答關鍵字，使用逗號分隔: {user_inputQA}"}
    ]

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )

    keywords = completion.choices[0].message.content.strip()
    # use OpenCC "s2tw" transfering simple to traditional
    converter = opencc.OpenCC('s2tw')
    keywords_traditional = converter.convert(keywords)
    keywords_cleaned = re.sub(r'\s*[,\n]+\s*', ',', keywords_traditional) 
    keywords_neat = [keyword.strip() for keyword in keywords_cleaned.split(',') if keyword.strip()]
    keyword_list = {str(index): keyword for index, keyword in enumerate(keywords_neat)}
    return keyword_list

def keyword_matches(doc_keywords, search_keywords):
        for keyword in search_keywords:
            if any(keyword in doc_keyword for doc_keyword in doc_keywords):
                return True
        return False

def fetch_and_compare_documents(appropriate_keywords, auto__keywords):

    documents = list(mycol.find({}))
    appr_keywords_set = set(appropriate_keywords.values())  
    auto_keywords_set = set(auto__keywords.values())  
    matched_docs = []
    
    for doc in documents:
        doc_keywords_dict = doc.get('keywords', {})
        doc_keywords_set = set(doc_keywords_dict.values())

        if any(keyword in doc_keywords_set for keyword in appr_keywords_set):
            matched_docs.append(doc)
        elif keyword_matches(doc_keywords_set, auto_keywords_set):
            matched_docs.append(doc)

        # # Check if there is any intersection between the two sets
        # if keywords_set.intersection(doc_keywords_set):
        #     matched_docs.append(doc)
    
    return matched_docs

def generate_response(matched_docs, user_inputQA):
    documents_text = [
        doc.get('block', {}).get('blockContent', '') + '\n' + doc.get('section', {}).get('sectionContent', '') 
        for doc in matched_docs
    ]
    prompt = f"請根據以下資料的內容精準的回答問題 '{user_inputQA}'。只回答問題，用繁體中文回答：\n\n" + "\n\n".join(documents_text) + "\n\n"
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一個專業的問題解答助手，請根據資料回答問題，不要提供額外的解釋或背景資訊。"},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

unique_keywords = set()
documents = list(mycol.find({}))
for doc in documents:
        doc_keywords_dict = doc.get('keywords', {})
        for keyword in doc_keywords_dict.values():
            unique_keywords.add(keyword)

unique_keywords_list = list(unique_keywords)

user_input = "我有1MW的光電案場，可以蓋多大的儲能案場？收益大概如何？" # 幫我說明目前sReg價金的計算方式？ 光儲的參與規則？
appropriate_keywords = choose_appropriate_keywords(user_input)
auto_keywords = generate_keywords(user_input)
print(f"user_input:{user_input}\nappropriate_keywords:{appropriate_keywords}\nauto_keywords:{auto_keywords}\n")
doc_list = fetch_and_compare_documents(appropriate_keywords, auto_keywords)
response = generate_response(doc_list, user_input)
print(f"回答 : {response}")

