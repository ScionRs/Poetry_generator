from bs4 import BeautifulSoup
import requests
import random
import time
import json
import re
import tkinter as tk

poem_list = []

def upload_poems():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
    }
    url = "https://www.culture.ru/literature/poems"
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    poems = soup.find_all('a', class_='card-heading_title-link')
    for item in poems:
        poem_url = item.get('href')
        if poem_url is not None:
            time.sleep(2)
            url_personal_page = f"https://www.culture.ru{poem_url}"
            response_personal_page = requests.get(url=url_personal_page, headers=headers)
            soup = BeautifulSoup(response_personal_page.text, 'lxml')
            poem_text = soup.find('div', class_='content-columns_block').text
            poem_re = re.sub(r'([А-Я])', r' \n\1', poem_text)
            poem_list.append(poem_re)
            # print(poem_list)
            with open("poem_list_m.json", "w", encoding="utf-8-sig") as file:
                json.dump(poem_list, file, indent=4, ensure_ascii=False)
    return True




