#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from gen_html import *
from new_note import new_note

def gen_html():
    # SUMMARY.toml の読み込み
    summary = read_summary()
    
    # pandoc により HTML ファイルを生成
    pandoc(summary)

    # HTML ファイルを調整しセクション番号および数式番号を付加,
    # 相対参照を解決してハイパーリンクを張る
    format_html(summary)

    # index.html を作成し, 各 HTML ファイルにフッターを付加
    make_index(summary)
    make_footer(summary)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        gen_html()
    elif sys.argv[1] == "gen":
        gen_html()
    elif sys.argv[1] == "new":
        new_note()
