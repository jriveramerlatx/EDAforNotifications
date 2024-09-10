import pickle
import os


class Database(object):
    def set(self, id, data):
        pass

    def get(self, id):
        pass

    def rows(self):
        return []

    def remove(self, id):
        pass

    def save(self):
        pass


class FileDatabase(Database):
    def __init__(
        self, name, loader=pickle.load, isfile=os.path.isfile, open=open
    ) -> None:
        self.name = name
        if isfile(self.name):
            with open(self.name, "rb") as f:
                self.data = loader(f)
        else:
            self.data = dict()

    def get(self, id):
        return self.data.get(id)

    def set(self, id, data):
        self.data[id] = data

    def rows(self):
        return [r for r in self.data.values()]

    def remove(self, id):
        del self.data[id]

    def save(self, dump=pickle.dump, open=open):
        with open(self.name, "wb") as f:
            dump(self.data, f, pickle.HIGHEST_PROTOCOL)
