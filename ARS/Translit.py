import pandas as pd
import cyrtranslit #this lib was edited

path = open('D:\\Sirena-export-fixed2.csv', 'w')

with open('D:\\Sirena-export-fixed.csv', 'rt', encoding = 'utf-8') as f:
    for line in f:
        line = cyrtranslit.to_latin(line, 'ru')
        path.write(line)
path.close()
