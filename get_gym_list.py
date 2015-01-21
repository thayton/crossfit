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
def get_gym_list(gyms):
#    for i in xrange(1, 7397 + 1):
    for i in xrange(1, 5):
        if str(i) in gyms:
            continue

        u = "http://map.crossfit.com/affinfo.php?a={}&t=0".format(i)
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
        gym['addr'] = s.text
        gym['phone'] = p
        gyms[str(i)] = gym
        sleep(0.5)

    return gyms

def save_gyms(gyms):
    with open('gyms.json', 'w+') as f:
        json.dump(gyms, f)

def load_gyms():
    gyms = {}

    try:
        f = open('gyms.json', 'r')
    except IOError as e:
        if e.errno == errno.ENOENT:
            pass
    else:
        d = f.read()
        if len(d):
            gyms = json.loads(d)

    return gyms
    
def get_gym_email(gym):
    if gym.get('email', False):
        return

    r = get(gym['link'])
    s = BeautifulSoup(r.text)
    r = re.compile(r'mailto:\b([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4})\b', re.I)
    a = s.find('a', href=re.compile(r))

    if a:
        m = re.search(r, a['href'])
        if len(m.groups()):
            gym['email'] = m.group(1)

    print a
    
if __name__ == '__main__':
    gyms = load_gyms()
    get_gym_list(gyms)

    for id,gym in gyms.items():
        get_gym_email(gym)
        print id,gym

    save_gyms(gyms)

