# coding:utf-8
import numpy as np
import pandas as pd


def PageRank(M, alpha, root):
    """
    Personal Rank in matrix formation
    :param M: transfer probability matrix
    :param index2node: index2node dictionary
    :param node2index: node2index dictionary
    :return:type of list of tuple, ex.
    [(node1, prob1),(node2, prob2),...]
    """
    a=pd.DataFrame(M).index.values.tolist()
    b=np.arange(len(a))

    node2index=dict(zip(a,b))
    index2node=dict(zip(b,a))

    result = []
    n = len(M)
    v = np.zeros(n)
    v[node2index[root]] = 1
    while np.sum(abs(v - (alpha*np.matmul(M,v) + (1-alpha)*v))) > 0.0001:
        v = alpha * np.matmul(M, v) + (1-alpha)*v
    for ind, prob in enumerate(v):
        result.append((index2node[ind], prob))
    result = sorted(result, key=lambda x:x[1], reverse=True)[:num_candidates]
    return result
