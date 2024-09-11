Project description:
The project is about a Notification System to users subscribed to some events categories.

The idea behind bas to create an Event Driven Architecture.

The directory ./Stream contains all the events stored to be processed by consumer programs.
The events can be created with the following command:
$  ./main.py --addcategory 
 or
$  ./main.py --addcategory --fields add categoryid categoryname

Also there is the file demo.sh with a demo for creating users, categories, subscriptions and publication of events to be notified to the users subscribed.


# HOW TO START
To execute the project:
1) Install anaconda
2) bash ./conda_start.sh
3) pip install -r requirements.txt
4) Execute demo with the following command: bash ./demo.sh

# Project files:

|    file        |           function                      |
|----------------|-----------------------------------------|
|Handlers.py     | Validations and handling of Events      |
|test_Handlers.py| Testing of Handlers                     |
|Storage.py      | Interfaces for saving objects to storage|
|test_Storage.py | Testing of Storage                      |
|main.py         | Program to execute on command line      |

# Events used on the System of Notifications:

| Name of Event | Description                                                                                |
|---------------|--------------------------------------------------------------------------------------------|
| User          | Event to handle add/modification or removing of Users                                      |
| Category      | Event to handle add/modification or removing of Categories                                 |
| Subscription  | Event to handle add/modification or removing of Subscriptions                              |
| Publication   | Event to handle add/modification or removing of Publications to notify to Users Subscribed |



# Main.py Usage:

You can find about the parameters executing:
$> ./main.py -?

The options are folowwing the structure of the command:

## Commandline for handling Users

| structure of command       |      comment                                                            |
|----------------------------|-------------------------------------------------------------------------|
| ./main.py --adduser        | create an event fot add a user                                          |
| ./main.py --resetuser      | reset the offset for processing user events                             |
| ./main.py --processuser    | process all the user events stored on the stream of events              |
| ./main.py --listnuser  N   | print on screen N users available after processing the stream of events |

## Commandline for handling Categories

| structure of command           |      comment                                                                 |
|--------------------------------|------------------------------------------------------------------------------|
| ./main.py --addcategory        | create an event fot add a category                                           |
| ./main.py --resetcategory      | reset the offset for processing category events                              |
| ./main.py --processcategory    | process all the category events stored on the stream of events               |
| ./main.py --listncategory  N   | print on screen N categories available after processing the stream of events |


## Commandline for handling Subscriptions

| structure of command               |      comment                                                                    |
|------------------------------------|---------------------------------------------------------------------------------|
| ./main.py --addsubscription        | create an event fot add a subscription                                          |
| ./main.py --resetsubscription      | reset the offset for processing subscription events                             |
| ./main.py --processsubscription    | process all the subscription events stored on the stream of events              |
| ./main.py --listnsubscription  N   | print on screen N subscriptions available after processing the stream of events |


## Commandline for handling publications

| structure of command               |      comment                                                                    |
|------------------------------------|---------------------------------------------------------------------------------|
| ./main.py --addpublication         | create an event fot add a publication                                           |
| ./main.py --resetpublication       | reset the offset for processing publicationevents                               |
| ./main.py --processpublication     | process all the publicationevents stored on the stream of events                |
| ./main.py --listnpublication N     | print on screen N publication available after processing the stream of events   |



## Command for handling publications

| structure of command               |      comment                                                                    |
|------------------------------------|---------------------------------------------------------------------------------|
| ./main.py --addpublication         | create an event fot add a publication                                           |
| ./main.py --resetpublication       | reset the offset for processing publicationevents                               |
| ./main.py --processpublication     | process all the publicationevents stored on the stream of events                |
| ./main.py --listnpublication N     | print on screen N publication available after processing the stream of events   |


## Command for handling publication events stored on the Stream of Events and send notifications

| structure of command               |      comment                                                                    |
|------------------------------------|---------------------------------------------------------------------------------|
| ./main.py --sendnotification       | Send notifications about the Publications to the Users subscribed               |

