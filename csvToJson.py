import csv
import json
import requests

# Open the CSV
f = open('template/exp.csv', 'r')
reader = csv.DictReader(f, fieldnames=("date", "type", "amount", 'income', 'limit','category', 'target'))
out = json.dumps([row for row in reader])


r = requests.post('http://127.0.0.1:5000/', data=out)
print(r.text)




#Save the JSON
f = open( 'parsed.json', 'w')
f.write(r.text)


# open JSON
with open('parsed.json', 'r') as f:
    datastore = json.load(f)

dict = datastore['monthBased']['amount']