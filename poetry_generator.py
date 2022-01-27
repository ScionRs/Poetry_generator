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
    poems = soup.find_all('a', class_='_2A3Np')
    print(poems)
    for item in poems:
        poem_url = item.get('href')
        if poem_url is not None:
            time.sleep(3)
            url_personal_page = f"https://www.culture.ru{poem_url}"
            print(url_personal_page)
            response_personal_page = requests.get(url=url_personal_page, headers=headers)
            soup = BeautifulSoup(response_personal_page.text, 'lxml')
            poem_text = soup.find('div', class_='_3x8Cp').text
            poem_re = re.sub(r'([А-Я])', r' \n\1', poem_text)
            poem_split = '\n'.join(poem_re.split('\n')[1:5])
            poem_list.append(poem_split)
            # print(poem_list)
            with open("poem_list.json", "w", encoding="utf-8-sig") as file:
                json.dump(poem_list, file, indent=4, ensure_ascii=False)
    return True

def get_random_poem():
    with open("poem_list.json", encoding="UTF-8-sig") as file:
        poem_text = json.load(file)
    first_verse = random.choice(poem_text)
    second_verse = random.choice(poem_text)
    third_verse = random.choice(poem_text)
    all_verse = first_verse + "\n *** \n" + second_verse + "\n *** \n" + third_verse
    poem_label.configure(text=all_verse)
    win.clipboard_append(all_verse)
    print(f"{all_verse}")
    return all_verse

def update_poem_list():
    checkState = upload_poems()
    if checkState != True:
        show_btn['state'] = 'disabled'
    else:
        show_btn['state'] = 'normal'

win = tk.Tk()
win.geometry(f"600x500+100+200")

show_btn = tk.Button(win, text=f'Сгенерировать стих',
                     command=get_random_poem,
                     pady=10,
                     bd=5,
                     bg='white'
                     )
show_btn.place(x=500, y=50)
update_btn = tk.Button(win, text=f'Обновить список',
                       command=update_poem_list,
                       pady=10,
                       bd=5,
                       bg='white'
                       )
update_btn.place(x=500, y=120)
poem_label = tk.Label(win, text='', font=("Courier", 10, "italic"), pady=3)
poem_label.pack()
win.update()
win.mainloop()
