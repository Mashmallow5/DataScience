
razm_kol = [60, 12, 12, 12, 12, 12, 6, 6, 6, 6, 6, 18, 12, 6, 6, 6, 6, 12, 24, 36, 60]

file_csv = open('D:\\Sirena-export-fixed-yes-yes.csv', 'w')

sch = 0

with open('D:\\Sirena-export-fixed.tab', 'rt', encoding = 'utf-8') as file_tab:
    for line in file_tab:
        row = ""
        for dlin in razm_kol:
            isfirst = 0
            soderzh = line[0:dlin]
            line = line[dlin:]
            soderzh = soderzh.strip()

            if soderzh == "N/A":
                soderzh = "NULL"

            if not soderzh:
                if sch == 0:
                    soderzh = "Bez_nazv"
                else: soderzh = "NULL"

            if isfirst == 0:
                soderzh = line[0:dlin]
                line = line[dlin:]
                buf = soderzh.strip().split(' ')
                soderzh = soderzh + ' ' + "FirstName" + ' ' + "ThirdName"
                isfirst = 1

            if not row:
                row = soderzh

            else:
                row = row + ',' + soderzh

        if not sch:
            file_csv.write(row + '\n')
            sch = 1

        else:
            file_csv.write(row + '\n')


file_csv.close()
