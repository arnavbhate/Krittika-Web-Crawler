import requests
from html.parser import HTMLParser
from urllib.parse import urljoin


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag in ["a", "area", "link", "base"]:
            for attr in attrs:
                if attr[0] == "href":
                    self.links.append(attr[1])
        elif tag in [
            "audio",
            "embed",
            "iframe",
            "img",
            "input",
            "script",
            "source",
            "track",
            "video",
        ]:
            for attr in attrs:
                if attr[0] == "src":
                    self.links.append(attr[1])


def get_links(url: str, links: list) -> None:
    initial_length = len(links)

    # Get content of the page
    response = requests.get(url)
    content = response.text

    # Parse the content
    parser = Parser()
    parser.feed(content)

    # Get links
    for link in parser.links:
        if link.startswith("http"):
            resolved_link = link
        else:
            resolved_link = urljoin(url, link)
        if resolved_link not in links:
            links.append(resolved_link)
    final_length = len(links)

    # Recursively get links (local only)
    for link in links[initial_length:final_length]:
        if link.startswith("https://krittikaiitb.github.io/"):
            get_links(link, links)


if __name__ == "__main__":
    links = []
    get_links("https://krittikaiitb.github.io/", links)
    print("Links found:")
    for link in links:
        print(link)
