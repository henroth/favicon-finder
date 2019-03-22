import threading
import database
import favicon
import queue
import time

def worker(url, results):
    try:
        print("GET %s" % (url, ))
        fav = favicon.get_favicon(url)
        print("GOT %s => %s" % (url, fav))
        results.put((url, fav))
    except Exception as e:
        print("Failed getting %s: %s" % (url, e))
    
def run(urls, max_threads=200):
    # TODO probably want to be more careful as this will drop the
    #      whole db if it exists
    db = database.FaviconDatabase()
    db.drop_table()
    db.create_table()

    results = queue.Queue()
    threads = []    
    count = 1
    total = len(urls)
    while urls:
        # remove finished threads
        threads = [ t for t in threads if t.is_alive() ]

        # Add new workers, up to the max
        while urls and len(threads) < max_threads:
            print("Starting url %d of %d" % (count, total))
            count += 1
            url = urls.pop()
            t = threading.Thread(target=worker, args=(url, results))
            t.start()
            threads.append(t)
            
        # Get results from the queue and write them to the DB
        # We do it here because sqlite requires writes from the same thread
        while not results.empty():
            url, fav = results.get()
            print("Insert %s => %s" % (url, fav))
            db.insert_or_update(url, fav)

    # Wait for any lingering threads
    for t in threads:
        t.join()

    # Write any remaining results
    while not results.empty():
        url, fav = results.get()
        print("Insert %s => %s" % (url, fav))
        db.insert_or_update(url, fav)

    db.close()
    
if __name__ == "__main__":
    urls = []
    with open('top-1m.csv', 'r') as f:
        count = 0
        for line in f:
            if len(urls) >= 200000:
                break
            place, domain = line.strip().split(',')
            urls.append("http://%s" % domain)
            
    run(urls)
