from hashlib import md5
from .models import Password
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def test_passwd(self):
        plain = '123'
        pwd = Password.make_passwd(plain)
        ent = Password.new(passwd=plain, name='test')
        self.assertEqual(pwd, ent.passwd)


