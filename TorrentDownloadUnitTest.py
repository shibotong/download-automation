import WebScraper
import DownloadItem
import unittest

class TestTorrent(unittest.TestCase):

    def test_searchTorrentLink(self):
        scraper = WebScraper.WebScraper("https://www.test.com/")
        html = "<ul class='attachlist'><a href='https://unittest'>OPFans 1111 [1080P]</a></ul>"
        rules = ["OPFans", "[1080P]"]
        series = 1111
        link = scraper.searchTorrentURL(html, rules, series, True)
        self.assertEqual(link, "https://unittest")

    def test_urlBuild(self):
        scraper = WebScraper.WebScraper("https://www.test.com/")
        url = scraper.fullURL("test")
        self.assertEqual(url, "https://www.test.com/test")


    def test_decodingItem(self):
        json = {
            "name": "One Piece",
            "link": "https://onepiece.com",
            "series": 1111,
            "rule": ["OPFans", "[1080P]"],
            "ambiSearch": True
        }
        item = DownloadItem.DownloadItem(json)
        self.assertEqual(item.seriesName, "One Piece")
        self.assertEqual(item.seriesLink, "https://onepiece.com")
        self.assertEqual(item.currentDownload, 1111)
        self.assertEqual(item.rules, ["OPFans", "[1080P]"])
        self.assertEqual(item.ambiSearch, True)

if __name__ == '__main__':
    unittest.main()
