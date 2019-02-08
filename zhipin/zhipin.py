import os
import requests
import time
from pyquery import PyQuery as pq

class Model(object):
    '''
    基类, 用来显示类的信息
    '''
    def __repr__(self):
        name = self.__class__.__name__
        properties = ('{}=({})'.format(k, v) for k, v in self.__dict__.items())
        s = '\n<{} \n  {}>'.format(name, '\n  '.join(properties))
        return s


class Job(Model):
    '''
    存储工作信息
    '''
    def __init__(self):
        self.title = ''
        self.demand = ''
        self.salary = ''
        self.conpany = ''
        self.detail_url = ''


def cached_url(url):
    '''
    网页缓存, 避免重复下载网页
    '''
    folder = 'cached'
    filename = url.split('ka=', 1)[-1] + '.html'
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
            'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
            }
        # 发送网络请求, 把结果写入到文件夹中
        r = requests.get(url, headers=headers)
        with open(path, 'wb') as f:
            f.write(r.content)
        return r.content


def job_from_div(div):
    '''
    从一个 div 里面获取到一个职位信息
    '''
    e = pq(div)

    # 小作用域变量用单字符
    j = Job()
    j.title = e('.job-title').text()
    j.demand = e('p').text()
    j.salary = e('.red').text()
    j.conpany = e('.conpany-text').text()
    j.detail_url = e('.info-primary a').attr('href')

    return j


def job_from_url(url):
    '''
    从 url 中下载网页并解析出页面内所有的职位信息
    只会下载一次
    '''
    page = cached_url(url)
    '''
    1. 解析 dom
    2. 找到父亲节点
    3. 每个子节点拿一个job-primary
    '''
    e = pq(page)
    # print(page.decode())
    # 2.父节点
    job_list = e('.job-primary')
    # 调用 book_from_div
    # list comprehension
    jobs = [job_from_div(i) for i in job_list]
    return jobs


def print_info(jobs):
    for j in jobs:
        print(j.title)
        print(j.demand)
        print(j.salary)
        print(j.conpany)
        print(j.detail_url)


def main():
    '''
    开始爬取先关职位信息
    '''
    for i in range(1, 10):
        url = 'https://www.zhipin.com/c101020100/?query=python&page={}&ka=page-{}'.format(i, i)
        #限制爬取速度，防止封IP
        time.sleep(5)
        jobs = job_from_url(url)
        print_info(jobs)


if __name__ == '__main__':
    main()
