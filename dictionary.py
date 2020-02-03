from pygtrie import StringTrie  # type: ignore

dictionary = StringTrie()

with open("words.txt") as words:
    for word in words.read().splitlines():
        if word:
            dictionary[word] = word
