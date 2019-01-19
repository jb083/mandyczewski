#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import toml
import copy
import lxml.html
import subprocess
import multiprocessing as mp

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
            fl.extend(c["files"])
        return fl
    else:
        print("Error: `SUMMARY.toml` must have `main` or `chapter`, but can not find it.")
        print( summary )
        sys.exit()


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
    devnull = open('/dev/null', 'w')
    subprocess.run(["pandoc", fp, "-t", "html5", "-s", "--mathml", "--section-divs",
                    "--css=../css/style.css", "-o", "../html/"+fp[:-2]+"html",
    ], stderr=devnull)

def pandoc(summary):
    # pandoc による html ソースの生成
    fl = file_list(summary)
    pool = mp.Pool(len(fl))
    pool.map(pandoc_convert, fl)
    pool.close()

    fl = summary["appendix"]
    if len(fl) > 0:
        pool = mp.Pool(len(fl))
        pool.map(pandoc_convert, fl)
        pool.close()


def format_html_file(fp, sec, dic):
    with open(fp,"r",encoding="utf-8") as f:
        src = lxml.html.fromstring(f.read())
        
    # head>title の情報を補う
    src.xpath("//title")[0].text = "{}".format(src.xpath("//h1")[0].text)

    # <p> タグを <div> タグに変換
    for dom in src.xpath("//p"):
        dom.tag = "div"
        dom.attrib["class"] = "paragraph"

    # 脚注があるとき, <hr> 要素を除去
    for footnote in src.xpath("//section[@class='footnotes']"):
        footnote.remove(footnote[0])

    # セクション番号を付加
    for section in src.xpath("//section[@class='level1']"):
        text = section[0].text
        if "{}".format(text) != "None":
            section[0].text = "{}. {}".format(sec, text)
        else:
            section[0].text = "{}. ".format(sec)
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
        math[1].text = "({}.{})".format(sec.replace("-","."),l)

    # 数式番号の名称を記録
    for label in src.xpath("//label"):
        eqlabel = label.attrib["id"]
        target = label.getprevious()
        target[0].attrib["id"] = eqlabel
        dic[eqlabel] = [ fp, target[1].text ]
        label.drop_tag()

    # 図に連番を振り記録
    figcount = 0
    for figure in src.xpath("//figure"):
        figcount += 1
        for child in list(figure):
            if child.tag == "figcaption":
                if "{}".format(child.text) != "None":
                    child.text = "図{}-{}: {}".format(sec, figcount, child.text)
                else:
                    child.text = "図{}-{}: ".format(sec, figcount)
        if "id" in figure.attrib:
            dic[figure.attrib["id"]] = [ fp, "{}-{}".format(sec, figcount) ]
        

    # ファイル書き出し
    write_src(src, fp)


def reference(fp, dic):
    fp = "../html/"+fp[:-2]+"html"
    with open(fp,"r",encoding="utf-8") as f:
        src = lxml.html.fromstring(f.read())
    for ref in src.xpath("//ref"):
        label = ref.attrib["ref"]
        ref.tag = "a"
        if not label in dic:
            print("Error: label {} in '{}' is not declared.".format(label, fp))
            sys.exit()
        ref.attrib["href"] = dic[label][0]+"#{}".format(label)
        ref.text = dic[label][1]
    # ファイル書き出し
    write_src(src, fp)
    
def format_html(summary):
    # 各 html ファイルの形を整える
    dic = {} # 数式番号の参照を解決するための辞書
    if "main" in summary:
        for sec, fp in enumerate(summary["main"]):
            sec += 1
            fp = "../html/"+fp[:-2]+"html"
            format_html_file(fp, "{}".format(sec), dic)
    elif "chapter" in summary:
        for cp, clist in enumerate(summary["chapter"]):
            cp += 1
            for sec, fp in enumerate(clist["files"]):
                sec += 1
                fp = "../html/"+fp[:-2]+"html"
                format_html_file(fp, "{}-{}".format(cp,sec), dic)
    for sec, fp in enumerate(summary["appendix"]):
        sec = [ "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", ][sec]
        fp = "../html/"+fp[:-2]+"html"
        format_html_file(fp, "{}".format(sec), dic)

    # 参照を解決
    for fp in file_list(summary):
        reference(fp, dic)
    for fp in summary["appendix"]:
        reference(fp, dic)
        


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


def make_index(summary):
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
    index = make_toc( index, file_list(summary) )
    index = make_toc( index, summary["appendix"] )

    # 著作権表示
    index[1][1][0].text = "©{} {}".format( summary["date"],
                                           summary["author"] )
            
    with open("../index.html","w") as f:
        index = lxml.html.tostring(index, encoding="utf-8",
                                   doctype='<!DOCTYPE html>',
                                   pretty_print=True ).decode("utf-8")
        f.write(index)


def make_footer(summary):
    fl = file_list(summary)
    # 各ファイルにフッターを生成
    section_names = []
    # セクション名を取得
    with open("../index.html", "r", encoding="utf-8") as f:
        src = lxml.html.fromstring(f.read())
    for a in src.xpath("/html/body/article/ul/li/a"):
        section_names.append(a.text)
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
            div.append(lxml.html.Element("a"))
            div[0].text = section_names[i-1]
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
            div.append(lxml.html.Element("a"))
            div[0].text = section_names[i+1]
            div[0].attrib["href"] = fl[i+1][:-2]+"html"
            footer[0].append( div )
        # 著作権表示
        div = lxml.html.Element("div")
        div.attrib["class"] = "copyright"
        div.text="©{} {}".format(summary["date"], summary["author"])
        footer.append(div)
        
        # ファイル書き出し
        src[1].append( footer )
        write_src(src, fp)
