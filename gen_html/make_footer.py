import lxml.html
from . import tool


def run(summary):
    fl = tool.file_list(summary)
    if "appendix" in summary:
        fl.extend(summary["appendix"])
    # 各ファイルにフッターを生成
    section_names = []
    # セクション名を取得
    with open("../index.html", "r", encoding="utf-8") as f:
        src = lxml.html.fromstring(f.read())
    for a in src.xpath("/html/body/article/ul/li/a"):
        section_names.append(a)
    for i, fp in enumerate(fl):
        fp = "../html/"+fp[:-2]+"html"
        with open(fp,"r",encoding="utf-8") as f:
            src = lxml.html.fromstring(f.read())
        # # 本文を <article> 要素で囲う
        # article = lxml.html.Element("article")
        # article.append( src[1][0] )
        # src[1].append(article)
        src[1][0].tag = "article"
        # フッター
        footer = lxml.html.Element("footer")
        footer.append( lxml.html.Element("nav") )
        # 前のセクション
        div = lxml.html.Element("div")
        div.attrib["class"] = "previous"
        if i > 0:
            div.append( section_names[i-1] )
            div[0].attrib["href"] = fl[i-1][:-2]+"html"
        footer[0].append( div )
        # 目次
        div = lxml.html.Element("div")
        div.append(lxml.html.Element("a"))
        div[0].text = "目次"
        div[0].attrib["href"] = "../index.html"
        footer[0].append( div )
        if i < len(fl)-1:
            # 次のセクション
            div = lxml.html.Element("div")
            div.append( section_names[i+1] )
            div[0].attrib["href"] = fl[i+1][:-2]+"html"
            footer[0].append( div )
        # 著作権表示
        div = lxml.html.Element("div")
        div.attrib["class"] = "copyright"
        div.text="©{} {}".format(summary["date"], summary["author"])
        footer.append(div)
        
        # ファイル書き出し
        src[1].append( footer )
        tool.write_src(src, fp)
