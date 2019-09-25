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
import re,urlparse
from resources.lib.modules import client,cleantitle,source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['cmovies.cc']
        self.base_link = 'https://cmovies.cc'
        self.search_link = '/?s=%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            search_id = cleantitle.getsearch(title)
            url = urlparse.urljoin(self.base_link, self.search_link)
            url = url  % (search_id.replace(':', ' ').replace(' ', '+'))
            search_results = client.request(url)
            match = re.compile('<span class="project-details"><a href="(.+?)">(.+?)</a>',re.DOTALL).findall(search_results)
            for row_url, row_title in match:
                if cleantitle.get(title) in cleantitle.get(row_title):
                    if year in str(row_title):
                        return row_url
            return
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            hostDict = hostDict + hostprDict
            if url == None:
                return sources
            html = client.request(url)
            links = re.compile('<iframe.+?src="(.+?)"',re.DOTALL).findall(html)
            for link in links:
                if not link.startswith('http'):
                    link =  "https:" + link
                host = link.split('//')[1].replace('www.','')
                host = host.split('/')[0].split('.')[0].title()
                quality,info = source_utils.get_release_quality(link, link)
                sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link, 'info': info, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


