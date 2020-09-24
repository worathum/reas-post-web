# -*- coding: utf-8 -*-

from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
import re
import json
import datetime
import sys
import requests
from urllib.parse import quote


property_types = {
    '2': '1',
    '3': '2',
    '4': '3',
    '1': '4',
    '7': '5',
    '5': '6',
    '9': '8',
    '10': '9',
    '25': '9',
    '6': '10',
    '8': '11'
}
httprequestObj = lib_httprequest()

class baan2day():
    name = 'baan2day'
    site_name = "https://www.baan2day.com"
   
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

        # start process
        success = "false"
        detail = 'An Error has Occurred'

        datapost = {
            "tname": postdata['user'],
            "tmyemail": postdata['user'],
            "tmypassword": postdata['pass'],
            "tconfirmpass": postdata['pass']
        }

        response = httprequestObj.http_post(self.site_name+'/member_register_aed.php?typ=add', data=datapost)
    
        if response.status_code==200:
            if "window.location.href='member.php';" in response.text:
                success = "true"
                detail = "Registration Successful!"
            elif "window.history.back();" in response.text:
                detail = "This email has already been used. Can not Register!"
        else:
            detail = 'An Error has Occurred with response code '+str(response.status_code)
            
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            'ds_id': postdata['ds_id'],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": self.name,
            "ds_id": postdata['ds_id']
        }



    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        
        # start process
        success = "false"
        detail = 'An Error has Occurred'

        datapost = {
            "tlogin_email": postdata['user'],
            "tlogin_password": postdata['pass']
        }
        
        response = httprequestObj.http_post(self.site_name+'/login_aed.php', data=datapost)
        
        if response.status_code==200:
            soup = BeautifulSoup(response.text, features=self.parser)
            scripts = soup.find_all('script')
            if len(scripts)==1:
                detail = "Email or password is incorrect."
            elif len(scripts)==2:
                success = "true"
                detail = "Login Successful!"
        else:
            detail = 'An Error has Occurred with response code '+str(response.status_code)

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": self.name,
            "ds_id": postdata['ds_id']
        }

    

    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        # login

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = "Unable to create post"
        post_id = ""
        post_url = ""

        if 'web_project_name' not in postdata or postdata['web_project_name'] is None:
            if 'project_name' in postdata and postdata['project_name'] is not None:
                postdata['web_project_name'] = postdata['project_name']
            else:
                postdata['web_project_name'] = postdata['post_title_th']
        
        if success=="true":
            taddress = ""
            for add in [postdata['addr_soi'],postdata['addr_road'],postdata['addr_sub_district'],postdata['addr_district'],postdata['addr_province']]:
                if add:
                    taddress += add + " "

            addr_province = postdata['addr_province']
            addr_district = postdata['addr_district']
            province = '64'
            district = '867'
            with open('./static/baan2day_province.json') as f:
                data = json.load(f)
            
            for key in data["provinces"]:
                if (addr_province.find(str(key)) != -1) or (str(key).find(addr_province) != -1):
                    province = data["provinces"][key]
                    break
            for key in data["districts"][province]:
                if(addr_district.find(str(key)) != -1)  or (str(key).find(addr_district) != -1):
                    district = data["districts"][province][key]
                    break
            
            area = ''
            if 'floor_area' in postdata:
                area = postdata["floor_area"]
            elif 'floorarea_sqm' in postdata:
                area = postdata['floorarea_sqm']
            if postdata['property_type']=="6":
                if postdata['land_size_ngan'] is None:
                        postdata['land_size_ngan'] = 0
                if postdata['land_size_rai'] is None:
                    postdata['land_size_rai'] = 0
                if postdata['land_size_wa'] is None:
                    postdata['land_size_wa'] = 0
                try:
                    postdata['land_size_ngan'] = int(postdata['land_size_ngan'])
                except ValueError:
                    postdata['land_size_ngan'] = 0
                try:
                    postdata['land_size_rai'] = int(postdata['land_size_rai'])
                except ValueError:
                    postdata['land_size_rai'] = 0
                try:
                    postdata['land_size_wa'] = int(postdata['land_size_wa'])
                except ValueError:
                    postdata['land_size_wa'] = 0
                area = 4*(400 * postdata["land_size_rai"] + 100 * postdata["land_size_ngan"] + postdata["land_size_wa"])
            
            floor_total, bath_room = '', ''
            if 'floor_total' in postdata:
                floor_total = postdata['floor_total']
            if 'bath_room' in postdata:
                bath_room = postdata['bath_room']

            datapost= {
                "property_type": '1' if postdata['listing_type']=='ขาย' else '2',
                "property_format": property_types[str(postdata['property_type'])],
                "thomedetail_title": postdata['post_title_th'].replace("\u2013",""),
                "thomedetail_name": postdata["web_project_name"],
                "thomedetail_address": taddress,
                "tprovince": province,
                "tamphur": district,
                "thomedetail_detail": postdata["post_description_th"],
                "thomedetail_floor": floor_total,
                "thomedetail_room": "",
                "thomedetail_bathroom": bath_room,
                "thomedetail_area": area,
                "thomedetail_price": postdata['price_baht'],
                "tuser_name": postdata['name'],
                "tuser_tel": postdata['mobile'].replace('-',''),
                "tuser_email": postdata['email'],
                "latitude": postdata['geo_latitude'],
                "longitude": postdata['geo_longitude']
            }

            files = {}
            for i,image in enumerate(postdata["post_images"][:10]):
                files["testimage"+str(i+1)] = open(os.getcwd()+"/"+image, 'rb')
    
            response = httprequestObj.http_post(self.site_name+'/member_property_aed.php?typ=add', data=datapost, files=files)
            # print(response.content)
            
            success = "false" 
            if response.status_code==200:
                if "window.location.href='member_property_list.php" in response.text:
                    success = "true"
                    detail = "Post Created Successfully!"
                    r = httprequestObj.http_get(self.site_name+'/member_property_list.php')
                    soup = BeautifulSoup(r.text, features=self.parser)
                    try:
                        rows = soup.find('tbody').find_all('tr')
                    except:
                        try:
                            time.sleep(3)
                            r = httprequestObj.http_get(self.site_name+'/member_property_list.php')
                            soup = BeautifulSoup(r.text, features=self.parser)
                            rows = soup.find('tbody').find_all('tr')
                        except:
                            rows = []
                            success = "false"
                            detail = "post created probably but not active yet."
                    if rows:
                        post = rows[0]
                        try:
                            td = post.find_all('td')
                            post_id = td[3].find('a').get('href').split('id=')[1]
                            post_url = self.site_name+'/homedisplay/'+post_id+'/'+quote(td[1].getText().strip())+'.html'
                        except (TypeError, IndexError):
                            pass
                    # for post in rows:
                    #     try:
                    #         td = post.find_all('td')
                    #         if td[1].getText().strip()==' '.join(str(postdata['post_title_th'].replace("\u2013","")).strip().split()):
                    #             post_id = td[3].find('a').get('href').split('id=')[1]
                    #             post_url = self.site_name+'/homedisplay/'+post_id+'/'+quote(td[1].getText().strip())+'.html'
                    #             break
                    #     except (TypeError, IndexError):
                    #         pass
                elif "alert('หัวข้อประกาศซ้ำค่ะ ไม่สามารถบันทึกได้ค่ะ');window.history.back()" in response.text:
                    detail = "Post Unsuccessful : same title post not allowed"
            else:  
                    detail = 'Unable to create post. Maybe problem with the title. Error response_code '+str(response.status_code) 
        else:
            detail = "cannot login"
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
            "websitename": self.name
        }



    def edit_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        # login

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = "Unable to update post"
        post_id = ""
        post_url = ""

        if 'web_project_name' not in postdata or postdata['web_project_name'] is None:
            if 'project_name' in postdata and postdata['project_name'] is not None:
                postdata['web_project_name'] = postdata['project_name']
            else:
                postdata['web_project_name'] = postdata['post_title_th']
        
        if success=="true":
            taddress = ""
            for add in [postdata['addr_soi'],postdata['addr_road'],postdata['addr_sub_district'],postdata['addr_district'],postdata['addr_province']]:
                if add:
                    taddress += add + " "

            addr_province = postdata['addr_province']
            addr_district = postdata['addr_district']
            province = '64'
            district = '867'
            with open('./static/baan2day_province.json') as f:
                data = json.load(f)
            
            for key in data["provinces"]:
                if (addr_province.find(str(key)) != -1) or (str(key).find(addr_province) != -1):
                    province = data["provinces"][key]
                    break
            for key in data["districts"][province]:
                if(addr_district.find(str(key)) != -1)  or (str(key).find(addr_district) != -1):
                    district = data["districts"][province][key]
                    break
            
            area = ''
            if 'floor_area' in postdata:
                area = postdata["floor_area"]
            elif 'floorarea_sqm' in postdata:
                area = postdata['floorarea_sqm']
            if postdata['property_type']=="6":
                if postdata['land_size_ngan'] is None:
                        postdata['land_size_ngan'] = 0
                if postdata['land_size_rai'] is None:
                    postdata['land_size_rai'] = 0
                if postdata['land_size_wa'] is None:
                    postdata['land_size_wa'] = 0
                try:
                    postdata['land_size_ngan'] = int(postdata['land_size_ngan'])
                except ValueError:
                    postdata['land_size_ngan'] = 0
                try:
                    postdata['land_size_rai'] = int(postdata['land_size_rai'])
                except ValueError:
                    postdata['land_size_rai'] = 0
                try:
                    postdata['land_size_wa'] = int(postdata['land_size_wa'])
                except ValueError:
                    postdata['land_size_wa'] = 0
                area = 4*(400 * postdata["land_size_rai"] + 100 * postdata["land_size_ngan"] + postdata["land_size_wa"])

            floor_total, bath_room = '0', '0'
            if 'floor_total' in postdata:
                floor_total = postdata['floor_total']
            if 'bath_room' in postdata:
                bath_room = postdata['bath_room']

            datapost= {
                "property_type": '1' if postdata['listing_type']=='ขาย' else '2',
                "property_format": property_types[str(postdata['property_type'])],
                "thomedetail_title": postdata['post_title_th'].replace("\u2013",""),
                "thomedetail_name": postdata["web_project_name"],
                "thomedetail_address": taddress,
                "tprovince": province,
                "tamphur": district,
                "thomedetail_detail": postdata["post_description_th"],
                "thomedetail_floor": floor_total,
                "thomedetail_room": "",
                "thomedetail_bathroom": bath_room,
                "thomedetail_area": area,
                "thomedetail_price": postdata['price_baht'],
                "tuser_name": postdata['name'],
                "tuser_tel": postdata['mobile'].replace('-',''),
                "tuser_email": postdata['email'],
                "latitude": postdata['geo_latitude'],
                "longitude": postdata['geo_longitude']
            }

            files = {}
            if len(postdata['post_images'])>0:
                r = httprequestObj.http_get(self.site_name+'/member_property_add.php?id='+postdata['post_id'])
                soup = BeautifulSoup(r.text, features=self.parser)
                images = soup.find(attrs={'name': 'fproperty_member'}).find_all('a')
                l = int(len(images)/2)
                for i,image in enumerate(postdata["post_images"][:10-l]):
                    files["testimage"+str(i+l+1)] = open(os.getcwd()+"/"+image, 'rb')
            
            response = httprequestObj.http_post(self.site_name+'/member_property_aed.php?typ=edit&id='+str(postdata['post_id']), data=datapost, files=files)
            success = "false"
    
            if response.status_code==200:
                if "window.location.href='member_property_list.php" in response.text:
                    success = "true"
                    detail = "Post Updated Successfully!"
                elif "alert('หัวข้อประกาศซ้ำค่ะ ไม่สามารถบันทึกได้ค่ะ');window.history.back()" in response.text:
                    detail = "Unable to update post. A Post with same title already exists"
            else:
                    detail = 'Unable to update post.  Maybe problem with the title. Error response_code '+str(response.status_code) 
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
            "log_id": postdata['log_id'],
            "account_type": "null",
            "detail": detail,
            "websitename": self.name,
            "ds_id": postdata['ds_id']
        }



    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = "Unable to delete post"

        if success=="true":
            response = httprequestObj.http_get(self.site_name+'/member_property_aed.php?typ=delete&id='+postdata['post_id'])
            success = "false"
            if response.status_code==200:
                if "alert('ลบข้อมูลเรียบร้อยแล้วค่ะ');window.location.href='member_property_list.php'" in response.text:
                    success = "true"
                    detail = "Post deleted successfully"
                elif "window.history.back()" in response.text:
                    detail = "No post found with given id"
            else:
                detail = "Unable to delete post. An Error has occurred with response_code "+str(response.status_code) 
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
            "websitename": self.name,
            "post_id": postdata['post_id'],
            "log_id": postdata['log_id'],
            "ds_id": postdata['ds_id']
        }



    def search_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        post_url = ""
        post_id = ""
        post_found = ""
        post_modify_time = ""
        post_create_time  = ""
        post_view = ""

        if success == "true":
            post_found = "false"
            detail = "No post found with given title"
            post_title = ' '.join(str(postdata['post_title_th'].replace("\u2013","")).split())

            response = httprequestObj.http_get(self.site_name+'/member_property_list.php')
            if response.status_code==200:
                soup = BeautifulSoup(response.text, features=self.parser)
                rows = soup.find('table').find('tbody').find_all('tr')
                for post in rows:
                    try:
                        td = post.find_all('td')
                        if td[1].getText()==post_title:
                            post_found = "true"
                            detail = "Post found successfully"
                            post_id = td[3].find('a').get('href').split('id=')[1]
                            post_url = self.site_name+'/homedisplay/'+post_id+'/'+postdata['post_title_th'].replace("\u2013","")+'.html'
                            post_view = td[2].getText()
                            break
                    except (TypeError, IndexError):
                        pass
            else:
                success = "false"
                detail = "Unable to search. An Error has occurred with response_code "+str(response.status_code)     
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
            "websitename": self.name,
            "account_type": None,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "post_create_time": post_create_time,
            "post_modify_time": post_modify_time,
            "post_view": post_view,
            "post_url": post_url,
            "post_found": post_found
        }

    

    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = "Unable to boost post"

        if success=="true":
            success = "false"
             
            response = httprequestObj.http_get(self.site_name+'/member_property_aed.php?typ=uptop&id='+postdata['post_id'])
            if response.status_code==200:
                if "window.location.href='member_property_list.php" in response.text:
                    success = "true"
                    detail = "Post boosted successfully!"
                elif 'window.history.back()' in response.text:
                    detail = "No post found with given id"
            else:
                detail = 'Unable to boost post. An Error has occurred with response_code '+str(response.status_code) 
        else:
            detail = "Cannot login"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "post_id": postdata['post_id'],
            "log_id": postdata['log_id'],
            "websitename": self.name,
            "ds_id": postdata['ds_id']
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
