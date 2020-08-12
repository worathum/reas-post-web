# -*- coding: utf-8 -*-

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


with open("./static/ploychao_province.json",encoding = 'utf-8') as f:
    provincedata = json.load(f)


class teedindd():

    name = 'teedindd'

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
            "websitename": "teedindd",
            "success": "true",
            "time_usage": time_end - time_start,
            "start_time": time_start,
            "end_time": time_end,
            "detail": ""
        }

    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        success = "true"
        detail = ""

        if 'surname_th' not in postdata:
            return{
                'websitename': 'teedindd',
                'success': 'false',
                    'ds_id': postdata['ds_id'],
                'detail': 'Missing required field name',
            }
        if 'name_th' not in postdata:
            return{
                'websitename': 'teedindd',
                    'ds_id': postdata['ds_id'],
                'success': 'false',
                'detail': 'Missing required field name',
            }
        if 'pass' not in postdata:
            return{
                'websitename': 'teedindd',
                    'ds_id': postdata['ds_id'],
                'success': 'false',
                'detail': 'Missing required field pass',
            }
        if 'user' not in postdata:
            return{
                'websitename': 'teedindd',
                'success': 'false',
                    'ds_id': postdata['ds_id'],
                'detail': 'Missing required field email',
            }

        datapost = dict(
            RegisterName=postdata['name_th']+" "+postdata['surname_th'],
            RegisterEmail=postdata['user'],
            RegisterPassword=postdata['pass'],
            CRegisterPassword=postdata['pass'],
            BttSave='Become a member'
        )

        url_n = "https://www.teedindd.com/register-process.php"
        s = requests.Session()
        r = s.post(url_n, data=datapost)
        data = r.text
        soup = BeautifulSoup(r.content, 'html5lib')
        classfind = soup.findAll('div', attrs={'class': 'pt20'})
        for i in classfind:
            if i.text == "อีเมล์ของคุณมีอยู่ในระบบแล้ว":
                data = ''
                break
        if data == '':
            success = "false"
            detail="Failed to register"
        else:
            detail = "registered"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "teedindd",
            "success": success,
                'ds_id': postdata['ds_id'],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
        }

    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        success = "true"
        detail = ""

        if 'pass' not in postdata:
            return{
                'websitename': 'teedindd',
                'success': 'false',
                'detail': 'Missing required field pass',
            }
        if 'user' not in postdata:
            return{
                'websitename': 'teedindd',
                'success': 'false',
                'detail': 'Missing required field email',
            }



        datapost = {
            'RegisterEmail': postdata['user'],
            'RegisterPassword': postdata['pass'],
            'BttSave':  'Login'
        }

        r = httprequestObj.http_post(
            'https://www.teedindd.com/login-check.php', data=datapost)
        data = r.text
        soup = BeautifulSoup(r.content, 'html5lib')
        classfind = soup.findAll('div', attrs={'class': 'pt20 pb20'})
        print(classfind)
        for i in classfind:
            if "ไม่พบอีเมล์ในระบบกรุณา" in  i.text:  
                data = ''
                break
            if "รหัสผ่านไม่ถูกต้อง" in i.text:
                data = "WP"
                break
        if data == '':
            success = "false"
            detail = "Verify email"
        elif data == "WP":
            success = "false"
            detail = "Wrong Password"
        else:
            detail = "Logged in"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "teedindd",
            "success": success,
            "ds_id": postdata['ds_id'],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail
        }

    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]     
        posturl="https://www.teedindd.com/admin/properties-process.php"
        r=httprequestObj.http_post(posturl,data={'DunDate':'1'})
        time_end = datetime.datetime.utcnow()
        return {
            "websitename": "teedindd",
            "success": "true",
            "usage_time": time_end - time_start,
            "start_time": time_start,
            "end_time": time_end,
            "detail": "",
                'ds_id': postdata['ds_id'],
            "log_id":postdata['log_id'],
            "post_id": postdata['post_id'],
        }        

    def editpost(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        theurl = ""
        post_id = ""

        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        ashopname = test_login["detail"]

        if success == "true":
            if 'name' not in postdata:
                return{
                'websitename': 'teedindd',
                'success': 'false',
                'detail': 'Missing required field name',
                'detail': '',
                'post_url': '',
                'post_id': ''
            }
            if 'mobile' not in postdata:
                return{
                    'websitename': 'teedindd',
                    'success': 'false',
                    'detail': 'Missing required field mobile',
                    'detail': '',
                    'post_url': '',
                    'post_id': ''
                }
            if 'pass' not in postdata:
                return{
                    'websitename': 'teedindd',
                    'success': 'false',
                    'detail': 'Missing required field pass',
                    'detail': '',
                    'post_url': '',
                    'post_id': ''
                }
            if 'user' not in postdata:
                return{
                    'websitename': 'teedindd',
                    'success': 'false',
                    'detail': 'Missing required field email',
                    'detail': '',
                    'post_url': '',
                    'post_id': ''
                }
            if 'property_type' not in postdata:
                return{
                    'websitename': 'teedindd',
                    'success': 'false',
                    'detail': 'Missing required field property_type',
                    'detail': '',
                    'post_url': '',
                    'post_id': ''
                }
            if 'listing_type' not in postdata:
                return{
                    'websitename': 'teedindd',
                    'success': 'false',
                    'detail': 'Missing required field listing_type',
                    'detail': '',
                    'post_url': '',
                    'post_id': ''
                }
            if 'price_baht' not in postdata:
                return{
                    'websitename': 'teedindd',
                    'success': 'false',
                    'detail': 'Missing required field price',
                    'detail': '',
                    'post_url': '',
                    'post_id': ''
                }
            if 'post_title_th' not in postdata:
                return{
                    'websitename': 'teedindd',
                    'success': 'false',
                    'detail': 'Missing required field title',
                    'detail': '',
                    'post_url': '',
                    'post_id': ''
                }
            if 'post_description_th' not in postdata:
                return{
                    'websitename': 'teedindd',
                    'success': 'false',
                    'detail': 'Missing required field description',
                    'detail': '',
                    'post_url': '',
                    'post_id': ''
                }

            list_url = 'https://www.teedindd.com/post.php?pd='
            list_url+=postdata['post_id']
            r = httprequestObj.http_get(list_url)
            soup = BeautifulSoup(r.content, 'html5lib')
            var=soup.find('input',attrs={'id':'ti'})
            if var['value']=="":
                time_end = datetime.datetime.utcnow()
                time_usage = time_end - time_start
                return {
                    "websitename": "teedindd",
                    "success": 'false',
                    "start_time": str(time_start),
                    "end_time": str(time_end),
                    "detail": 'Wrong Post id',
                }

            url_post = 'https://www.teedindd.com/post.php'
            r = httprequestObj.http_get(url_post)
            soup = BeautifulSoup(r.content, 'html5lib')
            var = soup.findAll('option')

            postdata['addr_province']=postdata['addr_province'].replace(' ','')
            postdata['addr_district']=postdata['addr_district'].replace(' ','')
            postdata['addr_sub_district']=postdata['addr_sub_district'].replace(' ','')
            


            for i in var:
                if i.text == postdata['addr_province']:
                    postdata['addr_pros'] = i['value']

            if 'addr_pros' not in postdata:
                for i in var:
                    if i.text in postdata['addr_province'] or postdata['addr_province'] in i.text:
                        postdata['addr_pros'] = i['value']
                        break
                    # print(i.text)
            if 'addr_pros' not in postdata:
                postdata['addr_pros'] = var[0]['value']

            uid = soup.find('input', attrs={'name': 'uid'})
            pd = soup.find('input', attrs={'name': 'pd'})
            PropAction = soup.find('input', attrs={'name': 'PropAction'})

            url_district = 'https://www.teedindd.com/admin/step-process.php'
            r = httprequestObj.http_post(url_district, data={'pid': postdata['addr_pros'].split(',')[0], 'name': postdata['addr_pros'].split(',')[1]})
            
            for i in json.loads(r.text):
                if i['name'] == postdata['addr_district']:
                    postdata['addr_dis'] = i
                    break
            
            if 'addr_dis' not in postdata:
                for i in json.loads(r.text):
                    if i['name'] in postdata['addr_district'] or postdata['addr_district'] in i['name']:
                        postdata['addr_dis'] = i
                        break
            if 'addr_dis' not in postdata:
                postdata['addr_dis'] = json.loads(r.text)[0]


            url_district = 'https://www.teedindd.com/admin/step-process.php'
            r = httprequestObj.http_post(url_district, data={
                                        'aid': postdata['addr_dis']['aid'], 'name': postdata['addr_dis']['name']})
            for i in json.loads(r.text):
                if i['name'] == postdata['addr_sub_district']:
                    postdata['addr_sub_dis'] = i
                    break

            if 'addr_sub_dis' not in postdata:
                for i in json.loads(r.text):
                    if i['name'] in postdata['addr_sub_district'] or postdata['addr_sub_district'] in i['name']:
                        postdata['addr_sub_dis'] = i
                        break   

            if 'addr_sub_dis' not in postdata:
                postdata['addr_sub_dis'] = json.loads(r.text)[0]


            prod_address = ""
            
            for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
                if add is not None or add=="" or add==" ": 
                    prod_address += add + ","
            prod_address = prod_address[:-1]
            if postdata['listing_type'] == 'เช่า' or postdata['listing_type'] == 're':
                postdata['listing_type'] = 're'
            else:
                postdata['listing_type'] = 'se'
            propertytype = {
                '6': 1,
                '2': 2,
                '3': 2,
                '1': 2,
                '7': 2,
                '5': 2,
                '9': 2,
                '10': 2,
                '4': 2,
                '8': 2
            }
            try:
                postdata['cate_id'] = propertytype[str(postdata['property_type'])]
            except:
                return{
                    'websitename':'teedindd',
                    'success': 'false',
                    # 'log_id': postdata['log_id'],
                    'ds_id': postdata['ds_id'],
                    'detail': "",
                    'post_url': "",
                    'post_id': ""
                }
            
            datapost = {
                'sr': postdata['listing_type'],
                'cid2': postdata['cate_id'],
                'ti': postdata['post_title_th'],
                'detail': postdata['post_description_th'],
                'price': postdata['price_baht'],
                'province': postdata['addr_pros'],
                'amphur': postdata['addr_dis']['aid'] +
                 ","+postdata['addr_dis']['name'],
                'district': postdata['addr_sub_dis']
                 ['did']+","+postdata['addr_sub_dis']['name'],
                'la': postdata['geo_latitude'],
                'lo': postdata['geo_longitude'],
                'fn': postdata['name'],
                't1': postdata['mobile'],
                'em': postdata['email'],
                'li': postdata['email'],
                'pa': postdata['pass'],
                'PropAction': PropAction['value'],
                'uid': uid['value'],
                'pd': pd['value'],
            }
            filename = "files[]"
            data={}

            if len(postdata['post_images'])==0:
                postdata['post_images']=['imgtmp/default/white.jpg']
                data[filename] = (postdata['post_images'][0], open(
                    postdata['post_images'][0], "rb"), "image/jpg")
            else:
                i=postdata['no']
                data[filename] = (postdata['post_images'][i], open(
                    postdata['post_images'][i], "rb"), "image/jpg")
            response = httprequestObj.http_post(
                'https://www.teedindd.com/upload-tmp/', data=datapost , files=data)
            res=json.loads(response.text)
            if len(postdata['post_images']) != 0:
                datapost['photo_name[]']=res['files'][0]['name']
            else:
                datapost['photo_name[]']=None
            datapost['photo_name_old']=''
            r = httprequestObj.http_post(
                'https://www.teedindd.com/admin/properties-process.php', data=datapost)
            data = r.text
            
            detail="edited"
        else:
            success = "False"
            detail = "Login Error"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "websitename": "teedindd",
            "success": success,
            # 'log_id': postdata['log_id'],
            'ds_id': postdata['ds_id'],
            'post_id':postdata['post_id'],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
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
        detail = ''

        if success == "true":
            if 'name' not in postdata:
                return{
                'websitename': 'teedindd',
                'success': 'false',
                'detail': 'Missing required field name',
                'post_url': '',
                'ds_id': postdata['ds_id'],
                'post_id': ''
            }
            if 'mobile' not in postdata:
                return{
                    'websitename': 'teedindd',
                    'success': 'false',
                'ds_id': postdata['ds_id'],
                    'detail': 'Missing required field mobile',
                    'post_url': '',
                    'post_id': ''
                }
            if 'property_type' not in postdata:
                return{
                    'websitename': 'teedindd',
                    'success': 'false',
                    'detail': 'Missing required field property_type',
                'ds_id': postdata['ds_id'],
                    'post_url': '',
                    'post_id': ''
                }
            if 'listing_type' not in postdata:
                return{
                    'websitename': 'teedindd',
                    'success': 'false',
                    'detail': 'Missing required field listing_type',
                    'post_url': '',
                'ds_id': postdata['ds_id'],
                    'post_id': ''
                }
            if 'price_baht' not in postdata:
                return{
                    'websitename': 'teedindd',
                'ds_id': postdata['ds_id'],
                    'success': 'false',
                    'detail': 'Missing required field price',
                    'post_url': '',
                    'post_id': ''
                }
            if 'post_title_th' not in postdata:
                return{
                    'websitename': 'teedindd',
                    'success': 'false',
                    'detail': 'Missing required field title',
                    'post_url': '',
                'ds_id': postdata['ds_id'],
                    'post_id': ''
                }
            if 'post_description_th' not in postdata:
                return{
                    'websitename': 'teedindd',
                    'success': 'false',
                    'ds_id': postdata['ds_id'],
                    'detail': 'Missing required field description',
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
        
            url_post = 'https://www.teedindd.com/post.php'
            r = httprequestObj.http_get(url_post)
            soup = BeautifulSoup(r.content, 'html5lib')
            var = soup.findAll('option')

            postdata['addr_province']=postdata['addr_province'].replace(' ','')
            postdata['addr_district']=postdata['addr_district'].replace(' ','')
            postdata['addr_sub_district']=postdata['addr_sub_district'].replace(' ','')
            for i in var:
                if i.text == postdata['addr_province']:
                    postdata['addr_pros'] = i['value']

            if 'addr_pros' not in postdata:
                for i in var:
                    if i.text in postdata['addr_province'] or postdata['addr_province'] in i.text:
                        postdata['addr_pros'] = i['value']
                        break
                    # print(i.text)
            if 'addr_pros' not in postdata:
                postdata['addr_pros'] = var[0]['value']

            uid = soup.find('input', attrs={'name': 'uid'})
            pd = soup.find('input', attrs={'name': 'pd'})
            PropAction = soup.find('input', attrs={'name': 'PropAction'})

            url_district = 'https://www.teedindd.com/admin/step-process.php'
            r = httprequestObj.http_post(url_district, data={'pid': postdata['addr_pros'].split(',')[0], 'name': postdata['addr_pros'].split(',')[1]})
            
            for i in json.loads(r.text):
                if i['name'] == postdata['addr_district']:
                    postdata['addr_dis'] = i
                    break
            
            if 'addr_dis' not in postdata:
                for i in json.loads(r.text):
                    if i['name'] in postdata['addr_district'] or postdata['addr_district'] in i['name']:
                        postdata['addr_dis'] = i
                        break
            if 'addr_dis' not in postdata:
                postdata['addr_dis'] = json.loads(r.text)[0]

            url_district = 'https://www.teedindd.com/admin/step-process.php'
            r = httprequestObj.http_post(url_district, data={
                                        'aid': postdata['addr_dis']['aid'], 'name': postdata['addr_dis']['name']})
            for i in json.loads(r.text):
                if i['name'] == postdata['addr_sub_district']:
                    postdata['addr_sub_dis'] = i
                    break

            if 'addr_sub_dis' not in postdata:
                for i in json.loads(r.text):
                    if i['name'] in postdata['addr_sub_district'] or postdata['addr_sub_district'] in i['name']:
                        postdata['addr_sub_dis'] = i
                        break   

            if 'addr_sub_dis' not in postdata:
                postdata['addr_sub_dis'] = json.loads(r.text)[0]

            if 'post_images' in postdata and len(postdata['post_images'])>0:
                pass
            else:
                postdata['post_images'] = ['imgtmp/default/white.png']
            prod_address = ""
            for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
                if add is not None or add=="" or add==" ":
                    prod_address += add + ","
            prod_address = prod_address[:-1]
            if postdata['listing_type'] == 'เช่า':
                postdata['listing_type'] = 're'
            else:
                postdata['listing_type'] = 'se'
            propertytype = {
                '6': 1,
                '2': 2,
                '3': 2,
                '1': 2,
                '7': 2,
                '5': 2,
                '9': 2,
                '10': 2,
                '4': 2,
                '8': 2,
                '25':2
            }
            try:
                postdata['cate_id'] = propertytype[str(postdata['property_type'])]
            except:
                return{
                    'websitename':'teedindd',
                    'success': 'false',
                    'detail': " Wrong property type",
                    'post_url': "",
                    'ds_id': postdata['ds_id'],
                    'post_id': ""
                }
            datapost = {
                'sr': postdata['listing_type'],
                'cid2': postdata['cate_id'],
                'ti': postdata['post_title_th'],
                'detail': postdata['post_description_th'],
                'price': postdata['price_baht'],
                'province': postdata['addr_pros'],
                'amphur': postdata['addr_dis']['aid'] +
                 ","+postdata['addr_dis']['name'],
                'district': postdata['addr_sub_dis']
                 ['did']+","+postdata['addr_sub_dis']['name'],
                'la': postdata['geo_latitude'],
                'lo': postdata['geo_longitude'],
                'fn': postdata['name'],
                't1': postdata['mobile'],
                'em': postdata['email'],
                'li': postdata['email'],
                'pa': postdata['pass'],
                'PropAction': PropAction['value'],
                'uid': uid['value'],
                'pd': pd['value'],
            }
            filename = "files[]"
            i=0
            data={}
            data[filename] = (postdata['post_images'][i], open(
                postdata['post_images'][i], "rb"), "image/jpg")
            response = httprequestObj.http_post(
                'https://www.teedindd.com/upload-tmp/', data=datapost , files=data)
            res=json.loads(response.text)
            datapost['photo_name[]']=res['files'][0]['name']
            datapost['photo_name_old']=''
            r = httprequestObj.http_post(
                'https://www.teedindd.com/admin/properties-process.php', data=datapost)
            data = r.text
            
            if data == '':
                success = "false"
            else:
                list_url = 'https://www.teedindd.com/admin/'
                r = httprequestObj.http_get(list_url)
                soup = BeautifulSoup(r.content, 'html5lib')
                var = soup.findAll('div')
                store=""
                final=""
                for i in var:
                    if i.text[:len(i.text)-1]==postdata['post_title_th']:
                        store=i
                        soup = store
                        final=soup.find('a')
                        break
                final=final['href']
                post_url=final
                i=len("../post.php?pd=")
                post_id = ''
                while i<len(final):
                    post_id += final[i]
                    i += 1
                postdata['post_id']=post_id
                list_url = 'https://www.teedindd.com/post.php?pd='
                list_url+=postdata['post_id']
                r = httprequestObj.http_get(list_url)
                soup = BeautifulSoup(r.content, 'html5lib')
                data=soup.find('input',attrs={'id':'ti'})
                if data =="":
                    time_end = datetime.datetime.utcnow()
                    time_usage = time_end - time_start
                    return {
                        "websitename": "teedindd",
                        "success": "false",
                        "detail" : "post not created",
                        "start_time": str(time_start),
                        "end_time": str(time_end),
                        'ds_id': postdata['ds_id'],
                        "post_url": '',
                        "post_id": '',
                    }
                j=1
                while j < len(postdata['post_images']):
                    # postdata['post_id']=post_id
                    postdata['no']=j
                    self.editpost(postdata)
                    j+=1
        else:
            post_url=""
            post_id=""
            detail = 'cannot login'
            success = "False"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "websitename": "teedindd",
            "success": success,
            "detail": success,
            "start_time": str(time_start),
            "ds_id": postdata['ds_id'],
            "end_time": str(time_end),
            "post_url": 'https://www.teedindd.com/property-detail.php?pd='+str(post_id),
            "post_id": post_id,
            'detail': detail
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
        flag=""

        if success == "true":
            post_title = postdata['post_title_th']
            # exists, authenticityToken, post_title = self.check_post(post_id)
            x=['1','2','3','4','5','6','7','8','9','10']
            for i in x:
                url = "https://www.teedindd.com/admin/index.php?page="+i    
                r = httprequestObj.http_get(url)
                exists = False
                soup = BeautifulSoup(r.content, 'html5lib')

                entry = soup.find('table')
                for title_row in entry.find_all('tr'):
                    if title_row is None:
                        continue
                    title_1 = title_row.find('td')
                    if title_1 is None:
                        continue
                    title = title_row.find_all('td')
                    if title is None:
                        continue
                    for title_2 in title_row.find_all('td'):
                        title_3=title_2.find('div')
                        if title_3 is None:
                            continue
                        title_3=title_2.text[1:-29]  
                        print(title_3)              
                        if post_title in title_3:
                            exists = True
                            post_id = title_1.text.strip()
                            post_url = "https://www.teedindd.com/property-detail.php?pd="+post_id
                            post_modify_time = "NOT SHOWED ON WEBSITE"
                            post_view = "NOT SHOWED ON WEBSITE"
                            post_found = "true"
                            detail = "post found successfully"
                            flag=1
                            break
                    if flag==1:
                        break                 
            if flag!=1:
                success = "false"
                detail = "No post found with given title."

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": "true",
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": "teedindd",
            "account_type":None,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "post_modify_time": post_modify_time,
            "post_view": post_view,
            "post_url": post_url,
            "post_found": post_found
        } 



    def edit_post(self,postdata):
        k=0
        while k<len(postdata['post_images']):
            postdata['no']=k
            j=self.editpost(postdata)
            k+=1
            if j['success']=="false":
                break
        if len(postdata['post_images'])==0:
            postdata['no']=0
            j=self.editpost(postdata)

        j['log_id'] = postdata['log_id']
        j['ds_id'] = postdata['ds_id']

        return j

    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        list_url = 'https://www.teedindd.com/post.php?pd='
        list_url+=postdata['post_id']
        r = httprequestObj.http_get(list_url)
        soup = BeautifulSoup(r.content, 'html5lib')
        var=soup.find('input',attrs={'id':'ti'})
        print(var)
        if var['value']=="":
            time_end = datetime.datetime.utcnow()
            time_usage = time_end - time_start
            return {
                "websitename": "teedindd",
                'ds_id': postdata['ds_id'],
                "success": 'false',
                "log_id": postdata['log_id'],
                "start_time": str(time_start),
                "end_time": str(time_end),
                "detail": 'Wrong Post id',
            }

        if success == "true":
            datapost = {
                'properties-delete':'1',
                'userDeleteProp':postdata['post_id']
            }
            r = httprequestObj.http_post('https://www.teedindd.com/admin/properties-process.php', data=datapost)
            data = r.text
            # print(data,'teedindd')
            if data == '':
                success = "false"
                detail = "Failed to Delete"

            else:
                detail = "Deleted"
        else:
            success = "false"
            detail="Failed Login"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "teedindd",
            "success": success,
                'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
        }


