''' test language creation '''
from foreigntongue import Language, Syllables, Word#, get_latin, get_ipa
import unittest

class Tests(unittest.TestCase):
    ''' are words? '''

    def test_create_language(self):
        ''' test that a language was created '''
        lang = Language()
        self.assertIsInstance(lang, Language)
        self.assertIsInstance(lang.syllables, Syllables)
        self.assertIsInstance(lang.dictionary, dict)

    def test_create_word(self):
        ''' words are useful '''
        lang = Language()

        # basic creation
        noun = lang.get_word('NN', 'fish')
        self.assertIsInstance(noun, Word)

        # should distinguish words based on POS
        verb = lang.get_word('VB', 'fish')

        # lookup existing words
        noun_lookup = lang.get_word('NN', 'fish')
        self.assertIs(noun, noun_lookup)

        verb_lookup = lang.get_word('VB', 'fish')
        self.assertIs(verb, verb_lookup)

        self.assertIsNot(noun, verb)


    def test_pos_tags(self):
        ''' part of speech tagging and display '''
        lang = Language()

        # standard pos
        noun = lang.get_word('NN', 'fish')
        self.assertEqual(noun.display_pos, 'noun')
        self.assertIsInstance(noun.base_tags, list)
        self.assertTrue(len(noun.base_tags) >= 1)

        verb = lang.get_word('VB', 'fish')
        self.assertEqual(verb.display_pos, 'verb')

        # nonstandard pos
        blerk = lang.get_word('BLRK', 'blork')
        self.assertEqual(blerk.display_pos, 'BLRK')


    def test_phonology(self):
        ''' sounds used in language '''
        lang = Language()
        syll = lang.syllables

        self.assertTrue(len(syll.vowels) >= 2)
        self.assertTrue(len(syll.consonants) >= 6)

        # make sure vowels and consonants actually are
        for _ in range(10):
            vowel = syll.pick_vowel()
            self.assertIn(vowel, syll.vowels)

            consonant = syll.pick_consonant()
            self.assertIn(consonant, syll.consonants)

        # make sure letters actually exist
        self.assertIsInstance(consonant, dict)
        self.assertIn('IPA', consonant)
        self.assertIn('latin', consonant)
        self.assertIsInstance(consonant['IPA'], str)
        self.assertIsInstance(consonant['latin'], str)


    def test_syllables(self):
        ''' sounds used in language '''
        lang = Language()
        syll = lang.syllables

        syllable = syll.get_syllable()
        self.assertIsInstance(syllable, list)
        self.assertTrue(len(syllable) > 0)

        self.assertIsInstance(syllable[0], dict)
        self.assertIn('IPA', syllable[0])
        self.assertIn('latin', syllable[0])
        self.assertIsInstance(syllable[0]['IPA'], str)
        self.assertIsInstance(syllable[0]['latin'], str)


if __name__ == '__main__':
    unittest.main()