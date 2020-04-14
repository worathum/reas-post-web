# -*- coding: utf-8 -*-
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
import os
from .lib_httprequest import *
import string
from bs4 import BeautifulSoup
import os.path
# from urlparse import urlparse
import re
import json
import datetime
import time
import sys
import shutil
from urllib.parse import unquote


httprequestObj = lib_httprequest()


# with open("./static/ploychao_province.json") as f:
#     provincedata = json.load(f)


class ddteedin():

    name = 'ddteedin'

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

    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']
        name_th = postdata["name_th"]
        surname_th = postdata["surname_th"]
        mobile_no = postdata["tel"]
        # start process
        success = "true"
        detail = ""

        datapost = dict(
            email=user,
            password=passwd,
            password2=passwd,
            firstname=name_th,
            lastname=surname_th,
            mobile=mobile_no,
            action='save_register',
        )
        r = httprequestObj.http_post(
            'https://www.ddteedin.com/register/', data=datapost)
        # print("yes")
        data = r.text
        if r.status_code == 404:
            detail = "Can't register"
            success = "false"
        else:
            detail = "Registered"
        # # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "website_name": "ddteedin",
            "detail": detail,
        }

    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']

        success = "true"
        detail = ""

        datapost = {
            'action': 'login',
            'log_u': user,
            'log_p': passwd,
            'login': 'Login'
        }

        r = httprequestObj.http_post(
            'https://www.ddteedin.com/login/', data=datapost)
        data = r.text
        # print(r.text)
        if data.find("ไม่ถูกต้องกรุณาตรวจสอบ") != -1:
            detail = "cannot login"
            success = "false"
        else:
            detail = "login successfull"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "website_name": "ddteedin",
            "detail": detail,
        }

    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        theurl = ""
        post_id = ""

        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        ashopname = test_login["detail"]

        getProdId = {'1': 24, '2': 25, '3': 26, '4': 27, '5': 29,
                     '6': 34, '7': 28, '8': 14, '9': 31, '10': 33}
        theprodid = getProdId[postdata['property_type']]
        # theprodid = post
        # for (key, value) in provincedata.items():
        #     if type(value) is str and postdata['addr_province'].strip() in value.strip():
        #         province_id = key
        #         break

        # for (key, value) in provincedata[province_id+"_province"].items():
        #     if postdata['addr_district'].strip() in value.strip():
        #         amphur_id = key
        #         break
        province_id = '10'
        amphur_id = '26'
        prod_address = ""
        for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
            if add is not None:
                prod_address += add
        prod_address = prod_address[:-1]

        if success == "true":
            r = httprequestObj.http_get(
                'http://www.ddteedin.com/post-land-for-sale/?rf=mypost', verify=False)

            data = r.text
            soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
            cverify = soup.find("input", {"name": "cverify"})['value']
            tumbon_id = '01'
            # print("cverify =",cverify)
            datapost = [
                ('action', 'create_post'),
                ('timeout', '5'),
                ('name', postdata['post_title_th']),
                ('code', theprodid),
                ('forid', '3'),
                ('typeid', '2'),
                ('isnew', '1'),
                ('project', postdata['project_name']),
                ('rooms', ''),
                ('bathroom', ''),
                ('floor', ''),
                ('usagesize', ''),
                ('sizerai', postdata['land_size_rai']),
                ('sizewa2', postdata['land_size_wa']),
                ('price', ''),
                ('province', province_id),
                ('amphur', province_id+""+amphur_id),
                ('tumbon', province_id+""+amphur_id+""+tumbon_id),
                ('detail', postdata['post_description_th']),
                ('warning', ""),
                ('lat', postdata['geo_latitude']),
                ('lng', postdata['geo_longitude']),
                ('opts[]', ''),
                ('cverify', cverify)
            ]
            files = {}
            for i in range(len(postdata["post_img_url_lists"])):
                resp = requests.get(
                    postdata["post_img_url_lists"][i], stream=True)
                resp.raw.decode_content = True
                with open('image'+str(i)+'.jpg', 'wb') as lfile:
                    shutil.copyfileobj(resp.raw, lfile)

                r = open('image'+str(i)+'.jpg', 'rb')
                print(r)
                if i > 20:
                    break
                if i == 0:
                    files['fileshow'] = r
                else:
                    files["file"+str(i)] = r
                datapost.append(('file[]', postdata["post_img_url_lists"][i]))
                # datapost['file[]'] = i
                r = httprequestObj.http_post(
                    'https://www.ddteedin.com/upload', datapost)

            r = httprequestObj.http_post(
                'https://www.ddteedin.com/post-land-for-sale/?rf=mypost', data=datapost, files=files)
            # print(r.text)
            query_element = {
                'q': postdata['name'],
                'pv': '',
                'order': 'createdate',
                'btn_srch': 'search'
            }
            query_string = 'https://www.ddteedin.com/myposts/?q='+query_element['q'].replace(' ', '+')+'&pv='+query_element['pv'].replace(
                ' ', '+')+'&order='+query_element['order'].replace(' ', '+')+"&btn_srch="+query_element['btn_srch'].replace(' ', '+')
            r = httprequestObj.http_get(
                query_string, verify=False)
            data = r.text
            soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
            id = soup.find("div", {"class": "it st1"})['id']
            id = id.replace('r', '')
            post_id += id
            # print(r.text)
            # print(r.status_code)
        else:
            success = "false"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "website_name": "ddteedin",
            "post_url": 'https://www.ddteedin.com/post-land-for-sale/?rf=mypost',
            "post_id": id,
            "account_type": "null",
        }

    def edit_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        theurl = ""
        post_id = ""

        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        ashopname = test_login["detail"]

        getProdId = {'1': 24, '2': 25, '3': 26, '4': 27, '5': 29,
                     '6': 34, '7': 28, '8': 14, '9': 31, '10': 33}
        theprodid = getProdId[postdata['property_type']]

        # for (key, value) in provincedata.items():
        #     if type(value) is str and postdata['addr_province'].strip() in value.strip():
        #         province_id = key
        #         break

        # for (key, value) in provincedata[province_id+"_province"].items():
        #     if postdata['addr_district'].strip() in value.strip():
        #         amphur_id = key
        #         break
        province_id = '10'
        amphur_id = '26'
        prod_address = ""
        for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
            if add is not None:
                prod_address += add
        prod_address = prod_address[:-1]

        if success == "true":
            tumbon_id = '01'
            # query_element = {
            #     'q': postdata['name'],
            #     'pv': '',
            #     'order': 'createdate',
            #     'btn_srch': 'search'
            # }
            # query_string = 'https://www.ddteedin.com/myposts/?q='+query_element['q'].replace(' ', '+')+'&pv='+query_element['pv'].replace(
            #     ' ', '+')+'&order='+query_element['order'].replace(' ', '+')+"&btn_srch="+query_element['btn_srch'].replace(' ', '+')
            # r = httprequestObj.http_get(
            #     query_string, verify=False)
            # data = r.text
            # soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
            # id = soup.find("div", {"class": "it st1"})['id']
            # id = id.replace('r', '')
            # # print(id)
            id = postdata['post_id']
            post_id += id
            query_element = {
                'q': postdata['post_id'],
                'pv': '',
                'order': 'createdate',
                'btn_srch': 'search'
            }
            query_string = 'https://www.ddteedin.com/myposts/?q='+query_element['q'].replace(' ', '+')+'&pv='+query_element['pv'].replace(
                ' ', '+')+'&order='+query_element['order'].replace(' ', '+')+"&btn_srch="+query_element['btn_srch'].replace(' ', '+')
            r = httprequestObj.http_get(
                query_string, verify=False)
            data = r.text
            query_string = 'https://www.ddteedin.com/post-land-for-sale/edit/'+id
            if data.find(" ไม่พบประกาศ") != -1:
                success = False
            else:
                r = httprequestObj.http_get(query_string, verify=False)
                data = r.text
                soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
                cverify = soup.find("input", {"name": "cverify"})['value']
                # print(cverify)
                datapost = [
                    ('action', 'create_post'),
                    ('timeout', '5'),
                    ('name', postdata['post_title_th']),
                    ('code', theprodid),
                    ('forid', '3'),
                    ('typeid', '2'),
                    ('isnew', '1'),
                    ('project', postdata['project_name']),
                    ('rooms', ''),
                    ('bathroom', ''),
                    ('floor', ''),
                    ('usagesize', ''),
                    ('sizerai', postdata['land_size_rai']),
                    ('sizewa2', postdata['land_size_wa']),
                    ('price', ''),
                    ('province', province_id),
                    ('amphur', province_id+""+amphur_id),
                    ('tumbon', province_id+""+amphur_id+""+tumbon_id),
                    ('detail', postdata['post_description_th']),
                    ('warning', ""),
                    ('lat', postdata['geo_latitude']),
                    ('lng', postdata['geo_longitude']),
                    ('opts[]', ''),
                    ('cverify', cverify)
                ]
                files = {}
                for i in range(len(postdata["post_img_url_lists"])):
                    resp = requests.get(
                        postdata["post_img_url_lists"][i], stream=True)
                    resp.raw.decode_content = True
                    with open('image'+str(i)+'.jpg', 'wb') as lfile:
                        shutil.copyfileobj(resp.raw, lfile)

                    r = open('image'+str(i)+'.jpg', 'rb')
                    print(r)
                    if i > 20:
                        break
                    if i == 0:
                        files['fileshow'] = r
                    else:
                        files["file"+str(i)] = r
                    datapost.append(('file[]', postdata["post_img_url_lists"][i]))
                    # datapost['file[]'] = i
                    r = httprequestObj.http_post(
                        'https://www.ddteedin.com/upload', datapost)

                r = httprequestObj.http_post(
                    query_string, data=datapost, files=files)

            # print(r.text)
        else:
            success = "false"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "website_name": "ddteedin",
            "post_url": query_string,
            "post_id": id,
            "account_type": "null",
        }

    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        theurl = ""
        post_id = ""

        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        ashopname = test_login["detail"]
        # print(ashopname)
        # for (key, value) in provincedata.items():
        #     if type(value) is str and postdata['addr_province'].strip() in value.strip():
        #         province_id = key
        #         break

        # for (key, value) in provincedata[province_id+"_province"].items():
        #     if postdata['addr_district'].strip() in value.strip():
        #         amphur_id = key
        #         break
        if success == "true":
            tumbon_id = '01'
            r = httprequestObj.http_get(
                'https://www.ddteedin.com/myposts/?rf=login', verify=False)
            data = r.text
            soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
            alls = soup.findAll('script')
            id1 = ""
            i = 0
            for x in alls:
                if i == 3:
                    id1 = id1 + (str(x))
                i += 1
            id1 = re.sub("[^0-9]", "", id1)
            print(id1)
            query_element = {
                'q': postdata['post_id'],
                'pv': '',
                'order': 'createdate',
                'btn_srch': 'search'
            }
            query_string = 'https://www.ddteedin.com/myposts/?q='+query_element['q'].replace(' ', '+')+'&pv='+query_element['pv'].replace(
                ' ', '+')+'&order='+query_element['order'].replace(' ', '+')+"&btn_srch="+query_element['btn_srch'].replace(' ', '+')
            r = httprequestObj.http_get(
                query_string, verify=False)
            data = r.text
            id = postdata['post_id']
            query_string = 'https://www.ddteedin.com/myposts/'+id1
            # print(r.text)
            if data.find(" ไม่พบประกาศ") != -1:
                success = False
            else:
            # soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
            # id = soup.find("div", {"class": "it st1"})['id']
            # id = id.replace('r', '')
            # print(id)
                # id1 = postdata['log_id']
                # query_element['q'] = ''
                datapost = {
                    'id': id,
                    'act': 'del'
                }
                r = httprequestObj.http_post(query_string, data=datapost)
                print(r.text)
            # print(r.text)
            # print(r.status_code)
        else:
            success = "false"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "website_name": "ddteedin",
            "post_url": query_string,
            "post_id": id,
            "account_type": "null",
        }

    def print_debug(self, msg):
        if(self.debug == 1):
            print(msg)
        return True

    def print_debug_data(self, data):
        if(self.debugdata == 1):
            print(data)
        return True

        if(self.debugdata == 1):
            print(data)
        return True


