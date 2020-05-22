# -*- coding: utf-8 -*-
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
import os
from lib_httprequest import *
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


httprequestObj = lib_httprequest()


with open("./static/ploychao_province.json") as f:
    provincedata = json.load(f)


class goodpriceproperty():

    name = 'goodpriceproperty'

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
        company_name = ''
        name = postdata["name_th"]
        surname = postdata["surname_th"]
        add = ''
        tel = postdata["tel"]
        email = postdata["user"]
        # start process
        success = "true"
        detail = ""
        for (key, value) in provincedata.items():
            # print("key",key,value)
            if type(value) is str and 'กรุงเทพ' in value.strip():
                province_id = key
                break

        for (key, value) in provincedata[province_id+"_province"].items():
            if 'พญาไท' in value.strip():
                amphur_id = key
                break
        datapost = dict(
            user=user,
            email=email,
            repass=passwd,
            name=name+" "+surname,
            shopname=company_name,
            action='save_register',
            province=province_id,
            amphur=amphur_id,
            website="",
            tel=tel,
            add=add
        )

        register_headers = {
            'Host': 'www.xn--42cf4b4c7ahl7albb1b.com',
            'Connection': 'keep-alive',
            'Content-Length': '36',
            'Cache-Control': 'max-age=0',
            'Origin': 'http://www.xn--42cf4b4c7ahl7albb1b.com',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Referer': 'http://www.xn--42cf4b4c7ahl7albb1b.com/member-condition.php',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
        }
        register_data = {
            'check': '1',
            'btLogin': 'Next | Next >>'
        }

        regist_url = 'http://www.xn--42cf4b4c7ahl7albb1b.com/register.php'
        with requests.Session() as s:
            r = s.post(regist_url, data=register_data, headers=headers)
        # print(r.content)
        soup = BeautifulSoup(r.content, 'html5lib')
        var = soup.find('input', attrs={'name': 'rands'})['value']


