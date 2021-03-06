"""A Python library to check for (and clean) profanity in strings.

"""

import os
import random
import re
import settings

lines = None
words = None
_censor_chars = '@#$%!'
_censor_pool = []


def get_words():
    if not words:
        try:
            load_words(settings.word_list, None)
        except AttributeError:
            try:
                load_words(None, settings.text_file)
            except AttributeError:
                print "no word source specified in settings.py"
                return None
    return words


def get_censor_char():
    """Plucks a letter out of the censor_pool. If the censor_pool is empty,
    replenishes it. This is done to ensure all censor chars are used before
    grabbing more (avoids ugly duplicates).

    """
    global _censor_pool
    if not _censor_pool:
        # censor pool is empty. fill it back up.
        _censor_pool = list(_censor_chars)
    return _censor_pool.pop(random.randrange(len(_censor_pool)))


def set_censor_characters(censor_chars):
    """Sets the pool of censor characters. Input should be a single string
    containing all the censor characters you'd like to use.
    Example: "@#$%^"

    """
    global _censor_chars
    _censor_chars = censor_chars


def contains_profanity(input_text):
    """Checks the input_text for any profanity and returns True if it does.
    Otherwise, returns False.
    """
    return input_text != censor(input_text)


def censor(input_text):
    """ Returns the input string with profanity replaced with a random string
    of characters plucked from the censor_characters pool.

    """
    ret = input_text
    words = get_words()
    for word in words:
        curse_word = re.compile(re.escape(word), re.IGNORECASE)
        cen = "".join(get_censor_char() for i in list(word))
        ret = curse_word.sub(cen, ret)
    return ret


def load_words(wordlist=None, text_file=None):
    """ Loads and caches the profanity word list. Input file (if provided)
    should be a flat text file with one profanity entry per line.

    """
    global words
    if not wordlist and text_file:
        # no wordlist was provided, load the wordlist from the local store
        f = open(text_file)
        wordlist = f.readlines()
        wordlist = [w.strip() for w in wordlist if w]
        if not wordlist:
            print "Unsuccessful loading word list. Check that text file is a flat file with one word per line."
            return None
    words = wordlist
    return True

def contains_profanity_re(input_text):
    """ Checks for profanity using regex string and returns True if profanity
        is present, False otherwise.
    """
    try:
        blockwords = settings.blockwords_re
    except AttributeError:
        print "Set a value for blockwords_re in settings.py"
        return None
    else:
        return len(re.findall(blockwords, input_text, flags=re.IGNORECASE)) > 0
