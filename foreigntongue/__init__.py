''' Create a language '''
from foreigntongue.syllable import Syllables
from foreigntongue.pos import pos_list
from foreigntongue.inflection import StemChange, Affix, Prefix
from foreigntongue.word import Word
import random
import re

class Language(object):
    ''' initialize a language '''
    space = [[{'IPA': ' ', 'latin': ' ', 'freq': 0}]]

    def __init__(self):
        self.dictionary = {}
        # this will just be a list of all created words, unkeyed
        self.dictionary_list = []

        # this selects phonemes and syllable formation patterns
        self.syllables = Syllables()

        # ------- WORDS FROM SYLLABLES
        ''' NOTES:
         - The idea is to produce base forms that will be modified with the
           correct endings based on part of speech
         - This is ludicrously simplified, it doesn't consider morphology
           at all, much less bound vs free or whatever else, and like, what
           about agglutination or concatenation???
         - Also doesn't consider word relationships and etymology
        '''
        self.syllable_stats = {
            'word_syllable_mode': random.randint(1, 2),
            'word_syllable_stdv': random.random() / 3
        }


        # -------- INFLECTION
        ''' NOTES:
         - Number is, in reality, more complicated than just singular/plural,
           so a better model would maybe have buckets, or flexible benchmarks
         - PoS uses a subset of Penn Treebank, and is very simplistic
         - Grammatical gender could also mark other characteristics like
           (in)animate, or, for that matter, any number of other offbeat things
        '''

        self.rules = []

        def create_rule(tags, rule_type=None):
            ''' generate an inflection rule to apply to a given tag set. NOTES:
            - stem change vs affix should be part of the whole conversation
              about grammar and morphology, instead of a random boolean '''

            if rule_type == 'affix' or random.random() > 0.5:
                ending = self.syllables.get_syllable()
                # prefer to append endings rather than prepend
                if random.choice([0, 1, 1]):
                    rule = Affix(tags, ending)
                else:
                    rule = Prefix(tags, ending)
            else:
                replacement = self.syllables.pick_vowel()
                rule = StemChange(tags, -1, replacement)

            self.rules.append(rule)

        for tag in pos_list:
            # apply endings to ~half of POSs, excluding proper nouns,
            # because they make names too confusing
            if random.randint(0, 1) and tag != 'NNP':
                continue
            create_rule([tag])

        # Plurals
        ''' plurals could also theoretically apply to adjectives, and
        number can matter with verbs, et cetera, so this is very
        anglocentric, and isn't considering how morphology works.'''
        plurals = ['singular', 'plural']
        if random.random() > 0.8:
            plurals.append('plural2')
            if random.random() > 0.6:
                plurals.append('plural3')
        for plural in plurals:
            create_rule(['NN', plural])

        # Verb tense
        ''' Notes:
         - A language usually has past, present, and future, but it can also
           have just past + present (really, past and non-past) or just present +
           future (really non-future and future).
         - That means baseline combos are [past, present, future]
                                          [past, present        ]
                                          [      present, future]
         - Tenseless lanagues are not considered here.
         - Here, tenses are only applied through endings, which is a very
           English-centric take - languages can mark this with additional words
           or stem modification
         - This system means that verbs given without tense will not be in the
           same form as present tense
         - No account is taken here for pronoun accompanying the verb, which is
           not ideal
         '''

        tenses = ['present']
        if random.randint(0, 20):
            tenses.append('past')
            if random.randint(0, 20):
                tenses.append('future')
        else:
            tenses.append('future')

        for tense in tenses:
            create_rule(['VB', tense])


    # -------- GENERATORS
    def get_word(self, pos=None, english=None, definition=None):
        ''' combine syllables into words
        if no part of speech is provided, one is picked at random,
        which does not consider frequency of different parts of speech.
        This also doesn't consider that some PoSs should probably
        prefer shorter words.

        This function creates the dictionary form of the word, and then
        (at least in theory) produces the full set of lexemes based on
        the generated inflection rules.
        '''

        # check if the word already exists
        if pos and english and english+pos in self.dictionary:
            return self.dictionary[english+pos]

        pos = pos if pos else random.choice(pos_list)
        tags = [pos]

        # doesn't consider appropriateness of word length for the POS
        syllables = int(random.normalvariate(
            self.syllable_stats['word_syllable_mode'],
            self.syllable_stats['word_syllable_stdv']))
        syllables = 1 if syllables < 1 else syllables

        data = [self.syllables.get_syllable() for _ in range(0, syllables)]

        # create provisional word before rules are applied
        word_data = Word(
            pos,
            data,
            base_tags=tags,
            english=english,
            definition=definition
        )

        # inflect word based on its part of speech
        word_data.set_lemma(self.rules)

        # location names and proper nouns won't necessarily have
        # unique english equivalents, so they aren't
        # added to the keyed dictionary, but they do need
        # entries in the html.
        if english and not pos in ['NNP', 'LOC']:
            # it seems janky to maintain these in parallel, but they
            # won't have exactly the same content
            # using the definition/translation as a key means that
            # english homonyms or words with multiple POSs are merged
            self.dictionary[english+pos] = word_data
        self.dictionary_list.append(word_data)
        return word_data


    def get_placename(self, definition=None):
        ''' a special case word generator for place names.
        This allows for names with literal translations, in the form of:
        adjective + noun (Swarming Bees),
        or just a word
        '''
        if random.random() > 0.25:
            # normal name
            return self.get_word(pos='LOC', definition=definition)
        else:
            ''' Note: this is assuming the language uses a adj+noun
            pattern, which there's no real reason to think '''
            # TODO: this is no wordlist
            english_adj = random.choice(['swarming', 'sleeping', 'many'])
            english_noun = random.choice(['bees', 'wasps', 'locust', 'rats'])

            adj = self.get_word(pos='JJ', english=english_adj)
            noun = self.get_word(pos='NN', english=english_noun)
            # this applies any location rules to the phrase
            definition += '; ' if definition else ''
            definition += 'literally "%s %s"' % (english_adj, english_noun)

            name = Word(
                'LOC',
                adj.lemma + self.space + noun.lemma,
                definition=definition
            )
            name.set_lemma(self.rules)

            self.dictionary_list.append(name)
            return name


    def about(self):
        ''' print out some info about this language '''
        vowels = self.syllables.vowels
        consonants = self.syllables.consonants
        print('ABOUT THIS LANGUAGE\n' \
              'Vowels:                  %s\n' \
              'Consonants:              %s\n' \
              'Ave. syllables per word: %s' %
              (len(vowels), len(consonants),
               self.syllable_stats['word_syllable_mode']))

        print('\nVOWELS:')
        print(' '.join(re.sub('/', '', v['IPA']) for v in vowels))
        print(' '.join(re.sub('/', '', v['latin']) for v in vowels))

        print('CONSONANTS:')
        print(' '.join(re.sub('/', '', v['IPA']) for v in consonants))
        print(' '.join(re.sub('/', '', v['latin']) for v in consonants))

        print('\nGRAMMAR:')
        for rule in self.rules:
            print(rule.tags, rule)

# ------ PRINTERS
def get_latin(word):
    ''' pick out the latin transcription '''
    text = ''
    for syllable in word.lemma:
        text = text + ''.join(l['latin'] for l in syllable)

    return re.sub('/', '', text)

def get_ipa(word):
    ''' pick out the latin transcription '''
    text = ''
    for syllable in word.lemma:
        text = text + ''.join(l['IPA'] for l in syllable)
    return re.sub('/', '', text)