#             'Submit.x'= 49,
        # 'Submit.y'=10
        datapost['Submit.x'] = '49'
        datapost['Submit.y'] = '10'
        datapost['capcha'] = datapost['rands'] = var

        datapost['pass'] = datapost['repass'] = passwd
        # print(datapost)
        url_n = "http://www.xn--42cf4b4c7ahl7albb1b.com/p-register.php"
        with requests.Session() as s:
            r = s.post(url_n, data=datapost, headers=headers)
        # httprequestObj.http_post(url)
        # print(r.content)
        # print(r.text)

        data = r.text
        if data == '':
            success = "false"
        else:
            detail = data
        success = "true"
        if data.find("alert") != -1:
            success = "false"

        # # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "websitename": "goodpriceproperty",
            "start_time": str(time_start),
            "end_time": str(time_end),
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
            'pass': passwd,
            'user': user,
            'Submit.x': '30',
            'Submit.y': '21'
        }
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8', 'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive', 'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'www.xn--42cf4b4c7ahl7albb1b.com', 'Origin': 'http://www.xn--42cf4b4c7ahl7albb1b.com',
            'Referer': 'http://www.xn--42cf4b4c7ahl7albb1b.com/index.php', 'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
        }
        r = httprequestObj.http_post(
            'http://www.xn--42cf4b4c7ahl7albb1b.com/login.php', data=datapost, headers=headers)

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
        }
        data = r.text

        if data.find("ขออภัยครับ") != -1:
            detail = "cannot login"
            success = "false"
        else:
            detail = "logged in"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "websitename": "goodpriceproperty",
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
        }

    def create_post(self, postdata):
        print(postdata['post_description_th'])
        postdata['post_description_th'] = postdata['post_description_th'].replace(
            "\r\n", "\\r\\n")
        postdata['post_description_th'] = postdata['post_description_th'].replace(
            "\n", "\\r\\n")
        print(postdata['post_description_th'])

        # postdata['post_description_th']=postdata['post_description_th'].replace("\n","<br>")
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        theurl = ""
        post_id = ""

        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        ashopname = test_login["detail"]
        try:
            floor_area = str(postdata['floor_area'])
        except:
            floor_area = ""

        getProdId = {'1': 4, '2': 1, '3': 2, '4': 3, '5': 6,
                     '6': 10, '7': 5, '8': 7, '9': 8, '10': 9}
        province_id = ""
        amphur_id = ""

        for (key, value) in provincedata.items():
            if type(value) is str and postdata['addr_province'].strip() in value.strip():
                province_id = key
                break
        if province_id == "" or success!='true':

            return{
                "websitename": "goodpriceproperty",
                'success': 'false',
                'websitename': 'goodpriceproperty',
                'ret': "",
                'post_url': "",
                'post_id': "",
                'detail': 'cannot find province id or amphur',
                # 'data': postdata
            }

        for (key, value) in provincedata[province_id+"_province"].items():
            if postdata['addr_district'].replace(" ", "") in value.replace(" ", ""):
                amphur_id = key
                break

        if amphur_id == "":
            return{
                "websitename": "goodpriceproperty",
                'province': province_id,
                'success': 'false',
                'websitename': 'goodpriceproperty',
                'ret': "",
                'post_url': "",
                'post_id': "",
                'detail': 'cannot find province id or amphur2',
                # 'data': postdata
            }
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
            floor_total, bedroom, bathroom = [''] * 3
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
            print(postdata['land_size_wa'], postdata['land_size_ngan'],
                  postdata['land_size_rai'], str(postdata['floor_area']))
            print("\n\n\n")

            if 'project_name' not in postdata:
                postdata['project_name'] = postdata['post_title_th']
            if len(postdata['post_images']) == 0:
                postdata['post_images'] = ['imgtmp/default/white.jpg']

            edit_url = "http://www.xn--42cf4b4c7ahl7albb1b.com/member/post-property.php"
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
            }

            with requests.Session() as s:
                r = httprequestObj.http_get_with_headers(
                    edit_url, headers=headers)

                # r=s.post(edit_url,,headers=register_headers)
            soup = BeautifulSoup(r.content, 'html5lib')
            var = soup.find('input', attrs={'name': 'rands'})['value']
            if len(var) == 0:
                return{
                    "websitename": "goodpriceproperty",

                    'success': 'false',
                    'websitename': 'goodpriceproperty',
                    'ret': "",
                    'post_url': "",
                    'post_id': "",
                    'detail': 'Un successful post'
                }

            datapost = {
                'class_type_id': '1',  # 1 for sell 2 for rent
                # the property tye
                'cate_id': postdata['property_type'],
                'action': 'saveproduct',
                'savetype': 'R',
                'title': postdata['post_title_th'],
                'project': postdata['project_name'],
                'detail': postdata['post_description_th'],
                'price': postdata['price_baht'],
                'product_unit[]': '',
                'product_warranty_price': '',
                'shipping_id': '',
                'add': prod_address,
                'province': province_id,
                'amphur': amphur_id,
                'map_lat': postdata['geo_latitude'],
                'map_zoom': '',
                'map_lng': postdata['geo_longitude'],
                'payment_method': '',
                'productcondition': '',
                'area': str(400*int(postdata['land_size_rai']) + 100 * int(postdata['land_size_ngan']) + int(postdata['land_size_wa'])),
                'capcha': var,
                'rands': var,
                'fileshow': 'download.jpeg',
                'op_s_show': '',
                'file1': '(binary)',
                'op1': '',
                'file2': '(binary)',
                'op2': '',
                'file3': '(binary)',
                'op3': '',
                'file4': '(binary)',
                'op4': '',
                'Submit.x': '79',
                'Submit.y': '17',
                'tel': postdata['mobile']
            }
            postdata['land_area_rai'] = str(postdata['land_area_rai'])
            postdata['land_area_ngan'] = str(postdata['land_area_ngan'])
            postdata['land_area_wa'] = str(postdata['land_area_wa'])
            postdata['land_size_rai'] = str(postdata['land_size_rai'])
            postdata['land_size_ngan'] = str(postdata['land_size_ngan'])
            postdata['land_size_wa'] = str(postdata['land_size_wa'])
            if postdata['property_type'] == 'บ้านเดี่ยว' or int(postdata['property_type']) == 2:
                datapost['cate_id'] = 1
                datapost['area'] = ''
                if postdata['land_size_rai'] != '0':
                    datapost['area'] += postdata['land_size_rai'] + ' ตร.ไร่ '
                if postdata['land_size_ngan'] != '0':
                    datapost['area'] += postdata['land_size_ngan'] + ' ตร.งาน '
                if postdata['land_size_wa'] != '0':
                    datapost['area'] += postdata['land_size_wa'] + '  ตร.วา '
                if str(postdata['floor_area']) != '0':
                    datapost['area'] += str(postdata['floor_area']) + ' ตร.ม '

                # datapost['area']=str(postdata['floor_area'])+' ตร.ม ' + postdata['land_size_rai']+' ตร.ไร่ '+postdata['land_size_ngan']+' ตร.งาน ' + postdata['land_size_wa']+'  ตร.วา'
            elif postdata['property_type'] == 'บ้านแฝด' or int(postdata['property_type']) == 3:
                datapost['area'] = ''

                datapost['cate_id'] = 2
                if postdata['land_size_rai'] != '0':
                    datapost['area'] += postdata['land_size_rai'] + ' ตร.ไร่ '
                if postdata['land_size_ngan'] != '0':
                    datapost['area'] += postdata['land_size_ngan'] + ' ตร.งาน '
                if postdata['land_size_wa'] != '0':
                    datapost['area'] += postdata['land_size_wa'] + '  ตร.วา '
                if str(postdata['floor_area']) != '0':
                    datapost['area'] += str(postdata['floor_area'])+' ตร.ม '

                # datapost['area']=str(postdata['floor_area'])+' ตร.ม ' + postdata['land_size_rai']+' ตร.ไร่ '+postdata['land_size_ngan']+' ตร.งาน ' + postdata['land_size_wa']+'  ตร.วา'
            elif postdata['property_type'] == 'ทาวน์โฮม ทาวน์เฮ้าส์' or int(postdata['property_type']) == 4:
                datapost['area'] = ''

                if postdata['land_size_rai'] != '0':
                    datapost['area'] += postdata['land_size_rai'] + ' ตร.ไร่ '
                if postdata['land_size_ngan'] != '0':
                    datapost['area'] += postdata['land_size_ngan'] + ' ตร.งาน '
                if postdata['land_size_wa'] != '0':
                    datapost['area'] += postdata['land_size_wa'] + '  ตร.วา '
                if str(postdata['floor_area']) != '0':
                    datapost['area'] += str(postdata['floor_area'])+' ตร.ม '

                # datapost['area']=str(postdata['floor_area'])+' ตร.ม ' + postdata['land_size_rai']+' ตร.ไร่ '+postdata['land_size_ngan']+' ตร.งาน ' + postdata['land_size_wa']+'  ตร.วา'
                datapost['cate_id'] = 3
            elif postdata['property_type'] == 'คอนโดมิเนียม' or int(postdata['property_type']) == 1:
                datapost['area'] = ''

                if str(postdata['floor_area']) != '0':
                    datapost['area'] += str(postdata['floor_area'])+' ตร.ม '
                datapost['cate_id'] = 4
                # datapost['area']=str(postdata['floor_area'])+' ตร.ม'
            elif postdata['property_type'] == 'อพาร์ทเมนท์' or int(postdata['property_type']) == 7:
                datapost['area'] = ''

                if postdata['land_size_rai'] != '0':
                    datapost['area'] += postdata['land_size_rai'] + ' ตร.ไร่ '
                if postdata['land_size_ngan'] != '0':
                    datapost['area'] += postdata['land_size_ngan'] + ' ตร.งาน '
                if postdata['land_size_wa'] != '0':
                    datapost['area'] += postdata['land_size_wa'] + '  ตร.วา '
                if str(postdata['floor_area']) != '0':
                    datapost['area'] += str(postdata['floor_area'])+' ตร.ม '

                # datapost['area']=str(postdata['floor_area'])+' ตร.ม ' + str(postdata['land_size_rai'])+' ตร.ไร่ '+str(postdata['land_size_ngan'])+' ตร.งาน ' + str(postdata['land_size_wa'])+'  ตร.วา'
                datapost['cate_id'] = 5
            elif postdata['property_type'] == 'อาคารพาณิชย์' or int(postdata['property_type']) == 5:
                datapost['area'] = ''

                if postdata['land_size_rai'] != '0':
                    datapost['area'] += postdata['land_size_rai'] + ' ตร.ไร่ '
                if postdata['land_size_ngan'] != '0':
                    datapost['area'] += postdata['land_size_ngan'] + ' ตร.งาน '
                if postdata['land_size_wa'] != '0':
                    datapost['area'] += postdata['land_size_wa'] + '  ตร.วา '
                if str(postdata['floor_area']) != '0':
                    datapost['area'] += str(postdata['floor_area'])+' ตร.ม '

                # datapost['area']=str(postdata['floor_area'])+' ตร.ม ' + postdata['land_size_rai']+' ตร.ไร่ '+postdata['land_size_ngan']+' ตร.งาน ' + postdata['land_size_wa']+'  ตร.วา'
                datapost['cate_id'] = 6
            elif postdata['property_type'] == 'บ้านรีสอร์ท บังกะโล':
                datapost['area'] = ''

                if postdata['land_size_rai'] != '0':
                    datapost['area'] += postdata['land_size_rai'] + ' ตร.ไร่ '
                if postdata['land_size_ngan'] != '0':
                    datapost['area'] += postdata['land_size_ngan'] + ' ตร.งาน '
                if postdata['land_size_wa'] != '0':
                    datapost['area'] += postdata['land_size_wa'] + '  ตร.วา '
                if str(postdata['floor_area']) != '0':
                    datapost['area'] += str(postdata['floor_area'])+' ตร.ม '

                # datapost['area']=str(postdata['floor_area'])+' ตร.ม ' + postdata['land_size_rai']+' ตร.ไร่ '+postdata['land_size_ngan']+' ตร.งาน ' + postdata['land_size_wa']+'  ตร.วา'
                datapost['cate_id'] = 7
            elif postdata['property_type'] == 'อาคาร พื้นที่สำนักตร.งาน' or int(postdata['property_type']) == 9:
                datapost['area'] = ''

                if postdata['land_size_rai'] != '0':
                    datapost['area'] += postdata['land_size_rai'] + ' ตร.ไร่ '
                if postdata['land_size_ngan'] != '0':
                    datapost['area'] += postdata['land_size_ngan'] + ' ตร.งาน '
                if postdata['land_size_wa'] != '0':
                    datapost['area'] += postdata['land_size_wa'] + '  ตร.วา '
                if str(postdata['floor_area']) != '0':
                    datapost['area'] += str(postdata['floor_area'])+' ตร.ม '

                # datapost['area']=str(postdata['floor_area'])+' ตร.ม ' + postdata['land_size_rai']+' ตร.ไร่ '+postdata['land_size_ngan']+' ตร.งาน ' + postdata['land_size_wa']+'  ตร.วา'
                datapost['cate_id'] = 8
            elif postdata['property_type'] == 'โรงตร.งาน คลังสินค้า' or int(postdata['property_type']) == 10 or int(postdata['property_type']) == 25:
                datapost['area'] = ''

                if postdata['land_size_rai'] != '0':
                    datapost['area'] += postdata['land_size_rai'] + ' ตร.ไร่ '
                if postdata['land_size_ngan'] != '0':
                    datapost['area'] += postdata['land_size_ngan'] + ' ตร.งาน '
                if postdata['land_size_wa'] != '0':
                    datapost['area'] += postdata['land_size_wa'] + '  ตร.วา '
                if str(postdata['floor_area']) != '0':
                    datapost['area'] += str(postdata['floor_area'])+' ตร.ม '

                # datapost['area']=str(postdata['floor_area'])+' ตร.ม ' + postdata['land_size_rai']+' ตร.ไร่ '+postdata['land_size_ngan']+' ตร.งาน ' + postdata['land_size_wa']+'  ตร.วา'
                datapost['cate_id'] = 9
            elif postdata['property_type'] == 'ที่ดินเปล่า' or int(postdata['property_type']) == 6:
                datapost['area'] = ''

                datapost['cate_id'] = 10
                ans = 0
                if postdata['land_size_rai'] != '0':
                    ans += 400*float(postdata['land_size_rai'])
                if postdata['land_size_ngan'] != '0':
                    ans += 100*float(postdata['land_size_ngan'])
                if postdata['land_size_wa'] != '0':
                    ans += float(postdata['land_size_wa'])
                datapost['area'] = str(int(ans))+' ตร.วา'
            elif postdata['property_type'] == 'อื่นๆ':
                datapost['area'] = ''
                if postdata['land_size_rai'] != '0':
                    datapost['area'] += postdata['land_size_rai'] + ' ตร.ไร่ '
                if postdata['land_size_ngan'] != '0':
                    datapost['area'] += postdata['land_size_ngan'] + ' ตร.งาน '
                if postdata['land_size_wa'] != '0':
                    datapost['area'] += postdata['land_size_wa'] + '  ตร.วา '
                if str(postdata['floor_area']) != '0':
                    datapost['area'] += str(postdata['floor_area'])+' ตร.ม '

                datapost['cate_id'] = 11
                # datapost['area']=str(postdata['floor_area'])+' ตร.ม ' + postdata['land_size_rai']+' ตร.ไร่ '+postdata['land_size_ngan']+' ตร.งาน ' + postdata['land_size_wa']+'  ตร.วา'
            else:
                datapost['area'] = ''
                if postdata['land_size_rai'] != '0':
                    datapost['area'] += postdata['land_size_rai'] + ' ตร.ไร่ '
                if postdata['land_size_ngan'] != '0':
                    datapost['area'] += postdata['land_size_ngan'] + ' ตร.งาน '
                if postdata['land_size_wa'] != '0':
                    datapost['area'] += postdata['land_size_wa'] + '  ตร.วา '
                if str(postdata['floor_area']) != '0':
                    datapost['area'] += str(postdata['floor_area'])+' ตร.ม '

                datapost['cate_id'] = 11  # default
                # datapost['area']=str(postdata['floor_area'])+' ตร.ม ' + str(postdata['land_area_rai'])+' ตร.ไร่ '+str(postdata['land_area_ngan'])+' ตร.งาน ' + str(postdata['land_area_wa'])+'  ตร.วา'
            if postdata['listing_type'] != 'ขาย':
                datapost['class_type_id'] = 2
            arr = ["fileshow", "file1", "file2", "file3", "file4"]
            # files = {'fileshow': open('download.jpeg', 'rb')}
            files = {}
            # print(postdata['post_images'])
            no = len(postdata['post_images'][:5])
            if no == 0:
                files = {'fileshow': ('imgtmp/default/white.png', open(
                    'imgtmp/default/white.png', 'rb'), 'image/png')}
            else:
                for i in range(no):
                    datapost[arr[i]] = postdata['post_images'][i]
                    files[arr[i]] = (postdata['post_images'][i], open(
                        postdata['post_images'][i], "rb"), "image/jpg")

            r = httprequestObj.http_post(
                'http://www.xn--42cf4b4c7ahl7albb1b.com/member/p-post-property.php', data=datapost, files=files)
            list_url = 'http://www.xn--42cf4b4c7ahl7albb1b.com/member/list-property.php'
            r = httprequestObj.http_get(list_url)
            soup = BeautifulSoup(r.content, 'html5lib')
            var = soup.find('a', attrs={'title': postdata['post_title_th']})[
                'href']
            if var == "" or var == 'http://www.อสังหาราคาดี.com/index.php':
                time_end = datetime.datetime.utcnow()
                time_usage = time_end - time_start
                return {
                    'success': 'false',
                    'action': "create_post",
                    "websitename": "goodpriceproperty",
                    "start_time": str(time_start),
                    "end_time": str(time_end),

                    'post_url': '',
                    'post_id': '',
                    'account_type': ''
                }
            # for i in '../property/':
            i = len('../property/')
            # post_id=''
            post_id = ''

            while var[i] != '/':
                post_id += var[i]
                i += 1
            if postdata['post_title_th'][len(postdata['post_title_th'])-1] == '%':
                postdata['post_title_th'] = postdata['post_title_th'][:len(
                    postdata['post_title_th'])-1]
            post_url = 'http://www.xn--42cf4b4c7ahl7albb1b.com/property/' + \
                post_id+"/"+postdata['post_title_th']+'.html'

            time_end = datetime.datetime.utcnow()
            time_usage = time_end - time_start
            data = r.text
            success = "true"
            if data.find("alert") != -1:
                success = "false"
            return {
                'prop_type': postdata['property_type'],
                'data_prop_type': datapost['cate_id'],
                'success': 'true',
                'action': "create_post",
                "websitename": "goodpriceproperty",
                "start_time": str(time_start),
                "end_time": str(time_end),
                'post_url': post_url,
                'post_id': post_id,
                'account_type': ''
            }
        else:
            time_end = datetime.datetime.utcnow()
            time_usage = time_end - time_start

            return{
                'success':'false',
                'detail':'login error',
                "websitename": "goodpriceproperty",
                "start_time": str(time_start),
                "end_time": str(time_end),
                
            }

    def edit_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # login
        success = 'true'
        test_login = self.test_login(postdata)
        success = test_login["success"]
        ashopname = test_login["detail"]

        post_id = ""
        detail = ""
        province_id = ""
        amphur_id = ""

        for (key, value) in provincedata.items():
            if type(value) is str and postdata['addr_province'].strip() in value.strip():
                province_id = key
                break

        if province_id == "" or success != 'true':
            return{
                "websitename": "goodpriceproperty",
                'success': 'false',
                'websitename': 'goodpriceproperty',
                'ret': "",
                'post_url': "",
                'post_id': "",
                'detail': 'cannot find province id or amphur',
                # 'data': postdata
            }
        url_list = 'http://www.xn--42cf4b4c7ahl7albb1b.com/member/list-property.php'
        r = httprequestObj.http_get(url_list)
        soup = BeautifulSoup(r.content, 'html5lib')
        ahref = soup.findAll('a')
        post_id = ''
        storeI = ''
        for i in ahref:
            var = i['href']
            j = len('../property/')
            post_id = ''

            while j < len(var) and var[j] != '/':
                post_id += var[j]
                j += 1
            if post_id == postdata['post_id']:
                storeI = i
                break
        if storeI == '':
            return {
                "websitename": "goodpriceproperty",

                'success': 'false',
                                'ret': "",
                'post_url': "",
                'post_id': "",
                'detail': 'cannot find the given post_id',

            }

        for (key, value) in provincedata[province_id+"_province"].items():
            if postdata['addr_district'].replace(" ", "") in value.replace(" ", ""):
                amphur_id = key
                break
        if amphur_id == "":
            return{
                "websitename": "goodpriceproperty",

                'success': 'false',
                'websitename': 'goodpriceproperty',
                'ret': "",
                'post_url': "",
                'post_id': ""
            }
        # province_id = 64
        # amphur_id = 864

        no = 0
        img_arr = {}
        topic_id = postdata['post_id']
        # for i in range(len(postdata['post_img_url_lists'])):
        #     img_arr[i] = str(no)+".jpg"
        #     print("imagefs ", postdata['post_img_url_lists'][i])
        #     urllib.request.urlretrieve(
        #         postdata['post_img_url_lists'][i], str(no)+".jpg")
        #     no += 1
        try:
            floor_area = postdata['floor_area_sqm']
        except:
            floor_area = ""

        prod_address = ""
        for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
            if add is not None:
                prod_address += add + ","
        # prod_address = prod_address
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
            floor_total, bedroom, bathroom = [''] * 3
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
            print(postdata['land_size_wa'], postdata['land_size_ngan'],
                  postdata['land_size_rai'], str(postdata['floor_area']))
            print("\n\n\n")

            if 'project_name' not in postdata:
                postdata['project_name'] = postdata['post_title_th']
            if len(postdata['post_images']) == 0:
                postdata['post_images'] = ['imgtmp/default/white.jpg']

            edit_url = "http://www.xn--42cf4b4c7ahl7albb1b.com/member/edit-property.php"
            payload = {'topic_id': topic_id}
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
            }

            with requests.Session() as s:
                r = httprequestObj.http_get_with_headers(
                    edit_url, headers=headers, params=payload)

                # r=s.post(edit_url,,headers=register_headers)
            soup = BeautifulSoup(r.content, 'html5lib')
            var = soup.find('input', attrs={'name': 'rands'})['value']
            if len(var) == 0:
                return{
                    "websitename": "goodpriceproperty",

                    'success': 'false',
                    'websitename': 'goodpriceproperty',
                    'ret': "",
                    'post_url': "",
                    'post_id': ""
                }

            datapost = {
                'class_type_id': '1',  # 1 for sell 2 for rent
                # remaining here
                'cate_id': postdata['property_type'],  # the property tye
                'action': 'saveproduct',
                # 'hidproduct_id': postdata['post_id'],
                'savetype': 'R',
                'title': postdata['post_title_th'],
                'topic_id': postdata['post_id'],
                'project': postdata['project_name'],
                'detail': postdata['post_description_th'],
                'price': postdata['price_baht'],
                'product_unit[]': '',
                'product_warranty_price': '',
                'shipping_id': '',
                'add': prod_address,
                'province': province_id,
                'amphur': amphur_id,
                'map_lat': postdata['geo_latitude'],
                'map_zoom': '',
                'map_lng': postdata['geo_longitude'],
                'payment_method': '',
                'productcondition': '',
                'area': str(400*int(postdata['land_size_rai']) + 100 * int(postdata['land_size_ngan']) + int(postdata['land_size_wa'])),
                'capcha': var,
                'rands': var,
                'fileshow': '(binary)',
                'op_s_show': '',
                'file1': '(binary)',
                'op1': '',
                'file2': '(binary)',
                'op2': '',
                'file3': '(binary)',
                'op3': '',
                'file4': '(binary)',
                'op4': '',
                'Submit.x': '79',
                'Submit.y': '17',
                'tel': postdata['mobile']

            }
            postdata['land_area_rai'] = str(postdata['land_area_rai'])
            postdata['land_area_ngan'] = str(postdata['land_area_ngan'])
            postdata['land_area_wa'] = str(postdata['land_area_wa'])
            postdata['land_size_rai'] = str(postdata['land_size_rai'])
            postdata['land_size_ngan'] = str(postdata['land_size_ngan'])
            postdata['land_size_wa'] = str(postdata['land_size_wa'])
            if postdata['property_type'] == 'บ้านเดี่ยว' or int(postdata['property_type']) == 2:
                datapost['cate_id'] = 1
                datapost['area'] = ''
                if postdata['land_size_rai'] != '0':
                    datapost['area'] += postdata['land_size_rai'] + ' ตร.ไร่ '
                if postdata['land_size_ngan'] != '0':
                    datapost['area'] += postdata['land_size_ngan'] + ' ตร.งาน '
                if postdata['land_size_wa'] != '0':
                    datapost['area'] += postdata['land_size_wa'] + '  ตร.วา '
                if str(postdata['floor_area']) != '0':
                    datapost['area'] += str(postdata['floor_area']) + ' ตร.ม '

                # datapost['area']=str(postdata['floor_area'])+' ตร.ม ' + postdata['land_size_rai']+' ตร.ไร่ '+postdata['land_size_ngan']+' ตร.งาน ' + postdata['land_size_wa']+'  ตร.วา'
            elif postdata['property_type'] == 'บ้านแฝด' or int(postdata['property_type']) == 3:
                datapost['area'] = ''

                datapost['cate_id'] = 2
                if postdata['land_size_rai'] != '0':
                    datapost['area'] += postdata['land_size_rai'] + ' ตร.ไร่ '
                if postdata['land_size_ngan'] != '0':
                    datapost['area'] += postdata['land_size_ngan'] + ' ตร.งาน '
                if postdata['land_size_wa'] != '0':
                    datapost['area'] += postdata['land_size_wa'] + '  ตร.วา '
                if str(postdata['floor_area']) != '0':
                    datapost['area'] += str(postdata['floor_area'])+' ตร.ม '

                # datapost['area']=str(postdata['floor_area'])+' ตร.ม ' + postdata['land_size_rai']+' ตร.ไร่ '+postdata['land_size_ngan']+' ตร.งาน ' + postdata['land_size_wa']+'  ตร.วา'
            elif postdata['property_type'] == 'ทาวน์โฮม ทาวน์เฮ้าส์' or int(postdata['property_type']) == 4:
                datapost['area'] = ''

                if postdata['land_size_rai'] != '0':
                    datapost['area'] += postdata['land_size_rai'] + ' ตร.ไร่ '
                if postdata['land_size_ngan'] != '0':
                    datapost['area'] += postdata['land_size_ngan'] + ' ตร.งาน '
                if postdata['land_size_wa'] != '0':
                    datapost['area'] += postdata['land_size_wa'] + '  ตร.วา '
                if str(postdata['floor_area']) != '0':
                    datapost['area'] += str(postdata['floor_area'])+' ตร.ม '

                # datapost['area']=str(postdata['floor_area'])+' ตร.ม ' + postdata['land_size_rai']+' ตร.ไร่ '+postdata['land_size_ngan']+' ตร.งาน ' + postdata['land_size_wa']+'  ตร.วา'
                datapost['cate_id'] = 3
            elif postdata['property_type'] == 'คอนโดมิเนียม' or int(postdata['property_type']) == 1:
                datapost['area'] = ''

                if str(postdata['floor_area']) != '0':
                    datapost['area'] += str(postdata['floor_area'])+' ตร.ม '
                datapost['cate_id'] = 4
                # datapost['area']=str(postdata['floor_area'])+' ตร.ม'
            elif postdata['property_type'] == 'อพาร์ทเมนท์' or int(postdata['property_type']) == 7:
                datapost['area'] = ''

                if postdata['land_size_rai'] != '0':
                    datapost['area'] += postdata['land_size_rai'] + ' ตร.ไร่ '
                if postdata['land_size_ngan'] != '0':
                    datapost['area'] += postdata['land_size_ngan'] + ' ตร.งาน '
                if postdata['land_size_wa'] != '0':
                    datapost['area'] += postdata['land_size_wa'] + '  ตร.วา '
                if str(postdata['floor_area']) != '0':
                    datapost['area'] += str(postdata['floor_area'])+' ตร.ม '

                # datapost['area']=str(postdata['floor_area'])+' ตร.ม ' + str(postdata['land_size_rai'])+' ตร.ไร่ '+str(postdata['land_size_ngan'])+' ตร.งาน ' + str(postdata['land_size_wa'])+'  ตร.วา'
                datapost['cate_id'] = 5
            elif postdata['property_type'] == 'อาคารพาณิชย์' or int(postdata['property_type']) == 5:
                datapost['area'] = ''

                if postdata['land_size_rai'] != '0':
                    datapost['area'] += postdata['land_size_rai'] + ' ตร.ไร่ '
                if postdata['land_size_ngan'] != '0':
                    datapost['area'] += postdata['land_size_ngan'] + ' ตร.งาน '
                if postdata['land_size_wa'] != '0':
                    datapost['area'] += postdata['land_size_wa'] + '  ตร.วา '
                if str(postdata['floor_area']) != '0':
                    datapost['area'] += str(postdata['floor_area'])+' ตร.ม '

                # datapost['area']=str(postdata['floor_area'])+' ตร.ม ' + postdata['land_size_rai']+' ตร.ไร่ '+postdata['land_size_ngan']+' ตร.งาน ' + postdata['land_size_wa']+'  ตร.วา'
                datapost['cate_id'] = 6
            elif postdata['property_type'] == 'บ้านรีสอร์ท บังกะโล':
                datapost['area'] = ''

                if postdata['land_size_rai'] != '0':
                    datapost['area'] += postdata['land_size_rai'] + ' ตร.ไร่ '
                if postdata['land_size_ngan'] != '0':
                    datapost['area'] += postdata['land_size_ngan'] + ' ตร.งาน '
                if postdata['land_size_wa'] != '0':
                    datapost['area'] += postdata['land_size_wa'] + '  ตร.วา '
                if str(postdata['floor_area']) != '0':
                    datapost['area'] += str(postdata['floor_area'])+' ตร.ม '

                # datapost['area']=str(postdata['floor_area'])+' ตร.ม ' + postdata['land_size_rai']+' ตร.ไร่ '+postdata['land_size_ngan']+' ตร.งาน ' + postdata['land_size_wa']+'  ตร.วา'
                datapost['cate_id'] = 7
            elif postdata['property_type'] == 'อาคาร พื้นที่สำนักตร.งาน' or int(postdata['property_type']) == 9:
                datapost['area'] = ''

                if postdata['land_size_rai'] != '0':
                    datapost['area'] += postdata['land_size_rai'] + ' ตร.ไร่ '
                if postdata['land_size_ngan'] != '0':
                    datapost['area'] += postdata['land_size_ngan'] + ' ตร.งาน '
                if postdata['land_size_wa'] != '0':
                    datapost['area'] += postdata['land_size_wa'] + '  ตร.วา '
                if str(postdata['floor_area']) != '0':
                    datapost['area'] += str(postdata['floor_area'])+' ตร.ม '

                # datapost['area']=str(postdata['floor_area'])+' ตร.ม ' + postdata['land_size_rai']+' ตร.ไร่ '+postdata['land_size_ngan']+' ตร.งาน ' + postdata['land_size_wa']+'  ตร.วา'
                datapost['cate_id'] = 8
            elif postdata['property_type'] == 'โรงตร.งาน คลังสินค้า' or int(postdata['property_type']) == 10 or int(postdata['property_type']) == 25:
                datapost['area'] = ''

                if postdata['land_size_rai'] != '0':
                    datapost['area'] += postdata['land_size_rai'] + ' ตร.ไร่ '
                if postdata['land_size_ngan'] != '0':
                    datapost['area'] += postdata['land_size_ngan'] + ' ตร.งาน '
                if postdata['land_size_wa'] != '0':
                    datapost['area'] += postdata['land_size_wa'] + '  ตร.วา '
                if str(postdata['floor_area']) != '0':
                    datapost['area'] += str(postdata['floor_area'])+' ตร.ม '

                # datapost['area']=str(postdata['floor_area'])+' ตร.ม ' + postdata['land_size_rai']+' ตร.ไร่ '+postdata['land_size_ngan']+' ตร.งาน ' + postdata['land_size_wa']+'  ตร.วา'
                datapost['cate_id'] = 9
            elif postdata['property_type'] == 'ที่ดินเปล่า' or int(postdata['property_type']) == 6:
                datapost['area'] = ''

                datapost['cate_id'] = 10
                ans = 0
                if postdata['land_size_rai'] != '0':
                    ans += 400*float(postdata['land_size_rai'])
                if postdata['land_size_ngan'] != '0':
                    ans += 100*float(postdata['land_size_ngan'])
                if postdata['land_size_wa'] != '0':
                    ans += float(postdata['land_size_wa'])
                datapost['area'] = str(int(ans))+' ตร.วา'
            elif postdata['property_type'] == 'อื่นๆ':
                datapost['area'] = ''
                if postdata['land_size_rai'] != '0':
                    datapost['area'] += postdata['land_size_rai'] + ' ตร.ไร่ '
                if postdata['land_size_ngan'] != '0':
                    datapost['area'] += postdata['land_size_ngan'] + ' ตร.งาน '
                if postdata['land_size_wa'] != '0':
                    datapost['area'] += postdata['land_size_wa'] + '  ตร.วา '
                if str(postdata['floor_area']) != '0':
                    datapost['area'] += str(postdata['floor_area'])+' ตร.ม '

                datapost['cate_id'] = 11
                # datapost['area']=str(postdata['floor_area'])+' ตร.ม ' + postdata['land_size_rai']+' ตร.ไร่ '+postdata['land_size_ngan']+' ตร.งาน ' + postdata['land_size_wa']+'  ตร.วา'
            else:
                datapost['area'] = ''
                if postdata['land_size_rai'] != '0':
                    datapost['area'] += postdata['land_size_rai'] + ' ตร.ไร่ '
                if postdata['land_size_ngan'] != '0':
                    datapost['area'] += postdata['land_size_ngan'] + ' ตร.งาน '
                if postdata['land_size_wa'] != '0':
                    datapost['area'] += postdata['land_size_wa'] + '  ตร.วา '
                if str(postdata['floor_area']) != '0':
                    datapost['area'] += str(postdata['floor_area'])+' ตร.ม '

                datapost['cate_id'] = 11  # default
                # datapost['area']=str(postdata['floor_area'])+' ตร.ม ' + str(postdata['land_area_rai'])+' ตร.ไร่ '+str(postdata['land_area_ngan'])+' ตร.งาน ' + str(postdata['land_area_wa'])+'  ตร.วา'
            if postdata['listing_type'] != 'ขาย':
                datapost['class_type_id'] = 2
            arr = ["fileshow", "file1", "file2", "file3", "file4"]
            # files = {'fileshow': open('download.jpeg', 'rb')}
            files = {}

            no = len(postdata['post_images'][:5])
            # if no == 0:
            #     files = {'fileshow': ('download.jpeg', open(
            #         'download.jpeg', 'rb'), 'image/jpeg')}
            # else:
            for i in range(no):
                datapost[arr[i]] = postdata['post_images'][i]
                files[arr[i]] = (postdata['post_images'][i], open(
                    postdata['post_images'][i], "rb"), "image/jpg")

            r = httprequestObj.http_post(
                'http://www.xn--42cf4b4c7ahl7albb1b.com/member/p-edit-property.php', data=datapost, headers=headers, files=files)
            print("RETURN ", r.content)
            print("RETURN ", r.text)
            print("DATA", datapost)
            data = r.text
            time_end = datetime.datetime.utcnow()
            time_usage = time_end - time_start
            # print("REACHED ")
            if data.find("alert") != -1:
                success = "false"
            return {
                'success': success,
                "action": "edit_post",
                "websitename": "goodpriceproperty",
                "start_time": str(time_start),
                "end_time": str(time_end),
                "detail": data,
                "log_id": "",
            }

    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]

        if success == "true":
            url_list = 'http://www.xn--42cf4b4c7ahl7albb1b.com/member/list-property.php'
            r = httprequestObj.http_get(url_list)
            soup = BeautifulSoup(r.content, 'html5lib')
            ahref = soup.findAll('a')
            post_id = ''
            storeI = ''
            for i in ahref:
                var = i['href']
                j = len('../property/')
                post_id = ''

                while j < len(var) and var[j] != '/':
                    post_id += var[j]
                    j += 1
                if post_id == postdata['post_id']:
                    storeI = i
                    break
            if storeI == '':
                return {
                    'success': 'false',
                    'websitename':'goodpriceproperty',
                    'detail':'Incorrect Post id'
                }

            datapost = [
                ('action', 'delete_product'),
                ('product_id',  postdata['post_id']),
            ]
            url = "http://www.xn--42cf4b4c7ahl7albb1b.com/member/del-property.php"
            payload = {'topic_id': postdata['post_id']}

            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
            }

            r = httprequestObj.http_get_with_headers(
                url, headers=headers, params=payload)
            # r = httprequestObj.http_post(
            #     'https://www.ploychao.com/member/', data=datapost)
            data = r.text
            time_end = datetime.datetime.utcnow()
            time_usage = time_end - time_start

            success = "true"
            # print(data)
            # if data.find("alert") != -1:
            #     success = "false"
            return{
                'success': success,
                "action": "delete_post",
                "websitename": "goodpriceproperty",
                "start_time": str(time_start),
                "end_time": str(time_end),
                "detail": "Successfully deleted",
                # "log_id": postdata['log_id'],
            }

        else:
            success = "false"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "websitename": "goodpriceproperty",
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "log_id": postdata['log_id']
            # "detail": "under construction",
        }

    def boost_post(self, postdata):
        
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]

        post_id = postdata['post_id']
        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Referer': 'http://www.xn--42cf4b4c7ahl7albb1b.com/member/list-property.php',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        params = (
            ('topic_id',post_id),
        )
        r1=httprequestObj.http_get('http://www.อสังหาราคาดี.com/member/list-property.php',headers=headers)
        if post_id not in r1.text:
            success='false'
            detail = 'Post id doesnt exist'

        r = httprequestObj.http_get('http://www.xn--42cf4b4c7ahl7albb1b.com/member/slide-property.php',
                                headers=headers, params=params, verify=False)

        if success == 'true' and 'เลื่อนประกาศเรียบร้อยแล้วครับ'  not in r.text:
            success='false'
            detail = 'Post already boosted'
        elif success=='true':
            detail = 'successfully boosted'

        time_end = datetime.datetime.utcnow()
        return {
            "success": success,
            'detail':detail,
            "time_usage": time_end - time_start,
            "time_start": time_start,
            "time_end": time_end,
            # "detail": detail,
            "post_id": post_id,
            "websitename": "goodpriceproperty"
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


# json_edit={
#     "action": "edit_post",
#     "timeout": "5",
#     'post_images':['../imgtmp/default/white.png'],

#     "post_img_url_lists": [
#         "http://imagestore.com/pic1.jpg",
#         "http://imagestore.com/pic2.jpg",
#         "http://imagestore.com/pic3.jpg",
#         "http://imagestore.com/pic4.jpg",
#         "http://imagestore.com/pic5.jpg"
#     ],
#     "name": "xxx",
#     "mobile": "xxx",
#     "email": "xxx",
#     "line": "xxx",
#     "property_id" : "289338",
#     "floorarea_sqm": "100",
#     "direction_type" : "11",
#     "addr_road": "ถนน",
#     "addr_soi": "ซอย",
#     "addr_near_by": "สถานที่ใกล้เคียง",
#     "listing_type": "ขาย",    
#     "property_type": "คอนโด",
#     "addr_province": "กาฬสินธุ์",
#     "addr_district": "เมืองกาฬสินธุ์",
#     "addr_sub_district": "ตำบล แขวง",
#     "price_baht": "5",
#     "county": "เขต",
#     "district": "แขวง",
#     "geo_latitude": "13.786862",
#     "geo_longitude": "100.757815",
#     "post_title_th": "xxx_new12",
#     "post_description_th": "xxx",
#     "post_title_en": "",
#     "post_description_en": "adhgdshgdsfhgjdsfhgfdh",
#     "project_name": "ลุมพีนีวิลล รามอินทราหลักสี่",
#     "post_id": "291746",
#     "log_id": "33333",             
#     "user": "temp",
#     "pass": "12",

#     "web": [
#         {
#             "ds_name": "thaihometown",
#             "ds_id": "4",
#             "post_id": "291746",
#             "log_id": "33333",             
#             "user": "temp",
#             "pass": "12"
#         },
#         {
#             "ds_name": "ddproperty",
#             "ds_id": "5",
#             "post_id": "4444",
#             "log_id": "44444",             
#             "account_type" : "corperate",
#             "user": "amarin.ta@gmail.com",
#             "pass": "5k4kk3253434",     
#             "web_project_name": "ลุมพีนี รามอินทราหลักสี่"
#         }
#     ]
# }
# a=goodpriceproperty()
# print(a.delete_post(json_edit))

        # company_name = postdata['company_name']
        # name_th = postdata["name_th"]
        # surname_th = postdata["surname_th"]
# email = "cu1123@3.com"
# reg_arr= { "action": "register_user", "timeout": "7","ds_name": "goodpriceproperty","ds_id": "4","user": email,"pass": "12345678","company_name": "amarkjjk","name_title": "mr","name_th": "อัมรินทร์","surname_th": "บุญเกิด","name_en": "Amarin","surname_en": "Boonkirt","tel": "0891999450","line": "amarin.ta","addr_province" : "นนทบุรี", "addr_district" : "เมืองนนทบุรี" }

# thedata = { "action": "edit_post", "timeout": "5", "project_name": "ลุมพีนีวิลล", "post_img_url_lists": [ "https://zignnet.sgp1.digitaloceanspaces.com/livingjoin/classified/189689/big/210120235215500991.jpg", "https://zignnet.sgp1.digitaloceanspaces.com/livingjoin/classified/189689/other/big/210120235220317918.jpg" ], "geo_latitude": "13.786862", "geo_longitude": "100.757815", "property_id" : "chu001", "post_title_th": "new edited dsfhfj ให้เช่า ที่ดินด่วน บางกรวยไทรน้อย 6 ไร่ เหมาะทำตลาด", "post_description_th": "What is description", "post_title_en": "Land for rent bangkloysainoi 6 rai suitable for developing", "post_description_en": "Land for rent bangkloysainoi 6 rai suita ble for developing", "price_baht": "100000", "listing_type": "เช่า", "property_type": "6", "prominent_point " : "หน้ากว้างมาก ให้เช่าถูกสุด", "direction_type" : "11", "addr_province": "นนทบุรี", "addr_district": "เมืองนนทบุรี", "addr_sub_district": "บางกรวย", "addr_road": "บางกรวย-ไทรน้อย", "addr_soi": "ซอยบางกรวย-ไทรน้อย 34", "addr_near_by": "ถนนพระราม5\nถนนนครอินทร์", "land_size_rai": "6", "land_size_ngan": "0", "land_size_wa": "0", "name": "ชู", "mobile": "0992899999", "email": "panuwat.ruangr",'user':'temp_007','pass':'123456','post_id':'289666'}
# a=goodpriceproperty()
# print(a.boost_post(json_edit))