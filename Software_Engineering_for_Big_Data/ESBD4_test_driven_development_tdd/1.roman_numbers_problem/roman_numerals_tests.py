import unittest
from roman_numerals import roman_numerals

class testRomanNumerals(unittest.TestCase):
    def test_single_digit(self):
        self.assertEqual(roman_numerals('I'), 1)
        self.assertEqual(roman_numerals('V'), 5)
        self.assertEqual(roman_numerals('X'), 10)
        self.assertEqual(roman_numerals('L'), 50)
        self.assertEqual(roman_numerals('C'), 100)
        self.assertEqual(roman_numerals('D'), 500)
        self.assertEqual(roman_numerals('M'), 1000)

    def test_combined_digits(self):
        self.assertEqual(roman_numerals('II'), )
        self.assertEqual(roman_numerals('IV'), 4)
        self.assertEqual(roman_numerals('IIIX'), 8)
        self.assertEqual(roman_numerals('XL'), 40)
        self.assertEqual(roman_numerals('IXXL'), 49)
        self.assertEqual(roman_numerals('LI'), 51)
        self.assertEqual(roman_numerals('LX'), 60)
        self.assertEqual(roman_numerals('ICC'), 199)
        self.assertEqual(roman_numerals('DCXXV'), 625)
        self.assertEqual(roman_numerals('MMXXIII'), 2023)

if __name__ == '__main__':
    unittest.main()