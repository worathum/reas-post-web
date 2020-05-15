# -*- coding: utf-8 -*-

import logging
import logging.config
from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
# from urlparse import urlparse
import re
import json
import datetime
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time

httprequestObj = lib_httprequest()

try:
    import configs
except ImportError:
    configs = {}
logging.config.dictConfig(getattr(configs, 'logging_config', {}))
log = logging.getLogger()


class residences():

    name = 'residences'

    def __init__(self):

        try:
            import configs
        except ImportError:
            configs = {}

        self.websitename = 'residences'
        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.primary_domain = 'https://www.residences.in.th'
        self.debug = 0
        self.debugresdata = 0
        self.handled = False

        self.options = Options()
        self.options.add_argument("--headless")  # Runs Chrome in headless mode.
        self.options.add_argument('--no-sandbox')  # Bypass OS security model
        self.options.add_argument('start-maximized')
        self.options.add_argument('disable-infobars')
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("window-size=1024,768")
        self.chromedriver_binary = "/bin/chromedriver"


'''

Method:    POST
URL:    https://www.residences.in.th/users
Request Body:   authenticity_token=yvcIuGwXogGW+epiaSMNKE6FyJI7Gaz6nV0iWw/mc8A=&commit=%E0%B8%AA%E0%B8%A1%E0%B8%B1%E0%B8%84%E0%B8%A3%E0%B8%AA%E0%B8%A1%E0%B8%B2%E0%B8%8A%E0%B8%B4%E0%B8%81&user%5Bemail%5D=amarin.ta@gmail.com&user%5Bemail_notice%5D=0&user%5Bemail_notice%5D=1&user%5Bmember_type%5D=0&user%5Bname%5D=amarin%20boonkirt&user%5Bpassword%5D=5k4kk3253434&user%5Bpassword_confirmation%5D=5k4kk3253434&user%5Btelephone%5D=0891999450&utf8=%E2%9C%93
'''
    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        #

        #TODO: find authenticity_token
        authenticity_token = ''
        
        success = "true"
        detail = "success register user"
        
        full_name = postdata["name_th"] + " " + postdata["surname_th"]

        #TODO ถ้าคีย์แบบนี้ไม่ได้ user%5Bemail%5D อาจจะเป็แบบนี้ user[email]
        
        datapost = {
            "authenticity_token": authenticity_token,
            "commit": "%E0%B8%AA%E0%B8%A1%E0%B8%B1%E0%B8%84%E0%B8%A3%E0%B8%AA%E0%B8%A1%E0%B8%B2%E0%B8%8A%E0%B8%B4%E0%B8%81",
            "user%5Bemail%5D": postdata['user'],
            "user%5Bemail_notice%5D": "0",
            "user%5Bemail_notice%5D": "1",
            "user%5Bmember_type%5D": "0",
            "user%5Bname%5D": full_name,
            "user%5Bpassword%5D": postdata['pass'],
            "user%5Bpassword_confirmation%5D":postdata['pass'],
            "user%5Btelephone%5D": postdata["tel"],
            "utf8": "%E2%9C%93"
        }
        datastr = json.dumps(datapost)

        #TODO: json post หรือเปล่าไม่รู้ response เป็นไง ยังไม่ได้เทส
        r = httprequestObj.http_post(self.primary_domain + '/users', data=datapost)
        data = r.text        

        register_success = "false"
        detail = "fail to register user"

        datajson = r.json()
        # if logged in ,session is 0 cause  {"status":0,"name":"\u0e14\u0e39\u0e14\u0e35 \u0e14\u0e2d\u0e17\u0e04\u0e2d\u0e21","email":"kla.arnut@hotmail.com","profile":"https:\/\/th1-cdn.pgimgs.com\/agent\/10760807\/APHO.74655966.C100X100.jpg"}
        if datajson['success'] and datajson['success'] == "true":        
            register_success = "true"
            detail = "success register user"
        #
        # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": register_success,
            "websitename": self.websitename,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": data,
        }

