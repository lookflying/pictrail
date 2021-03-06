from pictrail.models import User, Picture, Raised, Comment, Collection, LongPicture, SelectedPicture
from django.conf import settings
from datetime import datetime
from PIL import Image
import StringIO
import sys
from django.db.models import Q
from pictrail import geo_calc
from decimal import *
import json
def save_small_pic(pic_id, large_pic):
	large_file = StringIO.StringIO(large_pic.read())
	large_image = Image.open(large_file)
	(width, height) = large_image.size
	s_width = width
	s_height = height
	if width > height:
		s_width = width * settings.PIC_SMALL_LEN / height
		s_height = settings.PIC_SMALL_LEN
	else:
		s_height = height * settings.PIC_SMALL_LEN / width
		s_width = settings.PIC_SMALL_LEN
	small_image = large_image.resize((s_width, s_height), Image.ANTIALIAS)
	small_image.save(settings.PIC_SMALL_DIR + str(pic_id) + ".jpg")
	pass

def save_large_pic(pic_id, large_pic):
	large_file = StringIO.StringIO(large_pic.read())
	large_image = Image.open(large_file)
	(width, height) = large_image.size
	s_width = width
	s_height = height
	if width > height:
		s_width = width * settings.PIC_LARGE_LEN / height
		s_height = settings.PIC_LARGE_LEN
	else:
		s_height = height * settings.PIC_LARGE_LEN / width
		s_width = settings.PIC_LARGE_LEN
	small_image = large_image.resize((s_width, s_height), Image.ANTIALIAS)
	small_image.save(settings.PIC_LARGE_DIR + str(pic_id) + ".jpg")
	pass



def publish_pic(username, longitude, latitude, location, detail, photo, time):
	try:
		user = User.objects.get(name=username)
	except User.DoesNotExist:
		return False
	try:
		if len(location) > 50:
			location = location[:50]
		if len(detail) > 200:
			detail = detail[:50]
		pic = Picture.objects.create(user=user, time=datetime.strptime(time, "%d %B %Y"), location=location, longitude=longitude, latitude=latitude, detail=detail)
	except Exception, e:
		raise e
#	pic = Picture.objects.create(user=user, time=time, location=location, longitude=longitude, latitude=latitude, detail=detail)
#	pic = Picture.objects.create(user=user, time=time, location=location, longitude=longitude, latitude=latitude, detail=detail)
#	with open(settings.PIC_LARGE_DIR + str(pic.id) + ".jpg", 'wb+') as dest:
#		for chunk in photo.chunks():
#			dest.write(chunk)
#		dest.close()
	save_large_pic(pic.id, photo)
	photo.seek(0)
	save_small_pic(pic.id, photo)
	return True


def refresh_pic(longitude, latitude, scale, start_idx, count):
	rst = {}
	rst['result'] = 0
	if start_idx != '0':
		try:
			start_pic = Picture.objects.get(id=start_idx)
			start_time = start_pic.time
		except Picture.DoesNotExist:
			return rst
	else:
		start_time = datetime.now()
	DISTANCE_PER_DEGREE = 111000.0#only for latitude, use 1 for longitude
	range = scale / DISTANCE_PER_DEGREE
#	pics = Picture.objects.filter(Q(longitude__gte=longitude - range) & Q(longitude__lte=longitude + range) & Q(latitude_gte=latitude - range) & Q(latitude_lte=latitude + range) & Q(time__lt=start_time))#.order_by('-time')[:count]
	pics = Picture.objects.filter(Q(longitude__gte=longitude - 1) & Q(longitude__lte=longitude + 1) & Q(latitude__gte=latitude - range) & Q(latitude__lte=latitude + range) & Q(time__lt=start_time)).order_by('-time')
		
#	pics = Picture.objects.filter(time__lt=start_time).order_by('-time')[:count]
		
	rst['picArray'] = []
	pic_added = 0
	center_loc = (Decimal(longitude), Decimal(latitude))
	for pic in pics:
		if pic_added < count:
			pic_loc = (pic.longitude, pic.latitude)
			if geo_calc.distance(center_loc, pic_loc) <= scale:
				rst['picArray'].append({'picIndex': pic.id, 'time': pic.time.__str__()})
				pic_added+=1
		else:
			break
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
			pic_id_list[item['no']] = item['picIndex']#start from 0	
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
		rst['picArray'].append({'picIndex': collection.pic.id, 'time': collection.pic.time.__str__(), 'location': collection.pic.location, 'username': collection.pic.user.name, 'detail': collection.pic.detail})
	rst['picCount'] = len(rst['picArray'])
	rst['result'] = 1
	return rst


def manage(request):
	rst = {}
	rst['result'] = 0
	if request.META.has_key('CONTENT_TYPE'):
		if 'multipart/form-data' in request.META['CONTENT_TYPE']:
			if request.REQUEST.has_key('JSON'):
				json_data = json.loads(request.REQUEST['JSON'])
				if settings.DEBUG:
					rst['json'] = json_data
				if json_data.has_key('cmd') and json_data['cmd'] == 'publishPic' and json_data.has_key('username') and json_data.has_key('longitude') and json_data.has_key('latitude') and json_data.has_key('location') and json_data.has_key('detail') and json_data.has_key('time'):
					if request.FILES.has_key('uploadFile'):
						photo = request.FILES['uploadFile']
						if publish_pic(json_data['username'], json_data['longitude'], json_data['latitude'], json_data['location'], json_data['detail'], photo, json_data['time']):
							rst['result'] = 1
	return rst
