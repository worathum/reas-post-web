# -*- coding: utf-8 -*-

from time import sleep
from .lib_httprequest import *
from .lib_captcha import *
from bs4 import BeautifulSoup
import os.path
# from urlparse import urlparse
import requests
import json
import datetime
import sys
from urllib.parse import unquote
import os

httprequestObj = lib_httprequest()
captcha = lib_captcha()

class terrabkk():

    name = 'terrabkk'

    def __init__(self):

        try:
            import configs
        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.primarydomain = 'http://www.terrabkk.com/'
        self.debug = 0
        self.debugresdata = 0
        self.parser = 'html.parser'

    def register_user(self, userdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        # print("here in register")

        email = userdata['user']
        passwd = userdata['pass']
        name_title = userdata['name_title']
        name_th = userdata['name_th']
        surname_th = userdata['surname_th']
        tel = userdata['tel']
        line = userdata['line']
        company_name = ""
        if 'company_name' in userdata:
            company_name = userdata['company_name']
        nmaetitledic = { "ms": 'นางสาว', "mrs":'นาง', "mr" : 'นาย'}
        try:
            prefix = nmaetitledic[name_title]
        except:
            prefix = 'นาย'

        datapost={
            "hid_mode": "add",
            "txt_prefix": prefix,
            "txt_prefix_more" : "",
            "txt_firstname": name_th,
            "txt_lastname": surname_th,
            "txt_birthday": '04/05/1980',
            "telephone": tel,
            "txt_email": email,
            "line" : line,
            "id_no":"",
            "txt_address" : "-",
            "agent_type" : "2",
            "cert_id" : "",
            "txt_company" : "99999",
            "txt_company_name" : company_name,
            "txt_company_website" : "",
            "txt_insurance" : "",
            "province_id[1]" : '1',
            "amphur_id[1]" : "",
            "district_id[1]" : "",
            "street_name[1]" : " ",
            "txt_pass" : passwd,
            "txt_pass2" : passwd,
            "agree": "yes"
        }

        f = open(os.getcwd() + '/imgtmp/default/white.jpg', 'rb')
        filetoup = {
            "userfile" : f,
            "company_logo": f,
            "brokercard": f
        }

        sitekey = "6LdrH6IUAAAAAOG7H98SJ7wv9diFEBuJuPlrDCL1"
        g_response = captcha.reCaptcha(sitekey, "https://www.terrabkk.com/member/register-agent")
        
        if g_response != 0:
            datapost["g-recaptcha-response"] = g_response
            r = httprequestObj.http_post("https://www.terrabkk.com/member/submit_profile_agent", data = datapost, files=filetoup)            
            soup = BeautifulSoup(r.text, features=self.parser)
            if not soup.find(id="login"):
                success = "True"
                detail = "Successful Registration. Please verify email"
            else:
                success = "False"
                detail = "Registration Unsuccessful"
        else:
            success = "False"
            detail = "reCaptcha Error"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "terrabkk",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "ds_id":userdata['ds_id']
        }
    def logout_user(self,user_id,access_token):
        
        url = 'https://www.terrabkk.com/restapi/v2/token/{}'.format(user_id)
        headers = {
            'Authorization': access_token,
            'Content-Type': 'application/json'
        }
        data = {'user_id':user_id}
        r = requests.delete(url, data= json.dumps(data), headers=headers)

    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        
        success = False
        detail = ''
        user_id = ''
        access_token = ''

        url = 'https://www.terrabkk.com/restapi/v2/token'
        headers = {'Content-Type': 'application/json'}
        
        data = {
            "app_id": 'dzI2Q3RRM3pPQzhKWlRad3JQY01Fdz09',
            "email": postdata['user'],
            "password": postdata['pass']
        }

        r = httprequestObj.http_post(url, data= json.dumps(data), headers=headers)
        response = r.json()

        success = response['success']
        if success == True:
            detail = 'Login successful'
            user_id = response['data']['user_id']
            access_token = response['data']['access_token']
            if postdata['action'] == 'test_login':
                sleep(1)
                self.logout_user(user_id,access_token)
        else:
            error = response['messages']
            try:
                detail = error[0]
            except:
                detail = '{}.Please tell your developer to know this problem'.format(error)

        time_end = datetime.datetime.utcnow()
        time_usage = str(time_end - time_start)

        return {
            "websitename": "terrabkk",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "usage_time": time_usage,
            "ds_id": postdata['ds_id'],
            "detail": detail,
            "user_id": user_id,
            "access_token": access_token
        }


    def post_prop(self,action,access_token,postdata):
        
        if 'web_project_name' not in postdata:
            if 'project_name' in postdata:
                postdata['web_project_name'] = postdata['project_name']
            else:
                postdata['web_project_name'] = ''

        postdata['post_description_th'] = ''.join(c for c in postdata['post_description_th'] if c <= '\uFFFF')
        postdata['post_description_en'] = ''.join(c for c in postdata['post_description_en'] if c <= '\uFFFF')
        postdata['post_description_th'] = postdata['post_description_th'].replace('\r\n', '<br>')
        postdata['post_description_en'] = postdata['post_description_en'].replace('\r\n', '<br>')
            
        property_type = {
            '1':'CONDOMINIUM',
            '2':'DETACHED_HOUSE',
            '3':'SEMI_DETACHED_HOUSE',
            '4':'TOWNHOUSE',
            '5':'SHOPHOUSE',
            '6':'LAND',
            '7':'APARTMENT',
            '8':'HOTEL',
            '9':'OFFICE',
            '10':'WAREHOUSE',
            '25':'FACTORY',
            '30':'OTHER'
            }
        postdata['property_type'] = property_type[postdata['property_type']]
        
        address = ''
        for i in ['addr_number','addr_road','addr_soi']:
            if postdata[i] in ['-',' ']:
                postdata[i] = ''
            address += postdata[i]
            if i != 'addr_soi':
                address += ' '

        sub_district_id = postdata['addr_sub_district_code']

        headers = {
            'Authorization': access_token,
            'Content-Type': 'application/json'
        }
        url = 'https://www.terrabkk.com/restapi/v2/property'
        data = {
            'status': 'PUBLISH',
            'reference_id': postdata['property_id'],
            "title_th": postdata['post_title_th'][:50],
            "title_en": postdata['post_title_en'][:50],
            "detail_th": postdata['post_description_th'],
            "detail_en": postdata['post_description_en'],
            "project_name": postdata['web_project_name'],
            "property_type": postdata['property_type'],
            'address': address,
            "sub_district_code": sub_district_id,
            "floorarea": postdata['floor_area'],
            "landarea_rai": postdata['land_size_rai'],
            "landarea_ngaan": postdata['land_size_ngan'],
            "landarea_sqw": postdata['land_size_wa'],
            "areasize_sqm": postdata['floorarea_sqm'],
            "lat": postdata['geo_latitude'],
            "lng": postdata['geo_longitude'],
            "numberoffloors": postdata['floor_total'],
            "floor_position": postdata['floor_level'],
            "cover_image":postdata['post_img_url_lists'][0],
            "gallery_images": postdata['post_img_url_lists'][1:]
        }

        if postdata['property_type'] != 'LAND':
            data["bedrooms"] = postdata['bed_room']
            data["bathrooms"] = postdata['bath_room']

        if postdata['listing_type'] == 'ขาย':
            data["post_type"] = 'SELL'
            data["sell_price"] = postdata['price_baht']
        else:
            data["post_type"] = 'RENT'
            data["rent_price"] = postdata['price_baht']

        if action == 'edit':
            data['freepost_id'] = postdata['post_id']
            r = requests.put(url, data= json.dumps(data), headers=headers)
        else:
            r = httprequestObj.http_post(url, data= json.dumps(data), headers=headers)
            
        ret = r.json()
        success = ret['success']
        if success == True:
            post_id = ret['data']['freepost_id']
            post_url = ret['data']['freepost_url']
            detail = 'Post successful'
        else:
            error = ret['messages']
            try:
                detail = error[0]
            except:
                detail = '{}.Please tell your developer to know this problem'.format(error)
            post_id = ''
            post_url = ''

        return {
            'success': success,
            'detail': detail,
            'post_id': post_id,
            'post_url': post_url
        }

    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        
        success = ''
        detail = ''
        post_url = ''
        post_id = ''

        login = self.test_login(postdata)
        success = login['success']
        detail = login['detail']
        user_id = login['user_id']
        access_token = login['access_token']
        if success == True:
            sleep(1)
            post = self.post_prop('create',access_token,postdata)
            success = post['success']
            post_id = post['post_id']
            post_url = post['post_url']
            detail = post['detail']

            sleep(1)
            self.logout_user(user_id,access_token)
        
        time_end = datetime.datetime.utcnow()
        time_usage = str(time_end - time_start)
        return {
            "websitename": "terrabkk",
            "success": success,
            "time_usage": time_usage,
            "time_start": time_start,
            "time_end": time_end,
            "ds_id": postdata['ds_id'],
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "",
            "detail": detail
        }
    
    def edit_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        success = ''
        detail = ''
        post_url = ''
        post_id = ''

        login = self.test_login(postdata)
        success = login['success']
        detail = login['detail']
        user_id = login['user_id']
        access_token = login['access_token']
        if success ==True:
            sleep(1)
            edit = self.post_prop('edit',access_token,postdata)
            success = edit['success']
            post_id = edit['post_id']
            post_url = edit['post_url']
            if success == True:
                detail = 'Your post has been updated.'
            else:
                detail = edit['detail']

            sleep(1)
            self.logout_user(user_id,access_token)
      
        time_end = datetime.datetime.utcnow()
        time_usage = str(time_end - time_start)
        return {
            "websitename": "terrabkk",
            "success": success,
            "time_usage": time_usage,
            "time_start": time_start,
            "time_end": time_end,
            "ds_id": postdata['ds_id'],
            "log_id":postdata['log_id'],
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "",
            "detail": detail
        }

    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        success = False
        detail = 'No option boost in this site'
        time_end = datetime.datetime.utcnow()
        time_usage = str(time_end - time_start)
        return {
            "websitename": "terrabkk",
            "success": success ,
            "time_usage": time_usage,
            "time_start": time_start,
            "time_end": time_end,
            "ds_id": postdata['ds_id'],
            "detail": detail,
            "log_id": postdata['log_id'],
            "post_id": postdata['post_id'],
            "post_view": ""
        }

    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        success = False
        detail = ''

        login = self.test_login(postdata)
        success = login['success']
        detail = login['detail']
        user_id = login['user_id']
        access_token = login['access_token']
        sleep(1)
        if success == True:
            url = 'https://www.terrabkk.com/restapi/v2/property'
            headers = {
                'Authorization': access_token,
                'Content-Type': 'application/json'
            }
            data = {'freepost_id':postdata['post_id']}
            r = requests.delete(url, data= json.dumps(data), headers=headers)
            response = r.json()
            success = response['success']
            if success == True:
                detail = 'Your post has been deleted.'
            else:
                error = response['messages']
                try:
                    detail = error[0]
                except:
                    detail = '{}.Please tell your developer to know this problem'.format(error)
            sleep(1)
            self.logout_user(user_id,access_token)

        time_end = datetime.datetime.utcnow()
        time_usage = str(time_end - time_start)
        return {
            "websitename": "terrabkk",
            "success": success,
            "usage_time": time_usage,
            "start_time": time_start,
            "end_time": time_end,
            "detail": detail,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
        }

    def search_post(self,postdata):
        #self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        #search
        start_time = datetime.datetime.utcnow()
        end_time = datetime.datetime.utcnow()
        return {
            "websitename": "terrabkk",
            "success": False,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(end_time - start_time),
            "detail": "No post with given title",
            "account_type":'null',
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": "",
            "post_url": "",
            "post_modify_time": '',
            "post_create_time" : '',
            "post_view": '',
            "post_found": False
        }
    def print_debug(self, msg):
        if(self.debug == 1):
            print(msg)
        return True

    def print_debug_data(self, data):
        if(self.debugdata == 1):
            print(data)
        return True