# a = ddteedin()
# credentials = {
#     "action": "register_user",
#     "timeout": "7",
#     "web": [
#         {
#             "ds_name": "ddteedin",
#             "ds_id": "4",
#             "user": "amarin.ta@gmail.com",
#             "pass": "5k4kk3253434",
#             "company_name": "amarin inc",
#             "name_title": "mr",
#             "name_th": "อัมรินทร์",
#             "surname_th": "บุญเกิด",
#             "name_en": "Amarin",
#             "surname_en": "Boonkirt",
#             "tel": "0891999450",
#             "line": "amarin.ta",
#             "addr_province" : "nonthaburi"
#         }
#     ]
# }

# credentials = {
#     "geo_latitude": "13.786862",
#     "geo_longitude": "100.757815",
#     "property_id": "4",
#     "forid": "3",
#     "typeid": "2",
#     "isnew": "1",
#     "post_title_th": "xxx",
#     "short_post_title_th": "xxx",
#     "post_description_th": "xxx",
#     "post_title_en": "",
#     "short_post_title_en": "xxx",
#     "post_description_en": "",
#     "price_baht": "3000",
#     "listing_type": "ขาย",
#     "property_type": "คอนโด",
#     "floor_level  ": "11",
#     "floor_total  ": "11",
#     "floor_area  ": "11",
#     "bath_room  ": "11",
#     "bed_room  ": "11",
#     "prominent_point  ": "จุดเด่น",
#     "view_type ": "11",
#     "direction_type": "11",
#     "addr_province": "จังหวัด",
#     "addr_district": "เขต",
#     "addr_sub_district": "ตำบล แขวง",
#     "addr_road": "ถนน",
#     "addr_soi": "ซอย",
#     "addr_near_by": "สถานที่ใกล้เคียง",
#     "floorarea_sqm": "พื้นที่",
#     "price": "1234",
#     "product_details": "jslkfdklfjdfkldfjdflkdfjdflksjfklhgdfoewitogjdfjdlskfdsjfdklfgjfklgdhfdslkfdhfdlfhewioffhdlkghfdlkfdskjfdlkgjhglkdsfhlgdshkfefhioglshg",
#     "options": {},
#     "land_size_rai": "ขนาดที่ดินเป็นไร่",
#     "land_size_ngan": "ขนาดที่ดินเป็นงาน",
#     "land_size_wa": "ขนาดที่ดินเป็นวา",
#     "name": "land on rent",
#     "mobile": "9876543210",
#     "email": "ramu@gmail.com",
#     "line": "xxx",
#     "project_name": "ลุมพีนีวิลล รามอินทราหลักสี่",
#     "user": "ramu@gmail.com",
#     "pass": "raam1234"
# }
# ret = a.create_post(credentials)
# print(ret)
# login_credentials = {
#     "user":"reteh37681@fft-mail.com",
#     "pass":'12345678',
# }
# ret = a.test_login(login_credentials)
# # print(ret)
# postdata = {
#     "action": "edit_post", "timeout": "5", "project_name": "ลุมพีนีวิลล", "post_img_url_lists": ["https://zignnet.sgp1.digitaloceanspaces.com/livingjoin/classified/189689/big/210120235215500991.jpg", "https://zignnet.sgp1.digitaloceanspaces.com/livingjoin/classified/189689/other/big/210120235220317918.jpg"], "geo_latitude": "13.786862", "geo_longitude": "100.757815", "property_id": "chu001", "post_title_th": "new edited ให้เช่า ที่ดินด่วน บางกรวยไทรน้อย 6 ไร่ เหมาะทำตลาด", "post_description_th": "What is description", "post_title_en": "Land for rent bangkloysainoi 6 rai suitable for developing", "post_description_en": "Land for rent bangkloysainoi 6 rai suita ble for developing", "price_baht": "100000", "listing_type": "เช่า", "property_type": "6", "prominent_point ": "หน้ากว้างมาก ให้เช่าถูกสุด", "direction_type": "11", "addr_province": "นนทบุรี", "addr_district": "เมืองนนทบุรี", "addr_sub_district": "บางกรวย", "addr_road": "บางกรวย-ไทรน้อย", "addr_soi": "ซอยบางกรวย-ไทรน้อย 34", "addr_near_by": "ถนนพระราม5\nถนนนครอินทร์", "land_size_rai": "6", "land_size_ngan": "0", "land_size_wa": "0", "name": "ชู", "mobile": "0992899999", "email": "panuwat.ruangrak@gmail.com", "line": "0992899999", "ds_name": "ddteedin", "ds_id": "120", "user": "reteh37681@fft-mail.com", "pass": "12345678", "post_id": "484916", "log_id": "48791", "account_type": "corperate"
# }
# # a = ddteedin()
# # ret = a.edit_post(postdata)
# # print(ret)
# email = "reteh37681@fft-mail.com"
# site = "ddteedin.com"
# thedata = { "action": "create_post", "timeout": "5", "project_name": "ลุมพีนีวิลล รามอินทราหลักสี", "post_img_url_lists": [ "https://zignnet.sgp1.digitaloceanspaces.com/livingjoin/classified/189689/big/210120235215500991.jpg", "https://zignnet.sgp1.digitaloceanspaces.com/livingjoin/classified/189689/other/big/210120235220317918.jpg" ], "geo_latitude": "13.786862", "geo_longitude": "100.757815", "property_id" : "chu001", "post_title_th": "ให้เช่า ที่ดินด่วน บางกรวยไทรน้อย 6 ไร่ เหมาะทำตลาดสด เปิดท้าย", "post_description_th": "ขายที่ดินด่วน บางกรวยไทรน้อย 6 ไร่ เหมาะทำตลาด\r\nรายละเอียด\r\nที่ดิน\r\nขนาด 6 ไร่\r\nหน้ากว้าง 30 เมตร ติดถนนบางกรวยไทรน้อย\r\nที่ดินยังไม่ถมต่ำกว่าถนนประมาณ 1 เมตร\r\n\r\nสถานที่ใกล้เคียง\r\nถนนพระราม5\r\nถนนนครอินทร์\r\n\r\nให้เช่าระยะยาว 100,000 บาท ต่อเดือน\r\n\r\nสนใจติดต่อ คุณชู 0992899999\r\nline: 0992899999", "post_title_en": "Land for rent bangkloysainoi 6 rai suitable for developing", "post_description_en": "Land for rent bangkloysainoi 6 rai suitable for developing\r\nLand Size 6 rai\r\nWidth 30 meter", "price_baht": "100000", "listing_type": "เช่า", "property_type": "6", "prominent_point " : "หน้ากว้างมาก ให้เช่าถูกสุด", "direction_type" : "11", "addr_province": "นนทบุรี", "addr_district": "เมืองนนทบุรี", "addr_sub_district": "บางกรวย", "addr_road": "บางกรวย-ไทรน้อย", "addr_soi": "ซอยบางกรวย-ไทรน้อย 34", "addr_near_by": "ถนนพระราม5\r\nถนนนครอินทร์", "land_size_rai": "6", "land_size_ngan": "0", "land_size_wa": "0", "name": "jdlkf", "mobile": "0992899999", "email": email, "line": "0992899999","ds_name": site, "ds_id": "120", "user": email, "pass": "12345678"}
# # a = ddteedin()
# # ret = a.create_post(thedata)
# # print(ret)
