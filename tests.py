import pathlib
import unittest
import os
from utils import Editions, download_and_merge
from parser import eenaduParser

class TestParser(unittest.TestCase):

    def setUp(self) -> None:
        files = os.listdir()
        for f in files:
            if f.endswith("pdf"):
                os.remove(f)

    def test_parse_today(self):
        parser = eenaduParser("cookies.txt")
        parser.get_edition(Editions.HYDERABAD)
        fname = parser.gen_filename().replace(".pdf", "_TEST.pdf")
        download_and_merge(fname, parser.get_links())
        self.assertTrue(pathlib.Path(fname).exists())

    def test_parse_past(self):
        parser = eenaduParser("cookies.txt", "01/01/2022")
        parser.get_edition(Editions.HYDERABAD)
        fname = parser.gen_filename().replace(".pdf", "_TEST.pdf")
        download_and_merge(fname, parser.get_links())
        self.assertTrue(pathlib.Path(fname).exists())

class TestUtils(unittest.TestCase):

    def setUp(self) -> None:
        if os.path.exists("test.pdf"):
            os.remove("test.pdf")

    def test_download_and_merge(self):
        download_and_merge("test.pdf", [("https://i.imgur.com/SozZ1aP.jpg", "https://i.imgur.com/BKoaI3P.png")])
        self.assertTrue(pathlib.Path("test.pdf").exists())

if __name__ == '__main__':
    unittest.main()