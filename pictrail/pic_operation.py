from pictrail.models import User, Picture, Raised, Comment, Collection, LongPicture, SelectedPicture
from django.conf import settings
from datetime import datetime
from PIL import Image
import StringIO
import sys
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
	rst = {}
	rst['result'] = 0
	try:
		pic = Picture.objects.get(id=pic_idx)
	except Picture.DoesNotExist:
		return rst
	rst['username'] = pic.user.name
	rst['location'] = pic.location
	rst['time'] = pic.time.__str__()
	rst['detail'] = pic.detail
	rst['raiseCount'] = pic.raise_count
	if len(Raised.objects.filter(user__name=username, pic=pic)) > 0:
		rst['isRaised'] = 1
	else:
		rst['isRaised'] = 0
	comments = Comment.objects.filter(pic=pic)
	rst['commentArray'] = []
	for comment in comments:
		rst['commentArray'].append({'username': comment.user.name, 'comment': comment.content, 'time': comment.time.__str__()})
	rst['commentCount'] = len(rst['commentArray'])
	rst['result'] = 1	
	return rst

def concatenate_pic(pic_id_list, long_pic_id):
	min_width = settings.PIC_LONG_MAX_WIDTH
	image_list = []
	resized_image_list = []
	total_height = 0
	try:
		for pic_id in pic_id_list:
			ori_image = Image.open(settings.PIC_LARGE_DIR + str(pic_id) + ".jpg")
			(width, height) = ori_image.size
			if width < min_width:
				min_width = width;
			image_list.append(ori_image)
		for image in image_list:
			(width, height) = image.size
			resized_height = height * min_width / width
			resized_image_list.append(image.resize((min_width, resized_height), Image.ANTIALIAS))
			total_height += resized_height
		long_image = Image.new("RGB", (min_width, total_height))
		cur_height = 0
		for resized_image in resized_image_list:
			long_image.paste(resized_image, (0, cur_height))
			cur_height += resized_image.size[1]#add height to cur_height
		long_image.save(settings.PIC_LONG_DIR + str(long_pic_id) + ".jpg")
		return True 
	except Exception, e:
		raise e	
		return False


def make_long_pic(username, count, pic_array):
	rst = {}
	rst['result'] = 0
	try:
		user = User.objects.get(name=username)
	except User.DoesNotExist:
		return rst
	pic_id_list = range(len(pic_array))
	long_pic = LongPicture.objects.create(user=user, time=datetime.now())
	try:
		for item in pic_array:
			pic_id_list[item['no'] - 1] = item['picIndex']#start from 1	
			SelectedPicture.objects.create(pic=Picture.objects.get(id=item['picIndex']), long_pic=long_pic)
		if concatenate_pic(pic_id_list, long_pic.id):
			rst['result'] = 1
			rst['picIndex'] = long_pic.id
			return rst
	except Exception, e:
		if settings.DEBUG:
			raise e	
		return rst
	return rst
	
def refresh_mine(username):
	rst = {}
	pics = Picture.objects.filter(user__name=username)
	rst['picArray'] = []
	for pic in pics:
		rst['picArray'].append({'picIndex': str(pic.id), 'time': pic.time.__str__(), 'location': pic.location, 'detail': pic.detail})
	rst['picCount'] = len(rst['picArray'])
	rst['result'] = 1
	return rst

def refresh_collection(username):
	rst = {}
	collections  = Collection.objects.filter(user__name=username)
	rst['picArray'] = []
	for collection in collections:
		rst['picArray'].append({'pidIndex': collection.pic.id, 'time': collection.pic.time.__str__(), 'location': collection.pic.location, 'username': collection.pic.user.name, 'detail': collection.pic.detail})
	rst['picCount'] = len(rst['picArray'])
	rst['result'] = 1
	return rst



