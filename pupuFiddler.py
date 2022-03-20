# codeing = utf-8
#@Time : 2020/3/19
#Author : 212106729 潘乐静
#@File : pupuFiddler.py
#@Software : PyCharm

from bs4 import BeautifulSoup  #网页解析，获取数据，爬完网页将其中数据进行拆分
import re   #正则表达式，进行文字匹配，数据提炼
import urllib.request,urllib.error   #制定URL，获取网页数据，给网页就能爬
import xlwt   #进行Excel操作，存入Excel
import sqlite3  #进行SQLite 数据库操作 ，存入数据库
import requests
import datetime

def main():
    # 目标地址：
    baseUrl = "https://j1.pupuapi.com/client/product/storeproduct/detail/7c1208da-907a-4391-9901-35a60096a3f9/207af835-5dbf-4dcf-90ce-cbc680bcd0b9"
    #1、爬取网页
    dataList = getData(baseUrl)
    savePath = r".\朴朴商品信息.xls"
    #3、保存数据
    # saveData(savePath)
    # askURL("https://j1.pupuapi.com/client/product/storeproduct/detail/7c1208da-907a-4391-9901-35a60096a3f9/dc749b90-1781-40f9-b5af-3d0d944260c4")

#爬取网页
def getData(baseUrl):
    url = baseUrl  #调用获取页面信息的函数
    html = askURL(url)  #保存获取到的网页源码

    #2、逐一解析数据
    #①使用bs4逐一解析，拿到数据
    soup = BeautifulSoup(html, "html.parser")  #指定html解析器
    #②从bs4对象中查找数据
    # find(标签, 属性=值)  找第一个
    # find_all(标签, 属性=值)  找所有
    # dataList = []
    # return dataList

#得到指定一个URL的网页内容
def askURL(url):
    #伪装
    #模拟浏览器头部信息，向服务器发送消息
    head = {
        # 用户代理，表示告诉服务器，我们是什么类型的机器：浏览器，本质上是告诉浏览器，我们可以接受什么水平的文件内容
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0"
    }

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        print(html)
        response_result = requests.get(url, headers=head).json()
        data = response_result['data']
        name = data['name']  # 商品名称
        spec = data['spec']  # 商品规格
        price = str(data['price'] / 100)  # 商品价格
        market_price = str(data['market_price'] / 100)  # 原价
        share_content = data['share_content']  # 分享内容
        print('---------------商品：' + name + '---------------')
        print('规格：' + spec)
        print('价格：' + price)
        print('原价/折扣价：' + price + "/" + market_price)
        print('详细内容：' + share_content + '\n')
        print('---------------”' + name + '“价格波动---------------')
        for priceFluctuation in range(1, 8):  # 多次请求查看价格波动
            response = requests.get(url, headers=head).json()
            price = str(data['price'] / 100)
            time_stamp = datetime.datetime.now()
            print('当前时间为' + time_stamp.strftime('%Y.%m.%d-%H:%M:%S') + ',价格为' + price)

    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# #保存数据
# def saveData(savePath):
#     print(" ")


#按程序以我们组织的顺序来调用
if __name__ == "__main__":  #当程序执行时
    #调用函数
    main()

