import sqlite3

conn = sqlite3.connect('SH_Air.sqlite')
cur = conn.cursor()

cur.execute('''DROP TABLE IF EXISTS ACF''')
cur.execute('''CREATE TABLE ACF(
primk integer primary key,
cardP int not null,
cardN int not null,
flightCode varchar(10) not null,
flightDate date not null,
from_AP char(4) not null,
to_AP char(4) not null)''')
print("acf created")

cur.execute('''INSERT INTO ACF(cardP, cardN, flightCode, flightDate, from_AP, to_AP)
    select SH_CardFlight.cardProgram, SH_CardFlight.cardNumber, flightCode, flightDate, from_AP, to_AP from
		SH_CardFlight join SH_Flight on SH_Flight.flightID = SH_CardFlight.flightID''')
print("acf done")

cur.execute('''DROP TABLE IF EXISTS nextflight''')
cur.execute('''CREATE TABLE nextflight(
primk integer primary key,
cardP int not null,
cardN int not null,
code1 varchar(10) not null,
date1 date not null,
from1 char(4) not null,
to1 char(4) not null,
code2 varchar(10) not null,
date2 date not null,
from2 char(4) not null,
to2 char(4) not null)''')
print("nextflight created")
cur.execute('''INSERT INTO nextflight(cardP, cardN, code1, date1, from1, to1, code2, date2, from2, to2)
    select a.cardP, a.cardN, a.flightCode, a.flightDate, a.from_AP, a.to_AP,  b.flightCode, b.flightDate, b.from_AP, b.to_AP
		from ACF a join ACF b on a.cardP = b.cardP
			where CAST(strftime('%s', a.flightDate) AS integer) <= CAST(strftime('%s', b.flightDate) AS integer)
			and not exists (select null from ACF c where
				c.cardP = a.cardP and
				c.cardN = a.cardN and
				CAST(strftime('%s', a.flightDate) AS integer) <= CAST(strftime('%s', c.flightDate) AS integer) and
				CAST(strftime('%s', b.flightDate) AS integer) > CAST(strftime('%s', c.flightDate) AS integer))''')

print("nextflight done")
cur.execute('''select * from nextflight where to1 != from2''')
#cur.execute('''select * from nextflight''')
conn.commit() 
    
conn.close()