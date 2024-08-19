import pymongo
from pymongo.server_api import ServerApi
from openai import OpenAI
import re
import opencc
from collections import Counter

uri = "mongodb+srv://victoria91718:white0718@poxa.1j2eh.mongodb.net/?retryWrites=true&w=majority&appName=poxa"
client = pymongo.MongoClient(uri)

mydb = client["WebInformation"] # Test
mycol = mydb["article"] # info

api_key = '?????'
client = OpenAI(api_key = api_key)

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
    # use OpenCC transfering simple to traditional
    converter = opencc.OpenCC('s2tw')  # s2tw transfering simple to traditional
    keywords_traditional = converter.convert(keywords)
    keywords_cleaned = re.sub(r'\s*[,\n]+\s*', ',', keywords_traditional) 
    keywords_neat = [keyword.strip() for keyword in keywords_cleaned.split(',') if keyword.strip()]
    keyword_list = {str(index): keyword for index, keyword in enumerate(keywords_neat)}
    print(keyword_list)
    return keyword_list

def keyword_matches(doc_keywords, search_keywords):
        for keyword in search_keywords:
            if any(keyword in doc_keyword for doc_keyword in doc_keywords):
                return True
        return False

def fetch_and_compare_documents(keywords_3):
    # Fetch all documents from the collection
    documents = list(mycol.find({}))
    matched_docs = []
    
    # Convert keywords_3 from dictionary to set of values
    keywords_set = set(keywords_3.values())
    
    for doc in documents:
        doc_keywords_dict = doc.get('keywords', {})
        doc_keywords_set = set(doc_keywords_dict.values())

        # Check for partial matches
        if keyword_matches(doc_keywords_set, keywords_set):
            matched_docs.append(doc)

        # # Check for partial matches
        # if keyword_matches(doc_keywords_set, keywords_set):
        #     matched_docs.append(doc)
        #     #print(f"title:{doc['title']}")
    
    return matched_docs

def find_top_documents_by_keywords(keywords_3):
    # Fetch all documents from the collection
    documents = mycol.find()
    
    # Convert keywords from dictionary to set of values
    keywords_set = set(keywords_3.values())
    keyword_counts = []
    
    for doc in documents:
        # Get section content from the document
        section_text_dict = doc.get('section', {})
        matching_texts = []
        
        # Check each section for matching keywords
        if isinstance(section_text_dict, dict):
            for key, value in section_text_dict.items():
                if isinstance(value, dict) and 'sectionContent' in value:
                    section_content = value['sectionContent']
                    # Check if any keyword is in the section_content
                    if any(keyword in section_content for keyword in keywords_set):
                        matching_texts.append(section_content)
        combined_text = " ".join(matching_texts)
        
        # Count keywords in the combined_text
        counts = Counter(word for word in combined_text.split() if word in keywords_set)
        
        # Calculate the total count of matching keywords
        total_count = sum(counts.values())
        if total_count > 0:
            keyword_counts.append((doc, total_count))
    
    # Sort by total count and get the top 5
    keyword_counts.sort(key=lambda x: x[1], reverse=True)
    top_docs = keyword_counts[:5]
    return top_docs

def generate_response(matched_docs, user_inputQA):
    matched_docs =[]
    if not matched_docs:
        # If no documents matched, find top documents by keywords
        top_docs = find_top_documents_by_keywords(keywords_3)
        documents_text = [doc.get('content', '') for doc in top_docs]  # Assuming 'content' is the text field
    else:
        # Extract content from matched documents
        documents_text = [doc.get('content', '') for doc in matched_docs]  # Assuming 'content' is the text field
    
    # Create a prompt for GPT to generate a response based on the documents
    prompt = f"請根據以下資料的內容精準的回答問題 '{user_inputQA}'。只回答問題，用繁體中文回答：\n\n" + "\n\n".join(documents_text) + "\n\n"
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一個專業的問題解答助手，請根據資料直接回答問題，不要提供額外的解釋或背景資訊。"},
            {"role": "user", "content": prompt}
        ]
    )
    
    return completion.choices[0].message.content

# Example usage
user_inputQA = "我有1MW的光電案場，可以蓋多大的儲能案場？收益大概如何？"#幫我說明目前sReg價金的計算方式？光儲的參與規則？
print(user_inputQA)
keywords_3 = generate_keywords(user_inputQA)
matched_docs = fetch_and_compare_documents(keywords_3)
response = generate_response(matched_docs, user_inputQA)

print(f"回答:{response}")