# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import bs4,codecs

html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

soup = BeautifulSoup(html, 'lxml')
# print soup.prettify()
print soup.title
print soup.head
print soup.a
print soup.p
print type(soup.a)

print soup.name
print soup.head.name

print soup.p.attrs

print soup.p.attrs['class']

print soup.p.string
print type(soup.p.string)

# Comment 对象是一个特殊类型的 NavigableString 对象，
# 其实输出的内容仍然不包括注释符号，但是如果不好好处理它，
# 可能会对我们的文本处理造成意想不到的麻烦
print soup.a.string
print type(soup.a.string)
if type(soup.a.string) == bs4.element.Comment:
    print soup.a.string


print '*'*20 + "遍历" + '*'*20
print soup.head.contents
for child in soup.body.children:
    print child
print '-'*40
for child in soup.descendants:
    print child

ori_content = ''
with codecs.open('test.html','r',encoding='utf-8') as rf:
    ori_content = rf.read()
    #print content
content = BeautifulSoup(ori_content,'lxml')
nav = content.find(id='dict_nav_list')
firstClass = []
for ele in nav.find_all('a'):
    #print ele.attrs.get('href')
    firstClass.append(ele.attrs.get('href').split("/")[-1])
print firstClass
