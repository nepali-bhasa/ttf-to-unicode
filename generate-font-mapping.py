#!/usr/bin/python3

from fontTools.ttLib import TTFont
import yaml
import sys
from collections import OrderedDict


def represent_dictionary_order(self, dict_data):
    return self.represent_mapping('tag:yaml.org,2002:map', dict_data.items())


def setup_yaml():
    yaml.add_representer(OrderedDict, represent_dictionary_order)


setup_yaml()


def is_character_valid(char):
    order = ord(char)
    return 31 < order < 127 or order > 159


def get_font_characters(name, input_file, output_file):
    with TTFont(input_file) as font:
        mapping = [
            chr(y[0])
            for x in font["cmap"].tables
            for y in x.cmap.items()
        ]

        characters = {
            x: ''
            for x in mapping
            if is_character_valid(x)
        }

    with open(output_file, 'w', encoding='utf-8') as file:
        yml = OrderedDict()
        yml['name'] = name
        yml['v'] = '1.0.1'
        yml['charmap'] = characters

        yaml.dump(yml, file, allow_unicode=True)


def main():
    if len(sys.argv) < 4:
        print('Font name, source, destination must be specified')
        return 1

    name = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    get_font_characters(name, input_file, output_file)


if __name__ == '__main__':
    main()
