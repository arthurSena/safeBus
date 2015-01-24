import math

def deg2rad(deg) :
	return (deg * math.pi / 180.0)

def change_schedule_second(schedule):
	second = schedule.split(':')
	return int(second[0]) * 3600 + int(second[1]) * 60 + int(second[2])
