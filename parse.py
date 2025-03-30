"""Parse Finnish beach volleyball site to scrape data."""

import argparse
import datetime
import re
import typing

import requests
from bs4 import BeautifulSoup

date_pattern = re.compile(r"""[0-3]?[0-9]\.(?:1?[0-9])?(?:\.[0-9]{2,4})?""")


def strip(value: str | None) -> str | None:
    if value is None:
        return value
    stripped = value.strip()
    if stripped == "":
        return None
    return stripped


def parse_event_anchor(this_year: int, anchor) -> list:
    text = strip(anchor.string)
    if text is None:
        return []
    date_range = parse_date_range(this_year, text)
    if not date_range:
        return []
    start_index = date_pattern.search(text).start()
    primary = text[:start_index].strip()
    if len(date_range) == 1:
        date_range = date_range + date_range
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


def parse_html(this_year: int, html, limit, search_words: typing.Iterable | None):
    soup = BeautifulSoup(html, "html.parser")
    menu = soup.find("div", id="cssmenu")
    anchors = menu.find_all("a")
    events = []
    for each in anchors:
        event = parse_event_anchor(this_year, each)
        if event and contains(event, search_words):
            events.append(event)
    return events if limit < 0 else events[:limit]


def parse_date(this_year: int, text: str) -> str:
    stripped = text.strip(" .")
    pieces = stripped.split(".")
    date_pieces = []
    for index, each in enumerate(pieces):
        numeric = int(each)
        if index < 2:
            date_pieces.insert(0, f"{numeric:02d}")
        elif numeric < 1000:
            date_pieces.insert(0, 1000 * (this_year // 1000) + numeric)
        else:
            date_pieces.insert(0, numeric)
    return date_pieces


def parse_date_range(this_year: int, text: str) -> list:
    found = date_pattern.findall(text)
    if not found:
        return []
    piece_lists = []
    for each in found:
        piece_lists.append(parse_date(this_year, each))
    piece_lists = piece_lists[::-1]
    result = []
    for index, each in enumerate(piece_lists):
        if len(each) < 2:
            assert index > 0, index
            each.insert(0, piece_lists[index - 1][1])
        if len(each) < 3:
            each.insert(0, this_year)
        result.insert(0, "-".join(str(e) for e in each))
    return result


def extract_series(event_anchor) -> str | None:
    event_li = event_anchor.find_parent("li")
    assert event_li is not None, f'Can\'t find parent for "{event_anchor}"'
    event_ul = event_li.find_parent("ul")
    series_li = event_ul.find_parent("li")
    return series_li.a.string.strip()


def find_events(this_year: int, html, limit, search_words: typing.Iterable | None, order_by: str):
    parsed = parse_html(this_year, html, limit, search_words)
    if order_by == "date":
        parsed.sort(key=lambda e: (e[2], e[0], e[1]))
    return parsed


def parse_filters(values):
    values = [] if values is None else values
    filters = []
    for each in values:
        pieces = [e.strip() for e in each.split(",")]
        pieces = [e for e in pieces if e != ""]
        if pieces:
            filters.append(pieces)
    return filters


def add_gaps(events, index):
    pairs = []
    for idx in range(0, len(events) - 1, 1):
        first = datetime.date.fromisoformat(events[idx][index])
        second = datetime.date.fromisoformat(events[idx + 1][index])
        if (second - first).days <= 1:
            if pairs and pairs[-1][1] == idx:
                pairs[-1][1] = idx + 1
            else:
                pairs.append([idx, idx + 1])
    gapped = []
    inserted = set()
    for each in pairs:
        alpha = each[0]
        if alpha > 0:
            inserted.add(alpha)
        omega = each[1] + 1
        if omega < len(events):
            inserted.add(omega)
    for idx, each in enumerate(events):
        if idx in inserted:
            gapped.append(None)
        gapped.append(each)
    return gapped


def format_date(date):
    return datetime.date.fromisoformat(date).strftime("%a %Y-%m-%d")


def create_past_filter(today, enabled):
    def filter_nothing(events):
        return events

    def filter_past(events):
        filtered = []
        for each in events:
            if datetime.date.fromisoformat(each[3]) >= today:
                filtered.append(each)
        return filtered

    return filter_past if enabled else filter_nothing


def main(args):
    res = requests.get(args.url, timeout=10)
    res.raise_for_status()
    this_year = datetime.date.today().year
    events = find_events(
        this_year,
        res.text,
        args.limit,
        parse_filters(args.include),
        "date" if args.sort_by_date else None,
    )
    filter_by_date = create_past_filter(datetime.date.today(), not args.include_past)
    events = add_gaps(
        filter_by_date(events),
        2,
    )
    for each in events:
        if each is None:
            print(*(4 * ["|"]), sep="\t")
            continue
        print(format_date(each[2]), format_date(each[3]), each[1], each[0], sep="\t")


def cli():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "--url",
        "-u",
        help="URL for beach volleyball site to scrape.",
        default="https://beachvolley.torneopal.fi",
    )
    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        help="Limit events to specific count. <0 means there's no limit.",
        default=-1,
    )
    parser.add_argument(
        "--include",
        "-i",
        nargs="+",
        help=(
            "Only include events where all comma separated words are "
            'found.  E.g. "t18,07" would roughly only include events '
            "in T18 series taking place in July."
        ),
    )
    parser.add_argument(
        "--sort-by-date",
        "-d",
        action="store_true",
        help="When set, results are sorted by date in ascending order (oldest first).",
    )
    parser.add_argument(
        "--include-past", "-p", action="store_true", help="When set, include past events."
    )
    return parser.parse_args()


if __name__ == "__main__":
    main(cli())
