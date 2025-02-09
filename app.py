import TorrentDownload
from AutoDownloads import AutoDownloads
from utility import downloadRuleURL, period, log, push_notification
from datetime import datetime, date, timedelta
import Aria
import json
import sched, time
from DownloadItem import DownloadItem

s = sched.scheduler(time.time, time.sleep)
td = TorrentDownload.TorrentDownload()

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
                    torrentURL = td.downloadSeries(item)
                    download = Aria.addTorrentToAria2(torrentURL)
                    name = item['name']
                    season = item['season']
                    series = item['series']
                    number = 0
                    if 'number' in item:
                        number = item['number']
                    icon = item['icon']
                    print(f'Downloading {name} Season {season} Series {series}')
                    
                    downloadItem = AutoDownloads(name, season, series, number, download, icon)
                    downloadItems.append(downloadItem)
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