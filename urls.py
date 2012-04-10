import os
from django.conf.urls.defaults import *
from bticket.views import *
from django.views.generic.simple import direct_to_template
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

site_media = os.path.join(
	os.path.dirname(__file__), 'site_media'
)

urlpatterns = patterns('',
	(r'^$', main_page),
	(r'^user/$', user_page),
	(r'^login/$', 'django.contrib.auth.views.login'),
	(r'^logout', logout_page),
	(r'^register/$', register_page),
	(r'^register/success/$', direct_to_template, {'template': 'registration/register_success.html'}),
	(r'^ontheflyticket/success/$', direct_to_template, {'template': 'purchase/onthefly_success.html'}),
	(r'^site_media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	(r'^qrcode/(\w+)/$', generate_qrcode),
    (r'^recovery/(\w+)/$', send_email_from_recovery),
	(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/site_media/favicon.ico'}),
	
)