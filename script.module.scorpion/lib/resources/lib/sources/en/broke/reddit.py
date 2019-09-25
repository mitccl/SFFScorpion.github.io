# -*- coding: utf-8 -*-
'''
.............aOOOOOOOOOOOaa........................................................................................................................................................
..........Cf.               .G1....................................................................................................................................................
........G.                    C1..............C0@@@@@@@@@@@........................................................................................................................
......if                        .G...........C@@@@@@@@@@@@@@@......................................................................................................................
.....t1              LL          .G........C@@@@@@8...G@@@@@.......................................................................................................................
....;C        .81   ;@@;          ;t........@@@@@@@@@@@GC..........G@@@@@8GG......0@@@@@8G.....G8@@@@@@@@8G.......C8@@@@@@@@@8C..C8@@@@@0......C8@@@@@8C.....G8@@@@@G..0@@@@@8.....
....L;        t88    ff            8.........G@@@@@@@@@@@@8......8@@@@@@@@@@0...0@@@88@@@@@C...0@@@@@G0@@@@@C.....C@@@@@@G8@@@@0.C@@@@@@8....C@@@@8@@@@@8....0@@@@@@@@.8@@@@@8.....
....G.         t;                  L...........C@@@@@@@@@@@@0...@@@@@@C..@@@0..8@@@@...@@@@@C...G@@@@C.8@@@@........@@@@0.0@@@@@...@@@@@....C@@@@8..G@@@@@....0@@@@@@@G.G@@@8......
....C.                      C0     L.............G@@@@@@@@@@@C.@@@@@@.........G@@@@@...G@@@@@C..G@@@@@@@@@0.........@@@@@@@@@@@G...@@@@8....8@@@@0...8@@@@0...0@@@@@@@@G.@@@C......
....1f                   .G.      .G......8@@....@@@@@@@@@@@@0.@@@@@@C........8@@@@@G..C@@@@@G..0@@@@@@@@@@0C......C@@@@@@@@80C...G@@@@@....@@@@@@C..0@@@@@...0@@@@@@@@@@@@@8......
.....L.              .tCiC        C......G@@@@@@@@@@@@@@@@@@@0.@@@@@@@8G@@@@0.8@@@@@@@8@@@@@@G..@@@@@@.C@@@@@8.....G@@@@@G........8@@@@@C...@@@@@@@@@@@@@@@...@@@@@@.8@@@@@@@......
......L.   .CCCLCCCf.VCC         Ci......C@@@@@@@@@@@@@@@@@@@..@@@@@@@@@@@@@0.0@@@@@@@@@@@@@@G.G@@@@@@C.8@@@@@C....@@@@@@@........@@@@@@@...@@@@@@@@@@@@@@@..0@@@@@@0.8@@@@@@0.....
.......1f                      .0.........G@@@@@@@@@@@@@@@@@....8@@@@@@@@@@@0..8@@@@@@@@@@@@@.C@@@@@@@@C0@@@@@@...8@@@@@@@@......8@@@@@@@8..C@@@@@@@@@@@@@0.C@@@@@@@@0.8@@@@@@.....
.........Cf                  .0;............0@@@@@@@@@@@@@C......C8@@@@@@@@G....G@@@@@@@@@@0..8@@@@@@@@@.@@@@@@@..@@@@@@@@@G....0@@@@@@@@@C...0@@@@@@@@@8...8@@@@@@@@@C.8@@@@8.....
...........;ft.          .10t................@@@@@@@@@@@@..........@@@@@@@@.......@@@@@@@@....@@@@@@@@@@..@@@@@@.@@@@@@@@@@@@..@@@@@@@@@@@@@...@@@@@@@@@...@@@@@@@@@@@@..@@@@@@....
...............OOoooooaQQ..........................................................................................................................................................
'''

import json
import re
import urllib
import urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['www.reddit.com']
        self.base_link = ['https://www.reddit.com/r/fullmoviesonyoutube/',
                          'https://www.reddit.com/r/fullmoviesonvimeo/',
                          'https://www.reddit.com/r/fullmoviesongoogle/']
        self.search_link = 'search.json?q=%s+%s&restrict_sr=1'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year, 'aliases': aliases}
            url = urllib.urlencode(url)
            return url
        except BaseException:
            return

    def search(self, title, year):
        try:
            content = []
            for link in self.base_link:
                try:
                    query = urlparse.urljoin(link, self.search_link % (urllib.quote(title), year))
                    r = client.request(query)
                    r = json.loads(r)
                    r = r['data']['children'][0]['data']

                    if not cleantitle.get_simple(r['title'].split(year)[0]) == cleantitle.get(title): raise Exception()
                    if not year in r['title']: raise Exception()
                    content = [(r['title'], r['url'])]

                except BaseException:
                    pass
            return content
        except BaseException:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url is None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            urls = self.search(data['title'], data['year'])

            for url in urls:
                try:
                    link = client.replaceHTMLCodes(url[1])
                    link = link.encode('utf-8')
                    if link in sources: continue
                    if 'snahp' in link:
                        data = client.request(link)
                        data = client.parseDOM(data, 'center')
                        data = [i for i in data if 'Hidden Link' in i][0]
                        link = client.parseDOM(data, 'a', ret='href')[0]
                    if 'google' in link:
                        quality, info2 = source_utils.get_release_quality(url[0], link)
                        sources.append(
                            {'source': 'gvideo', 'quality': quality, 'language': 'en', 'url': link, 'direct': False,
                             'debridonly': False})

                    else:
                        host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(link.strip().lower()).netloc)[0]
                        if host in hostDict:
                            host = host.encode('utf-8')
                            quality, info2 = source_utils.get_release_quality(url[0], link)
                            sources.append(
                                {'source': host, 'quality': quality, 'language': 'en', 'url': link, 'direct': False,
                                 'debridonly': False})
                except BaseException:
                    pass
            return sources
        except BaseException:
            return sources

    def resolve(self, url):
        return url
