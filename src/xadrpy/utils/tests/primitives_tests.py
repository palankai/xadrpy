import unittest2
from xadrpy.utils.primitives import PrettyFloat

class PrettyFloatTestCase(unittest2.TestCase):
    
    def test_formats(self):
        self.assertEqual(PrettyFloat(12).__repr__(), "12.0")
        self.assertEqual(PrettyFloat(12.3).__repr__(), "12.3")
        self.assertEqual(PrettyFloat(12.103).__repr__(), "12.103")
        self.assertEqual(PrettyFloat(12.1030).__repr__(), "12.103")
        self.assertEqual(PrettyFloat(12.000003).__repr__(), "12.000003")
        self.assertEqual(PrettyFloat(12.0000003).__repr__(), "12.0")
