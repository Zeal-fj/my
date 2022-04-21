# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 12:04:03 2022

@author: Zeaf
"""

import re#导入正则匹配库

def zeaf(books,books_foreign,journals,journals_foreign,dissertations,others,literature):#定义一个整理单条文献的函数
    if len(re.findall('\.',literature))==0:
        literature=literature+'.'
    if len(re.findall('\[\d*?\]',literature))!=0:
        literature=literature.replace(re.findall('\[\d*?\]',literature)[0],'')#去除前缀
    if len(re.findall('【\d*?】',literature))!=0:
        literature=literature.replace(re.findall('【\d*?】',literature)[0],'')#去除前缀
    if len(re.findall('[M]',literature))!=0:#书籍归类
        if len(re.findall('\d.*?:\d',literature))!=0:#英文冒号后去除
            literature=literature.replace(re.findall(':\d.*',literature)[0],'.')
        elif len(re.findall('\d.*?：\d',literature))!=0:#中文冒号后去除
            literature=literature.replace(re.findall('：\d.*',literature)[0],'.')
        if len(re.findall('[A-Za-z][A-Za-z]',literature))!=0:#英文文献分类
            books_foreign.append(literature)
        else:
            books.append(literature)
    elif len(re.findall('[J]',literature))!=0:#期刊归类
        if len(re.findall('[A-Za-z][A-Za-z]',literature))!=0:#英文文献分类
            journals_foreign.append(literature)
        else:
            journals.append(literature)
    elif len(re.findall('[D]',literature))!=0:#论文归类
        dissertations.append(literature)
    else:#其他归类
        others.append(literature)

def date_sorted(literatures):#定义一个日期排序的函数
    newliteratures={}
    datedict={}
    datelist=[]
    sortedliteratures=[]
    for literature in literatures:
        date=re.findall('\d\d\d\d',literature)[0]
        datelist.append(date)
        datedict[literature]=date#创建以文献为key的字典(日期不唯一)
    sorted_datelist=sorted(datelist,reverse=True)#降序排序
    for sorted_date in sorted_datelist:
        lis=[key for key,value in datedict.items() if value==sorted_date]#通过值查找键
        for li in lis:            
            newliteratures[li]=sorted_date#建立排序好的键值对
    for key in newliteratures.keys():
        sortedliteratures.append(key)#遍历键
    return sortedliteratures#返回排序好的键

                       
with open('test.txt', 'r', encoding='utf8') as f1, open('全部文献.txt', 'w') as f2:
    literatures=f1.readlines()#逐行读取生成列表
    literatures=list(set(literatures))#去重
    books=[]
    books_foreign=[]
    journals=[]
    journals_foreign=[]
    dissertations=[]
    others=[]
    for literature in literatures:#读取每行数据
        literature = literature.strip()#去除空格
        if len(re.findall(';',literature))!=0:#当文献出现英文分号时
            literature = literature.split(';')
            literature[-1]=literature[-1][:-1]#去除最后一个文献的句号以统一格式
            for x in literature:
                x=x+'.'#加上句号
                x=x.strip()#去除空格
                zeaf(books,books_foreign,journals,journals_foreign,dissertations,others,x)
        elif len(re.findall('；',literature))!=0:#当文献出现中文分号时
            literature = literature.split('；')
            literature[-1]=literature[-1][:-1]#去除最后一个文献的句号以统一格式
            for x in literature:
                x=x+'.'#加上句号
                x=x.strip()#去除空格
                zeaf(books,books_foreign,journals,journals_foreign,dissertations,others,x)  
        else:            
            zeaf(books,books_foreign,journals,journals_foreign,dissertations,others,literature)
    #图书再处理
    books=list(set(books))#再次去重
    if len(books)!=0:
        books=date_sorted(books)
    #外文图书再处理
    books_foreign=list(set(books_foreign))#再次去重
    if len(books_foreign)!=0:
         books_foreign=date_sorted(books_foreign)
    #期刊再处理
    journals=list(set(journals))#再次去重
    if len(journals)!=0:
         journals=date_sorted(journals)
    #外文期刊再处理
    journals_foreign=list(set(journals_foreign))#再次去重
    if len(journals_foreign)!=0:
         journals_foreign=date_sorted(journals_foreign)
    #论文再处理
    dissertations=list(set(dissertations))#再次去重
    if len(dissertations)!=0:
         dissertations=date_sorted(dissertations)
    #其他再处理
    others=list(set(others))#再次去重
    if len(others)!=0:
         others=date_sorted(others)
    
    literatures=books+books_foreign+journals+journals_foreign+dissertations+others#合并整理好的列表
    i=1
    for literature in literatures:
        f2.write('['+str(i)+'] '+literature+'\n')#写入编号
        i+=1     














           
