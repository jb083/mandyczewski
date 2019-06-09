import lxml.html
from .. import tool

def run(index, summary):
    file_list = tool.file_list(summary)
    
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
            h2.tail = "" # 第1段落が div で囲まれていない場合うまくいかないのを修正
            h2.tag = "a"
            h2.attrib["href"] = fp[3:]+"#"+section.attrib["id"]
            subli = lxml.html.Element("li")
            subli.append(h2)
            li[1].append(subli)
        ul.append(li)
    index[1][0].append(ul)
    return index
