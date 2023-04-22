import markdown
import argparse
from pathlib import Path
from bs4 import BeautifulSoup
from utils import save_json


def get_markdown_as_html(path):
    with path.open("r", encoding="utf8") as f:
        html = markdown.markdown(f.read())
        return BeautifulSoup(html, "html.parser")


def join_paragraphs(start, tags):
    paragraphs = []
    for i in range(start + 1, len(tags)):
        if tags[i].name == "p":
            paragraphs.append(tags[i].text)
        else:
            break
    return " ".join(paragraphs)


def html_to_json(soup: BeautifulSoup):
    tags = soup.find_all(["h4", "p"])
    qa = []
    for i in range(len(tags)):
        if tags[i].name == "h4":
            if tags[i].text.startswith("You"):
                qa.append({"question": join_paragraphs(i, tags)})
            elif tags[i].text.startswith("ChatGPT"):
                qa[-1].update({"answer": join_paragraphs(i, tags)})
            else:
                pass
    return qa


def parse_history(path):
    soup = get_markdown_as_html(path)
    return html_to_json(soup)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="You can parse your chat history with ChatGPT as simple JSON format.",
    )
    parser.add_argument(
        "-m", dest="markdown", type=Path, help="Parses given markdown file."
    )
    parser.add_argument(
        "-d",
        dest="dir",
        type=Path,
        help="Parses all markdown files in given directory.",
    )
    parser.add_argument("-o", dest="out", type=Path, help="Path for output JSON file.")
    args = parser.parse_args()
    out_path = args.out or Path("history.json")
    if args.markdown:
        if not args.markdown.exists():
            raise RuntimeError(f"{args.markdown} not exist!")
        save_json(out_path, parse_history(args.markdown))
    if args.dir:
        if not args.dir.exists():
            raise RuntimeError(f"{args.dir} not exist!")
        history = []
        for md in args.dir.glob("*.md"):
            history.extend(parse_history(md))
        save_json(out_path, history)
