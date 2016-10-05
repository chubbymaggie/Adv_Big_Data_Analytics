import wikipedia
from collections import defaultdict
import time
import re


search_key = 'machine learning'

title_queue = wikipedia.search(search_key)
title_resultset = []
visited_title = defaultdict(int)

while len(title_queue) > 0 and len(title_resultset) < 100:
    the_title = title_queue[0]
    title_queue.remove(the_title)
    if not visited_title[the_title] > 0:
        visited_title[the_title] = 1
        try:
            wiki = wikipedia.page(the_title)
            for l in wiki.links:
                title_queue.append(l)
            content = re.sub(r'[\s]+', ' ', str(wiki.content))
            if len(content) > 1000:
                print str(content),
                print '\n',
                title_resultset.append(the_title)

        except:
            continue



