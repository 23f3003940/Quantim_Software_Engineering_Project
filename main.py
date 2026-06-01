import csv

lst = []
def readcsv(filename):
    with open(filename, newline='\n') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if row[0] == 'pink morsel':
                sales = float(row[1][1:]) * int(row[2])
                l = []
                l.append('$' + str(sales))
                l.append(row[3])
                l.append(row[4])
                lst.append(l)

readcsv('data/daily_sales_data_0.csv')
readcsv('data/daily_sales_data_1.csv')
readcsv('data/daily_sales_data_2.csv')

with open('data/output.csv', 'w', newline='\n') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Sales', 'Date', 'Region'])
    for row in lst:
        writer.writerow(row)