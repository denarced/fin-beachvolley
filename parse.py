"""Parse Finnish beach volleyball site to scrape data."""

import datetime
import logging
import re
import typing

from bs4 import BeautifulSoup

date_pattern = re.compile(r"""[0-3]?[0-9]\.(?:1?[0-9])?(?:\.[0-9]{2,4})?""")


def strip(value: str | None) -> str | None:
    if value is None:
        return value
    stripped = value.strip()
    if stripped == "":
        return None
    return stripped


def parse_event_anchor(anchor) -> list:
    text = strip(anchor.string)
    if text is None:
        return []
    date_range = parse_date_range(text)
    if not date_range:
        return []
    start_index = date_pattern.search(text).start()
    primary = text[:start_index].strip()
    return [extract_series(anchor)] + [primary] + date_range


def is_empty(lst: None | list[list]) -> bool:
    if lst is None:
        return True
    if not lst:
        return True
    for each in lst:
        if each:
            return False
    return True


def is_in_section(event: list[str], search_words: list[str]) -> bool:
    for each in search_words:
        found = False
        for piece in event:
            if each.casefold() in piece.casefold():
                found = True
                break
        if not found:
            return False
    return True


def contains(event: list[str], search_words: list[list[str]] | None):
    if is_empty(search_words):
        return True
    for section in search_words:
        if is_in_section(event, section):
            return True
    return False


def parse_html(html, limit, search_words: typing.Iterable | None):
    soup = BeautifulSoup(html, "html.parser")
    anchors = soup.find_all("a")
    events = []
    for each in anchors:
        event = parse_event_anchor(each)
        if event and contains(event, search_words):
            events.append(event)
    return events if limit < 0 else events[:limit]


def main():
    pass


if __name__ == "__main__":
    main()


def parse_date(text: str) -> str:
    stripped = text.strip(" .")
    pieces = stripped.split(".")
    date_pieces = []
    for index, each in enumerate(pieces):
        numeric = int(each)
        if index < 2:
            date_pieces.insert(0, f"{numeric:02d}")
        elif numeric < 1000:
            date_pieces.insert(0, 1000 * (datetime.date.today().year // 1000) + numeric)
        else:
            date_pieces.insert(0, numeric)
    return date_pieces


def parse_date_range(text: str) -> list:
    found = date_pattern.findall(text)
    logging.error("Found date range: %s", found)
    if not found:
        return []
    piece_lists = []
    for each in found:
        piece_lists.append(parse_date(each))
    piece_lists = piece_lists[::-1]
    result = []
    for index, each in enumerate(piece_lists):
        if len(each) < 2:
            assert index > 0, index
            each.insert(0, piece_lists[index - 1][1])
        if len(each) < 3:
            each.insert(0, datetime.date.today().year)
        result.insert(0, "-".join(str(e) for e in each))
    return result


def extract_series(event_anchor) -> str | None:
    event_li = event_anchor.find_parent("li")
    event_ul = event_li.find_parent("ul")
    series_li = event_ul.find_parent("li")
    return series_li.a.string.strip()


def find_events(html, limit, search_words: typing.Iterable | None, order_by: str):
    parsed = parse_html(html, limit, search_words)
    if order_by == "date":
        parsed.sort(key=lambda e: (e[2], e[0], e[1]))
    return parsed
