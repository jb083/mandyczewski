#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import datetime

style = r"""@charset "utf-8";
@import url('./mathfont.css');

/* 文字の表示 */
body { font-family: 'Yu Mincho', 'YuMincho', 'Source Han Serif JP', 'Noto Serif CJK JP', 'Noto Serif JP', serif; }
div.paragraph { padding-bottom: 1em; text-indent: 1em; line-height: 2; }
ul>li { list-style-type: square; }
h3 { text-indent: 1em; }
math[display="block"] {
    margin-top: 4px; margin-bottom: 4px;
}

h1 { font-size: x-large; }
h2 { font-size: x-large; }

/* .sourceCode { background: #f0f0f0; } */
figure {
    text-align: center;
}

/* テーブル */
table {
    margin-left: auto;
    margin-right: auto;
    border-collapse: collapse;
    caption-side: bottom;
    text-align: center; 
}
td { padding: 0 1em; }
td + td, th + th { border-left: 1px solid; }
tbody tr { border-top: 1px solid; }


/* 数式と数式番号の表示 */
div.matheq {
    display: grid;
    grid-template-columns: 4em 1fr;
    align-items: center;
    overflow: scroll;
}
.meq {
    grid-column: 2/3;
    grid-row: 1/2;
    margin-right: 3em;
    /* overflow: scroll; */
    text-indent: initial;
}
.mnumber {
    grid-column: 1/2;
    grid-row: 1/2;
    text-align: left;
    vertical-align: middle;
    text-indent: initial;
}

/* 脚注 */
section.footnotes {
    border-top: solid 1px;
}


/* フッター */
footer {
    margin-top: 1em;
    border-top: solid 1px;
}
footer nav {
    margin: 0.5em 0;
    display: grid;
    grid-template-columns: 4em 1fr;
}
footer nav div {
    text-align: center;
}
footer div.previous { /* 前の節へのリンクを非表示にする */
    display: none;
}
.copyright {
    font-size: small;
    text-align: center;
}



@media screen and (min-width: 520px) {
    .level1, .level2 {
	margin-left: 12.5%;
	margin-right: 12.5%;
    }
    div.matheq {
	grid-template-columns: 1fr 4em;
	overflow: visible;
    }

    .meq {
	grid-column: 1/2;
	grid-row: 1/2;
	margin-right: initial;
    }
    .mnumber {
	grid-column: 2/3;
	grid-row: 1/2;
	text-align: right;
    }

   /* 脚注 */
    .footnotes {
	margin-left: 12.5%;
	margin-right: 12.5%;
    }

    /* フッター */
    footer nav {
	grid-template-columns: 1fr 4em 1fr;
    }
    footer div.previous { display: block; }
}
"""

index = r"""@charset "utf-8";
@import url('./mathfont.css');
@import url('https://fonts.googleapis.com/css?family=Noto+Serif+JP:300,600&subset=japanese');

/* デザイン */
figure { text-align: center; }
table { text-align: center; }

/* 文字の表示 */
body { font-family: 'Yu Mincho', 'YuMincho', 'Source Han Serif JP', 'Noto Serif CJK JP', 'Noto Serif JP' }
a { color: black; text-decoration: none; }
a:hover { color: #800080; }
p { text-indent: 1em; line-height: 1.75; }
math[display="block"] {
    margin-top: 4px;
    margin-bottom: 4px;
}


/* 目次のナンバリング */
ul { padding-left: 0; }
li>ul { padding-left: 2em; }
article>ul {
    margin-top: 4px;
    margin-bottom: 16px;
}
li{
    list-style-type: none;
}
.chapter-title {
    margin-top: 4px;
    margin-bottom: 4px;
    padding-left: 1em;
    font-size: large;
}

/* フッター */
footer {
    margin-top: 1em;
    /* border-top: solid 1px; */
}
.copyright {
    margin-top: 0.5em;
    font-size: small;
    text-align: center;
}


@media screen and (min-width: 520px) {
    article {
	margin-left: 12.5%;
	margin-right: 12.5%;
    }
    ul, .abstract {
	margin-left: 12.5%;
	margin-right: 12.5%;
    }
    article>ul {
	padding-left: 3.125%;
    }
    li>ul {
	padding-left: 0;
    }

    .chapter-title {
	margin-left: 12.5%;
	margin-right: 12.5%;
	padding-left: 6.25%;
    }
}
"""


def new_note():
    path, summary = read_info()
    generate_dir(path)
    generate_summary(path+"/md/SUMMARY.toml", summary)
    



def read_info():
    summary = {}
    
    print("directory name: ", end="")
    directory = input().strip()
    path = "./{}".format(directory)
    
    print("note title: ", end="")
    summary["title"] = input().strip()
    
    print("author name: ", end="")
    summary["author"] = input().strip()

    summary["date"] = datetime.datetime.today().strftime("%Y-%m-%d")

    return [ path, summary ]


def generate_dir(path):
    os.mkdir(path)
    os.mkdir(path+"/md")
    os.mkdir(path+"/css")
    os.mkdir(path+"/html")

    with open(path+"/css/style.css", "w") as f:
        f.write(style)
    with open(path+"/css/index.css", "w") as f:
        f.write(index)


def generate_summary(fp, summary):
    with open(fp, "w", encoding="utf-8") as f:
        f.write('''title = "{}"
author = "{}"
date = "{}"

abstract = ""

# If it is a single-chapter document, use this "main" field.
# If not, remove this "main" field and use "chapter" field.
main = []

appendix = []

ref = []

# If there is the "main" field, this "chapter" field is ignored.
# So to generate a chaptered note, remove "main" field.
[[chapter]]
name = ""
files = []
'''.format(summary["title"], summary["author"], summary["date"]))



if __name__ == "__main__":
    new_note()

