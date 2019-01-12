#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import toml
from gen_html import *

def read_summary():
    # 文書データの読み込み
    if not os.path.exists("SUMMARY.toml"):
        print("Error: can not find `SUMMARY.toml` in this directory.")
        sys.exit()
    with open("SUMMARY.toml","r") as f:
        summary = toml.load(f)
    return summary

def file_list(summary):
    if "main" in summary:
        return summary["main"]
    elif "chapter" in summary:
        fl = []
        for c in summary["chapter"]:
            fl.extend(c)
        return fl
    else:
        sys.exit()

            
if __name__ == "__main__":
    summary = read_summary()
    pandoc(file_list(summary))
    if "main" in summary["files"]:
        format_html(summary["files"]["main"])
    make_index(summary)
    make_footer(summary["files"]["main"], summary["document"])
