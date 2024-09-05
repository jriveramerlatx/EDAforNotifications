import pytest
from StreamOfEvents import EventsReader
from unittest.mock import Mock


def test_EventsReader_fetch():
    mock_finder = Mock()
    category_name = "Category"
    expected_value = [f"{category_name}_{r:010}.txt" for r in range(3)]
    mock_finder.return_value = expected_value

    with EventsReader(event_name=category_name, finder=mock_finder) as R:
        ls = []
        for fn in R.fetch():
            ls.append(fn)
    assert ls == expected_value
