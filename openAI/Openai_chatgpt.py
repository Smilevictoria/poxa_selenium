from openai import OpenAI

api_key = '?????'
client = OpenAI(api_key = api_key)

conversation = [
    {"role": "assistant", "content": "你是一個專業的關鍵字分析師，會根據這16類對問題進行分析，16類有:用電大戶、光儲合一、市場資訊、E-dReg、sReg、dReg、即時備轉、補充備轉、創新能源技術、電價方案、再生能源、台電說明會、規範解析和台電供需資訊，請根據問題分析該問題符合這16類中的哪幾類，使用繁體中文回覆"},
    {"role": "user", "content": "我想知道如何計算家中電費?"}, # 跟我介紹一下E-dReg的規範？ 幫我說明目前sReg價金的計算方式？
    {"role": "assistant", "content": "請只回覆關鍵字"}
]

# # 將新提問加到對話歷史
# new_user_input = "請問有關於戀愛的小技巧嗎？"
# conversation_history.append({"role": "user", "content": new_user_input})

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=conversation
)

new_answer = completion.choices[0].message.content
print(new_answer)

# print("//////////////////////////////")
# print(completion)

# price = completion.usage.prompt_tokens/1000 * 0.0015 + completion.usage.completion_tokens/1000 * 0.002    
# print(price)