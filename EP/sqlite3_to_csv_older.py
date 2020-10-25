import sqlite3
import csv

#XML

conn = sqlite3.connect('PointzAggregator-AirlinesData.sqlite')
cur = conn.cursor()
cur.execute('''SELECT * FROM AirlinesData_User''')
with open('AirlinesData_User.csv','w') as out_csv_file:
  ad_u_out = csv.writer(out_csv_file)
  # write header                        
  ad_u_out.writerow([d[0] for d in cur.description])
  # write data                          
  for result in cur:
    ad_u_out.writerow(result)

cur.execute('''SELECT * FROM AirlinesData_Card''')
with open('AirlinesData_Card.csv','w') as out_csv_file:
  ad_c_out = csv.writer(out_csv_file)
  # write header                        
  ad_c_out.writerow([d[0] for d in cur.description])
  # write data                          
  for result in cur:
    ad_c_out.writerow(result)

cur.execute('''SELECT * FROM AirlinesData_Flight''')
with open('AirlinesData_Flight.csv','w') as out_csv_file:
  ad_f_out = csv.writer(out_csv_file)
  # write header                        
  ad_f_out.writerow([d[0] for d in cur.description])
  # write data                          
  for result in cur:
    ad_f_out.writerow(result)
    
#conn.close()

#YAML

#conn = sqlite3.connect('SkyTeam-Exchange,sqlite')
#cur = conn.cursor()
cur.execute('''SELECT * FROM Exchange_Flight''')
with open('Exchange_Flight.csv','w') as out_csv_file:
  ste_f_out = csv.writer(out_csv_file)
  # write header                        
  ste_f_out.writerow([d[0] for d in cur.description])
  # write data                          
  for result in cur:
    ste_f_out.writerow(result)

cur.execute('''SELECT * FROM Exchange_FlightCard''')
with open('Exchange_FlightCard.csv','w') as out_csv_file:
  ste_fc_out = csv.writer(out_csv_file)
  # write header                        
  ste_fc_out.writerow([d[0] for d in cur.description])
  # write data                          
  for result in cur:
    ste_fc_out.writerow(result)
    
conn.close()