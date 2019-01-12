#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import lxml.html
import subprocess
import multiprocessing as mp

### ツール群 ###

def clear_dom(dom):
    dom.attrib.pop("display")
    dom.attrib.pop("xmlns")
    for subdom in dom:
        subdom.drop_tree()

def write_src(src, file_name):
    # ファイル書き出し
    src = lxml.html.tostring(src, encoding="utf-8", doctype='<!DOCTYPE html>',
                             pretty_print=True ).decode("utf-8")
    with open(file_name,"w",encoding="utf-8") as f:
        f.write( src )

#################


def pandoc_convert(fp):
    subprocess.run(["pandoc", fp, "-t", "html5", "-s", "--mathml", "--section-divs",
                        "--css=../css/style.css", "-o", "../html/"+fp[:-2]+"html" ])

def pandoc(file_list):
    # pandoc による html ソースの生成
    pool = mp.Pool(len(file_list))
    pool.map(pandoc_convert, file_list)


def format_html(file_list):
    # 各 html ファイルの形を整える
    dic = {} # 数式番号の参照を解決するための辞書
    for sec, fp in enumerate(file_list):
        sec += 1
        fp = "../html/"+fp[:-2]+"html"
        with open(fp,"r",encoding="utf-8") as f:
            src = lxml.html.fromstring(f.read())
        
        # head>title の情報を補う
        src.xpath("//title")[0].text = src.xpath("//h1")[0].text

        # <p> タグを <div> タグに変換
        for dom in src.xpath("//p"):
            dom.tag = "div"
            dom.attrib["class"] = "paragraph"

        # セクション番号を付加
        for section in src.xpath("//section[@class='level1']"):
            text = section[0].text
            section[0].text = "{}. {}".format(sec, text)
            dic[section.attrib["id"]] = [ fp, "{}".format(sec) ]
        for subsec, section in enumerate(src.xpath("//section[@class='level2']")):
            text = section[0].text
            if "{}".format(text) != "None":
                section[0].text = "{}-{}. {}".format(sec, subsec+1, text)
            else:
                section[0].text = "{}-{}. ".format(sec, subsec+1)
            dic[section.attrib["id"]] = [ fp, "{}-{}".format(sec, subsec+1) ]
        
        # 独立した数式を <div> で囲い数式番号を付加
        l = 0
        for math in src.xpath("//math[@display='block']"):
            eq = copy.copy(math)
            eq.tail = ""
            # もともとあった要素を除去
            math.tag = "div"
            clear_dom(math)
            # 数式を追加
            math.attrib["class"] = "matheq"
            math.append(lxml.html.Element("span"))
            math[0].attrib["class"] = "meq"
            math[0].append(eq)
            # 数式番号を追加
            math.append(lxml.html.Element("span"))
            math[1].attrib["class"] = "mnumber"
            if math.getnext() is not None:
                if math.getnext().tag == "nolabel":
                    continue
            l += 1
            math[1].text = "({}.{})".format(sec,l)

        # 数式番号の名称を記録
        for label in src.xpath("//label"):
            eqlabel = label.attrib["id"]
            target = label.getprevious()
            target[0].attrib["id"] = eqlabel
            dic[eqlabel] = [ fp, target[1].text ]
            label.drop_tag()

        # ファイル書き出し
        src = lxml.html.tostring(src, encoding="utf-8",
                                 doctype='<!DOCTYPE html>',
                                 pretty_print=True ).decode("utf-8")
        with open(fp,"w",encoding="utf-8") as f:
            f.write( src )

    for fp in file_list:
        # 参照を解決
        fp = "../html/"+fp[:-2]+"html"
        with open(fp,"r",encoding="utf-8") as f:
            src = lxml.html.fromstring(f.read())
        for ref in src.xpath("//ref"):
            label = ref.attrib["ref"]
            ref.tag = "a"
            ref.attrib["href"] = dic[label][0]+"#{}".format(label)
            ref.text = dic[label][1]
        # ファイル書き出し
        src = lxml.html.tostring(src, encoding="utf-8",
                                 doctype='<!DOCTYPE html>',
                                 pretty_print=True ).decode("utf-8")
        with open(fp,"w",encoding="utf-8") as f:
            f.write( src )
            

def make_index(summary):
    # index.html の作成
    index = lxml.html.fromstring('''<html lang="ja">
  <head>
    <meta charset="UTF-8"/>
    <title></title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <link href="css/index.css" rel="stylesheet"/>
  </head>
  <body>
    <article>
      <h1></h1>
      <ul></ul>
    </article>
    <footer>
      <div class="copyright"></div>
    </footer>
  </body>
</html>''')
    # <title> タグ
    index[0][1].text = summary["document"]["title"]
    index[1][0][0].text = summary["document"]["title"]

    # 目次の作成
    ul = index[1][0][1]
    for fp in summary["files"]["main"]:
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

    # 著作権表示
    index[1][1][0].text = "©{} {}".format( summary["document"]["date"],
                                           summary["document"]["author"] )
            
    with open("../index.html","w") as f:
        index = lxml.html.tostring(index, encoding="utf-8",
                                   doctype='<!DOCTYPE html>',
                                   pretty_print=True ).decode("utf-8")
        f.write(index)


def make_footer(file_list, doc):
    # 各ファイルにフッターを生成
    section_names = []
    # セクション名を取得
    with open("../index.html", "r", encoding="utf-8") as f:
        src = lxml.html.fromstring(f.read())
    for a in src.xpath("/html/body/article/ul/li/a"):
        section_names.append(a.text)
    for i, fp in enumerate(file_list):
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
            div.append(lxml.html.Element("a"))
            div[0].text = section_names[i-1]
            div[0].attrib["href"] = file_list[i-1][:-2]+"html"
        footer[0].append( div )
        # 目次
        div = lxml.html.Element("div")
        div.append(lxml.html.Element("a"))
        div[0].text = "目次"
        div[0].attrib["href"] = "../index.html"
        footer[0].append( div )
        if i < len(file_list)-1:
            # 次のセクション
            div = lxml.html.Element("div")
            div.append(lxml.html.Element("a"))
            div[0].text = section_names[i+1]
            div[0].attrib["href"] = file_list[i+1][:-2]+"html"
            footer[0].append( div )
        # 著作権表示
        div = lxml.html.Element("div")
        div.attrib["class"] = "copyright"
        div.text="©{} {}".format(doc["date"], doc["author"])
        footer.append(div)
        
        # ファイル書き出し
        src[1].append( footer )
        write_src(src, fp)
