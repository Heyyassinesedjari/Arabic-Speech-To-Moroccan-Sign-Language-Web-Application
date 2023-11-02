import json
import requests
import os

file_path = "application/static/api_vars.json"
with open(file_path, 'r') as file:
    data1 = json.load(file)
data1


def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(data1["API_URL2"], headers=data1["headers"], data=data)
    return response.json()

def query2(data):
    response = requests.post(data1["API_URL2"], headers=data1["headers"], data=data)
    return response.json()


def getFilePath(directory):
    files = os.listdir(directory)
    if len(files) == 1:
        filename = files[0]
        if directory.endswith("/"):
            return directory+filename
        else:
            return directory+"/"+filename
    else:
        print("The directory does not contain a single file.")