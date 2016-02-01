from django import forms
## forms to handle input for precipitation check

## form for beginning date
class BeginningDateForm(forms.Form):
	beginning_year = forms.ChoiceField(choices=[(2016,"2016"), (2015, "2015")])
	beginning_month = forms.ChoiceField(choices=[(1, "01"), (12,"12") , (11,"11")])
	beginning_date = forms.ChoiceField(choices=[(x,x) for x in range(1,32)])

## form for end date
class EndDateForm(forms.Form):
	end_year = forms.ChoiceField(choices=[(2016, "2016"), (2015,"2015")])
	end_month = forms.ChoiceField(choices=[(1, "01"), (12,"12") , (11,"11")])
	end_date = forms.ChoiceField(choices=[(x,x) for x in range(1,32)])

## form for location
class LocationForm(forms.Form):
	location = forms.CharField(max_length = 100)

## form for phones
class PhoneForm(forms.Form):
	phone_number = forms.CharField(max_length = 100)

## form for text forms
class TextForm(forms.Form):
	text = forms.ChoiceField(choices=[(False, "No"), (True, "Yes")])