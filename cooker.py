import random
from datetime import datetime, timedelta
from basic_operations import *

MYDATA_JSON = 'mydata.json'
URL = 'url'
LIKES = 'likes'
TAGS = 'tags'
DATE = 'date'


class Instat(object):
    def __init__(self, json_fname):
        self.json_fname = json_fname
        self.collection = list()
        self.tags = set()
        self.cook()

    def cook(self):

        self.collection = list()
        collection = load_json(self.json_fname)

        for url in collection:
            item = collection[url]
            tags = item[TAGS]
            for tag in tags:
                self.tags.add(tag)
            date = datetime.strptime(item[DATE], "%b %d, %Y %I:%M%p %Z") + timedelta(hours=3)
            self.collection.append({URL: url, LIKES: item[LIKES], TAGS: tags, DATE: date})


    def filter_by_date(self, start, end, printer_on=False):
        # filter_by_date('29.01.2017', '29.01.2018')

        try:
            start, end = map(lambda d: datetime.strptime(d, "%d.%m.%Y"), (start, end))
        except ValueError:
            print("Wrong date(s)")
            return

        self.collection = [item for item in self.collection if start <= item[DATE] < end]

        if printer_on:
            print("Filtered from", start, 'to', end)
            self.prettyprint_sorted_by(DATE, large_to_small=False)

    def prettyprint(self, allotment=None):

        ind = 1

        if not allotment:
            allotment = self.collection

        for item in allotment:
            print('<%d>' % ind)
            print('url:', item[URL])
            print('date:', item[DATE].strftime("%d %B %Y, %A %I:%M%p"))
            print('likes:', item[LIKES])
            print('tags:')
            for tag in item[TAGS]:
                print("         ", tag)
            print()
            ind += 1

        print()

    def prettyprint_sorted_by(self, field, large_to_small=True, allotment=None):

        if not allotment:
            allotment = self.collection

        allotment.sort(key=lambda i: i[field], reverse=large_to_small)
        self.prettyprint(allotment)

    def get_random_pic(self): print(self.collection[random.randrange(len(self.collection))][URL], '\n')

    def find_by_tag(self, tag): self.prettyprint([item for item in self.collection if tag in item[TAGS]])

    def find_total_likes(self): print(sum(item[LIKES] for item in self.collection), '\n')

    def count_by_year(self):

        prefix = '01.01.'
        self.collection.sort(key=lambda i: i[DATE])
        initial_year = int(self.collection[0][DATE].strftime('%Y'))
        curr_year = int(datetime.today().strftime('%Y'))
        from_year = initial_year
        till_year = initial_year + 1

        while till_year <= curr_year + 1:
            self.cook()
            self.filter_by_date(prefix + str(from_year), prefix + str(till_year))
            print("%d: %d pics" % (from_year, len(self.collection)))
            from_year += 1
            till_year += 1

        self.cook()

        print(len(self.collection), "pics total", '\n')

    def find_tag_freqs(self):

        tag_freqs = dict.fromkeys(list(self.tags), 0)

        for item in self.collection:
            for tag in item[TAGS]:
                tag_freqs[tag] += 1

        for freq in sorted(tag_freqs.items(), key=lambda i: i[1], reverse=True):
            print(freq[0] + ':', freq[1])
        print()

    def analyse_tags(self, larger_than=0, smaller_than=float('inf'), sort_by_mean=False):

        all_tags = dict()
        for item in self.collection:
            tags = item[TAGS]
            for tag in tags:
                likes = all_tags.get(tag, list())
                likes.append(item[LIKES])
                all_tags[tag] = likes

        filtered_tags = list()
        for tag in all_tags:
            likes = all_tags[tag]
            num_likes = len(likes)
            if larger_than < num_likes < smaller_than:
                total_likes = sum(likes)
                mean = total_likes / float(num_likes)
                s_d = find_sd(likes, mean)
                try:
                    quotient = mean / s_d
                    filtered_tags.append((tag, num_likes, total_likes, mean, s_d, quotient))
                except ZeroDivisionError:
                    pass

        if sort_by_mean:
            filtered_tags.sort(key=lambda i: i[3], reverse=True)
        else:
            filtered_tags.sort(key=lambda i: i[5], reverse=True)

        for item in filtered_tags:
            tag = item[0]
            w_s = ' ' * (20 - len(tag))
            print("%s:%s μ/σ = %f, μ = %f, σ = %f, posted %d times, received %d likes" % (tag, w_s,
                                                                                          item[5],
                                                                                          item[3],
                                                                                          item[4],
                                                                                          item[1],
                                                                                          item[2]))
        print()

    def analyse_time(self, by_day):

        def sort_days(element): return element[1][2]

        def sort_hours(element): return element[0]

        if by_day:
            timestring = '%a'
            sorter = sort_days
        else:
            timestring = '%H'
            sorter = sort_hours

        times = dict()

        for item in self.collection:
            timelet = item[DATE].strftime(timestring)
            likes = times.get(timelet, list())
            likes.append(item[LIKES])
            times[timelet] = likes

        for timelet in times:
            likes = times[timelet]
            num_likes = len(likes)
            total_likes = sum(likes)
            mean = float(total_likes) / num_likes
            s_d = find_sd(likes, mean)
            times[timelet] = (num_likes, total_likes, mean, s_d)
        for item in sorted(times.items(), key=sorter):
            timelet, vals = item
            w_s = ' ' * (5 - len(timelet))
            print("%s:%s μ = %f, σ = %f, posted %d times, received %d likes" % (timelet, w_s,
                                                                                vals[2], vals[3], vals[0], vals[1]))
        print()


if __name__ == '__main__':
    inst = Instat(MYDATA_JSON)
    inst.count_by_year()
    inst.filter_by_date('29.01.2014', '29.01.2019', printer_on=False)
    inst.analyse_time(by_day=True)
    inst.analyse_time(by_day=False)
