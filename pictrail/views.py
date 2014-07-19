#-*- coding: UTF-8 -*-
from django.http import HttpResponse
import json
from django.http import Http404
from pictrail import pic_operation

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
		return HttpResponse(json.dumps(rst), content_type="application/json")
	else:
		raise Http404

