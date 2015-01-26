#!/usr/bin/env python

import re
import urlparse
import traceback

from bs4 import BeautifulSoup
from soup_requestor import SoupRequestor

class EmailScraper(object):
    def __init__(self):
        self.email_regex = r'\b([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4})\b'
        self.email_link_regex = r'mailto:\b([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4})\b'
        self.sreq = SoupRequestor()

    def follow_link(self, base_url, pattern):
        pass

    def get_email_link_from_page(self, soup):
        r = re.compile(self.email_link_regex, re.I)
        a = soup.find('a', href=re.compile(r))

        if a:
            m = re.search(r, a.get('href'))
            if len(m.groups()):
                return m.group(1)
        
        return None

    def get_email_text_from_page(self, soup):
        r = re.compile(self.email_regex, re.I)
        t = soup.find(text=re.compile(r))

        if t:
            m = re.search(r, t)
            if len(m.groups()):
                return m.group(1)
        
        return None

    def scrape_email(self, base_url):
        (r,s) = self.sreq.get(base_url)
        if r is None:
            return None

        if s.meta:
            if 'searchassist.verizon.com' in s.meta.get('content', ''):
                return None

        # First try landing page
        e = self.get_email_link_from_page(s)
        if e:
            return e

        e = self.get_email_text_from_page(s)
        if e:
            return e

        # See if there's a "contact us" page
        a = s.find('a', text=re.compile(r'contact', re.I))
        if a:
            u = urlparse.urljoin(base_url, a.get('href'))
            (r,s) = self.sreq.get(u)

            if r is not None:
                e = self.get_email_link_from_page(s)
                if e:
                    return e

                e = self.get_email_text_from_page(s)
                if e:
                    return e

        # Try escaped fragment version of landing page
        u = urlparse.urljoin(base_url, '?_escaped_fragment_=')
        (r,s) = self.sreq.get(u)

        if r is not None:
            e = self.get_email_link_from_page(s)
            if e:
                return e

            e = self.get_email_text_from_page(s)
            if e:
                return e

if __name__ == '__main__':
    scraper = EmailScraper()
    scraper.scrape_email('http://toddhayton.com')
