#!/usr/bin/python
"""
    Relies on the existance of /usr/share/dict/words to load a default dict.
    One can modify the code to pass in a new location to a dict at the bottom
    where load_dict() becomes load_dict('/path/to/awesometown')

    Handles three mispellings:
        1) Case (upper/lower) errors: "inSIDE" => "inside"
        2) Repeated letters: "jjoobbb" => "job"
        3) Incorrect vowels: "weke" => "wake"

    And a combination of them:
        "CUNsperrICY" => "conspiracy"
        "weeeeeeeeke" => "wake" (Wrong vowel, then repeated)
        "waeiouuioka" => "woke" (Repeated vowel, then vowel wrongified)
        "aaacapulco"  => "Acapulco"
        "AaAcapulco"  => "Acapulco"

    Tested on 32bit Ubuntu 10.04 & 11.04
    Python 2.6.5 & 2.7.1 & wamerican dict

"""

vowels = set(['a','e','i','o','u', 'A', 'E', 'I', 'O', 'U'])

class Node:
    def __init__(self, value=None):
        self.children = {}
        self.word = ""
        self.letter = value

    #helper for recursion
    def add_word(self, word):
        self.add_word_recur(word,word)

    def add_word_recur(self, full_word, word_left):
        if word_left == "":
            self.word = full_word
            return

        key = word_left[0]
        rest = word_left[1:]

        if key not in self.children:
            self.children[key] = Node(key)

        self.children[key].add_word_recur(full_word, rest)

    def find_fuzzy(self, word):
        matches = self.find_fuzzy_matches(word)

        if matches:
            return reduce(lambda x,y: x if x[0] <= y[0] else y, matches)[1]
        else:
            return 'NO SUGGESTIONS'

    def find_fuzzy_matches(self, word):
        if word == "":
            if self.word:
                return [(0,self.word)]
            else:
                return []

        key = word[0]
        rest = word[1:]

        #Deal with case problems
        #Handle:  
        lower_matches = []
        if key.lower() in self.children:
            lower_matches = self.children[key.lower()].find_fuzzy_matches(rest)
        lower_matches = [m for m in lower_matches if m] #remove None's
        if len(lower_matches) > 0:
            return lower_matches
        upper_matches = []
        if key.upper() in self.children:
            upper_matches = self.children[key.upper()].find_fuzzy_matches(rest)
        upper_matches = [m for m in upper_matches if m]            
        #Short-Circuit opportunity: We have a match!
        if len(upper_matches) > 0:
            return upper_matches

        fuzzy_matches = []
        #Try descending via mutated vowels
        #Handle: wuka -> wake
        if key in vowels:
            for v in vowels:
                if v != key:
                    if v in self.children:
                        m = self.children[v].find_fuzzy_matches(rest)
                        fuzzy_matches.extend(m)

        # try with repeated letters or repeated vowels removed
        # Handle: wakkkke -> wake
        #         weeeeeeke -> wake
        #         waeaoiooika -> wake
        vowel_repeat = (key in vowels and rest != "" and rest[0] in vowels)
        letter_repeat = (key and self.letter and self.letter.lower() == key.lower())
        if letter_repeat or vowel_repeat:
            m = self.find_fuzzy_matches(rest)
            fuzzy_matches.extend(m)

        # remove None's
        fuzzy_matches = [m for m in fuzzy_matches if m]
        # calculate edit distance of our fuzzy matches
        adjustd_fuzzy_matches = [(distance+1,w) for distance,w in fuzzy_matches]
        return adjustd_fuzzy_matches
        

dict_tree = Node()

def load_dict(words="/usr/share/dict/words"):
    with open(words, 'r') as f:
        for line in f:
            dict_tree.add_word(line.strip())

print "Loading dictionary at /usr/share/dict/words ..."
load_dict()
print "Loaded. Cntrl-C or Cntrl-D will kill program."

while(True):
    word = raw_input("> ")
    print dict_tree.find_fuzzy(word.strip())
