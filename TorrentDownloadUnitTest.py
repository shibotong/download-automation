import WebScraper
import DownloadItem
import FilePathController
import unittest

class TestTorrent(unittest.TestCase):

    def test_searchTorrentLink(self):
        scraper = WebScraper.WebScraper("https://www.test.com/")
        html = "<ul class='attachlist'><a href='abcdefg'>OPFans 1111 [1080P]</a></ul>"
        rules = ["OPFans", "[1080P]"]
        series = 1111
        link = scraper.searchTorrentURL(html, rules, series, True)
        self.assertEqual(link, "https://www.test.com/abcdefg")

    def test_urlBuild(self):
        scraper = WebScraper.WebScraper("https://www.test.com/")
        url = scraper.fullURL("test")
        self.assertEqual(url, "https://www.test.com/test")


    def test_decodingItem(self):
        json = {
            "name": "One Piece",
            "link": "https://onepiece.com",
            "season": 1,
            "series": 1111,
            "rule": ["OPFans", "[1080P]"],
            "ambiSearch": True,
            "icon": "icon"
        }
        item = DownloadItem.DownloadItem(json)
        self.assertEqual(item.seriesName, "One Piece")
        self.assertEqual(item.seriesLink, "https://onepiece.com")
        self.assertEqual(item.currentDownload, 1111)
        self.assertEqual(item.rules, ["OPFans", "[1080P]"])
        self.assertEqual(item.ambiSearch, True)

    def test_fileNewPath(self):
        controller = FilePathController.FilePathController('/test/Anime/')
        newPathNoNumber = controller.newPath("One Piece", 1, 1, 0, ".mkv")
        self.assertEqual(newPathNoNumber, "/test/Anime/One Piece/Season 1/One Piece - S1E1.mkv")

        newPathWithNumber = controller.newPath("One Piece", 1, 1, 1, ".mkv")
        self.assertEqual(newPathWithNumber, "/test/Anime/One Piece/Season 1/One Piece - S1E1 - [1].mkv")


if __name__ == '__main__':
    unittest.main()
