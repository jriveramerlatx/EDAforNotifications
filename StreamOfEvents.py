import glob
import pickle
import os
import logging
from tools import log_entry_exit


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s %(name)s %(message)s %(levelname)s"
)
logger = logging.getLogger(__name__)

PATH = "./Stream/"


class EventsReader:
    def __init__(self, event_name="Category", finder=glob.iglob):
        self.finder = finder
        self.storage_file = f"{event_name}.dat"
        self.event_name = event_name
        self.path = f"{PATH}/{self.event_name}_*.json"
        self.offset = 0
        if os.path.isfile(self.storage_file):
            with open(self.storage_file, "rb") as f:
                self.offset = pickle.load(f)
        self.fn = ""
        # return self

    # log_entry_exit
    def __enter__(self):
        return self

    def fetch(self):
        for r in self.finder(self.path):
            if self.get_current_offset(r) >= self.offset:
                yield r

    # log_entry_exit
    def get_current_offset(self, fn):
        basename = os.path.split(fn)[-1]
        basename = os.path.splitext(basename)[0]
        offset = basename.split("_")[-1]
        offset = int(offset)
        return offset

    # log_entry_exit
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.fn == "":
            pass
        else:
            self.offset = self.get_current_offset(self.fn)
            with open(self.storage_file, "wb") as f:
                pickle.dump(self.offset, f)
