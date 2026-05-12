# The file 'customers-100.csv' contains customer data, with one customer per line.
# Each line consists of several fields, including the customer's country.
#
# Counts how many customers come from each country and
# prints the results in alphabetical order of countries.
#
# For each country, it outputs a line of the form:
#     <number> from <country>

import csv
from collections import defaultdict

# INSERT YOUR CODE HERE
result = defaultdict(int)
with open('customers-100.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        result[row[6]] += 1
        
sorted_list = sorted(result.keys())

for i in sorted_list:
    print(result[i], ' from ' , i)