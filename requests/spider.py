# -*- coding:utf-8 -*-

import json
import requests
from requests.exceptions import RequestException
import re

#获取一个url下的html文件
def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

# 解析网页
def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)'
                         '</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>'
                         '.*?fraction">(.*?)</i>.*?</dd>',re.S) #使用re.S参数以后，多行匹配；反之，则换行就重新匹配
    items = re.findall(pattern,html)
    for item in items:  # 将解析的结果格式化(生成一个字典）
        yield{
            'index':item[0],
            'image':item[1],
            'name':item[2],
            'actor':item[3].strip()[3:],  #strip()去除空格和\n
            'time':item[4].strip()[5:],
            'score':item[5]+item[6]
        }

#将爬取到的电影信息保存到本地文件夹
def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:#将编码格式设置为utf-8
        f.write(json.dumps(content,ensure_ascii=False)+'\n')#将字典转化为字符串
        f.close()

# 以offset作为参数，实现分页抓取数据
def main(offset):
    url = 'http://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    for i in range(10):#单线程
        main(i*10)
        
    #多线程：    
    #pool = Pool()
    #pool.map(main,[i*10 for i in range(10)])
 
