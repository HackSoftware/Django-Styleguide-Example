from django.test import TestCase


class StandardUploadApiTests(TestCase):
    """
    We want to test the following general cases:

    1. Upload a file, below the size limit, assert models gets created accordingly.
    1. Upload a file, above the size limit (patch settings), assert API error, nothing gets created.
    """


class StandardUploadAdminTests(TestCase):
    """
    We want to test the following general cases:

    File within size limit:

    1. Create a new file via the Django admin, assert everything gets created (we are using services there).
    2. Update an existing file via the Django admin, assert everything gets updated (we are using services there).

    File not within size limit:

    1. Create a new file via the Django admin, assert error, nothing gets created.
    2. Update an existing fila via the Django admin, assert error, nothing gets created.
    """
