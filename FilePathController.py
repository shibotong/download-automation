class FilePathController():
    def __init__(self, basePath):
        self.basePath = basePath
    
    def newPath(self, name, season, series, number, extension) -> str:
        fileName = f'{self.basePath}{name}/Season {season}/{name} - S{season}E'
        if number != 0:
            fileName += str(number) + ' - [' + str(series) + ']'
        else:
            fileName += str(series)
        fileName += extension
        return fileName