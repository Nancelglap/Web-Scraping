import requests
import json


def get_captcha(data):
    with open('captcha.gif','wb') as fb:
        fb.write(data)
    return input('captcha')

def login(oncaptcha):
    # 首页地址
    baseUrl = "http://222.200.98.147"

    sessiona = requests.Session()
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Host':'222.200.98.147',
        'Referer':'http://222.200.98.147/',
    }
    sessiona.headers.update = headers

    # 获取验证码的图片并拿到Cookie
    soup = sessiona.get(baseUrl+"/yzm?d="+'1234', headers=headers)
    captcha_content = sessiona.get(baseUrl+"/yzm?d="+'1234', headers=headers).content

    # 将Cookie加到header中
    print(soup.headers['Set-Cookie'].split(';')[0]);
    cookie = soup.headers['Set-Cookie'].split(';')[0]
    headers['Cookie'] = cookie

    data = {
        'account': '学号',
        'pwd': '密码',
        'verifycode': oncaptcha(captcha_content)
    }


    sessiona.post('http://222.200.98.147/login!doLogin.action', data = data, headers = headers)
    #print(resp.cookies)
    for i in range(1, 21):
        content = sessiona.get('http://222.200.98.147/xsgrkbcx!getKbRq.action?xnxqdm=201701&zc='+str(i)).text
        info = json.loads(content)[0]
        if(not info):
            continue
        with open('courses.json', 'a') as fb:
            fb.write(json.dumps(info, indent=4, ensure_ascii=False))



if __name__ == "__main__":
    login(get_captcha)




