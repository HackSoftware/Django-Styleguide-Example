from typing import Optional, Iterable
from datetime import date

from django.db import transaction
from django.utils.text import slugify

from styleguide_example.testing_examples.models import (
    SchoolCourse,
    School,
    Student,
    Roster
)


@transaction.atomic
def school_course_create(
    *,
    name: str,
    slug: Optional[str] = None,
    school: School,
    students: Iterable[Student],
    start_date: date,
    end_date: date
) -> SchoolCourse:
    slug = slug or slugify(name)

    school_course = SchoolCourse(
        name=name,
        slug=slug,
        start_date=start_date,
        end_date=end_date,
        school=school
    )
    school_course.full_clean()
    school_course.save()

    rosters = []
    for student in students:
        roster = Roster(
            student=student,
            school_course=school_course,
            start_date=start_date,
            end_date=end_date
        )
        roster.full_clean()
        rosters.append(roster)

    Roster.objects.bulk_create(rosters, batch_size=50)

    return school_course
