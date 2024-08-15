from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pymongo
import json
from pymongo.server_api import ServerApi

uri = "mongodb+srv://victoria91718:white0718@poxa.1j2eh.mongodb.net/?retryWrites=true&w=majority&appName=poxa"
client = pymongo.MongoClient(uri)
# client = pymongo.MongoClient(uri, server_api=ServerApi('1'))

mydb = client["WebInformation"] # Test
mycol = mydb["article"] # info

# Initialize WebDriver
driver = webdriver.Chrome()
url = "https://info.poxa.io/"
driver.get(url)

origin_url = driver.current_url
data_list = []

# Calculate total number of items
data_size = total_items = len(driver.find_elements(By.CLASS_NAME, "text-2xl.font-bold"))

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

    # Check whether the same title exists in DB
    if mycol.find_one({"title": data_title}):
        break

    print(data_title)
    driver.get(link)

    data_subtitle = []
    data_subContent = []
    data_sectionTitle = []
    data_sectionContent = []
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
    for flag in range(1, len(section_list)-1):
        sectionCont = ""
        print(section_list[flag].text)
        data_sectionTitle.append(section_list[flag].text)
        while section_list[flag] != section_list[flag+1]:
            sectionCont += section_list[flag].text + "\n"
            try:
                next_sibling = section_list[flag].find_element(By.XPATH, "following-sibling::*[1]")
            except Exception as e:
                print(f"Error finding next sibling: {e}")
                break
            if next_sibling == section_list[flag]:
                break
            section_list[flag] = next_sibling
        data_sectionContent.append(sectionCont)

    # Prepare data to save in MongoDB
    data = {
        "title": data_title,
        "content": data_content,
        "labels": {str(i): data_labels[i] for i in range(len(data_labels))},
        "block": {str(i): {
            "blockTitle": data_subtitle[i],
            "blockContent": data_subContent[i]
            } for i in range(len(data_subtitle))},
        "section": {str(i): {
            "sectionTitle": data_sectionTitle[i],
            "sectionContent": data_sectionContent[i]
            } for i in range(len(data_sectionTitle))}
    }

    data_list.append(data)
    driver.get(origin_url)

# with open('GetchUp_data.json', 'w', encoding='utf-8') as f:
#         json.dump(data_list, f, ensure_ascii=False, indent=4)

if data_list:
    #mycol.insert_many(data_list)
    print("Inserted new data into the database.")
else:
    print("No new data to insert.")

driver.close()
