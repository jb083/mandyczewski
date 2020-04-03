# mandyczewski

mandyczewski は数式を含むマークダウン文書を HTML に変換するシステムです.


# Install

## Prerequirements

pandoc がインストールされていてパスが通っていることが必要です. Debian/Ubuntu の場合

```shell
$ sudo apt install pandoc
```

です.

また Python3 が必要です (Python2 での動作は確認していません).
Python ライブラリ [lxml](https://pypi.org/project/lxml/) および [toml](https://pypi.org/project/toml/) を pip 等で事前にインストールしてください.

```shell
$ pip3 install lxml toml
```

## Install

本システムは Python スクリプトです. `git clone` によりスクリプトを配置してください.

```shell
$ git clone git@github.com:jb083/mandyczewski.git
```

`./mandyczewski.py` が実体です. このファイルを直接叩けるように PATH を通すか, 
PATH の通ったディレクトリに symlink を配置することをおすすめします.


# Usage

## 新規文書の作成

任意の作業ディレクトリで次のコマンドを実行してください.

```
$ mandyczweski.py new
```

すると対話形式で情報を入力するように促されるので, ディレクトリ名, 文書のタイトル, 著者を入力します.
完了すると入力した通りにディレクトリが作成され, その中に `css/`, `html/`, `md/` という 3 個のディレクトリが配置されます.
また, `md/SUMMARY.toml` というファイルが自動的に作成されます.

## マークダウンの作成

## 数式番号の扱い

