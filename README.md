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
PATH の通ったディレクトリにこのファイルへの symlink を配置することをおすすめします.


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

`mandyczewski.py` を実行するとき, 同じフォルダに `SUMMARY.md` が存在することが仮定されます. 
なので前節で自動的に作成されたフォルダ `md` に移動します.

```
$ cd md
```

まずは単一の章からなる文書を作成しましょう. カレントディレクトリに任意の名前のマークダウンを作成します. 
ここでは `test1.md`, `test2.md` というふたつのマークダウンを作成したと仮定します.

ここで注意ですが, mandyczewski では各々のマークダウンファイルに __ちょうどひとつのセクション見出し__ が含まれることを前提としています.
そのようになっていない場合, HTML の生成に失敗したり, 表示が崩れる可能性があります.

さて, マークダウンを作成したら, 作成したファイル名を `SUMMARY.md` で指定する必要があります.
このファイルを開き, `main = []` という行を見つけたら次のように書き換えてください.

```toml
main = ["test1.md", "test2.md"]
```

そうしたら, `mandyczewski.py` を実行します. 万事うまくいけば, `../index.html` および `../html/test1.html`, 
`../html/test2.html` というファイルが作成されているはずなので, ブラウザで `../index.html` を開いてみてください.


## 数式番号の扱い

マークダウン文書中で, インライン数式は `$..$`, 別行立て数式は `$$..$$` という形で記述します.

すべての別行立て数式にはデフォルトで数式番号が振られます. 数式番号を振りたくない場合, 
数式の直後に `<nolabel/>` と記述してください.

```markdown
$$E = m c^2$$ <nolabel/>
```

一方, 数式番号を後から参照するためには, 数式に次のように名前をつけます.

```markdown
$E = \sqrt{ m^2 c^4 + p^2 c^2 }$$ <label id="special-relativity"/>
```

そして, 本文で数式番号を参照するためには次のようにします.

```markdown
相対論的な粒子の運動量とエネルギーは式 <ref ref="special-relativity"/> により関係する.
```

注意ですが, `<ref/>` タグの最後のスラッシュを忘れると変換に失敗します. 
また, 数式番号は異なるファイル内の数式に関しても参照することができます.


## 複数の章を持つ文書

複数の章を持つより大規模な文書を作成する場合, `SUMMARY.toml` の `main = []` という行を削除し, `[[chapter]]` という部分を使用します.
各章に対して同様のフィールドを用意し, 章名とその章に属するファイル名を指定します.

```toml
[[chapter]]
name = "宇宙膨張と Hubble 則"
files = [ "metric.md", "expansion.md", "causal.md", ]

[[chapter]]
name = "初期宇宙の熱史"
files = [ "thermo.md", "transfer.md", "bbn.md", "recombination.md", ]
```

