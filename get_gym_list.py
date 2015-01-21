#!/usr/bin/env python2.7

import re
import sys
import json
import errno

from time import sleep
from pprint import pprint
from requests import get
from bs4 import BeautifulSoup

# XXX Record rejected gym ids so we don't keep trying to request their urls
class CrossfitGymScraper(object):
    def __init__(self):
        self.gyms = {}
        self.url = "http://map.crossfit.com/affinfo.php?a={}&t=0"

    def get_gym_list(self):
        #    for i in xrange(1, 7397 + 1):
        for i in xrange(1, 15):
            if str(i) in self.gyms:
                continue

            u = self.url.format(i)
            try:
                r = get(u)
            except KeyboardInterrupt:
                sys.exit(1)
            except:
                print 'Rejected: {}'.format(i)
                rej.write('{}\n'.format(i))
                continue

            s = BeautifulSoup(r.text)
            b = s.b.extract()
            p = s.contents[-1].extract()

            gym = {}
            gym['name'] = b.a.text
            gym['link'] = b.a['href']
            gym['addr'] = ' '.join(['%s' % x for x in s.findAll(text=True)])
            gym['phone'] = p
            self.gyms[str(i)] = gym
            sleep(0.5)

    def save_gyms(self):
        with open('gyms.json', 'w+') as f:
            json.dump(self.gyms, f)

    def load_gyms(self):
        try:
            f = open('gyms.json', 'r')
        except IOError as e:
            if e.errno == errno.ENOENT:
                pass
        else:
            d = f.read()
            if len(d):
                self.gyms = json.loads(d)
    
    def get_email_link_from_page(self, soup):
        r = re.compile(r'mailto:\b([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4})\b', re.I)
        a = soup.find('a', href=re.compile(r))

        if a:
            m = re.search(r, a['href'])
            if len(m.groups()):
                return m.group(1)
        
        return None

    def get_email_text_from_page(self, soup):
        r = re.compile(r'\b([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4})\b', re.I)
        t = soup.find(text=re.compile(r))

        if t:
            m = re.search(r, t)
            if len(m.groups()):
                return m.group(1)
        
        return None

    def get_gym_email(self, gym):
        if gym.get('email', False):
            return

        r = get(gym['link'])
        s = BeautifulSoup(r.text)

        # First try landing page
        e = self.get_email_link_from_page(s)
        if e:
            gym['email'] = e
            return

        e = self.get_email_text_from_page(s)
        if e:
            gym['email'] = e
            return

        # See if there's a "contact us" page
        a = s.find('a', text=re.compile(r'contact', re.I))
        if not a:
            return

        r = get(a['href'])
        s = BeautifulSoup(r.text)

        e = self.get_email_link_from_page(s)
        if e:
            gym['email'] = e

        e = self.get_email_text_from_page(s)
        if e:
            gym['email'] = e

    def get_gym_emails(self):
        for id,gym in self.gyms.items():
            self.get_gym_email(gym)
        
    def print_gyms(self):
        for id,gym in self.gyms.items():
            print id,gym

    def scrape(self):
        self.load_gyms()
        self.get_gym_list()
        self.get_gym_emails()
        self.save_gyms()

if __name__ == '__main__':
    scraper = CrossfitGymScraper()
    scraper.scrape()

