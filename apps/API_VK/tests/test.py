from django.test import SimpleTestCase


class FirstTest(SimpleTestCase):
    def test1(self):
        self.assertEqual(1, 1)
