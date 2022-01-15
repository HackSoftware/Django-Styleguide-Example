from datetime import date
from typing import Optional

from django.db.models.query import Q, QuerySet
from django.core.exceptions import ValidationError

from styleguide_example.testing_examples.models import School, SchoolCourse


SCHOOL_LIST_SCHOOL_COURSES_PROVIDE_START_DATE_MSG =\
    'Provide `start_date` in order to list all School Courses for a period.'


def school_list_school_courses(
    *,
    school: School,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> QuerySet[SchoolCourse]:
    if start_date is None and end_date:
        raise ValidationError(SCHOOL_LIST_SCHOOL_COURSES_PROVIDE_START_DATE_MSG)

    school_courses = school.school_courses.order_by('start_date')

    if start_date and end_date:
        started_courses_Q = Q(start_date__lte=start_date, end_date__gte=start_date, end_date__lte=end_date)
        courses_in_period_q = Q(start_date__gte=start_date, end_date__lte=end_date)
        courses_wrapping_period_q = Q(start_date__lte=start_date, end_date__gte=end_date)
        future_course_q = Q(start_date__gte=start_date, start_date__lte=end_date, end_date__gte=end_date)

        return school_courses.filter(
            started_courses_Q
            | courses_in_period_q
            | courses_wrapping_period_q
            | future_course_q
        )

    if start_date and end_date is None:
        return school_courses.filter(
            Q(start_date__gte=start_date)
            | Q(start_date__lte=start_date, end_date__gte=start_date)
        )

    return school_courses
