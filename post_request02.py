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
    "date": str(pd.Timestamp('now')),
    "temperature": -30
}

post("http://127.0.0.1:5000", data)
