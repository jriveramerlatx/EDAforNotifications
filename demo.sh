#!/usr/bin/env bash
find ./Stream/ -iname "*.json" -delete
find ./ -iname "*.dat" -delete

./main.py --adduser --fields add bruce bbrucelee "Bruce Lee"
./main.py --adduser --fields add roy roy "Roy Rogerson"
./main.py --adduser --fields add peter peterframpton "Peter Frampton"
./main.py --adduser --fields add johny johnyjohnson "Johny Johnson"
./main.py --processuser
./main.py --listnuser 5

./main.py --addcategory --fields add sports "Sport Event"
./main.py --addcategory --fields add finance "Finance Event"
./main.py --addcategory --fields add films "Films Event"
./main.py --processcategory
./main.py --listncategory 5

./main.py --addsubscription --fields brucesport1 add sports bruce
./main.py --addsubscription --fields royfilm1 add films roy
./main.py --addsubscription --fields johny add finance johny
./main.py --addsubscription --fields peterfilms add films peter
./main.py --processsubscription
./main.py --listnsubscription 5

./main.py --addpublication --fields films1 add films "Scary Movie" "Scary Movie 2024"
./main.py --addpublication --fields films1 add films "Horror Movie" "World Best Horror Movie of the Year 2024"
./main.py --addpublication --fields finance1 add finance "Finance Conference" "The Mexican Finance Conference 2024"
./main.py --addpublication --fields sports1 add sports "Martial Arts Tournament" "Worlds First Martial Arts Tournament Championship 2024"
./main.py --processpublication
./main.py --listnpublication 5
./main.py --sendnotifications
