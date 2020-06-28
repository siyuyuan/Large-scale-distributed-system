# -*- coding: utf-8 -*-
"""
Created on Sat May  9 19:51:08 2020

@author: yuansiyu
"""

from pyspark import SparkContext

def read_matrix(address):
    f = open(address, encoding='UTF-8')
    line = f.readline()
    A = []
    B = []
    while line:
        line_ = line.replace('\n','')
        line_ = line_.split(' ')
        if line_[0] == 'A':
            A.append((int(line_[1]), int(line_[2]), int(line_[3])))
        else:
            B.append((int(line_[1]), int(line_[2]), int(line_[3])))
        line = f.readline()
    f.close()
    return A, B

def write_matrix(r):
    f = open('result.txt', 'w', encoding='UTF-8')
    for ele in r:
        f.write('C' + ' ' + str(ele[0][0]) + ' ' + str(ele[0][1]) + ' ' + str(ele[1]) + '\n')
    f.close()

A,B = read_matrix('matrix.txt')

print('read successful')
sc = SparkContext("local")
A_matrix = sc.parallelize(A)
B_matrix = sc.parallelize(B)
temp_A = A_matrix.map(lambda x: (x[1],(x[0],x[2])))
temp_B = B_matrix.map(lambda x: (x[0],(x[1],x[2])))

#temp1:((A(j,(i,v)), B(j,(k,w)))) temp1[0] = A(j,(i,v)) temp1[0][0] = j temp1[0][1][0] = i
temp1= temp_A.cartesian(temp_B).filter(lambda x: x[0][0] == x[1][0])
temp2= temp1.map(lambda x: ((x[0][1][0],x[1][1][0]),x[0][1][1]*x[1][1][1]))
result = temp2.reduceByKey(lambda x, y: x + y)
result = result.sortByKey()

r = result.collect()

write_matrix(r)
show = result.take(4)
print(show)

