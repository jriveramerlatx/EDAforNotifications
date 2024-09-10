from Storage import FileDatabase
from unittest import mock


class Mock_open(object):
    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass


def test_FileDatabase_new_datafile():
    dbname = "test.dat"
    db = FileDatabase(dbname, isfile=lambda x: False)
    assert db.get(1) == None


def test_FileDatabase_with_data():
    dbname = "test.dat"
    mock_loader = mock.Mock()
    mock_loader.return_value = {1: "test"}
    db = FileDatabase(dbname, loader=mock_loader, open=Mock_open, isfile=lambda x: True)
    x = db.get(1)
    assert x == "test"


def test_FileDatabase_remove():
    mock_dump = mock.Mock()
    dbname = "test.dat"
    db = FileDatabase(dbname, isfile=lambda x: False)
    x = db.set(1, "new data")
    y = db.get(1)
    assert y == "new data"
    db.remove(1)
    y = db.get(1)
    assert y is None


def test_FileDatabase_new_data():
    mock_dump = mock.Mock()
    dbname = "test.dat"
    db = FileDatabase(dbname, isfile=lambda x: False)
    x = db.set(1, "new data")
    y = db.get(1)
    assert y == "new data"
    db.save(
        dump=mock_dump,
        open=Mock_open,
    )
    saved_data = mock_dump.call_args[0][0]
    db2 = FileDatabase(
        dbname,
        loader=lambda x: saved_data,
        open=Mock_open,
        isfile=lambda x: True,
    )
    z = db2.get(1)
    assert y == z
