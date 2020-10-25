import json
import psycopg2
from pprint import PrettyPrinter

pprint = PrettyPrinter(indent=4).pprint
conn = psycopg2.connect(dbname="spy", user="maria", password="password", host="34.123.231.238", port="5433")

cur = conn.cursor()
with open("/home/mashmallow/Desktop/Airlines/FrequentFlyerForum-Profiles.json", "r") as json_file:
    data = json.load(json_file)

userFile = open("/home/mashmallow/Desktop/Airlines/output/users.csv", "w")
flightsFile = open("/home/mashmallow/Desktop/Airlines/output/flights.csv", "w")
flightsFileWithoutUID = open("/home/mashmallow/Desktop/Airlines/output/flights_no_uid.csv", "w")
cardsFile = open("/home/mashmallow/Desktop/Airlines/output/cards.csv", "w")
cardsFileWithoutUID = open("/home/mashmallow/Desktop/Airlines/output/cards_no_uid.csv", "w")

forum_profiles = data.get('Forum Profiles')
qty = len(forum_profiles)
profiles = 0
p = 0
n = 0
global uid
global last_name
global first_name
uid = -1
while profiles < qty:
    print(profiles)
    i = forum_profiles[profiles]
    uid = -1
    user = []
    flights = []
    loyal = []
    if i.get('Real Name').get('Last Name') is None or i.get('Real Name').get('First Name') is None:
        uid = -1
    else:
        print('here')
        last_name = i.get('Real Name').get('Last Name')
        first_name = i.get('Real Name').get('First Name')
        uid = p
        user_file = ';'.join(["{}".format(uid), last_name, first_name])
        print(user_file)
        userFile.write(user_file)
        userFile.write('\n')
        p += 1
    for f in i.get('Registered Flights'):
        arr = f.get('Arrival').get('Airport')
        dep = f.get('Departure').get('Airport')
        if uid != -1:
            flights_file = ';'.join([last_name, first_name, f.get('Date'), f.get('Flight'), "{}".format(profiles), "{}".format(uid), arr, dep, "{}".format(n)])
            flightsFile.write(flights_file)
            flightsFile.write('\n')
        else:
            flights_file = ';'.join([f.get('Date'), f.get('Flight'), "{}".format(profiles),  arr, dep, "{}".format(n)])
            flightsFileWithoutUID.write(flights_file)
            flightsFileWithoutUID.write('\n')
        n += 1
    for c in i.get('Loyality Programm'):
        status = c.get('Status')
        prog = c.get('programm')
        number = c.get('Number')
        if uid != -1:
            str_file = ';'.join([last_name, first_name, status, "{}".format(prog), "{}".format(number), "{}".format(profiles), "{}".format(uid)])
            cardsFile.write(str_file)
            cardsFile.write('\n')
        else:
            str_file = ';'.join([status, "{}".format(prog), "{}".format(number), "{}".format(profiles)])
            cardsFileWithoutUID.write(str_file)
            cardsFileWithoutUID.write('\n')
    profiles += 1

userFile.close()
flightsFile.close()
flightsFileWithoutUID.close()
cardsFile.close()
cardsFileWithoutUID.close()

