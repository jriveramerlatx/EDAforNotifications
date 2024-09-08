#!/usr/bin/env python

from Handlers import Category
from Handlers import Subscription
from Handlers import User
from Storage import FileDatabase
from StreamOfEvents import EventsReader
from tools import log_entry_exit
import argparse
import datetime
import json
import logging
import os
import random
import pandas as pd
from tabulate import tabulate

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger(__name__)

STREAM_PATH = "./Stream/"


def ask_data(fullschema):
    logger.info(f"Please provide the following data: {fullschema['title']}...")
    data = dict(data={}, schema=fullschema["title"])
    for fname in fullschema["properties"]:
        data["data"][fname] = input(f"{fullschema['properties'][fname]['title']}: ")
    data["id"] = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    data["idempotent"] = random.randrange(1, 100000000000000)
    return data


@log_entry_exit
def reset_offset(category_name):
    logger.info(f"Processing {category_name}...")
    with EventsReader(
        event_name=category_name, consumer=f"ConsumerOf{category_name}"
    ) as R:
        R.reset_offset()


def list_n_items(category_name, n, db):
    df = pd.DataFrame(db.rows())
    logger.info(f"List {n} items of {category_name}(s)... of df.size={df.shape}")
    print(tabulate(df.head(n), headers="keys", tablefmt="psql", showindex=False))


@log_entry_exit
def process_data(category_name, handler, db):
    logger.info(f"Processing {category_name}...")
    n = 0
    with EventsReader(
        event_name=category_name, consumer=f"ConsumerOf{category_name}"
    ) as R:
        for fn in R.fetch():
            logger.info(f"Event {fn} In Progress ...")
            with open(fn, "r") as file:
                logger.debug(f"Reading Event {fn} ...")
                data = json.load(file)
                logger.debug(f"Validating Event {fn} ...")
                x = handler(**data["data"])
                logger.debug(f"Handling Event {fn} action: {x.action}...")
                if x.action == "add":
                    db.set(id=x.id, data=x.model_dump())
            n += 1
        else:
            logger.warning(
                f"Processing {category_name} returned NO files to process !!"
            )
        db.save()
    logger.info(f"Processing {category_name} {n=} files...DONE")


def save_json_event(data):
    fn = "%(schema)s_%(id)s.json" % (data)
    fn = os.path.join(STREAM_PATH, fn)
    open(fn, "w").write(json.dumps(data, indent=2))
    return fn


def handle_menu_user(args, fields):
    if args.createuser:
        schema = User.model_json_schema()
        data = dict(schema=schema["title"])
        if fields:
            newdata = {r: fields[i] for i, r in enumerate(schema["properties"])}
            data["data"] = User(**newdata).model_dump()
            data["id"] = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        else:
            data = ask_data(schema)
        fn = save_json_event(data)
        logger.info(f"Event generated: {fn}...")
    elif args.resetuser:
        reset_offset(category_name="User")
    elif args.listnusers:
        list_n_items(
            category_name="User",
            n=args.listnusers,
            db=FileDatabase(name="UsersSystemState.dat"),
        )
    elif args.processuser:
        process_data(
            category_name="User",
            handler=User,
            db=FileDatabase(name="UsersSystemState.dat"),
        )


def handle_menu_category(args, fields):
    if args.createcategory:
        schema = Category.model_json_schema()
        data = dict(schema=schema["title"])
        if fields:
            newdata = {r: fields[i] for i, r in enumerate(schema["properties"])}
            data["data"] = Category(**newdata).model_dump()
            data["id"] = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        else:
            data = ask_data(schema)
        fn = save_json_event(data)
        logger.info(f"Event generated: {fn}...")
    elif args.resetcategory:
        reset_offset(category_name="Category")
    elif args.listncategories:
        list_n_items(
            category_name="Category",
            n=args.listncategories,
            db=FileDatabase(name="CategorySystemState.dat"),
        )
    elif args.processcategory:
        process_data(
            category_name="Category",
            handler=Category,
            db=FileDatabase(name="CategorySystemState.dat"),
        )


def handle_menu_subscription(args, fields):
    if args.createsubscription:
        schema = Subscription.model_json_schema()
        data = dict(schema=schema["title"])
        if fields:
            newdata = {r: fields[i] for i, r in enumerate(schema["properties"])}
            data["data"] = Subscription(**newdata).model_dump()
            data["id"] = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        else:
            data = ask_data(schema)
        fn = save_json_event(data)
        logger.info(f"Event generated: {fn}...")
    elif args.resetsubscription:
        reset_offset(category_name="Subscription")
    elif args.listnsubscriptions:
        list_n_items(
            category_name="Subscription",
            n=args.listnsubscriptions,
            db=FileDatabase(name="SubscriptionSystemState.dat"),
        )
    elif args.processsubscription:
        process_data(
            category_name="Subscription",
            handler=Subscription,
            db=FileDatabase(name="SubscriptionSystemState.dat"),
        )


def add_menu_category(parser):
    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "--createcategory", action="store_true", help="Create a category"
    )
    group.add_argument(
        "--processcategory", action="store_true", help="Process stream of categories"
    )
    group.add_argument(
        "--resetcategory", action="store_true", help="Reset offset of categories"
    )
    group.add_argument(
        "--listncategories",
        metavar="N",
        required=False,
        type=int,
        help="List N categories",
        default=0,
    )


def add_menu_user(parser):
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--createuser", action="store_true", help="Create a user")
    group.add_argument("--resetuser", action="store_true", help="Reset offset of users")
    group.add_argument(
        "--processuser", action="store_true", help="Process stream of users"
    )
    group.add_argument(
        "--listnusers",
        metavar="N",
        required=False,
        type=int,
        help="List N users",
        default=0,
    )


def add_menu_subscription(parser):
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--createsubscription", action="store_true", help="Create a subscription"
    )
    group.add_argument(
        "--processsubscription",
        action="store_true",
        help="Process stream of subscriptions",
    )
    group.add_argument(
        "--resetsubscription", action="store_true", help="Reset offset of subscriptions"
    )
    group.add_argument(
        "--listnsubscriptions",
        metavar="N",
        required=False,
        type=int,
        help="List N subscriptions",
        default=0,
    )


def add_menu_fields(parser):
    parser.add_argument(
        "--fields",
        metavar="FIELD_VALUE",  # type=int,
        nargs="+",
        required=False,
        help="an fields values",
    )


def main():
    parser = argparse.ArgumentParser(description="Envent Driven Main Processor")

    add_menu_category(parser)
    add_menu_user(parser)
    add_menu_subscription(parser)
    add_menu_fields(parser)

    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    fields = args.fields

    if args.verbose:
        logger.setLevel(logging.DEBUG)
        print("Verbose mode enabled.")

    handle_menu_category(args, fields)
    handle_menu_user(args, fields)
    handle_menu_subscription(args, fields)


if __name__ == "__main__":
    main()
