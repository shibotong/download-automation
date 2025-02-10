import os
from utility import push_notification, log, basePath
import FilePathController

controller = FilePathController.FilePathController(basePath + 'Anime/')

class AutoDownloads():

    def __init__(self, name, season, series, number, download, icon):
        self.name = name
        self.series = series
        self.season = season
        self.number = number
        self.download = download
        self.icon = icon
        return

    def updateStatus(self) -> bool:
        try:
            self.download.update()
            if self.download.status == 'complete':
                log(self.download.name + ' success')
                file, fileExtension = os.path.splitext(self.download.name)
                originalName = str(self.download.dir) + '/' + str(self.download.name)
                newName = controller.newPath(self.name, self.season, self.series, self.number, fileExtension)
                os.rename(originalName, newName)
                print(newName, 'success')
                # send request if success
                message = "Season " + str(self.season) + " Episode " + str(self.series) + " added to library"
                push_notification(self.name, message, self.icon)
                return True
            elif self.download.status == 'error':
                return True
            else:
                return False
        except Exception as e: 
            print(e)
            return False
    