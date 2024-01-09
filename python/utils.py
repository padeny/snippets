import csv
import os
import re
import sys
import pdb
import uuid
from datetime import datetime

import pypinyin
import tailhead


class ForkedPdb(pdb.Pdb):
    """
    多进程下调试代码, 用法与pdb相似
    import ForkedPdb;ForkedPdb().set_trace()
    """
    def interaction(self, *args, **kwargs):
        _stdin = sys.stdin
        try:
            sys.stdin = open('/dev/stdin')
            pdb.Pdb.interaction(self, *args, **kwargs)
        finally:
            sys.stdin = _stdin


def roll_save_file(file_path, max_row_num=50000, retain_row_num=5000):
    "保持一个文件最大多少行, 超出从前面删除一部分"
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r') as fp:
        lines = fp.readlines()
        if len(lines) > max_row_num:
            with open(file_path, 'w') as fp:
                fp.writelines(lines[-retain_row_num:])


def to_csv(path, row):
    with open(path, "a+") as f:
        writecsv = csv.writer(f, lineterminator=os.linesep)
        writecsv.writerow(row)


# https://thispointer.com/python-get-last-n-lines-of-a-text-file-like-tail-command/
# https://github.com/GreatFruitOmsk/tailhead
def get_last_n_lines(file_name, n=1):
    if not os.path.exists(file_name):
        return []
    with open(file_name, "rb") as f:
        list_of_lines = tailhead.tail(f, n)
        return [line.decode() for line in list_of_lines]


# https://stackoverflow.com/questions/845058/how-to-get-line-count-of-a-large-file-cheaply-in-python/68385697#68385697
def get_line_count(file_name):
    if not os.path.exists(file_name):
        return 0

    def _make_gen(reader):
        while True:
            b = reader(2 ** 16)
            if not b:
                break
            yield b
    with open(file_name, "rb") as f:
        count = sum(buf.count(b"\n") for buf in _make_gen(f.raw.read))
    return count


def get_pinyin(a_unicode_str):
    """
    将unicode编码的中文字符串转为拼音, 支持多音字
    '中国人' --> 'zhong-guo-ren'
    '重庆人' --> 'chong-qing-ren

    文档参考: https://pypinyin.readthedocs.io/zh_CN/master/api.html
    """
    return pypinyin.slug(a_unicode_str)


def add_mac_addr_colon(s):
    return ':'.join([s[i: i + 2] for i, j in enumerate(s) if not (i % 2)])


def remove_mac_addr_colon(s):
    return s.replace(":", "")


def gen_base64_str(a):
    param_cmd = '''echo  '%s' | base64'''
    return os.popen(param_cmd % a).read().strip()


def mac_is_valid(mac_address):
    # check mac address format
    return bool(
        re.match(r'^[0-9a-f]{2}([-:])[0-9a-f]{2}(\1[0-9a-f]{2}){4}$',
                 mac_address))


def gen_random_unique_string(length=32):
    res = uuid.uuid4().hex
    if length > 32 or length < 1:
        return res
    else:
        return res[:length]


def ts2str(ts):
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
