#!/usr/bin/env python


from Handlers import Category
from Handlers import Subscription
from Handlers import User
import argparse
import datetime
import json
import logging
import os
import random

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

STREAM_PATH = "./Stream/"


def ask_data(fullschema):
    schema = fullschema["properties"]
    data = dict(schema=fullschema["title"])
    data["data"] = {}
    for fname in schema.keys():
        data["data"][fname] = input(f"{schema[fname]['title']}: ")
    data["id"] = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    data["idempotent"] = random.randrange(1, 100000000000000)
    return data


def save_data(data):
    fn = "%(schema)s_%(id)s.json" % (data)
    fn = os.path.join(STREAM_PATH, fn)
    open(fn, "w").write(json.dumps(data))
    return fn


def main():
    parser = argparse.ArgumentParser(description="Envent Driven Main Processor")

    parser.add_argument(
        "-c", "--category", action="store_true", help="Create a category"
    )
    parser.add_argument("-u", "--user", action="store_true", help="Create user")
    parser.add_argument(
        "-s", "--subscription", action="store_true", help="Create subscription"
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)
        print("Verbose mode enabled.")

    if args.subscription:
        data = ask_data(Subscription.schema())
        fn = save_data(data)
        logger.info(f"Event generated: {fn}...")

    if args.user:
        data = ask_data(User.schema())
        fn = save_data(data)
        logger.info(f"Event generated: {fn}...")

    if args.category:
        data = ask_data(Category.schema())
        fn = save_data(data)
        logger.info(f"Event generated: {fn}...")


if __name__ == "__main__":
    main()
