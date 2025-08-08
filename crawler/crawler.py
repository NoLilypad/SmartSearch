import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def crawl(seed_url):
    # Gets the page
    page = requests.get(seed_url)
    soup = BeautifulSoup(page.content, "html.parser")

    # Extracts page's title
    title = soup.title.string if soup.title else ""

    # Extracts visible text
    for script in soup(["script", "style"]):
        script.decompose()
    text = soup.get_text(separator=" ", strip=True)

    # Extracts all valid links (absolute URLs)
    links = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        # Ignore empty, javascript, mailto, or fragment-only links
        if href.startswith("#") or href.startswith("javascript:") or href.startswith("mailto:"):
            continue
        # Convert relative URLs to absolute
        absolute_url = urljoin(seed_url, href)
        # Only keep http(s) links
        parsed = urlparse(absolute_url)
        if parsed.scheme in ["http", "https"]:
            links.append(absolute_url)

    return {
        "title": title,
        "text": text,
        "links": links
    }
