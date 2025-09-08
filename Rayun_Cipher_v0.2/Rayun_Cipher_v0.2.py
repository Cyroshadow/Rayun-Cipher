import string
import os
import random

def get_Elements(upCharQuery = True, lowCharQuery = True, symQuery = True, whispaQuery = True, numQuery = True):
    cipherElements = []
    alphUp = list(string.ascii_uppercase)
    alphLow = list(string.ascii_lowercase)
    numbers = list(string.digits)
    whitespace = list(string.whitespace)
    symbols = list(string.punctuation)

    if (upCharQuery):
        cipherElements.extend(alphUp)
    if (lowCharQuery):
        cipherElements.extend(alphLow)
    if (symQuery):
        cipherElements.extend(symbols)
    if (whispaQuery):
        cipherElements.extend(whitespace)
    if (numQuery):
        cipherElements.extend(numbers)

    return cipherElements

def get_Table(elements):
    table = []
    row = []
    for i in range(len(elements)):
        row.extend(elements[i])
    print(table)

get_Table(get_Elements(False, False, True, False))


