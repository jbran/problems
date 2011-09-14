class Node:
    def __init__(self):
        self.children = {}
        self.word = ""

    def __contains__(self, item):
        if self.find_word(item.lower()):
            return True
        return False

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


def load_dict(words="/usr/share/dict/words"):
    with open(words, 'r') as f:
        for line in f:
            if len(line) > 1:
                dict_tree.add_word(line.strip())
    dict_tree.add_word("a")

