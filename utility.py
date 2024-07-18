import json

# Settings

# Download base URL
basePath = '/downloads/'

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
    print(f"[DEBUG] {message}")

class DownloadError(Exception):
    pass