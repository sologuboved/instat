from datetime import datetime
from json_operations import *

MYDATA_JSON = 'mydata.json'
URL = 'url'
LIKES = 'likes'
TAGS = 'tags'
DATE = 'date'


class Collection(object):
    def __init__(self, json_fname):
        self.collection = list()
        self.tags = set()
        self.cook(json_fname)

    def cook(self, json_fname):
        collection = load_json(json_fname)
        for url in collection:
            item = collection[url]
            tags = item[TAGS]
            for tag in tags:
                self.tags.add(tag)
            date = datetime.strptime(item[DATE], "%b %d, %Y %I:%M%p %Z")
            self.collection.append({URL: url, LIKES: item[LIKES], TAGS: tags, DATE: date})

    def prettyprint(self):
        ind = 1
        for item in self.collection:
            print('<%d>' % ind)
            print('url:', item[URL])
            print('date:', item[DATE].strftime("%d %B %Y, %A %I:%M%p"))
            print('likes:', item[LIKES])
            print('tags:')
            for tag in item[TAGS]:
                print("         ", tag)
            print()
            ind += 1

    def find_tag_freqs(self):
        tag_freqs = dict.fromkeys(list(self.tags), 0)
        for item in self.collection:
            for tag in item[TAGS]:
                tag_freqs[tag] += 1
        for freq in sorted(tag_freqs.items(), key=lambda i: i[1], reverse=True):
            print(freq[0] + ':', freq[1])

    def sort_by_likes(self):
        self.collection.sort(key=lambda i: i[LIKES], reverse=True)
        self.prettyprint()

    def find_dayofweek_stat(self):
        dow = {'Mon': [0, 0], 'Tue': [0, 0], 'Wed': [0, 0], 'Thu': [0, 0], 'Fri': [0, 0], 'Sat': [0, 0], 'Sun': [0, 0]}
        for item in self.collection:
            times_likes = dow[item[DATE].strftime('%a')]
            times_likes[0] += 1
            times_likes[1] += item[LIKES]
        for day in dow:
            times, likes = dow[day]
            try:
                print("%s: μ = %d, posted %d times, received %d likes" % (day, float(likes) / times, times, likes))
            except ZeroDivisionError:
                print("%s: μ = n/a, posted %d times, received %d likes" % (day, times, likes))


if __name__ == '__main__':
    c = Collection(MYDATA_JSON)
    c.find_dayofweek_stat()

