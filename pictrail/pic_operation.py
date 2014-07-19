from pictrail.models import User, Picture
from django.conf import settings
from datetime import datetime
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


