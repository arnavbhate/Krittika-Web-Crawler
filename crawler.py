import requests


def get_links(url: str, links: list) -> None:
    initial_length = len(links)
    response = requests.get(url)
    content = response.text


if __name__ == "__main__":
    links = []
    get_links("https://krittikaiitb.github.io/", links)
