#!/usr/bin/env python

import re
import os
import sys
import json
import errno
import django
import urlparse

from time import sleep
from pprint import pprint
from requests import get
from bs4 import BeautifulSoup
from email_scraper import EmailScraper
from soup_requestor import SoupRequestor

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), 'scraper/')))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), 'scraper/scraper/')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
django.setup()

from django.core.exceptions import ObjectDoesNotExist
from crossfit_scraper.models import *

class CrossfitScraper(object):
    def __init__(self):
        self.url = "http://map.crossfit.com/affinfo.php?a={}&t=0"
        self.email_scraper = EmailScraper()
        self.sreq = SoupRequestor()

    def get_gym(self, affid):
        u = self.url.format(affid)
        r,s = self.sreq.get(u)
        return (r,s)

    def set_gym_from_response(self, affid, r, s):
        if s.b is None:
            return

        b = s.b.extract()
        p = s.contents[-1].extract()

        if b.a is None:
            return

        addr = ' '.join(['%s' % x for x in s.findAll(text=True)])
        addr = ' '.join(addr.split())

        gym = CrossfitGym()
        gym.name = b.a.text
        gym.link = b.a['href']
        gym.addr = addr
        gym.affid = affid
        gym.phone = p
        gym.save()
        
    def get_gym_list(self):
        for i in xrange(1, 3500):
            if CrossfitGym.objects.filter(affid=i).exists():
                continue

            print 'Getting info for %d' % i
            r,s = self.get_gym(i)
            if r is None:
                continue

            self.set_gym_from_response(i, r, s)
            sleep(0.75)

    def get_gym_email(self, gym):
        if not gym.email and gym.checked_email is False:
            print 'Getting email for %s' % gym
            e = self.email_scraper.scrape_email(gym.link)
            if e:
                gym.email = e
                gym.save()

            gym.checked_email = True
            gym.save()

    def get_gym_emails(self):
        for gym in CrossfitGym.objects.all():
            self.get_gym_email(gym)

    def scrape(self):
        self.get_gym_list()
        self.get_gym_emails()

if __name__ == '__main__':
    scraper = CrossfitScraper()
    scraper.scrape()

