from unittest.mock import patch
from datetime import timedelta

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone

from styleguide_example.testing_examples.tests.factories import (
    StudentFactory,
    SchoolCourseFactory
)

from styleguide_example.testing_examples.models import Roster
from styleguide_example.testing_examples.services import (
    roster_create,
    ROSTER_CREATE_DIFFERENT_SCHOOLS
)


class RosterCreateTests(TestCase):
    def test_service_raises_error_if_different_schools(self):
        school_course = SchoolCourseFactory.build()
        student = StudentFactory.build()

        with self.assertRaisesMessage(
            ValidationError,
            ROSTER_CREATE_DIFFERENT_SCHOOLS.format(student=student, school_course=school_course)
        ):
            roster_create(student=student, school_course=school_course)

        self.assertEqual(Roster.objects.count(), 0)

    @patch('styleguide_example.testing_examples.services.rosters.roster_validate_period')
    def test_service_does_not_create_roster_if_period_is_not_valid(self, roster_validate_period_mock):
        roster_validate_period_mock.side_effect = ValidationError('')

        school_course = SchoolCourseFactory.build()
        student = StudentFactory.build()

        with self.assertRaises(ValidationError):
            roster_create(student=student, school_course=school_course)

        self.assertEqual(Roster.objects.count(), 0)

    @patch('styleguide_example.testing_examples.services.rosters.roster_validate_period')
    def test_service_uses_school_course_period_for_default_period(self, roster_validate_period_mock):
        school_course = SchoolCourseFactory()
        student = StudentFactory(school=school_course.school)

        roster = roster_create(student=student, school_course=school_course)

        self.assertEqual(roster.start_date, school_course.start_date)
        self.assertEqual(roster.end_date, school_course.end_date)

    @patch('styleguide_example.testing_examples.services.rosters.roster_validate_period')
    def test_service_doesn_not_school_course_period_if_dates_are_passed(self, roster_validate_period_mock):
        school_course = SchoolCourseFactory()
        student = StudentFactory(school=school_course.school)

        start_date = timezone.now().date()
        end_date = school_course.end_date - timedelta(days=1)

        roster = roster_create(
            student=student,
            school_course=school_course,
            start_date=start_date,
            end_date=end_date
        )

        self.assertEqual(roster.start_date, start_date)
        self.assertEqual(roster.end_date, end_date)
