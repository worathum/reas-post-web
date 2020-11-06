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
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        }

        r = httprequestObj.http_post(
            'https://www.livinginsider.com/login.php', data=datapost)
        print(r.status_code)
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



        if success:
            getProdId = {'1': 1, '2': 2, '3': 2, '4': 6,
                        '5': 4, '6': 3, '7': 10, '8': 10, '9': 5, '10': 12, '25': 11}

            theprodid = getProdId[str(postdata['property_type'])]

            if 'web_project_name' not in postdata or postdata['web_project_name'] is None or postdata['web_project_name'] == '':
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
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
            }


            web_zone = ''
            idzone = '0'

            if str(postdata['property_type']) == '1':
                term = postdata['web_project_name'].replace(' ', '+')

                data = requests.get('https://www.livinginsider.com/a_project_list_json.php?term=' + term + '&_type=query&q=' + term)    

                data = json.loads(data.text)
                idzone = None

                for i in range(len(data)):
                    if postdata['web_project_name'].strip().lower() in data[i]['text'].strip().lower() or data[i]['text'].strip().lower() in postdata['web_project_name'].strip().lower():
                        if data[i]['id'] != postdata['web_project_name']:
                            idzone = data[i]['id']
                        break

                if idzone is None:
                    time_end = datetime.datetime.utcnow()
                    time_usage = time_end - time_start
                    return {
                        "success": False,
                        "websitename": "livinginsider",
                        "usage_time": str(time_usage),
                        "start_time": str(time_start),
                        "end_time": str(time_end),
                        "post_url": "",
                        "post_id": "",
                        "account_type": "null",
                        "detail": 'Project not Found. Post not created!',
                    }

                data = httprequestObj.http_post('https://www.livinginsider.com/a_project_child.php', data={'web_project_id': idzone})
                data = json.loads(data.text)
                print(data)

                r = data['value']
                soap = BeautifulSoup(r, self.parser)
                option = soap.find('option')
                web_zone = option.get('value')

            else:
                # term = postdata['web_location'].replace(' ', '+')
                # r = httprequestObj.http_get(
                #     'https://www.livinginsider.com/a_zone_list.php?term=' + term + '&_type=query&q=' + term)
                            
                # data = r.json()

                # web_zone = None

                # for i in range(len(data)):
                #     if postdata['web_location'].strip().lower() in data[i]['text'].strip().lower() or data[i]['text'].strip().lower() in postdata['web_location'].strip().lower():
                #         print(data[i])
                #         web_zone = data[i]['id']
                #         break
                
                try:
                    web_zone = int(str(postdata['location_area']).strip())
                except:
                    time_end = datetime.datetime.utcnow()
                    time_usage = time_end - time_start
                    return {
                        "success": False,
                        "websitename": "livinginsider",
                        "usage_time": str(time_usage),
                        "start_time": str(time_start),
                        "end_time": str(time_end),
                        "post_url": "",
                        "post_id": "",
                        "account_type": "null",
                        "detail": 'Location not Found. Post not created!',
                    }


            

            r = httprequestObj.http_post('https://www.livinginsider.com/a_zone_child.php', data={'web_zone_id': web_zone})

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


            for i in range(len(postdata['post_images'])):
                # print(i)
                f[arr[0]] = (postdata['post_images'][i], open(
                    postdata['post_images'][i], "rb"), "image/jpeg")
                # print(f)
                r = httprequestObj.http_post(img_link, data={'web_photo_folder': webFolder}, files=f)

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
            if theprodid == 3:
                data = {
                    'currentstep': '2',
                    'web_area_size': 400 * int(land_size_rai) + 100 * int(land_size_ngan) + int(land_size_wa),
                    'web_area_size1': land_size_rai,
                    'web_area_size2': land_size_wa,
                    'web_area_size3': land_size_ngan,
                    'web_near_transits': '0',
                    'web_near_academy': '0',
                    'web_keeping_pet': '0',
                    'web_price': postdata['price_baht'],
                    'web_income_year': '0',
                    'web_post_commission': '3',
                    'web_post_commission_include': '0',
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
                    'web_area_size': 400 * int(land_size_rai) + 100 * int(land_size_ngan) + int(land_size_wa),
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
                    'web_area_size': 400 * int(land_size_rai) + 100 * int(land_size_ngan) + int(land_size_wa),
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
                    'web_area_size': 400 * int(land_size_rai) + 100 * int(land_size_ngan) + int(land_size_wa),
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
            # print(data)
            r = httprequestObj.http_post(
                'https://www.livinginsider.com/a_add_living.php', data=data, headers=headers)
            print(r.url)
            print(r.status_code)
            print(r.text)

            data = {
                'action': 'save',
                'web_status': '1',
                'publish_flag': '1'
            }

            r = httprequestObj.http_get('https://www.livinginsider.com/living_confirm.php')
            # print(r.url)
            # print(r.status_code)
            # print(r.text)

            # with open('b.html', 'w') as f:
            #     print(r.text, file=f)

            r = httprequestObj.http_post('https://www.livinginsider.com/living_confirm.php', data=data)
            print(r.url)
            print(r.status_code)
            print(r.text)
            link = ''
            try:
                r = BeautifulSoup(r.content, self.parser)
                link = r.find('input', attrs={'id': 'link_copy'})['value']
            except:
                # print(r.text)
                r = json.loads(r.text)
                link = r['link_copy']
            
            if link == '':
                detail = 'Not posted. Some required information is missing OR Similar post already exists.'
                success = False
                time_end = datetime.datetime.utcnow()
                time_usage = time_end - time_start
                return {
                    "success": success,
                    "websitename": self.webname,
                    "usage_time": str(time_usage),
                    "start_time": str(time_start),
                    "end_time": str(time_end),
                    "post_url": "",
                    "post_id": "",
                    "account_type": "null",
                    "detail": detail,
                }
            temp = link.split('/')
            if len(temp)>4:
                post_id = temp[4]
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
        post_id = postdata['post_id']
        post_url = ""
        if success:

            post_found = False

            page = 1

            post_found = False
            max_page = 100
            r = httprequestObj.http_get(
                'https://www.livinginsider.com/mystock.php?action=1&pages=1&pagelimit=50&actiontype=&posttype=&search_zone_id=&search_project_id=&web_id_for_publish=&web_id_hidden=&check_open_graph=&id_scroll=-1&search_bedroom=0&search_area=0&search_price=0&topic_sort=1&group_list=&searchword=')
            soup = BeautifulSoup(r.content, self.parser)
            try:
                max_page = int(soup.find('ul', 'pagination').findChildren('li', recursive=False)[-3].find('a').string)
            except:
                max_page = 1
            while page <= max_page:
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
                r = httprequestObj.http_get('https://www.livinginsider.com/mystock.php', params=params)
                if r.history:
                    break
                soup = BeautifulSoup(r.content, self.parser)
                all_posts = soup.find_all(class_='mystock-item')
                for post in all_posts:
                    # print(post.get('topic-id'))
                    if str(post.get('topic-id')) == str(postdata['post_id']):
                        post_found = True
                        referer = post.find('a', {'href': re.compile('https://www.livinginsider.com/livingdetail/')}).get('href')
                        break
                page += 1
                if post_found:
                    break

            if post_found:

                headers = {
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Mobile Safari/537.36',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-User': '?1',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                    'Sec-Fetch-Site': 'same-origin',
                    'Referer': 'https://www.livinginsider.com/mystock.php',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                }


                r = httprequestObj.http_get('https://www.livinginsider.com/living_edit.php', params={'topic_id': str(post_id)}, headers=headers)
                print(r.status_code)


                getProdId = {'1': 1, '2': 2, '3': 2, '4': 6,
                             '5': 4, '6': 3, '7': 10, '8': 10, '9': 5, '10': 12, '25': 11}

                theprodid = getProdId[postdata['property_type']]

                if 'web_project_name' not in postdata or postdata['web_project_name'] is None or postdata['web_project_name'] == '':
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
                idzone = '0'
                web_zone = ''

                if str(postdata['property_type']) == '1':
                    term = postdata['web_project_name'].replace(' ', '+')

                    data = requests.get('https://www.livinginsider.com/a_project_list_json.php?term=' + term + '&_type=query&q=' + term)   

                r = httprequestObj.http_get('https://www.livinginsider.com/living_edit.php', params={'topic_id': postdata['post_id'], 'currentID': postdata['post_id']}, headers=headers, redirect=False)
                # print(r.url, "hi1")
                
                #print(r.status_code)
                #print(r.url)
                soup = BeautifulSoup(r.text, self.parser)
                csrf_token = soup.find('meta', {'name': 'csrf-token'}).get('content')
                typeposes = soup.find_all('input', {'name': 'web_post_type'})
                for typepose in typeposes:
                    if typepose.has_attr('checked'):
                        typep = typepose.get('value')
                detail_list = []
                options = soup.find_all('option')
                for opt in options:
                    if opt.has_attr('selected'):
                        detail_list.append(opt.get('value'))

                theprodid = int(detail_list[0])
                idzone = detail_list[1]
                web_zone = detail_list[2]

                data = {
                    'currentstep': '1',
                    'web_id': postdata['post_id'],
                    'web_member_type': '1',
                    'web_member_username': postdata['user'],
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
                    'state_renew': '',
                    'currentID': postdata['post_id']
                }

                referer = 'https://www.livinginsider.com/living_edit.php?topic_id=' + str(postdata['post_id']) + '&currentID=' + str(postdata['post_id'])

                headers = {
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'th-TH,th;q=0.9,en;q=0.8',
                    'Connection': 'keep-alive',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Host': 'www.livinginsider.com',
                    'Origin': 'https://www.livinginsider.com',
                    'Referer': referer,
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-origin',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36', 
                    'X-CSRF-TOKEN': csrf_token,
                    'X-Requested-With': 'XMLHttpRequest'
                }

                r = httprequestObj.http_post('https://www.livinginsider.com/a_edit_living.php', data=data, headers=headers)
                data = r.text
                #print(r.url)
                #print(r.status_code)
                #print(data)

                r = httprequestObj.http_get('https://www.livinginsider.com/living_edit2.php?topic_id='+ postdata['post_id'], headers=headers)
                #print('Page 2', r.status_code)
                soup = BeautifulSoup(r.text, self.parser)

                webFolder = soup.select_one('#web_photo_folder')['value']
                delete_params = soup.find_all('a', 'delete_img')

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

                post_id = postdata['post_id']
                if postdata['property_type'] == 3:
                    data = {
                        'currentstep': '2',
                        'web_id': post_id,
                        'web_area_size': 400 * int(land_size_rai) + 100 * int(land_size_ngan) + int(land_size_wa),
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
                        '$currentstep': '1',
                        'web_id': post_id,
                        'web_member_type': '1',
                        'web_member_username': postdata['user'],
                        'web_email': '',
                        'web_tel': '',
                        'web_lineid': '',
                        'web_post_type': str(typep),
                        'web_post_from': '2',
                        'web_building_type': str(theprodid),
                        'web_project_id': idzone,
                        'web_zone_id': str(web_zone),
                        'web_title': postdata['post_title_th'],
                        'web_description': postdata['post_description_th'],
                        'web_title_en': '',
                        'web_description_en': '',
                        'web_latitude': postdata['geo_latitude'],
                        'web_longitude': postdata['geo_longitude'],
                        'state_renew': ''
                    }

                    headers = {
                        'Connection': 'keep-alive',
                        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Mobile Safari/537.36',
                        'Sec-Fetch-Mode': 'navigate',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                        'Sec-Fetch-Site': 'same-origin',
                        'Referer': 'https://www.livinginsider.com/living_edit.php?topic_id=' + post_id,
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Content-Length': '6373',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                    }
                    r = httprequestObj.http_post('https://www.livinginsider.com/a_edit_living.php', data=data, headers=headers)
                    data = r.text
                    print(r.url)
                    print(data)
                    print(r.status_code)
                    print('Getting 2nd page')

                    headers = {
                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Mobile Safari/537.36',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-User': '?1',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                        'Sec-Fetch-Site': 'same-origin',
                        'Referer': 'https://www.livinginsider.com/living_edit.php?topic_id=' + post_id,
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                    }

                    params = (
                        ('topic_id', str(post_id)),
                    )


                    # k = httprequestObj.http_get('https://www.livinginsider.com/living_buysell2.php')
                    # soup = BeautifulSoup(k.text, self.parser)

                    r = httprequestObj.http_get('https://www.livinginsider.com/living_edit2.php', headers=headers, params=params)
                    print(r.url)
                    print(r.status_code)

                    soup = BeautifulSoup(r.text, self.parser)
                    # print(r.text)
                    webFolder = soup.select_one('#web_photo_folder')['value']

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
                    # webFolder = soup.select_one('#web_photo_folder')['value']

                    # webFolder = soup.find('input', {'id': 'web_photo_folder'}).get('value')
                    # print('WebFolder')
                    # webFolder = 'https://www.livinginsider.com/upload/topic415'
                    # print(webFolder)
                    print('UPLOADING PHOTOS')
                    for i in range(len(postdata['post_images'])):
                        filename = str(i) + '.jpeg'

                        datapost = [
                            ('files[]', (filename, open(postdata['post_images'][i], "rb"), "image/jpeg")),
                        ]
                        # print(f)
                        r = httprequestObj.http_post(img_link, data={'web_photo_folder': webFolder}, files=datapost)
                        print(r.url)
                        print(r.status_code)
                        # print(r.text)

                        if r.status_code == 200:
                            r = json.loads(r.text)
                            print(r)

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
                    print(filelist, "filelist")
                    postdata['floor'] = postdata['floor_total']
                    # folder = 'https://www.livinginsider.com/upload/topic415'
                    print(theprodid)
                    print(webFolder)
                    onlyfolder =  webFolder.split("/")[-1] + ' '
                    if theprodid == 3:
                        data = {
                            'currentstep': '2',
                            'web_id': post_id,
                            'web_area_size': 400 * int(land_size_rai) + 100 * int(land_size_ngan) + int(land_size_wa),
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
                            'web_photo_delete': '',
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
                        # onlyfolder = 'topic415 '
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
                            'web_area_size': 400 * int(land_size_rai) + 100 * int(land_size_ngan) + int(land_size_wa),
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
                            'web_area_size': 400 * int(land_size_rai) + 100 * int(land_size_ngan) + int(land_size_wa),
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
                            'web_area_size': 400 * int(land_size_rai) + 100 * int(land_size_ngan) + int(land_size_wa),
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

                r = httprequestObj.http_post('https://www.livinginsider.com/living_edit_confirm.php', params={'topic_id': post_id}, data=data)
                #print(r)

                    try:
                        r = BeautifulSoup(r.content, self.parser)
                        link = r.find('input', attrs={'id': 'link_copy'})['value']
                        post_id = post_url.split('/')[4]
                    except:
                        print(r.text)
                        print(r.url)
                        print(r.status_code)
                        r = json.loads(r.text)
                        link = r['link_copy']

                    t = 'https:\/\/www.livinginsider.com\/livingdetail\/495548\/1\/fsa.html'
                    if link == '':
                        detail = 'Not posted. Low Credits maybe.'
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

                t = 'https:\/\/www.livinginsider.com\/livingdetail\/495548\/1\/fsa.html'
                if link == '':
                    detail = 'Not posted. Low Credits maybe.'
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
                        "detail": 'Post edited successfully',
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
        data={}
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = ""
        post_url = ""
        mem_id = ''
        device_id = ''

        if success:
            page = 0

            post_found = False
            max_page = 100
            r = httprequestObj.http_get(
                'https://www.livinginsider.com/mystock.php?action=1&pages=1&pagelimit=50&actiontype=&posttype=&search_zone_id=&search_project_id=&web_id_for_publish=&web_id_hidden=&check_open_graph=&id_scroll=-1&search_bedroom=0&search_area=0&search_price=0&topic_sort=1&group_list=&searchword=')

            device_id = r.text.split("let device_id")[1].split("'")[1].split("'")[0]            
            mem_id = r.text.split("let mem_id")[1].split("'")[1].split("'")[0]            
            print(device_id)
            print(mem_id)
            soup = BeautifulSoup(r.content, self.parser)
            try:
                max_page = int(soup.find('ul', 'pagination').findChildren('li', recursive=False)[-3].find('a').string)
            except:
                max_page = 1
            while page <= max_page:
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
                r = httprequestObj.http_get('https://www.livinginsider.com/mystock.php', params=params)
                if r.history:
                    break
                soup = BeautifulSoup(r.content, self.parser)
                all_posts = soup.find_all(class_='mystock-item')
                for post in all_posts:
                    if str(post.get('topic-id')) == str(postdata['post_id']):
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
                headers = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                }
                r = httprequestObj.http_post('https://api.livinginsider.com/living_delete_reason.php', data=datapost, headers=headers)
                # print(r.url)
                # print(r.status_code)
                if r.text:
                    data = r.json()
                    # print(data)
                else:
                    detail = 'no content returned'

                datapost['web_id'] = post_id
                datapost['web_delete_reason_text'] = ''
                print(datapost)
                r = httprequestObj.http_post('https://api.livinginsider.com/my_living_topic_delete.php', data=datapost, headers=headers)
                print(r.status_code)
                print(r.text)
                # print(r.url)
                if r.text:
                    data = r.json()
                    if data['module'] == 'my_living_topic_delete':
                        success = True
                        detail = "Post deleted successfully"
                    else:
                        success = False
                        detail = 'Couldnot delete post'
                else:
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
        post_url = ""
        mem_id = ''
        device_id = ''

        if success:
            page = 0

            post_found = False
            max_page = 100
            r = httprequestObj.http_get(
                'https://www.livinginsider.com/mystock.php?action=1&pages=1&pagelimit=50&actiontype=&posttype=&search_zone_id=&search_project_id=&web_id_for_publish=&web_id_hidden=&check_open_graph=&id_scroll=-1&search_bedroom=0&search_area=0&search_price=0&topic_sort=1&group_list=&searchword=')
            device_id = r.text.split("let device_id")[1].split("'")[1].split("'")[0]            
            mem_id = r.text.split("let mem_id")[1].split("'")[1].split("'")[0]            

            soup = BeautifulSoup(r.content, self.parser)
            try:
                max_page = int(soup.find('ul', 'pagination').findChildren('li', recursive=False)[-3].find('a').string)
            except:
                max_page = 1
            while page <= max_page:
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
                r = httprequestObj.http_get('https://www.livinginsider.com/mystock.php', params=params)
                if r.history:
                    break
                soup = BeautifulSoup(r.content, self.parser)
                all_posts = soup.find_all(class_='mystock-item')
                for post in all_posts:
                    if str(post.get('topic-id')) == str(postdata['post_id']):
                        post_found = True
                        break
                if post_found:
                    break

            if post_found:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
                }
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
                if r.text:
                    data = r.json()

                    if data['result_msg'] == 'ดันประกาศเรียบร้อย':
                        success = True
                        detail = "Post boosted successfully"
                    else:
                        success = False
                        detail = 'Couldnot boost post'
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
            page = 1

            post_found = False
            max_page = 100
            r = httprequestObj.http_get(
                'https://www.livinginsider.com/mystock.php?action=1&pages=%d&pagelimit=50&actiontype=&posttype=&search_zone_id=&search_project_id=&web_id_for_publish=&web_id_hidden=&check_open_graph=&id_scroll=-1&search_bedroom=0&search_area=0&search_price=0&topic_sort=1&group_list=&searchword=' % page)
            soup = BeautifulSoup(r.content, self.parser)
            try:
                max_page = int(soup.find('ul', 'pagination').findChildren('li', recursive=False)[-3].find('a').string)
            except:
                max_page = 1
            while page <= max_page:

                # if page == max_page:
                #     print('\n\nsearched till max\n\n')

                r = httprequestObj.http_get('https://www.livinginsider.com/mystock.php?action=1&pages=%d&pagelimit=50&actiontype=&posttype=&search_zone_id=&search_project_id=&web_id_for_publish=&web_id_hidden=&check_open_graph=&id_scroll=-1&search_bedroom=0&search_area=0&search_price=0&topic_sort=1&group_list=&searchword=' % page)
                soup = BeautifulSoup(r.content, self.parser)

                all_posts = soup.find_all('div', attrs={'class':'mystock-item'})

                for post in all_posts:

                    # info = post.fin
                    post_url = str(post.find('a', attrs = {'target':'_blank'})['href'])
                    title = post.find('div', attrs={'class': "limit-title-ms"}).text  # .split(':').strip()
                    # print(title + '\n' + postdata['post_title_th'] + "\n\n")
                    if title in postdata['post_title_th'] :
                        # print('Found post')
                        post_found = "True"
                        detail = "Post Found"
                        post_id = post_url.split('/')[4]

                        post_view = ''

                        break
                page += 1
                if post_found:
                    break

            if not post_found:
                post_url = ''
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
            "post_created": '',
            "post_modified": "",
            "post_view": post_view,
            "post_url": post_url
        }

    def print_debug(self, msg):
        if self.debug == 1:
            print(msg)
        return True
