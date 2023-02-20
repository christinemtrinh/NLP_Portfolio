# Need the following package to be installed
# If using PyCharm:
# File -> Settings -> Project -> Python Interpreter -> Search 'nltk' -> Install
import sys
import os
import math
from random import seed
from random import randint
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download('averaged_perceptron_tagger')

def preprocess_file(filepath):
    """
    Reads the file into a (very large) string variable
    Args -
        filepath: str that specifies location of data file
    Returns -
        tokens: list of filtered str tokens
        nouns: list of filtered str nouns
    """
    with open(os.path.join(os.getcwd(), filepath), 'r') as f:
        text_in = f.read()
    tokens = word_tokenize(text_in)

    # Calculating lexical diversity from tokens
    unique_tokens = set()
    for i in tokens:
        unique_tokens.add(i)
    lexical_diversity = len(unique_tokens) / len(tokens)
    print(str(math.ceil(lexical_diversity*100*100)/100) + '% of words are unique')

    # 3a. Filtering tokens
    stop_words = set(stopwords.words('english'))
    filtered_tokens = []
    for i in tokens:
        if i.isalpha() and len(i) > 5 and i not in stop_words:
            filtered_tokens.append(i.lower())

    # 3b. Lemmatizing tokens and saving unique ones
    lemmatizer = WordNetLemmatizer()
    unique_lemmas = set()
    for i in filtered_tokens:
        unique_lemmas.add(lemmatizer.lemmatize(i))

    # 3c. POS tag the lemmas and print the first 20
    unique_lemmas_list = list(unique_lemmas)
    tagged_lemmas = nltk.pos_tag(unique_lemmas_list) # Accepts lists only
    print('\nShowing first 20 tagged unique lemmas:')
    for i in range(20):
        print(tagged_lemmas[i])

    # 3d. Filter lemmas to nouns then print proportion
    noun_lemmas = []
    for i in tagged_lemmas:
        if i[1] in {'NN', 'NNS', 'NNP', 'NNPS'}:
            noun_lemmas.append(i[0])
    print('\nNum tokens:', len(filtered_tokens))
    print('Num unique noun lemmas:', len(noun_lemmas))

    # 3f. Return filtered tokens and noun lemmas
    return filtered_tokens, noun_lemmas

def pool_nouns(tokens, nouns):
    """
    Counts occurrences of nouns in tokens and keeps most frequent 500
    Args -
        nouns: list of words to count
        tokens: body of text to count nouns in
    Returns -
        word_list: list of 50 words to be used in guessing game
    """

    # Count occurrences
    noun_count = dict()
    for i in tokens:
        if i in nouns:
            if i in noun_count:
                noun_count[i] = noun_count[i] + 1
            else:
                noun_count[i] = 1

    # Sort dictionary based on occurrences
    sorted_nouns = sorted(noun_count.items(), key=lambda x:x[1], reverse=True)
    sorted_nouns = [x[0] for x in sorted_nouns] # Keep keys only
    return sorted_nouns[:50]                    # Keep top 50 only

def run_game(word_list):
    """
    Facilitates guessing game through the console
    Args -
        word_list: list of words to guess
    Returns -
        None
    """
    # Initialize variables
    point = 5                   # player's starting points
    guess = ''                  # stores the player's guess
    round_in_progress = False   # indicates if new word needs to be generated
    key = ''                    # stores word to guess
    progress = []               # boolean tracking letters guessed
    seed()                      # helps to pick random word
    game_over = False           # indicates to end game
    letters_guessed = set()     # tracks letters guessed for this round so far
    letters_left=0

    # Run game
    while point >= 0 and not game_over:
        # Generate new word if needed
        if not round_in_progress:
            key = word_list[randint(0, 49)]
            progress.clear()
            progress += len(key) * [False]
            round_in_progress = True
            letters_guessed.clear()
            letters_left = len(key)

        # Display game state
        print('')
        for i, j in enumerate(progress):
            if not j:
                print('_', end=' ')
            else:
                print(key[i], end=' ')

        # Take user guess and validate length and alpha
        guess = ''
        print('')
        while (len(guess) != 1 and len(guess) != len(key)) or (guess.isalpha() == False and guess != '!') or guess in letters_guessed:
            guess = input("Guess ('!' to quit): ")
            if (len(guess) != 1 and len(guess) != len(key)) or (guess.isalpha() == False and guess != '!'):
                print('Invalid guess')
            if guess in letters_guessed:
                print('You guessed that letter already')

        # Process guess
        if guess == '!':                    # 1. User terminates
            game_over = True
        elif len(guess) == 1:               # 2. Letter guess
            letters_guessed.add(guess)
            if guess in key:                # 2a. Correct
                point += 1
                print('Right!', point, 'points.')
                for i, j in enumerate(key): # Update display
                    if j == guess:
                        progress[i] = True
                        letters_left -= 1
                if letters_left == 0:       # Check if word complete
                    print('\nWord complete! Generating new word...')
                    round_in_progress = False
            else:                           # 2b. Bad guess
                point -= 1
                if point < 0:
                    print('No points left!')
                    game_over = True
                else:
                    print('Sorry, guess again.', point, 'points.')
        else:
            if guess == key:
                for i in progress:
                    if i == False:
                        point += 1
                print('You guessed the word correctly!', point, 'points.')
                round_in_progress = False
            else:
                print('You guessed the wrong word. 5 pt penalty.')
                point -= 5
                game_over = True

    # Display end of game summary
    print('\nGame over! You had', point, 'points.')
    print('(The word was', key, ';p)')

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('No system arg is present. Please specify via Run -> Edit Configurations -> Parameters.')
        exit()

    # Preprocess text
    tokens, nouns = preprocess_file(sys.argv[1])

    # Make pool of words for guessing game
    word_list = pool_nouns(tokens, nouns)

    # Run game
    run_game(word_list)