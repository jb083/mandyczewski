# pandoc
#
# markdown ファイルを pandoc により html ファイルに変換する
# 

import os
import subprocess
import multiprocessing as mp


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


def pandoc_convert(fp):
    devnull = open('/dev/null', 'w')
    subprocess.run(["pandoc", fp, "-t", "html5", "-s", "--mathml", "--section-divs",
                    "--css=../css/style.css", "-o", "../html/"+fp[:-2]+"html",
    ], stderr=devnull)

def run(summary):
    # html ディレクトリが存在しなければつくる
    if not os.path.exists("../html"):
        os.mkdir("../html")
    # pandoc による html ソースの生成
    fl = file_list(summary)
    pool = mp.Pool(len(fl))
    pool.map(pandoc_convert, fl)
    pool.close()

    if "appendix" in summary:
        fl = summary["appendix"]
        if len(fl) > 0:
            pool = mp.Pool(len(fl))
            pool.map(pandoc_convert, fl)
            pool.close()


