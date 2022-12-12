import datetime
from typing import TypedDict, List, Optional

from lessons.models import (
    RepetitionWeekdays,
    LessonTypes,
    LessonLevels,
    LessonPaymentTypes,
    LessonComplexities,
)


class CommentCreateData(TypedDict):
    text: str
    lesson_id: int


class ScheduleCreateData(TypedDict):
    weekday: RepetitionWeekdays
    start_time: datetime.time


class LessonCreateData(TypedDict):
    name: str
    description: str
    lesson_type: LessonTypes
    link: str
    link_info: str
    level: LessonLevels
    duration: str
    repeat_editing: bool
    start_datetime: datetime.datetime
    deadline_date: Optional[datetime.date]
    payment: LessonPaymentTypes
    price: int
    complexity: LessonComplexities
    schedule: Optional[List[ScheduleCreateData]]


class TicketCreateData(TypedDict):
    name: str
    amount: str


