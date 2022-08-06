from typing import Literal, Union

import uvicorn
from fastapi import FastAPI
from pydantic import Field
from typing_extensions import Annotated

from fastapi_cloudevents import (CloudEvent, CloudEventSettings, ResponseMode,
                                 install_fastapi_cloudevents)

app = FastAPI()
app = install_fastapi_cloudevents(
    app, settings=CloudEventSettings(response_mode=ResponseMode.structured)
)


class MyEvent(CloudEvent):
    type: Literal["my.type.v1"]


class YourEvent(CloudEvent):
    type: Literal["your.type.v1"]


OurEvent = Annotated[Union[MyEvent, YourEvent], Field(discriminator="type")]

_source = "dummy:source"


@app.post("/")
async def on_event(event: OurEvent) -> CloudEvent:
    if isinstance(event, MyEvent):
        return CloudEvent(
            type="my.response-type.v1",
            data=f"got {event.data} from my event!",
            datacontenttype="text/plain",
        )
    else:
        return CloudEvent(
            type="your.response-type.v1",
            data=f"got {event.data} from your event!",
            datacontenttype="text/plain",
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
