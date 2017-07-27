''' general logic for inflecting words '''
from foreigntongue.syllable import is_vowel

class Rule(object):
    ''' Abstract class for an inflection rule
    This modifies a word based on a selection of applicable
    grammatical and lexical categories.
    '''

    def __init__(self, tags):
        ''' the list of POS and grammatical tags that must all be present to
        apply this rule. For example:
         - to get the plural of "cat," the list of tags is ['NN', 'Pl']
         - to get the past tense of "run," the tag list is ['VB', 'Past']
        Grammatical tags can be whatever the language might choose to inflect
        on, your imagination is the limit, I guess.
        '''
        self.tags = tags


    def apply(self, syllables, tags):
        ''' apply a rule by modifying word syllables if the tags match '''
        if not self.is_tag_match(tags):
            return syllables

        return self.rule(syllables)


    def is_tag_match(self, tags):
        ''' This checks is the tags that define how this particular word
        should be inflected fit the pattern of this rule. For example:
        Say the rule matches plural nouns;
         - If the word should be plural, feminine, and a noun then YES
         - If the word should be a plural adjective, then NO '''

        unmatched = [t for t in self.tags if t not in tags]
        return not len(unmatched) or not tags

    def rule(self, word):
        ''' implemented by whatever rule type '''
        raise NotImplementedError('Rule functionality must be implemented')


class StemChange(Rule):
    ''' a stem change rule '''
    def __init__(self, tags, syllable_index, replacement):
        Rule.__init__(self, tags)
        self.syllable_index = syllable_index
        self.replacement = replacement

    def rule(self, syllables):
        ''' change a vowel in a syllable '''
        for (letter_index, letter) in enumerate(syllables[self.syllable_index]):
            if is_vowel(letter):
                syllables[self.syllable_index][letter_index] = self.replacement
        return syllables


class Affix(Rule):
    ''' modify a word by appending a syllable '''
    def __init__(self, tags, affix_syllable):
        Rule.__init__(self, tags)
        self.affix = affix_syllable

    def rule(self, syllables):
        ''' change a vowel in a syllable '''
        return syllables + [self.affix]


class Prefix(Rule):
    ''' prepend a syllable '''
    def __init__(self, tags, prefix_syllable):
        Rule.__init__(self, tags)
        self.prefix = prefix_syllable

    def rule(self, syllables):
        ''' change a vowel in a syllable '''
        return [self.prefix] + syllables
