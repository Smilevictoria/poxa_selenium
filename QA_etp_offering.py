import pymongo, json
from openai import OpenAI
from pymongo.server_api import ServerApi

uri = "mongodb+srv://victoria91718:white0718@poxa.1j2eh.mongodb.net/?retryWrites=true&w=majority&appName=poxa"
client = pymongo.MongoClient(uri)

api_key = '?????'
client = OpenAI(api_key = api_key)

def execute_code_logic(data, date, prefix, is_qse, suffix):
    try:
        total_value = 0
        count = 0

        for entry in data:
            if entry["tranDate"] == date:
                product_field = f"{prefix}{suffix}"
                qse_field = f"{prefix}{suffix}Qse" if is_qse else product_field
                
                if qse_field in entry:
                    total_value += entry[qse_field]
                    count += 1

        if count > 0:
            answer = total_value / count
        else:
            answer = "無數據可供計算"

        return answer

    except Exception as e:
        return f"執行代碼時出錯: {e}"
    
def execute_database(data, date, classify):
    try:
        total_value = 0
        count = 0

        for entry in data:
            if entry["tranDate"] == date:
                field = classify
                if field in entry:
                    total_value += entry[field]
                    count += 1

        if count > 0:
            answer = total_value / count
        else:
            answer = "無數據可供計算"

        return answer

    except Exception as e:
        return f"執行代碼時出錯: {e}"

def classify_question(question):
    rule = """
    字首: 當問題提到E-dReg，prefix=edreg；提到調頻備轉，prefix=reg；提到即時備轉，prefix=sr；提到補充備轉，prefix=sup。
    字中: midfix=Offering，當問題提到得標量，midfix=Bid；提到非交易，midfix=BidNontrade；提到結清價格，midfix=Price。
    字尾: 當問題中提到民營，suffix=Qse。若未提到則無suffix。
    輸出: 僅輸出 prefix+midfix+suffix，不需加入其他文字和解釋。
    """

    prompt = f"""
    根據以下規則，判斷該問題查詢的資料庫項目，並嚴格按照格式「prefix+midfix+suffix」輸出結果。如果 suffix 不存在則略過 suffix。請只輸出資料庫項目，**不要加入任何解釋、引言、或其他文字**。
    
    問題：{question}
    
    規則:
    {rule}
    
    範例：
    1. 問題：「請問調頻備轉的得標量？」 -> 輸出：regBid
    2. 問題：「民營的即時備轉結清價格是？」 -> 輸出：srPriceQse
    3. 問題：「補充備轉的結清價格？」 -> 輸出：supPrice
    4. 問題：「請問E-dReg非交易的得標量？」 -> 輸出：edregBidNontrade
    5. 問題：「民營調頻備轉？」 -> 輸出：regOfferingQse
    6. 問題：「非交易調頻備轉的得標量？」 -> 輸出：regBidNontrade
    """
    
    # 生成回答
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {"role": "system", "content": "你是一個專業的問題分析助手，請判斷問題符合規則哪點，並輸出欲查詢的資料庫項目。"},
            {"role": "user", "content": prompt}
        ]
    )
    
    answer = response.choices[0].message.content.strip()
    
    if "：" in answer or ":" in answer:
        answer = answer.split("：")[-1].strip()
    return answer


user_input = input("請輸入您的問題: ")
date = input("請輸入您想查詢的日期 (格式：YYYY-MM-DD): ")
classify = classify_question(user_input)
print("classify:", classify)
# Determine if it's for a private or public
is_qse = "民營" in user_input

# Determine the product prefix
if "即時備轉" in user_input:
    prefix = "sr"
elif "調頻備轉" in user_input:
    prefix = "reg"
elif "E-dReg" in user_input:
    prefix = "edreg"
elif "補充備轉" in user_input:
    prefix = "sup"
else:
    prefix = None

# Determine the suffix
if "非交易" in user_input:
    suffix = "BidNontrade"
elif "結清價格" in user_input:
    suffix = "Price"
elif "得標量" in user_input:
    suffix = "Bid"
else:
    suffix = "Offering"

if suffix != "Offering":
    json_file = 'poxa-info.etp_settle_value_query.json'
else:
    json_file = 'poxa-info.etp_offering.json'

if "Offering" not in classify:
    file = 'poxa-info.etp_settle_value_query.json'
else:
    file = 'poxa-info.etp_offering.json'

print(f"Using JSON file: {json_file}")
print("product_prefix:", prefix)
print("suffix:", suffix)
print(f"Using file: {file}")

if prefix and suffix is not None:
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
        with open(file, 'r', encoding='utf-8') as f:
            Edata = json.load(f)

        answer = execute_code_logic(existing_data, date, prefix, is_qse, suffix)
        ans = execute_database(Edata, date, classify)
        
        if isinstance(answer, float):
            print(f"回答1-1: {answer:.2f}")
            print(f"回答1-2: {ans:.2f}")
        else:
            print(f"回答2-1: {answer}")
            print(f"回答2-2: {ans}")

    except FileNotFoundError:
        print(f"找不到檔案: {json_file}")
        print(f"找不到檔案: {file}")
else:
    print("無法解析您的問題，請確認輸入格式。")