# -*- coding: utf-8 -*-

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


class module_websitename():

    name = 'module_websitename'

    def __init__(self):

        try:
            import configs
        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
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

    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        #
        datahandled = self.postdata_handle(postdata)
        success = "true"
        detail = ""

        #
        # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": register_success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
        }

    def test_login_httpreq(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        #

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
            "agent_id": agent_id
        }

    def test_login_headless(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        #

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
            "agent_id": agent_id
        }

    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        #
        handleddata = self.postdata_handle(postdata)
      
        success = "true"
        detail = ""
        agent_id = ""

        #
        # condition such as
        # login by test_login_headless OR test_login_httpreq
        # default http req
        #

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
            "agent_id": agent_id
        }

    def postdata_handle(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')

        # if data is handled
        if self.handled == True:
            return postdata

        datahandled = {}

        # "SALE", "RENT", "OPT" ขาย ให้เช่า ขายดาวน์
        try:
            datahandled['listing_type'] = postdata['listing_type']
        except KeyError:
            datahandled['listing_type'] = "SALE"
        if datahandled['listing_type'] == "ให้เช่า":
            datahandled['listing_type'] = "RENT"
        elif datahandled['listing_type'] == "ขายดาวน์":
            datahandled['listing_type'] = "OPT"
        else:
            datahandled['listing_type'] = "SALE"

        # "CONDO","BUNG","TOWN","LAND","APT","RET","OFF","WAR","BIZ","SHOP"]
        try:
            datahandled['property_type'] = postdata['property_type']
        except KeyError:
            datahandled['property_type'] = "CONDO"
        if datahandled['property_type'] == 2 or datahandled['property_type'] == "บ้านเดี่ยว":
            datahandled['property_type'] = "BUNG"
        elif datahandled['property_type'] == 3 or datahandled['property_type'] == "บ้านแฝด":
            datahandled['property_type'] = "BUNG"
        elif datahandled['property_type'] == 4 or datahandled['property_type'] == "ทาวน์เฮ้าส์":
            datahandled['property_type'] = "TOWN"
        elif datahandled['property_type'] == 5 or datahandled['property_type'] == "ตึกแถว-อาคารพาณิชย์":
            datahandled['property_type'] = "SHOP"
        elif datahandled['property_type'] == 6 or datahandled['property_type'] == "ที่ดิน":
            datahandled['property_type'] = "LAND"
        elif datahandled['property_type'] == 7 or datahandled['property_type'] == "อพาร์ทเมนท์":
            datahandled['property_type'] = "APT"
        elif datahandled['property_type'] == 8 or datahandled['property_type'] == "โรงแรม":
            datahandled['property_type'] = "BIZ"
        elif datahandled['property_type'] == 9 or datahandled['property_type'] == "ออฟฟิศสำนักงาน":
            datahandled['property_type'] = "OFF"
        elif datahandled['property_type'] == 10 or datahandled['property_type'] == "โกดัง-โรงงาน":
            datahandled['property_type'] = "WAR"
        else:
            datahandled['property_type'] = "CONDO"

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
