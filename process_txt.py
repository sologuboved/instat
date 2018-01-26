# -*- coding: utf-8 -*-

import re


def process(fname, border=None):
    with open(fname, encoding="utf-8") as handler1:
        big_str = ' '.join(handler1.readlines())
        postfixes = re.findall('a href="(.*?taken-by=thalassografia)', big_str)
        if not border:
            border = len(postfixes)
        return postfixes[: border]


def collect_urls(fname25, fname, prefix):
    postfixes = process(fname25, 25) + process(fname)
    print(postfixes[0])
    return [prefix + postfix for postfix in postfixes]


if __name__ == '__main__':
    r = collect_urls('myrawdata25.txt', 'myrawdata.txt', 'https://www.instagram.com')
    print(r[-1])
