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
lib_captcha = lib_captcha()


class residences():

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
        self.webname = 'residences'

    def print_debug(self, msg):
        if self.debug == 1:
            print(msg)
        return True

    def logout_user(self):
        url = 'https://www.residences.in.th/users/sign_out'
        httprequestObj.http_get(url)

    def register_user(self, postdata):
        self.logout_user()
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        r = httprequestObj.http_get('https://www.residences.in.th/users/sign_up')
        print(r.url)
        print(r.status_code)

        soup = BeautifulSoup(r.content, self.parser)
        auth_token = soup.find('input', {'name': 'authenticity_token'}).get('value')
        print(auth_token)

        datapost = {
            'utf8': '✓',
            'authenticity_token': auth_token,
            'user[name]': postdata['name_th'] + ' ' + postdata['surname_th'],
            'user[email]': postdata['user'],
            'user[telephone]': postdata['tel'],
            'user[password]': postdata['pass'],
            'user[password_confirmation]': postdata['pass'],
            'user[member_type]': '0',
            'user[email_notice]': '0',
            'commit': 'สมัครสมาชิก'
        }
        r = httprequestObj.http_post('https://www.residences.in.th/users', data=datapost)
        data = r.text
        print(r.url)
        print(r.status_code)

        if 'เราได้ส่งลิงค์ คำยืนยันไปยังอีเมล์ของคุณ กรุณาเปิดลิงค์เพื่อยืนยันบัญชีของคุณคะ.' in data:
            success = True
            detail = "Registered successfully, Confirm your email"
        elif 'ถูกใช้ไปแล้ว' in data:
            success = False
            detail = "Email already registered."
        elif 'สั้นเกินไป (ต้องยาวกว่า 8 ตัวอักษร)' in data:
            success = False
            detail = "Password must be longer than 8 characters."
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

        r = httprequestObj.http_get('https://www.residences.in.th/users/sign_in')
        print(r.url)
        print(r.status_code)

        soup = BeautifulSoup(r.content, self.parser)
        auth_token = soup.find('input', {'name': 'authenticity_token'}).get('value')
        print(auth_token)

        datapost = {
            'utf8': '✓',
            'authenticity_token': auth_token,
            'user[email]': postdata['user'],
            'user[password]': postdata['pass'],
            'user[remember_me]': '0',
            'commit': 'เข้าสู่ระบบ'
        }
        r = httprequestObj.http_post('https://www.residences.in.th/users/sign_in', data=datapost)
        print(r.url)
        print(r.status_code)

        r = httprequestObj.http_get('https://www.residences.in.th/dashboard/apartments')
        print(r.url)
        print(r.status_code)
        data = r.text

        #with open('/home/codelover/Desktop/rough.html', 'w') as f:
            #f.write(data)
        # print(data)
        if 'ออกจากระบบ' in data:
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
            getProdId = {'1': 159, '2': 156, '3': 156, '4': 157,
                         '5': 158, '6': 161, '7': 162, '8': 162, '9': 162, '10': 162, '25': 162}

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

            r = httprequestObj.http_get('https://www.residences.in.th/apartments/new')
            print(r.url)
            print(r.status_code)

            soup = BeautifulSoup(r.content, self.parser)
            auth_token = soup.find('meta', {'name': 'csrf-token'}).get('content')

            try:
                provinces = soup.find('select', {'name': 'apartment[province_id]'}).findChildren('option')[1:]
            except:
                time_end = datetime.datetime.utcnow()
                time_usage = time_end - time_start
                if "ยืนยันเบอร์โทรศัพท์มือถือ" in r.text:
                    return {
                        "success": "false",
                        "usage_time": str(time_usage),
                        "start_time": str(time_start),
                        "end_time": str(time_end),
                        "post_url": post_url,
                        "ds_id": postdata['ds_id'],
                        "post_id": post_id,
                        "account_type": "null",
                        "detail": "Please verify your mobile phone number before posting / promoting ranking.",
                        "websitename": self.webname,
                    }
                else:
                    return {
                        "success": "false",
                        "usage_time": str(time_usage),
                        "start_time": str(time_start),
                        "end_time": str(time_end),
                        "post_url": post_url,
                        "ds_id": postdata['ds_id'],
                        "post_id": post_id,
                        "account_type": "null",
                        "detail": "Can't create post.",
                        "websitename": self.webname,
                    }

            province_id = provinces[0].get('value')

            for province in provinces:
                area = province.string
                if area.replace(' ', '') in postdata['addr_province'].replace(' ', '') or postdata[
                    'addr_province'].replace(' ', '') in area.replace(' ', ''):
                    province_id = province.get('value')
                    break

            r = httprequestObj.http_post('https://www.residences.in.th/dynamic_amphurs/' + province_id,
                                         data={province_id: ''})
            print(r.url)
            print(r.status_code)

            data = r.text.split('\n')[2:-2]

            district_id = data[0].split('value\",')[1].split(')')[0]

            for row in data:
                area = row.split('text(\'')[1].split('\'')[0]
                id = row.split('value\",')[1].split(')')[0].strip()
                # print(area)
                # print(id)
                if area.replace(' ', '') in postdata['addr_district'].replace(' ', '') or postdata[
                    'addr_district'].replace(' ', '') in area.replace(' ', ''):
                    district_id = id
                    break

            print('District id = ' + district_id)

            r = httprequestObj.http_post('https://www.residences.in.th/dynamic_districts/' + district_id,
                                         data={district_id: ''})
            print(r.url)
            print(r.status_code)

            data = r.text.split('\n')[3:-2]

            # print(data)

            sub_district_id = data[0].split('value\",')[1].split(')')[0]

            for row in data:
                area = row.split('text(\'')[1].split('\'')[0]
                id = row.split('value\",')[1].split(')')[0].strip()
                # print(area)
                # print(id)
                if area.replace(' ', '') in postdata['addr_sub_district'].replace(' ', '') or postdata[
                    'addr_sub_district'].replace(' ', '') in area.replace(' ', ''):
                    sub_district_id = id
                    break

            print('Subdistrict id = ' + sub_district_id)

            g = lib_captcha.reCaptcha('6LfAohcUAAAAAAnZ86DXS9_JzyGlIqyxEXTAUQMz',
                                      'https://www.residences.in.th/apartments/new')
            print(g)

            #if len(postdata['post_title_th'])>60:
            #    postdata['post_title_th']=postdata['post_title_th'][:60]

            datapost = [
                ('utf8', '✓'),
                ('authenticity_token', auth_token),
                ('apartment[name]', postdata['post_title_th']),
                ('apartment[en_name]', postdata['post_title_th']),
                ('apartment[apartment_type]', '0'),
                ('apartment[province_id]', province_id),
                ('apartment[amphur_id]', district_id),
                ('apartment[district_id]', sub_district_id),
                ('ignore_reverse_district_id', '0'),
                ('apartment[postcode]', '10400'),
                ('apartment[address]', '11'),
                ('apartment[road]', postdata['addr_road']),
                ('apartment[street]', postdata['addr_soi']),
                ('apartment[latitude]', postdata['geo_latitude']),
                ('apartment[longitude]', postdata['geo_longitude']),
                ('apartment[gmaps_zoom]', ''),
                ('apartment[staff]', postdata['name']),
                ('apartment[telephone]', postdata['mobile']),
                ('apartment[en_telephone]', ''),
                ('apartment[email]', postdata['email']),
                ('apartment[line_user_id]', postdata['line']),
                ('apartment[facebook_url]', ''),
                ('apartment[description]', postdata['post_description_th'].replace('\r\n', '<br>')),
                ('_wysihtml5_mode', '1'),
                ('_wysihtml5_mode', '1'),
                ('apartment[en_description]', ''),
                ('apartment[create_level]', '1'),
                ('ref_action', 'new'),
                ('g-recaptcha-response', g)
            ]

            r = httprequestObj.http_post('https://www.residences.in.th/apartments', data=datapost)
            print(r.url)
            print(r.status_code)

            #with open('/home/aymaan/Desktop/rough1.html', 'w') as f:
            #     f.write(r.text)

            print('First part done')

            second_url = r.url

            r = httprequestObj.http_get(second_url)
            print(r.url)
            print(r.status_code)

            soup = BeautifulSoup(r.content, self.parser)
            utf8 = soup.find('input', {'name': 'utf8'}).get('value')
            method = soup.find('input', {'name': '_method'}).get('value')
            auth_token = soup.find('input', {'name': 'authenticity_token'}).get('value')
            apartment_fi = soup.find('input', {'name': 'apartment[facility_ids][]'}).get('value')
            apartment_cfi = soup.find('input', {'name': 'apartment[central_facility_ids][]'}).get('value')
            dnvaf = soup.find('input', {'name': 'do_not_validation_all_facility'}).get('value')
            dnvli = soup.find('input', {'name': 'do_not_validation_listing_images'}).get('value')
            apartment_cl = soup.find('input', {'name': 'apartment[create_level]'}).get('value')
            ref_action = soup.find('input', {'name': 'ref_action'}).get('value')


            # postdata['post_images'] = []

            for i, img in enumerate(postdata['post_images']):
                filename = str(i) + '.jpeg'
                datapost = [
                    ('utf8', (None, utf8)),
                    ('_method', (None, method)),
                    ('authenticity_token', (None, auth_token)),
                    ('apartment[facility_ids][]', (None, apartment_fi)),
                    ('apartment[central_facility_ids][]', (None, apartment_cfi)),
                    ('do_not_validation_all_facility', (None, dnvaf)),
                    ('do_not_validation_listing_images', (None, dnvli)),
                    ('apartment[create_level]', (None, apartment_cl)),
                    ('ref_action', (None, ref_action)),
                    ('apartment[images_attributes][][attachment]', (filename, open(img, 'rb'), 'image/jpeg')),
                ]
                # print(second_url[:-10])
                # print(httprequestObj)
                # print(auth_token)
                r = httprequestObj.http_post(second_url[:-10], data={}, files=datapost)
                # print(r)
                print(r.url)
                print(r.status_code)
                print(r.text)

                r = httprequestObj.http_get(second_url)
                print(r.url)
                print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                utf8 = soup.find('input', {'name': 'utf8'}).get('value')
                method = soup.find('input', {'name': '_method'}).get('value')
                auth_token = soup.find('input', {'name': 'authenticity_token'}).get('value')
                apartment_fi = soup.find('input', {'name': 'apartment[facility_ids][]'}).get('value')
                apartment_cfi = soup.find('input', {'name': 'apartment[central_facility_ids][]'}).get('value')
                dnvaf = soup.find('input', {'name': 'do_not_validation_all_facility'}).get('value')
                dnvli = soup.find('input', {'name': 'do_not_validation_listing_images'}).get('value')
                apartment_cl = soup.find('input', {'name': 'apartment[create_level]'}).get('value')
                ref_action = soup.find('input', {'name': 'ref_action'}).get('value')

            print(auth_token)
            print(apartment_cl)
            print(ref_action)

            datapost = [
                ('utf8', utf8),
                ('_method', method),
                ('authenticity_token', auth_token),
                ('apartment[facility_ids][]', apartment_fi),
                ('apartment[central_facility_ids][]', ''),
                ('apartment[facility_ids][]', '5'),
                ('do_not_validation_all_facility', '0'),
                ('do_not_validation_listing_images', dnvli),
                ('apartment[create_level]', apartment_cl),
                ('ref_action', ref_action)
            ]

            r = httprequestObj.http_post(second_url[:-10], data=datapost)
            print(r.url)
            print(r.status_code)

            #with open('/home/aymaan/Desktop/rough2.html', 'w') as f:
            #    f.write(r.text)

            print('Second part done')

            third_url = r.url + '/roomtypes'
            r = httprequestObj.http_get(third_url)
            print(r.url)
            print(r.status_code)

            # with open('/home/codelover/Desktop/rough.html', 'w') as f:
            #     f.write(r.text)

            soup = BeautifulSoup(r.content, self.parser)
            utf8 = soup.find('input', {'name': 'utf8'}).get('value')
            method = soup.find('input', {'name': '_method'}).get('value')
            auth_token = soup.find('input', {'name': 'authenticity_token'}).get('value')

            # sp_id = soup.find('td', 'col-md-3 room-name-column').find('input').get('id').split('_')[-2]
            # print(sp_id)
            sp_id = '0'

            datapost = [
                ('utf8', utf8),
                ('_method', method),
                ('authenticity_token', auth_token),
                ('apartment[rooms_attributes]['+sp_id+'][name]', 'bedroom'),
                ('apartment[rooms_attributes]['+sp_id+'][room_type]', 'R2'),
                ('apartment[rooms_attributes]['+sp_id+'][size]', '11'),
                ('apartment[rooms_attributes]['+sp_id+'][monthly]', '0'),
                ('apartment[rooms_attributes]['+sp_id+'][monthly]', '1'),
                ('apartment[rooms_attributes]['+sp_id+'][min_price_permonth]', '100'),
                ('apartment[rooms_attributes]['+sp_id+'][max_price_permonth]', '200'),
                ('apartment[rooms_attributes]['+sp_id+'][daily]', '0'),
                ('apartment[rooms_attributes]['+sp_id+'][daily]', '1'),
                ('apartment[rooms_attributes]['+sp_id+'][min_price_perday]', '100'),
                ('apartment[rooms_attributes]['+sp_id+'][max_price_perday]', '200'),
                ('apartment[rooms_attributes]['+sp_id+'][available]', '0'),
                ('apartment[rooms_attributes]['+sp_id+'][available]', '1'),
                ('apartment[rooms_attributes]['+sp_id+'][_destroy]', 'false'),
                ('apartment[water_price]', ''),
                ('apartment[water_price_monthly_per_person]', ''),
                ('apartment[water_price_monthly_per_room]', ''),
                ('apartment[water_price_remark]', ''),
                ('apartment[water_price_type]', '5'),
                ('apartment[water_price_note]', ''),
                ('apartment[electric_price]', ''),
                ('apartment[electric_price_remark]', ''),
                ('apartment[electric_price_type]', '3'),
                ('apartment[electric_price_note]', ''),
                ('apartment[deposit_month]', ''),
                ('apartment[deposit_type]', '2'),
                ('apartment[deposit_bath]', postdata['price_baht']),
                ('apartment[deposit]', ''),
                ('apartment[advance_fee_month]', ''),
                ('apartment[advance_fee_bath]', ''),
                ('apartment[advance_fee_type]', '3'),
                ('apartment[advance_fee]', ''),
                ('apartment[phone_price_minute]', ''),
                ('apartment[phone_price_minute_unit]', ''),
                ('apartment[phone_price_per_time]', ''),
                ('apartment[phone_price_type]', '3'),
                ('apartment[phone_price]', ''),
                ('apartment[internet_price_bath]', ''),
                ('apartment[internet_price_unit]', ''),
                ('apartment[internet_price_type]', '2'),
                ('apartment[internet_price]', ''),
                ('apartment[has_promotion]', '0'),
                ('apartment[promotion_start]', ''),
                ('apartment[promotion_end]', ''),
                ('apartment[promotion_description]', ''),
                ('_wysihtml5_mode', '1'),
                ('apartment[create_level]', '3'),
                ('ref_action', 'roomtypes'),
            ]

            r = httprequestObj.http_post(third_url[:-10], data=datapost)
            print(r.url)
            print(r.status_code)

            url = 'https://www.residences.in.th/dashboard/apartments'
            r = httprequestObj.http_get(url)
            print(r.url)
            print(r.status_code)

            url = third_url[:-10] + '/edit'
            r = httprequestObj.http_get(url)
            print(r.url)
            print(r.status_code)

            url = third_url[:-10] + '/information'
            r = httprequestObj.http_get(url)
            print(r.url)
            print(r.status_code)

            r = httprequestObj.http_get(third_url)
            print(r.url)
            print(r.status_code)

            soup = BeautifulSoup(r.content, self.parser)
            room_id = soup.find('tbody').find('tr').get('id').split('_')[-1]
            print(room_id)

            soup = BeautifulSoup(r.content, self.parser)
            utf8 = soup.find('input', {'name': 'utf8'}).get('value')
            method = soup.find('input', {'name': '_method'}).get('value')
            auth_token = soup.find('input', {'name': 'authenticity_token'}).get('value')

            datapost = [
                ('utf8', '✓'),
                ('_method', 'put'),
                ('authenticity_token', auth_token),
                ('apartment[rooms_attributes][' + sp_id + '][name]', 'bedroom'),
                ('apartment[rooms_attributes][' + sp_id + '][room_type]', 'R2'),
                ('apartment[rooms_attributes][' + sp_id + '][size]', '11'),
                ('apartment[rooms_attributes][' + sp_id + '][monthly]', '0'),
                ('apartment[rooms_attributes][' + sp_id + '][monthly]', '1'),
                ('apartment[rooms_attributes][' + sp_id + '][min_price_permonth]', '100'),
                ('apartment[rooms_attributes][' + sp_id + '][max_price_permonth]', '200'),
                ('apartment[rooms_attributes][' + sp_id + '][daily]', '0'),
                ('apartment[rooms_attributes][' + sp_id + '][daily]', '1'),
                ('apartment[rooms_attributes][' + sp_id + '][min_price_perday]', '100'),
                ('apartment[rooms_attributes][' + sp_id + '][max_price_perday]', '200'),
                ('apartment[rooms_attributes][' + sp_id + '][available]', '0'),
                ('apartment[rooms_attributes][' + sp_id + '][available]', '1'),
                ('apartment[rooms_attributes][' + sp_id + '][_destroy]', 'false'),
                ('apartment[rooms_attributes][' + sp_id + '][id]', room_id),
                ('apartment[water_price]', ''),
                ('apartment[water_price_monthly_per_person]', ''),
                ('apartment[water_price_monthly_per_room]', ''),
                ('apartment[water_price_remark]', ''),
                ('apartment[water_price_type]', '5'),
                ('apartment[water_price_note]', ''),
                ('apartment[electric_price]', ''),
                ('apartment[electric_price_remark]', ''),
                ('apartment[electric_price_type]', '3'),
                ('apartment[electric_price_note]', ''),
                ('apartment[deposit_month]', ''),
                ('apartment[deposit_type]', '2'),
                ('apartment[deposit_bath]', postdata['price_baht']),
                ('apartment[deposit]', ''),
                ('apartment[advance_fee_month]', ''),
                ('apartment[advance_fee_bath]', ''),
                ('apartment[advance_fee_type]', '3'),
                ('apartment[advance_fee]', ''),
                ('apartment[phone_price_minute]', ''),
                ('apartment[phone_price_minute_unit]', ''),
                ('apartment[phone_price_per_time]', ''),
                ('apartment[phone_price_type]', '3'),
                ('apartment[phone_price]', ''),
                ('apartment[internet_price_bath]', ''),
                ('apartment[internet_price_unit]', ''),
                ('apartment[internet_price_type]', '2'),
                ('apartment[internet_price]', ''),
                ('apartment[has_promotion]', '0'),
                ('apartment[promotion_start]', ''),
                ('apartment[promotion_end]', ''),
                ('apartment[promotion_description]', ''),
                ('_wysihtml5_mode', '1'),
                ('apartment[create_level]', '4'),
                ('ref_action', 'roomtypes'),
            ]

            r = httprequestObj.http_post(third_url[:-10], data=datapost)
            print(r.url)
            print(r.status_code)

            # with open('/home/codelover/Desktop/rough.html', 'w') as f:
            #     f.write(r.text)

            print('Third part done')

            fourth_url = r.url + '/verify'
            r = httprequestObj.http_get(fourth_url)
            print(r.url)
            print(r.status_code)

            post_id = fourth_url.split('/')[-2].split('-')[0]
            post_url = ''

            #with open('/home/aymaan/Desktop/rough3.html', 'w') as f:
            #    f.write(r.text)

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

            r = httprequestObj.http_get('https://www.residences.in.th/apartments/new')
            print(r.url)
            print(r.status_code)

            soup = BeautifulSoup(r.content, self.parser)
            auth_token = soup.find('meta', {'name': 'csrf-token'}).get('content')

            provinces = soup.find('select', {'name': 'apartment[province_id]'}).findChildren('option')[1:]
            province_id = provinces[0].get('value')

            for province in provinces:
                area = province.string
                if area.replace(' ', '') in postdata['addr_province'].replace(' ', '') or postdata[
                    'addr_province'].replace(' ', '') in area.replace(' ', ''):
                    province_id = province.get('value')
                    break

            r = httprequestObj.http_post('https://www.residences.in.th/dynamic_amphurs/' + province_id,
                                         data={province_id: ''})
            print(r.url)
            print(r.status_code)

            data = r.text.split('\n')[2:-2]

            district_id = data[0].split('value\",')[1].split(')')[0]

            for row in data:
                area = row.split('text(\'')[1].split('\'')[0]
                id = row.split('value\",')[1].split(')')[0].strip()
                # print(area)
                # print(id)
                if area.replace(' ', '') in postdata['addr_district'].replace(' ', '') or postdata[
                    'addr_district'].replace(' ', '') in area.replace(' ', ''):
                    district_id = id
                    break

            print('District id = ' + district_id)

            r = httprequestObj.http_post('https://www.residences.in.th/dynamic_districts/' + district_id,
                                         data={district_id: ''})
            print(r.url)
            print(r.status_code)

            data = r.text.split('\n')[3:-2]

            # print(data)

            sub_district_id = data[0].split('value\",')[1].split(')')[0]

            for row in data:
                area = row.split('text(\'')[1].split('\'')[0]
                id = row.split('value\",')[1].split(')')[0].strip()
                # print(area)
                # print(id)
                if area.replace(' ', '') in postdata['addr_sub_district'].replace(' ', '') or postdata[
                    'addr_sub_district'].replace(' ', '') in area.replace(' ', ''):
                    sub_district_id = id
                    break

            print('Subdistrict id = ' + sub_district_id)

            g = lib_captcha.reCaptcha('6LfAohcUAAAAAAnZ86DXS9_JzyGlIqyxEXTAUQMz',
                                      'https://www.residences.in.th/apartments/new')
            print(g)

            datapost = [
                ('utf8', '✓'),
                ('authenticity_token', auth_token),
                ('apartment[name]', postdata['post_title_th']),
                ('apartment[en_name]', postdata['post_title_th']),
                ('apartment[apartment_type]', '0'),
                ('apartment[province_id]', province_id),
                ('apartment[amphur_id]', district_id),
                ('apartment[district_id]', sub_district_id),
                ('ignore_reverse_district_id', '0'),
                ('apartment[postcode]', '10400'),
                ('apartment[address]', '11'),
                ('apartment[road]', postdata['addr_road']),
                ('apartment[street]', postdata['addr_soi']),
                ('apartment[latitude]', postdata['geo_latitude']),
                ('apartment[longitude]', postdata['geo_longitude']),
                ('apartment[gmaps_zoom]', ''),
                ('apartment[staff]', postdata['name']),
                ('apartment[telephone]', postdata['mobile']),
                ('apartment[en_telephone]', ''),
                ('apartment[email]', postdata['email']),
                ('apartment[line_user_id]', postdata['line']),
                ('apartment[facebook_url]', ''),
                ('apartment[description]', postdata['post_description_th'].replace('\r\n', '<br>')),
                ('_wysihtml5_mode', '1'),
                ('_wysihtml5_mode', '1'),
                ('apartment[en_description]', ''),
                ('apartment[create_level]', '1'),
                ('ref_action', 'new'),
                ('g-recaptcha-response', g)
            ]

            r = httprequestObj.http_post('https://www.residences.in.th/apartments', data=datapost)
            print(r.url)
            print(r.status_code)

            with open('/home/aymaan/Desktop/rough.html', 'w') as f:
                f.write(r.text)

            print('First part done')

            second_url = r.url

            r = httprequestObj.http_get(second_url)
            print(r.url)
            print(r.status_code)

            soup = BeautifulSoup(r.content, self.parser)
            utf8 = soup.find('input', {'name': 'utf8'}).get('value')
            method = soup.find('input', {'name': '_method'}).get('value')
            auth_token = soup.find('input', {'name': 'authenticity_token'}).get('value')
            apartment_fi = soup.find('input', {'name': 'apartment[facility_ids][]'}).get('value')
            apartment_cfi = soup.find('input', {'name': 'apartment[central_facility_ids][]'}).get('value')
            dnvaf = soup.find('input', {'name': 'do_not_validation_all_facility'}).get('value')
            dnvli = soup.find('input', {'name': 'do_not_validation_listing_images'}).get('value')
            apartment_cl = soup.find('input', {'name': 'apartment[create_level]'}).get('value')
            ref_action = soup.find('input', {'name': 'ref_action'}).get('value')


            # postdata['post_images'] = []

            for i, img in enumerate(postdata['post_images']):
                filename = str(i) + '.jpeg'
                datapost = [
                    ('utf8', (None, utf8)),
                    ('_method', (None, method)),
                    ('authenticity_token', (None, auth_token)),
                    ('apartment[facility_ids][]', (None, apartment_fi)),
                    ('apartment[central_facility_ids][]', (None, apartment_cfi)),
                    ('do_not_validation_all_facility', (None, dnvaf)),
                    ('do_not_validation_listing_images', (None, dnvli)),
                    ('apartment[create_level]', (None, apartment_cl)),
                    ('ref_action', (None, ref_action)),
                    ('apartment[images_attributes][][attachment]', (filename, open(img, 'rb'), 'image/jpeg')),
                ]
                # print(second_url[:-10])
                # print(httprequestObj)
                # print(auth_token)
                r = httprequestObj.http_post(second_url[:-10], data={}, files=datapost)
                # print(r)
                print(r.url)
                print(r.status_code)
                print(r.text)

                r = httprequestObj.http_get(second_url)
                print(r.url)
                print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                utf8 = soup.find('input', {'name': 'utf8'}).get('value')
                method = soup.find('input', {'name': '_method'}).get('value')
                auth_token = soup.find('input', {'name': 'authenticity_token'}).get('value')
                apartment_fi = soup.find('input', {'name': 'apartment[facility_ids][]'}).get('value')
                apartment_cfi = soup.find('input', {'name': 'apartment[central_facility_ids][]'}).get('value')
                dnvaf = soup.find('input', {'name': 'do_not_validation_all_facility'}).get('value')
                dnvli = soup.find('input', {'name': 'do_not_validation_listing_images'}).get('value')
                apartment_cl = soup.find('input', {'name': 'apartment[create_level]'}).get('value')
                ref_action = soup.find('input', {'name': 'ref_action'}).get('value')

            print(auth_token)
            print(apartment_cl)
            print(ref_action)

            datapost = [
                ('utf8', utf8),
                ('_method', method),
                ('authenticity_token', auth_token),
                ('apartment[facility_ids][]', apartment_fi),
                ('apartment[central_facility_ids][]', ''),
                ('apartment[facility_ids][]', '5'),
                ('do_not_validation_all_facility', '0'),
                ('do_not_validation_listing_images', dnvli),
                ('apartment[create_level]', apartment_cl),
                ('ref_action', ref_action)
            ]

            r = httprequestObj.http_post(second_url[:-10], data=datapost)
            print(r.url)
            print(r.status_code)

            # with open('/home/codelover/Desktop/rough.html', 'w') as f:
            #     f.write(r.text)

            print('Second part done')

            third_url = r.url + '/roomtypes'
            r = httprequestObj.http_get(third_url)
            print(r.url)
            print(r.status_code)

            # with open('/home/codelover/Desktop/rough.html', 'w') as f:
            #     f.write(r.text)

            soup = BeautifulSoup(r.content, self.parser)
            utf8 = soup.find('input', {'name': 'utf8'}).get('value')
            method = soup.find('input', {'name': '_method'}).get('value')
            auth_token = soup.find('input', {'name': 'authenticity_token'}).get('value')

            # sp_id = soup.find('td', 'col-md-3 room-name-column').find('input').get('id').split('_')[-2]
            # print(sp_id)
            sp_id = '0'

            datapost = [
                ('utf8', utf8),
                ('_method', method),
                ('authenticity_token', auth_token),
                ('apartment[rooms_attributes]['+sp_id+'][name]', 'bedroom'),
                ('apartment[rooms_attributes]['+sp_id+'][room_type]', 'R2'),
                ('apartment[rooms_attributes]['+sp_id+'][size]', '11'),
                ('apartment[rooms_attributes]['+sp_id+'][monthly]', '0'),
                ('apartment[rooms_attributes]['+sp_id+'][monthly]', '1'),
                ('apartment[rooms_attributes]['+sp_id+'][min_price_permonth]', '100'),
                ('apartment[rooms_attributes]['+sp_id+'][max_price_permonth]', '200'),
                ('apartment[rooms_attributes]['+sp_id+'][daily]', '0'),
                ('apartment[rooms_attributes]['+sp_id+'][daily]', '1'),
                ('apartment[rooms_attributes]['+sp_id+'][min_price_perday]', '100'),
                ('apartment[rooms_attributes]['+sp_id+'][max_price_perday]', '200'),
                ('apartment[rooms_attributes]['+sp_id+'][available]', '0'),
                ('apartment[rooms_attributes]['+sp_id+'][available]', '1'),
                ('apartment[rooms_attributes]['+sp_id+'][_destroy]', 'false'),
                ('apartment[water_price]', ''),
                ('apartment[water_price_monthly_per_person]', ''),
                ('apartment[water_price_monthly_per_room]', ''),
                ('apartment[water_price_remark]', ''),
                ('apartment[water_price_type]', '5'),
                ('apartment[water_price_note]', ''),
                ('apartment[electric_price]', ''),
                ('apartment[electric_price_remark]', ''),
                ('apartment[electric_price_type]', '3'),
                ('apartment[electric_price_note]', ''),
                ('apartment[deposit_month]', ''),
                ('apartment[deposit_type]', '2'),
                ('apartment[deposit_bath]', postdata['price_baht']),
                ('apartment[deposit]', ''),
                ('apartment[advance_fee_month]', ''),
                ('apartment[advance_fee_bath]', ''),
                ('apartment[advance_fee_type]', '3'),
                ('apartment[advance_fee]', ''),
                ('apartment[phone_price_minute]', ''),
                ('apartment[phone_price_minute_unit]', ''),
                ('apartment[phone_price_per_time]', ''),
                ('apartment[phone_price_type]', '3'),
                ('apartment[phone_price]', ''),
                ('apartment[internet_price_bath]', ''),
                ('apartment[internet_price_unit]', ''),
                ('apartment[internet_price_type]', '2'),
                ('apartment[internet_price]', ''),
                ('apartment[has_promotion]', '0'),
                ('apartment[promotion_start]', ''),
                ('apartment[promotion_end]', ''),
                ('apartment[promotion_description]', ''),
                ('_wysihtml5_mode', '1'),
                ('apartment[create_level]', '3'),
                ('ref_action', 'roomtypes'),
            ]

            r = httprequestObj.http_post(third_url[:-10], data=datapost)
            print(r.url)
            print(r.status_code)

            url = 'https://www.residences.in.th/dashboard/apartments'
            r = httprequestObj.http_get(url)
            print(r.url)
            print(r.status_code)

            url = third_url[:-10] + '/edit'
            r = httprequestObj.http_get(url)
            print(r.url)
            print(r.status_code)

            url = third_url[:-10] + '/information'
            r = httprequestObj.http_get(url)
            print(r.url)
            print(r.status_code)

            r = httprequestObj.http_get(third_url)
            print(r.url)
            print(r.status_code)

            soup = BeautifulSoup(r.content, self.parser)
            room_id = soup.find('tbody').find('tr').get('id').split('_')[-1]
            print(room_id)

            soup = BeautifulSoup(r.content, self.parser)
            utf8 = soup.find('input', {'name': 'utf8'}).get('value')
            method = soup.find('input', {'name': '_method'}).get('value')
            auth_token = soup.find('input', {'name': 'authenticity_token'}).get('value')

            datapost = [
                ('utf8', '✓'),
                ('_method', 'put'),
                ('authenticity_token', auth_token),
                ('apartment[rooms_attributes][' + sp_id + '][name]', 'bedroom'),
                ('apartment[rooms_attributes][' + sp_id + '][room_type]', 'R2'),
                ('apartment[rooms_attributes][' + sp_id + '][size]', '11'),
                ('apartment[rooms_attributes][' + sp_id + '][monthly]', '0'),
                ('apartment[rooms_attributes][' + sp_id + '][monthly]', '1'),
                ('apartment[rooms_attributes][' + sp_id + '][min_price_permonth]', '100'),
                ('apartment[rooms_attributes][' + sp_id + '][max_price_permonth]', '200'),
                ('apartment[rooms_attributes][' + sp_id + '][daily]', '0'),
                ('apartment[rooms_attributes][' + sp_id + '][daily]', '1'),
                ('apartment[rooms_attributes][' + sp_id + '][min_price_perday]', '100'),
                ('apartment[rooms_attributes][' + sp_id + '][max_price_perday]', '200'),
                ('apartment[rooms_attributes][' + sp_id + '][available]', '0'),
                ('apartment[rooms_attributes][' + sp_id + '][available]', '1'),
                ('apartment[rooms_attributes][' + sp_id + '][_destroy]', 'false'),
                ('apartment[rooms_attributes][' + sp_id + '][id]', room_id),
                ('apartment[water_price]', ''),
                ('apartment[water_price_monthly_per_person]', ''),
                ('apartment[water_price_monthly_per_room]', ''),
                ('apartment[water_price_remark]', ''),
                ('apartment[water_price_type]', '5'),
                ('apartment[water_price_note]', ''),
                ('apartment[electric_price]', ''),
                ('apartment[electric_price_remark]', ''),
                ('apartment[electric_price_type]', '3'),
                ('apartment[electric_price_note]', ''),
                ('apartment[deposit_month]', ''),
                ('apartment[deposit_type]', '2'),
                ('apartment[deposit_bath]', postdata['price_baht']),
                ('apartment[deposit]', ''),
                ('apartment[advance_fee_month]', ''),
                ('apartment[advance_fee_bath]', ''),
                ('apartment[advance_fee_type]', '3'),
                ('apartment[advance_fee]', ''),
                ('apartment[phone_price_minute]', ''),
                ('apartment[phone_price_minute_unit]', ''),
                ('apartment[phone_price_per_time]', ''),
                ('apartment[phone_price_type]', '3'),
                ('apartment[phone_price]', ''),
                ('apartment[internet_price_bath]', ''),
                ('apartment[internet_price_unit]', ''),
                ('apartment[internet_price_type]', '2'),
                ('apartment[internet_price]', ''),
                ('apartment[has_promotion]', '0'),
                ('apartment[promotion_start]', ''),
                ('apartment[promotion_end]', ''),
                ('apartment[promotion_description]', ''),
                ('_wysihtml5_mode', '1'),
                ('apartment[create_level]', '4'),
                ('ref_action', 'roomtypes'),
            ]

            r = httprequestObj.http_post(third_url[:-10], data=datapost)
            print(r.url)
            print(r.status_code)

            # with open('/home/codelover/Desktop/rough.html', 'w') as f:
            #     f.write(r.text)

            print('Third part done')

            fourth_url = r.url + '/verify'
            r = httprequestObj.http_get(fourth_url)
            print(r.url)
            print(r.status_code)

            #with open('/home/codelover/Desktop/rough.html', 'w') as f:
            #    f.write(r.text)

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
