import unittest
import favicon

class FaviconTests(unittest.TestCase):
    def test_compose_link_1(self):
        url = "http://www.example.com"
        fav = "favicon.ico"
        expected = "http://www.example.com/favicon.ico"
        result = favicon.compose_link(url, fav)
        self.assertEqual(result, expected)
        
    def test_compose_link_2(self):
        url = "http://www.example.com/"
        fav = "favicon.ico"
        expected = "http://www.example.com/favicon.ico"
        result = favicon.compose_link(url, fav)
        self.assertEqual(result, expected)

    def test_compose_link_3(self):
        url = "http://www.example.com/"
        fav = "/favicon.ico"
        expected = "http://www.example.com/favicon.ico"
        result = favicon.compose_link(url, fav)
        self.assertEqual(result, expected)

    def test_compose_link_4(self):
        url = "http://www.example.com?q1=hello"
        fav = "favicon.ico"
        expected = "http://www.example.com/favicon.ico"
        result = favicon.compose_link(url, fav)
        self.assertEqual(result, expected)

    def test_find_favicon_link(self):
        page = favicon.load_page("test_data/example.html")
        raw_link = favicon.find_favicon(page)
        self.assertIsNone(raw_link)
        
        page = favicon.load_page("test_data/google.html")
        raw_link = favicon.find_favicon(page)
        self.assertIsNone(raw_link)

        page = favicon.load_page("test_data/hackernews.html")
        raw_link = favicon.find_favicon(page)
        self.assertIsNotNone(raw_link)
        self.assertEqual(raw_link, 'favicon.ico')

        page = favicon.load_page("test_data/yahoo.html")
        raw_link = favicon.find_favicon(page)
        self.assertIsNotNone(raw_link)
        self.assertEqual(raw_link, 'https://s.yimg.com/rz/l/favicon.ico')

    def test_compose_favicon(self):
        result = favicon.compose_favicon('http://example.com', 'favicon.ico')
        self.assertEqual(result, 'http://example.com/favicon.ico')

        result = favicon.compose_favicon('http://example.com', 'https://example.com/favicon.ico')
        self.assertEqual(result, 'https://example.com/favicon.ico')
        
if __name__ == "__main__":
    unittest.main()
    
        
