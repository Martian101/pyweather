#!/usr/bin/env python
#encoding=utf-8
import urllib2
import socket
import time
import string
from xml.dom import minidom
# 这是Yahoo提供的天气预报的URL，其中w表示地区，u表示是摄氏度还是华氏度
WEATHER_URL = 'http://xml.weather.yahoo.com/forecastrss?w=%d&u=c'

global city
wuhan = 2163866
city = wuhan

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
	'28':'在白天有很多云',
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
    	dom = minidom.parse(urllib2.urlopen(url, timeout=5))
    except:
    	print "不能从url获得信息，断网了？"
    	net = False
    if net:
	wind = (dom.getElementsByTagName('yweather:wind'))[0] #风速
	humidi = (dom.getElementsByTagName('yweather:atmosphere'))[0] #湿度
	sun = (dom.getElementsByTagName('yweather:astronomy'))[0] #太阳升落      
    	node0 = (dom.getElementsByTagName('yweather:forecast'))[0] #当天信息
    	node1 = (dom.getElementsByTagName('yweather:forecast'))[1] #次日信息
    	return {
    		'wind':wind.getAttribute('speed'),
    		'humidi':humidi.getAttribute('humidity'),
    		'sunup':sun.getAttribute('sunrise'),
    		'sundown':sun.getAttribute('sunset'),
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
    		t = (string.atoi(w['high0']) + string.atoi(w['low0']))/2
    		td = string.atoi(w['high0']) - string.atoi(w['low0'])
    		tds = ''
    		ws = ''
    		if td > 10:
    			tds = '，还有今天温差很大！'
    		v = string.atoi(w['wind']) * 1.609344
    		if v > 28:
    			ws = ',注意今天刮大风！！'
    		f = string.atoi(w['humidi'])
    		ssd=(1.818*t+ 18.18)*(0.88 + 0.002*f)+(t- 32) / (45 -t)- 3.2 * v + 18.2
    		print ssd
    		ssd = round(ssd)
    		print ssd
    		if ssd > 90:
    			notion = '尼玛，这天气是要逆天了啊'
    		if ssd in range(86, 89):
    			notion = '估计可能会很热，太阳要把人晒死了'
    		if ssd in range(80, 86):
    			notion = '应该会感觉到很热，不太舒适，保持好心情:D'
    		if ssd in range(76, 80):
    			notion = '也许会感觉热，不知道会不会下雨-U-'
    		if ssd in range(71, 76):
    			notion = '据说将会是很暖和，很舒适的感觉~'
    		if ssd in range(59, 71):
    			notion = '他们说，这个范围会是最舒适的'
    		if ssd in range(51, 59):
    			notion = '天气转凉，请严防感冒～'
    		if ssd in range(39, 51):
    			notion = '听说今天感觉会蛮清凉的，但不很舒适，加衣服吧！'
    		if ssd in range(26, 39):
    			notion = '天气已经很冷了，保暖防寒啊，多喝水'
    		if ssd < 25:
    			notion = '。。。冷？总之是不爽，保重><'
        	weather0 = WEATHER_MAP[w['code0']]
        	weather1 = WEATHER_MAP[w['code1']]
        	logofile = WEATHER_PNG[w['code0']]
    	message = '%s 日出: %s  日落: %s 风速: %s\n今天也许会%s,最高气温%s,最低到%s\n明天也许会%s,最高气温%s,最低到%s\
    	\n%s%s%s' % (date, w['sunup'], w['sundown'], w['wind'], weather0, w['high0'], w['low0'],weather1, w['high1'], w['low1'], notion,ws,tds)
    else:
    	logofile = 'weather/xiaoxin.png'
    	message = '难道是断网了...自己去看看吧><'
	
    messlo = {
    	'天气信息':message,
    	'图片':logofile
    	}
    return messlo
