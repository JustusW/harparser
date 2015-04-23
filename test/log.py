import unittest
from harparser import HAR


class TestLog(unittest.TestCase):
    def test_json_scaffold_on_derived_classes(self):
        class derived(HAR.log):
            pass
        
        tmp = derived({
            "version":"1.2",
            "creator":{"name":"MITMPROXY HARExtractor","version":"0.1","comment":""},
            "pages":[],
            "entries":[]
        })

        assert tmp.json().startswith('{"log":')
