from datetime import timedelta

import factory

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone

from styleguide_example.utils.tests import faker
from styleguide_example.testing_examples.selectors import (
    school_list_school_courses,
    SCHOOL_LIST_SCHOOL_COURSES_PROVIDE_START_DATE_MSG
)
from styleguide_example.testing_examples.tests.factories import (
    SchoolFactory,
    SchoolCourseFactory
)


class SchoolListSchoolCoursesTests(TestCase):
    def _order_school_courses(self, school_courses):
        # Helper method - the result from the selector is ordered
        return sorted(school_courses, key=lambda x: x.start_date)

    def test_selector_raises_validation_error_if_unexpected_period_is_given(self):
        with self.assertRaisesMessage(
            ValidationError,
            SCHOOL_LIST_SCHOOL_COURSES_PROVIDE_START_DATE_MSG
        ):
            school_list_school_courses(
                school=SchoolFactory.build(),
                start_date=None,
                end_date=faker.future_date()
            )

    def test_selector_returns_all_school_courses_if_no_dates_passed(self):
        school = SchoolFactory()
        school_courses = SchoolCourseFactory.create_batch(3, school=school)

        result = school_list_school_courses(school=school)

        self.assertEqual(
            self._order_school_courses(school_courses),
            list(result)
        )

    def test_selector_does_not_return_school_courses_for_other_schools(self):
        expected_school_course = SchoolCourseFactory()
        other_school_course = SchoolCourseFactory()

        result = school_list_school_courses(school=expected_school_course.school)

        self.assertNotIn(other_school_course, result)
        self.assertEqual([expected_school_course], list(result))

    def test_selector_returns_all_school_courses_for_a_given_start_date(self):
        school = SchoolFactory()
        now = timezone.now()

        future_school_course = SchoolCourseFactory(
            school=school,
            start_date=faker.future_date()
        )
        started_school_course = SchoolCourseFactory(
            school=school,
            start_date=faker.past_date(),
            end_date=faker.future_date()
        )

        finished_school_course = SchoolCourseFactory(
            school=school,
            start_date=faker.past_date(),
            # Uses timedelta in order to make sure the generated date is not equal to the period
            end_date=factory.LazyAttribute(lambda _self: faker.date_between_dates(
                date_start=_self.start_date + timedelta(days=1),
                date_end=now - timedelta(days=1)
            ))
        )

        result = school_list_school_courses(school=school, start_date=now)

        self.assertNotIn(finished_school_course, result)
        self.assertEqual(
            [started_school_course, future_school_course],
            list(result)
        )

    def test_selector_returns_all_school_courses_for_a_given_period(self):
        school = SchoolFactory()

        period_start = faker.date_object()
        period_end = period_start + timedelta(days=100)

        started_school_course = SchoolCourseFactory(
            school=school,
            start_date=period_start - timedelta(days=10),
            end_date=period_end - timedelta(days=10)
        )
        school_course_inside_period = SchoolCourseFactory(
            school=school,
            start_date=period_start + timedelta(days=10),
            end_date=period_end - timedelta(days=10)
        )
        school_course_wrapping_period = SchoolCourseFactory(
            school=school,
            start_date=period_start - timedelta(days=5),
            end_date=period_end + timedelta(days=5)
        )
        starting_school_course = SchoolCourseFactory(
            school=school,
            start_date=period_end - timedelta(days=10),
            end_date=period_end + timedelta(days=10)
        )

        past_school_course = SchoolCourseFactory(
            school=school,
            start_date=period_start - timedelta(days=20),
            end_date=period_start - timedelta(days=10)
        )
        future_school_course = SchoolCourseFactory(
            school=school,
            start_date=period_end + timedelta(days=10),
            end_date=period_end + timedelta(days=20)
        )

        result = school_list_school_courses(
            school=school,
            start_date=period_start,
            end_date=period_end
        )

        self.assertNotIn(past_school_course, result)
        self.assertNotIn(future_school_course, result)
        self.assertEqual(
            self._order_school_courses([
                started_school_course,
                school_course_inside_period,
                school_course_wrapping_period,
                starting_school_course
            ]),
            list(result)
        )
