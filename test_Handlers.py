import pytest
from pydantic import ValidationError
from Handlers import Category


def test_category_ok():
    """Tests that the Category class is initialized correctly."""

    category_name = "Fun"
    category = Category(name=category_name)

    assert (
        category.name == category_name
    )  # Assert that the name attribute is set correctly


def test_category_no_ok():
    """Tests that the Category class fails for wrong data."""

    invalid_name = None  # Example of an invalid name (None)
    with pytest.raises(ValidationError):
        category = Category(name=invalid_name)
