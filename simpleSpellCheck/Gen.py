'''
    Will generate combinations of mutated vowels and then repeated characters to generate a mispelled word given a source word. Does not try to handle randomly capitlizing words since those all covered by a call to lower
'''

vowels = set(['a','e','i','o','u'])

def generate(word):
    v_combins = [word]#Add original
    items = find_vowel_combinations(word,0,0)
    v_combins.extend(items)
    combinations = generate_repeats(v_combins)
    return combinations

def vowel_combin(word,i,x,distance):
    possibles = []
    for vowel in vowels:
        if vowel != x:
            new_word = word[:i] + vowel + word[i+1:]
            possibles.append(new_word  )
            items = find_vowel_combinations(new_word,i+1,distance+1)
            possibles.extend(items)
    return possibles   

def find_vowel_combinations(word,start,distance):
    output = []
    for i,x in enumerate(word):
        if i < start:
            continue
        if x in vowels:
            items = vowel_combin(word,i,x,distance)
            output.extend(items)
    return output

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
    max_repeat = 4 #Max because I said so
    repeats = [word]
    while max_repeat > 0:
        new_word = word[:i] + (max_repeat*word[i]) + word[i:]
        repeats.append(new_word)
        max_repeat -= 1
    return repeats
    
    
            


words = [
        "weke",
        "awesomme"
        ]



for word in words:
    possibles = generate(word)
    for item in possibles:
        print item
