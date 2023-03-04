import os
import pickle
import math
import nltk
from nltk.tokenize import word_tokenize
from nltk import ngrams

def compute_prob(tokens, unigram_dict, bigram_dict, V):
    """
    Calculates the probability based on test data from given model.
    Note that we will use Laplace smoothing
    Args -
        text: tokens of test data
        unigram_dict: dictionary of unigram model
        bigram_dict: dictionary of bigram model
        V: number of unique tokens in training data
    Returns -
        prob: probability of these words showing in this data
    """
    test_bigrams = list(ngrams(tokens, 2))
    prob = 1

    for i in test_bigrams:
        # b = number of appearances in training data
        b = bigram_dict[i] if i in bigram_dict else 0
        # u = unigram count of first word in bigram
        u = unigram_dict[i[0]] if i[0] in unigram_dict else 0
        prob = prob * ((b+1) / (u+V))
    return prob

if __name__ == '__main__':

    # 2a. Read in pickles
    english_unigram = pickle.load(open('eng_uni.p', 'rb'))
    english_bigram = pickle.load(open('eng_bi.p', 'rb'))
    french_unigram = pickle.load(open('fre_uni.p', 'rb'))
    french_bigram = pickle.load(open('fre_bi.p', 'rb'))
    italian_unigram = pickle.load(open('ita_uni.p', 'rb'))
    italian_bigram = pickle.load(open('ita_bi.p', 'rb'))

    # Read test file line by line
    with open(os.path.join(os.getcwd(), 'data\LangId.test'), 'r', encoding='utf-8') as f:
        text_in = f.read()
    text_in = text_in.splitlines()

    # Open file to record tests
    f = open('ModelOutputs.txt', 'a')

    # Calculate probabilities for each language on each line
    vocab_size = len(english_unigram) + len(french_unigram) + len(italian_unigram)
    probabilities = dict()
    ct = 1
    for i in text_in:
        tokens = word_tokenize(i)
        probabilities['English'] = compute_prob(tokens, english_unigram, english_bigram, vocab_size)
        probabilities['French'] = compute_prob(tokens, french_unigram, french_bigram, vocab_size)
        probabilities['Italian'] = compute_prob(tokens, italian_unigram, italian_bigram, vocab_size)

        # Find max probability and write that language to a file
        ordered_lang = sorted(probabilities.items(), reverse=True, key=lambda x:x[1])
        f.write(str(ct) + ' ' + ordered_lang[0][0]+'\n')
        ct += 1
    f.close()

    # Read output file with solution file and get accuracy
    with open(os.path.join(os.getcwd(), 'data\LangId.sol'), 'r', encoding='utf-8') as a:
        solutions = a.read()
    solutions = solutions.splitlines()

    with open(os.path.join(os.getcwd(), 'ModelOutputs.txt'), 'r', encoding='utf-8') as b:
        answer = b.read()
    answer = answer.splitlines()

    count = 0
    correct = 0
    for i in range(len(answer)):
        count += 1
        if solutions[i] == answer[i]:
            correct += 1
        else:
            print(answer[i].split()[0], '\n\tGuess:', answer[i].split()[1],
                  '\tActual:', solutions[i].split()[1])

    print('Accuracy:', correct/count * 100)

