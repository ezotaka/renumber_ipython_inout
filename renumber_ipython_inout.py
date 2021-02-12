#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys


class Processor:
    """テキストに含まれるIPythonコンソールのIn、Outオブジェクトの添字番号の再割り当てを行うクラス。

        >>> p = Processor()
        >>> print(p.renumber('In [100]:'))
        In [1]:
        >>> print(p.renumber('In []:'))
        In [1]:
        >>> print(p.renumber('In [not number]:'))
        In [1]:
        >>> print(p.renumber('Out[100]:'))
        Out[0]:
        >>> print(p.renumber('Out[]:'))
        Out[0]:
        >>> print(p.renumber('Out[not number]:'))
        Out[0]:
        >>> print(p.renumber('In []: Out[]:'))
        In [1]: Out[1]:
        >>> print(p.renumber('In []: aaa\\nOut[]: bbb'))
        In [1]: aaa
        Out[1]: bbb
        >>> print(p.renumber('In []: In []: Out[]: In []: Out[]: Out[]:'))
        In [1]: In [2]: Out[2]: In [3]: Out[3]: Out[3]:
        >>> print(p.renumber(['In []:\\n', 'Out[]: In []:\\n', 'Out[]:']))
        In [1]:
        Out[1]: In [2]:
        Out[2]:
        >>> print(p.renumber('In [^]:'))
        In [1]:
        >>> print(p.renumber('In [^10]:'))
        In [10]:
        >>> print(p.renumber('In [^20aaa]:'))
        In [20]:
        >>> print(p.renumber('In []: In []: Out[]: In [^]: Out[]: Out[]:'))
        In [1]: In [2]: Out[2]: In [1]: Out[1]: Out[1]:
        >>> print(p.renumber('In [^20]: In []: Out[]: In [^30]: Out[]: Out[]:'))
        In [20]: In [21]: Out[21]: In [30]: Out[30]: Out[30]:
        >>> print(p.renumber('In [] In[]: In  []: Out[] Out []:'))
        In [] In[]: In  []: Out[] Out []:
        >>> p.renumber(1)
        Traceback (most recent call last):
        ...
        TypeError: 'int' object is not iterable
        >>> p.renumber([1, 2])
        Traceback (most recent call last):
        ...
        TypeError: expected string or bytes-like object
    """

    def __init__(self):
        self.result_buffer = ''
        self.current_number = 0

    def renumber(self, texts):
        """ テキストに含まれるIPythonコンソールのIn、Outオブジェクトの添字番号の再割り当てを行った文字列を返します。

        :param texts: 入力テキスト
        :return: 再割り当て結果のテキスト
        """

        self.result_buffer = ''
        self.current_number = 0

        if type(texts) is str:
            texts = [texts]

        for text in texts:
            if text:
                self.process_in(text)

        return self.result_buffer

    def process_in(self, text):
        # text内の最初のInを見つける
        match = re.search(r'In \[([^\]]*)\]:', text)
        if match:
            self.process_out(text[:match.start()])  # Inの前
            self.current_number += 1
            index = match.groups()[0]  # Inの添字番号部分
            self.result_buffer += self.get_renumbered_in(index)
            self.process_in(text[match.end():])  # Inの後ろ
        else:
            self.process_out(text)

    def process_out(self, text):
        split_texts = re.split(r'Out\[[^\]]*\]:', text)
        self.result_buffer += split_texts[0]
        for split_text in split_texts[1:]:
            self.result_buffer += f'Out[{self.current_number}]:'
            self.result_buffer += split_text

    def get_renumbered_in(self, index):
        """必要であれば添字番号を再初期化した'In [*]:'の文字列を返します

        >>> p = Processor()
        >>> p.current_number = 100
        >>> print(p.get_renumbered_in(''))
        In [100]:
        >>> print(p.get_renumbered_in('^'))  # 添字が^から始まって直後に正の整数がなければ1に初期化
        In [1]:
        >>> p.current_number = 100
        >>> print(p.get_renumbered_in(''))
        In [100]:
        >>> print(p.get_renumbered_in('^aaa'))  # 正の整数以外は無視
        In [1]:
        >>> p.current_number = 100
        >>> print(p.get_renumbered_in(''))
        In [100]:
        >>> print(p.get_renumbered_in('^-50'))  # 正の整数以外は無視
        In [1]:
        >>> print(p.get_renumbered_in('^10'))  # 添字が^から始まって直後に正の整数があればその整数に初期化
        In [10]:
        >>> print(p.get_renumbered_in('^20aaa'))  # 正の整数部分だけを見る
        In [20]:
        >>> print(p.get_renumbered_in('^30.4'))  # 正の整数部分だけを見る
        In [30]:
        >>> print(p.get_renumbered_in('   ^'))  # 先頭の空白は無視
        In [1]:
        >>> print(p.get_renumbered_in('    ^40'))  # 先頭に空白は無視
        In [40]:
        >>> print(p.get_renumbered_in('    _^'))
        In [40]:
        >>> print(p.get_renumbered_in(' 50^'))  # 順番が大事
        In [40]:

        :param index: テキスト中の添字番号部分
        :return: 添字番号を再初期化した'In [*]:'
        """

        match = re.match(r'^\s*(\^)(\d*).*', index)
        if match:
            tokens = match.groups()
            if tokens[0]:
                if tokens[1]:
                    self.current_number = int(tokens[1])
                else:
                    self.current_number = 1
        return f'In [{self.current_number}]:'


def _main():
    if len(sys.argv) == 1:
        try:
            result = Processor().renumber(iter(sys.stdin.readline, ''))
            print(result, end='')
        except KeyboardInterrupt:
            print()
    elif len(sys.argv) >= 2:
        for file in sys.argv[1:]:
            f = open(file, 'r')
            result = Processor().renumber(iter(f.readline, ''))
            print(result, end='')
            f.close()


if __name__ == '__main__':
    _main()
    #import doctest
    #doctest.testmod()
