# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 17:47:23 2020

@author: Zeaf
"""

import tkinter as tk
from tkinter import END  #单独把这个申明是因为后面的往text控件插入内容会报错
import requests,re,time,codecs,os
import pandas as pd # 导入pandas库
import matplotlib.pyplot as plt
import wordcloud as wc
import pandas as pd

zeaf=tk.Tk() #生成root主窗口
zeaf.title("工具箱@Author Zeaf") #窗口标题
zeaf.geometry("1000x500") #窗口大小，中间是英文x,而不能是运算符*,很搞笑
#zeaf.resizable(0,0) #框体大小可调性，分别表示x,y方向的可变性,0即指不能缩放；
tk.Label(zeaf,text="如出现问题请联系作者！",font=("华文行楷", 20)).place(x=50,y=20)
tk.Label(zeaf, text="输入：", font=13).place(x=40,y=100)#贴标签
tk.Label(zeaf, text="其它：", font=13).place(x=40,y=205)#贴标签
tk.Label(zeaf, text="输出：", font=13).place(x=400,y=60)#贴标签
#输入值与输入框
input_1=tk.StringVar()
tk.Entry(zeaf, font=10, textvariable = input_1).place(x=100,y=100)
#加入滑动条！！！
scrollbar=tk.Scrollbar(zeaf)
scrollbar.place(x=900,y=100,height=300)
text=tk.Text(zeaf, font=10,yscrollcommand=scrollbar.set)#yscrollcommand=scrollbar.set设置滑动条
text.place(x=400,y=100,width=500,height=300)
scrollbar.config(command=text.yview)#.config(command=text.yview)同步text内容
text.insert(END, 'Github:https://github.com/Zeal-fj/my/tree/python\n无响应时请看cmd窗口，iso图片需开代理。')

def get_douyin(): 
    share = input_1.get()#千万记得加括号！
    pat = '(https://v.douyin.com/.*?/)'  
    url_in = re.compile(pat)
    try:
        url = url_in.findall(share)[0]#正则匹配分享链接    
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3904.108 Safari/537.36'
        }
        r = requests.get(url, headers=headers)
        pat = 'playAddr: "(.*?)",'
        play = re.compile(pat).findall(r.text)[0].replace("playwm", "play")
        headers = {
            'user-agent': 'Android',
        }
        r = requests.get(play, headers=headers, allow_redirects=False)
        geturl = r.headers['location']
        response = requests.get(geturl, headers=headers)
        text.insert(END, '\n获取到的链接：\n'+geturl)
        with open('短视频.mp4', 'wb') as f:  # 用wb模式打开创建文件，w写模式
            f.write(response.content)  # 写入二进制文件内容  
            f.close
            text.insert(END, '\n保存成功!')
    except:
        text.insert(END, '\n获取链接失败或输入有误！')
      
tk.Button(zeaf, text='抖音解析',command=get_douyin).place(x=120,y=150)#加按钮,调用方法千万别加括号！！！

def get_law():
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
    text.insert(END, '\n保存成功！')
    #导入数据
    data={'标题':title_in, '发布日期':date_in, '来源':place_in, '关键词语':keyword_in,'原文链接':url_in}
    y=pd.DataFrame(data)
    y.to_excel('news.xlsx',index=False)#制表
    text.insert(END, '\n表格生成成功！')   
    #绘制词云
    content = ' '.join(keyword_in)
    wordcloud = wc.WordCloud(max_words=50,font_path='simhei.ttf').generate(content)#黑体字
    plt.imshow(wordcloud)#绘制
    plt.show()
    wordcloud.to_file('news.jpg')#保存图片，可以d:\来指定目录
    text.insert(END, '\n词云生成成功！')
    
tk.Button(zeaf, text='新闻获取+生成表格+制作词云',command=get_law).place(x=100,y=200,width=248)#加按钮,调用方法千万别加括号！！！

def get_bilibili():
    url_in=[]#创建空列表
    keyword=input_1.get()#千万记得加括号！
    text.insert(END, '\n正在保存中...')
    try:
        for i in range(1,10):#运用循环语句输出多个页码，这里可改为列表
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
        text.insert(END, '保存成功正在生成表格...')
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
        text.insert(END, '\n表格生成成功！')
    except:
        text.insert(END, '\n未获取到内容！')

tk.Button(zeaf, text='b站数据',command=get_bilibili).place(x=240,y=150)#加按钮,调用方法千万别加括号！！！

def get_lowiso():
    def save():#定义一个函数用来保存图片
        for url,name in zip(urls, names):  # 循环获取每一个图片网址和标题
            time.sleep(3)  # 设定3秒延时,太快会被检测
            response = requests.get(url, headers=user)  # 用requeste库的get函数访问图片网址，用headers进行伪装
            print("正在保存图片中……")
            with open('iso图片/'+name+'.jpg', 'wb') as f:  # 用wb模式打开创建文件，w写模式
                f.write(response.content)  # 写入二进制文件内容  
                
    if not os.path.exists('iso图片'):  # 判断文件夹是否存在，如果不存在：
        os.mkdir('iso图片')  # 创建一个文件夹
    user = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    response = requests.get('https://isorepublic.com/',headers=user)  # 用requests库的get函数访问总网页，用headers进行伪装，获得源码
    html = response.text  # 用文本显示访问网页得到的内容
    urls = re.findall('https://isorepublic.com/wp-content/uploads/.*?.jpg', html)  # 用正则表达式获得图片的所有网址
    names = re.findall('title="(.*?)" class=', html)  # 正则表达式创建图片名字
    if len(urls):#判断提取的地址是否为空
        save()
        print("保存第1页图片完毕！")
        for i in range(2,6): #循环输出2-99（实际上还不止100页）
            response = requests.get('https://isorepublic.com/page/'+str(i)+'/',headers=user)
            html = response.text  # 用文本显示访问网页得到的内容
            urls = re.findall('https://isorepublic.com/wp-content/uploads/.*?.jpg', html)
            names = re.findall('title="(.*?)" class=', html)
            if len(urls):
                save()
                print("保存第"+str(i)+"页图片完毕！")
            else:
                text.insert(END, '\n保存失败')
    else:
        text.insert(END, '\n保存失败')
    text.insert(END, '\n完毕！')
def get_highiso():
    def save():#定义一个函数用来保存图片
        for url,name in zip(urls,names):
            response = requests.get(url, headers=user)  # 用requeste库的get函数访问图片网址，用headers进行伪装
            with open('iso图片/'+name+'.jpg', 'wb') as f:  # 用wb模式打开创建文件，w写模式
                f.write(response.content)  # 写入二进制文件内容  
                f.close
                print('保存图片成功！')
    
    if not os.path.exists('iso图片'):  # 判断文件夹是否存在，如果不存在：
        os.mkdir('iso图片')  # 创建一个文件夹
    user = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
    }
    response = requests.get('https://isorepublic.com/',headers=user)  # 用requests库的get函数访问总网页，用headers进行伪装，获得源码
    html = response.text  # 用文本显示访问网页得到的内容
    urls_in = re.findall('<a href="(https://isorepublic.com/photo/.*?)" title=', html)  # 用正则表达式获得进入图片的所有网址
    if len(urls_in):#判断提取的网址是否为空
        for url_in in urls_in:#循环获取每一个图片的进入网址
            time.sleep(5)#快了GG
            response = requests.get(url_in,headers=user)#打开图片进入网址获取源码
            html = response.text
            urls = re.findall('<a href="(https://isorepublic.com/wp-content/uploads/.*?\.jpg)" title=', html)  # 用正则表达式获得图片的网址
            names = re.findall('.jpg" title="Download (.*?)"', html)  # 正则表达式创建图片名字
            if len(urls):
                save()#调用之前定义的函数保存
            else:
                print('获取图片网址失败！')
        print('保存第1页图片完毕！')
    else:
        print('获取进入网址失败！')        
    #获取多页内容
    for i in range(2,6):#循环输出2-99
        response = requests.get('https://isorepublic.com/page/'+str(i)+'/',headers=user)  # 用requests库的get函数访问总网页，用headers进行伪装，获得源码
        html = response.text  # 用文本显示访问网页得到的内容
        urls_in = re.findall('<a href="(https://isorepublic.com/photo/.*?)" title=', html)  # 用正则表达式获得进入图片的所有网址
        if len(urls_in):#判断提取的网址是否为空
            for url_in in urls_in:#循环获取每一个图片的进入网址
                time.sleep(5)#快了GG
                response = requests.get(url_in,headers=user)#打开图片进入网址获取源码
                html = response.text
                urls = re.findall('<a href="(https://isorepublic.com/wp-content/uploads/.*?\.jpg)" title=', html)  # 用正则表达式获得图片的网址
                names = re.findall('.jpg" title="Download (.*?)"', html)  # 正则表达式创建图片名字
                if len(urls):
                    save()#调用之前定义的函数保存
                else:
                    text.insert(END, '\n获取图片网址失败！')
            print('保存第'+str(i)+'页图片完毕！')
        else:
            text.insert(END, '\n获取进入网址失败！')
    text.insert(END, '\n完毕！')

tk.Button(zeaf, text='iso图片获取',command=get_lowiso).place(x=100,y=240)#加按钮,调用方法千万别加括号！！！
tk.Button(zeaf, text='iso高清图片',command=get_highiso).place(x=252,y=240)#加按钮,调用方法千万别加括号！！！
#tk.Menu(zeaf)
zeaf.mainloop()
