import database
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin

def compose_link(url, favicon):
    return urljoin(url, favicon)

def download_page(url, timeout=3.0):
    page = requests.get(url, timeout=timeout)
    return (page.url, page.status_code, page.text)

def find_favicon(page):
    bs = BeautifulSoup(page, 'html.parser')
    tag = bs.find(rel="shortcut icon")
    return tag.get('href') if tag else None

def compose_favicon(url, raw_favicon_link):
    if raw_favicon_link.startswith('http'):
        return raw_favicon_link
    return compose_link(url, raw_favicon_link)

def get_favicon(url):
    try:
        # TODO Will need to check status potentially if we want to
        #      decide to retry them at a future point
        final_url, status, page = download_page(url)
        raw_favicon = find_favicon(page)

        # Some pages may not have a favicon
        if not raw_favicon:
            return None

        # If the page is redirected and the favicon is relative then it
        # will be relative to the final url, not the original
        favicon = compose_favicon(final_url, raw_favicon)
        return favicon
    except Exception as e:
        # TODO log the error better
        print("Failed getting %s: %s" % (url, e))
        return None

class FaviconService(object):
    def __init__(self, database):
        self.database = database

    def get_favicon(self, url, fresh=False):
        if fresh:
            return self._find_and_store(url)
        favicon = self.database.find(url)
        if favicon:
            return favicon

        return self._find_and_store(url)

    def _find_and_store(self, url):
        favicon = get_favicon(url)
        # TODO if the original url is redirect we may want to store both the orig
        #      and the redirect as having this favicon
        self.database.insert(url, favicon)
        return database.Favicon(url, favicon)
        
# These functions are mostly to facilitate the testing of parsing out the favicon link
# without needing to keep downloading the pages
def save_page(filename, page):
    with open(filename, 'w') as f:
        f.write(page)

def load_page(filename):
    with open(filename, 'r') as f:
        return f.read()

def download_and_save_page(url, filename):
    _, _, page = download_page(url)
    save_page(filename, page)

def display_favicon(url):
    print('-----')
    print("url: %s" % url)
    print("fav: %s" % get_favicon(url))
    
if __name__ == "__main__":
    # Save a couple pages locally for testing
    #download_and_save_page("http://example.com", "example.html")
    #download_and_save_page("http://news.ycombinator.com", "hackernews.html")
    #download_and_save_page("http://yahoo.com", "yahoo.html")
    #download_and_save_page("http://www.google.com", "google.html")

    display_favicon("http://example.com")
    display_favicon("http://news.ycombinator.com")
    display_favicon("http://yahoo.com")
    display_favicon("http://www.google.com")

    
    
