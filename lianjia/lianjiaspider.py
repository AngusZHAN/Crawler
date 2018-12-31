import os
import requests
from openpyxl import Workbook
from pyquery import PyQuery as pq

class Model(object):
    """
    基类, 用来显示类的信息
    """
    def __repr__(self):
        name = self.__class__.__name__
        properties = ('{}=({})'.format(k, v) for k, v in self.__dict__.items())
        s = '\n<{} \n  {}>'.format(name, '\n  '.join(properties))
        return s


class House(Model):
    """
    存储房屋信息
    """
    def __init__(self):
        self.title = ''
        self.detail = ''
        self.rent = ''
        self.cover_url = ''


def cached_url(url):
    """
    网页缓存, 避免重复下载网页
    """
    folder = 'cached'
    filename = url.split("zufang/", 1)[-1] + '.html'
    'cached/pg1.html'
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            s = f.read()
            return s
    else:
        # 建立 cached 文件夹
        if not os.path.exists(folder):
            os.makedirs(folder)

        headers = {
            'user-agent': '''Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36
            Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8''',
        }
        # 发送网络请求, 把结果写入到文件夹中
        r = requests.get(url, headers)
        with open(path, 'wb') as f:
            f.write(r.content)
        return r.content


def house_from_div(div):
    """
    从一个 div 里面获取到一个房屋信息
    """
    e = pq(div)

    h = House()
    h.title = e('.content__list--item--title twoline').text()
    h.detail = e('.content__list--item--des').text()
    h.rent = e('.content__list--item-price').text()
    h.cover_url = e('content__list--item--aside').attr('src')

    return h


def houses_from_url(url):
    '''
    从 url 中下载网页并解析出页面内所有的电影
    只会下载一次
    '''
    page = cached_url(url)
    '''
    1. 解析 dom
    2. 找到父亲节点
    3. 每个子节点拿一个movie
    '''
    e = pq(page)
    # print(page.decode())
    # 2.父节点
    items = e('.content__list--item')
    # 调用 movie_from_div
    # list comprehension
    houses = [house_from_div(i) for i in items]
    return houses


def download_image(url):
    folder = "img"
    name = url.split("/")[-1]
    path = os.path.join(folder, name)

    if not os.path.exists(folder):
        os.makedirs(folder)

    if os.path.exists(path):
        return

    headers = {
        'user-agent': '''Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36
         Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8''',
    }
    # 发送网络请求, 把结果写入到文件夹中
    r = requests.get(url, headers)
    with open(path, 'wb') as f:
        f.write(r.content)


def write_excel(houses):
    '''
    将爬取到的信息写入excel
    '''
    wb = Workbook(optimized_write=True)
    ws = []
    ws.append(wb.create_sheet(title=house))#utf8->unicode
    
    for i in range(len(houses)):
        ws[i].append(['房屋标题', '房屋详情', '每月租金', '图片详情'])
        count = 1
        for h in houses:
            ws[i].append([count, m[0], float(m[1]), m[2]])
            count += 1
    
    save_path = 'house'
    save_path += '.xlsx'
    wb.save(save_path)


def main():
    for i in range(3):
        url = 'https://sh.lianjia.com/zufang/pg{}'.format(i)
        houses = houses_from_url(url)
        write_excel(houses)
        print('链家租房信息', houses)
        [download_image(h.cover_url) for h in houses]


if __name__ == '__main__':
    main()
