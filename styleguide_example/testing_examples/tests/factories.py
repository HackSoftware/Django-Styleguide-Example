from datetime import timedelta

import factory

from django.utils.text import slugify

from styleguide_example.utils.tests import faker
from styleguide_example.testing_examples.models import (
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
    def students(obj, create, extracted, **kwargs):
        if create:
            students = extracted or StudentFactory.create_batch(
                kwargs.pop('count', 5),
                **kwargs
            )
            obj.students.set(students)
            return students


class SchoolCourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SchoolCourse

    name = factory.LazyAttribute(lambda _: faker.unique.sentence(nb_words=3)[:-1])  # remove the end punctuation
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

    # NOTE: You can use `factory.SelfAttribute` for the below attributes.
    # We prefer using `factory.LazyAttribute` as we find the definition more explicit.
    school_course = factory.SubFactory(
        SchoolCourseFactory,
        school=factory.LazyAttribute(
            lambda course: course.factory_parent.student.school
        )
    )

    start_date = factory.LazyAttribute(lambda _self: _self.school_course.start_date)
    end_date = factory.LazyAttribute(lambda _self: _self.school_course.end_date)


def get_future_roster_start_date(roster_obj):
    if not roster_obj.start_after:
        return faker.future_date()

    return roster_obj.start_after + timedelta(days=faker.pyint(2, 100))


class FutureRosterFactory(RosterFactory):
    """
    Example usage:
        future_roster1 = FutureRosterFactory()
        future_roster2 = FutureRosterFactory(start_after=future_roster1.end_date)
    """

    class Params:
        start_after = None

    start_date = factory.LazyAttribute(get_future_roster_start_date)


class SchoolCourseWithRostersFactory(SchoolCourseFactory):
    @factory.post_generation
    def rosters(obj, create, extracted, **kwargs):
        if create:
            rosters = extracted or RosterFactory.create_batch(
                kwargs.pop('count', 5),
                **kwargs,
                student__school=obj.school  # NOTE!
            )

            obj.rosters.set(rosters)

            return rosters
