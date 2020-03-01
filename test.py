import unittest
import glob
import os

import ttf2utf


def readLine(line):
    splitted_line = line.rstrip('\r\n').split('\t')
    return splitted_line


class TestVectors(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName=methodName)
        self.all_rules = ttf2utf.load_rules('rules/')

    def test(self):
        for filename in glob.glob('vectors/*.vector'):
            key = os.path.splitext(os.path.basename(filename))[0].lower()
            rule = self.all_rules[key]
            with open(filename, encoding='utf-8') as vector_file:
                print('Testing', key)
                for line in vector_file:
                    vec = readLine(line)
                    converted = ttf2utf.convert_word(vec[0], rule)
                    self.assertEqual(
                        converted,
                        vec[1],
                        'got {0} expected {1} for {2} in {3}'
                        .format(converted, vec[1], vec[0], filename)
                    )


if __name__ == "__main__":
    unittest.main()

