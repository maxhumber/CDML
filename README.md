

![ODSC](https://odsc.com/wp-content/uploads/2015/12/HIGHRESODSCLOGO.png)

### Continuously Deployed ML 

On-Demand Course for ODSC AI+

Full source code: `step_by_step.ipynb`

---

Post Request function:

```
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
```