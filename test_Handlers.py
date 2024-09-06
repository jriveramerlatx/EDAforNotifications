import pytest
from pydantic import ValidationError
from Handlers import Category


def test_category_ok():
    """Tests that the Category class is initialized correctly."""

    name = "Sport"
    category = Category(id="S", name=name, action="add")

    assert category.id == "S"
    assert category.name == name


def test_category_no_ok():
    """Tests that the Category class fails for wrong data."""

    invalid_name = None
    with pytest.raises(ValidationError):
        category = Category(id="S", name=invalid_name, action="add")
