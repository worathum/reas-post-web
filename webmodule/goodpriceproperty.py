# -*- coding: utf-8 -*-
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
import os
from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
# from urlparse import urlparse
import re
import json
import datetime
import time
import sys
import urllib.request
from urllib.parse import unquote


httprequestObj = lib_httprequest()


with open("./static/ploychao_province.json") as f:
    provincedata = json.load(f)


class goodpriceproperty():

    name = 'goodpriceproperty'

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


    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        user = postdata['user']
        passwd = postdata['pass']
        company_name = ''
        name = postdata["name_th"]
        surname = postdata["surname_th"]
        add = 'กรุงเทพ'
        tel = postdata["tel"]
        email = postdata["user"]
        # start process
        success = "true"
        detail = ""
        for (key, value) in provincedata.items():
            # print("key",key,value)
            if type(value) is str and 'กรุงเทพ' in value.strip():
                province_id = key
                break

        for (key, value) in provincedata[province_id+"_province"].items():
            if 'พญาไท' in value.strip():
                amphur_id = key
                break
        datapost = dict(

            user=user,
            email=email,
            repass=passwd,
            name=name+" "+surname,
            shopname=company_name,
            action='save_register',
            province=province_id,
            amphur=amphur_id,
            website="",
            tel=tel,
            add=add

        )

        register_headers = {
            'Host': 'www.xn--42cf4b4c7ahl7albb1b.com',
            'Connection': 'keep-alive',
            'Content-Length': '36',
            'Cache-Control': 'max-age=0',
            'Origin': 'http://www.xn--42cf4b4c7ahl7albb1b.com',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Referer': 'http://www.xn--42cf4b4c7ahl7albb1b.com/member-condition.php',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
        }
        register_data = {
            'check': '1',
            'btLogin': 'Next | Next >>'
        }

        regist_url = 'http://www.xn--42cf4b4c7ahl7albb1b.com/register.php'
        with requests.Session() as s:
            r = s.post(regist_url, data=register_data, headers=headers)
        # print(r.content)
        soup = BeautifulSoup(r.content, 'html5lib')
        var = soup.find('input', attrs={'name': 'rands'})['value']


