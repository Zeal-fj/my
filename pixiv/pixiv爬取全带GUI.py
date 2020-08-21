# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 21:05:11 2020

@author: Zeaf
"""

import tkinter as tk # 导入tk库
from tkinter import END # 防止插入消息出错
import requests  # 导入requests库
import re  # 导入正则表达式库
import os # 保存文件
import threading    #导入多线程库

zeaf=tk.Tk() #生成root主窗口
zeaf.title("Pixiv图片爬取 @吾爱破解 Zeaf") #窗口标题
zeaf.geometry("980x500") #窗口大小，中间是英文x,而不能是运算符*,很搞笑
zeaf.resizable(0,0) #框体大小可调性，分别表示x,y方向的可变性,0即指不能缩放；
tk.Label(zeaf,text="遇到任何问题请联系原作者解决，本软件仅供学习交流使用！",font=("华文行楷", 13)).place(x=50,y=20)
tk.Label(zeaf, text="Tag：", font=13).place(x=40,y=100)#贴标签
tk.Label(zeaf, text="ID：", font=13).place(x=40,y=150)#贴标签
tk.Label(zeaf, text="Date：", font=13).place(x=40,y=200)#贴标签
tk.Label(zeaf, text="Page：", font=13).place(x=40,y=250)#贴标签
tk.Label(zeaf, text="Try：", font=13).place(x=40,y=300)#贴标签
tk.Label(zeaf, text="Output：", font=13).place(x=400,y=60)#贴标签
tk.Label(zeaf, text="By Zeaf", font=("Times New Roman",13)).place(x=890,y=460)#贴标签
#输入值与输入框
input_1=tk.StringVar()#定义输入值的类型，下同
input_2=tk.StringVar()
input_3=tk.StringVar()
input_4=tk.StringVar()
tk.Entry(zeaf, font=10, textvariable = input_1).place(x=100,y=100,width=248)#放置输入框
tk.Entry(zeaf, font=10, textvariable = input_2).place(x=100,y=150,width=248)
tk.Entry(zeaf, font=10, textvariable = input_3).place(x=100,y=200,width=248)
tk.Entry(zeaf, font=10, textvariable = input_4).place(x=100,y=250,width=248)
#加入图片
#photo = tk.PhotoImage(file="pixiv.gif")
#tk.Label(zeaf, image=photo).place(x=700,y=50)#贴标签
#加入滑动条！！！
scrollbar=tk.Scrollbar(zeaf)
scrollbar.place(x=900,y=100,height=350)
text=tk.Text(zeaf, font=10,yscrollcommand=scrollbar.set)#yscrollcommand=scrollbar.set设置滑动条
text.place(x=400,y=100,width=500,height=350)
scrollbar.config(command=text.yview)#.config(command=text.yview)同步text内容

text.insert(END, '#Tag为搜索关键词，ID为画师ID\n#Tag可加入热度，如女子5000users入り')
#定义下载函数
def download(name_url_id,file):
    name=name_url_id[0] # 获取元组信息
    id=name_url_id[1]
    url=name_url_id[2]
    user = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
    'Referer': 'https://pixivic.com/illusts/'+id+'?VNK=dbcbfa01', # 缺少此将返回403
    'Accept': 'image/png, image/svg+xml, image/*; q=0.8, */*; q=0.5',
    'Host': 'original.img.cheerfun.dev',
    'Cache-Control': 'max-age=0',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'Keep-Alive',
    'Accept-Language': 'zh-CN'
}   
    response = requests.get(url,headers=user)#模拟访问
    if response.status_code == 200: # 200即为成功
        if not os.path.exists('pixivimg'+ '/' +file+ '/' +name+'.jpg'): # 判断该图片是否存在，如果不存在
            text.insert(END, '\n正在下载图片：'+name)
            with open('pixivimg'+ '/' +file+ '/' +name+'.jpg', 'wb') as f: # 保存图片
                f.write(response.content) 
        else:
            text.insert(END, '\n'+name+'.jpg已存在，跳过。')
    else:
        text.insert(END, '\n错误代码'+str(response.status_code)+'下载图片'+name+'失败！')
#定义获取下载链接列表的函数
def get_downloadpool(tag,information,html): 
    downloadpool=[]
    if len(re.findall('{"message":"'+information+'"(.*?)}',html)[0]):#判断该页是否存在数据，如果存在            
        urls = re.findall('"original":"https://i.pximg.net/img-original/img/(..../../../../../../[0-9]*?_p0.*?g)"', html)  # 用正则表达式获得本页各网址
        names = re.findall('"artistId":.*?,"title":"(.*?)","type"', html) # 获取图片名字
        ids = re.findall('"original":"https://i.pximg.net/img-original/img/..../../../../../../([0-9]*?)_p0.*?g"', html) # 获取图片id，为后面referer做准备
        if not os.path.exists('pixivimg'):  # 判断文件夹是否存在，如果不存在：
            os.mkdir('pixivimg')  # 创建一个文件夹
        if not os.path.exists('pixivimg'+'/'+tag):  # 判断文件夹是否存在，如果不存在：
            os.mkdir('pixivimg'+'/'+tag)  # 创建一个文件夹   
        for name,url,id in zip(names,urls,ids): # 按顺序遍历每一个画作名称、下载链接和id
            url = 'https://original.img.cheerfun.dev/img-original/img/'+url # 真实的原图地址，抓包获得，无法直接访问
            try:
                # 防止创建文件时因名字问题失败
                name = name.replace('\\','_') 
                name = name.replace('/','_') 
                name = name.replace('?','')
            except:
                name = name
            downloadpool.append((name,id,url))
    else: # 不存在数据时的输出
        text.insert(END, '\n所选页数超出实际范围！')
    return downloadpool # 返回列表

#定义爬取搜索结果的函数
def pixiv_search():
    pages=input_4.get()
    tag=input_1.get()
    try:
        int(pages)
    except:
        text.insert(END, '\nPage输入有误！')
    if not len(tag):
        text.insert(END, '\nTag输入有误！')
    for page in [x for x in range(1,int(pages)+1)]: # 遍历每一页
        user = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
        } # 这里的ua随便写写就好，无限制
        url='https://api.pixivic.com/illustrations?illustType=illust&searchType=original&maxSanityLevel=4&page='+str(page)+'&keyword='+tag+'&pageSize=30' # 异步加载接口，返回json数组
        try:
            response = requests.get(url,headers=user) # 模拟访问
        except:
            text.insert(END, '\n网络错误或原网站波动，请稍后再试~')
        response.encoding = response.apparent_encoding # 防止乱码
        html = response.text  # 用文本显示访问网页得到的内容
        information='搜索结果获取成功'
        downloadpool = get_downloadpool(tag,information,html) # 调用函数并定义返回的列表
        text.insert(END, '\n获取下载链接成功，等待下载~')
        for name_url_id in downloadpool:
            threading.Thread(target=download, args=(name_url_id,tag)).start() # 启动多线程
            
tk.Button(zeaf, text='pixiv搜索【Tag+Page】',command=pixiv_search).place(x=100,y=300,width=248)#加按钮,调用方法千万别加括号！！！

#检测画师作品页数
def get_page(artistid,information):
    num = 1 # 设置初始页数
    while True:
        url='https://api.pixivic.com/artists/'+artistid+'/illusts/illust?page='+str(num)+'&pageSize=30&maxSanityLevel=10' # 异步加载接口，返回json数组
        user = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
        } # 这里的ua随便写写就好，无限制
        try:
            response = requests.get(url,headers=user)#模拟访问
        except:
            text.insert(END, '\n网络错误或原网站波动，请稍后再试~')
        response.encoding = response.apparent_encoding # 防止乱码
        html = response.text  # 用文本显示访问网页得到的内容 
        if len(re.findall('{"message":"'+information+'"(.*?)}',html)[0]): # 利用正则表达式获取数据，如果存在数据
            num+=1 # 页数+1
            #text.insert(END, '\n检测页数中...')
            continue # 继续循环
        else:
            text.insert(END, '\n检测成功，共有'+str(num-1)+'页！')
            break # 退出循环
                
def pixiv_artist():
    artistid=input_2.get()
    information='获取画师画作列表成功'
    try:
        int(artistid)
    except:
        text.insert(END, '\nID输入有误！')
    threading.Thread(target=get_page, args=(artistid,information)).start()
    pages=input_4.get()
    try:
        int(pages)
    except:
        text.insert(END, '\nPage输入有误！')
    for page in [x for x in range(1,int(pages)+1)]:
        user = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
        } # 这里的ua随便写写就好，无限制
        url='https://api.pixivic.com/artists/'+artistid+'/illusts/illust?page='+str(page)+'&pageSize=30&maxSanityLevel=10' # 异步加载接口，返回json数组
        try:
            response = requests.get(url,headers=user) # 模拟访问
        except:
            text.insert(END, '\n网络错误或原网站波动，请稍后再试~')
        response.encoding = response.apparent_encoding # 防止乱码
        html = response.text  # 用文本显示访问网页得到的内容
        artist = re.findall('"name":"(.*?)","account"',html) # 获取画师名字
        file = artist[0]+artistid # 设置文件夹名称
        downloadpool = get_downloadpool(file,information,html)  # 调用函数并定义返回的列表
        text.insert(END, '\n获取下载链接成功，等待下载~')
        for name_url_id in downloadpool:
            threading.Thread(target=download, args=(name_url_id,file)).start() # 启动多线程

tk.Button(zeaf, text='pixiv画师【ID+Page】',command=pixiv_artist).place(x=100,y=350,width=248)#加按钮,调用方法千万别加括号！！！

def pixiv_daily():
    information='获取排行成功'
    pages=input_4.get()
    try:
        int(pages)
    except:
        text.insert(END, '\nPage输入有误！')
    date=input_3.get()
    if not len(re.findall('[0-9]{4}-[0-9]{2}-[0-9]{2}',date)):
        text.insert(END, '\nDate输入有误！格式为:2020-07-11,且时间早于今日3天。')
    for page in [x for x in range(1,int(pages)+1)]:
        user = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
        } # 这里的ua随便写写就好，无限制
        url='https://api.pixivic.com/ranks?page='+str(page)+'&date='+date+'&mode=day&pageSize=30' # 异步加载接口，返回json数组
        try:
            response = requests.get(url,headers=user) # 模拟访问
        except:
            text.insert(END, '\n网络错误或原网站波动，请稍后再试~')
        response.encoding = response.apparent_encoding # 防止乱码
        html = response.text  # 用文本显示访问网页得到的内容
        downloadpool = get_downloadpool(date,information,html)  # 调用函数并定义返回的列表
        text.insert(END, '\n获取下载链接成功，等待下载~')
        for name_url_id in downloadpool:
            threading.Thread(target=download, args=(name_url_id,date)).start() # 启动多线程

tk.Button(zeaf, text='pixiv日榜【Date+Page】',command=pixiv_daily).place(x=100,y=400,width=248)#加按钮,调用方法千万别加括号！！！
zeaf.mainloop()
