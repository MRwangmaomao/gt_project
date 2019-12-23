# -*- coding: UTF-8 -*-
import os
import re
import numpy as np
import sys
import math

critical_section = False
critical_counter = 0
start_x = 0 
start_y = 0
max_dist = 0.5


def startPoint(line):
    global critical_section
    global critical_counter
    global start_x
    global start_y
    global max_dist 
    if line.split()[0] == '#':
        return False
     
    if not critical_section:
        x = float(line.split()[1])
        y = float(line.split()[2])
        dis = math.sqrt((x - start_x) * (x - start_x) + (y - start_y) * (y - start_y))
 
        if dis < max_dist:
            critical_section = True
            # print(x)
            return True
        return False
    else:
        critical_counter = critical_counter + 1
        if critical_counter > 500:
            critical_counter = 0
            critical_section = False
        return False

def main(traj_num):
    try:
        os.mkdir('trajs')
    except:
        pass

    # open files and clear
    for i in range(1,traj_num):
        f=open('trajs/traj'+ str(i) + '.txt','wa')
        rf=open('trajs/rela_time_traj'+ str(i) + '.txt','wa')
        f.truncate()
        rf.truncate() 
        f.close()
        rf.close()

    # input data into trajs
    counter = 0
    fp = open('recentLog.txt')
    start_flag = False

    while True:
        line = fp.readline()
        if counter == traj_num or (not line):
            
            f.close()
            # os.remove('trajs/traj11.txt')
            break
        if startPoint(line):
            if start_flag:
               f.close()
            start_flag = True
            counter = counter + 1
            path_file_name = 'trajs/traj' + str(counter)
            f=open(path_file_name + '.txt','w')

            
        if start_flag:
            f.write(line)

    # change timestaps
    for i in range(1,traj_num):
        ft=open('trajs/traj'+ str(i) + '.txt')
        rf=open('trajs/rela_time_traj'+ str(i) + '.txt','wa')
        print('trajs/rela_time_traj'+ str(i) + '.txt')
        line = ft.readline()
        list_line = line.split()
        start_time = float(list_line[0])
        list_line[0] = '0.0'
        new_line = str(list_line[0]) + ' ' + str(list_line[1]) + ' ' + str(list_line[2]) + ' '  + str(list_line[3]) + ' '  + str(list_line[4]) + ' '  + str(list_line[5]) + ' ' + str(list_line[6]) +  ' ' + str(list_line[7]) +'\n'
        rf.write(new_line)
        while True:
            line = ft.readline()
            if not line:
                break
            list_line = line.split()
            current_time = float(list_line[0])
            list_line[0] = str(current_time - start_time)
            new_line = str(list_line[0]) + ' ' + str(list_line[1]) + ' ' + str(list_line[2]) + ' '  + str(list_line[3]) + ' '  + str(list_line[4]) + ' '  + str(list_line[5]) + ' ' + str(list_line[6]) +  ' ' + str(list_line[7]) + '\n'
            rf.write(new_line)
        ft.close()
        rf.close()
    print("Ten trajectorys generate end !!!!!!!!!!")

if __name__ == '__main__':
    print('Auto generate '+ sys.argv[1] +' trajectorys')
    if len(sys.argv) == 2:
        num = int(sys.argv[1])
        main(num)
    else:
        print("Please input number of trajectory!!!")