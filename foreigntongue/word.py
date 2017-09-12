''' An object representing data about a word '''
import random
from foreigntongue.pos import pos_lookup

class Word(object):
    ''' a foreign word and its metadata '''

    def __init__(self, pos, syllables, translation, base_tags=None):
        self.pos = pos
        self.display_pos = pos_lookup['LOC']

        # (hopefully) unique identifier
        self.id = random.randint(100000000, 999999999)

        # grammatical tags that ALWAYS apply to this word, ie pos and gender
        self.base_tags = [pos] + base_tags if base_tags else [pos]

        # this is the baseline list of syllables before any inflection
        self.stem = syllables

        # we can't tell what the word actually looks like without grammar
        self.lemma = None

        # equivalent translation word, if available
        self.translation = translation


    def set_lemma(self, rules):
        ''' return or create the lemma for this word '''
        self.lemma = self.inflect(rules)


    def inflect(self, rules, additional_tags=None):
        ''' perform inflection '''
        tags = self.base_tags
        if additional_tags:
            tags += additional_tags

        syllables = self.stem
        for rule in rules:
            # the Rule class handles whether a rule should be applied
            syllables = rule.apply(syllables, tags)

        return syllables
