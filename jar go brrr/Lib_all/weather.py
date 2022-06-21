# weather.py
# Version 1.01, March 17, 2019

from tcpcom import HTTPClient
import json
import time

def _errorDict(status):
    return {'status' : status, 
            'temp' : 0, 
            'pressure' : 0,
            'humidity' : 0, 
            'temp_min' : 0, 
            'temp_max' : 0, 
            'description' : '-'}

def _getValues(data):
    data_dict = json.loads(data)
    code = data_dict[u'cod']
    if code == 401:  # int
        return _errorDict('Invalid authorization key')
    if code == u'404':  # string!
        return _errorDict('City not found')
    main = data_dict['main']
    status = 'OK'
    temp = main['temp']
    pressure = main['pressure']
    humidity = main['humidity']
    temp_min = main['temp_min']
    temp_max = main['temp_max']
    weather = data_dict['weather']
    weather_dict = weather[0]
    description = weather_dict['description']
    sys = data_dict['sys']
    sunrise = _getTime(sys['sunrise'])
    sunset = _getTime(sys['sunset'])
    datetime = _getDateTime(data_dict['dt'])
    return {'status' : status, 
            'temp' : _toCentigrades(temp), 
            'pressure' : pressure, 
            'humidity' : humidity, 
            'temp_min' : _toCentigrades(temp_min), 
            'temp_max' : _toCentigrades(temp_max), 
            'description' : description, # unicode
            'sunrise' : sunrise,
            'sunset' : sunset,
            'datetime' : datetime}

def request(city, key = '3344d39b56d7bf351f39ddb8a84961a4', lang = 'en'):
    data = {}
    data['q'] = city
    data['appid'] = key
    data['lang'] = lang  # used for description
    url = 'http://' + _host + '/data/2.5/weather'
    response = HTTPClient.getRequest(url, data)
    values = _getValues(response)
    return values

def _epochToDateTime(epoch):
    t = time.localtime(epoch)
    datetime = {'year' : t[0], 
                'month' : t[1],
                'day' : t[2],
                'hour' : t[3],
                'minute' : t[4],
                'second' : t[5],
                'weekday' : t[6],
                'yearday' : t[7]}
    return datetime

def _getTime(epoch):
    datetime = _epochToDateTime(epoch)
    hour = datetime['hour']
    min = datetime['minute']
    sec = datetime['second']
    return "%02d:%02d:%02d" %(hour, min, sec)

def _getDateTime(epoch):
    datetime = _epochToDateTime(epoch)
    weekday = _toDay(datetime['weekday'])
    year = datetime['year']
    month = datetime['month']
    day = datetime['day']
    hour = datetime['hour']
    min = datetime['minute']
    sec = datetime['second']
    return "%2s %4d-%02d-%02d %02d:%02d:%02d" %(weekday, year, month, day, hour, min, sec)

def _toDay(d):
    if d == 0:
        return "Mo"
    if d == 1:
        return "Tu"
    if d == 2:
        return "We"
    if d == 3:
        return "Th"
    if d == 4:
        return "Fr"
    if d == 5:
        return "Sa"
    if d == 6:
        return "Su"
    return ""
    
def _toCentigrades(kelvin):
    t = "%5.1f" %(kelvin - 273.15)
    return float(t)


_host = 'api.openweathermap.org'
