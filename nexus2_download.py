import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

def get_html_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 如果请求失败，会引发HTTPError异常
        return response.text
    except requests.RequestException as e:
        print(f"Error during request: {e}")
        return None

def download_file(url, save_directory):
    try:
        # 在这里可以添加文件下载的逻辑，例如使用 requests.get 下载文件
        response = requests.get(url)
        if response.status_code == 200:
            # 从URL中提取文件名
            filename = os.path.join(save_directory, url.split("/")[-1])

            # 这里可以保存文件到本地
            with open(filename, "wb") as file:
                file.write(response.content)
            with open('urltext.txt','at') as f:
                f.write(f"File downloaded from: {url}.\n")
                # print()
        else:
            print(f"Failed to download file from: {url}")
    except Exception as e:
        print(f"Error during file download: {e}")

def process_a_tags(soup, base_url, save_directory):
    td_a_tags = soup.find_all('td')
    for td_tag in td_a_tags:
        a_tag = td_tag.find('a')
        if a_tag:
            link_url = a_tag['href']
            # 如果链接还是一个网页，递归调用函数处理嵌套的<a>标签
            if link_url.endswith('/'):
                try:
                    nested_html = requests.get(link_url).text
                    nested_soup = BeautifulSoup(nested_html, 'html.parser')
                    process_a_tags(nested_soup, link_url, save_directory)
                except Exception as e:
                    print(f"{e}")
            # 如果链接是一个文件，下载文件
            else:
                download_file(link_url, save_directory)

if __name__ == '__main__':
    save_directory="/data/maven2_snapshots"  # 下载的资源保存目录
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    url="http://maven.aliyun.com/nexus/content/repositories/snapshots/" # 要下载的仓库的url 
    html_content = get_html_content(url)
    if html_content:
        soup = BeautifulSoup(html_content,'html.parser')
        process_a_tags(soup,url,save_directory)
