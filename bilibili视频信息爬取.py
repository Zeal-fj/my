#哔哩哔哩 - ( ゜- ゜)つロ 乾杯~
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 00:12:16 2019

@author: Zeaf
"""
import re,requests,codecs
import pandas as pd
import time

url_in=[]#创建空列表
keyword=input('请输入想要查找的关键词：')#个性化搜索
for i in range(1,10):#运用循环语句输出多个页码，这里可改为列表
    time.sleep(1)#停顿1s
    if i==1:
        kw={'keyword':keyword,'page':'1'}#keyword是输入的关键词，page是页码
        r=requests.get(url='https://search.bilibili.com/all?',params=kw)
        r.encoding='utf8'#防止乱码
        print(r.status_code)#200即正常
        #建立html源码文本
        x=codecs.open('缓存区.txt','w','utf8')
        x.write(r.text)
        x.close()
        #正则表达式提取（真的难搞）
        title=re.findall('<a title="(.*?)" href="//www.bilibili.com/',r.text)#标题
        playbacknumber=re.findall('<span title="观看" class="so-icon watch-num"><i class="icon-playtime"></i>\n        (.*?)\n      </span>',r.text)#播放量
        uploadtime=re.findall('<span title="上传时间" class="so-icon time"><i class="icon-date"></i>\n        (.*?)\n      </span>',r.text)#上传时间
        upname=re.findall('class="up-name">(.*?)</a>',r.text)#up主
        url=re.findall('<a title=".*?" href="(.*?)" target="_blank" class="title">',r.text)#视频链接
    else:
        kw={'keyword':keyword,'page':i}
        r=requests.get(url='https://search.bilibili.com/all?',params=kw)
        r.encoding='utf8'
        print(r.status_code)
        x=codecs.open('缓存区.txt','w','utf8')#若想保存所有源码文件可以插入'+str(i)+'，为节省空间采用此方式
        x.write(r.text)
        x.close()
        title_=re.findall('<a title="(.*?)" href="//www.bilibili.com/',r.text)
        title+=title_#叠加
        playbacknumber_=re.findall('<span title="观看" class="so-icon watch-num"><i class="icon-playtime"></i>\n        (.*?)\n      </span>',r.text)
        playbacknumber+=playbacknumber_
        uploadtime_=re.findall('<span title="上传时间" class="so-icon time"><i class="icon-date"></i>\n        (.*?)\n      </span>',r.text)
        uploadtime+=uploadtime_
        upname_=re.findall('class="up-name">(.*?)</a>',r.text)
        upname+=upname_
        url_=re.findall('<a title=".*?" href="(.*?)" target="_blank" class="title">',r.text)
        url+=url_
#将链接补全
url_in=[]
for url_true in url:
    i= 'https:'+url_true
    url_in.append(i)
data={'标题':title,'播放量':playbacknumber,'上传时间':uploadtime,'UP主':upname, '视频地址': url_in}
y=pd.DataFrame(data)
#下面浮点化数据方便作图（注意播放量单位带有”万“）
for a,b in enumerate(y['播放量']):   
    if b[-1]=='万':
        y['播放量'][a]=float(y['播放量'][a][:-1])*10000
    else:
        y['播放量'][a]=float(y['播放量'][a])
#下面建立excel文件
y.to_excel('有关'+keyword+'的哔哩哔哩视频信息.xlsx',index=False)#制表
y.plot(y='播放量',kind='hist')#制作直方图，要浮点化才能作图哦
print('请在与本文件同级区域查看输出表格')
time.sleep(5)
