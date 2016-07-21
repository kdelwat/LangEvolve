import random
from itertools import takewhile
from pprint import pprint
from itertools import combinations_with_replacement

import rules
from table import Table

VOWELS = Table('vowels.csv')
available_rules = [rules.sonorization, rules.degemination]

def get_substitutions(category):
    '''Given a category, e.g. V (vowel) or plosive, return a list of members.'''
    if category == 'V':
        return VOWELS.members()

def expand_rule(rule):
    '''Given the rule (target, replacement, environment), expands the rule into a
    list of rules where each environment contains no special instructions. For
    example, an environment '[V]_[V]' would be converted to the list 'a_a', 'o_o',
    etc. The following substitutions apply:
        * [x] [x]: all substitutions from x must be the same
        * (x) (x): all substitutions from x may be different.
    Only zero, one, or two substitutions may be made.'''
    target, replacement, env = rule

    # If there are no substitutions to make, the rule is fine as-is
    if '[' not in env and '(' not in env:
        return [rule]


    # Handle identical substitutions
    if '[' in env:
        # Isolate the required substitution
        category = env[env.find('[')+1:env.find(']')]

        # Make substitutions
        rules = []
        for substitution in get_substitutions(category):
            rule = (target, replacement, env.replace('[' + category + ']', substitution))
            rules.append(rule)

    # Handle non-identical substitutions
    else:
        # Isolate the required substitution
        category = env[env.find('(')+1:env.find(')')]

        # Get pairs of possible substitutions, e.g. ('a', 'b')
        substitution_pairs = combinations_with_replacement(get_substitutions(category), 2)

        # Make substitutions
        rules = []
        for pair in substitution_pairs:
            first, second = pair
            rule = (target, replacement, env.replace('(' + category + ')', first, 1).replace('(' + category + ')', second, 1))
            rules.append(rule)
            rule = (target, replacement, env.replace('(' + category + ')', second, 1).replace('(' + category + ')', first, 1))
            rules.append(rule)

    return rules

def apply_rule(word, rule):
    '''Applies rule in the form (target, replacement, environment) to the word.
    Environment is in the form of string like 'a_c', where the underscore is
    taken by the target and replacement.'''
    target, replacement, environment = rule

    # Create target and replacement strings
    target_string = environment.replace('_', target)
    replacement_string = environment.replace('_', replacement)

    # Handle environments involving the beginning and end of lines. Delete
    # special characters from replacement string that may be present in the
    # environment. This bit's really filthy, sorry.
    if replacement_string[0] == '^':
        replacement_string = replacement_string[1:]
        if word[:len(replacement_string)] == target_string[1:]:
            return replacement_string + word[len(replacement_string):]
        else:
            return word
    elif replacement_string[-1] == '$':
        replacement_string = replacement_string[:-1]
        if word[-len(replacement_string):] == target_string[:-1]:
            return word[:-len(replacement_string)] + replacement_string
        else:
            return word
    # Otherwise, handle standard substitutions. Much nicer.
    else:
        return word.replace(target_string, replacement_string)

def step(inventory, word_list):
    '''Given a phonetic inventory and a list of words, apply one step of evolution
    and return the inventory and word list.'''

    # Apply a random change to the inventory until it's deemed valid
    random_rule = random.choice(available_rules)
    valid, rule_list, representation = random_rule(inventory)

    while not valid:
        random_rule = random.choice(available_rules)
        valid, rule_list, representation = random_rule(inventory)

    # Delete the change so it isn't used again
    available_rules.remove(random_rule)

    # Create a list to hold every fully-expanded rule
    all_rules = []
    for rule in rule_list:
        all_rules.extend(expand_rule(rule))

    # Apply all rules to all words
    modified_words = []
    for word in word_list:
        for rule in all_rules:
            word = apply_rule(word, rule)
        modified_words.append(word)

    print(representation)
    return inventory, modified_words

def main():
    #rules = load_rules('rules.txt')
    inventory = Table('pulmonicinventory.csv')
    words = ['ppotato', 'paraddʰise']
    print(words)

    while len(available_rules) > 0:
        inventory, words = step(inventory, words)
        print(inventory, words)
        print('')

if __name__ == '__main__':
    main()

