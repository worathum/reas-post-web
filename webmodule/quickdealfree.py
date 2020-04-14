# -*- coding: utf-8 -*-

from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
# from urlparse import urlparse
import re
import json
import datetime
import sys
import requests
import shutil
from urllib.parse import unquote


httprequestObj = lib_httprequest()

with open("./static/quickdealfree_province.json") as f:
    provincedata = json.load(f)


class quickdealfree():

    name = 'quickdealfree'

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

        # start process
        #
        success = "true"
        detail = ""

        datapost = {
            "email": user,
            "pass": passwd,
            "rands": "M7DQ",
            "capcha": "M7DQ",
            "submit": "สมัครสมาชิก"
        }
        r = httprequestObj.http_post(
            'http://www.quickdealfree.com/p-register.php', data=datapost)
        data = r.text
        # print(data)
        if data.find("อีเมล์นี้มีอยู่ในระบบแล้ว") != -1:
            detail = "Email Already registered"
        else:
            detail = "Registered"
        # #
        # # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": "quickdealfree",
        }

    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']
        # start process
        #
        success = "true"
        detail = "logged in"

        datapost = {
            'submit': 'Login',
            'pass': passwd,
            'email': user,

        }
        r = httprequestObj.http_post(
            'http://www.quickdealfree.com/login.php', data=datapost)
        data = r.text
        # print(data)
        if data.find("Email") != -1:
            detail = "cannot login"
            success = "false"
        #
        # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": "quickdealfree",
        }

    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        #

        # login

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""

        proid = {
            'คอนโด': '1',
            'บ้านเดี่ยว': '2',
            'บ้านแฝด': '3',
            'ทาวน์เฮ้าส์': '4',
            'ตึกแถว-อาคารพาณิชย์': '5',
            'ที่ดิน': '6',
            'อพาร์ทเมนท์': '7',
            'โรงแรม': '8',
            'ออฟฟิศสำนักงาน': '9',
            'โกดัง-โรงงาน': '10'
        }
        getProdId = {'1': 159, '2': 156, '3': 157, '4': 157,
                     '5': 158, '6': 161, '7': 162, '8': 162, '9': 162, '10': 162}

        try:
            theprodid = getProdId[proid[postdata['property_type']]]
        except:
            theprodid = getProdId[postdata['property_type']]

        province_id = ''

        for (key, value) in provincedata.items():
            if type(value) is str and postdata['addr_province'].strip() in value.strip():
                province_id = key
                # print("yes")
                break

        prod_address = ""
        for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
            if add is not None:
                prod_address += add + " "
        prod_address = prod_address[:-1]

        if success == "true":

            datapost = [
                ('cate_id', '23'),
                ('sub_cate_id', theprodid),
                ('post_title', postdata['post_title_th']),
                ('detail', postdata['post_description_th']),
                ('post_price_type', '2'),
                ('post_price', postdata['price_baht']),
                ('add', prod_address),
                ('province', province_id),
                ('name', postdata['name']),
                ('email', postdata['email']),
                ('tel', postdata['mobile']),
                ('rands', 'ZF71'),
                ('capcha', 'ZF71'),
                ('submit', 'Confirm announcement'),
            ]

            if postdata['listing_type'] != 'ขาย':
                datapost.append(('class_type_id', '4'))
            else:
                datapost.append(('class_type_id', '2'))

            files = {}
            allimages = postdata["post_images"][:5]
            for i in range(len(allimages)):
                # r = open(postdata["post_img_url_lists"][i],'rb')
                # if i>5 :
                    # break
                r = open(os.getcwd()+"/"+allimages[i], 'rb')
                if i == 0:
                    files['fileshow'] = r
                else:
                    files["file"+str(i)] = r

            r = httprequestObj.http_post(
                'http://www.quickdealfree.com/member/p-classifieds-post.php', data=datapost, files=files)
            data = r.text
            # print(data)
            r = httprequestObj.http_get(
                "http://www.quickdealfree.com/member/list-classifieds.php")
            soup = BeautifulSoup(r.text, 'lxml')
            post_url = soup.select(
                "#frmMain > div > table > tbody > tr:nth-child(2) > td:nth-child(1) > a")[0]['href']
            post_id = post_url[8:13]
            post_url = "http://quickdealfree.com"+post_url[2:]
            # print(post_url,post_id)
            detail = "Post Created"
        else:
            detail = "cannot login"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
            "websitename": "quickdealfree",
        }

    def edit_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process

        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = ""
        post_id = ""
        post_url = ""

        proid = {
            'คอนโด': '1',
            'บ้านเดี่ยว': '2',
            'บ้านแฝด': '3',
            'ทาวน์เฮ้าส์': '4',
            'ตึกแถว-อาคารพาณิชย์': '5',
            'ที่ดิน': '6',
            'อพาร์ทเมนท์': '7',
            'โรงแรม': '8',
            'ออฟฟิศสำนักงาน': '9',
            'โกดัง-โรงงาน': '10'
        }
        getProdId = {'1': 159, '2': 156, '3': 157, '4': 157,
                     '5': 158, '6': 161, '7': 162, '8': 162, '9': 162, '10': 162}

        try:
            theprodid = getProdId[proid[postdata['property_type']]]
        except:
            theprodid = getProdId[postdata['property_type']]

        province_id = ''

        # for i in postdata["post_img_url_lists"]:

        for (key, value) in provincedata.items():
            if type(value) is str and postdata['addr_province'].strip() in value.strip():
                province_id = key
                # print("yes")
                break

        prod_address = ""
        for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
            if add is not None:
                prod_address += add + " "
        prod_address = prod_address[:-1]
        # resp = requests.get(image_url, stream=True)
        files = {}
        if success == "true":
            r = httprequestObj.http_get(
                "http://www.quickdealfree.com/member/list-classifieds.php")
            soup = BeautifulSoup(r.text, 'lxml')
            post_url = soup.select(
                "#frmMain > div > table > tbody > tr > td> a")
            success = "false"
            for i in post_url:
                if i['href'][8:13] == postdata['post_id']:
                    success = "true"
                if success == "true":
                    datapost = [
                        ('id', postdata['post_id']),
                        ('cate_id', '23'),
                        ('sub_cate_id', theprodid),
                        ('post_title', postdata['post_title_th']),
                        ('detail', postdata['post_description_th']),
                        ('post_price_type', '2'),
                        ('post_price', postdata['price_baht']),
                        ('add', prod_address),
                        ('province', province_id),
                        ('name', postdata['name']),
                        ('email', postdata['email']),
                        ('tel', postdata['mobile']),
                        ('rands', 'ZF71'),
                        ('capcha', 'ZF71'),
                        ('submit', 'Confirm announcement'),
                    ]
                    allimages = postdata["post_images"][:5]
                    for i in range(len(allimages)):
                        r = open(os.getcwd()+"/"+allimages[i], 'rb')
                        if i == 0:
                            files['fileshow'] = r
                        else:
                            files["file"+str(i)] = r

                    r = httprequestObj.http_post(
                        'http://www.quickdealfree.com/member/p-edit-classifieds-post.php', data=datapost, files=files)
                else:
                    detail = "No post found with given id."
        else:
            detail = "cannot login"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            # "post_url": "http://www.quickdealfree.com/post-"+postdata['post_id']+'/'+postdata['post_title_th']+".html",
            # "post_id": postdata['post_id'],
            "account_type": "null",
            "detail": detail,
            "websitename": "quickdealfree",
        }

    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # TODO ประกาศที่ทดสอบไป ยังไม่ครบ 7 วัน ทำทดสอบการลบไม่ได้ วันหลังค่อยมาทำใหม่
        r = httprequestObj.http_get(
            "http://www.quickdealfree.com/member/list-classifieds.php")
        soup = BeautifulSoup(r.text, 'lxml')
        post_url = soup.select(
            "#frmMain > div > table > tbody > tr > td> a")
        success = "false"
        for i in post_url:
                    if i['href'][8:13] == postdata['post_id']:
                        success = "true"
        user = postdata['user']
        passwd = postdata['pass']

        # start process
        #
        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        if success == "true":
            r = httprequestObj.http_get(
                "http://www.quickdealfree.com/member/list-classifieds.php")
            soup = BeautifulSoup(r.text, 'lxml')
            post_url = soup.select(
                "#frmMain > div > table > tbody > tr > td> a")
            success = "false"
            for i in post_url:
                if i['href'][8:13] == postdata['post_id']:
                    success = "true"
            if success == "true":
                r = httprequestObj.http_get(
                    'http://www.quickdealfree.com/member/del-classifieds.php?id='+postdata['post_id'])
            else:
                detail = "No post found with given id."
        else:
            detail = "cannot login"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": "quickdealfree",
            "log_id": 1,
        }
    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        post_id = postdata['post_id']
        log_id = postdata['log_id']

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


# tri = quickdealfree()
# dic = {"user": "shikhar100mit@gmail.com", "email": "shikhar100mit@gmail.com", "post_id": "82860", "pass": 12345678, "addr_soi": "xyz",'post_images':[], 
#        "addr_road": "123", "addr_sub_district": "abc", "addr_district": "bbc", 'addr_province': "กระบี่", 'property_type': 'ที่ดิน',
#        "post_title_th": "ppppppppp", "post_description_th": "ahhahahaha", "price_baht": "128", 'name': 'shikhar',
#        'mobile': ''}
# print(tri.edit_post(dic))
# {"user":"shikhar100mit@gmail.com","email": "rohibe8488@gotkmail.com", "id": "823", "pass": 12345678, "addr_soi": "xyz", "post_img_url_lists": ["http://pngimg.com/uploads/birds/birds_PNG115.png","http://pngimg.com/uploads/birds/birds_PNG111.png"],
# "addr_road": "123", "addr_sub_district": "abc", "addr_district": "bbc","addr_province": "กระบี่", "property_type": "1","post_title_th": "ppppppppp", "post_description_th": "ahhahahaha", "price_baht": "128", "name": "shikhar",        "mobile": ""}
