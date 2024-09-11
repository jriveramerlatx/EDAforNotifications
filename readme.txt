Project description:
The project is about a Notification System to users subscribed to some events categories.

The idea behind bas to create an Event Driven Architecture.

The directory ./Stream contains all the events.
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

|            file|                                 function|
|----------------|-----------------------------------------|
|     Handlers.py|       Validations and handling of Events|
|test_Handlers.py|                      Testing of Handlers|
|      Storage.py| Interfaces for saving objects to storage|
| test_Storage.py|                       Testing of Storage|
