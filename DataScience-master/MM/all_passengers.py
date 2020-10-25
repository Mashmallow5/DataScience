import psycopg2


def check_sex(person_sex):
    if person_sex == 'Female':
        return 'MRS'
    return 'MR'


def check_booking_code(code):
    if len(code) > 6 or code == 'Not presented':
        return ''
    return code


def check_ticket_number(ticket):
    if len(ticket) != 16 or ticket == 'Not presented':
        return ''
    return ticket


conn = psycopg2.connect(dbname="spy", user="maria", password="password", host="34.123.231.238", port="5433")
cur = conn.cursor()

with open('/home/mashmallow/Desktop/Airlines/BoardingData.csv', 'r') as f:
    i = 0
    while i != 89256:
        s = f.readline()
        i += 1
    s = f.readline()
    while s:
        data = s.split(";")
        cur.execute("""INSERT INTO mm_passenger VALUES(DEFAULT, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"""
                    .format(data[0],
                            data[1],
                            data[2],
                            check_sex(data[3]),
                            data[4],
                            data[5],
                            check_booking_code(data[6]),
                            check_ticket_number(data[7]),
                            data[8],
                            data[9],
                            data[10],
                            data[11],
                            data[12],
                            data[13][:-1]))
        conn.commit()
        s = f.readline()
