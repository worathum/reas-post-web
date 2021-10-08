# -*- coding: utf-8 -*-

from .lib_httprequest import *
from bs4 import BeautifulSoup
from .lib_captcha import *
import os.path
import re
import json
import datetime
import sys
import requests
import random


category_types_sell = {
    '1': '5',
    '2': '1',
    '3': '1',    
    '4': '3',
    '5': '2',
    '6': '6',
    '7': '4',
    '8': '4',
    '9': '2',
    '10': '2',
    '25': '2'
}

category_types_rent = {
    '1': '5',
    '2': '8',
    '3': '8',    
    '4': '7',
    '5': '2',
    '6': '8',
    '7': '2',
    '8': '2',
    '9': '7',
    '10': '8',
    '25': '8'
}

captcha = lib_captcha()

class baansecondhand():
    name = 'baansecondhand'
    site_name = "https://www.baansecondhand.com"

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
        self.session = lib_httprequest()

    def logout_user(self):
        url = 'https://www.baansecondhand.com/logout.php'
        self.session.http_get(url)

    def register_user(self, postdata):
        self.logout_user()
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')

        time_start = datetime.datetime.utcnow()

        success = "false"
        detail = 'An Error has Occurred'
        
        datapost = {
            "ok": "1",
            "name": postdata['name_th']+' '+postdata['surname_th'],
            "password": postdata['pass'],
            "address": "-",
            "postcode": "10400",
            "country": "กรุงเทพมหานคร   ",  
            "phone": postdata['tel'],
            "email": postdata['user'],
            "bt_register": "สมัครสมาชิก",
            "img_ver": ""
        }

        r = self.session.http_get(self.site_name+'/register.php')

        captcha_img = self.session.http_get(self.site_name+'/images/cap.php', stream=True)
        if captcha_img.status_code==200:
            with open(os.getcwd() + '/imgtmp/Img_Captcha/imagecaptcha.jpg','wb') as local_file :
                for block in captcha_img.iter_content(1024):
                    if not block:
                        break
                    local_file.write(block)
            g_response = captcha.imageCaptcha(os.getcwd() + '/imgtmp/Img_Captcha/imagecaptcha.jpg')
           
            if g_response[0]==1:
                datapost['img_ver'] = g_response[1]
            
                response = self.session.http_post(self.site_name+'/register.php', data=datapost)    
                if response.status_code==200:
                    if 'window.location="https://www.baansecondhand.com/"' in response.text:
                        success = "true"
                        detail = "User registered successfully!"
                    elif 'alert("มีอีเมล์นี้  ในระบบครับ"); window.history.back()' in response.text:
                        detail = "This email is already in the system"
                    elif 'alert("Worng Verifly Image"); window.history.back()' in response.text:
                        detail = "Captcha error"
                else:
                    detail = "An error occurred with response code "+str(response.status_code)
            else:
                detail = "Image captcha error"
        else:
            detail = "An error occurred while fetching captcha, with response code "+str(captcha_img.status_code)

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

    def test_login(self, postdata):
        self.logout_user()
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')

        time_start = datetime.datetime.utcnow()
        
        success = "false"
        detail = 'An Error has Occurred'

        datapost = {
            "email": postdata['user'],
            "pass": postdata['pass'],
            "bt_login": "เข้าสู่ระบบ"
        }

        response = self.session.http_post(self.site_name+'/', data=datapost)   
         
        if response.status_code==200:
            if "history.back()" in response.text:
                detail = "Cannot Login" 
            else:
                r = self.session.http_get(self.site_name+"/mypage.php")
                if "history.back()" in r.text:
                    detail = "Cannot Login"
                else:
                    success = "true"
                    detail = "Logged in successfully!"
        else:
            detail = "An error occurred with response code "+str(response.status_code)

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
            success = "false"

            postcode = '0'
            if 'addr_postcode' in postdata:
                postcode = postdata['addr_postcode']

            addr_province = "".join(str(postdata['addr_province']).strip().split())
            addr_district = "".join(str(postdata['addr_district']).strip().split())
            addr_sub_district = "".join(str(postdata['addr_sub_district']).strip().split())
            direction = '1'
            province = '38'
            district = '568'
            subdistrict = '5119'
          
            with open('./static/baansecondhand_province.json') as f:
                province_data = json.load(f)

            for key in province_data["provinces"]:
                if (addr_province.find(str(key)) != -1) or (str(key).find(addr_province) != -1):
                    province = province_data["provinces"][key]["id"]
                    direction = province_data["provinces"][key]["direction_id"]
                    break
            for key in province_data["districts"][province]:
                if(addr_district.find(str(key)) != -1)  or (str(key).find(addr_district) != -1):
                    district = province_data["districts"][province][key]
                    break
            for key in province_data["subdistricts"][district]:
                if(addr_sub_district.find(str(key)) != -1)  or (str(key).find(addr_sub_district) != -1):
                    subdistrict = province_data["subdistricts"][district][key]
                    break

            area = str(postdata['floor_area']) if postdata['floor_area'] else '0'
            floor = str(postdata['floor_total']) if postdata['floor_total'] else '0'
            if str(postdata['property_type'])!='1':
                if 'land_size_ngan' not in postdata or postdata['land_size_ngan']==None:
                    postdata['land_size_ngan'] = 0
                if 'land_size_rai' not in postdata or postdata['land_size_rai']==None:
                    postdata['land_size_rai'] = 0
                if 'land_size_wa' not in postdata or postdata['land_size_wa']==None:
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
                area = str(400 * postdata['land_size_rai'] + 100 * postdata['land_size_ngan'] + postdata['land_size_wa'])           

            datapost = {
                "title_head": postdata['post_title_th'],
                "prize": postdata['price_baht'],
                "home_size": area,
                "home_detial": str(postdata['post_description_th']).replace('\n','<br>'),
                "geography": direction,
                "province_post": province,
                "amphur_post": district,
                "district_post": subdistrict,
                "home_address": postdata['addr_province']+', '+postdata['addr_district']+', '+postdata['addr_sub_district'],
                "home_post": postcode,
                "latbox": postdata['geo_latitude'],
                "lonbox": postdata['geo_longitude']
            }

            if postdata['listing_type']=='ขาย':
                datapost["home_type"] = category_types_sell[str(postdata['property_type'])]
                datapost["home_step"] = floor,
                datapost["home_room"] = postdata['bed_room'] if postdata['bed_room'] else "0",
                datapost["home_tolit"] = postdata['bath_room'] if postdata['bath_room'] else "0",
                datapost["post_submit"] = "บันทึกข้อมูล"
                request_url = self.site_name+'/post.php?post=home'
                rent_error = False
            else:
                datapost["room_type"] = category_types_rent[str(postdata['property_type'])]
                datapost["room_submit"] = "บันทึกข้อมูล"
                request_url = self.site_name+'/post.php?post=rent'
                rent_error = True

            if len(postdata['post_images'])==0:
                postdata['post_images'] = ['imgtmp/default/white.jpg']

            files = {"pic1": b'', "pic2": b'', "pic3": b'', "pic4": b'', "pic5": b''}
            for i, image in enumerate(postdata['post_images'][:5]):
                files["pic"+str(i+1)] = (str(random.random())[2:]+'.'+image.split('.')[-1], open(os.getcwd()+"/"+image, 'rb'), 'image/png')
            if rent_error:
                detail = "Can't post for rent at this time because of website issues."
            else:
                response = self.session.http_post(request_url, data=datapost, files=files)
                if response.status_code==200:
                    if 'https://www.baansecondhand.com/thank.php' in response.text:
                        success = "true"
                        detail = "Post created successfully"
                        post_title = str(postdata['post_title_th']).strip()
                        r = self.session.http_get('https://www.baansecondhand.com/mypage.php')
                        if r.status_code==200:
                            soup = BeautifulSoup(r.text, features=self.parser)
                            posts_element = soup.find_all(class_='board')
                            for posts in posts_element:
                                for post in posts.find_all('tr')[1:]:
                                    title = post.find_all('a')
                                    if title[0].getText().strip()==post_title:
                                        post_url = title[0].get('href')
                                        post_id = post_url.split('?home_id=')[1]
                                        break
                        else:
                            detail += 'But an error has occurred while fetching post id '+str(r.status_code)

                    elif 'window.history.back()' in response.text:
                        detail = "Following error occurred: "+response.text.split('alert(')[1].split(')')[0][1:-1]
                else:
                    detail = 'An Error has occurred with response_code '+str(response.status_code)

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
            success = "false"

            r = self.session.http_get('https://www.baansecondhand.com/mypage.php')
            if r.status_code==200:
                soup = BeautifulSoup(r.text, features=self.parser)
                posts_element = soup.find_all(class_='board')
                flag = False
                post_id = str(postdata['post_id'])

                for post in posts_element[0].find_all('tr')[1:]:
                    post_url = post.find('a').get('href')
                    if post_url.split('?home_id=')[1]==post_id:
                        flag = True

                if not flag:
                    for post in posts_element[1].find_all('tr')[1:]:
                        post_url = post.find('a').get('href')
                        if post_url.split('?home_id=')[1]==post_id:
                            flag = True

                if flag:
                    postcode = '0'
                    if 'addr_postcode' in postdata:
                        postcode = postdata['addr_postcode']

                    addr_province = "".join(str(postdata['addr_province']).strip().split())
                    addr_district = "".join(str(postdata['addr_district']).strip().split())
                    addr_sub_district = "".join(str(postdata['addr_sub_district']).strip().split())
                    direction = '1'
                    province = '38'
                    district = '568'
                    subdistrict = '5119'
                
                    with open('./static/baansecondhand_province.json') as f:
                        province_data = json.load(f)

                    for key in province_data["provinces"]:
                        if (addr_province.find(str(key)) != -1) or (str(key).find(addr_province) != -1):
                            province = province_data["provinces"][key]["id"]
                            direction = province_data["provinces"][key]["direction_id"]
                            break
                    for key in province_data["districts"][province]:
                        if(addr_district.find(str(key)) != -1)  or (str(key).find(addr_district) != -1):
                            district = province_data["districts"][province][key]
                            break
                    for key in province_data["subdistricts"][district]:
                        if(addr_sub_district.find(str(key)) != -1)  or (str(key).find(addr_sub_district) != -1):
                            subdistrict = province_data["subdistricts"][district][key]
                            break
                    if 'floor_total' not in postdata:
                        postdata['floor_total'] = '0'      
                    if 'bed_room' not in postdata:
                        postdata['bed_room'] = '0'    
                    if 'bath_room' not in postdata:
                        postdata['bath_room'] = '0' 
                    area = str(postdata['floor_area']) if postdata['floor_area'] else '0'
                    floor = str(postdata['floor_total']) if postdata['floor_total'] else '0'
                    if str(postdata['property_type'])!='1':
                        if 'land_size_ngan' not in postdata or postdata['land_size_ngan']==None:
                            postdata['land_size_ngan'] = 0
                        if 'land_size_rai' not in postdata or postdata['land_size_rai']==None:
                            postdata['land_size_rai'] = 0
                        if 'land_size_wa' not in postdata or postdata['land_size_wa']==None:
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
                        area = str(400 * postdata['land_size_rai'] + 100 * postdata['land_size_ngan'] + postdata['land_size_wa'])           

                    datapost = {
                        "home_id": post_id,
                        "title_head": postdata['post_title_th'],
                        "prize": postdata['price_baht'],
                        "home_size": area,
                        "home_detial": str(postdata['post_description_th']).replace('\n','<br>'),
                        "geography": direction,
                        "province_post": province,
                        "amphur_post": district,
                        "district_post": subdistrict,
                        "home_address": postdata['addr_province']+', '+postdata['addr_district']+', '+postdata['addr_sub_district'],
                        "home_post": postcode,
                        "latbox": postdata['geo_latitude'],
                        "lonbox": postdata['geo_longitude']
                    }

                    if postdata['listing_type']=='ขาย':
                        datapost["home_type"] = category_types_sell[str(postdata['property_type'])]
                        datapost["home_step"] = floor,
                        datapost["home_room"] = postdata['bed_room'] if postdata['bed_room'] else "0",
                        datapost["home_tolit"] = postdata['bath_room'] if postdata['bath_room'] else "0",
                        datapost["post_submit"] = "บันทึกข้อมูล"
                        request_url = self.site_name+'/edit_home.php?edit=true&home_id='+post_id
                    else:
                        datapost["home_type"] = category_types_rent[str(postdata['property_type'])]
                        datapost["post_submit"] = "บันทึกข้อมูล"
                        request_url = self.site_name+'/edit_room.php?edit=true&home_id='+post_id

                    files = {"pic1": b'', "pic2": b'', "pic3": b'', "pic4": b'', "pic5": b''}
                    if len(postdata['post_images'])==0:
                        postdata['post_images'] = ['imgtmp/default/white.jpg']
                    for i, image in enumerate(postdata['post_images'][:5]):
                        files["pic"+str(i+1)] = (str(random.random())[2:]+'.'+image.split('.')[-1], open(os.getcwd()+"/"+image, 'rb'), 'image/png')
                    
                    response = self.session.http_post(request_url, data=datapost, files=files)
                    if response.status_code==200:    
                        if "alert('บันทึกข้อมูลแล้วครับ')" in response.text:
                            success = "true"
                            detail = "Post updated successfully"
                    else:
                        detail = 'An Error has occurred with response_code '+str(response.status_code)
                else:
                    detail = "No post found with given id"
            else:
                detail = 'An Error has occurred while fetching page, with response_code '+str(r.status_code)
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



    def search_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        post_url = ""
        post_id = ""
        post_found = ""
        post_modify_time = ""
        post_create_time = ""
        post_view = ""

        if success == "true":
            post_found = "false"
            success="false"
            detail = "No post found with given title"
            post_title = str(postdata['post_title_th']).strip()
            

            response = self.session.http_get('https://www.baansecondhand.com/mypage.php')
            if response.status_code==200:
                soup = BeautifulSoup(response.text, features=self.parser)
                posts_element = soup.find_all(class_='board')
                for posts in posts_element:
                    for post in posts.find_all('tr')[1:]:
                        title = post.find_all('a')
                        ttl=title[0].getText().strip()
                        if ttl in post_title or post_title in ttl :
                            success="true"
                            post_found = "true"
                            detail = "Post found successfully!"
                            post_url = title[0].get('href')
                            post_id = post_url.split('?home_id=')[1]
                            post_modify_time = title[-1].getText()
                            break
                        else:
                            success = 'false'
                    if post_found=="true":
                        break
            else:
                success = 'false'
                post_title = ''
                detail = 'An Error has occurred with response_code '+str(response.status_code)
        else:
            success = 'false'
            post_title = ''
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
            "post_found": post_found,
            "post_title_th" : post_title
        }



    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = "Unable to delete post"

        if success=="true":
            success = "false"

            r = self.session.http_get('https://www.baansecondhand.com/mypage.php')
            if r.status_code==200:
                soup = BeautifulSoup(r.text, features=self.parser)
                posts_element = soup.find_all(class_='board')
                flag = False
                post_id = str(postdata['post_id'])
                delete = 'delete'
                for i, posts in enumerate(posts_element):
                    for post in posts.find_all('tr')[1:]:
                        post_url = post.find('a').get('href')
                        if post_url.split('?home_id=')[1]==post_id:
                            flag = True
                            if i%2:
                                delete = 'delete_room'
                            break
                
                if flag:
                    delete_url = self.site_name+'/mypage.php?'+delete+'=true&home_id='+post_id
                    response = self.session.http_get(delete_url)
                    if response.status_code==200:
                        if response.url==delete_url:
                            success = "true"
                            detail = "Post deleted successfully!"
                    else:
                        detail = 'An Error has occurred with response_code '+str(response.status_code)
                else:
                    detail = "No post found with given id"
            else:
                detail = 'An Error has occurred while fetching page, with response_code '+str(r.status_code)
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



    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        
        if success=="true":
            success = "false"
            detail = "Unable to boost post"
            
            r = self.session.http_get('https://www.baansecondhand.com/mypage.php')
            if r.status_code==200:
                soup = BeautifulSoup(r.text, features=self.parser)
                posts_element = soup.find_all(class_='board')
                flag = False
                post_id = str(postdata['post_id'])
                update = 'update'
                for i, posts in enumerate(posts_element):
                    for post in posts.find_all('tr')[1:]:
                        post_url = post.find('a').get('href')
                        if post_url.split('?home_id=')[1]==post_id:
                            flag = True
                            if i%2:
                                update = 'update_room'
                            break

                if flag:
                    update_url = self.site_name+'/mypage.php?'+update+'=true&home_id='+post_id
                    response = self.session.http_get(update_url)
                    if response.status_code==200:
                        if response.url==update_url:
                            success = "true"
                            detail = "Post boosted successfully!"
                    else:
                        detail = 'An Error has occurred with response_code '+str(response.status_code)
                else:
                    detail = "No post found with given id"
            else:
                detail = 'An Error has occurred while fetching page, with response_code '+str(r.status_code)
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
