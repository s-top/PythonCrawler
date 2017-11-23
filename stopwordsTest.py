#-*- coding: UTF-8 -*-
import pymysql
import jieba
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

stopwords = {}.fromkeys(['的', '附近'])
print stopwords
segs = jieba.cut('北京附近的租房', cut_all=False)
final = ''
for seg in segs:
    seg = seg.encode('utf-8')
    if seg not in stopwords:
            final += seg
print final