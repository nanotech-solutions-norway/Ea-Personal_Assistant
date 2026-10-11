import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from ea_backend.provider_paging import SourcePage, collect_source_pages
from ea_backend.unified_sync import SourceItem, SyncContractError

class PagingTests(unittest.TestCase):
    def test_complete_multi_page_snapshot(self):
        item = SourceItem("business", "google_drive", "f1", "rev1", collection_key="project")
        seen = []
        def fetch(token):
            seen.append(token)
            if token is None:
                return SourcePage((item,), "page2")
            return SourcePage((), None, "cursor-last")
        outcome = collect_source_pages(fetch)
        self.assertEqual(outcome.pages_fetched, 2)
        self.assertEqual(outcome.source_cursor, "cursor-last")
        self.assertEqual(len(outcome.items), 1)
        self.assertEqual(seen, [None, "page2"])
    def test_repeated_page_token_rejected(self):
        with self.assertRaises(SyncContractError):
            collect_source_pages(lambda _: SourcePage((), "again"), max_pages=4)
    def test_missing_final_cursor_rejected(self):
        with self.assertRaises(SyncContractError):
            collect_source_pages(lambda _: SourcePage((), None))
    def test_page_limit_fails_closed(self):
        with self.assertRaises(SyncContractError):
            collect_source_pages(lambda t: SourcePage((), "a" if t is None else "b"), max_pages=2)
    def test_nonterminal_cursor_rejected(self):
        with self.assertRaises(SyncContractError):
            collect_source_pages(lambda _: SourcePage((), "p2", "early"))
    def test_item_cap_rejected(self):
        item = SourceItem("business","github","issue1","rev1")
        with self.assertRaises(SyncContractError):
            collect_source_pages(lambda _: SourcePage((item,item), None, "cursor"),max_items=1)

if __name__ == "__main__":
    unittest.main()
