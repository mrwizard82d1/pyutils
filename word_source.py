#!/bin/env python


"""Defines a source of words to be used in testing."""

import argparse
import itertools
import os
import random


class WordSource(object):
    """Models a source of words."""

    def __init__(self, src_dir='.'):
        source_file_name = os.path.join(src_dir, 'latin_words.txt')
        lines = [l.rstrip('\n') for l
                 in open(source_file_name, 'rt').readlines()]
        latin_terms = []
        english_definitions = []
        line_no = 0
        while line_no < len(lines):
            if ':' in lines[line_no]:
                latin_terms.append(lines[line_no])
                line_no += 1
            else:
                english_definition = lines[line_no]
                line_no += 1
                while line_no < len(lines) and ':' not in lines[line_no]:
                    english_definition += ' ' + lines[line_no].lstrip()
                    line_no += 1
                english_definitions.append(' ' + english_definition)

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
    return [random.randrange(3), random.randrange(6)]


def noun():
    """Calculate a random (first or second) noun declension."""
    return [random.randrange(5), random.randrange(2)]


def noun3():
    """Calculate a random third noun declension."""
    return [random.randrange(3)] + noun()


def adj():
    """Calculate a random 1st and 2nd adjective declension."""
    return [random.randrange(3), random.randrange(6), random.randrange(2)]


def adj31():
    """Calculate a random 3rd adjective declension (one or two endings)."""
    return [random.randrange(2), random.randrange(6), random.randrange(2)]


def adj33():
    """Calculate a random 3rd adjective declension (two endings)."""
    return [random.randrange(3), random.randrange(6), random.randrange(2)]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate random words (for testing).',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('src_dir', nargs='?', default='.',
                        help=('Source directory (to search for'
                              ' latin_words.txt files)'))

    args = parser.parse_args()
    ws = WordSource(args.src_dir)
    i = 0
    for latin, english in ws:
        i += 1
        print('%s\n%s' % (latin, english))
        if i >= 9:
            break
