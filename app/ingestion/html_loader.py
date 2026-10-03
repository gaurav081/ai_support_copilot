from pathlib import Path
from bs4 import BeautifulSoup


def load_html(file_path: str) -> str:
    html = Path(file_path).read_text(encoding="utf-8")

    soup = BeautifulSoup(html, "html.parser")

    article = soup.find("article", class_="article")

    if article is None:
        raise ValueError("Could not find article content in the HTML document.")

    section_heading = article.find(
        lambda tag: tag.name in ["h2", "h3"]
        and tag.get_text(strip=True) == "In this section"
    )

    if section_heading:
        navigation_list = section_heading.find_next("ul")

        section_heading.decompose()

        if navigation_list:
            navigation_list.decompose()

    blocks = []

    for element in article.find_all(["h1", "h2", "h3", "p", "li"]):
        if element.name == "p" and element.parent.name == "li":
            continue

        text = element.get_text(" ", strip=True)

        if text:
            blocks.append(text)

    return "\n\n".join(blocks)