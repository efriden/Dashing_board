from django.conf import settings
from urllib.request import urlopen
import json
import random
from dashing.widgets import NumberWidget
from dashing.widgets import GraphWidget
from dashing.widgets import ListWidget
from dashing.widgets import KnobWidget
import datetime
import TestApp.weather as w

class Weather(NumberWidget):
	def get_title(self):
		weatherData = w.getCurrentWeather()
		if (str(weatherData["weather"]).startswith("Ingen observation")==False):
			result = weatherData["weather"]
		else:
			result = "Temperatur i Uppsala"
		return result
	def get_value(self):
		weatherData = w.getCurrentWeather()
		return str(weatherData["temperature"]) + "\u00b0C"
	def get_updated_at(self):
		weatherData = w.getCurrentWeather()
		return str(weatherData["date"])
	def get_more_info(self):
		weatherData = w.getCurrentWeather()
		result = "Känns som " + str(int(weatherData["effectiveTemperature"])) + "\u00b0C."
		return result

class Forecast(GraphWidget):
	title = "2-dygnsprognos"
	def get_data(self):
		fcstData = w.create24hForecastData()
		return fcstData
	def get_more_info(self):
		fcstData = w.create24hForecastData()
		temps = [point["y"] for point in fcstData]
		return "Max: " + str(max(temps)) + "\u00b0C  Min: " + str(min(temps)) + "\u00b0C"

class Sun(KnobWidget):
	title = "▼"
	value = 100
	def get_data(self):
		t = w.getSunTimes()
		return {
				'angleArc': ((time2Minutes(t['sunset']) - time2Minutes(t['sunrise'])) / 1440 ) * 360,
				'fgColor': 'ffa73d',
				'angleOffset': ((time2Minutes(t['sunrise']) + time2Minutes(t['current'])) / 1440) * 360,
				'displayInput': False,
				'displayPrevious': False,
				'step': 10,
				'min': 0,
				'max': 100,
				'readOnly':True
				}
	
	#def get_data(self):
	#	t = w.getSunTimes()
	#	return {
	#			'angleArc': 360,
	#			'fgColor': "lightgreen",
	#			'angleOffset': ((time2Minutes(t['sunrise']) + time2Minutes(t['current'])) / 1440) * 360,
	#			'displayInput': False,
	#			'displayPrevious': False,
	#			'step': 10,
	#			'min': 0,
	#			'max': 1440,
	#			'readOnly':True
	#			}
	#def get_value(self):
	#	t = w.getSunTimes()
	#	return time2Minutes(t['sunset']) - time2Minutes(t['sunrise'])

	def get_more_info(self):
		t = w.getSunTimes()
		return 'Sol upp: {} -- Sol ned: {}'.format(t['sunrise'].strftime('%H:%M'),t['sunset'].strftime('%H:%M'))


class Trello(ListWidget):
	title = "Måltider:"
	def get_data(self):
		rot13 = str.maketrans( 
			"ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz", 
			"NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")
		#for food:
		idRot13 = '5p042np33s8nq686o86oqs70'
		
		#for the todolist:
		#idRot13 = '5or4o7613703151rp11rp087'

		tokenRot13 = '71qn6qsnr0r0362425s6n3316541725r6o82144841659p4s336655rq6790spo5'
		keyRot13 = '17255qn4o8r755q4s11pn295806nspo5'

		url = "https://api.trello.com/1/lists/{}/cards?fields=name&key={}&token={}".format(str.translate(idRot13, rot13),
																						str.translate(keyRot13, rot13),
																						str.translate(tokenRot13, rot13))

		a = [{ "label": "-", "value": key["name"]} for key in get_jsonparsed_data(url)]

		# result = random.sample(a, 5)

		return a
		
def get_jsonparsed_data(url):
    """
    Receive the content of ``url``, parse it as JSON and return the object.
	
    Parameters
    ----------
    url : str

    Returns
    -------
    dict
    """
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)

def time2Minutes(time):
	return time.hour * 60 + time.minute

