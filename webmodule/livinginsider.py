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

    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']
        username = user.replace("@","").replace(".","")
        # start process
        #
        success = "true"
        detail = ""

        datapost = {
            "email": user,
            "password": passwd,
            "repassword": passwd,
            "username": username,
            "mem_tel": postdata['tel']
        }
        # print(datapost)
        r = httprequestObj.http_post(
            'https://www.livinginsider.com/member_create.php', data=datapost)
        data = json.loads(r.text)
        if data['error_field'] != '':
            success = 'false'
            detail = data['result_msg']
        else:
            success = 'true'
            detail = 'Registered'
        # #
        # # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": 'livinginsider',
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            'ds_id': postdata['ds_id'],
            "detail": detail,
        }

    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user'].replace("@","").replace(".","")
        passwd = postdata['pass']
        # start process
        #
        success = "true"
        detail = "logged in"

        datapost = {
            'password': passwd,
            'username': user,

        }
        r = httprequestObj.http_post(
            'https://www.livinginsider.com/login.php', data=datapost)
        data = json.loads(r.text)
        # print(data)
        if data['status'] == True:
            success = 'true'
        else:
            success = data['status']
        detail = data['error']

        # r = httprequestObj.http_get('https://www.livinginsider.com/mystock.php?action=home')
        # with open('a.html','w') as f:
        #     print(r.text, file=f)

        #
        # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": 'livinginsider',
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
        }

    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""

        print('Here')

        proid = {
            'คอนโด': '1',                                               #condo
            'บ้านเดี่ยว': '2',                                              #detached houses /home / house / Single House
            'บ้านแฝด': '3',                                              #twin houses 
            'ทาวน์เฮ้าส์': '4',                                             #townhouses / town home / home office
            'ตึกแถว-อาคารพาณิชย์': '5',                                    #commercial buildings
            'ที่ดิน': '6',                                                 #land 
            'อพาร์ทเมนท์': '7',                                           #apartments
            'โรงแรม': '8',                                              #hotels, Real Estate Residencial
            'ออฟฟิศสำนักงาน': '9',                                       #Office
            'โกดัง-โรงงาน': '10',                                        #warehouses
            'โรงงาน': '25'                                              #factory
        }
        getProdId = {'1': 1, '2': 2, '3': 2, '4': 6,
                     '5': 4, '6': 3, '7': 10, '8': 10, '9': 5, '10': 12, '25': 11}

        print(getProdId)

        try:
            # print('try')
            theprodid = getProdId[proid[str(postdata['property_type'])]]
        except:
            # print('except')
            theprodid = getProdId[str(postdata['property_type'])]

        print(theprodid)

        if 'web_project_name' not in postdata or postdata['web_project_name'] != None:
            if 'project_name' in postdata and postdata['project_name'] != None:
                postdata['web_project_name'] = postdata['project_name']
            else:
                postdata['web_project_name'] = postdata['post_title_th']

        if 'floor_total' not in postdata:
            postdata['floor_total'] = 1
        elif postdata['floor_total'] == None or postdata['floor_total'] == '':
            postdata['floor_total'] = 1

        if 'floor_level' not in postdata:
            postdata['floor_level'] = 1
        elif postdata['floor_level'] == None or postdata['floor_level'] == '':
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

        data = requests.get(
            'https://www.livinginsider.com/a_project_list_json.php?term='+term+'&_type=query&q='+term)
        # print(data.url)
        data = json.loads(data.text)

        if len(data) == 1:
            term = postdata['addr_district']+'+'+postdata['addr_province']
            data = requests.get(
                'https://www.livinginsider.com/a_project_list_json.php?term='+term+'&_type=query&q='+term)
            data = json.loads(data.text)
            # print(data)
            try: 
                idzone = data[1]['id']
            except:
                idzone = data[0]['id']
        else:
            idzone = data[1]['id']
        # print(idzone)
        data = requests.post(
            'https://www.livinginsider.com/a_project_child.php', data={'web_project_id': idzone})
        data = json.loads(data.text)
        r = data['value']
        soap = BeautifulSoup(r,'html.parser')
        option = soap.find('option')
        option = option['value']
        # print(option)
        prod_address = ""
        for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
            if add is not None or add == "" or add == " ":
                prod_address += add + ","
       
        prod_address = prod_address[:-1]
        if postdata['listing_type'] != 'ขาย':
            typep = 4
        else:
            typep = 1

        if success == "true":
            # datapost = [
            #     ('currentstep', 1),
            #     ('web_member_type', 1),
            #     ('web_post_from', 2),
            #     ('web_post_type', typep),
            #     ('web_title', postdata['post_title_th']),
            #     ('web_description', postdata['post_description_th']),
            #     ('web_post_id', idzone),
            #     ('web_building_type', theprodid),
            #     ('web_latitude', postdata['geo_latitude']),
            #     ('web_longitude', postdata['geo_longitude']),
            #     ('web_zone_id', option)
            # ]

            data = {
            'currentstep': '1',
            'web_member_type': '1',
            'web_member_username':  postdata['user'],
            'web_email': '',
            'web_tel': '',
            'web_lineid': '',
            'web_post_type': typep,
            'web_post_from': '2',
            'web_building_type': theprodid,
            'web_project_id': idzone,
            'web_zone_id': option,
            'web_title': postdata['post_title_th'],
            'web_description': postdata['post_description_th'],
            'web_title_en': '',
            'web_description_en': '',
            'web_latitude': postdata['geo_latitude'],
            'web_longitude': postdata['geo_longitude']
            }

            r = httprequestObj.http_post(
                'https://www.livinginsider.com/a_add_living.php', data=data)
            data = r.text
            print(r.text)
            img_link = 'https://www.livinginsider.com/js_upload/php/'
            arr = ["files[]"]
            folders = ''
            filelist = ''
            onlyfolder = ''
            files = []
            start = 1
            f={}
            data={}
            k = httprequestObj.http_get('https://www.livinginsider.com/living_buysell2.php')
            print(k.status_code)
            soup = BeautifulSoup(k.text,'html.parser')
            webFolder = soup.select_one('#web_photo_folder')['value']

            # print(webFolder)

            for i in range(len(postdata['post_images'])):
                f[arr[0]] = (postdata['post_images'][i], open(
                    postdata['post_images'][i], "rb"), "image/jpeg")
                # print(f)
                r = httprequestObj.http_post(img_link, data={ 'web_photo_folder': webFolder}, files=f)
                r=json.loads(r.text)
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
                filelist += file+"||"
                files.append(file)
            postdata['floor'] = postdata['floor_total']
            if (postdata['property_type'] == 3):
                data = {
                    'currentstep': '2',
                    'web_area_size': 400*land_size_rai + 100 * land_size_ngan + 1*land_size_wa,
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
                    'web_photo_folder': folder,
                }
                for i in range(len(postdata['post_images'])):
                    data['web_photo_caption[' +
                         str(i)+'][web_folder]'] = onlyfolder
                    data['web_photo_caption['+str(i)+'][web_id]'] = ''
                    data['web_photo_caption['+str(i)+'][photoname]'] = files[i]
                    data['web_photo_caption['+str(i)+'][caption]'] = ''
            elif (theprodid == 1):
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
                    'web_photo_folder': folder,
                    'web_fq': '0',
                    'web_youtube': '',
                    'web_useful_space': '0',
                }
                for i in range(len(postdata['post_images'])):
                    data['web_photo_caption[' +
                         str(i)+'][web_folder]'] = onlyfolder[:-1]
                    data['web_photo_caption['+str(i)+'][web_id]'] = ''
                    data['web_photo_caption['+str(i)+'][photoname]'] = files[i]
                    data['web_photo_caption['+str(i)+'][caption]'] = ''
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
                    'web_photo_folder': folder,
                    'web_fq': '0',
                    'web_youtube': '',
                    'web_useful_space': '0',
                }
                for i in range(len(postdata['post_images'])):
                    data['web_photo_caption[' +
                         str(i)+'][web_folder]'] = onlyfolder
                    data['web_photo_caption['+str(i)+'][web_id]'] = ''
                    data['web_photo_caption['+str(i)+'][photoname]'] = files[i]
                    data['web_photo_caption['+str(i)+'][caption]'] = ''
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
                    'web_photo_folder': folder,
                    'web_fq': '0',
                    'web_youtube': '',
                    'web_useful_space': postdata['floor_area'],
                }
                for i in range(len(postdata['post_images'])):
                    data['web_photo_caption[' +
                         str(i)+'][web_folder]'] = onlyfolder
                    data['web_photo_caption['+str(i)+'][web_id]'] = ''
                    data['web_photo_caption['+str(i)+'][photoname]'] = files[i]
                    data['web_photo_caption['+str(i)+'][caption]'] = ''

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
                    'web_photo_folder': folder,
                    'web_fq': '0',
                    'web_youtube': '',
                    'web_useful_space': postdata['floor_area'],
                }
                for i in range(len(postdata['post_images'])):
                    data['web_photo_caption[' +
                         str(i)+'][web_folder]'] = onlyfolder
                    data['web_photo_caption['+str(i)+'][web_id]'] = ''
                    data['web_photo_caption['+str(i)+'][photoname]'] = files[i]
                    data['web_photo_caption['+str(i)+'][caption]'] = ''

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
                    'web_photo_folder': folder,
                    'web_fq': '0',
                    'web_youtube': '',
                    'web_useful_space': '0',
                }
                for i in range(len(postdata['post_images'])):
                    data['web_photo_caption[' +
                         str(i)+'][web_folder]'] = onlyfolder
                    data['web_photo_caption['+str(i)+'][web_id]'] = ''
                    data['web_photo_caption['+str(i)+'][photoname]'] = files[i]
                    data['web_photo_caption['+str(i)+'][caption]'] = ''

            elif theprodid==10:
                data = {
                    'currentstep': '2',
                    'web_room': postdata['bed_room'],
                    'web_floor': postdata['floor_total'],
                    'web_area_size': 400*land_size_rai + 100 * land_size_ngan + 1*land_size_wa,
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
                    'web_photo_folder': folder,
                    'web_fq': '0',
                    'web_youtube': '',
                    'web_useful_space': '0',
                }
                for i in range(len(postdata['post_images'])):
                    data['web_photo_caption[' +
                         str(i)+'][web_folder]'] = onlyfolder
                    data['web_photo_caption['+str(i)+'][web_id]'] = ''
                    data['web_photo_caption['+str(i)+'][photoname]'] = files[i]
                    data['web_photo_caption['+str(i)+'][caption]'] = ''
            elif theprodid == 12:
                data = {
                    'currentstep': '2',
                    'web_room': postdata['bed_room'],
                    'web_floor': '0',
                    'web_area_size': 400*land_size_rai + 100 * land_size_ngan + 1*land_size_wa,
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
                    'web_photo_folder': folder,
                    'web_fq': '0',
                    'web_youtube': '',
                    'web_useful_space': postdata['floor_area'],
                }
                for i in range(len(postdata['post_images'])):
                    data['web_photo_caption[' +
                         str(i)+'][web_folder]'] = onlyfolder
                    data['web_photo_caption['+str(i)+'][web_id]'] = ''
                    data['web_photo_caption['+str(i)+'][photoname]'] = files[i]
                    data['web_photo_caption['+str(i)+'][caption]'] = ''
            elif theprodid == 11:
                data = {
                    'currentstep': '2',
                    'web_room': '0',
                    'web_floor': '0',
                    'web_area_size': 400*land_size_rai + 100 * land_size_ngan + 1*land_size_wa,
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
                    'web_photo_folder': folder,
                    'web_fq': '0',
                    'web_youtube': '',
                    'web_useful_space': postdata['floor_area'],
                }
                for i in range(len(postdata['post_images'])):
                    data['web_photo_caption[' +
                         str(i)+'][web_folder]'] = onlyfolder
                    data['web_photo_caption['+str(i)+'][web_id]'] = ''
                    data['web_photo_caption['+str(i)+'][photoname]'] = files[i]
                    data['web_photo_caption['+str(i)+'][caption]'] = ''
            print(data)
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
            r = httprequestObj.http_post(
                'https://www.livinginsider.com/a_add_living.php', data=data, headers = headers)
            print(r.status_code)

            data = {
            'action': 'save',
            'web_status': '1',
            'publish_flag': '1'
            }

            r = httprequestObj.http_get('https://www.livinginsider.com/living_confirm.php')

            with open('b.html','w') as f:
                print(r.text,file=f)

            r = httprequestObj.http_post('https://www.livinginsider.com/living_confirm.php',data=data)
            print(r.status_code)
            # print(r.text)
            try:
                r = BeautifulSoup(r.content,'html.parser')
                link = r.find('input',attrs={'id':'link_copy'})['value']
                print(link)
            except:
                print(r.text)
                r=json.loads(r.text)
                link=r['link_copy']
            print(link)
            t = 'https:\/\/www.livinginsider.com\/livingdetail\/495548\/1\/fsa.html'
            if link=='':
                detail='not posted'
                success=False
                time_end = datetime.datetime.utcnow()
                time_usage = time_end - time_start
                return {
                    "success": success,
                    "websitename":"livinginsider",
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
                "websitename":"livinginsider",
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
            "websitename":"livinginsider",
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
        }

    def edit_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process

        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = ""
        post_id = ""
        post_url = ""

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
            'โกดัง-โรงงาน': '10'
        }
        getProdId = {'1': 159, '2': 156, '3': 157, '4': 157,
                     '5': 158, '6': 161, '7': 162, '8': 162, '9': 162, '10': 162}

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
        elif postdata['floor_total'] == None or postdata['floor_total'] == '':
            postdata['floor_total'] = 1

        if 'floor_level' not in postdata:
            postdata['floor_level'] = 1
        elif postdata['floor_level'] == None or postdata['floor_level'] == '':
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

        data = requests.get(
            'https://www.livinginsider.com/a_project_list_json.php?term='+term+'&_type=query&q='+term)
        # print(data.url)
        data = json.loads(data.text)

        if len(data) == 1:
            term = postdata['addr_district']+'+'+postdata['addr_province']
            data = requests.get(
                'https://www.livinginsider.com/a_project_list_json.php?term='+term+'&_type=query&q='+term)
            data = json.loads(data.text)
            print("data", data)
            try: 
                idzone = data[1]['id']
            except:
                idzone = data[0]['id']
        else:
            idzone = data[1]['id']
        print("idzone", idzone)

        data = requests.post(
            'https://www.livinginsider.com/a_project_child.php', data={'web_project_id': idzone})
        data = json.loads(data.text)
        print("data", data)
        r = data['value']
        if r == '':
            data = requests.get(
                'https://www.livinginsider.com/a_project_list_json.php?term=a&_type=query&q=a')
            data = json.loads(data.text)
            try:
                idzone = data[1]['id']
            except:
                idzone = data[0]['id']
            data = requests.post(
                'https://www.livinginsider.com/a_project_child.php', data={'web_project_id': idzone})
            data = json.loads(data.text)
            r = data['value']


        soap = BeautifulSoup(r,'html.parser')
        option = soap.find('option')
        option = option['value']
        # for i in postdata["post_img_url_lists"]:

        # for (key, value) in provincedata.items():
        #     if type(value) is str and postdata['addr_province'].strip() in value.strip():
        #         province_id = key
        #         print("yes")
        #         break

        prod_address = ""
        for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
            if add is not None:
                prod_address += add
        prod_address = prod_address[:-1]
        # resp = requests.get(image_url, stream=True)
        files = {}
        if success == "true":

            datapost = [
                ('id', postdata['post_id']),
                ('cate_id', '23'),
                ('sub_cate_id', theprodid),
                ('post_title', postdata['post_title_th']),
                ('post_s_detail', postdata['post_description_th']),
                ('post_price_type', '2'),
                ('post_price', postdata['price_baht']),
                ('add', prod_address),
                # ('province', province_id),
                ('name', postdata['name']),
                ('email', postdata['email']),
                ('tel', postdata['mobile']),
                ('web_zone_id', option),
                ('rands', 'ZF71'),
                ('capcha', 'ZF71'),
                ('submit', 'Confirm announcement'),
            ]
            allimages = postdata["post_images"][:5]
            for i in range(len(allimages)):
                r = open(os.getcwd()+"/"+allimages[i], 'rb')
                if i == 0:
                    files['fileshow'] = r
                else:
                    files["file"+str(i)] = r

            r = httprequestObj.http_post(
                'http://www.livinginsider.com/a_edit_living.php', data=datapost, files=files)
            data = r.text
            print(data)
        else:
            detail = "cannot login"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_id": postdata['post_id'],
            "account_type": "null",
            "detail": detail,
            "websitename": "livinginsider",
        }

    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # TODO ประกาศที่ทดสอบไป ยังไม่ครบ 7 วัน ทำทดสอบการลบไม่ได้ วันหลังค่อยมาทำใหม่
        user = postdata['user']
        passwd = postdata['pass']

        # start process
        #
        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        if success == "true":
            r = httprequestObj.http_get(
                'http://www.quickdealfree.com/member/del-classifieds.php?id='+postdata['post_id'])
            data = r.text
        else:
            detail = "cannot login"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "log_id": 1,
            "websitename": "livinginsider",
        }

    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        post_id = postdata['post_id']
        log_id = postdata['log_id']

        #
        #

        time_end = datetime.datetime.utcnow()
        return {
            "success": "false",
            "time_usage": time_end - time_start,
            "time_start": time_start,
            "time_end": time_end,
            "detail": "",
            "log_id": log_id,
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

            while True:
                page += 1
                url = 'https://www.livinginsider.com/public_profile/' + str(page) + '/fyIeC.html'
                try:
                    r = httprequestObj.http_get(url)
                except:
                    # print('No more pages')
                    break
                # print(r.url)
                # print(r.status_code)

                soup = BeautifulSoup(r.content, 'html.parser')
                all_posts = soup.find_all('div', 'item-desc')
                # print(len(all_posts))

                if len(all_posts) == 0:
                    break

                for post in all_posts:
                    info = post.findChildren('div', recursive=False)
                    post_url = info[0].find('div').find('a').get('href')
                    title = info[0].find('div').find('a').get('title')  # .split(':').strip()
                    # print(title)

                    if postdata['post_title_th'] in title:
                        # print('Found post')
                        post_found = True
                        detail = "Post Found"
                        post_id = post_url.split('/')[-2]
                        post_modified = str(info[1].find('div').find_all('div')[0].contents[2])
                        # print(post_modified)
                        post_view = str(info[1].find('div').find_all('div')[1].contents[2])
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

    def print_debug_data(self, data):
        if(self.debugdata == 1):
            print(data)
        return True

        if(self.debugdata == 1):
            print(data)
        return True


# tri = livinginsider()
# dic = {
#     "action": "create_post",
#     "timeout": "5",
#     "post_images": [
#          '../../../../../Pictures/cafeTerrance.jpeg',
#     ],
#     "name_th": "อัมรินทร์abz",
#     "surname_th": "บุญเกิด",
#     "geo_latitude": "13.786862",
#     "geo_longitude": "100.757815",
#     "property_id": "",
#     "post_title_th": "newxxxx",
#     "short_post_title_th": "xxxxxx",
#     "post_description_th": "ขายที่ดินด่วน บางกรวยไทรน้อย 6\n ไร่ เหมาะทำตลาดรายละเอียดที่ดินขนาด 6\n ไร่หน้ากว้าง 30 เมตร ติดถนนบางกรวยไทรน้อยที่ดินยังไม่ถมต่ำกว่าถนนประมาณ 1 เมตรสถานที่ใกล้เคียงถนนพระราม5ถนนนครอินทร์ให้เช่าระยะยาว\n 100,000 บาท ต่อเดือนสนใจติดต่อ คุณชู 0992899999line: 0992899999",
#     "post_title_en": "",
#     "short_post_title_en": "xxx",
#     "post_description_en": "",
#     "price_baht": "3000",
#     "project_name": "ลุมพีนีวิลล รามอินทราหลักสี่",

#     "listing_type": "ขาย",
#     "property_type": '1',
#     "floor_level": '4',
#     "floor_total": '3',
#     "floor_area": '2',
#     "bath_room": '2',
#     "bed_room": '4',
#     "prominent_point": "จุดเด่น",
#     "view_type": "11",
#     "direction_type": "11",
#     "addr_province": "กระบี่",
#     "addr_district": "เกาะลันตา",
#     "addr_sub_district": "คลองยาง",
#     "addr_road": "ถนน",
#     "addr_soi": "ซอย",
#     "addr_near_by": "สถานที่ใกล้เคียง",
#     "floorarea_sqm": "พื้นที่",

#     "land_size_rai": "10",
#     "land_size_ngan": "1",
#     "land_size_wa": "12",

#     "name": "user_name_haha",
#     "mobile": "0872379469",
#     "tel": "0899999999",
#     "email": "new@dfb55.com",
#     "line": "9899999999",
#     "ds_name": "thaihometown",`
#     "ds_id": "4",
#     "user": "new@dfb55.com",
#     "pass": "12345678",
#     "post_id": "5e9e069b20aaba0019a465b8"
# }
# print(tri.create_post(dic))
# print(tri.register_user(dic))
