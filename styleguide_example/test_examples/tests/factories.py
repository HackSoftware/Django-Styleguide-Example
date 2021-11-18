from datetime import timedelta

import factory

from django.utils.text import slugify

from styleguide_example.utils.tests import faker
from styleguide_example.test_examples.models import (
    School,
    Student,
    Roster,
    SchoolCourse
)


class SchoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = School

    name = factory.LazyAttribute(lambda _: f'{faker.unique.company()} School')
    slug = factory.LazyAttribute(lambda self: slugify(self.name))


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student

    email = factory.LazyAttribute(lambda _: faker.unique.email())
    identifier = factory.LazyAttribute(lambda _: faker.unique.uuid4())
    school = factory.SubFactory(SchoolFactory)


class SchoolWithStudentsFactory(SchoolFactory):
    @factory.post_generation
    def students(obj, created, extracted, **kwargs):
        if created and extracted is None:
            students = StudentFactory.create_batch(kwargs.get('count', 5))
            obj.students.set(students)

            return students


class SchoolCourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SchoolCourse

    name = factory.LazyAttribute(lambda _: faker.unique.sentence(nb_words=3)[:-1])  # remove the end punctuation
    short_name = factory.LazyAttribute(lambda self: self.name.split(' ')[0])
    slug = factory.LazyAttribute(lambda self: slugify(self.name))
    school = factory.SubFactory(SchoolFactory)

    start_date = factory.LazyAttribute(lambda _: faker.past_date())
    # The code below might cause bugs if you only pass start_date to you factory
    # end_date = factory.LazyAttribute(lambda _: faker.future_date())
    end_date = factory.LazyAttribute(lambda self: self.start_date + timedelta(days=365))


class RosterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Roster

    student = factory.SubFactory(StudentFactory)
    # Make sure the student and the school_course are from the same school
    school_course = factory.SubFactory(SchoolCourseFactory, school=factory.SelfAttribute('..student.school'))

    # The code below might cause bugs because of the school_course period
    # start_date = factory.LazyAttribute(lambda _: faker.past_date())
    # end_date = factory.LazyAttribute(lambda _: faker.future_date())
    start_date = factory.LazyAttribute(lambda self: faker.date_between_dates(
        date_start=self.school_course.start_date,
        date_end=self.school_course.end_date - timedelta(days=1)
    ))
    end_date = factory.LazyAttribute(lambda self: faker.date_between_dates(
        date_start=self.start_date,
        date_end=self.school_course.end_date
    ))

    active = True
    deactivated_at = factory.Maybe(
        'active',
        no_declaration=factory.LazyAttribute(lambda self: faker.date_between_dates(
            date_start=self.start_date,
            date_end=self.end_date
        )),
        yes_declaration=None
    )


class SchoolCourseWithRostersFactory(SchoolCourseFactory):
    @factory.post_generation
    def rosters(obj, created, extracted, **kwargs):
        if created and extracted is None:
            rosters = RosterFactory.create_batch(
                kwargs.get('count', 5),
                student__school=obj.school  # NOTE!
            )
            obj.rosters.set(rosters)

            return rosters
