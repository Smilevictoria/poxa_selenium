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

def extract_keywords(question):
    # 調用 GPT 模型提取關鍵詞
    prompt = f"請提取以下問題中的關鍵詞，並使用逗號分隔：\n問題：{question}\n\n關鍵詞："
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一個專業的問題解答助手，請從問題中提取出關鍵詞。"},
            {"role": "user", "content": prompt}
        ]
    )
    keywords = response.choices[0].message.content.strip()
    keywords_traditional = converter.convert(keywords)
    keywords_cleaned = re.sub(r'\s*[,\n]+\s*', ',', keywords_traditional) 
    keywords_neat = [keyword.strip() for keyword in keywords_cleaned.split(',') if keyword.strip()]
    keyword_list = {str(index): keyword for index, keyword in enumerate(keywords_neat)}
    return keyword_list

def classify_question(question):
    # 調用 GPT 模型進行問題分類
    prompt = f"請將以下問題分類為事實性問題、意見性問題或推理性問題：\n問題：{question}\n\n分類："
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一個專業的問題解答助手，請將問題分類為事實性問題、意見性問題或推理性問題。"},
            {"role": "user", "content": prompt}
        ]
    )
    classification = response.choices[0].message.content.strip()
    classification_traditional = converter.convert(classification)
    return classification_traditional

def search_articles(question):
    # 使用 GPT 提取關鍵詞
    keywords = extract_keywords(question)
    print("提取的關鍵詞:", keywords)
    
    # 使用提取的關鍵詞進行 MongoDB 查詢
    query = {"$text": {"$search": " ".join(keywords)}}
    results = mycol.find(query)
    return list(results)

def generate_answer(question, articles, classification):
    total_content = ""
    for article in articles:
        content = ""
        content += f"標題: {article['title']}\n"
        content += f"內容: {article['content']}\n"
        
        for i, block in article['block'].items():
            content += f"段落內容: {block['blockContent']}\n"
        
        for i, section in article['section'].items():
            content += f"部分內容: {section['sectionContent']}\n"
        content += "\n"
        prompt = f"問題: {question}\n\n根據以下文章內容生成相關摘要500字:\n{content}\n\n"
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一個專業的問題解答助手，請根據資料回答相關內容。"},
                {"role": "user", "content": prompt}
            ]
        )
        total_content += response.choices[0].message.content.strip() +"\n"
    
    ans_type = ""
    if "事實性問題" in classification:
        ans_type = "簡明"
    elif "意見性問題" in classification:
        ans_type = "詳細"
    elif "推理性問題" in classification:
        ans_type = "綜合"

    prompt = f"問題: {question}\n\n根據以下文章內容生成{ans_type}回答:\n{total_content}\n\n回答:"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一個專業的問題解答助手，請根據資料直接回答問題，不要提供額外的解釋或背景資訊。"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

mycol.create_index([("content", "text"),
                    ("block.blockContent", "text"),
                    ("section.sectionContent", "text")])
# mycol.drop_indexes() # 刪除所建立的索引
user_input = "幫我說明目前sReg價金的計算方式？" #我有1MW的光電案場，可以蓋多大的儲能案場？收益大概如何？ 光儲的參與規則？
converter = opencc.OpenCC('s2tw')
qa_classification = classify_question(user_input)
print("問題分類:", qa_classification)
appropriate_articles = search_articles(user_input)
if appropriate_articles:
    answer = generate_answer(user_input, appropriate_articles, qa_classification)
    answer_traditional = converter.convert(answer)
    print("回答:", answer_traditional)
else:
    print("無相關文章可供參考。")