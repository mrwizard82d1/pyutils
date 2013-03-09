#!/bin/env python


"""Defines a source of words to be used in testing."""
import glob
import itertools
import random


class WordSource(object):
    """Models a source of words."""

    def __init__(self):
        lines = [l.rstrip('\n') for l
                 in open('latin_words.txt', 'rt').readlines()]
        latin_terms = itertools.islice(lines, 0, len(lines), 2)
        english_definitions = itertools.islice(lines,
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


def verb():
    """Calculate a random verb declension."""
    return random.randrange(6)


def noun():
    """Calculate a random (first or second) noun declension."""
    return [random.randrange(6), random.randrange(2)]


def noun3():
    """Calculate a random third noun declension."""
    return [random.randrange(3)] + noun()


if __name__ == '__main__':
    ws = WordSource()
    i = 0
    for latin, english in ws:
        i += 1
        print('%s\n%s' % (latin, english))
        if i >= 9:
            break
