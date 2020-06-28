# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 21:07:31 2020

@author: yuansiyu
"""

temp1 = []

address2 = "D:\output.txt"
with open(address2, 'r') as f1:
    for line in f1:
        line = line.strip('\n') 
        temp1.append(line)


ls0 = []
for ele in temp1:
    a = ele.split('\t')
    a[0] = a[0].encode('utf-8').decode('unicode_escape')
    a[1] = eval(a[1])
    ls0.append(a)

f = open("D:/output_rewrite.txt", "w", encoding = 'utf-8')
for element in ls0:
    f.write(str(element[0])+'\t'+str(element[1])+'\n')
f.close()
