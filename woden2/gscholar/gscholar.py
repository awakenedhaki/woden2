import requests

from time import sleep
from random import randint
from .scholar import Scholar
from bs4 import BeautifulSoup
from utils import random_headers


class GoogleScholar(object):
    _HOST = 'https://scholar.google.com'
    _PROFILE = '/citations?user=%s&hl=en'
    _AUTHORSEARCH = '/citations?view_op=search_authors&mauthors=%s&hl=en'
    _PUBSEARCH = '/scholar?q=%s'
    _KEYWORD = '/citations?view_op=search_authors&hl=en&mauthors=label:%s'
    _SESSION = requests.Session()
    _USERAGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0')
    _SECONDS = 3
    _TIMEOUT = 3

    def __init__(self, headers=None, http=None, https=None):
        if http and https:
            self._SESSION.proxies = {
                'http': http,
                'https': https
            }
        self._headers = random_headers(headers if headers is not None else self._USERAGENT)

    def _search(self, query):
        '''
        GET request for google scholar

        Parameters
        ----------
        query : str
            Query string with search parameters

        Returns
        -------
        BeautifulSoup object of source HTML
        '''
        # sleep for 5 to 10 seconds
        sleep(self._SECONDS + randint(0, 5))
        with self._SESSION.get(self._HOST + query, timeout=self._TIMEOUT, headers=self._headers()) as response:
            return BeautifulSoup(response.content, 'html.parser')

    def search_keyword(self, keyword: str, limit = 10):
        '''
        Searches for scholars associated with keyword.

        Parameters
        ----------
        keyword : str
            A registered keyword for Google Scholar

        Returns
        -------
        Generators of Scholar instance representing 
        '''
        def _continue(button, number_scholars, limit):
            active_button = button and 'disabled' not in button.attrs
            maxed = num_scholars > limit
            return active_button or maxed

        query = self._KEYWORD % keyword.replace(' ', '_')
        soup = self._search(query)
        
        button = soup.select_one('button.gs_btnPR.gs_in_ib.gs_btn_half.gs_btn_lsb.gs_btn_srt.gsc_pgn_pnx')
        num_scholars = 0
        # Iterate until button is not found, or disabled
        while _continue(button, num_scholars, limit):
            for result in soup.select('div.gs_ai.gs_scl.gs_ai_chpr'):
                yield Scholar(result)
                num_scholars += 1
        
            # Path + query for next page
            next_page = button['onclick'].split("'")[1].encode('utf-8').decode('unicode-escape')
            soup = self._search(next_page)

    def search_profile(self, id_):
        query = self._PROFILE % id_
        soup = self._search(query)
        return Scholar(soup, self)

    def search_publication(self, string):
        pass