from Internet.Internet_prompt import extract_question
from Internet.retrieve_Internet import retrieve_html
from client.clientfactory import Clientfactory
from env import get_app_root

import re
import os
import requests
import shutil
from bs4 import BeautifulSoup

_SAVE_PATH = os.path.join(get_app_root(), "data/cache/internet")

def InternetSearchChain(question,history):
    if os.path.exists(_SAVE_PATH):
        shutil.rmtree(_SAVE_PATH)
    whole_question = extract_question(question,history)
    question_list = re.split(r'[;；]', whole_question)
    for question in question_list:
        links = search_bing(question, num_results=3)
        download_html(links)
    
    if has_html_files(_SAVE_PATH):
        docs,_context = retrieve_html(question)
        prompt = f"请根据搜索到的文件信息\n{_context}\n 回答问题：\n{question}"
        response = Clientfactory().get_client().chat_with_ai_stream(prompt)
    else:
        response = Clientfactory().get_client().chat_with_ai_stream(question)
        print("爬取到的html文件为空，请检查代理是否关闭，可自定义爬虫代码")
    
    return response
    
    
    
    
def search_bing(query, num_results=3):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    }
    
    search_url = f"https://cn.bing.com/search?q={query}"
    response = requests.get(search_url)
    
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        
        for item in soup.find_all('li', class_='b_algo')[:num_results]:
            title = item.find('h2').text
            link = item.find('a')['href'].split('#')[0]  # 删除 '#' 后的部分
            links.append({'title': title, 'link': link})
        
        return links
    else:
        print("Error:", response.status_code)
        return []

def download_html(links, folder=_SAVE_PATH):
    # 创建保存网页的文件夹
    
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    for link in links:
        try:
            response = requests.get(link['link'], timeout=10)
            if response.status_code == 200:
                filename = f"{folder}/{link['title']}.html"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"Downloaded and saved: {link['link']} as {filename}")
            else:
                print(f"Failed to download {link['link']}: Status code {response.status_code}")
        except Exception as e:
            print(f"Error downloading {link['link']}: {e}")
            
def has_html_files(folder_path):
    # 确保路径存在且是文件夹
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        # 遍历文件夹中的所有文件，检查扩展名是否为 .html
        for filename in os.listdir(folder_path):
            # 获取文件的扩展名
            if filename.endswith('.html'):
                return True
        return False
    else:
        raise ValueError(f"{folder_path} is not a valid directory")
    
    