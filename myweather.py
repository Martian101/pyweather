#!/usr/bin/env python
# coding:utf-8
# Contributor:
#      zqzhao5        <zqzhao5@gmail.com>



import time
import thread
import sys
import os
from getweather import *
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
	
	spawn_later(3600*2, self.auto_update)
	
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
        itemlist = [('Show Weather', self.on_show),
        	    ('Update Weather',self.on_update),
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
    	os.execl("/usr/bin/python", "python", 'myweather.py')
    	print '天气更新成功！'
    def auto_update(self):
    	os.execl("/usr/bin/python", "python", 'myweather.py')

def main():
    window = gtk.Window()
    WeathReporGTK(window)
    gtk.main()    

if __name__ == '__main__':
    print weather_for_zip(city)
    print tell_weather(city)
    main()
