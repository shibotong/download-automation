import WebScraper
import unittest

class TestTorrent(unittest.TestCase):

    def test_searchTorrentLink(self):
        scraper = WebScraper.WebScraper()
        html = "<ul class='attachlist'><a href='https://unittest'>OPFans 1111 [1080P]</a></ul>"
        rules = ["OPFans", "[1080P]"]
        series = 1111
        link = scraper.searchTorrentURL(html, rules, series, True)
        self.assertEqual(link, "https://unittest")

if __name__ == '__main__':
    unittest.main()
