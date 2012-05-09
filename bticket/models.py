from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class UserProfile(models.Model):
    user   = models.OneToOneField(User)
    avatar = models.ImageField(upload_to = 'profile_avatars')

class QRCode(models.Model):
	qr_code = models.CharField(max_length = 400, unique = True)

class Ticket(models.Model):
	user = models.ForeignKey(UserProfile)
	qr_code = models.ForeignKey(QRCode)
	emission_date = models.DateField(default = datetime.datetime.today)
	number_of_trips = models.DecimalField(max_digits = 2, decimal_places = 0)

class Pass(models.Model):
	user = models.ForeignKey(UserProfile)
	qr_code = models.ForeignKey(QRCode)
	emission_date = models.DateField(default = datetime.datetime.today)
	expiration_date = models.DateField(default = datetime.datetime.today)

class BillingAccount(models.Model):
	card_number = models.DecimalField(max_digits = 16, decimal_places = 0)
	user = models.ForeignKey(UserProfile)

class OnTheFlyTicket(models.Model):
	recovery_code = models.CharField(blank = True, max_length = 100, unique = True)
	qr_code = models.ForeignKey(QRCode)
	emission_date = models.DateField(default = datetime.datetime.today)
	number_of_trips = models.DecimalField(max_digits = 12, decimal_places = 0)
	card_number = models.DecimalField(max_digits = 16, decimal_places = 0)

