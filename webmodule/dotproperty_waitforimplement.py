# -*- coding: utf-8 -*-

from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
# from urlparse import urlparse
import re
import json
import datetime
import sys

httprequestObj = lib_httprequest()

'''
https://www.dotproperty.co.th/login
'''
class dotproperty():

    name = 'dotproperty'

    def __init__(self):

        try:
            import configs
        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.primary_domain = 'https://www.dotproperty.co.th'
        self.debug = 0
        self.debugresdata = 0
        self.PARSER = 'html.parser'
        
# _token=zTBJM5ODToev1CyL1fA6y2FwYf3hjYi6pgwHF61d&agency_id=&company_name=&email=amarin_ta@hotmail.com&mail_list=yes&name=amarin%20boonkirt&password=5k4kk3253434&phone=&phone-full=&seller_type=private&type_register=buyer&username=
    def register_user(self, userdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        email_user = userdata['user']
        email_pass = userdata['pass']
        email_user = userdata['email']
        
        company_name = userdata['company_name']
        name_title = userdata["name_title"]
        name_th = userdata["name_th"]
        surname_th = userdata["surname_th"]
        name_en = userdata["name_en"]
        surname_en = userdata["surname_en"]
        tel = userdata["tel"]
        addr_province = userdata["addr_province"]

        #bot process begin
        
        r = httprequestObj.http_get_with_headers(self.primary_domain + '/signup',verify=False)
        data = r.text
        soup = BeautifulSoup(data, self.PARSER)      
          
        frm_token = soup.find("input", {"name":"_token"})['value']        
        print(frm_token)
        exit
        frm_name = name_title
        frm_email = email_user
        frm_pass = email_pass
        frm_type_register = 'buyer'
        frm_mail_list = 'yes'
        
        datapost = {
            '_token': frm_token,
            'name': frm_name,
            'email': frm_email,            
            'password': frm_pass,
            'type_register': frm_type_register,
            'mail_list': frm_mail_list            
        }
        print(datapost)
        exit

        r = httprequestObj.http_post_with_headers(self.primary_domain + '/agent-register', data=datapost)
        
        #bot process end               
        time_end = datetime.datetime.utcnow()
        return {
            "success": "true",
            "time_usage": time_end - time_start,
            "time_start": time_start,
            "time_end": time_end,
            "detail": ""
        }

# https://www.dotproperty.co.th/login
# https://www.dotproperty.co.th/ajaxLogin  _token=I3saeeA5CnOvCAdnCeNi9YssrAg4XNdSWhFbuzNf&email=amarin_ta@hotmail.com&password=5k4kk3253434&refer_type=login&remember=on

    def test_login(self, logindata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        #r = httprequestObj.http_get_with_headers(self.primary_domain + '/signup',verify=False)
        #data = r.text
        #soup = BeautifulSoup(data, self.PARSER)                
        #frm_token = soup.find("input", {"name":"_token"})['value']
        frm_token = ''
        login_user = logindata['user']
        login_pass = logindata['pass']
        
        success = "false"        
        
        datapost = {
            '_token': frm_token,            
            'email': login_user,            
            'password': login_pass,
            'refer_type': 'login',
            'remember': 'on'            
        }

        r = httprequestObj.http_post_with_headers(self.primary_domain + '/ajaxLogin', data=datapost)
        data = r.json()
        detail = data['msg']
        
        #matchObj = re.search(r'อีเมลและ\/หรือรหัสผ่านของคุณไม่ตรงกัน', data['msg'])
        matchObj = re.search(r'login-my-dashboard', data['msg'])
        if matchObj:
            success = "true"
            detail = data['msg']
        #
        #
        #
        time_end = datetime.datetime.utcnow()
        return {
            "success": success,
            "time_usage": time_end - time_start,
            "time_start": time_start,
            "time_end": time_end,
            "detail": detail
        }
        

# https://www.dotproperty.co.th/my-dashboard/properties
# PUT https://www.dotproperty.co.th/dashboard-api/user/check-verified/1524090
# requestBody: {"data":{}}

# 1 ask to gen post id
# PUT https://www.dotproperty.co.th/dashboard-api/properties/store
# requestBody: {"data":{"user_id":1524090,"property_type":"property","name":""}}

# 2 return post id
# GET https://www.dotproperty.co.th/dashboard/properties/4817126/edit

# 3 redirect to edit view
# GET https://www.dotproperty.co.th/my-dashboard/properties/4817126/edit
        
    def create_post(self, postdata, webdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        listing_type = postdata['listing_type']
        property_type = postdata['property_type']
        post_img_url_lists = postdata['post_img_url_lists']
        price_baht = postdata['price_baht']
        addr_province = postdata['addr_province']
        addr_district = postdata['addr_district']
        addr_sub_district = postdata['addr_sub_district']
        addr_road = postdata['addr_road']
        addr_near_by = postdata['addr_near_by']
        floorarea_sqm = postdata['floorarea_sqm']
        geo_latitude = postdata['geo_latitude']
        geo_longitude = postdata['geo_longitude']
        property_id = postdata['property_id']
        post_title_th = postdata['post_title_th']
        post_description_th = postdata['post_description_th']
        post_title_en = postdata['post_title_en']
        post_description_en = postdata['post_description_en']
        ds_id = webdata["ds_id"]
        account_type = webdata["account_type"]
        user = webdata["user"]
        password = webdata["pass"]
        project_name = webdata["project_name"]

        #
        #
        #

        time_end = datetime.datetime.utcnow()
        return {
            "success": "true",
            "time_usage": time_end - time_start,
            "time_start": time_start,
            "time_end": time_end,
            "ds_id": "4",
            "post_url": "http://xxxxx/post/232323",
            "post_id": "33333",
            "account_type": null,
            "detail": ""
        }

    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        post_id = postdata['post_id']
        log_id = postdata['log_id']
        email_user = postdata['email_user']
        email_pass = postdata['email_pass']

        #
        #
        #

        time_end = datetime.datetime.utcnow()
        return {
            "success": "true",
            "time_usage": time_end - time_start,
            "time_start": time_start,
            "time_end": time_end,
            "detail": "",
            "log_id": log_id,
            "post_id": post_id,
        }

    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        log_id = postdata['post_id']
        email_user = postdata['email_user']
        email_pass = postdata['email_pass']

        #
        #
        #

        time_end = datetime.datetime.utcnow()
        return {
            "success": "true",
            "time_usage": time_end - time_start,
            "time_start": time_start,
            "time_end": time_end,
            "detail": "",
            "log_id": log_id,
        }
        
# https://www.dotproperty.co.th/my-dashboard/properties/4817078/edit

    def edit_post(self, postdata, webdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        post_img_url_lists = postdata['post_img_url_lists']
        price_baht = postdata['price_baht']
        county = postdata["county"]
        district = postdata["district"]
        addr_province = postdata['addr_province']
        addr_district = postdata['addr_district']
        addr_sub_district = postdata['addr_sub_district']
        addr_road = postdata['addr_road']
        addr_near_by = postdata['addr_near_by']
        floorarea_sqm = postdata['floorarea_sqm']
        geo_latitude = postdata['geo_latitude']
        geo_longitude = postdata['geo_longitude']
        property_id = postdata['property_id']
        post_title_th = postdata['post_title_th']
        post_description_th = postdata['post_description_th']
        post_title_en = postdata['post_title_en']
        post_description_en = postdata['post_description_en']
        post_id = webdata["post_id"]
        user = webdata["user"]
        password = webdata["pass"]
        log_id = webdata["log_id"]


        jsonstr = '''
{
    "data": {
        "formName": "infomation",
        "formData": [
            {
                "key": "reference",
                "value": ""
            },
            {
                "key": "propertyContact",
                "value": {
                    "title": "à¹à¸à¸¥à¸µà¹à¸¢à¸à¹à¸«à¸¡à¹",
                    "tel": {
                        "key": "tel",
                        "title": null,
                        "value": "",
                        "inputType": "inter-tel",
                        "options": {
                            "validate": "required",
                            "requiredMsg": {
                                "required": "à¸à¸³à¸«à¸à¸à¹à¸«à¹à¸à¹à¸­à¸à¸£à¸°à¸à¸¸à¸à¹à¸­à¸¡à¸¹à¸¥"
                            },
                            "label": "à¹à¸à¸­à¸£à¹à¹à¸à¸£",
                            "countries": [
                                "TH",
                                "US",
                                "GB"
                            ],
                            "isDisable": false
                        }
                    },
                    "name": {
                        "key": "name",
                        "title": null,
                        "value": "",
                        "inputType": "text-label",
                        "options": {
                            "validate": "required",
                            "requiredMsg": {
                                "required": "à¸à¸³à¸«à¸à¸à¹à¸«à¹à¸à¹à¸­à¸à¸£à¸°à¸à¸¸à¸à¹à¸­à¸¡à¸¹à¸¥"
                            },
                            "label": "à¸à¸·à¹à¸­",
                            "isDisable": false
                        }
                    },
                    "email": {
                        "key": "email",
                        "title": null,
                        "value": "",
                        "inputType": "text-label",
                        "options": {
                            "validate": "required|email",
                            "requiredMsg": {
                                "required": "à¸à¸³à¸«à¸à¸à¹à¸«à¹à¸à¹à¸­à¸à¸£à¸°à¸à¸¸à¸à¹à¸­à¸¡à¸¹à¸¥",
                                "email": "à¸­à¸µà¹à¸¡à¸¥à¸à¸´à¸à¸à¹à¸­ à¸à¹à¸­à¸à¹à¸à¹à¸à¸­à¸µà¹à¸¡à¸¥à¹à¸­à¸à¹à¸à¸£à¸ªà¸à¸µà¹à¸¡à¸µà¸­à¸¢à¸¹à¹à¸à¸£à¸´à¸à¹à¸à¹à¸²à¸à¸±à¹à¸"
                            },
                            "label": "à¸­à¸µà¹à¸¡à¸¥à¸à¸´à¸à¸à¹à¸­",
                            "isDisable": false
                        }
                    },
                    "contactType": "default"
                }
            },
            {
                "key": "sellRent",
                "value": "sell"
            },
            {
                "key": "salePrice",
                "value": "''' + price_baht + '''"
            },
            {
                "key": "rentPrice",
                "value": 0
            },
            {
                "key": "rentalMinTerms",
                "value": 12
            },
            {
                "key": "project",
                "value": ""
            },
            {
                "key": "propertyType",
                "value": "condo"
            },
            {
                "key": "furnished",
                "value": null
            },
            {
                "key": "ownership",
                "value": null
            },
            {
                "key": "subType",
                "value": ""
            },
            {
                "key": "bedroom",
                "value": ""
            },
            {
                "key": "bathroom",
                "value": ""
            },
            {
                "key": "floor",
                "value": ""
            },
            {
                "key": "usableArea",
                "value": "45.00"
            },
            {
                "key": "landArea",
                "value": "Rai"
            },
            {
                "key": "rai",
                "value": "0"
            },
            {
                "key": "ngan",
                "value": "0"
            },
            {
                "key": "sqw",
                "value": "0"
            },
            {
                "key": "sqm",
                "value": "0.00"
            },
            {
                "key": "facilities",
                "value": [
                    {
                        "key": "AIR",
                        "title": "à¹à¸à¸£à¸·à¹à¸­à¸à¸à¸£à¸±à¸à¸­à¸²à¸à¸²à¸¨",
                        "name": "AIR",
                        "value": false
                    },
                    {
                        "key": "BBQ",
                        "title": "à¸¥à¸²à¸à¸à¸²à¸à¸´à¸à¸´à¸§",
                        "name": "BBQ",
                        "value": false
                    },
                    {
                        "key": "CTV",
                        "title": "à¸à¸¥à¹à¸­à¸à¸§à¸à¸à¸£à¸à¸´à¸",
                        "name": "CTV",
                        "value": false
                    },
                    {
                        "key": "CON",
                        "title": "à¸à¸à¸±à¸à¸à¸²à¸à¸à¹à¸­à¸à¸£à¸±à¸",
                        "name": "CON",
                        "value": false
                    },
                    {
                        "key": "FIT",
                        "title": "à¸à¸´à¸à¹à¸à¸ª",
                        "name": "FIT",
                        "value": false
                    },
                    {
                        "key": "GAR",
                        "title": "à¸ªà¸§à¸à¸«à¸¢à¹à¸­à¸¡",
                        "name": "GAR",
                        "value": false
                    },
                    {
                        "key": "LIB",
                        "title": "à¸«à¹à¸­à¸à¸ªà¸¡à¸¸à¸",
                        "name": "LIB",
                        "value": false
                    },
                    {
                        "key": "MOU",
                        "title": "à¸§à¸´à¸§à¸ à¸¹à¹à¸à¸²",
                        "name": "MOU",
                        "value": false
                    },
                    {
                        "key": "PARK",
                        "title": "à¸à¸µà¹à¸à¸­à¸à¸£à¸",
                        "name": "PARK",
                        "value": false
                    },
                    {
                        "key": "PLAY",
                        "title": "à¸ªà¸à¸²à¸¡à¹à¸à¹à¸à¹à¸¥à¹à¸",
                        "name": "PLAY",
                        "value": false
                    },
                    {
                        "key": "SEA",
                        "title": "à¸§à¸´à¸§à¸à¸°à¹à¸¥",
                        "name": "SEA",
                        "value": false
                    },
                    {
                        "key": "SEC",
                        "title": "à¸£à¸°à¸à¸à¸£à¸±à¸à¸©à¸²à¸à¸§à¸²à¸¡à¸à¸¥à¸­à¸à¸ à¸±à¸¢",
                        "name": "SEC",
                        "value": false
                    },
                    {
                        "key": "SIN",
                        "title": "à¸à¹à¸²à¸à¸à¸±à¹à¸à¹à¸à¸µà¸¢à¸§",
                        "name": "SIN",
                        "value": false
                    },
                    {
                        "key": "SWI",
                        "title": "à¸ªà¸£à¸°à¸§à¹à¸²à¸¢à¸à¹à¸³",
                        "name": "SWI",
                        "value": false
                    },
                    {
                        "key": "TEN",
                        "title": "à¸ªà¸à¸²à¸¡à¹à¸à¸à¸à¸´à¸ª",
                        "name": "TEN",
                        "value": false
                    },
                    {
                        "key": "WIFI",
                        "title": "à¸£à¸°à¸à¸à¸­à¸´à¸à¹à¸à¸­à¸£à¹à¹à¸à¹à¸à¹à¸§-à¹à¸",
                        "name": "WIFI",
                        "value": false
                    }
                ]
            },
            {
                "key": "title_en",
                "value": "''' + post_title_en + '''"
            },
            {
                "key": "description_en",
                "value": "<p>''' + post_description_en + '''</p>"
            },
            {
                "key": "title_th",
                "value": "''' + post_title_th + '''"
            },
            {
                "key": "description_th",
                "value": "<p>''' + post_description_th + '''</p>"
            },
            {
                "key": "province",
                "value": "Bangkok"
            },
            {
                "key": "city",
                "value": ""
            },
            {
                "key": "area",
                "value": ""
            },
            {
                "key": "transport",
                "value": ""
            },
            {
                "key": "address",
                "value": ""
            },
            {
                "key": "latitude",
                "value": ''' + geo_latitude + '''
            },
            {
                "key": "longitude",
                "value": ''' + geo_longitude + '''
            },
            {
                "key": "geoType",
                "value": ""
            },
            {
                "key": "showMap",
                "value": 1
            },
            {
                "key": "showSv",
                "value": 0
            },
            {
                "key": "mapView",
                "value": ""
            },
            {
                "key": "povHeading",
                "value": 0
            },
            {
                "key": "povPitch",
                "value": 0
            }
        ]
    }
}
'''
        # PUT https://www.dotproperty.co.th/dashboard-api/properties/update/4817079

        r = httprequestObj.http_post_json(self.primary_domain + '/dashboard-api/properties/update/' + post_id, jsoncontent=jsonstr)
    
        data = r.text
        #
        #
        #

        time_end = datetime.datetime.utcnow()
        return {
            "success": "true",
            "time_usage": time_end - time_start,
            "time_start": time_start,
            "time_end": time_end,
            "detail": data,
            "log_id": ""
        }

    def print_debug(self, msg):
        if(self.debug == 1):
            print(msg)
        return True

    def print_debug_data(self, data):
        if(self.debugdata == 1):
            print(data)
        return True
