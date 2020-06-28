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
            tf = str(tf)
            yield w, title + '  ' + tf
    def reducer(self, w, value):
        temp = '\t'.join(value)
        val = temp.split('\t')
        ls = []
        c = 0
        total_title = 196
        for m in val:
            c = c + 1
        for ele in val:
            temp2 = ele.split(' ')
            tf_idf = eval(temp2[-1]) * math.log(total_title * 1.0 / c + 1)
            ls.append([temp2[:-2], tf_idf])
        yield w, ls
if __name__=='__main__':
    MRFILE_TYPE_Counter.run()


