from mrjob.job import MRJob
from mrjob.step import MRStep
import heapq
import os
class MRFILE_SIZE_Counter(MRJob):

    def mapper(self, key, line):
        temp = line.split()
        Size = temp[2]
        if ',' in temp[-2]:
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
        return[MRStep(mapper = self.mapper,reducer = self.reducer_1),
               MRStep(reducer = self.reducer_2)]
        
if __name__=='__main__':
    MRFILE_SIZE_Counter.run()
