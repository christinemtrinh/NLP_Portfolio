import sys
import os
import nltk
from nltk.tokenize import word_tokenize
import pickle
def preprocess_file(filepath):
    """
    Reads the file into a (very large) string variable then creates dictionaries
    for probabilities of appearance in the given text.
    Args -
        filepath: str that specifies location of data file
    Returns -
        unigram_dict: dictionary with frequency of unigrams
        bigram_dict: dictionary with frequency of bigrams
    """

    # 1b. Read in text and remove newlines
    with open(os.path.join(os.getcwd(), filepath), 'r', encoding='utf-8') as f:
        text_in = f.read()
    text_in = ''.join(text_in.splitlines())

    # 1c. Tokenize text
    tokens = word_tokenize(text_in)

    # 1d. Create bigrams list
    bigram_list = list(nltk.bigrams(tokens))

    # 1e. Create unigrams list
    unigram_list = list(nltk.ngrams(tokens, 1))

    # 1f. Create bigram frequency dictionary
    bigram_dict = {b:bigram_list.count(b) for b in set(bigram_list)}

    # 1g. Creat unigram frequency dictionary
    unigram_dict = {t:unigram_list.count(t) for t in set(unigram_list)}

    # 1h. Return dictionaries
    return unigram_dict, bigram_dict

if __name__ == '__main__':

    # Preprocess text
    english_unigram, english_bigram = preprocess_file('data\LangId.train.English')
    french_unigram, french_bigram = preprocess_file('data\LangId.train.French')
    italian_unigram, italian_bigram = preprocess_file('data\LangId.train.Italian')

    # Save to pickle files
    pickle.dump(english_unigram, open('eng_uni.p', 'wb'))
    pickle.dump(english_bigram, open('eng_bi.p', 'wb'))
    pickle.dump(french_unigram, open('fre_uni.p', 'wb'))
    pickle.dump(french_bigram, open('fre_bi.p', 'wb'))
    pickle.dump(italian_unigram, open('ita_uni.p', 'wb'))
    pickle.dump(italian_bigram, open('ita_bi.p', 'wb'))