'''
Method:    POST
URL:    https://www.residences.in.th/users/sign_in
Request Body:   authenticity_token=vndE2khGfIByWf1IkPZdqlcuUnDwfe4xv87ouKLY/jM=&commit=%E0%B9%80%E0%B8%82%E0%B9%89%E0%B8%B2%E0%B8%AA%E0%B8%B9%E0%B9%88%E0%B8%A3%E0%B8%B0%E0%B8%9A%E0%B8%9A&user%5Bemail%5D=amarin.ta@gmail.com&user%5Bpassword%5D=5k4kk3253434&user%5Bremember_me%5D=0&utf8=%E2%9C%93
'''
    def test_login_httpreq(self, postdata):
        log.debug('')

        #TODO: find authenticity_token
        authenticity_token = ''
        datapost = {
            "authenticity_token": authenticity_token,            
            "commit": "%E0%B9%80%E0%B8%82%E0%B9%89%E0%B8%B2%E0%B8%AA%E0%B8%B9%E0%B9%88%E0%B8%A3%E0%B8%B0%E0%B8%9A%E0%B8%9A",
            "user%5Bemail%5D": postdata['user'],
            "user%5Bpassword%5D": postdata['p0ass'],
            "user%5Bremember_me%5D" : "0",
            "utf8": "%E2%9C%93"
        }


        datastr = json.dumps(datapost)

        #TODO: json post หรือเปล่าไม่รู้ response เป็นไง ยังไม่ได้เทส
        r = httprequestObj.http_post(self.primary_domain + '/users/sign_in', data=datapost)
        data = r.text    
        }
        
        datastr = json.dumps(datapost)

        #TODO: json post หรือเปล่าไม่รู้ response เป็นไง ยังไม่ได้เทส
        r = httprequestObj.http_post_json(self.primary_domain + '/member/ajaxverify/', jsoncontent=datastr)
        datajson = r.json()

        success = "false"
        detail = "login fail"
        # {\"success\" : true, \"data\" : {\"email\":false,\"password\":false,\"status\":false}}
        if datajson['success'] and datajson['success'] == "true":        
            success = "true"
            detail = "login success"
        detail = detail + r.text
        #
        # end process
        return {"success": success, "detail": detail}


    def test_login(self, postdata):
        log.debug('')

        time_start = datetime.datetime.utcnow()

        # start process
        #

        response = {}
        
        response = self.test_login_httpreq(postdata)

        # end process
        #
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        response['usage_time'] = str(time_usage)
        response['start_time'] = str(time_start)
        response['end_time'] = str(time_end)
        response['websitename'] = self.websitename
        response['ds_id'] = postdata['ds_id']

        return response

    def postdata_handle(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')

        # if data is handled
        if self.handled == True:
            return postdata

        datahandled = {}

'''
S ขาย
R ให้เช่า
B ซื้อ
L เช่า
'''     
        try:
            datahandled['listing_type'] = postdata['listing_type']
        except KeyError:
            datahandled['listing_type'] = "S"
        if datahandled['listing_type'] == "ให้เช่า":
            datahandled['listing_type'] = "R"
        elif datahandled['listing_type'] == "ขายดาวน์":
            datahandled['listing_type'] = "S"
        else:
            datahandled['listing_type'] = "S"

'''
L ที่ดิน
H บ้าน
C คอนโด
'''
        try:
            datahandled['property_type'] = postdata['property_type']
        except KeyError:
            datahandled['property_type'] = "C"
        if datahandled['property_type'] == 2 or datahandled['property_type'] == "บ้านเดี่ยว":
            datahandled['property_type'] = "H"
        elif datahandled['property_type'] == 3 or datahandled['property_type'] == "บ้านแฝด":
            datahandled['property_type'] = "H"
        elif datahandled['property_type'] == 4 or datahandled['property_type'] == "ทาวน์เฮ้าส์":
            datahandled['property_type'] = "H"
        elif datahandled['property_type'] == 5 or datahandled['property_type'] == "ตึกแถว-อาคารพาณิชย์":
            datahandled['property_type'] = "H"
        elif datahandled['property_type'] == 6 or datahandled['property_type'] == "ที่ดิน":
            datahandled['property_type'] = "L"
        elif datahandled['property_type'] == 7 or datahandled['property_type'] == "อพาร์ทเมนท์":
            datahandled['property_type'] = "H"
        elif datahandled['property_type'] == 8 or datahandled['property_type'] == "โรงแรม":
            datahandled['property_type'] = "H"
        elif datahandled['property_type'] == 9 or datahandled['property_type'] == "ออฟฟิศสำนักงาน":
            datahandled['property_type'] = "H"
        elif datahandled['property_type'] == 10 or datahandled['property_type'] == "โกดัง-โรงงาน":
            datahandled['property_type'] = "H"
        else:
            datahandled['property_type'] = "C"

        try:
            datahandled['post_img_url_lists'] = postdata['post_img_url_lists']
        except KeyError:
            datahandled['post_img_url_lists'] = {}

        try:
            datahandled['price_baht'] = postdata['price_baht']
        except KeyError:
            datahandled['price_baht'] = 0

        try:
            datahandled['addr_province'] = postdata['addr_province']
        except KeyError:
            datahandled['addr_province'] = ''

        try:
            datahandled['addr_district'] = postdata['addr_district']
        except KeyError:
            datahandled['addr_district'] = ''

        try:
            datahandled['addr_sub_district'] = postdata['addr_sub_district']
        except KeyError:
            datahandled['addr_sub_district'] = ''

        try:
            datahandled['addr_road'] = postdata['addr_road']
        except KeyError:
            datahandled['addr_road'] = ''

        try:
            datahandled['addr_near_by'] = postdata['addr_near_by']
        except KeyError:
            datahandled['addr_near_by'] = ''

        try:
            datahandled['addr_postcode'] = postdata['addr_postcode']
        except KeyError:
            datahandled['addr_postcode'] = ''

        try:
            datahandled['floorarea_sqm'] = postdata['floorarea_sqm']
        except KeyError:
            datahandled['floorarea_sqm'] = ''

        try:
            datahandled['geo_latitude'] = postdata['geo_latitude']
        except KeyError:
            datahandled['geo_latitude'] = ''

        try:
            datahandled['geo_longitude'] = postdata['geo_longitude']
        except KeyError:
            datahandled['geo_longitude'] = ''

        try:
            datahandled['property_id'] = postdata['property_id']
        except KeyError:
            datahandled['property_id'] = ''

        try:
            datahandled['post_title_th'] = postdata['post_title_th']
        except KeyError:
            datahandled['post_title_th'] = ''

        try:
            datahandled['post_description_th'] = postdata['post_description_th']
        except KeyError:
            datahandled['post_description_th'] = ''

        try:
            datahandled['post_title_en'] = postdata['post_title_en']
        except KeyError:
            datahandled['post_title_en'] = ''

        try:
            datahandled['post_description_en'] = postdata['post_description_en']
        except KeyError:
            datahandled['post_description_en'] = ''

        try:
            datahandled['ds_id'] = postdata["ds_id"]
        except KeyError:
            datahandled['ds_id'] = ''

        try:
            datahandled['ds_name'] = postdata["ds_name"]
        except KeyError:
            datahandled['ds_name'] = ''

        try:
            datahandled['user'] = postdata['user']
        except KeyError:
            datahandled['user'] = ''

        try:
            datahandled['pass'] = postdata['pass']
        except KeyError:
            datahandled['pass'] = ''

        try:
            datahandled['project_name'] = postdata["project_name"]
        except KeyError:
            datahandled['project_name'] = ''

        try:
            datahandled['bed_room'] = postdata["bed_room"]
        except KeyError:
            datahandled['bed_room'] = ''

        try:
            datahandled['bath_room'] = postdata["bath_room"]
        except KeyError:
            datahandled['bath_room'] = ''

        try:
            datahandled['name'] = postdata["name"]
        except KeyError:
            datahandled['name'] = ''

        try:
            datahandled['mobile'] = postdata["mobile"]
        except KeyError:
            datahandled['mobile'] = ''

        try:
            datahandled['email'] = postdata["email"]
        except KeyError:
            datahandled['email'] = ''

        try:
            datahandled['web_project_name'] = postdata["web_project_name"]
        except KeyError:
            datahandled['web_project_name'] = ''

        self.handled = True

        return datahandled



    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        #
        datahandled = self.postdata_handle(postdata)
        success = "true"
        detail = ""
        postid = ""


        datapost = {
            "data": {
                "lat_lng": datahandled['geo_latitude'], datahandled['geo_longitude'],
                "post_type_code": datahandled['listing_type'],
                "property_type_code": datahandled['property_type'],
                "geo_id": "2",
                "province_id": "1",
                "amphur_id": "33",
                "district_id": "192",
                "subject": datahandled['post_title_th'],
                "price": datahandled['price_baht'],
                "description": datahandled['post_description_th'],
                "map_use": "1",
                "poster_name": datahandled['name'],
                "poster_telephone": datahandled['mobile'],
                "poster_email": datahandled['email'],
                "poster_lineid": "amarin.ta",
                "password": datahandled['pass']
            },
            "photos": {
                "name": [
                    "20200502124232_6821785ead08482d618.jpg"
                ],
                "angle": [
                    "0"
                ]
            }
        }

        
        r = httprequestObj.http_post(self.primary_domain + '/post/add', data=datapost)
        data = r.text

        # if datahandled['web_project_name'] != '' , MUST use datahandled['web_project_name']

        #
        # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": datahandled['ds_id'],
            "post_url": "https://www.ddproperty.com/preview-listing/"+post_id if post_id != "" else "",
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
        }

    def create_post_apartment(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        #
        datahandled = self.postdata_handle(postdata)
        success = "true"
        detail = ""
        postid = ""


        datapost = {
            "data": {
                "lat_lng": datahandled['geo_latitude'], datahandled['geo_longitude'],
                "post_type_code": datahandled['listing_type'],
                "property_type_code": datahandled['property_type'],
                "geo_id": "2",
                "province_id": "1",
                "amphur_id": "33",
                "district_id": "192",
                "subject": datahandled['post_title_th'],
                "price": datahandled['price_baht'],
                "description": datahandled['post_description_th'],
                "map_use": "1",
                "poster_name": datahandled['name'],
                "poster_telephone": datahandled['mobile'],
                "poster_email": datahandled['email'],
                "poster_lineid": "amarin.ta",
                "password": datahandled['pass']
            },
            "photos": {
                "name": [
                    "20200502124232_6821785ead08482d618.jpg"
                ],
                "angle": [
                    "0"
                ]
            }
        }

        #TODO 1 residenst first post apartment   after post it will redirect to edit view
        datapost = {            
            "utf8": "✓",
            "authenticity_token": "dv4lzOLDo4iu5i5xNGKn0AITatN9pHDAv3YUk10gA8Q=",
            "apartment": {
                "name": "title thai",
                "en_name": "title eng",
                "apartment_type": "0",
                "province_id": "1",
                "amphur_id": "13",
                "district_id": "98",
                "postcode": "11000",
                "address": "111",
                "road": "ถนน เจริญกรุง",
                "street": "-",
                "latitude": "13.734090465567979",
                "longitude": "100.51106613769531",
                "gmaps_zoom": "",
                "staff": "amarin boonkirt",
                "telephone": "+66891999450",
                "en_telephone": "+66891999450",
                "email": "amarin.ta@gmail.com",
                "line_user_id": "amarin.ta",
                "facebook_url": "",
                "description": "detail thai",
                "en_description": "detail eng",
                "create_level": "1"
            },
            "ignore_reverse_district_id": "0",
            "_wysihtml5_mode": "1",
            "ref_action": "new"            
        }

        
        r = httprequestObj.http_post(self.primary_domain + '/apartments', data=datapost)
        data = r.text


        #TODO 2 edit view https://www.residences.in.th/apartments/114489-%E0%B9%83%E0%B8%AB%E0%B9%89%E0%B9%80%E0%B8%8A%E0%B9%88%E0%B8%B2-%E0%B8%84%E0%B8%AD%E0%B8%99%E0%B9%82%E0%B8%94-watermark-%E0%B9%80%E0%B8%88%E0%B9%89%E0%B8%B2%E0%B8%9E%E0%B8%A3%E0%B8%B0%E0%B8%A2%E0%B8%B2%E0%B8%A3%E0%B8%B4%E0%B9%80%E0%B8%A7%E0%B8%A7%E0%B8%AD%E0%B8%AD%E0%B8%A3%E0%B9%8C-105-%E0%B8%95%E0%B8%A3%E0%B8%A1-2-%E0%B8%99%E0%B8%AD%E0%B8%99-2/amenities
        # เหมือน upload รูปจะเป็น ajax อัพโหลดต่างหาก
        # post สิ่งอำนวยความสะดวก และรูปภาพ
        datapost = {
            "utf8": "✓",
            "_method": "put",
            "authenticity_token": "dv4lzOLDo4iu5i5xNGKn0AITatN9pHDAv3YUk10gA8Q=",
            "apartment": {
                "facility_ids": [
                "",
                "11",
                "9",
                "4",
                "10"
                ],
                "central_facility_ids": [
                "",
                "4",
                "5",
                "8"
                ],
                "create_level": "2"
            },
            "do_not_validation_all_facility": "0",
            "do_not_validation_listing_images": "0",
            "ref_action": "amenities"
        }

        #TODO 3 edit view ประเภทห้องพักและค่าใช้จ่าย
        datapost = {
            "utf8": "✓",
            "_method": "put",
            "authenticity_token": "dv4lzOLDo4iu5i5xNGKn0AITatN9pHDAv3YUk10gA8Q=",
            "apartment": {
                "rooms_attributes": {
                "1589559076605": {
                    "name": "ห้องพัก",
                    "room_type": "R1",
                    "size": "0.09",
                    "monthly": "1",
                    "min_price_permonth": "500",
                    "max_price_permonth": "40000",
                    "daily": "0",
                    "min_price_perday": "",
                    "max_price_perday": "",
                    "available": "1",
                    "_destroy": "false"
                }
                },
                "water_price": "",
                "water_price_monthly_per_person": "",
                "water_price_monthly_per_room": "",
                "water_price_remark": "",
                "water_price_type": "6",
                "water_price_note": "",
                "electric_price": "",
                "electric_price_remark": "",
                "electric_price_type": "4",
                "electric_price_note": "",
                "deposit_month": "",
                "deposit_bath": "",
                "deposit_type": "4",
                "deposit": "",
                "advance_fee_month": "",
                "advance_fee_bath": "",
                "advance_fee_type": "4",
                "advance_fee": "",
                "phone_price_minute": "",
                "phone_price_minute_unit": "",
                "phone_price_per_time": "",
                "phone_price_type": "4",
                "phone_price": "",
                "internet_price_bath": "",
                "internet_price_unit": "",
                "internet_price_type": "4",
                "internet_price": "",
                "has_promotion": "0",
                "promotion_start": "",
                "promotion_end": "",
                "promotion_description": "",
                "create_level": "3"
            },
            "_wysihtml5_mode": "1",
            "ref_action": "roomtypes"
        }
        
        # if datahandled['web_project_name'] != '' , MUST use datahandled['web_project_name']

        #
        # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": datahandled['ds_id'],
            "post_url": "https://www.ddproperty.com/preview-listing/"+post_id if post_id != "" else "",
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
        }

