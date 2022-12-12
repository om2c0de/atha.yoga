import datetime
from typing import TypedDict, Optional

from lessons.models import LessonComplexities


class LessonFilterData(TypedDict, total=False):
    query: Optional[str]
    complexity: Optional[LessonComplexities]
    start_datetime: Optional[datetime.datetime]
    day: Optional[int]
    end_datetime: Optional[datetime.datetime]


class TicketCreateData(TypedDict):
    name: str
    amount: str
