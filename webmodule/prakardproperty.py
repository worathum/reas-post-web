# -*- coding: utf-8 -*-

from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
import re
import json
import datetime
import sys

class prakardproperty():

    name = 'prakardproperty'

    def __init__(self):

        try:
            import configs
        except ImportError:
            configs = {}

        self.httprequestObj = lib_httprequest()
        self.primarydomain = 'http://www.prakardproperty.com/'
        self.debug = 0

    def register_user(self, userdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        email = userdata['user']
        passwd = userdata['pass']
        display_name = userdata['name_th']
        mobile = userdata['tel']
        
        datapost={
            'data[Members][email]':email,
            'data[Members][password]':passwd,
            'data[Members][re-password]':passwd,
            'data[Members][display_name]':display_name,
            'data[Members][mobile]': mobile,
            'data[Members][accept_newsletter]' : 0
        }
        try:
            r = self.httprequestObj.http_post('http://www.prakardproperty.com/register/save', data=datapost)
            data = r.text
            matchObj = re.search(r'/register/resentmail', data)
            if matchObj:
                success = "True"
                detail = "Sucessful Registration"
            else:
                success = "False"
                detail = "Not Registered"
        except:
            success = "True"
            detail = "Sucessful Registration"


        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "prakardproperty",
            "success": success,
            'ds_id': userdata['ds_id'],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
        }

    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        success = False
        detail = 'Login unsuccess'
        datapost = {
            'login_email' : postdata['user'],
            'login_password' : postdata['pass']
        }
        r = self.httprequestObj.http_post('http://www.prakardproperty.com/login/checkmember', data=datapost)
        
        if r.url == 'http://www.prakardproperty.com/':
            success = True
            detail = 'Login successful'
        else:
            success = False
            detail = 'Login unsuccessful'

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "prakardproperty",
            "success": success,
            "ds_id": postdata['ds_id'],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "usage_time": str(time_usage),
            "detail": detail,
        }

    def check_post(self,postdata):
        r = self.httprequestObj.http_get('http://www.prakardproperty.com/property/show/{}'.format(postdata['post_id']))
        if 'Sorry, The requested URL was not found on this server.' in r.text:
            Found = False
        else:
            Found = True
        return Found

    def post_prop(self,action,postdata):
        success = False
        detail = 'Something wrong in this website.'
        post_id =  postdata['post_id']
        post_url = 'http://www.prakardproperty.com/property/show/'+post_id
        if action == 'create':
            r = self.httprequestObj.http_get('http://www.prakardproperty.com/properties/add')
            soup = BeautifulSoup(r.content, 'html.parser')
            upload_id = soup.find("input", {"id": "running_number"}).get('value')
        else:
            r = self.httprequestObj.http_get('http://www.prakardproperty.com/properties/edit/{}'.format(postdata['post_id']))
            soup = BeautifulSoup(r.content, 'html.parser')
        
        province = soup.find("select", {"id": "province"}).find_all('option')
        if postdata['addr_province'] == 'กรุงเทพ':
            postdata['addr_province'] = 'กรุงเทพมหานคร'
        province_id = [s for s in province if postdata['addr_province'] in s][0].get('value')

        r = self.httprequestObj.http_post('http://www.prakardproperty.com/location/getdistrict/mode:geomap/province_id:{}'.format(province_id),data={})
        soup = BeautifulSoup(r.content, 'html.parser')
        district = soup.find_all('option')
        district_id = [s for s in district if postdata['addr_district'] in s][0].get('value')
        r = self.httprequestObj.http_post('http://www.prakardproperty.com/location/getsubdistrict/mode:geomap/province_id:2/district_id:{}'.format(district_id),data={})
        soup = BeautifulSoup(r.content, 'html.parser')
        subdistrict = soup.find_all('option')
        try:
            subdistrict_id = [s for s in subdistrict if postdata['addr_sub_district'] in s][0].get('value')
            r = self.httprequestObj.http_post('http://www.prakardproperty.com/location/getsubdistrict_geo/mode:geomap/province_id:2/district_id:16/sub_district_id:{}'.format(subdistrict_id),data={})
            success = True
        except:
            success = False
            detail = 'This subdistrict does not exist on this site.'
        if action == 'edit':
            Found = self.check_post(postdata)
            if not Found:
                success = False
                detail = 'Post id not found.'
        if success:
            propety_type = {
                '1': '3',
                '2': '1',
                '3': '1',
                '4': '2',
                '5': '4',
                '6': '6',
                '7': '5',
                '8': '5',
                '9': '9',
                '10': '7',
                '25': '7',
                '30': '6'
            }

            purposeId = {
                'ขาย': 1,
                'เช่า': 2
            }

            if postdata['floor_level'] == '':
                postdata['floor_level'] = postdata['floor_total']

            prod_address = ""
            for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
                if add is not None:
                    prod_address += add + ","
            prod_address = prod_address[:-1]

            datapost = {
                'data[Properties][title]': postdata["post_title_th"],
                'data[Properties][property_type_id]': propety_type[postdata['property_type']],
                'data[Properties][property_post_type_id]': purposeId[postdata['listing_type']],
                'data[Properties][size_square_metre]': postdata['floorarea_sqm'],
                'data[Properties][land_size_rai]': postdata['land_size_rai'],
                'data[Properties][land_size_ngan]': postdata['land_size_ngan'],
                'data[Properties][land_size_wah]': postdata['land_size_wa'],
                'data[Properties][floor_no]': postdata['floor_level'],
                'data[Properties][bedroom]': postdata['bed_room'],
                'data[Properties][bathroom]': postdata['bath_room'],
                'data[PropertyDetails][address]': prod_address,
                'data[PropertyDetails][street]': postdata['addr_soi'],
                'data[PropertyDetails][road]': postdata['addr_road'],
                'data[Properties][province_id]': province_id,
                'data[Properties][district_id]': district_id,
                'data[Properties][sub_district_id]': subdistrict_id,
                'data[PropertyDetails][google_map_latitude]': postdata['geo_latitude'],
                'data[PropertyDetails][google_map_longitude]': postdata['geo_longitude'],
                'data[PropertyDetails][location_datail]': '',
                'data[Properties][youtube]': '' ,
                'data[PropertyDetails][detail]': postdata['post_description_th']
            }
            if purposeId[postdata['listing_type']] == 1:
                datapost['data[Properties][sell_price]'] =  postdata['price_baht']
                datapost['data[Properties][unit_type_id1]'] = 1
                datapost['data[Properties][unit_type_id2]'] = None
            else:
                datapost['data[Properties][rental_price]'] =  postdata['price_baht']
                datapost['data[Properties][unit_type_id1]'] = None
                datapost['data[Properties][unit_type_id2]'] = 2
            if action == 'edit':
                datapost['data[Properties][id]'] = postdata['post_id']
                r = self.httprequestObj.http_get('http://www.prakardproperty.com/filesupload/updateimagelists/id:{}'.format(postdata['post_id']))
                soup = BeautifulSoup(r.content, 'html.parser')
                img_item = soup.find_all("div", {"class": "item"})
                if len(img_item) != 0:
                    for i in img_item:
                        r = self.httprequestObj.http_post('http://www.prakardproperty.com/filesupload/deletepostimage/id:{}'.format(i.get('title')),data={})
                for i in postdata['post_images']:
                    files = {'files[]': (i, open(i, "rb"), "image/jpeg")}
                    r = self.httprequestObj.http_post('http://www.prakardproperty.com/filesupload/properties/id:{}'.format(postdata['post_id']), data=datapost, files=files)
                r = self.httprequestObj.http_get('http://www.prakardproperty.com/filesupload/updateimagelists/id:{}'.format(postdata['post_id']))
                soup = BeautifulSoup(r.content, 'html.parser')
                img_item = soup.find_all("div", {"class": "item"})
                img = []
                for i in img_item:
                    img.append(int(i.get('title')))
                img.sort()
                url = 'http://www.prakardproperty.com/filesupload/updatepostorder/id:'
                for i in img:
                    url += str(i)+','
                r = self.httprequestObj.http_post(url[:-1], data={})
                r = self.httprequestObj.http_post('http://www.prakardproperty.com/properties/editsave', data=datapost)
                if r.status_code == 200:
                    success == True
                else:
                    success == False
            else:
                datapost['data[Properties][running_number]'] = upload_id
                for i in postdata['post_images']:
                    files = {'files[]': (i, open(i, "rb"), "image/jpeg")}
                    r = self.httprequestObj.http_post('http://www.prakardproperty.com/filesupload/temp/id:{}'.format(upload_id), data=datapost, files=files)
                r = self.httprequestObj.http_get('http://www.prakardproperty.com/filesupload/updatetemplists/running_number:{}'.format(upload_id))
                soup = BeautifulSoup(r.content, 'html.parser')
                img_item = soup.find_all("div", {"class": "item"})
                img = []
                for i in img_item:
                    img.append(int(i.get('title')))
                img.sort()
                url = 'http://www.prakardproperty.com/filesupload/updatetemporder/id:'
                for i in img:
                    url += str(i)+','
                r = self.httprequestObj.http_post(url[:-1], data={})
                datapost['propertyConfirm1'] = 'on'
                r = self.httprequestObj.http_post('http://www.prakardproperty.com/properties/addsave', data=datapost)
                try:
                    soup = BeautifulSoup(r.content, 'html.parser')
                    post_id = str(soup.find("div", {"id": "content"}).find_all('a')[0].get('href')).split('show/')[1]
                    post_url = 'http://www.prakardproperty.com/property/show/'+post_id
                    success = True
                except:
                    success = False
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
        detail = 'Something wrong in this website.'
        login = self.test_login(postdata)
        success = login['success']
        detail = login['detail']
        post_url = ''
        post_id = ''
        
        if success:
            create = self.post_prop('create',postdata)
            success = create['success']
            if success:
                detail = 'Post successful'
                post_id = create['post_id']
                post_url = create['post_url']
            else:
                detail = create['detail']
        else:
            detail = login['detail']

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "prakardproperty",
            "success": success,
            "time_usage": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": postdata['ds_id'],
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "",
            "detail": detail
        }

    def edit_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        success = False
        detail = 'Something wrong in this website.'
        login = self.test_login(postdata)
        success = login['success']
        detail = login['detail']

        if success:
            edit = self.post_prop('edit',postdata)
            success = edit['success']
            if success:
                detail = 'Edit successful'
            else:
                detail = edit['detail']
        else:
            detail = login['detail']

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "prakardproperty",
            "success": success,
            "time_usage": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_url": '',
            "post_id": postdata['post_id'],
            "account_type": "",
            "detail": detail
        }

    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        
        success = False
        detail = ''
        login = self.test_login(postdata)
        success = login["success"]
        post_id = postdata['post_id']

        if success:
            Found = self.check_post(postdata)
            if not Found:
                success = False
                detail = 'Post id not found.'
            else:
                r = self.httprequestObj.http_get('http://www.prakardproperty.com/properties/updatedate/{}'.format(post_id))
                if 'OK' in r.text:
                    success = True
                    detail = "Post sucessfully Boosted"
                else:
                    success = False
                    detail = "Cannot Boost this post."
        else:
            detail = login["detail"]

        time_end = datetime.datetime.utcnow()
        return {
            "websitename": "prakardproperty",
            "success": success,
            "time_usage": time_end - time_start,
            "start_time": time_start,
            "end_time": time_end,
            'ds_id': postdata['ds_id'],
            "detail": detail,
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "post_view": ""
        }

    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        
        success = False
        detail = ''
        login = self.test_login(postdata)
        success = login["success"]
        post_id = postdata['post_id']

        if success:
            Found = self.check_post(postdata)
            if not Found:
                success = False
                detail = 'Post id not found.'
            else:
                r = self.httprequestObj.http_post('http://www.prakardproperty.com/properties/delete/{}'.format(post_id),data={})
                if 'delete property success' in r.text:
                    success = True
                    detail = "Delete sucessfully"
                else:
                    success = False
                    detail = "Cannot delete this post."
        else:
            detail = login["detail"]

        time_end = datetime.datetime.utcnow()
        return {
            "websitename": "prakardproperty",
            "success": success,
            "time_usage": time_end - time_start,
            "start_time": time_start,
            "end_time": time_end,
            "detail": detail,
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id":postdata['post_id']
        }

    def search_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        if success:
            post_title = postdata['post_title_th']

            url = "http://www.prakardproperty.com/member/posted"
            r = self.httprequestObj.http_get(url)
            exists = False
            soup = BeautifulSoup(r.content, 'lxml')
            post_url = ""
            post_modify_time = ""
            post_view = ""
            post_found = "false"
            entry = soup.find('div', attrs={'id':'member-list'})
            for title_row in entry.find_all('div', attrs={'class':'c3'}):
                if title_row is None:
                    continue
                title = title_row.find('a')
                title_1=title.text.strip()
                if post_title == title_1:
                    exists = True
                    post_id = title['href'][-6:]
                    post_url = "https://www.prakardproperty.com/property/show/"+post_id
                    post_modify_time = title_row.find('span', attrs={'class':'update'}).text[13:-2]
                    post_view = title_row.find('p', attrs={'class':'stat'}).text[7:]
                    post_found = "true"
                    detail = "post found successfully"

            if not exists:
                detail = "No post found with given title."

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": "true",
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": "prakardproperty",
            "account_type":None,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "post_modify_time": post_modify_time,
            "post_view": post_view,
            "post_url": post_url,
            "post_found": post_found
        }



    def print_debug(self, msg):
        if(self.debug == 1):
            print(msg)
        return True

    def print_debug_data(self, data):
        if(self.debugdata == 1):
            print(data)
        return True
