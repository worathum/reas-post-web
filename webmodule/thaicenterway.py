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

captcha = lib_captcha()


class thaicenterway():

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
        self.webname = 'thaicenterway'
        self.session = lib_httprequest()

    def print_debug(self, msg):
        if self.debug == 1:
            print(msg)
        return True

    def register_user(self, userdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()
        success = "true"
        detail = ""

        os.system('touch ./imgtmp/captcha.jpeg')
        r = self.session.http_get('http://www.thaicenterway.com/captcha.php?width=100&height=40&characters=5')
        with open("./imgtmp/captcha.jpeg", 'wb') as img_f:
            img_f.write(r.content)
        # print(captcha_url)
        captcha_text = captcha.imageCaptcha('./imgtmp/captcha.jpeg')
        print(captcha_text)

        datapost = {
            "username": userdata['user'],
            "password": userdata['pass'],
            "password1": userdata['pass'],
            "name": userdata['name_th'] + ' ' + userdata['surname_th'],
            "address": "พญาไท, กรุงเทพ",
            "sex": "ชาย",
            "distric": "พญาไท",
            "province": "กรุงเทพมหานคร",
            "code": "10400",
            "email": userdata['user'],
            "mobile": userdata['tel'],
            "tel": userdata['tel'],
            "fax": "",
            "birth": "13/04/2517",
            "salary": "มากกว่า 25,000 บาท",
            "work": "อื่นๆ",
            "education": "ปริญญาตรี",
            "mstatus": "โสด",
            "task": "add",
            "ok": "สมัครสมาชิก",
            "confirm2": captcha_text
        }

        r = self.session.http_post('http://www.thaicenterway.com/regis_process.php', params={'task': 'add'},
                                     data=datapost)
        # print(r.url)
        # print(r.status_code)
        data = r.text
        # print(data)

        if 'Loading...' in data:
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

        datapost = {
            'Cus_user': userdata['user'],
            'Cus_pass': userdata['pass'],
            'submit': 'เข้าสู่ระบบ',

        }
        r = self.session.http_post('http://www.thaicenterway.com/Login_check.php', data=datapost)
        # print(r.url)
        # print(r.status_code)
        data = r.text

        if 'สวัสดีคุณ ' + userdata['user'] + ' คุณได้เข้าสู่ระบบเรียบร้อยแล้ว' in data:
            detail = "Login successful"
            success = True
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
            "websitename": self.webname,
            "ds_id": userdata['ds_id'],
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
            getProdId = {'1': 159, '2': 156, '3': 156, '4': 157,
                         '5': 158, '6': 161, '7': 162, '8': 162, '9': 162, '10': 162, '25': 162}

            try:
                theprodid = getProdId[proid[str(postdata['property_type'])]]
                postdata['property_type'] = proid[str(postdata['property_type'])]
            except:
                theprodid = getProdId[str(postdata['property_type'])]

            prod_address = ""
            for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'],
                        postdata['addr_district'], postdata['addr_province']]:
                if add is not None:
                    prod_address += add + " "
            prod_address = prod_address[:-1]

            r = self.session.http_get('http://www.thaicenterway.com/myClassified.php')
            # print(r.url)
            # print(r.status_code)

            r = self.session.http_get(
                'http://www.thaicenterway.com/%E0%B8%A5%E0%B8%87%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B8%81%E0%B8%B2%E0%B8%A8%E0%B8%9F%E0%B8%A3%E0%B8%B5')
            # print(r.url)
            # print(r.status_code)

            r = self.session.http_get(
                'http://www.thaicenterway.com/%E0%B8%9A%E0%B9%89%E0%B8%B2%E0%B8%99-%E0%B8%97%E0%B8%B5%E0%B9%88%E0%B8%94%E0%B8%B4%E0%B8%99-%E0%B8%AD%E0%B8%AA%E0%B8%B1%E0%B8%87%E0%B8%AB%E0%B8%B2%E0%B8%A3%E0%B8%B4%E0%B8%A1%E0%B8%97%E0%B8%A3%E0%B8%B1%E0%B8%9E%E0%B8%A2%E0%B9%8C')
            # print(r.url)
            # print(r.status_code)

            r = self.session.http_get(
                'https://p4-hxzjxiqnyxtva-je26frt6rc5d6arg-286468-s1-v6exp3-v4.metric.gstatic.com/gen_204?ipv6exp=dz&sentinel=1&dz_img_dt=1141&4z_img_dt=808')
            # print(r.url)
            # print(r.status_code)

            r = self.session.http_get(
                'http://www.thaicenterway.com/%E0%B8%A5%E0%B8%87%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B8%81%E0%B8%B2%E0%B8%A8%E0%B8%9F%E0%B8%A3%E0%B8%B5/10/%E0%B8%9A%E0%B9%89%E0%B8%B2%E0%B8%99-%E0%B8%AD%E0%B8%AA%E0%B8%B1%E0%B8%87%E0%B8%AB%E0%B8%B2%E0%B8%A3%E0%B8%B4%E0%B8%A1%E0%B8%97%E0%B8%A3%E0%B8%B1%E0%B8%9E%E0%B8%A2%E0%B9%8C/')
            # print(r.url)
            # print(r.status_code)

            # with open('/home/codelover/Desktop/rough.html', 'w') as f:
            #     f.write(r.text)

            det_p = [
                ('pts_id', (None, '10')),
                # ('post_detail', (None, 'abcdef')),
                ('keyword', (None, postdata['post_title_th'])),
                ('keyword1', (None, '')),
                ('keyword2', (None, '')),
                ('keyword3', (None, '')),
                ('keyword4', (None, '')),
                ('keyword5', (None, '')),
                ('date_expire', (None, '15')),
                ('quality2', (None, 'มือสอง')),
                ('website', (None, 'http://')),
                ('post_name', (None, postdata['name'])),
                ('email', (None, postdata['email'])),
                ('price', (None, postdata['price_baht'])),
                ('tel', (None, postdata['mobile'])),
                ('mobile', (None, postdata['mobile'])),
                ('address', (None, prod_address)),
                ('picture', (None, 'picture'))
            ]

            datapost = det_p
            datapost.append(('topic', (None, 'xyz123')))
            datapost.append(('post_detail', (None, 'abcd')))
            datapost.append(('Submit2', (None, 'เคลียร์ข้อมูล')))

            if postdata['listing_type'] != 'เช่า':
                # sell
                det_p.append(('post_want', (None, 'ขาย')))
                datapost.append(('post_want', (None, 'ขาย')))
            else:
                # rent
                det_p.append(('post_want', (None, 'ให้เช่า')))
                datapost.append(('post_want', (None, 'ให้เช่า')))

            soup = BeautifulSoup(r.content, self.parser)
            all_provinces = soup.find('select', {'name': 'province'}).findChildren('option')[1:]

            province_id_map = {}
            post_found = False
            post_id = ''

            for province in all_provinces:
                province_id_map[province.string] = province.get('value')

            # print(province_id_map)

            for (key, value) in province_id_map.items():
                if key == postdata['addr_province'] or key == postdata['addr_province'].replace(" ", ""):
                    post_id = value
                    # print('Direct match')
                    post_found = True
                    break

            if not post_found:
                for (key, value) in province_id_map.items():
                    if key in postdata['addr_province'] or key.replace(" ", "") in postdata['addr_province'].replace(
                            " ", "") or postdata['addr_province'].replace(" ", "") in key.replace(" ", ""):
                        post_id = value
                        # print('Partial match')
                        # print(post_id)
                        post_found = True
                        break

            if not post_found:
                # print('No match')
                post_id = next(iter(province_id_map.values()))
                # print(post_id)

            det_p.append(('province', (None, post_id)))
            datapost.append(('province', (None, post_id)))

            small_images = []

            for image in postdata['post_images']:
                with open(image, 'rb') as imf:
                    img = imf.read()
                print(len(img))
                if len(img) < 100000:
                    small_images.append(image)

            postdata['post_images'] = small_images[:3]

            if len(postdata['post_images']) > 0:
                det_p.append(('picture', ('0.jpeg', open(postdata['post_images'][0], 'rb'), 'image/jpeg')))
                datapost.append(('picture', ('0.jpeg', open(postdata['post_images'][0], 'rb'), 'image/jpeg')))
                datapost.append(('alt', (None, 'ขายอสสงหาฯ')))
            else:
                det_p.append(('picture', (None, None)))
                datapost.append(('picture', (None, None)))
                datapost.append(('alt', (None, '')))

            if len(postdata['post_images']) > 1:
                det_p.append(('picture1', ('1.jpeg', open(postdata['post_images'][1], 'rb'), 'image/jpeg')))
                datapost.append(('picture1', ('1.jpeg', open(postdata['post_images'][1], 'rb'), 'image/jpeg')))
                datapost.append(('alt1', (None, 'ขายอสสงหาฯ')))
            else:
                det_p.append(('picture1', (None, None)))
                datapost.append(('picture1', (None, None)))
                datapost.append(('alt1', (None, '')))

            if len(postdata['post_images']) > 2:
                det_p.append(('picture2', ('2.jpeg', open(postdata['post_images'][2], 'rb'), 'image/jpeg')))
                datapost.append(('picture2', ('2.jpeg', open(postdata['post_images'][2], 'rb'), 'image/jpeg')))
                datapost.append(('alt2', (None, 'ขายอสสงหาฯ')))
            else:
                det_p.append(('picture2', (None, None)))
                datapost.append(('picture2', (None, None)))
                datapost.append(('alt2', (None, '')))

            r = self.session.http_post('http://www.thaicenterway.com/post_process.php', params={'task': 'add'},
                                         data={}, files=datapost)
            # print(r.url)
            # print(r.status_code)

            if 'เพิ่มข้อมูลประกาศเรียบร้อยแล้ว กรุณารอสักครู่...' in r.text:
                success = True
                detail = "Post created successfully"
                soup = BeautifulSoup(r.content, self.parser)
                post_id = str(soup.find('meta', {'http-equiv': 'refresh'}).get('content')).split('=')[-1]
                # post_id = r.url.split('=')[-1]
                post_url = 'http://www.thaicenterway.com/' + postdata['post_title_th'].replace(' ', '-') + '/' + post_id + '.html'

                datapost = det_p

                if len(postdata['post_images']) > 0:
                    # det_p.append(('picture', ('0.jpeg', open(postdata['post_images'][0], 'rb'), 'image/jpeg')))
                    datapost.append(('picture', ('0.jpeg', open(postdata['post_images'][0], 'rb'), 'image/jpeg')))
                    datapost.append(('alt', (None, 'ขายอสสงหาฯ')))
                else:
                    # det_p.append(('picture', (None, None)))
                    datapost.append(('picture', (None, None)))
                    datapost.append(('alt', (None, '')))

                if len(postdata['post_images']) > 1:
                    # det_p.append(('picture1', ('1.jpeg', open(postdata['post_images'][1], 'rb'), 'image/jpeg')))
                    datapost.append(('picture1', ('1.jpeg', open(postdata['post_images'][1], 'rb'), 'image/jpeg')))
                    datapost.append(('alt1', (None, 'ขายอสสงหาฯ')))
                else:
                    # det_p.append(('picture1', (None, None)))
                    datapost.append(('picture1', (None, None)))
                    datapost.append(('alt1', (None, '')))

                if len(postdata['post_images']) > 2:
                    # det_p.append(('picture2', ('2.jpeg', open(postdata['post_images'][2], 'rb'), 'image/jpeg')))
                    datapost.append(('picture2', ('2.jpeg', open(postdata['post_images'][2], 'rb'), 'image/jpeg')))
                    datapost.append(('alt2', (None, 'ขายอสสงหาฯ')))
                else:
                    # det_p.append(('picture2', (None, None)))
                    datapost.append(('picture2', (None, None)))
                    datapost.append(('alt2', (None, '')))

                datapost.append(('topic', (None, postdata['post_title_th'])))
                datapost.append(('post_detail', (None, postdata['post_description_th'])))
                datapost.append(('item', (None, post_id)))
                datapost.append(('delpic', (None, '')))
                datapost.append(('delpic2', (None, '')))
                datapost.append(('delpic3', (None, '')))
                datapost.append(('Submit', (None, 'แก้ไขประกาศ')))

                r = self.session.http_get('http://www.thaicenterway.com/ClassifiedEdit.php', params={'item': post_id})
                # print(r.url)
                # print(r.status_code)

                r = self.session.http_post('http://www.thaicenterway.com/ClassifiedEditDo.php', data={}, files=datapost)
                # print(r.url)
                # print(r.status_code)

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
            "detail": detail,
            "websitename": self.webname,
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
            "post_url": post_url
        }

    def edit_post(self, postdata):
        '''
        Since images cannot be deleted, deleting and re-creating post
        '''

        result=self.delete_post(postdata)
        if result["success"]:
            resp = self.create_post(postdata)
            resp['log_id'] = postdata['log_id']
            resp['detail'] = 'Post edited successsfully'
        else:
            return result
        return resp

    def boost_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""

        if success:

            r = self.session.http_get('http://www.thaicenterway.com/myClassified.php')
            soup = BeautifulSoup(r.content, self.parser)
            all_posts = soup.find_all('td', {'valign': 'top', 'class': 'AR12BlackB'})

            post_found = False

            for post in all_posts:
                post_url = post.find('a').get('href')
                post_id = post_url.split('/')[-1][:-5]
                # print(post_id)
                if post_id == postdata['post_id']:
                    post_found = True
                    break

            if post_found:
                r = self.session.http_get('http://www.thaicenterway.com/movefirst.php', params={'post_id': post_id})
                # print(r.url)
                # print(r.status_code)

                if 'เลื่อนประกาศหมายเลข '+post_id+' เรียบร้อยแล้ว' in r.text:
                    success = True
                    detail = "Post boosted successfully"
                elif 'คุณสามารถเลื่อนประกาศได้วันละ 3 ประกาศ เท่านั้น!!!' in r.text:
                    success = False
                    detail = "Can only postpone 3 announcements per day"
                else:
                    success = False
                    detail = "Couldnot boost post"
            else:
                success = False
                detail = "Couldnot boost post"
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
            "websitename": self.webname,
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
            "log_id": postdata['log_id']
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

            r = self.session.http_get('http://www.thaicenterway.com/myClassified.php')
            soup = BeautifulSoup(r.content, self.parser)
            all_posts = soup.find_all('td', {'valign': 'top', 'class': 'AR12BlackB'})

            post_found = False

            for post in all_posts:
                post_url = post.find('a').get('href')
                post_id = post_url.split('/')[-1][:-5]
                # print(post_id)
                if post_id == postdata['post_id']:
                    post_found = True
                    break

            if post_found:
                r = self.session.http_get('http://www.thaicenterway.com/ClassifiedDel.php', params={'post_id': post_id})
                # print(r.url)
                # print(r.status_code)

                if 'ลบประกาศเรียบร้อยแล้ว' in r.text:
                    success = True
                    detail = "Post deleted successfully"
                else:
                    success = False
                    detail = "Couldnot delete post"
            else:
                success = False
                detail = 'No post with given post_id'
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
            "websitename": self.webname,
            "ds_id": postdata['ds_id'],
            "post_id": postdata['post_id'],
            "log_id": postdata['log_id']
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
        post_view = ""

        if success:

            r = self.session.http_get('http://www.thaicenterway.com/myClassified.php')
            soup = BeautifulSoup(r.content, self.parser)
            all_posts = soup.find_all('td', {'valign': 'top', 'class': 'AR12BlackB'})

            post_found = False

            for post in all_posts:
                post_url = post.find('a').get('href')
                post_title = post_url.split('/')[-2].replace('-', ' ').strip()
                post_id = post_url.split('/')[-1][:-5]
                postdata['post_title_th'] = str(postdata['post_title_th']).replace('-',' ')
                print(post_title)
                print(postdata['post_title_th'],'\n\n\n')
                if postdata['post_title_th'] in post_title or post_title in postdata['post_title_th']:
                    post_found = True
                    break

            if post_found:
                success = True
                detail = "Post Found"
                r = self.session.http_get(post_url)
                # print(r.url)
                # print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                try:
                    table = soup.find('table', {'style': 'border: solid 1px #CCCCCC'})

                    table = table.findChildren('tr', recursive=False)
                    # print(table)

                    post_created = table[3].find('td').find('span', 'style23').string
                    post_view = table[4].find('td').find('span', 'style23').string.split(' ')[-1]
                except:
                    pass

            else:
                post_id = ""
                post_url = ""
                success = False
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
            "websitename": self.webname,
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
            "post_url": post_url,
            "log_id": postdata['log_id'],
            "post_created": str(post_created),
            "post_modified": "",
            "post_view": str(post_view)
        }



