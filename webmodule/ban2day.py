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
import random
from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys



class ban2day():

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
        self.webname = 'ban2day'
        self.httprequestObj = lib_httprequest()

    def print_debug(self, msg):
        if self.debug == 1:
            print(msg)
        return True

    def register_user(self, userdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        datapost = {
            "username": userdata['user'].split('@')[0],
            "pass": userdata['pass'],
            "conpass": userdata['pass'],
            "email": userdata['user'],
            "name": userdata['name_th'],
            "lastname": userdata['surname_th'],
            "phone": userdata['tel'],
            "submit": "",
        }

        if 'address' in userdata.keys():
            datapost['address'] = userdata['address']
        else:
            datapost['address'] = ''

        r = self.httprequestObj.http_post('http://www.ban2day.com/signup_member.php', data=datapost)
        # print(r.url)
        # print(r.status_code)
        data = r.text

        if 'สมัครสมาชิกเรียบร้อยแล้ว' in data:
            success = True
            detail = "Registered successfully"
        else:
            success = False
            detail = "Could not register"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": userdata['ds_id'],
            "detail": detail,
            "websitename": self.webname,
        }

    def test_login(self, userdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        datapost = {
            "log_u": userdata['user'],
            "log_p": userdata['pass'],
            "submit": "",
        }

        # print(datapost)

        r = self.httprequestObj.http_post('http://www.ban2day.com/login.php', data=datapost)
        # print(r.url)
        # print(r.status_code)
        data = r.text

        if 'Username หรือ Password ไม่ถูกต้อง' not in data:
            success = True
            detail = "Login successful"
        else:
            success = False
            detail = "Could not login"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": userdata['ds_id'],
            "detail": detail,
            "websitename": self.webname,
        }

    def create_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        # print(postdata)
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
            getProdId = {'1': '1', '2': '5', '3': '3', '4': '3',
                         '5': '2', '6': '4', '7': '7', '8': '7', '9': '6', '10': '8', '25': '8'}

            try:
                theprodid = getProdId[proid[str(postdata['property_type'])]]
                postdata['property_type'] = str(proid[str(postdata['property_type'])])
            except:
                theprodid = getProdId[str(postdata['property_type'])]

            r = self.httprequestObj.http_get('http://www.ban2day.com/maneg_property.php')
            # print(r.url)
            # print(r.status_code)

            r = self.httprequestObj.http_get('http://www.ban2day.com/add_property.php')
            # print(r.url)
            # print(r.status_code)

            soup = BeautifulSoup(r.content, self.parser)
            provinces = soup.find('select', {'name': 'Province'})
            provinces = provinces.find_all('option')[1:]

            ## FOR PROVINCE SELECTION
            province_id_map = {}

            for province in provinces:
                cur_prov_id = province.get('value')
                cur_prov_name = province.string

                province_id_map[cur_prov_name] = cur_prov_id

            found_prov = False
            province_id = ''

            # FOR DIRECT MATCH
            for (key, value) in province_id_map.items():
                if postdata['addr_province'] == key or postdata['addr_province'] == key.replace(' ', ''):
                    found_prov = True
                    province_id = value
                    break

            # FOR INDIRECT MATCH
            if not found_prov:
                for (key, value) in province_id_map.items():
                    if postdata['addr_province'] in key or postdata['addr_province'].replace(' ', '') in key.replace(
                            ' ',
                            '') or key.replace(
                        ' ', '') in postdata['addr_province'].replace(' ', ''):
                        found_prov = True
                        province_id = value
                        break

            # FOR NO MATCH
            if not found_prov:
                province_id = next(iter(province_id_map.values()))

            # print("Province id  = " + str(province_id))

            params = {
                'ID': province_id,
                'TYPE': 'District'
            }

            r = self.httprequestObj.http_get('http://www.ban2day.com/getaddress.php', params=params)
            # print(r.url)
            # print(r.status_code)

            ## FOR DISTRICT SELECTION
            district_id_map = {}

            for item in r.json():
                district_id_map[item["AMPHUR_NAME"]] = item["AMPHUR_ID"]

            found_distr = False
            district_id = ''

            # FOR DIRECT MATCH
            for (key, value) in district_id_map.items():
                if postdata['addr_district'] == key or postdata['addr_district'] == key.replace(' ', ''):
                    found_distr = True
                    district_id = value
                    break

            # FOR INDIRECT MATCH
            if not found_distr:
                for (key, value) in district_id_map.items():
                    if postdata['addr_district'] in key or postdata['addr_district'].replace(' ', '') in key.replace(
                            ' ',
                            '') or key.replace(
                        ' ', '') in postdata['addr_district'].replace(' ', ''):
                        found_distr = True
                        district_id = value
                        break

            # FOR NO MATCH
            if not found_distr:
                district_id = next(iter(district_id_map.values()))

            # print("District id  = " + str(district_id))

            params = {
                'ID': district_id,
                'TYPE': 'Subdistrict'
            }

            r = self.httprequestObj.http_get('http://www.ban2day.com/getaddress.php', params=params)
            # print(r.url)
            # print(r.status_code)

            ## FOR SUBDISTRICT SELECTION
            subdistrict_id_map = {}

            for item in r.json():
                subdistrict_id_map[item["DISTRICT_NAME"]] = item["DISTRICT_ID"]

            found_subdistr = False
            subdistrict_id = ''

            # FOR DIRECT MATCH
            for (key, value) in subdistrict_id_map.items():
                if postdata['addr_sub_district'] == key or postdata['addr_sub_district'] == key.replace(' ', ''):
                    found_subdistr = True
                    subdistrict_id = value
                    break

            # FOR INDIRECT MATCH
            if not found_subdistr:
                for (key, value) in subdistrict_id_map.items():
                    if postdata['addr_sub_district'] in key or postdata['addr_sub_district'].replace(' ',
                                                                                                     '') in key.replace(
                        ' ',
                        '') or key.replace(
                        ' ', '') in postdata['addr_sub_district'].replace(' ', ''):
                        found_subdistr = True
                        subdistrict_id = value
                        break

            # FOR NO MATCH
            if not found_subdistr:
                subdistrict_id = next(iter(subdistrict_id_map.values()))

            # print("Subdistrict id  = " + str(subdistrict_id))

            if postdata['property_type'] == 1:
                try:
                    area = postdata['floor_area']
                except:
                    area = 0.0
            else:
                if postdata['land_size_rai'] is None or postdata['land_size_rai'] == '':
                    postdata['land_size_rai'] = 0.0
                if postdata['land_size_ngan'] is None or postdata['land_size_ngan'] == '':
                    postdata['land_size_ngan'] = 0.0
                if postdata['land_size_wa'] is None or postdata['land_size_wa'] == '':
                    postdata['land_size_wa'] = 0.0
                area = float(postdata['land_size_rai']) * 400 + float(postdata['land_size_ngan']) * 100 + float(
                    postdata['land_size_wa'])

            prod_address = ""
            for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'],
                        postdata['addr_district'], postdata['addr_province']]:
                if add is not None:
                    prod_address += add + " "
            prod_address = prod_address[:-1]

            ## Stage I
            datapost = [
                ('name', (None, postdata['post_title_th'])),
                ('project', (None, postdata['web_project_name'])),
                ('section', (None, str(theprodid))),
                ('number', (None, prod_address)),
                ('road', (None, postdata['addr_road'])),
                ('Province', (None, province_id)),
                ('District', (None, district_id)),
                ('Subdistrict', (None, subdistrict_id)),
                ('price', (None, postdata['price_baht'])),
                ('area', (None, str(area))),
                ('layer', (None, postdata['floor_total'])),
                ('room', (None, postdata['bed_room'])),
                ('toilet', (None, postdata['bath_room'])),
                ('detail', (None, postdata['post_description_th'].replace('\r\n', '<br>'))),
                ('Submit', (None, 'เพิ่มข้อมูลประกาศ')),
            ]

            if postdata['listing_type'] != 'เช่า':
                # sell
                datapost.append(('cate', (None, '1')))
            else:
                # rent
                datapost.append(('cate', (None, '2')))

            r = self.httprequestObj.http_post('http://www.ban2day.com/add_property.php', data={}, files=datapost)
            # print(r.url)
            # print(r.status_code)

            soup = BeautifulSoup(r.content, self.parser)
            post_data = soup.find('meta', {'http-equiv': 'refresh'}).get('content')

            post_id = post_data.split('=')[-1]
            post_url = 'http://www.ban2day.com/property.php?id=' + post_id

            # print(post_id)
            # print(post_url)
            #
            # print('Entering stage II')

            r = self.httprequestObj.http_get('http://www.ban2day.com/add_map.php', params={'id': post_id})
            # print(r.url)
            # print(r.status_code)

            ## STAGE II
            map_data = [
                ('namePlace', (None, '')),
                ('lat_value', (None, str(postdata['geo_latitude']))),
                ('lon_value', (None, str(postdata['geo_longitude']))),
                ('zoom_value', (None, '0')),
                ('ID', (None, post_id)),
                ('Submit', (None, 'เพิ่มข้อมูลแผนที่'))
            ]

            r = self.httprequestObj.http_post('http://www.ban2day.com/add_map.php', params={'id': post_id}, data={},
                                         files=map_data)
            # print(r.url)
            # print(r.status_code)

            # print('Entering stage III')

            ## STAGE III

            r = self.httprequestObj.http_get('http://www.ban2day.com/add_img.php', params={'id': post_id})
            # print(r.url)
            # print(postdata['post_img_url_lists'])

            for i, image in enumerate(postdata['post_images']):
                # file_data = []
                filename = str(random.randint(1,10000000)) + '.jpeg'
                file_data = {'photoimg': (filename, open(image, 'rb'), 'image/jpeg')}
                r = self.httprequestObj.http_post('http://www.ban2day.com/ajax_img.php', data={}, files=file_data)
                # print(filename)
                # print(r.url)
                #print(r.text)
                #time.sleep(0.8)
                # self.httprequestObj.http_get("http://www.ban2day.com/"+r.text.split("src='")[1].split("'")[0])
                # self.httprequestObj.http_get("http://www.ban2day.com/"+r.text.split("src='")[1].split("'")[0])
                # r = self.httprequestObj.http_get('http://www.ban2day.com/add_img.php', params={'id': post_id})
                # print(r.url)

            r = self.httprequestObj.http_get('http://www.ban2day.com/property.php', params={'id': post_id})
            # print(r.url)
            # print(r.status_code)

            soup = BeautifulSoup(r.content, self.parser)
            title = soup.find('h2', 'panel-property').string

            if title == postdata['post_title_th']:
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
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
            "post_url": post_url,
            "detail": detail,
            "websitename": self.webname,
        }

    def edit_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        # print(postdata)
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""

        if success:

            ind = 0
            post_found = True

            """while True:
                r = self.httprequestObj.http_get('http://www.ban2day.com/maneg_property.php?&page=' + str(ind))
                # print(ind)
                # print(r.url)
                # print(r.status_code)
                ind += 1

                soup = BeautifulSoup(r.content, self.parser)
                all_posts = soup.find('tbody').findChildren('tr')
                # print(len(all_posts))

                if len(all_posts) == 0:
                    break

                for post in all_posts:
                    post_id = post.findChildren('td', recursive=False)[1].find('a').get('href').split('-')[1]
                    # print(post_id)
                    if post_id == postdata['post_id']:
                        post_found = True
                        # print('Found post')
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
                getProdId = {'1': '1', '2': '5', '3': '3', '4': '3',
                             '5': '2', '6': '4', '7': '7', '8': '7', '9': '6', '10': '8', '25': '8'}

                try:
                    theprodid = getProdId[proid[str(postdata['property_type'])]]
                    postdata['property_type'] = str(proid[str(postdata['property_type'])])
                except:
                    theprodid = getProdId[str(postdata['property_type'])]

                r = self.httprequestObj.http_get('http://www.ban2day.com/maneg_property.php')
                # print(r.url)
                # print(r.status_code)

                r = self.httprequestObj.http_get('http://www.ban2day.com/edit_property.php',
                                            params={'id': postdata['post_id']})
                # print(r.url)
                # print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                provinces = soup.find('select', {'name': 'Province'})
                provinces = provinces.find_all('option')[1:]

                ## FOR PROVINCE SELECTION
                province_id_map = {}

                for province in provinces:
                    cur_prov_id = province.get('value')
                    cur_prov_name = province.string

                    province_id_map[cur_prov_name] = cur_prov_id

                found_prov = False
                province_id = ''

                # FOR DIRECT MATCH
                for (key, value) in province_id_map.items():
                    if postdata['addr_province'] == key or postdata['addr_province'] == key.replace(' ', ''):
                        found_prov = True
                        province_id = value
                        break

                # FOR INDIRECT MATCH
                if not found_prov:
                    for (key, value) in province_id_map.items():
                        if postdata['addr_province'] in key or postdata['addr_province'].replace(' ',
                                                                                                 '') in key.replace(
                            ' ',
                            '') or key.replace(
                            ' ', '') in postdata['addr_province'].replace(' ', ''):
                            found_prov = True
                            province_id = value
                            break

                # FOR NO MATCH
                if not found_prov:
                    province_id = next(iter(province_id_map.values()))

                # print("Province id  = " + str(province_id))

                params = {
                    'ID': province_id,
                    'TYPE': 'District'
                }

                r = self.httprequestObj.http_get('http://www.ban2day.com/getaddress.php', params=params)
                # print(r.url)
                # print(r.status_code)

                ## FOR DISTRICT SELECTION
                district_id_map = {}

                for item in r.json():
                    district_id_map[item["AMPHUR_NAME"]] = item["AMPHUR_ID"]

                found_distr = False
                district_id = ''

                # FOR DIRECT MATCH
                for (key, value) in district_id_map.items():
                    if postdata['addr_district'] == key or postdata['addr_district'] == key.replace(' ', ''):
                        found_distr = True
                        district_id = value
                        break

                # FOR INDIRECT MATCH
                if not found_distr:
                    for (key, value) in district_id_map.items():
                        if postdata['addr_district'] in key or postdata['addr_district'].replace(' ',
                                                                                                 '') in key.replace(
                            ' ',
                            '') or key.replace(
                            ' ', '') in postdata['addr_district'].replace(' ', ''):
                            found_distr = True
                            district_id = value
                            break

                # FOR NO MATCH
                if not found_distr:
                    district_id = next(iter(district_id_map.values()))

                # print("District id  = " + str(district_id))

                params = {
                    'ID': district_id,
                    'TYPE': 'Subdistrict'
                }

                r = self.httprequestObj.http_get('http://www.ban2day.com/getaddress.php', params=params)
                # print(r.url)
                # print(r.status_code)

                ## FOR SUBDISTRICT SELECTION
                subdistrict_id_map = {}

                for item in r.json():
                    subdistrict_id_map[item["DISTRICT_NAME"]] = item["DISTRICT_ID"]

                found_subdistr = False
                subdistrict_id = ''

                # FOR DIRECT MATCH
                for (key, value) in subdistrict_id_map.items():
                    if postdata['addr_sub_district'] == key or postdata['addr_sub_district'] == key.replace(' ', ''):
                        found_subdistr = True
                        subdistrict_id = value
                        break

                # FOR INDIRECT MATCH
                if not found_subdistr:
                    for (key, value) in subdistrict_id_map.items():
                        if postdata['addr_sub_district'] in key or postdata['addr_sub_district'].replace(' ',
                                                                                                         '') in key.replace(
                            ' ',
                            '') or key.replace(
                            ' ', '') in postdata['addr_sub_district'].replace(' ', ''):
                            found_subdistr = True
                            subdistrict_id = value
                            break

                # FOR NO MATCH
                if not found_subdistr:
                    subdistrict_id = next(iter(subdistrict_id_map.values()))

                # print("Subdistrict id  = " + str(subdistrict_id))

                if postdata['property_type'] == 1:
                    try:
                        area = postdata['floor_area']
                    except:
                        area = 0.0
                else:
                    if postdata['land_size_rai'] is None:
                        postdata['land_size_rai'] = 0.0
                    if postdata['land_size_ngan'] is None:
                        postdata['land_size_ngan'] = 0.0
                    if postdata['land_size_wa'] is None:
                        postdata['land_size_wa'] = 0.0
                    area = float(postdata['land_size_rai']) * 400 + float(postdata['land_size_ngan']) * 100 + float(
                        postdata['land_size_wa'])

                prod_address = ""
                for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'],
                            postdata['addr_district'], postdata['addr_province']]:
                    if add is not None:
                        prod_address += add + " "
                prod_address = prod_address[:-1]

                ## Stage I
                datapost = [
                    ('name', (None, postdata['post_title_th'])),
                    ('project', (None, postdata['web_project_name'])),
                    ('section', (None, str(theprodid))),
                    ('number', (None, prod_address)),
                    ('road', (None, postdata['addr_road'])),
                    ('Province', (None, province_id)),
                    ('District', (None, district_id)),
                    ('Subdistrict', (None, subdistrict_id)),
                    ('price', (None, postdata['price_baht'])),
                    ('area', (None, str(area))),
                    ('layer', (None, postdata['floor_total'])),
                    ('room', (None, postdata['bed_room'])),
                    ('toilet', (None, postdata['bath_room'])),
                    ('detail', (None, postdata['post_description_th'].replace('\r\n', '<br>'))),
                    ('ID', (None, postdata['post_id'])),
                    ('Submit', (None, 'แก้ไขข้อมูลประกาศ')),
                ]

                if postdata['listing_type'] != 'เช่า':
                    # sell
                    datapost.append(('cate', (None, '1')))
                else:
                    # rent
                    datapost.append(('cate', (None, '2')))

                r = self.httprequestObj.http_post('http://www.ban2day.com/edit_property.php',
                                             params={'id': postdata['post_id']}, data={}, files=datapost)
                # print(r.url)
                # print(r.status_code)

                # print('Entering stage II')

                r = self.httprequestObj.http_get('http://www.ban2day.com/edit_map.php', params={'id': post_id})
                # print(r.url)
                # print(r.status_code)

                ## STAGE II
                map_data = [
                    ('namePlace', (None, '')),
                    ('lat_value', (None, postdata['geo_latitude'])),
                    ('lon_value', (None, postdata['geo_longitude'])),
                    ('zoom_value', (None, '0')),
                    ('ID', (None, postdata['post_id'])),
                    ('Submit', (None, 'แก้ไขข้อมูลแผนที่'))
                ]

                r = self.httprequestObj.http_post('http://www.ban2day.com/edit_map.php', params={'id': postdata['post_id']},
                                             data={},
                                             files=map_data)
                # print(r.url)
                # print(r.status_code)

                # print('Entering stage III')

                ## STAGE III

                try:
                    options = Options()

                    options.add_argument("--headless")
                    options.add_argument('--no-sandbox')
                    options.add_argument('start-maximized')
                    options.add_argument('disable-infobars')
                    options.add_argument("--disable-extensions")
                    options.add_argument("disable-gpu")
                    options.add_argument("window-size=1920,1080")
                    path = './static/chromedriver'
                    self.driver = webdriver.Chrome(executable_path=path, options=options)
                    self.driver.get('http://www.ban2day.com/index.php')
                    sleep(5)
                    self.driver.find_element_by_xpath("/html/body/nav/div/div[2]/div/a[1]").click()
                    sleep(3)
                    self.driver.find_element_by_id('username').send_keys(postdata['user'])
                    self.driver.find_element_by_id('password').send_keys(postdata['pass'])
                    self.driver.find_element_by_name("submit").click()
                    sleep(3)
                    self.driver.get('http://www.ban2day.com/edit_img.php?id={}'.format(postdata['post_id']))
                    sleep(3)
                    while True:
                        try:
                            self.driver.find_element_by_xpath("/html/body/div[5]/div/div[1]/div/div[3]/div[2]/a/p/span").click()
                            sleep(2)
                            alert = self.driver.switch_to.alert
                            alert.accept()
                            sleep(2)
                            webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                            sleep(1)
                        except:
                            break
                    for pic in reversed(postdata['post_images']):
                        upload = self.driver.find_element_by_id("photoimg")
                        upload.send_keys(os.path.abspath(pic))
                        sleep(3)
                    sleep(3)
                finally:
                    self.driver.close()
                    self.driver.quit()
                """r = self.httprequestObj.http_get('http://www.ban2day.com/edit_img.php', params={'id': postdata['post_id']})
                # print(r.url)
                # print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                old_images = soup.find_all('a', 'thumbnail')

                for image in old_images:
                    del_url = 'http://www.ban2day.com/' + image.get('href')
                    r = self.httprequestObj.http_get(del_url)
                    # print(r.url)
                    # print(r.status_code)

                for i, image in enumerate(postdata['post_images']):
                    file_data = []
                    filename = str(i) + '.jpeg'
                    file_data.append(('photoimg', (filename, open(image, 'rb'), 'image/jpeg')))
                    r = self.httprequestObj.http_post('http://www.ban2day.com/ajax_img.php', data={}, files=file_data)"""
                    # print(r.url)
                    # print(r.status_code)

                r = self.httprequestObj.http_get('http://www.ban2day.com/property.php', params={'id': postdata['post_id']})
                # print(r.url)
                # print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                title = soup.find('h2', 'panel-property').string

                if title == postdata['post_title_th']:
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
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "detail": detail,
            "websitename": self.webname,
        }

    def boost_post(self, postdata):
        '''
        Not supported currently as it doesnot retain old information
        '''
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""

        if success:

            ind = 0
            post_found = True

            """while True:
                r = self.httprequestObj.http_get('http://www.ban2day.com/maneg_property.php?&page=' + str(ind))
                # print(ind)
                # print(r.url)
                # print(r.status_code)
                ind += 1

                soup = BeautifulSoup(r.content, self.parser)
                all_posts = soup.find('tbody').findChildren('tr')
                # print(len(all_posts))

                if len(all_posts) == 0:
                    break

                for post in all_posts:
                    post_id = post.findChildren('td', recursive=False)[1].find('a').get('href').split('-')[1]
                    # print(post_id)
                    if post_id == postdata['post_id']:
                        post_found = True
                        # print('Found post')
                        break

                if post_found:
                    break"""

            if post_found:

                ## Stage I
                datapost = [
                    # ('name', (None, 'great')),
                    ('ID', (None, postdata['post_id'])),
                    ('Submit', (None, 'แก้ไขข้อมูลประกาศ')),
                ]

                r = self.httprequestObj.http_post('http://www.ban2day.com/edit_property.php',
                                             params={'id': postdata['post_id']}, data={}, files=datapost)
                # print(r.url)
                # print(r.status_code)

                # r = self.httprequestObj.http_get('http://www.ban2day.com/property.php', params={'id': postdata['post_id']})
                # # print(r.url)
                # # print(r.status_code)

                # soup = BeautifulSoup(r.content, self.parser)
                # title = soup.find('h2', 'panel-property').string

                if 'บันทึกข้อมูลเรียบร้อยแล้ว' in r.text:
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
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "detail": detail,
            "websitename": self.webname,
        }

    def delete_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        # print(postdata)
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""

        if success:

            ind = 0
            post_found = True

            """while True:
                r = self.httprequestObj.http_get('http://www.ban2day.com/maneg_property.php?&page=' + str(ind))
                # print(ind)
                # print(r.url)
                # print(r.status_code)
                ind += 1

                soup = BeautifulSoup(r.content, self.parser)
                all_posts = soup.find('tbody').findChildren('tr')
                # print(len(all_posts))

                if len(all_posts) == 0:
                    break

                for post in all_posts:
                    post_id = post.findChildren('td', recursive=False)[1].find('a').get('href').split('-')[1]
                    # print(post_id)
                    if post_id == postdata['post_id']:
                        post_found = True
                        # print('Found post')
                        break

                if post_found:
                    break"""

            if post_found:

                ## Stage I

                r = self.httprequestObj.http_get('http://www.ban2day.com/maneg_property.php',
                                            params={'delete': postdata['post_id']}, data={})
                # print(r.url)
                # print(r.status_code)

                if 'ลบรายการที่เลือกเรียบร้อยแล้ว' in r.text:
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
            "log_id": postdata['log_id'],
            "post_id": postdata['post_id'],
            "detail": detail,
            "websitename": self.webname,
        }

    def search_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        # print(postdata)
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]

        post_id = ""
        post_url = ""
        post_created = ""
        post_view = ""

        if success:

            ind = 0
            post_found = False

            while True:
                r = self.httprequestObj.http_get('http://www.ban2day.com/maneg_property.php?&page=' + str(ind))

                with open('b.html', 'w') as f:
                    f.write(r.text)
                    
                # print(ind)
                # print(r.url)
                # print(r.status_code)
                ind += 1

                soup = BeautifulSoup(r.content, self.parser)
                all_posts = soup.find('tbody').findChildren('tr')
                # print(len(all_posts))

                if len(all_posts) == 0:
                    break

                for post in all_posts:
                    post_title = post.findChildren('td', recursive=False)[1].findChild('a').find('strong').string
                    print(post_title)
                    if post_title in postdata['post_title_th'] or postdata['post_title_th'] in post_title :
                        # print('Found post')
                        post_found = True
                        post_id = post.findChildren('td', recursive=False)[1].find('a').get('href').split('-')[1]
                        post_url = 'http://www.ban2day.com/property.php?id=' + post_id
                        r = self.httprequestObj.http_get('http://www.ban2day.com/property-' + post_id + '-xxx')
                        # print(r.url)
                        # print(r.status_code)
                        soup = BeautifulSoup(r.content, self.parser)
                        post_created_raw = soup.find('p', 'small marginb0').string

                        first_blank = -1
                        for i in range(len(post_created_raw)):
                            if post_created_raw[i] == ' ':
                                first_blank = i
                                break

                        post_created = post_created_raw[first_blank + 1:]
                        post_view = soup.find('div', 'col-xs-6 borright').find('strong', recursive=False).string
                        break

                if post_found:
                    break

            if post_found:
                success = True
                detail = "Found post"

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
            "post_found": post_found,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "post_url": post_url,
            "post_create_time": str(post_created),
            "post_modify_time": "",
            "post_view": str(post_view),
            "detail": detail,
            "websitename": self.webname,
        }
