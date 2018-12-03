from django.conf import settings
from urllib.request import urlopen
import json
from dashing.widgets import NumberWidget
from dashing.widgets import GraphWidget
from dashing.widgets import ListWidget
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



class Trello(ListWidget):
	title = "Lista!"
	def get_data(self):
		rot13 = str.maketrans( 
			"ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz", 
			"NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")
		str.translate("Hello World! + Uryyb Jbeyq!", rot13)
		idRot13 = '5or4o7613703151rp11rp087'
		tokenRot13 = '71qn6qsnr0r0362425s6n3316541725r6o82144841659p4s336655rq6790spo5'
		keyRot13 = '17255qn4o8r755q4s11pn295806nspo5'

		url = "https://api.trello.com/1/lists/{}/cards?fields=name&key={}&token={}".format(str.translate(idRot13, rot13),
																						str.translate(keyRot13, rot13),
																						str.translate(tokenRot13, rot13))

		return [{ "label": key["name"], "value": ""} for key in get_jsonparsed_data(url)]
		
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