# obj = teedindd()
# postdata = {
#     'post_id':'298292',
#     'user': 'tirth.upadhyaya20012001@gmail.com',
#     'pass': 'temptemp',
#     'name': 'temp1234',
#     'name_th': 'temp1234',
#     'surname_th': 'temp1234',
#     'property_type': '2',
#     'mobile': '12345678',
#     'geo_latitude': '13',
#     'geo_longitude': '34',
#     'price_baht': '2123',
#     'post_title_th': 'DU',
#     'post_description_th': 'fasdfasdfasfasdgasd',
#     'listing_type': 'ffer',
#     'addr_province': 'ชลบุรี',
#     'addr_district': 'บางละมุง',
#     'addr_sub_district': 'นาเกลือ',
#     "addr_road": "ถนน",
#     "addr_soi": "ซอย",
#     "addr_near_by": "สถานที่ใกล้เคียง",
#     'post_images': ["download.jpeg",]
# }
# # print(obj.register_user(postdata))
# # print(obj.test_login(postdata))
# # print(obj.create_post(postdata))
# # print(obj.edit_post(postdata))
# # print(obj.delete_post(postdata))
# print(obj.boost_post(postdata))
'''
{"action": "edit_post", "timeout": "5", "post_img_url_lists": ["https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885__340.jpg"], "geo_latitude": "13.998983386212497", "geo_longitude": "99.74464029046142", "property_id": "", "post_title_th": "xYx", "short_post_title_th": "xxx", "post_description_th": "xxx", "post_title_en": "abcdaskjdfg", "short_post_title_en": "xxx", "post_description_en": "Editted with newline\r\nnewline\r\nnewline", "price_baht": 3000, "project_name": "projectnameisenetertedhere", "listing_type": "\u0e02\u0e32\u0e22", "property_type": 2, "floor_level": 2, "floor_total": "11", "floor_area": "11", "bath_room": 2, "bed_room": 3,"duration":30, "prominent_point": "\u0e08\u0e38\u0e14\u0e40\u0e14\u0e48\u0e19", "view_type ": "11", "direction_type": "11", "addr_province": "\u0e01\u0e32\u0e0d\u0e08\u0e19\u0e1a\u0e38\u0e23\u0e35", "addr_district": "\u0e17\u0e48\u0e32\u0e21\u0e30\u0e01\u0e32", "addr_sub_district": "\u0e15\u0e30\u0e04\u0e23\u0e49\u0e33\u0e40\u0e2d\u0e19", "addr_road": "", "addr_soi": "", "addr_near_by": "", "floorarea_sqm": 1234, "land_size_rai": 32, "land_size_ngan": 21, "land_size_wa": 12, "name": "xxx", "mobile": "xxx", "email": "xxx", "line": "xxx", "web": [{"ds_name": "teedindd", "ds_id": "4", "user": "wemica1039@farmdeu.com", "pass": "12345678", "post_id": "326914", "log_id": "444444"}]}
'''