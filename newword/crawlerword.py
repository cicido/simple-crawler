# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests, re, time
import codecs
from urllib import quote, unquote

'''
a = '/item/马云/6252'
print quote(a)
保存为三个文件:
1. 已完成爬取词:word-finished.txt
2. 未完成爬取词:word-unfinished.txt
3. 爬取结果: word-related.txt
'''
finished_file = 'word-finished.txt'
unfinished_file = 'word-unfinished.txt'
words_file = 'word-related2.txt'
finished_set = set()
unfinished_set = set()

with codecs.open(finished_file, 'r', 'utf-8') as f:
    finished_set.update([i.strip() for i in f.readlines() if len(i.strip()) != 0])

with codecs.open(unfinished_file, 'r', 'utf-8') as f:
    unfinished_set.update([i.strip() for i in f.readlines() if len(i.strip()) != 0])

tmp_unfinished_set = set()
#finished_set.update(unfinished_set)

fw = codecs.open(words_file, 'a', 'utf-8')
#fend = codecs.open(finished_file,'a', 'utf-8')

base_url = "http://baike.baidu.com/item/"
while True:
    num = 0
    for uword in unfinished_set:
        try:
            print uword
            url = base_url + quote(uword.encode('utf-8'))
            response = requests.get(url)
            content = BeautifulSoup(response.text.encode(response.encoding), 'lxml')

            relate_words = []
            for a in content.find_all('a'):
                if a.attrs.has_key('href'):
                    href = a.attrs['href']
                    if href.startswith('/item') and not href.endswith('fr=navbar') and not href.endswith('force=1'):
                        word = unquote(href.replace('/item/', '').replace('#viewPageContent', ''))
                        if type(word) == str:
                            word = word.decode('utf-8')
                        relate_words.append(word)
            #标记该词已处理，并记录到文件
            finished_set.add(uword)
            #fend.write(uword+'\n')

            # 保存页结item结果
            fw.write(uword + '\t')
            fw.write(','.join(relate_words) + '\n')
            if num == 10:
                num = 0
                #time.sleep(1)
                fw.flush()

            #保证tmp_unfinished_set有数据，且当set过大时，把数据存放在文件中
            if len(tmp_unfinished_set) < 100000:
                tmp_unfinished_set.update(set(relate_words) - finished_set)
            else:
                fstart = codecs.open(unfinished_file, 'a', 'utf-8')
                fstart.write('\n'.join(set(relate_words) - finished_set))
                fstart.write('\n')
                fstart.close()

        except Exception,e:
            print e.message

    unfinished_set = tmp_unfinished_set - finished_set
    tmp_unfinished_set = set()
    print "finished_set:", len(finished_set)
    print "unfinished_set:", len(unfinished_set)


fw.close()

'''
content = response.text.encode(response.encoding)

pattern = re.compile(">(.*?)<")
items = re.findall(pattern, content)
for item in items:
    if len(item) < 20 and len(item) > 1 and not item.startswith('&nbsp'):
        print item
'''
