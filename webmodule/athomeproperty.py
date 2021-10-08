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


category_types = {
    '1': '3',
    '2': '1',
    '3': '1',    
    '4': '2',
    '5': '4',
    '6': '6',
    '7': '5',
    '8': '9',
    '9': '8',
    '10': '7',
    '25': '7'
}
captcha = lib_captcha()

class athomeproperty():
    name = 'athomeproperty'
    site_name = "http://www.athomeproperty.com"

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


    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        success = "false"
        detail = 'Unable to register user'

        datapost = {
            "username": postdata['user'].replace('.','')[:15],
            "password": postdata['pass'],
            "cpassword": postdata['pass'],
            "email": postdata['user'],
            "accept": "1"
        }

        headers = {
            "Host": "www.athomeproperty.com",
            "Origin": "http://www.athomeproperty.com",
            "Referer": "http://www.athomeproperty.com/signup.php",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
        }
        
        r = self.session.http_get(self.site_name+'/signup.php', headers=headers)
        if r.status_code==200:
            soup = BeautifulSoup(r.text, features=self.parser)
            captcha_img = self.session.http_get(soup.find(id='captcha').get('src'), stream=True)
            with open(os.getcwd() + '/imgtmp/Img_Captcha/imagecaptcha.jpg','wb') as local_file :
                for block in captcha_img.iter_content(1024):
                    if not block:
                        break
                    local_file.write(block)
            
            g_response = captcha.imageCaptcha(os.getcwd() + '/imgtmp/Img_Captcha/imagecaptcha.jpg')
            if g_response[0]==1:
                datapost['captcha'] = g_response[1]

                response = self.session.http_post(self.site_name+'/signup.php', data=datapost, headers=headers)
                if response.status_code==200:
                    if "http://www.athomeproperty.com/signin.php?ac=active" in response.url:
                        success = "true"
                        detail = "User registered successfully. Please visit this link to activate your account: "+str(response.url)
                    elif "<script>alert('มีผู้ใช้งานชื่อนี้แล้ว');window.location='javascript:history.back()'</script>" in response.text:
                        detail = "This email is already in use"
                else:
                    detail = 'An Error has occurred with response_code '+str(response.status_code)
            else:
                detail = 'Image captcha error'
        else:
            detail = 'An Error has occurred while fetching page, with response_code '+str(r.status_code)

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



    def test_login(self, postdata, from_function=False):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        
        # start process
        success = "false"
        detail = 'An Error has Occurred'
        user_id = ''

        datapost = {
            "username": postdata['user'].replace('.','')[:15],
            "password": postdata['pass'],
            "sendurl": "" 
        }

        response = self.session.http_post(self.site_name+'/signin2.php', data=datapost)
        # with open("temp.html", "w") as f:
        #     f.write(response.text)
        if response.status_code==200:
            if response.url=="http://www.athomeproperty.com?ac=complete":
                success = "true"
                detail = "Logged in successfully!"
                if from_function:
                    r = self.session.http_get('http://www.athomeproperty.com?ac=complete')
                    soup = BeautifulSoup(r.text, features=self.parser)
                    user_id = soup.find(class_='blinktop').get('href').split('id=')[1].split('&')[0]
            elif response.url=="http://www.athomeproperty.com/signin.php?ac=invalid":
                detail = "Invalid username or password"
        
        else:
            detail = 'An Error has occurred with response_code '+str(response.status_code)
        
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return_data =  {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": self.name,
            "ds_id": postdata['ds_id'],
        }
        if from_function:
            return_data['user_id'] = user_id
        return return_data



    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        # login

        test_login = self.test_login(postdata, True)
        success = test_login["success"]
        detail = "Unable to create post"
        post_id = ""
        post_url = ""
        
        if 'web_project_name' not in postdata or postdata['web_project_name'] is None:
            if 'project_name' in postdata and postdata['project_name'] is not None:
                postdata['web_project_name'] = postdata['project_name']
            else:
                postdata['web_project_name'] = postdata['post_title_th']
                postdata['project_name'] = "-" 
        
        if success=="true":  
            user_id = test_login['user_id']        
            success = "false"
            
            addr_province = postdata['addr_province']
            addr_district = ''.join(postdata['addr_district'].split())
            addr_sub_district = ''.join(postdata['addr_sub_district'].split())
            province = '1'
            district = '1,50,0'
            subdistrict = ''
          
            with open('./static/athomeproperty_province.json') as f:
                province_data = json.load(f)

            for key in province_data["provinces"]:
                if (addr_province.find(str(key)) != -1) or (str(key).find(addr_province) != -1):
                    province = province_data["provinces"][key]
                    break
            for key in province_data["districts"][province]:
                if(addr_district.find(str(key)) != -1)  or (str(key).find(addr_district) != -1):
                    district = province_data["districts"][province][key]
                    break
            for key in province_data["subdistricts"][district]:
                if(addr_sub_district.find(str(key)) != -1)  or (str(key).find(addr_sub_district) != -1):
                    subdistrict = province_data["subdistricts"][district][key]
                    break
            if subdistrict=='':
                subdistrict = district
            
            if postdata["listing_type"]=="ขาย":
                ad_type = 2
            else:
                ad_type = 4

            datapost = {
                "topic": str(postdata['post_title_th']),
                "grp": category_types[str(postdata['property_type'])],
                "type_p": "1" if postdata["listing_type"]=="ขาย" else "2",
                "price": postdata['price_baht'],
                "punit": "บาท",
                "pricepl": "0",
                "punitpl": "บาทต่อปี",
                "rai": postdata['land_size_rai'],
                "ngan": postdata['land_size_ngan'], 
                "wa": postdata['land_size_wa'],
                "size": postdata['floor_area'],
                "sizeroom": "",
                "bedroom": postdata['bed_room'],
                "bathroom": postdata['bath_room'],
                "nfloor": postdata['floor_total'],
                "on_floor": postdata['floor_level'],
                "livingroom": "0",
                "parking": "0",
                "materoom": "0",
                "age": "0",
                "aircon": "0",
                "pname": postdata['web_project_name'],
                "address": postdata['addr_province']+', '+postdata['addr_district']+', '+postdata['addr_sub_district'],
                "road": postdata['addr_road'],
                "street": "",
                "place": postdata['addr_province'],
                "AP": postdata['addr_district'],
                "TB": postdata['addr_sub_district'],
                "gmap1": postdata['geo_latitude'],
                "gmap2": postdata['geo_longitude'],
                "kw": "", 
                "bts": "", 
                "mrt": "",
                "addressdetail": "",
                "detail": str(postdata['post_description_th']).replace('\n','<br>'),
                "code_edit": postdata['user'],
                "tag": "", 
                "name_user": postdata['name'],
                "tel": postdata['mobile'],
                "email": postdata['email'],
                "savedata": "ลงประกาศ"
            }
            r = self.session.http_get(self.site_name+'/addpackage.php?map='+subdistrict)
            if r.status_code==200:
                soup = BeautifulSoup(r.text, features=self.parser)
                form = soup.find(attrs={'name': 'picForm'})
                if form:
                    id_topic = ''
                    for inp in form.find_all('input', {'type': 'hidden'}):
                        datapost[inp.get('name')] = inp.get('value')
                        if inp.get('name')=='id_topic':
                            id_topic = inp.get('value')
                    for inp in form.find_all('input', {'readonly': 'readonly'}):
                        datapost[inp.get('name')] = inp.get('value')

                    flag = True
                    if len(postdata['post_images'])>0:
                        image = postdata['post_images'][0]
                        files = {'filename': open(os.getcwd()+"/"+image, 'rb')}
                        r = self.session.http_post(self.site_name+'/ajaxupload.php?relPath=25&picname=pk&sm=4&tb=tb_centershop&pkz=yes&fn=pic1&eid='+id_topic, data={'filename':'filename'}, files=files)
                        if r.status_code==200:
                            if "http://www.108home.com/img/error.gif" in r.text:
                                flag = False
                                detail = "An error occurred while uploading images"
                        else:
                            flag = False
                            detail = "An error occurred while uploading images"

                    if flag:
                        response = self.session.http_post(self.site_name+'/addpackage.php', data=datapost)
                        if response.status_code==200:
                            if "cid" in response.url:
                                success = "true"
                                detail = "Post created successfully!"
            
                                r = self.session.http_get(self.site_name+'/membertool.php?id='+user_id+'&job=product&topic=all')
                                soup = BeautifulSoup(r.text, features=self.parser)
                                form = soup.find(attrs={'name':'frmSample'})
                                if form:
                                    post_url = form.find(class_='sw600').find('a').get('href')
                                    post_id = post_url.split('www.athomeproperty.com/p-')[1].split('/')[0]
                        else:
                            detail = 'An Error has occurred with response_code '+str(response.status_code)
            else:
                detail = 'An Error has occurred while fetching page, with response_code '+str(r.status_code)
            self.logout()
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

        test_login = self.test_login(postdata, True)
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
            user_id = test_login['user_id'] 
            success = "false"
            
            addr_province = postdata['addr_province']
            addr_district = ''.join(postdata['addr_district'].split())
            addr_sub_district = ''.join(postdata['addr_sub_district'].split())
            province = '1'
            district = '1,50,0'
            subdistrict = ''
          
            with open('./static/athomeproperty_province.json') as f:
                province_data = json.load(f)

            for key in province_data["provinces"]:
                if (addr_province.find(str(key)) != -1) or (str(key).find(addr_province) != -1):
                    province = province_data["provinces"][key]
                    break
            for key in province_data["districts"][province]:
                if(addr_district.find(str(key)) != -1)  or (str(key).find(addr_district) != -1):
                    district = province_data["districts"][province][key]
                    break
            for key in province_data["subdistricts"][district]:
                if(addr_sub_district.find(str(key)) != -1)  or (str(key).find(addr_sub_district) != -1):
                    subdistrict = province_data["subdistricts"][district][key]
                    break
            if subdistrict=='':
                subdistrict = district
            
            if postdata["listing_type"]=="ขาย":
                ad_type = 2
            else:
                ad_type = 4

            if 'land_size_rai' not in postdata:
                postdata['land_size_rai'] = ''
            if 'land_size_ngan' not in postdata:
                postdata['land_size_ngan'] = ''
            if 'land_size_wa' not in postdata:
                postdata['land_size_wa'] = ''

            datapost = {
                "topic": str(postdata['post_title_th']),
                "grp": category_types[str(postdata['property_type'])],
                "type_p": "1" if postdata["listing_type"]=="ขาย" else "2",
                "price": postdata['price_baht'],
                "punit": "บาท",
                "pricepl": "0",
                "punitpl": "บาทต่อปี",
                "rai": postdata['land_size_rai'],
                "ngan": postdata['land_size_ngan'], 
                "wa": postdata['land_size_wa'],
                "size": postdata['floor_area'],
                "sizeroom": "",
                "bedroom": postdata['bed_room'],
                "bathroom": postdata['bath_room'],
                "nfloor": postdata['floor_total'],
                "on_floor": postdata['floor_level'],
                "livingroom": "0",
                "parking": "0",
                "materoom": "0",
                "age": "0",
                "aircon": "0",
                "pname": postdata['web_project_name'],
                "address": postdata['addr_province']+', '+postdata['addr_district']+', '+postdata['addr_sub_district'],
                "road": postdata['addr_road'],
                "street": "",
                "place": postdata['addr_province'],
                "AP": postdata['addr_district'],
                "TB": postdata['addr_sub_district'],
                "gmap1": postdata['geo_latitude'],
                "gmap2": postdata['geo_longitude'],
                "kw": "", 
                "bts": "", 
                "mrt": "",
                "addressdetail": "",
                "detail": str(postdata['post_description_th']).replace('\n','<br>'),
                "code_edit": postdata['user'],
                "tag": "", 
                "name_user": postdata['name'],
                "tel": postdata['mobile'],
                "email": postdata['email'],
                "savedata": "ลงประกาศ"
            }
            r = self.session.http_get(self.site_name+'/addpackage.php?eid='+postdata['post_id'])
            if r.status_code==200:
                soup = BeautifulSoup(r.text, features=self.parser)
                form = soup.find(attrs={'name': 'picForm'})
                if form:
                    for inp in form.find_all('input', {'type': 'hidden'}):
                        datapost[inp.get('name')] = inp.get('value')

                    flag = True
                    if len(postdata['post_images'])>0:
                        image = postdata['post_images'][0]
                        files = {'filename': open(os.getcwd()+"/"+image, 'rb')}
                        r = self.session.http_post(self.site_name+'/ajaxupload.php?relPath=25&picname=pk&sm=4&tb=tb_centershop&pkz=yes&fn=pic1&eid='+str(postdata['post_id']), data={'filename':'filename'}, files=files)
                        if r.status_code==200:
                            if "http://www.108home.com/img/error.gif" in r.text:
                                flag = False
                                detail = "An error occurred while uploading images"
                        else:
                            flag = False
                            detail = "An error occurred while uploading images"

                    if flag:
                        response = self.session.http_post(self.site_name+'/addpackage.php', data=datapost)
                        if response.status_code==200:
                            if "cid" in response.url:
                                success = "true"
                                detail = "Post updated successfully!"
                    else:
                        detail = 'An Error has occurred with response_code '+str(response.status_code)
            else:
                detail = 'An Error has occurred while fetching page, with response_code '+str(r.status_code)
            self.logout()
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

        test_login = self.test_login(postdata, True)
        success = test_login["success"]
        post_url = ""
        post_id = ""
        post_found = ""
        post_modify_time = ""
        post_create_time = ""
        post_view = ""

        if success == "true":
            post_found = "false"
            user_id = test_login['user_id'] 
            detail = "No post found with given title"
            post_title = " ".join(str(postdata['post_title_th']).strip().split())

            response = self.session.http_get(self.site_name+'/membertool.php?id='+user_id+'&job=product&topic=all')
            if response.status_code==200:
                soup = BeautifulSoup(response.text, features=self.parser)
                form = soup.find(attrs={'name':'frmSample'})
                if form:
                    posts = form.find_all(class_='sw400')
                    for post in posts:
                        a = post.find('a')
                        title = " ".join(a.getText().strip().split())
                        print(" ".join(a.getText().strip().split()))
                        print(post_title)
                        if post_title in title or title in post_title:
                            post_found ="true"
                            detail = "Post found successfully!" 
                            post_url = a.get('href')
                            post_id = post_url.split('www.athomeproperty.com/p-')[1].split('/')[0]
                            break  
            self.logout()
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



    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata, True)
        success = test_login["success"]
        detail = "Unable to delete post"

        if success=="true":
            response = self.session.http_get(self.site_name+'/product.php?job=del&id='+str(postdata['post_id']))
            success = "true"
            detail = "Post deleted successfully!"
            self.logout()
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
            url = self.site_name+'/product.php?id='+postdata['post_id']+'&action=update'
            response = self.session.http_get(url)
            success = "true"
            detail = "Post boosted successfully!"
            self.logout()
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
    

    def logout(self):
        response = self.session.http_get(self.site_name)
        if response.status_code==200:
            soup = BeautifulSoup(response.text, features=self.parser)
            url_div = soup.find_all(class_="blinktop")
            for url in url_div:
                if url.get("href") and "logout.php" in url.get("href"):
                    self.session.http_get(url.get("href"))


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
