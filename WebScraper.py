import requests
import DownloadAutomationErrors
from DownloadItem import DownloadItem
from bs4 import BeautifulSoup


class WebScraper:

    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    }

    def searchTorrentLink(self, baseurl: str, item: DownloadItem) -> str:
        html = self.fetchHTML(baseurl + item.seriesLink, self.header)
        return self.searchTorrentURL(html, item.rules, item.currentDownload, item.ambiSearch)

    def fetchHTML(self, url, header) -> str:
        try:
            r = requests.get(url, headers=header)
            r.raise_for_status()
            return r.text
        except:
            raise DownloadAutomationErrors.HTMLFetchError("Failed to fetch HTML")


    def searchTorrentURL(self, html, rules, series, isAmbisearch) -> str:
        soup = BeautifulSoup(html, "html.parser")

        # Get Link Name
        seriesStr = str(series)
        if series < 10:
            seriesStr = "0" + seriesStr
        linkName = rules[0] + seriesStr + rules[1]
        for i in soup.find_all('ul', {'class': 'attachlist'}):
            links = i('a')
            for link in links:
                linkText = link.get_text()
                if isAmbisearch:
                    if seriesStr in linkText:
                        if all(word in linkText for word in rules):
                            downloadLink = link.get('href')
                            return downloadLink
                else:
                    if linkName in linkText:
                        downloadLink = link.get('href')
                        return downloadLink
