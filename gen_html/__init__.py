#!/usr/bin/env python3

def gen_html():
    # SUMMARY.toml の読み込み
    from . import read_summary
    summary = read_summary.read_summary()
    
    # pandoc により HTML ファイルを生成
    from . import pandoc
    pandoc.run(summary)

    # HTML ファイルを調整しセクション番号および数式番号を付加,
    # 相対参照を解決してハイパーリンクを張る
    from . import format_html
    format_html.run(summary)

    # index.html を作成し, 各 HTML ファイルにフッターを付加
    from . import make_index
    make_index.run(summary)
    from . import make_footer
    make_footer.run(summary)
