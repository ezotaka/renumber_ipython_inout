# renumber_ipython_inout.py
テキストに含まれるIPythonコンソールIn、Outオブジェクトのインデックスの再割り当てを行うスクリプトです。

## このスクリプトの使い道
IPythonコンソールの実行結果のコピペを、きれいにして共有したいときなどにお使いください。

例えば、以下のようにインデックスがバラバラなテキストが、

```python
In [2]: index = '  ^100hoge'

In [3]: import re

In [13]: match = re.match(r'^\s*(\^)(\d*).*', index)

In [29]: match.groups()
Out[29]: ('^', '100')
```

スクリプト適用後には以下のようになります。

```python
In [1]: index = '  ^100hoge'

In [2]: import re

In [3]: match = re.match(r'^\s*(\^)(\d*).*', index)

In [4]: match.groups()
Out[4]: ('^', '100')

```

## 使い方
[renumber_ipython_inout.py](https://raw.githubusercontent.com/ezotaka/renumber_ipython_inout/main/renumber_ipython_inout.py)をダウンロードして実行してください。

引数にファイル名を与えるか、標準入力からテキストを入力すると、変換結果を標準出力します。

```
$ python renumber_ipython_inout.py filename

もしくは

$ cat file_name | python renumber_ipython_inout.py 
```

## 仕様
* テキスト中に``In [.*]:``もしくは``Out[.*]:``を見つけたら、インデックス部分の文字列を適切な数値に置換します。
* それ以外の文字列の置換は行いません。
* テキストの先頭から順に、1からの連番になります。
* ``In [^]:``と書くことで、任意の箇所で1に初期化することもできます。
* ``In [^正の整数]:``と書くことで、任意の箇所で任意の数値に初期化することもできます。

## 実行例
スクリプト適用前

```python
In [10]:

In []:  # 空でもいい
Out[何か]:  # 何でもいい

In [^]:  # 1に初期化される

In [40]:
Out[40]:

In [  ^100hoge]: # 先頭の空白や数値以外は無視して、100に初期化される
Out[50]:

# 先頭じゃなくても適用されるので注意 In []: Out[]:

In [60]:
```

スクリプト適用後

```python
In [1]:

In [2]:  # 空でもいい
Out[2]:  # 何でもいい

In [1]:  # 1に初期化される

In [2]:
Out[2]:

In [100]: # 先頭の空白や数値以外は無視して、100に初期化される
Out[100]:

# 先頭じゃなくても適用されるので注意 In [101]: Out[101]:

In [102]:
```
