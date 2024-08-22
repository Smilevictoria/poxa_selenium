from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json, re
# from selenium.webdriver.chrome.service import Service

# driver_path = "C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe" 
# service = Service(executable_path=driver_path)
# driver = webdriver.Chrome(service=service)

def get_data_from_web(new_answer):
    driver = webdriver.Chrome()
    url  = "https://info.poxa.io/"
    driver.get(url)

    categories = [
        "用電大戶", "光儲合一", "市場資訊", "E-dReg", "sReg", "dReg", "即時備轉", "補充備轉",
        "創新能源技術", "電價方案", "再生能源", "台電說明會", "規範解析", "台電供需資訊"
    ]
    target_tags = re.split('、|,',new_answer)
    limit_size = 5
    if target_tags[len(target_tags)-1] == "本週":
        limit_size = 1
    if limit_size != 1:
        tags_pos = [index for index, category in enumerate(categories) if category in target_tags]
        print(f"位置:{tags_pos}")
        tags = []

        tag_list = driver.find_element(By.CLASS_NAME,"flex.flex-wrap.gap-3.px-6")
        for i in range(len(tags_pos)):
            tag = tag_list.find_elements(By.XPATH, f".//a[contains(text(), '{categories[tags_pos[i]]}')]")
            # "E-dReg" & "dReg"  XPATH會抓符合字樣，需辨識
            if tag[0].text == categories[tags_pos[i]]:
                    tags.append(tag[0])
                    print(tag[0].text)
            else:
                tags.append(tag[1])
                print(tag[1].text)
        for t in tags:
            t.click()


    origin_url = driver.current_url
    data_list = []
    data_size = limit_size   # 要抓多少筆資料
    for target in range(data_size):
        links_list = driver.find_elements(By.TAG_NAME,"a")
        link = links_list[target+16].get_attribute('href') #first title start from 16
        title_list = driver.find_elements(By.CLASS_NAME,"text-2xl.font-bold")
        data_title = title_list[target].text
        content_list = driver.find_elements(By.CLASS_NAME,"text-gray-500")
        data_content = content_list[target].text
        label_list = driver.find_elements(By.CLASS_NAME,"mt-4.flex.gap-2")
        labels = label_list[target].find_elements(By.TAG_NAME,"span")
        # data_labels = [label.text for label in labels] 無序列
        data_labels = {index: label.text for index, label in enumerate(labels)}

        print(data_title)

        links_list[target+16].click()
        driver.get(link)

        # subtitle 2~7 & sub_content 0~5
        data_subtitle = []
        data_subContent = []
        data_section = [] 
        flag_k = 2
        # 0~5
        for flag in range(6):
            found_records = False
            while not found_records:
                # print(f"Trying with k={flag_k} and flag={flag}")
                subtitle = driver.find_elements(By.TAG_NAME, "p")
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
                    flag_k += 1  # flag_k++ Rerun

        section_list = driver.find_elements(By.CLASS_NAME, "text-3xl.font-bold")
        for flag in range(1, len(section_list)):
            section_between_h2s = []
            section_part = []
            if section_list[flag].text == "下週預告❓":
                break
            sections = section_list[flag].find_elements(By.XPATH, 'following-sibling::*')
            for s in sections:
                if s == section_list[flag + 1]:
                    break
                section_between_h2s.append(s)
            for sbh in section_between_h2s:
                if sbh.tag_name == 'p':
                    section_part.append(sbh.text)
                elif sbh.tag_name == 'ul':
                    section_part.append(sbh.text)
                elif sbh.tag_name == 'ol':
                    section_part.append(sbh.text)
            data_section.append(section_part)
                    
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

    # # save as a file
    # with open('GetchUp_data.json', 'w', encoding='utf-8') as f:
    #     json.dump(data_list, f, ensure_ascii=False, indent=4)

     # 讀取現有資料
    try:
        with open('GetchUp_data.json', 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []

    # 新增不重複的資料
    existing_titles = {item['title'] for item in existing_data}
    for new_data in data_list:
        if new_data['title'] not in existing_titles:
            existing_data.append(new_data)

    # 保存合併後的資料
    with open('GetchUp_data.json', 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)
        
    print("爬完ㄌㄌㄌㄌ~")
    driver.close

    return data_list