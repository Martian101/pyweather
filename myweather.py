#!/usr/bin/env python
# coding:utf-8
# Contributor:
#      zqzhao5        <zqzhao5@gmail.com>


#coding:utf-8
import urllib2
import time
import thread
import sys
import os
from xml.dom import minidom
from PyWapFetion import Fetion, send2self, send #通过短信发送信息
reload(sys)
sys.setdefaultencoding('utf-8')

global city
wuhan = 2163866
city = wuhan

try:
    import pygtk
    pygtk.require('2.0')
    import gtk
    gtk.gdk.threads_init()
except Exception:
    sys.exit(os.system(u'gdialog --title "WeathRepor GTK" --msgbox "\u8bf7\u5b89\u88c5 python-gtk2" 15 60'.encode(sys.getfilesystemencoding() or sys.getdefaultencoding(), 'replace')))
try:
    import pynotify
    pynotify.init('WeathRepor Info')
except ImportError:
    pynotify = None
try:
    import appindicator
except ImportError:
    appindicator = None


# 这是Yahoo提供的天气预报的URL，其中w表示地区，u表示是摄氏度还是华氏度
WEATHER_URL = 'http://xml.weather.yahoo.com/forecastrss?w=%d&u=c'

# 这是根据Yahoo提供的weather code和对应天气情况的映射表，这只是一小部分
WEATHER_MAP = {
        '3':'有阵雨',
	'4':'有阵雨',
	'5':'有雨夹雪',
	'6':'有雨夹雪',
	'7':'有雨夹雪',
	'8':'有冻雨',
	'9':'有毛毛细雨',
	'10':'有冻雨',
	'11':'下像淋浴一样的雨',
	'12':'下像淋浴一样的雨',
	'13':'有飘雪',
	'14':'有轻度飘雪',
	'15':'有大风吹雪',
	'16':'下雪',
	'17':'下冰雹',
	'18':'有雨夹雪',
	'19':'有雨夹雪',
	'20':'有雾',
	'21':'是阴霾漫天',
	'22':'是大雾如烟',
	'23':'晚上时候天气不太好',
	'24':'有大风',
        '25':'很冷',
	'26':'有很多云',
	'27':'在晚上有很多云',
	'28':'在白天很多云',
	'29':'在晚上有一些云',
	'30':'在白天有一些云',
	'31':'晚上的天空很干净',
	'32':'是晴天',
	'33':'晚上天气不错！',
	'34':'天气不错，晴朗的很！',
	'35':'下雨，而且雨里有冰雹',
	'36':'感觉真是太热了',
	'37':'就下一阵雷阵雨',
	'38':'下雷阵雨，而且断断续续',
	'39':'下雷阵雨，而且断断续续',
	'40':'下断断续续的雷阵小雨',
	'41':'下很严重的大雪！！',
	'42':'看到零零落落的雪花会像淋浴一样',
	'43':'见到很大的大雪！！',
	'44':'看到部分时候天上会有云',
	'45':'下一阵雷阵小雨',
	'46':'看到零零落落的雪花会像淋浴一样',
	'47':'就下一阵雷阵雨',
	'3200':'巴拉巴拉'
        }
        
WEATHER_PNG = {
	'3':'weather/tstorm2.png',
	'4':'weather/tstorm1.png',
	'5':'weather/sleet.png',
	'6':'weather/sleet.png',
	'7':'weather/sleet.png',
	'8':'weather/sleet.png',
	'9':'weather/showers1.png',
	'10':'weather/sleet.png',
	'11':'weather/shower1.png',
	'12':'weather/shower1.png',
	'13':'weather/snow1.png',
	'14':'weather/snow1.png',
	'15':'weather/snow2.png',
	'16':'weather/snow3.png',
	'17':'weather/hail.png',
	'18':'weather/sleet.png',
	'19':'weather/sleet.png',
	'20':'weather/fog.png',
	'21':'weather/mist.png',
	'22':'weather/fog.png',
	'23':'weather/tstorm2.png',
	'24':'weather/wind.png',
	'25':'weather/cold.png',
	'26':'weather/cloudy1.png',
	'28':'weather/cloudy3.png',
	'29':'weather/cloudy1_night.png',
	'30':'weather/cloudy4.png',
	'31':'weather/sunny_night.png',
	'32':'weather/sunny.png',
	'33':'weather/sunny_night.png',
	'34':'weather/sunny.png',
	'35':'weather/sleet.png',
	'36':'weather/sunny.png',
	'37':'weather/tstorm1.png',
	'38':'weather/tstorm1.png',
	'39':'weather/tstorm1.png',
	'40':'weather/tstorm1.png',
	'41':'weather/snow5.png',
	'42':'weather/tstorm1.png',
	'43':'weather/snow5.png',
	'44':'weather/cloudy2.png',
	'45':'weather/tstorm1.png',
	'46':'weather/snow1.png',
	'47':'weather/tstorm1.png',
	'3200':'weather/puzzled.png'
	}
