'''
Will generate combinations of mutated vowels and then repeated characters to generate a mispelled word given a source word. Does not do full vowel mutation for the sake of speed: Just replaces every vowel with 'aeiou'

'''

import random

vowels = set(['a','e','i','o','u'])

def generate(word):
    """
    Given a word will generate:
        1) Bad vowel combinations 
            wake => weke
                    woka ...
        2) Letter repetition
            wake => wwwwake
                    waaaake ...
        3) All vowels wrongified
            wake => waeioukaeiou

    """
    v_combins = [word]#Add original
    #items = find_vowel_combinations(word,0,0)
    #v_combins.extend(items)
    combinations = generate_repeats(v_combins)
    wrong_vowels = generate_wrong_vowels(word) 
    combinations.extend(wrong_vowels)
    return combinations

def generate_wrong_vowels(word):
    """ One way to generate bad vowels """
    vowels = "aeiou"
    word = word.replace("u","a")
    word = word.replace("o","a")
    word = word.replace("i","a")
    word = word.replace("e","a")
    word = word.replace("a",vowels)
    return [word]
 
def generate_repeats(list_of_words):
    combins = []
    combins.extend(list_of_words)
    for word in list_of_words:
        word_combs = []
        for i in reversed(range(len(word))):
            word_combs.extend(add_repeat(word,i))
    combins.extend(word_combs)
    return combins

def add_repeat(word,i):
    max_repeat = 3 #Max because I said so
    repeats = [word]
    while max_repeat > 0:
        new_word = word[:i] + (max_repeat*word[i]) + word[i:]
        repeats.append(new_word)
        max_repeat -= 1
    return repeats


words = []
    
def load_words(dictionary="/usr/share/dict/words"):
    #with open(dictionary, 'r') as f:
    f = open(dictionary, 'r')
    for line in f:
        if random.randint(0,100) < 4:    
	    words.append(line.strip())

load_words()            
for word in words:
    possibles = generate(word)
    for item in possibles:
        if random.randint(0,100) < 1:
            #Randomize the case of the word
            #By have the 10 most popular letters uppercase only
            item = item.lower()
            item = item.replace("e","E",2)
            item = item.replace("t","T",2)
            item = item.replace("a","A",2)
            item = item.replace("o","O",2)
            item = item.replace("i","I",2)
            item = item.replace("n","n",2)
            item = item.replace("s","S",2)
            item = item.replace("h","H",2)
            item = item.replace("r","R",2)
            item = item.replace("d","D",2)
        print item
