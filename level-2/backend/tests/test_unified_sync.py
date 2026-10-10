import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from ea_backend.unified_sync import SourceItem, SyncContractError, plan_sync, source_key

class TestUnifiedSync(unittest.TestCase):
    def test_idempotent(self):
        r = SourceItem('ea', 'google_calendar', 'item', 'r1')
        opts = dict(tenant_scope='ea', source='google_calendar', mode='incremental')
        self.assertEqual(plan_sync([], [r], **opts).changed, 1)
        self.assertEqual(plan_sync([r], [r], **opts).changed, 0)
        self.assertEqual(plan_sync([r], [], **opts).changed, 0)
    def test_tenant_isolation(self):
        self.assertNotEqual(source_key('business', 'gmail', '1'), source_key('family', 'gmail', '1'))

if __name__ == '__main__':
    unittest.main()
