from flask import Flask, render_template, request
import json
from flask import jsonify
import pandas as pd
import numpy as np


app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    res = request.data

    res = str(res, 'utf-8')
    js = json.loads(res)
    df = pd.DataFrame.from_records(js)
    df = df.drop([0])
    df['amount'] = df['amount'].astype(int)
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

    max_row = df.loc[df['amount'].idxmax()]
    max_row = max_row[['type', 'date', 'amount']]
    max_row = max_row.rename('maxSpend')
    max_row = max_row.to_frame()

    min_row = df.loc[df['amount'].idxmin()]
    min_row = min_row[['type', 'date', 'amount']]
    min_row = min_row.rename('minSpend')
    min_row = min_row.to_frame()

    print(min_row)

    df['YearMonth'] = pd.to_datetime(df['date']).apply(
        lambda x: '{month}-{year}'.format(year=x.year, month=x.month))
    df['month'] = pd.to_datetime(df['date']).apply(
        lambda x: '{month}'.format(month=x.month))
    df['year'] = pd.to_datetime(df['date']).apply(
        lambda x: '{year}'.format(year=x.year))

    monthlyYear = df.groupby(["YearMonth"]).sum(
    ).sort_values("amount", ascending=False)

    monthly = df.groupby(["month"]).sum(
    ).sort_values("amount", ascending=False)

    year = df.at[1, 'year']

    max_row = max_row.astype('str')
    min_row = min_row.astype('str')

    print(df)
    type_js = gf.to_dict('dict')
    month_js = monthly.to_dict('dict')
    percentage = perc.to_dict('dict')
    yearMonth = monthlyYear.to_dict('dict')
    maxSpend = max_row.to_dict('dict')
    minSpend = min_row.to_dict('dict')

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
        'maxSpend': maxSpend,
        'minSpend': minSpend,
    }
    return res


if __name__ == "__main__":
    app.run(debug=True)
