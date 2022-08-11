import factory

from styleguide_example.utils.tests import faker

from styleguide_example.users.models import BaseUser


class BaseUserFactory(factory.django.DjangoModelFactory):
    email = factory.LazyAttribute(lambda _: faker.unique.email())

    class Meta:
        model = BaseUser
