# -*- coding: utf-8 -*-

from .lib_httprequest import *
from bs4 import BeautifulSoup
from .lib_captcha import *
import os.path
import re
import json
import datetime
import sys
import requests
import random


category_types = {
    '1': '1',
    '2': '5',
    '3': '5',    
    '4': '3',
    '5': '2',
    '6': '4',
    '7': '7',
    '8': '7',
    '9': '6',
    '10': '8',
    '25': '8'
}

httprequestObj = lib_httprequest()
captcha = lib_captcha()

class landmarket():
    name = 'landmarket'
    site_name = "https://xn--22c9abbmn4dva1jczk1w.com"

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

        # start process
        success = "false"
        detail = 'An Error has Occurred'
        
        datapost = {
            "username": postdata['user'].split('@')[0],
            "pass": postdata['pass'],
            "conpass": postdata['pass'],
            "email": postdata['user'],
            "name": postdata['name_th'],
            "lastname": postdata['surname_th'],
            "phone": postdata['tel'],
            "address": "no address",
            "submit": "" 
        }
        
        response = httprequestObj.http_post(self.site_name+'/signup_member.php', data=datapost)     
        if response.status_code==200:
            soup = BeautifulSoup(response.text, features=self.parser)
            if 'alert-success' in soup.find(class_='alert').get('class'):
                success = "true"
                detail = "User registered successfully!"
            else:
                detail =  "This email id is already in use"
        else:
            detail = "An error occurred with response code "+str(response.status_code)

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": self.name,
            "ds_id": postdata['ds_id']
        } 



    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        
        # start process
        success = "false"
        detail = 'An Error has Occurred'

        datapost = {
            "log_u": postdata['user'],
            "log_p": postdata['pass'],
            "submit": ""
        }

        response = httprequestObj.http_post(self.site_name+'/login.php', data=datapost)    
        if response.status_code==200:
            soup = BeautifulSoup(response.text, features=self.parser)
            if soup.find(class_='alert') and 'alert-danger' in soup.find(class_='alert').get('class'):
                detail =  "Invalid username or password"
            else:
                confirm = soup.find(class_='panel-body')
                if confirm.find('img') and confirm.find('img').get('src')=='images/loading.gif':
                    success = "true"
                    detail = "Logged in successfully!"        
        else:
            detail = "An error occurred with response code "+str(response.status_code)

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": self.name,
            "ds_id": postdata['ds_id']
        }



    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        # login

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = "Unable to create post"
        post_id = ""
        post_url = ""
        
        if 'web_project_name' not in postdata or postdata['web_project_name'] is None:
            if 'project_name' in postdata and postdata['project_name'] is not None:
                postdata['web_project_name'] = postdata['project_name']
            else:
                postdata['web_project_name'] = postdata['post_title_th'] 
        
        if success=="true":            
            success = "false"

            listing_type = 2
            if postdata['listing_type']=='ขาย':
                listing_type = 1

            addr_province = "".join(str(postdata['addr_province']).strip().split())
            addr_district = "".join(str(postdata['addr_district']).strip().split())
            addr_sub_district = "".join(str(postdata['addr_sub_district']).strip().split())
            province = '64'
            district = '864'
            subdistrict = '7785'
          
            with open('./static/landmarket_province.json') as f:
                province_data = json.load(f)

            for key in province_data["provinces"]:
                if (addr_province.find(str(key)) != -1) or (str(key).find(addr_province) != -1):
                    province = province_data["provinces"][key]
                    break
            for key in province_data["districts"][province]:
                if(addr_district.find(str(key)) != -1)  or (str(key).find(addr_district) != -1):
                    district = province_data["districts"][province][key]
                    break
            for key in province_data["subdistricts"][district]:
                if(addr_sub_district.find(str(key)) != -1)  or (str(key).find(addr_sub_district) != -1):
                    subdistrict = province_data["subdistricts"][district][key]
                    break

            area = str(postdata['floor_area'])+' sqm'
            if str(postdata['property_type'])!='1':
                if 'land_size_ngan' not in postdata or postdata['land_size_ngan']==None:
                    postdata['land_size_ngan'] = 0
                if 'land_size_rai' not in postdata or postdata['land_size_rai']==None:
                    postdata['land_size_rai'] = 0
                if 'land_size_wa' not in postdata or postdata['land_size_wa']==None:
                    postdata['land_size_wa'] = 0
                try:
                    postdata['land_size_ngan'] = int(postdata['land_size_ngan'])
                except ValueError:
                    postdata['land_size_ngan'] = 0
                try:
                    postdata['land_size_rai'] = int(postdata['land_size_rai'])
                except ValueError:
                    postdata['land_size_rai'] = 0
                try:
                    postdata['land_size_wa'] = int(postdata['land_size_wa'])
                except ValueError:
                    postdata['land_size_wa'] = 0
                area = str(400 * postdata['land_size_rai'] + 100 * postdata['land_size_ngan'] + postdata['land_size_wa'])+' sqw'
            
            datapost = {
                "name": str(postdata['post_title_th']),
                "cate": listing_type,
                "section": category_types[str(postdata['property_type'])],
                "Province": province,
                "District": district,
                "Subdistrict": subdistrict,
                "price": postdata['price_baht'],
                "area": area,
                "detail": postdata['post_description_th'],
                "username": postdata['name'],
                "tel": postdata['mobile'],
                "email": postdata['email'],
                "line": postdata['line'],
                "pass": postdata['email'],
                "Submit": "เพิ่มข้อมูลประกาศ"
            }

            files = {'image1': b'', 'image2': b'', 'image3': b'', 'image4': b''}
            for i, image in enumerate(postdata['post_images'][:4]):
                files['image'+str(i+1)] =  open(os.getcwd()+"/"+image, 'rb')
            
            r = httprequestObj.http_get(self.site_name+'/post')
            if r.status_code==200:
                soup = BeautifulSoup(r.text, features=self.parser)
                flag = True
                code_input = soup.find('input', attrs={'name': 'code'})
                if code_input:
                    captcha_img = self.site_name+'/'+code_input.findNext('img').get('src')
                    g_response = captcha.image_captcha(captcha_img)
                    if g_response!=0:
                        datapost['code'] = g_response
                    else:
                        flag = False
                        detail = "Image captcha error"
                
                if flag:
                    response = httprequestObj.http_post(self.site_name+'/add_property.php', data=datapost, files=files)
                    if response.status_code==200:
                        soup = BeautifulSoup(response.text, features=self.parser)
                        if 'alert-success' in soup.find(class_='alert').get('class'):
                            success = "true"
                            detail = "Post created successfully!"

                            post_title = str(postdata['post_title_th']).strip()
                            r = httprequestObj.http_get(self.site_name+'/maneg_property.php')
                            if r.status_code==200:
                                soup = BeautifulSoup(r.text, features=self.parser)
                                posts_element = soup.find(class_='well')
                                
                                if posts_element and posts_element.find('tbody'):
                                    posts = posts_element.find('tbody').find_all('tr')
                                    for post in posts:
                                        title = post.find_all('td')[1].a
                                        if title.getText().strip()==post_title:
                                            post_url = title.get('href')
                                            post_id = post_url.split('-')[-1].replace('.html','')
                                            break
                            else:
                                detail += ' But an error occurred while fetching post details with response code'+str(r.status_code)
                    else:
                        detail = 'An Error has occurred with response_code '+str(response.status_code)
            else:
                detail = 'An Error has occurred while fetching page, with response_code '+str(r.status_code)
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
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
            "websitename": self.name
        }

    

    def edit_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        # login

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = "Unable to update post"
        post_id = ""
        post_url = ""

        if 'web_project_name' not in postdata or postdata['web_project_name'] is None:
            if 'project_name' in postdata and postdata['project_name'] is not None:
                postdata['web_project_name'] = postdata['project_name']
            else:
                postdata['web_project_name'] = postdata['post_title_th']

        if success=="true":
            success = "false"
            
            listing_type = 2
            if postdata['listing_type']=='ขาย':
                listing_type = 1

            addr_province = "".join(str(postdata['addr_province']).strip().split())
            addr_district = "".join(str(postdata['addr_district']).strip().split())
            addr_sub_district = "".join(str(postdata['addr_sub_district']).strip().split())
            province = '64'
            district = '864'
            subdistrict = '7785'
          
            with open('./static/landmarket_province.json') as f:
                province_data = json.load(f)

            for key in province_data["provinces"]:
                if (addr_province.find(str(key)) != -1) or (str(key).find(addr_province) != -1):
                    province = province_data["provinces"][key]
                    break
            for key in province_data["districts"][province]:
                if(addr_district.find(str(key)) != -1)  or (str(key).find(addr_district) != -1):
                    district = province_data["districts"][province][key]
                    break
            for key in province_data["subdistricts"][district]:
                if(addr_sub_district.find(str(key)) != -1)  or (str(key).find(addr_sub_district) != -1):
                    subdistrict = province_data["subdistricts"][district][key]
                    break

            area = str(postdata['floor_area'])+' sqm'
            if str(postdata['property_type'])!='1':
                if 'land_size_ngan' not in postdata or postdata['land_size_ngan']==None:
                    postdata['land_size_ngan'] = 0
                if 'land_size_rai' not in postdata or postdata['land_size_rai']==None:
                    postdata['land_size_rai'] = 0
                if 'land_size_wa' not in postdata or postdata['land_size_wa']==None:
                    postdata['land_size_wa'] = 0
                try:
                    postdata['land_size_ngan'] = int(postdata['land_size_ngan'])
                except ValueError:
                    postdata['land_size_ngan'] = 0
                try:
                    postdata['land_size_rai'] = int(postdata['land_size_rai'])
                except ValueError:
                    postdata['land_size_rai'] = 0
                try:
                    postdata['land_size_wa'] = int(postdata['land_size_wa'])
                except ValueError:
                    postdata['land_size_wa'] = 0
                area = str(400 * postdata['land_size_rai'] + 100 * postdata['land_size_ngan'] + postdata['land_size_wa'])+' sqw'
            
            datapost = {
                "name": str(postdata['post_title_th']),
                "cate": listing_type,
                "section": category_types[str(postdata['property_type'])],
                "Province": province,
                "District": district,
                "Subdistrict": subdistrict,
                "price": postdata['price_baht'],
                "area": area,
                "tag": "",
                "detail": postdata['post_description_th'],
                "username": postdata['name'],
                "tel": postdata['mobile'],
                "email": postdata['email'],
                "line": postdata['line'],
                "pass": postdata['email'],
                "ID": str(postdata['post_id']),
                "Submit": "แก้ไขข้อมูลประกาศ"
            }

            files = {'image1': b'', 'image2': b'', 'image3': b'', 'image4': b''}
            for i, image in enumerate(postdata['post_images'][:4]):
                files['image'+str(i+1)] =  open(os.getcwd()+"/"+image, 'rb')
            
            r = httprequestObj.http_get(self.site_name+'/edit_property.php?id='+str(postdata['post_id']))
            if r.status_code==200:
                soup = BeautifulSoup(r.text, features=self.parser)
                flag = True
                code_input = soup.find('input', attrs={'name': 'code'})
                if code_input:
                    captcha_img = self.site_name+'/'+code_input.findNext('img').get('src')
                    g_response = captcha.image_captcha(captcha_img)
                    if g_response!=0:
                        datapost['code'] = g_response
                    else:
                        flag = False
                        detail = "Image captcha error"

                if flag:
                    response = httprequestObj.http_post(self.site_name+'/edit_property.php?id='+str(postdata['post_id']), data=datapost, files=files)
                    if response.status_code==200:
                        soup = BeautifulSoup(response.text, features=self.parser)
                        if 'alert-success' in soup.find(class_='alert').get('class'):
                            success = "true"
                            detail = "Post updated successfully!"
                    else:
                        detail = 'An Error has occurred with response_code '+str(response.status_code)
        else:
            detail = "cannot login"
        
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_id": postdata['post_id'],
            "log_id": postdata['log_id'],
            "account_type": "null",
            "detail": detail,
            "websitename": self.name,
            "ds_id": postdata['ds_id']
        }



    def search_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        post_url = ""
        post_id = ""
        post_found = ""
        post_modify_time = ""
        post_create_time = ""
        post_view = ""

        if success == "true":
            post_found = "false"
            detail = "No post found with given title"
            post_title = " ".join(str(postdata['post_title_th']).strip().split())
            
            page_num = 0
            flag = True
            while flag:
                response = httprequestObj.http_get(self.site_name+'/maneg_property.php?&page='+str(page_num))
                if response.status_code==200:
                    soup = BeautifulSoup(response.text, features=self.parser)
                    posts_element = soup.find(class_='well')             
                    
                    if posts_element and posts_element.find('tbody'): 
                        posts = posts_element.find('tbody').find_all('tr')
                        if len(posts)<10:
                            flag = False
                        for post in posts:
                            title = post.find_all('td')[1].a
                            title_text = " ".join(title.getText().strip().split())
                            print(title_text)
                            print(post_title)
                            print(title_text==post_title)
                            if title_text==post_title:
                                post_found = "true"
                                detail = "Post found successfully"
                                post_url = title.get('href')
                                post_id = post_url.split('-')[-1].replace('.html','')
                                post_view = title.findNext('p').getText().strip().split()[0]
                                break
                    else:
                        break
                page_num += 1
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
            "websitename": self.name,
            "account_type": None,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "post_create_time": post_create_time,
            "post_modify_time": post_modify_time,
            "post_view": post_view,
            "post_url": post_url,
            "post_found": post_found
        }



    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = "Unable to delete post"

        if success=="true":
            success = "false"

            response = httprequestObj.http_get(self.site_name+'/maneg_property.php?delete='+str(postdata['post_id']))
            if response.status_code==200:
                soup = BeautifulSoup(response.text, features=self.parser)
                alert_element = soup.find(class_='alert')
                if alert_element:
                    if 'alert-success' in alert_element.get('class'):
                        success = "true"
                        detail = "Post deleted successfully!"
                else:
                    detail = "No post found with given id"
            else:
                detail = 'An Error has occurred with response_code '+str(response.status_code)
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
            "websitename": self.name,
            "post_id": postdata['post_id'],
            "log_id": postdata['log_id'],
            "ds_id": postdata['ds_id']
        }



    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        
        if success=="true":
            success = "false"
            detail = "Unable to boost post"

            datapost = {}
            files = {'image1': b'', 'image2': b'', 'image3': b'', 'image4': b''}

            r = httprequestObj.http_get(self.site_name+'/edit_property.php?id='+str(postdata['post_id']))
            if r.status_code==200:
                soup = BeautifulSoup(r.text, features=self.parser)
                inputs_list = ["name", "cate", "section", "Province", "District", "Subdistrict",
                "price", "area", "tag", "detail", "username", "tel", "email", "line", "ID", "Submit"]

                for name in inputs_list:
                    inputs = soup.find_all(attrs={'name': name})
                    for inp in inputs:
                        if inp.name=='input':
                            if inp.get('type') in ['text', 'password', 'email', 'number', 'hidden', 'submit']: 
                                datapost[name] = inp.get('value')
                            elif inp.get('type')=='radio'and inp.get('checked')=='checked':
                                datapost[name] = inp.get('value')
                        elif inp.name=='select':
                            option = inp.find_all('option', selected=True)
                            if option:
                                datapost[name] = option[-1].get('value')
                            else:
                                datapost[name] = inp.find('option').get('value')
                        elif inp.name=='textarea':
                            datapost[name] = inp.getText()
                datapost["pass"] = postdata['user']
                
                flag = True
                code_input = soup.find('input', attrs={'name': 'code'})
                if code_input:
                    captcha_img = self.site_name+'/'+code_input.findNext('img').get('src')
                    g_response = captcha.image_captcha(captcha_img)
                    if g_response!=0:
                        datapost['code'] = g_response
                    else:
                        flag = False
                        detail = "Image captcha error"

                if flag:
                    response = httprequestObj.http_post(self.site_name+'/edit_property.php?id='+str(postdata['post_id']), data=datapost, files=files)
                    if response.status_code==200:
                        soup = BeautifulSoup(response.text, features=self.parser)
                        if 'alert-success' in soup.find(class_='alert').get('class'):
                            success = "true"
                            detail = "Post boosted successfully!"
                    else:
                        detail = 'An Error has occurred with response_code '+str(response.status_code)
            else:
                detail = 'An Error has occurred while fetching page, with response_code '+str(r.status_code)
        else:
            detail = "Cannot login"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "post_id": postdata['post_id'],
            "log_id": postdata['log_id'],
            "websitename": self.name,
            "ds_id": postdata['ds_id']
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
