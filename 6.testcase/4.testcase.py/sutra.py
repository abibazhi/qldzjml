# sutra.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class Sutra:
    number: int           # 编号：1, 2, ...
    title: str            # 经名：大般若波罗蜜多经
    author: str           # 译者：唐三藏法师玄奘奉诏译
    start_page: str       # 起始页码（原始字符串）
    end_page: str         # 结束页码（原始字符串）
    section: str          # 所属部类：大乘般若部、大乘宝积部...
