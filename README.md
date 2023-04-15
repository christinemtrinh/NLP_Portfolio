# NLP_Portfolio
 Following Spring 2023 CS 4395 course taught by Karen Mazidi, UT Dallas
 
## Index
### 0. Introduction to NLP  
A [document](Overview_of_NLP.pdf) discussing basic background information (definition, history, personal interest) about NLP.
<br/>
### 1. Text Processing with Python
A [program](Homework1/Homework1_cmt180004.py) that takes a CSV file and processes them with format checking. It then creates a dictionary from all of the entries and loads it into a pickle file. It immediately unpacks the pickle file and is able to use the objects and their methods.  
#### How to Run:  
Download the contents of the folder labeled "Homework1." Upload it into the preferred IDE. Sysargs should be specified to point to the location of the data file. It was data\data.csv in my case. Also the script path should be specified as the .py file named "Homework1_cmt180004.py."  
#### Reflection:  
Python is useful for text processing because of how dynamically it treats data. Strings are simply lists of characters, so operations are very simple and straight forward. It also has a lot of built in methods for applicable checking and manipulating: alphabetical, cases, empty. This flexibility can also come as a weakness. Code can easily run without raising errors so it could cause unexpected behavior requiring extensive testing to catch.  
This assignment enabled me to learn how to use regular expressions. I also have never used pickle files before. It seems to be helpful for developing code and working with data where it would waste a lot of time to process the data over and over. Rather, it can be saved in a pickle file to unpack for future steps. This assignment was also a useful review of Python lists and classes.
<br/>
### 2. Word Guessing Game
A [program](Homework2/Homework2_cmt180004.py) that accepts a text file and does some preprocessing (including calculating lexical diversity, filtering, pos-tagging using NLTK) before starting a hangman game with the user.

### 3. Using WordNet
A [program](Homework3/Homework3_cmt180004.ipynb) that explores different features of WordNet and sentiment analysis.

### 4. Ngrams Language Modeling
This assignment uses two programs. The [first](Homework4/Homework4a_cmt180004.py) uses given texts to train three different models representing a different language. The [second](Homework4/Homework4b_cmt180004.py) then unpacks the models and runs them with some test data to recognize the language being used. Finally, the models' outputs are compared with the solution given by a human annotator to assess the performance of the model.

### 5. Sentence Parsing 
A [document](Homework5/Homework5_cmt180004.pdf) that uses three kinds of parsers for a complex sentence. All of these parsers aim to reduce ambiguity in different ways.

### 6. Building a Corpus
A [program](Homework6/Homework6_cmt180004.py) that recursively scrapes websites to get info about a predefined topic (Mediterranean food!). It does its best to filter out what may not be helpful and keep what is. It builds a knowledge base that can have further applications, such as a chatbot.

### 7. Trying Machine Learning Approaches
A [report](Homework7/Homework7_cmt180004.pdf) where I created 3 different ML models that attempts sentiment analysis, a common application of NLP. I found that the logistic regression performed best with this data set and my chosen hyperparameters.

### 8. Implementing a Chatbot
A [program](ChatbotProject/Project1_cmt180004_emu200000.ipynb) that attempts to implement a chatbot that can answer AI/ML/NLP related questions.
