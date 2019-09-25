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
from resources.lib.modules import dom_parser
from resources.lib.modules import jsunpack
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['watch32hd.co']
        self.base_link = 'https://watch32hd.co/'
        self.search_link = 'results?q=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except BaseException:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url is None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['title']

            hdlr = data['year']

            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', title)

            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url)
            r = client.request(url)

            posts = client.parseDOM(r, 'div', attrs={'class': 'video_title'})

            items = []

            for post in posts:
                try:
                    data = dom_parser.parse_dom(post, 'a', req=['href', 'title'])[0]
                    t = data.content
                    y = re.findall('\((\d{4})\)', data.attrs['title'])[0]
                    qual = data.attrs['title'].split('-')[1]
                    link = data.attrs['href']

                    if not cleantitle.get(t) == cleantitle.get(title): raise Exception()
                    if not y == hdlr: raise Exception()

                    items += [(link, qual)]

                except BaseException:
                    pass
            for item in items:
                try:
                    r = client.request(item[0]) if item[0].startswith('http') else client.request(
                        urlparse.urljoin(self.base_link, item[0]))

                    qual = client.parseDOM(r, 'h1')[0]
                    quality = source_utils.get_release_quality(item[1], qual)[0]

                    url = re.findall('''frame_url\s*=\s*["']([^']+)['"]\;''', r, re.DOTALL)[0]
                    url = url if url.startswith('http') else urlparse.urljoin('https://', url)

                    sources.append({'source': 'GVIDEO', 'quality': quality, 'language': 'en', 'url': url,
                                    'direct': False, 'debridonly': False})

                except BaseException:
                    pass

            return sources
        except BaseException:
            return sources

    def resolve(self, url):
        try:
            if 'vidlink' in url:
                ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1'}
                html = client.request(url, headers=ua)
                postID = re.findall("postID\s*=\s*'([^']+)", html)[0]

                rid = client.request('https://vidlink.org/embed/update_views', post=None, headers=ua, referer=url)
                id_view = re.findall('''id_view['"]\s*:\s*['"]([^'"]+)['"]''', rid)[0]

                plink = 'https://vidlink.org/streamdrive/info'
                data = {'browserName': 'Firefox',
                        'platform': 'Win32',
                        'postID': postID,
                        'id_view': id_view}
                headers = ua
                headers['X-Requested-With'] = 'XMLHttpRequest'
                headers['Referer'] = url
                ihtml = client.request(plink, post=data, headers=headers)
                linkcode = jsunpack.unpack(ihtml).replace('\\', '')
                sources = json.loads(re.findall('window\.srcs\s*=\s*([^;]+)', linkcode, re.DOTALL)[0])
                for src in sources:
                    link = src['url']
                    return link
            else:
                return url
        except BaseException:
            return url
