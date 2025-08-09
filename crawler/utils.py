from urllib.parse import urlparse
import urllib.robotparser
import time

def get_site_root(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"

def load_seed_urls(seed_urls_file):
    with open(seed_urls_file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith("//")]
    return urls

class Domains_cache():
    def __init__(self, request_delay_in_milliseconds):
        self.list = {}
        self.request_delay_in_milliseconds = request_delay_in_milliseconds

    def check_url(self, url):
        root = get_site_root(url)
        timestamp_in_milliseconds = int(time.time() * 1000)
        if root in self.list:
            rp = self.list[root]['rp']
            can_request =  rp.can_fetch('RubzBot', url)
            valid_delay = timestamp_in_milliseconds > self.list[root]['last_visited'] + self.request_delay_in_milliseconds
            return (can_request, valid_delay)
        else:
            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(f"{root}/robots.txt")
            rp.read()
            can_request =  rp.can_fetch('RubzBot', url)
            self.list[root] = {'last_visited': timestamp_in_milliseconds,
                               'rp': rp}
            return (can_request, True)
