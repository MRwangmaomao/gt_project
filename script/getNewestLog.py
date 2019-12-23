import os
import re
import sys
import gzip


log_folder = '/sdcard/pudu/log/'

#change to current  folder 
os.chdir(os.path.dirname(os.path.realpath(__file__)))

def decompress(pull_log):
    print('decompressing:' + pull_log)
    if os.path.splitext(pull_log)[1] == 'gz':            
        f = gzip.GzipFile(fileobj=open(pull_log, 'rb'))
        log_out = open(os.path.splitext(pull_log)[0] + '.log', 'wb')
        if not f:
            print('file:' + pull_log + ' open fail')
        try:        
            while True:
                data = f.read(100);
                if not data:
                    break
                log_out.write(data)
        except Exception as e:
            print(e)
            pass
    else:
        os.system("ppmd -d " + pull_log + " " + "recentLog.log")
    print('done!')

def main(select_mode, device = None):
    try:
        os.mkdir('logs')
    except:
        pass
    device_string = ''
    if device:
        device_string = ' -s ' + device
    #os.system('adb ' + device_string + ' shell " su -c \'chmod -R 777 /sdcard\'"')
    tmp_list = os.popen('adb ' + device_string + ' shell ls ' + log_folder).read()
    print('list tmp folder:', tmp_list)
    all_logs = re.findall(r'.+\.(?:gz|pdlog)', tmp_list)
    if not all_logs or len(all_logs) == 0:
        return
    pull_log = ''
    if not select_mode:
        pull_log = max(all_logs)
    else:
        print('-------------------------')
        for i in range(len(all_logs)):
            print(i, all_logs[i])
        log_index = 0
        while True:
            log_index = int(input("input the log index:"))
            if log_index >= 0 and log_index <= len(all_logs):
                break
            print('wrong index')
        pull_log = all_logs[log_index]
    print('pulling log:', pull_log)
    #os.system('adb ' + device_string + ' pull /sdcard/PuduRobotMap/ATLAS_DATA static/map.json')
    os.system('adb ' + device_string + ' pull ' + log_folder + pull_log + ' logs/' + pull_log)
    decompress('logs/' + pull_log)    

if __name__ == '__main__':
    print('Auto pull newest log file from device, and decompress')
    print('use "select" mode if need select which file you need, like this:')
    print('    python pull_last_android_log.py select')
    print('decompress local pdlog file:')
    print('    python pull_last_android_log.py -d file.pdlog')
    if len(sys.argv) > 1 and sys.argv[1] == 'select':
        main(True)
    elif len(sys.argv) > 2 and sys.argv[1] == '-d':
        decompress(sys.argv[2])
    elif len(sys.argv) > 2 and sys.argv[1] == '-s':
        main(True, sys.argv[2])
    else:
        main(False)