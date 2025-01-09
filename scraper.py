import httpx
import re
from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup

def get_url(url, all_traveled_links=[]):
    r = httpx.get(url)

    parsed_url = urlparse(url)
    next_base_url = parsed_url.scheme + "://" + parsed_url.netloc

    soup = BeautifulSoup(r.text, "html.parser")
    links = []
    for link in soup.css.select("#mw-content-text a"):
        links.append({"href": link.get("href"), "text" : link.text })

    pattern = re.compile("^[a-z]")

    for link in links:
        if "/wiki/" in link['href'] and pattern.match(link['text']):
            print("found match", link["href"], link["text"])
            all_traveled_links.append({"href": link["href"], "text": link["text"]})
            next_url = construct_next_url(next=link['href'], base=next_base_url)
            get_url(next_url, all_traveled_links)
            break
        
    return links


def construct_next_url(next, base="https://en.wikipedia.org/"):
    return f"{base}{next}"
