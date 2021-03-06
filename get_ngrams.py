import sklearn
import os
from csv import reader
import pickle
from time import time
import matplotlib.pyplot as plt
import heapq # implementation of priority queue algorithm

#label: integer 1-9 inclusive
def loadLabels(path, label):
    # print os.getcwd()
    contents = reader(open(path, 'rb'))
    labels = [line for line in contents]
    labels = labels[1:]
    res =  [record[0] for record in labels if int(record[1]) == label]
    return res

# generate grams dictionary for each file
def grams_dict(f_name, N=4):
    path = r"train\%s.bytes" %f_name
    grams_list =[]
    for line in open(path, 'rb'):
        grams_list += line.rstrip().split(" ")[1:]
    tree = dict()
    for i in range(len(grams_list)-N+1):
        gram = ''.join(grams_list[i:i + N])
        if gram not in tree:
            tree[gram] = 1     # always 1 for a single file
    return tree

# merge all ngrams in one dictionary
def reduce_dict(f_labels):
    # merge all the labels(files) into one same dict
    res = dict()
    for ind ,label in enumerate(f_labels):
        if ind > 100:
            break
        tree = grams_dict(label)
        for k,v in tree.iteritems():
            if k in res:
                res[k] += v
            else:
                res[k] = v
        del tree
    return res

def hist(ratio_list):
    plt.hist(ratio_list)
    plt.xlabel("ratio")
    plt.xlabel("frequency")
    plt.title(r'histgram of add ratio')
    #plt.axis([0,1,0,1])
    plt.grid(True)

    plt.show()

def line(total_list):
    plt.plot(total_list)
    plt.xlabel("file number")
    plt.xlabel("total number of grams")
    plt.title(r'line of grams total number')
    # plt.axis([0,1,0,1])
    plt.grid(True)

    plt.show()

# get the top-k features of corresponding class, pickle down
def heap_top(dic, label, num = 100000):
    heap = [(0,'xxx')]*num
    root = heap[0]
    for ngram, count in dic.iteritems():
        if count > root[0]:
            # pop and return the smallest item from the heap,
            # and also push the new item. The heap size will not change.
            # This operation equals to heappop()+ heappush() conbination,
            # but more efficient.
            root = heapq.heapreplace(heap, (count, ngram))

    cur = r'C:\Users\admin\PycharmProjects\MalwareDetection'
    os.chdir(cur)
    pickle.dump(heap, open(r'grams\ngram_%d_top%d'%(label,num),'wb'))


if __name__ =='__main__':
    for i in range(1,10):
        dir = r"C:\MalwareData"
        os.chdir(dir)
        labels = loadLabels('trainLabels.csv',i)
        heap_top(reduce_dict(labels),i)



