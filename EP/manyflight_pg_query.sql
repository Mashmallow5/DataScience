DROP TABLE IF EXISTS ACF
CREATE TABLE ACF(
primk integer primary key,
cardP int not null,
cardN int not null,
flightCode varchar(10) not null,
flightDate date not null,
from_AP char(4) not null,
to_AP char(4) not null)

cur.execute('''INSERT INTO ACF(cardP, cardN, flightCode, flightDate, from_AP, to_AP)
    select distinct SH_CardFlight.cardProgram, SH_CardFlight.cardNumber, flightCode, flightDate, from_AP, to_AP from
		SH_CardFlight join SH_Flight on SH_Flight.flightID = SH_CardFlight.flightID''')
print("acf done")

cur.execute('''DROP TABLE IF EXISTS AUF''')
cur.execute('''CREATE TABLE AUF(
primk integer primary key,
ufirst varchar(20) not null,
ulast varchar(20) not null,
flightCode varchar(10) not null,
flightDate date not null,
from_AP char(4) not null,
to_AP char(4) not null)''')
print("auf created")

cur.execute('''INSERT INTO AUF(ufirst, ulast, flightCode, flightDate, from_AP, to_AP)
    select distinct passengerfirstname, passengerlasttname, flightCode, flightDate, from_AP, to_AP from
		ACF join SH_Card on (cardP = cardProgram and cardN = cardNumber)
        join SH_User on (SH_Card.uid = SH_User.uid)''')
print("auf done")

cur.execute('''DROP TABLE IF EXISTS counter''')
cur.execute('''CREATE TABLE counter(
primk integer primary key,
ufirst varchar(20) not null,
ulast varchar(20) not null,
flightDate date not null,
cnt int not null)''')
print("counter created")

cur.execute('''insert into counter(ufirst, ulast, flightDate, cnt) select ufirst, ulast, flightDate, count(flightCode) from AUF group by ufirst, ulast, flightDate''')
print("counter done")

conn.commit()
    
conn.close()