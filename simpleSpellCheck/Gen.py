vowels = set(['a','e','i','o','u'])

def generate(word):
    v_combins = [word]#Add original
    items = find_vowel_combinations(word,0,0)
    v_combins.extend(items)
    return v_combins 

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

words = [
        "weke",
        "awesomme"
        ]




for word in words:
    possibles = generate(word)
    for item in possibles:
        print item
