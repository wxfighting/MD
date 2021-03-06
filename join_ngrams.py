import sklearn
import os
from csv import reader
import pickle
from time import time
import matplotlib.pyplot as plt
import heapq # implementation of priority queue algorithm
import math
import glob


def join_ngrams(num=100000):
    dict_all = {}
    # iterate on each class
    for c in range(1,10):
        dic = pickle.load('grams/gram_%d_top%d' %(c, num))
        for count , gram in dic.iteritems():
            if gram not in dict_all:
                dict_all[gram] = [0]*9  # for every ngram, create a list for all class
            dict_all[gram][c-1] = count
    return dict_all

# p: number of positive examples
# n: number of negtive examples
def entropy(p, n):
    p_ratio = float(p)/(p+n)
    n_ratio = float(n)/(p+n)
    return - p_ratio* math.log(p_ratio) - n_ratio * math.log(n_ratio)


# cal the info gain after split the dataset by feature
# (p, n): the positive and negtive examples in the set before spliting
# (p1, n1): the positive and negtive examples in the subset with the feature
# (p0, n0): the positive and negtive examples in the subset without the feature
# the more info gain one feature corresponds, the more discriminative the feature is.
def info_gain(p,n, p1,n1, p0, n0):
    p_ratio = float(p1+n1)/(p+n)
    n_ratio = float(p0+n0)/(p+n)
    return entropy(p,n)- p_ratio* entropy(p1, n1) - n_ratio* entropy(p0, n0)

# get the number of positive and negtive examples for a class label: 1-9
def pn_instances(path, label):
    p = 0
    n = 0
    contents = reader(open(path, 'rb'))
    labels = [line for line in contents]
    labels = labels[1:]
    for record in labels:
        if int(record[1]) == label:
            p += 1
        else:
            n += 1
    return p, n


# select the discriminative features for each class
def heap_gain(p, n, class_label, dict_all, num_features=750, gain_min = -100000):
    heap = [(gain_min, 'xxx')] * num_features # select num_features features for each class based on the info gain
    root = heap[0] # get the min of the heap
    for gram, count_list in dict_all:
        p1 = dict_all[gram][class_label-1]
        n1 = sum(dict_all[gram]) - p1

        p0 = p - p1
        n0 = n - n1
        if p1*p0*n1*n0 != 0:
            gain = info_gain(p,n,p1,n1,p0,n0)
            if gain > root[0]:
                root = heapq.heapreplace(heap, (gain, gram))

    # return the list of discriminative grams
    return [ele[1] for ele in heap]

def gen_binary_feature_data(features_all, train=True, N = 4):
    dir = r"C:\MalwareData"
    os.chdir(dir)
    if train == True:
        path = "train"
    else:
        path = "test"
    sample_files = glob.glob(path+r'\*.bytes')
    features = []
    for sample in sample_files:
        grams_list = []
        with open(sample, 'rb') as input:
            for line in input:
                grams_list += line.rstrip().split(" ")[1:]
        grams_string = set([''.join(grams_list[i:i+N]) for i in range(len(grams_list)-N)])

        binary_feature = []
        for feature in features_all:
            if feature in grams_string:
                binary_feature.append(1)
            else:
                binary_feature.append(0)
        del grams_string
        features.append(binary_feature)

    return features


if __name__ == "__main__":
    dict_all = join_ngrams()
    features_all = []
    for c in range(1,10):
        dir = r"C:\MalwareData"
        os.chdir(dir)
        p, n = pn_instances('trainLabels.csv', c)
        features_all += heap_gain(p, n, c, dict_all)
    train_data = gen_binary_feature_data(features_all,train=True)
    test_data = gen_binary_feature_data(features_all,train=False)
