# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
import os.path
import sys
from .lib_httprequest import *
import ast
import codecs

#from urlparse import urlparse
import re
import json
from datetime import  datetime
from .lib_captcha import  *

httprequestObj = lib_httprequest()


class property2share():

    name = 'https://www.property2share.com/'

    def __init__(self):

        try:
            import configs
        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.primarydomain = ''
        self.debug = 0
        self.debugresdata = 0
        self.register_link = 'https://www.property2share.com/%E0%B8%A5%E0%B8%87%E0%B8%97%E0%B8%B0%E0%B9%80%E0%B8%9A%E0%B8%B5%E0%B8%A2%E0%B8%99'
        self.login_link =  'https://www.property2share.com/submitLogin2.php'

    def register_user(self, userdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.now()

        email_user = userdata['user']
        email_pass = userdata['pass']
        name_th = userdata["name_th"]
        surname_th = userdata["surname_th"]
        phone_num = userdata['tel']

        response = httprequestObj.http_get(
            'https://www.property2share.com/capcha/captcha.php?width=100&amp;height=40&amp;characters=5')
        file = open('tmp.jpeg', 'wb')
        file.write(response.content)
        file.close()

        captcha_solver = lib_captcha()

        result = captcha_solver.imageCaptcha('tmp.jpeg')

        if(result [0] == 1):
            captcha_code = result[1]

        else:
            time_end = datetime.utcnow()
            return {
                "success": "true",
                "time_usage": str(time_end - time_start),
                "start_time": str(time_start),
                'ds_id': userdata['ds_id'],
                "end_time": str(time_end),
                "detail": "Unable to solve captcha",
                "websitename" : "property2share"
            }

        reg_dat = {
            'agent': 2,
            'txtEmail': email_user,
            'txtPass': email_pass,
            'txtName': name_th,
            'lastName': surname_th,
            'secret_code': captcha_code,
            'txtTelephone': phone_num
        }

        register_req = httprequestObj.http_post(self.register_link, data=reg_dat)
        decoded_result = register_req.content.decode('utf-8')

        time_end = datetime.now()

        resp = {
            "success": True,
            "time_usage": str(time_end - time_start),
            'ds_id': userdata['ds_id'],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": "",
            "websitename" : 'property2share'
        }

        if('บันทึกข้อมูลเรียบร้อยแล้ว' in  decoded_result):
            resp['detail'] = "User Registered Successfully"


        else:
            resp['success'] = False
            if('อีเมลล์นี้มีการใช้งานแล้ว' in decoded_result):
                resp['detail'] = "Email Already in use."

            elif('กรอกรหัสผ่านอย่างน้อย 4 หลัก' in decoded_result):
                resp['detail'] = "Password required for more than 4 characters"

            elif('คุณใส่รหัสตัวอักษรไม่ถูกต้องกรุณากรอกใหม่' in decoded_result):
                resp['detail'] = 'Invalid Captcha recieved'

        return resp

    def test_login(self, logindata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        st_time = datetime.utcnow()

        email_user = logindata['user']
        passwd = logindata['pass']

        inc_data = {
            'txtEmail': email_user,
            'txtPass': passwd
        }

        login_resp = httprequestObj.http_post(self.login_link, data = inc_data)
        decoded_result = login_resp.content.decode('utf-8')
        #print(decoded_result)
        en_time = datetime.utcnow()

        resp = {
            "success": True,
            "ds_id": logindata["ds_id"],
            "time_usage": str(en_time-st_time),
            "websitename": "property2share",
            "start_time": str(st_time),
            "end_time": str(en_time),
            "detail": "Logged in successfully"
        }

        if('ชื่อหรือรหัสผ่านผิด' in decoded_result):
            resp['success'] = False
            resp['detail'] = 'Incorrect Username or Password'

        return resp

    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.utcnow()

        if ('log_id' not in postdata or postdata['log_id'] == None or postdata['log_id'] == ""):
            log_id = ''

        else:
            log_id = int(postdata['log_id'])

        # Required Data
        listing_type = postdata['listing_type']
        property_type = postdata['property_type']
        price_baht = postdata['price_baht']
        addr_province = postdata['addr_province']
        addr_district = postdata['addr_district']
        geo_latitude = postdata['geo_latitude']
        geo_longitude = postdata['geo_longitude']
        post_title_th = postdata['post_title_th']
        post_description_th = postdata['post_description_th']

        # login with user info first
        login = self.test_login(postdata)
    
        if login['success'] == False:
            return login

        # MAKE GET REQUEST FOR GETTING DROPDOWN DETAILS
        request = httprequestObj.http_get('https://www.property2share.com/pageuser/new_publish.php')
        soup = BeautifulSoup(request.content, 'html.parser')
        #GET PROVINCES BY SCRAPING
        provinces = soup.find_all("select", {"name": "province_id"})
        each_option = provinces[0].find_all("option")
        provinces_dict = {}
        province_list = []

        for i in range(len(each_option)):
            provinces_dict[each_option[i].text[:-3]] = each_option[i].attrs['value']
            province_list.append(each_option[i].text[:-3])

        #TYPE OF THE PROPERTY MAPPED
        type_mapping = {
            1 : 2, 2 : 1, 3 : 1 , 4 : 3, 5 : 7, 6 : 4, 7 : 5, 8 : 8, 9 : 9, 10 : 6, 25 : 6
        }

        #POST TYPE (RENT/ SELL)
        post_type = 21

        if(listing_type == 'เช่า'):
            post_type = 22

        province_id = 1

        for i in range(len(province_list)):
            if(addr_province in province_list[i]):
                province_id = provinces_dict[province_list[i]]
                break

        district_list_full = []

        district_list_resp = httprequestObj.http_get('https://www.property2share.com/connection/amphur.php?province_id=' + province_id)
        district_list = district_list_resp.content.decode('utf-8')
        district_list = ast.literal_eval(district_list)

        amphur_id = 46
        for districts in district_list:
            district_list_full.append(districts['AMPHUR_NAME'])
            if(addr_district in districts['AMPHUR_NAME']):
                amphur_id = int(districts['AMPHUR_ID'])

        #LAND SIZE CALCULATIONS
        rai_size = 0
        if('land_size_rai' not in postdata or postdata['land_size_rai'] == None or postdata['land_size_rai'] == ""):
            rai_size = 0
        else:
            rai_size = int(postdata['land_size_rai'])

        ngan_size = 0
        if('land_size_ngan' not in postdata or postdata['land_size_ngan'] == None or postdata['land_size_ngan'] == ""):
            ngan_size = 0

        else:
            ngan_size = int(postdata['land_size_ngan'])

        wa_size = 0

        if('land_size_wa' not in postdata or postdata['land_size_wa'] == None or postdata['land_size_wa'] == ""):
            wa_size = 0

        else:
            wa_size = int(postdata['land_size_wa'])

        #SQM SIZE
        # sqm_size = ((400 * rai_size) + (100 * ngan_size) + (wa_size))

        if('floorarea' not in postdata or postdata['floorarea'] == None):
            floorarea = 0

        else:
            floorarea = postdata['floorarea']

        # REQUEST FOR CREATE POST
        url = 'https://www.property2share.com/pageuser/submitNewPublish.php?type=2'
        data = {
            'find_broker': 'on',
            'type_publish': post_type,
            'asset_type': type_mapping[int(property_type)],
            'location_home': 'on',
            'publish_title': post_title_th,
            'txtDescription': post_description_th,
            'publish_special': '',
            'location_detail': addr_province,
            'province_id': province_id,
            'amphur_id': amphur_id,
            'latLngPublish': '(' + str(geo_latitude)+', '+str(geo_longitude)+')',
            'station_type': 0,
            'station_id': 0,
            'publish_price': price_baht,
            'unit_price': 1,
            'area_rai': rai_size,
            'area_ngan': ngan_size,
            'area_va2': wa_size,
            'area_use': floorarea,
            'contact_name': postdata['name'],
            'contact_tel': postdata['mobile'],
            'contact_mobile': postdata['mobile'],
            'contact_email': postdata['email'],
            'contact_website': ''
        }

        #POST REQUEST WITH DATA
        res = httprequestObj.http_post(url,data=data)
        url = res.url
        print(res.status_code)
        url = url.split('?')
        post_id = str(url[1][11:])
        url = 'https://www.property2share.com/pageuser/upload.php'

        allimages = postdata["post_images"][:15]
        files = {}
        for i in range(len(allimages)-1,-1,-1):

            r = open(os.getcwd() + "/" + allimages[i], 'rb')
            params = (
                ('type', '1'),
                ('publish_id', post_id),
            )
            files['myfile'] = r
            res1 = httprequestObj.http_post(url, data = None, params =params, files = files)

        url = 'https://www.property2share.com/pageuser/preview_publish.php?id='
        url += str(post_id)
        data = { 'publish_id': int(post_id) }
        register_req = httprequestObj.http_post(url,data=data)

        #CHECK IF PROP
        time_end = datetime.utcnow()
        posturl = 'https://www.property2share.com/property-' + str(post_id)
        retc = httprequestObj.http_get(posturl)
        retc = retc.status_code

        success,posted = "false", "post not created"
        if retc == 200:
            success,posted = "true", "posted successfully"
        return {
            "success": success,
            "time_usage": str(time_end - time_start),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": posturl,
            "post_id": post_id,
            "log_id" : log_id,
            "ds_id": postdata["ds_id"],
            "detail": posted,
            "websitename": "property2share"
        }


    def check_posted(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')

        login = self.test_login(postdata)
        if(login['success'] == False):
            return login

        all_posts_response = httprequestObj.http_get('https://www.property2share.com/pageuser/publish_getAll2.php?type=0&flag=1&asset_type=0&page=1&limit=20000')
        all_posts_response = all_posts_response.content.decode('utf-8')
        print(all_posts_response.find(str(postdata['post_id'])))

        post_id = postdata['post_id']
        check_string = '"publish_id":"' + str(post_id) + '"'

        if check_string in all_posts_response:
            return True
        else:
            return False

    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.utcnow()

        post_id = postdata['post_id']

        # login with user info first
        login = self.test_login(postdata)

        if (login['success'] == False):
            return login

        check_posted = self.check_posted(postdata)
        if ('log_id' not in postdata or postdata['log_id'] == None or postdata['log_id'] == ""):
            log_id = ''


        else:
            log_id = int(postdata['log_id'])

        if(check_posted == False):
            success = False
            time_end = datetime.utcnow()
            detail = 'This Post is not created by user'
            return {
                "success": success,
                "time_usage": str(time_end - time_start),
                'ds_id': postdata['ds_id'],
                'log_id': postdata['log_id'],
                "start_time": str(time_start),
                "end_time": str(time_end),
                "detail": detail,
                "websitename": "property2share"
            }

        response = httprequestObj.http_get('https://www.property2share.com/pageuser/set_move_up.php?id='+post_id)

        #GET ALL PARAMTERS PREVIOUSLY ENTERED IN THE POST
        # request = httprequestObj.http_get('https://www.property2share.com/pageuser/edit_publish.php?id='+str(post_id))
        # soup = BeautifulSoup(request.content, 'html.parser')
        # provinces = soup.find_all("select",{"name" : "province_id"})
        # province_id = int(provinces[0].find_all("option", selected = True)[0]['value'])
        #
        # amphur = soup.find_all("select", {"name" : "amphur_id"})
        # amphur_id = int(amphur[0].find_all("option", selected=True)[0]['value'])
        #
        # post_type = soup.find_all("select", {"name" : "type_publish"})
        # post_type = int(post_type[0].find_all("option", selected=True)[0]['value'])
        #
        # asset_type = soup.find_all("select", {"name" : "asset_type"})
        # asset_type = int(asset_type[0].find_all("option", selected = True)[0]['value'])
        #
        # post_title_th = soup.find_all("input", {"name" : "publish_title"})
        # post_title_th = post_title_th[0]['value']
        #
        # post_description_th = soup.find_all("textarea", {"name" : "txtDescription"})
        # post_description_th = (post_description_th[0].contents[0])
        #
        # addr_province = soup.find_all("input", {"name" : "location_detail"})
        # addr_province = (addr_province[0]['value'])
        #
        # lat_longitude = soup.find_all("input",type="hidden")
        # lat_longitude = lat_longitude[0]['value']
        #
        # price_baht = soup.find_all("input", {"name" : "publish_price"})
        # price_baht = price_baht[0]['value']
        #
        # rai_size = soup.find_all("input", {"name" : "area_rai"})
        # rai_size = rai_size[0]['value']
        #
        # ngan_size = soup.find_all("input", {"name" : "area_ngan"})
        # ngan_size = ngan_size[0]['value']
        #
        # sqm_size = soup.find_all("input" , {"name" : "area_va2"})
        # sqm_size = sqm_size[0]['value']
        #
        # floorarea_sqm = soup.find_all("input", {"name" : "area_use"})
        # floorarea_sqm = floorarea_sqm[0]['value']
        #
        #
        # contact_name = soup.find_all("input", {"name" : "contact_name"})
        # contact_name = contact_name[0]['value']
        #
        # contact_tel = soup.find_all("input" , {"name" : "contact_tel"})
        # contact_tel = contact_tel[0]['value']
        #
        # contact_mobile = soup.find_all("input", {"name" : "contact_mobile"})
        # contact_mobile = contact_mobile[0]['value']
        #
        # contact_email = soup.find_all("input", {"name" : "contact_email"})
        # contact_email = contact_email[0]['value']
        #
        # # boost post request
        # url = 'https://www.property2share.com/pageuser/submitEdit_Publish.php?id=' + str(post_id) + '&type=2'
        # data = {
        #     'find_broker': 'on',
        #     'type_publish': post_type,
        #     'asset_type': asset_type,
        #     'location_home': 'on',
        #     'publish_title': post_title_th,
        #     'txtDescription': post_description_th,
        #     'publish_special': '',
        #     'location_detail': addr_province,
        #     'province_id': province_id,
        #     'amphur_id': amphur_id,
        #     'latLngPublish': lat_longitude,
        #     'station_type': 0,
        #     'station_id': 0,
        #     'publish_price': price_baht,
        #     'unit_price': 1,
        #     'area_rai': rai_size,
        #     'area_ngan': ngan_size,
        #     'area_va2': sqm_size,
        #     'area_use': floorarea_sqm,
        #     'contact_name': contact_name,
        #     'contact_tel': contact_tel,
        #     'contact_mobile': contact_mobile,
        #     'contact_email': contact_email,
        #     'contact_website': ''
        # }
        #
        # # Make Post request to the link
        # res = httprequestObj.http_post(url, data=data)

        #Check if request is successful
        if(response.status_code == 200):
            success = True
            detail = "Post Boosted Successfully"

        else:
            success = False
            detail = "Unable to Boost the Boost"

        time_end = datetime.utcnow()
        return {
            "success": success,
            "time_usage": str(time_end - time_start),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "post_link" :'https://www.property2share.com/property-'+str(post_id),
            'ds_id': postdata['ds_id'],
            "post_id": post_id,
            "log_id" : log_id,
            "websitename": "property2share"
        }

    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.utcnow()

        log_id = ''
        if 'log_id' not in postdata or postdata['log_id'] == None or log_id == "":
            log_id = ''
        else:
            log_id = int(postdata['log_id'])

        #Login User With Data
        login = self.test_login(postdata)
        if login['success'] == False:
            return login

        check_posted = self.check_posted(postdata)

        if check_posted == False:
            success = False
            time_end = datetime.utcnow()
            detail = 'This Post is not created by user'
            return {
                "success": success,
                "time_usage": str(time_end - time_start),
                "start_time": str(time_start),
                "end_time": str(time_end),
                "detail": detail,
                'ds_id': postdata['ds_id'],
                "log_id": log_id,
                "post_id": postdata["post_id"],
                "websitename": "property2share"
            }

        post_id = postdata['post_id']
        #Get request On the Delete Link
        response = httprequestObj.http_get('https://www.property2share.com/pageuser/delete_publish.php?type=1&id='+ str(post_id) + '&flag=0')

        success = False
        # Check if Request is successful
        if(response.status_code == 200):
            detail = 'Post Deleted Successfully'
            success = True

        else:
            detail = 'Unable to Delete The Post'


        time_end = datetime.utcnow()
        return {
            "success": success,
            "time_usage": str(time_end - time_start),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            'ds_id': postdata['ds_id'],
            "log_id": log_id,
            "post_id": postdata["post_id"],
            "websitename": "property2share"
        }

    def edit_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.utcnow()

        log_id = postdata['log_id']

        post_id = postdata['post_id']
        listing_type = postdata['listing_type']
        property_type = postdata['property_type']
        post_img_url_lists = postdata['post_img_url_lists']
        price_baht = postdata['price_baht']
        addr_province = postdata['addr_province']
        addr_district = postdata['addr_district']
        geo_latitude = postdata['geo_latitude']
        geo_longitude = postdata['geo_longitude']
        post_title_th = postdata['post_title_th']
        post_description_th = postdata['post_description_th']

        # login with user info first
        login = self.test_login(postdata)
        
        if login['success'] == False:
            return login

        check_posted = self.check_posted(postdata)

        if (check_posted == False):
            success = False
            time_end = datetime.utcnow()
            detail = 'This Post is not created by user'
            return {
                "success": success,
                "time_usage": str(time_end - time_start),
                "start_time": str(time_start),
                "end_time": str(time_end),
                "detail": detail,
                'ds_id': postdata['ds_id'],
                "log_id": log_id,
                "post_id": postdata["post_id"],
                "websitename": "property2share"
            }

        request = httprequestObj.http_get('https://www.property2share.com/pageuser/new_publish.php')
        soup = BeautifulSoup(request.content, 'html.parser')
        provinces = soup.find_all("select", {"name": "province_id"})
        each_option = provinces[0].find_all("option")
        provinces_dict = {}
        province_list = []

        for i in range(len(each_option)):
            provinces_dict[each_option[i].text[:-3]] = each_option[i].attrs['value']
            province_list.append(each_option[i].text[:-3])

        type_mapping = {
            1: 2, 2: 1, 3: 1, 4: 3, 5: 7, 6: 4, 7: 5, 8: 8, 9: 9, 10: 6, 25: 6
        }

        post_type = 21

        if (listing_type == 'เช่า'):
            post_type = 22

        province_id = 1

        for i in range(len(province_list)):
            if (addr_province in province_list[i]):
                province_id = provinces_dict[province_list[i]]
                break

        district_list_full = []

        district_list_resp = httprequestObj.http_get(
            'https://www.property2share.com/connection/amphur.php?province_id=' + province_id)
        district_list = district_list_resp.content.decode('utf-8')
        district_list = ast.literal_eval(district_list)

        amphur_id = 46
        for districts in district_list:
            district_list_full.append(districts['AMPHUR_NAME'])
            if (addr_district in districts['AMPHUR_NAME']):
                amphur_id = int(districts['AMPHUR_ID'])

        rai_size = 0
        if ('land_size_rai' not in postdata or postdata['land_size_rai'] == None or postdata['land_size_rai'] == ""):
            rai_size = 0
        else:
            rai_size = int(postdata['land_size_rai'])

        ngan_size = 0
        if ('land_size_ngan' not in postdata or postdata['land_size_ngan'] == None or postdata['land_size_ngan'] == ""):
            ngan_size = 0

        else:
            ngan_size = int(postdata['land_size_ngan'])

        wa_size = 0

        if ('land_size_wa' not in postdata or postdata['land_size_wa'] == None or postdata['land_size_wa'] == ""):
            wa_size = 0

        else:
            wa_size = int(postdata['land_size_wa'])

        # sqm_size = (400 * rai_size) + (100 * ngan_size) + (wa_size)

        floorarea_sqm = 0
        if (floorarea_sqm not in postdata or postdata['floor_area'] == None or postdata['floor_area'] == ""):
            floorarea_sqm = 0

        else:
            floorarea_sqm = postdata['floor_area']

        # create post request to add post
        url = 'https://www.property2share.com/pageuser/submitEdit_Publish.php?id='+str(post_id) + '&type=2'
        data = {
            'find_broker': 'on',
            'type_publish': post_type,
            'asset_type': type_mapping[int(property_type)],
            'location_home': 'on',
            'publish_title': post_title_th,
            'txtDescription': post_description_th,
            'publish_special': '',
            'location_detail': addr_province,
            'province_id': province_id,
            'amphur_id': amphur_id,
            'latLngPublish': '(' + str(geo_latitude) + ', ' + str(geo_longitude) + ')',
            'station_type': 0,
            'station_id': 0,
            'publish_price': price_baht,
            'unit_price': 1,
            'area_rai': rai_size,
            'area_ngan': ngan_size,
            'area_va2': wa_size,
            'area_use': floorarea_sqm,
            'contact_name': postdata['name'],
            'contact_tel': postdata['mobile'],
            'contact_mobile': postdata['mobile'],
            'contact_email': postdata['email'],
            'contact_website': ''
        }

        res = httprequestObj.http_post(url, data=data)
        url = res.url

        allimages = postdata["post_images"][:15]
        files = {}
        for i in range(len(allimages)):
            r = open(os.getcwd() + "/" + allimages[i], 'rb')
            params = (
                ('type', '1'),
                ('publish_id', post_id),
            )
            files['myfile'] = r
            res1 = httprequestObj.http_post(url, data=None, params=params, files=files)


        time_end = datetime.utcnow()
        posturl = 'https://www.property2share.com/property-' + str(post_id)
        retc = httprequestObj.http_get(posturl)
        retc = retc.status_code
        success, posted = "false", "Unable to Edit the Post"
        if retc == 200:
            success, posted = "true", "Post Edited Successfully"

        return {
            "success": success,
            "time_usage": str(time_end - time_start),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": posturl,
            "post_id": post_id,
            "detail": posted,
            'ds_id': postdata['ds_id'],
            "log_id" : log_id,
            "websitename": "property2share"
        }

    def search_post(self, postdata):

        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.utcnow()

        login = self.test_login(postdata)
        log_id = ''
        if ('log_id' not in postdata or postdata['log_id'] == None):
            log_id = ''


        else:
            log_id = postdata['log_id']

        if(login['success'] == False):
            return login

        post_title = postdata['post_title_th']
        all_posts_response = httprequestObj.http_get('https://www.property2share.com/pageuser/publish_getAll2.php?type=0&flag=1&asset_type=0&page=1&limit=20000')
        all_posts_response = json.loads(all_posts_response.content.decode('utf-8')[2:])

        if 'data' in all_posts_response:
            all_posts = all_posts_response['data']
        else:
            all_posts = []
        detail = 'Unable To Find the Post'
        success = True
        post_found = False
        post_url = ''
        post_id = ''
        post_create_time = ''
        post_view = ''

        post_title = post_title.split()

        for post in all_posts:

            actual_title = post['title'].split()
            if(post_title == actual_title):
                detail = 'Successfully Found the Post'
                post_found = True
                post_url = 'https://www.property2share.com/property-'+str(post['publish_id'])
                post_id = (post['publish_id'])
                post_create_time = post['create_date']
                post_view = post['view']
                break


        time_end = datetime.utcnow()

        return {
            "success": success,
            'ds_id': postdata['ds_id'],
            "log_id" : log_id,
            "usage_time": str(time_end - time_start),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": "property2share",
            "post_found": post_found,
            "post_url": post_url,
            "post_id": post_id,
            "account_type": None,
            "post_create_time": post_create_time,
            "post_view": post_view
        }

    def print_debug(self, msg):
        if(self.debug == 1):
            print(msg)
        return True

    def print_debug_data(self, data):
        if(self.debugdata == 1):
            print(data)
        return True
