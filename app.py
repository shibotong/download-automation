import TorrentDownload
from utility import downloadRuleURL, DownloadError
import Aria
import json
import sched, time

s = sched.scheduler(time.time, time.sleep)
td = TorrentDownload.TorrentDownload()

def main(sc):
    downloadFile = open(downloadRuleURL)
    series = json.load(downloadFile)
    for item in series:
        print(item['name'])
        try:
            torrentURL = td.downloadSeries(item)
            Aria.addTorrentToAria2(torrentURL)
            item['series'] += 1
        except DownloadError as error:
            print(error)
         
    with open(downloadRuleURL, "w") as outfile:
        json.dump(series, outfile)
    sc.enter(60 * 60 * 24, 1, main, (sc, ))

if __name__ == "__main__":
    s.enter(0, 1, main, (s, ))
    s.run()