from vehicle import vehicle
text_file = open("a1_2.txt", "r")
lines = text_file.read().split('\n')
for i in lines:
	j = i.split(',')
	print int(j[2])
	#vehicle(j[0], int(j[1]), int(j[2]), j[3], 6)