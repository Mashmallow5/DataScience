import sqlite3
import yaml

dates = set()
codes = set()
cardNums = set()

flightSet = set()
cardSet = set()

conn = sqlite3.connect('SH_Air.sqlite')
cur = conn.cursor()

cur.execute('''DROP TABLE IF EXISTS Exchange_Flight''')
cur.execute('''CREATE TABLE Exchange_Flight (
    flightID int PRIMARY KEY,
    flightDate date not null,
    flightCode text not null,
    from_AP text not null,
    to_AP text not null,
    status text not null)''')

cur.execute('''DROP TABLE IF EXISTS Exchange_FlightCard''')
cur.execute('''CREATE TABLE Exchange_FlightCard (
    cardID int PRIMARY KEY,
    cardProgram text not null,
    cardNumber int not null,
    class text not null,
    fare text not null,
    flightID not null REFERENCES Exchange_Flight)''')
    
flightID = 0
cardID = 0

#splitting the file
src_file = open("SkyTeam-Exchange.yaml", 'r')
part_size = 65536
file_i = 0
str_num = 0
f = open("stex_part_%d.yaml" % file_i, 'w')
print('Created STEx part %d' % file_i)
for line in src_file:
    if (str_num >= part_size and line[0] == '\''):
        f.close()
        file_i += 1
        str_num = 0
        f = open("stex_part_%d.yaml" % file_i, 'w')
        print('Created STEx part %d' % file_i)
    f.write(line[:-1] + '\n')
    str_num += 1
f.close()

file_count = file_i

#parsing
for file_i in range(file_count):
    stream = open("stex_part_%d.yaml" % file_i, 'r')
    print('Parsing STEx part %d' % file_i)
    yaml_data = yaml.load(stream, Loader = yaml.SafeLoader)
    print('Loaded')
    for flightDate in yaml_data:
        print('Parsing date:\tdate %s' % flightDate)
        if flightDate in dates:
            print('Duplicate date:\t %s' % flightDate)
        else:
            dates.add(flightDate)
            
            for flightCode in yaml_data[flightDate]:
                if flightCode in codes:
                    print('Duplicate flight:\t %s' % flightCode)
                else:
                    codes.add(flightCode)
                    
                    from_AP = yaml_data[flightDate][flightCode]['FROM']
                    to_AP = yaml_data[flightDate][flightCode]['TO']
                    status = yaml_data[flightDate][flightCode]['STATUS']
                    #print('Parsing flight:\tdate %s\tcode %s\tfrom %s\tto %s\tstatus %s' % (flightDate, flightCode, from_AP, to_AP, status))
                    flightSet.add((flightID, flightDate, flightCode, from_AP, to_AP, status))
                    flightID += 1
                    
                    for cardNumberFull in yaml_data[flightDate][flightCode]['FF']:
                        cardProgram = cardNumberFull.strip().split(' ')[0]
                        cardNumber = cardNumberFull.strip().split(' ')[1]
                        if (cardProgram, cardNumber) in cardNums:
                            print('Duplicate card:\tprogram %s\tnumber %s' % (cardProgram, cardNumber))
                        else:
                            cardNums.add((cardProgram, cardNumber))
                            passClass = yaml_data[flightDate][flightCode]['FF'][cardNumberFull]['CLASS']
                            fare = yaml_data[flightDate][flightCode]['FF'][cardNumberFull]['FARE']
                            #print('Parsing card:\tcardProg %s\tcardNum %s\tclass %s\tfare %s' % (cardProgram, cardNumber, passClass, fare))
                            cardSet.add((cardID, cardProgram, cardNumber, passClass, fare, flightID))
                            cardID += 1
                    cardNums.clear()
                codes.clear()
            dates.clear()
        conn.commit()

print('Total cards: %d' % len(cardSet))
print('Total flights: %d' % len(flightSet))

cur.executemany('''INSERT INTO Exchange_Flight VALUES(?,?,?,?,?,?)''', flightSet)

cur.executemany('''INSERT INTO Exchange_FlightCard VALUES (?,?,?,?,?,?)''', cardSet)

conn.commit()
conn.close()

