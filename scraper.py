import re
import requests
from bs4 import BeautifulSoup
from json_operations import *
from process_txt import collect_urls


MYDATA = 'myrawdata.txt'
MYDATA25 = 'myrawdata25.txt'
INSTAURLS = 'instaurls.json'
MYDATA_JSON = 'mydata.json'
INSTAGRAM = 'https://www.instagram.com'

LIKES = 'likes'
TAGS = 'tags'
DATE = 'date'


def dump_collection(json_fname, fname25, fname, prefix):
    dump_json(build_collection(fname25, fname, prefix), json_fname)


def build_collection(fname25, fname, prefix):
    collection = dict()
    try:
        urls = load_json(INSTAURLS)
    except FileNotFoundError as e:
        print(e)
        urls = collect_urls(fname25, fname, prefix)
    total = len(urls)
    ind = 1
    for url in urls:
        print("(%d of %d) %s" % (ind, total, url))
        collection[url] = scrape_page(url)
        ind += 1
    return collection


def scrape_page(page_url):
    page_html = requests.get(page_url).content
    str_soup = str(BeautifulSoup(page_html, 'lxml'))

    # print(str_soup)

    # <meta content="0 Likes, 1 Comments - Буратино (@thalassografia) on Instagram: “Собр. статей греческих
    # психоаналитиков о У.Р. Бионе #βιβλία #w_r_bion #ελληνικά_τώρα”" name="description"/>

    # <meta content="dusk" property="instapp:hashtags"/>

    # <meta content="Instagram post by Буратино • Jan 7, 2018 at 10:17am UTC" property="og:title"/>

    try:
        likes = re.findall('<meta content="(.*?) Likes', str_soup)[0]
        try:
            likes = int(likes)
        except (TypeError, ValueError):
            print_glitch("Likes rubric contains a non-int:", page_url)
    except IndexError:
        likes = None
        print_glitch("Likes rubric missing:", page_url)
    tags = re.findall('<meta content="(.*?)" property="instapp:hashtags"/>', str_soup)
    date = re.findall('<meta content="Instagram post by Буратино • (.*?) at (.*?)" property', str_soup)
    try:
        date = date[0]
        date = date[0] + ' ' + date[1]
    except IndexError:
        date = None
        print_glitch("Date rubric missing or disfigured:", page_url)
    return {LIKES: likes, TAGS: tags, DATE: date}


def print_glitch(text, page_url):
    print()
    print(text)
    print(page_url)
    print()


# def convert(json_fname):
#     collection = load_json(json_fname)
#     for url in collection:
#         item = collection[url]
#         item[LIKES] = int(item[LIKES])
#         item[DATE] = item[DATE][0] + ' ' + item[DATE][1]
#         print(item[DATE])
#     # dump_json(collection, json_fname)


if __name__ == '__main__':
    pass
    # scrape_page('https://www.instagram.com/p/BdpQMUFBf3b/?taken-by=thalassografia')
    dump_collection(MYDATA_JSON, MYDATA25, MYDATA, INSTAGRAM)
    # coll = load_json(MYDATA_JSON)
    # print(coll['https://www.instagram.com/p/7TNru4AwSX/?taken-by=thalassografia'])
    # print(len(coll))
    # convert(MYDATA_JSON)

