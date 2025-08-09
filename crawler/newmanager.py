### Importations
from collections import deque
import threading
import time


import utils
from crawler import crawl

### Global variables
seed_urls = utils.load_seed_urls('../data/seed_urls.txt')
urls_to_visit = deque()
for url in seed_urls:
    urls_to_visit.append(url)

domains_cache = utils.Domains_cache(request_delay_in_milliseconds=1000)

pages = []

lock_urls = threading.Lock()
lock_domains = threading.Lock()
lock_pages = threading.Lock()


### Function definitions


def threaded_crawler(nb_pages):
    global urls_to_visit
    global domains_cache
    global pages
    global lock_urls, lock_domains, lock_pages

    thread_pages = []

    while len(thread_pages) < nb_pages:
        with lock_urls:
            if not urls_to_visit:
                break
            next_url = urls_to_visit.popleft()
        with lock_domains:
            can_request, valid_delay = domains_cache.check_url(next_url)
        if can_request:
            if valid_delay:
                page = crawl(next_url)
                thread_pages.append(page['title'])
                with lock_urls:
                    urls_to_visit.extend(page['links'])
            else:
                with lock_urls:
                    urls_to_visit.append(next_url)

    with lock_pages:
        pages.extend(thread_pages)

            
def launch_crawlers(nb_threads, nb_pages_per_thread):
    threads = []
    for _ in range(nb_threads):
        t = threading.Thread(target=threaded_crawler, args=(nb_pages_per_thread,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()


        


if __name__ == "__main__":
    THREADS = 5
    TOTAL_PAGES = 200
    PAGES_PER_THREAD = TOTAL_PAGES // THREADS

    start_time = time.time()
    launch_crawlers(THREADS, PAGES_PER_THREAD)
    elapsed_time = time.time() - start_time

    print(f"{THREADS} threads, {len(pages)}/{TOTAL_PAGES} pages done, in {elapsed_time:.2f} s, {len(pages)/elapsed_time:.2f} pages per second")




