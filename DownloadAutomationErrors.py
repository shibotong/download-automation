class DownloadAutomationError(Exception):
    pass

class ScraperError(DownloadAutomationError):
    pass

class HTMLFetchError(ScraperError):
    pass

class DownloadError(Exception):
    pass



