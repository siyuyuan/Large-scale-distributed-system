# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 16:03:26 2020

@author: yuansiyu
"""
'''
from mrjob.job import MRJob
from mrjob.step import MRStep
import math
import os
from collections import Counter
class MRFILE_TYPE_Counter(MRJob):

    def mapper(self, key, line):
        temp = line.split('\t')
        title  = temp[0]
        text = temp[1]
        words = text.split(' ')
        count= Counter(words)
        for w in count:
            tf = count[w] * 1.0/ len(words)
            yield w, (title, tf)

    def reducer_1(self, w, key):
        ls = []
        total_title = 196
        total_show = len(key)
        for title, tf in key:
            tf_idf = tf * math.log(total_title * 1.0 / total_show + 1)
            ls.append((title, tf_idf))
        yield w, ls
        
if __name__=='__main__':
    MRFILE_TYPE_Counter.run()
    
'''


import jieba

def write_file(r):
    f = open("D:/MRresults.txt", "w", encoding = 'utf-8')
    
    for key in r.keys():
        f.write(key + '\t' + r[key])
        f.write('\n')
    f.close()
    
if __name__ == '__main__':
    r = {}
    file = open('E:/学习资料/大三下/大规模分布式系统/作业/lab3/news_tensite_xml.smarty.txt', 'r', encoding='utf-8')
    ls = []
    for line in file.readlines():
        ls.append(line)
    
    
    l = len(ls)
    for i in range(l):
        if "contenttitle" in ls[i]:
            title = ls[i].replace('<contenttitle>','')
            title = title.replace('</contenttitle>\n','')
            text = ls[i+1].replace('<content>','')
            text = text.replace('</content>\n','')
            text = jieba.cut(text,cut_all=False)
            r[title] = ' '.join(text) 
    
    write_file(r)