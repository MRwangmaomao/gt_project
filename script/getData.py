from datetime import datetime
import numpy as np
import re

#0. get global path
def getGlobalPath(log_path):
    path_x = []
    path_y = []
    global_path = []

    log_data = open(log_path, "r", encoding='UTF-8')
    lines = log_data.readlines()
    for line in lines:
        if not line.strip(): continue
        if "D/debug_bridge:" in line:
            if "global_path" in line:
                #print(line)
                r = line.split(":[")[1]
                p = re.compile(r'[[](.*?)[]]', re.S)
                size = len(re.findall(p,r))
                for i in range(size):
                    #print(i, re.findall(p,r)[i])
                    data = re.findall(p,r)[i]
                    x = data.split(",")[0]
                    y = data.split(",")[1]

                    path_x.append(x)
                    path_y.append(y)
                    #print(i, data, x, y)

                    pose = np.array([float(x), float(y)])
                    global_path.append(pose)

    log_data.close()

    return path_x, path_y, global_path

#1.get robot pose data from log. (the real trajectory)
def getPoseData(log_path, st, et):
    stime = []
    pose_x = []
    pose_y = []
    pose_z = []
    local_pose = []
    log_data = open(log_path, "r",  encoding='UTF-8')
    lines = log_data.readlines()
    for line in lines:
        if not line.strip(): continue
        if "D/Json2PC: send json,pose" in line:

            print(line)
            hr = line.split()[0]
            mes = line.split()[1].split("(")[0]
            str_time = hr + '.' + mes
            stime.append(str_time)

            r = line.split("{")[2].split("}")[0]
            x = r.split(",")[0].split(":")[1]
            y = r.split(",")[1].split(":")[1]
            z = r.split(",")[2].split(":")[1]
            #print(x,y,z)
            pose_x.append(x)
            pose_y.append(y)
            pose_z.append(z)

            p = np.array([float(x), float(y)])
            local_pose.append(p)
    log_data.close()

    time = []
    time_start = datetime.strptime(str(stime[0]), "%H:%M:%S.%f")
    for i in range(len(stime)):
        date_time = datetime.strptime(str(stime[i]), "%H:%M:%S.%f")
        # print date_time
        dt_s = (date_time - time_start).seconds
        dt_ms = (date_time - time_start).microseconds / float(1000000)
        dt = dt_s + dt_ms
        #print(i,dt)
        time.append(dt)

    pose_x = list(map(float, pose_x))
    pose_y = list(map(float, pose_y))
    pose_z = list(map(float, pose_z))
    #print(len(pose_x))

    if (et > max(time)):
        print("Input Error: end_time > max_time")
    else:
        if(st != et):
            st_index, et_index = calSEindex(time, st, et)

            pose_x = pose_x[st_index:et_index]
            pose_y = pose_y[st_index:et_index]
            pose_z = pose_z[st_index:et_index]
            local_pose = local_pose[st_index:et_index]


    return pose_x,pose_y,pose_z,local_pose

#2.get can speed from log. (speed of robot move)
def getCanSpeedData(log_path, st, et):
    stime = []
    linear_velocity = []
    angular_velocity = []
    log_data = open(log_path, "r",  encoding='UTF-8')
    lines = log_data.readlines()
    for line in lines:
        if not line.strip(): continue

        if "D/CanDataProcess: robot speed" in line:
            #print(line)
            #r = line.split()
            #if len(r) < 8: continue
            l1 = line.split()[0]
            l2 = line.split()[1].split("(")[0]

            l7 = line.split()[5]
            l8 = line.split()[6]

            str_time = l1 + '.' + l2
            stime.append(str_time)

            lv = l7.split('=')[1]
            av = l8.split('=')[1]
            #print lv, av
            linear_velocity.append(lv)
            angular_velocity.append(av)

    log_data.close()

    time = []
    time_start = datetime.strptime(str(stime[0]), "%H:%M:%S.%f")
    for i in range(len(stime)):
        date_time = datetime.strptime(str(stime[i]), "%H:%M:%S.%f")
        # print date_time
        dt_s = (date_time - time_start).seconds
        dt_ms = (date_time - time_start).microseconds / float(1000000)
        dt = dt_s + dt_ms
        # print(dt)
        time.append(dt)

    linear_velocity = list(map(float, linear_velocity))
    angular_velocity = list(map(float, angular_velocity))

    if (et > max(time)):
        print("Input Error: end_time > max_time")
    else:
        if (st != et):
            st_index, et_index = calSEindex(time, st, et)

            time = time[st_index:et_index]
            linear_velocity = linear_velocity[st_index:et_index]
            angular_velocity = angular_velocity[st_index:et_index]


    return time,linear_velocity,angular_velocity

