from .forms import BeginningDateForm, EndDateForm, LocationForm, PhoneForm, TextForm
from .weather import WeatherScraper
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from twilio.rest import TwilioRestClient
from .sms import SMSSender
import re

def home(request):

	## if the request is post, then initiate variables to get data from the forms
	if request.method == "POST":

		## retrieves phone and text data
		text = request.POST['text']
		phone = request.POST['phone_number']

		## retrieves initial date information
		beginning_year = request.POST['beginning_year']
		beginning_date = request.POST['beginning_date']
		beginning_month = request.POST['beginning_month']

		## formats initial date into format amenable for API call
		if beginning_year and beginning_month and beginning_date:
			beg = beginning_year + "-" + beginning_month + "-" + beginning_date
		
		## retrieves end date information
		end_year = request.POST['end_year']
		end_date = request.POST['end_date']
		end_month = request.POST['end_month']

		## formats end date into format amenable for API call
		if end_year and end_month and end_date:
			end = end_year + "-" + end_month + "-" + end_date

		## retrieves location 
		locale = request.POST['location']


		## if all variables are set then redirect to result
		## depending on decision to send a text, then redirect to appropriate URL
		if locale and beg and end:
			if text and phone:
				return HttpResponseRedirect(reverse('text_result', kwargs=({"locale": locale, "beg": beg, "end":end, "text": text, "phone": phone})))
			return HttpResponseRedirect(reverse('result', kwargs=({"locale": locale, "beg": beg, "end":end})))
		## if appropriate variables are not set then re render page
		else:
			return render(request, 'templates/precipcheck/home.html', {'beg_form': beg_form, 'end_form': end_form, 'location_form': location_form, 'phone_form': phone_form, 'text_form': text_form})


	else:
		## initial initiation of forms
		beg_form = BeginningDateForm()
		end_form = EndDateForm()
		location_form = LocationForm()
		phone_form = PhoneForm()
		text_form = TextForm()

	return render(request, 'templates/precipcheck/home.html', {'beg_form': beg_form, 'end_form': end_form, 'location_form': location_form, 'phone_form': phone_form, 'text_form': text_form})


def valid_date(date):

	## check to see if date is in format amenable for API call
	return re.match(r'\d{4}[-]\d{1,2}[-]\d{1,2}', date)
	
def give_value(item):

	## comparator function for sorting
	return item[1]

def text_result(request, locale, beg, end, text, phone):

	## check to see if beginning and end date are valid dates
	if valid_date(beg) and valid_date(end):

		## initiate weather scraper object
		## call function to retrieve precipitation data for given input
		## sort by precipitation totals
		weatherObject = WeatherScraper()
		result_list = weatherObject.returnTotals(locale, beg, end)
		result_list = sorted(result_list, key=give_value, reverse=True)
		
		## if text set to true
		## create text_message to send using 
		if text == "True":
			
			text_message = "Here are the precipitation totals at {location}".format(location = locale)
			text_message += "\n"
			for element in result_list:
				text_message += "The precipitation total on {date} was {value}.".format(date = element[0], value = element[1])
				text_message += "\n" 
			if phone:
				SMSObject = SMSSender()
				SMSObject.send_sms(phone, text_message)


	return render(request, 'templates/precipcheck/result.html', {'result_list': result_list, 'locale': locale, "beg": beg, "end": end})


def result(request, locale, beg, end):

	result_list = []
	## check to see if beginning and end date are valid dates
	## if so call function to retrieve precipitation data
	## sort by precipitation totals
	if valid_date(beg) and valid_date(end):
		weatherObject = WeatherScraper()
		result_list = weatherObject.returnTotals(locale, beg, end)
		result_list = sorted(result_list, key=give_value, reverse=True)
	
	return render(request, 'templates/precipcheck/result.html', {'result_list': result_list, 'locale': locale, "beg": beg, "end": end})

