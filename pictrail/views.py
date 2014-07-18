#-*- coding: UTF-8 -*-
from django.http import HttpResponse
import json
from django.http import Http404

def interface(request):
	if request.method == 'GET':
		return HttpResponse("Please use Post method!")
	elif request.method == 'POST':
		data = {}
		if request.META.has_key('CONTENT_TYPE'):
			data['type'] = request.META['CONTENT_TYPE']
			if 'multipart/form-data' in request.META['CONTENT_TYPE']:
				count = 0
				names = []
				for f in request.FILES:
					cur_file = request.FILES[f]
					names.append(request.FILES[f].name)
					with open(cur_file.name, 'wb+') as dest:
						for chunk in cur_file.chunks():
							dest.write(chunk)
						dest.close()
					count = count + 1
				data['count'] = count
				data['file'] = names
			if request.POST.has_key('json'):
				json_data = json.loads(request.POST['json'])
				data['json'] = json_data
		return HttpResponse(json.dumps(data), content_type="application/json")
	else:
		raise Http404

