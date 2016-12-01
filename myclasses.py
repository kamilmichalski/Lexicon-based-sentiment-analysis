
# -*- coding: utf-8 -*-
import numpy as np

plutchik = [u'xw-rad', u'xw-ufn', u'xw-ocz', u'xw-smu',
            u'xw-zlo', u'xw-str', u'xw-odr', u'xw-zas']


class Document:
    def __init__(self):
        self.tokens = []
        self.sentiment_score = np.zeros(8)

    def add_token(self, token):
        self.tokens.append(token)


class Token:
    def __init__(self, index, sentence_index):
        self.sentiment_score = np.zeros(8)
        self.index = index
        self.sentence_index = sentence_index


# class Sentence:
#     def __init__(self):
#         self.sentiment_score = np.zeros(8)
#         self.tokens = []
#
#     def add_token(self, token):
#         self.tokens.append(token)
#
#     def __len__(self):
#         return len(self.tokens)
#
#     def __repr__(self):
#         sent = []
#         for i in xrange(len(self.tokens)-1):
#             if self.tokens[i+1].ctag == 'interp':
#                 sent.append(self.tokens[i].orth)
#             else:
#                 sent.append(self.tokens[i].orth + ' ')
#         sent.append(self.tokens[-1].orth)
#         return ''.join(sent).encode('utf-8')
