"""
Given a string "aaaabbbbccc", break it into a list of valid words
given a dictionary.
"""
import prefix_dict

#Our pruned dictionary of /usr/share/dict/words
dict_tree = prefix_dict.Node()

def load_dict(words="/usr/share/dict/words"):
    with open(words, 'r') as f:
        for line in f:
            if len(line.strip()) > 1:
                dict_tree.add_word(line.strip())
    dict_tree.add_word("a")

load_dict()

def break_down(dictionary, word):
    if word == '':
        return []
    else:
        return word_break(dictionary, word)

def word_break(dictionary, word):
    for prefix_location in xrange(len(word)+1):
        prefix = word[:prefix_location]
        suffix = word[prefix_location:]
   
        if prefix in dictionary:
            # Try some more
            result = break_down(dictionary, suffix)
            if result != None:
                return [prefix] + result
             
    return None            

print "be" in dict_tree
print "ware" in dict_tree
print word_break(dict_tree, "beware")
print word_break(dict_tree, "superbewaretree")
