import pytest

from parse import (
    add_gaps,
    contains,
    find_events,
    format_date,
    parse_date_range,
    parse_filters,
    parse_html,
)


def test_parse_html():
    with open("testdata/page.html", encoding="utf-8") as file:
        result = parse_html(
            2024, file.read(), -1, [["miehet 55"], ["miehet", "kalajoki"], ["tytöt 18", "finaalit"]]
        )
    assert result == [
        ["Masters", "Masters miehet 55", "2024-07-28", "2024-07-28"],
        ["Miehet", "Kalajoki", "2024-07-12", "2024-07-14"],
        ["JNBT miehet", "Kalajoki", "2024-07-13", "2024-07-13"],
        ["Tytöt 18", "Tampere Finaalit T18", "2024-08-10", "2024-08-11"],
        ["JNCT miehet", "Kalajoki", "2024-07-12", "2024-07-12"],
    ]


@pytest.mark.parametrize(
    "text, expected",
    [
        ["Jake 25.7", ["2024-07-25"]],
        ["25.7.", ["2024-07-25"]],
        ["1.1.10", ["2010-01-01"]],
        ["5.6. 8.6.", ["2024-06-05", "2024-06-08"]],
        ["5.6. 8.6.", ["2024-06-05", "2024-06-08"]],
        ["1.1.2024 - 2.1.2025", ["2024-01-01", "2025-01-02"]],
        ["12.-14.7", ["2024-07-12", "2024-07-14"]],
    ],
)
def test_parse_date_range(text, expected):
    assert parse_date_range(2024, text) == expected


@pytest.mark.parametrize(
    "event, search_words, expected",
    [
        [["Masters", "Kalajoki"], [["mast"]], True],
        [["Masters", "Kalajoki"], [["Joki"]], True],
        [["Masters", "Kalajoki"], [[]], True],
        [["Masters", "Kalajoki"], [], True],
        [["Masters", "Kalajoki"], None, True],
        [["Masters", "Kalajoki"], [["mast", "kalajoki"]], True],
        [["Masters", "Kalajoki"], [["mast", "paha"]], False],
    ],
)
def test_contains(event, search_words, expected):
    assert contains(event, search_words) is expected


def test_find_events():
    with open("testdata/page.html", encoding="utf-8") as file:
        result = find_events(
            2024,
            file.read(),
            -1,
            [["miehet 55"], ["miehet", "kalajoki"], ["tytöt 18", "finaalit"]],
            "date",
        )
    assert result == [
        ["JNCT miehet", "Kalajoki", "2024-07-12", "2024-07-12"],
        ["Miehet", "Kalajoki", "2024-07-12", "2024-07-14"],
        ["JNBT miehet", "Kalajoki", "2024-07-13", "2024-07-13"],
        ["Masters", "Masters miehet 55", "2024-07-28", "2024-07-28"],
        ["Tytöt 18", "Tampere Finaalit T18", "2024-08-10", "2024-08-11"],
    ]


@pytest.mark.parametrize(
    "year, days, expected_days",
    [
        [None, [], []],
        [2010, [1], [1]],
        [2011, [1, 2], [1, 2]],
        [2012, [1, 3], [1, 3]],
        [2013, [1, 2, 4], [1, 2, None, 4]],
        [2014, [1, 3, 4], [1, None, 3, 4]],
        [
            2015,
            [1, 2, 4, 5, 7, 8, 10, 12, 14],
            [1, 2, None, 4, 5, None, 7, 8, None, 10, 12, 14],
        ],
    ],
)
def test_add_gaps(year, days, expected_days):
    def to_events(day_list):
        events = []
        for each in day_list:
            if each is None:
                events.append(None)
            else:
                events.append([f"{year}-01-{each:02d}"])
        return events

    events = to_events(days)
    # EXERCISE
    with_gaps = add_gaps(events, 0)

    # VERIFY
    assert to_events(expected_days) == with_gaps


@pytest.mark.parametrize(
    "original, expected",
    [
        [[], []],
        [[" a\t"], [["a"]]],
        [["a", "b,c", "c,,d,e"], [["a"], ["b", "c"], ["c", "d", "e"]]],
    ],
)
def test_parse_filters(original, expected):
    assert expected == parse_filters(original)


def test_format_date():
    assert "Mon 2024-06-03" == format_date("2024-06-03")
