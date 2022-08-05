import requests
from cloudevents.http import CloudEvent, from_http, to_binary

headers, data = to_binary(
    CloudEvent(
        attributes={"type": "com.your-corp.response.v1", "source": "your:source"},
        data={"hello": "world"},
    )
)
response = requests.post("http://localhost:8000", headers=headers, data=data)
print(from_http(response.headers, response.content))
