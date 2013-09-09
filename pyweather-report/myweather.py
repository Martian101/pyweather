#!/usr/bin/env python
# coding:utf-8
# Contributor:
#      zqzhao5        <zqzhao5@gmail.com>


#coding:utf-8
import urllib
import time
import thread
import sys
import os
from xml.dom import minidom
reload(sys)
sys.setdefaultencoding('utf-8')

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
        '3':'阵雨',
	'4':'阵雨',
	'5':'雨夹雪',
	'6':'雨夹雪',
	'7':'雨夹雪',
	'8':'冻雨',
	'9':'毛毛细雨',
	'10':'冻雨',
	'11':'淋浴一样的雨',
	'12':'淋浴一样的雨',
	'13':'飘雪',
	'14':'轻度飘雪',
	'15':'大风吹雪',
	'16':'雪',
	'17':'冰雹',
	'18':'雨夹雪',
	'19':'雨夹雪',
	'20':'雾',
	'21':'阴霾漫天',
	'22':'大雾如烟',
	'24':'有大风',
        '25':'很冷',
	'26':'有很多云',
	'28':'白天大部分有云',
	'30':'白天一部分有云',
	'32':'晴天',
	'34':'天气不错，晴朗的很！',
	'35':'雨里有冰雹',
	'36':'太热了',
	'37':'就一阵雷阵雨',
	'38':'雷阵雨断断续续',
	'39':'雷阵雨断断续续',
	'40':'雷阵小雨断断续续',
	'41':'很严重的大雪！！',
	'42':'零零落落的雪花会像淋浴一样',
	'43':'很严重的大雪！！',
	'44':'部分时候天上会有云',
	'45':'雷阵小雨',
	'46':'零零落落的雪花会像淋浴一样',
	'47':'就一阵雷阵雨',
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
	'26':'weather/cloudy1.png',
	'28':'weather/cloudy3.png',
	'30':'weather/cloudy4.png',
	'32':'weather/sunny.png',
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
# 但是对于我来说，我只关心温度，和天气是晴朗还是下雨仅此而已...
def weather_for_zip(zip_code):
    url = WEATHER_URL % zip_code
    dom = minidom.parse(urllib.urlopen(url))
    node = (dom.getElementsByTagName('yweather:forecast'))[0]

    return {
        'low': node.getAttribute('low'),
        'high': node.getAttribute('high'),
        'code': node.getAttribute('code')
    }

# Moonya会调用这个函数，传进来的是一个地区参数
def tell_weather(code):
    w = weather_for_zip(code)
    weather = ''
    global logofile
    if w['code'] not in WEATHER_MAP:
        weather = '有点危险～=～'
        logofile = 'weather/puzzled.png'
    else:
        weather = WEATHER_MAP[w['code']]
        logofile = WEATHER_PNG[w['code']]
    date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    message = '%s\n今天也许会是%s,最高气温有%s,最低到%s。好吧，我还不够智能><,鬼知道你该多穿衣服还是少出门...不过天气预报是准的~' \
            % (date, weather, w['high'], w['low'])
    return message
    
message = tell_weather(2163866)   

def spawn_later(seconds, target, *args, **kwargs):
    def wrap(*args, **kwargs):
        import time
        time.sleep(seconds)
        return target(*args, **kwargs)
    return thread.start_new_thread(wrap, args, kwargs)
    
class WeathReporGTK:
    global message
    message = tell_weather(2163866)
    fail_message = u'自己去看天吧～'

    def __init__(self, window):
        self.window = window
        
	spawn_later(0.5, self.show_startup_notify)
	
        logo_filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), logofile)

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
            notification = pynotify.Notification('Weather Info', message)
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
        gtk.main_iteration()
        print '啊哈，天气更新成功啦！'
        print message
        self.show_notify(message,timeout=0)
    while gtk.events_pending():
        gtk.main_iteration_do(False)

def main():
    window = gtk.Window()
    WeathReporGTK(window)
    gtk.main()    
    
if __name__ == '__main__':
        #2163866这是武汉的Code，其他的需要上Yahoo一个一个搜，好像没有提供专门的映射表
    city = 2163866
    print weather_for_zip(city)
    print tell_weather(city)
    main()
