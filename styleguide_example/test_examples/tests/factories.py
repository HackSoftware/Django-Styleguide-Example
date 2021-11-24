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
    def students(obj, create, extracted, **kwargs):
        if create:
            students = extracted or StudentFactory.create_batch(kwargs.get('count', 5))
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
    # Make sure the student and the school_course are from the same school
    school_course = factory.SubFactory(
        SchoolCourseFactory,
        school=factory.SelfAttribute('..student.school')
    )
    # The `SelfAttribute` is just an interface that uses LazyAttribute under the hood:
    # school_course = factory.SubFactory(
    #     SchoolCourseFactory,
    #     school=factory.LazyAttribute(lambda course: course.factory_parent.student.school)
    # )

    start_date = factory.SelfAttribute('school_course.start_date')
    end_date = factory.SelfAttribute('school_course.end_date')

    active = True
    # We'd recommend you using LazyAttribute instead of Maybe as it's more explicit
    deactivated_at = factory.Maybe(
        'active',
        no_declaration=factory.LazyAttribute(lambda self: faker.date_between_dates(
            date_start=self.start_date,
            date_end=self.end_date
        )),
        yes_declaration=None
    )


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
                kwargs.get('count', 5),
                student__school=obj.school  # NOTE!
            )

            obj.rosters.set(rosters)

            return rosters
