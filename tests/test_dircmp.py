import os
import tempfile
import unittest

from dircmp import compare, snapshot


class DirCmpTest(unittest.TestCase):
    def test_compare(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = os.path.join(tmp, "a")
            b = os.path.join(tmp, "b")
            os.makedirs(a)
            os.makedirs(b)
            open(os.path.join(a, "same"), "w").write("1")
            open(os.path.join(b, "same"), "w").write("1")
            open(os.path.join(a, "only"), "w").write("x")
            open(os.path.join(b, "same"), "a").write("more")
            only_a, only_b, changed = compare(snapshot(a), snapshot(b))
            self.assertEqual(only_a, ["only"])
            self.assertEqual(only_b, [])
            self.assertEqual(changed, ["same"])


if __name__ == "__main__":
    unittest.main()
