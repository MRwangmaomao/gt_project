#!/bin/bash
adb connect 10.0.36.248
python getNewestLog.py -s 10.0.36.248


python getPose.py recentLog.log
sleep 1s
evo_traj tum recentLog.txt  -p --plot_mode=xyz

python generateTenTraj.py 4
sleep 1s

cd results
rm -r pudu.zip
rm -r timestamps.npz seconds_from_start.npz stats.json info.json error_array.npz
cd ..

# display all trajetory
#evo_traj tum recentLog.txt  -p --plot_mode=xyz

# display ten trajectorys
#evo_traj tum trajs/rela_time_traj1.txt trajs/rela_time_traj2.txt trajs/rela_time_traj3.txt trajs/rela_time_traj4.txt trajs/rela_time_traj5.txt trajs/rela_time_traj6.txt trajs/rela_time_traj7.txt trajs/rela_time_traj8.txt trajs/rela_time_traj9.txt  trajs/rela_time_traj10.txt -p --plot_mode=xy
evo_traj tum trajs/rela_time_traj1.txt  -p --plot_mode=xyz
# calculate trajectory relative error
evo_ape tum trajs/rela_time_traj3.txt trajs/rela_time_traj4.txt -va --plot --plot_mode xy --save_results results/pudu.zip

# evo_rpe tum trajs/rela_time_traj1.txt trajs/rela_time_traj3.txt -r angle_deg --delta 1 --delta_unit m -va --plot --plot_mode xy


cd results
unzip  pudu.zip
cd ..

python statsRead.py

