import sqlite3
import csv

conn = sqlite3.connect('SH_Air.sqlite')
cur = conn.cursor()

cur.execute('''select * from counter where cnt > 4''')
with open('counter.csv','w', newline='') as out_csv_file:
  ad_f_out = csv.writer(out_csv_file)
  # write header                        
  ad_f_out.writerow([d[0] for d in cur.description])
  # write data                          
  for result in cur:
    ad_f_out.writerow(result)
    
conn.close()