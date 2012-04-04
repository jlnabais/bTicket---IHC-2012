from django import forms
import re
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
	username = forms.CharField(label = u'Username', max_length = 30)
	email = forms.EmailField(label = u'Email')
	password1 = forms.CharField(
		label = u'Password',
		widget = forms.PasswordInput()
	)
	password2 = forms.CharField(
		label = u'Password(Again)',
		widget = forms.PasswordInput()
	)
	
	def clean_password2(self):
		if 'password1' in self.cleaned_data:
			password1 = self.cleaned_data['password1']
			password2 = self.cleaned_data['password2']
			if password1 == password2:
				return password2
		raise forms.ValidationError('Passwords do not match.')
		
	def clean_username(self):
		username = self.cleaned_data['username']
		if not re.search(r'^\w+$', username):
			raise froms.ValidationError('Usename can only contain '
				'alphanumeric characters and the underscore')
		try:
			User.objects.get(username = username)
		except:
			return username
		raise forms.ValidationError('Username is already taken.')

class OnTheFlyTicket(forms.Form):
	number_of_trips = forms.DecimalField(max_digits = 2 , decimal_places = 0)
	card_number = forms.DecimalField(max_digits = 16 , decimal_places = 0)
	