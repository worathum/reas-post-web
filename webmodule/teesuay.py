# -*- coding: utf-8 -*-

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
from urllib.parse import unquote


httprequestObj = lib_httprequest()


with open("./static/ploychao_province.json") as f:
    provincedata = json.load(f)


class teesuay():

    name = 'teesuay'

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
        self.websitename = 'teesuay'




    def register_user(self, postdata):        
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        province_id=0
        amphur_id=0
        success = "true"
        detail = ""
        passwd = postdata['pass']
        add = 'กรุงเทพ'
        tel = postdata["tel"]
        email = postdata["user"]
        website = ""
        for (key, value) in provincedata.items():
            if type(value) is str and 'กรุงเทพ' in value.strip():
                province_id = key
                break
        for (key, value) in provincedata[str(province_id)+"_province"].items():
            if 'พญาไท' in value.strip():
                amphur_id = key
                break
        datapost = dict(
            email=email,
            repass=passwd,
            name=postdata['name_th']+" "+postdata['surname_th'],
            action='p-member-register.php',
            province=province_id,
            amphur=amphur_id,
            website=website,
            tel=tel
        )
        datapost['pass']=passwd
        datapost['Submit.x']='43'
        datapost['Submit.y']='11'
        datapost['capcha']=datapost['rands']="ABCD"
        url_n="http://www.teesuay.com/p-member-register.php"
        with requests.Session() as s:
            r=s.post(url_n,data=datapost)
        # print(r.content)
        # print(r.text)
        data = r.text
        if data == '':
            success = "false"
        else:
            detail = "registered"  

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "teesuay",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
        }


    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        email = postdata['user']
        passwd = postdata['pass']
        btloginx=22
        btloginy=21
        success = "true"
        detail = ""

        datapost = {
            'action': 'login.php',
            'email': email,
            'pass': passwd,
            'btlogin.x':btloginx,
            'btlogin.y':btloginy
        }

        r = httprequestObj.http_post('http://www.teesuay.com/login.php', data=datapost)
        data = r.text
        if data.find("ขออภัยครับ") != -1:
            success = "false"
        else:
            detail = "logged in"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "teesuay",
            "success": success,
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


        # getProdId = {'1':24,'2':25,'3':26,'4':27,'5':29,'6':34,'7':28,'8':14,'9':31,'10':33}
        # theprodid = getProdId[postdata['property_id']]
        province_id=-1
        amphur_id=0
        for (key, value) in provincedata.items():
            if type(value) is str and postdata['addr_province'].strip() in value.strip():
                province_id = key
                break
        if province_id==-1:
            return{
                'success': 'False',
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
        prod_address = ""
        for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
            if add is not None:
                prod_address += add + ","
        prod_address = prod_address[:-1]

        propertytype={
            '6':1,
            '2':2,
            '3':3,
            '1':4,
            '7':5,
            '5':6,
            # 'Resort hotel':7,
            '9':8,
            '10':9,
            '4':10,
            '8':10
            }
        try:
            postdata['cate_id']=propertytype[postdata['property_type']]
        except:
            return{
                'success': 'false',
                'ret': "",
                'post_url': "",
                'post_id': ""
            }
        if success == "true":
            floor_total, bedroom, bathroom, floor_area = [''] * 4
            if 'floor_total' in postdata: floor_total = postdata['floor_total']
            if 'bedroom' in postdata: bedroom = postdata['bedroom']
            if 'bathroom' in postdata: bathroom = postdata['bathroom']
            if 'floor_area' in postdata: floor_area = postdata['floor_area']
            datapost = {
                'class_type_id':'1', # 1 for sell 2 for rent
                'cate_id':postdata['cate_id'], #the property tye
                'action': 'p-edit-property.php',
                'status': '1',
                'title': postdata['post_title_th'],
                'project': postdata['project_name'],
                'price':postdata['price_baht'],
                'add':prod_address,
                'province':province_id,
                'amphur':amphur_id,
                'map_lat':postdata['geo_latitude'],
                'map_zoom':'',
                'map_lng':postdata['geo_longitude'],
                'bedroom':bedroom,
                'bathroom':bathroom,
                'floors':floor_total,
                'area':floor_area,
                'capcha':"ABCD",
                'rands':"ABCD",
                'fileshow': '(binary)',
                'opshow':'',
                'op_s_show':'',
                'file1': '(binary)',
                'op1': '',
                'file2':'(binary)',
                'op2': '',
                'file3': '(binary)',
                'op3': '',
                'file4': '(binary)',
                'op4':'',
                'name':'Temp',
                'email':postdata['user'],
                'website':'http://temp.com',
                'Submit':'Continue >>'
            }
            if postdata['listing_type']!='ขาย':
                datapost['class_type_id']=2
            
            arr = ["fileshow", "file1", "file2", "file3", "file4"]
            files={}
            for i in range(len(postdata['post_images'][:5])):
                datapost[arr[i]] = postdata['post_images'][i]
                files[arr[i]] = (postdata['post_images'][i], open(postdata['post_images'][i], "rb"), "image/jpg")

            r = httprequestObj.http_post(
                'http://www.teesuay.com/member/p-post-property.php', data=datapost,files=files)

            data = r.text
            if data == '1':
                success = "false"
            else:
                list_url = 'http://www.teesuay.com/member/list-property.php'
                r = httprequestObj.http_get(list_url)
                soup = BeautifulSoup(r.content, 'html5lib')
                var = soup.find('a', attrs={'title': postdata['post_title_th']})[
                    'href']
                # for i in '../property/':
                i = len('../property/')
                # post_id=''
                post_id = ''

                while var[i] != '/':
                    post_id += var[i]
                    i += 1
                post_url = 'http://www.teesuay.com/property-' + \
                    post_id+"/"+postdata['post_title_th'].replace(' ','-')+'.html'

        else:
            success = "False"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "websitename": "teesuay",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": post_url,
            "post_id": post_id,
        }


    def edit_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        # print(test_login)
        success = test_login["success"]
        ashopname = test_login["detail"]
        post_id = ""
        detail = ""
        post_id = ""
        detail = ""
        province_id=-1
        amphur_id=0

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

        if amphur_id==-1:
            return{
                'success': 'false',
                'ret': "",
                'post_url': "",
                'post_id': ""
            }
        no = 0
        # img_arr = {}
        # for i in range(len(postdata['post_img_url_lists'])):
        #     img_arr[i] = str(no)+".jpg"
        #     print("imagefs ", postdata['post_img_url_lists'][i])
        #     urllib.request.urlretrieve(
        #         postdata['post_img_url_lists'][i], str(no)+".jpg")
        #     no += 1


        prod_address = ""
        for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
            if add is not None:
                prod_address += add + ","
        prod_address = prod_address[:-1]

        propertytype={
            '6':1,
            '2':2,
            '3':3,
            '1':4,
            '7':5,
            '5':6,
            # 'Resort hotel':7,
            '9':8,
            '10':9,
            '4':10,
            '8':10
            }
        try:
            postdata['cate_id']=propertytype[postdata['property_type']]
        except:
            return{
                'success': 'false',
                'detail':'wrong propertytype',
                'ret': '',
                'post_url': '',
                'post_id': ''
            }
        if success == "true":
            datapost = {
                'post_id':postdata['post_id'],
                # 'class_type_id':postdata['class_type_id'], # 1 for sell 2 for rent
                'cate_id':postdata['cate_id'], #the property tye
                'action': 'p-edit-property.php',
                'status': '1',
                'title': postdata['post_title_th'],
                'project': postdata['post_title_th'],
                'price':postdata['price_baht'],
                'add':prod_address,
                'province':province_id,
                'amphur':amphur_id,
                'map_lat':postdata['geo_latitude'],
                'map_zoom':'',
                'map_lng':postdata['geo_longitude'],
                'input':'',
                'bedroom':'',
                'bathroom':'',
                'floors':'',
                'area':prod_address,
                'capcha':"ABCD",
                'rands':"ABCD",
                'fileshow': '(binary)',
                'opshow':'',
                'op_s_show':'',
                'file1': '(binary)',
                'op1': '',
                'file2':'(binary)',
                'op2': '',
                'file3': '(binary)',
                'op3': '',
                'file4': '(binary)',
                'op4':'',
                'name':'Temp',
                'email':'temp@gmail.com',
                'website':'http://temp.com',
                'Submit':'Continue >>'
            }
            if postdata['listing_type']!='ขาย':
                datapost['class_type_id']=2
            else:    
                datapost['class_type_id']=1    
            arr = ["fileshow", "file1", "file2", "file3", "file4"]
            files={}
            for i in range(len(postdata['post_images'][:5])):
                datapost[arr[i]] = postdata['post_images'][i]
                files[arr[i]] = (postdata['post_images'][i], open(postdata['post_images'][i], "rb"), "image/jpg")

 


            url_n='http://www.teesuay.com/member/p-edit-property.php'

            r=httprequestObj.http_post(url_n,datapost)
            detail=r.text
            success="true"
        else:
            success = "false"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "teesuay",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
        }



    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        r=httprequestObj.http_get('http://www.teesuay.com/member/list-property.php')
            # r=s.post(edit_url,,headers=register_headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        var = soup.find('input', attrs={'name': 'hdnCount'})['value']
        if len(var) == 0:
            return{
                'success': 'false',
                'ret': "",
                'post_url': "",
                'post_id': ""
            }
        if success == "true":
            datapost = {
                'action':'manage-property-not-sale.php',
                'chkDel[]': postdata['post_id'],
                'type':'2',
                'Submit':'Proceed',
                'hdncount':var
            }
            r = httprequestObj.http_post('http://www.teesuay.com/member/manage-property-not-sale.php', data=datapost)
            data = r.text
            if data == '':
                success = "false"
            else:
                detail = data
        else:
            success = "false"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "teesuay",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            # "log_id":postdata['log_id'],
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
            "websitename": "teesuay",
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

        return {
            "websitename": "teesuay",
            "success": "true",
            "time_usage": time_end - time_start,
            "time_start": time_start,
            "time_end": time_end,
            "detail": ""
        }

