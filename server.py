from flask import Flask, render_template, request
import json
from flask import jsonify
import pandas as pd

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
    print(df)
    maxim = df['amount'].astype(int).max()
    mini = df['amount'].astype(int).min()
    mean = df['amount'].astype(int).mean()
    res = json.dumps({
        "maximum": f"{maxim}",
        "minimum": f"{mini}",
        "mean": f"{mean}",
    }, indent=4)
    print(type(res))
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
