cur.execute('''DROP TABLE IF EXISTS SH_User CASCADE''')
cur.execute('''CREATE TABLE SH_User (
    uid int constraint pk_user_sh PRIMARY KEY,
    passengerfirstname varchar(20) not null,
    passengerlasttname varchar(20) not null)''')

cur.execute('''DROP TABLE IF EXISTS SH_Card CASCADE''')
cur.execute('''CREATE TABLE SH_Card (
    cardProgram char(3) not null,
    cardNumber int not null,
    
    programName varchar(20) null,
    uid int null REFERENCES SH_User,
    
    constraint pk_card_sh PRIMARY KEY (cardProgram, cardNumber))''')

cur.execute('''DROP TABLE IF EXISTS SH_Flight CASCADE''')
cur.execute('''CREATE TABLE SH_Flight (
    flightID int constraint pk_flight_sh PRIMARY KEY,
    flightCode varchar(10) not null,
    flightDate date not null,
    
    from_AP char(4) not null,
    to_AP char(4) not null)''')

cur.execute('''DROP TABLE IF EXISTS SH_CardFlight CASCADE''')
cur.execute('''CREATE TABLE SH_CardFlight (
    flightID int constraint pk_flight_sh REFERENCES SH_Flight,
    cardProgram char(3) not null,
    cardNumber int not null,
    fare char(7) not null,
    
    class char(2) null,
    
    PRIMARY KEY (flightID, cardProgram, cardNumber),
    constraint pk_card_sh FOREIGN KEY (cardProgram, cardNumber) REFERENCES SH_Card)''')

