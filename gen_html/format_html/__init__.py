import sys
import copy
import lxml.html
import subprocess
from itertools import chain
import multiprocessing as mp

from .. import tool


def format_html_file(fp, sec, book_title):
    dic = {}
    with open(fp,"r",encoding="utf-8") as f:
        src = lxml.html.fromstring(f.read())
        
    # head>title の情報を補う
    h1 = src[1][0][0]
    title = ""
    if "{}".format(h1.text) != "None":
        title += h1.text
    for elem in list(h1):
        if elem.tag == "math": # <math> 要素が含まれるとき, <annotation> 要素のテキストに置き換える
            title += elem[0][-1].text 
        elif "{}".format(elem.text) != "None":
            title += elem.text # そうでなく text フィールドを持つとき, そのテキストに置き換える (em タグ等)
        title += elem.tail
    src.xpath("//title")[0].text = title + " - {}".format(book_title)

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
        tool.clear_dom(math)
        # 数式を追加
        math.attrib["class"] = "matheq"
        math.append(lxml.html.Element("span"))
        math[0].attrib["class"] = "meq"
        math[0].append(eq)
        # 数式番号を追加
        math.append(lxml.html.Element("span"))
        math[1].attrib["class"] = "mnumber"
        if math.getnext() is not None:
            next_element = math.getnext()
            if next_element.tag == "nolabel":
                next_element.drop_tag()
                continue
            if next_element.tag == "tag":
                math[1].text = "({})".format(next_element.attrib["id"])
                continue
        l += 1
        math[1].text = "({}.{})".format(sec.replace("-","."),l)
    
    # 数式番号の名称を記録
    for label in chain( src.xpath("//label"), src.xpath("//tag") ):
        eqlabel = label.attrib["id"]
        parent = label.getparent()
        if len(parent) == 1:
            # (誤って) label 要素が p タグで囲まれた場合, p 要素自体を label とみなす
            label.drop_tree()
            label = parent
        target = label.getprevious()
        target[0].attrib["id"] = eqlabel
        if eqlabel in dic:
            print("Error: The id {} in {} already exists!".format(eqlabel,fp))
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
    tool.write_src(src, fp)

    return dic


def reference(fp, dic):
    # 参照の解決
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
    tool.write_src(src, fp)

    
def parallel_format(args):
    fp = args[0]
    name = args[1]
    book_title = args[2]
    dic = format_html_file(fp, name, book_title)
    return dic


def run(summary):
    # 各 html ファイルの形を整える
    dic = {} # 数式番号の参照を解決するための辞書
    if "main" in summary:
        # すべての節に対して parallel_format 関数を並列に適用
        args = []
        for sec, fp in enumerate(summary["main"]):
            args.append([ "../html/"+fp[:-2]+"html", "{}".format(sec+1), summary["title"] ])
        pool = mp.Pool(len(summary["main"]))
        dics = pool.map(parallel_format, args)
        for d in dics:
            dic.update(d)
    elif "chapter" in summary:
        for cp, clist in enumerate(summary["chapter"]): # 章を巡回
            if len(clist["files"]) == 0:
                # この章が節を含まないとき警告を表示して以下の処理を省略
                sys.stderr.write("Warning: no files in the chapter '{}'\n".format(clist["name"]))
                continue
            # すべての節に対して parallel_format 関数を並列に適用
            cp += 1
            args = []
            for sec, fp in enumerate(clist["files"]):
                args.append([ "../html/"+fp[:-2]+"html", "{}-{}".format(cp,sec+1), summary["title"] ])
            pool = mp.Pool(len(clist["files"]))
            dics = pool.map(parallel_format, args)
            for d in dics:
                dic.update(d)
    # appendix がある場合はそれも実行
    if "appendix" in summary:
        if len(summary["appendix"]) > 0:
            args = []
            for sec, fp in enumerate(summary["appendix"]):
                sec = [ "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                        "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", ][sec]
                args.append([ "../html/"+fp[:-2]+"html", "{}".format(sec), summary["title"] ])
            pool = mp.Pool(len(summary["appendix"]))
            dics = pool.map(parallel_format, args)
            for d in dics:
                dic.update(d)

    # 参照を解決
    for fp in tool.file_list(summary):
        reference(fp, dic)
    if "appendix" in summary:
        for fp in summary["appendix"]:
            reference(fp, dic)
        

