from flask import Flask, render_template, request
import json
from flask import jsonify
import pandas as pd
import numpy as np


app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    # print (request.data)
    res = request.data

    res = str(res, 'utf-8')
    js = json.loads(res)
    # df = pd.read_json(js)
    df = pd.DataFrame.from_records(js)
    df = df.drop([0])
    df['amount'] = df['amount'].astype(int)
    # df['income'] = df['income'].astype(int)
    df["date"] = pd.to_datetime(df["date"])

    maxim = df.amount.max()
    mini = df['amount'].min()
    sumi = df['amount'].sum()
    median = df['amount'].median()
    mean = df['amount'].mean()

    gf = df.groupby(["type"]).sum().sort_values("amount", ascending=False)

    perc = gf
    perc['percentage'] = (100*perc['amount'])/(int(df.at[1, 'income']))

    date_amount = df.groupby(["date"]).sum(
    ).sort_values("amount", ascending=False)

    max_amount = date_amount[date_amount.amount == date_amount.amount.max()]

    df['YearMonth'] = pd.to_datetime(df['date']).apply(lambda x: '{month}-{year}'.format(year=x.year, month=x.month))
    df['month'] = pd.to_datetime(df['date']).apply(lambda x: '{month}'.format( month=x.month))
    df['year'] = pd.to_datetime(df['date']).apply(lambda x: '{year}'.format( year=x.year))


    # monthly = df.groupby('YearMonth')['amount'].sum()

    monthlyYear = df.groupby(["YearMonth"]).sum(
    ).sort_values("amount", ascending=False)

    monthly = df.groupby(["month"]).sum(
    ).sort_values("amount", ascending=False)

    year = df.at[1, 'year']



 
    print(df)
    type_js = gf.to_dict('dict')
    month_js = monthly.to_dict('dict')
    percentage = perc.to_dict('dict')
    yearMonth = monthlyYear.to_dict('dict')
    # max_spend_js = max_amount.to_dict('dict')

    res = {
        'year': f'{year}',
        'maximum': f'{maxim}',
        'minimum': f'{mini}',
        'sum': f'{sumi}',
        'median': f'{median}',
        'mean': f'{mean}',
        'typeBased': type_js,
        'monthBased': month_js,
        'monthlyYear': yearMonth,
    }
    return res


if __name__ == "__main__":
    app.run(debug=True)
