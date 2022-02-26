import time
from bs4 import BeautifulSoup
import requests
import json
from selenium_python.get_data_with_selenium import *

browser_headers ={
    "accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
}

DOMEN_NAME = "https://learngerman.dw.com"

def foo(text):
    if "\n" in text:
        text = text.replace("\n", "")
    if " " in text:
        text =  text.replace(" ", "")
    if "\"" in  text:
        text = text.replace("\"", " ")
    if "<p>" in text:
        text = text.replace("<p>", "")
    if  "</p>" in text:
        text = text.replace("</p>", "")
    if "<br>" in text:
        text = text.replace("<br>", " " )
    return text

def save_main_page():
    url = "https://learngerman.dw.com/en/beginners/c-36519789"
    req = requests.get(url, headers=browser_headers)
    src = req.text
    with open("index.html", "w") as file:
        file.write(src)

def save_topik_link():


    with open("index.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    courses = soup.find_all("li", class_="course")

    all_name_and_links = {}
    for item in courses:
        name_course = item.find("h2").text
        topics = item.find_all("li", class_="lesson-item")
        for topic in topics:
            link = DOMEN_NAME + topic.find("a").get("href")
            name_topic = topic.find("h3").text
            if name_topic == "Final Test A1":
                continue
            all_name_and_links[name_topic] = link

    with open("all_name_and_links.json", "w") as file:
        json.dump(all_name_and_links, file, indent=4, ensure_ascii=False)

def save_dict_link():
    with open("all_name_and_links.json") as file:
        all_topics = json.load(file)

    dictionary = {}
    l = len(all_topics)
    for topic in all_topics:

        name_topic = topic
        url_topic = all_topics[name_topic]
        req = requests.get(url_topic, browser_headers)
        src = req.text
        soup = BeautifulSoup(src, "lxml")
        url_voc = soup.find("a", {"id" : "vocabulary"}).get("href")
        dictionary[name_topic] = DOMEN_NAME + url_voc
        l -=1
        print(f"{name_topic} are done, {l} left")

    with open("dictionary.json", "w") as file:
        json.dump(dictionary, file, indent=4, ensure_ascii=False)

def create_list_of_links_dict():
    with open("dictionary.json", "r") as file:
        data = json.load(file)

    for topick in data:
        name_topick = topick
        url_topick = "https://learngerman.dw.com/graphql?operationName=LessonVocabulary&variables=%7B%22lessonId%22%3A37250531%2C%22lessonLang%22%3A%22ENGLISH%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%223c66359c2145d0a13962cda4f0ad878278858c12b1bda1a43b01be335534fd57%22%7D%7D"
        req = requests.get(url_topick, headers=browser_headers)

        src = req.json()
        d = src['data']['content']['vocabularies']
        dict = {}
        # dict = [[x, y] for x in d['name'] for y in d['text']]
        for i in src['data']['content']['vocabularies']:
            dict[i['name']] = foo(i['text'])
        print(dict)
        # with open("index2.html", "w") as file:
        #     file.write(src)
        break

def download_dictionary_main_page():
    with open("dictionary.json", "r") as file:
        links_to_dictionary = json.load(file)
    count = 0
    for i in links_to_dictionary:
        link = links_to_dictionary[i]
        count += 1
        b = HTML_getter(2, "/Users/viktor/PycharmProjects/selenium_python/chromedriver")
        src = b.get_html_code_by(link)
        with open(f"data/index_{i}.html", 'w') as file:
            file.write(src)
        print(f"{i} done, left {count}/{len(links_to_dictionary)}")

def create_dictionary():
    data = {}
    with open("dictionary.json", "r") as file:
        links_to_dictionary = json.load(file)
    count = 0
    for i in links_to_dictionary:
        with open(f"data/index_{i}.html", "r") as file:
            src = file.read()

        soup =  BeautifulSoup(src, "lxml")
        rows_vocabulary = soup.find_all('div', class_='row vocabulary')

        for row in rows_vocabulary:
            ger_word = foo(row.find('div', class_="col-sm-offset-1 col-sm-3 col-lg-offset-2 col-lg-3 vocabulary-entry").text)
            eng_word = foo(row.find('div', class_ = "col-sm-4 col-lg-3 vocabulary-entry").text)
            data[ger_word] = eng_word
    with open("ger-eng_dict.json", "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)




    

        

def main():
    # save_main_page()
    # save_topik_link()
    #  save_dict_link()
    # download_dictionary_main_page()
    # create_dictionary()
    pass



if __name__ == '__main__':
    main()