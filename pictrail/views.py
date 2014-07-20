#-*- coding: UTF-8 -*-
from django.http import HttpResponse
import json
from django.http import Http404
from pictrail import pic_operation
from django.conf import settings

def interface(request):
	rst = {}
	if request.method == 'GET':
		return HttpResponse("Please use Post method!")
	elif request.method == 'POST':
		rst['result'] = 0
		if request.META.has_key('CONTENT_TYPE'):
			if 'multipart/form-data' in request.META['CONTENT_TYPE']:
				if request.POST.has_key('json'):
					json_data = json.loads(request.POST['json'])
					if settings.DEBUG :
						rst['json'] = json_data
					if json_data.has_key('cmd') and json_data['cmd'] == 'publishPic' and json_data.has_key('username') and json_data.has_key('longitude') and json_data.has_key('latitude') and json_data.has_key('location') and json_data.has_key('detail'):
						for f in request.FILES:
							photo = request.FILES[f]
							if pic_operation.publish_pic(json_data['username'], json_data['longitude'], json_data['latitude'], json_data['location'], json_data['detail'], photo):
								rst['result'] = 1
			elif 'application/json' == request.META['CONTENT_TYPE']:
				json_data = json.loads(request.body)
				if json_data.has_key('cmd'):
					if json_data['cmd'] == 'refreshPic':
						if json_data.has_key('longitude') and json_data.has_key('latitude') and json_data.has_key('scale') and json_data.has_key('startIndex') and json_data.has_key('refreshCount'):
							rst = pic_operation.refresh_pic(json_data['longitude'], json_data['latitude'], json_data['scale'], json_data['startIndex'], json_data['refreshCount'])
					elif json_data['cmd'] == 'picInfo':
					  if json_data.has_key('username') and json_data.has_key('picIndex'):
						  rst = pic_operation.pic_info(json_data['username'], json_data['picIndex'])
		return HttpResponse(json.dumps(rst), content_type="application/json")
	else:
		raise Http404

