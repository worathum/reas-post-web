# -*- coding: utf-8 -*-
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
# from urlparse import urlparse
import re
import json
import datetime
import time
import sys
import urllib.request
from urllib.parse import unquote

property_mapping={'กระบี่': '117', 'กรุงเทพมหานคร': '54', 'กาญจนบุรี': '109', 'กาฬสินธุ์': '87', 'กำแพงเพชร': '102', 'ขอนแก่น': '81', 'จันทบุรี': '66', 'ฉะเชิงเทรา': '68', 'ชลบุรี': '64', 'ชัยนาท': '62', 'ชัยภูมิ': '78', 'ชุมพร': '122', 'ตรัง': '125', 'ตราด': '67', 'ตาก': '103', 'นครนายก': '70', 'นครปฐม': '111', 'นครพนม': '89', 'นครราชสีมา': '72', 'นครศรีธรรมราช': '116', 'นครสวรรค์': '100', 'นนทบุรี': '56', 'นราธิวาส': '129', 'น่าน': '96', 'บุรีรัมย์': '73', 'ปทุมธานี': '57', 'ประจวบคีรีขันธ์': '115', 'ปราจีนบุรี': '69', 'ปัตตานี': '127', 'พระนครศรีอยุธยา': '58', 'พะเยา': '97', 'พังงา': '118', 'พัทลุง': '126', 'พิจิตร': '106', 'พิษณุโลก': '105', 'ภูเก็ต': '119', 'มหาสารคาม': '85', 'มุกดาหาร': '90', 'ยะลา': '128', 'ยโสธร': '77', 'ระนอง': '121', 'ระยอง': '65', 'ราชบุรี': '108', 'ร้อยเอ็ด': '86', 'ลพบุรี': '60', 'ลำปาง': '93', 'ลำพูน': '92', 'ศรีสะเกษ': '75', 'สกลนคร': '88', 'สงขลา': '123', 'สตูล': '124', 'สมุทรปราการ': '55', 'สมุทรสงคราม': '113', 'สมุทรสาคร': '112', 'สระบุรี': '63', 'สระแก้ว': '71', 'สิงห์บุรี': '61', 'สุพรรณบุรี': '110', 'สุราษฎร์ธานี': '120', 'สุรินทร์': '74', 'สุโขทัย': '104', 'หนองคาย': '84', 'หนองบัวลำภู': '80', 'อำนาจเจริญ': '79', 'อุดรธานี': '82', 'อุตรดิตถ์': '94', 'อุทัยธานี': '101', 'อุบลราชธานี': '76', 'อ่างทอง': '59', 'เชียงราย': '98', 'เชียงใหม่': '91', 'เพชรบุรี': '114', 'เพชรบูรณ์': '107', 'เลย': '83', 'แพร่': '95', 'แม่ฮ่องสอน': '99'}
def get_security(flag1, post_id=''):
    if flag1 == 0:

        web = httprequestObj.http_get_with_headers('https://www.proptecheasy.com/#')
        soup = BeautifulSoup(web.content, 'lxml')
        # with open('temp','w') as f:
        #     f.write(str(soup))
        arr = soup.find_all('script')
        var = ""
        for script1 in arr:
            json_string = re.search(
                r"pfget_usersystemhandler\"\:\"...........", str(script1))
            if json_string:
                temp_ind = json_string.group(0).index(
                    'pfget_usersystemhandler')+len('"pfget_usersystemhandler":"')-1

                var = json_string.group(0)[temp_ind:temp_ind+10]
        return var
    if flag1 == 6:
        url = 'https://www.proptecheasy.com/dashboard/?ua=myitems'
        headers = {
            'authority': 'www.proptecheasy.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'sec-fetch-site': 'same-origin',
            'referer': 'https://www.proptecheasy.com/dashboard/?ua=myitems',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        web = httprequestObj.http_get(url,headers=headers)
        web=web.content
        soup = BeautifulSoup(web, 'lxml')
        # with open('temp','w') as f:
        #     f.write(str(soup))
        arr = soup.find_all('script')
    
        var = ""
        for script1 in arr:
            json_string = re.search(
                r"pfget_itemsystem\"\:\"...........", str(script1))
            if json_string:
                temp_ind = json_string.group(0).index(
                    'pfget_itemsystem')+len('"pfget_itemsystem":"')-1

                var = json_string.group(0)[temp_ind:temp_ind+10]
        return var

# for image
    elif flag1 == 1:
        headers = {
            'authority': 'www.proptecheasy.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'sec-fetch-site': 'none',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        web = httprequestObj.http_get(
            'https://www.proptecheasy.com/dashboard/?ua=newitem', headers=headers)

        web = web.content
        soup = BeautifulSoup(web, 'lxml')
        with open('temp', 'w') as f:
            f.write(str(soup))

        arr = soup.find_all('script')
        var = ""
        ret = ""
        for script1 in arr:
            index = str(script1).find('security')
            if index != -1:
                ret = str(script1)[index+11:index+11+10]
                return ret
        return ret
# for create post
    elif flag1 == 2:
        headers = {
            'authority': 'www.proptecheasy.com',
            'cache-control': 'max-age=0',
            'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'upgrade-insecure-requests': '1',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'sec-fetch-site': 'none',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        web = httprequestObj.http_get(
            'https://www.proptecheasy.com/dashboard/?ua=newitem', headers=headers)

        web = web.content
        soup = BeautifulSoup(web, 'lxml')
        var = soup.find('input', attrs={'name': 'security'})['value']
        return str(var)
# final in create post
    elif flag1 == 3:
        headers = {
            'authority': 'www.proptecheasy.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'sec-fetch-site': 'none',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        web = httprequestObj.http_get(
            'https://www.proptecheasy.com/dashboard/?ua=newitem', headers=headers)

        web = web.content
        soup = BeautifulSoup(web, 'lxml')
        with open('temp', 'w') as f:
            f.write(str(soup))

        arr = soup.find_all('script')
        var = ""
        ret = ""
        for script1 in arr:
            index = str(script1).find('pfget_itemsystem')
            if index != -1:
                ret = str(script1)[index+len('pfget_itemsystem":"')
                          :index+len('pfget_itemsystem":"')+10]
                return ret
        return ret
    elif flag1 == 4:
        headers = {
            'authority': 'www.proptecheasy.com',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'sec-fetch-site': 'same-origin',
            'referer': 'https://www.proptecheasy.com/dashboard/?ua=myitems',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        params = (
            ('ua', 'edititem'),
            ('i', post_id),
        )

        web = httprequestObj.http_get(
            'https://www.proptecheasy.com/dashboard/', headers=headers, params=params)
        web = web.content
        with open('temp.html', 'w') as f:
            f.write(str(web))
        soup = BeautifulSoup(web, 'lxml')
        var = soup.find('input', attrs={'name': 'security'})['value']
        return str(var)
    elif flag1 == 5:
        headers = {
            'authority': 'www.proptecheasy.com',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'sec-fetch-site': 'same-origin',
            'referer': 'https://www.proptecheasy.com/dashboard/?ua=myitems',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        params = (
            ('ua', 'edititem'),
            ('i', post_id),
        )

        web = httprequestObj.http_get(
            'https://www.proptecheasy.com/dashboard/', headers=headers, params=params)
        web = web.content
        soup = BeautifulSoup(web, 'lxml')
        with open('temp', 'w') as f:
            f.write(str(soup))

        arr = soup.find_all('script')
        var = ""
        ret = ""
        for script1 in arr:
            index = str(script1).find('pfget_itemsystem')
            if index != -1:
                ret = str(script1)[index+len('pfget_itemsystem":"'):index+len('pfget_itemsystem":"')+10]
                return ret
        return ret
    # for image edit


def upload_image(img_add,security_code):
    url = 'https://www.proptecheasy.com/wp-content/plugins/pointfindercoreelements/includes/pfajaxhandler.php'
    files = {'file': (img_add, open(
        img_add, 'rb'), 'image/jpeg')}

    data = {
        'action': 'pfget_imageupload',
        'security': security_code,
        'file': files,
    }
    headers = {
        'Host': 'www.proptecheasy.com',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cache-Control': 'no-cache',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.proptecheasy.com',
        'Connection': 'keep-alive',
        'Referer': 'https://www.proptecheasy.com/dashboard/?ua=newitem',
        'Pragma': 'no-cache',
    }
    response = httprequestObj.http_post(
        'https://www.proptecheasy.com/wp-content/plugins/pointfindercoreelements/includes/pfajaxhandler.php', headers=headers, data=data, files=files)
    if 'X-WP-Upload-Attachment-ID' in response.headers.keys():
        temp = response.headers['X-WP-Upload-Attachment-ID']
    else:
        temp = -1
    return temp


httprequestObj = lib_httprequest()


class proptecheasy():

    name = 'proptecheasy'

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
        # with open("./static/ploychao_province.json") as f:
        #     self.provincedata = json.load(f)
        # product categ id
        # self.getProdId = {'1': 24, '2': 25, '3': 26, '4': 27,
        #   '5': 29, '6': 34, '7': 28, '8': 14, '9': 31, '10': 33}

    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        user = postdata['user'].replace("@", "%40")
        passwd = postdata['pass'].replace("@", "%40")
        name_th = postdata["name_th"].replace("@", "%40")
        surname_th = postdata["surname_th"].replace("@", "%40")
        if 'email' in postdata:
            email = postdata['email'].replace("@", "%40")
        else:
            email = postdata['user'].replace('@',"%40")
        phone = postdata['tel']
        try:
            company_name = postdata['company_name']
        except:
            company_name = name_th
        # start process
        success = "true"
        detail = ""
        formtype = 'register'
        vars = ''
        vars = 'username='+user + '&pass='+passwd + '&firstname=' + \
            name_th+'&email='+email+'&mobile='+phone+'&pftermsofuser=1'

        datapost = {
            'action': 'pfget_usersystemhandler',
            'formtype': 'register',
            'vars': vars,
            'lang': 'th',
            'security': get_security(0)

        }
        headers = {
            'sec-fetch-mode': 'cors',
            'origin': 'https://www.proptecheasy.com',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'referer': 'https://www.proptecheasy.com/',
            'authority': 'www.proptecheasy.com',
            'sec-fetch-site': 'same-origin',
        }
        r = httprequestObj.http_post(
            'https://www.proptecheasy.com/wp-content/plugins/pointfindercoreelements/includes/pfajaxhandler.php', headers=headers, data=datapost)

        # r = httprequestObj.http_post(
        #     'https://www.proptecheasy.com/wp-content/plugins/pointfindercoreelements/includes/pfajaxhandler.php', data=datapost,headers=headers)
        data = r.text
        temp_json = json.loads(data)

        if data == '' or data == '0' or data == '-1' or 'Success' not in temp_json['mes']:
            success = "false"
        else:
            detail = temp_json['mes']

        # # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "proptecheasy",
            "success": success,
            "start_time": str(time_start),
            "usage_time": str(time_usage),
            "end_time": str(time_end),
            "detail": detail,
        }

    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user'].replace("@", "%40")
        passwd = postdata['pass']
        headers = {
            'sec-fetch-mode': 'cors',
            'origin': 'https://www.proptecheasy.com',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'referer': 'https://www.proptecheasy.com/',
            'authority': 'www.proptecheasy.com',
            'sec-fetch-site': 'same-origin',
        }
        vars = 'username='+user+'&password='+passwd+'&rem=on&redirectpage=0'
        datapost = {
            'action': 'pfget_usersystemhandler',
            'formtype': 'login',
            'vars': vars,
            'lang': 'th',
            'security': get_security(0),
        }

        success = "true"
        detail = ""

        r = httprequestObj.http_post(
            'https://www.proptecheasy.com/wp-content/plugins/pointfindercoreelements/includes/pfajaxhandler.php', headers=headers, data=datapost)
        get_security(1)
        data = json.loads(r.text)
        if data['login'] == 'false' or data['login'] == 'False' or data['login'] == False:
            success = "false"
            detail = "cannot login"
        # elif str(data) == '2':
        #     success = "false"
        #     detail = "account suspended"
        else:
            detail = "login successful"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "proptecheasy",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
        }

    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        success = "true"
        detail = ""
        post_url = ""
        post_id = ""

        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]

        if 'addr_soi' in postdata and postdata['addr_soi'] != None:
            pass
        else:
            postdata['addr_soi'] = ''
        if 'addr_road' in postdata and postdata['addr_soi'] != None:
            pass
        else:
            postdata['addr_road'] = ''

        prod_address = ""
        for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
            if add is not None:
                prod_address += add + ","
        prod_address = prod_address

        if success == "true":
            if 'prominent_point' not in postdata or postdata['prominent_point'] == None:
                postdata['prominent_point'] = ''
            if 'floor_area' not in postdata or postdata['floor_area'] == None:
                postdata['floor_area'] = '0'
            if 'floor_total' in postdata and postdata['floor_total'] != None:
                floor_total = str(postdata['floor_total'])
            else:
                floor_total = '7'
            if 'bedroom' in postdata and postdata['bedroom'] != None:
                bedroom = str(postdata['bedroom'])
            else:
                bedroom = '7'
            if 'bathroom' in postdata and postdata['bathroom'] != None:
                bathroom = str(postdata['bathroom'])
            else:
                bathroom = '7'
            if 'land_area_ngan' not in postdata or str(postdata['land_area_ngan']) == None:
                postdata['land_area_ngan'] = '0'
            if 'land_area_rai' not in postdata or str(postdata['land_area_rai']) == None:
                postdata['land_area_rai'] = '0'
            if 'land_area_wa' not in postdata or str(postdata['land_area_wa']) == None:
                postdata['land_area_wa'] = '0'

            if 'land_size_ngan' not in postdata or postdata['land_size_ngan'] == None:
                postdata['land_size_ngan'] = '0'
            if 'land_size_rai' not in postdata or postdata['land_size_rai'] == None:
                postdata['land_size_rai'] = '0'
            if 'land_size_wa' not in postdata or postdata['land_size_wa'] == None:
                postdata['land_size_wa'] = '0'
            if 'project_name' not in postdata:
                postdata['project_name'] = postdata['post_title_th']
            if len(postdata['post_images']) == 0:
                postdata['post_images'] = ['imgtmp/default/white.jpg']

            prod_address = ""
            for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
                if add is not None:
                    prod_address += add
            prod_address = prod_address[:-1]
            upload_id = ''
            security_code=get_security(1)

            for i in postdata['post_images']:
                temp = upload_image(i,security_code)
                if temp != -1:
                    if upload_id != '':
                        upload_id = str(upload_id)+'%2c'+temp
                    else :
                        upload_id=temp
            # upload_id = upload_image('download.jpeg')
            if upload_id == '':
                success = "false"

            headers = {
                'Host': 'www.proptecheasy.com',
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Length': '920',
                'Origin': 'https://www.proptecheasy.com',
                'Connection': 'keep-alive',
                'Referer': 'https://www.proptecheasy.com/dashboard/?ua=newitem',
                'TE': 'Trailers', }
            



            if postdata['listing_type'] == 'ขาย':  # sell
                type_prop = 13
            else:
                type_prop = 12  # rent

            if postdata['property_type'] == 'คอนโด' or int(postdata['property_type']) == 1:
                prop = 34
                area = str(postdata['floor_area'])

            elif int(postdata['property_type']) == 4 or postdata['property_type'] == 'ทาวน์โฮม ทาวน์เฮ้าส์':
                area = str(postdata['floor_area'])
                prop = 49
            elif int(postdata['property_type']) == 2 or postdata['property_type'] == 'บ้านเดี่ยว' or int(postdata['property_type'])==3:
                area = str(postdata['floor_area'])
                prop = 31
            elif postdata['property_type'] == 'อพาร์ทเมนท์' or int(postdata['property_type']) == 7:
                area = str(postdata['floor_area'])
                prop = 32
            elif postdata['property_type'] == 'ที่ดินเปล่า' or int(postdata['property_type']) == 6:
                prop = 51
                ans = 0
                if postdata['land_size_rai'] != '0':
                    ans += 400*float(postdata['land_size_rai'])
                if postdata['land_size_ngan'] != '0':
                    ans += 100*float(postdata['land_size_ngan'])
                if postdata['land_size_wa'] != '0':
                    ans += float(postdata['land_size_wa'])
                area = ans*4  # (In sqm)
            elif postdata['property_type'] == 'อาคาร พื้นที่สำนักงาน' or int(postdata['property_type'] )== 9:
                area = str(postdata['floor_area'])
                prop = 20
            elif postdata['property_type'] == 'อาคารพาณิชย์' or int(postdata['property_type']) == 5:
                area = str(postdata['floor_area'])
                prop = 50
            elif int(postdata['property_type']) == 10:
                area = str(postdata['floor_area'])
                prop = 26
            elif int(postdata['property_type']) == 25:
                area = str(postdata['floor_area'])
                prop = 53
            elif int(postdata['property_type']) == 8:
                area = str(postdata['floor_area'])
                prop = 52
            else:
                area = str(postdata['floor_area'])
                prop = 34

            if 'floor_level' not in postdata or postdata['floor_level'] is None:
                postdata['floor_level'] = ''

            for pm in property_mapping.keys():
                if postdata['addr_province'] in pm:
                    province = property_mapping[pm]
            else:
                province = '117'


            dt = 'pfupload_listingtypes='+str(type_prop)+'&pfupload_listingpid=&pfupload_type=1&pfupload_c=&pfupload_f=&pfupload_p=&radio=211&pfupload_sublistingtypes='+ \
                str(type_prop)+'&item_title='+str(postdata['post_title_th'])+'&item_desc=' + str(postdata['post_description_th']) + '&pfupload_itemtypes='+ \
                str(prop)+'&pfupload_conditions=&field_project_name='+str(postdata['project_name'])+'&field_buliding=&field_floors='+str(postdata['floor_total']) + \
                '&field_floor_condo='+str(postdata['floor_level']) + '&field_size=' + str(area) + '&field_priceforsale=' + str(postdata['price_baht']) + '&field_bedroom='+ \
                str(postdata['bed_room']) + '&field_bathroom='+str(postdata['bath_room'])+'&field_near='+str(postdata['addr_near_by'])+'&field_strengths='+\
                str(postdata['prominent_point'])+'&posttags=&pfuploadfeaturedvideo=&pfupload_locations='+str(province)+'&pflocationselector='+str(province)+'&customlocation=&pfupload_address='+ \
                str(postdata['addr_road'])+'&leaflet-base-layers_49=on&pfupload_lat='+str(postdata['geo_latitude'])+'&pfupload_lng='+str(postdata['geo_longitude'])+\
                '&pfuploadimagesrc=' + str(upload_id) + '&pfpackselector=1&pf_lpacks_payment_selection=free&pftermsofuser=1&action=pfget_uploaditem&security='+str(get_security(2))
            data = {
                'action': 'pfget_itemsystem',
                'formtype': 'upload',
                #   'dt': 'pfupload_listingtypes=48&pfupload_listingpid=&pfupload_type=1&pfupload_c=&pfupload_f=&pfupload_p=&radio=211&pfupload_sublistingtypes=48&item_title=dhfjffsdf&item_desc=%3Cp%3E%3Cstrong%3Esdfjkgh%3C%2Fstrong%3E%3C%2Fp%3E&pfupload_itemtypes=34&pfupload_conditions=284&field_project_name=adhjkd&field_buliding=snf&field_floors=2&field_floor_condo=2&field_size=100&field_bedroom=12&field_bathroom=12&field_near=sdfjlfdq12&field_strengths=ahdfjh1323&posttags=(great%2Cperfect)&pfuploadfeaturedvideo=&pfupload_locations=117&pflocationselector=117&customlocation=&pfupload_address=&leaflet-base-layers_39=on&pfupload_lat=10&pfupload_lng=10&pfuploadimagesrc=624992&pfpackselector=1&pf_lpacks_payment_selection=free&pftermsofuser=1&action=pfget_uploaditem&security=067469be34',
                'dt': dt,
                'lang': 'th',
                'security': get_security(3),
            }
            url = "https://www.proptecheasy.com/wp-content/plugins/pointfindercoreelements/includes/pfajaxhandler.php"

            r = httprequestObj.http_post(
                url, data=data, headers=headers)

            data = r.text
            # return
            temp_json = json.loads(data)
            post_id = temp_json['returnval']['post_id']
            if data == '1' or temp_json['returnval']['errorval'] != ''or post_id == '':
                success = "false"
                detail = "Post could not be created."
            else:
                headers = {
                    'authority': 'www.proptecheasy.com',
                    'cache-control': 'max-age=0',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-user': '?1',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                    'sec-fetch-site': 'none',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                }
                class2 = 'pfmu-itemlisting-inner pfmu-itemlisting-inner' + \
                    str(post_id)+' pf-row clearfix pfmylistingpage'

                r2 = httprequestObj.http_get(
                    'https://www.proptecheasy.com/dashboard/?ua=myitems')
                data2 = r2.text
                soup = BeautifulSoup(r2.content, 'html5lib')
                post_url = soup.find("div", {"class": class2}).find("div", {
                    "class": 'col-lg-5 col-md-4 col-sm-4 col-xs-9 pfmu-itemlisting-title-wd'}).find("div", {'class': 'pfmu-itemlisting-title'}).find('a')['href']
                if post_url == '':
                    success = 'false'
                    detail = 'error while getting post url'
                # else :

        else:
            detail = test_login["detail"]

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {

            "websitename": "proptecheasy",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": post_url,
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
        }

    def edit_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        success = "true"
        detail = ""
        post_url = ""
        post_id = postdata['post_id']
        test_login = self.test_login(postdata)
        success = test_login["success"]

        class2 = 'pfmu-itemlisting-inner' + \
            str(post_id)
        r2 = httprequestObj.http_get(
            'https://www.proptecheasy.com/dashboard/?ua=myitems')
        data2 = r2.text
        soup = BeautifulSoup(r2.content, 'html5lib')
        try:
            post_url = soup.find("div", {"class": class2}).find("div", {
                "class": 'col-lg-5 col-md-4 col-sm-4 col-xs-9 pfmu-itemlisting-title-wd'}).find("div", {'class': 'pfmu-itemlisting-title'}).find('a')['href']
        except Exception:
            post_url=''
        if post_url == '':
            success = 'false'
            detail = 'error while getting post url'            # return "false"

        # login

        if success == "true":
            if 'prominent_point' not in postdata or postdata['prominent_point'] == None:
                postdata['prominent_point'] = ''
            if 'floor_area' not in postdata or postdata['floor_area'] == None:
                postdata['floor_area'] = '0'
            if 'floor_total' in postdata and postdata['floor_total'] != None:
                floor_total = str(postdata['floor_total'])
            else:
                floor_total = '7'
            if 'bedroom' in postdata and postdata['bedroom'] != None:
                bedroom = str(postdata['bedroom'])
            else:
                bedroom = '7'
            if 'bathroom' in postdata and postdata['bathroom'] != None:
                bathroom = str(postdata['bathroom'])
            else:
                bathroom = '7'
            if 'land_area_ngan' not in postdata or str(postdata['land_area_ngan']) == None:
                postdata['land_area_ngan'] = '0'
            if 'land_area_rai' not in postdata or str(postdata['land_area_rai']) == None:
                postdata['land_area_rai'] = '0'
            if 'land_area_wa' not in postdata or str(postdata['land_area_wa']) == None:
                postdata['land_area_wa'] = '0'

            if 'land_size_ngan' not in postdata or postdata['land_size_ngan'] == None:
                postdata['land_size_ngan'] = '0'
            if 'land_size_rai' not in postdata or postdata['land_size_rai'] == None:
                postdata['land_size_rai'] = '0'
            if 'land_size_wa' not in postdata or postdata['land_size_wa'] == None:
                postdata['land_size_wa'] = '0'
            if 'project_name' not in postdata:
                postdata['project_name'] = postdata['post_title_th']
            if len(postdata['post_images']) == 0:
                postdata['post_images'] = ['imgtmp/default/white.jpg']

            prod_address = ""
            for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
                if add is not None:
                    prod_address += add
            prod_address = prod_address[:-1]
            upload_id = ''
            security_code=get_security(1)
            for i in postdata['post_images']:
                temp = upload_image(i,security_code)
                if temp != -1:
                    upload_id = str(upload_id)+'%2c'+temp
            # upload_id = upload_image('download.jpeg')
            if upload_id == '':
                success = "false"
            if postdata['listing_type'] == 'ขาย':  # sell
                type_prop = 13
            else:
                type_prop = 12  # rent

            if postdata['property_type'] == 'คอนโด' or int(postdata['property_type']) == 1:
                prop = 34
                area = str(postdata['floor_area'])

            elif int(postdata['property_type']) == 4 or postdata['property_type'] == 'ทาวน์โฮม ทาวน์เฮ้าส์':
                area = str(postdata['floor_area'])
                prop = 49
            elif int(postdata['property_type']) == 2 or postdata['property_type'] == 'บ้านเดี่ยว' or int(postdata['property_type'])==3:
                area = str(postdata['floor_area'])
                prop = 31
            elif postdata['property_type'] == 'อพาร์ทเมนท์' or int(postdata['property_type']) == 7:
                area = str(postdata['floor_area'])
                prop = 32
            elif postdata['property_type'] == 'ที่ดินเปล่า' or int(postdata['property_type']) == 6:
                prop = 51
                ans = 0
                if postdata['land_size_rai'] != '0':
                    ans += 400*float(postdata['land_size_rai'])
                if postdata['land_size_ngan'] != '0':
                    ans += 100*float(postdata['land_size_ngan'])
                if postdata['land_size_wa'] != '0':
                    ans += float(postdata['land_size_wa'])
                area = ans*4  # (In sqm)
            elif postdata['property_type'] == 'อาคาร พื้นที่สำนักงาน' or int(postdata['property_type'] )== 9:
                area = str(postdata['floor_area'])
                prop = 20
            elif postdata['property_type'] == 'อาคารพาณิชย์' or int(postdata['property_type']) == 5:
                area = str(postdata['floor_area'])
                prop = 50
            elif int(postdata['property_type']) == 10:
                area = str(postdata['floor_area'])
                prop = 26
            elif int(postdata['property_type']) == 25:
                area = str(postdata['floor_area'])
                prop = 53
            elif int(postdata['property_type']) == 8:
                area = str(postdata['floor_area'])
                prop = 52
            else:
                area = str(postdata['floor_area'])
                prop = 34
            for pm in property_mapping.keys():
                if postdata['addr_province'] in pm:
                    province = property_mapping[pm]
            else:
                province = '117'

            if 'floor_level' not in postdata or postdata['floor_level'] is None:
                postdata['floor_level'] = ''
            # dt = 'pfupload_listingtypes='+str(type_prop)+'&pfupload_listingpid='+str(post_id)+'&pfupload_type=1&pfupload_o='+str(post_id)+'&pfupload_c=&pfupload_f=&pfupload_p=&pfupload_px=1&radio=211&pfupload_sublistingtypes='+str(type_prop)+'&item_title='+str(postdata['post_title_th'])+'&item_desc=' + str(postdata['post_description_th']) + '&pfupload_itemtypes='+str(prop)+'&pfupload_conditions=285&field_project_name='+str(postdata['project_name'])+'&field_buliding=1&field_floors='+str(postdata['floor_total']) + '&field_floor_condo='+str(postdata['floor_total']) + '&field_size=' + str(area) + '&ield_priceforsale=' + str(postdata['price_baht']) + '&field_bedroom='+str(postdata[
            #     'bed_room']) + '&field_bathroom='+str(postdata['bath_room'])+'&field_near='+str(postdata['addr_near_by'])+'&field_strengths='+str(postdata['prominent_point'])+'&posttags=&pfuploadfeaturedvideo=&pfupload_locations=&pflocationselector=&customlocation=&pfupload_address='+str(postdata['addr_road'])+'&leaflet-base-layers_49=on&pfupload_lat='+str(postdata['geo_latitude'])+'&pfupload_lng='+str(postdata['geo_longitude'])+'&pfuploadimagesrc=' + str(upload_id) + '&pfpackselector=1&pf_lpacks_payment_selection=free&pftermsofuser=1&edit_pid='+str(post_id)+'action=pfget_uploaditem&security='+str(get_security(4, post_id))
            dt = 'pfupload_listingtypes='+str(type_prop)+'&pfupload_listingpid='+str(post_id)+'&pfupload_type=1&pfupload_o='+str(
                post_id)+'&pfupload_c=&pfupload_f=0&pfupload_p=1&pfupload_px=1&radio=211&pfupload_sublistingtypes='+str(type_prop)+'&item_title='+str(postdata['post_title_th'])
            dt = dt + '&item_desc='+str(postdata['post_description_th'])
            dt = dt+'+&pfupload_itemtypes=' + \
                str(prop)+'&pfupload_conditions=&field_project_name=' + \
                str(postdata['project_name'])
            dt = dt+'&field_buliding=1&field_floors='+str(postdata['floor_total'])+'&field_floor_condo='+str(postdata['floor_level'])+'&field_size='+str(area)+'&field_priceforsale=' + \
                str(postdata['price_baht']) + '&field_bedroom='+str(postdata['bed_room']) + '&field_bathroom='+str(postdata['bath_room'])+'&field_near='+str(postdata['addr_near_by'])+ \
                    '&field_strengths='+str(postdata['prominent_point'])+'&posttags=&pfuploadfeaturedvideo=&pfupload_locations='+str(province)+'&pflocationselector='+str(province)+'&customlocation=&pfupload_address=' + \
                str(postdata['addr_road'])+'&leaflet-base-layers_45=on&pfupload_lat='+str(postdata['geo_latitude'])+'&pfupload_lng='+ \
                    str(postdata['geo_longitude'])+'&pfpackselector=1&pftermsofuser=1&edit_pid='+str(post_id)+'&action=pfget_edititem&security='+get_security(4, post_id=post_id)
            data = {
                'action': 'pfget_itemsystem',
                'formtype': 'edit',
                'dt': dt,
                'lang': 'th',
                'security': get_security(5, post_id=post_id),
            }
            url = "https://www.proptecheasy.com/wp-content/plugins/pointfindercoreelements/includes/pfajaxhandler.php"
            headers = {
                'authority': 'www.proptecheasy.com',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'sec-fetch-site': 'none',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            }

            r = httprequestObj.http_post(
                url, data=data, headers=headers)

            data = r.text
            temp_json = json.loads(data)
            if data == '1' or 'returnval' not in temp_json:
                success = "false"
                detail = "Post could not be edited."
            else:
                detail = data
                detail = "Successfully edited"

        else:
            pass
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "proptecheasy",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "log_id": postdata['log_id']
        }

    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        # start process

        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        headers = {
            'sec-fetch-mode': 'cors',
            'origin': 'https://www.proptecheasy.com',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'x-requested-with': 'XMLHttpRequest',
            'pragma': 'no-cache',
            'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'cache-control': 'no-cache',
            'authority': 'www.proptecheasy.com',
            'referer': 'https://www.proptecheasy.com/dashboard/?ua=myitems',
            'sec-fetch-site': 'same-origin',
        }
        data = {
            'action': 'pfget_itemsystem',
            'formtype': 'delete',
            'dt': postdata['post_id'],
            'lang': 'th',
            'security': get_security(6,postdata['post_id']),
        }


        if success == "true":
            r = httprequestObj.http_post('https://www.proptecheasy.com/wp-content/plugins/pointfindercoreelements/includes/pfajaxhandler.php', headers=headers, data=data)

            # r = httprequestObj.http_post(
            #     'https://www.ploychao.com/member/', data=datapost)
            data = r.text
            temp_json = json.loads(r.text)
            if data == '' or data.find("Wrong") != -1:
                success = "false"
                detail = "post not deleted"
            else:
                detail = "deleted"
        else:
            success = "false"
            detail = "cannot login"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {

            "websitename": "proptecheasy",

            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "log_id": postdata['log_id'],
        }

    def boost_post(self, postdata):

        # https://www.proptecheasy.com/dashboard/?ua=myitems&action=pf_extend&i=629031
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]

        post_id = postdata['post_id']
        params=(
            ('ua','myitems'),
            ('action','pf_extend'),
            ('i',str(post_id))
        )

        # class2 = 'pfmu-itemlisting-inner pfmu-itemlisting-inner' + \
        #     str(post_id)+' pf-row clearfix pfmylistingpage'
        # r2 = httprequestObj.http_get(
        #     'https://www.proptecheasy.com/dashboard/?ua=myitems')
        # data2 = r2.text
        # soup = BeautifulSoup(r2.content, 'html5lib')
        # try:
        #     post_url = soup.find("div", {"class": class2}).find("div", {
        #         "class": 'col-lg-5 col-md-4 col-sm-4 col-xs-9 pfmu-itemlisting-title-wd'}).find("div", {'class': 'pfmu-itemlisting-title'}).find('a')['href']
        # except Exception:
        #     post_url=''

        r=httprequestObj.http_get('https://www.proptecheasy.com/dashboard',params=params)
        # if post_url == '':
        #     success = 'false'
        #     detail = 'error while getting post url'            # return "false"

        if 'Item could not extend.' in r.text:
            success='false'
            detail='item can not be extended before expiring'
        else :
            success='true'
            detail = 'post boosted'
        time_end = datetime.datetime.utcnow()
        return {
            "websitename": "proptecheasy",
            "log_id": postdata['log_id'],

            "success": success,
            "time_usage": time_end - time_start,
            "time_start": time_start,
            "time_end": time_end,
            "detail": detail,
            "post_id": post_id,
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

        # user = postdata['user']
        # passwd = postdata['pass']
        # name_th = postdata["name_th"]
        # surname_th = postdata["surname_th"]
        # email=postdata['email']
        # phone=postdata['phone']


# Arr = {
#     'user': 'newk@1.com',
#     'pass': '123456',
#     'name_th': "killer",
#     'surname_th': 'shfjd',
#     'email': 'newk@1.com',
#     'phone': '12345623'

# }
# c_a = {
#     "action": "create_post",
#     "timeout": "5",
#     "post_img_url_lists": [
#         "http://imagestore.com/pic1.jpg",
#         "http://imagestore.com/pic2.jpg",
#     ],
#     "geo_latitude": "13.786862",
#     "geo_longitude": "100.757815",
#     "property_id": "",
#     "post_title_th": "xxx",
#     "short_post_title_th": "xxx",
#     "post_description_th": "xxx",
#     "post_title_en": "",
#     "short_post_title_en": "xxx",
#     "post_description_en": "",
#     "price_baht": "3000",
#     "listing_type": "ขาย",
#     "property_type": "คอนโด",
#     "floor_level": "11",
#     "floor_total": "11",
#     "floor_area": "11",
#     "bath_room": "11",
#     "bed_room": "11",
#     "prominent_point": "จุดเด่น",
#     "view_type": "11",
#     "direction_type": "11",
#     "addr_province": "จังหวัด",
#     "addr_district": "เขต",
#     "addr_sub_district": "ตำบล แขวง",
#     "addr_road": "ถนน",
#     "addr_soi": "ซอย",
#     "addr_near_by": "สถานที่ใกล้เคียง",
#     "floorarea_sqm": "พื้นที่",

#     "land_size_rai": "ขนาดที่ดินเป็นไร่",
#     "land_size_ngan": "ขนาดที่ดินเป็นงาน",
#     "land_size_wa": "ขนาดที่ดินเป็นวา",

#     "name": "xxx",
#     "mobile": "xxx",
#     "email": "xxx",
#     "line": "xxx",
#     'user': 'newk@1.com',
#     'pass': '123456',
#     'post_title_en': 'sfds',
#     "project_name": "ลุมพีนีวิลล รามอินทราหลักสี่",
#     "web": [
#         {
#             "ds_name": "thaihometown",
#             "ds_id": "4",
#             "user": "amarin.ta@gmail.com",
#             "pass": "5k4kk3253434"
#         },
#         {
#             "ds_name": "ddproperty",
#             "ds_id": "5",
#             "user": "amarin.ta@gmail.com",
#             "pass": "5k4kk3253434",
#             "web_project_name": "ลุมพีนี รามอินทราหลักสี่"
#         }
#     ]
# }
# # user = postdata['user'].replace("@", "%40")
# # passwd = postdata['pass'].replace("@", "%40")
# name_th = postdata["name_th"].replace("@", "%40")
# surname_th = postdata["surname_th"].replace("@", "%40")
# email = postdata['user'].replace("@", "%40")
# phone = postdata['phone']

# reg_arr = {'user': 'sdjkjsfj@21.com', 'pass': '123456', 'name_th': 'sdjfdsjf_name',
        #    'surname_th': 'surname_th', 'email': 'email@email1.com', 'phone': 'phone'}
# temp = {'ds_name': 'goodpriceproperty', 'ds_id': '3', 'post_id': '643933', 'user': 'newk@1.com', 'pass': '123456', 'action': 'create_post', 'timeout': '5', 'post_img_url_lists': ['https://firebasestorage.googleapis.com/v0/b/reas-240123.appspot.com/o/my_property%2F868eaba8-ecd6-4bbc-aab3-c65178205a28?alt=media&token=534cfb58-ea42-4b37-aa48-89dbd517f744', 'https://firebasestorage.googleapis.com/v0/b/reas-240123.appspot.com/o/my_property%2Fc35a8b18-a8ba-4a4c-9164-df97c7377cf7?alt=media&token=23516bcc-ebfb-4829-9dd7-ac5facfbcb72', 'https://firebasestorage.googleapis.com/v0/b/reas-240123.appspot.com/o/my_property%2F1d491a5c-98f9-40a8-8801-6180c274b50d?alt=media&token=2819bd81-1212-41d1-b848-5ac2f74160c1', 'https://firebasestorage.googleapis.com/v0/b/reas-240123.appspot.com/o/my_property%2F4f50d2d8-9a14-482d-9ed3-2bb7827170cf?alt=media&token=3303a7a4-4d38-4d9d-8d57-ccb62ff1bf58', 'https://firebasestorage.googleapis.com/v0/b/reas-240123.appspot.com/o/my_property%2F87d46cc0-bdc7-4d87-99af-6d92fcfb4a6a?alt=media&token=676899af-4b56-4d80-bcb2-8cf8838fddcc', 'https://firebasestorage.googleapis.com/v0/b/reas-240123.appspot.com/o/my_property%2Fabea5596-4e82-4a13-a0c7-1c0250f38fc5?alt=media&token=ea155cbe-11c6-46a6-b414-f68f75b09918', 'https://firebasestorage.googleapis.com/v0/b/reas-240123.appspot.com/o/my_property%2F577ca9ca-5ad7-4dd6-b80d-b8fa7ffa05d9?alt=media&token=f9f93ab0-924b-440d-bed7-d65de246b322', 'https://firebasestorage.googleapis.com/v0/b/reas-240123.appspot.com/o/my_property%2Fbbc702a1-332b-4bd4-842a-170edcb261dd?alt=media&token=db1d1e6c-9cab-4bfb-b3a4-78efd03222ad', 'https://firebasestorage.googleapis.com/v0/b/reas-240123.appspot.com/o/my_property%2F20754f77-5aa7-4c39-9537-2d15b877f295?alt=media&token=5c69e8ed-21f5-4b3c-9542-639ee3531fc1', 'https://firebasestorage.googleapis.com/v0/b/reas-240123.appspot.com/o/my_property%2F2e10206a-0e90-4385-a76e-18b3c991bf2b?alt=media&token=fbbae8f1-b63b-4816-9f16-6ec8d67d2a6c'], 'geo_latitude': 13.710968, 'geo_longitude': 100.498459, 'property_id': None,
        # 'post_title_th': 'ขาย คอนโด watermark เจ้าพระยาริเวอร์ 105 ตรม. 2 นอน 2 น้ำ ชั้น 33 ทิศ เหนือ วิว เมือง Fully furnished', 'short_post_title_th': 'ขาย  watermark เจ้าพระยาริเวอร์ 105 ตรม 2 ห้องนอน ชั้น 33', 'post_description_th': 'New killer ขาย คอนโด watermark เจ้าพระยาริเวอร์ 105 ตรม. 2 นอน 2 น้ำ ชั้น 33 ทิศ เหนือ วิว เมือง Fully furnished\n\n:: รายละเอียดห้อง ::\n - ขนาด 105 ตรม.\n - ชนิด 2 ห้องนอน 2 ห้องน้ำ \n - อาคาร 1 ชั้น 33\n - ระเบียงหันทางทิศ เหนือ วิว เมือง\n\n\n:: รายละเอียดโครงการ ::\n - ชื่อโครงการ: watermark เจ้าพระยาริเวอร์\n\n\n\nProject Owner: Major Development\nProject Area: 11 Rai\nNumber of building: 2\n52 floors 486 units\n\n:: สถานที่ใกล้เตียง ::\n- Senan fest: 1.2 km\n- icon SIAM : 2km\nพิกัด: http://maps.google.com/maps?q=13.710968,100.498459\n\nราคา: 13,900,000 บาท\n\nสนใจติดต่อ: NADECHAuto 0852546523\nLine: Pokajg\n#ณเดชพร็อพดพอร์ตี้', 'post_title_en': 'Condo for sale at watermark ChaoPhraya River, 105 Sqm, 33th floor, fully furnished', 'short_post_title_en': None, 'post_description_en': ':: Room Details ::\n- Size 105 sqm.\n- Type 2 bed 2 bath\n- Fully furnished and electric appliances\n- Building 1, Floor 33\n- Balcony facing the city view\n\n:: Project Details ::\nProject Name: WaterMark Chaopraya River\nProject Owner: Major Development\nProject Area: 11 Rai\nNumber of building: 2\n52 floors 486 units', 'price_baht': 2000, 'listing_type': 'ขาย', 'property_type': '1', 'floor_level': 33, 'floor_total': 52, 'floor_area': 105, 'bath_room': 2, 'bed_room': 2, 'prominent_point': None, 'view_type': 17, 'direction_type': 11, 'addr_province': 'กรุงเทพมหานคร', 'addr_district': 'เขต คลองสาน', 'addr_sub_district': 'บางลำภูล่าง', 'addr_road': None, 'addr_soi': None, 'addr_near_by': '- Senan fest: 1.2 km\n- icon SIAM : 2km', 'floorarea_sqm': 105, 'land_size_rai': None, 'land_size_ngan': None, 'land_size_wa': None, 'name': 'NADECHAuto', 'mobile': '0852546523', 'email': 'Puautopost@gmail.com', 'line': 'Pokajg', 'post_images': ['imgtmp/26820_2020050200:40:56/1.jpeg']}
# for i in range(len(temp))
# obj = proptecheasy()
# Ask about promenint point default, building number