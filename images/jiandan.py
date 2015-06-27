# encoding: utf-8
#my blog:http://www.lylinux.org

import urllib2
from BeautifulSoup import BeautifulSoup
import socket

baseurl = "http://jandan.net/ooxx/"

def user_agent(url):
    req_header = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req_timeout = 20
    try:
        req = urllib2.Request(url,None,req_header)
        page = urllib2.urlopen(req,None,req_timeout)
    except urllib2.URLError as e:
        print e.message
    except socket.timeout as e:
        user_agent(url)
    return page

def page_loop(pageid):
   # url = baseurl+'?p=%s'%page
    url = baseurl + 'page-%s'%pageid
    print url
    page = user_agent(url)
    soup = BeautifulSoup(page)
    total_img = 0
    img = soup.findAll(['img'])
    for myimg in img:
        link = myimg.get('src')
        total_img += 1
        print link
      #  content2 = urllib2.urlopen(link).read()
        content2 = user_agent(link).read()
        with open(u'D:\\var\\data\\pictures\\mm\\'+link[-11:],'wb') as code:   
            code.write(content2)
    print total_img
    return total_img

page_start = 1000
page_stop = 1100
total = 0
for i in range(page_start,page_stop):
    total+=page_loop(i)

print total

