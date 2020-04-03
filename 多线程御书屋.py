# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 20:33:49 2020

@author: Zeaf
"""

import requests  # 导入requests库
import re  # 导入正则表达式库
import os # 保存文件
import time # 用来停顿
import threading    #导入多线程库
os.system('吾爱破解@Zeaf')
print('@Author Zeaf')
user = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
}
def get_book(url_in, webname):
    number=1
    while True:
        try:
            url=url_in[:-1]+'_'+str(number)+'/#all'#补全网址
            response = requests.get(url,headers=user)#模拟访问
            response.encoding = response.apparent_encoding#防止乱码
            html = response.text  # 用文本显示访问网页得到的内容            
            url3s = re.findall('<li><a href="(.*?)">.*?</a></li>', html)  # 用正则表达式获得本页章节网址
            dir_name=re.findall('<h1>(.*?)</h1>', html)[-1]#正则提取书名,这里实际上提取到两个，选择一个
            print('正在保存的书籍为：'+dir_name)
            if not os.path.exists(webname+'/'+dir_name):  # 判断文件夹是否存在，如果不存在：
                os.mkdir(webname+'/'+dir_name) # 创建文件夹
            if len(url3s) > 10: # 防止无限循环，因为有最新章节存在
                for url3 in url3s: # 遍历本页所有章节网址
                    time.sleep(stop) # 暂停，防止频繁被发现
                    url3 = 'https://m.xipu8.com'+url3 # 补全网址
                    response = requests.get(url3,headers=user)
                    response.encoding = response.apparent_encoding
                    html = response.text  
                    texts_in = re.findall('&nbsp;&nbsp;&nbsp;&nbsp;(.*?)<br/>', html)#提取文本内容
                    text_true = '' # 创建空字符串
                    for texts in texts_in: # 遍历文本内容
                        text_true=text_true+texts+'\n' # \n换行排版
                    file_name = re.findall('<h1>(.*?)</h1>', html)[-1] # 提取章节名
                    with open(webname+'/'+dir_name + '/'  + file_name+'.txt', 'wb') as f: # str(number)方便排序，不想要可去掉
                        f.write(text_true.encode()) # encode()用于str转为bytes，py3.0必备，py2.0无需
                        f.write('\n'.encode()) # 换行
                        f.close() # 关闭文件，可去除，with open自带关闭功能
                    print('成功保存一章！')
                print('成功保存第'+str(number)+'页！') 
                number+=1 # 为进入下一页做准备
            else:
                print('本书保存完成！')
                break
        except:
            print('失败！')
            break # 跳出循环    
        
def get_allvote():
    #爬取总推荐榜
    for i in range(1,pages+1):    
        response = requests.get('https://m.xipu8.com/top/allvote_'+str(i)+'/', headers=user)  # 用requests库的get函数访问总网页，用headers进行伪装，获得源码
        response.encoding = response.apparent_encoding # 防止乱码
        html = response.text  # 用文本显示访问网页得到的内容
        urls = re.findall('<a href="(/.*?/)" class="blue">', html)  # 用正则表达式获得本页所有文章网址
        for url in urls: # 遍历获取到的文章链接
            time.sleep(stop)
            url_in = 'https://m.xipu8.com/'+url # 补全本页所有文章链接
            webname = '总推荐榜'
            if not os.path.exists(webname):  # 判断文件夹是否存在，如果不存在：
                os.mkdir(webname) # 创建文件夹
            get_book(url_in, webname) # 调用之前写好的函数
        print('已爬取完总推荐榜一页！')
    print('第一线程运行完毕！')
    
def get_postdate():
    #爬取最新入库
    for i in range(1,pages+1):    
        response = requests.get('https://m.xipu8.com/top/postdate_'+str(i)+'/', headers=user)  # 用requests库的get函数访问总网页，用headers进行伪装，获得源码
        response.encoding = response.apparent_encoding # 防止乱码
        html = response.text  # 用文本显示访问网页得到的内容
        urls = re.findall('<a href="(/.*?/)" class="blue">', html)  # 用正则表达式获得本页所有文章网址
        for url in urls: # 遍历获取到的文章链接
            time.sleep(stop)
            url_in = 'https://m.xipu8.com/'+url # 补全本页所有文章链接
            webname = '最新入库'
            if not os.path.exists(webname):  # 判断文件夹是否存在，如果不存在：
                os.mkdir(webname) # 创建文件夹
            get_book(url_in, webname) # 调用之前写好的函数
        print('已爬取完最新入库一页！')
    print('第二线程运行完毕！')
    
def get_allvisit():
    #爬取总点击榜
    for i in range(1,pages+1):    
        response = requests.get('https://m.xipu8.com/top/allvisit_'+str(i)+'/', headers=user)  # 用requests库的get函数访问总网页，用headers进行伪装，获得源码
        response.encoding = response.apparent_encoding # 防止乱码
        html = response.text  # 用文本显示访问网页得到的内容
        urls = re.findall('<a href="(/.*?/)" class="blue">', html)  # 用正则表达式获得本页所有文章网址
        for url in urls: # 遍历获取到的文章链接
            time.sleep(stop)
            url_in = 'https://m.xipu8.com/'+url # 补全本页所有文章链接
            webname = '总点击榜'
            if not os.path.exists(webname):  # 判断文件夹是否存在，如果不存在：
                os.mkdir(webname) # 创建文件夹
            get_book(url_in, webname) # 调用之前写好的函数
        print('已爬取完总点击榜一页！')
    print('第三线程运行完毕！')

pages = int(input('爬取页数：'))
stop = int(input('停顿时间（整数）：'))
t1 = threading.Thread(target=get_allvote)    #第一个线程
t2 = threading.Thread(target=get_postdate)    #第二个线程
t3 = threading.Thread(target=get_allvisit)    #第三个线程
t1.start()    #启动第一个线程
t2.start()   #以此类推
t3.start()
