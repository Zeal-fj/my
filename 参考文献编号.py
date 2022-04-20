# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 16:40:01 2022

@author: Zeaf
"""
import re
with open('test.txt', 'r', encoding='utf8') as f1, open('全部文献.txt', 'w') as f2:
    literatures=f1.readlines()#逐行读取生成列表
    literatures=list(set(literatures))#去重
    books=[]
    journals=[]
    dissertations=[]
    others=[]
    for literature in literatures:#读取每行数据
        literature = literature.strip()#去除空格
        if len(re.findall(';',literature))!=0:#当文献出现分号时
            literature = literature.split(';')
            for x in literature:
                if len(re.findall('\.',x))==0:
                    x=x+'.'
                if len(re.findall('\[\d*?\]',x))!=0:
                    x=x.replace(re.findall('\[\d*?\]',x)[0],'')#去除前缀
                if len(re.findall('【\d*?】',x))!=0:
                    x=x.replace(re.findall('【\d*?】',x)[0],'')#去除前缀
                if len(re.findall('[M]',x))!=0:#书籍归类
                    if len(re.findall('\d.*?:\d',x))!=0:
                        x=x.replace(re.findall(':\d.*',x)[0],'.')
                    books.append(x)
                elif len(re.findall('[J]',x))!=0:#期刊归类
                    journals.append(x)
                elif len(re.findall('[D]',x))!=0:#论文归类
                    dissertations.append(x)
                else:#其他归类
                    others.append(x)     
        else:            
            if len(re.findall('\[\d*?\]',literature))!=0:
                literature=literature.replace(re.findall('\[\d*?\]',literature)[0],'')#去除前缀
            if len(re.findall('【\d*?】',literature))!=0:
                literature=literature.replace(re.findall('【\d*?】',literature)[0],'')#去除前缀
            if len(re.findall('[M]',literature))!=0:#书籍归类
                if len(re.findall('\d.*?:\d',literature))!=0:
                    literature=literature.replace(re.findall(':\d.*',literature)[0],'.')
                books.append(literature)
            elif len(re.findall('[J]',literature))!=0:#期刊归类
                journals.append(literature)
            elif len(re.findall('[D]',literature))!=0:#论文归类
                dissertations.append(literature)
            else:#其他归类
                others.append(literature)
    i=1
    books=list(set(books))#再次去重
    journals=list(set(journals))#再次去重
    dissertations=list(set(dissertations))#再次去重
    others=list(set(others))#再次去重
    literatures=books+journals+dissertations+others#合并整理好的列表
    for literature in literatures:
        f2.write('['+str(i)+'] '+literature+'\n')#写入编号
        i+=1                


    
        
