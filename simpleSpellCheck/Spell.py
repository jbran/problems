#!/usr/bin/python
"""
    Relies on the existance of /usr/share/dict/words to load a default dict.
    One can modify the code to pass in a new location to a dict at the bottom
    where load_dict() becomes load_dict('/path/to/awesometown')

    The dictionary is backed by a prefix tree and candidate words are found via
    mutations in the input string.

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

    Developed on 32bit Ubuntu 10.04 & 11.04
    Python 2.6.5 & 2.7.1 & wamerican dict

"""


vowels = set(['a','e','i','o','u'])

class Node:
    def __init__(self, value=None):
        self.children = {}
        self.word = ""
        self.letter = value

    #helper for recursion
    def add_word(self, word):
        #Store the "proper" word, but build the path to it via the lower
        #This allows all searching to be done with just lower case
        #but to return a proper case word
        self.add_word_recur(word,word.lower())

    def add_word_recur(self, full_word, word_left):
        if word_left == "":
            self.word = full_word
            return

        key = word_left[0]
        rest = word_left[1:]

        if key in vowels:
            key = 'a'

        if key not in self.children:
            self.children[key] = Node(key)

        self.children[key].add_word_recur(full_word, rest)

    def find_fuzzy(self, word):
        matches = self.find_fuzzy_matches(word.strip().lower())

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

        if key in vowels:
            key = 'a'

        #Deal with case problems
        #Handle: acapulco -> Acapulco
        matches = []
        if key in self.children:
            matches = self.children[key].find_fuzzy_matches(rest)
        matches = [m for m in matches if m] #remove None's
        #Short-Circuit opportunity: We have a match!
        if len(matches) > 0:
            return matches

        # try with repeated letters or repeated vowels removed
        # Handle: wakkkke -> wake
        #         weeeeeeke -> wake
        #         waeaoiooika -> wake
        fuzzy_matches = []
        if self.letter == key:
            m = self.find_fuzzy_matches(rest)
            fuzzy_matches.extend(m)

        # remove None's
        fuzzy_matches = [m for m in fuzzy_matches if m]
        # calculate edit distance of our fuzzy matches
        adjustd_fuzzy_matches = [(distance+1,w) for distance,w in fuzzy_matches]
        return adjustd_fuzzy_matches
        

dict_tree = Node()

def load_dict(words="/usr/share/dict/words"):
    f = open(words, 'r')
    for line in f:
            dict_tree.add_word(line.strip())

print "Loading dictionary at /usr/share/dict/words ..."
load_dict()
print "Loaded. Cntrl-C or Cntrl-D will kill program."

while(True):
    word = raw_input("> ")
    #We only search on lower case input. See the comment in add_word
    print dict_tree.find_fuzzy(word)
