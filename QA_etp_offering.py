import pymongo, json
from openai import OpenAI

uri = "mongodb+srv://victoria91718:white0718@poxa.1j2eh.mongodb.net/?retryWrites=true&w=majority&appName=poxa"
client = pymongo.MongoClient(uri)

api_key = '?????'
client = OpenAI(api_key = api_key)

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