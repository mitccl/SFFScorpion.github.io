# -*- coding: UTF-8 -*-
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
----------------------------------------------------------------------------
"THE BEER-WARE LICENSE" (Revision 42):
@tantrumdev wrote this file.  As long as you retain this notice you
can do whatever you want with this stuff. If we meet some day, and you think
this stuff is worth it, you can buy me a beer in return. - Muad'Dib
----------------------------------------------------------------------------

Addon Name: Scorpion
Addon id: plugin.video.scorpion
Addon Provider: Supremacy
'''
import re, urllib, urlparse, time

from resources.lib.modules import client
from resources.lib.modules import debrid
from resources.lib.modules import source_utils
from resources.lib.modules import workers
from resources.lib.modules import cfscrape

class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domains = ['best-moviez.ws']
        self.base_link = 'https://www.best-moviez.ws/'
        self.search_link = '?s={0}&submit=Search'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except BaseException:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except BaseException:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return

            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except BaseException:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            self._sources = []

            if url is None:
                return self._sources

            if not debrid.status():
                raise Exception()

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            self.imdb = data['imdb']
            content = 'tvshow' if 'season' in data else 'movie'
            self.hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            
            items = []
            self.hostDict = hostprDict + hostDict

            query = '%s S%02dE%02d' % (self.imdb, int(data['season']), int(data['episode'])) if 'tvshowtitle' in data\
                else '%s' % self.imdb

            url = urlparse.urljoin(self.base_link, self.search_link.format(query))
            scraper = cfscrape.create_scraper()
            headers = {'User-Agent': client.agent(),
                       'Referer': self.base_link}
            r = scraper.get(url, headers=headers).content

            data = client.parseDOM(r, 'article')
            links = [client.parseDOM(i, 'a', ret='href')[0] for i in data if i]

            threads = []
            for i in links:
                threads.append(workers.Thread(self._get_sources, i))
            [i.start() for i in threads]
            [i.join() for i in threads]

            return self._sources
        except BaseException:
            return self._sources
            
    def _get_sources(self, i):
        try:
            url = urlparse.urljoin(self.base_link, i)
            scraper = cfscrape.create_scraper()
            headers = {'User-Agent': client.agent(),
                       'Referer': self.base_link}
            r = scraper.get(url, headers=headers).content
            if r: 
                items = []
                post = client.parseDOM(r, 'div', attrs={'class': 'entry-content'})
                post = [i for i in post if (self.imdb in i or self.hdlr.lower() in i)][0]
                try:
                    try:
                        size = re.findall('((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|MB|MiB))', i, re.DOTALL)
                        size = size[0].strip()
                        div = 1 if size.endswith(('GB', 'GiB')) else 1024
                        size = float(re.sub('[^0-9|/.|/,]', '', size.replace(',', '.'))) / div
                        size = '%.2f GB' % size
                    except IndexError:
                        size = '0'

                    try:
                        frames = client.parseDOM(post, 'a', ret='href')
                        frames = [i for i in frames if not any(x in i for x in ['.rar', '.zip', '.iso'])]
                    except IndexError:
                        pass
                    u = [(i, size, post) for i in frames]
                    items += u
                except BaseException:
                    pass
                for item in items:
                    try:
                        url = client.replaceHTMLCodes(item[0])
                        url = url.encode('utf-8')
                        valid, host = source_utils.is_host_valid(url, self.hostDict)
                        if not valid: continue
                        quality, info = source_utils.get_release_quality(item[0], item[2])
                        info.append(item[1])
                        info = ' | '.join(info)
                        self._sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url,
                                        'info': info, 'direct': False, 'debridonly': True})
                    except BaseException:
                        pass

                return self._sources
            return self._sources
        except BaseException:
            return self._sources

    def resolve(self, url):
        return url
