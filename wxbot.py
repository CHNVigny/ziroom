#*-coding:utf-8-*-
from wxpy import *
import requests
import re
import time
import urllib2
import random
import thread
import threading
from bs4 import BeautifulSoup

headers=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},\
    {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},\
    {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},\
    {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},\
    {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}]

class ZiroomWxBot():
    def __init__(self):
        self.bot = Bot(qr_path="E:\Py_trade\ziroom\qr.png")
        self.bot.enable_puid('wxpy_puid.pkl')
        self.my_friend = self.bot.friends().search(u'王睿')[0]

    @staticmethod
    def success_login():
        print 'success login'

    def download_html(self, url):
        req = urllib2.Request(url, headers=headers[random.randint(0, len(headers) - 1)])
        source_code = urllib2.urlopen(req, timeout=10).read()
        #print source_code
        return source_code

    def parse(self, html):
        soup = BeautifulSoup(html, "html.parser")
        return soup.title.text

    def get_title(self, url):
         return self.parse(self.download_html(url))

    def ziroom_bot(self, url):

        session = requests.session()
        while 1:
            try:
                response_ziroom = session.get(url,
                                              headers={
                                                  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:48.0) Gecko/20100101 Firefox/48.0'})
                webpage_result = re.compile(r'title="配置中"')
                analyze_result = re.search(webpage_result, response_ziroom._content)
                if analyze_result:
                    print "still processing! wait!"
                    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    time.sleep(30)
                else:
                    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    print u"找到房源"
                    return 1
            except:
                print "fuck socket is closed, retry..."
            time.sleep(120)
            continue


    def monitor(self, url):
        #if self.ziroom_bot():
        title = self.get_title(url=url)
        text = u"%s%s%s" % (u"您的房子：", title, u"处于监控中")
        self.my_friend.send(text)
        if self.ziroom_bot(url=url) == 1:
            for i in xrange(20, 0, -1):
                self.my_friend.send(u"%s可用，尽快下手！回复“收到”可以取消提醒"%(title))
                @self.bot.register(self.my_friend)
                def msg_reply(msg):
                    if msg.text == u"收到":
                        msg.reply(u"已取消提醒")
                        i = 0
                time.sleep(30)
                if i == 1:
                    i += 19
            embed()





if __name__ == "__main__":
    urls = ["http://www.ziroom.com/z/vr/276223.html", "http://www.ziroom.com/z/vr/61279423.html"]
    zrbot = ZiroomWxBot()
    zrbot.monitor(url="http://www.ziroom.com/z/vr/276223.html")
    # def thread_monitor(bot, urls):
    #     for url in urls:
    #         try:
    #             t = threading.Thread(target=bot.monitor(), args=(url,))
    #             t.start()
    #         except:
    #             print "Error: unable to start thread"
    # thread_monitor(bot=zrbot, urls=urls)
    #try
    #def monitor(url):
        #:
        #thread.start_new_thread(monitor(), ("http://www.ziroom.com/z/vr/276223.html"))
        #thread.start_new_thread(monitor(), ("http://www.ziroom.com/z/vr/61279423.html"))
    #except:
        #print "Error: unable to start thread"
    #bot.start()
    #title = get_title(url="http://www.ziroom.com/z/vr/276223.html")
    #text = u"%s%s%s" % (u"您的房子：", title, u"处于监控中")
    #print text
    #download_html(url="http://www.ziroom.com/z/vr/276223.html")
    #for i in xrange(20, 0, -1):
    #    print i









