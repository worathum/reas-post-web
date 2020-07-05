from selenium import webdriver
from urllib.parse import unquote
import sys
import time
from .lib_httprequest import *
import os
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os.path
from urllib import parse
import re
import json
import datetime
import random



httprequestObj = lib_httprequest()
with open("./static/ips.txt",'r') as f:
    allips = f.read()
ips = allips.split('\n')

username = ips[random.randint(0,len(ips)-2)].split(":")[2]
password = 'v1y3mbh26qk9'
port = 22225
super_proxy_url = ('http://%s:%s@zproxy.lum-superproxy.io:%d' %
        (username, password, port))

proxy_handler = {
    'http': super_proxy_url,
    'https': super_proxy_url,
}

httprequestObj.session.proxies.update(proxy_handler)

with open("./static/novabizz.json") as f:
    provincedata = json.load(f)


class novabizz():

    name = 'novabizz'

    def __init__(self):

        try:
            import configs
        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.debug = 0
        self.debugresdata = 0
        self.parser = 'html.parser'


    def print_debug(self, msg):
        if(self.debug == 1):
            print(msg)
        return True

    def print_debug_data(self, data):
        if(self.debugdata == 1):
            print(data)
        return True

        if(self.debugdata == 1):
            print(data)
        return True

        return {
            "success": "true",
            "time_usage": time_end - time_start,
            "time_start": time_start,
            "time_end": time_end,
            "detail": ""
        }

    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        if 'name_th' not in postdata:
            return{
                "websitename":"novabizz",
                'success': 'false',
                'detail': 'Missing required field name_th',
                'ret': '',
               
            }
        if 'tel' not in postdata:
            return{
                'websitename':'novabizz',
                'success': 'false',
                'detail': 'Missing required field tel',
                'ret': '',
               
            }
        province_id = 0
        amphur_id = 0
        success = "true"
        detail = ""
        postdata['addr_province'] = "กรุงเทพ"
        postdata['addr_district'] = "พญาไท"
        add = postdata["addr_province"]
        for (key, value) in provincedata.items():
            if type(value) is str and postdata['addr_province'].strip() in value.strip():
                province_id = key
                break
        for (key, value) in provincedata[str(province_id)+"_province"].items():
            if postdata['addr_district'].strip() in value.strip():
                amphur_id = key
                break

        r = httprequestObj.http_get('https://www.novabizz.com/register.php')
        soup = BeautifulSoup(r.content, 'html5lib')
        save = soup.find('input', attrs={'id': 'save'})['value']
        prod_address = ""
        for add in  [postdata['addr_district'], postdata['addr_province']]:
            if add is not None:
                prod_address += add + ","
        prod_address = prod_address[:-1]
        if 'website' not in postdata:
            postdata['website']=" "
        datapost = dict(
            save=save,
            email=postdata['user'],
            repassword=postdata['pass'],
            password=postdata['pass'],
            name=postdata['name_th']+" "+postdata['surname_th'],
            address="",
            action='p-member-register.php',
            province=province_id,
            amphur=amphur_id,
            title=" ",
            website=postdata['website'],
            phone=postdata['tel'],
            zipcode='10400',
            description=" ",
            answer=7777,
            hiddenanswer=7777,
            accept=1
        )
        url_check = "https://www.novabizz.com/lib/checkuser.php"
        r = httprequestObj.http_post(url_check, data=datapost)
        # print(r.text)
        if r.text == "-1":
            success = "false"
            detail = "Failed Registration"
            time_end = datetime.datetime.utcnow()
            time_usage = time_end - time_start
            return {
                "websitename":"novabizz",
                "success": success,
                "start_time": str(time_start),
                "end_time": str(time_end),
                "detail": detail,
            }
        url_n = "https://www.novabizz.com/register.php"
        r = httprequestObj.http_post(url_n, data=datapost)
        data = r.text
        if data == '':
            success = "false"
        else:
            success = "true"
            detail = data

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            'ds_id': postdata['ds_id'],
            "websitename":"novabizz",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": "Registered",
        }

    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        email = postdata['user']
        passwd = postdata['pass']
        r = httprequestObj.http_get('https://www.novabizz.com/member.php')
        soup = BeautifulSoup(r.content, 'html5lib')
        save = soup.find('input', attrs={'name': 'save'})['value']
        success = "true"
        detail = ""

        datapost = {
            'action': 'login.php',
            'email': email,
            'password': passwd,
            'save': save
        }
        r = httprequestObj.http_post(
            'https://www.novabizz.com/member.php', data=datapost)
        data = r.text
        soup = BeautifulSoup(r.content, 'html5lib')
        save = soup.find('h3', attrs={'class': 'fail'})
        # print(save)
        if save != None:
            detail="Failed Login"
            success = "false"
        else:
            detail = "logged in"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename":"novabizz",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "ds_id": postdata['ds_id'],
        }
    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        post_id = postdata['post_id']
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]

        url_list = 'https://www.novabizz.com/manage-post.php'
        r = httprequestObj.http_get(url_list)
        soup = BeautifulSoup(r.content, 'html5lib')
        ahref = soup.findAll('a')
        post_id = ''
        storeI = ''
        for i in ahref:
            var = i['href']
            j = len('//www.novabizz.com/p')
            post_id = ''
            while j < len(var) and var[j] != '/':
                post_id += var[j]
                j += 1
            if post_id == postdata['post_id']:
                storeI = i
                break
        if storeI == '':    
            time_end = datetime.datetime.utcnow()
            time_usage = time_end - time_start
            return {
                "log_id": postdata['log_id'],
                "ds_id": postdata['ds_id'],
                "websitename":"novabizz",
                "success": "false",
                "start_time": str(time_start),
                "end_time": str(time_end),
                "detail": "wrong post id",
            }
        posturl="https://www.novabizz.com/manage-post.php?update="+postdata['post_id']
        r=httprequestObj.http_get(posturl)

        time_end = datetime.datetime.utcnow()
        return {
            "log_id": postdata['log_id'],
            "ds_id": postdata['ds_id'],
            "websitename": "novabizz",
            "success": "true",
            "time_usage": time_end - time_start,
            "time_start": time_start,
            "time_end": time_end,
            "detail": "",
            "post_id": post_id,
        }        


    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]

        url_list = 'https://www.novabizz.com/manage-post.php'
        r = httprequestObj.http_get(url_list)
        soup = BeautifulSoup(r.content, 'html5lib')
        ahref = soup.findAll('a')
        # print(ahref)
        # print()
        post_id = ''
        storeI = ''
        for i in ahref:
            # title=i['href'][:len("../property-"+str(postdata['post_id'])+"/")]
            var = i['href']
            j = len('//www.novabizz.com/p')
            post_id = ''
            while j < len(var) and var[j] != '/':
                post_id += var[j]
                j += 1
            # print(post_id)
            if post_id == postdata['post_id']:
                storeI = i
                break
        if storeI == '':    
            time_end = datetime.datetime.utcnow()
            time_usage = time_end - time_start
            return {
                "websitename":"novabizz",
                "log_id": postdata['log_id'],
                "ds_id": postdata['ds_id'],
                "post_id":postdata['post_id'],
                "success": "false",
                "start_time": str(time_start),
                "end_time": str(time_end),
                "detail": "wrong post id",
            }

        if success == "true":
            datapost = {
                'action': 'manage-property-not-sale.php',
                'delete': postdata['post_id'],
                'page': ""
            }
            r = httprequestObj.http_get(
                'https://www.novabizz.com/manage-post.php', params=datapost)
            data = r.text
            if data == '':
                success = "false"
            else:
                detail = "Deleted Post"
        else:
            success = "false"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename":"novabizz",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "log_id":postdata['log_id'],
            "ds_id": postdata['ds_id'],
            "post_id": postdata['post_id']
        }

    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        theurl = ""
        post_id = ""
        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        ashopname = test_login["detail"]
        r = httprequestObj.http_get('https://www.novabizz.com/post-add.php')
        soup = BeautifulSoup(r.content, 'html5lib')
        save = soup.find('input', attrs={'name': 'save'})['value']
        subcategory = {
            "2": "1432",
            "1": "1430",
            "3": "1432",
            "7": "1433",
            "5": "1434",
            "6": "1436",
            "8": "1435",  # resort
            "25": "1437",
            "9": "1438",
            "4": "1431",
            "10": "1437",
        }
       
        province_id = -1
        amphur_id = -1
        if 'addr_district' not in postdata:
            print("1")
            return{
                'websitename':'novabizz',
                'success': 'false',
                'detail': 'Missing required field district',
                'ret': '',
                'post_url': '',
                'post_id': ''
            }
        if 'addr_province' not in postdata:
            print("2")
            return{
                'websitename':'novabizz',
                'success': 'false',
                'detail': 'Missing required field province',
                'ret': '',
                'post_url': '',
                'post_id': ''
            }
        if postdata['addr_province']=='กรุงเทพมหานคร':
            postdata['addr_province']='กรุงเทพ'

        for (key, value) in provincedata.items():
            if type(value) is str and postdata['addr_province'].strip() in value.strip():
                province_id = key
                break

        if province_id == -1:
            print("3")
            return{
                'websitename':'novabizz',
                'success': 'false',
                'ret': "wrong province id",
                'post_url': "",
                'post_id': ""
            }
        postdata['addr_district']=postdata['addr_district'].replace(' ','')
        for (key, value) in provincedata[province_id+"_province"].items():
            if postdata['addr_district'].strip() in value.strip():
                amphur_id = key
                break

        if amphur_id == -1:
            print("4")
            return{
                'websitename':'novabizz',
                'success': 'false',
                'ret': "wrong amphur id",
                'post_url': "",
                'post_id': ""
            }

        if 'name' not in postdata:
            print("5")
            return{
                'websitename':'novabizz',
                'success': 'false',
                'ret': 'Missing required field name',
                'post_url': '',
                'post_id': ''
            }
        if 'mobile' not in postdata:
            print("6")
            return{
                'websitename':'novabizz',
                'success': 'false',
                'ret': 'Missing required field mobile',
                'post_url': '',
                'post_id': ''
            }
        if 'pass' not in postdata:
            print("7")
            return{
                'websitename':'novabizz',
                'success': 'false',
                'ret': 'Missing required field pass',
                'post_url': '',
                'post_id': ''
            }
        if 'user' not in postdata:
            print("8")
            return{
                'websitename':'novabizz',
                'success': 'false',
                'ret': 'Missing required field user',
                'post_url': '',
                'post_id': ''
            }
        if 'property_type' not in postdata:
            print("9")
            return{
                'websitename':'novabizz',
                'success': 'false',
                'ret': 'Missing required field property_type',
                'post_url': '',
                'post_id': ''
            }
        if 'listing_type' not in postdata:
            print("10")
            return{
                'websitename':'novabizz',
                'success': 'false',
                'ret': 'Missing required field listing_type',
                'post_url': '',
                'post_id': ''
            }
       
        if 'price_baht' not in postdata:
            print("11")
            return{
                'websitename':'novabizz',
                'success': 'false',
                'ret': 'Missing required field price',
                'post_url': '',
                'post_id': ''
            }
        if 'post_title_th' not in postdata:
            print("12")
            return{
                'websitename':'novabizz',
                'success': 'false',
                'ret': 'Missing required field title',
                'post_url': '',
                'post_id': ''
            }
        if 'post_description_th' not in postdata:
            print("13")
            return{
                'websitename':'novabizz',
                'success': 'false',
                'ret': 'Missing required field description',
                'post_url': '',
                'post_id': ''
            }
        if 'addr_soi' in postdata and postdata['addr_soi']!=None:
                pass
        else:
            postdata['addr_soi']=''
        if 'addr_road' in postdata and postdata['addr_soi']!=None:
                pass
        else:
            postdata['addr_road']=''
        prod_address = ""
        for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
            if add is not None or add=="" or add==" ":
                prod_address += add + ","
        prod_address = prod_address[:-1]
        postdata['address'] = prod_address
        if 'website' not in postdata or postdata['website']==None:
            postdata['website']=' '
        if success == "true":
            if postdata['listing_type'] == 'เช่า':
                postdata['listing_type'] = 'forrent'
            else:
                postdata['listing_type'] = 'sale'
            if 'website' not in postdata:
                postdata['website']=""
            # postdata['post_title_th']=postdata['post_title_th'].replace('%','')
            # postdata['post_title_th']=postdata['post_title_th'][:84]
            datapost = {
                'save': save,
                'email': postdata['user'],
                'category': '1009',
                'subcategory': subcategory[str(postdata['property_type'])],
                'type': 'business',
                'want': postdata['listing_type'],
                'status': '2hand',
                'duration': '',
                'city': province_id,
                'district': amphur_id,
                'name': postdata['post_title_th'],
                'price': postdata['price_baht'],
                'detail': postdata['post_description_th'],
                'maplat': postdata['geo_latitude'],
                'maplon': postdata['geo_longitude'],
                'mapzoom': '',
                'contact': postdata['name'],
                'hiddenemail': postdata['email'],
                'phone': postdata['mobile'],
                'address': prod_address,
                'amphur': 'พญาไท',
                'province': 'กรุงเทพ',
                'zipcode': '10400',
                'website': postdata['website'],
            }
            if len(postdata['post_images'])==0:
                postdata['post_images']=['imgtmp/default/white.png']
            
            arr = ["photo1", "photo2", "photo3", "photo4", "photo5", "photo6"]
            files = {}
            for i in range(len(postdata['post_images'])):
                datapost[arr[i]] = postdata['post_images'][i]
                files[arr[i]] = (postdata['post_images'][i], open(
                    postdata['post_images'][i], "rb"), "image/png")
                if i == 5:
                    break
            r = httprequestObj.http_post(
                'https://www.novabizz.com/post-add.php', data=datapost, files=files)

            data = r.text
            if data == '-1':
                post_url=""
                success = "False"
                print("14")
            else:
                list_url = 'https://www.novabizz.com/manage-post.php'
                r = httprequestObj.http_get(list_url)
                soup = BeautifulSoup(r.content, 'html5lib')
                spancode=soup.find('span',attrs={'class':'code'}).text
                i=len('รหัส ')
                post_id = ''
                
                while i<len(spancode):
                    post_id += spancode[i]
                    i += 1
                ahref = soup.findAll('a')
                pos_id = ''
                storeI = ''
                for i in ahref:
                    var = i['href']
                    j = len('//www.novabizz.com/p')
                    pos_id = ''
                    while j < len(var) and var[j] != '/':
                        pos_id += var[j]
                        j += 1
                    # print(post_id)
                    if pos_id == post_id:
                        storeI = i
                        break
                print(storeI['href'])
                post_url=storeI['href'][2:]
                # post_url = 'https://www.novabizz.com/p' + post_id+"/"+ postdata['post_title_th'].replace(' ','-') + '.html'
                print("16")

        else:
            post_url=""
            print("15")
            success = "False"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            'websitename':'novabizz',
            "success": success,
            "start_time": str(time_start),
            "ds_id": postdata['ds_id'],
            "end_time": str(time_end),
            "post_url": post_url,
            "post_id": post_id,
        }

    def search_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_url = ""
        post_id = ""
        post_modify_time = ""
        post_view = ""
        post_found = "false"

        if success == "true":
            post_title = postdata['post_title_th']
            # exists, authenticityToken, post_title = self.check_post(post_id)
            x=['1','2','3','4','5','6','7','8','9','10']
            for i in x:
                url = "https://www.novabizz.com/manage-post.php?page="+i    
                r = httprequestObj.http_get(url)
                exists = False
                soup = BeautifulSoup(r.content, 'lxml')

                entry = soup.find('div', attrs={'class':'postlist'})
                for title_row in entry.find_all('ul',{'class':'lileft'}):
                    if title_row is None:
                        continue
                    title = title_row.find('a')
                    # print(title)
                    # print(title['href'][27:47])
                    # title_1=title['href'][27:47]
                    if title is None:
                        continue                    
                    if post_title == title['href'][27:47]:
                        exists = True
                        post_id = title['href'][20:26]
                        post_url = "http://"+title['href'][2:]
                        post_modify_time = title_row.find('li', attrs={'class':'date'}).text[7:-14]
                        post_view = title_row.find('span', attrs={'class':'pageview'}).text[7:]
                        post_found = "true"
                        detail = "post found successfully"
                        break
                if exists:
                    break                    
            if not exists:
                success = "false"
                detail = "No post found with given title."

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": "novabizz",
            "ds_id":postdata['ds_id'],
            "log_id": 1,
            "post_id": post_id,
            "post_modify_time": post_modify_time,
            "post_view": post_view,
            "post_url": post_url,
            "post_found": post_found
        } 



    def edit_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        subcategory = {
            "2": "1432",
            "1": "1430",
            "3": "1432",
            "7": "1433",
            "5": "1434",
            "6": "1436",
            "8": "1435",  # resort
            "25": "1437",
            "9": "1438",
            "4": "1431",
            "10": "1437",
        }
        try:
            postdata['cate_id'] = subcategory[str(postdata['property_type'])]
        except:
            return{
                'websitename':'novabizz',
                'success': 'false',
                'detail': 'wrong propertytype',
                "ds_id": postdata['ds_id'],
                "log_id": postdata['log_id'],
                'ret': '',
                'post_url': '',
                'post_id': ''
            }
        province_id = -1
        amphur_id = -1
        if 'addr_district' not in postdata:
            return{
                'websitename':'novabizz',
                'success': 'false',
                'detail': 'Missing required field district',
                "ds_id": postdata['ds_id'],
                "log_id": postdata['log_id'],
                'ret': '',
                'post_url': '',
                'post_id': ''
            }
        if 'addr_province' not in postdata:
            return{
                'websitename':'novabizz',
                'success': 'false',
                'detail': 'Missing required field province',
                "ds_id": postdata['ds_id'],
                "log_id": postdata['log_id'],
                'ret': '',
                'post_url': '',
                'post_id': ''
            }
        if postdata['addr_province']=='กรุงเทพมหานคร':
            postdata['addr_province']='กรุงเทพ'
        
        for (key, value) in provincedata.items():
            if type(value) is str and postdata['addr_province'].strip() in value.strip() and value.strip() in postdata['addr_province'].strip():
                province_id = key
                break

        if province_id == -1:
            return{
                'websitename':'novabizz',
                'success': 'false',
                'ret': "provinceid",
                "ds_id": postdata['ds_id'],
                "log_id": postdata['log_id'],
                'post_url': "",
                'post_id': ""
            }

        for (key, value) in provincedata[province_id+"_province"].items():
            if postdata['addr_district'].strip() in value.strip():
                amphur_id = key
                break

        if amphur_id == -1:
            return{
                'websitename':'novabizz',
                'success': 'false',
                'ret': "amphurid",
                "ds_id":postdata['ds_id'],
                "log_id":postdata['log_id'],
                'post_url': "",
                'post_id': ""
            }
        test_login = self.test_login(postdata)
        success = test_login["success"]
        ashopname = test_login["detail"]

        url_list = 'https://www.novabizz.com/manage-post.php'
        r = httprequestObj.http_get(url_list)
        soup = BeautifulSoup(r.content, 'html5lib')
        ahref = soup.findAll('a')
        # print(ahref)
        # print()
        post_id = ''
        storeI = ''
        for i in ahref:
            # title=i['href'][:len("../property-"+str(postdata['post_id'])+"/")]
            var = i['href']
            j = len('//www.novabizz.com/p')
            post_id = ''
            while j < len(var) and var[j] != '/':
                post_id += var[j]
                j += 1
            # print(post_id)
            if post_id == postdata['post_id']:
                storeI = i
                break
        if storeI == '':
            return{
                'websitename':'novabizz',
                'success': 'false',
                'ret': " Does not exist",
                "ds_id": postdata['ds_id'],
                "log_id": postdata['log_id'],
                'post_url': "",
                'post_id': ""
            }

        post_id = ""
        detail = ""
        post_id = ""
        detail = ""

        if 'name' not in postdata:
            return{
                'websitename':'novabizz',
                'success': 'false',
                'detail': 'Missing required field name',
                "ds_id": postdata['ds_id'],
                "log_id": postdata['log_id'],
                'ret': '',
                'post_url': '',
                'post_id': ''
            }
        if 'mobile' not in postdata:
            return{
                'websitename':'novabizz',
                'success': 'false',
                'detail': 'Missing required field mobile',
                "ds_id": postdata['ds_id'],
                "log_id": postdata['log_id'],
                'ret': '',
                'post_url': '',
                'post_id': ''
            }
        if 'pass' not in postdata:
            return{
                'websitename':'novabizz',
                'success': 'false',
                'detail': 'Missing required field password',
                "ds_id": postdata['ds_id'],
                "log_id": postdata['log_id'],
                'ret': '',
                'post_url': '',
                'post_id': ''
            }
        if 'user' not in postdata:
            return{
                'websitename':'novabizz',
                'success': 'false',
                'detail': 'Missing required field user',
                "ds_id": postdata['ds_id'],
                "log_id": postdata['log_id'],
                'ret': '',
                'post_url': '',
                'post_id': ''
            }
        if 'property_type' not in postdata:
            return{
                'websitename':'novabizz',
                'success': 'false',
                'detail': 'Missing required field property type',
                "ds_id": postdata['ds_id'],
                "log_id": postdata['log_id'],
                'ret': '',
                'post_url': '',
                'post_id': ''
            }
        if 'listing_type' not in postdata:
            return{
                'websitename':'novabizz',
                'success': 'false',
                'detail': 'Missing required field',
                "ds_id": postdata['ds_id'],
                "log_id": postdata['log_id'],
                'ret': '',
                'post_url': '',
                'post_id': ''
            }
        # if 'duration' not in postdata:
        #     return{
        #         'websitename':'novabizz',
        #         'success': 'false',
        #         'detail': 'Missing required field duration',
        #         'ret': '',
        #         'post_url': '',
        #         'post_id': ''
        #     }
        if 'price_baht' not in postdata:
            return{
                'websitename':'novabizz',
                'success': 'false',
                'detail': 'Missing required field price',
                "ds_id": postdata['ds_id'],
                "log_id": postdata['log_id'],
                'ret': '',
                'post_url': '',
                'post_id': ''
            }
        if 'post_title_th' not in postdata:
            return{
                'websitename':'novabizz',
                'success': 'false',
                'detail': 'Missing required field title',
                "ds_id": postdata['ds_id'],
                "log_id": postdata['log_id'],
                'ret': '',
                'post_url': '',
                'post_id': ''
            }
        if 'post_description_th' not in postdata:
            return{
                'websitename':'novabizz',
                'success': 'false',
                'detail': 'Missing required field description',
                "ds_id": postdata['ds_id'],
                "log_id": postdata['log_id'],
                'ret': '',
                'post_url': '',
                'post_id': ''
            }
        prod_address = ""
        for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
            if add is not None or add=="" or add==" ":
                prod_address += add + ","
        prod_address = prod_address[:-1]
        postdata['address'] = prod_address
        url_n = 'https://www.novabizz.com/post-edit.php?id='
        url_n += str(postdata['post_id'])
        r = httprequestObj.http_get(url_n)
        soup = BeautifulSoup(r.content, 'html5lib')
        save = soup.find('input', attrs={'name': 'save'})['value']
        if success == "true":

            if postdata['listing_type'] == 'เช่า':
                postdata['listing_type'] = 'forrent'
            else:
                postdata['listing_type'] = 'sale'
            if 'website' not in postdata:
                postdata['website']=""
            datapost = {
                'save': save,
                'email': postdata['user'],
                'category': '1009',
                'subcategory': subcategory[str(postdata['property_type'])],
                'type': 'business',
                'want': postdata['listing_type'],
                'status': '2hand',
                'duration': '',
                'city': province_id,
                'district': amphur_id,
                'name': postdata['post_title_th'],
                'price': postdata['price_baht'],
                'detail': postdata['post_description_th'],
                'maplat': postdata['geo_latitude'],
                'maplon': postdata['geo_longitude'],
                'mapzoom': '',
                'contact': postdata['name'],
                'hiddenemail': postdata['user'],
                'phone': postdata['mobile'],
                'address': prod_address,
                'amphur': 'พญาไท',
                'province': 'กรุงเทพ',
                'zipcode': '10400',
                'website': postdata['website'],
            }
            arr = ["photo1", "photo2", "photo3", "photo4", "photo5", "photo6"]
            files = {}
            for i in range(len(postdata['post_images'])):
                datapost[arr[i]] = postdata['post_images'][i]
                files[arr[i]] = (postdata['post_images'][i], open(
                    postdata['post_images'][i], "rb"), "image/png")
                if i == 4:
                    break
            r = httprequestObj.http_post(
                url_n, data=datapost, files=files)
            success = "true"
        else:
            success = "false"
            print("False")

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            'websitename':'novabizz',
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": postdata['ds_id'],
            "post_id": postdata['post_id'],
            "log_id": postdata['log_id'],
            "detail": "Edited",
        }


