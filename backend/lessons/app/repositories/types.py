import datetime
from typing import TypedDict, Optional

from lessons.models import CourseComplexities


class CourseFilterData(TypedDict, total=False):
    query: Optional[str]
    complexity: Optional[CourseComplexities]
    start_datetime: Optional[datetime.datetime]
    day: Optional[int]
    end_datetime: Optional[datetime.datetime]
