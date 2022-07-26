import requests
from bs4 import BeautifulSoup
import shutil
import json
import os
import aria2p
import sched, time
s = sched.scheduler(time.time, time.sleep)


baseURL = 'https://www.btbtt12.com/'

header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ApplewebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
}

# initialization, these are the default values
aria2 = aria2p.API(
    aria2p.Client(
        host="http://192.168.4.186",
        port=6800,
        secret="NOBODYKNOWSME"
    )
)


def getHTML(url, header):
    try:
        r = requests.get(url, headers=header)
        r.raise_for_status()
        # print(r.request.headers)
        return r.text
    except:
        print("worm failed")
        return ""


def getDownloadLink(link, rules, series):
    html = getHTML(link, header)
    soup = BeautifulSoup(html, "html.parser")
    for i in soup.find_all('div', {'class': 'attachlist'}):
        links = i('a')
        for link in links:
            linkText = link.get_text()
            if str(series) in linkText:
                if all(word in linkText for word in rules):
                    downloadLink = link.get('href')
                    downloadurl = baseURL + downloadLink
                    downloadHTML = getHTML(downloadurl, header)
                    return parseDownloadPage(downloadHTML)


def parseDownloadPage(html):
    soup = BeautifulSoup(html, "html.parser")
    for i in soup.find_all('a'):
        if '本地下载' in i.get_text():
            torrentLink = baseURL + i.get('href')
            return torrentLink


def downloadTorrent(link, name, series):
    filename = name + "_" + str(series) + ".torrent"
    r = requests.get(link, stream=True)
    if r.status_code == 200:
        r.raw.decode_content = True
        filepath = "./" + name + '/'
        with open(filepath + filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        print('torrent Download successful: ', filename)
        return filepath + filename


def addTorrentToAria2(pathOfTorrent):
    # add downloads
    download = aria2.add_torrent(pathOfTorrent)
    print("added to aria2 " + pathOfTorrent)


def downloadSeries(item):
    seriesName = item['name']
    seriesLink = baseURL + item['link']
    currentDownload = item['series']
    rules = item['rule']

    # create a dir if not exist
    filepath = "./" + seriesName + '/'
    if not os.path.exists(filepath):
        os.makedirs(seriesName)

    torrentLink = getDownloadLink(seriesLink, rules, currentDownload)
    print(torrentLink)
    if torrentLink is not None:
        torrentPath = downloadTorrent(torrentLink, seriesName, currentDownload)
        addTorrentToAria2(torrentPath)
        item['series'] += 1
    else:
        print('no link skip this')


def main(sc):
    downloadFile = open('./downloadRule.json')
    series = json.load(downloadFile)
    for item in series:
        downloadSeries(item)
    with open("./downloadRule.json", "w") as outfile:
        json.dump(series, outfile)
    sc.enter(60 * 60 * 24, 1, main, (sc, ))

if __name__ == "__main__":
    s.enter(0, 1, main, (s, ))
    s.run()
