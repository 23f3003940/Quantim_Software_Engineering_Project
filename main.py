import csv
from datetime import datetime
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

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

def get_date(row):
    return datetime.strptime(row[1], "%Y-%m-%d")
sorted_data = sorted(lst, key=get_date)


with open('data/output.csv', 'w', newline='\n') as csvfile:
     writer = csv.writer(csvfile, delimiter=',')
     writer.writerow(['Sales', 'Date', 'Region'])
     for row in sorted_data:
         writer.writerow(row)

app = Dash()

sales = []
regions = []
dates = []
for row in sorted_data:
    sales.append(row[0])
    dates.append(row[1])
    regions.append(row[2])

df = pd.DataFrame({
    "Date": dates,
    "Sales": sales,
    "Regions": regions
})

fig = px.line(df, x="Date", y="Sales")

app.layout = html.Div(children=[
    html.H1(children='Sales Dashboard'),

    html.Div(children='''
        Forecasting sales of the Pink Morsel after and before price increase on the 15th of January, 2021
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run(debug=True)