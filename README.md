#### nexus3_migrate.py: 通过python调用nexu3的api接口实现 maven仓库中资源的获取，把jar包的url和groupid,version,artifactid等信息保存下来放到文件中，具体资源需要额外通过脚本进行下载

### nexus2 maven仓库的迁移
#### nexus2_download.py： 需要打开nexus2的网页访问功能，使用BeautifulSoup循环列表来拿到 具体的资源的url链接，并下载到本地。
#### nexus2_up.sh： 此脚本相对应的是`nexus2_download.py` 下载资源文件然后上传到 maven仓库，通过读取pom 文件获取资源的groupid,version,artifactid。使用mvn上传到nexus仓库
