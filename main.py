#!/usr/bin/env python

from Handlers import Category
from Handlers import Subscription
from Handlers import Publication
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
from collections import defaultdict

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
def reset_offset(category_name, consumer=None):
    logger.info(f"Processing {category_name}...")
    myconsumer = f"ConsumerOf{category_name}" if consumer is None else consumer
    with EventsReader(event_name=category_name, consumer=myconsumer) as R:
        R.reset_offset()


def list_n_items(category_name, n, db):
    df = pd.DataFrame(db.rows())
    if df.shape[0] == 0:
        logger.warning(f"No information available to list on {category_name}!!")
    else:
        df.sort_values(by=["id"], inplace=True)
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
            stats = os.stat(fn)
            if stats.st_size == 0:
                logger.warning(f"Empty file {fn}...")
            else:
                with open(fn, "r") as file:
                    try:
                        logger.debug(f"Reading Event {fn} ...")
                        data = json.load(file)
                        logger.debug(f"Validating Event {fn} ...")
                        x = handler(**data["data"])
                        logger.debug(f"Handling Event {fn} action: {x.action}...")
                        if x.action == "add":
                            db.set(id=x.id, data=x.model_dump())
                        if x.action == "remove":
                            db.remove(x.id)
                    except:
                        data = {}
                        logger.exception(f"Error reading event {fn}")
            n += 1
        if n == 0:
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


def handle_fields(fields, obj):
    schema = obj.model_json_schema()
    if fields:
        newdata = {r: fields[i] for i, r in enumerate(schema["properties"])}
        data = dict(schema=schema["title"])
        data["data"] = obj(**newdata).model_dump()
        data["id"] = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    else:
        data = ask_data(schema)
    return data


def handle_menu_publication(args, fields):
    if args.addpublication:
        data = handle_fields(fields, obj=Publication)
        fn = save_json_event(data)
        logger.info(f"Event generated: {fn}...")
    elif args.resetpublication:
        reset_offset(category_name="Publication")
    elif args.listnpublication:
        list_n_items(
            category_name="Publication",
            n=args.listnpublication,
            db=FileDatabase(name="PublicationsSystemState.dat"),
        )
    elif args.processpublication:
        process_data(
            category_name="Publication",
            handler=Publication,
            db=FileDatabase(name="PublicationsSystemState.dat"),
        )


def handle_menu_user(args, fields):
    if args.adduser:
        data = handle_fields(fields, obj=User)
        fn = save_json_event(data)
        logger.info(f"Event generated: {fn}...")
    elif args.resetuser:
        reset_offset(category_name="User")
    elif args.listnuser:
        list_n_items(
            category_name="User",
            n=args.listnuser,
            db=FileDatabase(name="UsersSystemState.dat"),
        )
    elif args.processuser:
        process_data(
            category_name="User",
            handler=User,
            db=FileDatabase(name="UsersSystemState.dat"),
        )


def handle_menu_category(args, fields):
    if args.addcategory:
        data = handle_fields(fields, obj=Category)
        fn = save_json_event(data)
        logger.info(f"Event generated: {fn}...")
    elif args.resetcategory:
        reset_offset(category_name="Category")
    elif args.listncategory:
        list_n_items(
            category_name="Category",
            n=args.listncategory,
            db=FileDatabase(name="CategorySystemState.dat"),
        )
    elif args.processcategory:
        process_data(
            category_name="Category",
            handler=Category,
            db=FileDatabase(name="CategorySystemState.dat"),
        )


def handle_menu_subscription(args, fields):
    if args.addsubscription:
        data = handle_fields(fields, obj=Subscription)
        fn = save_json_event(data)
        logger.info(f"Event generated: {fn}...")
    elif args.resetsubscription:
        reset_offset(category_name="Subscription")
    elif args.listnsubscription:
        list_n_items(
            category_name="Subscription",
            n=args.listnsubscription,
            db=FileDatabase(name="SubscriptionSystemState.dat"),
        )
    elif args.processsubscription:
        process_data(
            category_name="Subscription",
            handler=Subscription,
            db=FileDatabase(name="SubscriptionSystemState.dat"),
        )


def add_menu(parser, names):
    for name in names:
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            f"--add{name}", action="store_true", help=f"Add/update a {name}"
        )
        group.add_argument(
            f"--process{name}", action="store_true", help=f"Process stream of {name}"
        )
        group.add_argument(
            f"--reset{name}", action="store_true", help=f"Reset offset of {name}"
        )
        group.add_argument(
            f"--listn{name}",
            metavar="N",
            required=False,
            type=int,
            help=f"List N {name}",
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


@log_entry_exit
def send_notifications(
    category_name="Publication",
    handler=Publication,
    db=FileDatabase(name="PublicationsSystemState.dat"),
):
    logger.info(f"Sending Notifications ...")
    n = 0
    Users = FileDatabase(name="UsersSystemState.dat")
    Subscriptions = FileDatabase(name="SubscriptionSystemState.dat")
    subscribers = defaultdict(list)
    for subscriber in Subscriptions.data.values():
        subscribers[subscriber["categoryid"]].append(subscriber["userid"])

    with EventsReader(
        event_name=category_name,
        consumer="SenderOfNotifications",
    ) as R:
        for fn in R.fetch():
            logger.info(f"Event {fn} In Progress ...")
            stats = os.stat(fn)
            if stats.st_size == 0:
                logger.warning(f"Empty file {fn}...")
            else:
                with open(fn, "r") as file:
                    try:
                        logger.debug(f"Reading Event {fn} ...")
                        data = json.load(file)
                        logger.debug(f"Validating Event {fn} ...")
                        x = handler(**data["data"])
                        logger.debug(f"Handling Event {fn} action: {x.action}...")
                        if x.action == "add":
                            for userid in subscribers[x.categoryid]:
                                logger.info(
                                    f"<<<==== NOTIFICATION SEND ABOUT '{x.title}' ({x.comments}) TO '{Users.data[userid]['fullname']}' ====>>>"
                                )
                    except:
                        data = {}
                        logger.exception(f"Error reading event {fn}")
            n += 1
        if n == 0:
            logger.warning(
                f"Processing {category_name} returned NO files to process !!"
            )
    logger.info(f"Processing {category_name} {n=} files...DONE")


def handle_menu_sendnotifications(args, fields):
    if args.sendnotifications:
        send_notifications(
            category_name="Publication",
            handler=Publication,
            db=FileDatabase(name="PublicationsSystemState.dat"),
        )
    if args.resetsendnotifications:
        reset_offset(category_name="Publication", consumer="SenderOfNotifications")


def add_menu_sendnotifications(parser):
    parser.add_argument(
        "--sendnotifications", action="store_true", help=f"Send Notifications"
    )
    parser.add_argument(
        "--resetsendnotifications",
        action="store_true",
        help=f"Reset Send Notifications",
    )


def main():
    parser = argparse.ArgumentParser(description="Envent Driven Main Processor")

    add_menu(parser, names=["user", "category", "subscription", "publication"])
    add_menu_sendnotifications(parser)
    add_menu_fields(parser)
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    fields = args.fields

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    handle_menu_category(args, fields)
    handle_menu_user(args, fields)
    handle_menu_subscription(args, fields)
    handle_menu_publication(args, fields)
    handle_menu_sendnotifications(args, fields)


if __name__ == "__main__":
    main()
