# -*- coding:utf-8 -*-
import codecs
import copy

def get_multi_layer(key,reslist):
    for i in reslist:
        i.append(key)
    if key not in layerMap:
        return reslist
    else:
        newlist = []
        for val in layerMap[key]:
            newlist.extend(get_multi_layer(val, reslist))
        return newlist

if __name__ == "__main__":
    layerMap = {}
    with codecs.open('data/tags-layer.txt') as fr:
        for tag in fr.readlines():
            tag = tag.split('\t')[0].split('->')
            layerMap.setdefault(tag[0], []).append(tag[1])
            #do not use follows
            #layerMap[tag[0]] = layerMap.setdefault(tag[0],[]).append(tag[-1])
        #print(layerMap)

    with codecs.open('data/multi-layer.txt','w','utf-8') as fw:
        for key in layerMap.keys():
            reslist = [[]]
            print(get_multi_layer(key,reslist))



