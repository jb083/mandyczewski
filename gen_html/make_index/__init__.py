import lxml.html

def run(summary):
    # index.html の作成
    index = lxml.html.fromstring('''<html lang="ja">
  <head>
    <meta charset="UTF-8"/>
    <title>{0}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <link href="css/index.css" rel="stylesheet"/>
  </head>
  <body>
    <article>
      <h1>{0}</h1>
    </article>
    <footer>
      <div class="copyright"></div>
    </footer>
  </body>
</html>'''.format(summary["title"]))

    # アブストラクトの挿入
    if summary["abstract"] != "":
        abst = lxml.html.Element("div")
        abst.attrib["class"] = "abstract"
        abst.text = summary["abstract"]
        index[1][0].append(abst)

    # 目次の作成
    if "main" in summary:
        # 単一の章のみの場合
        from . import toc_main
        index = toc_main.run( index, summary )
    else:
        # 複数の章を含む場合
        from . import toc_chapter
        index = toc_chapter.run( index, summary )
    if "appendix" in summary:
        # appendix がある場合
        from . import toc_appendix
        index = toc_appendix.run( index, summary )

    # 著作権表示
    index[1][1][0].text = "©{} {}".format( summary["date"],
                                           summary["author"] )
            
    with open("../index.html","w") as f:
        index = lxml.html.tostring(index, encoding="utf-8",
                                   doctype='<!DOCTYPE html>',
                                   pretty_print=True ).decode("utf-8")
        f.write(index)


