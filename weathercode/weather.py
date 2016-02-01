
##############################################################################################################################################################
################ Weather Information
################ Given a location, return weather information about the last five days
################ Input: A location
################ Output: Information about the weather
########################################################################################################################################################

from bs4 import BeautifulSoup
import requests
import lxml

class WeatherScraper(object):

	
	## define the comparator function for the sorting of the precipitation list
	def getValue(self, item):
		return item[1]

	## given a location, date, and enddate, return last 5 days of precipitation totals sorted in descending order by precipitation totals
	def returnTotals(self, location, beginning, end):
		
		## open up the response and pass as parameter for parsing
		url = "http://api.worldweatheronline.com/free/v2/past-weather.ashx"
		keyword_dict = {"key":"bd09fe006c6c3dac887f001fcdc9e", "q": location, "date": beginning, "enddate": end, "tp": "24"}
		url_response = requests.get(url, params=keyword_dict)

		
		## if successful, then start scraping data for relevant information
		result_list = self.processPage(url_response.text)

		## sort result_list by precipitation in ascending order
		result_list = sorted(result_list, key=self.getValue, reverse=True)

		return result_list

	## given a response, return 
	def processPage(self, response):
		
		## create result list
		result_list = []

		## format response into format amenable for parsing
		soup = BeautifulSoup(response, "xml")
		weather_list = soup.find_all('weather')

		## iterate through response's DOM
		## put date and precipitation for that day into a list
		## put that list into the final result list

		for day in weather_list:
			entry_list = []

			for tag in day.contents:
				if tag.name == "date":
					entry_list.append(tag.string)
				if tag.name == "hourly":

					for hourly_tag in tag:
						if hourly_tag.name == "precipMM":
							entry_list.append(float(hourly_tag.string))

			result_list.append(entry_list)

		# return final result list
		return result_list

if __name__ == "__main__":

	weatherObject = WeatherScraper()
	location = str(raw_input("Enter your location: "))
	date = str(raw_input("Enter the beginning date: "))
	enddate = str(raw_input("Enter the final date: "))

	print weatherObject.returnTotals(location, date, enddate)


