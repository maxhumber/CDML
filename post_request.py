import json
from urllib.request import Request, urlopen
import pandas as pd


def post(url, data):
    data = bytes(json.dumps(data).encode("utf-8"))
    request = Request(
        url=url,
        data=data,
        method="POST"
    )
    request.add_header("Content-type", "application/json; charset=UTF-8")
    with urlopen(request) as response:
        data = json.loads(response.read().decode("utf-8"))
    return data

data = {
    "date": str(pd.Timestamp('2021-08-24 15:25:28.514397')),
    "temperature": 28
}

post("http://127.0.0.1:5000", data)

post("http://178.128.238.123", data)
