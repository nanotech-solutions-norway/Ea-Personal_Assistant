import pathlib
import sys
import unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from ea_backend.unified_sync import SourceItem, plan_sync, SyncContractError

class TestUnifiedSyncDeletion(unittest.TestCase):
    def test_full_missing_only_when_complete(self):
        old = [SourceItem('ea','google_calendar','a','1')]
        a = dict(tenant_scope='ea',source='google_calendar',mode='full')
        self.assertEqual(plan_sync(old, [], **a).changed, 0)
        self.assertEqual(len(plan_sync(old, [], collection_complete=True, **a).to_tombstone), 1)
    def test_explicit_delete(self):
        old = [SourceItem('ea','google_calendar','a','1')]
        changed = [SourceItem('ea','google_calendar','a','2','deleted')]
        self.assertEqual(len(plan_sync(old,changed,tenant_scope='ea',source='google_calendar',mode='incremental').to_tombstone),1)
