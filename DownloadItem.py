class DownloadItem():
    
    def __init__(self, json):
        self.seriesName = json['name']
        self.seriesLink = json['link']
        self.currentDownload = json['series']
        self.rules = json['rule']
        if 'number' in json:
            self.number = json['number']
        else:
            self.number = 0

        self.season = json['season']
        self.icon = json['icon']
        self.amiSearch = False
        if 'ambiSearch' in json:
            self.ambiSearch = json['ambiSearch']

    def downloadingText(self) -> str:
        return f'Downloading {self.seriesName} Season {self.season} Series {self.currentDownload}'