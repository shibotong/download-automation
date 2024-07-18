import requests
from bs4 import BeautifulSoup
import shutil
import os
from utility import baseURL, torrentSavingPath, log



class TorrentDownload():
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ApplewebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    }
    
    def __init__(self):
        return
    
    def getHTML(self, url, header):
        try:
            r = requests.get(url, headers=header)
            r.raise_for_status()
            return r.text
        except:
            return ""

    def downloadSeries(self, item):
        seriesName = item['name']
        seriesLink = item['link']
        currentDownload = item['series']
        rules = item['rule']
        ambiSearch = False
        if 'ambiSearch' in item:
            ambiSearch = item['ambiSearch']

        torrentLink = self.getDownloadLink1Lou(baseURL, seriesLink, rules, currentDownload, ambiSearch)
        if torrentLink is not None:
            try:
                torrentPath = self.downloadTorrent(torrentLink, seriesName, currentDownload)
                return torrentPath
            except Exception as e:
                raise e
        else:
            raise Exception("no download link")
            
    def getHTML(self, url, header):
        try:
            r = requests.get(url, headers=header)
            r.raise_for_status()
            return r.text
        except Exception as e:
            print(e)
            return ""


    def getDownloadLink(self, link, rules, series, ambiSearch):
        html = self.getHTML(link, self.header)
        soup = BeautifulSoup(html, "html.parser")

        # Get Link Name
        seriesStr = str(series)
        if series < 10:
            seriesStr = "0" + seriesStr
        linkName = rules[0] + seriesStr + rules[1]
        log(linkName)

        for i in soup.find_all('div', {'class': 'attachlist'}):
            links = i('a')
            for link in links:
                linkText = link.get_text()
                if ambiSearch:
                    if seriesStr in linkText:
                        if all(word in linkText for word in rules):
                            downloadLink = link.get('href')
                            downloadurl = baseURL + downloadLink
                            downloadHTML = self.getHTML(downloadurl, self.header)
                            return self.parseDownloadPage(downloadHTML)
                else:
                    if linkName in linkText:
                        downloadLink = link.get('href')
                        downloadurl = baseURL + downloadLink
                        downloadHTML = self.getHTML(downloadurl, self.header)
                        return self.parseDownloadPage(downloadHTML)


    def parseDownloadPage(self, html):
        soup = BeautifulSoup(html, "html.parser")
        for i in soup.find_all('a'):
            if '本地下载' in i.get_text():
                torrentLink = baseURL + i.get('href')
                return torrentLink
            
    
            
    def getDownloadLink1Lou(self, baseurl, tailurl, rules, series, ambiSearch):
        searchingURL = baseurl + tailurl
        downloadtail = self.searchDownloadURL1Lou(searchingURL, rules, series, ambiSearch)
        downloadurl = baseurl + downloadtail
        return downloadurl
    
    def searchDownloadURL1Lou(self, link, rules, series, ambiSearch):
        html = self.getHTML(link, self.header)
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
                if ambiSearch:
                    if seriesStr in linkText:
                        if all(word in linkText for word in rules):
                            downloadLink = link.get('href')
                            return downloadLink
                else:
                    if linkName in linkText:
                        downloadLink = link.get('href')
                        return downloadLink

    def downloadTorrent(self, link, name, series):
        filename = name + "_" + str(series) + ".torrent"
        r = requests.get(link, stream=True)
        if r.status_code == 200:
            r.raw.decode_content = True
            filepath = torrentSavingPath + name + '/'
            if not os.path.exists(filepath):
                os.mkdir(filepath)
            with open(filepath + filename, 'wb') as f:
                try:
                    shutil.copyfileobj(r.raw, f)
                    return filepath + filename
                except Exception as e:
                    raise e
            