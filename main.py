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

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s"
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


@log_entry_exit
def reset_offset(category_name):
    logger.info(f"Processing {category_name}...")
    with EventsReader(
        event_name=category_name, consumer=f"ConsumerOf{category_name}"
    ) as R:
        R.reset_offset()


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
                    db.set(id=x.id, data=x.dict())
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
    open(fn, "w").write(json.dumps(data))
    return fn


def main():
    parser = argparse.ArgumentParser(description="Envent Driven Main Processor")

    parser.add_argument(
        "--createcategory", action="store_true", help="Create a category"
    )
    parser.add_argument(
        "--processcategory", action="store_true", help="Process stream of categories"
    )
    parser.add_argument(
        "--resetcategory", action="store_true", help="Reset offset of categories"
    )

    parser.add_argument("--createuser", action="store_true", help="Create user")
    parser.add_argument(
        "--processuser", action="store_true", help="process stream of users"
    )
    parser.add_argument(
        "--resetuser", action="store_true", help="reset offset of users"
    )

    parser.add_argument(
        "--createsubscription", action="store_true", help="Create subscription"
    )
    parser.add_argument(
        "--processsubscription",
        action="store_true",
        help="process stream of subscriptions",
    )
    parser.add_argument(
        "--resetsubscription", action="store_true", help="Reset subscription offset"
    )
    parser.add_argument(
        "--fields",
        metavar="FIELD_VALUE",  # type=int,
        nargs="+",
        required=False,
        help="an fields values",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    fields = args.fields

    if args.verbose:
        logger.setLevel(logging.DEBUG)
        print("Verbose mode enabled.")

    if args.createcategory:
        id_fields = [
            Fields(i, f, f.title()) for i, f in enumerate(Category.model_fields)
        ]
        if fields:
            data = Category({r.name: fields[r.id] for r in id_fields})
        else:
            data = ask_data(id_fields)
        fn = save_json_event(data)
        logger.info(f"Event generated: {fn}...")
    elif args.resetcategory:
        reset_offset(category_name="Category")
    elif args.processcategory:
        process_data(
            category_name="Category",
            handler=Category,
            db=FileDatabase(name="CategorySystemState.dat"),
        )

        # if args.createuser:
        #    data = ask_data(tuple(User.model_fields.keys())
        #    fn = save_json_event(data)
        #    logger.info(f"Event generated: {fn}...")
        # elif args.resetuser:
        #    reset_offset(category_name="User")
        # elif args.processuser:
        #    process_data(
        #        category_name="User",
        #        handler=User,
        #        db=FileDatabase(name="UserSystemState.dat"),
        #    )

        # if args.createsubscription:
        #    data = ask_data(tuple(Subscription.model_fields.keys())
        #    fn = save_json_event(data)
        #    logger.info(f"Event generated: {fn}...")
        # elif args.resetsubscription:
        #    reset_offset(category_name="subscription")
        # elif args.processsubscription:
        #    process_data(
        #        category_name="subscription",
        #        handler=subscription,
        #        db=FileDatabase(name="subscriptionSystemState.dat"),
        #    )


if __name__ == "__main__":
    main()
