'''
from mrjob.job import MRJob
import os
class MRFILE_TYPE_Counter(MRJob):

    def mapper(self, key, line):
        temp = line.split()
        file = temp[-1]
        f = os.path.splitext(file)
        filename,ty = f
        yield ty, 1

    def reducer(self, word, occurrences):
        yield word, sum(occurrences)
        
if __name__=='__main__':
    MRFILE_TYPE_Counter.run()
'''
'''
from mrjob.job import MRJob
from mrjob.step import MRStep
import heapq
import os
class MRFILE_SIZE_Counter(MRJob):

    def mapper(self, key, line):
        temp = line.split()
        Size = temp[2]
        if len(line) == 4:
            F = temp[-1]
        else:
            F = temp[-2]+' '+temp[-1]
        yield (int(Size.replace(',','')),F),1

    def reducer_1(self, key, value):
        yield None, key

    def reducer_2(self, _, value):
        for s, f in heapq.nlargest(85, value):
            yield s,f
    def steps(self):
        return[MRStep(mapper = self.mapper,reducer = self.reducer_1),MRStep(reducer = self.reducer_2)]
        
if __name__=='__main__':
    MRFILE_SIZE_Counter.run()

'''


temp1 = []

address2 = "D:\output2.txt"
with open(address2, 'r') as f1:
    for line in f1:
        line = line.strip('\n') 
        temp1.append(line)

ls0 = []
for ele in temp1:
    a = ele.split('\t')
    a[1] = a[1].encode('utf-8').decode('unicode_escape')
    ls0.append(a)

f = open("D:/output2_rewrite.txt", "w")
for element in ls0:
    f.write(str(element[0])+'\t'+element[1]+'\n')
f.close()        
