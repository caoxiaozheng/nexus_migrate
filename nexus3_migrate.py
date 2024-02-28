import requests
import json
import shutil
import os,sys
# 源 Nexus 信息
url = ""
repository=""
username = ""
password = ""


# 设置请求头
headers = {
    "accept": "application/json"
}
# 创建认证信息
auth = (username, password)
params = {
    "repository": repository
}
# 定义文件信息下载后的内容保存的位置
filetxt="_nexus_list.txt"
filedir="../file/"
filename=f"{filedir}{repository}{filetxt}"
maveninfo=f"{filedir}{repository}_maveninfo.txt"
urlinfo=f"{filedir}{repository}_urlinfo.txt"
if  os.path.exists(maveninfo):
    os.remove(maveninfo)




# 获取源 Nexus 仓库内容列表
def get_source_repository_contents(continuationToken=None):
    if continuationToken:
        params['continuationToken'] = continuationToken
    response = requests.get(url, auth=auth, headers=headers, params=params)
    if response.status_code == 200:
        # 请求成功，可以处理响应数据
        return response.json()
    else:
        # 请求失败，处理错误
        print(f"Request failed with status code: {response.status_code}")
        return response.text
# 将nexus 仓库资源列表进行整理
def anl_source_repository_contents():
    first_source_contents = get_source_repository_contents()
    next_page = first_source_contents.get('continuationToken')
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename,mode='at',encoding='utf-8') as f:
        f.write(str(first_source_contents['items'])+"\n")
    while True:
        if next_page:
            other_source_contents = get_source_repository_contents(next_page)
            with open(filename, mode='at', encoding='utf-8') as f:
                f.write(str(other_source_contents['items'])+"\n")
            next_page = other_source_contents.get('continuationToken')
            continue
        else:
            break

# 将整理好的仓库资源列表进行 细化拆分,达到可以直接下载，并且有上传条件的
def assetes_info(datalists):
    for datalist in datalists:
        groupid = datalist['group']
        version = datalist['version']
        artifactId = datalist['name']
        asserts = datalist['assets']
        # print(groupid,version)
        for asse in asserts:
            asserturl = asse['downloadUrl']

            if asserturl.endswith(".pom") or asserturl.endswith(".jar"):
                asserturlinfo = str(asserturl).split("/")[-1]
                info = f"{groupid} {version} {artifactId} {asserturlinfo}"
                with open(maveninfo,mode='at',encoding='utf-8') as  f:
                     f.write(info + "\n")
                with open(urlinfo,mode='at',encoding='utf-8') as  f:
                    f.write(asserturl + "\n")


if __name__ == "__main__":
    anl_source_repository_contents()
    with open(filename, mode='rt', encoding='utf-8') as f:
        for line in f:
            datalist = eval(line)
            assetes_info(datalist)
