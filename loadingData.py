#-*- coding: UTF-8 -*-
#爬取taobao商品
import urllib2
import pymysql
import re

#打开网页，获取网页内容
def url_open(url):
    headers=("user-agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0")
    opener=urllib2.build_opener()
    opener.addheaders=[headers]
    urllib2.install_opener(opener)
    data=urllib2.urlopen(url).read().decode("utf-8","ignore")
    return data

#将数据存入mysql中
def data_Import(sql):
    conn=pymysql.connect(host='127.0.0.1',user='root',password='123456',db='python',charset='utf8')
    conn.query(sql)
    conn.commit()
    conn.close()

if __name__=='__main__':
    try:
        #定义要查询的商品关键词
        keywd="短裙"
        keywords=urllib2.quote(keywd)
        #定义要爬取的页数
        num=100
        id = 0
        for i in range(num):
            # url="https://s.taobao.com/search?q="+keywords+"&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.50862.201856-taobao-item.1&ie=utf8&bcoffset=4&ntoffset=4&p4ppushleft=1%2C48&s="+str(i*44)
            if i == 0:
                url = "https://s.taobao.com/search?q="+keywords+"&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20171113&ie=utf8"
            else:
                url = "https://s.taobao.com/search?q="+keywords+"&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20171113&ie=utf8&bcoffset=4&ntoffset=4&p4ppushleft=1%2C48&s="+str(i*44)
            data=url_open(url)
            #定义各个字段正则匹配规则
            # 商品图片
            img_pat='"pic_url":"(//.*?)"'
            # 商品名
            name_pat='"raw_title":"(.*?)"'
            # 店铺名
            nick_pat='"nick":"(.*?)"'
            # 价格
            price_pat='"view_price":"(.*?)"'
            # 邮费
            fee_pat='"view_fee":"(.*?)"'
            # 付款人数
            # sales_pat='"view_sales":"(.*?)"'
            # 评论数
            comment_pat='"comment_count":"(.*?)"'
            # 店铺所在地
            city_pat='"item_loc":"(.*?)"'
            #查找满足匹配规则的内容，并存在列表中
            imgL=re.compile(img_pat).findall(data)
            nameL=re.compile(name_pat).findall(data)
            nickL=re.compile(nick_pat).findall(data)
            priceL=re.compile(price_pat).findall(data)
            feeL=re.compile(fee_pat).findall(data)
            # salesL=re.compile(sales_pat).findall(data)
            commentL=re.compile(comment_pat).findall(data)
            cityL=re.compile(city_pat).findall(data)
            for j in range(len(nameL)):
                id = id + 1;
                img="http:"+imgL[j]#商品图片链接
                name=nameL[j]#商品名称
                nick=nickL[j]#淘宝店铺名称
                price=priceL[j]#商品价格
                fee=feeL[j]#运费
                # sales=salesL[j]#商品付款人数
                comment=commentL[j]#商品评论数，会存在为空值的情况
                if(comment==""):
                    comment=0
                city=cityL[j]#店铺所在城市
                print('正在爬取第'+str(i)+"页，第"+str(j)+"个商品信息...")
                sql="insert into taobao(id,name,price,fee,comment,city,nick) values('%d','%s','%s','%s','%s','%s','%s')" %(id,name,price,fee,comment,city,nick)
                data_Import(sql)
                print("爬取完成，且数据已存入数据库")
    except Exception as e:
        print(str(e))
        print("任务完成")