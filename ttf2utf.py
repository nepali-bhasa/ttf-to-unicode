import re
import os
import yaml

DEFAULTS_FILE = 'defaults.yaml'


def _load_defaults(yaml_path):
    path = os.path.join(yaml_path, DEFAULTS_FILE)
    with open(path, encoding='utf-8') as infile:
        default = yaml.load(infile, Loader=yaml.FullLoader)
        default['pre-rules'] = [
            (re.compile(r[0]), r[1]) for r in default['pre-rules']
        ]
        default['post-rules'] = [
            (re.compile(r[0]), r[1]) for r in default['post-rules']
        ]
    return default


def load_rules(yaml_path):
    default = _load_defaults(yaml_path)

    files = [x for x in os.listdir(yaml_path) if x != DEFAULTS_FILE]
    paths = [os.path.join(yaml_path, x) for x in sorted(files)]
    paths = [x for x in paths if os.path.isfile(x)]

    all_rules = {}
    for path in paths:
        with open(path, encoding='utf-8') as infile:
            rule = yaml.load(infile, Loader=yaml.FullLoader)
            rule['post-rules'] = default['post-rules']
            rule['pre-rules'] = default['pre-rules']

            rule_key = re.sub(r'\s+', '_', rule['name'].lower())
            all_rules[rule_key] = rule
    return all_rules


def convert_word(word, rule, debugRuleIndex=None):
    utf_word = word
    for rulez in rule['pre-rules']:
        utf_word = re.sub(rulez[0], rulez[1], utf_word)

    utf_word = ''.join([
        rule['char-map'].get(c, c) for c in utf_word
    ])

    for i, rulez in enumerate(rule['post-rules']):
        old_word = utf_word
        utf_word = re.sub(rulez[0], rulez[1], utf_word)
        if debugRuleIndex and i == debugRuleIndex:
            print(old_word, '->', utf_word)

    return utf_word
