from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json
import sys

sys.path.append('openai')
from Openai_chatgpt import new_answer

# 初始化WebDriver
driver = webdriver.Chrome()
url = "https://info.poxa.io/"
driver.get(url)

categories = [
    "用電大戶", "光儲合一", "市場資訊", "E-dReg", "sReg", "dReg", "即時備轉", "補充備轉",
    "創新能源技術", "電價方案", "再生能源", "台電說明會", "規範解析", "台電供需資訊"
]
target_tags = new_answer.split('、')
tags_pos = [index for index, category in enumerate(categories) if category in target_tags]
print(f"位置: {tags_pos}")

tags = []
tag_list = driver.find_element(By.CLASS_NAME, "flex.flex-wrap.gap-3.px-6")
for pos in tags_pos:
    tag_elements = tag_list.find_elements(By.XPATH, f".//a[contains(text(), '{categories[pos]}')]")
    for tag in tag_elements:
        if tag.text == categories[pos]:
            tags.append(tag)
            print(tag.text)
            break

# 点击标签
for t in tags:
    t.click()

origin_url = driver.current_url
data_list = []
data_size = 5  # 要抓多少笔资料

for target in range(data_size):
    links_list = driver.find_elements(By.TAG_NAME, "a")
    link = links_list[target + 16].get_attribute('href')  # First title starts from 16
    title_list = driver.find_elements(By.CLASS_NAME, "text-2xl.font-bold")
    data_title = title_list[target].text
    content_list = driver.find_elements(By.CLASS_NAME, "text-gray-500")
    data_content = content_list[target].text
    label_list = driver.find_elements(By.CLASS_NAME, "mt-4.flex.gap-2")
    labels = label_list[target].find_elements(By.TAG_NAME, "span")
    data_labels = {index: label.text for index, label in enumerate(labels)}

    print(data_title)
    print(data_content)
    for index, label in enumerate(labels):
        print(f"{index}: {label.text}")

    driver.get(link)

    data_subtitle = []
    data_subContent = []
    data_section = []
    flag_k = 2

    # Collect subtitles and subcontents
    for flag in range(6):
        found_records = False
        while not found_records:
            subtitle = driver.find_elements(By.TAG_NAME, "p")
            if flag + flag_k >= len(subtitle):
                break
            records = subtitle[flag + flag_k].find_elements(By.TAG_NAME, "a")

            if records:
                try:
                    sub_content = subtitle[flag + flag_k].find_element(By.XPATH, 'following-sibling::ul')
                    found_records = True
                    for record in records:
                        if record.text == "下週預告❓":
                            break
                        data_subtitle.append(record.text)
                        data_subContent.append(sub_content.text)
                except NoSuchElementException:
                    flag_k += 1
            else:
                flag_k += 1

    # Collect sections
    section_list = driver.find_elements(By.CLASS_NAME, "text-3xl.font-bold")
    for flag in range(1, len(section_list)):
        if section_list[flag].text == "下週預告❓":
            break
        sections_between_h2s = []
        sections = section_list[flag].find_elements(By.XPATH, 'following-sibling::*')
        for section in sections:
            if section == section_list[flag + 1]:
                break
            sections_between_h2s.append(section)
        data_section.append([s.text for s in sections_between_h2s if s.tag_name in ['p', 'ul', 'ol']])

    # Prepare data to save in JSON
    data = {
        "title": data_title,
        "content": data_content,
        "labels": data_labels,
        "subtitle": {str(i): data_subtitle[i] for i in range(len(data_subtitle))},
        "subcontent": {str(i): data_subContent[i] for i in range(len(data_subContent))},
        "section": {str(i): data_section[i] for i in range(len(data_section))}
    }

    data_list.append(data)
    driver.get(origin_url)

# Save data to file
with open('GetchUp_data.json', 'w', encoding='utf-8') as f:
    json.dump(data_list, f, ensure_ascii=False, indent=4)

print("爬完ㄌㄌㄌㄌ~")
driver.close()
