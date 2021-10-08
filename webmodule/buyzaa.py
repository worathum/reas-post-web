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



class buyzaa():

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
        self.webname = 'buyzaa'
        self.session = lib_httprequest()

    def print_debug(self, msg):
        if self.debug == 1:
            print(msg)
        return True

    def register_user(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']

        r = self.session.http_get('http://www.buyzaa.com/register.php')
        print(r.url)
        print(r.status_code)

        soup = BeautifulSoup(r.content, self.parser)
        sum = soup.find('input', {'name': 'hiddenanswer'}).get('value')

        datapost = {
            "save": 'kkqm48ec2hkabfa1q22qbfnmg3',
            "email": user,
            "password": passwd,
            "repassword": passwd,
            "name": postdata['name_th'] + ' ' + postdata['surname_th'],
            "phone": postdata['tel'],
            "address": 'พญาไท กรุงเทพ',
            "province": '2',
            "amphur": '22',
            "zipcode": '10400',
            "title": '',
            "description": '',
            "keyword": '',
            "website": '',
            "answer": sum,
            "hiddenanswer": sum,
            "accept": '1',
        }
        r = self.session.http_post('http://www.buyzaa.com/lib/checkuser.php', data=datapost)
        # print(r.url)
        # print(r.status_code)
        data = r.text

        r = self.session.http_post('http://www.buyzaa.com/register.php', data=datapost)
        # print(r.url)
        # print(r.status_code)
        data = r.text

        status = r.url.split('?')[1].split('&')[0].split('=')[1]

        # print(data)
        if status == '1':
            success = True
            detail = "Registered successfully"
        elif data.find('ชื่ออีเมล์นี้ถูกใช้ไปแล้วค่ะ') != -1:
            success = False
            detail = "email already registered"
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
        r = self.session.http_get('http://www.buyzaa.com/logout.php')
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']

        success = ""
        detail = ""

        r = self.session.http_get('http://www.buyzaa.com/member.php')
        # print(r.url)
        # print(r.status_code)

        datapost = {
            "save": 'kkqm48ec2hkabfa1q22qbfnmg3',
            "email": user,
            "password": passwd,
        }

        r = self.session.http_post('http://www.buyzaa.com/member.php', data=datapost)
        # print(r.url)
        # print(r.status_code)
        data = r.text

        # print(data)
        if 'manage-post' in r.url:
            success = True
            detail = "Login successfully"
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
            getProdId = {'1': '1149', '2': '1147', '3': '1154', '4': '1154',
                         '5': '1153', '6': '1148', '7': '1150', '8': '1156', '9': '1151', '10': '1155', '25': '1155'}

            try:
                theprodid = getProdId[proid[str(postdata['property_type'])]]
                postdata['property_type'] = str(proid[str(postdata['property_type'])])
            except:
                theprodid = getProdId[str(postdata['property_type'])]

            r = self.session.http_get('http://www.buyzaa.com/post-add.php')
            # print(r.url)
            # print(r.status_code)

            soup = BeautifulSoup(r.content, self.parser)
            provinces = soup.find('select', {'name': 'city'}).findChildren('option')[1:]

            province_id = provinces[0].get('value')
            for province in provinces:
                area = province.string
                if area.replace(' ', '') in postdata['addr_province'].replace(' ', '') or postdata[
                    'addr_province'].replace(' ', '') in area.replace(' ', ''):
                    province_id = province.get('value')
                    break

            # print("Province_id = " + province_id)

            r = self.session.http_get('http://www.buyzaa.com/lib/district.php', params={'province': province_id})
            # print(r.url)
            # print(r.status_code)

            soup = BeautifulSoup(r.content, self.parser)
            districts = soup.find('select', {'name': 'district'}).findChildren('option')

            district_id = districts[0].get('value')
            for district in districts:
                area = district.string
                if area.replace(' ', '') in postdata['addr_province'].replace(' ', '') or postdata[
                    'addr_province'].replace(' ', '') in area.replace(' ', ''):
                    district_id = district.get('value')
                    break

            # print("District_id = " + district_id)

            prod_address = ""
            for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'],
                        postdata['addr_district'], postdata['addr_province']]:
                if add is not None:
                    prod_address += add + " "
            prod_address = prod_address[:-1]

            datapost = {
                'save': 'kkqm48ec2hkabfa1q22qbfnmg3',
                'type': 'guest',
                'status': '2hand',
                'duration': '-1',
                'category': '1009',
                'subcategory': theprodid,
                'city': province_id,
                'district': district_id,
                'name': postdata['post_title_th'],
                'price': str(postdata['price_baht']),
                'detail': postdata['post_description_th'],
                'checkdetail': postdata['post_description_th'],
                'maplat': str(postdata['geo_latitude']),
                'maplon': str(postdata['geo_longitude']),
                'mapzoom': '',
                'contact': postdata['name'],
                'email': postdata['email'],
                'hiddenemail': postdata['user'],
                'phone': postdata['mobile'],
                'address': prod_address,
                'amphur': 'เขตคลองเตย',
                'province': 'กรุงเทพมหานคร',
                'zipcode': '10400',
                'website': ''
            }

            if postdata['listing_type'] != 'เช่า':
                # sell
                datapost['want'] = 'sale'
            else:
                # rent
                datapost['want'] = 'forrent'

            r = self.session.http_post('http://www.buyzaa.com/lib/checkpost.php', data=datapost)
            # print(r.url)
            # print(r.status_code)

            datapost = [
                ('save', (None, 'kkqm48ec2hkabfa1q22qbfnmg3')),
                ('type', (None, 'guest')),
                ('status', (None, '2hand')),
                ('duration', (None, '-1')),
                ('category', (None, '1009')),
                ('subcategory', (None, theprodid)),
                ('city', (None, province_id)),
                ('district', (None, district_id)),
                ('name', (None, postdata['post_title_th'])),
                ('price', (None, str(postdata['price_baht']))),
                ('detail', (None, postdata['post_description_th'])),
                ('checkdetail', (None, postdata['post_description_th'])),
                ('maplat', (None, str(postdata['geo_latitude']))),
                ('maplon', (None, str(postdata['geo_longitude']))),
                ('mapzoom', (None, '')),
                ('contact', (None, postdata['name'])),
                ('email', (None, postdata['email'])),
                ('hiddenemail', (None, postdata['user'])),
                ('phone', (None, postdata['mobile'])),
                ('address', (None, prod_address)),
                ('amphur', (None, 'เขตคลองเตย')),
                ('province', (None, 'กรุงเทพมหานคร')),
                ('zipcode', (None, '10400')),
                ('website', (None, ''))
            ]

            if postdata['listing_type'] != 'เช่า':
                # sell
                datapost.append(('want', (None, 'sale')))
            else:
                # rent
                datapost.append(('want', (None, 'forrent')))

            for i, img in enumerate(postdata['post_images'][:6]):
                filename = str(i + 1) + '.jpeg'
                indexname = 'photo' + str(i + 1)
                datapost.append((indexname, (filename, open(img, 'rb'), 'image/jpeg')))

            r = self.session.http_post('http://www.buyzaa.com/post-add.php', data={}, files=datapost)
            # print(r.url)
            # print(r.status_code)

            info = r.url.split('?')[-1].split('&')
            status = info[0].split('=')[-1]

            if status == '1':
                success = True
                detail = "Post created successfully"
                post_id = info[1].split('=')[-1]
                post_title = info[2].split('=')[-1].replace(' ', '-')
                post_url = 'http://www.buyzaa.com/view' + post_id + '/' + post_title
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
            tot_pages = 100

            """while True:
                page += 1
                if page > tot_pages:
                    break
                r = self.session.http_get('http://www.buyzaa.com/manage-post.php', params={'page': str(page)})
                # print(r.url)
                # print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                tot_pages = int(len(soup.find('div', 'pagination').find('ul').find_all('li'))) - 2
                all_posts = soup.find('div', 'postlist').findChildren('ul')
                # print(tot_pages)

                # if len(all_posts) == 0:
                #     break

                for post in all_posts:
                    post_id = post.find('li', 'title').find('a').get('href').split('/')[-2][4:]
                    # print(post_id)

                    if post_id == postdata['post_id']:
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
                getProdId = {'1': '1149', '2': '1147', '3': '1154', '4': '1154',
                             '5': '1153', '6': '1148', '7': '1150', '8': '1156', '9': '1151', '10': '1155',
                             '25': '1155'}

                try:
                    theprodid = getProdId[proid[str(postdata['property_type'])]]
                    postdata['property_type'] = str(proid[str(postdata['property_type'])])
                except:
                    theprodid = getProdId[str(postdata['property_type'])]

                r = self.session.http_get('http://www.buyzaa.com/post-edit.php', params={'id': postdata['post_id']})
                # print(r.url)
                # print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                provinces = soup.find('select', {'name': 'city'}).findChildren('option')[1:]

                province_id = provinces[0].get('value')
                for province in provinces:
                    area = province.string
                    if area.replace(' ', '') in postdata['addr_province'].replace(' ', '') or postdata[
                        'addr_province'].replace(' ', '') in area.replace(' ', ''):
                        province_id = province.get('value')
                        break

                # print("Province_id = " + province_id)

                r = self.session.http_get('http://www.buyzaa.com/lib/district.php', params={'province': province_id})
                # print(r.url)
                # print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                districts = soup.find('select', {'name': 'district'}).findChildren('option')

                district_id = districts[0].get('value')
                for district in districts:
                    area = district.string
                    if area.replace(' ', '') in postdata['addr_province'].replace(' ', '') or postdata[
                        'addr_province'].replace(' ', '') in area.replace(' ', ''):
                        district_id = district.get('value')
                        break

                # print("District_id = " + district_id)

                prod_address = ""
                for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'],
                            postdata['addr_district'], postdata['addr_province']]:
                    if add is not None:
                        prod_address += add + " "
                prod_address = prod_address[:-1]

                datapost = {
                    'save': 'kkqm48ec2hkabfa1q22qbfnmg3',
                    'type': 'guest',
                    'status': '2hand',
                    'duration': '',
                    'category': '1009',
                    'subcategory': theprodid,
                    'city': province_id,
                    'district': district_id,
                    'name': postdata['post_title_th'],
                    'hiddenname': postdata['post_title_th'],
                    'price': str(postdata['price_baht']),
                    'detail': postdata['post_description_th'],
                    'checkdetail': postdata['post_description_th'],
                    'maplat': str(postdata['geo_latitude']),
                    'maplon': str(postdata['geo_longitude']),
                    'mapzoom': '',
                    'contact': postdata['name'],
                    'email': postdata['email'],
                    'hiddenemail': postdata['user'],
                    'phone': postdata['mobile'],
                    'address': prod_address,
                    'amphur': 'เขตคลองเตย',
                    'province': 'กรุงเทพมหานคร',
                    'zipcode': '10400',
                    'website': ''
                }

                if postdata['listing_type'] != 'เช่า':
                    # sell
                    datapost['want'] = 'sale'
                else:
                    # rent
                    datapost['want'] = 'forrent'

                for i in range(6):
                    params = {
                        'id': post_id,
                        'o': 'photo' + str(i + 1),
                        'n': post_id + '-' + str(i + 1) + '.jpeg'
                    }

                    r = self.session.http_get('http://www.buyzaa.com/post-edit.php', params=params)
                    # print(r.url)
                    # print(r.status_code)

                r = self.session.http_post('http://www.buyzaa.com/lib/checkpost.php', data=datapost)
                # print(r.url)
                # print(r.status_code)

                datapost = [
                    ('save', (None, 'kkqm48ec2hkabfa1q22qbfnmg3')),
                    ('type', (None, 'guest')),
                    ('status', (None, '2hand')),
                    ('duration', (None, '-1')),
                    ('category', (None, '1009')),
                    ('subcategory', (None, theprodid)),
                    ('city', (None, province_id)),
                    ('district', (None, district_id)),
                    ('name', (None, postdata['post_title_th'])),
                    ('price', (None, str(postdata['price_baht']))),
                    ('detail', (None, postdata['post_description_th'])),
                    ('checkdetail', (None, postdata['post_description_th'])),
                    ('maplat', (None, str(postdata['geo_latitude']))),
                    ('maplon', (None, str(postdata['geo_longitude']))),
                    ('mapzoom', (None, '')),
                    ('contact', (None, postdata['name'])),
                    ('email', (None, postdata['email'])),
                    ('hiddenemail', (None, postdata['user'])),
                    ('phone', (None, postdata['mobile'])),
                    ('address', (None, prod_address)),
                    ('amphur', (None, 'เขตคลองเตย')),
                    ('province', (None, 'กรุงเทพมหานคร')),
                    ('zipcode', (None, '10400')),
                    ('website', (None, ''))
                ]

                if postdata['listing_type'] != 'เช่า':
                    # sell
                    datapost.append(('want', (None, 'sale')))
                else:
                    # rent
                    datapost.append(('want', (None, 'forrent')))

                for i, img in enumerate(postdata['post_images'][:6]):
                    filename = str(i + 1) + '.jpeg'
                    indexname = 'photo' + str(i + 1)
                    datapost.append((indexname, (filename, open(img, 'rb'), 'image/jpeg')))

                n = len(postdata['post_images'][:6])

                params = {
                    'id': post_id,
                    'o': 'photo' + str(n),
                    'n': post_id + '-' + str(n) + '.jpeg'
                }

                r = self.session.http_post('http://www.buyzaa.com/post-edit.php', params=params, data={},
                                             files=datapost)
                # print(r.url)
                # print(r.status_code)

                success = True
                detail = "Post edited successfully"
                
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
            "log_id": postdata['log_id'],
            "post_id": post_id,
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
        post_id = postdata['post_id']
        post_url = ""

        if success:

            """page = 0
            post_found = False
            tot_pages = 100

            while True:
                page += 1
                if page > tot_pages:
                    break
                r = self.session.http_get('http://www.buyzaa.com/manage-post.php', params={'page': str(page)})
                # print(r.url)
                # print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                tot_pages = int(len(soup.find('div', 'pagination').find('ul').find_all('li'))) - 2
                all_posts = soup.find('div', 'postlist').findChildren('ul')
                # print(tot_pages)

                # if len(all_posts) == 0:
                #     break

                for post in all_posts:
                    post_id = post.find('li', 'title').find('a').get('href').split('/')[-2][4:]
                    # print(post_id)

                    if post_id == postdata['post_id']:
                        post_found = True
                        break

                if post_found:
                    break"""

            try:
                r = self.session.http_get('http://www.buyzaa.com/manage-post.php', params={'update': post_id})
                # print(r.url)
                # print(r.status_code)
                if 'ยินดีด้วยค่ะ ระบบได้ทำการเลื่อนประกาศให้ท่านเรียบร้อยแล้ว' in r.text:
                    success = True
                    detail = "Post boosted successfully"
                    # post_id = info[1].split('=')[-1]
                    # post_title = info[2].split('=')[-1].replace(' ', '-')
                    # post_url = 'http://www.buyzaa.com/view' + post_id + '/' + post_title
                else:
                    success = False
                    detail = "Couldnot boost post"
            except:
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
            "log_id": postdata['log_id'],
            "post_id": post_id,
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
        post_id = postdata['post_id']
        post_url = ""

        if success:

            page = 0
            post_found = True
            tot_pages = 100

            """while True:
                page += 1
                if page > tot_pages:
                    break
                r = self.session.http_get('http://www.buyzaa.com/manage-post.php', params={'page': str(page)})
                # print(r.url)
                # print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                tot_pages = int(len(soup.find('div', 'pagination').find('ul').find_all('li'))) - 2
                all_posts = soup.find('div', 'postlist').findChildren('ul')
                # print(tot_pages)

                # if len(all_posts) == 0:
                #     break

                for post in all_posts:
                    post_id = post.find('li', 'title').find('a').get('href').split('/')[-2][4:]
                    # print(post_id)

                    if post_id == postdata['post_id']:
                        post_found = True
                        break

                if post_found:
                    break"""

            if post_found:
                r = self.session.http_get('http://www.buyzaa.com/manage-post.php', params={'delete': post_id})
                # print(r.url)
                # print(r.status_code)

                if 'ยินดีด้วยค่ะ ระบบได้ทำการลบประกาศให้ท่านเรียบร้อยแล้ว' in r.text:
                    success = True
                    detail = "Post deleted successfully"
                    # post_id = info[1].split('=')[-1]
                    # post_title = info[2].split('=')[-1].replace(' ', '-')
                    # post_url = 'http://www.buyzaa.com/view' + post_id + '/' + post_title
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
            "log_id": postdata['log_id'],
            "post_id": post_id,
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
            tot_pages = 100

            while True:
                page += 1
                if page > tot_pages:
                    break
                r = self.session.http_get('http://www.buyzaa.com/manage-post.php', params={'page': str(page)})
                # print(r.url)
                # print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                tot_pages = int(len(soup.find('div', 'pagination').find('ul').find_all('li'))) - 2
                all_posts = soup.find('div', 'postlist').findChildren('ul')
                # print(tot_pages)

                # if len(all_posts) == 0:
                #     break

                for post in all_posts:
                    post_title = post.find('li', 'title').find('a').get('href').split('/')[-1]
                    # print(post_title)

                    if post_title == postdata['post_title_th'].replace('.', '').replace(',', '')[:100].strip().replace(' ', '-'):
                        post_found = True
                        post_id = post.find('li', 'title').find('a').get('href').split('/')[-2][4:]
                        post_url = 'http://www.buyzaa.com/view' + post_id + '/' + post_title
                        r = self.session.http_get(post_url)
                        # print(r.url)
                        # print(r.status_code)
                        soup = BeautifulSoup(r.content, self.parser)
                        info = soup.find('div', 'data').findChildren('p', recursive=False)
                        post_created = str(info[6].contents[-1])
                        post_modified = str(info[7].contents[-1])
                        post_view = str(info[11].contents[-1])
                        success = True
                        detail = "Post Found"
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
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "post_url": post_url,
            "post_created": post_created,
            "post_modified": post_modified,
            "post_view": post_view,
            "account_type": "null",
            "detail": detail,
            "websitename": self.webname,
            "post_title_th": postdata['post_title_th']
        }
