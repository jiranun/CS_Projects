__author__ = 'Jiranun.J'

import text_sum as ts
from sklearn.cross_validation import KFold
import numpy as np
import matplotlib.pyplot as plt
import os

def compare_summaries(predict, actual):
    predict = set(predict)
    actual = set(actual)
    if len(predict.union(actual)) == 0:
        return 0.

    return len(predict.intersection(actual))*1./len(predict.union(actual))


data_a, data_s = ts.get_all_labeled_data()
kf = KFold(ts.number_of_files, n_folds=5)
fold_number = 0
params = [(i,1.-i,j) for i in np.linspace(0,1,21) for j in np.linspace(0,1,11)]
acc_plot = []


for param in params:
    loc_ratio = param[0]
    int_ratio = param[1]
    sigma = param[2]
    total_acc = 0
    for train_index, test_index in kf:

        train_a = [data_a[i] for i in train_index]
        train_s = [data_s[i] for i in train_index]
        test_a = [data_a[i] for i in test_index]
        test_s = [data_s[i] for i in test_index]

        # density, loc_ratio, int_ratio = ts.train_data(train_a, train_s, init_loc_ratio, init_int_ratio)
        density = ts.get_density(train_a,train_s, sigma)
        n_test_cases = len(test_a)
        accuracy = 0.

        for i in range(n_test_cases):
            actual_summary = ts.content_to_sentences(test_s[i])
            total_score = ts.get_total_score(test_a[i], density, loc_ratio, int_ratio)
            predict_summary = ts.get_top_sents(test_a[i], total_score, len(actual_summary))
            accuracy += compare_summaries(predict_summary, actual_summary)

        accuracy /= n_test_cases
        total_acc += accuracy
        print 'Fold :', str(fold_number+1), ', accuracy =',accuracy
        # print
        fold_number = (fold_number+1) % 5
    total_acc /= 5.
    print 'param = ',param,', total_acc = ',total_acc
    print
    acc_plot.append(total_acc)


x = np.linspace(0,len(acc_plot), len(acc_plot))
max_ind = np.argmax(acc_plot)
print '== Params with max accuracy =='
print 'loc_ratio =',params[max_ind][0]
print 'int_ratio =',params[max_ind][1]
print 'sigma =', params[max_ind][2]
print
print 'Max accuracy = ', acc_plot[max_ind]
print

density = ts.get_density(data_a, data_s, params[max_ind][2])
xs = np.linspace(0,1,1000)
ys = density(xs)
norm_ratio = 1./max(ys)
plt.plot(xs, ys)
plt.ylabel('count')
plt.xlabel('summary sentence location')
plt.savefig('location_density.png')

print 'location_density.png has been generated at' ,os.getcwd()

plt.clf()
plt.plot(x, acc_plot)
plt.ylabel('Accuracy')
plt.xlabel('location and intersection ratio')
plt.savefig('BestParameters.png')
plt.show()

print 'BestParameters.png has been generated at' ,os.getcwd()
