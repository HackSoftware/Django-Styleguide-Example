from django.db.models import CharField

import string, random

def generate_uid(length):
    _letters_and_digits = string.ascii_letters + string.digits
    return ''.join((random.choice(_letters_and_digits) for i in range(length)))


class UidField(CharField):
    def __init__(self, length=28, **kwargs):
        kwargs['max_length'] = length
        kwargs['default'] = generate_uid(length)

        self.uid = kwargs['default']

        super().__init__(**kwargs)


    def __str__(self):
        return self.uid

    def __repr__(self):
        return self.uid
