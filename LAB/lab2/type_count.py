from mrjob.job import MRJob
import os
class MRFILE_TYPE_Counter(MRJob):

    def mapper(self, key, line):
        temp = line.split('    ')
        F = temp[-1]
        f = os.path.splitext(F)
        filename,ty = f
        yield ty, 1

    def reducer(self, word, occurrences):
        yield word, sum(occurrences)
        
if __name__=='__main__':
    MRFILE_TYPE_Counter.run()
