#!/usr/bin/env python2.7

import sys
from time import sleep
from requests import get
from bs4 import BeautifulSoup

# XXX Track which affiliate IDs get rejected and don't try them a second time
f = open('scraped.csv', 'wb')
f.write('"Name","URL","Address Line 1","new_line1","new_line2","Phone"\n')

rej = open('rejected.csv', 'wb')
rej.write('"ID"\n')

gyms = []

for i in xrange(1, 7397 + 1):
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
    gym['id'] = i
    gym['name'] = b.a.text
    gym['link'] = b.a['href']
    gym['addr'] = s.text
    gym['phone'] = p
    print gym
    gyms.append(gym)
    sleep(0.5)

f.close()
rej.close()
