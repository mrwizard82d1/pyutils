#!/bin/env python


"""Defines a source of words to be used in testing."""
import glob
import itertools
import random


class WordSource(object):
    """Models a source of words."""

    def __init__(self):
        lines = open('latin_words.txt', 'rt').readlines()
        latin_terms = itertools.islice(lines, 0, len(lines), 2)
        english_definitions = itertools.islice(lines[1:],
                                               1, len(lines), 2)
        self.latin_english_dict = \
            dict(list(itertools.izip(latin_terms, english_definitions)))
        self.latin_words = self.latin_english_dict.keys()

    def __iter__(self):
        """This class is an iterator."""
        return self

    def __next__(self):
        """Return the next item in the sequence."""
        return self.next()

    def next(self):
        """Return the next item in the sequence."""
        word_index = random.randrange(len(self.latin_english_dict))
        next_latin_word = self.latin_words[word_index]
        return next_latin_word, self.latin_english_dict[next_latin_word]


if __name__ == '__main__':
    ws = WordSource()
    i = 0
    for english, latin in ws:
        i += 1
        print('english: latin=%s: %s' % (english, latin))
        if i >= 9:
            break
