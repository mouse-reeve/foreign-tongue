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

        # this selects phonemes and syllable formation patterns
        self.syllables = Syllables()

        # -------- MORPHOLOGY
        ''' Not going to worry about analytic/synthetic/etc terminology, instead
        I'm going to view the mophological typology as two scales:

        inflection <----- vs ---> isolation   (morpheme per word ratio)
        agglutination <-- or ---> fusion      (feature per inflection ratio)
        inflection: redest. Isolation: most red.

        the first scale determines how many morphemes go into a word, and the
        second determines how to combine those morphemes (if at all, of course).

        This gets hard because the concept of a "word" gets mushy in translation
        and you end up with people flipping out about someone having one hundred
        words for snow.

        So, Russian would be more inflection and fusional. The list of things it
        codes for nouns is gender, number, and case.
        '''

        # ------- WORDS FROM SYLLABLES
        ''' NOTES:
         - The idea is to produce base forms that will be modified with the
           correct endings based on part of speech
        '''
        self.syllable_stats = {
            'syllables_mode': random.randint(2, 3),
            'syllables_stdv': random.random() / 3
        }


        # -------- INFLECTION
        ''' NOTES:
         - Number is, in reality, more complicated than just singular/plural,
           so a better model would maybe have buckets, or flexible benchmarks
            See also Greenberg's 34th rule of morphology
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
    def get_word(self, pos, translation, definition=None):
        ''' combine syllables into words
        NOTES:
        - some PoSs should probably prefer shorter words.
        - doesn't consider portmanteau, blendwords, compounding, &c
        - assumes that the string concatenation of translation and pos is unique
        '''

        # check if the word already exists
        if translation+pos in self.dictionary:
            return self.dictionary[translation+pos]

        pos = pos if pos else random.choice(pos_list)
        tags = [pos]

        # doesn't consider appropriateness of word length for the POS
        syllables = int(random.normalvariate(
            self.syllable_stats['syllables_mode'],
            self.syllable_stats['syllables_stdv']))
        syllables = 1 if syllables < 1 else syllables

        data = [self.syllables.get_syllable() for _ in range(0, syllables)]

        # create provisional word before rules are applied
        word_data = Word(
            pos,
            data,
            translation,
            base_tags=tags,
            definition=definition
        )

        # inflect word based on its part of speech
        word_data.set_lemma(self.rules)

        self.dictionary[translation+pos] = word_data
        return word_data


    def get_phrase(self, pos, words, translation):
        ''' A constituent phrase with a distinct meaning or translation,
        such as a place name like "Los Gatos" '''
        if len(words) < 2:
            raise IndexError('Phrases must be made of 2 or more words')

        syllables = words[0].lemma
        for word in words[1:]:
            syllables += self.space + word.lemma

        phrase = Word(
            pos,
            syllables,
            translation
        )
        phrase.set_lemma(self.rules)

        self.dictionary[translation+pos] = phrase
        return phrase


    def about(self):
        ''' print out some info about this language '''
        vowels = self.syllables.vowels
        consonants = self.syllables.consonants
        print('ABOUT THIS LANGUAGE\n' \
              'Vowels:                  %s\n' \
              'Consonants:              %s\n' \
              'Ave. syllables per word: %s' %
              (len(vowels), len(consonants),
               self.syllable_stats['syllables_mode']))

        print('\nVOWELS:')
        print(' '.join(re.sub('/', '', v['IPA']) for v in vowels))
        print(' '.join(re.sub('/', '', v['latin']) for v in vowels))

        print('CONSONANTS:')
        print(' '.join(re.sub('/', '', v['IPA']) for v in consonants))
        print(' '.join(re.sub('/', '', v['latin']) for v in consonants))

        print('\nGRAMMAR:')
        for rule in self.rules:
            print(rule.tags, rule)


    def get_stats(self):
        ''' json formatted info on the language '''
        return {
            'vowels': self.syllables.vowels,
            'consonants': self.syllables.consonants,
            'mode_syllables': self.syllable_stats['syllables_mode']
        }

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

