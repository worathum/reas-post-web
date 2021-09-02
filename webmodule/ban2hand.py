# -*- coding: utf-8 -*-

from .lib_httprequest import *
from bs4 import BeautifulSoup
from .lib_captcha import *
import os.path
# from urlparse import urlparse
import re
import json
import datetime
import sys
import requests
import shutil
from urllib.parse import unquote
import urllib.request
import urllib
from PIL import Image

httprequestObj = lib_httprequest()
captcha = lib_captcha()


class ban2hand():

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
        self.webname = 'ban2hand'

    def print_debug(self, msg):
        if self.debug == 1:
            print(msg)
        return True

    def register_user(self, userdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        os.system('touch ./imgtmp/captcha.jpeg')
        r = httprequestObj.http_get('https://www.ban2hand.com/captcha.php')
        with open("./imgtmp/captcha.jpeg", 'wb') as img_f:
            img_f.write(r.content)

        captcha_text = captcha.imageCaptcha('./imgtmp/captcha.jpeg')
        # print(captcha_text)

        username = userdata['user'].split('@')[0]

        datapost = {
            "username": username,
            "password": userdata['pass'],
            "cpassword": userdata['pass'],
            "email": userdata['user'],
            "captcha": captcha_text,
            "accept": "1"
        }

        r = httprequestObj.http_post('https://www.ban2hand.com/signup.php', data=datapost)
        # print(r.url)
        # print(r.status_code)
        data = r.text
        # print(data)

        if 'Activate User Account Complete' in data:
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
        time_start = datetime.datetime.utcnow()

        username = userdata['user'].split('@')[0]

        datapost = {
            "username": username,
            "password": userdata['pass'],
            "sendurl": ""
        }
        
        r = httprequestObj.http_post('https://www.ban2hand.com/signin2.php', data=datapost)
        # print(r.url)
        # print(r.status_code)
        data = r.text
        """ with open('./log/testban2hand.html','w') as f:
            f.write(data) """
        
        if 'Welcome ! ' in r.text:
            success = True
            detail = "Login successful"
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
            'ds_id': userdata['ds_id'],
            "detail": detail,
            "websitename": self.webname,
        }

    def get_address(self, content, choice):

        for reg in content:
            if reg.get('value') == choice or reg.get('value') == choice.replace(" ", ""):
                # print('Direct match')
                return reg.get('value')

        for reg in content:
            if reg.get('value') in choice or reg.get('value').replace(" ", "") in choice.replace(" ",
                                                                                                 "") or choice.replace(
                    " ", "") in reg.get('value').replace(" ", ""):
                # print('Partial match')
                return reg.get('value')

        # print('No match')
        return content[0].get('value')

    def create_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""

        username = postdata['user'].split('@')[0]

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
            getProdId = {'1': '2', '2': '6', '3': '4', '4': '4',
                         '5': '3', '6': '5', '7': '9', '8': '10', '9': '8', '10': '10', '25': '10'}

            try:
                theprodid = getProdId[proid[str(postdata['property_type'])]]
                postdata['property_type'] = str(proid[str(postdata['property_type'])])
            except:
                theprodid = getProdId[str(postdata['property_type'])]

            province_id = ''

            prod_address = ""
            for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'],
                        postdata['addr_district'], postdata['addr_province']]:
                if add is not None:
                    prod_address += add + " "
            prod_address = prod_address[:-1]

            r = httprequestObj.http_get('https://www.ban2hand.com/addhome.php')
            # print(r.url)
            # print(r.status_code)

            soup = BeautifulSoup(r.content, self.parser)
            provinces = soup.find('select', {'name': 'place'}).findChildren('option')[1:]

            province_id = self.get_address(provinces, postdata['addr_province'])

            province_url = 'https://www.ban2hand.com/findState.php'

            r = httprequestObj.http_get(province_url, params={'country': province_id})
            # print(r.url)
            # print(r.status_code)

            soup1 = BeautifulSoup(r.content, self.parser)
            districts = soup1.find_all('option')[1:]

            district_id = self.get_address(districts, postdata['addr_district'])

            district_url = 'https://www.ban2hand.com/findCity.php'

            r = httprequestObj.http_get(district_url, params={'country': province_id, 'state': district_id})
            # print(r.url)
            # print(r.status_code)

            soup2 = BeautifulSoup(r.content, self.parser)
            sub_districts = soup2.find_all('option')[1:]

            sub_district_id = self.get_address(sub_districts, postdata['addr_sub_district'])

            id_user = soup.find('input', {'name': 'id_user'}).get('value')
            id = soup.find('input', {'name': 'id'}).get('value')
            ogrp = soup.find('input', {'name': 'ogrp'}).get('value')
            job = soup.find('input', {'name': 'job'}).get('value')

            start_header = '<html><head><title></title></head><body><p>'
            end_header = '</p></body></html>'

            desc = (start_header + postdata['post_description_th'] + end_header).replace('\n', '<br>')
            # print(desc)

            datapost = [
                ('grp', (None, theprodid)),
                ('rai', (None, str(postdata['land_size_rai']))),
                ('ngan', (None, str(postdata['land_size_ngan']))),
                ('wa', (None, str(postdata['land_size_wa']))),
                ('size', (None, str(postdata['floorarea_sqm']))),
                ('sizeroom', (None, None)),
                ('bedroom', (None, str(postdata['bed_room']))),
                ('bathroom', (None, str(postdata['bath_room']))),
                ('nfloor', (None, str(postdata['floor_total']))),
                ('on_floor', (None, str(postdata['floor_level']))),
                ('livingroom', (None, None)),
                ('parking', (None, None)),
                ('materoom', (None, None)),
                ('age', (None, None)),
                ('aircon', (None, None)),
                ('topic', (None, postdata['post_title_th'])),
                ('detail', (None, desc)),
                ('place', (None, province_id)),
                ('AP', (None, district_id)),
                ('TB', (None, sub_district_id)),
                ('address', (None, postdata['addr_sub_district'])),
                ('road', (None, postdata['addr_road'])),
                ('street', (None, postdata['addr_soi'])),
                ('gmap1', (None, str(postdata['geo_latitude']))),
                ('gmap2', (None, str(postdata['geo_longitude']))),
                ('kw', (None, "")),
                ('price', (None, str(postdata['price_baht']))),
                ('punit', (None, 'บาท')),
                ('name', (None, postdata['name'])),
                ('tel', (None, postdata['mobile'])),
                ('email', (None, postdata['email'])),
                ('event', (None, 'upload')),
                ('id_user', (None, id_user)),
                ('id', (None, id)),
                ('ogrp', (None, ogrp)),
                ('job', (None, job))
            ]

            if postdata['listing_type'] != 'เช่า':
                # sell
                datapost.append(('type_p', (None, '1')))
            else:
                # rent
                datapost.append(('type_p', (None, '2')))

            for i in range(5):
                index_name = 'bicm' + str(i + 1) + '[]'
                if i < len(postdata['post_images']):
                    filename = str(i + 1) + '.jpeg'
                    img = postdata['post_images'][i]
                    datapost.append((index_name, (filename, open(img, 'rb'), 'image/jpeg')))
                else:
                    datapost.append((index_name, (None, None)))

            r = httprequestObj.http_post('https://www.ban2hand.com/savehome.php', data={}, files=datapost)
            # print(r.url)
            # print(r.status_code)

            if 'บันทึกรายการเสร็จสมบูรณ์' in r.text:
                soup = BeautifulSoup(r.content, self.parser)
                post_url = soup.find('a', 'BB-HGRAYS').get('href')
                post_id = post_url.split('/')[-2].split('-')[-1]
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
            "post_url": post_url,
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
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

        username = postdata['user'].split('@')[0]

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
            getProdId = {'1': '2', '2': '6', '3': '4', '4': '4',
                         '5': '3', '6': '5', '7': '9', '8': '10', '9': '8', '10': '10', '25': '10'}

            try:
                theprodid = getProdId[proid[str(postdata['property_type'])]]
                postdata['property_type'] = str(proid[str(postdata['property_type'])])
            except:
                theprodid = getProdId[str(postdata['property_type'])]

            province_id = ''

            prod_address = ""
            for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'],
                        postdata['addr_district'], postdata['addr_province']]:
                if add is not None:
                    prod_address += add + " "
            prod_address = prod_address[:-1]

            r = httprequestObj.http_get('https://www.ban2hand.com/', params={'ac': 'complete'})
            # print(r.url)
            # print(r.status_code)

            soup = BeautifulSoup(r.content, self.parser)
            tot_url = soup.find('a', {'title': 'logout'}).get('href')
            # print(tot_url)
            user_id = tot_url.split('=')[1].split('&')[0]
            # print(user_id)

            params = {
                'id': user_id,
                'job': 'product',
                'topic': 'all'
            }

            r = httprequestObj.http_get('https://www.ban2hand.com/membertool.php', params=params)
            # print(r.url)
            # print(r.status_code)

            soup = BeautifulSoup(r.content, self.parser)
            all_posts = soup.find_all('a', 'b fc-gray-brown')

            post_found = False

            for post in all_posts:
                post_id = post.get('href').split('/')[-2].split('-')[-1]
                if post_id == postdata['post_id']:
                    # print('Found post')
                    post_found = True
                    break

            if post_found:

                r = httprequestObj.http_get('https://www.ban2hand.com/addhome.php', params={'eid': post_id})
                # print(r.url)
                # print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                provinces = soup.find('select', {'name': 'place'}).findChildren('option')[1:]

                province_id = self.get_address(provinces, postdata['addr_province'])

                province_url = 'https://www.ban2hand.com/findState.php'

                r = httprequestObj.http_get(province_url, params={'country': province_id})
                # print(r.url)
                # print(r.status_code)

                soup1 = BeautifulSoup(r.content, self.parser)
                districts = soup1.find_all('option')[1:]

                district_id = self.get_address(districts, postdata['addr_district'])

                district_url = 'https://www.ban2hand.com/findCity.php'

                r = httprequestObj.http_get(district_url, params={'country': province_id, 'state': district_id})
                # print(r.url)
                # print(r.status_code)

                soup2 = BeautifulSoup(r.content, self.parser)
                sub_districts = soup2.find_all('option')[1:]

                sub_district_id = self.get_address(sub_districts, postdata['addr_sub_district'])

                id_user = soup.find('input', {'name': 'id_user'}).get('value')
                id = soup.find('input', {'name': 'id'}).get('value')
                ogrp = soup.find('input', {'name': 'ogrp'}).get('value')
                job = soup.find('input', {'name': 'job'}).get('value')

                start_header = '<html><head><title></title></head><body><p>'
                end_header = '</p></body></html>'
                desc = (start_header + postdata['post_description_th'] + end_header).replace('\r\n', '<br>')
                # print(desc)

                datapost = [
                    ('grp', (None, theprodid)),
                    ('rai', (None, postdata['land_size_rai'])),
                    ('ngan', (None, postdata['land_size_ngan'])),
                    ('wa', (None, postdata['land_size_wa'])),
                    ('size', (None, postdata['floor_area'])),
                    ('sizeroom', (None, None)),
                    ('bedroom', (None, postdata['bed_room'])),
                    ('bathroom', (None, postdata['bath_room'])),
                    ('nfloor', (None, postdata['floor_total'])),
                    ('on_floor', (None, postdata['floor_level'])),
                    ('livingroom', (None, None)),
                    ('parking', (None, None)),
                    ('materoom', (None, None)),
                    ('age', (None, None)),
                    ('aircon', (None, None)),
                    ('topic', (None, postdata['post_title_th'])),
                    ('detail', (None, desc)),
                    ('place', (None, province_id)),
                    ('AP', (None, district_id)),
                    ('TB', (None, sub_district_id)),
                    ('address', (None, postdata['addr_sub_district'])),
                    ('road', (None, postdata['addr_road'])),
                    ('street', (None, postdata['addr_soi'])),
                    ('gmap1', (None, postdata['geo_latitude'])),
                    ('gmap2', (None, postdata['geo_longitude'])),
                    ('kw', (None, "")),
                    ('price', (None, postdata['price_baht'])),
                    ('punit', (None, 'บาท')),
                    ('name', (None, postdata['name'])),
                    ('tel', (None, postdata['mobile'])),
                    ('email', (None, postdata['email'])),
                    ('event', (None, 'upload')),
                    ('id_user', (None, id_user)),
                    ('id', (None, id)),
                    ('ogrp', (None, ogrp)),
                    ('job', (None, job))
                ]

                if postdata['listing_type'] != 'เช่า':
                    # sell
                    datapost.append(('type_p', (None, '1')))
                else:
                    # rent
                    datapost.append(('type_p', (None, '2')))

                old_images = soup.find_all('li')

                for image in old_images:
                    pic_id = image.get('id').split('_')[-1]
                    # print(pic_id)
                    r = httprequestObj.http_get('https://www.ban2hand.com/delpici.php', params={'id': pic_id})
                    # print(r.url)
                    # print(r.status_code)

                for i in range(5):
                    index_name = 'bicm' + str(i + 1) + '[]'
                    if i < len(postdata['post_images']):
                        filename = str(i + 1) + '.jpeg'
                        img = postdata['post_images'][i]
                        datapost.append((index_name, (filename, open(img, 'rb'), 'image/jpeg')))
                    else:
                        datapost.append((index_name, (None, None)))

                r = httprequestObj.http_post('https://www.ban2hand.com/savehome.php', data={}, files=datapost)
                # print(r.url)
                # print(r.status_code)

                if 'บันทึกรายการเสร็จสมบูรณ์' in r.text:
                    soup = BeautifulSoup(r.content, self.parser)
                    post_url = soup.find('a', 'BB-HGRAYS').get('href')
                    post_id = post_url.split('/')[-2].split('-')[-1]
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
            "ds_id": postdata['ds_id'],
            "post_id": postdata['post_id'],
            "log_id": postdata['log_id'],
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

        username = postdata['user'].split('@')[0]

        if success:

            r = httprequestObj.http_get('https://www.ban2hand.com/', params={'ac': 'complete'})
            # print(r.url)
            # print(r.status_code)

            soup = BeautifulSoup(r.content, self.parser)
            tot_url = soup.find('a', {'title': 'logout'}).get('href')
            # print(tot_url)
            user_id = tot_url.split('=')[1].split('&')[0]
            # print(user_id)

            params = {
                'id': user_id,
                'job': 'product',
                'topic': 'all'
            }

            r = httprequestObj.http_get('https://www.ban2hand.com/membertool.php', params=params)
            # print(r.url)
            # print(r.status_code)

            soup = BeautifulSoup(r.content, self.parser)
            all_posts = soup.find_all('a', 'b fc-gray-brown')

            post_found = False

            for post in all_posts:
                post_id = post.get('href').split('/')[-2].split('-')[-1]
                if post_id == postdata['post_id']:
                    # print('Found post')
                    post_found = True
                    break

            if post_found:

                params = {
                    'id': post_id,
                    'action': 'update'
                }

                r = httprequestObj.http_get('https://www.ban2hand.com/product.php?id=105654&action=update', params=params)
                # print(r.url)
                # print(r.status_code)

                success = True
                detail = "Post boosted successfully"

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
            "ds_id": postdata['ds_id'],
            "post_id": postdata['post_id'],
            "log_id": postdata['log_id'],
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

            r = httprequestObj.http_get('https://www.ban2hand.com/', params={'ac': 'complete'})
            #print(r.url)
            # print(r.status_code)

            soup = BeautifulSoup(r.content, self.parser)
            tot_url = soup.find('a', {'title': 'logout'}).get('href')
            # print(tot_url)
            user_id = tot_url.split('=')[1].split('&')[0]
            # print(user_id)

            params = {
                'id': user_id,
                'job': 'product',
                'topic': 'all'
            }

            r = httprequestObj.http_get('https://www.ban2hand.com/membertool.php', params=params)
            # print(r.url)
            # print(r.status_code)

            soup = BeautifulSoup(r.content, self.parser)
            all_posts = soup.find_all('a', 'b fc-gray-brown')

            post_found = False

            for post in all_posts:
                post_id = post.get('href').split('/')[-2].split('-')[-1]
                if post_id == postdata['post_id']:
                    # print('Found post')
                    post_found = True
                    break

            if post_found:

                params = {
                    'id': post_id,
                    'job': 'del'
                }

                r = httprequestObj.http_get('https://www.ban2hand.com/product.php?job=del&id=105644', params=params)
                # print(r.url)
                # print(r.status_code)

                success = True
                detail = "Post deleted successfully"

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
            "ds_id": postdata['ds_id'],
            "post_id": postdata['post_id'],
            "log_id": postdata['log_id'],
            "detail": detail,
            "websitename": self.webname,
        }

    def search_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""
        post_create = ''
        post_view = ''

        if success:

            r = httprequestObj.http_get('https://www.ban2hand.com/', params={'ac': 'complete'})
            # print(r.url)
            # print(r.status_code)

            soup = BeautifulSoup(r.content, self.parser)
            tot_url = soup.find('a', {'title': 'logout'}).get('href')
            # print(tot_url)
            user_id = tot_url.split('=')[1].split('&')[0]
            # print(user_id)

            params = {
                'id': user_id,
                'job': 'product',
                'topic': 'all'
            }

            r = httprequestObj.http_get('https://www.ban2hand.com/membertool.php', params=params)
            # print(r.url)
            # print(r.status_code)

            soup = BeautifulSoup(r.content, self.parser)
            all_posts = soup.find_all('a', {'class':'b fc-gray-brown'})

            post_found = False

            for post in all_posts:
                post_title = str(post.get_text())
                postdata['post_title_th'] = str(postdata['post_title_th']).strip()
                # print(post_title,'\n',postdata['post_title_th'],'\n\n\n')
                if  postdata['post_title_th'] in post_title or post_title in postdata['post_title_th']:
                    # print('Found post')
                    post_url = post.get('href')
                    post_id = post_url.split('/')[-2].split('-')[-1]
                    # print(post_url)

                    r = httprequestObj.http_get(post_url)
                    # print(r.url)
                    # print(r.status_code)

                    soup1 = BeautifulSoup(r.content, self.parser)
                    info = soup1.find_all('div','fl ml7 fs13 mt8')
                    post_create = info[0].string
                    post_view = info[1].string
                    post_found = True
                    break

            if post_found:
                success = True
                detail = "Post Found"

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
            "post_url": post_url,
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
            "log_id": postdata['log_id'],
            "post_create": str(post_create),
            "post_modified": '',
            "post_view": str(post_view),
            "detail": detail,
            "websitename": self.webname,
        }
