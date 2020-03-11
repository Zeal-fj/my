# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 10:50:21 2020

@author: Zeaf
"""

import requests  # 导入requests库
import re  # 导入正则表达式库
import time  # 导入时间库
import pandas as pd # 导入pandas库
import matplotlib.pyplot as plt
import wordcloud as wc

print('created by Zeaf')
print('若想停止请按ctrl+C')
user = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
}
response = requests.get('http://www.pkulaw.cn/cluster_form.aspx?Db=news&menu_item=law&EncodingName=&keyword=%u884C%u653F%u590D%u8BAE%u6CD5&range=name&',headers=user)  # 用requests库的get函数访问总网页，用headers进行伪装，获得源码
html = response.text  # 用文本显示访问网页得到的内容
urls = re.findall('href="(.*?)" target="_blank"', html)  # 用正则表达式获得所有文章网址
#创建空列表用于存储数据
title_in = []
date_in = []
place_in = []
keyword_in = []
url_in = []
for url in urls:#循环输出获得的网址
    time.sleep(1)#暂停1s
    url= 'http://www.pkulaw.cn/'+url#因为爬取得到的网址只是部分，故以此方式填充
    response = requests.get(url,headers=user)  # 用requests库的get函数访问总网页，用headers进行伪装，获得源码
    html = response.text  # 用文本显示访问网页得到的内容
    title = re.findall('<strong>(.*?)</strong>', html)  # 获取标题
    date = re.findall('【发布日期】</font> (.*?)</td>', html) # 获取日期
    place = re.findall('【来源】</font> (.*?)</td>', html) # 获取来源
    keyword = re.findall('【关键词语】</font> <a href=".*?" target=_blank>(.*?)</a>', html) # 获取关键词
    #合并数据用于制表
    title_in.append(title[0])#注意这里title为列表，须先读取后导入，下同
    date_in.append(date[0])
    place_in.append(place[0])
    keyword_in.append(keyword[0])
    url_in.append(url)
    print('保存中...')
#导入数据
data={'标题':title_in, '发布日期':date_in, '来源':place_in, '关键词语':keyword_in,'原文链接':url_in}
y=pd.DataFrame(data)
y.to_excel('news.xlsx',index=False)#制表
print('生成表格成功！')
#绘制词云
content = ' '.join(keyword_in)
wordcloud = wc.WordCloud(max_words=50,font_path='simhei.ttf').generate(content)#黑体字
plt.imshow(wordcloud)#绘制
plt.show()
wordcloud.to_file('news.jpg')#保存图片，可以d:\来指定目录
