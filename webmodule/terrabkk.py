# -*- coding: utf-8 -*-

from time import sleep

from .lib_httprequest import *
from bs4 import BeautifulSoup
import requests
import json
import datetime
import sys


class terrabkk():

    name = 'terrabkk'

    def __init__(self):

        try:
            import configs
        except ImportError:
            configs = {}

        self.httprequestObj = lib_httprequest()
        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.primarydomain = 'http://www.terrabkk.com/'
        self.debug = 0
        self.debugresdata = 0
        self.parser = 'html.parser'

    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        success = False

        url = 'https://www.terrabkk.com/restapi/v2/user'

        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            'app_id': 'dzI2Q3RRM3pPQzhKWlRad3JQY01Fdz09',
            'user_email': postdata['user'],
            'user_password': postdata['pass'],
            'user_first_name': postdata['name_en'],
            'user_last_name': postdata['surname_en'],
            'user_telephone': postdata['tel'],
            'user_line_id': postdata['line'],
            'user_agent': 1
        }

        r = requests.post(url, data= json.dumps(data), headers=headers)
        response = r.json()

        if response['success'] == True:
            success = True
            detail = 'Registered successfully'
        else:
            success = False
            try:
                detail = str(response['messages'][0]).split('p>')[1].split('<')[0]
            except:
                detail = 'Something wrong'
        time_end = datetime.datetime.utcnow()

        time_usage = str(time_end - time_start)
        return {
            "websitename": "terrabkk",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "time_usage": time_usage,
            "detail": detail,
            "ds_id":postdata['ds_id']
        }
    def logout_user(self,user_id,access_token):
        
        url = 'https://www.terrabkk.com/restapi/v2/{}'.format(user_id)
        headers = {
            'Authorization': access_token,
            'Content-Type': 'application/json'
        }
        data = {'user_id':user_id}
        requests.delete(url, data= json.dumps(data), headers=headers)

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

        r = self.httprequestObj.http_post(url, data= json.dumps(data), headers=headers)
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
                detail = '{}.'.format(error)

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

        postdata['land_size_wa'] = int(postdata['land_size_wa'])
        postdata['land_size_rai'] = int(postdata['land_size_rai'])
        postdata['land_size_ngan'] = int(postdata['land_size_ngan'])
        if postdata['land_size_wa'] >=400:
            postdata['land_size_rai'] += postdata['land_size_wa']//400
            postdata['land_size_wa'] = postdata['land_size_wa']%400
        if postdata['land_size_ngan'] >=4:
            postdata['land_size_rai'] += postdata['land_size_ngan']//4
            postdata['land_size_ngan'] = postdata['land_size_ngan']%4
        postdata['land_size_wa'] = str(postdata['land_size_wa'])
        postdata['land_size_rai'] = str(postdata['land_size_rai'])
        postdata['land_size_ngan'] = str(postdata['land_size_ngan'])

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

        # on web is not บางนาใต้, บางนาเหนือ
        sub_district_id = postdata['addr_sub_district_code']
        if postdata['addr_sub_district'] == 'บางนาเหนือ' or postdata['addr_sub_district'] == 'บางนาใต้' or postdata['addr_sub_district'] == 'บางนา':
            sub_district_id = 104701 # บางนา

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
            if postdata['bed_room'] != '':
                data["bedrooms"] = postdata['bed_room']
            if postdata['bath_room'] != '':
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
            r = self.httprequestObj.http_post(url, data= json.dumps(data), headers=headers)
            
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
                detail = '{}.'.format(error)
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
            if '<p>The Sub district code field is required.</p>' in detail:
                detail = 'This website is required to fill in the district information.'
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
            "post_id": postdata['post_id'],
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
                    detail = '{}.'.format(error)
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