# -*- coding: utf-8 -*-
# SEND USERNAME in login, NOT email
from .lib_httprequest import *
from bs4 import BeautifulSoup
from .lib_captcha import *
import os.path
import re
import json
import datetime
import sys
import requests


property_types = {
    '1': ('155', {'building_name':'building', 'where_floor':'floor_level', 'prop_size':'floor_area', 'prop_beds':'bed_room', 'prop_baths':'bath_room'}),
    '2': ('143', {'property_area_rai':'land_size_rai', 'property_area_ngan':'land_size_ngan', 'prop_land_area':'land_size_wa', 'prop_size':'floor_area', 'amount_floor':'floor_total', 'prop_beds':'bed_room', 'prop_baths':'bath_room'}),
    '3': ('143', {'property_area_rai':'land_size_rai', 'property_area_ngan':'land_size_ngan', 'prop_land_area':'land_size_wa', 'prop_size':'floor_area', 'amount_floor':'floor_total', 'prop_beds':'bed_room', 'prop_baths':'bath_room'}),
    '4': ('151', {'property_area_rai':'land_size_rai', 'property_area_ngan':'land_size_ngan', 'prop_land_area':'land_size_wa', 'prop_size':'floor_area', 'front_width':'0', 'amount_floor':'floor_total', 'prop_beds':'bed_room', 'prop_baths':'bath_room', 'prop_garage': ''}),
    '5': ('161', {'property_area_rai':'land_size_rai', 'property_area_ngan':'land_size_ngan', 'prop_land_area':'land_size_wa', 'prop_size':'floor_area', 'front_width':'0', 'amount_floor':'floor_total', 'prop_beds':'bed_room', 'prop_baths':'bath_room', 'prop_garage': ''}),
    '6': ('176', {'property_area_rai':'land_size_rai', 'property_area_ngan':'land_size_ngan', 'prop_land_area':'land_size_wa', 'near_road':'', 'width_near_road':'', 'width_near_water':'', 'land_color_plan':''}),
    '7': ('188', {'property_area_rai':'land_size_rai', 'property_area_ngan':'land_size_ngan', 'prop_land_area':'land_size_wa', 'prop_size':'floor_area', 'amount_floor':'floor_total', 'prop_beds':'bed_room', 'prop_baths':'bath_room', 'prop_garage': ''}),
    '8': ('188', {'property_area_rai':'land_size_rai', 'property_area_ngan':'land_size_ngan', 'prop_land_area':'land_size_wa', 'prop_size':'floor_area', 'amount_floor':'floor_total', 'prop_beds':'bed_room', 'prop_baths':'bath_room', 'prop_garage': ''}),
    '9': ('2211', {'property_area_rai':'land_size_rai', 'property_area_ngan':'land_size_ngan', 'prop_land_area':'land_size_wa', 'prop_size':'floor_area', 'front_width':'0', 'amount_floor':'floor_total', 'prop_beds':'bed_room', 'prop_baths':'bath_room', 'prop_garage': ''}),
    '10': ('189', {'property_area_rai':'land_size_rai', 'property_area_ngan':'land_size_ngan', 'prop_land_area':'land_size_wa', 'prop_size':'floor_area', 'amount_floor':'floor_total', 'prop_beds':'bed_room', 'prop_baths':'bath_room'}),
    '25': ('189', {'property_area_rai':'land_size_rai', 'property_area_ngan':'land_size_ngan', 'prop_land_area':'land_size_wa', 'prop_size':'floor_area', 'amount_floor':'floor_total', 'prop_beds':'bed_room', 'prop_baths':'bath_room'})
}

captcha = lib_captcha()