# obj = novabizz()
# datapost = {
#     'email': '1234567@gmail.com',
#     'subcategory': '3',
#     'duration': '60',
#     'name': 'dafsdfa',
#     'price': '523',
#     'detail': '5234534dfgfsgsdfgsdfgsdfgsd',
#     "geo_latitude": "13.786862",
#     "geo_longitude": "100.757815",
#     'contact': '52452452',
#     'phone': '5243523',
#     "addr_province": "จังหวัด",
#     "addr_district": "เขต",
#     "addr_sub_district": "ตำบล แขวง",
#     "addr_road": "ถนน",
#     "addr_soi": "ซอย",
#     "addr_near_by": "สถานที่ใกล้เคียง",
#     'website': 'http://sdas.com',
# }
# r=obj.test_login({'user':'temp@gmail.com','pass':'12345678'})
# print(r)
# postdata = dict(
#     email="1234567@gmail.com",
#     password="12345678",
#     name="1234",
#     address="1234",
#     addr_province="กาฬสินธุ์",
#     addr_district="กระบ",
#     title="1234",
#     website="http://1234.com",
#     phone="1234",
#     zipcode="1234",
#     description="1234"
# )
# # obj.register_user(postdata)
# postdata = dict(
#     email='1234567@gmail.com',
#     category='1009',
#     subcategory='6',
#     type='business',
#     want='sale',
#     status='new',
#     duration='60',
#     addr_province='กระบี่',
#     addr_district='อำเภอเกาะลันตา',
#     post_title_en='AAAAVAAbsgdABhhuuAABafsdfas',
#     name='12345678',
#     price='133422',
#     detail='fasdddddddddddddfffff',
#     maplat='',
#     maplon='',
#     mapzoom='',
#     contact='12432',
#     phone='1234',
#     address='1234',
#     amphur='อำเภอคลองใหญ่',
#     province='ตราด',
#     zipcode='1234',
#     website='http://wen344.com',
#     password='12345678',
#     post_images=['download.png'],
# )
# # r=obj.create_post(postdata)
# # print(r)
# postdata = dict(
#     user='parzodupso@yevme.com',
#     post_id='554796',
# )
# postdata['pass']='123456aa9'
# obj.boost_post(postdata)
# # obj.modify_post(postdata)
# obj.delete_post(postdata)
