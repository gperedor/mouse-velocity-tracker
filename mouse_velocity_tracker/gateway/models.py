import datetime

import pydantic


class FrontendMouseEvent(pydantic.BaseModel):
    client_id: str
    x: int
    y: int
    client_timestamp: datetime.datetime