#             'Submit.x'= 49,
        # 'Submit.y'=10
        datapost['Submit.x'] = '49'
        datapost['Submit.y'] = '10'
        datapost['capcha'] = datapost['rands'] = var

        datapost['pass'] = datapost['repass'] = passwd
        # print(datapost)
        url_n = "http://www.xn--42cf4b4c7ahl7albb1b.com/p-register.php"
        with requests.Session() as s:
            r = s.post(url_n, data=datapost, headers=headers)
        # httprequestObj.http_post(url)
        # print(r.content)
        # print(r.text)

        data = r.text
        if data == '':
            success = "false"
        else:
            detail = data
        success="true"
        if data.find("alert")!=-1:
            success="false"

        # # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "websitename": "goodpriceproperty",
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,

        }

    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']

        success = "true"
        detail = ""

        datapost = {
            'action': 'login',
            'pass': passwd,
            'user': user,
            'Submit.x': '30',
            'Submit.y': '21'
        }
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8', 'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive', 'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'www.xn--42cf4b4c7ahl7albb1b.com', 'Origin': 'http://www.xn--42cf4b4c7ahl7albb1b.com',
            'Referer': 'http://www.xn--42cf4b4c7ahl7albb1b.com/index.php', 'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
        }
        r = httprequestObj.http_post(
            'http://www.xn--42cf4b4c7ahl7albb1b.com/login.php', data=datapost, headers=headers)

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
        }
        data = r.text

        if data.find("ขออภัยครับ") != -1:
            detail = "cannot login"
            success = "false"
        else:
            detail = "logged in"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "websitename": "goodpriceproperty",
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": self.websitename
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

        try:
            floor_area = postdata['floor_area']
        except:
            floor_area = ""

        getProdId = {'1': 4, '2': 1, '3': 2, '4': 3, '5': 6,
                     '6': 10, '7': 5, '8': 7, '9': 8, '10': 9}
        province_id=""
        amphur_id=""

        for (key, value) in provincedata.items():
            if type(value) is str and postdata['addr_province'].strip() in value.strip():
                province_id = key
                break
        if province_id=="":
            
            return{
                'success': 'false',
                'ret': "",
                'post_url': "",
                'post_id': ""
            }

        for (key, value) in provincedata[province_id+"_province"].items():
            if postdata['addr_district'].strip() in value.strip():
                amphur_id = key
                break

        if amphur_id=="":
            return{
                'success': 'false',
                'ret': "",
                'post_url': "",
                'post_id': ""
            }
        # no = 0
        # img_arr = {}
        # for i in range(len(postdata['post_img_url_lists'])):
        #     img_arr[i] = str(no)+".jpg"
        #     urllib.request.urlretrieve(
        #         postdata['post_img_url_lists'][i], str(no)+".jpg")
        #     no += 1


        prod_address = ""
        for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
            if add is not None:
                prod_address += add + ","
        prod_address = prod_address

        if success == "true":
            edit_url = "http://www.xn--42cf4b4c7ahl7albb1b.com/member/post-property.php"
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
            }

            with requests.Session() as s:
                r = httprequestObj.http_get_with_headers(
                    edit_url, headers=headers)

                # r=s.post(edit_url,,headers=register_headers)
            soup = BeautifulSoup(r.content, 'html5lib')
            var = soup.find('input', attrs={'name': 'rands'})['value']
            if len(var) == 0:
                return{
                    'success': 'false',
                    'ret': "",
                    'post_url': "",
                    'post_id': ""
                }

            datapost = {
                'class_type_id': '1',  # 1 for sell 2 for rent
                'cate_id': getProdId[postdata['property_type']],  # the property tye
                'action': 'saveproduct',
                'savetype': 'R',
                'title': postdata['post_title_th'],
                'project': postdata['project_name'],
                'detail': postdata['post_description_en'],
                'price': postdata['price_baht'],
                'product_unit[]': '',
                'product_warranty_price': '',
                'shipping_id': '',
                'add': prod_address,
                'province': province_id,
                'amphur': amphur_id,
                'map_lat': postdata['geo_latitude'],
                'map_zoom': '',
                'map_lng': postdata['geo_longitude'],
                'payment_method': '',
                'productcondition': '',
                'area': floor_area,
                'capcha': var,
                'rands': var,
                'fileshow': 'download.jpeg',
                'op_s_show': '',
                'file1': '(binary)',
                'op1': '',
                'file2': '(binary)',
                'op2': '',
                'file3': '(binary)',
                'op3': '',
                'file4': '(binary)',
                'op4': '',
                'Submit.x': '79',
                'Submit.y': '17',
            }
            if postdata['listing_type']!='ขาย':
                datapost['class_type_id']=2
            arr = ["fileshow", "file1", "file2", "file3", "file4"]
            # files = {'fileshow': open('download.jpeg', 'rb')}
            files = {}
            # print(postdata['post_images'])
            no =len(postdata['post_images'][:5])
            if no == 0:
                files = {'fileshow': ('imgtmp/default/white.png', open(
                    'imgtmp/default/white.png', 'rb'), 'image/png')}
            else:
                for i in range(no):
                    datapost[arr[i]] = postdata['post_images'][i]
                    files[arr[i]] = (postdata['post_images'][i], open(postdata['post_images'][i], "rb"), "image/jpg")

            # return ""

            # return ""

            r = httprequestObj.http_post(
                'http://www.xn--42cf4b4c7ahl7albb1b.com/member/p-post-property.php', data=datapost, files=files)
            list_url = 'http://www.xn--42cf4b4c7ahl7albb1b.com/member/list-property.php'
            r = httprequestObj.http_get(list_url)
            soup = BeautifulSoup(r.content, 'html5lib')
            var = soup.find('a', attrs={'title': postdata['post_title_th']})[
                'href']
            if var =="" or var =='http://www.อสังหาราคาดี.com/index.php':
                time_end = datetime.datetime.utcnow()
                time_usage = time_end - time_start
                return {
                'success': 'false',
                'action':"create_post",
                "websitename": "goodpriceproperty",
                "start_time": str(time_start),
                "end_time": str(time_end),
                
                'post_url': '',
                'post_id': '',
                'account_type':''
                }
            # for i in '../property/':
            i = len('../property/')
            # post_id=''
            post_id = ''

            while var[i] != '/':
                post_id += var[i]
                i += 1
            post_url = 'http://www.xn--42cf4b4c7ahl7albb1b.com/property/' + \
                post_id+"/"+postdata['post_title_th']+'.html'
            
            
            
            time_end = datetime.datetime.utcnow()
            time_usage = time_end - time_start
            data=r.text
            success="true"
            if data.find("alert")!=-1:
                success="false"
            return {
                'success': 'true',
                'action':"create_post",
                "websitename": "goodpriceproperty",
                "start_time": str(time_start),
                "end_time": str(time_end),
                'post_url': post_url,
                'post_id': post_id,
                'account_type':''
            }

    def edit_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        ashopname = test_login["detail"]
        post_id = ""
        detail = ""
        province_id = ""
        amphur_id = ""

        for (key, value) in provincedata.items():
            if type(value) is str and postdata['addr_province'].strip() in value.strip():
                province_id = key
                break

        if province_id=="":
            return{
                'success': 'false',
                'ret': "",
                'post_url': "",
                'post_id': ""
            }


        for (key, value) in provincedata[province_id+"_province"].items():
            if postdata['addr_district'].strip() in value.strip():
                amphur_id = key
                break
        if amphur_id=="":
            return{
                'success': 'false',
                'ret': "",
                'post_url': "",
                'post_id': ""
            }
        # province_id = 64
        # amphur_id = 864

        no = 0
        img_arr = {}
        topic_id=postdata['post_id']
        # for i in range(len(postdata['post_img_url_lists'])):
        #     img_arr[i] = str(no)+".jpg"
        #     print("imagefs ", postdata['post_img_url_lists'][i])
        #     urllib.request.urlretrieve(
        #         postdata['post_img_url_lists'][i], str(no)+".jpg")
        #     no += 1
        try:
            floor_area = postdata['floor_area']
        except:
            floor_area = ""

        getProdId = {'1': 4, '2': 1, '3': 2, '4': 3, '5': 6,
                     '6': 10, '7': 5, '8': 7, '9': 8, '10': 9}

        prod_address = ""
        for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
            if add is not None:
                prod_address += add + ","
        # prod_address = prod_address

        if success == "true":
            edit_url = "http://www.xn--42cf4b4c7ahl7albb1b.com/member/edit-property.php"
            payload = {'topic_id':topic_id }
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
            }

            with requests.Session() as s:
                r = httprequestObj.http_get_with_headers(
                    edit_url, headers=headers, params=payload)

                # r=s.post(edit_url,,headers=register_headers)
            soup = BeautifulSoup(r.content, 'html5lib')
            var = soup.find('input', attrs={'name': 'rands'})['value']
            if len(var) == 0:
                return{
                    'success': 'false',
                    'ret': "",
                    'post_url': "",
                    'post_id': ""
                }


            datapost = {
                'class_type_id': '1',  # 1 for sell 2 for rent
                'cate_id': getProdId[postdata['property_type']],  # the property tye
                'action': 'saveproduct',
                # 'hidproduct_id': postdata['post_id'],
                'savetype': 'R',
                'title': postdata['post_title_th'],
                'topic_id': postdata['post_id'],
                'project': postdata['project_name'],
                'detail': postdata['post_description_en'],
                'price': postdata['price_baht'],
                'product_unit[]': '',
                'product_warranty_price': '',
                'shipping_id': '',
                'add': prod_address,
                'province': province_id,
                'amphur': amphur_id,
                'map_lat': postdata['geo_latitude'],
                'map_zoom': '',
                'map_lng': postdata['geo_longitude'],
                'payment_method': '',
                'productcondition': '',
                'area': floor_area,
                'capcha': var,
                'rands': var,
                'fileshow': '(binary)',
                'op_s_show': '',
                'file1': '(binary)',
                'op1': '',
                'file2': '(binary)',
                'op2': '',
                'file3': '(binary)',
                'op3': '',
                'file4': '(binary)',
                'op4': '',
                'Submit.x': '79',
                'Submit.y': '17',

            }
            # print(datapost)
            if postdata['listing_type']!='ขาย':
                datapost['class_type_id']=2
            arr = ["fileshow", "file1", "file2", "file3", "file4"]
            # files = {'fileshow': open('download.jpeg', 'rb')}
            files = {}

            no =len(postdata['post_images'][:5])
            # if no == 0:
            #     files = {'fileshow': ('download.jpeg', open(
            #         'download.jpeg', 'rb'), 'image/jpeg')}
            # else:
            for i in range(no):
                datapost[arr[i]] = postdata['post_images'][i]
                files[arr[i]] = (postdata['post_images'][i], open(postdata['post_images'][i], "rb"), "image/jpg")


            r = httprequestObj.http_post(
                'http://www.xn--42cf4b4c7ahl7albb1b.com/member/p-edit-property.php', data=datapost, headers=headers, files=files)
            # print("RETURN ", r.content)
            # print("RETURN ", r.text)
            data = r.text
            time_end = datetime.datetime.utcnow()
            time_usage = time_end - time_start
            # print("REACHED ")
            if data.find("alert")!=-1:
                success="false"
            return {
                'success':success,
                "action": "edit_post",
                "websitename": "goodpriceproperty",
                "start_time": str(time_start),
                "end_time": str(time_end),
                "detail":data,
                "log_id": "",             
            }


    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]

        if success == "true":

            datapost = [
                ('action', 'delete_product'),
                ('product_id',  postdata['post_id']),
            ]
            url = "http://www.xn--42cf4b4c7ahl7albb1b.com/member/del-property.php"
            payload = {'topic_id': postdata['post_id']}

            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
            }

            r = httprequestObj.http_get_with_headers(
                url, headers=headers, params=payload)
            # r = httprequestObj.http_post(
            #     'https://www.ploychao.com/member/', data=datapost)
            data = r.text
            time_end = datetime.datetime.utcnow()
            time_usage = time_end - time_start

            success="true"
            if data.find("alert") != -1:
                success="false"
            return{
                'success':success,
                "action": "delete_post",
                "websitename": "goodpriceproperty",
                "start_time": str(time_start),
                "end_time": str(time_end),
                "detail":data,
                "log_id": postdata['log_id'],             
            }

            if data == '':
                success = "false"
            else:
                detail = data
        else:
            success = "false"
            # print(data)
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "websitename": "goodpriceproperty",
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "log_id": postdata['log_id'],
            # "detail": "under construction",
        }

    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        post_id = postdata['post_id']
        log_id = postdata['log_id']

        #
        #
        #

        time_end = datetime.datetime.utcnow()
        return {
            "success": "false",
            "time_usage": time_end - time_start,
            "time_start": time_start,
            "time_end": time_end,
            "detail": "",
            "log_id": log_id,
            "post_id": post_id,
        }    


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

        # company_name = postdata['company_name']
        # name_th = postdata["name_th"]
        # surname_th = postdata["surname_th"]
