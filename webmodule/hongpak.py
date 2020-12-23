# -*- coding: utf-8 -*-

from .lib_captcha import *
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
captcha = lib_captcha()


class hongpak():

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
        self.webname = 'hongpak'

    def print_debug(self, msg):
        if self.debug == 1:
            print(msg)
        return True

    def logout_user(self):
        url = 'https://www.hongpak.in.th/logout/'
        httprequestObj.http_get(url)


    def register_user(self, postdata):
        self.logout_user()
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        success = "true"
        detail = ""

        r = httprequestObj.http_get('https://www.hongpak.in.th/register/')
        print(r.url)
        print(r.status_code)

        soup = BeautifulSoup(r.content, self.parser)
        #print(soup.find_all('img'))
        print(soup.select(".control-label img"))
        #captcha_url = 'https://hongpak.in.th' + soup.find_all('img')[1].get('src')
        captcha_url = 'https://hongpak.in.th' + soup.select(".control-label img")[0].get('src')
        print(captcha_url)

        r = httprequestObj.http_get(captcha_url)
        print(r.url)
        print(r.status_code)

        os.system('touch ./imgtmp/Img_Captcha/captcha.jpeg')
        print('Made')
        with open('./imgtmp/Img_Captcha/captcha.jpeg', 'wb') as imf:
            imf.write(r.content)

        captcha_text = captcha.imageCaptcha('./imgtmp/Img_Captcha/captcha.jpeg')
        print(captcha_text)

        datapost = {
            "email": postdata['user'],
            "password": postdata['pass'],
            "firstname": postdata['name_th'],
            "lastname": postdata['surname_th'],
            "usefor": '2',
            "codecheck": captcha_text
        }

        r = httprequestObj.http_post(
            'https://www.hongpak.in.th/register/', data=datapost)
        print(r.url)
        print(r.status_code)
        data = r.text

        datapost = {
            'picture': '',
            'file': '',
            'firstname': postdata['name_th'],
            'lastname': postdata['surname_th'],
            'postcode': '10400',
            'province': '10',
            'amphur': '1014',
            'tumbon': '101401',
            'addr': '',
            'mobile': postdata['tel'],
            'phone': postdata['tel'],
            'btSubmit': 'แก้ไขข้อมูล'
        }

        r = httprequestObj.http_get('https://www.hongpak.in.th/profile/newuser?reg=1')
        print(r.url)
        print(r.status_code)

        r = httprequestObj.http_post('https://www.hongpak.in.th/profile', data=datapost)
        print(r.url)
        print(r.status_code)

        #with open('/home/aymaan/Desktop/rough.html', 'w') as f:
        #    f.write(r.text)


        if postdata["user"] in r.text:
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
        self.logout_user()
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        success = "true"
        detail = ""
        print('Here')

        r = httprequestObj.http_get('https://www.hongpak.in.th/login/')
        print(r.url)
        print(r.status_code)

        datapost = {
            "log_u": postdata['user'],
            "log_p": postdata['pass'],
            "autolog": 'Y'
        }

        r = httprequestObj.http_post('https://www.hongpak.in.th/login/', data=datapost)
        print(r.url)
        print(r.status_code)

        #r = httprequestObj.http_get('https://www.hongpak.in.th/', data=datapost)
        #print(r.url)
        #print(r.status_code)
        #data = r.text

        # datapost = {
        #     'picture': '',
        #     'file': '',
        #     'firstname': postdata['name_th'],
        #     'lastname': postdata['surname_th'],
        #     'postcode': '10400',
        #     'province': '10',
        #     'amphur': '1014',
        #     'tumbon': '101401',
        #     'addr': '',
        #     'mobile': postdata['tel'],
        #     'phone': postdata['tel'],
        #     'btSubmit': 'แก้ไขข้อมูล'
        # }
        #
        # r = httprequestObj.http_get('https://www.hongpak.in.th/profile/newuser?reg=1')
        # print(r.url)
        # print(r.status_code)
        #
        # r = httprequestObj.http_post('https://www.hongpak.in.th/profile', data=datapost)
        # print(r.url)
        # print(r.status_code)

        #with open('/home/aymaan/Desktop/rough.html', 'w') as f:
        #    f.write(r.text)
        r = httprequestObj.http_get('https://www.hongpak.in.th/profile')

        if postdata["user"] in r.text :
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

        # start process
        #

        # login

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
            getProdId = {'1': '3', '2': '6', '3': '6', '4': '4',
                         '5': '6', '6': '6', '7': '1', '8': '7', '9': '6', '10': '6', '25': '6'}

            try:
                theprodid = getProdId[proid[str(postdata['property_type'])]]
            except:
                theprodid = getProdId[str(postdata['property_type'])]
                for i in proid:
                    if proid[i] == str(postdata['property_type']):
                        postdata['property_type'] = i

            prod_address = ""
            for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'],
                        postdata['addr_district'], postdata['addr_province']]:
                if add is not None:
                    prod_address += add + " "
            prod_address = prod_address[:-1]

            print('Going to post')

            r = httprequestObj.http_get('https://www.hongpak.in.th/roominfo/new')
            print(r.url)
            print(r.status_code)

            soup = BeautifulSoup(r.content, self.parser)
            try:
                r_field = soup.find('input', {'name': 'r'}).get('value')
            except:
                if "ยืนยันหมายเลขโทรศัพท์" in r.text:
                    time_end = datetime.datetime.utcnow()
                    time_usage = time_end - time_start
                    return {
                        "success": False,
                        "usage_time": str(time_usage),
                        "start_time": str(time_start),
                        "end_time": str(time_end),
                        "ds_id": postdata['ds_id'],
                        "post_id": post_id,
                        "post_url": post_url,
                        "account_type": "null",
                        "detail": "Please verify your phone Number First.",
                        "websitename": self.webname,
                    }
            provinces = soup.find('select', {'name': 'province'}).findChildren('option')[1:]

            province_id = provinces[0].get('value')

            for province in provinces:
                name = province.string
                if name.replace(' ', '') in postdata['addr_province'].replace(' ', '') or postdata[
                    'addr_province'].replace(' ', '') in name.replace(' ', ''):
                    province_id = province.get('value')
                    break

            print("Province_id= " + province_id)

            tempdata = {
                'province': province_id,
                'name': 'post',
                'r': '1594980331',
                'allowcomm': 'Y',
                'acept_warning': '1',
            }
            r = httprequestObj.http_post('https://www.hongpak.in.th/roominfo/new', data=tempdata)
            print(r.url)
            print(r.status_code)

            # with open('/home/codelover/Desktop/rough.html', 'w') as f:
            #     f.write(r.text)

            soup = BeautifulSoup(r.content, self.parser)
            districts = soup.find('select', {'name': 'amphur'}).findChildren('option')[1:]

            district_id = districts[0].get('value')

            for district in districts:
                name = district.string
                if name.replace(' ', '') in postdata['addr_district'].replace(' ', '') or postdata[
                    'addr_district'].replace(' ', '') in name.replace(' ', ''):
                    district_id = district.get('value')
                    break

            print("District_id= " + district_id)

            tempdata = {
                'province': province_id,
                'amphur': district_id,
                'name': 'post',
                'r': '1594980331',
                'allowcomm': 'Y',
                'acept_warning': '1',
            }
            r = httprequestObj.http_post('https://www.hongpak.in.th/roominfo/new', data=tempdata)
            print(r.url)
            print(r.status_code)

            soup = BeautifulSoup(r.content, self.parser)
            sub_districts = soup.find('select', {'name': 'tumbon'}).findChildren('option')[1:]

            sub_district_id = sub_districts[0].get('value')

            for sub_district in sub_districts:
                name = sub_district.string
                if name.replace(' ', '') in postdata['addr_sub_district'].replace(' ', '') or postdata[
                    'addr_sub_district'].replace(' ', '') in name.replace(' ', ''):
                    sub_district_id = sub_district.get('value')
                    break

            print("Subdistrict_id= " + sub_district_id)

            datapost = [
                ('code', ''),
                ('type', theprodid),
                ('name', postdata['post_title_th']),
                ('name_en', ''),
                ('email', postdata['email']),
                ('phone', postdata['mobile']),
                ('phone_en', ''),
                ('line', postdata['line']),
                ('fax', ''),
                ('condo_name', postdata['web_project_name']),
                ('roomno', ''),
                ('floor', postdata['floor_total']),
                ('bed', postdata['bed_room']),
                ('bath', postdata['bath_room']),
                ('usage', postdata['floorarea_sqm']),
                ('address', prod_address),
                ('soi', ''),
                ('street', ''),
                ('province', province_id),
                ('amphur', district_id),
                ('tumbon', sub_district_id),
                ('postcode', ''),
                ('address_en', ''),
                ('soi_en', ''),
                ('street_en', ''),
                ('warning', ''),
                ('warning', ''),
                ('lat', postdata['geo_latitude']),
                ('lng', postdata['geo_longitude']),
                ('detail', postdata['post_description_th']),
                ('detail_en', ''),
                ('near', ''),
                ('near_en', ''),
                ('guide', ''),
                ('guide_en', ''),
                ('r', r_field),
                ('price1', postdata['price_baht']),
                ('price2', ''),
                ('dailyprice1', ''),
                ('dailyprice2', ''),
                ('watercost', ''),
                ('watercost_en', ''),
                ('powercost', ''),
                ('powercost_en', ''),
                ('centercost', ''),
                ('centercost_en', ''),
                ('files[]', ''),
                ('allowcomm', 'Y'),
                ('acept_warning', '1'),
            ]

            for i, image in enumerate(postdata['post_images']):
                imgdata = [
                    ('r', (None, r_field)),
                    ('allowcomm', (None, 'Y')),
                    ('acept_warning', (None, '1'))
                ]
                filename = str(i) + '.jpeg'
                imgdata.append(('files', (filename, open(image, 'rb'), 'image/jpeg')))
                r = httprequestObj.http_post('https://www.hongpak.in.th/upload/', data={}, files=imgdata)
                print(r.url)
                print(r.status_code)
                print(r.json())
                img_path = r.json()['images'][0][0]
                datapost.append(('pid[]', ''))
                datapost.append(('file[]', img_path))
                if i == 0:
                    datapost.append(('df[]', '1'))
                else:
                    datapost.append(('df[]', ''))

            r = httprequestObj.http_post('https://www.hongpak.in.th/roominfo/new', data=datapost)
            print(r.url)
            print(r.status_code)

            #with open('/home/aymaan/Desktop/rough.html', 'w') as f:
            #   f.write(r.text)

            if 'ฉันไม่ต้องการใส่ประเภทห้อง, ข้ามไป ' in r.text:

                post_id = r.url.split('/')[-1]
                post_url = 'https://www.hongpak.in.th/' + post_id
                success = True
                detail = "Post created successsfully"
            elif "ชื่อประกาศนี้มีอยู่แล้วในระบบ" in r.text:
                success = False
                detail = "The title of this announcement already exists in the system."
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
            "account_type": "null",
            "detail": detail,
            "websitename": self.webname,
        }

    def edit_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        # start process
        #

        # login

        # print(postdata)
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""

        if success:

            page = 0
            post_found = False

            while True:
                page += 1
                r = httprequestObj.http_get('https://www.hongpak.in.th/myrooms/?p=' + str(page))
                print(r.url)
                print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                all_posts = soup.find_all('div', 'it st5')
                print(all_posts)

                if len(all_posts) == 0:
                    break

                for post in all_posts:
                    post_id = post.get('data-id')
                    if post_id == postdata['post_id']:
                        post_found = True
                        print('Post found')
                        break

                if post_found:
                    break

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
                getProdId = {'1': '3', '2': '6', '3': '6', '4': '4',
                             '5': '6', '6': '6', '7': '1', '8': '7', '9': '6', '10': '6', '25': '6'}

                try:
                    theprodid = getProdId[proid[str(postdata['property_type'])]]
                except:
                    theprodid = getProdId[str(postdata['property_type'])]
                    for i in proid:
                        if proid[i] == str(postdata['property_type']):
                            postdata['property_type'] = i

                prod_address = ""
                for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'],
                            postdata['addr_district'], postdata['addr_province']]:
                    if add is not None:
                        prod_address += add + " "
                prod_address = prod_address[:-1]

                print('Going to post')

                r = httprequestObj.http_get('https://www.hongpak.in.th/roominfo/' + post_id)
                print(r.url)
                print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                r_field = soup.find('input', {'name': 'r'}).get('value')
                provinces = soup.find('select', {'name': 'province'}).findChildren('option')[1:]

                province_id = provinces[0].get('value')

                for province in provinces:
                    name = province.string
                    if name.replace(' ', '') in postdata['addr_province'].replace(' ', '') or postdata[
                        'addr_province'].replace(' ', '') in name.replace(' ', ''):
                        province_id = province.get('value')
                        break

                print("Province_id= " + province_id)

                tempdata = {
                    'province': province_id,
                    'name': 'post',
                    'r': r_field,
                    'allowcomm': 'Y',
                    'acept_warning': '1',
                }
                r = httprequestObj.http_post('https://www.hongpak.in.th/roominfo/new', data=tempdata)
                print(r.url)
                print(r.status_code)

                # with open('/home/codelover/Desktop/rough.html', 'w') as f:
                #     f.write(r.text)

                soup = BeautifulSoup(r.content, self.parser)
                try:
                    r_field = soup.find('input', {'name': 'r'}).get('value')
                except:
                    if "ยืนยันหมายเลขโทรศัพท์" in r.text:
                        time_end = datetime.datetime.utcnow()
                        time_usage = time_end - time_start
                        return {
                            "success": False,
                            "usage_time": str(time_usage),
                            "start_time": str(time_start),
                            "end_time": str(time_end),
                            "ds_id": postdata['ds_id'],
                            "post_id": post_id,
                            "post_url": post_url,
                            "account_type": "null",
                            "detail": "Please verify your phone Number First.",
                            "websitename": self.webname,
                        }
                districts = soup.find('select', {'name': 'amphur'}).findChildren('option')[1:]

                district_id = districts[0].get('value')

                for district in districts:
                    name = district.string
                    if name.replace(' ', '') in postdata['addr_district'].replace(' ', '') or postdata[
                        'addr_district'].replace(' ', '') in name.replace(' ', ''):
                        district_id = district.get('value')
                        break

                print("District_id= " + district_id)

                tempdata = {
                    'province': province_id,
                    'amphur': district_id,
                    'name': 'post',
                    'r': r_field,
                    'allowcomm': 'Y',
                    'acept_warning': '1',
                }
                r = httprequestObj.http_post('https://www.hongpak.in.th/roominfo/new', data=tempdata)
                print(r.url)
                print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                r_field = soup.find('input', {'name': 'r'}).get('value')
                sub_districts = soup.find('select', {'name': 'tumbon'}).findChildren('option')[1:]

                sub_district_id = sub_districts[0].get('value')

                for sub_district in sub_districts:
                    name = sub_district.string
                    if name.replace(' ', '') in postdata['addr_sub_district'].replace(' ', '') or postdata[
                        'addr_sub_district'].replace(' ', '') in name.replace(' ', ''):
                        sub_district_id = sub_district.get('value')
                        break

                print("Subdistrict_id= " + sub_district_id)

                datapost = [
                    ('id', post_id),
                    ('code', ''),
                    ('type', theprodid),
                    ('name', postdata['post_title_th']),
                    ('name_en', ''),
                    ('email', postdata['email']),
                    ('phone', postdata['mobile']),
                    ('phone_en', ''),
                    ('line', postdata['line']),
                    ('fax', ''),
                    ('condo_name', postdata['web_project_name']),
                    ('roomno', ''),
                    ('floor', postdata['floor_total']),
                    ('bed', postdata['bed_room']),
                    ('bath', postdata['bath_room']),
                    ('usage', postdata['floorarea_sqm']),
                    ('address', prod_address),
                    ('soi', ''),
                    ('street', ''),
                    ('province', province_id),
                    ('amphur', district_id),
                    ('tumbon', sub_district_id),
                    ('postcode', '10400'),
                    ('address_en', ''),
                    ('soi_en', ''),
                    ('street_en', ''),
                    ('warning', ''),
                    ('warning', ''),
                    ('lat', postdata['geo_latitude']),
                    ('lng', postdata['geo_longitude']),
                    ('detail', postdata['post_description_th']),
                    ('detail_en', ''),
                    ('near', ''),
                    ('near_en', ''),
                    ('guide', ''),
                    ('guide_en', ''),
                    ('r', r_field),
                    ('price1', postdata['price_baht']),
                    ('price2', ''),
                    ('dailyprice1', ''),
                    ('dailyprice2', ''),
                    ('watercost', ''),
                    ('watercost_en', ''),
                    ('powercost', ''),
                    ('powercost_en', ''),
                    ('centercost', ''),
                    ('centercost_en', ''),
                    ('files[]', ''),
                    ('allowcomm', 'Y'),
                    ('acept_warning', '1'),
                    ('warning', '')
                ]

                for i, image in enumerate(postdata['post_images']):
                    imgdata = [
                        ('id', (None, post_id)),
                        ('r', (None, r_field)),
                        ('allowcomm', (None, 'Y')),
                        ('acept_warning', (None, '1'))
                    ]
                    filename = str(i) + '.jpeg'
                    imgdata.append(('files', (filename, open(image, 'rb'), 'image/jpeg')))
                    print(imgdata)
                    r = httprequestObj.http_post('https://www.hongpak.in.th/upload/', data={}, files=imgdata)
                    print(r.url)
                    print(r.status_code)
                    print(r.json())
                    img_path = r.json()['images'][0][0]
                    print(img_path)
                    datapost.append(('pid[]', ''))
                    datapost.append(('file[]', img_path))
                    if i == 0:
                        datapost.append(('df[]', '1'))
                    else:
                        datapost.append(('df[]', ''))

                edit_url = 'https://www.hongpak.in.th/roominfo/' + post_id
                r = httprequestObj.http_post(edit_url, data=datapost)
                print(r.url)
                print(r.status_code)

                with open('/home/aymaan/Desktop/rough.html', 'w') as f:
                  f.write(r.text)

                if 'บันทึกข้อมูลสำเร็จแล้ว' in r.text:
                    success = True
                    detail = "Post edited successfully"
                elif "ชื่อประกาศนี้มีอยู่แล้วในระบบ" in r.text:
                    success = False
                    detail = "The title of this announcement already exists in the system."
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
            "post_url": post_url,
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
        post_id = ""
        post_url = ""

        if success:

            page = 0
            post_found = False

            while True:
                page += 1
                r = httprequestObj.http_get('https://www.hongpak.in.th/myrooms/?p=' + str(page))
                print(r.url)
                print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                all_posts = soup.find_all('div', 'it st5')
                print(all_posts)

                if len(all_posts) == 0:
                    break

                for post in all_posts:
                    post_id = post.get('data-id')
                    if post_id == postdata['post_id']:
                        post_found = True
                        break

                if post_found:
                    break

            if post_found:
                boost_url = 'https://www.hongpak.in.th/apis/room'
                datapost = {
                    'xact': 'renew',
                    'id': post_id
                }
                r = httprequestObj.http_post(boost_url, data=datapost)
                print(r.url)
                print(r.status_code)
                data = r.json()

                if 'result' in data.keys() and data['result'] == 'OK':
                    success = True
                    detail = "Post boosted successfully"
                elif 'error' in data.keys() and data['error'] == 'ประกาศนี้ถูกเลื่อนแล้ว เลื่อนได้อีกครั้งในวันพรุ่งนี้':
                    success = False
                    detail = "Can boost tomorrow"
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
            "post_url": post_url,
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
        post_id = ""
        post_url = ""

        if success:

            page = 0
            post_found = False

            while True:
                page += 1
                r = httprequestObj.http_get('https://www.hongpak.in.th/myrooms/?p=' + str(page))
                print(r.url)
                print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                all_posts = soup.find_all('div', 'it st5')
                extra_posts = soup.find_all('div', 'it st6')
                for post in extra_posts:
                    all_posts.append(post)
                # print(all_posts)

                #with open('/home/codelover/Desktop/rough.html', 'w') as f:
                #   f.write(r.text)

                if len(all_posts) == 0:
                    break

                for post in all_posts:
                    post_id = post.get('data-id')
                    print(post.find('div', 'info'))
                    post_vis = post.find('div', 'info').find('div', 'info1').find('div', 'status').string
                    print(post_vis)
                    if post_id == postdata['post_id']:
                        post_found = True
                        break

                if post_found:
                    break

            if post_found:
                del_url = 'https://www.hongpak.in.th/apis/room'
                datapost = {
                    'xact': 'showhide',
                    'cstatus': 'hide',
                    'id': post_id
                }
                r = httprequestObj.http_post(del_url, data=datapost)
                print(r.url)
                print(r.status_code)
                data = r.text

                if 'set_row_status('+post_id+',6);' in data:
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
            "post_url": post_url,
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

        # start process
        #

        # login

        # print(postdata)
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""
        post_created = ''
        post_modified = ''
        post_view = ''

        if success:

            page = 0
            post_found = False

            while True:
                page += 1
                r = httprequestObj.http_get('https://www.hongpak.in.th/myrooms/?p=' + str(page))
                print(r.url)
                print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                all_posts = soup.find_all('div', 'it st5')
                print(all_posts)

                if len(all_posts) == 0:
                    break

                for post in all_posts:
                    post_title = post.find('div', 'info').find('div', 'info1').find('a', 'name').string
                    if post_title in postdata['post_title_th'] or postdata['post_title_th'] in post_title:
                        post_found = True
                        success = True
                        detail = "Post Found"
                        print("Post found")
                        post_id = post.get('data-id')
                        post_url = 'https://www.hongpak.in.th/' + post_id
                        dates = post.find('div', 'info').find('div', 'info1').find('div', 'stats').string.split(',')
                        post_created = str(dates[0].split(':')[1] + ':' + dates[0].split(':')[-1])
                        post_modified = str(dates[1].split(':')[1] + ':' + dates[1].split(':')[-1])
                        view_url = 'https://www.hongpak.in.th/roomstats/' + post_id + '/?rf=page'
                        r = httprequestObj.http_get(view_url)
                        print(r.url)
                        print(r.status_code)
                        soup = BeautifulSoup(r.content, self.parser)
                        post_view = str(soup.find('div', 'v').string)
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
            "detail": detail,
            "websitename": self.webname,
        }
