# coding:utf-8
import requests
import re
import os

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
url1 = 'https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8'
url2 = 'https://mm.taobao.com/self/aiShow.htm?userId='
data={'currentPage':1}

def get_html(url):
    response = requests.get(url, headers=headers)
    html = response.text
    return html

#取出总页数
def get_totle_page(url):
    html=get_html(url)
    return re.findall(r'totalPage":(\d*)',html)

#取出userId
def get_ID():
    for i in range(int(get_totle_page(url1)[0])):
        data['currentPage']=i+1
        response=requests.post(url1,data=data)
        html = response.text
        yield re.findall(r'userId":(\d*)', html)

#取出所有图的链接
def get_img():
    for i in get_ID():
        for j in i:
            html = get_html(url2 + j)
            yield re.findall(r'src="//(.*?)"/>', html)

def create_dir(x):
    if os.path.isdir('images/%s' % (x)):
        pass
    else:
        os.mkdir('images/%s' % (x))

def save_img():
    x = 0
    for i in get_img():
        x += 1
        create_dir(x)
        y = 0
        for j in i:
            y += 1
            img_url = 'https://' + j
            img = requests.get(img_url).content
            print('正在下载第%s组第%s张图片' % (x, y))
            with open('images/%s/%s.jpg' % (x, y), 'wb') as f:
                f.write(img)

if __name__ == '__main__':
    save_img()
