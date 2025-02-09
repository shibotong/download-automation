import requests
import os
import shutil
from utility import log

class TorrentDownloader:

    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    }

    def __init__(self, torrentSavePath):
        self.torrentSavePath = torrentSavePath

    def download(self, name, series, link) -> str:
        filename = name + "_" + str(series) + ".torrent"
        r = requests.get(link, headers=self.header, stream=True)
        log('downloading torrent' + r)
        if r.status_code == 200:
            r.raw.decode_content = True
            filepath = self.torrentSavePath + name + '/'
            log(filepath)
            if not os.path.exists(filepath):
                os.mkdir(filepath)
            with open(filepath + filename, 'wb') as f:
                try:
                    shutil.copyfileobj(r.raw, f)
                    return filepath + filename
                except Exception as e:
                    raise e
        else:
            raise Exception("Error downloading torrent")