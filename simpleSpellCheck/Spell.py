#!/usr/bin/python
"""
    Relies on the existance of /usr/share/dict/words to load a default dict.
    One can modify the code to pass in a new location to a dict at the bottom
    where load_dict() becomes load_dict('/path/to/awesometown')

    Tested on 32bit Ubuntu 10.04
"""

import heapq
import operator

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
    value = find_exact(lower) 
    
    valids = {}
    # If lower failed: Prune Repeats and vowel combinations
    if value is None or value is "":
        # Repeats
        possibles = find_combinations(lower,0,1)
        #print possibles
        #Add to valid everything after just repeated pruning
        for item in possibles:
            if item == find_exact(item):
                valids[item] = possibles[item]

        # Find Vowel Combinations
        total_words = {}
        for item,distance in possibles.iteritems():
            more_words = find_vowel_combinations(item,0,distance)
            total_words.update(more_words)
        print total_words
        #Add to valid everything that is vowel mutated 
        for item,distance in total_words.iteritems():
            if item == find_exact(item):
                valids[item] = total_words[item]

    if len(valids) > 0:
        print valids 
        print sorted(valids.iteritems(), key=operator.itemgetter(1))
        print sorted(valids, key=valids.get)
        

    output_str = "  Looking for a match for "+ word+ ": "
    if value is None or value is "":
        return output_str+'NO SUGGESTIONS'
    else:
        return output_str+value

def find_vowel_combinations(word,start,distance):
    output = {}
    for i,x in enumerate(word):
        if i < start:
            continue
        if x in vowels:
            items = vowel_combin(word,i,x,distance)
            output.update(items)
            #for item in items:
                #moreitems = find_vowel_combinations(item,i+1,distance)
                #print item
                #for this in moreitems:
                #    output.append(this)
            #    output[item]=items[item] #Use update?
    return output

def vowel_combin(word,i,x,distance):
    possibles = {}
    for vowel in vowels:
        if not vowel is x:
            new_word = word[:i] + vowel + word[i+1:]
            possibles[new_word] = distance
            #possibles.append(new_word)
            items = find_vowel_combinations(new_word,i+1,distance+1)
            possibles.update(items)
            #for item in items:
            #    possibles[item] = items[item]
                #possibles.append(item)
    return possibles
            

def find_combinations(word,start,distance):
    output = {}
    last = None #The last letter we saw
    last_repeat= None #The last consecutive repeat
    for i,x in enumerate(word):
        if i < start:
            last = x
            continue
        if x is last: 
            if not x is last_repeat:
                last_repeat = x
                #Remove i from the word: Better way?
                new_word = word[:i] + word[i+1:]
                output[new_word]=distance
                #Don't increment i, since we are trimming the old i away
                items = find_combinations(new_word, i, distance+1)
                output.update(items)
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

