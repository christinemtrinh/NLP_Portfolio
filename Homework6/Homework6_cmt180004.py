import nltk
from collections import deque
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import requests
import pickle
import urllib.request
import re


def get_links(start_url, keywords, filtered_out):
    """
    Takes a starting URL and uses links on that page to build
    a reference list to an external file.
    Args -
        start_url: str URL where the crawling begins
        keywords: list of words that, if appearing in link, determines inclusion
        filtered_out: list of words determining exclusion even if keyword included
    Returns -
        Nones
    """
    # Initialize starting point of web crawler
    url_queue = deque([])       # Queue of URLs to scan
    link_set = set()            # Set of added URLs
    url_queue.append(start_url)
    counter = 0

    # Write URLs to a file
    with open('urls.txt', 'w') as f:

        # Get next URL of queue
        while url_queue:
            this_url = url_queue.popleft()

            # Try to open it and process
            try:
                r = requests.get(this_url)
                data = r.text
                soup = BeautifulSoup(data, "html.parser")

                # Get through all links of this page before going back to queue
                for link in soup.find_all('a'):
                    link_str = str(link.get('href'))

                    # Filter links
                    if any([x in link_str for x in keywords])\
                            and all([x not in link_str for x in filtered_out]):
                        # Trim left side
                        if link_str.startswith('/url?q='):
                            link_str = link_str[7:]
                        # Trim right side
                        if '&' in link_str:
                            i = link_str.find('&')
                            link_str = link_str[:i]
                        # Check that this isn't a duplicate
                        if link_str not in link_set:
                            link_set.add(link_str)

                            # Trick for including more links within domain
                            if link_str.startswith('/wiki'):
                                link_str = 'http://en.wikipedia.org' + link_str

                            # Rid any non-URLs
                            if link_str.startswith('http'):
                                url_queue.append(link_str)
                                f.write(link_str + '\n')
                                counter += 1
            # Page could not open, move to next item in queue
            except requests.exceptions.RequestException:
                print('Could not open', this_url)

            # Trying to get 40+ URLs
            if counter > 1:
                break

    # Finished link building
    print('Crawler found', counter, 'links\nExtracting their content...')


def visible(element):
    """
    Helper function to determine if HTML is visible
    Args -
        element: HTML element to check
    Returns -
        True or False: if element can be displayed
    """
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))): # HTML comments
        return False
    return True


def extract_text():
    """
    Extracts each URL's contents and puts it into its own file
    Args -
        url: str of URL to extract
    Returns -
        page_title: str of file name containing content
    """
    # Create a text file to work like an index of titles
    counter = 0
    with open('page_titles.txt', 'w') as f:

        # Read through all available URLs
        with open('urls.txt', 'r') as g:
            urls = g.read().splitlines()
            for my_url in urls:
                try:
                    # Open URL and get content
                    html = urllib.request.urlopen(my_url)
                    soup = BeautifulSoup(html, 'html.parser')
                    data = soup.find_all('p')
                    tmp_lst = []
                    for d in data:
                        segment = d.get_text()
                        tmp_lst.append(segment)
                    #result = filter(visible, data)
                    #tmp_lst = list(result).get_text()
                    tmp_str = ' '.join(tmp_lst)

                    # Prepare file name
                    page_title = soup.find('title').string
                    page_title = page_title.replace(' ', '_')
                    page_title += '.txt'

                    # Write content to file
                    with open(page_title, 'w', encoding='utf-8') as h:
                        h.write(tmp_str)

                    f.write(page_title + '\n')
                    counter += 1
                # Abandon failed links i.e. OSError, requests.error.HTTPError, etc.
                # While developing, it seems like most of the failed were non-Wikipedia
                # Other than that, I'm not sure why their extraction would be unsuccessful
                except Exception as e:
                    print('Failed extraction:', my_url)

    print('\nExtracted content from', counter, 'files\nCleaning their content...')




