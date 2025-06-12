import os
from html.parser import HTMLParser
import unittest

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href':
                    self.hrefs.append(value)

class TestLinks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parser = LinkParser()
        with open('index.html', 'r', encoding='utf-8') as f:
            parser.feed(f.read())
        cls.hrefs = parser.hrefs

    def test_link_targets_exist(self):
        base_dir = os.path.dirname(os.path.abspath('index.html'))
        for href in self.hrefs:
            if href.startswith(('http://', 'https://')):
                continue
            target = os.path.join(base_dir, href.split('#')[0].split('?')[0])
            self.assertTrue(
                os.path.exists(target),
                f"Missing file for link: {href}"
            )

if __name__ == '__main__':
    unittest.main()
