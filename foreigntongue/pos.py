''' These parts of speech are based on Penn treebank:
https://ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
I've modified it -- for example, 'LOC' for location names, and
switched comparative and supurlative forms of adjectives and adverbs
to tags.
The names here are meant to be what you might find in a dictionary
aimed at the casual reader, rather than a linguist, so they elide
some of the nuances.
'''
pos_lookup = {
    'CC': 'conjunction', # coordinated conjunction
    'CD': 'noun',        # cardinal number
    'DT': 'determiner',  # here, a dictionary would be more specific
    'IN': 'preposition',
    'JJ': 'adjective',
    'MD': 'auxiliary verb', # modal
    'NN': 'noun',
    'NNP': 'noun',
    'PRP': 'pronoun',
    'RB': 'adverb',
    'RP': 'particle',
    'VB': 'verb',
    'WDT': 'pronoun', # wh-determiner
    'LOC': 'noun',
}

pos_list = list(pos_lookup.keys())

