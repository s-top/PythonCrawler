#-*- coding: UTF-8 -*-
import pymysql
import jieba
import sys
from loadingData import *
import jieba.posseg as pseg
reload(sys)
sys.setdefaultencoding('utf-8')

# 创建停用词list
def stopwordslist(filepath):
    stopwords = {}.fromkeys([line.rstrip() for line in open(filepath)])
    return stopwords

# 创建连接
conn = pymysql.connect(host='127.0.0.1',user='root',password='123456',db='python',charset='utf8')
# 创建游标
cursor = conn.cursor()
sql="select id,name from taobao"
# 执行SQL，并返回收影响行数
data = cursor.execute(sql)
# 获取结果所有数据
result = cursor.fetchall()
# 提交
conn.commit()
# 关闭游标
cursor.close()
# 关闭连接
conn.close()
#去停用词
stopwords = stopwordslist('split-words/stopwords-CN.txt')

for index in range(data):
   # 1, 短裙百褶裙半身裙防走光裙裤伞裙a字裙裙子
   # print str(result[index][0]) + "," + result[index][1]
   id = result[index][0]
   name = result[index][1]
   text = ""
   seg_list = pseg.cut(result[index][1].strip())  # 默认是精确模式
   for word in seg_list :
      if word.word.strip() != "":
         if word.word.strip() not in stopwords:
            text = text + word.word + " "
   sql = "insert into split_words(id,name,split) values('%d','%s','%s')" %(id, name, text)
   data_Import(sql)
print("爬取完成，且数据已存入数据库")

