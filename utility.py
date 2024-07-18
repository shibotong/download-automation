import os
import json

debugString = os.environ.get("debug", "False")
debug = True #debugString == "True"

# Settings

# Download base URL
basePath = '/downloads/'
if debug:
    basePath = '/Users/shibotong/MyProjects/downloadTesting/'



# Recursive Period (seconds)
period = 3600

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
host = configurations['host']

def log(message):
    if debug:
        print(f"[DEBUG] {message}")

class DownloadError(Exception):
    pass