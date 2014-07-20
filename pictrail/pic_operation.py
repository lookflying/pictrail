from pictrail.models import User, Picture
from django.conf import settings
from datetime import datetime
from PIL import Image
import StringIO
def save_small_pic(pic_id, large_pic):
	large_file = StringIO.StringIO(large_pic.read())
	large_image = Image.open(large_file)
	(width, height) = large_image.size
	s_width = width
	s_height = height
	if width > height:
		ratio = height / settings.PIC_SMALL_LEN
		s_width = width / ratio
		s_height = settings.PIC_SMALL_LEN
	else:
		ratio = width / settings.PIC_SMALL_LEN
		s_height = height / ratio
		s_width = settings.PIC_SMALL_LEN
	small_image = large_image.resize((s_width, s_height), Image.ANTIALIAS)
	small_image.save(settings.PIC_SMALL_DIR + str(pic_id) + ".jpg")
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


def refresh_pic(longitude, latitude, scale, start_idx, count):
	rst = {}
	rst['result'] = 0
	try:
		start_pic = Picture.objects.get(id=start_idx)
	except Picture.DoesNotExist:
		return rst
	pass
	pics = Picture.objects.filter(time__lt=start_pic.time).order_by('-time')[:count]
#TODO geography search
	rst['picArray'] = []
	for pic in pics:
		rst['picArray'].append({'picIndex': pic.id, 'time': pic.time.__str__()})
	rst['picCount'] = len(rst['picArray'])
	rst['result'] = 1
	return rst

def pic_info(username, pic_idx):
	pass

def make_long_pic(count, pic_array):
	pass

def refresh_mine(username):
	pass

def refresh_collection(username):
	pass


