from flask import Flask, render_template, request
import json
from flask import jsonify
import pandas as pd
import matplotlib.pyplot as plt


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
    df["date"]= pd.to_datetime(df["date"]) 


    maxim = df['amount'].max()
    mini = df['amount'].min()
    mean = df['amount'].mean()

    gb = df.groupby("type")

    gf = df.groupby(["type"]).sum().sort_values("amount", ascending=False)

    df['YearMonth'] = pd.to_datetime(df['date']).apply(lambda x: '{month}-{year}'.format(year=x.year, month=x.day))

    # monthly = df.groupby('YearMonth')['amount'].sum()

    monthly =df.groupby(["YearMonth"]).sum().sort_values("amount", ascending=False)

    print(monthly)
    print(gf)

    types = []
    typeSpend = {}
    # for name, group in df.groupby("type"):
    #     types.append(name)
   
    type_js = gf.to_dict('dict')
    month_js = monthly.to_dict('dict')



    res = {
        'maximum': f'{maxim}',
        'minimum': f'{mini}',
        'mean': f'{mean}',
        'typeBased': type_js,
        'monthBased': month_js,
    }
    return res


if __name__ == "__main__":
    app.run(debug=True)

    # res = str(res, 'utf-8')

    # print(res[0])
    # f = open( 'api_flask/sheets/parsed.json', 'w')
    # f.write(res)
    # print(df)
    # js = json.loads(res)
    # # df = pd.read_json(js)
    # print(type(js))
    # df = pd.DataFrame.from_records(js)
    # df = df.drop([0])
    # print(df)
    # maxim = df['amount'].astype(int).max()
    # mini = df['amount'].astype(int).min()
    # mean = df['amount'].astype(int).mean()
    # res = json.dumps({
    #     "maximum": f"{maxim}",
    #     "minimum": f"{mini}",
    #     "mean": f"{mean}",
    # }, indent=4)
    # print(sd[1]['amount'])
    # print(type(request.data))
    # print(request['data'])
