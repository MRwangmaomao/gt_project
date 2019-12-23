from datetime import datetime
import numpy as np
import re
import os
import string
import math
import sys


def main():
	log_data = open(sys.argv[1], "r")
	lines = log_data.readlines()

	fisrt_flag = False
	path_file_name = './' + sys.argv[1].split(".")[0] + '.txt'
	print("output the file:" + path_file_name)
	with open(path_file_name, "wb+") as f:
		f.truncate()
		f.write("# ground truth trajectory\n")
		f.write("# file: " + path_file_name + "\n")
		f.write("# timestamp tx ty tz qx qy qz qw\n")

		for line in lines:
			if not line.strip(): continue
			if "D/MarkerLocalization: get pose" in line:
				# 13:53:40 175(1398)D/MarkerLocalization: get pose (-0.571508, 1.13417, -0.617302)
				#print(line)
				
				hour = line.split(":")[0]
				minute = line.split(":")[1].split(":")[0]
				second = line.split(":")[2].split()[0]
				mes = line.split()[1].split("(")[0]
				if fisrt_flag == False:
					fisrt_flag = True
					str_time = str(0)
					first_time = float(hour)*3600 + float(minute)*60 + float(second) + float(mes)/1000
				else:
					str_time = str(float(hour)*3600 + float(minute)*60 + float(second) + float(mes)/1000 - first_time)
				#print(hour+" " + minute+" " + second+" " + mes)
				# print(str_time)
				r = line.split("(")[2].split(")")[0]
				x = r.split(",")[0]
				y = r.split()[1].split(",")[0]
				z = r.split()[2].split(",")[0]

				#print(x,y,z)
				#w = cos(a/2)
				#x = sin(a/2)cos(beta_x)
				#y = sin(a/2)cos(beta_y)
				#z = sin(a/2)cos(beta_z)
				p = str_time + " " + x + " " + y  + " " + "0" + " " + "0" + " " + "0" + " " + str(math.sin(float(z)/2)) + " " + str(math.cos(float(z)/2)) + '\n'
				# + " " + str(math.cos(z/2)) + "\n"
				# print(str(x) +  str(y))
				f.write(p)

	log_data.close()

if __name__ == "__main__":
    main()
