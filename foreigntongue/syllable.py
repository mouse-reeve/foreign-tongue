''' create syllables out of phonemes and probabalistic structure '''
from foreigntongue.phonemes import vowels as ipa_vowels, consonants as ipa_consonants
import random

class Syllables(object):
    ''' Generate syllables that fit a language pattern '''

    def __init__(self):
        # -------  PICK LETTERS
        ''' Notes:
         - Only uses pulmonic consonants. 27% of langauges contain nonpulmonic
           consontants
         - Phonemes are selected randomly, when in reality there are patterns
           to which phonemes can coexist in a language (see, allophony)
         - How many phonemes should there be? It varies widely, see
        en.wikipedia.org/wiki/Phoneme#Numbers_of_phonemes_in_different_languages
           The distribution mean/standard devs here are based on the counts from
           http://wals.info/chapter/1 and http://wals.info/chapter/2
         - Some phonemes are more common across langs, that is not considered
           here
         '''

        # a phone looks like ['/m/', ['/m/']] -> [IPA, [transcription choices]]
        v_count = int(random.normalvariate(5, 1)) or 2
        while 2 > v_count > len(ipa_vowels) - 2:
            v_count = int(random.normalvariate(5, 1)) or 2
        vowels = random.sample(ipa_vowels, v_count)

        c_count = int(random.normalvariate(22, 3)) or 3
        while 3 > c_count > len(ipa_consonants) - 3:
            c_count = int(random.normalvariate(22, 3)) or 3
        consonants = random.sample(ipa_consonants, c_count)

        # assign them frequencies
        ''' Notes:
         - There are different frequencies depending on where in a word a
           phoneme is used. This is not considered here.
         - Zipf's law is used to determine frequency, rank is determined by a
           random.sample function below.
        '''
        # Zipf's law, or frequency = constant / rank
        frequency = lambda rank: float(v_count + c_count) / rank

        # list of all letters
        letters = random.sample(vowels + consonants, v_count + c_count)
        letters = [{'IPA': l[0], 'latin': l[1], 'freq': frequency(i + 1)} \
                        for i, l in enumerate(letters)]

        # vary up the orthography for similar phonemes
        graphemes = []
        for letter in letters:
            choices = letter['latin']
            success = False
            for choice in choices:
                if choice in graphemes:
                    continue
                letter['latin'] = choice
                graphemes.append(choice)
                success = True
                break
            if not success:
                letter['latin'] = letter['latin'][0]

        # re-create the vowel and consonant list with the new data format
        vowels = [v[0] for v in vowels]
        consonants = [c[0] for c in consonants]

        self.vowels = [l for l in letters if l['IPA'] in vowels]
        self.consonants = [l for l in letters if l['IPA'] in consonants]

        ''' this allows words to join into phrases without having to remember
        the non-obvious format in which letters are stored. '''

        # ------- DEFINE SYLLABLES
        ''' Notes:
         - The onset (initial consonants) can be obligatory, optional, or
           restricted
         - The nucleus (middle vowels) are obligatory
         - The coda (terminal consonants) can be obligatory, optional, or
           restricted
         - This isn't considering consonant clusters or diphthongs
         - the obligation settings mean you are more likely to have a coda than
           an onset
        '''
        def syllable_frequency_calculator(obligatory=False):
            ''' determine if a coda or onset is used and if so how '''
            # obligatory, optional, or restricted, weighted against restricted
            option = random.choice([0, 1, 1, 2, 2])
            if not obligatory and option < 2:
                return option
            else:
                # the frequency at which it is used, if optional
                freq = random.normalvariate(0.7, 0.12)
                if freq <= 0:
                    return 0.1
                elif freq >= 1:
                    return 0.99
                return freq

        self.onset_frequency = syllable_frequency_calculator()
        # obligatory if there is no onset, otherwise we never got consonants
        self.coda_frequency = syllable_frequency_calculator(
            obligatory=(not self.onset_frequency))


    def get_syllable(self):
        ''' form a syllable based on defined frequencies '''
        syllable = []
        #onset
        if random.random() < self.onset_frequency:
            syllable.append(self.pick_consonant())
        # nucleus
        syllable.append(self.pick_vowel())
        #coda
        if random.random() < self.coda_frequency:
            syllable.append(self.pick_consonant())
        return syllable


    def pick_vowel(self):
        ''' select from the phonology of this language '''
        return pick_letter(self.vowels)


    def pick_consonant(self):
        ''' select from the phonology of this language '''
        return pick_letter(self.consonants)


all_vowels = [vo[0] for vo in ipa_vowels]
def is_vowel(phoneme):
    ''' check if a phoneme is a vowel. Could be written in
    a more efficient way for sure '''
    return phoneme['IPA'] in all_vowels


def pick_letter(letter_set):
    ''' weighted random choice '''
    total_weight = sum(l['freq'] for l in letter_set)
    r = random.uniform(0, total_weight)
    upto = 0
    for letter in letter_set:
        if upto + letter['freq'] >= r:
            return letter
        upto += letter['freq']

