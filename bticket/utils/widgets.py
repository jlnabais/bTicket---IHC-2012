from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.conf import settings
from PIL import Image
import os

try:
	from sorl.thumbnail import get_thumbnail
	def thumbnail(image_path):
		t = get_thumbnail(image_path, "34x34", crop="center", quality=99, format='PNG')
		return u'<img src="%s" alt="%s" />' % (t.url, image_path)
except ImportError:
	def thumbnail(image_path):
		absolute_url = os.path.join(settings.MEDIA_URL, image_path)
		print absolute_url
		return u'<img src="%s" alt="%s" />' % (absolute_url, image_path)

class AdminImageWidget(AdminFileWidget):
	"""
	A FileField Widget that displays an image instead of a file path
	if the current file is an image.
	"""
	def render(self, name, value, attrs = None):
		print name, value, attrs
		output = []
		file_name = value
		if file_name:
			file_name = str(value)
			file_path = '%s%s' % (settings.MEDIA_URL, file_name)
			try:			# is image
				Image.open(os.path.join(settings.MEDIA_ROOT, file_name))
				output.append('<a target="_blank" href="%s">%s</a><br />%s <a target="_blank" href="%s">%s</a><br />%s ' % \
					(file_path, thumbnail(file_name), _('Currently:'), file_path, file_name, _('Change:')))
			except IOError: # not image
				output.append('%s <a target="_blank" href="%s">%s</a> <br />%s ' % \
					(_('Currently:'), file_path, file_name, _('Change:')))
			
		output.append(super(AdminFileWidget, self).render(name, value, attrs))
		return mark_safe(u''.join(output))