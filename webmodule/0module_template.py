# -*- coding: utf-8 -*-

import lib_httprequest
from bs4 import BeautifulSoup
import os.path
from urlparse import urlparse
import re
import json
import datetime


class websitename():

    name = 'websitename'

    def __init__(self):

        try:
            import configs
        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.primarydomain = ''
        self.debug = 0
        self.debugresdata = 0

    def register_user(self, userdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        email_user = userdata['email_user']
        email_pass = userdata['email_pass']
        company_name = userdata['company_name']
        name_title = userdata["name_title"]
        name_th = userdata["name_th"]
        surname_th = userdata["surname_th"]
        name_en = userdata["name_en"]
        surname_en = userdata["surname_en"]
        tel = userdata["tel"]
        addr_province = userdata["addr_province"]

        #
        #
        #

        return {
            "success": "true",
            "time_usage": time_end - time_start,
            "time_start": time_start,
            "time_end": time_end,
            "detail": ""
        }

    def test_login(self, logindata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        email_user = logindata['email_user']
        email_pass = logindata['email_pass']

        #
        #
        #

        return {
            "success": "true",
            "time_usage": time_end - time_start,
            "time_start": time_start,
            "time_end": time_end,
            "detail": ""
        }

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
