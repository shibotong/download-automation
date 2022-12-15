import requests
from bs4 import BeautifulSoup
import shutil
import os
from utility import baseURL, DownloadError



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
            print("worm failed")
            return ""

    def downloadSeries(self, item):
        seriesName = item['name']
        seriesLink = baseURL + item['link']
        currentDownload = item['series']
        rules = item['rule']

        # create a dir if not exist
        filepath = "./" + seriesName + '/'
        if not os.path.exists(filepath):
            os.makedirs(seriesName)

        torrentLink = self.getDownloadLink(seriesLink, rules, currentDownload)
        if torrentLink is not None:
            torrentPath = self.downloadTorrent(torrentLink, seriesName, currentDownload)
            return torrentPath
        else:
            raise DownloadError('DownloadError: no download link')
            
    def getHTML(self, url, header):
        try:
            r = requests.get(url, headers=header)
            r.raise_for_status()
            return r.text
        except:
            print("worm failed")
            return ""


    def getDownloadLink(self, link, rules, series):
        html = self.getHTML(link, self.header)
        soup = BeautifulSoup(html, "html.parser")
        for i in soup.find_all('div', {'class': 'attachlist'}):
            links = i('a')
            for link in links:
                linkText = link.get_text()
                if str(series) in linkText:
                    if all(word in linkText for word in rules):
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


    def downloadTorrent(self, link, name, series):
        filename = name + "_" + str(series) + ".torrent"
        r = requests.get(link, stream=True)
        if r.status_code == 200:
            r.raw.decode_content = True
            filepath = "/downloads/Torrents/" + name + '/'
            if os.path.exists(filepath) == False:
                os.mkdir(filepath)
            with open(filepath + filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

            print('torrent Download successful: ', filename)
            return filepath + filename