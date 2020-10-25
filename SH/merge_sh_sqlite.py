import sqlite3


conn = sqlite3.connect('SH_Air.sqlite')

conn = sqlite3.connect('SH_Air.sqlite')
cur = conn.cursor()

cur.execute('''DROP TABLE IF EXISTS SH_User''')
cur.execute('''CREATE TABLE SH_User (
    uid int PRIMARY KEY,
    passengerfirstname varchar(20) not null,
    passengerlasttname varchar(20) not null)''')

cur.execute('''DROP TABLE IF EXISTS SH_Card''')
cur.execute('''CREATE TABLE SH_Card (
    cardProgram char(3) not null,
    cardNumber int not null,
    
    programName varchar(20) null,
    uid int null REFERENCES SH_User,
    
    PRIMARY KEY (cardProgram, cardNumber))''')

cur.execute('''DROP TABLE IF EXISTS SH_Flight''')
cur.execute('''CREATE TABLE SH_Flight (
    flightID int PRIMARY KEY,
    flightCode varchar(10) not null,
    flightDate date not null,
    
    from_AP char(4) not null,
    to_AP char(4) not null)''')

cur.execute('''DROP TABLE IF EXISTS SH_CardFlight''')
cur.execute('''CREATE TABLE SH_CardFlight (
    flightID int REFERENCES SH_Flight,
    cardProgram char(3) not null,
    cardNumber int not null,
    fare char(7) not null,
    
    class char(2) null,
    
    PRIMARY KEY (flightID, cardProgram, cardNumber),
    FOREIGN KEY (cardProgram, cardNumber) REFERENCES SH_Card)''')

#users
cur.execute('''INSERT INTO SH_User SELECT * FROM AirlinesData_User''')

#cards - all 1
cur.execute('''INSERT INTO SH_Card SELECT * FROM AirlinesData_Card''')
#cards - not in 1
cur.execute('''INSERT INTO SH_Card (cardProgram, cardNumber)
    SELECT cardProgram, cardNumber FROM Exchange_FlightCard WHERE NOT EXISTS (
        SELECT cardProgram, cardNumber FROM  SH_Card
            WHERE (cardProgram = SH_Card.cardProgram and cardNumber=SH_Card.cardNumber))
        GROUP BY cardProgram, cardNumber''')

#flights - 1
#no flightID collisions due to smart ID selection)))0)
cur.execute('''INSERT INTO SH_Flight (flightID, flightCode, flightDate, from_AP, to_AP)
    SELECT flightID, flightCode, flightDate, departure, arrival FROM AirlinesData_Flight
        GROUP BY flightCode, flightDate, departure, arrival''')
        #grouping to prevent flightID repeats
#flights - only 2
cur.execute('''INSERT INTO SH_Flight (flightID, flightCode, flightDate, from_AP, to_AP)
    SELECT flightID, flightCode, flightDate, from_AP, to_AP FROM Exchange_Flight
        WHERE NOT EXISTS (
        SELECT null from SH_Flight join Exchange_Flight on (
        SH_Flight.flightCode = Exchange_Flight.flightCode and
        SH_Flight.flightDate = Exchange_Flight.flightDate and
        SH_Flight.from_AP = Exchange_Flight.from_AP and
        SH_Flight.to_AP = Exchange_Flight.to_AP))
    GROUP BY flightCode, flightDate, from_AP, to_AP''')
            
            
print('Fare problems:')
#cardflights - check fare
cur.execute('''SELECT AirlinesData_Flight.flightCode, AirlinesData_Flight.flightDate, AirlinesData_Flight.departure, AirlinesData_Flight.arrival, AirlinesData_Flight.cardProgram, AirlinesData_Flight.cardNumber, AirlinesData_Flight.fare FROM
        (Exchange_Flight join Exchange_FlightCard on Exchange_Flight.flightID = Exchange_FlightCard.flightID)
            join AirlinesData_Flight on (
                AirlinesData_Flight.flightCode = Exchange_Flight.flightCode and
                AirlinesData_Flight.flightDate = Exchange_Flight.flightDate and
                AirlinesData_Flight.departure = Exchange_Flight.from_AP and
                AirlinesData_Flight.arrival = Exchange_Flight.to_AP and
                AirlinesData_Flight.cardProgram = Exchange_FlightCard.cardProgram and
                AirlinesData_Flight.cardNumber = Exchange_FlightCard.cardNumber)
        WHERE AirlinesData_Flight.fare != Exchange_FlightCard.fare''')
print (cur.fetchone())
            
#cardflights - 2
cur.execute('''INSERT INTO SH_CardFlight (flightID, cardProgram, cardNumber, fare, class)
    SELECT SH_Flight.flightID, cardProgram, cardNumber, fare, class FROM
        (Exchange_Flight join Exchange_FlightCard on Exchange_Flight.flightID = Exchange_FlightCard.flightID)
            join SH_Flight on (
                SH_Flight.flightCode = Exchange_Flight.flightCode and
                SH_Flight.flightDate = Exchange_Flight.flightDate and
                SH_Flight.from_AP = Exchange_Flight.from_AP and
                SH_Flight.to_AP = Exchange_Flight.to_AP)''')
            
#cardflights - only 1
cur.execute('''INSERT INTO SH_CardFlight (flightID, cardProgram, cardNumber, fare)
    SELECT SH_Flight.flightID, cardProgram, cardNumber, fare FROM
        AirlinesData_Flight join SH_Flight on (
            SH_Flight.flightCode = AirlinesData_Flight.flightCode and
            SH_Flight.flightDate = AirlinesData_Flight.flightDate and
            SH_Flight.from_AP = AirlinesData_Flight.departure and
            SH_Flight.to_AP = AirlinesData_Flight.arrival)''')

conn.commit()
conn.close()