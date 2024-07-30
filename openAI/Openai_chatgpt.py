from openai import OpenAI

api_key = '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'
client = OpenAI(api_key = api_key)

conversation = [
    {"role": "assistant", "content": "你是一個專業的心理學顧問，請根據問題使用繁體中文回覆"},
    {"role": "user", "content": "我想學習微表情"}
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