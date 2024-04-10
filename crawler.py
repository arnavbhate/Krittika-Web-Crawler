# SPDX-License-Identifier: MIT
import requests
from html.parser import HTMLParser
from urllib.parse import urljoin

website = "https://krittikaiitb.github.io/"


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag in ["a", "area", "link", "base", "iframe"]:
            for attr in attrs:
                if attr[0] in ["href", "src"]:
                    url = urljoin(website, attr[1])
                    # Check for local domain and some common file extensions
                    if url.startswith(website) and url.split(".")[-1] not in [
                        "css",
                        "js",
                        "pdf",
                        "txt",
                        "csv",
                        "jpg",
                        "jpeg",
                        "png",
                        "gif",
                        "svg",
                        "ico",
                        "mp4",
                        "mp3",
                    ]:
                        link = [url, True]
                    else:
                        link = [url, False]
                    if link not in self.links:
                        self.links.append(link)
        elif tag in [
            "audio",
            "embed",
            "img",
            "input",
            "script",
            "source",
            "track",
            "video",
        ]:
            for attr in attrs:
                if attr[0] == "src":
                    link = [urljoin(website, attr[1]), False]
                    if link not in self.links:
                        self.links.append(link)


def get_links(url: str, links: list) -> None:
    initial_length = len(links)

    # Get content of the page
    response = requests.get(url)
    content = response.text

    # Check if the content is HTML
    if "html" not in response.headers["Content-Type"]:
        return

    # Parse the content
    parser = Parser()
    parser.feed(content)

    # Get links
    for link in parser.links:
        for l in links:
            if link[0] == l[0]:
                break
        else:
            links.append(link)
    final_length = len(links)
    parser.close()

    # Recursively get links (local only)
    for link in links[initial_length:final_length]:
        if link[1]:
            get_links(link[0], links)


if __name__ == "__main__":
    links = [[website, "True"]]
    get_links(links[0][0], links)
    for link in links:
        print(link[0])
