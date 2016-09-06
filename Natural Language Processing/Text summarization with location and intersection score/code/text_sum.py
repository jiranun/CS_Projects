__author__ = 'Jiranun.J, Sihan Zhao'

import os
import re

from scipy.stats import gaussian_kde
import numpy as np
import matplotlib.pyplot as plt

xs = np.linspace(0,1.,2000)
number_of_files = 100

def strip_spaces(sent):
    sent = sent.lstrip()
    sent = sent.rstrip()
    return sent


def content_to_sentences(content):
    content = content.rstrip('\n')
    content = content.replace('\n','')
    content = content.replace('"','')
    content = content.replace("?", ".")
    content = content.replace("!", ".")
    sentences = content.split(".")
    sentences = [strip_spaces(re.sub('\W+', ' ', s)) for s in sentences]
    sentences = [s for s in sentences if s != '']
    return sentences


def get_all_labeled_data():
    global number_of_files
    article_path = '../data/articles/'
    summary_path = '../data/summary/'
    articles = []
    summaries = []

    for i in range(number_of_files):
        article_filename = article_path+str(i+1)+'.txt'
        summary_filename = summary_path+str(i+1)+'.txt'

        if not os.path.isfile(article_filename) or not os.path.isfile(summary_filename):
            continue

        a_file = open(article_filename)
        s_file = open(summary_filename)

        articles.append(a_file.read())
        summaries.append(s_file.read())

        a_file.close()
        s_file.close()

    number_of_files = len(articles)
    return articles, summaries


def get_summary_positions(article, summary):
    a_sents = content_to_sentences(article)
    s_sents = content_to_sentences(summary)
    positions = []
    for sent in s_sents:
        if sent not in a_sents:
            continue
        indx = a_sents.index(sent)
        positions.append(1.*indx/(len(a_sents)-1.))
    return positions


def get_density(data_a, data_s, sigma):
    num_data = len(data_a)
    positions = []

    for i in range(num_data):
        article = data_a[i]
        summary = data_s[i]
        positions.extend(get_summary_positions(article, summary))

    density = gaussian_kde(positions)
    density.covariance_factor = lambda : sigma
    density._compute_covariance()
    return density


def get_location_score(sentences, density):
    num_sent = len(sentences)
    ys = density(xs)
    norm_ratio = 1./max(ys)
    loc_scores = []

    for i in range(num_sent):
        norm_location = float(i)/float(num_sent-1)
        score = density(norm_location)[0]
        score = score*norm_ratio
        loc_scores.append(score)

    return loc_scores


def sentences_intersection(sent1, sent2):
    s1 = set(sent1.split(" "))
    s2 = set(sent2.split(" "))

    if float(len(s1.union(s2))) == 0.:
        return 0

    return float(len(s1.intersection(s2))) / float(len(s1.union(s2)))


def get_intersection_score(sentences):
    num_sent = len(sentences)
    scores = []

    for i in range(num_sent):
        s = 0
        for j in range(num_sent):
            s += sentences_intersection(sentences[i], sentences[j])
        scores.append(s)

    # normalize
    scores = [s/sum(scores) for s in scores]
    return scores


def ratio_fit(location_scores, intersection_scores, num_sents_a, num_sents_s, location_ratio, intersection_ratio):
    all_top_locations = []

    curr = 0

    for i in range(len(num_sents_a)):
        num_sent = int(num_sents_a[i])
        location_score = [location_scores[j] for j in range(curr, curr+num_sent)]
        intersection_score = [intersection_scores[j] for j in range(curr, curr+num_sent)]
        total_score = [location_score[j]*location_ratio+intersection_score[j]*intersection_ratio for j in range(num_sent)]
        top = sorted(range(len(total_score)), key=lambda sen: float(total_score[sen]), reverse=True)[:int(num_sents_s[i])]
        top_pos = [t/float(num_sent-1) for t in top]
        all_top_locations.extend(top_pos)
        curr += num_sent

    return all_top_locations


# def train_data(articles, summaries, init_loc_ratio = .7, init_int_ratio = .3):
#     density = get_density(articles, summaries, .05)
#
#     location_scores = []
#     intersection_scores = []
#     summaries_pos = []
#     num_sents_a = []
#     num_sents_s = []
#
#     for i in range(len(articles)):
#         article = articles[i]
#         a_sentences = content_to_sentences(article)
#         num_sents_a.append(len(a_sentences))
#
#         summary = summaries[i]
#         s_sentences = content_to_sentences(summary)
#         num_sents_s.append(len(s_sentences))
#
#         location_scores.extend(get_location_score(a_sentences, density))
#         intersection_scores.extend(get_intersection_score(a_sentences))
#         summaries_pos.extend(get_summary_positions(article, summary))
#
#
#     model = Model(ratio_fit, independent_vars = ['location_scores','intersection_scores', 'num_sents_a', 'num_sents_s'])
#     result = model.fit(summaries_pos, location_scores = location_scores,
#                        intersection_scores = intersection_scores,
#                        num_sents_a = num_sents_a,
#                        num_sents_s = num_sents_s,
#                        location_ratio = init_loc_ratio,
#                        intersection_ratio = init_int_ratio,
#                        verbose = False)
#     # print result.values
#     # print summaries_pos
#     # print ratio_fit(location_scores = location_scores,
#     #                    intersection_scores = intersection_scores,
#     #                    num_sents_a = num_sents_a,
#     #                    num_sents_s = num_sents_s,**result.values
#     #                 )
#     res = result.values
#
#     return density, res['location_ratio'], res['intersection_ratio']


def get_total_score(article, density, loc_ratio, int_ratio):
    sents = content_to_sentences(article)
    location_score = get_location_score(sents, density)
    intersection_score = get_intersection_score(sents)
    total_score = [location_score[i]*loc_ratio + intersection_score[i]*int_ratio for i in range(len(sents))]
    return total_score


def get_top_sents(article, total_score, n):
    sents = content_to_sentences(article)
    top_indx = sorted(range(len(total_score)), key=lambda sen: float(total_score[sen]), reverse=True)[:n]
    return [sents[i] for i in top_indx]

if __name__ == "__main__":
    data_a, data_s = get_all_labeled_data()

    article = data_a[0] # add input here
    number_of_sum_sentence = 5

    input_filename = 'input.txt'

    if not os.path.isfile(input_filename):
        print 'Error : cannot find input.txt'
    else:
        a_file = open(input_filename)
        article = a_file.read()
        a_file.close()

        # these params produced highest accuracy in evaluation.py
        loc_ratio = 0.1
        int_ratio = 0.9
        sigma = 0.1

        density = get_density(data_a, data_s, sigma)
        total_scores = get_total_score(article, density, loc_ratio, int_ratio)
        summary = get_top_sents(article, total_scores, number_of_sum_sentence)


        print number_of_sum_sentence, 'summary sentences :'
        for sent in summary:
            print sent
