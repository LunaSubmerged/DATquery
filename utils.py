from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def fuzzySearch(value, dictionary):
    value = value.lower()
    if value in dictionary:
        return dictionary[value]
    fuzzy = process.extract(value, dictionary.keys(), limit = 1)
    fuzzyName = fuzzy[0][0]
    if fuzzyName in dictionary:
        return dictionary[fuzzyName]