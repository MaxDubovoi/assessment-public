from flask import Flask, jsonify, request, make_response
import requests as r
import pandas as pd
import datetime
import json

app = Flask(__name__)
path_to_csv = "../client/client/data/sample.csv"
fmt_for_datetime = '%Y-%m-%dT%H:%M:%S.%fZ'


@app.route('/')
def hello_world():
    return 'Hello world!'


@app.route('/test', methods=['GET', 'POST'])
def test():
    resp = {"response": 'Success!'}
    return jsonify(resp)


@app.route('/api/v1/candle', methods=['POST'])
def send_candles():
    req = request
    f = request.files.get('sample.csv')
    candles = get_candles(f)
    json_candles = []
    json_candles_str = ''
    for candle in candles:
        json_candles_str += candle.serialize()
    #        json_candles.append(jsonify(candle.serialize()))
    # test_json = json.dumps(json_candles)
    response = make_response(json_candles_str)

    return response


def get_candles(f):
    _candles = []
    all_data = read_csv_file(f)
    minutes = get_minute_data(all_data)
    candles = []
    for _minute in minutes:
        candles.append(get_candle(_minute))
    return candles


def read_csv_file(f):
    _data = pd.read_csv(f)
    # pd.read_csv(f)
    return _data


def get_candle(_minute):
    candle = Candle(get_max_price_candle(_minute),
                    get_min_price_candle(_minute),
                    get_open_price_candle(_minute),
                    get_close_price_candle(_minute))

    return candle


def get_minute_data(_all_data: pd.DataFrame):
    prev = _all_data.iloc[0]
    minute_data = pd.DataFrame()
    minute_data = minute_data.append(prev, ignore_index=True)
    minutes = list()
    for index, row in _all_data.iterrows():
        minute_data = minute_data.append(row, ignore_index=True)
        if get_time_interval(prev['timestamp'], row['timestamp']).seconds >= 60:
            minutes.append(minute_data)
            prev = row
    return minutes


def get_max_price_candle(_candle_data: pd.DataFrame):
    row = _candle_data.loc[_candle_data['price'].idxmax()]
    return row['price']


def get_min_price_candle(_candle_data: pd.DataFrame):
    row = _candle_data.loc[_candle_data['price'].idxmin()]
    return row['price']


def get_close_price_candle(_candle_data: pd.DataFrame):
    timestamp_strs = _candle_data['timestamp']
    times = []
    for timestamp_str in timestamp_strs:
        times.append(convert_str_time(timestamp_str).timestamp())
    return _candle_data.get_value(get_max_index(times), 'price')


def get_open_price_candle(_candle_data: pd.DataFrame):
    timestamp_strs = _candle_data['timestamp']
    times = []
    for timestamp_str in timestamp_strs:
        times.append(convert_str_time(timestamp_str).timestamp())
    return _candle_data.get_value(get_min_index(times), 'price')


def get_time_interval(old_time: str, new_time):
    return datetime.datetime.strptime(new_time, fmt_for_datetime) - datetime.datetime.strptime(old_time,
                                                                                               fmt_for_datetime)


def get_max_index(i_list: list):
    _max = i_list.__getitem__(0)
    _index = 0
    index_max = 0
    for i in i_list:
        if i >= _max:
            _max = i
            index_max = _index
        _index = _index + 1
    return index_max


def get_min_index(i_list: list):
    _min = i_list.__getitem__(0)
    _index = 0
    index_min = 0
    for i in i_list:
        if i <= _min:
            _min = i
            index_min = _index
        _index = _index + 1
    return index_min


def convert_str_time(time_string: str):
    return datetime.datetime.strptime(time_string, fmt_for_datetime)


class Candle:
    max_price: float
    min_price: float
    open_price: float
    close_price: float

    def __init__(self, _max, _min, _open, _close):
        self.max_price = _max
        self.min_price = _min
        self.open_price = _open
        self.close_price = _close

    def serialize(self):
        return json.dumps({
            'max': self.max_price,
            'min': self.min_price,
            'open': self.open_price,
            'close': self.close_price,
        })


if __name__ == '__main__':
    app.run(host='0.0.0.0')
