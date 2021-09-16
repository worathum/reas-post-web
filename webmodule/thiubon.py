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

httprequestObj = lib_httprequest()


class thiubon():

    def __init__(self):

        try:
            import configs

        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.debug = 1
        self.debugresdata = 0
        self.parser = 'html.parser'
        self.webname = 'thiubon'

    def print_debug(self, msg):
        if self.debug == 1:
            print(msg)
        return True

    def register_user(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        success = "true"
        detail = ""

        r = httprequestObj.http_get('http://classified.thiubon.com/signup.php')
        # print(r.url)
        # print(r.status_code)

        datapost = [
            ('check', (None, '1')),
            ('submit', (None, 'สมัครสมาชิกใหม่'))
        ]

        r = httprequestObj.http_post('http://classified.thiubon.com/register.php', data={}, files=datapost)
        # print(r.url)
        # print(r.status_code)

        soup = BeautifulSoup(r.content, self.parser)
        capcha = soup.find('input', {'name': 'rands'}).get('value')
        # print(capcha)

        datapost = [
            ('name', (None, postdata['name_th'] + ' ' + postdata['surname_th'])),
            ('email', (None, postdata['user'])),
            ('pass', (None, postdata['pass'])),
            ('rands', (None, capcha)),
            ('capcha', (None, capcha)),
            ('submit', (None, 'สมัครสมาชิก'))
        ]

        r = httprequestObj.http_post('http://classified.thiubon.com/p-register.php', data={}, files=datapost)
        # print(r.url)
        # print(r.status_code)
        data = r.text

        # print(data)
        if 'member/index.php' in data:
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
            'ds_id': postdata['ds_id'],
            "detail": detail,
            "websitename": self.webname,
        }

    def test_login(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        success = "true"
        detail = ""

        r = httprequestObj.http_get('http://classified.thiubon.com/signup.php')
        # print(r.url)
        # print(r.status_code)

        datapost = {
            'email': postdata['user'],
            'pass': postdata['pass'],
            'submit': 'เข้าสู่ระบบ'
        }

        r = httprequestObj.http_post('http://classified.thiubon.com/login.php', data=datapost)
        # print(r.url)
        # print(r.status_code)
        data = r.text

        # print(data)
        if 'member/index.php' in data:
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
            'ds_id': postdata['ds_id'],
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
            getProdId = {'1': '159', '2': '156', '3': '156', '4': '157',
                         '5': '158', '6': '161', '7': '162', '8': '162', '9': '162', '10': '162', '25': '162'}

            try:
                theprodid = getProdId[proid[str(postdata['property_type'])]]
                postdata['property_type'] = str(postdata['property_type'])
            except:
                theprodid = getProdId[str(postdata['property_type'])]

            prod_address = ""
            for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'],
                        postdata['addr_district'], postdata['addr_province']]:
                if add is not None:
                    prod_address += add + " "
            prod_address = prod_address[:-1]

            r = httprequestObj.http_get('http://classified.thiubon.com/member/classifieds-post.php')
            # print(r.url)
            # print(r.status_code)

            soup = BeautifulSoup(r.content, self.parser)
            capcha = soup.find('input', {'name': 'rands'}).get('value')
            # print(capcha)

            provinces = soup.find('select', {'name': 'province'}).findChildren('option')[1:]
            province_id = '1'

            for province in provinces:
                name = province.string.replace(' ', '')

                if name in postdata['addr_province'].replace(' ', '') or postdata['addr_province'].replace(' ',
                                                                                                           '') in name:
                    province_id = str(province.get('value'))
                    break

            # print('Province_id = ' + province_id)

            desc = '<p><span>' + postdata['post_description_th'].replace('\n', '</span><br><span>') + '</span></p>'

            datapost = [
                ('cate_id', (None, '23')),
                ('sub_cate_id', (None, theprodid)),
                ('post_title', (None, postdata['post_title_th'])),
                ('post_s_detail', (None, postdata['web_project_name'])),
                ('detail', (None, desc)),
                ('tag1', (None, '')),
                ('tag2', (None, '')),
                ('tag3', (None, '')),
                ('tag4', (None, '')),
                ('tag5', (None, '')),
                ('tag6', (None, '')),
                ('post_price_type', (None, '2')),
                ('post_price', (None, postdata['price_baht'])),
                ('prd_condition', (None, '3')),
                ('post_day', (None, '1')),
                ('post_comment', (None, '1')),
                ('name', (None, postdata['name'])),
                ('add', (None, prod_address)),
                ('province', (None, province_id)),
                ('tel', (None, postdata['mobile'])),
                ('email', (None, postdata['email'])),
                ('rands', (None, capcha)),
                ('capcha', (None, capcha)),
                ('submit', (None, 'ยืนยันการประกาศ'))
            ]

            if postdata['listing_type'] != 'เช่า':
                # sell
                datapost.append(('class_type_id', (None, '2')))
            else:
                # rent
                datapost.append(('class_type_id', (None, '3')))

            small_images = []

            for image in postdata['post_images']:
                with open(image, 'rb') as imf:
                    img = imf.read()
                # print(len(img))
                if len(img) < 200000:
                    small_images.append(image)

            postdata['post_images'] = small_images[:6]

            for i, img in enumerate(postdata['post_images']):
                filename = str(i) + '.jpeg'
                if i == 0:
                    index_name = 'fileshow'
                else:
                    index_name = 'file' + str(i)
                datapost.append((index_name, (filename, open(img, 'rb'), 'image/jpeg')))

            # print("here\n", datapost)

            r = httprequestObj.http_post('http://classified.thiubon.com/member/p-classifieds-post.php', data={},
                                         files=datapost)
            # print(r.url)
            # print(r.status_code)

            data = r.text

            # print(data)
            if 'ระบบจัดการข้อมูลสมาชิก | ไทอุบลดอทคอม' in data:
                success = True
                detail = "Post created successfully"
                r = httprequestObj.http_get('http://classified.thiubon.com/member/list-classifieds.php')
                # print(r.url)
                # print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                url_raw = soup.find('table', 'table table-hover').find('tbody').find_all('tr')[1].find('td').find(
                    'a').get('href')
                post_url = 'http://classified.thiubon.com' + url_raw[2:]
                post_id = url_raw.split('/')[1].split('-')[-1]
                # print(post_url)
                # print(post_id)

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
            "account_type": "null",
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

            page = 0
            post_found = True

            """while True:
                page += 1
                params = {
                    'QueryString': 'value',
                    'Page': str(page)
                }
                r = httprequestObj.http_get('http://classified.thiubon.com/member/list-classifieds.php', params=params)
                # print(r.url)
                # print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                all_posts = soup.find('table', 'table table-hover').find('tbody').find_all('tr')[1:-1]
                if len(all_posts)==0:
                    break

                for post in all_posts:
                    post_id = str(post.find('td').find('a').get('href').split('/')[1].split('-')[-1])
                    if post_id == postdata['post_id']:
                        post_found = True
                        # print('Post found')
                        break"""

            if post_found:
                self.delete_post(postdata)
                resp = self.create_post(postdata)
                resp['log_id'] = postdata['log_id']
                if resp['detail'] == 'Post created successfully':
                    resp['detail'] = 'Post edited successfully'
                elif resp['detail'] == 'Couldnot create post':
                    resp['detail'] = 'Couldnot edit post'
                return resp
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
            "post_id": post_id,
            "log_id": postdata['log_id'],
            "account_type": "null",
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

            page = 0
            post_found = True

            """while True:
                page += 1
                params = {
                    'QueryString': 'value',
                    'Page': str(page)
                }
                r = httprequestObj.http_get('http://classified.thiubon.com/member/list-classifieds.php', params=params)
                print(r.url)
                # print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                all_posts = soup.find('table', 'table table-hover').find('tbody').find_all('tr')[1:-1]

                # print(all_posts[0])

                if len(all_posts) == 0:
                    break

                for post in all_posts:
                    post_id = post.find('td').find('a').get('href').split('/')[1].split('-')[-1]
                    if post_id == postdata['post_id']:
                        post_found = True
                        # print('Post found')
                        break

                if post_found:
                    break"""

            if post_found:
                r = httprequestObj.http_get('http://classified.thiubon.com/member/slide-classified-post.php',
                                            params={'id': post_id})
                # print(r.url)
                # print(r.status_code)

                data = r.text

                if 'เลื่อนประกาศเรียบร้อยแล้วครับ' in r.text:
                    success = True
                    detail = "Post boosted successfully"
                elif 'ขอโทษครับ ท่านสามารถเลื่อนประกาศได้เพียงวันละ 1 ครั้งเท่านั้นครับ' in r.text:
                    success = False
                    detail = "Announcement can be postponed only once per day"
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
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
            'log_id': postdata['log_id'],
            "account_type": "null",
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

            page = 0
            post_found = True

            """while True:
                page += 1
                params = {
                    'QueryString': 'value',
                    'Page': str(page)
                }
                r = httprequestObj.http_get('http://classified.thiubon.com/member/list-classifieds.php', params=params)
                # print(r.url)
                # print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                all_posts = soup.find('table', 'table table-hover').find('tbody').find_all('tr')[1:-1]

                if len(all_posts) == 0:
                    break

                for post in all_posts:
                    post_id = post.find('td').find('a').get('href').split('/')[1].split('-')[-1]
                    if post_id == postdata['post_id']:
                        post_found = True
                        # print('Post found')
                        break

                if post_found:
                    break"""

            if post_found:
                r = httprequestObj.http_get('http://classified.thiubon.com/member/del-classifieds.php',
                                            params={'id': post_id})
                # print(r.url)
                # print(r.status_code)

                data = r.text

                if 'ระบบจัดการข้อมูลสมาชิก' in data:
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
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
            'log_id': postdata['log_id'],
            "account_type": "null",
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
        post_created = ""
        post_modified = ""
        post_view = ""

        if success:

            page = 0
            post_found = False

            while True:
                page += 1
                params = {
                    'QueryString': 'value',
                    'Page': str(page)
                }
                r = httprequestObj.http_get('http://classified.thiubon.com/member/list-classifieds.php', params=params)
                # print(r.url)
                # print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                all_posts = soup.find('table', 'table table-hover').find('tbody').find_all('tr')[1:-1]

                if len(all_posts) == 0:
                    break

                for post in all_posts:
                    post_title = post.find('td').find('a').get('href').split('/')[2][:-5]
                    # print(post_title)
                    if post_title == postdata['post_title_th'].replace(' ', '-'):
                        post_found = True
                        # print('Post found')
                        success = True
                        detail = "Post Found"
                        post_id = post.find('td').find('a').get('href').split('/')[1].split('-')[-1]
                        post_url = 'http://classified.thiubon.com' + post.find('td').find('a').get('href')[2:]

                        r = httprequestObj.http_get(post_url)
                        # print(r.url)
                        # print(r.status_code)

                        #soup = BeautifulSoup(r.content, self.parser)
                        #info = soup.find('ul', 'list-group').findChildren('li', 'list-group-item')
                        # print(info)
                        #post_created = str(info[3].contents[-1]).strip()
                        #post_modified = str(info[4].contents[-1]).strip()
                        # print(str(soup.find('p', 'box-post-line').contents[0]).split(' '))
                        #post_view = str(soup.find('p', 'box-post-line').contents[0]).split('เข้าชม')[1].split('คร')[
                            #0].strip()
                        break

                if post_found:
                    break

            if not post_found:
                success = False
                detail = "No post with given title"

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
            "post_id": post_id,
            'log_id': postdata['log_id'],
            "post_url": post_url,
            "post_created": post_created,
            "post_modified": post_modified,
            "post_view": post_view,
            "account_type": "null",
            "detail": detail,
            "websitename": self.webname,
            "post_title_th": postdata['post_title_th'],
            "post_found": post_found
        }
