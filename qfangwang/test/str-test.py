# -*- coding:utf-8 -*-
b = []
b.append(0xd6)
b.append(0xd0)
b.append(0xb9)
b.append(0xfa)
c= bytearray(b)
print(c.decode('gbk'))