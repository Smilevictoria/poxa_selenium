import pymongo, json
from openai import OpenAI

uri = "mongodb+srv://victoria91718:white0718@poxa.1j2eh.mongodb.net/?retryWrites=true&w=majority&appName=poxa"
client = pymongo.MongoClient(uri)

api_key = '?????'
client = OpenAI(api_key = api_key)

def generate_answer_logic(question, rule):
    prompt = f"""
    根據以下規則和 JSON 結構生成Python代碼來回答問題。

    JSON_DATA example：
    [
        {{
            "date": "YYYY-MM-DD",
            "hour": "HH:MM",
            "edregOffering": float,
            "edregOfferingQse": float,
            "regOffering": float,
            "regOfferingQse": float,
            "srOffering": float,
            "srOfferingQse": float,
            "supOffering": float,
            "supOfferingQse": float
        }},
        ...
    ]

    規則: {rule}

    問題: {question}

    請生成Python代碼來處理上述JSON數據並計算答案。代碼應該能識別問題中的商品類型和是否為民營合格交易者(Qse)，並根據指定的日期進行計算。確保代碼是完整的，並使用 try-except 結構來處理任何可能的錯誤。
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一個專業的問題解答助手，請根據以下規則生成 MongoDB 查詢。"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    query = response.choices[0].message.content.strip()
    return query

def execute_code_logic(data, date, product_prefix, is_qse):
    try:
        total_price = 0
        count = 0

        for entry in data:
            if entry["date"] == date:
                product_field = f"{product_prefix}Offering"
                qse_field = f"{product_prefix}OfferingQse"

                if is_qse:
                    if qse_field in entry:
                        total_price += entry[qse_field]
                        count += 1
                else:
                    if product_field in entry:
                        total_price += entry[product_field]
                        count += 1

        if count > 0:
            answer = total_price / count
        else:
            answer = "無數據可供計算"

        return answer

    except Exception as e:
        return f"執行代碼時出錯: {e}"

rule = "字首: Edreg, reg, sr, sup 分別代表 E-dReg，調頻備轉、即時備轉，補充備轉四種商品。字尾: Qse 代表民營合格交易者，沒有代表沒有。"
user_input = input("請輸入您的問題: ")
date = input("請輸入您想查詢的日期 (格式：YYYY-MM-DD): ")
if "民營" in user_input:
    is_qse = True
else:
    is_qse = False

if "即時備轉" in user_input:
    product_prefix = "sr"
elif "調頻備轉" in user_input:
    product_prefix = "reg"
elif "E-dReg" in user_input:
    product_prefix = "edreg"
elif "補充備轉" in user_input:
    product_prefix = "sup"
else:
    product_prefix = None

if product_prefix is not None:
    with open('poxa-info.etp_offering.json', 'r', encoding='utf-8') as f:
        existing_data = json.load(f)

    answer = execute_code_logic(existing_data, date, product_prefix, is_qse)
    print(f"回答: {answer}")
else:
    print("無法解析您的問題，請確認輸入格式。")