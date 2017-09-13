''' test language creation '''
from foreigntongue import Language, Syllables, Word#, get_latin, get_ipa
from foreigntongue.inflection import Rule, Affix, Prefix, StemChange
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

        self.assertEqual(len(lang.dictionary), 2)


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


    def test_auto_create_rules(self):
        ''' inflection rules '''
        lang = Language()
        rules = lang.rules

        # there should at least be a pluralization rule
        self.assertTrue(len(rules) > 0)

        for rule in rules:
            self.assertIsInstance(rule, Rule)
            self.assertIsInstance(rule.tags, list)
            self.assertTrue(len(rule.tags) > 0)


    def test_abstract_rule_class(self):
        ''' rule class template for rule types '''
        with self.assertRaises(NotImplementedError):
            rule = Rule(['NN'])
            rule.rule([])


    def test_affix_rule(self):
        ''' adding a syllable to the end '''
        lang = Language()
        syllable = lang.syllables.get_syllable()
        rule = Affix(['NN'], syllable)
        self.assertIsInstance(rule, Rule)

        word = lang.get_word('NN', 'bip')
        inflected = rule.apply(word.stem, word.base_tags)

        self.assertEqual(len(word.stem) + 1, len(inflected))
        self.assertEqual(word.stem, inflected[:-1])
        self.assertEqual(inflected[-1], syllable)


    def test_prefix_rule(self):
        ''' adding a syllable to the start '''
        lang = Language()
        syllable = lang.syllables.get_syllable()
        rule = Prefix(['NN'], syllable)
        self.assertIsInstance(rule, Rule)

        word = lang.get_word('NN', 'bip')
        inflected = rule.apply(word.stem, word.base_tags)

        self.assertEqual(len(word.stem) + 1, len(inflected))
        self.assertEqual(word.stem, inflected[1:])
        self.assertEqual(inflected[0], syllable)


    def test_stem_change_rule(self):
        ''' modify the vowel in a syllable '''
        lang = Language()
        vowel = {'latin': 'ME', 'ipa': 'mua'}
        rule = StemChange(['NN'], 0, vowel)
        self.assertIsInstance(rule, Rule)

        word = lang.get_word('NN', 'bip')
        inflected = rule.apply(word.stem, word.base_tags)

        self.assertEqual(len(word.stem), len(inflected))
        self.assertEqual(word.stem[1:], inflected[1:])
        self.assertIn(vowel, inflected[0])


if __name__ == '__main__':
    unittest.main()
