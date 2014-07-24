#-*- coding: UTF-8 -*-
import json
import time
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from pictrail.models import User, Suggest, Raised, Comment, Collection, Picture

#method for user logging in operation. 
def userLogin(json_data):
    if json_data.has_key('username') and json_data.has_key('password'):
        user_name = json_data['username']
        pass_word = json_data['password']
    else:
        return 0
    try:
        realpsw = User.objects.get(name=user_name).password
        if realpsw == pass_word:
            return 1
        else:
            return 0
    except ObjectDoesNotExist:
        return 0

#method for user register
def userRegister(json_data):
    if json_data.has_key('username') and json_data.has_key('password'):
        user_name = json_data['username']
        pass_word = json_data['password']
    else:
        return 0
    try:
        User.objects.get(name=user_name)
        return 0
    except ObjectDoesNotExist:
        new_user = User(name=user_name, password=pass_word)
        new_user.save()
        return 1

#method for making advice 
def sendAdvice(json_data):
    if json_data.has_key('username') and json_data.has_key('advice'):
        user_name = json_data['username']
        advice = json_data['advice']
    else:
        return 0
    try:
        cur_user = User.objects.get(name=user_name)
    except ObjectDoesNotExist:
        return 0
    cur_time = timezone.now()
    new_suggest = Suggest(user=cur_user, content=advice, time=cur_time)
    new_suggest.save()
    return 

#collect pictures. If action == 0, decollect. Else, collect.
def collectPic(json_data):
    if json_data.has_key('username') and json_data.has_key('picIndex') and json_data.has_key('action'):
        user_name = json_data['username']
        picIndex = long(json_data['picIndex'])
        action = json_data['action']
    else:
        return 0
    try:
        cur_user = User.objects.get(name=user_name)
        cur_pic = Picture.objects.get(id=picIndex)
    except ObjectDoesNotExist:
        return 0
    if action == 0:
        try:
            precollect = Collection.objects.get(Q(user=cur_user), Q(pic=cur_pic))
            precollect.delete()
            return 1
        except ObjectDoesNotExist:
            return 0
    elif action == 1:
        try:
            Collection.objects.get(Q(user=cur_user), Q(pic=cur_pic))
            return 0
        except ObjectDoesNotExist:
            newcollect = Collection(user=cur_user, pic=cur_pic)
            newcollect.save()
            return 1
    else:
        return 0

#Raise a picture. 
def raisePic(json_data):
    if json_data.has_key('username') and json_data.has_key('picIndex') and json_data.has_key('action'):
        user_name = json_data['username']
        picIndex = long(json_data['picIndex'])
        action = json_data['action']
    else:
        return 0
    try:
        cur_user = User.objects.get(name=user_name)
        cur_pic = Picture.objects.get(id=picIndex)
    except ObjectDoesNotExist:
        return 0
    if action == 0:
        try:
            preraised = Raised.objects.get(Q(user=cur_user), Q(pic=cur_pic))
            preraised.delete()
            cur_pic.raise_count = cur_pic.raise_count - 1
            cur_pic.save()
            return 1
        except ObjectDoesNotExist:
            return 0
    elif action == 1:
        try:
            Raised.objects.get(Q(user=cur_user), Q(pic=cur_pic))
            return 0
        except ObjectDoesNotExist:
            newraised = Raised(user=cur_user, pic=cur_pic)
            newraised.save()
            cur_pic.raise_count = cur_pic.raise_count + 1
            cur_pic.save()
            return 1
    else:
        return 0

#make comments to a certain picture. 
def comment(json_data):
    if json_data.has_key('username') and json_data.has_key('picIndex') and json_data.has_key('comment'):
        user_name = json_data['username']
        picIndex = json_data['picIndex']
        comment = json_data['comment']
    else:
        return 0
    try:
        cur_user = User.objects.get(name=user_name)
        cur_pic = Picture.objects.get(id=picIndex)
    except ObjectDoesNotExist:
        return 0
    cur_time = timezone.now()
    newcomment = Comment(user=cur_user, pic=cur_pic, content=comment, time=cur_time)
    newcomment.save()
    return 1
