import os
import json

debugString = os.environ.get("debug", "False")
debug = debugString == "True"

# Settings

# Download base URL
basePath = '/downloads/'
if debug:
    basePath = '/Users/shibotong/MyProjects/downloadTesting/'



# Recursive Period (seconds)
period = 3600

# Aria2 hosting server
host = os.environ.get("url", "http://192.168.4.35")

# Download Rules
downloadRuleURL = basePath + 'configs/downloadRule.json'
configs = basePath + 'configs/configuration.json'
torrentSavingPath = basePath + 'Torrents/'

try:
    configFile = open(configs)
except:
    print("Configuration file not found")
    exit(1)
configurations = json.load(configFile)
baseURL = configurations['url']
token = configurations['token']

def log(message):
    if debug:
        print(f"[DEBUG] {message}")

class DownloadError(Exception):
    pass