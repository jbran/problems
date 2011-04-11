#!/usr/bin/python
"""
    Relies on the existance of /usr/share/dict/words to load a default dict.
    One can modify the code to pass in a new location to a dict at the bottom
    where load_dict() becomes load_dict('/path/to/awesometown')

    Tested on 32bit Ubuntu 10.04
"""

class Node:
    def __init__(self):
        self.children = {}
        self.word = ""

    def add_word(self, word):
        self.add_word_int(word,word)

    def add_word_int(self, full_word, word_left):
        if word_left == "":
            self.word = full_word
            return

        key = word_left[0]
        rest = word_left[1:]

        if key not in self.children:
            self.children[key] = Node()

        self.children[key].add_word_int(full_word, rest)

    def find_word(self, word):
        if word == "":
            return self.word

        key = word[0]
        rest = word[1:]

        try:
            return self.children[key].find_word(rest)
        except:
            return ""

dict_tree = Node()

vowels = set(['a','e','i','o','u'])


def load_dict(words="/usr/share/dict/words"):
    with open(words, 'r') as f:
        for line in f:
            dict_tree.add_word(line.strip())

def find_exact(word):
    return dict_tree.find_word(word)

def find_word(word):
    lower = word.lower()
    # Try lower case word first
    value = find_exact(lower) 
    
    valids = {}
    # Prune Repeats and vowel combinations
    if value is None or value is "":
        # Repeats
        possibles = find_combinations(lower,0,1)
        print possibles
        for item in possibles:
            if item == find_exact(item):
                valids[item] = possibles[item]

        # Find Vowel Combinations
                



    if len(valids) > 0:
        print valids 

    output_str = "  Looking for a match for "+ word+ ": "
    if value is None or value is "":
        return output_str+'NO SUGGESTIONS'
    else:
        return output_str+value


def find_combinations(word, start,distance):
    output = {}
    last = None
    last_repeat= None
    for i,x in enumerate(word):
        if i < start:
            last = x
            continue
        if x is last: 
            if not x is last_repeat:
                last_repeat = x
                new_word = word[:i] + word[i+1:]
                output[new_word]=distance
                #output.append(new_word)
                items = find_combinations(new_word, i, distance+1)
                output.update(items)
                #for item in items:
                #    output.append(item)
        else:
            last_repeat = None
        last = x
    return output



print "Loading dictionary at /usr/share/dict/words ..."
load_dict()
print "Loaded."
#print find_word("mateg")
print find_word("mate")
print find_word("MATE")
print find_word("mATe")
print find_word("matte")
#print find_word("mattte")
print find_word("mmmattte")
#print find_word("CUNsperrICY")

