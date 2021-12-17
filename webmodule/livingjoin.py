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
        
        listing_type = {'ขาย' : '1','เช่า':'2'}
        postdata['property_type'] = property_type[postdata['property_type']]
        postdata['listing_type'] = listing_type[postdata['listing_type']]
        #############################ทำscrap province ต่อ
        r = self.httprequestObj.http_get('https://www.livingjoin.com/member/post?prop_type_id={}'.format(postdata['property_type']))
        soup = BeautifulSoup(r.content, features = "html.parser")
        provinces = soup.find('select', {'id': 'province_id'})
        provinces = provinces.find_all('option')[1:]
        print(provinces)

        data = [
            ('prop_type_id', postdata['property_type']),
            ('small_fb', '1'),
            ('title_x', postdata['post_title_th']),
            ('post_type_id', postdata['listing_type']),
            ('price', postdata['price_baht']),
            ('price_type_id', '1'),
            ('province_id', '2'),
            ('amphur_id', '52'),
            ('district_id', '238'),
            ('place_list[]',''),
            ('place_list[]',''),
            ('place_list[]', ''),
            ('unit_type_id', '9'),
            ('room_class', '2'),
            ('unit_size', '32'),
            ('unit_width',''),
            ('unit_height',''),
            ('living_area', '32'),
            ('have_detail',''),
            ('detail', postdata['post_description_th']),
            ('dir_name', 'classified'),
            ('default_pic','' ),
            ('feature_list_other[]',''),
            ('feature_list_other[]',''),
            ('feature_list_other[]',''),
            ('display_map', 'H'),
            ('lat', '13.7563309'),
            ('lng', '100.50176510000006'),
            ('formatted_address','' ),
            ('tag_list', ''),
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