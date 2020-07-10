# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 14:22:03 2020

@author: Zeaf
"""

import requests  # 导入requests库
import re  # 导入正则表达式库
import os # 保存文件
from multiprocessing import Pool #导入pool库

os.system('title pixiv画师爬取@Zeaf')#设置窗口标题
if not os.path.exists('pixivimg'):  # 判断文件夹是否存在，如果不存在：
    os.mkdir('pixivimg')  # 创建一个文件夹
print('原网站：https://pixivic.com/')
print('因本人只看插画，所以为名字与插画对应，实际上获得的图片少于原页面上应有的图片。')

VNK = '7d3dc86d' # 默认的VNK
tag = input('请输入你想爬取的关键词,可加入热度（如女子5000users入り）：') # 获取关键词
pages = int(input('你想爬取的页数，每页大概30张图片:')) # 因为异步加载，所以实际上是多页
    
downloadpool=[]#创建空列表便于存储参数
for page in [x for x in range(1,pages+1)]:#遍历每一页
    user = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
    } # 这里的ua随便写写就好，无限制
    url='https://api.pixivic.com/illustrations?illustType=illust&searchType=original&maxSanityLevel=4&page='+str(page)+'&keyword='+tag+'&pageSize=30' # 异步加载接口，返回json数组
    response = requests.get(url,headers=user) # 模拟访问
    response.encoding = response.apparent_encoding # 防止乱码
    html = response.text  # 用文本显示访问网页得到的内容
    if len(re.findall('{"message":"搜索结果获取成功"(.*?)}',html)[0]):#判断该页是否存在数据，如果存在            
        urls = re.findall('"original":"https://i.pximg.net/img-original/img/(..../../../../../../[0-9]*?_p0.*?g)"', html)  # 用正则表达式获得本页各网址
        names = re.findall('"artistId":.*?,"title":"(.*?)","type"', html) # 获取图片名字
        ids = re.findall('"original":"https://i.pximg.net/img-original/img/..../../../../../../([0-9]*?)_p0.*?g"', html) # 获取图片id，为后面referer做准备
        if not os.path.exists('pixivimg'+'/'+tag):  # 判断文件夹是否存在，如果不存在：
            os.mkdir('pixivimg'+'/'+tag)  # 创建一个文件夹   
        for name,url,id in zip(names,urls,ids): # 按顺序遍历每一个画作名称、下载链接和id
            url = 'https://original.img.cheerfun.dev/img-original/img/'+url # 真实的原图地址，抓包获得，无法直接访问
            try:
                # 防止创建文件时因名字问题失败
                name = name.replace('\\','_') 
                name = name.replace('?','过滤')
            except:
                name = name
            downloadpool.append((name,id,url))
    else: # 不存在数据时的输出
        print('所选页数超出实际范围！')

def download(name_url_id): # 定义一个下载函数
    name=name_url_id[0] # 提取元组的信息
    id=name_url_id[1]
    url=name_url_id[2]
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
    response = requests.get(url,headers=user)#模拟访问
    if response.status_code == 200: # 200即为成功
        if not os.path.exists('pixivimg'+ '/' +tag+ '/' +name+'.jpg'): # 判断该图片是否存在，如果不存在
            print('正在下载图片：'+name)
            with open('pixivimg'+ '/' +tag+ '/' +name+'.jpg', 'wb') as f: # 保存图片
                f.write(response.content) 
        else:
            print(name+'.jpg已存在，跳过。')
    else:
        print('错误代码'+str(response.status_code)+'下载图片'+name+'失败！')

pool = Pool(processes=3) # 设置进程数
pool.map(download, downloadpool) # 运用map函数开启多进程