class klungbaan():
    name = 'klungbaan'
    site_name = "https://www.klungbaan.com"

    def __init__(self):
        try:
            import configs
        except ImportError:
            configs = {}
        self.httprequestObj = lib_httprequest()
        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.debug = 0
        self.debugresdata = 0
        self.parser = 'html.parser'

    def logout_user(self):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        url = "https://www.klungbaan.com/wp-dashboard/?action=logout"
        res = self.httprequestObj.http_get(url)
        soup = BeautifulSoup(res.text, self.parser)
        logout = soup.find("a")["href"]
        self.httprequestObj.http_get(logout)



    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        success = False
        detail = 'An Error has Occurred'

        datapost = {
            "username": postdata['user'].replace('@','').replace('.',''),
            "first_name": str(postdata['name_th']),
            "last_name": str(postdata['surname_th']),
            "register_pass": postdata['pass'],
            "register_pass_retype": postdata['pass'],
            "userstate": "bangkok",
            "phone_number": postdata['tel'],
            "useremail": postdata['user'],
            "term_condition": "on",
            "_wp_http_referer": "/register-salesman/",
            "action": "houzez_register",
            "is_register_page": "1"
        }
        
        r = self.httprequestObj.http_get(self.site_name+'/register-salesman/')
        if r.status_code==200:
            soup = BeautifulSoup(r.text, features=self.parser)
            houzez_register_security2 = soup.find(id='houzez_register_security')
            datapost['houzez_register_security'] = houzez_register_security2.get('value') 
           
            sitekey = "6LdMoTgUAAAAAOCwIhJ8pHeXK0BAiBkge-Lat67-"
            g_response = captcha.reCaptcha(sitekey, self.site_name+"/register-salesman/")
            if g_response != 0:
                datapost["g-recaptcha-response"] = g_response
                
                response = self.httprequestObj.http_post(self.site_name+'/wp-admin/admin-ajax.php', data=datapost) 
                if response.status_code==200: 
                    response = json.loads(response.text)
                    if response["success"]:
                        success = True
                        detail = "Registration successful!"
                    else:
                        detail = str(response["msg"])
                else:
                    detail = 'An Error has occurred with response_code '+str(response.status_code)
            else:
                detail = "reCaptcha error"
        else:
            detail = 'An Error has occurred during fetching page with response_code '+str(r.status_code)

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            'ds_id': postdata['ds_id'],
            "websitename": self.name,
            "ds_id": postdata['ds_id']
        }



    def test_login(self, postdata):
        self.logout_user()
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        
        # start process
        success = False
        detail = 'An Error has Occurred'

        datapost = {
            "username": postdata['user'],
            "password": postdata['pass'],
            "_wp_http_referer": "/",
            "action": "houzez_login"
        }
        r = self.httprequestObj.http_get(self.site_name)
        if r.status_code==200:
            for round in range(5):
                soup = BeautifulSoup(r.text, features=self.parser)
                houzez_login_security = soup.find(id='houzez_login_security')
                datapost['houzez_login_security'] = houzez_login_security.get('value')

                sitekey = "6LdMoTgUAAAAAOCwIhJ8pHeXK0BAiBkge-Lat67-"
                g_response = captcha.reCaptcha(sitekey, self.site_name)
                if g_response != 0:
                    datapost["g-recaptcha-response"] = g_response
                
                    response = self.httprequestObj.http_post(self.site_name+'/wp-admin/admin-ajax.php', data=datapost)
            
                    if response.status_code==200:
                        response = json.loads(response.text)
                        if response["success"]:
                            success = True
                            detail = "Logged in successfully!"
                            break
                        else:
                            detail = str(response["msg"].replace('<strong>', '').replace('</strong>', ''))
                    else:
                        detail = 'An Error has occurred with response_code '+str(response.status_code)
                else:
                    detail = "reCaptcha error"
        else:
            detail = 'An Error has occurred during fetching page with response_code '+str(r.status_code)

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": self.name,
            "ds_id": postdata['ds_id'],
        }

    def get_province(self, postdata):
        addr_province = postdata['addr_province']
        addr_district = postdata['addr_district']
        province = 'krabi'
        district = 'khlong-thom-krabi'
        province_th = '??????????????????'
        district_th = '????????????????????????'
        with open('./static/klungbaan_province.json') as f:
            province_data = json.load(f)

        for key in province_data["provinces"]:
            if (addr_province.find(str(key)) != -1) or (str(key).find(addr_province) != -1):
                province = province_data["provinces"][key]
                province_th = str(key)
                break
        for key in province_data["districts"][province]:
            if(addr_district.find(str(key)) != -1)  or (str(key).find(addr_district) != -1):
                district = province_data["districts"][province][key]
                district_th = str(key)
                break
        return province, district, district_th, province_th
        

    def data_post_sell(self, postdata):

        province, district, district_th, province_th = self.get_province(postdata)
        datapost = {
                    "prop_title": postdata['post_title_th'],
                    "prop_title_eng": postdata['post_title_en'],
                    "prop_project_name": postdata['web_project_name'],
                    "prop_price": postdata['price_baht'],
                    "prop_type": property_types[str(postdata['property_type'])][0],
                    "want_agent": "yes",
                    "status_property": "empty",
                    "prop_des": postdata['post_description_th'],
                    "prop_status": "17",
                    "building_name": "",
                    "where_floor": "",
                    "property_area_rai": "",
                    "property_area_ngan": "",
                    "prop_land_area": "",
                    "width_near_road": "",
                    "width_near_water": "",
                    "land_color_plan": "",
                    "prop_size": "",
                    "front_width": "",
                    "amount_floor": "",
                    "prop_beds": "",
                    "prop_baths": "",
                    "prop_garage": "",
                    "property_address": province_th+" "+district_th+" ????????????????????? (?????????/????????????)", 
                    "administrative_area_level_1": province,
                    "locality": district,
                    "near_road": "concrete" if str(postdata['property_type'])=='6' else "none",
                    "neighborhood": "other",
                    "train_type": "", 
                    "train_line": "",
                    "train_station": "",
                    "property_map_address": postdata['addr_province']+' '+postdata['addr_district'],
                    "prop_google_street_view": "show",
                    "prop_video_url": "", 
                    "lat": postdata['geo_latitude'],
                    "lng": postdata['geo_longitude'],
                    "fave_agent_display_option": "author_info",
                    "prop_tel": postdata['mobile'],
                    "prop_website": "-", 
                    "prop_lineid": postdata['line'],
                    "prop_email": postdata['email'],
                    "_wp_http_referer": "/property-create/",
                    "action": "add_property",
                    "prop_featured": "0",
                    "prop_sales_self": "0",
                    "prop_payment": "not_paid"
                }
        try:
            if int(postdata['bed_room'])>5:
                postdata['bed_room'] = '????????????????????? 5'
        except (TypeError, ValueError):
            postdata['bed_room'] = '1'
        try:
            if int(postdata['bath_room'])>5:
                postdata['bath_room'] = '????????????????????? 5'
        except (TypeError, ValueError):
            postdata['bath_room'] = '1'
        
        for key, value in property_types[str(postdata['property_type'])][1].items():
            if value and value in postdata:
                datapost[key] = postdata[value]

        return datapost

    def data_post_rent(self, postdata):
        province, district, district_th, province_th = self.get_province(postdata)
        if str(postdata['property_type'])=='6':
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
            prop_size = 400 * postdata['land_size_rai'] + 100 * postdata['land_size_ngan'] + postdata['land_size_wa']
            prop_size_prefix = "??????.??????"
        else:
            prop_size = postdata['floor_area']
            prop_size_prefix = "??????.???."

        datapost = {
            "prop_title": postdata['post_title_th'],
            "prop_des": postdata['post_description_th'],
            "prop_tel": postdata['mobile'],
            "prop_website": "-", 
            "prop_lineid": postdata['line'],
            "prop_email": postdata['email'],
            "prop_status": "17",
            "prop_type": property_types[str(postdata['property_type'])][0],
            "prop_sec_price": postdata['price_baht'],
            "prop_label": "???????????????",
            "prop_size": prop_size,
            "prop_size_prefix": prop_size_prefix,
            "prop_beds": "",
            "prop_baths": "",
            "prop_garage": "",
            "train_type": "", 
            "train_line": "",
            "train_station": "",
            "property_address": province_th+" "+district_th+" ????????????????????? (?????????/????????????)",
            "administrative_area_level_1": province,
            "locality": district,
            "neighborhood": "other",
            "property_map_address": postdata['addr_province']+' '+postdata['addr_district'],
            "prop_google_street_view": "show",
            "prop_video_url": "", 
            "lat": postdata['geo_latitude'],
            "lng": postdata['geo_longitude'],
            "_wp_http_referer": "/property-create/",
            "action": "add_property",
            "prop_featured": "0",
            "prop_payment": "not_paid"   
        }
        return datapost

    def pull_imgs(self, postdata):
        # files = {}
        allimages = []

        for count in range(len(postdata["post_img_url_lists"])):
            link = postdata["post_img_url_lists"][count]
            path = os.getcwd()+"/imgtmp/"+"photo_{}.jpg".format(count+1)
            img_data = requests.get(link).content
            with open(path, 'wb') as handler:
                handler.write(img_data)
            allimages.append(path)


        # for i in range(len(allimages)):
        #     r = open(allimages[i], 'rb')
        #     name = 'property_upload_file'
        #     files[name] = ("{}".format(allimages[i]),r,"image/jpeg")
        
        return allimages


    def create_post(self, postdata):
        self.logout_user()
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        # login

        test_login = self.test_login(postdata)
        detail = "Unable to create post"
        post_id = ""
        post_url = ""
        success = False
        
        if 'web_project_name' not in postdata or postdata['web_project_name'] is None:
            if 'project_name' in postdata and postdata['project_name'] is not None:
                postdata['web_project_name'] = postdata['project_name']
            else:
                postdata['web_project_name'] = postdata['post_title_th'] 
        
        if test_login["success"] == True:
                      
            # sell
            if postdata['listing_type']=='?????????':
                website = 'https://www.klungbaan.com'
                datapost = self.data_post_sell(postdata)
                
            # rent    
            else:
                website = 'https://rent.klungbaan.com'
                datapost = self.data_post_rent(postdata)

            # replace : space and break the line
            datapost["prop_des"].replace("\r\n", "<p>&nbsp;</p>")

            exceed_post = False
            account_type = False
            head_post = ""
            matchObj = '?????????????????????????????????????????????????????????????????????????????????????????????????????????'
            matchObj1 = '?????????????????????????????????????????????????????????(PropertyDescription)'

            r = self.httprequestObj.http_get(website+'/property-create/')
            soup = BeautifulSoup(r.text, self.parser)
            for hit in soup.find_all("h2"):
                head_all = hit.text
                head_post = head_all.replace(" ", "")
                if matchObj1 == head_post:
                    account_type = True
                    break
                if matchObj == head_post:
                    exceed_post = True
                    break

            
            if r.status_code==200 and exceed_post==False and account_type==True:
                verify_nonce = ""
                soup = BeautifulSoup(r.text, features=self.parser)
                datapost['property_nonce'] = soup.find(id='property_nonce').get('value')
                scripts = soup.find_all('script', {'type': 'text/javascript', 'src': False})
                for script in scripts:
                    if 'houzezProperty' in script.string:
                        nonce_script = json.loads("{"+script.string.split("{")[1].split("}")[0]+"}")
                        verify_nonce = nonce_script["verify_nonce"]
                        break

                image_ids = []
                flag = True
                path_imgs = self.pull_imgs(postdata)
                for image in path_imgs:
                    data = {"name": image}
                    files = {"property_upload_file": open(image, 'rb')}
                    r = self.httprequestObj.http_post(website+'/wp-admin/admin-ajax.php?action=houzez_property_img_upload&verify_nonce='+verify_nonce, data=data, files=files)
                    if r.status_code==200:
                        r = json.loads(r.text)
                        if not r["success"]:
                            if "msg" in r:
                                detail = r["msg"]
                            elif "reason" in r:
                                detail = r["reason"]
                            flag = False
                            break
                        else:
                            image_ids.append(r["attachment_id"])
                    else:
                        detail = "Unable to upload images. An Error occurred with status code "+str(r.status_code)
                        flag = False
                        break
                
                if flag:
                    datapost['propperty_image_ids[]'] = image_ids
                    response = self.httprequestObj.http_post(website+'/property-create/', data=datapost)
                    try:
                        for f in path_imgs:
                            os.remove(f)
                    except:
                        pass
    
                    if response.status_code==200:
                        if "thank-you" in response.url:
                            success = True
                            detail = "Post created successfully!"
                            r = self.httprequestObj.http_get(website+'/my-properties/')
                            if r.status_code==200:
                                soup = BeautifulSoup(r.text, features=self.parser)
                                post_div = soup.find(class_='dashboard-table-properties')
                                
                                if post_div:
                                    # post_title = " ".join(str(postdata['post_title_th']).strip().split())
                                    post_title = str(postdata['post_title_th']).strip()
                                    post_body = post_div.find('tbody')
                                    for post in post_body.find_all('tr'):
                                        post_url_div = post.find(class_="property-table-address").find("a")
                                        post_url = post_url_div.get("href")
                                        post_id = post.find(class_="property-table-actions").find(class_="dropdown-item").get("href").split("=")[-1]
                                        break
                            else:
                                detail += ' But an error has occurred while fetching post_id, with response_code '+str(r.status_code) 
                    else:
                        detail = 'Unable to create post. An Error has occurred with response_code '+str(response.status_code) 
            else:
                detail = 'Unable to create post. An Error has occurred while fetching page, with response_code '+str(r.status_code)
                if exceed_post:
                    detail = 'This account cannot post more than 4 posts.'
                elif not(account_type):
                    detail = 'This account type not for post. Please register account for agent or project owner.'
        else:
            detail = "Cannot login, "+test_login["detail"]


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
        self.logout_user()
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        # login

        test_login = self.test_login(postdata)
        success = False
        detail = "Unable to update post"
        post_url = ""

        if 'web_project_name' not in postdata or postdata['web_project_name'] is None:
            if 'project_name' in postdata and postdata['project_name'] is not None:
                postdata['web_project_name'] = postdata['project_name']
            else:
                postdata['web_project_name'] = postdata['post_title_th']

        if test_login['success']==True:
            success = False

            # sell
            if postdata['listing_type']=='?????????':
                website = 'https://www.klungbaan.com'
                datapost = self.data_post_sell(postdata)
                
            # rent    
            else:
                website = 'https://rent.klungbaan.com'
                datapost = self.data_post_rent(postdata)

            # replace : space and break the line
            datapost["prop_des"].replace("\r\n", "<p>&nbsp;</p>")

            r = self.httprequestObj.http_get("https://www.klungbaan.com/property-create/?edit_property="+str(postdata['post_id']))
            #print(website+'/property-create/?edit_property='+str(postdata['post_id']))
            if r.status_code==200:
                try:
                    verify_nonce = ""
                    soup = BeautifulSoup(r.text, features=self.parser)
                    datapost['property_nonce'] = soup.find(id='property_nonce').get('value')
                    scripts = soup.find_all('script', {'type': 'text/javascript', 'src': False})
                    for script in scripts:
                        if 'houzezProperty' in script.string:
                            nonce_script = json.loads("{"+script.string.split("{")[1].split("}")[0]+"}")
                            verify_nonce = nonce_script["verify_nonce"]
                            break
                    
                    if len(postdata['post_images'])>0:
                        images = soup.find_all(attrs={'name': 'propperty_image_ids[]'})
                        for image in images:
                            data = {
                                "action": "houzez_remove_property_thumbnail",
                                "prop_id": str(postdata['post_id']),
                                "thumb_id": image.get('value'),
                                "removeNonce": verify_nonce
                            }
                            r = self.httprequestObj.http_post(website+'/wp-admin/admin-ajax.php', data=data)
                    
                    image_ids = []
                    flag = True
                    path_imgs = self.pull_imgs(postdata)
                    for image in path_imgs:
                        data = {"name": image}
                        files = {"property_upload_file": open(image, 'rb')}
                        r = self.httprequestObj.http_post(website+'/wp-admin/admin-ajax.php?action=houzez_property_img_upload&verify_nonce='+verify_nonce, data=data, files=files)
                        if r.status_code==200:
                            r = json.loads(r.text)
                            if not r["success"]:
                                detail = r["msg"]
                                flag = False
                                break
                            else:
                                image_ids.append(r["attachment_id"])
                        else:
                            detail = "Unable to upload images. An Error occurred with status code "+str(r.status_code)
                            flag = False
                            break
                    
                    if flag:
                        datapost['propperty_image_ids[]'] = image_ids
                        response = self.httprequestObj.http_post(website+'/property-create/?edit_property='+str(postdata['post_id']), data=datapost)
                        try:
                            for f in path_imgs:
                                os.remove(f)
                        except:
                            pass
 
                        if response.status_code==200:
                            soup = BeautifulSoup(response.text, features=self.parser)
                            if "thank-you" in response.url:
                                success = True
                                detail = "Post updated successfully!"
                except AttributeError:
                    detail = "No post found with given id"
            else:
                detail = 'Unable to update post. An Error has occurred while fetching page, with response_code '+str(r.status_code) 
        else:
            detail = "Cannot login, "+test_login["detail"]
        
        
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
        self.logout_user()
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = False
        post_url = ""
        post_id = ""
        post_found = ""
        post_modify_time = ""
        post_create_time = ""
        post_view = ""

        if test_login["success"] == True:
            post_found = False
            detail = "No post found with given title"
            post_title = " ".join(str(postdata['post_title_th']).strip().split()).replace("-", "").replace("???", "")
            page = 1
            flag = False

            while not flag:
                response = self.httprequestObj.http_get('https://www.klungbaan.com/my-properties/page/'+str(page))
                if response.status_code==200:
                    soup = BeautifulSoup(response.text, features=self.parser)
                    post_div = soup.find(class_='dashboard-table-properties')
                    
                    if post_div:
                        post_title = " ".join(str(postdata['post_title_th']).strip().split()).replace("-", "").replace("???", "")
                        post_body = post_div.find('tbody')
                        for post in post_body.find_all('tr'):
                            post_url_div = post.find(class_="property-table-address").find("a")
                            title = " ".join(str(post_url_div.getText()).strip().split()).replace("-", "").replace("???", "")
                            # print(post_title)
                            # print(title)
                            # print(title==post_title)
                            if title==post_title:
                                post_url = post_url_div.get("href")
                                post_id = post.find(class_="property-table-actions").find(class_="dropdown-item").get("href").split("=")[-1]
                                post_found = True
                                detail = "Post found successfully!"
                                success = True
                                flag = True
                                break
                    else:
                        flag = True
                page += 1

            
            if post_found==False:
                page = 1
                flag = False
                while not flag:
                    response = self.httprequestObj.http_get('https://rent.klungbaan.com/my-properties/page/'+str(page))
                    if response.status_code==200:
                        soup = BeautifulSoup(response.text, features=self.parser)
                        post_div = soup.find(class_='dashboard-table-properties')
                        
                        if post_div:
                            post_title = " ".join(str(postdata['post_title_th']).strip().split()).replace("-", "").replace("???", "")
                            post_body = post_div.find('tbody')
                            for post in post_body.find_all('tr'):
                                post_url_div = post.find(class_="property-table-address").find("a")
                                title = " ".join(str(post_url_div.getText()).strip().split()).replace("-", "").replace("???", "")
                                if title==post_title:
                                    post_url = post_url_div.get("href")
                                    post_id = post.find(class_="property-table-actions").find(class_="dropdown-item").get("href").split("=")[-1]
                                    post_found = True
                                    detail = "Post found successfully!"
                                    success = True
                                    flag = True
                                    break
                        else:
                            flag = True
                    page += 1
        else:
            detail = "Cannot login, "+test_login["detail"]
        
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
        self.logout_user()
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = "Unable to delete post"

        if success==True:
            success = False
            r = self.httprequestObj.http_get('https://klungbaan.com/my-properties/')
            print(r.url)
            print(r.status_code)
            if r.status_code==200:
                soup = BeautifulSoup(r.text, features=self.parser)
                security = soup.find(class_='delete-property').get('data-nonce')    
                datapost = {
                    "action": "houzez_delete_property",
                    "prop_id": postdata['post_id'],
                    "security": security
                }
    
                response = self.httprequestObj.http_post('https://klungbaan.com/wp-admin/admin-ajax.php', data=datapost)
                if response.status_code==200:
                    response = json.loads(response.text)
                    if response["success"]:
                        success = True
                        detail = "Post deleted successfully!"
                    else:
                        r = self.httprequestObj.http_get('https://rent.klungbaan.com/my-properties/')
                        if r.status_code==200:
                            soup = BeautifulSoup(r.text, features=self.parser)
                            security = soup.find(class_='delete-property').get('data-nonce')    
                            datapost = {
                                "action": "houzez_delete_property",
                                "prop_id": postdata['post_id'],
                                "security": security
                            }
                            response = self.httprequestObj.http_post('https://rent.klungbaan.com/wp-admin/admin-ajax.php', data=datapost)
                            if response.status_code==200:
                                response = json.loads(response.text)
                                if response["success"]:
                                    success = True
                                    detail = "Post deleted successfully!"
                                else:
                                    detail = response["reason"]
                else:
                    detail = 'Unable to delete post. An Error has occurred with response_code '+str(response.status_code) 
            else:
                detail = 'An Error has occurred during fetching page with response_code '+str(r.status_code)
        else:
            detail = "Cannot login, "+test_login["detail"]

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
        self.logout_user()
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        
        if success == True:
            success = False
            detail = "Unable to boost post"
            datapost = {
                "action": "houzez_property_update_modified_date",
                "propID": postdata['post_id']
            }
            
            response = self.httprequestObj.http_post('https://www.klungbaan.com/wp-admin/admin-ajax.php', data=datapost)
            if response.status_code==200:
                response = json.loads(response.text)
                if response["success"]:
                    success = True
                    detail = "Post boosted successfully!"
                else:
                    response = self.httprequestObj.http_post('https://rent.klungbaan.com/wp-admin/admin-ajax.php', data=datapost)
                    if response.status_code==200:
                        response = json.loads(response.text)
                        if response["success"]:
                            success = True
                            detail = "Post boosted successfully!"
                        else:
                            detail = response["reason"]
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
