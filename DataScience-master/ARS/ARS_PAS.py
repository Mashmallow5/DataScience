import sqlite3

conn = sqlite3.connect('ARS_PASSENGEERS.sqtite')
cur = conn.cursor()

cur.execute("ATTACH DATABASE 'D:/sqlite/ARS_FROM_TAB_PEREL.db' AS other;")
 #cursor.execute("\
      #  INSERT INTO table \
      #  (ID) \
       # SELECT * \
       # FROM other.table ;")

cur.execute('''DROP TABLE IF EXISTS ARS_PAS_INF''')

cur.execute('''CREATE TABLE ARS_PAS_INF (
                PassengeerID int PRIMARY KEY,
                PassengeerFirstName varchar(20),
                PassengerSecondName varchar(20),
                PassengerLastName varchar(20),
                PassengerBirthDate varchar(10) null,
                PassengerDocument varchar(11))''')

cur.execute('''INSERT INTO ARS_PAS_INF (PassengeerID, PassengeerFirstName, PassengerSecondName, PassengerLastName,
                                        PassengerBirthDate, PassengerDocument)
                SELECT sid, paxFirstName, paxLastName, paxSecondName, PaxBirthDate, TravelDoc FROM Sirena_export_fixed2''')

cur.execute('''DROP TABLE IF EXISTS ARS_FLIGHT_INF''')

cur.execute('''CREATE TABLE ARS_FLIGHT_INF (
                FlightID int PRIMARY KEY,
                DepartDate date,
                DepartTime time,
                ArrivalDate date,
                ArrivalTime time,
                FlightCode varchar(6),
                FromAP varchar(3),
                DestAP varchar(3))''')

cur.execute('''INSERT INTO ARS_FLIGHT_INF (FlightID, DepartDate, DepartTime, ArrivalDate,
                                        ArrivalTime, FlightCode, FromAP, DestAP)
                SELECT rowid, DepartDate, DepartTime, ArrivalDate, ArrivalTime, FlightCode, FromAF, DestAF FROM Sirena_export_fixed2''')

cur.execute('''DROP TABLE IF EXISTS ARS_TICKET_INF''')

cur.execute('''CREATE TABLE ARS_TICKET_INF (
                PassengeerID int REFERENCES ARS_PAS_INF,
                FlightID int int REFERENCES ARS_FLIGHT_INF,
                Code varchar(6),
                e_Ticket text,
                Travel_class varchar(1),
                Fare varchar(6),
                Baggage varchar(3),
                PRIMARY KEY (PassengeerID, FlightID))''')

cur.execute('''INSERT INTO ARS_TICKET_INF (PassengeerID, FlightID, Code, e_Ticket, Travel_class, Fare,
                                        Baggage)
                SELECT sid, rowid, Code, eTicket, TrvCls, Fare, Baggage FROM Sirena_export_fixed2''')

cur.execute('''DROP TABLE IF EXISTS ARS_BOARDING_PASS_INF''')

cur.execute('''CREATE TABLE ARS_BOARDING_PASS_INF (
                PassengeerID int PRIMARY KEY,
                PassengeerFirstName varchar(20),
                PassengerSecondName varchar(20),
                PassengerSex varchar(3),
                DepartDate date,
                DepartTime time,
                FlightCode varchar(6),
                FromAP varchar(3),
                DestAP varchar(3),
                Code varchar(6),
                e_Ticket text,
                Travel_class varchar(1))''')

cur.execute('''INSERT INTO ARS_BOARDING_PASS_INF (PassengeerID, PassengeerFirstName, PassengerSecondName, PassengerSex, DepartDate,
                                        DepartTime, FlightCode, FromAP, DestAP, Code, e_Ticket, Travel_class)
                SELECT rowid, FirstName, SecondName, Sex, DepartDate, DepartTime,FlightCode,
                       FromAP,  DestAP,  Code, e_Ticket, Travel_class FROM Out_vih2''')


conn.commit()
conn.close()
