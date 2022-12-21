import datetime
from typing import TypedDict, List, Optional

from lessons.models import (
    RepetitionWeekdays,
    CourseTypes,
    CourseLevels,
    CoursePaymentTypes,
    CourseComplexities,
)


class CourseReviewCreateData(TypedDict):
    star_rating: int
    text: str


class LessonCreateData(TypedDict):
    weekday: RepetitionWeekdays
    start_time: datetime.time


class CourseCreateData(TypedDict):
    name: str
    description: str
    course_type: CourseTypes
    link: str
    link_info: str
    level: CourseLevels
    duration: str
    repeat_editing: bool
    start_datetime: datetime.datetime
    deadline_datetime: Optional[datetime.datetime]
    payment: CoursePaymentTypes
    price: int
    complexity: CourseComplexities
    lesson: Optional[List[LessonCreateData]]


class CourseUpdateData(TypedDict):
    description: str
    course_type: CourseTypes
    level: CourseLevels
    complexity: CourseComplexities
