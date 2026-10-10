import unittest

class TestSmoke(unittest.TestCase):
    def test_planner(self):
        from ea_backend.unified_sync import source_key
        self.assertNotEqual(source_key('a','gmail','1'),source_key('b','gmail','1'))
