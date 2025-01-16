from typing import List, Dict

import httpx
from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup
from dataclasses import dataclass

all_traveled_links = list()
already_visited = set()

@dataclass
class URLData:
    links: List[Dict[str, str]]
    base_url: str

def construct_next_url(next, base="https://en.wikipedia.org/"):
    return f"{base}{next}"

def get_links_from_url(url: str) -> URLData:
    print(f"Getting links from {url}")
    r = httpx.get(url)

    parsed_url = urlparse(url)
    next_base_url = parsed_url.scheme + "://" + parsed_url.netloc

    soup = BeautifulSoup(r.text, "html.parser")
    links = []
    for link in soup.css.select("#mw-content-text a"):
        links.append({"href": link.get("href"), "text" : link.text })
    return URLData(links, next_base_url)


"""Main entry point
must pass in URL, for example:
https://en.wikipedia.org/wiki/Bear
"""
def get_url(url):
    print(f"getting {url}")
    result = get_links_from_url(url)
    links = result.links
    base_url = result.base_url
    next_urls = list()

    for link in links:
        if 'href' not in link:
            print('no href')
            continue

        if not link['href']:
            print('href is falsey')
            continue

        if link['href'] in already_visited:
            print('already traveled')
            continue

        if not link['href'].startswith("/wiki/"):
            print('not a wiki link')
            continue

        if not len(link['text']) > 0 or link['text'][0].isupper():
            print('now a lower case text')
            continue

        print("found match", link["href"], link["text"])
        already_visited.add(link["href"])
        all_traveled_links.append(link)
        next_url = construct_next_url(next=link['href'], base=base_url)
        next_urls.append(next_url)
        if not links:
            links = next_urls
            next_urls = list()
    print(all_traveled_links)
    return all_traveled_links
