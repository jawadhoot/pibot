import csv
from datetime import date,datetime
history_location = "data/coin_order_history.csv"
nav_location = "data/current_nav.csv"

nav_url = "https://www.amfiindia.com/spages/NAVOpen.txt"

interest = 10/365/100

def get_days(trade_date):
    tokens = trade_date.split('-')
    days = (date.today() - date(int(tokens[0]),int(tokens[1]),int(tokens[2]))).days
    return pow(1+interest,days)

current_nav = {}
csv_file = open(nav_location)
reader = csv.reader(csv_file)
for row in reader:
    current_nav[row[0]] = float(row[1])

csv_file = open(history_location)
reader = csv.DictReader(csv_file)
folios = {}
today = date.today()
for row in reader:
    if not row['isin'] in folios:
        folios[row['isin']] = {}
        folios[row['isin']]["scheme_name"] = row['scheme_name']
        folios[row['isin']]['units'] = 0.0
        folios[row['isin']]['amount'] = 0.0
        folios[row['isin']]['gains'] = 0.0
    if row['status'] == "Allotted": 
        folios[row['isin']]['gains'] += get_days(row['trade_date']) * float(row['units']) * float(row['nav'])
        folios[row['isin']]['units'] += float(row['units'])
        folios[row['isin']]['amount'] -= float(row['units']) * float(row['nav'])
    if row['status'] == "Redeemed":
        folios[row['isin']]['gains'] -= get_days(row['trade_date']) * float(row['units']) * float(row['nav'])
        folios[row['isin']]['units'] -= float(row['units'])
        folios[row['isin']]['amount'] += float(row['units']) * float(row['nav'])

sum = 0
invested = 0
for folio in folios:
    invested += folios[folio]['amount']
    print(folios[folio])
    if folios[folio]['units'] > 0.01:
        profit = folios[folio]['units'] * current_nav[folio] - folios[folio]['gains']
    else:
        profit = folios[folio]['amount'] - folios[folio]['gains']
    print(profit)
    sum += profit
        
print(sum)
