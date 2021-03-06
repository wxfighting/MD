from csv import DictReader
from datetime import datetime
import pickle
import heapq
import sys

# load data
def load_label(path, label):
    result = []
    for row in DictReader(open(path)):
        if int(row['Class']) == label:
            result.append((row['Id']))
    return result


# generate grams dictionary for one file
def grams_dict(f_name, N=4):
    path = "train/%s.bytes"%f_name
    one_list = []
    with open(path, 'rb') as f:
        for line in f:
            one_list += line.rstrip().split(" ")[1:]
    grams_string = [''.join(one_list[i:i+N]) for i in xrange(len(one_list)-N+1)]
    tree = dict()
    for gram in grams_string:
        if gram not in tree:
            tree[gram] = 1
    return tree


# add up ngram dictionaries
def reduce_dict(f_labels):
    result = dict()
    for f_name in f_labels:
        d = grams_dict(f_name)
        for k,v in d.iteritems():
            if k in result:
                result[k] += v
            else:
                result[k] = v
        del d
    #print "this class has %i keys"%len(result)
    #pickle.dump(result, open('gram/ngram_%i'%label,'wb'))
    return result

# heap to get the top 100,000 features.
def Heap_top(dictionary, label, num = 100000):
    heap = [(0,'tmp')]* num # initialize the heap
    root = heap[0]
    for ngram,count in dictionary.iteritems():
            if count > root[0]:
                root = heapq.heapreplace(heap, (count, ngram))
    pickle.dump(heap, open('gram/ngram_%i_top%i'%(label,num),'wb'))




if __name__ == '__main__':
    start = datetime.now()
    #for label in range(1,10): # take too much memory
    label = int(sys.argv[1])
    print "Gathering 4 grams, Class %i out of 9..."%label
    f_labels = load_label('trainLabels.csv', label)
    Heap_top(reduce_dict(f_labels),label)
    #print datetime.now() - start