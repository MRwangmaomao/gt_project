import json

MAX_STD = 0.1
MAX_RMSE = 0.1

def resolveJson(path, max_std, max_rmse):
    file = open(path, "rb")
    fileJson = json.load(file)
    std = fileJson["std"]
    rmse = fileJson["rmse"]
    sse = fileJson["sse"]
    error_max = fileJson["max"]
    error_min = fileJson["min"]
    median = fileJson["median"]
    mean = fileJson["mean"]
    print("std:",std)
    print("rmse:",rmse)
    # print (std, rmse, sse, error_max, error_min, median, mean)
    if rmse < MAX_RMSE:
        print("This robot is OK!")
    else:
        print("This robot is bad!")
 
path = r"results/stats.json"
resolveJson(path, MAX_STD, MAX_RMSE)