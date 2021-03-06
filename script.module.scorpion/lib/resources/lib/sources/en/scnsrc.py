# -*- coding: UTF-8 -*-
#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # @tantrumdev wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. - Muad'Dib
 # ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Scorpion
# Addon id: plugin.video.Scorpion
# Addon Provider: Supremacy

import re, urllib, urlparse

from resources.lib.modules import debrid
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import dom_parser2
from resources.lib.modules import workers
from resources.lib.modules import source_utils
from resources.lib.modules import cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['scnsrc.me']
        self.base_link = 'https://www.scnsrc.me'


        self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = urlparse.urljoin(self.base_link, self.search_link % cleantitle.geturl(title).replace('-', '+'))
            r = self.scraper.get(url, headers={'cookie': 'check=2'}).content
            m = dom_parser.parse_dom(r, 'div', attrs={'class': 'masonry'})
            m = dom_parser.parse_dom(m, 'a', req='href')
            m = [(i.attrs['href']) for i in m if i.content == title]
            if m is not None:
                url = urlparse.urljoin(self.base_link, m[0])
            return url
        except:
            return None

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None:
                return
            data = urlparse.parse_qs(url)
            data = dict((i, data[i][0]) for i in data)
            url = urlparse.urljoin(self.base_link, self.search_link %
                                   cleantitle.geturl(data['tvshowtitle']).replace('-', '+'))
            r = self.scraper.get(url, headers={'cookie': 'check=2'}).content
            m = dom_parser.parse_dom(r, 'div', attrs={'class': 'masonry'})
            m = dom_parser.parse_dom(m, 'a', req='href')
            m = [(i.attrs['href']) for i in m if i.content == data['tvshowtitle']]
            query = '%s/season-%s/episode-%s/' % (m[0], season, episode)
            url = urlparse.urljoin(self.base_link, query)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url is None:
                return
            r = self.scraper.get(url, headers={'cookie': 'check=2'}).content

            m = dom_parser.parse_dom(r, 'table', attrs={'class': 'show_links'})[0]
            links = re.findall('k">(.*?)<.*?f="(.*?)"', m.content)
            for link in links:
                try:
                    sources.append({'source': link[0], 'quality': 'SD', 'language': 'en',
                                    'url': link[1], 'direct': False, 'debridonly': False})
                except Exception:
                    pass

            return sources
        except Exception:
            return sources

    def resolve(self, url):
        r = self.scraper.get(url).content
        r = dom_parser.parse_dom(r, 'div', {'class': 'link_under_video'})
        r = dom_parser.parse_dom(r, 'a', req='href')
        return r[0].attrs['href']