#3.get speed from plan;
def getPlanSpeedData(log_path, st, et):
    stime = []
    plan_lv = []
    plan_av = []
    cur_lv = []
    cur_av = []
    log_data = open(log_path,"r", encoding='UTF-8')
    lines = log_data.readlines()
    for line in lines:
        if not line.strip(): continue
        if "D/local_planner: final plan tangentialVel:" in line:
            #print(line)
            hr = line.split()[0]
            msec = line.split()[1]
            str_time = hr + '.' + msec
            stime.append(str_time)

            str_plan_lv = line.split("tangentialVel:")[1].split("axialVel:")[0]
            str_plan_av = line.split("axialVel:")[1].split("current tangentialVel:")[0]
            plan_lv.append(str_plan_lv)
            plan_av.append(str_plan_av)
            #print(str_plan_lv, str_plan_av)

            str_cur_lv = line.split("current tangentialVel:")[1].split("axialVel:")[0]
            str_cur_av = line.split("current tangentialVel:")[1].split("axialVel:")[1]
            cur_lv.append(str_cur_lv)
            cur_av.append(str_cur_av)
            #print(cur_lv,cur_av)
    log_data.close()

    time = []
    if (len(stime) == 0):
        return time, plan_lv, plan_av, cur_lv, cur_av

    time_start = datetime.strptime(str(stime[0]), "%H:%M:%S.%f")
    for j in range(len(stime)):
        date_time = datetime.strptime(str(stime[j]), "%H:%M:%S.%f")
        dt_s = (date_time - time_start).seconds
        dt_ms = (date_time - time_start).microseconds / float(1000000)
        dt = dt_s + dt_ms
        time.append(dt)

    plan_lv = list(map(float, plan_lv))
    plan_av = list(map(float, plan_av))
    cur_lv = list(map(float, cur_lv))
    cur_av = list(map(float, cur_av))

    if (et > max(time)):
        print("Input Error: end_time > max_time")
    else:
        if (st != et):
            st_index, et_index = calSEindex(time, st, et)

            time = time[st_index:et_index]
            plan_lv = plan_lv[st_index:et_index]
            plan_av = plan_av[st_index:et_index]
            cur_lv = cur_lv[st_index:et_index]
            cur_av = cur_av[st_index:et_index]

    return time,plan_lv,plan_av,cur_lv,cur_av

#4.get left and right speed from localPlanner and can
def getSpeedData(log_path, st, et):
    stime = []
    plan_left = []
    plan_right = []
    odom_left = []
    odom_right = []
    log_data = open(log_path, "r", encoding='UTF-8')
    lines = log_data.readlines()
    for line in lines:
        if not line.strip(): continue
        if "set target=" in line:
            hr = line.split()[0]
            msec = line.split()[1].split("(")[0]
            #print(hr,msec)
            str_time = hr + '.' + msec
            stime.append(str_time)

            str_plan_speed = line.split("[")[1].split("]")[0]
            str_odom_speed = line.split("now speed=[")[1].split("]")[0]
            # speed get from local planner
            plan_speed_left = str_plan_speed.split(",")[0]
            plan_speed_right = str_plan_speed.split(",")[1]
            plan_left.append(plan_speed_left)
            plan_right.append(plan_speed_right)
            # speed get from robot traj in real world
            odom_speed_left = str_odom_speed.split(",")[0]
            odom_speed_right = str_odom_speed.split(',')[1]
            odom_left.append(odom_speed_left)
            odom_right.append(odom_speed_right)

    log_data.close()

    time = []
    time_start = datetime.strptime(str(stime[0]), "%H:%M:%S.%f")
    for j in range(len(stime)):
        date_time = datetime.strptime(str(stime[j]), "%H:%M:%S.%f")
        dt_s = (date_time - time_start).seconds
        dt_ms = (date_time - time_start).microseconds / float(1000000)
        dt = dt_s + dt_ms
        time.append(dt)

    plan_left = list(map(float, plan_left))
    plan_right = list(map(float, plan_right))
    odom_left = list(map(float, odom_left))
    odom_right = list(map(float, odom_right))

    if (et > max(time)):
        print("Input Error: end_time > max_time")
    else:
        if (st != et):
            st_index,et_index = calSEindex(time,st,et)

            time = time[st_index:et_index]
            plan_left = plan_left[st_index:et_index]
            plan_right = plan_right[st_index:et_index]
            odom_left = odom_left[st_index:et_index]
            odom_right = odom_right[st_index:et_index]

    #cal. if control can follow the plan speed
    diff_left = []
    diff_right = []
    for k in range(len(time)-1):
        single_diff_left = abs(plan_left[k] - odom_left[k+1])
        single_diff_right = abs(plan_right[k] - plan_left[k+1])
        diff_left.append(single_diff_left)
        diff_right.append(single_diff_right)

    return time,plan_left,plan_right,odom_left,odom_right,diff_left,diff_right


#cal index based on start_time and end_time;
def calSEindex(time,st,et):
    st_index = et_index = 0
    if (st != et):
        for j in range(len(time)):
            if (time[j] > st):
                st_index = j
                # print(st_index)
                break
        for j in range(len(time)):
            if (time[j] > et):
                et_index = j
                # print(et_index)
                break

    return st_index,et_index

#if __name__ == '__main__':
