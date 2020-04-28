# -*- coding: utf-8 -*-

import os.path
import requests
from bs4 import BeautifulSoup
import socket
import ssl

from requests_toolbelt import SSLAdapter


class lib_httprequest():

    name = 'lib_httprequest'

    def __init__(self):
        self.encoding = 'utf-8'
        self.proxies = None
        self.parser = 'html.parser'
        self.timeout = 30

        self.session = requests.Session()
        self.session.is_patch = True
        self.session.mount('https://', SSLAdapter())

    def http_get(self, url, params=None, *args, **kwargs):
        '''
        New version of web_get
        '''

        def get_soup(self):
            if not hasattr(self, '_soup'):
                self._soup = BeautifulSoup(
                    self.text, self.parser, from_encoding=self.encoding)
            # time.sleep(.250)
            return self._soup

        try:
            proxies = {'http': self.proxies,
                       'https': self.proxies} if self.proxies else None
            r = self.session.get(
                url, params=params, allow_redirects=True, timeout=self.timeout, proxies=proxies)
            if hasattr(self, 'encoding'):
                r.encoding = self.encoding
            r.__class__.soup = property(get_soup)
            return r
        except (ssl.SSLError, socket.error) as e:
            raise requests.exceptions.RequestException(str(e))
    
    def http_get_with_encode(self, url, params=None,encoder='utf-8', *args, **kwargs):
        '''
        New version of web_get
        '''

        def get_soup(self):
            if not hasattr(self, '_soup'):
                self._soup = BeautifulSoup(
                    self.text, self.parser, from_encoding=encoder)
            # time.sleep(.250)
            return self._soup

        try:
            proxies = {'http': self.proxies,
                       'https': self.proxies} if self.proxies else None
            r = self.session.get(
                url, params=params, allow_redirects=True, timeout=self.timeout, proxies=proxies)
            if hasattr(self, 'encoding'):
                r.encoding = encoder
            r.__class__.soup = property(get_soup)
            return r
        except (ssl.SSLError, socket.error) as e:
            raise requests.exceptions.RequestException(str(e))

    def http_get_with_headers(self, url, params=None, *args, **kwargs):
        '''
        New version of web_get
        '''

        def get_soup(self):
            if not hasattr(self, '_soup'):
                self._soup = BeautifulSoup(
                    self.text, self.parser, from_encoding=self.encoding)
            # time.sleep(.250)
            return self._soup

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36', }
        try:
            proxies = {'http': self.proxies,
                       'https': self.proxies} if self.proxies else None
            r = self.session.get(
                url, headers=headers, params=params, allow_redirects=True, timeout=self.timeout, proxies=proxies)
            if hasattr(self, 'encoding'):
                r.encoding = self.encoding
            r.__class__.soup = property(get_soup)
            return r
        except (ssl.SSLError, socket.error) as e:
            raise requests.exceptions.RequestException(str(e))

    def http_post(self, url, data, params=None, *args, **kwargs):
        '''
        New version of web_post
        '''

        def get_soup(self):
            if not hasattr(self, '_soup'):
                self._soup = BeautifulSoup(
                    self.text, self.parser, from_encoding=self.encoding)
            # time.sleep(.255)
            return self._soup
        try:
            proxies = {'http': self.proxies,
                       'https': self.proxies} if self.proxies else None
            r = self.session.post(url, data=data,  params=params, allow_redirects=True,
                                  timeout=self.timeout, proxies=proxies, *args, **kwargs)
            if hasattr(self, 'encoding'):
                r.encoding = self.encoding
            r.__class__.soup = property(get_soup)
            return r
        except (ssl.SSLError, socket.error) as e:
            raise requests.exceptions.RequestException(str(e))
   
    def http_post_with_headers(self, url,headers, data, params=None, *args, **kwargs):
        '''
        New version of web_post
        '''

        def get_soup(self):
            if not hasattr(self, '_soup'):
                self._soup = BeautifulSoup(
                    self.text, self.parser, from_encoding=self.encoding)
            # time.sleep(.255)
            return self._soup
        #headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36', }
        try:
            proxies = {'http': self.proxies,
                       'https': self.proxies} if self.proxies else None
            r = self.session.post(url, data=data,  headers=headers, params=params, allow_redirects=True,
                                  timeout=self.timeout, proxies=proxies, *args, **kwargs)
            if hasattr(self, 'encoding'):
                r.encoding = self.encoding
            r.__class__.soup = property(get_soup)
            return r
        except (ssl.SSLError, socket.error) as e:
            raise requests.exceptions.RequestException(str(e))

    def http_post_json(self, url, jsoncontent, params=None, *args, **kwargs):
        '''
        New version of web_post
        '''

        def get_soup(self):
            if not hasattr(self, '_soup'):
                self._soup = BeautifulSoup(
                    self.text, self.parser, from_encoding=self.encoding)
            # time.sleep(.255)
            return self._soup

        headers = {"content-type": "application/json"}

        try:
            proxies = {'http': self.proxies,
                       'https': self.proxies} if self.proxies else None
            r = self.session.post(url, data=jsoncontent, headers=headers, params=params,
                                  allow_redirects=True, timeout=self.timeout, proxies=proxies, *args, **kwargs)
            if hasattr(self, 'encoding'):
                r.encoding = self.encoding
            r.__class__.soup = property(get_soup)
            return r
        except (ssl.SSLError, socket.error) as e:
            raise requests.exceptions.RequestException(str(e))

    def http_post_with_multi_options(self, url, headerreg={}, jsoncontent={}, params=None, *args, **kwargs):
        '''
        New version of web_post
        '''

        def get_soup(self):
            if not hasattr(self, '_soup'):
                self._soup = BeautifulSoup(
                    self.text, self.parser, from_encoding=self.encoding)
            # time.sleep(.255)
            return self._soup

        try:
            proxies = {'http': self.proxies,
                       'https': self.proxies} if self.proxies else None
            r = self.session.post(url, data=jsoncontent, headers=headerreg, params=params,
                                  allow_redirects=True, timeout=self.timeout, proxies=proxies, *args, **kwargs)
            if hasattr(self, 'encoding'):
                r.encoding = self.encoding
            r.__class__.soup = property(get_soup)
            return r
        except (ssl.SSLError, socket.error) as e:
            raise requests.exceptions.RequestException(str(e))

    def http_put_json(self, url, jsoncontent, params=None, *args, **kwargs):
        '''
        New version of web_post
        '''

        def get_soup(self):
            if not hasattr(self, '_soup'):
                self._soup = BeautifulSoup(
                    self.text, self.parser, from_encoding=self.encoding)
            # time.sleep(.255)
            return self._soup

        headers = {"content-type": "application/json"}

        try:
            proxies = {'http': self.proxies,
                       'https': self.proxies} if self.proxies else None
            r = self.session.put(url, data=jsoncontent, headers=headers, params=params,
                                 allow_redirects=True, timeout=self.timeout, proxies=proxies,  *args, **kwargs)
            if hasattr(self, 'encoding'):
                r.encoding = self.encoding
            r.__class__.soup = property(get_soup)
            return r
        except (ssl.SSLError, socket.error) as e:
            raise requests.exceptions.RequestException(str(e))
