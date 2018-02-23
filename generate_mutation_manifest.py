import csv
import string
import sys

reader = csv.reader(sys.stdin, dialect='excel-tab')
next(reader)  # Skip header
templates = [row[0] for row in reader]
combined_template = ' '.join(templates)

for letter in string.ascii_lowercase:
    print(letter, end=' ')
    print(combined_template.replace('.', letter))
