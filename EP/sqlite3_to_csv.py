import sqlite3
import csv

conn = sqlite3.connect('SH_Air.sqlite')
cur = conn.cursor()
cur.execute('''SELECT * FROM SH_User''')
with open('SH_User.csv','w', newline='') as out_csv_file:
  ad_u_out = csv.writer(out_csv_file)
  # write header                        
  ad_u_out.writerow([d[0] for d in cur.description])
  # write data                          
  for result in cur:
    ad_u_out.writerow(result)

cur.execute('''SELECT * FROM SH_Card''')
with open('SH_Card.csv','w', newline='') as out_csv_file:
  ad_c_out = csv.writer(out_csv_file)
  # write header                        
  ad_c_out.writerow([d[0] for d in cur.description])
  # write data                          
  for result in cur:
    ad_c_out.writerow(result)

cur.execute('''SELECT * FROM SH_Flight''')
with open('SH_Flight.csv','w', newline='') as out_csv_file:
  ad_f_out = csv.writer(out_csv_file)
  # write header                        
  ad_f_out.writerow([d[0] for d in cur.description])
  # write data                          
  for result in cur:
    ad_f_out.writerow(result)

cur.execute('''SELECT * FROM SH_CardFlight''')
with open('SH_CardFlight.csv','w', newline='') as out_csv_file:
  ad_f_out = csv.writer(out_csv_file)
  # write header                        
  ad_f_out.writerow([d[0] for d in cur.description])
  # write data                          
  for result in cur:
    ad_f_out.writerow(result)
    
conn.close()