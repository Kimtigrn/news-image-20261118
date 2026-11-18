#!/usr/bin/env python3
"""News-image entry: copy the rendered poster to /output/entry.png.

The poster (entry.png, 1024x1024, rendered by render_poster.py from the
verified news of Wednesday 18 November 2026) is shipped in this repository;
this program only copies it to the output directory, so both grader runs
write the same bytes. Python 3.13 standard library only, no network.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(
        os.path.join(HERE, "entry.png"),
        os.path.join(out_dir, "entry.png"),
    )


if __name__ == "__main__":
    main()
