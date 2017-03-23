
from ..lib.schedule import ScheduleSubproject
import unittest

class TestScheduleSubproject(unittest.TestCase):

    def test_basic(self):
        sp = ScheduleSubproject("Calculus")
        self.assertEqual(sp.getName(), "Calculus")

