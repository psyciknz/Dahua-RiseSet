import sqlite3
import json
import urllib
import time
import datetime
import calendar

WEATHER_DATA_API_KEY='API_KEY'          #sign up to openweathermap.org and obtain an APIkey
WEATHER_DATA_LOCATION='city_id_number'  #get the city ID by searching for you city.  ID in url http://openweathermap.org/city/2179537
USERPASS = 'camerauser:camerapassword'

#For mulitple cameras enter as below.
#SERVERS = ["cam-garage.lan", "cam-backdoor.lan", "cam-frontdoor.lan"]

#for nvr enter the server channels as well.
SERVERS = ["cam-nvr.lan"]
SERVER_CHANNELS = [0,1,2,3]

#offset to add to sunrise or minus from sunrise.  Since there is enough light just before or after sunrise/sunset.
OFFSET = 15



GET_URL = 'http://{0}@{1}/cgi-bin/configManager.cgi?action=getConfig&name=VideoInOptions[{2}].NightOptions'
WEATHER_DATA_URL = 'http://api.openweathermap.org/data/2.5/weather?id={0}&appid={1}&units=metric'.format(WEATHER_DATA_LOCATION,WEATHER_DATA_API_KEY)

#You shouldn't need to change this unless the API does.
SET_SUNRISE_SUNSET = 'http://{0}@{1}/cgi-bin/configManager.cgi?action=setConfig&VideoInOptions[{6}].NightOptions.SunriseHour={2}&VideoInOptions[{6}].NightOptions.SunriseMinute={3}&VideoInOptions[{6}].NightOptions.SunsetHour={4}&VideoInOptions[{6}].NightOptions.SunsetMinute={5}'



def get_data():
    """get weather data from openweathermap"""
    print 'Getting Weather data for sunrise runset: %s' % WEATHER_DATA_URL
    response = urllib.urlopen(WEATHER_DATA_URL)
    data = json.loads(response.read())
    print 'Weather data retrieved: %s' % data

    temp = data['main']['temp']
    pressure = data['main']['pressure']
    temp_min = data['main']['temp_min']
    temp_max = data['main']['temp_max']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    try:
        wind_gust = data['wind']['gust']
    except KeyError:
        wind_gust = None
    wind_deg = data['wind']['deg']
    clouds = data['clouds']['all']
    try:
        rain = data['rain']['3h']
    except KeyError:
        rain = None
    try:
        snow = data['snow']['3h']
    except KeyError:
        snow = None
    weather_id = data['weather'][0]['id']
    sunrise = data['sys']['sunrise']
    sunset = data['sys']['sunset']
    print 'Obtained sunrise and sunset times'
    print 'Sunrise (local): %s' % datetime.datetime.fromtimestamp(sunrise).strftime('%Y-%m-%d %H:%M:%S')
    print 'Sunset: (local): %s' % datetime.datetime.fromtimestamp(sunset).strftime('%Y-%m-%d %H:%M:%S')

    return [temp, pressure, temp_min, temp_max, humidity, wind_speed, wind_gust, wind_deg, clouds, rain, snow,
            weather_id, sunrise, sunset]


def update_dahua(data):
    """http://user:pass@cameraip/cgi-bin/configManager.cgi?action=getConfig&name=VideoInOptions[0].NightOptions"""
    sunriseunix = data[12]
    sunsetunix = data[13]
    sunrise = datetime.datetime.fromtimestamp(data[12])
    sunset = datetime.datetime.fromtimestamp(data[13])
    sunrise = sunrise - datetime.timedelta(minutes=OFFSET)
    sunset = sunset + datetime.timedelta(minutes=OFFSET)
    print 'Sunrise with enough light (-%s mins) %s' % (OFFSET,sunrise.strftime('%Y-%m-%d %H:%M:%S'))
    print 'Sunset with enough light (+%s mins) %s' % (OFFSET,sunset.strftime('%Y-%m-%d %H:%M:%S'))

    for server in SERVERS:
	    for channel in SERVER_CHANNELS:
        	updateurl = SET_SUNRISE_SUNSET.format(USERPASS,server,sunrise.strftime('%H'),sunrise.strftime('%M'),sunset.strftime('%H'), sunset.strftime('%M'),channel)
		print updateurl
        	response = urllib.urlopen(updateurl)
	        dahua_update = response.read()
	        print 'Result of Dahua update: %s ' % dahua_update
	        time.sleep(5)
	        response = urllib.urlopen(GET_URL.format(USERPASS,server,channel))
	        dahua_data =  response.read()
	        print 'After Updating {0} Dahua video parms'.format(server)
	        print dahua_data

def main():
    data = get_data()
    time.sleep(2)
    update_dahua(data)




if __name__ == '__main__':
    main()
