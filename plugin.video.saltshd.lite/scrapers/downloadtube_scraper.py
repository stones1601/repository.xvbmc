"""
    SALTS XBMC Addon
    Copyright (C) 2014 tknorris

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import scraper
import urlparse
import re
import urllib
import kodi
import log_utils
import dom_parser
from salts_lib import scraper_utils
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import XHR

BASE_URL = 'http://www.mydownloadtube.com'

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'DownloadTube'

    def get_sources(self, video):
        source_url = self.get_url(video)
        sources = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=8)
            streams = dom_parser.parse_dom(html, 'a', {'class': 'download_item'}, ret='href')
            labels = dom_parser.parse_dom(html, 'a', {'class': 'download_item'})
            for stream_url, label in zip(streams, labels):
                label = re.sub('\s+', ' ', label)
                log_utils.log(label)
                if 'bit.ly' in stream_url:
                    redir_url = self._http_get(stream_url, allow_redirect=False, method='HEAD', require_debrid=True, cache_limit=8)
                    if redir_url.startswith('http'):
                        stream_url = redir_url
                        
                movie = scraper_utils.parse_movie_link(label)
                quality = scraper_utils.height_get_quality(movie['height'])
                is_3d = True if re.search('\s+3D\s+', label) else False
                if is_3d: quality = QUALITIES.HD1080
                host = urlparse.urlparse(stream_url).hostname
                source = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': False}
                source['3D'] = is_3d
                match = re.search('([\d.]+\s+[MG]?B)', label)
                if match:
                    source['size'] = match.group(1)
                sources.append(source)

        return sources

    def search(self, video_type, title, year, season=''):
        results = []
        search_url = urlparse.urljoin(self.base_url, '/search/search_val?language=English%%20-%%20UK&term=%s')
        search_url = search_url % (urllib.quote_plus(title))
        referer = urlparse.urljoin(self.base_url, '/search')
        headers = {'Referer': referer}
        headers.update(XHR)
        html = self._http_get(search_url, headers=headers, require_debrid=True, cache_limit=8)
        js_data = scraper_utils.parse_json(html, search_url)
        for item in js_data:
            if item.get('category', '').lower() != 'movies': continue
            match_title_year = item['label']
            match_url = item['url']
            match = re.search('(.*?)\s+\((\d{4})\)\s*', match_title_year)
            if match:
                match_title, match_year = match.groups()
            else:
                match_title = match_title_year
                match_year = ''
            
            if not year or not match_year or year == match_year:
                result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                results.append(result)

        return results