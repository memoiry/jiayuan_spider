# -*- coding:utf8 -*-
import urllib2
import urllib
import cookielib
from lxml import etree
import re
import sys
import time
import cProfile
import pstats 
import tqdm 
from multiprocessing.dummy import Pool as ThreadPool #多线程  
import argparse  
import os

reload(sys)
sys.setdefaultencoding('utf8')

def crawl(page):
    global img_count
    try:
        pbar.update(1)
        search_url = url + str(page)
        op=opener.open(search_url)
    #读取页面源码
        data= op.read()


#print data
        exist_pattern = re.compile("<dd class='last'>(.+?)</dd>")
        exits = re.search(exist_pattern, data)
    #print data
        if not exits is None:
        #    print "Error pages, continue"
            return
        img_pattern = re.compile('href="(.+?)"><img class="img_absolute"')
        img_base_url = re.search(img_pattern, data).group(1)
    #print img_base_url
        op_img = opener.open(img_base_url, data)
    #读取页面源码
        img_data = op_img.read()
    #print img_data
        imgs_url = []
        #print img_data
    #print img_data

    #第一张图片
        base_img_url_pattern = re.compile('<td align="center"><img src="(.+?)"></td>')
        base_img_url = re.search(base_img_url_pattern, img_data)
        #print base_img_url
        if base_img_url is None:
            print "Do not have images"
            return 

    #其他图片
        other_img_url_pattern = re.compile('<img style="max-width:675px;" src="(.+?)" alt=""/>')
        other_img_url = re.findall(other_img_url_pattern, img_data)
        if other_img_url is None:
            other_img_url = []
        other_img_url.append(base_img_url.group(1))

    #排除默认图片
        if default_female_img in other_img_url:
            other_img_url.remove(default_female_img)

        if default_male_img in other_img_url:
            other_img_url.remove(default_male_img)

        if default_male_star_img in other_img_url or default_male_key_img in other_img_url or default_female_key_img in other_img_url: 
            return 

        if other_img_url == [] or len(other_img_url) > 20:
            print "Only have default imgs"
            return 

    #开始爬虫
        count = 0
        for img_url in other_img_url:
            #print img_url
            urllib.urlretrieve(img_url, 'imgs/%d_%d.jpg' % (page, count))
            count = count +1
        print "crawing user id: %s at speed %s /s" % (page,img_count/(time.time()-time_start))
        img_count = img_count + 1
        #pattern2 = re.compile('<li class="cur">.*>(.+?)</a></li>')
        #XB = re.search(pattern2, data)  # 资料，查询性别
        #pattern = re.compile('<h6 class="member_name">(.+?)</h6>', re.S)
        #NL = re.search(pattern, data)  # 年龄和居住地
        #selector = etree.HTML(data)
        #ID = selector.xpath('//div[@class="member_info_r yh"]/h4/span/text()')[0].replace('ID:', '')  # id
        #userInfo = u' '
        #userInfo = userInfo + XB.group(1) + u':' + NL.group(1) + u',ID：' + ID
    # 获取基本资料
        #list = selector.xpath('//ul[@class="member_info_list fn-clear"]/li/div[@class="fl pr"]/em/text()')
        #for each in list:
        # print each
        #    userInfo = userInfo + u',' + each
    # 获取择偶要求
        #list = selector.xpath('//ul[@class="js_list fn-clear"]/li/div/text()')
        #for each in list:
        # print each
        #    userInfo = userInfo + u',' + each
    #print(userInfo)
    except Exception as e:
        print e
        pass


  
parser = argparse.ArgumentParser()  
parser.add_argument("--user", help="User name")  
parser.add_argument("--password", help="Password")  
parser.add_argument("--cookie", help="User cookie")  
parser.add_argument("--order", help="Task order", type = int)  
parser.add_argument("--thread", help="Task order", type = int, default = 30)  


args = parser.parse_args()  

default_male_img = "http://images1.jyimg.com/w4/profile/i/photo_invite_m_bp.jpg"
default_female_img = "http://images1.jyimg.com/w4/profile/i/photo_invite_f_bp.jpg"
default_male_star_img = "http://images1.jyimg.com/w4/global/i/xjhykj_m_bp.jpg"
default_male_key_img = "http://images1.jyimg.com/w4/global/i/xyaqmm_m_bp.jpg"
default_female_key_img = "http://images1.jyimg.com/w4/global/i/xjhykj_f_bp.jpg"
img_count = 1

url ='http://www.jiayuan.com/'
page = 20000000
id_list = []
#f = open('uid_f_20.txt', 'r')
#lines = f.readlines()

#for line in lines:
#    id_list.append(int(line.replace("\n", "")))

#登陆页面，可以通过抓包工具分析获得，如fiddler，wireshark
login_page = "https://passport.jiayuan.com/dologin.php?pre_url=http://usercp.jiayuan.com/"
#获得一个cookieJar实例
img_base = "http://photo.jiayuan.com/showphoto.php?uid_hash="

print args.cookie
cj = cookielib.CookieJar()
#cookieJar作为参数，获得一个opener的实例
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
#伪装成一个正常的浏览器，避免有些web服务器拒绝访问。
if args.cookie is None:
    opener.addheaders = [('User-agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5)')]
else:
    cookie = args.cookie
    opener.addheaders = [('User-agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5)'), ('Cookie', cookie)]

if not os.path.isdir("imgs"):
    os.mkdir("imgs")

#生成Post数据，含有登陆用户名密码。
data = urllib.urlencode({'name':args.user,
'password':args.password})

#以post的方法访问登陆页面，访问之后cookieJar会自定保存cookie
opener.open(login_page,data)

#以带cookie的方式访问页面
#print data
# print data
start_num = 20000000 + (args.order -1) * 1000000
end_num = 20000000 + (args.order) * 1000000
id_list = range(start_num, end_num)

downloaded_img = os.listdir("imgs")
for i in range(len(downloaded_img)):
    downloaded_img[i] = int(downloaded_img[i].split("_")[0])

downloaded_img = filter(lambda x:(x < end_num and x >= start_num), downloaded_img)
#tqbar = tqdm.tqdm(total = len(downloaded_img))

id_list = list(set(id_list) - set(downloaded_img))
#id_list = (x for x in range(start_num, end_num) if x not in downloaded_img)
    
print "%s imgs left" % len(id_list)
pbar = tqdm.tqdm(total = len(id_list))
time_start = time.time()
pool = ThreadPool(args.thread)
pool.map(crawl, id_list)
pool.join()
pbar.close()
