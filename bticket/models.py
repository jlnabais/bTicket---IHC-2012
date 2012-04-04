from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class QRCode(models.Model):
	qr_code = models.CharField(max_length = 400, unique = True) 

class Ticket(models.Model):
	#number for the annymous ticket buyers get it from recovery
	number = models.DecimalField(max_digits = 12, decimal_places = 0)
	user = models.ForeignKey(User)
	qr_code = models.ForeignKey(QRCode)
	emission_date = models.DateField(default = datetime.datetime.today)
	number_of_trips = models.DecimalField(max_digits = 12, decimal_places = 0)

class Pass(models.Model):
	number = models.DecimalField(max_digits = 12, decimal_places = 0)
	user = models.ForeignKey(User)
	qr_code = models.ForeignKey(QRCode)
	emission_date = models.DateField(default = datetime.datetime.today)
	expiration_date = models.DateField(default = datetime.datetime.today)

class BillingAccount(models.Model):
	Card_Number = models.DecimalField(max_digits = 16, decimal_places = 0)
	NIB = models.DecimalField(max_digits = 21, decimal_places = 0)
	IBAN =  models.DecimalField(max_digits = 34, decimal_places = 0)
	SWIFT = models.DecimalField(max_digits = 11, decimal_places = 0)
	user = models.ForeignKey(User)

