from collections import deque
import sqlite3
import os
import urllib.robotparser

from crawler import crawl
import utils

# Launches crawling
if __name__ == "__main__":
    # DB setup
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'pages.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Queue of URLs to crawl
    urls_to_crawl = deque()

    # Initial seed
    urls_to_crawl.append(['https://fr.wikipedia.org'])

    

    while urls_to_crawl:
        print('urls_to_crawl length :',len(urls_to_crawl))
        # Get URL batch
        batch = urls_to_crawl.popleft()

        # Crawl each URL in the batch
        while batch:
            print('Batch length :',len(batch))
            # Get page
            next_url = batch.pop()

            # Checks if it can crawl the page
            root = utils.get_site_root(next_url)
            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(f"{root}/robots.txt")
            rp.read()
            can_crawl = rp.can_fetch("RubzBot", next_url)

            print(can_crawl)

            # Crawls the page
            if can_crawl:
                page = crawl(next_url)

            # Insert new batch of URL 
            urls_to_crawl.append(page['links'])

            # Insert page into DB
            try:
                c.execute(
                    "INSERT OR IGNORE INTO pages (url, title, text) VALUES (?, ?, ?)",
                    (next_url, page.get('title', ''), page.get('text', ''))
                )
                conn.commit()
            except Exception as e:
                print(f"DB error for {next_url}: {e}")

    conn.close()

    

