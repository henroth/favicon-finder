import datetime
import sqlite3

CREATE_TABLE = ('CREATE TABLE IF NOT EXISTS favicons ('
                'id INTEGER PRIMARY KEY, '
                'url text NOT NULL, '
                'favicon text, '
                'created text NOT NULL)')

DROP_TABLE = "DROP TABLE IF EXISTS favicons"

CREATE_INDEX = "CREATE UNIQUE INDEX idx_favicons_url ON favicons (url)"

INSERT = "INSERT INTO favicons (url, favicon, created) VALUES (?, ?, ?)"
UPDATE = "UPDATE favicons SET favicon = ? where url = ?"
SELECT_BY_URL = "SELECT id, favicon, created FROM favicons WHERE url=?"

class Favicon(object):
    def __init__(self, url, favicon):
        self.url = url
        self.favicon = favicon

class FaviconDatabase(object):
    def __init__(self, name='favicon.db'):
        self.conn = sqlite3.connect(name)

    def create_table(self):
        with self.conn as cursor:
            cursor.execute(CREATE_TABLE)
            cursor.execute(CREATE_INDEX)
        
    def drop_table(self):
        with self.conn as cursor:
            cursor.execute(DROP_TABLE)
        
    def insert_or_update(self, url, favicon):
        with self.conn as cursor:
            c = cursor.cursor()
            c.execute(SELECT_BY_URL, (url,))
            row = c.fetchone()
            if row:
                # TODO may want to check that the favicon has actually changed
                # TODO may want to include a last_updated time stamp
                c.execute(UPDATE, (favicon, url))
            else:
                c.execute(INSERT, (url, favicon, datetime.datetime.now()))

    def find(self, url):
        cursor = self.conn.cursor()
        cursor.execute(SELECT_BY_URL, (url,))
        row = cursor.fetchone()
        cursor.close()

        if row:
            _, favicon, created = row
            return Favicon(url, favicon)
        else:
            return None
    
    def close(self):
        self.conn.close()
    
if __name__ == "__main__":
    pass
