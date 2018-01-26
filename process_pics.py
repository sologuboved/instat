from bs4 import BeautifulSoup
import requests
import re
from process_txt import collect_urls
from json_operations import *


def dump_collection(json_fname, fname25, fname, prefix):
    dump_json(build_collection(fname25, fname, prefix), json_fname)


def build_collection(fname25, fname, prefix):
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
    likes = re.findall('<meta content="(.*?) Likes', str_soup)[0]
    tags = re.findall('<meta content="(.*?)" property="instapp:hashtags"/>', str_soup)
    date = re.findall('<meta content="Instagram post by Буратино • (.*?) at', str_soup)
    return {'likes': likes, 'tags': tags, 'date': date}


if __name__ == '__main__':
    # build_collection('myrawdata25.txt', 'myrawdata.txt', 'https://www.instagram.com')
    # scrape_page('https://www.instagram.com/p/BdpQMUFBf3b/?taken-by=thalassografia')
    dump_collection('mydata.json', 'myrawdata25.txt', 'myrawdata.txt', 'https://www.instagram.com')
