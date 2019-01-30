# 生成した HTML ファイル等を指定フォルダへコピーする

import os
import sys
import glob
import toml
import shutil

def read_summary():
    # 文書データの読み込み
    if not os.path.exists("SUMMARY.toml"):
        print("Error: can not find `SUMMARY.toml` in this directory.")
        sys.exit()
    with open("SUMMARY.toml","r") as f:
        summary = toml.load(f)
    return summary


def deploy():
    summary = read_summary()
    if not "deploy" in summary:
        print('Error: The "deploy" field is not found in "SUMMARY.md"!')
        sys.exit()
        
    target = summary["deploy"]

    if not os.path.exists(target+"/html"):
        os.mkdir(target+"/html")
    if not os.path.exists(target+"/css"):
        os.mkdir(target+"/css")
    
    shutil.copyfile("../index.html", target+"/index.html")
    for fp in glob.glob("../html/*"):
        if os.path.isfile(fp):
            shutil.copyfile( fp, target+"/html/{}".format(os.path.basename(fp)))
    for fp in glob.glob("../css/*"):
        if os.path.isfile(fp):
            shutil.copyfile( fp, target+"/css/{}".format(os.path.basename(fp)))
            
    if os.path.exists("../fig"):
        if not os.path.exists(target+"/fig"):
            os.mkdir(target+"/fig")
        for fp in glob.glob("../fig/*.svg"):
            shutil.copyfile( fp, target+"/fig/{}".format(os.path.basename(fp)))
        for fp in glob.glob("../fig/*.mp4"):
            shutil.copyfile( fp, target+"/fig/{}".format(os.path.basename(fp)))

