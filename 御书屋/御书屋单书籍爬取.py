# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 15:34:39 2020

@author: Zeaf
"""

import requests  # 导入requests库
import re  # 导入正则表达式库
import os # 保存文件
import time # 用来停顿
#伪装
user = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
}
#自定义书籍爬取
url1=input('请输入所要爬取书籍的网址：')#这里可以再去爬推荐榜什么的来替换
#多页爬取
i=15
while True:
    try:
        url=url1[:-1]+'_'+str(i)+'/#all'#补全网址
        response = requests.get(url,headers=user)#模拟访问
        response.encoding = response.apparent_encoding#防止乱码
        html = response.text  # 用文本显示访问网页得到的内容            
        url3s = re.findall('<li><a href="(.*?)">.*?</a></li>', html)  # 用正则表达式获得本页章节网址
        dir_name=re.findall('<h1>(.*?)</h1>', html)[-1]#正则提取书名,这里实际上提取到两个，选择一个
        print('正在保存的书籍为：'+dir_name)
        if not os.path.exists(dir_name):  # 判断文件夹是否存在，如果不存在：
            os.mkdir(dir_name)#创建文件夹
        if len(url3s) > 10:#防止无限循环，因为有最新章节存在
            for url3 in url3s:#遍历本页所有章节网址
                time.sleep(2)#暂停2s，防止频繁被发现
                url3 = 'https://m.xipu8.com'+url3#补全网址
                response = requests.get(url3,headers=user)
                response.encoding = response.apparent_encoding
                html = response.text  
                texts_in = re.findall('&nbsp;&nbsp;&nbsp;&nbsp;(.*?)<br/>', html)#提取文本内容
                text_true = ''#创建空字符串
                for texts in texts_in:#遍历文本内容
                    text_true=text_true+texts+'\n'#\n换行排版
                file_name = re.findall('<h1>(.*?)</h1>', html)[-1]#提取章节名
                with open(dir_name + '/'  + file_name+'.txt', 'wb') as f:#str(i)方便排序，不想要可去掉
                    f.write(text_true.encode())#encode()用于str转为bytes，py3.0必备，py2.0无需
                    f.write('\n'.encode())#换行
                    f.close()#关闭文件
                print('成功保存一章！')
            print('成功保存第'+str(i)+'页！') 
            i+=1#为进入下一页做准备
        else:
            print('本书保存完成！')
            break
    except:
        print('失败！')
        break#跳出循环
