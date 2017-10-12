from bs4 import BeautifulSoup
from multiprocessing import Pool
from urllib.parse import urljoin

import requests
import os, time

def get_article(href, headers):
    print('run process %d' % os.getpid())
    start_time = time.time()
    s = BeautifulSoup(requests.get(href, headers=headers).content, "html.parser")
    headline_title = s.find(class_="headline-title").string
    question_title = s.find("h2").string
    author = s.find("span", class_="author").string
    content = s.find(class_="content")
    ps = content.find_all("p")
    with open(headline_title + '.txt', 'a') as fn:
        fn.write("Author: " + str(author) + "\r\n" + "question_title: " + str(
            question_title) + "\r\n" + "content: " + "\r\n" + "=======================================================" + "\r\n")
    for p in ps:
        if (not p.string):
            continue
        with open(headline_title + '.txt', 'a') as fn:
            fn.write("    " + str(p.string) + "\n")

    end_time = time.time()
    print('process:%d run for %0.2f seconds' % (os.getpid(), (end_time - start_time)))
    return (end_time - start_time)

if __name__ == '__main__':
    data = []
    all_time = 0
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
    }
    sessiona = requests.Session()
    sessiona.headers.update = headers
    # print(requests.get("http://www.baidu.com", headers = headers).content)
    soup = BeautifulSoup(sessiona.get("http://daily.zhihu.com/", headers=headers).content, "html.parser").find_all("a", class_="link-button")
    # print(soup)
    p = Pool(4)
    time_all = 0
    hrefs = []
    for href in soup:
        hrefs.append(urljoin("http://daily.zhihu.com", href['href']))
    content = requests.get(hrefs[0], headers=headers).content

    # s = BeautifulSoup(content, 'html.parser')
    # soup1 = s.find("h2")
    # soup2 = s.find(class_="author")
    # print(soup1.string)
    # print(soup2.string)
    # print(soup)
    for href in hrefs:
        all_time += p.apply_async(get_article, args=(href, headers)).get()

        # s = BeautifulSoup(requests.get(href, headers=headers).content, "html.parser")
        # question_title = s.find("h2").string
        # author = s.find("span", class_="author").string
        # content = s.find(class_="content")
        # ps = content.find_all("p")
        # with open(author+'.txt', 'a') as fn:
        #     fn.write("Author: " + str(author) + "\r\n" + "question_title: " + str(question_title) + "\r\n" + "content: " + "\r\n" + "=======================================================" + "\r\n")
        # for p in ps:
        #     if(not p.string):
        #         continue
        #     with open(author+'.txt', 'a') as fn:
        #         fn.write("    " + str(p.string) + "\n")
        # with open(author+'.txt', 'a') as fn:
        #         fn.write(content.p)
        # for tag in content:
        #     print(tag.string)
        # print(content)
        # data.append({'author': author, 'question-title': question_title})

        # with open(author + '.text', 'a') as fn:
        #     fn.write("作者: " + author + '\r\n' + "问题标题: " + question_title + '\r\n' + "文章内容: " + '\r\n' + '=============================================' + '\r\n')
        #     for tag in content:
        #         fn.write(tag.string)
        #     fn.write("=====================================\r\n")

        # each_time = get_article(href, headers)
        # time_all += each_time
        # p.apply_async(get_article, args=(href, headers))
        #data.append({'author': author, 'question_title': question_title})

    print('Waiting for all done...')
    p.close()
    p.join()
    print('All done, script worked for %0.2f' % all_time)

    # print(soup)