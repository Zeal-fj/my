# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 13:25:46 2020

@author: Zeaf
"""
import requests  # 导入requests库
import re  # 导入正则表达式库
import os # 保存文件
import threading    #导入多线程库

os.system('title pixiv画师爬取@Zeaf')#设置窗口标题
if not os.path.exists('pixivimg'):  # 判断文件夹是否存在，如果不存在：
    os.mkdir('pixivimg')  # 创建一个文件夹
print('原网站：https://pixivic.com/')
print('因本人只看插画，所以为名字与插画对应，实际上获得的图片少于原页面上应有的图片。')
'''
VNK = input('请输入VNK（可跳过）：') # 获取VNK，虽然仍然不知道有什么用，不过是根据ua变化的VNK
if VNK == '':
    VNK = 'dbcbfa01' # 默认的VNK
'''
VNK = 'dbcbfa01' # 默认的VNK
artistid = input('请输入你想爬取的画师的id（网址上就有哦）：') # 获取画师id

#检测画师作品页数
num = 1 # 设置初始页数
while True:
    url='https://api.pixivic.com/artists/'+artistid+'/illusts/illust?page='+str(num)+'&pageSize=30&maxSanityLevel=10' # 异步加载接口，返回json数组
    user = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
    } # 这里的ua随便写写就好，无限制
    response = requests.get(url,headers=user)#模拟访问
    response.encoding = response.apparent_encoding # 防止乱码
    html = response.text  # 用文本显示访问网页得到的内容 
    if len(re.findall('{"message":"获取画师画作列表成功"(.*?)}',html)[0]): # 利用正则表达式获取数据，如果存在数据
        num+=1 # 页数+1
        print('检测页数中...')
        continue # 继续循环
    else:
        print('检测成功，共有'+str(num-1)+'页！') # 提示用户页数
        break

# 爬取单页的函数
def get_artist(page):
    user = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
    } # 这里的ua随便写写就好，无限制
    url='https://api.pixivic.com/artists/'+artistid+'/illusts/illust?page='+str(page)+'&pageSize=30&maxSanityLevel=10' # 异步加载接口，返回json数组
    response = requests.get(url,headers=user) # 模拟访问
    response.encoding = response.apparent_encoding # 防止乱码
    html = response.text  # 用文本显示访问网页得到的内容            
    urls = re.findall('"original":"https://i.pximg.net/img-original/img/(..../../../../../../[0-9]*?_p0.*?g)"', html)  # 用正则表达式获得本页各网址
    names = re.findall('"artistId":.*?,"title":"(.*?)","type"', html) # 获取图片名字
    ids = re.findall('"original":"https://i.pximg.net/img-original/img/..../../../../../../([0-9]*?)_p0.*?g"', html) # 获取图片id，为后面referer做准备
    artist = re.findall('"name":"(.*?)","account"',html) # 获取画师名字
    file = artist[0]+artistid # 设置文件夹名称
    if not os.path.exists('pixivimg'+'/'+file):  # 判断文件夹是否存在，如果不存在：
        os.mkdir('pixivimg'+'/'+file)  # 创建一个文件夹   
    for name,url,id in zip(names,urls,ids):
        user = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
        'Referer': 'https://pixivic.com/illusts/'+id+'?VNK='+VNK, # 缺少此将返回403
        'Accept': 'image/png, image/svg+xml, image/*; q=0.8, */*; q=0.5',
        'Host': 'original.img.cheerfun.dev',
        'Cache-Control': 'max-age=0',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'Keep-Alive',
        'Accept-Language': 'zh-CN'
    }
        url = 'https://original.img.cheerfun.dev/img-original/img/'+url # 真实的原图地址，抓包获得，无法直接访问
        try:
            name = name.replace('\\','_') # 防止创建文件时因名字问题失败
            name = name.replace('?','过滤')
        except:
            name = name
        response = requests.get(url,headers=user)#模拟访问
        if response.status_code == 200: # 200即为成功
            if not os.path.exists('pixivimg'+ '/' +file+ '/' +name+'.jpg'): # 判断该图片是否存在，如果不存在
                print('正在下载图片：'+name)
                with open('pixivimg'+ '/' +file+ '/' +name+'.jpg', 'wb') as f: # 保存图片
                    f.write(response.content) 
            else:
                print(name+'.jpg已存在，跳过。')
        else:
            print('错误代码'+response.status_code+'下载图片'+name+'失败！')

for page in [x for x in range(1,num)]: # 生成数字列表，便于循环爬取
    threading.Thread(target=get_artist, args=(page,)).start() # 启动多线程
