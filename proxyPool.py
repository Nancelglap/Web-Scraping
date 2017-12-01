from bs4 import BeautifulSoup
import requests
import socket
import urllib.request
import redis

# 可传页码参数 page
url = "http://www.xicidaili.com/wn/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
}

sessiona = requests.Session()
sessiona.headers.update(headers)

soup = BeautifulSoup(sessiona.get(url).content, 'html.parser').find_all("td");

r = redis.Redis(host = 'localhost', port = 6379, db=0)
#r.delete("who")

# 获取当前页码所有ip
ipCollection = []
check = "."

count = 1;
for i in soup:
    if not i.string:
        continue
    if check in i.string:
        socket.setdefaulttimeout(2)
        proxy_handler = urllib.request.ProxyHandler({"https": i.string})
        opener = urllib.request.build_opener(proxy_handler)
        urllib.request.install_opener(opener)
        try:
            html = urllib.request.urlopen('http://222.200.98.147/')
        except Exception as e:
            continue
        r.hset(name="proxyIp", key=str(count), value=i.string)
        count += 1

print("ok")