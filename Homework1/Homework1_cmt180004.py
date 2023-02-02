import sys
import os
import re
import pickle

def read_file(filepath):
    """
    Reads the file into a (very large) string variable
    Args -
        filepath: str that specifies location of data file
    Returns -
        text_in: str of the file's contents
    """
    with open(os.path.join(os.getcwd(), filepath), 'r') as f:
        text_in = f.read()
    return text_in


def process_file(input_text):
    """
    Processes the file to make list of 'Person' entities
    Args -
        input_text: str that has content of input file
    Returns -
        all_people: dict of people in file with unique IDs
    """
    # Create dict to add people in
    all_people = {}

    # Break down into list of lines
    line_list = input_text.split('\n')

    # Break down each entry into list of words to
    # process each Person's information
    for i in range(1, len(line_list)):
        word_list = line_list[i].split(',')

        # Save information about this person
        # If unavailable or invalid, prompt for reentry

        # Last name requirements
        #   1. Alphabetical
        # Prompt user if
        #   1. Empty
        #   2. Non-alphabetical (numeric, spaces)
        my_last = word_list[0]
        first = True
        while first:
            if my_last.isalpha():
                last = my_last.capitalize()
                first = False
            else:
                print('\n')
                print(word_list)
                my_last = input('Entry above missing alphabetical last name.\nPlease enter: ')
                word_list[0] = my_last

        # First name requirements
        #   1. Alphabetical
        # Prompt user if
        #   1. Empty
        #   2. Non-alphabetical (numeric, spaces)
        my_first = word_list[1]
        second = True
        while second:
            if my_first.isalpha():
                first = my_first.capitalize()
                second = False
            else:
                print('\n')
                print(word_list)
                my_first = input('Entry above missing an alphabetical first name.\n Please enter: ')
                word_list[1] = my_first

        # Middle initial requirements:
        #   1. 'X' if empty
        #   2. First letter if alphabetical
        # Prompt user if
        #   1. Non-alphabetical (numeric, spaces)
        my_mi = word_list[2]
        third = True
        while third:
            if not my_mi:
                mi = 'X'
                third = False
            elif my_mi.isalpha():  # Take first letter if given alpha string
                mi = my_mi[0].capitalize()
                third = False
            else:
                print('\n')
                print(word_list)
                my_mi = input('Entry above is missing valid middle initial. \nPlease enter: ')
                word_list[2] = my_mi

        # ID requirements:
        #   1. 2 alphabetical followed by 4 numerical
        # Prompt user if
        #   1. ID does not meet requirements
        my_id = word_list[3]
        fourth = True
        valid_id = re.compile('^[A-Za-z]{2}[0-9]{4}$')
        while fourth:
            id_match = valid_id.match(my_id)
            if id_match:
                id = my_id.upper()
                fourth = False
            else:
                print('\n')
                print(word_list)
                my_id = input(
                    'Entry above is missing valid ID.\nShould be 2 alphabetical character followed by 4 digits. \nPlease enter: ')
                word_list[3] = my_id

        # Phone number requirements:
        #   1. ###-###-####, can reformat if needed
        # Prompt user if
        #   1. Phone number still invalid after reformatting
        my_phone = word_list[4]
        fifth = True
        valid_phone = re.compile('^[0-9]{3}[-][0-9]{3}[-][0-9]{4}$')
        while fifth:
            # Use regex to remove '.' and ' ' and '(' and ')'
            my_phone = re.sub(r"(\.)|(\s)|(\()|(\))", '', my_phone)
            # Insert '-' if not already there
            if my_phone[3] != '-':
                my_phone = my_phone[0:3] + '-' + my_phone[3:]
            if my_phone[7] != '-':
                my_phone = my_phone[0:7] + '-' + my_phone[7:]
            # Check against requirement
            phone_match = valid_phone.match(my_phone)
            if phone_match:
                phone = my_phone
                fifth = False
            else:
                print('\n')
                print(word_list)
                my_phone = input('Entry above is missing valid phone number.\nFormat is XXX-XXX-XXXX.\nPlease enter: ')
                word_list[4] = my_phone

        # Instantiate Person and add to dictionary
        new_person = Person(last, first, mi, id, phone)

        if id in all_people:
            print('Could not add the following person with duplicate ID to system.')
            new_person.display()
        else:
            all_people[id] = new_person
    return all_people


class Person:
    """
    Represents each entity of the data file read in.
    """

    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    def display(self):
        """
        Prints out each Person and information about their field
        Args -
            None
        Returns -
            None
        """
        print('Employee id:', self.id)
        print('\t', self.first, self.mi, self.last)
        print('\t', self.phone)


if __name__ == '__main__':
    # Read file into a string field
    fp = sys.argv[1]
    input_text = read_file(fp)

    # Process the file
    people_dict = process_file(input_text)

    # Save created dict into a pickle file
    pickle.dump(people_dict, open('dict.p', 'wb'))

    # Open pickle file and display each Person
    other_people_dict = pickle.load(open('dict.p', 'rb'))
    print('Employee list:\n')
    for person in other_people_dict.values():
        person.display()
