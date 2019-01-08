# import requests
#
# response = requests.get('http://baidu.com')
# content = requests.get('http://baidu.com').content
# print('response headers:', response.headers)
# print('content:', content)

# import requests
#
# s = requests.Session()
# headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
# print(s.get('http://baidu.com', headers=headers).cookies)
# print(s)
# s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
# r = s.get('http://httpbin.org/cookies')
#
# print(r.text)

import requests,time
from bs4 import BeautifulSoup

url = 'https://www.zhihu.com/login/email'

def get_captcha(data):
    with open('captcha.gif','wb') as fb:
        fb.write(data)
    return input('captcha')

def login(username,password,oncaptcha):
    sessiona = requests.Session()
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Host': 'www.zhihu.com',
        'Referer': 'http://www.zhihu.com/'
    }
    xyz = sessiona.get('https://www.zhihu.com/#signin',headers=headers).content
    _xsrf = BeautifulSoup(sessiona.get('https://www.zhihu.com/#signin',headers=headers).content,'html.parser').find('input',attrs={'name':'_xsrf'}).get('value')
    captcha_content = sessiona.get('https://www.zhihu.com/captcha.gif?r=%d&type=login'%(time.time()*1000),headers=headers).content
    data = {
        "_xsrf":_xsrf,
        "email": username,
        "password": password,
        "remember_me":True,
        "captcha":oncaptcha(captcha_content)
    }
    sessiona.headers.update(headers);
    resp = sessiona.post('https://www.zhihu.com/login/email', data = data)

    # regex = re.compile("z_c0=\"(.*?)\"")

    # cookie = regex.findall(str(resp.cookies))
    # print(regex.findall(str(resp.cookies)))
    cookies = dict(resp.cookies)
    # print(resp.cookies)
    # print(cookies)
    content1 = sessiona.get('https://www.zhihu.com/topic/19552832',cookies = cookies).text

    # 设置登录的cookie，以后get post等请求都不用再设置cookie
    for k,v in cookies.items():
        sessiona.cookies.set(k, v)

    # 自动带着上面设置的cookies和headers请求url
    content2 = sessiona.get('https://www.zhihu.com/question/20039623').text
    # print(content)
    with open('url.html', 'w') as fp:
        fp.write(content1)

    with open('url2.html', 'w') as fp:
        fp.write(content2)
    # print(content.decode('unicode_escape'))
    # print('resp:', resp)
    # print('resp.content:', resp.content.decode('unicode_escape'))
    # print('cookie:', resp.cookies)
    # return resp

if __name__ == "__main__":
    login('account','password',get_captcha)
