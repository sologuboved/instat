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

    def sort_by(self, field):
        self.collection.sort(key=lambda i: i[field], reverse=True)
        self.prettyprint()

    def find_dayofweek_stat(self):
        dow = dict()
        for item in self.collection:
            day = item[DATE].strftime('%a')
            times_likes = dow.get(day, [0, 0])
            times_likes[0] += 1
            times_likes[1] += item[LIKES]
            dow[day] = times_likes
        for day in dow:
            times, likes = dow[day]
            print("%s: μ = %d, posted %d times, received %d likes" % (day, float(likes) / times, times, likes))

    def find_timeofday_stat(self):
        utc_tod = dict()
        for item in self.collection:
            hour = item[DATE].strftime('%I') + item[DATE].strftime('%p')
            times_likes = utc_tod.get(hour, [0, 0])
            times_likes[0] += 1
            times_likes[1] += item[LIKES]
            utc_tod[hour] = times_likes
        tod = dict()
        for utc_hour in utc_tod:
            times, likes = utc_tod[utc_hour]
            hour = str(int(utc_hour[:2]) + 3) + utc_hour[2:]
            tod[hour] = (times, likes, float(likes) / times)
        for item in sorted(tod.items(), key=lambda i: i[1][2]):
            hour = item[0]
            w_s = ' ' * (5 - len(hour))
            print("%s:%s μ = %d, posted %d times, received %d likes" % (hour, w_s, item[1][2], item[1][0], item[1][1]))

    def find_total_likes(self):
        print(sum(item[LIKES] for item in self.collection))


if __name__ == '__main__':
    c = Collection(MYDATA_JSON)
    c.find_total_likes()

