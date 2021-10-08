from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
import re
import json
import datetime
import sys
import requests
import shutil
from urllib.parse import unquote
from requests_toolbelt.multipart.encoder import MultipartEncoder
import math

class baania():

    name = 'baania'

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
        self.session = lib_httprequest()

    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')

        time_start = datetime.datetime.utcnow()

        success = "false"
        detail = "can't connect to register."

        if (postdata['company_name'] == ""):
            postdata['company_name'] = "-"

        datapost = {
            "email": postdata['user'],
            "password": postdata['pass'],
            "name": postdata['name_en']+' '+postdata['surname_en'],
            "mobile": postdata['tel'],
            "description_th" : "-",
            "company" : postdata['company_name']
        }

        headers = {"Content-type": "application/json"}
        url = "https://api-feed.baania.com/register"

        r = self.session.http_post(url, data=json.dumps(datapost), headers=headers)
        ret = json.loads(r.text)

        if r.status_code == 200:
            success = "true"
            detail = "success register"
        else:
            success = "false"
            detail = ret['message']

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "websitename": "baania",
            "success": success,
            "detail": detail,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "usage_time": str(time_usage),
            "ds_id": postdata['ds_id']
        }

    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')

        time_start = datetime.datetime.utcnow()

        success = "false"
        detail = "can't connect to login."

        datapost = {
            "email": postdata['user'],
            "password": postdata['pass'],
        }

        headers = {"Content-type": "application/json"}
        url = "https://api-feed.baania.com/login"

        r = self.session.http_post(url, data=json.dumps(datapost), headers=headers)
        ret = json.loads(r.text)

        if r.status_code == 200:
            success = "true"
            detail = "success login"
        else:
            success = "false"
            detail = ret['message']

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        if success == "true":
            return {
                "websitename": "baania",
                "success": success,
                "detail": detail,
                "start_time": str(time_start),
                "end_time": str(time_end),
                "usage_time": str(time_usage),
                "ds_id": postdata['ds_id'],
                "login_token": ret['token']
            }
        else:
            return {
                "websitename": "baania",
                "success": success,
                "detail": detail,
                "start_time": str(time_start),
                "end_time": str(time_end),
                "usage_time": str(time_usage),
                "ds_id": postdata['ds_id']
            }

    def payload_data(self, postdata, paytype):
        recdata = {}

        if paytype == 'create':
            recdata['code'] = postdata["property_id"]
        elif paytype == 'edit':
            recdata['code'] = postdata["property_id"]
            recdata['baaniaId'] = postdata["post_id"]

        if postdata['property_type'] == "1":
            recdata['property_type_id'] = 2
        elif postdata['property_type'] == "2":
            recdata['property_type_id'] = 1
        elif postdata['property_type'] == "3":
            recdata['property_type_id'] = 10753
        elif postdata['property_type'] == "4":
            recdata['property_type_id'] = 3
        elif postdata['property_type'] == "5":
            recdata['property_type_id'] = 4
        elif postdata['property_type'] == "6":
            recdata['property_type_id'] = 7
        elif postdata['property_type'] == "7":
            recdata['property_type_id'] = 5
        elif postdata['property_type'] == "8":
            recdata['property_type_id'] = 2362
        elif postdata['property_type'] == "9":
            recdata['property_type_id'] = 6
        elif postdata['property_type'] == "10":
            recdata['property_type_id'] = 8
        elif postdata['property_type'] == "25":
            recdata['property_type_id'] = 10753

        if postdata['listing_type'] == "ขาย":
            recdata['listing_type'] = 'for-sale'
            recdata['sell_state'] = 'on-sale'
            recdata['price_listing'] = int(postdata["price_baht"])
        else:
            recdata['listing_type'] = 'for-rent'
            recdata['sell_state'] = 'on-rent'
            recdata['price_renting'] = int(postdata["price_baht"])

        recdata['title_th'] = postdata['post_title_th']
        recdata['description_th'] = postdata['post_description_th']

        if (postdata['post_title_en'] == "") or (postdata['post_title_en'] is None):
            pass
        else:
            recdata['title_en'] = postdata['post_title_en']

        if (postdata['post_description_en'] == "") or (postdata['post_description_en'] is None):
            pass
        else:
            recdata['description_en'] = postdata['post_description_en']

        recdata['address'] = {}
        recdata['address']['floor'] = postdata['floor_level']
        recdata['address']['province'] = postdata['addr_province']
        recdata['address']['district'] = postdata['addr_district']
        recdata['address']['sub_district'] = postdata['addr_sub_district']
        recdata['address']['post_code'] = postdata['addr_postcode']

        recdata['area_land'] = {}
        if (postdata['land_size_rai'] == "") or (postdata['land_size_rai'] is None):
            pass
        else:
            recdata['area_land']['rai'] = int(postdata['land_size_rai'])

        if (postdata['land_size_wa'] == "") or (postdata['land_size_wa'] is None):
            pass
        else:
            recdata['area_land']['wa'] = int(postdata['land_size_wa'])

        if (postdata['land_size_ngan'] == "") or (postdata['land_size_ngan'] is None):
            pass
        else:
            recdata['area_land']['ngan'] = int(postdata['land_size_ngan'])

        recdata['cover'] = postdata['post_img_url_lists'][0]
        recdata['images'] = postdata['post_img_url_lists'][1:]

        recdata['geo_point'] = {}
        recdata['geo_point']['lat'] = float(postdata['geo_latitude'])
        recdata['geo_point']['lng'] = float(postdata['geo_longitude'])

        if (postdata['bath_room'] == "") or (postdata['bath_room'] is None):
            pass
        else:
            recdata['num_bath'] = int(postdata['bath_room'])

        if (postdata['bed_room'] == "") or (postdata['bed_room'] is None):
            pass
        else:
            recdata['num_bed'] = int(postdata['bed_room'])

        if (postdata['floor_total'] == "") or (postdata['floor_total'] is None):
            pass
        else:
            recdata['num_floor'] = int(postdata['floor_total'])

        if postdata['bed_room'] == '1':
            recdata['room_type'] = '1br'
        elif postdata['bed_room'] == '2':
            recdata['room_type'] = '2br'
        elif postdata['bed_room'] == '3':
            recdata['room_type'] = '3br' 
        elif postdata['bed_room'] == '4':
            recdata['room_type'] = '4br' 
        else:
            recdata['room_type'] = '5br'

        recdata['contact_name'] = postdata['name']
        recdata['contact_email'] = postdata['email']
        recdata['contact_tel'] = postdata['mobile']

        """
        recdata["project"] = {}
        recdata["project"]['id'] = "5e43cf362f2cb30012cefe2c"
        recdata["project"]['name'] = "แอสตร้า สกายริเวอร์"
        """

        recdata['published'] = True

        return (recdata)

    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')

        time_start = datetime.datetime.utcnow()

        success = "false"
        detail = "can't connect to create."

        test_login = self.test_login(postdata)

        if test_login["success"] == 'true':
            payload = self.payload_data(postdata,'create')

            headers = {"Content-type": "application/json","Authorization":"Bearer "+test_login['login_token']}
            
            url = "https://api-feed.baania.com/listing"

            r = self.session.http_post(url, data=json.dumps(payload), headers=headers)
            ret = json.loads(r.text)

            if r.status_code == 200:
                success = "true"
                detail = "Post created successfully!"
                post_url = ret['link']
                post_id = ret['baaniaId']
            else:
                success = "false"
                detail = ret['message']
                post_url = ""
                post_id = ""
            
        else:
            success = "false"
            detail = "cannot login."
            post_url = ""
            post_id = ""

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "websitename": "baania",
            "success": success,
            "detail": detail,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "usage_time": str(time_usage),
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "null"
            
        }

    def edit_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')

        time_start = datetime.datetime.utcnow()

        success = "false"
        detail = "can't connect to edit."

        post_url = "https://baania.com/listing/"+postdata['post_id']
        post_id = postdata['post_id']

        test_login = self.test_login(postdata)

        if test_login["success"] == 'true':
            payload = self.payload_data(postdata,'edit')

            headers = {"Content-type": "application/json","Authorization":"Bearer "+test_login['login_token']}
            
            url = "https://api-feed.baania.com/listing"

            r = requests.put(url, data=json.dumps(payload), headers=headers)
            ret = json.loads(r.text)

            if r.status_code == 200:
                success = "true"
                detail = "Post edited successfully!"
                
            else:
                success = "false"
                detail = ret['message']

        else:
            success = "false"
            detail = "cannot login."

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "websitename": "baania",
            "success": success,
            "detail": detail,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "usage_time": str(time_usage),
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "null"
        }

    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')

        time_start = datetime.datetime.utcnow()

        success = "false"
        detail = "can't connect to delete."

        test_login = self.test_login(postdata)
        
        if test_login["success"] == 'true':

            datapost = {
                'baaniaId': postdata['post_id']
            }

            headers = {"Content-type": "application/json","Authorization":"Bearer "+test_login['login_token']}
            
            url = "https://api-feed.baania.com/listing"

            r = requests.delete(url, data=json.dumps(datapost), headers=headers)
            
            if r.status_code == 200:
                success = "true"
                detail = "post deleted successfully."
            else:
                ret = json.loads(r.text)
                success = "false"
                detail = ret['message']
        else:
            success = "false"
            detail = "cannot login."

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "websitename": "baania",
            "success": success,
            "detail": detail,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "usage_time": str(time_usage),
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": postdata['post_id']
        }

    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')

        time_start = datetime.datetime.utcnow()

        success = "false"
        detail = "can't connect to boost."

        test_login = self.test_login(postdata)

        if test_login["success"] == 'true':

            datapost = {
                'baaniaId': postdata['post_id']
            }

            headers = {"Content-type": "application/json","Authorization":"Bearer "+test_login['login_token']}

            url = "https://api-feed.baania.com/listing/ranking"

            r = requests.post(url, data=json.dumps(datapost), headers=headers)

            if r.status_code == 200 or r.status_code==502:
                success = "true"
                detail = "Post was boosted was successfully."
            else:
                ret = json.loads(r.text)
                success = "false"
                detail = ret['message']
        else:
            success = "false"
            detail = "cannot login."

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "websitename": "baania",
            "success": success,
            "detail": detail,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "usage_time": str(time_usage),
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": postdata['post_id'],
            "post_view": ""
        }

    def search_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')

        time_start = datetime.datetime.utcnow()
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        # return false because create check post by property_id
        detail = 'create already check same post.'

        return {
            "websitename": "baania",
            "success": "true",
            "detail": detail,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "usage_time": str(time_usage),
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": "",
            "post_url": "",
            "post_modify_time": "",
            "post_view": "",
            "post_found": "false",
            "account_type": "null"
        }

    def print_debug(self, msg):
        if(self.debug == 1):
            print(msg)
        return "true"

    def print_debug_data(self, data):
        if(self.debugdata == 1):
            print(data)
        return "true"

        if(self.debugdata == 1):
            print(data)
        return "true"