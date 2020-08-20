import json
from urllib.request import Request, urlopen
import pandas as pd

data = json.dumps({
    "date": str(pd.Timestamp('now')),
    "temperature": -30
})

request = Request(
    url='http://localhost:5000',
    data=bytes(data.encode("utf-8")),
    method="POST"
)

request.add_header("Content-type", "application/json; charset=UTF-8")

with urlopen(request) as response:
    data = json.loads(response.read().decode("utf-8"))
    print(data)
