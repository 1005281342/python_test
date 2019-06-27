# pip3 install attrs cattrs
from attr import attrs, attrib

"""
库名：attrs

导入包名：attr

修饰类：s 或 attributes 或 attrs

定义属性：ib 或 attr 或 attrib
"""


@attrs
class Color(object):
    r = attrib(type=int, default=0)
    g = attrib(type=int, default=0)
    b = attrib(type=int, default=0)


if __name__ == '__main__':
    color = Color(255, 255, 255)
    print(color)
