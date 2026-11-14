#!/usr/bin/env python3
"""dircmp - structural comparison of two directory trees."""
import argparse
import os
import sys


def snapshot(root):
    out = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in {".git", "__pycache__"})
        for name in filenames:
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, root).replace(os.sep, "/")
            try:
                out[rel] = os.path.getsize(path)
            except OSError:
                out[rel] = -1
    return out


def compare(left, right):
    only_left = sorted(set(left) - set(right))
    only_right = sorted(set(right) - set(left))
    changed = sorted(k for k in set(left) & set(right) if left[k] != right[k])
    return only_left, only_right, changed


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="dircmp", description=__doc__)
    ap.add_argument("left")
    ap.add_argument("right")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)
    a, b = snapshot(args.left), snapshot(args.right)
    only_a, only_b, changed = compare(a, b)
    for path in only_a:
        print("- %s" % path)
    for path in only_b:
        print("+ %s" % path)
    for path in changed:
        print("~ %s (%d -> %d bytes)" % (path, a[path], b[path]))
    if not (only_a or only_b or changed):
        print("identical")
    return 0 if not changed else 1


if __name__ == "__main__":
    raise SystemExit(main())
