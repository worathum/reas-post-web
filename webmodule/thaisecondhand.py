# -*- coding: utf-8 -*-

from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
# from urlparse import urlparse
import re
import json
import datetime
import sys
from urllib.parse import unquote
import os
import random


httprequestObj = lib_httprequest()

# with open("./static/ips.txt",'r') as f:
#     allips = f.read()
# ips = allips.split('\n')

# username = ips[random.randint(0,len(ips)-2)].split(":")[2]
# password = 'v1y3mbh26qk9'
# port = 22225
# super_proxy_url = ('http://%s:%s@zproxy.lum-superproxy.io:%d' %
#         (username, password, port))

# proxy_handler = {
#     'http': super_proxy_url,
#     'https': super_proxy_url,
# }

# httprequestObj.session.proxies.update(proxy_handler)



class thaisecondhand():

    name = 'thaisecondhand'

    def __init__(self):

        try:
            import configs
        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.primarydomain = 'http://www.thaisecondhand.com/'
        self.debug = 0
        self.debugresdata = 0
        self.parser = 'html.parser'
        self.max_image = 6

    def register_user(self, userdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()
        httprequestObj.http_get('https://www.thaisecondhand.com/logout', verify=False)
        # print("here in register")

        email = userdata['user']
        passwd = userdata['pass']
        
        datapost={
            'email': email,
            'birthdate_year': '1999',
            'birthdate_month': '1',
            'birthdate_day': '1',
            'gender': 'Male',
            'password': passwd,
            'confirmpassword': passwd,
            'confirm_username': "",
            'f_confirm': "Y",
            
            'registraion-submit': "Become a member"
        }

        r = httprequestObj.http_get('https://www.thaisecondhand.com/register')
        data = r.text
        soup = BeautifulSoup(data, self.parser)
        authenticityToken = soup.find("input", {"name": "csrf_token"})['value']
        datapost['csrf_token'] = authenticityToken
        r = httprequestObj.http_post('https://www.thaisecondhand.com/register/submit', data = datapost)
        data = r.text
        matchobj = matchObj = re.search(r'alert-success', data)
        # print(matchObj)
        if matchObj:
            success = "True"
            detail = "Successful Registration"
        else:
            success = "False"
            detail = "Registration Unsuccessful"
        end_time = datetime.datetime.utcnow()
        time_usage = end_time - start_time
        return {
            "websitename": "thaisecondhand",
            "success": success,
            "start_time": str(start_time),
            'ds_id': userdata['ds_id'],
            "end_time": str(end_time),
            "detail": detail
        }

    def test_login(self, logindata):
        # print("Here in test_login")
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()

        email_user = logindata['user']
        email_pass = logindata['pass']



        httprequestObj.http_get('https://www.thaisecondhand.com/logout', verify=False)
        r = httprequestObj.http_get('https://www.thaisecondhand.com/login', verify=False)
        # r = httprequestObj.http_get_with_headers('https://www.thaisecondhand.com/login', verify=False, proxies=proxy_handler)
        data = r.text
        # print(data)
        soup = BeautifulSoup(data, self.parser)
        csrf = soup.find("input", {"name": "csrf_token"})['value']
        
        
        datapost = {
            'username' : email_user,
            'password' : email_pass,
            'registration-submit' : 'Login',
            'csrf_token' : csrf
        }
        # print(datapost)
        r = httprequestObj.http_post('https://www.thaisecondhand.com/member/login_submit', data=datapost)
        data = r.text
        # print(data)
        # print("Data Printed")
        matchObj = re.search(r'/logout', data)
        # print(matchObj)
        if matchObj:
            success = "True"
            detail = "Sucessful Login"
        else:
            success = "False"
            detail = "Login Unsucessful"
        end_time = datetime.datetime.utcnow()
        time_usage = end_time - start_time
        
        return {
            "websitename": "thaisecondhand",
            "success": success,
            "ds_id": logindata['ds_id'],
            "start_time": str(start_time),
            "end_time": str(end_time),
            "detail": detail,
        }
        #
        #
        #
    
    def create_post(self, postdata):
        # https://www.thaisecondhand.com/post/get_json_district?province_id=13   ->     for district
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()
        # print(postdata)
        # postdata = postdata
        #print(self.max_image)
        listing_type = postdata['listing_type']
        property_type = postdata['property_type']
        post_img_url_lists = postdata['post_img_url_lists']
        price_baht = postdata['price_baht']
        addr_province = postdata['addr_province']
        addr_district = postdata['addr_district']
        # addr_sub_district = postdata['addr_sub_district']
        # addr_road, addr_near_by, floorarea_sqm = ['','','']
        # if 'addr_road' in postdata:
            # addr_road = postdata['addr_road']
        # if 'addr_near_by' in postdata:
            # addr_near_by = postdata['addr_near_by']
        # if 'floorarea_sqm' in postdata:
            # floorarea_sqm = postdata['floorarea_sqm']
        
        geo_latitude = postdata['geo_latitude']
        geo_longitude = postdata['geo_longitude']
        property_id = postdata['property_id']
        post_title_th = postdata['post_title_th']
        post_description_th = postdata['post_description_th']
        # post_title_en = postdata['post_title_en']
        # post_description_en = postdata['post_description_en']
        # floor_no = postdata['floor_level']
        # bedroom = postdata['bed_room']
        # bathroom = postdata['bath_room']
        # ds_id = postdata["ds_id"]
        name = postdata["name"]
        mobile = postdata["mobile"]
        email = postdata["email"]
        # account_type = postdata["account_type"]
        user = postdata["user"]
        password = postdata["pass"]
        # project_name = postdata["project_name"]
        land_size_rai = postdata['land_size_rai']
        land_size_ngan = postdata['land_size_ngan']
        land_size_wah = postdata['land_size_wa']
        # post_description_en =  post_description_en.replace("\r\n","<br>")
        post_description_th =  post_description_th.replace("\r\n","<br>")
        post_description_th =  post_description_th.replace("\n","<br>")
        
        #print(post_description_th)
        list_dict = {'ขาย' : 1, 'ซื้อ':2,'แจกฟรี':6,'เช่า':9,'บริการ':16}
        province = {}
        with open('./static/thaisecondhand_province.json',encoding='utf-8') as f:
            province = json.load(f)
        # print(addr_province)
        # print(province[addr_province])
        datapost = {
           "cat_path" : "" ,#yet to be decided what to do, need to check
           "cat_id" : "" ,# default for Real_Estate -> Others
            "type":list_dict[listing_type],
            "title":post_title_th,
            "detail":post_description_th,
            "price":price_baht,
            "status":2,#default value
            "status_year":0, #not valid fro real estate
            "status_month":0,#not valid fro real estate
            "keywords": "Default", #default value
            "due_date":7, #default value
            "name":name,
            "email":email,
            "mobile_number":mobile,
            "province_id":province[addr_province],
            "province_name":addr_province,
            "district_id":"",
            "acception":"on",
            "csrf_token":"",
        }    
        print(property_type)
        if(property_type == "ที่ดิน" or property_type == "6"):# land
            datapost["cat_id"] = "2127" # Defaults land type to other of the four option
            datapost["cat_path"] = "อสังหาริมทรัพย์ > ที่ดิน > ที่ดินเปล่า"
        elif(property_type == "คอนโดมีเนียม"or property_type == "1"): # condo
            datapost["cat_id"] = "2119" 
            datapost["cat_path"] = "อสังหาริมทรัพย์ > บ้าน อาคารพาณิชย์ > คอนโดมีเนียม"
        elif(property_type == "บ้าน"or property_type == "2" or property_type == "3"): #house
            datapost["cat_id"] = "2117" 
            datapost["cat_path"] = "อสังหาริมทรัพย์ > บ้าน อาคารพาณิชย์ > บ้าน"
        elif(property_type == "ทาวน์เฮ้าส์"or property_type == "4"): # townhouses
            datapost["cat_id"] = "2118" 
            datapost["cat_path"] = "อสังหาริมทรัพย์ > บ้าน อาคารพาณิชย์ > ทาวน์เฮ้าส์"
        elif(property_type == "ตึกแถว"or property_type == "5"): # commercial building
            print("here here")
            datapost["cat_id"] = "5736" 
            datapost["cat_path"] = "อสังหาริมทรัพย์ > บ้าน อาคารพาณิชย์ > ตึกแถว"
        elif(property_type == "อพาร์ทเม้นต์"or property_type == "7"): # Apartment
            datapost["cat_id"] = "2122" 
            datapost["cat_path"] = "อสังหาริมทรัพย์ > บ้าน อาคารพาณิชย์ > อพาร์ทเม้นต์"
        elif(property_type == "สำนักงานต์"or property_type == "9"): # office
            datapost["cat_id"] = "2116" 
            datapost["cat_path"] = "อสังหาริมทรัพย์ > บ้าน อาคารพาณิชย์ > สำนักงาน"
        elif(property_type == "โรงงาน"or property_type == "25"): # factory
            datapost["cat_id"] = "2121" 
            datapost["cat_path"] = "อสังหาริมทรัพย์ > บ้าน อาคารพาณิชย์ > โรงงาน"
        elif(property_type == "โรงงาน"or property_type == "10"): # warehouse
            datapost["cat_id"] = "5739" 
            datapost["cat_path"] = "อสังหาริมทรัพย์ > บ้าน อาคารพาณิชย์ > โกดัง"    
        else:
            datapost["cat_id"] = "2131" 
            datapost["cat_path"] = "อสังหาริมทรัพย์ > อื่นๆ"
        # login
        login = self.test_login(postdata)
        success = login["success"]
        detail = login["detail"]
        post_id = ""
        post_url = ""
        filestoup = {}
        numdict = {1:"first",2:"second",3:"third",4:"fourth",5:"fifth",6:"sixth"}
        # print("postimages",postdata['post_images'])
        for i in range(len(postdata['post_images'][:self.max_image])):
            filestoup['images_'+str(i+1)] = open(os.getcwd() + "/"+ postdata['post_images'][i],'rb')
            datapost[numdict[i+1] + "_images_status"] = "1"
        # print(datapost["first"])
        # print("debug")
        # print(filestoup)
        if(success == "True"):
            # print("debug2")
            r = httprequestObj.http_get('https://www.thaisecondhand.com/post', verify=False)
            data = r.text
            soup = BeautifulSoup(data, self.parser)
            authenticityToken = soup.find("input", {"name": "csrf_token"})['value']
            datapost['csrf_token'] = authenticityToken
            r = httprequestObj.http_get('https://www.thaisecondhand.com/post/get_json_district?province_id='+str(datapost["province_id"]), verify=False)
            data = r.json()
            for key in data:
                if(addr_district.find(data[key]["name"]["thai"]) != -1):
                    datapost["district_id"] = key
                    break
            r = httprequestObj.http_post('https://www.thaisecondhand.com/post/submit', data = datapost,files=filestoup)#/property/show
            #print(r)
            data = r.text
            #print(data)
            link = re.findall(r'https://www.thaisecondhand.com/product/\d+',data)
            # print("printing link",link)
            if len(link) == 0:
                success = "False"    
                detail = "Cannot post to Thai second hand"
                while self.max_image > 1:
                    self.max_image -= 1               
                    r = httprequestObj.http_get('https://www.thaisecondhand.com/logout')
                    return(self.create_post(postdata))
                    # del datapost[numdict[self.max_image] + "_images_status"]
                    # del filestoup['images_' + str(self.max_image)]
                    # r = httprequestObj.http_get('https://www.thaisecondhand.com/post', verify=False)
                    # data = r.text
                    # soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
                    # authenticityToken = soup.find("input", {"name": "csrf_token"})['value']
                    # datapost['csrf_token'] = authenticityToken
                    # print(datapost)
                    # print(filestoup)
                    # r = httprequestObj.http_post('https://www.thaisecondhand.com/post/submit', data = datapost,files=filestoup)#/property/show
                    # data = r.text
                    # print("REDO", data)
                    # link = re.findall(r'https://www.thaisecondhand.com/product/\d+',data)
                    # if(len(link) != 0):
                    #     post_id = re.findall(r'\d+',link[0])[0]
                    #     post_url = link
                    #     success = "True"
                    #     detail = "Posted with lesser image " + str(self.max_image - 1) 
                    break  
            else:
                post_id = re.findall(r'\d+',link[0])[0]
                post_url = link[0] 
        
        end_time = datetime.datetime.utcnow()
        print({
            "websitename": "thaisecondhand",
            "success": success,
            "time_usage": end_time - start_time,
            "start_time": start_time,
            "end_time": end_time,
            # "ds_id": "4",
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "",
            "detail": detail
        }
)
        return {
            "websitename": "thaisecondhand",
            "success": success,
            "time_usage": end_time - start_time,
            "start_time": start_time,
            "end_time": end_time,
            "ds_id": postdata['ds_id'],
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "",
            "detail": detail
        }

    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()

        post_id = postdata['post_id']
        log_id = postdata['log_id']
        email_user = postdata['user']
        email_pass = postdata['pass']
        #https://www.thaisecondhand.com/member
        #
        #
        #
        datapost = {
            "product_id" : post_id
        }
        login = self.test_login(postdata)
        success = login["success"]
        detail = login["detail"]
        if(success == "True"):
            r = httprequestObj.http_get('https://www.thaisecondhand.com/member', verify=False)
            data = r.text
            #print(data)
            csrf = re.findall(r'csrf_token:"\w+',data)
            datapost["csrf_token"] = csrf[0].replace("csrf_token:\"", "")
            if(re.search(r''+post_id,data)):
                r = httprequestObj.http_post('https://www.thaisecondhand.com/member/product_postpone', data=datapost)
                if r.status_code != 200:
                    success = "False"
                    detail = "Cannot boost post with id"+post_id
                else:
                    success = "True"
                    detail = "Post sucessfully boosted"
            else:
                success = "False"
                detail = "Wrong Post ID"
                                    
                
            #print(datapost)
        end_time = datetime.datetime.utcnow()
        return {
            "websitename": "thaisecondhand",
            "success": success ,
            "ds_id": postdata['ds_id'],
            "time_usage": end_time - start_time,
            "start_time": start_time,
            "end_time": end_time,
            "detail": detail,
            "log_id": log_id,
            "post_id": post_id

        }

    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()
        
        datapost = {}
        login = self.test_login(postdata)
        success = login["success"]
        detail = login["detail"]
        post_id = postdata['post_id']
        post_url = 'https://www.thaisecondhand.com/product/'+post_id
        if(success == "True"):
            # print()
            r = httprequestObj.http_get(post_url)
            data = r.text
            if (re.search('ขออภัยค่ะ หน้าที่คุณเปิดไม่อยู่ในระบบ', data)):
                end_time = datetime.datetime.utcnow()
                return {
                    "websitename": "thaisecondhand",
                    "success": "False",
                    "time_usage": end_time - start_time,
                    "start_time": start_time,
                    "end_time": end_time,
                    # "ds_id": "4",
                    "post_url": post_url,
                    "post_id": post_id,
                    "account_type": "",
                    "detail": "Post_id Invalid"
                }
            datapost['product_id'] = post_id
            r = httprequestObj.http_get('https://www.thaisecondhand.com/member')
            data = r.text
            csrf_token = re.findall(r'csrf_token:"\w+',data)[0]
            csrf_token = csrf_token.replace('csrf_token:"',"")
            # print(csrf_token)
            datapost['csrf_token'] = csrf_token
            # print(postdata)
            r = httprequestObj.http_post('https://www.thaisecondhand.com/member/product_remove',data=datapost)#/property/show
            data = r.text
            # print(data)
            # print(r.status_code)
            if r.status_code != 200:
                success = "False"
                detail = "Cannot delete post with id"+post_id
            else:
                success = "True"
                detail = "Post sucessfully deleted"

        #
        #
        #

        end_time = datetime.datetime.utcnow()
        return {
            "websitename": "thaisecondhand",
            "success": success,
            "ds_id": postdata['ds_id'],
            "time_usage": end_time - start_time,
            "start_time": start_time,
            "end_time": end_time,
            "detail": detail,
            "log_id": postdata['log_id']
        }
    
    def edit_post(self, postdata):
        # https://www.thaisecondhand.com/post/get_json_district?province_id=13   ->     for district
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()
        # print(postdata)
        # postdata = postdata
        listing_type = postdata['listing_type']
        property_type = postdata['property_type']
        # post_img_url_lists = postdata['post_img_url_lists']
        price_baht = postdata['price_baht']
        addr_province = postdata['addr_province']
        addr_district = postdata['addr_district']
        # addr_sub_district = postdata['addr_sub_district']
        # addr_road = postdata['addr_road']
        # addr_near_by = postdata['addr_near_by']
        # floorarea_sqm = postdata['floorarea_sqm']
        geo_latitude = postdata['geo_latitude']
        geo_longitude = postdata['geo_longitude']
        property_id = postdata['property_id']
        post_title_th = postdata['post_title_th']
        post_description_th = postdata['post_description_th']
        # post_title_en = postdata['post_title_en']
        # post_description_en = postdata['post_description_en']
        # floor_no = postdata['floor_level']
        # bedroom = postdata['bed_room']
        # bathroom = postdata['bath_room']
        # ds_id = postdata["ds_id"]
        name = postdata["name"]
        mobile = postdata["mobile"]
        email = postdata["email"]
        # account_type = postdata["account_type"]
        user = postdata["user"]
        password = postdata["pass"]
        # project_name = postdata["project_name"]
        land_size_rai = postdata['land_size_rai']
        land_size_ngan = postdata['land_size_ngan']
        land_size_wah = postdata['land_size_wa']
        # post_description_en =  post_description_en.replace("\r\n","<br>")
        post_description_th =  post_description_th.replace("\r\n","<br>")
        post_description_th =  post_description_th.replace("\n","<br>")
        print(post_description_th)
        list_dict = {'ขาย' : 1, 'ซื้อ':2,'แจกฟรี':6,'เช่า':9,'บริการ':16}
        province = {}
        
        with open('./static/thaisecondhand_province.json',encoding='utf-8') as f:
            province = json.load(f)
        datapost = {
           "cat_path" : "" ,#yet to be decided what to do, need to check
           "cat_id" : "" ,# default for Real_Estate -> Others
            "type":list_dict[listing_type],
            "title":post_title_th,
            "detail":post_description_th,
            "price":price_baht,
            "status":2,#default value
            "status_year":0, #not valid fro real estate
            "status_month":0,#not valid fro real estate
            "keywords": "Default", #default value
            "product_id":postdata["post_id"],
            "name":name,
            "email":email,
            "mobile_number":mobile,
            "province_id":province[addr_province],
            "province_name":addr_province,
            "district_id":"",
            "acception":"on",
            "csrf_token":"",
        }    
        print(property_type)
        if(property_type == "ที่ดิน" or property_type == 6):# land
            datapost["cat_id"] = "2127" # Defaults land type to other of the four option
            datapost["cat_path"] = "อสังหาริมทรัพย์ > ที่ดิน > ที่ดินเปล่า"
        elif(property_type == "คอนโดมีเนียม"or property_type == 1): # condo
            datapost["cat_id"] = "2119" 
            datapost["cat_path"] = "อสังหาริมทรัพย์ > บ้าน อาคารพาณิชย์ > คอนโดมีเนียม"
        elif(property_type == "บ้าน"or property_type == 2):
            datapost["cat_id"] = "2117" 
            datapost["cat_path"] = "อสังหาริมทรัพย์ > บ้าน อาคารพาณิชย์ > บ้าน"
        elif(property_type == "ทาวน์เฮ้าส์"or property_type == 4): # townhouses
            datapost["cat_id"] = "2118" 
            datapost["cat_path"] = "อสังหาริมทรัพย์ > บ้าน อาคารพาณิชย์ > ทาวน์เฮ้าส์"
        elif(property_type == 5): # commercial building
            print("Here here")
            datapost["cat_id"] = "5736" 
            datapost["cat_path"] = "อสังหาริมทรัพย์ > บ้าน อาคารพาณิชย์ > ตึกแถว"
        elif(property_type == "อพาร์ทเม้นต์"or property_type == 7): # Apartment
            datapost["cat_id"] = "2122" 
            datapost["cat_path"] = "อสังหาริมทรัพย์ > บ้าน อาคารพาณิชย์ > อพาร์ทเม้นต์"
        elif(property_type == "สำนักงานต์"or property_type == 9): # office
            datapost["cat_id"] = "2116" 
            datapost["cat_path"] = "อสังหาริมทรัพย์ > บ้าน อาคารพาณิชย์ > สำนักงาน"
        elif(property_type == "โรงงาน"or property_type == 25): # factory
            datapost["cat_id"] = "2121" 
            datapost["cat_path"] = "อสังหาริมทรัพย์ > บ้าน อาคารพาณิชย์ > โรงงาน"
        elif(property_type == "โรงงาน"or property_type == 10): # warehouse
            datapost["cat_id"] = "5739" 
            datapost["cat_path"] = "อสังหาริมทรัพย์ > บ้าน อาคารพาณิชย์ > โกดัง"    
        else:
            datapost["cat_id"] = "2131" 
            datapost["cat_path"] = "อสังหาริมทรัพย์ > อื่นๆ"
        # login
        login = self.test_login(postdata)
        success = login["success"]
        detail = login["detail"]
        post_id = postdata["post_id"]
        post_url = 'https://www.thaisecondhand.com/product/'+post_id
        filestoup = {}
        numdict = {1:"first",2:"second",3:"third",4:"fourth",5:"fifth",6:"sixth"}
        # print("postimages",postdata['post_images'])
        for i in range(len(postdata['post_images'][:6])):
            filestoup['images_'+str(i+1)] = open(os.getcwd() + "/"+ postdata['post_images'][i],'rb')
            datapost[numdict[i+1] + "_images_status"] = "1"
        # print(datapost["first"])
        # print("debug")
        # print(filestoup)
        if(success == "True"):
            # print("debug2")
            r = httprequestObj.http_get(post_url)
            data = r.text
            if (re.search('ขออภัยค่ะ หน้าที่คุณเปิดไม่อยู่ในระบบ', data)):
                end_time = datetime.datetime.utcnow()
                return {
                    "websitename": "thaisecondhand",
                    "success": "False",
                    "time_usage": end_time - start_time,
                    "start_time": start_time,
                    "end_time": end_time,
                    "ds_id": postdata['ds_id'],
                    "log_id": postdata['log_id'],
                    "post_url": post_url,
                    "post_id": post_id,
                    "account_type": "",
                    "detail": "Post_id Invalid"
                }
            r = httprequestObj.http_get('https://www.thaisecondhand.com/post/edit/'+post_id, verify=False)
            data = r.text
            soup = BeautifulSoup(data, self.parser)
            authenticityToken = soup.find("input", {"name": "csrf_token"})['value']
            print(authenticityToken)
            datapost['csrf_token'] = authenticityToken
            r = httprequestObj.http_get('https://www.thaisecondhand.com/post/get_json_district?province_id='+str(datapost["province_id"]), verify=False)
            data = r.json()
            # print(data)
            for key in data:
                if(addr_district.find(data[key]["name"]["thai"]) != -1):
                    datapost["district_id"] = key
                    break
            print(datapost)
            r = httprequestObj.http_post('https://www.thaisecondhand.com/post/edit_submit', data = datapost,files=filestoup)#/property/show
            data = r.text
            print(data)
            link = re.findall(r'แก้ไขประกาศเรียบร้อยแล้วค่ะ',data)
            # print("printing link",link)
            if len(link) == 0:
                success = "False"
                detail = "Cannot edit to Thai second hand"
            else:
                success = "True"
                detail = "Edit post successful"
        

        end_time = datetime.datetime.utcnow()
        
        print({
            "websitename": "thaisecondhand",
            "success": success,
            "time_usage": end_time - start_time,
            "start_time": start_time,
            "end_time": end_time,
            # "ds_id": "4",
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "",
            "detail": detail
        })
        
        return {
            "websitename": "thaisecondhand",
            "success": success,
            "ds_id": postdata['ds_id'],
            "time_usage": end_time - start_time,
            "start_time": start_time,
            "end_time": end_time,
            "log_id": postdata['log_id'],
            "post_url": post_url[0],
            "post_id": post_id,
            "account_type": "",
            "detail": detail
        }

    def search_post(self,postdata):
        start_time = datetime.datetime.utcnow()

        login = self.test_login(postdata)
        post_found = "False"
        post_id = ''
        post_url = ''
        post_view = ''
        post_modify_time = ''
        post_create_time = ''
        detail = 'No post with this title'
        title = ''
        if (login['success'] == 'True'):

            
            all_posts_url = 'https://www.thaisecondhand.com/member'

            all_posts = httprequestObj.http_get(all_posts_url)

            page = BeautifulSoup(all_posts.content, features = "html5lib")

            print(page)
            divi = page.find('div', attrs = {'class':'list-post'})
            print(divi)
            prodList = divi.findAll('p',attrs={'class':'pd-name'})
            #print(xyz,len(xyz))
            
            if prodList == None:
                detail = "Post Not Found"
            else:
                flag= 0
                for prd in prodList:
                    one = prd.find('a')
                    if one.has_attr('target') and one.text==postdata['post_title_th']:
                        post_url = "https:"+str(one['href'])
                        pid = post_url.split('/')[-1]
                        print("yha phuncha",post_url)
                        
                        #print(post_url,end = '\n')
                        post_found = "True"
                        postPage = httprequestObj.http_get(post_url)
                        print("yha phuncha 1")
                        ppage = BeautifulSoup(postPage.text,'html5lib').find('ul',attrs={'class':'info-post'}).findAll('li')
                        print("yha phuncha 2")
                        time = ppage[-3].find('span').text
                        view = ppage[-1].find('span').text
                        post_modify_time = time
                        post_id = pid

                        post_view = view
                                            
                        detail = "Post Found "
                        flag=1
                        break
                if flag==0:
                    detail = "Post Not Found"
                    post_found = 'False'
                    #print("yha se gya")
                      
                    
        else :
            detail = 'Can not log in'
            post_found = 'False'

        end_time = datetime.datetime.utcnow()
        

        return {
            "websitename": "thaisecondhand",
            "success": post_found,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(end_time - start_time),
            "detail": detail,
            "account_type":"null",
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "post_url": post_url,
            "post_modify_time": post_modify_time,
            "post_create_time" : post_create_time,
            "post_view": post_view,
            "post_found": post_found
        }
    
    
    def print_debug(self, msg):
        if(self.debug == 1):
            print(msg)
        return True

    def print_debug_data(self, data):
        if(self.debugdata == 1):
            print(data)
        return True
