# -*- coding: utf-8 -*-
import uuid

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


with open("./static/teedinzone_province.json") as f:
    province_id_map = json.load(f)

with open("./static/teedinzone.json") as f:
    id_regionid_map = json.load(f)


class teedinzone():

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
        self.webname = 'teedinzone'
        self.session = lib_httprequest()

    def print_debug(self, msg):
        if self.debug == 1:
            print(msg)
        return True

    def logout_user(self):
        url = 'https://teedinzone.com/index.php?page=main&action=logout'
        self.session.http_get(url)

    def register_user(self, userdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        self.logout_user()
        time_start = datetime.datetime.utcnow()

        params = {
            'page': 'register',
            'action': 'register'
        }

        r = self.session.http_get('https://teedinzone.com/index.php', params=params)
        # print(r.url)
        # print(r.status_code)

        soup = BeautifulSoup(r.text, self.parser)
        csrf_name = soup.find('input', {'name': 'CSRFName'}).get('value')
        csrf_token = soup.find('input', {'name': 'CSRFToken'}).get('value')

        reg_data = {
            'CSRFName': csrf_name,
            'CSRFToken': csrf_token,
            'page': 'register',
            'action': 'register_post',
            's_name': userdata['name_th'] + ' ' + userdata['surname_th'],
            's_password': userdata['pass'],
            's_password2': userdata['pass'],
            's_phone_mobile': userdata['tel'],
            'b_company': '0',
            's_email': userdata['user']
        }

        r = self.session.http_post('https://teedinzone.com/index.php', data=reg_data)
        # print(r.url)
        # print(r.status_code)

        if 'การสร้างบัญชีของคุณเสร็จเรียบร้อย' in r.text:
            success = True
            detail = "Registered successfully"
        else:
            success = False
            detail = "Couldnot register"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            'ds_id': userdata['ds_id'],
            "detail": detail,
            "websitename": self.webname,
        }

    def test_login(self, userdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        self.logout_user()
        time_start = datetime.datetime.utcnow()

        params = {
            'page': 'login',
            'action': 'register'
        }
        self.session.http_get('https://teedinzone.com/index.php?page=main&action=logout')
        r = self.session.http_get('https://teedinzone.com/index.php', params=params)
        # print(r.url)
        # print(r.status_code)

        soup = BeautifulSoup(r.text, self.parser)
        csrf_name = soup.find('input', {'name': 'CSRFName'}).get('value')
        csrf_token = soup.find('input', {'name': 'CSRFToken'}).get('value')

        reg_data = {
            'CSRFName': csrf_name,
            'CSRFToken': csrf_token,
            'page': 'login',
            'action': 'login_post',
            'email': userdata['user'],
            'password': userdata['pass']
        }

        r = self.session.http_post('https://teedinzone.com/index.php', data=reg_data)
        # print(r.url)
        # print(r.status_code)

        if 'บัญชีผู้ใช้งานนของฉัน' in r.text and 'ออกจากระบบ' in r.text:
            success = True
            detail = "Login successful"
        else:
            success = False
            detail = "Login failed"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            'ds_id': userdata['ds_id'],
            "detail": detail,
            "websitename": self.webname,
        }

    def create_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""

        if success:

            if 'web_project_name' not in postdata or postdata['web_project_name'] is None:
                if 'project_name' in postdata and postdata['project_name'] is not None:
                    postdata['web_project_name'] = postdata['project_name']
                else:
                    postdata['web_project_name'] = postdata['post_title_th']

            proid = {
                'คอนโด': '1',
                'บ้านเดี่ยว': '2',
                'บ้านแฝด': '3',
                'ทาวน์เฮ้าส์': '4',
                'ตึกแถว-อาคารพาณิชย์': '5',
                'ที่ดิน': '6',
                'อพาร์ทเมนท์': '7',
                'โรงแรม': '8',
                'ออฟฟิศสำนักงาน': '9',
                'โกดัง-โรงงาน': '10',
                'โรงงาน': '25'
            }
            getProdId = {'1': '49', '2': '43', '3': '43', '4': '43',
                         '5': '50', '6': '49', '7': '43', '8': '47', '9': '50', '10': '50', '25': '50'}

            try:
                theprodid = getProdId[proid[str(postdata['property_type'])]]
                postdata['property_type'] = proid[str(postdata['property_type'])]
            except:
                theprodid = getProdId[str(postdata['property_type'])]

            province_found = False
            province_id = ''
            region_id = ''

            for (key, value) in province_id_map.items():
                if postdata['addr_province'] == key or postdata['addr_province'].replace(' ', '') == key:
                    province_id = value
                    region_id = id_regionid_map[province_id]
                    # print("Full match")
                    province_found = True
                    break

            if not province_found:
                for (key, value) in province_id_map.items():
                    if postdata['addr_province'] in key or postdata['addr_province'].replace(' ', '') in key:
                        province_id = value
                        region_id = id_regionid_map[province_id]
                        # print("Partial match")
                        province_found = True
                        break

            if not province_found:
                province_id = next(iter(province_id_map.values()))
                region_id = id_regionid_map[province_id]
                # print("No match")

            prod_address = ""
            for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'],
                        postdata['addr_district'], postdata['addr_province']]:
                if add is not None:
                    prod_address += add + " "
            prod_address = prod_address[:-1]

            if postdata['property_type'] == '6':
                category = '1'
                sub_category = '10'
            else:
                category = '4'
                sub_category = theprodid

            params = {
                'page': 'item',
                'action': 'item_add'
            }

            r = self.session.http_get('https://teedinzone.com/index.php', params=params)
            # print(r.url)
            # print(r.status_code)

            soup = BeautifulSoup(r.text, self.parser)
            csrf_name = soup.find('input', {'name': 'CSRFName'}).get('value')
            csrf_token = soup.find('input', {'name': 'CSRFToken'}).get('value')

            datapost = [
                ('CSRFName', (None, csrf_name)),
                ('CSRFToken', (None, csrf_token)),
                ('action', (None, 'item_add_post')),
                ('page', (None, 'item')),
                ('catId', (None, sub_category)),
                ('select_1', (None, category)),
                ('select_2', (None, sub_category)),
                ('title[th_TH]', (None, postdata['post_title_th'][:100])),
                ('description[th_TH]', (None, postdata['post_description_th'].replace('\r\n', '&#13;&#10;'))),
                ('price', (None, postdata['price_baht'])),
                ('currency', (None, 'THB')),
                ('regionId', (None, region_id)),
                ('cityId', (None, province_id)),
                ('cityArea', (None, postdata['addr_district'])),
                ('address', (None, prod_address)),
                ('meta[1]', (None, postdata['line']))
            ]

            file = []
            params = {
                'page': 'ajax',
                'action': 'ajax_upload'
            }

            for i, img in enumerate(postdata['post_images']):
                with open(img, 'rb') as img_file:
                    cont = img_file.read()
                filename = str(i) + '.jpeg'
                file_uuid = str(uuid.uuid1())
                file_length = len(cont)

                # print('File properties')
                # print(file_uuid)
                # print(file_length)

                file.append(('qquuid', (None, file_uuid)))
                file.append(('qqtotalfilesize', (None, file_length)))
                file.append(('qqfile', (filename, open(img, "rb"), "image/jpeg")))
                r = self.session.http_post('https://teedinzone.com/index.php', params=params, data={}, files=file)
                # print(r.url)
                # print(r.status_code)

                upload_name = json.loads(r.text)['uploadName']

                datapost.append(('ajax_photos[]', (None, upload_name)))
                datapost.append(('qqfile', (filename, open(img, "rb"), "image/jpeg")))

            # print('Posted images')

            r = self.session.http_post('https://teedinzone.com/index.php', data={}, files=datapost)
            # print(r.url)
            # print(r.status_code)

            register_redirect_page = r.text

            params = {
                'page': 'user',
                'action': 'dashboard'
            }

            r = self.session.http_get('https://teedinzone.com/index.php', params=params)
            # print(r.url)
            # print(r.status_code)

            soup = BeautifulSoup(r.content, self.parser)
            latest_block = soup.find('div', 'col-sm-12 latest-item').findChild('div')
            # print(latest_block.findChildren('div', recursive=False))

            # title = latest_block.findChildren('div', recursive=False)[0].find('p', 'text').string

            if 'รายการของคุณได้ถูกเผยแพร' in register_redirect_page:
                post_url = latest_block.findChildren('div', recursive=False)[2].find('div', 'img').find('a').get('href')
                post_id = post_url.split('=')[-1]
                success = True
                detail = "Post created successfully"

            else:
                success = False
                detail = "Couldnot create post"

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
            'ds_id': postdata['ds_id'],
            'post_id': post_id,
            'post_url': post_url,
            "detail": detail,
            "websitename": self.webname,
        }

    def edit_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""

        if success:

            ind = 0
            post_found = True

            """while True:
                ind += 1
                params = {
                    'page': 'user',
                    'action': 'items',
                    'iPage': str(ind)
                }

                r = self.session.http_get('https://teedinzone.com/index.php', params=params)
                # print(ind)
                # print(r.url)
                # print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                all_posts = soup.find('div', 'col-sm-9').findChildren('div', recursive=False)[:-1]
                # print(len(all_posts))

                if len(all_posts) == 0:
                    break

                for post in all_posts:
                    post_url = post.find('div').findChildren('div', recursive=False)[3].find('a', 'btn').get('href')
                    post_id = post_url.split('=')[-1]
                    if post_id == postdata['post_id']:
                        # print("Found post")
                        post_found = True
                        break

                if post_found:
                    break"""

            if post_found:

                if 'web_project_name' not in postdata or postdata['web_project_name'] is None:
                    if 'project_name' in postdata and postdata['project_name'] is not None:
                        postdata['web_project_name'] = postdata['project_name']
                    else:
                        postdata['web_project_name'] = postdata['post_title_th']

                proid = {
                    'คอนโด': '1',
                    'บ้านเดี่ยว': '2',
                    'บ้านแฝด': '3',
                    'ทาวน์เฮ้าส์': '4',
                    'ตึกแถว-อาคารพาณิชย์': '5',
                    'ที่ดิน': '6',
                    'อพาร์ทเมนท์': '7',
                    'โรงแรม': '8',
                    'ออฟฟิศสำนักงาน': '9',
                    'โกดัง-โรงงาน': '10',
                    'โรงงาน': '25'
                }
                getProdId = {'1': '49', '2': '43', '3': '43', '4': '43',
                             '5': '50', '6': None, '7': '43', '8': None, '9': '50', '10': '50', '25': '50'}

                try:
                    theprodid = getProdId[proid[str(postdata['property_type'])]]
                    postdata['property_type'] = proid[str(postdata['property_type'])]
                except:
                    theprodid = getProdId[str(postdata['property_type'])]

                province_found = False
                province_id = ''
                region_id = ''

                for (key, value) in province_id_map.items():
                    if postdata['addr_province'] == key or postdata['addr_province'].replace(' ', '') == key:
                        province_id = value
                        region_id = id_regionid_map[province_id]
                        # print("Full match")
                        province_found = True
                        break

                if not province_found:
                    for (key, value) in province_id_map.items():
                        if postdata['addr_province'] in key or postdata['addr_province'].replace(' ', '') in key:
                            province_id = value
                            region_id = id_regionid_map[province_id]
                            # print("Partial match")
                            province_found = True
                            break

                if not province_found:
                    province_id = next(iter(province_id_map.values()))
                    region_id = id_regionid_map[province_id]
                    # print("No match")

                prod_address = ""
                for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'],
                            postdata['addr_district'], postdata['addr_province']]:
                    if add is not None:
                        prod_address += add + " "
                prod_address = prod_address[:-1]

                if postdata['property_type'] == '6':
                    category = '1'
                    sub_category = '9'
                else:
                    category = '4'
                    sub_category = theprodid

                params = {
                    'page': 'item',
                    'action': 'item_edit',
                    'id': postdata['post_id']
                }

                r = self.session.http_get('https://teedinzone.com/index.php', params=params)
                # print(r.url)
                # print(r.status_code)

                soup = BeautifulSoup(r.text, self.parser)
                csrf_name = soup.find('input', {'name': 'CSRFName'}).get('value')
                csrf_token = soup.find('input', {'name': 'CSRFToken'}).get('value')
                secret = soup.find('input', {'name': 'secret'}).get('value')

                old_photos = soup.find('ul', 'qq-upload-list')
                if old_photos is not None:
                    old_photos = old_photos.findChildren('li')
                    # print(old_photos)

                    params = {
                        'page': 'ajax',
                        'action': 'delete_image'
                    }

                    for photo in old_photos:
                        photo_block = photo.find('a', 'qq-upload-delete')
                        params['id'] = photo_block.get('photoid')
                        params['item'] = photo_block.get('itemid')
                        params['code'] = photo_block.get('photoname')

                        r = self.session.http_post('https://teedinzone.com/index.php', params=params, data={})
                        # print(r.url)
                        # print(r.status_code)

                datapost = [
                    ('CSRFName', (None, csrf_name)),
                    ('CSRFToken', (None, csrf_token)),
                    ('secret', (None, secret)),
                    ('id', (None, postdata['post_id'])),
                    ('action', (None, 'item_edit_post')),
                    ('page', (None, 'item')),
                    ('catId', (None, sub_category)),
                    ('select_1', (None, category)),
                    ('select_2', (None, sub_category)),
                    ('title[th_TH]', (None, postdata['post_title_th'][:100])),
                    ('description[th_TH]', (None, postdata['post_description_th'].replace('\r\n', '&#13;&#10;'))),
                    ('price', (None, postdata['price_baht'])),
                    ('currency', (None, 'THB')),
                    ('regionId', (None, region_id)),
                    ('cityId', (None, province_id)),
                    ('cityArea', (None, postdata['addr_district'])),
                    ('address', (None, prod_address)),
                    ('meta[1]', (None, postdata['line']))
                ]

                file = []

                params_validate = {
                    'page': 'ajax',
                    'action': 'ajax_validate',
                    'id': postdata['post_id'],
                    'secret': secret
                }

                params_upload = {
                    'page': 'ajax',
                    'action': 'ajax_upload'
                }

                for i, img in enumerate(postdata['post_images']):
                    with open(img, 'rb') as img_file:
                        cont = img_file.read()
                    filename = str(i) + '.jpeg'
                    file_uuid = str(uuid.uuid1())
                    file_length = len(cont)

                    # print('File properties')
                    # print(file_uuid)
                    # print(file_length)

                    r = self.session.http_get('https://teedinzone.com/index.php', params=params_validate)

                    file.append(('qquuid', (None, file_uuid)))
                    file.append(('qqtotalfilesize', (None, file_length)))
                    file.append(('qqfile', (filename, open(img, "rb"), "image/jpeg")))
                    r = self.session.http_post('https://teedinzone.com/index.php', params=params_upload, data={},
                                                 files=file)
                    # print(r.url)
                    # print(r.status_code)

                    upload_name = json.loads(r.text)['uploadName']

                    # print(upload_name)

                    datapost.append(('ajax_photos[]', (None, upload_name)))
                    datapost.append(('qqfile', (filename, open(img, "rb"), "image/jpeg")))

                # print('Posted images')

                r = self.session.http_post('https://teedinzone.com/index.php', data={}, files=datapost)
                # print(r.url)
                # print(r.status_code)

                if 'ดีมาก! คุณเพิ่งจะทำการอัพเดตรายการของคุณ' in r.text:
                    success = True
                    detail = "Post edited successfully"

                else:
                    success = False
                    detail = "Couldnot edit post"

            else:
                success = False
                detail = "No post with given post_id"

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
            'ds_id': postdata['ds_id'],
            'log_id': postdata['log_id'],
            'post_id': postdata["post_id"],
            "detail": detail,
            "websitename": self.webname,
        }

    def boost_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""

        if success:

            ind = 0
            post_found = True

            """while True:
                ind += 1
                params = {
                    'page': 'user',
                    'action': 'items',
                    'iPage': str(ind)
                }

                r = self.session.http_get('https://teedinzone.com/index.php', params=params)
                # print(ind)
                # print(r.url)
                # print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                all_posts = soup.find('div', 'col-sm-9').findChildren('div', recursive=False)[:-1]
                # print(len(all_posts))

                if len(all_posts) == 0:
                    break

                for post in all_posts:
                    post_url = post.find('div').findChildren('div', recursive=False)[3].find('a', 'btn').get('href')
                    post_id = post_url.split('=')[-1]
                    if post_id == postdata['post_id']:
                        # print("Found post")
                        post_found = True
                        break

                if post_found:
                    break"""

            if post_found:

                params = {
                    'page': 'item',
                    'action': 'item_edit',
                    'id': postdata['post_id']
                }

                r = self.session.http_get('https://teedinzone.com/index.php', params=params)
                # print(r.url)
                # print(r.status_code)

                soup = BeautifulSoup(r.text, self.parser)
                csrf_name = soup.find('input', {'name': 'CSRFName'}).get('value')
                csrf_token = soup.find('input', {'name': 'CSRFToken'}).get('value')
                secret = soup.find('input', {'name': 'secret'}).get('value')
                catId = soup.find('input', {'name': 'catId'}).get('value')
                price = soup.find('input', {'name': 'price'}).get('value')
                regionId = soup.find('select', {'name': 'regionId'}).get('value')
                cityId = soup.find('select', {'name': 'cityId'}).get('value')
                cityArea = soup.find('input', {'name': 'cityArea'}).get('value')
                address = soup.find('input', {'name': 'address'}).get('value')

                datapost = [
                    ('CSRFName', (None, csrf_name)),
                    ('CSRFToken', (None, csrf_token)),
                    ('catId', (None, catId)),
                    ('price', (None, price)),
                    ('regionId', (None, regionId)),
                    ('cityId', (None, cityId)),
                    ('cityArea', (None, cityArea)),
                    ('address', (None, address)),
                    ('secret', (None, secret)),
                    ('id', (None, postdata['post_id'])),
                    ('action', (None, 'item_edit_post')),
                    ('page', (None, 'item')),
                ]

                r = self.session.http_post('https://teedinzone.com/index.php', data={}, files=datapost)
                # print(r.url)
                # print(r.status_code)

                if 'ดีมาก! คุณเพิ่งจะทำการอัพเดตรายการของคุณ' in r.text:
                    success = True
                    detail = "Post boosted successfully"
                else:
                    success = False
                    detail = "Couldnot boost post"

            else:
                success = False
                detail = "No post with given post_id"

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
            'ds_id': postdata['ds_id'],
            'log_id': postdata['log_id'],
            'post_id': post_id,
            "detail": detail,
            "websitename": self.webname,
        }

    def search_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        # print(detail)
        post_id = ""
        post_url = ""
        post_created = ""
        post_modified = ""
        post_view = ""

        if success:

            ind = 0
            post_found = False

            while True:
                ind += 1
                params = {
                    'page': 'user',
                    'action': 'items',
                    'iPage': str(ind)
                }

                r = self.session.http_get('https://teedinzone.com/index.php', params=params)
                # print(ind)
                # print(r.url)
                # print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                all_posts = soup.find('div', 'col-sm-9').findChildren('div', recursive=False)[:-1]
                # print(len(all_posts))

                if len(all_posts) == 0:
                    break

                for post in all_posts:
                    post_title = post.findChild('div').findChildren('div', recursive=False)[0].find('p', 'text').string[:-3]
                    # print(post_title)

                    if post_title in postdata['post_title_th']:
                        post_url = post.findChild('div').findChildren('div', recursive=False)[3].find('a', 'btn').get(
                            'href')
                        post_id = post_url.split('=')[-1]
                        # print(post_id)
                        params = {
                            'page': 'item',
                            'id': post_id
                        }
                        r = self.session.http_get('https://teedinzone.com/index.php', params=params)
                        # print(r.url)
                        # print(r.status_code)

                        soup_inner = BeautifulSoup(r.content, self.parser)
                        post_created = soup_inner.find('div', 'pub-date').find('p', 'text').string
                        try:
                            post_modified = soup_inner.find('div', 'mod-date').find('p', 'text').string
                        except:
                            post_modified = ""
                        # print(post_modified)
                        post_view = soup_inner.find('div', 'views').find('p', 'text').string
                        # print(post_view)

                        # print("Found post")
                        post_found = True
                        success = True
                        detail = "Post Found"
                        break

                if post_found:
                    break

            if not post_found:
                success = False
                detail = "No post with with given title"
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
            'ds_id': postdata['ds_id'],
            'log_id': postdata['log_id'],
            'post_id': post_id,
            'post_url': post_url,
            'post_created': str(post_created),
            'post_modified': str(post_modified),
            'post_view': str(post_view),
            "detail": detail,
            "websitename": self.webname,
        }

    def delete_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""

        if success:

            ind = 0
            post_found = True

            """while True:
                ind += 1
                params = {
                    'page': 'user',
                    'action': 'items',
                    'iPage': str(ind)
                }

                r = self.session.http_get('https://teedinzone.com/index.php', params=params)
                # print(ind)
                # print(r.url)
                # print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                all_posts = soup.find('div', 'col-sm-9').findChildren('div', recursive=False)[:-1]
                # print(len(all_posts))

                if len(all_posts) == 0:
                    break

                for post in all_posts:
                    post_url = post.find('div').findChildren('div', recursive=False)[3].find('a', 'btn').get('href')
                    post_id = post_url.split('=')[-1]
                    if post_id == postdata['post_id']:
                        # print("Found post")
                        post_found = True
                        break

                if post_found:
                    break"""

            if post_found:

                params = {
                    'page': 'item',
                    'action': 'item_delete',
                    'id': postdata['post_id']
                }

                r = self.session.http_post('https://teedinzone.com/index.php', params=params, data=())
                # print(r.url)
                # print(r.status_code)

                if 'รายการถูกลบ' in r.text:
                    success = True
                    detail = "Post deleted successfully"
                else:
                    success = False
                    detail = "Couldnot delete post"

            else:
                success = False
                detail = "No post with given post_id"

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
            'ds_id': postdata['ds_id'],
            'log_id': postdata['log_id'],
            'post_id': post_id,
            "detail": detail,
            "websitename": self.webname,
        }
