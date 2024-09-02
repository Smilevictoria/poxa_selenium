import pymongo
from openai import OpenAI

uri = "mongodb+srv://victoria91718:white0718@poxa.1j2eh.mongodb.net/?retryWrites=true&w=majority&appName=poxa"
client = pymongo.MongoClient(uri)

mydb = client["WebInformation"] # Test
mycol = mydb["article"] # info

api_key = '?????'
client = OpenAI(api_key = api_key)

def generate_query(question):
    prompt = f"""
    根據以下規則，生成相應的 MongoDB 查詢。

    字首: Edreg, reg, sr, sup 分別代表E-dReg，調頻備轉、即時備轉，補充備轉四種商品。
    字尾: Qse 代表民營合格交易者，沒有代表沒有。

    問題: {question}
    查詢:
    """
    
    response = client.Completion.create(
      engine="gpt-3.5-turbo",
      prompt=prompt,
      max_tokens=200
    )

    query = response.choices[0].text.strip()
    return query

def execute_query(query):
    # 假設 query 是一個可以 eval 的字串，轉換為字典
    query_dict = eval(query)
    result = mycol.find(query_dict)
    
    return result

user_question = input("請輸入您的問題: ")
query = generate_query(user_question)
print(f"生成的查詢: {query}")

if query:
    results = execute_query(query)
    for record in results:
        print(record)
else:
    print("無法生成查詢。請確認您的問題格式。")