# -*- coding: utf-8 -*-
import base64
from .lib_httprequest import *
from bs4 import BeautifulSoup
import datetime
import sys

class aecmarketing():
    name = 'aecmarketing'

    def __init__(self):

        try:
            import configs

        except ImportError:
            configs = {}

        self.debug = 0
        self.httprequestObj = lib_httprequest()
        self.webname = 'aecmarketing'

    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        
        success = False
        detail = 'Something wrong'

        datapost = {
            'user_firstname': postdata['name_th'],
            'user_lastname': postdata['surname_th'],
            'user_email': postdata['user'],
            'user_password': postdata['pass']
        }

        r = self.httprequestObj.http_post('https://www.aecmarketinghome.com/th/user/register.html', data=datapost)
        response = r.json()
        if response['result']['status_code'] == 200:
            success = True
            detail = 'Registration Successful'
        else:
            detail = response['result']['description']

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            'ds_id': postdata['ds_id'],
            "detail": detail,
            "websitename": self.webname,
        }

    def test_login(self, postdata):
        time_start = datetime.datetime.utcnow()

        success = False
        detail = 'Something wrong'

        datapost = {
            'login_user': postdata['user'],
            'login_password': postdata['pass']
        }
        r = self.httprequestObj.http_post('https://www.aecmarketinghome.com/th/user/userlogin.html', data=datapost)
        response = r.json()
        if response['result']['status_code'] == 200:
            success = True
            detail = 'Login successful'
        else:
            detail = 'Wrong username or password'

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": self.webname,
            "ds_id": postdata['ds_id'],
        }

    def post_prop(self, postdata,action):
        success =False
        detail = 'Something wrong'
        post_url = ''
        post_id = ''
        province_id = ''
        subdistrict_id = ''
        
        r = self.httprequestObj.http_get('https://www.aecmarketinghome.com/th/post.html')
        soup = BeautifulSoup(r.content, features = "html.parser")
        provinces = soup.find('select', {'name': 'district_id'})
        provinces = provinces.find_all('option')

        if postdata['addr_province'] == 'กรุงเทพมหานคร':
            postdata['addr_province'] = 'กรุงเทพ'

        for i in provinces:
            if (postdata['addr_province'] in i.text) and (postdata['addr_district'] in i.text):
                province_id = i['value']
                break

        r = self.httprequestObj.http_get('https://www.aecmarketinghome.com/th/post/get_subdistrict/{}'.format(province_id))
        if r.text != '[]':
            response = r.json()
            for i in response:
                if postdata['addr_sub_district'] in i['subdistrict_name']:
                    subdistrict_id = i['subdistrict_id']
                    break

        if province_id == '' or subdistrict_id == '':
            detail = 'This subdistrict does not exist on this site.'
        else:
            property_type = {
                    '1':'3',
                    '2':'1',
                    '3':'1',
                    '4':'2',
                    '5':'5',
                    '6':'6',
                    '7':'4',
                    '8':'4',
                    '9':'8',
                    '10':'7',
                    '25':'7'
                }
            
            listing_type = {'ขาย' : '1','เช่า':'4'}
            postdata['property_type'] = property_type[postdata['property_type']]
            postdata['listing_type'] = listing_type[postdata['listing_type']]

            data = [
                ('name', postdata['post_title_th']),
                ('type', postdata['property_type']),
                ('post_type', postdata['listing_type']),
                ('price', postdata['price_baht']),
                ('price_rent', postdata['price_baht']),
                ('rent_time', '12'),
                ('land_rai', postdata['land_size_rai']),
                ('land_ngaan', postdata['land_size_ngan']),
                ('land_sqw', postdata['land_size_wa']),
                ('useable_sqm', postdata['floorarea_sqm']),
                ('bedroom',postdata['bed_room']),
                ('bathroom',postdata['bath_room']),
                ('living', ''),
                ('parking', ''),
                ('floor_no', postdata['floor_level']),
                ('floor', postdata['floor_total']),
                ('contact_name',postdata['name']),
                ('contact_phone', postdata['mobile']),
                ('contact_lineid', postdata['line']),
                ('detail', postdata['post_description_th'].replace('\r','')),
                ('district_id',province_id),
                ('subdistrict_id',subdistrict_id),
                ('address_no', postdata['addr_number']),
                ('address_road', postdata['addr_road']),
                ('location_lat', postdata['geo_latitude']),
                ('location_lng',postdata['geo_longitude'])
            ]

            image_string = []
            for file in postdata['post_images'][:10]:
                with open(os.getcwd() + "/" + file, 'rb') as img_file:
                    encode = 'data:image/jpeg;base64,' + str(base64.b64encode(img_file.read()))[2:-1]
                image_string.append(encode)
            data.append(('photos[]',image_string))
            if action == ('post'):
                r = self.httprequestObj.http_post('https://www.aecmarketinghome.com/th/post/save_property.html', data=data)
            else:
                r = self.httprequestObj.http_post('https://www.aecmarketinghome.com/th/post/save_property/{}.html'.format(postdata['post_id']), data=data)
            response = r.json()
            if response['result']['status_code'] == 200:
                post_url = response['result']['redirect']
                post_id = post_url.split('/')[-1].split('-')[0]
                success = True
                if action == ('post'):
                    postdata['post_id'] = post_id
                    self.boost_post(postdata)
            else:
                detail = response['result']['description']
        return {
            'success': success,
            'detail': detail,
            'post_id': post_id,
            'post_url': post_url
        }

    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        success = False
        detail = 'Something wrong'
        post_url = ''
        post_id = ''
        test_login = self.test_login(postdata)
        success = test_login["success"]
        
        if success:
            success =False
            post = self.post_prop(postdata,'post')
            success = post['success']
            if success:
                detail = 'Post successful'
                post_id = post['post_id']
                post_url = post['post_url']
            else:
                detail = post['detail']
        else:
            detail = test_login["detail"]

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
            "websitename": self.webname,
        }

    def edit_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        success = False
        detail = 'Something wrong'
        test_login = self.test_login(postdata)
        success = test_login["success"]
        
        if success:
            success =False
            edit = self.post_prop(postdata,'edit')
            success = edit['success']
            if success:
                detail = 'Edit successful'
            else:
                detail = edit['detail']
        else:
            detail = test_login["detail"]

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": postdata['ds_id'],
            "post_id": postdata['post_id'],
            "account_type": "null",
            "detail": detail,
            "websitename": self.webname,
        }

    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        success = False
        detail = 'Something wrong'
        test_login = self.test_login(postdata)
        success = test_login["success"]
        
        if success:
            success =False
            data = {
                'prop_id': postdata['post_id']
            }
            r = self.httprequestObj.http_post('https://www.aecmarketinghome.com/profile/expire', data=data)
            response = r.json()

            if response['result']['status_code'] == 200:
                success = True
                detail = 'Boost successful'
            else:
                detail = response['result']['description']

        else:
            detail = test_login["detail"]

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": postdata['post_id'],
            "websitename": self.webname,
            "post_view": ""
        }

    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        success = False
        detail = 'Something wrong'
        test_login = self.test_login(postdata)
        success = test_login["success"]
        
        if success:
            success =False
            data = {
                'prop_id': postdata['post_id']
            }
            r = self.httprequestObj.http_post('https://www.aecmarketinghome.com/profile/delete', data=data)
            response = r.json()

            if response['result']['status_code'] == 200:
                success = True
                detail = 'Delete successful'
            else:
                detail = response['result']['description']

        else:
            detail = test_login["detail"]

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": self.webname,
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": postdata['post_id']
        }

    def search_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        success = False
        post_found = False
        detail = 'Something wrong'
        post_id = ''
        post_url = ''
        test_login = self.test_login(postdata)
        success = test_login["success"]
        
        if success:
            success =False
            r = self.httprequestObj.http_get("https://www.aecmarketinghome.com/th/profile.html")
            soup = BeautifulSoup(r.content, features = "html.parser")
            postdata['post_title_th'] = postdata['post_title_th'].replace(' ','-')
            for a in soup.find_all('a', href=True):
                if postdata['post_title_th'][:50] in a['href']:
                    post_url = a['href']
                    post_id = post_url.split('/')[-1].split('-')[0]
                    success = True
                    detail = 'Post found'
                    post_found = True
                    break
            if not success:
                post_found = False
                detail = 'Not found this post'
        else:
            detail = test_login["detail"]

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": self.webname,
            "account_type":None,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "post_modify_time": '',
            "post_view": '',
            "post_url": post_url,
            "post_found": post_found
        }

    def print_debug(self, msg):
        if(self.debug == 1):
            print(msg)
        return True