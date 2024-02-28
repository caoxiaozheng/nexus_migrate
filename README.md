#### nexus3_migrate.py: 通过python调用nexu3的api接口实现 maven仓库中资源的获取，把jar包的url和groupid,version,artifactid等信息保存下来放到文件中，具体资源需要额外通过脚本进行下载
#### nexus2_download.py： 需要打开nexus2的网页访问功能，使用BeautifulSoup循环列表来拿到 具体的资源的url链接，并下载到本地。
