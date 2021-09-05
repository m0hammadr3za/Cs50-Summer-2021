import sys
import csv

if len(sys.argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")
    sys.exit(1)

strs = {}
database = []
dna = ""

with open(sys.argv[1]) as data_file:
    dict_reader = csv.DictReader(data_file)
    for row in dict_reader:
        database.append(row)

keys = []
for i in database[0]:
    keys.append(i)

keys = keys[1:len(keys)]
for k in keys:
    strs[k] = 0;

with open(sys.argv[2]) as sequence_file:
    dna = sequence_file.read()

for s in strs:
    for i in range(len(dna)):
        if dna[i:i + len(s)] == s:
            counter = 1
            while dna[i + len(s) * counter: (i + len(s) * counter) + len(s)] == s:
                counter += 1
            if counter > strs[s]:
                strs[s] = counter

for p in database:
    matched = True
    for s in strs:
        if strs[s] != int(p[s]):
            matched = False
    if matched:
        print(p["name"])
        sys.exit(0)

print("No match")