# Yahoo的提供的信息很多，连日出日落时间都有...

def weather_for_zip(zip_code):
    url = WEATHER_URL % zip_code
    net = True
    try:
    	dom = minidom.parse(urllib2.urlopen(url))
    except:
    	print "不能从url获得信息，断网了？"
    	net = False
    if net:
    	node0 = (dom.getElementsByTagName('yweather:forecast'))[0]
    	node1 = (dom.getElementsByTagName('yweather:forecast'))[1]

    	return {
        	'low0': node0.getAttribute('low'),
        	'high0': node0.getAttribute('high'),
        	'code0': node0.getAttribute('code'),
        	'low1': node1.getAttribute('low'),
        	'high1': node1.getAttribute('high'),
        	'code1': node1.getAttribute('code')
    	}
    return net
# Moonya会调用这个函数，传进来的是一个地区参数
def tell_weather(code):
    date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    w = weather_for_zip(code)
    if w != False:
   	weather = ''
    	global logofile
    	if w['code0'] not in WEATHER_MAP:
        	weather = '有点危险～=～'
        	logofile = 'weather/xiaoxin.png'
    	else:
        	weather0 = WEATHER_MAP[w['code0']]
        	weather1 = WEATHER_MAP[w['code1']]
        	logofile = WEATHER_PNG[w['code0']]
    	message = '%s\n今天也许会%s,最高气温有%s,最低到%s\n明天也许会%s,最高气温有%s,最低到%s\
    	\n好吧，我还不够智能><,鬼知道你该多穿衣服还是少出门...不过天气预报是准的~' \
            	% (date, weather0, w['high0'], w['low0'],weather1, w['high1'], w['low1'])
    else:
    	logofile = 'weather/xiaoxin.png'
    	message = '难道是断网了...自己去看看吧><'
	
    messlo = {
    	'天气信息':message,
    	'图片':logofile
    	}
    return messlo
    
    
def spawn_later(seconds, target, *args, **kwargs):
    def wrap(*args, **kwargs):
        import time
        time.sleep(seconds)
        return target(*args, **kwargs)
    return thread.start_new_thread(wrap, args, kwargs)
    
class WeathReporGTK:
    global message
    message = tell_weather(city)
    fail_message = u'出错啦～'

    def __init__(self, window):
        self.window = window
        
	spawn_later(0.5, self.show_startup_notify)
	
        logo_filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), message['图片'])

        if appindicator:
            self.trayicon = appindicator.Indicator('WeathRepor', 'indicator-messages', appindicator.CATEGORY_APPLICATION_STATUS)
            self.trayicon.set_status(appindicator.STATUS_ACTIVE)
            self.trayicon.set_attention_icon('indicator-messages-new')
            self.trayicon.set_icon(logo_filename)
            self.trayicon.set_menu(self.make_menu())
        else:
            self.trayicon = gtk.StatusIcon()
            self.trayicon.set_from_file(logo_filename)
            self.trayicon.connect('popup-menu', lambda i, b, t: self.make_menu().popup(None, None, gtk.status_icon_position_menu, b, t, self.trayicon))
            self.trayicon.set_visible(True)

    def make_menu(self):
        menu = gtk.Menu()
        itemlist = [('Show Info', self.on_show),
        	    ('Update',self.on_update),
                    ('Quit', gtk.main_quit)]
        for text, callback in itemlist:
            item = gtk.MenuItem(text)
            item.connect('activate', callback)
            item.show()
            menu.append(item)
        menu.show()
        return menu

    def show_notify(self, message=None, timeout=None):
        if pynotify and message:
            notification = pynotify.Notification('Weather Info', message['天气信息'])
            notification.set_hint('x', 200)
            notification.set_hint('y', 400)
            if timeout:
                notification.set_timeout(timeout)
            notification.show()

    def show_startup_notify(self):
        	self.show_notify(message, timeout=0)

    def on_show(self, widget, data=None):
        self.show_notify(message, timeout=0)
        
    def on_update(self, widget, data=None):
    	message = tell_weather(city)
    	print '啊哈，天气更新成功啦！'
        self.show_notify(message,timeout=0)

def main():
    window = gtk.Window()
    WeathReporGTK(window)
    gtk.main()    
    
if __name__ == '__main__':
    print weather_for_zip(city)
    print tell_weather(city)
    main()
