from django import forms
import re
from django.contrib.auth.models import User
from django.forms import ModelForm
from bticket.models import *
from bticket.utils.widgets import AdminImageWidget
from django.contrib.auth.forms import PasswordResetForm


class OnTheFlyTicketForm(ModelForm):
	class Meta:
		model = OnTheFlyTicket
		exclude = ('recovery_code', 'emission_date', 'qr_code')
	email = forms.EmailField(label = u'Email')

class RecoveryOnTheFlyTicketForm(forms.Form):
	recovery_code = forms.CharField(label = u'Recovery Code', max_length = 100)

class SentEmailFromRecoveryForm(forms.Form):
	email = forms.EmailField(label = u'Email')

class CheckNuberOfTripsForm(forms.Form):
	code = forms.CharField(label = u'Recovery Code', max_length = 100)

class UserProfileRegistrationForm(ModelForm):
	class Meta:
		model = UserProfile
		exclude = ('username')
	
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
	first_name = forms.CharField(label = u'First Name', max_length = 30)
	last_name = forms.CharField(label = u'Last Name', max_length = 30)
		
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

class UserProfileManagementForm(ModelForm):
	class Meta:
		model = UserProfile
		exclude = ('username')
	
	avatar = forms.FileField(widget = AdminImageWidget, required = False)
	email = forms.EmailField(label = u'Email')
	first_name = forms.CharField(label = u'First Name', max_length = 30)
	last_name = forms.CharField(label = u'Last Name', max_length = 30)

class BuyTicketForm(ModelForm):
	class Meta:
		model = Ticket
		exclude = ('user', 'qr_code', 'emission_date')
	
