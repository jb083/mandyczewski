# read_summary
#
# "SUMMARY.toml" を読み込んでパースする.
#

import os
import sys
import toml

def read_summary():
    # 文書データの読み込み
    if not os.path.exists("SUMMARY.toml"):
        print("Error: can not find `SUMMARY.toml` in this directory.")
        sys.exit()
    with open("SUMMARY.toml","r") as f:
        summary = toml.load(f)
    return summary
