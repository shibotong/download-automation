class DownloadItem():
    
    def __init__(self, json):
        self.seriesName = json['name']
        self.seriesLink = json['link']
        self.currentDownload = json['series']
        self.rules = json['rule']
        self.amiSearch = False
        if 'ambiSearch' in json:
            self.ambiSearch = json['ambiSearch']