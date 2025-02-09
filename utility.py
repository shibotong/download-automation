import json
import requests

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
    print(f'Configuration file not found in {configs}')
    exit(1)
configurations = json.load(configFile)
baseURL = configurations['url']
token = configurations['token']
host = configurations['host']

def log(message):
    print(f"[DEBUG] {message}")

def push_notification(title, message, icon):
    server = 'https://api.day.app/'
    endpoint = server + token
    url = endpoint + '/' + title + '/' + message
    parameter = {'icon': icon}
    requests.get(url=url, params=parameter)

