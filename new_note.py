#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import datetime


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

