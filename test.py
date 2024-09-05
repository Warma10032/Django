import re
import os
import requests
import shutil
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning

_SAVE_PATH = "data/cache/internet"


# 修改为 Google 搜索
def search_baidu(query, num_results=3):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, compress",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0",
    }
    search_url = f"https://www.baidu.com/s?wd={query}"  # 百度搜索URL

    flag = 0
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # 百度搜索结果的条目
        for item in soup.find_all("div", class_="result"):
            if flag >= num_results:
                break
            try:
                # 获取标题和链接
                title = item.find("h3").text
                link = item.find("a")["href"].split("#")[0]  # 删除 '#' 后的部分

                # 禁用 SSL 验证的警告
                requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
                response = requests.get(link, timeout=10)

                if response.status_code == 200:
                    filename = f"{_SAVE_PATH}/{title}.html"
                    if response.text is not None:
                        with open(filename, "w", encoding="utf-8") as f:
                            f.write(response.text)
                            flag += 1
                        print(f"Downloaded and saved: {link} as {filename}")
                    else:
                        print(f"Failed to download {link}: Empty content")
                else:
                    print(f"Failed to download {link}: Status code {response.status_code}")
            except Exception as e:
                print(f"Error downloading {link}: {e}")
        
        # 检查是否达到了期望的结果数
        if flag < num_results:
            print("可能被百度反爬虫机制限制")
    else:
        print("Error: ", response.status_code)


if __name__ == "__main__":
    query = "中国简介"
    links = search_baidu(query)
    print(links)
