# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 18:16:04 2020

@author: yuansiyu
"""

def sort_result(result):
    dic1 = {}
    for r in result:
        dic1[r[0][0]] = r[1]
    dic2 = sorted(dic1.items(), key=lambda x:x[1], reverse=True)
    
    print("查询结果为：\n")
    for r in dic2:
        print("网页名字：{}, 相关度：{}".format(r[0], str(r[1])))
        
if __name__ == '__main__':
    temp1 = []
    
    address2 = "D:/output_rewrite.txt"
    with open(address2, 'r', encoding = 'utf-8') as f1:
        for line in f1:
            line = line.strip('\n') 
            temp1.append(line)
    
    dic = {}
    for ele in temp1:
        a = ele.split('\t')
        a[0] = eval(a[0])
        a[1] = eval(a[1])
        dic[a[0]] = a[1]
    
    
    print("请输入你想查询的关键词" + '\n')
    key_word = input()
    if key_word not in dic.keys():
        print("无相关页面显示，试试其他的关键词吧！")
    else:
        result = dic[key_word]
        sort_result(result)
    