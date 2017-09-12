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



if __name__ == '__main__':
    unittest.main()
