from unittest.mock import patch

from django.test import TestCase

from styleguide_example.utils.tests import faker

from styleguide_example.testing_examples.services import student_create
from styleguide_example.testing_examples.tests.factories import SchoolFactory, SchoolCourseFactory


class StudentCreateTests(TestCase):
    @patch('styleguide_example.testing_examples.services.students.school_list_school_courses')
    @patch('styleguide_example.testing_examples.services.students.roster_create')
    def test_student_is_rostered_to_all_active_school_courses(
        self,
        roster_create_mock,
        school_courses_mock
    ):
        school = SchoolFactory()
        start_date = faker.date()
        email = faker.unique.email()

        school_courses_mock.select_related.return_value = SchoolCourseFactory.stub_batch(size=5)

        student = student_create(
            email=email,
            school=school,
            start_date=start_date
        )

        self.assertEqual(student.email, email)
        self.assertEqual(student.school, school)

        for school_course in school_courses_mock.return_value:
            roster_create_mock.assert_called_with(
                school_course=school_course,
                student=student,
                start_date=start_date,
                end_date=school_course.end_date
            )
