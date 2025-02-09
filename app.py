from AutoDownloads import AutoDownloads
from utility import downloadRuleURL, period, log, push_notification, baseURL, torrentSavingPath
from datetime import datetime, date, timedelta
import Aria
import json
import sched, time
from DownloadItem import DownloadItem


import WebScraper
import TorrentDownloader

s = sched.scheduler(time.time, time.sleep)
ws = WebScraper(baseURL)
tdr = TorrentDownloader(torrentSavingPath)

downloadItems = []

def main(sc, dateTime):
    try:
        today = date.today()
        if today != dateTime:
            print('-------' + str(today) + '--------')  
        log(datetime.now())
        downloadFile = open(downloadRuleURL)
        seriesItem = json.load(downloadFile)
        for item in seriesItem:
            try:
                while True:
                    torrentItem = DownloadItem(item)
                    downloadItem(torrentItem)
                    item['series'] += 1
                    if 'number' in item:
                        item['number'] += 1
            except Exception as error:
                log(error)
                pass
        downloadFile.close()
        with open(downloadRuleURL, "w", encoding="utf-8") as outfile:
            json.dump(seriesItem, outfile, ensure_ascii=False)

        checkDownloads()
    except Exception as error:
        log(error)
        push_notification("Error", "An error occured", "")
        pass

    sc.enter(period, 1, main, (sc,today))

def downloadItem(item: DownloadItem):
    torrentURL = ws.searchTorrentURL(item)
    savedTorrentPath = tdr.download(item.seriesName, item.currentDownload, torrentURL)
    download = Aria.addTorrentToAria2(savedTorrentPath)
    print(item.downloadingText())

    downloadItem = AutoDownloads(item.seriesName, item.season, item.currentDownload, item.number, download, item.icon)
    downloadItems.append(downloadItem)


def checkDownloads():
    for downloadItem in downloadItems:
        if downloadItem.updateStatus():
            downloadItems.remove(downloadItem)
            



if __name__ == "__main__":
    yesterday =  date.today() - timedelta(days=1)
    today = date.today()
    print("Starting....")
    s.enter(0, 1, main, (s, yesterday))
    s.run()