from django.conf import settings
from urllib.request import urlopen
import json
from dashing.widgets import NumberWidget
from dashing.widgets import GraphWidget
from dashing.widgets import ListWidget
import TestApp.weather as w

class Weather(NumberWidget):
	title = "Temperatur i Uppsala"
	def get_value(self):
		weatherData = w.getCurrentWeather()
		return str(weatherData["temperature"]) + "\u00b0C"
	def get_updated_at(self):
		weatherData = w.getCurrentWeather()
		return str(weatherData["date"])
	def get_more_info(self):
		weatherData = w.getCurrentWeather()
		result = "Känns som " + str(int(weatherData["effectiveTemperature"])) + "\u00b0C."
		if (str(weatherData["weather"]).startswith("Ingen observation")==False):
			result += " " + weatherData["weather"]
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
		id = "5be4b7613703151ec11ec087"
		token = "71da6dfae0e0362425f6a3316541725e6b82144841659c4f336655ed6790fcb5"
		key = "17255da4b8e755d4f11ca295806afcb5"

		url = "https://api.trello.com/1/lists/{}/cards?fields=name&key={}&token={}".format(id, key, token)

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


