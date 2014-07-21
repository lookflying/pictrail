from math import *

RADIUS = 6371393  #Earth's mean raadius in meters

def distance(origin, destiny):
	(latitude1, longitude1) = (origin[0], origin[1])
	(latitude2, longitude2) = (destiny[0], destiny[1])
	d_lat = radians(latitude1 - latitude2)
	d_long = radians(longitude1 - longitude2)
	a = sin(d_lat/2) * sin(d_lat/2) + cos(radians(latitude1)) * cos(radians(latitude2)) * sin(d_long/2) * sin(d_long/2)
	c = 2 * atan2(sqrt(a), sqrt(1-a))
	return (RADIUS * c)

