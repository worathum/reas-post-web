# -*- coding: utf-8 -*-

from .lib_httprequest import *
from bs4 import BeautifulSoup
import datetime
import sys

class livingjoin():

    name = 'livingjoin'

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
        self.httprequestObj = lib_httprequest()

    def test_login(self, postdata):
        time_start = datetime.datetime.utcnow()

        success = False
        detail = 'Something wrong'

        datapost = {
            'refer': '',
            'login_username': postdata['user'],
            'login_password': postdata['pass']
        }
        r = self.httprequestObj.http_post('https://www.livingjoin.com/login', data=datapost)
        r = self.httprequestObj.http_get('https://www.livingjoin.com/member/account')

        if r.url == 'https://www.livingjoin.com/member/account':
            success = True
            detail = 'Login successful'
        else:
            detail = 'Wrong username or password'

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": "livingjoin",
            "ds_id": postdata['ds_id'],
        }

    def post_prop(self, postdata,action):
        success =False
        detail = 'Something wrong'
        post_url = ''
        post_id = ''
        province_id = ''
        district_id = ''
        subdistrict_id = ''

        property_type = {
            '1':'3',
            '2':'1',
            '3':'1',
            '4':'2',
            '5':'5',
            '6':'8',
            '7':'4',
            '8':'4',
            '9':'6',
            '10':'7',
            '25':'7'
        }

        property_type_tag = {
                '1':'คอนโด',
                '2':'บ้านเดี่ยว',
                '3':'บ้านแฝด',
                '4':'ทาวน์เฮ้าส์',
                '5':'ตึกแถว-อาคารพาณิชย์',
                '6':'ที่ดิน',
                '7':'อพาร์ทเมนท์',
                '8':'โรงแรม',
                '9':'ออฟฟิศสำนักงาน',
                '10':'โกดัง',
                '25':'โรงงาน'
            }

        sub_propertytype = {
            '1':'3',
            '2':'1',
            '3':'2',
            '4':'',
            '5':'',
            '6':'7',
            '7':'10',
            '8':'11',
            '9':'18',
            '10':'21',
            '25':'20'
        }
        postdata['property_type'] = property_type_tag[postdata['property_type']]
        tag = ''
        for i in ['addr_province','addr_district','addr_sub_district','listing_type','property_type']:
            if postdata[i] != '':
                tag += postdata[i] + ','
        tag += 'ราคาถูก'

        sub_propertytype = sub_propertytype[postdata['property_type']]
        listing_type = {'ขาย' : '1','เช่า':'2'}
        postdata['property_type'] = property_type[postdata['property_type']]
        postdata['listing_type'] = listing_type[postdata['listing_type']]

        r = self.httprequestObj.http_get('https://www.livingjoin.com/member/post?prop_type_id={}'.format(postdata['property_type']))
        soup = BeautifulSoup(r.content, features = "html.parser")
        provinces = soup.find('select', {'id': 'province_id'})
        provinces = provinces.find_all('option')

        if postdata['addr_province'] == 'กรุงเทพ':
            postdata['addr_province'] = 'กรุงเทพมหานคร'
        for province in provinces:
            if province.text == postdata['addr_province']:
                province_id = province['value']
                break
        get_district = {
            'province_id': province_id,
            'PH': '../../',
            'andval': '0.94461133400528'
        }
        r = self.httprequestObj.http_post('https://www.livingjoin.com/ajax/misc/set_province?province_id={}&PH=../../&andval=0.94461133400528'.format(province_id), data=get_district)
        for i in (r.text).split('option'):
            if postdata['addr_district'] in i:
                district_id = i.split('"')[1]
                break

        get_subdistrict = {
            'amphur_id': district_id,
            'PH': '../../',
            'andval': '0.33840354397483763'
        }
        r = self.httprequestObj.http_post('https://www.livingjoin.com/ajax/misc/set_district?amphur_id={}&PH=../../&andval=0.33840354397483763'.format(district_id), data=get_subdistrict)
        
        for i in (r.text).split('option'):
            if postdata['addr_sub_district'] in i:
                subdistrict_id = i.split('"')[1]
                break

        if postdata['floor_level'] == '':
            postdata['floor_level'] = postdata['floor_total']

        if province_id == '' or district_id == '' or subdistrict_id == '':
            detail = 'This subdistrict does not exist on this site.'
        #############place_list
        else:
            data = [
                ('prop_type_id', postdata['property_type']),
                ('small_fb', '1'),
                ('title_x', postdata['post_title_th']),
                ('post_type_id', postdata['listing_type']),
                ('price', postdata['price_baht']),
                ('price_type_id', '1'),
                ('province_id', province_id),
                ('amphur_id', district_id),
                ('district_id', subdistrict_id),
                ('place_list[]',''),
                ('place_list[]',''),
                ('place_list[]', ''),
                ('unit_type_id', sub_propertytype),
                ('room_class', postdata['floor_level']),
                ('total_class', postdata['floor_total']),
                ('total_bedroom',postdata['bed_room']),
                ('total_bathroom',postdata['bath_room']),
                ('total_kitchenroom', '0'),
                ('total_livingroom','0'),
                ('total_carpark','0'),
                ('size_rai', postdata['land_size_rai']),
                ('size_gan',postdata['land_size_ngan']),
                ('size_va',postdata['land_size_wa']),
                ('unit_size', postdata['floorarea_sqm']),
                ('unit_width',''),
                ('unit_height',''),
                ('living_area', postdata['floorarea_sqm']),
                ('have_detail','yes'),
                ('detail', postdata['post_description_th']),
                ('dir_name', 'classified'),
                ('default_pic','201221144551161242.jpg' ),
                ('feature_list_other[]',''),
                ('feature_list_other[]',''),
                ('feature_list_other[]',''),
                ('display_map', 'H'),
                ('lat', postdata['geo_latitude']),
                ('lng', postdata['geo_longitude']),
                ('formatted_address','' ),
                ('tag_list', tag),
                ('fullname', postdata['name']),
                ('phone', postdata['mobile']),
                ('post','')
            ]
            files = []
            for i in postdata['post_images'][:10]:
                files.append(('imageproduct[]',((i, open(i, "rb"), "image/jpeg"))))

        return {
            'success': success,
            'detail': detail,
            'post_id': post_id,
            'post_url': post_url
        }

    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        success = False
        detail = 'Something wrong'
        post_url = ''
        post_id = ''
        test_login = self.test_login(postdata)
        success = test_login["success"]
        
        if success:
            success =False
            post = self.post_prop(postdata,'post')
            success = post['success']
            if success:
                detail = 'Post successful'
                post_id = post['post_id']
                post_url = post['post_url']
            else:
                detail = post['detail']
        else:
            detail = test_login["detail"]

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
            "websitename": "livingjoin",
        }
    
    def print_debug(self, msg):
        if(self.debug == 1):
            print(msg)
        return True