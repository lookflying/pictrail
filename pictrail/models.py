from django.db import models

# Create your models here.
class User(models.Model):
	name = models.CharField(max_length=50)
	password = models.CharField(max_length=200)
	def __unicode__(self):
		return self.name

class Picture(models.Model):
	user = models.ForeignKey(User)
	raise_count = models.IntegerField(default=0)
	time = models.DateTimeField('Taken time')
	detail = models.CharField(max_length=200)
	location = models.CharField(max_length=50)
	longitude = models.DecimalField(max_digits=10, decimal_places=6)
	latitude = models.DecimalField(max_digits=10, decimal_places=6)

	def __unicode__(self):
		return self.time.__str__() + " @ " + self.location + "(" + self.longitude.to_eng_string() + "," + self.latitude.to_eng_string() + ")"  + " by " + self.user.name 

class Raised(models.Model):
	user = models.ForeignKey(User)
	pic = models.ForeignKey(Picture)

class Collection(models.Model):
	user = models.ForeignKey(User)
	pic = models.ForeignKey(Picture)

class Comment(models.Model):
	user = models.ForeignKey(User)
	pic = models.ForeignKey(Picture)
	content = models.CharField(max_length=50)
	time = models.DateTimeField('Comment time')
	def __unicode__(self):
		return self.user.name + " said: " + self.content + " about " + str(self.pic.id) + " @ " + self.time.__str__()

class Suggest(models.Model):
	user = models.ForeignKey(User)
	content = models.CharField(max_length=200)
	time = models.DateTimeField('Suggest time')

class LongPicture(models.Model):
	user = models.ForeignKey(User)
	time = models.DateTimeField('create time')

class SelectedPicture(models.Model):
	pic = models.ForeignKey(Picture)
	long_pic = models.ForeignKey(LongPicture)

	