# not have boost post , use edit_post
    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        #
        datahandled = self.postdata_handle(postdata)
        success = "true"
        detail = ""
        post_id = ""
        log_id = ""

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
            "log_id": log_id,
            "post_id": post_id,
        }

'''
Method:    POST
URL:    https://www.teedin108.com/post/trash/
Request Body:   post_id=2082326
'''
    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        #
        datahandled = self.postdata_handle(postdata)
        success = "true"
        detail = ""
        log_id = ""

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
            "log_id": log_id,
        }

    def edit_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start proces
        #
        datahandled = self.postdata_handle(postdata)
        success = "true"
        detail = ""
        log_id = ""

        post_id = ""
        datapost = {
            "data": {
                "lat_lng": datahandled['geo_latitude'], datahandled['geo_longitude'],
                "post_type_code": datahandled['listing_type'],
                "property_type_code": datahandled['property_type'],
                "geo_id": "2",
                "province_id": "1",
                "amphur_id": "33",
                "district_id": "192",
                "subject": datahandled['post_title_th'],
                "price": datahandled['price_baht'],
                "description": datahandled['post_description_th'],
                "map_use": "1",
                "poster_name": datahandled['name'],
                "poster_telephone": datahandled['mobile'],
                "poster_email": datahandled['email'],
                "poster_lineid": "amarin.ta",
                "password": datahandled['pass']
            },
            "photos": {
                "name": [
                    "20200502124232_6821785ead08482d618.jpg"
                ],
                "angle": [
                    "0"
                ]
            }
        }
        
        r = httprequestObj.http_post(self.primary_domain + '/post/save/' + post_id + '/', data=datapost)
        data = r.text

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
            "log_id": log_id
        }

    def print_debug(self, msg):
        if(self.debug == 1):
            print(msg)
        return True

    def print_debug_data(self, data):
        if(self.debugdata == 1):
            print(data)
        return True
residences