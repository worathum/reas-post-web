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


class livinginsider():
    name = 'livinginsider'

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
        self.webname = 'livinginsider'

    def register_user(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']
        username = user.replace("@","").replace(".","")
        success = "true"
        detail = ""
        username = user.split('@')

        datapost = {
            "email": user,
            "password": passwd,
            "repassword": passwd,
            "username": username,
            "mem_tel": postdata['tel']
        }
        # print(datapost)
        r = httprequestObj.http_post('https://www.livinginsider.com/member_create.php', data=datapost)
        data = json.loads(r.text)
        # print(data)
        if data['error_field'] != '':
            success = False
            detail = data['result_msg']
        else:
            success = True
            detail = 'Registered successfully'

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": self.webname,
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            'ds_id': postdata['ds_id'],
            "detail": detail,
        }

    def test_login(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']
        success = "true"
        detail = "logged in"

        datapost = {
            'password': passwd,
            'username': user,

        }
        r = httprequestObj.http_post(
            'https://www.livinginsider.com/login.php', data=datapost)
        # print(r.url)
        # print(r.status_code)
        data = json.loads(r.text)
        # print(data)
        if data['status']:
            success = True
            detail = 'Login successful'
        else:
            success = False
            detail = 'Couldnot login'

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": self.webname,
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "ds_id": postdata['ds_id'],
            "end_time": str(time_end),
            "detail": detail,
        }

    def create_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""

        proid = {
            'คอนโด': '1',  # condo
            'บ้านเดี่ยว': '2',  # detached houses /home / house / Single House
            'บ้านแฝด': '3',  # twin houses
            'ทาวน์เฮ้าส์': '4',  # townhouses / town home / home office
            'ตึกแถว-อาคารพาณิชย์': '5',  # commercial buildings
            'ที่ดิน': '6',  # land
            'อพาร์ทเมนท์': '7',  # apartments
            'โรงแรม': '8',  # hotels, Real Estate Residencial
            'ออฟฟิศสำนักงาน': '9',  # Office
            'โกดัง-โรงงาน': '10',  # warehouses
            'โรงงาน': '25'  # factory
        }
        getProdId = {'1': 1, '2': 2, '3': 2, '4': 6,
                     '5': 4, '6': 3, '7': 10, '8': 10, '9': 5, '10': 12, '25': 11}

        try:
            theprodid = getProdId[proid[postdata['property_type']]]
        except:
            theprodid = getProdId[postdata['property_type']]

        if 'web_project_name' not in postdata or postdata['web_project_name'] is not None:
            if 'project_name' in postdata and postdata['project_name'] is not None:
                postdata['web_project_name'] = postdata['project_name']
            else:
                postdata['web_project_name'] = postdata['post_title_th']

        if 'floor_total' not in postdata:
            postdata['floor_total'] = 1
        elif postdata['floor_total'] is None or postdata['floor_total'] == '':
            postdata['floor_total'] = 1

        if 'floor_level' not in postdata:
            postdata['floor_level'] = 1
        elif postdata['floor_level'] is None or postdata['floor_level'] == '':
            postdata['floor_level'] = 1

        if 'bath_room' not in postdata:
            postdata['bath_room'] = 1
        elif postdata['bath_room'] is None or postdata['bath_room'] == '':
            postdata['bath_room'] = 1

        if 'bed_room' not in postdata:
            postdata['bed_room'] = 1
        elif postdata['bed_room'] == None or postdata['bed_room'] == '':
            postdata['bed_room'] = 1

        if int(postdata['bed_room']) > 10:
            postdata['bed_room'] = 11

        if int(postdata['bath_room']) > 5:
            postdata['bath_room'] = 6

        if postdata['land_size_rai'] == None:
            land_size_rai = 0
        else:
            land_size_rai = postdata['land_size_rai']

        if postdata['land_size_ngan'] == None:
            land_size_ngan = 0
        else:
            land_size_ngan = postdata['land_size_ngan']

        if postdata['land_size_wa'] == None:
            land_size_wa = 0
        else:
            land_size_wa = postdata['land_size_wa']

        province_id = ''
        term = postdata['web_project_name'].replace(' ', '+')

        data = requests.get(
            'https://www.livinginsider.com/a_project_list_json.php?term=' + term + '&_type=query&q=' + term)
        data = json.loads(data.text)

        if len(data) == 1:
            term = postdata['addr_district'] + '+' + postdata['addr_province']
            data = requests.get(
                'https://www.livinginsider.com/a_project_list_json.php?term=' + term + '&_type=query&q=' + term)
            data = json.loads(data.text)

            # print(data)
            try:
                idzone = data[1]['id']
            except:
                idzone = data[0]['id']
        else:
            idzone = data[1]['id']
        # print(idzone)
        data = requests.post('https://www.livinginsider.com/a_project_child.php', data={'web_project_id': idzone})
        # print(data.status_code)
        data = json.loads(data.text)
        # print(data)
        r = data['value']
        if len(r) == 0:
            params = {
                'term': postdata['addr_province'],
                '_type': 'query',
                'q': postdata['addr_province']
            }
            r = requests.get('https://www.livinginsider.com/a_zone_list.php', params=params)
            # print(r.url)
            # print(r.status_code)
            data = r.json()
            web_zone = data[0]['id']
            for row in data:
                if postdata['addr_district'].replace(' ', '') in row and postdata['addr_sub_district'].replace(' ',
                                                                                                               '') in row:
                    web_zone = row['id']
                    break
            # print('Web_zone = ' + str(web_zone))

            r = requests.post('https://www.livinginsider.com/a_zone_child.php', data={'web_zone_id': web_zone})
            # print(r.url)
            # print(r.status_code)
            # print(r.json())

        else:
            soap = BeautifulSoup(r, self.parser)
            option = soap.find('option')
            web_zone = option.get('value')
            # print('Web_zone = ' + str(web_zone))
            # print(option)
        prod_address = ""
        for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'],
                    postdata['addr_district'], postdata['addr_province']]:
            if add is not None or add == "" or add == " ":
                prod_address += add + ","

        prod_address = prod_address[:-1]
        if postdata['listing_type'] != 'ขาย':
            typep = 4
        else:
            typep = 1

        if success:

            data = {
                'currentstep': '1',
                'web_member_type': '1',
                'web_member_username': postdata['user'],
                'web_email': '',
                'web_tel': '',
                'web_lineid': '',
                'web_post_type': typep,
                'web_post_from': '2',
                'web_building_type': theprodid,
                'web_project_id': idzone,
                'web_zone_id': web_zone,
                'web_title': postdata['post_title_th'],
                'web_description': postdata['post_description_th'],
                'web_title_en': '',
                'web_description_en': '',
                'web_latitude': postdata['geo_latitude'],
                'web_longitude': postdata['geo_longitude']
            }

            r = httprequestObj.http_post('https://www.livinginsider.com/a_add_living.php', data=data)
            data = r.text
            # print(r.url)
            # print(r.status_code)
            # print(data)
            img_link = 'https://www.livinginsider.com/js_upload/php/'
            arr = ["files[]"]
            folders = ''
            filelist = ''
            onlyfolder = ''
            files = []
            start = 1
            f = {}
            data = {}
            k = httprequestObj.http_get('https://www.livinginsider.com/living_buysell2.php')
            soup = BeautifulSoup(k.text, self.parser)
            webFolder = soup.select_one('#web_photo_folder')['value']

            # print(webFolder)

            for i in range(len(postdata['post_images'])):
                # print(i)
                f[arr[0]] = (postdata['post_images'][i], open(
                    postdata['post_images'][i], "rb"), "image/jpeg")
                # print(f)
                r = httprequestObj.http_post(img_link, data={'web_photo_folder': webFolder}, files=f)
                # print(r.url)
                # print(r.status_code)
                # print(r.text)

                if r.status_code == 200:
                    r = json.loads(r.text)
                    # print(r)

                    # with open('c.html','w') as f:
                    #     print(k.text,file=f)

                    folderandfile = r['files'][0]['url']
                    cntr = 0
                    folder = ''
                    for i in range(len(folderandfile)):
                        if start == '':
                            onlyfolder += folderandfile[i]
                        if folderandfile[i] == '/':
                            cntr += 1
                            if cntr == 4:
                                start = ''
                            if cntr == 5:
                                break
                        folder += folderandfile[i]
                    file = r['files'][0]['name']
                    filelist += file + "||"
                    files.append(file)
            postdata['floor'] = postdata['floor_total']
            if postdata['property_type'] == 3:
                data = {
                    'currentstep': '2',
                    'web_area_size': 400 * land_size_rai + 100 * land_size_ngan + 1 * land_size_wa,
                    'web_area_size1': land_size_rai,
                    'web_area_size2': land_size_wa,
                    'web_area_size3': land_size_ngan,
                    'web_near_transits': '0',
                    'web_near_academy': '0',
                    'web_keeping_pet': '0',
                    'web_price': postdata['price_baht'],
                    'web_income_year': '0',
                    'web_post_commission_include': '0',
                    'web_post_accept': '1',
                    'web_fq': '0',
                    'web_youtube': '',
                    'web_useful_space': '0',
                    'web_photo_list': filelist,
                    'web_photo_folder': webFolder,
                }
                for i in range(len(postdata['post_images'])):
                    data['web_photo_caption[' +
                         str(i) + '][web_folder]'] = onlyfolder
                    data['web_photo_caption[' + str(i) + '][web_id]'] = ''
                    data['web_photo_caption[' + str(i) + '][photoname]'] = files[i]
                    data['web_photo_caption[' + str(i) + '][caption]'] = ''
            elif theprodid == 1:
                data = {
                    'currentstep': '2',
                    'web_room': postdata['bed_room'],
                    'web_bathroom': postdata['bath_room'],
                    'web_floor': postdata['floor_total'],
                    'web_area_size': postdata['floor_area'],
                    'web_near_transits': '0',
                    'web_near_academy': '0',
                    'web_keeping_pet': '0',
                    'web_price': postdata['price_baht'],
                    'web_income_year': '0',
                    'web_post_commission_include': '0',
                    'web_post_accept': '1',
                    'web_photo_list': filelist,
                    'web_photo_folder': webFolder,
                    'web_fq': '0',
                    'web_youtube': '',
                    'web_useful_space': '0',
                }
                # for i in range(len(postdata['post_images'])):
                for i in range(len(files)):
                    data['web_photo_caption[' +
                         str(i) + '][web_folder]'] = onlyfolder[:-1]
                    data['web_photo_caption[' + str(i) + '][web_id]'] = ''
                    data['web_photo_caption[' + str(i) + '][photoname]'] = files[i]
                    data['web_photo_caption[' + str(i) + '][caption]'] = ''
            elif theprodid == 2:
                data = {
                    'currentstep': '2',
                    'web_room': postdata['bed_room'],
                    'web_bathroom': postdata['bath_room'],
                    'web_floor': postdata['floor_total'],
                    'web_area_size': land_size_wa,
                    'web_near_transits': '0',
                    'web_near_academy': '0',
                    'web_keeping_pet': '1',
                    'web_price': postdata['price_baht'],
                    'web_income_year': '0',
                    'web_post_commission_include': '0',
                    'web_post_accept': '1',
                    'web_photo_list': filelist,
                    'web_photo_folder': webFolder,
                    'web_fq': '0',
                    'web_youtube': '',
                    'web_useful_space': '0',
                }
                for i in range(len(postdata['post_images'])):
                    data['web_photo_caption[' +
                         str(i) + '][web_folder]'] = onlyfolder
                    data['web_photo_caption[' + str(i) + '][web_id]'] = ''
                    data['web_photo_caption[' + str(i) + '][photoname]'] = files[i]
                    data['web_photo_caption[' + str(i) + '][caption]'] = ''
            elif theprodid == 4:
                data = {
                    'currentstep': '2',
                    'web_room': postdata['bed_room'],
                    'web_bathroom': postdata['bath_room'],
                    'web_floor': postdata['floor_level'],
                    'web_area_size': land_size_wa,
                    'web_near_transits': '0',
                    'web_near_academy': '0',
                    'web_keeping_pet': '0',
                    'web_price': postdata['price_baht'],
                    'web_income_year': '0',
                    'web_post_commission_include': '0',
                    'web_post_accept': '1',
                    'web_photo_list': filelist,
                    'web_photo_folder': webFolder,
                    'web_fq': '0',
                    'web_youtube': '',
                    'web_useful_space': postdata['floor_area'],
                }
                for i in range(len(postdata['post_images'])):
                    data['web_photo_caption[' +
                         str(i) + '][web_folder]'] = onlyfolder
                    data['web_photo_caption[' + str(i) + '][web_id]'] = ''
                    data['web_photo_caption[' + str(i) + '][photoname]'] = files[i]
                    data['web_photo_caption[' + str(i) + '][caption]'] = ''

            elif theprodid == 5:
                data = {
                    'currentstep': '2',
                    'web_room': postdata['bed_room'],
                    'web_bathroom': postdata['bath_room'],
                    'web_floor': '0',
                    'web_area_size': '0',
                    'web_near_transits': '0',
                    'web_near_academy': '0',
                    'web_keeping_pet': '0',
                    'web_price': postdata['price_baht'],
                    'web_income_year': '0',
                    'web_post_commission_include': '0',
                    'web_post_accept': '1',
                    'web_photo_list': filelist,
                    'web_photo_folder': webFolder,
                    'web_fq': '0',
                    'web_youtube': '',
                    'web_useful_space': postdata['floor_area'],
                }
                for i in range(len(postdata['post_images'])):
                    data['web_photo_caption[' +
                         str(i) + '][web_folder]'] = onlyfolder
                    data['web_photo_caption[' + str(i) + '][web_id]'] = ''
                    data['web_photo_caption[' + str(i) + '][photoname]'] = files[i]
                    data['web_photo_caption[' + str(i) + '][caption]'] = ''

            elif theprodid == 6:
                # if land_size_wa == 0:
                # land_size_wa=1
                data = {
                    'currentstep': '2',
                    'web_room': postdata['bed_room'],
                    'web_bathroom': postdata['bath_room'],
                    'web_floor': postdata['floor_total'],
                    'web_area_size': land_size_wa,
                    'web_near_transits': '0',
                    'web_near_academy': '0',
                    'web_keeping_pet': '0',
                    'web_price': postdata['price_baht'],
                    'web_income_year': '0',
                    'web_post_commission_include': '0',
                    'web_post_accept': '1',
                    'web_photo_list': filelist,
                    'web_photo_folder': webFolder,
                    'web_fq': '0',
                    'web_youtube': '',
                    'web_useful_space': '0',
                }
                for i in range(len(postdata['post_images'])):
                    data['web_photo_caption[' +
                         str(i) + '][web_folder]'] = onlyfolder
                    data['web_photo_caption[' + str(i) + '][web_id]'] = ''
                    data['web_photo_caption[' + str(i) + '][photoname]'] = files[i]
                    data['web_photo_caption[' + str(i) + '][caption]'] = ''

            elif theprodid == 10:
                data = {
                    'currentstep': '2',
                    'web_room': postdata['bed_room'],
                    'web_floor': postdata['floor_total'],
                    'web_area_size': 400 * land_size_rai + 100 * land_size_ngan + 1 * land_size_wa,
                    'web_area_size1': land_size_rai,
                    'web_area_size2': land_size_wa,
                    'web_area_size3': land_size_ngan,
                    'web_near_transits': '0',
                    'web_near_academy': '0',
                    'web_keeping_pet': '0',
                    'web_price': postdata['price_baht'],
                    'web_income_year': '0',
                    'web_post_commission_include': '0',
                    'web_post_accept': '1',
                    'web_photo_list': filelist,
                    'web_photo_folder': webFolder,
                    'web_fq': '0',
                    'web_youtube': '',
                    'web_useful_space': '0',
                }
                for i in range(len(postdata['post_images'])):
                    data['web_photo_caption[' +
                         str(i) + '][web_folder]'] = onlyfolder
                    data['web_photo_caption[' + str(i) + '][web_id]'] = ''
                    data['web_photo_caption[' + str(i) + '][photoname]'] = files[i]
                    data['web_photo_caption[' + str(i) + '][caption]'] = ''
            elif theprodid == 12:
                data = {
                    'currentstep': '2',
                    'web_room': postdata['bed_room'],
                    'web_floor': '0',
                    'web_area_size': 400 * land_size_rai + 100 * land_size_ngan + 1 * land_size_wa,
                    'web_area_size1': land_size_rai,
                    'web_area_size2': land_size_wa,
                    'web_area_size3': land_size_ngan,
                    'web_near_transits': '0',
                    'web_near_academy': '0',
                    'web_keeping_pet': '0',
                    'web_price': postdata['price_baht'],
                    'web_income_year': '0',
                    'web_post_commission_include': '0',
                    'web_post_accept': '1',
                    'web_photo_list': filelist,
                    'web_photo_folder': webFolder,
                    'web_fq': '0',
                    'web_youtube': '',
                    'web_useful_space': postdata['floor_area'],
                }
                for i in range(len(postdata['post_images'])):
                    data['web_photo_caption[' +
                         str(i) + '][web_folder]'] = onlyfolder
                    data['web_photo_caption[' + str(i) + '][web_id]'] = ''
                    data['web_photo_caption[' + str(i) + '][photoname]'] = files[i]
                    data['web_photo_caption[' + str(i) + '][caption]'] = ''
            elif theprodid == 11:
                data = {
                    'currentstep': '2',
                    'web_room': '0',
                    'web_floor': '0',
                    'web_area_size': 400 * land_size_rai + 100 * land_size_ngan + 1 * land_size_wa,
                    'web_area_size1': land_size_rai,
                    'web_area_size2': land_size_wa,
                    'web_area_size3': land_size_ngan,
                    'web_near_transits': '0',
                    'web_near_academy': '0',
                    'web_keeping_pet': '0',
                    'web_price': postdata['price_baht'],
                    'web_income_year': '0',
                    'web_post_commission_include': '0',
                    'web_post_accept': '1',
                    'web_photo_list': filelist,
                    'web_photo_folder': webFolder,
                    'web_fq': '0',
                    'web_youtube': '',
                    'web_useful_space': postdata['floor_area'],
                }
                for i in range(len(postdata['post_images'])):
                    data['web_photo_caption[' +
                         str(i) + '][web_folder]'] = onlyfolder
                    data['web_photo_caption[' + str(i) + '][web_id]'] = ''
                    data['web_photo_caption[' + str(i) + '][photoname]'] = files[i]
                    data['web_photo_caption[' + str(i) + '][caption]'] = ''
            # print(data)
            headers = {
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': 'https://www.livinginsider.com',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://www.livinginsider.com/living_confirm.php',
                'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            }
            # print('Posting data')
            r = httprequestObj.http_post(
                'https://www.livinginsider.com/a_add_living.php', data=data, headers=headers)
            # print(r.url)
            # print(r.status_code)
            # print(r.text)

            data = {
                'action': 'save',
                'web_status': '1',
                'publish_flag': '1'
            }

            r = httprequestObj.http_get('https://www.livinginsider.com/living_confirm.php')
            # print(r.url)
            # print(r.status_code)

            # with open('b.html', 'w') as f:
            #     print(r.text, file=f)

            r = httprequestObj.http_post('https://www.livinginsider.com/living_confirm.php', data=data)
            # print(r.url)
            # print(r.status_code)

            try:
                r = BeautifulSoup(r.content, self.parser)
                link = r.find('input', attrs={'id': 'link_copy'})['value']
                post_id = post_url.split('/')[4]
            except:
                # print(r.text)
                r = json.loads(r.text)
                link = r['link_copy']

            t = 'https:\/\/www.livinginsider.com\/livingdetail\/495548\/1\/fsa.html'
            if link == '':
                detail = 'not posted'
                success = False
                time_end = datetime.datetime.utcnow()
                time_usage = time_end - time_start
                return {
                    "success": success,
                    "websitename": self.webname,
                    "usage_time": str(time_usage),
                    "start_time": str(time_start),
                    "end_time": str(time_end),
                    "post_url": post_url,
                    "post_id": post_id,
                    "account_type": "null",
                    "detail": detail,
                }

            cntr = 0
            start = 0
            post_id = ''
            for i in link:
                if cntr == 3:
                    post_id += i
                if i == '/':
                    if cntr == 3:
                        post_id = ''
                    if cntr == 4:
                        break
                    cntr += 1
            time_end = datetime.datetime.utcnow()
            time_usage = time_end - time_start
            return {
                "success": True,
                "websitename": "livinginsider",
                "usage_time": str(time_usage),
                "start_time": str(time_start),
                "end_time": str(time_end),
                "post_url": link,
                "post_id": post_id,
                "account_type": "null",
                "detail": '20 credits deducted Post created',
            }
        else:
            detail = "cannot login"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "websitename": self.webname,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
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
            max_page = 100
            post_found = False

            while True:
                page += 1
                params = (
                    ('pages', str(page)),
                    ('action', '1'),
                    ('actiontype', ''),
                    ('posttype', ''),
                    ('searchword', ''),
                    ('search_area', '0'),
                    ('search_bedroom', '0'),
                    ('search_price', '0'),
                    ('from_fq_flag', ''),
                    ('from_pet_flag', ''),
                    ('from_expiring_flag', ''),
                    ('from_autoboost_flag', ''),
                    ('topic_sort', '1'),
                    ('search_zone_id', ''),
                    ('pagelimit', '50'),
                )

                if page == max_page:
                    break

                r = httprequestObj.http_get('https://www.livinginsider.com/mystock.php', params=params)
                # print(r.url)
                # print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                # print(soup.find('ul', 'pagination').findChildren('li', recursive=False)[-3])
                # print(soup.find('ul', 'pagination').findChildren('li', recursive=False)[-3])
                try:
                    max_page = int(soup.find('ul', 'pagination').findChildren('li', recursive=False)[-3].find('a').string)
                except:
                    max_page = 1

                all_posts = soup.find('div', 'head-item bg-mystock-card').findChildren('div', recursive=False)
                mem_id = soup.find('input', {'name': 'mem_id'}).get('value')
                # print(mem_id)
                device_id = r.text.split("let device_id = '")[1].split("'")[0]
                # print(device_id)

                for post in all_posts:
                    post_id = post.get('class')[2].split('item')[-1]
                    # print(post_id)
                    if post_id == postdata['post_id']:
                        # print('Found post')
                        post_found = True
                        break

                if post_found:
                    break

            if post_found:

                r = httprequestObj.http_get('https://www.livinginsider.com/living_edit.php',
                                            params={'topic_id': post_id})
                # print(r.url)
                # print(r.status_code)

                proid = {
                    'คอนโด': '1',  # condo
                    'บ้านเดี่ยว': '2',  # detached houses /home / house / Single House
                    'บ้านแฝด': '3',  # twin houses
                    'ทาวน์เฮ้าส์': '4',  # townhouses / town home / home office
                    'ตึกแถว-อาคารพาณิชย์': '5',  # commercial buildings
                    'ที่ดิน': '6',  # land
                    'อพาร์ทเมนท์': '7',  # apartments
                    'โรงแรม': '8',  # hotels, Real Estate Residencial
                    'ออฟฟิศสำนักงาน': '9',  # Office
                    'โกดัง-โรงงาน': '10',  # warehouses
                    'โรงงาน': '25'  # factory
                }
                getProdId = {'1': 1, '2': 2, '3': 2, '4': 6,
                             '5': 4, '6': 3, '7': 10, '8': 10, '9': 5, '10': 12, '25': 11}

                try:
                    theprodid = getProdId[proid[postdata['property_type']]]
                except:
                    theprodid = getProdId[postdata['property_type']]

                if 'web_project_name' not in postdata or postdata['web_project_name'] != None:
                    if 'project_name' in postdata and postdata['project_name'] != None:
                        postdata['web_project_name'] = postdata['project_name']
                    else:
                        postdata['web_project_name'] = postdata['post_title_th']

                if 'floor_total' not in postdata:
                    postdata['floor_total'] = 1
                elif postdata['floor_total'] is None or postdata['floor_total'] == '':
                    postdata['floor_total'] = 1

                if 'floor_level' not in postdata:
                    postdata['floor_level'] = 1
                elif postdata['floor_level'] is None or postdata['floor_level'] == '':
                    postdata['floor_level'] = 1

                if 'bath_room' not in postdata:
                    postdata['bath_room'] = 1
                elif postdata['bath_room'] == None or postdata['bath_room'] == '':
                    postdata['bath_room'] = 1

                if 'bed_room' not in postdata:
                    postdata['bed_room'] = 1
                elif postdata['bed_room'] == None or postdata['bed_room'] == '':
                    postdata['bed_room'] = 1

                if int(postdata['bed_room']) > 10:
                    postdata['bed_room'] = 11

                if int(postdata['bath_room']) > 5:
                    postdata['bath_room'] = 6

                if postdata['land_size_rai'] == None:
                    land_size_rai = 0
                else:
                    land_size_rai = postdata['land_size_rai']

                if postdata['land_size_ngan'] == None:
                    land_size_ngan = 0
                else:
                    land_size_ngan = postdata['land_size_ngan']

                if postdata['land_size_wa'] == None:
                    land_size_wa = 0
                else:
                    land_size_wa = postdata['land_size_wa']

                province_id = ''
                term = postdata['web_project_name'].replace(' ', '+')

                data = httprequestObj.http_get(
                    'https://www.livinginsider.com/a_project_list_json.php?term=' + term + '&_type=query&q=' + term)
                data = json.loads(data.text)

                if len(data) == 1:
                    term = postdata['addr_district'] + '+' + postdata['addr_province']
                    data = httprequestObj.http_get(
                        'https://www.livinginsider.com/a_project_list_json.php?term=' + term + '&_type=query&q=' + term)
                    data = json.loads(data.text)

                    # print(data)
                    try:
                        idzone = data[1]['id']
                    except:
                        idzone = data[0]['id']
                else:
                    idzone = data[1]['id']
                # print(idzone)
                data = httprequestObj.http_post('https://www.livinginsider.com/a_project_child.php',
                                                data={'web_project_id': idzone})
                # print(data.status_code)
                data = json.loads(data.text)
                # print(data)
                r = data['value']
                if len(r) == 0:
                    params = {
                        'term': postdata['addr_province'],
                        '_type': 'query',
                        'q': postdata['addr_province']
                    }
                    r = httprequestObj.http_get('https://www.livinginsider.com/a_zone_list.php', params=params)
                    # print(r.url)
                    # print(r.status_code)
                    data = r.json()
                    web_zone = data[0]['id']
                    for row in data:
                        if postdata['addr_district'].replace(' ', '') in row and postdata['addr_sub_district'].replace(
                                ' ',
                                '') in row:
                            web_zone = row['id']
                            break
                    # print('Web_zone = ' + str(web_zone))

                    r = httprequestObj.http_post('https://www.livinginsider.com/a_zone_child.php',
                                                 data={'web_zone_id': web_zone})
                    # print(r.url)
                    # print(r.status_code)
                    # print(r.json())

                else:
                    soap = BeautifulSoup(r, self.parser)
                    option = soap.find('option')
                    web_zone = option.get('value')
                    # print('Web_zone = ' + str(web_zone))
                    # print(option)
                prod_address = ""
                for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'],
                            postdata['addr_district'], postdata['addr_province']]:
                    if add is not None or add == "" or add == " ":
                        prod_address += add + ","

                prod_address = prod_address[:-1]
                if postdata['listing_type'] != 'ขาย':
                    typep = 4
                else:
                    typep = 1

                if success:
                    data = {
                        'currentstep': '1',
                        'web_id': post_id,
                        'web_member_type': '1',
                        'web_member_username': postdata['user'],
                        'web_email': '',
                        'web_tel': '',
                        'web_lineid': '',
                        'web_post_type': typep,
                        'web_post_from': '2',
                        'web_building_type': theprodid,
                        'web_project_id': idzone,
                        'web_zone_id': web_zone,
                        'web_title': postdata['post_title_th'],
                        'web_description': postdata['post_description_th'],
                        'web_title_en': '',
                        'web_description_en': '',
                        'web_latitude': postdata['geo_latitude'],
                        'web_longitude': postdata['geo_longitude'],
                        'state_renew': ''
                    }

                    r = httprequestObj.http_post('https://www.livinginsider.com/a_edit_living.php', data=data)
                    data = r.text
                    # print(r.url)
                    # print(r.status_code)
                    # print(data)
                    # print('Getting 2nd page')

                    headers = {
                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'Sec-Fetch-Site': 'same-origin',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-User': '?1',
                        'Sec-Fetch-Dest': 'document',
                        'Referer': 'https://www.livinginsider.com/living_edit.php?topic_id=' + post_id,
                        'Accept-Language': 'en-IN,en-US;q=0.9,en;q=0.8',
                    }

                    r = httprequestObj.http_get('https://www.livinginsider.com/living_edit2.php',
                                                params={'topic_id': post_id}, headers=headers)
                    # print(r.url)
                    # print(r.status_code)

                    soup = BeautifulSoup(r.content, self.parser)
                    webFolder = soup.find('input', {'id': 'web_photo_folder'}).get('value')
                    delete_params = soup.find_all('a', 'delete_img')

                    # print('DELETING PHOTOS')
                    for img in delete_params:
                        info = img.get('onclick').split('"')
                        images_name = info[1]
                        web_photo_folder = info[3]
                        # print(images_name)
                        # print(web_photo_folder)
                        params = {
                            'images_name': images_name,
                            'web_photo_folder': web_photo_folder
                        }
                        r = httprequestObj.http_get('https://www.livinginsider.com/a_delete_photo.php', params=params)
                        # print(r.url)
                        # print(r.status_code)
                    img_link = 'https://www.livinginsider.com/js_upload/php/'
                    arr = ["files[]"]
                    folders = ''
                    filelist = ''
                    onlyfolder = ''
                    files = []
                    start = 1
                    f = {}
                    data = {}
                    k = httprequestObj.http_get('https://www.livinginsider.com/living_buysell2.php')
                    soup = BeautifulSoup(k.text, self.parser)
                    # webFolder = soup.find('input', {'id': 'web_photo_folder'}).get('value')
                    # print('WebFolder')
                    # print(webFolder)
                    # webFolder = 'https://www.livinginsider.com/upload/topic415'
                    # print(webFolder)
                    # print('UPLOADING PHOTOS')
                    for i in range(len(postdata['post_images'])):
                        filename = str(i) + '.jpeg'
                        datapost = [
                            ('web_photo_folder', (None, webFolder)),
                            ('web_status', (None, '')),
                            ('state_renew', (None, '')),
                            ('web_room', (None, '')),
                            ('web_bathroom', (None, '')),
                            ('web_floor', (None, '')),
                            ('web_area_size', (None, '')),
                            ('web_price', (None, '')),
                            ('web_contract_startdate', (None, '')),
                            ('web_price6', (None, '')),
                            ('web_price3', (None, '')),
                            ('web_price1', (None, '')),
                            ('web_youtube', (None, '')),
                            ('web_photo_list', (None, '')),
                            ('files[]', (filename, open(postdata['post_images'][i], "rb"), "image/jpeg")),
                        ]
                        # print(f)
                        r = httprequestObj.http_post(img_link, data={}, files=datapost)
                        # print(r.url)
                        # print(r.status_code)
                        # print(r.text)

                        if r.status_code == 200:
                            r = json.loads(r.text)
                            # print(r)

                            folderandfile = r['files'][0]['url']
                            cntr = 0
                            folder = ''
                            for i in range(len(folderandfile)):
                                if start == '':
                                    onlyfolder += folderandfile[i]
                                if folderandfile[i] == '/':
                                    cntr += 1
                                    if cntr == 4:
                                        start = ''
                                    if cntr == 5:
                                        break
                                folder += folderandfile[i]
                            file = r['files'][0]['name']
                            filelist += file + "||"
                            files.append(file)
                    postdata['floor'] = postdata['floor_total']
                    # folder = 'https://www.livinginsider.com/upload/topic415'
                    if postdata['property_type'] == 3:
                        data = {
                            'currentstep': '2',
                            'web_id': post_id,
                            'web_area_size': 400 * land_size_rai + 100 * land_size_ngan + 1 * land_size_wa,
                            'web_area_size1': land_size_rai,
                            'web_area_size2': land_size_wa,
                            'web_area_size3': land_size_ngan,
                            'web_near_transits': '0',
                            'web_near_academy': '0',
                            'web_keeping_pet': '0',
                            'web_price': postdata['price_baht'],
                            'web_price6': '',
                            'web_price3': '',
                            'web_price1': '',
                            'web_contract_startdate': '',
                            'web_income_year': '0',
                            'web_post_commission_include': '0',
                            'web_post_accept': '1',
                            'web_fq': '0',
                            'web_youtube': '',
                            'web_useful_space': '0',
                            'web_photo_list': filelist,
                            'web_photo_folder': webFolder,

                        }
                        for i in range(len(postdata['post_images'])):
                            data['web_photo_caption[' +
                                 str(i) + '][web_folder]'] = onlyfolder[:-1]
                            data['web_photo_caption[' + str(i) + '][web_id]'] = post_id
                            data['web_photo_caption[' + str(i) + '][photoname]'] = files[i]
                            data['web_photo_caption[' + str(i) + '][web_caption_id]'] = '0'
                            data['web_photo_caption[' + str(i) + '][caption]'] = ''
                    elif theprodid == 1:
                        data = {
                            'currentstep': '2',
                            'web_room': postdata['bed_room'],
                            'web_bathroom': postdata['bath_room'],
                            'web_floor': postdata['floor_total'],
                            'web_area_size': postdata['floor_area'],
                            'web_near_transits': '0',
                            'web_near_academy': '0',
                            'web_keeping_pet': '0',
                            'web_price': postdata['price_baht'],
                            'web_id': post_id,
                            'web_price6': '',
                            'web_price3': '',
                            'web_price1': '',
                            'web_contract_startdate': '',
                            'web_post_commission_include': '0',
                            'web_post_accept': '1',
                            'web_photo_list': filelist,
                            'web_photo_folder': webFolder,
                            'web_fq': '0',
                            'web_youtube': '',
                        }
                        # for i in range(len(postdata['post_images'])):
                        # print(files)
                        onlyfolder = 'topic415 '
                        for i in range(len(files)):
                            data['web_photo_caption[' +
                                 str(i) + '][web_folder]'] = onlyfolder[:-1]
                            data['web_photo_caption[' + str(i) + '][web_id]'] = post_id
                            data['web_photo_caption[' + str(i) + '][photoname]'] = files[i]
                            data['web_photo_caption[' + str(i) + '][web_caption_id]'] = '0'
                            data['web_photo_caption[' + str(i) + '][caption]'] = ''
                    elif theprodid == 2:
                        data = {
                            'currentstep': '2',
                            'web_room': postdata['bed_room'],
                            'web_bathroom': postdata['bath_room'],
                            'web_floor': postdata['floor_total'],
                            'web_area_size': land_size_wa,
                            'web_near_transits': '0',
                            'web_near_academy': '0',
                            'web_keeping_pet': '1',
                            'web_price': postdata['price_baht'],
                            'web_id': post_id,
                            'web_price6': '',
                            'web_price3': '',
                            'web_price1': '',
                            'web_contract_startdate': '',
                            'web_income_year': '0',
                            'web_post_commission_include': '0',
                            'web_post_accept': '1',
                            'web_photo_list': filelist,
                            'web_photo_folder': webFolder,
                            'web_fq': '0',
                            'web_youtube': '',
                            'web_useful_space': '0',
                        }
                        for i in range(len(postdata['post_images'])):
                            data['web_photo_caption[' +
                                 str(i) + '][web_folder]'] = onlyfolder[:-1]
                            data['web_photo_caption[' + str(i) + '][web_id]'] = post_id
                            data['web_photo_caption[' + str(i) + '][photoname]'] = files[i]
                            data['web_photo_caption[' + str(i) + '][web_caption_id]'] = '0'
                            data['web_photo_caption[' + str(i) + '][caption]'] = ''
                    elif theprodid == 4:
                        data = {
                            'currentstep': '2',
                            'web_room': postdata['bed_room'],
                            'web_bathroom': postdata['bath_room'],
                            'web_floor': postdata['floor_level'],
                            'web_area_size': land_size_wa,
                            'web_near_transits': '0',
                            'web_near_academy': '0',
                            'web_keeping_pet': '0',
                            'web_price': postdata['price_baht'],
                            'web_id': post_id,
                            'web_price6': '',
                            'web_price3': '',
                            'web_price1': '',
                            'web_contract_startdate': '',
                            'web_income_year': '0',
                            'web_post_commission_include': '0',
                            'web_post_accept': '1',
                            'web_photo_list': filelist,
                            'web_photo_folder': webFolder,
                            'web_fq': '0',
                            'web_youtube': '',
                            'web_useful_space': postdata['floor_area'],
                        }
                        for i in range(len(postdata['post_images'])):
                            data['web_photo_caption[' +
                                 str(i) + '][web_folder]'] = onlyfolder[:-1]
                            data['web_photo_caption[' + str(i) + '][web_id]'] = post_id
                            data['web_photo_caption[' + str(i) + '][photoname]'] = files[i]
                            data['web_photo_caption[' + str(i) + '][web_caption_id]'] = '0'
                            data['web_photo_caption[' + str(i) + '][caption]'] = ''

                    elif theprodid == 5:
                        data = {
                            'currentstep': '2',
                            'web_room': postdata['bed_room'],
                            'web_bathroom': postdata['bath_room'],
                            'web_floor': '0',
                            'web_area_size': '0',
                            'web_near_transits': '0',
                            'web_near_academy': '0',
                            'web_keeping_pet': '0',
                            'web_price': postdata['price_baht'],
                            'web_id': post_id,
                            'web_price6': '',
                            'web_price3': '',
                            'web_price1': '',
                            'web_contract_startdate': '',
                            'web_income_year': '0',
                            'web_post_commission_include': '0',
                            'web_post_accept': '1',
                            'web_photo_list': filelist,
                            'web_photo_folder': webFolder,
                            'web_fq': '0',
                            'web_youtube': '',
                            'web_useful_space': postdata['floor_area'],
                        }
                        for i in range(len(postdata['post_images'])):
                            data['web_photo_caption[' +
                                 str(i) + '][web_folder]'] = onlyfolder[:-1]
                            data['web_photo_caption[' + str(i) + '][web_id]'] = post_id
                            data['web_photo_caption[' + str(i) + '][photoname]'] = files[i]
                            data['web_photo_caption[' + str(i) + '][web_caption_id]'] = '0'
                            data['web_photo_caption[' + str(i) + '][caption]'] = ''

                    elif theprodid == 6:
                        # if land_size_wa == 0:
                        # land_size_wa=1
                        data = {
                            'currentstep': '2',
                            'web_room': postdata['bed_room'],
                            'web_bathroom': postdata['bath_room'],
                            'web_floor': postdata['floor_total'],
                            'web_area_size': land_size_wa,
                            'web_near_transits': '0',
                            'web_near_academy': '0',
                            'web_keeping_pet': '0',
                            'web_price': postdata['price_baht'],
                            'web_id': post_id,
                            'web_price6': '',
                            'web_price3': '',
                            'web_price1': '',
                            'web_contract_startdate': '',
                            'web_income_year': '0',
                            'web_post_commission_include': '0',
                            'web_post_accept': '1',
                            'web_photo_list': filelist,
                            'web_photo_folder': webFolder,
                            'web_fq': '0',
                            'web_youtube': '',
                            'web_useful_space': '0',
                        }
                        for i in range(len(postdata['post_images'])):
                            data['web_photo_caption[' +
                                 str(i) + '][web_folder]'] = onlyfolder[:-1]
                            data['web_photo_caption[' + str(i) + '][web_id]'] = post_id
                            data['web_photo_caption[' + str(i) + '][photoname]'] = files[i]
                            data['web_photo_caption[' + str(i) + '][web_caption_id]'] = '0'
                            data['web_photo_caption[' + str(i) + '][caption]'] = ''

                    elif theprodid == 10:
                        data = {
                            'currentstep': '2',
                            'web_room': postdata['bed_room'],
                            'web_floor': postdata['floor_total'],
                            'web_area_size': 400 * land_size_rai + 100 * land_size_ngan + 1 * land_size_wa,
                            'web_area_size1': land_size_rai,
                            'web_area_size2': land_size_wa,
                            'web_area_size3': land_size_ngan,
                            'web_near_transits': '0',
                            'web_near_academy': '0',
                            'web_keeping_pet': '0',
                            'web_price': postdata['price_baht'],
                            'web_id': post_id,
                            'web_price6': '',
                            'web_price3': '',
                            'web_price1': '',
                            'web_contract_startdate': '',
                            'web_income_year': '0',
                            'web_post_commission_include': '0',
                            'web_post_accept': '1',
                            'web_photo_list': filelist,
                            'web_photo_folder': webFolder,
                            'web_fq': '0',
                            'web_youtube': '',
                            'web_useful_space': '0',
                        }
                        for i in range(len(postdata['post_images'])):
                            data['web_photo_caption[' +
                                 str(i) + '][web_folder]'] = onlyfolder[:-1]
                            data['web_photo_caption[' + str(i) + '][web_id]'] = post_id
                            data['web_photo_caption[' + str(i) + '][photoname]'] = files[i]
                            data['web_photo_caption[' + str(i) + '][web_caption_id]'] = '0'
                            data['web_photo_caption[' + str(i) + '][caption]'] = ''
                    elif theprodid == 12:
                        data = {
                            'currentstep': '2',
                            'web_room': postdata['bed_room'],
                            'web_floor': '0',
                            'web_area_size': 400 * land_size_rai + 100 * land_size_ngan + 1 * land_size_wa,
                            'web_area_size1': land_size_rai,
                            'web_area_size2': land_size_wa,
                            'web_area_size3': land_size_ngan,
                            'web_near_transits': '0',
                            'web_near_academy': '0',
                            'web_keeping_pet': '0',
                            'web_price': postdata['price_baht'],
                            'web_id': post_id,
                            'web_price6': '',
                            'web_price3': '',
                            'web_price1': '',
                            'web_contract_startdate': '',
                            'web_income_year': '0',
                            'web_post_commission_include': '0',
                            'web_post_accept': '1',
                            'web_photo_list': filelist,
                            'web_photo_folder': webFolder,
                            'web_fq': '0',
                            'web_youtube': '',
                            'web_useful_space': postdata['floor_area'],
                        }
                        for i in range(len(postdata['post_images'])):
                            data['web_photo_caption[' +
                                 str(i) + '][web_folder]'] = onlyfolder[:-1]
                            data['web_photo_caption[' + str(i) + '][web_id]'] = post_id
                            data['web_photo_caption[' + str(i) + '][photoname]'] = files[i]
                            data['web_photo_caption[' + str(i) + '][web_caption_id]'] = '0'
                            data['web_photo_caption[' + str(i) + '][caption]'] = ''
                    elif theprodid == 11:
                        data = {
                            'currentstep': '2',
                            'web_room': '0',
                            'web_floor': '0',
                            'web_area_size': 400 * land_size_rai + 100 * land_size_ngan + 1 * land_size_wa,
                            'web_area_size1': land_size_rai,
                            'web_area_size2': land_size_wa,
                            'web_area_size3': land_size_ngan,
                            'web_near_transits': '0',
                            'web_near_academy': '0',
                            'web_keeping_pet': '0',
                            'web_price': postdata['price_baht'],
                            'web_id': post_id,
                            'web_price6': '',
                            'web_price3': '',
                            'web_price1': '',
                            'web_contract_startdate': '',
                            'web_income_year': '0',
                            'web_post_commission_include': '0',
                            'web_post_accept': '1',
                            'web_photo_list': filelist,
                            'web_photo_folder': webFolder,
                            'web_fq': '0',
                            'web_youtube': '',
                            'web_useful_space': postdata['floor_area'],
                        }
                        for i in range(len(postdata['post_images'])):
                            data['web_photo_caption[' +
                                 str(i) + '][web_folder]'] = onlyfolder[:-1]
                            data['web_photo_caption[' + str(i) + '][web_id]'] = post_id
                            data['web_photo_caption[' + str(i) + '][photoname]'] = files[i]
                            data['web_photo_caption[' + str(i) + '][web_caption_id]'] = '0'
                            data['web_photo_caption[' + str(i) + '][caption]'] = ''
                    headers = {
                        'Connection': 'keep-alive',
                        'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'X-Requested-With': 'XMLHttpRequest',
                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Origin': 'https://www.livinginsider.com',
                        'Sec-Fetch-Site': 'same-origin',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Dest': 'empty',
                        'Referer': 'https://www.livinginsider.com/living_edit2.php?topic_id=' + post_id,
                        'Accept-Language': 'en-IN,en-US;q=0.9,en;q=0.8',
                    }
                    # print('Posting data')
                    r = httprequestObj.http_post('https://www.livinginsider.com/a_edit_living.php', data=data, headers=headers)
                    # print(r.url)
                    # print(r.status_code)
                    # print(r.text)

                    data = {
                        'hidden_status': '',
                        'action': 'save',
                        'web_status': '1',
                        'publish_flag': '0',
                        'state_renew': ''
                    }

                    r = httprequestObj.http_get('https://www.livinginsider.com/living_edit_confirm.php',
                                                params={'topic_id': post_id})
                    # print(r.url)
                    # print(r.status_code)

                    r = httprequestObj.http_post('https://www.livinginsider.com/living_edit_confirm.php',
                                                 params={'topic_id': post_id}, data=data)
                    # print(r.url)
                    # print(r.status_code)

                    try:
                        r = BeautifulSoup(r.content, self.parser)
                        link = r.find('input', attrs={'id': 'link_copy'})['value']
                        post_id = post_url.split('/')[4]
                    except:
                        # print(r.text)
                        r = json.loads(r.text)
                        link = r['link_copy']

                    t = 'https:\/\/www.livinginsider.com\/livingdetail\/495548\/1\/fsa.html'
                    if link == '':
                        detail = 'not posted'
                        success = False
                        time_end = datetime.datetime.utcnow()
                        time_usage = time_end - time_start
                        return {
                            "success": success,
                            "websitename": self.webname,
                            "usage_time": str(time_usage),
                            "start_time": str(time_start),
                            "end_time": str(time_end),
                            "post_url": post_url,
                            "post_id": post_id,
                            "account_type": "null",
                            "detail": detail,
                        }

                    cntr = 0
                    start = 0
                    post_id = ''
                    for i in link:
                        if cntr == 3:
                            post_id += i
                        if i == '/':
                            if cntr == 3:
                                post_id = ''
                            if cntr == 4:
                                break
                            cntr += 1
                    time_end = datetime.datetime.utcnow()
                    time_usage = time_end - time_start
                    return {
                        "success": True,
                        "websitename": self.webname,
                        "usage_time": str(time_usage),
                        "start_time": str(time_start),
                        "end_time": str(time_end),
                        "post_url": link,
                        "post_id": post_id,
                        "account_type": "null",
                        "detail": 'Post editeded successfully',
                    }
                else:
                    success = False
                    detail = "Couldnot edit post"
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
            "websitename": self.webname,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
        }

    def delete_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        post_id = postdata['post_id']
        log_id = postdata['log_id']

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = ""
        post_id = ""
        post_url = ""
        mem_id = ''
        device_id = ''

        if success:

            page = 0
            post_found = False
            max_page = 100

            while True:
                page += 1
                params = (
                    ('pages', str(page)),
                    ('action', '1'),
                    ('actiontype', ''),
                    ('posttype', ''),
                    ('searchword', ''),
                    ('search_area', '0'),
                    ('search_bedroom', '0'),
                    ('search_price', '0'),
                    ('from_fq_flag', ''),
                    ('from_pet_flag', ''),
                    ('from_expiring_flag', ''),
                    ('from_autoboost_flag', ''),
                    ('topic_sort', '1'),
                    ('search_zone_id', ''),
                    ('pagelimit', '50'),
                )

                if page == max_page:
                    break

                r = httprequestObj.http_get('https://www.livinginsider.com/mystock.php', params=params)
                # print(r.url)
                # print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                # print(soup.find('ul', 'pagination').findChildren('li', recursive=False)[-3])
                try:
                    max_page = int(soup.find('ul', 'pagination').findChildren('li', recursive=False)[-3].find('a').string)
                except:
                    max_page = 1
                

                all_posts = soup.find('div', 'head-item bg-mystock-card').findChildren('div', recursive=False)
                mem_id = soup.find('input', {'name': 'mem_id'}).get('value')
                # print(mem_id)
                device_id = r.text.split("let device_id = '")[1].split("'")[0]
                # print(device_id)

                for post in all_posts:
                    post_id = post.get('class')[2].split('item')[-1]
                    # print(post_id)
                    if post_id == postdata['post_id']:
                        # print('Found post')
                        post_found = True
                        break

                if post_found:
                    break

            if post_found:
                datapost = {
                    'mem_id': mem_id,
                    'device_id': device_id,
                    'device_type': '1',
                    'lang': 'TH',
                    'sub_mem_id': '0',
                    'sub_device_id': '0'
                }

                r = httprequestObj.http_post('https://api.livinginsider.com/living_delete_reason.php', data=datapost)
                # print(r.url)
                # print(r.status_code)
                data = r.json()
                # print(data)

                datapost['web_id'] = post_id
                datapost['web_delete_reason_text'] = ''

                r = httprequestObj.http_post('https://api.livinginsider.com/my_living_topic_delete.php', data=datapost)
                # print(r.url)
                # print(r.status_code)
                data = r.json()
                # print(data)

                if data['module'] == 'my_living_topic_delete':
                    success = True
                    detail = "Post deleted successfully"
                else:
                    success = False
                    detail = 'Couldnot delete post'
            else:
                success = False
                detail = 'No post with given post_id'
        else:
            success = False
            detail = 'Couldnot login'

        time_end = datetime.datetime.utcnow()
        return {
            "success": success,
            "usage_time": time_end - time_start,
            "start_time": time_start,
            "end_time": time_end,
            "detail": detail,
            "log_id": log_id,
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
            "websitename": "livinginsider",
        }

    def boost_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        post_id = postdata['post_id']
        log_id = postdata['log_id']

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = ""
        post_id = ""
        post_url = ""
        mem_id = ''
        device_id = ''

        if success:

            page = 0
            post_found = False
            max_page = 100

            while True:
                page += 1
                params = (
                    ('pages', str(page)),
                    ('action', '1'),
                    ('actiontype', ''),
                    ('posttype', ''),
                    ('searchword', ''),
                    ('search_area', '0'),
                    ('search_bedroom', '0'),
                    ('search_price', '0'),
                    ('from_fq_flag', ''),
                    ('from_pet_flag', ''),
                    ('from_expiring_flag', ''),
                    ('from_autoboost_flag', ''),
                    ('topic_sort', '1'),
                    ('search_zone_id', ''),
                    ('pagelimit', '50'),
                )

                if page == max_page:
                    break

                r = httprequestObj.http_get('https://www.livinginsider.com/mystock.php', params=params)
                # print(r.url)
                # print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                # print(soup.find('ul', 'pagination').findChildren('li', recursive=False)[-3])
                try:
                    max_page = int(soup.find('ul', 'pagination').findChildren('li', recursive=False)[-3].find('a').string)
                except:
                    max_page = 1

                all_posts = soup.find('div', 'head-item bg-mystock-card').findChildren('div', recursive=False)
                mem_id = soup.find('input', {'name': 'mem_id'}).get('value')
                # print(mem_id)
                device_id = r.text.split("let device_id = '")[1].split("'")[0]
                # print(device_id)

                for post in all_posts:
                    post_id = post.get('class')[2].split('item')[-1]
                    # print(post_id)
                    if post_id == postdata['post_id']:
                        # print('Found post')
                        post_found = True
                        break

                if post_found:
                    break

            if post_found:
                datapost = {
                    'mem_id': mem_id,
                    'device_id': device_id,
                    'device_type': '1',
                    'lang': 'TH',
                    'sub_mem_id': '0',
                    'sub_device_id': '0'
                }

                r = httprequestObj.http_post('https://api.livinginsider.com/current_coin.php', data=datapost)
                # print(r.url)
                # print(r.status_code)
                data = r.json()
                # print(data)

                datapost = {
                    'web_member_username': postdata['user'],
                    'web_id': post_id,
                    'mem_id': mem_id,
                    'device_id': device_id,
                    'device_type': '1',
                    'lang': 'TH',
                    'sub_mem_id': '0',
                    'sub_device_id': '0'
                }

                r = httprequestObj.http_post('https://api.livinginsider.com/living_topic_up.php', data=datapost)
                # print(r.url)
                # print(r.status_code)
                data = r.json()

                if data['result_msg'] == 'ดันประกาศเรียบร้อย':
                    success = True
                    detail = "Post boosted successfully"
                else:
                    success = False
                    detail = 'Couldnot boost post'
            else:
                success = False
                detail = 'No post with given post_id'
        else:
            success = False
            detail = 'Couldnot login'

        time_end = datetime.datetime.utcnow()
        return {
            "success": success,
            "usage_time": time_end - time_start,
            "start_time": time_start,
            "end_time": time_end,
            "detail": detail,
            "log_id": log_id,
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
            "websitename": "livinginsider",
        }

    def search_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_url = ""
        post_id = ""
        post_modified = ""
        post_view = ""

        if success:
            page = 0
            post_found = False
            max_page = 100

            while True:
                page += 1
                params = (
                    ('pages', str(page)),
                    ('action', '1'),
                    ('actiontype', ''),
                    ('posttype', ''),
                    ('searchword', ''),
                    ('search_area', '0'),
                    ('search_bedroom', '0'),
                    ('search_price', '0'),
                    ('from_fq_flag', ''),
                    ('from_pet_flag', ''),
                    ('from_expiring_flag', ''),
                    ('from_autoboost_flag', ''),
                    ('topic_sort', '1'),
                    ('search_zone_id', ''),
                    ('pagelimit', '50'),
                )

                if page == max_page:
                    break

                r = httprequestObj.http_get('https://www.livinginsider.com/mystock.php', params=params)
                # print(r.url)
                # print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                # print(soup.find('ul', 'pagination').findChildren('li', recursive=False)[-3])
                try:
                    max_page = int(soup.find('ul', 'pagination').findChildren('li', recursive=False)[-3].find('a').string)
                except:
                    max_page = 1

                all_posts = soup.find('div', 'head-item bg-mystock-card').findChildren('div', recursive=False)
                mem_id = soup.find('input', {'name': 'mem_id'}).get('value')
                # print(mem_id)
                device_id = r.text.split("let device_id = '")[1].split("'")[0]
                # print(device_id)

                # for post in all_posts:
                #     post_id = post.get('class')[2].split('item')[-1]
                #     # print(post_id)
                #     if post_id == postdata['post_id']:
                #         # print('Found post')
                #         post_found = True
                #         break


            

                for post in all_posts:
                    info = post.findChildren('div', recursive=False)
                    post_url = info[2].find('div').find('a').get('href')
                    title = info[2].find('div').find('a').find('div').find('div').string  # .split(':').strip()
                    # print(title)

                    if postdata['post_title_th'] in title:
                        # print('Found post')
                        post_found = True
                        detail = "Post Found"
                        post_id = post_url.split('/')[-2]
                        post_modified = ''
                        # print(post_modified)
                        post_view = ''
                        # print(post_view)
                        break

                if post_found:
                    break

            if not post_found:
                post_url = ''
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
            "websitename": "livinginsider",
            "account_type": None,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "post_created": "",
            "post_modified": post_modified,
            "post_view": post_view,
            "post_url": post_url
        }

    def print_debug(self, msg):
        if self.debug == 1:
            print(msg)
        return True
