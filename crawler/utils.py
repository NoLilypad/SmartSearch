from urllib.parse import urlparse

def get_site_root(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


