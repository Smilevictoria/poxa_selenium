import pymongo, time
from pymongo.server_api import ServerApi
from openai import OpenAI
import numpy as np
from sentence_transformers import SentenceTransformer

uri = "mongodb+srv://victoria91718:white0718@poxa.1j2eh.mongodb.net/?retryWrites=true&w=majority&appName=poxa"
client = pymongo.MongoClient(uri)

mydb = client["WebInformation"] # Test
mycol = mydb["article"] # info

api_key = '?????'
client = OpenAI(api_key = api_key)

def word_embedding(text):
    return model.encode(text)

def article_word_embedding():
    datas = list(mycol.find({}))
    data_embedding = []

    for data in datas:
        combined_content = ""
        combined_content += f"標題: {data['title']}\n"
        combined_content += f"內容: {data['content']}\n"
        
        for i, block in data['block'].items():
            combined_content += f"段落內容: {block['blockContent']}\n"
        
        for i, section in data['section'].items():
            combined_content += f"部分內容: {section['sectionContent']}\n"
        combined_content += "\n"

        article_embedding = word_embedding(combined_content)
        data_embedding.append((combined_content, article_embedding))
    return data_embedding

def cosine_similarity(embedding1, embedding2):
    return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

def find_most_relevant(qa_emb, article_emb):
    max_similarity = -1
    most_relevant = None

    for data, embedding in article_emb:
        similarity = cosine_similarity(qa_emb, embedding)
        if similarity > max_similarity:
            max_similarity = similarity
            most_relevant = data
    return most_relevant

def generate_response(question, rel_content):
    prompt = f"問題: {question}\n\n根據以下內容生成嚴謹的回答:\n{rel_content}\n\n回答:"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一個專業的問題解答助手，請根據資料直接回答問題，不要提供額外的解釋或背景資訊。"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

start_time = time.time()
model = SentenceTransformer('all-MiniLM-L6-v2')

user_input = "光儲的參與規則？" # 目前調頻備轉價格是多少？ 我有1MW的光電案場，可以蓋多大的儲能案場？收益大概如何？
qa_embedding = word_embedding(user_input)
article_embedding = article_word_embedding()
relevant_content = find_most_relevant(qa_embedding, article_embedding)
response = generate_response(user_input, relevant_content)

end_time = time.time()
elapsed_time = end_time - start_time
print("user_input", user_input,"\nAns:", response)
print(f"Total_running_time : {elapsed_time:.2f} 秒")