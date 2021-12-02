# -*- coding: utf-8 -*-

from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
# from urlparse import urlparse
import re
import json
import datetime
import sys
import requests
import shutil
from urllib.parse import unquote
import hashlib
import csv


class livinginsider():
    name = 'livinginsider'

    def __init__(self):

        try:
            import configs

        except ImportError:
            configs = {}

        self.webbaseurl = 'https://api.livinginsider.com/tpx'
        self.httprequestObj = lib_httprequest()
        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.debug = 1
        self.debugresdata = 0
        self.parser = 'html.parser'
        self.webname = 'livinginsider'

    def logout_user(self,mem_id,device_id):

        url = '{}/logout.php'.format(self.webbaseurl)
        data = {
            'mem_id': mem_id,
            'device_id': device_id,
            'device_type': 6
        }
        r = self.httprequestObj.http_post(url, data=data)
        response = r.json()
        print(response)

    def register_user(self, postdata):
        self.logout_user()
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']
        username = user.replace("@","").replace(".","")
        success = "true"
        detail = ""
        username = user.split('@')

        datapost = {
            "email": user,
            "password": passwd,
            "repassword": passwd,
            "username": username,
            "mem_tel": postdata['tel']
        }
        # print(datapost)
        r = self.httprequestObj.http_post('https://www.livinginsider.com/member_create.php', data=datapost)
        data = json.loads(r.text)
        # print(data)
        if data['error_field'] != '':
            success = False
            detail = data['result_msg']
        else:
            success = True
            detail = 'Registered successfully'

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": self.webname,
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            'ds_id': postdata['ds_id'],
            "detail": detail,
        }

    def test_login(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        success = False
        detail = 'Something wrong'
        device_id = ''
        mem_id = ''
        mem_status = ''

        hash = hashlib.sha1(postdata['pass'].encode())
        url = '{}/login.php'.format(self.webbaseurl)
        data = {
            'username': postdata['user'],
            'password': hash.hexdigest(),
            'device_type': 6
        }
        
        r = self.httprequestObj.http_post(url, data=data)
        response = r.json()

        if response['result_code'] == 0:
            success = True
            detail = 'Login successful'
            device_id = response['profile']['device_id']
            mem_id = response['profile']['mem_id']
            mem_status = response['profile']['mem_status']
        else:
            detail = response['result_msg']

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": self.webname,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "success": success,
            "detail": detail,
            'device_id': device_id,
            'mem_id': mem_id,
            'mem_status': mem_status,
            "ds_id": postdata['ds_id']
        }

    def post_prop(self,action,url,postdata,mem_id,device_id):
        
        success = False
        detail = 'Something wrong'

        with open('./static/living_zone_id.json') as f:
            zone_data = json.load(f)

        web_zone_id = 0
        zone = postdata['addr_province']
        if postdata['addr_province'] == 'กรุงเทพ':
            zone = postdata['addr_district']
        elif postdata['addr_province'] == 'พระนครศรีอยุธยา':
            zone = 'อยุธยา'
        
        for key in zone_data:
            if zone in zone_data[key]['Zone name \u0e44\u0e17\u0e22']:
                web_zone_id = key
                break
        with open('./static/living_project_id.json') as f:
            project_data = json.load(f)

        if 'web_project_name' not in postdata:
            if 'project_name' in postdata:
                postdata['web_project_name'] = postdata['project_name']
            else:
                postdata['web_project_name'] = 'None'

        project_id = 0
        for key in project_data:
            if postdata['web_project_name'] in project_data[key]['Project name English']:
                project_id = key
                break
            elif postdata['web_project_name'] in project_data[key]['Project name ไทย']:
                project_id = key
                break

        property_type = {
            '1':1,
            '2':2,
            '3':2,
            '4':6,
            '5':4,
            '6':3,
            '7':10,
            '8':10,
            '9':6,
            '10':11,
            '25':11
            }

        if postdata['listing_type'] == 'ขาย':
            postdata['listing_type'] = 1
        else:
            postdata['listing_type'] = 4

        img = ''
        for count, value in enumerate(postdata['post_img_url_lists']):
            if '.jpg' not in value:
                value += '.jpg'
            if count != len(postdata['post_img_url_lists'])-1:
                img += value + '||'
            else:
                img += value
        
        if postdata['floor_level'] == '':
            postdata['floor_level'] = postdata['floor_total']

        web_building_type = property_type[postdata['property_type']]

        for i in ['land_size_rai', 'land_size_ngan','land_size_wa','floorarea_sqm']:
            if postdata[i] == '':
                postdata[i] = 0

        if web_building_type == 1:
            area = postdata['floorarea_sqm']
        else:
            area = int(postdata['land_size_rai'])*400 + int(postdata['land_size_ngan'])*100 + int(postdata['land_size_wa'])
            if area == 0:
                area = int(postdata['floorarea_sqm'])/4

        if postdata['price_baht'] == '':
            postdata['price_baht'] = 0
        postdata['post_description_th'] = postdata['post_description_th'].replace('\r','')
        postdata['post_description_en'] = postdata['post_description_en'].replace('\r','')
        data = {
            'mem_id': mem_id,
            'device_id': device_id,
            'device_type': 6,
            'web_sku': postdata['property_id'],
            'web_zone_id': int(web_zone_id),
            'web_building_type': int(web_building_type),
            'web_post_type': int(postdata['listing_type']),
            'web_post_from': 2,
            'photo_list': img,
            'web_title': postdata['post_title_th'],
            'web_title_en': postdata['post_title_en'],
            'web_description': postdata['post_description_th'],
            'web_description_en': postdata['post_description_en'],
            'web_status': 1, 
            'web_price': int(postdata['price_baht']),
            'web_area_size': area
        }

        if web_building_type in [1,2,4,5,6,7,10]:
            if postdata['floor_level'] == '':
                postdata['floor_level'] = 1
            data['web_floor'] = int(postdata['floor_level'])

        if web_building_type in [1,2,4,6]:
            if 'bed_room' not in postdata or postdata['bed_room'] == '' or postdata['bed_room'] == 0:
                data['web_room'] = 1
            elif int(postdata['bed_room']) > 10:
                data['web_room'] = 11
            else:
                data['web_room'] = int(postdata['bed_room'])

        if web_building_type in [1,2,4,5,6,7]:
            if 'bath_room' not in postdata or postdata['bath_room'] == '' or postdata['bath_room'] == 0: 
                data['web_bathroom'] = 1
            elif int(postdata['bath_room']) > 5:
                data['web_bathroom'] = 6
            else:
                data['web_bathroom'] = int(postdata['bath_room'])

        if web_building_type == 3:
            data['web_area_rai'] = int(postdata['land_size_rai'])
            data['web_area_ngan'] = int(postdata['land_size_ngan'])
            data['web_area_wa'] = int(postdata['land_size_wa'])
        elif web_building_type == 1:
            data['web_project_id'] = int(project_id)
        elif web_building_type in [4,5,6,8,9,11]:
            data['web_useful_space'] = float(postdata['floorarea_sqm'])
        elif web_building_type == 10:
            data['web_income_year'] = 0

        if project_id == 0:
            data['web_project_id'] = int(project_id)
            data['web_latitude'] = postdata['geo_latitude']
            data['web_longitude'] = postdata['geo_longitude']
        
        if action == 'edit':
            data['web_id'] = int(postdata['post_id'])
        
        if web_zone_id != 0:
            r = self.httprequestObj.http_post(url, data=data)
            response = r.json()
            success = True
        else:
            detail = 'Cannot found zone id'
            response = ''
        return {
            'success': success,
            'detail': detail,
            'response':response
        }
    
    def create_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()
        
        success = False
        detail = 'Something wrong'
        post_url = ''
        post_id = ''
        test_login = self.test_login(postdata)
        success = test_login['success']

        if success:
            device_id = test_login['device_id']
            mem_id = test_login['mem_id']
            mem_status = test_login['mem_status']
            if mem_status == '1':
                data = {
                    'mem_id': mem_id,
                    'device_id': device_id,
                    'device_type': 6
                }
                r = self.httprequestObj.http_post('{}/profile.php'.format(self.webbaseurl), data=data)
                response = r.json()
                if str(response['result_code']) == '0':
                    if int(response['profile']['credit_balance'])>= 20:
                        url = '{}/post_add.php'.format(self.webbaseurl)
                        post = self.post_prop('create',url,postdata,mem_id,device_id)
                        success = post['success']
                        detail = post['detail']
                        if success:
                            if str(post['response']['result_code']) == '0':
                                post_id = post['response']['web_id']
                                post_url = post['response']['share_url']
                                detail = 'Post successful'
                            else:
                                success = False
                                detail = post['response']['result_msg']
                    else:
                        success = False
                        detail = 'No balance to post.'
                else:
                    success = False
                    detail = response['result_msg']
            elif mem_status == '2':
                success = False
                detail = 'Your account is waiting to activate'
            else:
                success = False
                detail = 'Your account is suspended'
        else:
            detail = test_login['detail']
        
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "websitename": self.webname,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
        }

    def edit_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        success = False
        detail = 'Something wrong'
        post_url = ''
        post_id = postdata['post_id']
        test_login = self.test_login(postdata)
        success = test_login['success']

        if success:
            device_id = test_login['device_id']
            mem_id = test_login['mem_id']
            mem_status = test_login['mem_status']
            if mem_status == '1':
                url = '{}/post_edit.php'.format(self.webbaseurl)
                edit = self.post_prop('edit',url,postdata,mem_id,device_id)
                success = edit['success']
                detail = edit['detail']
                if success:
                    if str(edit['response']['result_code']) == '0':
                        post_id = edit['response']['web_id']
                        post_url = edit['response']['share_url']
                        detail = 'Edit successful'
                    else:
                        detail = edit['response']['result_msg']
            elif mem_status == '2':
                success = False
                detail = 'Your account is waiting to activate'
            else:
                success = False
                detail = 'Your account is suspended'
        else:
            success = False
            detail = test_login['detail']

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "websitename": self.webname,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
        }

    def delete_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()
        
        success = False
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = 'Something wrong'
        if success:
            device_id = test_login['device_id']
            mem_id = test_login['mem_id']
            mem_status = test_login['mem_status']
            data={
                'mem_id': mem_id,
                'device_id': device_id,
                'device_type': 6,
                'web_id': postdata['post_id'],
                'reason_id': 2
            }
            url = '{}/post_delete.php'.format(self.webbaseurl)
            r = self.httprequestObj.http_post(url, data=data)
            response = r.json()
            if str(response['result_code']) == '0':
                success = True
                detail = 'Post deleted successfully'
            else:
                success = False
                detail = response['result_msg']

        time_end = datetime.datetime.utcnow()
        return {
            "success": success,
            "usage_time": time_end - time_start,
            "start_time": time_start,
            "end_time": time_end,
            "detail": detail,
            "log_id": postdata['log_id'],
            "ds_id": postdata['ds_id'],
            "post_id": postdata['post_id'],
            "websitename": "livinginsider",
        }
    

    def boost_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        post_id = postdata['post_id']
        log_id = postdata['log_id']

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = ""

        if success:

            headers = {
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Mobile Safari/537.36',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-User': '?1',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                    'Sec-Fetch-Site': 'same-origin',
                    'Referer': 'https://www.livinginsider.com/mystock.php',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                }
            res = self.httprequestObj.http_get('https://www.livinginsider.com/living_edit.php', params={'topic_id': str(post_id)}, headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            #print(soup.find('meta', {'name': 'csrf-token'}).get('content'))
            csrf_token = soup.find('meta', {'name': 'csrf-token'}).get('content')
            referer = 'https://www.livinginsider.com/living_edit.php?topic_id=' + str(postdata['post_id']) + '&currentID=' + str(postdata['post_id'])

            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'th-TH,th;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'www.livinginsider.com',
                'Origin': 'https://www.livinginsider.com',
                'Referer': referer,
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36', 
                'X-CSRF-TOKEN': csrf_token,
                'X-Requested-With': 'XMLHttpRequest'
            }

            r = self.httprequestObj.http_post('https://www.livinginsider.com/a_edit_living.php', data=None, headers=headers)
            res = self.httprequestObj.http_get('https://www.livinginsider.com/living_edit2.php?topic_id='+ postdata['post_id'], headers=headers)
            
            headers = {
                'Connection': 'keep-alive',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': 'https://www.livinginsider.com',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://www.livinginsider.com/living_edit2.php?topic_id=' + post_id,
                'Accept-Language': 'en-IN,en-US;q=0.9,en;q=0.8',
            }

            r = self.httprequestObj.http_post('https://www.livinginsider.com/a_edit_living.php', headers=headers, data=None)

            data = {
                'hidden_status': '',
                'action': 'save',
                'web_status': '1',
                'publish_flag': '0',
                'state_renew': ''
            }

            r = self.httprequestObj.http_post('https://www.livinginsider.com/living_edit_confirm.php', params={'topic_id': post_id}, data=data)

            if r.status_code == 200:
                success = 'true'
                detail = 'Post was boosted was successfully.'
            else:
                success = 'false'
                detail = 'Can not boost the post.'
            
        else:
            success = False
            detail = 'Couldnot login'

        time_end = datetime.datetime.utcnow()
        return {
            "success": success,
            "usage_time": time_end - time_start,
            "start_time": time_start,
            "end_time": time_end,
            "detail": detail,
            "log_id": log_id,
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
            "websitename": "livinginsider",
            "post_view": ''
        }

    def search_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_url = ""
        post_id = ""
        post_modified = ""
        post_view = ""

        if success:
            page = 1

            post_found = False
            max_page = 100
            r = self.httprequestObj.http_get(
                'https://www.livinginsider.com/mystock.php?action=1&pages=%d&pagelimit=50&actiontype=&posttype=&search_zone_id=&search_project_id=&web_id_for_publish=&web_id_hidden=&check_open_graph=&id_scroll=-1&search_bedroom=0&search_area=0&search_price=0&topic_sort=1&group_list=&searchword=' % page)
            soup = BeautifulSoup(r.content, self.parser)
            try:
                max_page = int(soup.find('ul', 'pagination').findChildren('li', recursive=False)[-3].find('a').string)
            except:
                max_page = 1
            while page <= max_page:

                # if page == max_page:
                #     print('\n\nsearched till max\n\n')

                r = self.httprequestObj.http_get('https://www.livinginsider.com/mystock.php?action=1&pages=%d&pagelimit=50&actiontype=&posttype=&search_zone_id=&search_project_id=&web_id_for_publish=&web_id_hidden=&check_open_graph=&id_scroll=-1&search_bedroom=0&search_area=0&search_price=0&topic_sort=1&group_list=&searchword=' % page)
                soup = BeautifulSoup(r.content, self.parser)

                all_posts = soup.find_all('div', attrs={'class':'mystock-item'})

                for post in all_posts:

                    # info = post.fin
                    post_url = str(post.find('a', attrs = {'target':'_blank'})['href'])
                    title = post.find('div', attrs={'class': "limit-title-ms"}).text  # .split(':').strip()
                    # print(title + '\n' + postdata['post_title_th'] + "\n\n")
                    if title in postdata['post_title_th'] :
                        # print('Found post')
                        post_found = "True"
                        detail = "Post Found"
                        post_id = post_url.split('/')[4]

                        post_view = ''

                        break
                page += 1
                if post_found:
                    break

            if not post_found:
                post_url = ''
                detail = "No post with given post_title"
        else:
            success = False
            detail = "Couldnot login"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": "livinginsider",
            "account_type": None,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "post_created": '',
            "post_modified": "",
            "post_view": post_view,
            "post_url": post_url
        }
    
    ############## Extra Boost ###############
    def extra_boost(self,postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        success = False
        detail = 'Something wrong'
        post_id = postdata['post_id']
        test_login = self.test_login(postdata)
        success = test_login['success']
        if success:
            device_id = test_login['device_id']
            mem_id = test_login['mem_id']
            url = '{}/post_boost.php'.format(self.webbaseurl)
            data = {
                'mem_id': mem_id,
                'device_id': device_id,
                'device_type': 6,
                'web_id': post_id
            }
            r = self.httprequestObj.http_post(url, data=data)
            response = r.json()
            if str(response['response']) == '0':
                success = True
                detail = 'Boost successful'
            else:
                success = False
                detail = response['result_msg']
        
        time_end = datetime.datetime.utcnow()
        return {
            "success": success,
            "usage_time": time_end - time_start,
            "start_time": time_start,
            "end_time": time_end,
            "detail": detail,
            "log_id": postdata['log_id'],
            "ds_id": postdata['ds_id'],
            "post_id": postdata['post_id'],
            "websitename": "livinginsider",
            "post_view": ''
        }

    def print_debug(self, msg):
        if self.debug == 1:
            print(msg)
        return True
