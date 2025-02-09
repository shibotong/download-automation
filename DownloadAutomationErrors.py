class DownloadAutomationError(Exception):
    pass

class ScraperError(DownloadAutomationError):
    pass

class HTMLFetchError(ScraperError):
    pass

class TorrentNotFoundError(ScraperError):
    pass

class DownloadError(Exception):
    pass



