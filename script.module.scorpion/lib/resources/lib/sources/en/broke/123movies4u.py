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

import re

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['123movies4u.ch']
        self.base_link = 'https://123movies4u.ch'
        self.search_link = '/movie/%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title).replace('--', '-')
            url = self.base_link + self.search_link % title
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            hostDict = hostDict + hostprDict
            sources = []
            r = client.request(url)
            qual = re.compile('<span class="quality">(.+?)<').findall(r)
            if 'DVD' in qual:
                quality = '720p'
            else:
                quality = 'SD'
            u = client.parseDOM(r, "div", attrs={"id": "link_list"})
            for t in u:
                u = client.parseDOM(t, 'a', ret='href')
                for url in u:
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if host not in hostDict:
                        continue
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
                return sources
        except:
            return

    def resolve(self, url):
        return url
