#-*- coding: UTF-8 -*-
from django.http import HttpResponse

def index(request):
    file_object = open('index.html')
    try:
        content = file_object.read()
    finally:
        file_object.close()
	return HttpResponse(content)
# Create your views here.
