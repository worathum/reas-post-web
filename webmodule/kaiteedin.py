
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
import os
import re
import random
from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
# from urlparse import urlparse
import re
import json
import datetime
import time
import sys
from urllib.parse import unquote


httprequestObj = lib_httprequest()


with open("./static/ploychao_province.json") as f:
    provincedata = json.load(f)


class kaiteedin():

    name = 'kaiteedin'

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

        return {
            "websitename": "kaiteedin",
            "success": "true",
            "time_usage": time_end - time_start,
            "time_start": time_start,
            "time_end": time_end,
            "detail": ""
        }

    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        success = "true"
        detail = ""

        if 'surname_th' not in postdata:
            return{
                'websitename': 'kaiteedin',
                'success': 'false',
                'detail': 'Missing required field name',
            }
        if 'name_th' not in postdata:
            return{
                'websitename': 'kaiteedin',
                'success': 'false',
                'detail': 'Missing required field name',
            }
        if 'tel' not in postdata:
            return{
                'websitename': 'kaiteedin',
                'success': 'false',
                'detail': 'Missing required field tel',
            }
        if 'pass' not in postdata:
            return{
                'websitename': 'kaiteedin',
                'success': 'false',
                'detail': 'Missing required field pass',
            }
        if 'user' not in postdata:
            return{
                'websitename': 'kaiteedin',
                'success': 'false',
                'detail': 'Missing required field email',
            }
        prod_address = "พญาไท, กรุงเทพ"
        datapost = dict(
            Member_name=postdata['name_th']+" "+postdata['surname_th'],
            Member_email=postdata['user'],
            Member_password=postdata['pass'],
            Member_password_re=postdata['pass'],
            Member_gender="ชาย",
            Member_career='broker',
            Member_date='2004-12-31',
            Member_address=prod_address,
            Member_tel=postdata['tel'],
        )

        url_n = "http://kaiteedin.net/member_signup.php"
        s = requests.Session()
        r = s.post(url_n, data=datapost)
        data = r.text
        soup = BeautifulSoup(r.content, "html5lib")
        script = soup.find("script", attrs={'language': 'JavaScript'})
        html = "บันทึกข้อมูลของคุณเรียบร้อยแล้ว กรุณาตรวจสอบอีเมลของท่านเพื่อยืนยันตนก่อนเข้าสู่ระบบ"
        if html not in script.text:
            success = "false"
            detail = "Failed to register"
        else:
            detail = "registered"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "kaiteedin",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
        }

    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        success = "true"
        detail = ""
        if 'pass' not in postdata:
            return{
                'websitename': 'kaiteedin',
                'success': 'false',
                'detail': 'Missing required field pass',
                "ds_id": postdata['ds_id'],
            }
        if 'user' not in postdata:
            return{
                'websitename': 'kaiteedin',
                'success': 'false',
                'detail': 'Missing required field email',
                "ds_id": postdata['ds_id'],
            }

        datapost = {
            'Member_email': postdata['user'],
            'Member_password': postdata['pass'],
            'remember':  'on'
        }

        r = httprequestObj.http_post(
            'http://kaiteedin.net/member_signin.php', data=datapost)
        data = r.text
        soup = BeautifulSoup(r.content, "html5lib")
        script = soup.find("script", attrs={'language': 'JavaScript'})
        if script != None:
            success = "false"
            if "อีเมล หรือ รหัสผ่านของท่านไม่ถูกต้องกรุณาตรวจสอบใหม่อีกครั้ง !" in script.text:
                detail = "Wrong Password or verfiy need to email"
        else:
            success = "true"
            detail = "Logged in"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "kaiteedin",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
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
        print(success)
        if success == "true":
            listurl="http://kaiteedin.net/mylisting.php"
            r=httprequestObj.http_get(listurl)
            soup=BeautifulSoup(r.content,'html5lib')
            table=soup.find('table',attrs={'class':'table table-hover'})
            tr=table.findAll('tr')
            l=len(tr)
            finalcurrent=tr[l-1]
            try:
                tdarray=finalcurrent.findAll('td')
                finalpost=tdarray[0].text
            except:
                finalpost="lol"

            if 'name' not in postdata:
                return{
                    'websitename': 'kaiteedin',
                    'success': 'false',
                    'detail': 'Missing required field name',
                    'ret': '',
                    'post_url': '',
                    'post_id': ''
                }
            if 'mobile' not in postdata:
                return{
                    'websitename': 'kaiteedin',
                    'success': 'false',
                    'detail': 'Missing required field mobile',
                    'ret': '',
                    'post_url': '',
                    'post_id': ''
                }
            if 'pass' not in postdata:
                return{
                    'websitename': 'kaiteedin',
                    'success': 'false',
                    'detail': 'Missing required field pass',
                    'ret': '',
                    'post_url': '',
                    'post_id': ''
                }
            if 'user' not in postdata:
                return{
                    'websitename': 'kaiteedin',
                    'success': 'false',
                    'detail': 'Missing required field email',
                    'ret': '',
                    'post_url': '',
                    'post_id': ''
                }
            if 'property_type' not in postdata:
                return{
                    'websitename': 'kaiteedin',
                    'success': 'false',
                    'detail': 'Missing required field property_type',
                    'ret': '',
                    'post_url': '',
                    'post_id': ''
                }
            if 'listing_type' not in postdata:
                return{
                    'websitename': 'kaiteedin',
                    'success': 'false',
                    'detail': 'Missing required field listing_type',
                    'ret': '',
                    'post_url': '',
                    'post_id': ''
                }
            if 'price_baht' not in postdata:
                return{
                    'websitename': 'kaiteedin',
                    'success': 'false',
                    'detail': 'Missing required field price',
                    'ret': '',
                    'post_url': '',
                    'post_id': ''
                }
            if 'post_title_th' not in postdata:
                return{
                    'websitename': 'kaiteedin',
                    'success': 'false',
                    'detail': 'Missing required field title',
                    'ret': '',
                    'post_url': '',
                    'post_id': ''
                }
            if 'post_description_th' not in postdata:
                return{
                    'websitename': 'kaiteedin',
                    'success': 'false',
                    'detail': 'Missing required field description',
                    'ret': '',
                    'post_url': '',
                    'post_id': ''
                }
            if postdata['listing_type'] == 'เช่า':
                postdata['listing_type'] = 'สำหรับเช่า'
            else:
                postdata['listing_type'] = 'สำหรับขาย'
            propertytype = {
                '6': 'ที่ดิน',
                '2': 'บ้าน',
                '1': 'คอนโด',
                '7': 'อพาตเมนต์',
                '5': 'อาคารพาณิชย์',
                '9': 'สำนักงาน',
                '10': 'โกดัง/โรงงาน',
                '25': 'โกดัง/โรงงาน',
                '4': 'ทาวน์โฮม',
                '8': 'อาคารพาณิชย์',
                '3': 'ทาวน์โฮม'
            }
            try:
                postdata['cate_id'] = propertytype[str(
                    postdata['property_type'])]
            except:
                return{
                    'websitename': 'kaiteedin',
                    'success': 'false',
                    'ret': " Wrong property type",
                    'post_url': "",
                    'post_id': ""
                }
            postdata['post_title_th']=postdata['post_title_th'].replace('%','')
            datapost = {
                'listing_name': postdata['name'],
                'listing_type': postdata['listing_type'],
                'listing_prop': postdata['cate_id'],
                'listing_title': postdata['post_title_th'],
                'listing_price': postdata['price_baht']
            }
            url_post = 'http://www.kaiteedin.net/listing.php'
            r = httprequestObj.http_post(url_post, data=datapost)
            soup2 = BeautifulSoup(r.content, 'html5lib')
            postdata['post_project_name']=postdata['post_description_th']
            postdata['post_description_th']=postdata['post_description_th'].replace('\r\n','<br>')
            postdata['post_description_th']=postdata['post_description_th'].replace('\n','<br>')
            floor_total, bedroom, bathroom = [''] * 3
            if 'floor_total' in postdata and postdata['floor_total']!=None: 
                floor_total = str(postdata['floor_total'])
            else:
                if postdata['property_type']=='6' or postdata['property_type']=='10'or postdata['property_type']=='25':
                    pass
                else:
                    floor_total = ''
            if 'bed_room' in postdata and postdata['bed_room']!=None: 
                bedroom = str(postdata['bed_room'])
            else:
                if postdata['property_type']=='6' or postdata['property_type']=='9' or postdata['property_type']=='10'or postdata['property_type']=='25':
                    pass
                else:
                    bedroom=''
            if 'bath_room' in postdata and postdata['bath_room']!=None: 
                bathroom = str(postdata['bath_room'])
            else:
                if postdata['property_type']=='6' or postdata['property_type']=='9' or postdata['property_type']=='10'or postdata['property_type']=='25':
                    pass
                else:
                    bathroom=''


            if 'land_size_ngan' not in postdata or postdata['land_size_ngan']==None:
                postdata['land_size_ngan']=0
            if 'land_size_rai' not in postdata or postdata['land_size_rai']==None:
                postdata['land_size_rai']=0
            if 'land_size_wa' not in postdata or postdata['land_size_wa']==None:
                postdata['land_size_wa']=0
            if 'project_name' not in postdata:
                postdata['project_name']=postdata['post_title_th']
            if len(postdata['post_images'])==0:
                postdata['post_images']=['imgtmp/default/white.jpg']
            # if 'floor_area' in postdata: floor_area = postdata['floor_area']
            floorarea='0'
            # print(postdata['property_type']==1)
            # print(str(postdata['property_type'])=='6' or str(postdata['property_type'])=='1' or str(postdata['property_type'])=='9' or str(postdata['property_type'])=='10' or str(postdata['property_type'])=='25')
            if str(postdata['property_type']) !='6':
                if 'floor_area' not in postdata or postdata['floor_area']==None:
                    postdata['floor_area']=0
                floorarea=str(postdata['floor_area'])+ " ตรม"
                # print(floorarea)
            else:
                # floorarea=str(400*int(postdata['land_size_rai']) + 100 * int(postdata['land_size_ngan']) + int(postdata['land_size_wa'])) +" ตรว"
                floorarea = ""            
            xml = httprequestObj.http_get('http://kaiteedin.net/thailand.xml')
            soup = BeautifulSoup(xml.content, 'lxml')
            province = soup.findAll('table', attrs={'name': 'province'})
            amphur = soup.findAll('table', attrs={'name': 'amphur'})
            district = soup.findAll('table', attrs={'name': 'district'})

            province_id = ''
            province_code = ''
            province_name = ''
            for i in province:
                soup = i
                column = soup.find('column', attrs={'name': 'PROVINCE_NAME'})
                pro = column.text
                if pro.replace(' ', '') == postdata['addr_province']:
                    province_name = postdata['addr_province']
                    province_id = soup.find(
                        'column', attrs={'name': 'PROVINCE_ID'}).text
                    geo_id = soup.find('column', attrs={'name': 'GEO_ID'}).text
                    province_code = soup.find(
                        'column', attrs={'name': 'PROVINCE_CODE'}).text
            amphur_id = ''
            amphur_code = ''
            amphur_name = ''
            postcode=''
            for i in amphur:
                soup = i
                column = soup.find('column', attrs={'name': 'AMPHUR_NAME'})
                amp = column.text
                if amp.replace(' ', '') == postdata['addr_district']:
                    amphur_name = postdata['addr_district']
                    amphur_id = soup.find(
                        'column', attrs={'name': 'AMPHUR_ID'}).text
                    amphur_code = soup.find(
                        'column', attrs={'name': 'AMPHUR_CODE'}).text
                    postcode = soup.find(
                        'column', attrs={'name': 'POSTCODE'}).text

            district_id = ''
            district_code = ''
            district_name = ''
            for i in district:
                soup = i
                column = soup.find('column', attrs={'name': 'DISTRICT_NAME'})
                dis = column.text
                if dis.replace(' ', '') == postdata['addr_sub_district']:
                    district_name = postdata['addr_sub_district']
                    district_id = soup.find(
                        'column', attrs={'name': 'DISTRICT_ID'}).text
                    district_code = soup.find(
                        'column', attrs={'name': 'DISTRICT_CODE'}).text

            prod_address = ""
            for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
                if add is not None and add!="" and add!=" ":
                    prod_address += add + ","
            prod_address = prod_address[:-1]
            confirmtext = 'ระบบบันทึกข้อมูลของคุณแล้ว กรุณารอการตรวจสอบประกาศของคุณภายใน 10 นาที'
            near_by = ""
            if 'addr_near_by' in postdata and postdata['addr_near_by'] is not None:
                near_by = postdata['addr_near_by']

            datapost = [
                ('Listing_name', postdata['name']),
                ('Listing_user_id', soup2.find(
                    'input', attrs={'name': 'Listing_user_id'})['value']),
                ('Listing_email', postdata['email']),
                ('Listing_tel', postdata['mobile']),
                ('Listing_type', postdata['listing_type']),
                ('Listing_pro', 'มือสอง'),
                ('Listing_prop', postdata['cate_id']),
                ('Listing_topic', postdata['post_title_th']),
                ('Listing_add_province', province_id),
                ('Listing_add_amphur', amphur_id),
                ('Listing_add_postcode', postcode),
                ('Listing_add_tambol', district_id),
                ('Listing_add_name', postdata['project_name']),
                ('Listing_add_no', prod_address),
                ('Listing_add_road', postdata['addr_road']),
                ('Listing_floor', floor_total),
                ('Listing_size', floorarea),
                ('Listing_price', postdata['price_baht']),
                ('Listing_bed', bedroom),
                ('Listing_bath', bathroom),
                ('Listing_garage', ''),
                ('Listing_furniture','ไม่มี'),
                ('Listing_kitchen', ''),
                ('Listing_dining', ''),
                ('Listing_living', ''),
                ('Listing_recept', ''),
                ('Listing_storage', ''),
                ('Listing_maid', ''),
                ('Listing_nearplace',near_by),
                ('Listing_desc', postdata['post_description_th']),
                ('Listing_status', 'yes'),
            ]

            # return
            if 'post_images' in postdata and len(postdata['post_images']) > 0:
                pass
            else:
                postdata['post_images'] = ['./imgtmp/default/white.jpg']

            filename = "fileUpload[]"
            file = []
            for i in postdata['post_images'][:9]:
                y=str(random.randint(0,100000000000000000))+".jpg"
                print(y)
                datapost.append(
                    ('fileUpload[]', (y, open(i, "rb"), "image/jpg")))
                file.append(('fileUpload[]', (y, open(i, "rb"), "image/jpg")))
            r = httprequestObj.http_post(
                'http://www.kaiteedin.net/listing_insert.php', data=datapost, files=file)
            data = r.text
            if confirmtext not in data:
                success = "false"
                post_url = ""
                post_id = ""
            else:
                listurl="http://kaiteedin.net/mylisting.php"
                r=httprequestObj.http_get(listurl)
                soup=BeautifulSoup(r.content,'html5lib')
                table=soup.find('table',attrs={'class':'table table-hover'})
                tr=table.findAll('tr')
                l=len(tr)
                final=tr[l-1]
                tdarray=final.findAll('td')
                finalnewpost=tdarray[0].text
                if finalnewpost==finalpost:
                    time_end = datetime.datetime.utcnow()
                    time_usage = time_end - time_start
                    return {
                        "websitename": "kaiteedin",
                        "success": success,
                        "start_time": str(time_start),
                        "end_time": str(time_end),
                        "ds_id": postdata['ds_id'],
                        "post_url": 'post will be approved after 10 minutes',
                        "post_id": ''
                    }
                if tdarray[2].text==postdata['post_title_th']:
                    post_id=tdarray[0].text
                    atd=tdarray[5]
                    post_url="http://kaiteedin.net/"
                    post_url+=atd.find('a')['href']
                    time_end = datetime.datetime.utcnow()
                    time_usage = time_end - time_start
                    return {
                        "websitename": "kaiteedin",
                        "success": success,
                        "start_time": str(time_start),
                        "end_time": str(time_end),
                        "post_url": post_url, 
                        "ds_id": postdata['ds_id'],
                        "post_id": post_id
                    }
                else:
                    time_end = datetime.datetime.utcnow()
                    time_usage = time_end - time_start
                    return {
                        "websitename": "kaiteedin",
                        "success": success,
                        "start_time": str(time_start),
                        "end_time": str(time_end),
                        "post_url": 'post will be created after 10 minutes',
                        "ds_id": postdata['ds_id'],
                        "post_id": ''
                    }
        else:
            post_url = ""
            post_id = ""
            success = "False"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "websitename": "kaiteedin",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": post_url,
            "post_id": post_id,
            "ds_id": postdata['ds_id'],
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
        print(success)
        if success == "true":
            if 'name' not in postdata:
                return{
                'websitename': 'kaiteedin',
                'success': 'false',
                'detail': 'Missing required field name',
                'ret': '',
                'post_url': '',
                'post_id': ''
            }
            if 'mobile' not in postdata:
                return{
                    'websitename': 'kaiteedin',
                    'success': 'false',
                    'detail': 'Missing required field mobile',
                    'ret': '',
                    'post_url': '',
                    'post_id': ''
                }
            if 'pass' not in postdata:
                return{
                    'websitename': 'kaiteedin',
                    'success': 'false',
                    'detail': 'Missing required field pass',
                    'ret': '',
                    'post_url': '',
                    'post_id': ''
                }
            if 'user' not in postdata:
                return{
                    'websitename': 'kaiteedin',
                    'success': 'false',
                    'detail': 'Missing required field email',
                    'ret': '',
                    'post_url': '',
                    'post_id': ''
                }
            if 'property_type' not in postdata:
                return{
                    'websitename': 'kaiteedin',
                    'success': 'false',
                    'detail': 'Missing required field property_type',
                    'ret': '',
                    'post_url': '',
                    'post_id': ''
                }
            if 'listing_type' not in postdata:
                return{
                    'websitename': 'kaiteedin',
                    'success': 'false',
                    'detail': 'Missing required field listing_type',
                    'ret': '',
                    'post_url': '',
                    'post_id': ''
                }
            if 'price_baht' not in postdata:
                return{
                    'websitename': 'kaiteedin',
                    'success': 'false',
                    'detail': 'Missing required field price',
                    'ret': '',
                    'post_url': '',
                    'post_id': ''
                }
            if 'post_title_th' not in postdata:
                return{
                    'websitename': 'kaiteedin',
                    'success': 'false',
                    'detail': 'Missing required field title',
                    'ret': '',
                    'post_url': '',
                    'post_id': ''
                }
            if 'post_description_th' not in postdata:
                return{
                    'websitename': 'kaiteedin',
                    'success': 'false',
                    'detail': 'Missing required field description',
                    'ret': '',
                    'post_url': '',
                    'post_id': ''
                }

            list_url = 'http://kaiteedin.net/mylisting.php'
            r = httprequestObj.http_get(list_url)
            soup = r.text
            if str(postdata['post_id']) not in soup:
                time_end = datetime.datetime.utcnow()
                time_usage = time_end - time_start
                return {
                    "websitename": "kaiteedin",
                    "success": 'false',
                    "start_time": str(time_start),
                    "end_time": str(time_end),
                    "detail": 'Wrong Post id'
                }
       
            prod_address = ""
            for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
                if add is not None:
                    prod_address += add + ","
            prod_address = prod_address[:-1]
            confirmtext = 'ระบบบันทึกข้อมูลของคุณแล้ว กรุณารอการตรวจสอบประกาศของคุณภายใน 10 นาที'


            prod_address = ""
            for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
                if add is not None:
                    prod_address += add + ","
            prod_address = prod_address[:-1]
            if postdata['listing_type'] == 'เช่า':
                postdata['listing_type'] = 'สำหรับเช่า'
            else:
                postdata['listing_type'] = 'สำหรับขาย'
            propertytype = {
                '6': 'ที่ดิน',
                '2': 'บ้าน',
                '1': 'คอนโด',
                '7': 'อพาตเมนต์',
                '5': 'อาคารพาณิชย์',
                '9': 'สำนักงาน',
                '10': 'โกดัง/โรงงาน',
                '25': 'โกดัง/โรงงาน',
                '4': 'ทาวน์โฮม',
                '8': 'อาคารพาณิชย์',
                '3': 'ทาวน์โฮม'
            }
            try:
                postdata['cate_id'] = propertytype[str(
                    postdata['property_type'])]
            except:
                return{
                    'websitename': 'kaiteedin',
                    'success': 'false',
                    'ret': " Wrong property type",
                    'post_url': "",
                    'post_id': ""
                }
            
            postdata['post_title_th']=postdata['post_title_th'].replace('%','')
            postdata['post_project_name']=postdata['post_description_th']
            postdata['post_description_th']=postdata['post_description_th'].replace('\r\n','<br>')
            postdata['post_description_th']=postdata['post_description_th'].replace('\n','<br>')
            floor_total, bedroom, bathroom = [''] * 3
            if 'floor_total' in postdata and postdata['floor_total']!=None: 
                floor_total = str(postdata['floor_total'])
            else:
                if postdata['property_type']=='6' or postdata['property_type']=='10'or postdata['property_type']=='25':
                    pass
                else:
                    floor_total = '2'
            if 'bed_room' in postdata and postdata['bed_room']!=None: 
                bedroom = str(postdata['bed_room'])
            else:
                if postdata['property_type']=='6' or postdata['property_type']=='9' or postdata['property_type']=='10'or postdata['property_type']=='25':
                    pass
                else:
                    bedroom='2'
            if 'bath_room' in postdata and postdata['bath_room']!=None: 
                bathroom = str(postdata['bath_room'])
            else:
                if postdata['property_type']=='6' or postdata['property_type']=='9' or postdata['property_type']=='10'or postdata['property_type']=='25':
                    pass
                else:
                    bathroom='2'
            if 'land_size_ngan' not in postdata or postdata['land_size_ngan']==None:
                postdata['land_size_ngan']=0
            if 'land_size_rai' not in postdata or postdata['land_size_rai']==None:
                postdata['land_size_rai']=0
            if 'land_size_wa' not in postdata or postdata['land_size_wa']==None:
                postdata['land_size_wa']=0
            if 'project_name' not in postdata:
                postdata['project_name']=postdata['post_title_th']
            if len(postdata['post_images'])==0:
                postdata['post_images']=['imgtmp/default/white.jpg']
            # if 'floor_area' in postdata: floor_area = postdata['floor_area']
            floorarea='0'
            if str(postdata['property_type']) !='6':
                if 'floor_area' not in postdata:
                    postdata['floor_area']=0
                floorarea = str(postdata['floor_area'])+ " ตรม"
            else:
                floorarea = ""
            near_by = ""
            if 'addr_near_by' in postdata and postdata['addr_near_by'] is not None:
                near_by = postdata['addr_near_by']
            datapost=[
                ('Listing_id',postdata['post_id']),
                ('Listing_type', postdata['listing_type']),
                ('Listing_pro', 'มือสอง'),
                ('Listing_prop', postdata['cate_id']),
                ('Listing_topic', postdata['post_title_th']),
                ('Listing_add_name',postdata['project_name']),
                ('Listing_add_no', prod_address),
                ('Listing_add_road', postdata['addr_road']),
                ('Listing_floor', floor_total),
                ('Listing_size', floorarea),
                ('Listing_price', postdata['price_baht']),
                ('Listing_bed', bedroom),
                ('Listing_bath', bathroom),
                ('Listing_garage', ''),
                ('Listing_furniture','ไม่มี'),
                ('Listing_kitchen', ''),
                ('Listing_dining', ''),
                ('Listing_living', ''),
                ('Listing_recept', ''),
                ('Listing_storage', ''),
                ('Listing_maid', ''),
                ('Listing_nearplace',near_by),
                ('Listing_desc', postdata['post_description_th']),
                ('Listing_status', 'yes'),
                ]
            r = httprequestObj.http_post(
                'http://kaiteedin.net/mylisting_edit_save.php', data=datapost)
            data = r.text
            if 'ระบบบันทึกข้อมูลของคุณแล้ว' in data:
                detail="edited"
            else:
                success = "False"
                detail = "Failed to Edit"

        else:
            success = "False"
            detail = "Login Error"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "websitename": "kaiteedin",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "log_id": postdata['log_id'],
        }



    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        # login

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        list_url = 'http://kaiteedin.net/mylisting.php'
        r = httprequestObj.http_get(list_url)
        soup = r.text
        if str(postdata['post_id']) not in soup:
            time_end = datetime.datetime.utcnow()
            time_usage = time_end - time_start
            return {
                "log_id": postdata['log_id'],
                "websitename": "kaiteedin",
                "success": 'false',
                "start_time": str(time_start),
                "end_time": str(time_end),
                "detail": 'Wrong Post id',
            }
        if success == "true":
            datapost = {
                'id': postdata['post_id']
            }
            urldel = 'http://kaiteedin.net/mylisting_delete.php?id=' + \
                str(postdata['post_id'])
            r = httprequestObj.http_post(
                urldel, data=datapost)
            data = r.text
            if 'ลบข้อมูลเรียบร้อย' not in data:
                success = "false"
                detail = "Failed to Delete"
            else:
                detail = "Deleted"
        else:
            success = "false"
            detail = "Failed Login"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "log_id": postdata['log_id'],
            "websitename": "kaiteedin",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
        }
    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        # login

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        list_url = 'http://kaiteedin.net/mylisting.php'
        r = httprequestObj.http_get(list_url)
        soup = r.text
        if str(postdata['post_id']) not in soup:
            time_end = datetime.datetime.utcnow()
            time_usage = time_end - time_start
            return {
                "log_id": postdata['log_id'],
                "websitename": "kaiteedin",
                "success": 'false',
                "start_time": str(time_start),
                "end_time": str(time_end),
                "detail": 'Wrong Post id',
            }
        if success == "true":
            datapost=[
                ('Listing_id',postdata['post_id'])
            ]
            r = httprequestObj.http_post(
                'http://kaiteedin.net/mylisting_edit_save.php', data=datapost)
            data = r.text
            if 'ระบบบันทึกข้อมูลของคุณแล้ว' in data:
                detail="edited"
            else:
                success = "False"
                detail = "Failed to Edit"
        else:
            success = "False"
            detail = "Login Error"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "log_id": postdata['log_id'],
            "websitename": "kaiteedin",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
        }


# obj = kaiteedin()
# postdata = {
#     'post_id': '171128',
#     'user': 'tirth.upadhyaya20012001@gmail.com',
#     'pass': 'temptemp',
#     'name': 'temp1234',
#     'name_th': 'temp1234',
#     'surname_th': 'temp1234',
#     'property_type': '2',
#     'mobile': '12345678',
#     'geo_latitude': '13',
#     'geo_longitude': '34',
#     'price_baht': '2123',
#     'post_title_th': 'FUUU',
#     'post_description_th': 'fasdfasdfasfasdgasd',
#     'listing_type': 'ffer',
#     'addr_province': 'ชลบุรี',
#     'addr_district': 'บางละมุง',
#     'addr_sub_district': 'นาเกลือ',
#     'tel': '14241412',
#     "addr_road": "ถนน",
#     "addr_soi": "ซอย",
#     "addr_near_by": "สถานที่ใกล้เคียง",
#     'post_images': ['./imgtmp/default/white.jpg']
# }
# print(obj.register_user(postdata))
# print(obj.test_login(postdata))
# print(obj.create_post(postdata))
# print(obj.edit_post(postdata))
# print(obj.delete_post(postdata))
# print(obj.boost_post(postdata))