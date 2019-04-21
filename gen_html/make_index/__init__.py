import lxml.html
from .. import tool

def make_toc(index, file_list):
    ul = lxml.html.Element("ul")
    for fp in file_list:
        fp = "../html/"+fp[:-2]+"html"
        with open(fp, "r", encoding="utf-8") as f:
            src = lxml.html.fromstring(f.read())
        li = lxml.html.Element("li")
        for section in src.xpath("//section[@class='level1']"):
            h1 = section[0]
            h1.tag = "a"
            h1.attrib["href"] = fp[3:]
            li.append(h1)
        li.append(lxml.html.Element("ul"))
        for section in src.xpath("//section[@class='level2']"):
            h2 = section[0]
            h2.tag = "a"
            h2.attrib["href"] = fp[3:]+"#"+section.attrib["id"]
            subli = lxml.html.Element("li")
            subli.append(h2)
            li[1].append(subli)
        ul.append(li)
    index[1][0].append(ul)
    return index


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
    index = make_toc( index, tool.file_list(summary) )
    if "appendix" in summary:
        index = make_toc( index, summary["appendix"] )

    # 著作権表示
    index[1][1][0].text = "©{} {}".format( summary["date"],
                                           summary["author"] )
            
    with open("../index.html","w") as f:
        index = lxml.html.tostring(index, encoding="utf-8",
                                   doctype='<!DOCTYPE html>',
                                   pretty_print=True ).decode("utf-8")
        f.write(index)


