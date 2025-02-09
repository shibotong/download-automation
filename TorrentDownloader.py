import requests
import os
import shutil

class TorrnetDownloader:
    def __init__(self, torrentSavePath):
        self.torrentSavePath = torrentSavePath

    def download(self, name, series, link) -> str:
        filename = name + "_" + str(series) + ".torrent"
        r = requests.get(link, stream=True)
        if r.status_code == 200:
            r.raw.decode_content = True
            filepath = self.torrentSavePath + name + '/'
            if not os.path.exists(filepath):
                os.mkdir(filepath)
            with open(filepath + filename, 'wb') as f:
                try:
                    shutil.copyfileobj(r.raw, f)
                    return filepath + filename
                except Exception as e:
                    raise e