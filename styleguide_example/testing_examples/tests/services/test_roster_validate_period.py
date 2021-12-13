from datetime import timedelta

from django.test import TestCase
from django.core.exceptions import ValidationError

from styleguide_example.testing_examples.tests.factories import SchoolCourseFactory
from styleguide_example.testing_examples.services import (
    roster_validate_period,
    ROSTER_VALIDATE_PERIOD_OUTSIDE_COURSE_PERIOD
)


class RosterValidatePeriodTests(TestCase):
    def test_service_does_not_raise_error_if_valid_period(self):
        course = SchoolCourseFactory.build()

        roster_period_equal_to_course_period = {
            'start_date': course.start_date,
            'end_date': course.end_date
        }
        roster_period_inside_course_period = {
            'start_date': course.start_date + timedelta(days=1),
            'end_date': course.end_date - timedelta(days=1)
        }
        roster_period_end_inside_course_period = {
            'start_date': course.start_date,
            'end_date': course.end_date - timedelta(days=1)
        }
        roster_period_start_inside_course_period = {
            'start_date': course.start_date + timedelta(days=1),
            'end_date': course.end_date
        }

        roster_validate_period(school_course=course, **roster_period_equal_to_course_period)
        roster_validate_period(school_course=course, **roster_period_inside_course_period)
        roster_validate_period(school_course=course, **roster_period_end_inside_course_period)
        roster_validate_period(school_course=course, **roster_period_start_inside_course_period)

    def test_services_raises_error_for_rosters_outside_period(self):
        course = SchoolCourseFactory.build()

        roster_period_end_before_course_start = {
            'start_date': course.start_date - timedelta(days=10),
            'end_date': course.start_date - timedelta(days=5)
        }
        roster_period_start_before_course_start = {
            'start_date': course.start_date - timedelta(days=10),
            'end_date': course.start_date + timedelta(days=1)
        }
        roster_period_start_after_course_end = {
            'start_date': course.end_date + timedelta(days=5),
            'end_date': course.end_date + timedelta(days=10)
        }
        roster_period_end_after_course_end = {
            'start_date': course.end_date - timedelta(days=1),
            'end_date': course.end_date + timedelta(days=10)
        }

        for roster_period in [
            roster_period_end_before_course_start,
            roster_period_start_before_course_start,
            roster_period_start_after_course_end,
            roster_period_end_after_course_end
        ]:
            with self.assertRaisesMessage(
                ValidationError,
                ROSTER_VALIDATE_PERIOD_OUTSIDE_COURSE_PERIOD.format(school_course=course)
            ):
                roster_validate_period(school_course=course, **roster_period)
