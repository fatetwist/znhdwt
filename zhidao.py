import requests
import re
import json
import random
from bs4 import BeautifulSoup
headers = {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'Accept-Encoding': "gzip, deflate, sdch, br",
        'Accept-Language': "zh-CN,zh;q=0.8",
        'Connection': "keep-alive",
        'Cookie': "BAIDUID=3ED486A4F56C74DC6D49748C7C1601F5:FG=1; BIDUPSID=3ED486A4F56C74DC6D49748C7C1601F5; PSTM=1515997906; MCITY=-163%3A; FP_UID=f8d270d822e069af943418397b3bd9f2; BDUSS=Hh5YndZRUx0NUJ3cndBeXBFeHIwMExsY2owOEw4Wm1DNmt3ajJsZUNVelhPNHhhQVFBQUFBJCQAAAAAAAAAAAEAAABHHYw22K-7ytfl7OHW78POAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANeuZFrXrmRaN; BDRCVFR[EaNsStaiD7m]=mk3SLVN4HKm; PSINO=6; H_PS_PSSID=1468_21121; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; Hm_lvt_6859ce5aaf00fb00387e6434e4fcc925=1516354817,1516360224,1516547437,1516547465; Hm_lpvt_6859ce5aaf00fb00387e6434e4fcc925=1516549149",
        'Host': "zhidao.baidu.com",
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': "Mozilla/5.0 (iPhone 84; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.8.0 Mobile/14G60 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",
        'Cache-Control': "no-cache",
    }


def download(url,headers,retries=2,encoding='auto'):
    res = requests.request('GET', url, headers=headers)
    if encoding != 'auto':
        res.encoding = encoding

    if res.status_code == 200 :
        return res.text
    elif 400 <= res.status_code < 500:
        return 'Error: Not Found'
    elif res.status_code >= 500:
        retries -= 1
        while retries == 0:
            res = requests.request('GET', url, headers=headers)
            if res.status_code == 200:
                retries = 0
                return res.text
            else:
                retries -= 1
        return 'Error: Service Error'
    else:
        return 'Error: Unknown Error'


def download_soup(url, headers, encoding='auto'):
    res = requests.get(url,headers=headers)
    if encoding == 'auto':
        encoding = res.encoding
    soup = BeautifulSoup(res.content,'html.parser',from_encoding=encoding)
    return soup


def get_answer_by_id(id):
    url = 'https://zhidao.baidu.com/question/%s.html?fr=qlquick&entry=qb_list_default&is_force_answer=0' % id

    text = download(url, headers=headers, encoding='utf-8')
    rp = {}
    # rp{title,best,answers,status}
    if '最佳答案' in text:
        rp['best'] = True
    else:
        rp['best'] = False
    with open('html','a+') as file :
        file.write(text)
    if text.__len__() > 100:
        # 获得问题并检查是否为百度知道标准问题
        _title = re.findall('<title>\n(.+?)\n</title>', text)

        if _title:
            title = _title[0]
        else:
            rp['answers'] = ''
            rp['title'] = ''
            rp['status'] = '2'
            rp['error'] = text
            return rp

        # 获得回答
        regex_best = re.compile('<div class="full-content">\n(.+?)\n</div>.+?')
        answers = regex_best.findall(text)
        rp['answers'] = answers
        rp['title'] = title
        rp['status'] = '4'
        return rp
    else:
        rp['answers'] = ''
        rp['title'] = ''
        rp['status'] = '3'
        rp['error'] = text
        return rp


def search_question(keyword):
    url = 'https://zhidao.baidu.com/search?word=' + keyword
    soup = download_soup(url,headers=headers,encoding='utf-8')
    a = soup.select('a.search-title')
    a = [x.get('href') for x in a]

    id = []
    for x in a:
        try:
            id.append(re.findall(r'/question/(.+?)\?',x)[0])
        except IndexError:
            pass

    return id



def start(a,b):
    for x in range(a, b+1):
        contents = get_answer_by_id(x)
        # 检查状态
        status = contents['status']
        if status == '4':
            answers = contents['answers']
            has_best = contents['best']
            title = contents['title']

        else:
            best_answer = '没有最佳答案'
            answer = '没有回答'
            title = '无标题'
        # best_answer answer title
        # 开始放入数据库...



# while True:
#     word = input('请输入关键词：')
#     ids = search_question(word)
#     a = random.randint(0, len(ids))
#     answers = get_answer_by_id(ids[a])
#     b = random.randint(0, len(answers['answers'])-1)
#     print(len(answers['answers']))
#     print(b)
#     print(answers['answers'][b])


