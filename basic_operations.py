import json
from math import sqrt


def load_json(json_file):
    with open(json_file) as data:
        return json.load(data)


def dump_json(entries, json_file):
    with open(json_file, 'w') as handler:
        json.dump(entries, handler)


def find_mean(vals):
    return sum(vals) / float(len(vals))


def find_variance(vals):
    return sum([(val - find_mean(vals)) ** 2 for val in vals]) / len(vals)


def find_sd(vals):
    return sqrt(find_variance(vals))
