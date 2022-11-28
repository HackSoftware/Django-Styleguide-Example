import factory

from styleguide_example.common.models import RandomModel, SimpleModel
from styleguide_example.utils.tests import faker


class RandomModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RandomModel

    end_date = factory.LazyAttribute(lambda self: faker.date_object())
    start_date = factory.LazyAttribute(lambda self: faker.date_object(end_datetime=self.end_date))


class SimpleModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SimpleModel

    name = factory.LazyAttribute(lambda self: faker.word())
