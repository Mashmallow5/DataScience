drop table if exists sh_joined_cardflight

create table sh_joined_cardflight
(
    primk   serial primary key,
    cardprogram char(3) not null,
    cardnumber  integer not null,
    flightcode varchar(10) not null,
    flightdate date        not null,
    from_ap    char(4)     not null,
    to_ap      char(4)     not null
);

insert into sh_joined_cardflight(cardprogram, cardnumber, flightcode, flightdate, from_ap, to_ap)
    select distinct sh_cardflight.cardprogram, sh_cardflight.cardnumber, flightcode, flightdate, from_ap, to_ap from
		sh_cardflight join sh_flight on sh_flight.flightid = sh_cardflight.flightid

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
    flightdate1 date        not null,
    from_ap1    char(4)     not null,
    to_ap1      char(4)     not null,
    flightcode2 varchar(10) not null,
    flightdate2 date        not null,
    from_ap2    char(4)     not null,
    to_ap2      char(4)     not null
);

insert into sh_nextflight(cardprogram, cardnumber, flightcode1, flightdate1, from_ap1, to_ap1, flightcode2, flightdate2, from_ap2, to_ap2)
    select a.cardprogram, a.cardnumber, a.flightcode, a.flightdate, a.from_ap, a.to_ap,  b.flightcode, b.flightdate, b.from_ap, b.to_ap
		from sh_joined_cardflight a join sh_joined_cardflight b on a.cardprogram = b.cardprogram
			where a.flightdate <= b.flightdate
			and not exists (select null from sh_joined_cardflight c where
				c.cardprogram = a.cardprogram and
				c.cardnumber = a.cardnumber and
				a.flightdate <= c.flightdate and
				b.flightdate > c.flightdate)

select * from sh_nextflight where to_ap1 != from_ap2