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

import re,requests,urlparse
from resources.lib.modules import client,cleantitle,tvmaze
from resources.lib.modules import source_utils,source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.genre_filter = ['animation', 'anime']
        self.domains = ['cartoonextra.in']
        self.base_link = 'http://cartoonextra.in'
        self.search_link = '/toon/search?key=%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            url = '%s-%s' % (title, year)
            url = self.base_link + '/' + url
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            tv_maze = tvmaze.tvMaze()
            tvshowtitle = tv_maze.showLookup('thetvdb', tvdb)
            tvshowtitle = tvshowtitle['name']
            t = cleantitle.get(tvshowtitle)
            q = self.base_link + self.search_link %(tvshowtitle)
            r = client.request(q)
            r = client.parseDOM(r, 'div', attrs={'class': 'cartoon-box'})
            for i in r:
                match = re.compile('<a href="(.+?)" class="image">',re.DOTALL).findall(i)
                for url in match:
                    if t in cleantitle.get(url):
                        return source_utils.strip_domain(url)
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            if season == '1': 
                url = self.base_link + url + '-episode-' + episode
            else:
                url = self.base_link + url + '-season-' + season + '-episode-' + episode
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            hostDict = hostDict + hostprDict
            sources = []
            if url == None:
                return sources
            r = client.request(url)
            match = re.compile('<iframe.+?src="(.+?)"',re.DOTALL).findall(r)
            for url in match:
                quality = source_utils.get_quality(url)
                info = source_utils.get_info(url)
                valid, host = source_utils.is_host_valid(url, hostDict)
                if valid or 'gogoanime' in url:
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            open = requests.get(url, timeout=3).content
            if 'gogoanime' in url:
                url = re.compile('"link":"(.+?)"',re.DOTALL).findall(open)[0]
                url = url.replace('\\','')
        except:
            pass
        return url


