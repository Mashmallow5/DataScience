drop table if exists sh_joined_cardflight

create table sh_joined_cardflight
(
    primk   serial primary key,
    cardprogram char(3) not null,
    cardnumber  integer not null,
    flightcode varchar(10)  not null,
    departtime timestamp         not null,
    arrivaltime timestamp        not null,
    from_ap    char(4)     not null,
    to_ap      char(4)     not null
)

insert into sh_joined_cardflight(cardprogram, cardnumber, flightcode, departtime, arrivaltime, from_ap, to_ap)
    select distinct sh_cardflight.cardprogram, sh_cardflight.cardnumber, sh_flight.flightcode, departdate + departtime, arrivaldate + arrivaltime, from_ap, to_ap from
		sh_cardflight join sh_flight on sh_flight.flightid = sh_cardflight.flightid
            join ars_flight on
                sh_flight.flightcode = ars_flight.flightcode and
                sh_flight.from_ap = ars_flight.fromap and
                sh_flight.flightdate = ars_flight.departdate and
                sh_flight.from_ap = ars_flight.fromap and
                sh_flight.from_ap = ars_flight.fromap

select * from sh_joined_cardflight limit 500

alter table sh_joined_cardflight
    owner to maria;

drop table if exists sh_nextflight

create table sh_nextflight
(
    primk   serial primary key,
    cardprogram char(3) not null,
    cardnumber  integer not null,
    flightcode1 varchar(10) not null,
    departtime1 timestamp         not null,
    arrivaltime1 timestamp        not null,
    from_ap1    char(4)     not null,
    to_ap1      char(4)     not null,
    flightcode2 varchar(10) not null,
    departtime2 timestamp         not null,
    arrivaltime2 timestamp        not null,
    from_ap2    char(4)     not null,
    to_ap2      char(4)     not null
)

insert into sh_nextflight(cardprogram, cardnumber, flightcode1, departtime1, arrivaltime1, from_ap1, to_ap1,
                                                   flightcode2, departtime2, arrivaltime2, from_ap2, to_ap2)
    select a.cardprogram, a.cardnumber, a.flightcode, a.departtime, a.arrivaltime, a.from_ap, a.to_ap,
                                        b.flightcode, b.departtime, b.arrivaltime, b.from_ap, b.to_ap
		from sh_joined_cardflight a join sh_joined_cardflight b on a.cardprogram = b.cardprogram and a.cardnumber = b.cardnumber
			where a.arrivaltime < b.departtime
			and not exists (select null from sh_joined_cardflight c where
				c.cardprogram = a.cardprogram and
				c.cardnumber = a.cardnumber and
				a.arrivaltime < c.departtime and
                b.departtime > c.departtime)

select * from ars_flight where departtime+departdate > arrivaltime+arrivaldate

select * from sh_nextflight