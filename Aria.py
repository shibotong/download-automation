import aria2p
from utility import host
# initialization, these are the default values
aria2 = aria2p.API(
    aria2p.Client(
        host=host,
        port=6800,
        secret="NOBODYKNOWSME"
    )
)

def addTorrentToAria2(pathOfTorrent) -> aria2p.Download:
    # add downloads
    try:
        download = aria2.add_torrent(pathOfTorrent)
        return download
    except Exception as e:
        raise e
