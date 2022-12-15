import TorrentDownload
from AutoDownloads import AutoDownloads
from utility import downloadRuleURL, DownloadError, period
from datetime import date
import Aria
import json
import sched, time

s = sched.scheduler(time.time, time.sleep)
td = TorrentDownload.TorrentDownload()

downloadItems = []

def main(sc):
    downloadFile = open(downloadRuleURL)
    seriesItem = json.load(downloadFile)
    print('-------' + str(date.today()) + '--------')
    for item in seriesItem:
        print(item['name'] + ' ' + str(item['series']))
        try:
            torrentURL = td.downloadSeries(item)
            download = Aria.addTorrentToAria2(torrentURL)
            name = item['name']
            season = item['season']
            series = item['series']
            number = 0
            if 'number' in item:
                number = item['number']
            icon = item['icon']
            
            downloadItem = AutoDownloads(name, season, series, number, download, icon)
            downloadItems.append(downloadItem)
            item['series'] += 1
            if 'number' in item:
                item['number'] += 1
        except DownloadError as error:
            print(error)
    downloadFile.close()
    with open(downloadRuleURL, "w") as outfile:
        json.dump(seriesItem, outfile)

    checkDownloads()
    sc.enter(period, 1, main, (sc, ))

def checkDownloads():
    for downloadItem in downloadItems:
        if downloadItem.updateStatus():
            downloadItems.remove(downloadItem)
            



if __name__ == "__main__":
    s.enter(0, 1, main, (s, ))
    s.run()