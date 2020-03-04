#!/usr/bin/python3

from argparse import ArgumentParser
from collections import OrderedDict

import yaml
from fontTools.ttLib import TTFont


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


def default_args():
    default_parser = ArgumentParser()
    default_parser.add_argument(
        "-f", "--font",
        help="Font Name",
        required=True
    )
    default_parser.add_argument(
        "-s", "--source",
        help="Font source file",
        required=True
    )
    default_parser.add_argument(
        "-d", "--destination",
        help="Destination mapping file",
        required=True
    )
    return default_parser.parse_args()


def main():
    parsed_args = default_args()
    name = parsed_args.font
    input_file = parsed_args.source
    output_file = parsed_args.destination
    get_font_characters(name, input_file, output_file)


if __name__ == '__main__':
    main()
