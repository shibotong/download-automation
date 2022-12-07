import os

class AutoDownloads():

    def __init__(self, name, season, series, number, download):
        self.name = name
        self.series = series
        self.season = season
        self.number = number
        self.download = download
        return

    def updateStatus(self) -> bool:
        try:
            self.download.update()
            if self.download.status == 'complete':
                file, fileExtension = os.path.splitext(self.download.name)
                originalName = str(self.download.dir) + '/' + str(self.download.name)
                fileName = self.name + '.s' + str(self.season)
                if self.number != 0:
                    fileName += '.e' + str(self.number) + '.[' + str(self.series) + ']' + fileExtension
                else:
                    fileName += '.e' + str(self.series) + fileExtension
                newName = str(self.download.dir) + '/Anime' + '/' + self.name + '/Season ' + str(self.season) + '/' + fileName
                os.rename(originalName, newName)
                print(newName, 'success')
                return True
            elif self.download.status == 'error':
                return True
            else:
                return False
        except Exception as e: 
            print(e)
            return False
    