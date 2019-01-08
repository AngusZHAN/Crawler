import os
from selenium import webdriver
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

        # 模拟Chrome发送网络请求, 把结果写入到文件夹中
        browser = webdriver.Chrome()
        browser.get(url)
        content = bytes(browser.page_source, encoding = "utf-8")
        with open(path, 'wb') as f:
            f.write(content)
        return browser.page_source


def house_from_div(div):
    """
    从一个 div 里面获取到一个房屋信息
    """
    e = pq(div)

    h = House()
    h.title = e('.content__list--item--title twoline').text()
    h.detail = e('.content__list--item--des').text()
    h.rent = e('.content__list--item-price').text()
    h.cover_url = e('content__list--item--aside').attr('href')

    return h


def houses_from_url(url):
    '''
    从 url 中下载网页并解析出页面内所有的信息
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
    # 调用 house_from_div
    # list comprehension
    houses = [house_from_div(i) for i in items]
    return houses


def print_info(houses):
    '''
    将爬取到的信息写入输出
    '''
    for h in houses:
        print(h.title)
        print(h.detail)
        print(h.rent)
        print(h.cover_url)
    


def main():
    for i in range(1, 4):
        url = 'https://sh.lianjia.com/zufang/pg{}'.format(i)
        houses = houses_from_url(url)
        print_info(houses)


if __name__ == '__main__':
    main()
