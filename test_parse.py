import pytest

from parse import contains, find_events, parse_date_range, parse_html


def test_parse_html():
    with open("testdata/page.html", encoding="utf-8") as file:
        result = parse_html(
            file.read(), -1, [["miehet 55"], ["miehet", "kalajoki"], ["tytöt 18", "finaalit"]]
        )
    assert result == [
        ["Masters", "Masters miehet 55", "2024-07-28"],
        ["Miehet", "Kalajoki", "2024-07-12", "2024-07-14"],
        ["JNBT miehet", "Kalajoki", "2024-07-13"],
        ["Tytöt 18", "Tampere Finaalit T18", "2024-08-10", "2024-08-11"],
        ["JNCT miehet", "Kalajoki", "2024-07-12"],
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
    assert parse_date_range(text) == expected


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
            file.read(),
            -1,
            [["miehet 55"], ["miehet", "kalajoki"], ["tytöt 18", "finaalit"]],
            "date",
        )
    assert result == [
        ["JNCT miehet", "Kalajoki", "2024-07-12"],
        ["Miehet", "Kalajoki", "2024-07-12", "2024-07-14"],
        ["JNBT miehet", "Kalajoki", "2024-07-13"],
        ["Masters", "Masters miehet 55", "2024-07-28"],
        ["Tytöt 18", "Tampere Finaalit T18", "2024-08-10", "2024-08-11"],
    ]
