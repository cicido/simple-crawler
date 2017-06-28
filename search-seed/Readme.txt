2017-6-28
这个程序主要通过百度百科的全局搜索功能,来获取百科词条种子.
由于是全局搜索,我们可以丢入任意词或非词模式,来获取百科词条种子.

1. search_seed_manager.py是主程序,用于分发种子与去重,启动时需要提供一个文件名参数,
该文件包含当前已完成爬取的种子
2. search_seed_worker.py是用于解析html,保留解析结果,并生成新的种子发送给主程序.
3. add_seed_from_file.py从文件中向主程序添加种子,需要提供一个文件名参数,该文件
中包含需要爬取的种子.
执行流程：
i. python search_seed_manager.py <complete-seed.txt>
ii. python search_seed_worker.py
iii.python add_seed_from_file.py <unfinish-word.txt>
第三步比较重要, 必须丢入一些种子让程序能运行下去
