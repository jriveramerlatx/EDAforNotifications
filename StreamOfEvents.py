import glob
import pickle
import os
import logging
from tools import log_entry_exit


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger(__name__)


PATH = "./Stream/"


class EventsReader:
    def __init__(
        self,
        event_name="Category",
        finder=glob.iglob,
        consumer="default",
        test=False,
    ):
        self.test = test
        self.consumer = consumer
        self.storage_file = f"{event_name}.dat"
        self.event_name = event_name
        self.path = f"{PATH}/{self.event_name}_*.json"
        self.offset = {self.consumer: 0}
        self.max_offset = 0
        if os.path.isfile(self.storage_file):
            with open(self.storage_file, "rb") as f:
                self.offset = pickle.load(f)
                self.offset[self.consumer] = self.offset.get(self.consumer, 0)
        self.finder = filter(
            lambda x: self.get_current_offset(x) > self.offset[self.consumer],
            finder(self.path),
        )
        self.fn = ""
        # return self

    # log_entry_exit
    def __enter__(self):
        return self

    def fetch(self):
        logger.info(f"Start fetching data... (CURRENT: {self.offset[self.consumer]})")
        n = 0
        last_offset = self.offset[self.consumer]
        for self.fn in self.finder:
            current_file_offset = self.get_current_offset(self.fn)
            logger.debug(
                f"{current_file_offset=} > {self.offset[self.consumer]=} ==> {current_file_offset > self.offset[self.consumer]}"
            )
            if current_file_offset > last_offset:
                self.max_offset = max(self.max_offset, current_file_offset, last_offset)
                yield self.fn
                n += 1
        logger.debug(f"Finished fetching data... {n} event(s) processed")

    # log_entry_exit
    def get_current_offset(self, fn):
        basename = os.path.split(fn)[-1]
        basename = os.path.splitext(basename)[0]
        offset = basename.split("_")[-1]
        offset = int(offset)
        return offset

    def reset_offset(self):
        self.offset[self.consumer] = 0

    # log_entry_exit
    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug(f"Closing data... {self.fn=}")
        if self.test:
            self.offset[self.consumer] = 0
            logger.debug("TEST ACTIVATED -> offset=0")
        elif self.fn:
            self.offset[self.consumer] = self.max_offset
        else:
            logger.info(
                f"Offset for consumer  {self.consumer} offset {self.max_offset} with nothing to be saved"
            )
        with open(self.storage_file, "wb") as f:
            pickle.dump(self.offset, f)
        logger.info(f"Offset for consumer {self.consumer} {self.max_offset} saved")
