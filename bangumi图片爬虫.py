# -*- coding: utf-8 -*-
"""
Created on Wed May  6 09:58:44 2020

@author: Zeaf
"""

import requests  # 导入requests库
import re  # 导入正则表达式库
import os # 保存文件
import threading    #导入多线程库

os.system('title bangumi图片爬取@Zeaf')#设置窗口标题
if not os.path.exists('img'):  # 判断文件夹是否存在，如果不存在：
    os.mkdir('img')  # 创建一个文件夹
user = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
}

def get_img(i):
    #爬取第i页图片
    url='https://bangumi.tv/anime/browser?sort=rank&page='+str(i)
    response = requests.get(url,headers=user)#模拟访问
    response.encoding = response.apparent_encoding#防止乱码
    html = response.text  # 用文本显示访问网页得到的内容            
    url1s = re.findall('<a href="(/subject/.*?)" class=', html)  # 用正则表达式获得本页各网址
    url1s = sorted(set(url1s),key=url1s.index) # 去除重复元素
    for url1 in url1s:
        url1 = 'https://bangumi.tv'+url1
        response = requests.get(url1,headers=user)#模拟访问
        response.encoding='utf8'#防止乱码
        html = response.text  # 用文本显示访问网页得到的内容            
        url2s = re.findall('<a href="(//lain.bgm.tv/pic/cover/.*?)" title', html)  # 用正则表达式获得图片直链
        file_name = re.findall('title="(.*?)" alt=', html)[0]
        url2 = 'https:'+url2s[0]
        response = requests.get(url2, headers=user)
        with open('img'+ '/' + file_name+'.jpg', 'wb') as f: 
            f.write(response.content) 
            print('成功保存图片'+file_name+'~')
    print('第'+str(i)+'线程结束！')
          
if __name__ == '__main__':    
    i = int(input('你想爬取的页数：'))
    for x in range(1,i+1):
        threading.Thread(target=get_img, args=(x,)).start() # 启动多线程
