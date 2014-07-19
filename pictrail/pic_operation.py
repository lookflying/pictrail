from pictrail.models import User, Picture
from django.conf import settings
from datetime import datetime
from PIL import Image
import StringIO
def save_small_pic(pic_id, pic_large):
	file_large = StringIO.StringIO(pic_large.read())
	image_large = Image.open(file_large)
	(width, height) = image_large.size
	width_s = width
	height_s = height
	if width > height:
		ratio = height / settings.PIC_SMALL_LEN
		width_s = width / ratio
		height_s = settings.PIC_SMALL_LEN
	else:
		ratio = width / settings.PIC_SMALL_LEN
		height_s = height / ratio
		width_s = settings.PIC_SMALL_LEN
	image_small = image_large.resize((width_s, height_s), Image.ANTIALIAS)
	image_small.save(settings.PIC_SMALL_DIR + str(pic_id) + ".jpg")
	pass


def publish_pic(username, longitude, latitude, location, detail, photo):
	try:
		user = User.objects.get(name=username)
	except User.DoesNotExist:
		return False
	pic = Picture.objects.create(user=user, time=datetime.now(), location=location, longitude=longitude, latitude=latitude, detail=detail)
	with open(settings.PIC_LARGE_DIR + str(pic.id) + ".jpg", 'wb+') as dest:
		for chunk in photo.chunks():
			dest.write(chunk)
		dest.close()
	photo.seek(0)
	save_small_pic(pic.id, photo)
	return True


def refresh_pic(longtitude, latitude, scale, start_idx, count):
	pass

def pic_info(username, pic_idx):
	pass

def make_long_pic(count, pic_array):
	pass

def refresh_mine(username):
	pass

def refresh_collection(username):
	pass


