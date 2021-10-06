# -*- coding: utf-8 -*-
import base64

from .lib_httprequest import *
from .lib_captcha import *
from bs4 import BeautifulSoup
import os.path
from shutil import copyfile
# from urlparse import urlparse
import re
import json
import datetime
import sys
import random
from urllib.parse import unquote
import os
import time
from requests_toolbelt.multipart.encoder import MultipartEncoder


Captcha = lib_captcha()


class onlineannouncement():

    def __init__(self):

        self.debugdata = None
        try:
            import configs
        except ImportError:
            configs = {}
            
        self.httprequestObj = lib_httprequest()
        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.url = 'http://www.xn--12c2caf4bot4ba0ax4tzd.com'
        self.debug = 0
        self.webname = 'onlineannouncement'

        self.parser = 'html.parser'

    def print_debug(self, msg):
        if self.debug == 1:
            print(msg)
        return True

    def register_user(self, userdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        reg_data = {
            'name': userdata['name_th'] + ' ' + userdata['surname_th'],
            'email': userdata['user'],
            'lineid': userdata['line'],
            'phone': userdata['tel'],
            'pass': userdata['pass'],
            'conpass': userdata['pass'],
            'submit': ''
        }

        response = self.httprequestObj.http_post('https://www.xn--12c2caf4bot4ba0ax4tzd.com/register.php', data=reg_data)

        time_end = datetime.datetime.utcnow()

        # print(response.url)
        # print(response.status_code)

        success = False
        detail = "Couldnot register"

        if 'สมัครสมาชิกเรียบร้อยแล้ว' in response.text:
            success = True
            detail = "Successfully registered"

        return {
            "websitename": self.webname,
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "usage_time": str(time_end - time_start),
            "ds_id": userdata['ds_id'],
            "detail": detail,
        }

    def test_login(self, userdata):
        response = self.httprequestObj.http_get('https://www.ประกาศออนไลน์.com/logout')
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        login_data = {
            'log_e': userdata['user'],
            'log_p': userdata['pass'],
            'submit': 'เข้าสู่ระบบ'
        }

        response = self.httprequestObj.http_post('https://www.xn--12c2caf4bot4ba0ax4tzd.com/login', data=login_data)

        time_end = datetime.datetime.utcnow()

        # print(response.url)
        # print(response.status_code)

        success = False
        detail = "Couldnot login"

        if 'อีเมลล์หรือรหัสผ่านไม่ถูกต้อง กรุณาลองใหม่อีกครั้งค่ะ' not in response.text:
            success = True
            detail = "Successful Login"

        return {
            "websitename": self.webname,
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "usage_time": str(time_end - time_start),
            "ds_id": userdata['ds_id'],
            "detail": detail,
        }

    def get_province(self, content, province):

        soup = BeautifulSoup(content, self.parser)
        provinces = soup.find('select', {"id": 'Province'})
        # print(provinces)
        options = provinces.findChildren('option')[1:]

        for option in options:
            cur_id = option.get('value')
            cur_province = option.string
            # print(option)

            if province == cur_province or province.replace(" ", "") == cur_province:
                # print('direct match province')
                # print(cur_id)
                return cur_id

        for option in options:
            cur_id = option.get('value')
            cur_province = option.string

            # print(cur_id, cur_province)

            if province in cur_province or province.replace(" ", "") in cur_province:
                # print('partial match province')
                # print(cur_id)
                return cur_id

        # print('no match province')
        # print(options[0].get('value'))
        return options[0].get('value')

    def matching_district(self, content, district):
        # print('list of districts')
        # print(content.values())
        for x in content:
            print(x["am_name"])
            if x["am_name"] == district or x["am_name"].replace(" ", "") == district:
                # print("Direct match district")
                return x["am_id"]

        for x in content:
            if x["am_name"] in district or x["am_name"].replace(" ", "") in district.replace(" ",
                                                                                             "") or district.replace(
                    " ", "") in x["am_name"].replace(" ", ""):
                # print("Partial match district")
                return x["am_id"]

        # print("No match district")
        return content[0]["am_id"]

    def create_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]

        post_url = ""
        post_id = ""

        if success:
            response = self.httprequestObj.http_get('https://www.xn--12c2caf4bot4ba0ax4tzd.com/posting')
            province_id = self.get_province(response.content, postdata['addr_province'])

            # print('Province id= ' + str(province_id))
            # print('0')

            params = {
                'ID': str(province_id),
                'TYPE': 'District'
            }

            response = self.httprequestObj.http_get('https://www.xn--12c2caf4bot4ba0ax4tzd.com/getaddress.php',
                                               params=params)

            district_id = self.matching_district(response.json(), postdata['addr_district'])

            # print('District_id= ' + str(district_id))

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

            getProdId = {'1': '935',
                         '2': '799',
                         '3': '799',
                         '4': '934',
                         '5': '938',
                         '6': '939',
                         '7': '936',
                         '8': '937',
                         '9': '806',
                         '10': '1043',
                         '25': '1043'}

            try:
                theprodid = getProdId[proid[str(postdata['property_type'])]]
                postdata['property_type'] = proid[str(postdata['property_type'])]
            except:
                theprodid = getProdId[str(postdata['property_type'])]

            postdata['post_description_th'] = postdata['post_description_th'].replace("'","")

            datapost = {
                'action': 'addpost',
                'c_category': 'undefined',
                'c_group': '109',
                'c_cate': theprodid,
                'c_register': postdata['post_title_th'],
                'c_gear': 'มือสอง',
                'c_power': 'undefined',
                'c_year': 'undefined',
                'c_mile': 'undefined',
                'c_price': postdata['price_baht'],
                'c_detail': postdata['post_description_th'],
                'c_province': str(province_id),
                'c_amphur': str(district_id)
            }

            if postdata['listing_type'] != 'เช่า':
                # sell
                datapost['c_color'] = 'ขาย'
            else:
                # rent
                datapost['c_color'] = 'ให้เช่า'

            response = self.httprequestObj.http_post('https://www.xn--12c2caf4bot4ba0ax4tzd.com/process_function.php',
                                                data=datapost)

            file = []
            # print(postdata['post_images'])

            for i, img in enumerate(postdata['post_images']):
                filename = str(i) + '.jpg'
                file.append(('photoimg[]', (filename, open(img, "rb"), "image/jpeg")))

            img_page = self.httprequestObj.http_get('https://www.xn--12c2caf4bot4ba0ax4tzd.com/imgcar')

            try:
                soup = BeautifulSoup(img_page.content, self.parser)
                post_url = soup.find('a', 'btn btn-primary btn-block margint15').get('href')
                post_id = post_url.split('-')[-1]

                response = self.httprequestObj.http_post('https://www.xn--12c2caf4bot4ba0ax4tzd.com/ajax_img.php', data={},
                                                    files=file)

                success = True
                detail = "Post created successfully"
            except:
                success = False
                detail = "Couldnot create post"

        else:
            success = False
            detail = "Couldnot login"

        time_end = datetime.datetime.utcnow()

        return {
            "websitename": self.webname,
            "success": success,
            "ds_id": postdata["ds_id"],
            "post_id": post_id,
            "post_url": post_url,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "usage_time": str(time_end - time_start),
            "detail": detail,
        }

    def edit_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]

        post_id = ""

        if success:
            i = 0
            found = True
            """while True:
                if i == 0:
                    url = 'https://www.xn--12c2caf4bot4ba0ax4tzd.com/post'
                else:
                    url = 'https://www.xn--12c2caf4bot4ba0ax4tzd.com/post?&page=' + str(i)
                response = self.httprequestObj.http_get(url)
                # print(i)
                # print(response.url)
                i += 1

                soup = BeautifulSoup(response.content, self.parser)
                all_posts = soup.find_all('a', 'blue')
                if len(all_posts) == 0:
                    break

                for post in all_posts:
                    if post.get('href').split('-')[-1] == postdata['post_id']:
                        found = True
                        break
                if found:
                    break"""

            if found:
                response = self.httprequestObj.http_get('https://www.xn--12c2caf4bot4ba0ax4tzd.com/posting')
                province_id = self.get_province(response.content, postdata['addr_province'])

                # print('Province id= ' + str(province_id))

                params = {
                    'ID': str(province_id),
                    'TYPE': 'District'
                }

                response = self.httprequestObj.http_get('https://www.xn--12c2caf4bot4ba0ax4tzd.com/getaddress.php',
                                                   params=params)

                district_id = self.matching_district(response.json(), postdata['addr_district'])

                # print('District_id= ' + str(district_id))

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

                getProdId = {'1': '935',
                             '2': '799',
                             '3': '799',
                             '4': '934',
                             '5': '938',
                             '6': '939',
                             '7': '936',
                             '8': '937',
                             '9': '806',
                             '10': '1043',
                             '25': '1043'}

                try:
                    theprodid = getProdId[proid[str(postdata['property_type'])]]
                    postdata['property_type'] = proid[str(postdata['property_type'])]
                except:
                    theprodid = getProdId[str(postdata['property_type'])]

                postdata['post_description_th'] = postdata['post_description_th'].replace("'","")

                datapost = {
                    'Submit': 'Submit',
                    'c_brand': '109',
                    'c_model': theprodid,
                    'c_register': postdata['post_title_th'],
                    'c_gear': 'มือสอง',
                    'c_id': str(postdata['post_id']),
                    'c_price': postdata['price_baht'],
                    'c_detail': postdata['post_description_th'],
                    'c_province': str(province_id),
                    'c_amphur': str(district_id)
                }

                if postdata['listing_type'] != 'เช่า':
                    # sell
                    datapost['c_color'] = 'ขาย'
                else:
                    # rent
                    datapost['c_color'] = 'ให้เช่า'

                params = {'id': postdata['post_id']}

                response = self.httprequestObj.http_post('https://www.xn--12c2caf4bot4ba0ax4tzd.com/edit_post',
                                                    params=params,
                                                    data=datapost)

                file = []

                for i, img in enumerate(postdata['post_images']):
                    filename = str(i) + '.jpg'
                    file.append(('photoimg[]', (filename, open(img, "rb"), "image/jpeg")))

                img_page = self.httprequestObj.http_get('https://www.xn--12c2caf4bot4ba0ax4tzd.com/edit_img', params=params)

                try:
                    soup = BeautifulSoup(img_page.content, self.parser)
                    preview_parent = soup.find('div', {'id': 'preview'})
                    # print(preview_parent)
                    previews = preview_parent.findChildren('div')

                    for preview in previews:
                        pid = preview.get('id')
                        if pid is not None and len(pid) > 5 and preview.get('id')[:5] == 'd_img':
                            # print(pid[5:])
                            img_id = pid[5:]
                            response = self.httprequestObj.http_post(
                                'https://www.xn--12c2caf4bot4ba0ax4tzd.com/process_function.php',
                                data={'action': 'dimg', 'i_id': img_id})

                    file = []

                    for i, img in enumerate(postdata['post_images']):
                        filename = str(i) + '.jpg'
                        file.append(('photoimg[]', (filename, open(img, "rb"), "image/jpeg")))

                    img_page = self.httprequestObj.http_get('https://www.xn--12c2caf4bot4ba0ax4tzd.com/edit_img',
                                                       params=params)
                    # print(img_page.url)

                    response = self.httprequestObj.http_post('https://www.xn--12c2caf4bot4ba0ax4tzd.com/ajax_img.php',
                                                        data={}, files=file)
                    # print(response.url)

                    success = True
                    detail = "Post edited successfully"

                except:
                    success = False
                    detail = "Couldnot edit post"

            else:
                success = False
                detail = "No post with given post_id"

        else:
            success = False
            detail = "Couldnot login"

        time_end = datetime.datetime.utcnow()

        return {
            "websitename": self.webname,
            "success": success,
            "ds_id": postdata["ds_id"],
            "post_id": post_id,
            "log_id": postdata["log_id"],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "usage_time": str(time_end - time_start),
            "detail": detail,
        }

    def delete_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        # print(postdata)
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        # print(type(success))
        # print(detail)

        if success:

            i = 0
            found = True
            """while True:
                if i == 0:
                    url = 'https://www.xn--12c2caf4bot4ba0ax4tzd.com/post'
                else:
                    url = 'https://www.xn--12c2caf4bot4ba0ax4tzd.com/post?&page=' + str(i)
                response = self.httprequestObj.http_get(url)
                # print(i)
                # print(response.url)
                i += 1

                soup = BeautifulSoup(response.content, self.parser)
                all_posts = soup.find_all('a', 'blue')
                if len(all_posts) == 0:
                    break

                for post in all_posts:
                    if post.get('href').split('-')[-1] == postdata['post_id']:
                        found = True
                        break
                if found:
                    break"""

            if found:

                del_data = {
                    'action': 'pstatus',
                    'p_id': postdata['post_id'],
                    's_id': '1'
                }

                response = self.httprequestObj.http_post('https://www.xn--12c2caf4bot4ba0ax4tzd.com/process_function.php',
                                                    data=del_data)
                # print(response.url)
                # print(response.status_code)

                success = True
                detail = "Post deleted"

            else:
                success = False
                detail = "Post not found"
        else:
            success = False
            detail = "Couldnot login"

        time_end = datetime.datetime.utcnow()

        return {
            "websitename": self.webname,
            "success": success,
            "ds_id": postdata["ds_id"],
            "log_id": postdata["log_id"],
            "post_id": postdata["post_id"],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "usage_time": str(time_end - time_start),
            "detail": detail,
        }

    def boost_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        # print(postdata)
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        # print(type(success))
        # print(detail)

        if success:

            i = 0
            found = True
            """while True:
                if i == 0:
                    url = 'https://www.xn--12c2caf4bot4ba0ax4tzd.com/post'
                else:
                    url = 'https://www.xn--12c2caf4bot4ba0ax4tzd.com/post?&page=' + str(i)
                response = self.httprequestObj.http_get(url)
                # print(i)
                # print(response.url)
                i += 1

                soup = BeautifulSoup(response.content, self.parser)
                all_posts = soup.find_all('a', 'blue')
                if len(all_posts) == 0:
                    break

                for post in all_posts:
                    if post.get('href').split('-')[-1] == postdata['post_id']:
                        found = True
                        break
                if found:
                    break"""

            if found:
                params = {
                    'id': postdata['post_id']
                }

                data = {
                    'Submit': 'Submit'
                }

                response = self.httprequestObj.http_post('https://www.xn--12c2caf4bot4ba0ax4tzd.com/edit_post', params=params,
                                                    data=data)

                # print(response.url)
                # print(response.status_code)
                success = True
                detail = "Post boosted successfully"
            else:
                success = False
                detail = "No post with given post_id"

        else:
            success = False
            detail = "Couldnot login"

        time_end = datetime.datetime.utcnow()

        return {
            "websitename": self.webname,
            "success": success,
            "ds_id": postdata["ds_id"],
            "log_id": postdata["log_id"],
            "post_id": postdata["post_id"],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "usage_time": str(time_end - time_start),
            "detail": detail,
        }

    def search_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        # print(postdata)
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        # print(type(success))
        # print(detail)

        post_url = ""
        post_id = ""
        post_create = ""
        post_view = ""
        post_modified = ""

        if success:

            i = 0
            found = False
            while True:
                if i == 0:
                    url = 'https://www.xn--12c2caf4bot4ba0ax4tzd.com/post'
                else:
                    url = 'https://www.xn--12c2caf4bot4ba0ax4tzd.com/post?&page=' + str(i)
                response = self.httprequestObj.http_get(url)
                # print(i)
                # print(response.url)
                i += 1

                soup = BeautifulSoup(response.content, self.parser)

                all_posts = soup.find_all('div', 'media-body media-body-post')
                # print(all_posts)
                if len(all_posts) == 0:
                    break

                for post in all_posts:
                    post_url = post.findChildren('a', recursive=True)[0].get('href')
                    pos_id = post_url.split('-')[-1]
                    # post_url= soup1.find('a','blue').get('href')
                    # print("Post url")
                    # print(post_url)

                    # print("Post title")
                    post_children = post.findChildren(recursive=True)

                    # print(post_children[1])
                    post_url = post_children[1].get('href')
                    post_id = post_url.split('-')[-1]
                    post_title = post_children[1].string

                    # print(post_url)
                    # print(post_id)
                    # print(post_title)

                    time = str(post_children[6]).split('</span>')[1].strip().split(' ')
                    post_create = time[0] + " " + time[1]
                    # print(post_create)

                    if post_title == postdata['post_title_th']:
                        found = True
                        success = True
                        detail = "Post Found"
                        break

                if found:
                    break

            if not found:
                post_url = ""
                post_id = ""
                post_create = ""
                post_modified = ""
                post_view = ""
                success = False
                detail = "Post not found"

        else:
            success = False
            detail = "Couldnot login"

        time_end = datetime.datetime.utcnow()

        return {
            "websitename": self.webname,
            "success": success,
            "ds_id": postdata["ds_id"],
            "log_id": postdata["log_id"],
            "post_id": post_id,
            "post_url": post_url,
            "post_create": post_create,
            "post_modified": post_modified,
            "post_view": post_view,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "usage_time": str(time_end - time_start),
            "detail": detail,
            "post_title_th": postdata['post_title_th'],
            "post_found": found
        }
