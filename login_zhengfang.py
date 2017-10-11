import requests

url = "http://jwgl.gdut.edu.cn/default2.aspx"


def get_captcha(data):
    with open('captcha.gif','wb') as fb:
        fb.write(data)
    return input('captcha')

def login(number, password, oncaptcha):
    s = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Host': 'jwgl.gdut.edu.cn',
        'Referer': 'http://jwgl.gdut.edu.cn/default2.aspx',
    }
    s.headers.update(headers)

    captcha_content = s.get("http://jwgl.gdut.edu.cn/CheckCode.aspx").content
    data = {
        "__VIEWSTATE": "dDwyODE2NTM0OTg7Oz5UoOEfVcEjibt6YhO5jK121XS0BA==",
        "__VIEWSTATEGENERATOR": "92719903",
        "txtUserName": number,
        "TextBox2": password,
        "txtSecretCode": oncaptcha(captcha_content),
        "RadioButtonList1": "学生",
        "Button1": "",
        "lbLanguage": "",
        "hidPdrs": "",
        "hidsc": "",
    }

    resp = s.post(url, data=data)
    print(resp.text)
    cookies = dict(resp.cookies)
    print(cookies)
    # with open('url1.html', 'w') as fp:
    #     fp.write(content)

if __name__ == '__main__':
    login('3116004736', 'lzy2113018', get_captcha)