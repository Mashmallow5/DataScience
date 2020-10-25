import xml.etree.ElementTree as etree
import sqlite3

def fixlit(name_str):
    return name_str.replace("'", '').replace("SHCH", "SH").replace("YU", "IU").replace("YA", "IA").replace("AY", "AI").replace("IY", "II").replace("EY", "EI").replace('X', 'KS')

uids = set()
cardNums = set()
flightCodes = set()

userSet = set()
cardSet = set()
flightSet = set()

conn = sqlite3.connect('SH_Air.sqlite')
cur = conn.cursor()

cur.execute('''DROP TABLE IF EXISTS AirlinesData_User''')
cur.execute('''CREATE TABLE AirlinesData_User (
    uid int PRIMARY KEY,
    passengerfirstname text not null,
    passengerlasttname text not null)''')

cur.execute('''DROP TABLE IF EXISTS AirlinesData_Card''')
cur.execute('''CREATE TABLE AirlinesData_Card (
    cardProgram text not null,
    cardNumber int not null,
    programName text not null,
    uid int not null REFERENCES AirlinesData_User,
    PRIMARY KEY (cardProgram, cardNumber))''')

cur.execute('''DROP TABLE IF EXISTS AirlinesData_Flight''')
cur.execute('''CREATE TABLE AirlinesData_Flight (
    flightID int PRIMARY KEY,
    flightCode text not null,
    flightDate date not null,
    departure text not null,
    arrival text not null,
    fare text not null,
    cardProgram text not null,
    cardNumber int not null,
    FOREIGN KEY (cardProgram, cardNumber) REFERENCES AirlinesData_Card)''')

flightID = 2000000

xml_tree = etree.parse('PointzAggregator-AirlinesData.xml')
xml_root = xml_tree.getroot()
for user in xml_root:
    uid = user.get('uid')
    name = user.find('name')
    passengerfirstname = fixlit(name.get('first'))
    passengerlasttname = fixlit(name.get('last'))
    #print('Parsing user:\tUID %d;\tName %s %s' % (int(uid), passengerfirstname, passengerlasttname))

    if uid in uids:
        print('Duplicate user:\tUID %d' % int(uid))
    else:
        uids.add(uid)
        userSet.add((uid, passengerfirstname, passengerlasttname))

    cards = user.find('cards')
    for card in cards:
        cardNumberFull = card.get('number')
        cardProgram = cardNumberFull.strip().split(' ')[0]
        cardNumber = cardNumberFull.strip().split(' ')[1]
        programName = card.find('bonusprogramm').text
        #print('Parsing card:\tprog %s\tnumber %s\tbProg %s' % (cardProgram, cardNumber, programName))

        if (cardProgram, cardNumber) in cardNums:
            print('Duplicate card:\tprogram %s\tnumber %s' % (cardProgram, cardNumber))
        else:
            cardNums.add((cardProgram, cardNumber))
            cardSet.add((cardProgram, cardNumber, programName, uid))

        activities = card.find('activities')
        for activity in activities:
            code = activity.find('Code').text
            date = activity.find('Date').text
            departure = activity.find('Departure').text
            arrival = activity.find('Arrival').text
            fare = activity.find('Fare').text
            #print('Parsing flight:\tcode %s\tdate %s\tdep %s\tarr %s\tfare %s' % (code, date, departure, arrival, fare))

            if (code, date) in flightCodes:
                print('Duplicate flight:\tcode %s' % code)
            else:
                flightCodes.add((code, date))
                flightID += 1
                flightSet.add((flightID, code, date, departure, arrival, fare, cardProgram, cardNumber))
        flightCodes.clear() #well, several people on the same flight, why not?

print('Total users: %d' % len(userSet))
print('Total cards: %d' % len(cardSet))
print('Total flights: %d' % len(flightSet))

cur.executemany('''INSERT INTO AirlinesData_User VALUES(?,?,?)''', userSet)
cur.executemany('''INSERT INTO AirlinesData_Card VALUES(?,?,?,?)''', cardSet)
cur.executemany('''INSERT INTO AirlinesData_Flight VALUES(?,?,?,?,?,?,?,?)''', flightSet)

conn.commit()
conn.close()
