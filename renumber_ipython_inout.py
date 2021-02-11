#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""テキストに含まれるIPythonコンソールのIn、Outオブジェクトの添字番号の再割り当てを行って出力します。

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

import re
import sys

class Processor:
    def __init__(self):
        self.result_buffer = ''
        self.current_number = 0
        self.in_re = re.compile(r'In \[[^\]]*\]:')
        self.out_re = re.compile(r'Out\[[^\]]*\]:')

    def renumber(self, texts):
        self.result_buffer = ''
        self.current_number = 0

        if type(texts) is str:
            texts = [texts]

        for text in texts:
            if text:
                self.process_in(text)

        return self.result_buffer

    def process_in(self, text):
        split_texts = self.in_re.split(text)
        self.process_out(split_texts[0])
        for split_text in split_texts[1:]:
            self.current_number = self.current_number + 1
            self.result_buffer += f'In [{self.current_number}]:'
            self.process_out(split_text)

    def process_out(self, text):
        split_texts = self.out_re.split(text)
        self.result_buffer += split_texts[0]
        for split_text in split_texts[1:]:
            self.result_buffer += f'Out[{self.current_number}]:'
            self.result_buffer += split_text


def _main():
    if len(sys.argv) == 1:
        result = Processor().renumber(iter(sys.stdin.readline, ''))
        print(result, end='')
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
