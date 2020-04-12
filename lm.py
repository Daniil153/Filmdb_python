import numpy as np
from collections import Counter
from scipy.sparse import csr_matrix

NGRAM = 2

def normalize(x):
    return x / x.sum(axis=-1)


def train(token_list, word_to_id, id_to_word):
    """
    Trains n-gram language model on the given train set represented as a list of token ids.
    :param token_list: a list of token ids
    :return: learnt parameters, or any object you like (it will be passed to the next_proba_gen function)
    """

    ############################# REPLACE THIS WITH YOUR CODE #############################
    l = len(token_list)
    counters = [Counter(tuple(token_list[i:i+ng]) for i in range(l-ng) ) for ng in range(1,NGRAM+1)]
    vocab_size = len(word_to_id)
    return vocab_size, counters
    ############################# REPLACE THIS WITH YOUR CODE #############################


def next_proba_gen(token_gen, params, hidden_state=None):
    """
    For each input token estimate next token probability distribution.
    :param token_gen: generator returning sequence of arrays of token ids (each array has batch_size independent ids);
     i-th element of next array is next token for i-th element of previous array
    :param params: parameters received from train function
    :param hidden_state: the initial state for next token that may be required 
     for sampling from the language model
    :param hidden_state: use this as the initial state for your language model(if it is not None).
     That may be required for sampling from the language model.

    :return: probs: for each array from token_gen should yield vector of shape (batch_size, vocab_size)
     representing predicted probabilities of each token in vocabulary to be next token.
     hidden_state: return the hidden state at each time step of your language model. 
     For sampling from language model it will be used as the initial state for the following tokens.
    """

    ############################# REPLACE THIS WITH YOUR CODE #############################

    # This is interpolation between Unigram and Bigram language models
    vocab_size, counters = params
    lambda1, lambda2 = 0.2, 0.8
    unigram_probs = normalize(np.array([counters[0][(i,)] for i in range(vocab_size)]))
    bigrams = list(counters[1].keys())
    ii, jj = zip(*bigrams)
    ii, jj = list(ii), list(jj)
    data = [counters[1][p] for p in bigrams]
    m = csr_matrix((data, (ii, jj)), shape=(vocab_size, vocab_size))
    m /= m.sum(axis=1).reshape(vocab_size, 1)
    # print(m.sum(axis=1))

    for token_arr in token_gen:
        probs = np.vstack([unigram_probs * lambda1 + np.asarray(m[token, :]).reshape(-1) * lambda2 for token in token_arr])
        assert (np.abs(np.sum(probs, axis=-1)-1) < 1e-5).all()
        assert probs.shape[1]==vocab_size
        yield probs, hidden_state

    ############################# REPLACE THIS WITH YOUR CODE #############################
