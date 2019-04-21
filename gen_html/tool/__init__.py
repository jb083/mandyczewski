import sys
import lxml.html


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

