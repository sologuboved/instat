# -*- coding: utf-8 -*-

import re
from json_operations import dump_json


MYDATA = 'myrawdata.txt'
MYDATA25 = 'myrawdata25.txt'
INSTAURLS = 'instaurls.json'
INSTAGRAM = 'https://www.instagram.com'


def process(fname, border=None):
    with open(fname, encoding="utf-8") as handler1:
        big_str = ' '.join(handler1.readlines())
        postfixes = re.findall('a href="(.*?taken-by=thalassografia)', big_str)
        if not border:
            border = len(postfixes)
        return postfixes[: border]


def collect_urls(fname25, fname, prefix):
    postfixes = process(fname25, 25) + process(fname)
    return [prefix + postfix for postfix in postfixes]


def dump_urls(fname_urls, fname25, fname, prefix):
    dump_json(collect_urls(fname25, fname, prefix), fname_urls)


if __name__ == '__main__':
    pass
    # r = collect_urls(MYDATA25, MYDATA, INSTAGRAM)
    # print(r[-1])
    dump_urls(INSTAURLS, MYDATA25, MYDATA, INSTAGRAM)
