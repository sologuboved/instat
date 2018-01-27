import re
import requests
from bs4 import BeautifulSoup
from json_operations import *
from process_txt import collect_urls


MYDATA = 'myrawdata.txt'
MYDATA25 = 'myrawdata25.txt'
MYDATA_JSON = 'mydata.json'
INSTAGRAM = 'https://www.instagram.com'


def dump_collection(json_fname, fname25, fname, prefix):
    print("Dumping json...")
    dump_json(build_collection(fname25, fname, prefix), json_fname)


def build_collection(fname25, fname, prefix):
    print("Building collection...")
    collection = dict()
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
    except IndexError:
        likes = None
        print()
        print("Likes rubric missing:")
        print(page_url)
        print()
    tags = re.findall('<meta content="(.*?)" property="instapp:hashtags"/>', str_soup)
    date = re.findall('<meta content="Instagram post by Буратино • (.*?) at', str_soup)
    return {'likes': likes, 'tags': tags, 'date': date}


if __name__ == '__main__':
    pass
    # scrape_page('https://www.instagram.com/p/BdpQMUFBf3b/?taken-by=thalassografia')
    # dump_collection(MYDATA_JSON, MYDATA25, MYDATA, INSTAGRAM)
    # coll = load_json(MYDATA_JSON)
    # print(coll['https://www.instagram.com/p/7TNru4AwSX/?taken-by=thalassografia'])
    # print(len(coll))