def preprocess1():
    """
    Creates a file of sentence tokens for each file
    Args -
        None
    Returns -
        None
    """

    counter = 0
    with open('page_titles.txt', 'r', ) as f:
        titles = f.read().splitlines()
        for t in titles:
            with open(t, 'r+', encoding='utf-8') as g:
                text = g.read()

                # Delete newlines and tabs
                text = ''.join(text.splitlines())
                text = ''.join(text.split('\t'))

                # Sentence tokens
                sentences = sent_tokenize(text)
                counter += 1
                # Sentence file namer
                sent_file = 'Sen_' + t

                # Write sentences to file
                with open(sent_file, 'w', encoding='utf-8') as h:
                    for i in sentences:
                        h.write(i+'\n')

    print(counter, 'sentence files made')


def preprocess2():
    """
    Preprocesses files (again) this time for word tokens.
    Will also find most frequent terms and output.
    Args -
        None
    Returns -
        None
    """
    with open('page_titles.txt', 'r', encoding='latin-1') as f:
        titles = f.read().splitlines()
        overall_dict = {}
        for t in titles:
            with open(t, 'r+', encoding='utf-8') as g:
                text = g.read()
                # Delete newlines and tabs
                text = ' '.join(text.splitlines())
                text = ' '.join(text.split('\t'))

                # Tokenize by word
                tokens = word_tokenize(text)
                # Remove stop words and punctuation
                filtered_tokens = []
                stop_words = set(stopwords.words('english'))
                filtered_tokens = [w.lower() for w in tokens if w.isalpha() and w not in stop_words]
                # Write tokens back to file

                # Make a dict name
                this_dict = create_tf_dict(filtered_tokens)

                # Make a dict in an overwriting fashion, to keep greatest tf
                for i in this_dict.items():
                    if i[0] in overall_dict.keys():
                        overall_dict[i[0]] = max(i[1], overall_dict[i[0]])
                    else:
                        overall_dict[i[0]] = i[1]

    tf_weights = sorted(overall_dict.items(), key=lambda x: x[1], reverse=True)
    # print(len(tf_weights)) #44305 words, repeat enabled
    print(tf_weights[:32])


def create_tf_dict(tokens):
    tf_dict = {}
    for t in tokens:
        if t in tf_dict:
            tf_dict[t] += 1
        else:
            tf_dict[t] = 1
    # Normalize tf by number of tokens
    for t in tf_dict.keys():
        tf_dict[t] = tf_dict[t] / len(tokens)
    return tf_dict


def build_knowledge(topics):
    """
    Build knowledge base for each topic
    Args -
        topics: list of str that are topics to build knowledge base
    Return -
        None
    """
    knowledge_base = {}
    with open('page_titles.txt', 'r', encoding='latin-1') as f:
        titles = f.read().splitlines()
        for t in titles:
            sentence_file = 'Sen_' + t
            with open(sentence_file, 'r', encoding='utf-8') as g:
                text = g.read()
                text = text.splitlines()
                for i in text:
                    for j in topics:
                        if j in i.lower():          # topic word found in sentence, add to dict
                            if j in knowledge_base.keys():
                                knowledge_base[j].append(i)
                            else:
                                knowledge_base[j] = [i]
    for i, j in knowledge_base.items():
        print(i)
        for k in j:
            print('\t'+k)

    # Save knowledge to pickle file
    pickle.dump(knowledge_base, open('knowledge_base.p', 'wb'))


if __name__=='__main__':

    # Define criteria of links to keep or filter out and starting point
    keywords = ['Mediterranean', 'cuisine', 'food']
    filtered_out = ['Templat', 'Special', 'Cookbook', 'Talk', 'Category',
                    'instagram', 'facebook', 'pinterest', 'twitter']
    start_url = 'https://en.wikipedia.org/wiki/Mediterranean_cuisine'

    # Create file of relevant URLs
    get_links(start_url, keywords, filtered_out)

    # Extract information from each
    extract_text()

    # Reopen each file and preprocess text
    preprocess1()

    # Continue preprocessing and get most frequent terms
    preprocess2()

    # Build my knowledge base based on 10 selected terms
    knowledge_topics = ['cuisine', 'history', 'levantine', 'indian', 'arbëreshë',
                        'north', 'american', 'greek', 'italian', 'albanian']
    build_knowledge(knowledge_topics)







