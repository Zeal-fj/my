# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 12:39:32 2020

@author: 370125229 and Zeaf
"""
import tkinter as tk  #安装python，自带这个包
from tkinter import END  #单独把这个申明是因为后面的往text控件插入内容会报错
import requests,re
import time

# 一个顶层窗口的实例（Top Level），也称为根窗口
# #------------------------------窗口-----------------------------------#
window = tk.Tk()  #创建最上层主窗口
window.title("抖音视频解析@author Zeaf") #窗口标题
window.geometry("900x600") #窗口大小，中间是英文x,而不能是运算符*,很搞笑
#lable 组件是显示文字或图片，第一个参数是父窗口名称。
#text，参数显示内容，\n用来换行。每一行居中显示，靠左显示没研究，不需要，没那么高的要求。
#font字体，窗口太大，不设置字体，就会很小。
#place是依据主窗口的相对位置，，x就是x轴，下面所有的控件都需要这样定位
tk.Label(window,text="使用说明：分享链接请进入每个用户的界面点击它的视频进行分享，然后粘贴到本程序即可。",font=("华文行楷", 20)).place(x=50,y=20)
tk.Label(window,text="链接：",font=("华文行楷", 20)).place(x=50,y=150)
#Text组件用于显示和处理多行文本。我用来展示程序的运行状态，输出到这个组件里面
show_text = tk.Text()
show_text.place(x=500,y=150) 
#Entry输入框，输入的值必须要定义，这里定义成字符串类型
var_token = tk.StringVar()
#Entry输入框，输入的值必须要定义
entry_token = tk.Entry(window,textvariable = var_token)
entry_token.place(x=160,y=150) 
#按钮组件点击触发的函数，我把输入框的获取到的两个值输出到Text控件
#END就是插入到Text控件里面最后。
#.get就是获取目标的输入框的方法
def get_tar():
    token =  var_token.get() 
    share = token
    time.sleep(1)#停顿1s
    pat = '(https://v.douyin.com/.*?/)'  
    url = re.compile(pat).findall(share)[0]  #正则匹配分享链接
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
    show_text.insert(END, '获取到的链接：\n'+geturl+'\n保存成功!')
    with open('抖音视频.mp4', 'wb') as f:  # 用wb模式打开创建文件，w写模式
        f.write(response.content)  # 写入二进制文件内容  
        f.close
 
#Button组件，按钮组件，主要是触发一些功能，command指向一个函数就只触发的功能函数
get_detail = tk.Button(window,text='解析',font='20',command = get_tar)
get_detail.place(x=170,y=230)
 
 
#启动主窗口循环
window.mainloop()