# email = "cu1123@3.com"
# reg_arr= { "action": "register_user", "timeout": "7","ds_name": "goodpriceproperty","ds_id": "4","user": email,"pass": "12345678","company_name": "amarkjjk","name_title": "mr","name_th": "อัมรินทร์","surname_th": "บุญเกิด","name_en": "Amarin","surname_en": "Boonkirt","tel": "0891999450","line": "amarin.ta","addr_province" : "นนทบุรี", "addr_district" : "เมืองนนทบุรี" }

# thedata = { "action": "edit_post", "timeout": "5", "project_name": "ลุมพีนีวิลล", "post_img_url_lists": [ "https://zignnet.sgp1.digitaloceanspaces.com/livingjoin/classified/189689/big/210120235215500991.jpg", "https://zignnet.sgp1.digitaloceanspaces.com/livingjoin/classified/189689/other/big/210120235220317918.jpg" ], "geo_latitude": "13.786862", "geo_longitude": "100.757815", "property_id" : "chu001", "post_title_th": "new edited dsfhfj ให้เช่า ที่ดินด่วน บางกรวยไทรน้อย 6 ไร่ เหมาะทำตลาด", "post_description_th": "What is description", "post_title_en": "Land for rent bangkloysainoi 6 rai suitable for developing", "post_description_en": "Land for rent bangkloysainoi 6 rai suita ble for developing", "price_baht": "100000", "listing_type": "เช่า", "property_type": "6", "prominent_point " : "หน้ากว้างมาก ให้เช่าถูกสุด", "direction_type" : "11", "addr_province": "นนทบุรี", "addr_district": "เมืองนนทบุรี", "addr_sub_district": "บางกรวย", "addr_road": "บางกรวย-ไทรน้อย", "addr_soi": "ซอยบางกรวย-ไทรน้อย 34", "addr_near_by": "ถนนพระราม5\nถนนนครอินทร์", "land_size_rai": "6", "land_size_ngan": "0", "land_size_wa": "0", "name": "ชู", "mobile": "0992899999", "email": "panuwat.ruangr",'user':'temp_007','pass':'123456','post_id':'289666'}
# a=goodpriceproperty()
# # print(reg_arr)
# print(a.register_user(reg_arr))