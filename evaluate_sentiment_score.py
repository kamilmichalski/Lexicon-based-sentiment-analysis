from get_data import get_data
import numpy as np
from myclasses import plutchik
import sys


def wrapper(func):
    def modify_scores_according_to_index(document):
        max_sentence_len_dict = get_sentence_len_dict(document)
        for tok in document.tokens:
            tok.sentiment_score = np.multiply(tok.sentiment_score,
                                              (tok.index / max_sentence_len_dict[tok.sentence_index]))
        return func(document)
    return modify_scores_according_to_index


@wrapper
def evaluate_sentiment_score_add(document):
    for token in document.tokens:
        document.sentiment_score = np.add(document.sentiment_score, token.sentiment_score)

    return [round(score/len(document.tokens)) for score in document.sentiment_score]


def get_sentence_len_dict(document):
    sentence_len = dict()
    for tok in document.tokens:
        if sentence_len.get(tok.sentence_index) is not None:
            sentence_len[tok.sentence_index] += 1
        else:
            sentence_len[tok.sentence_index] = 1
    return sentence_len


def norm(vector):
    old_min, old_max = -1, 1
    new_min, new_max = -5, 5
    old_range = (old_max - old_min)
    new_range = (new_max - new_min)
    magnitude = np.linalg.norm(vector)
    for i in range(len(vector)):
        vector[i] = round(((((vector[i]/magnitude) - old_min) * new_range) / old_range) + new_min)

    return vector


if __name__ == '__main__':
    documents = sys.argv[1:]
    for document in documents:
        doc, text_body = (get_data(document))
        score = evaluate_sentiment_score_add(doc)
        score_filename = open('result_{0}.txt'.
                              format(str(document)), 'w')
        score_filename.write('''Score for document {0} is {1} in accordance with following pattern: {2}
\nText body: {3}'''
                             .format(str(document), str(norm(score)), plutchik, text_body))
