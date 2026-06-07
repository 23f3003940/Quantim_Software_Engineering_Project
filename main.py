import csv
from datetime import datetime
from dash import Dash, html, dcc, Input
import plotly.express as px
import pandas as pd

lst = []
def readcsv(filename):
    with open(filename, newline='\n') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if row[0] == 'pink morsel':
                sales = float(row[1][1:]) * int(row[2])
                l = ['$' + str(sales), row[3], row[4]]
                lst.append(l)

readcsv('data/daily_sales_data_0.csv')
readcsv('data/daily_sales_data_1.csv')
readcsv('data/daily_sales_data_2.csv')

def get_date(item_row):
    return datetime.strptime(item_row[1], "%Y-%m-%d")

sorted_data = sorted(lst, key=get_date)


with open('data/output.csv', 'w', newline='\n') as csvfile:
     writer = csv.writer(csvfile, delimiter=',')
     writer.writerow(['Sales', 'Date', 'Region'])
     for row in sorted_data:
         writer.writerow(row)


def filter_region(index):
    regions_based_list = []
    for sorted_row in sorted_data:
        if index == sorted_row[2]:
            regions_based_list.append(sorted_row)

    return regions_based_list


app = Dash()

def loadChart(region):
    regions_based_list = filter_region(region)

    sales = []
    dates = []
    for region_row in regions_based_list:
        sales.append(region_row[0])
        dates.append(region_row[1])


    df = pd.DataFrame({
        "Date": dates,
        "Sales": sales
    })

    fig = px.line(df, x="Date", y="Sales")

    app.layout = html.Div(children=[
        html.H1(children='Sales Dashboard'),

        html.Div(children='''
            Forecasting sales of the Pink Morsel after and before price increase on the 15th of January, 2021
        '''),

        html.Div(
            [
                html.Label("Select Region:"),
                dcc.RadioItems(
                    id="region-radio",
                    options=[
                        {"label": "West", "value": "west"},
                        {"label": "East", "value": "east"},
                        {"label": "North", "value": "north"},
                        {"label": "South", "value": "south"}
                    ],
                    value="west",  # default selection
                    inline=True
                )
            ],
            className="radio-container"
        ),

        dcc.Graph(
            id='example-graph',
            figure=fig
        )
    ])

@app.callback(
    Input("region-radio", "value")
)
def radio_clicked(selected_region):
    loadChart(selected_region)

radio_clicked("north")

if __name__ == '__main__':
    app.run(debug=True)
