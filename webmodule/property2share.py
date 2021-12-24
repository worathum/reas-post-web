# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
import os.path
import sys
from .lib_httprequest import *
import ast
import json
from datetime import  datetime
from .lib_captcha import  *
import re



class property2share():

    name = 'https://www.property2share.com/'

    def __init__(self):

        try:
            import configs
        except ImportError:
            configs = {}
        self.httprequestObj = lib_httprequest()
        self.webname = 'property2share'
        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.primarydomain = ''
        self.debug = 0
        self.debugresdata = 0
        self.register_link = 'https://www.property2share.com/%E0%B8%A5%E0%B8%87%E0%B8%97%E0%B8%B0%E0%B9%80%E0%B8%9A%E0%B8%B5%E0%B8%A2%E0%B8%99'
        self.login_link =  'https://www.property2share.com/submitLogin2.php'

    def logout_user(self):
        url = "https://www.property2share.com/pageuser/logout.php"
        self.httprequestObj.http_get(url)

    def register_user(self, userdata):
        self.logout_user()
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.now()

        email_user = userdata['user']
        email_pass = userdata['pass']
        name_th = userdata["name_th"]
        surname_th = userdata["surname_th"]
        phone_num = userdata['tel']

        response = self.httprequestObj.http_get(
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

        register_req = self.httprequestObj.http_post(self.register_link, data=reg_dat)
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
        self.logout_user()
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        st_time = datetime.utcnow()

        email_user = logindata['user']
        passwd = logindata['pass']

        inc_data = {
            'txtEmail': email_user,
            'txtPass': passwd
        }

        login_resp = self.httprequestObj.http_post(self.login_link, data = inc_data)
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

    def get_province(self, postdata):

        addr_province = postdata['addr_province']
        addr_district = postdata['addr_district']

        # MAKE GET REQUEST FOR GETTING DROPDOWN DETAILS
        request = self.httprequestObj.http_get('https://www.property2share.com/pageuser/new_publish.php')
        soup = BeautifulSoup(request.content, 'html.parser')
        #GET PROVINCES BY SCRAPING
        provinces = soup.find_all("select", {"name": "province_id"})
        each_option = provinces[0].find_all("option")
        provinces_dict = {}
        province_list = []

        for i in range(len(each_option)):
            provinces_dict[each_option[i].text[:-3]] = each_option[i].attrs['value']
            province_list.append(each_option[i].text[:-3])


        province_id = 1

        for i in range(len(province_list)):
            if(addr_province in province_list[i]):
                province_id = provinces_dict[province_list[i]]
                break

        district_list_full = []

        district_list_resp = self.httprequestObj.http_get('https://www.property2share.com/connection/amphur.php?province_id=' + province_id)
        district_list = district_list_resp.content.decode('utf-8')
        district_list = ast.literal_eval(district_list)

        amphur_id = 46
        for districts in district_list:
            district_list_full.append(districts['AMPHUR_NAME'])
            if(addr_district in districts['AMPHUR_NAME']):
                amphur_id = int(districts['AMPHUR_ID'])

        return province_id, amphur_id

    def pull_imgs(self, postdata):
        files = {}
        allimages = []
        # try:
        for count in range(len(postdata["post_img_url_lists"])):
            link = postdata["post_img_url_lists"][count]
            path = os.getcwd()+"/imgtmp/"+"photo_{}.jpg".format(count+1)
            img_data = requests.get(link).content
            with open(path, 'wb') as handler:
                handler.write(img_data)
            allimages.append(path)

        # except:
        #     allimages = os.getcwd()+postdata["post_images"]

        for i in range(len(allimages)):
            r = open(allimages[i], 'rb')
            name = 'photo{}'.format(i+1)
            files[name] = ("{}".format(allimages[i]),r,"image/jpeg")
        
        return allimages

    def datapost_detail(self, postdata):

        if postdata['listing_type'] == "เช่า":
            post_type = 22
        elif postdata['listing_type'] == "ขาย":
            post_type = 21
        
        type_mapping = {
            1 : 2, 2 : 1, 3 : 1 , 4 : 3, 5 : 7, 6 : 4, 7 : 5, 8 : 8, 9 : 9, 10 : 6, 25 : 6
        }

        province_id, amphur_id = self.get_province(postdata)


        # invalid literal for int() with base 10: ''
        postdata['land_size_rai'] = str(re.sub("[^0-9]", "", postdata['land_size_rai']))
        postdata['land_size_ngan'] = str(re.sub("[^0-9]", "", postdata['land_size_ngan']))
        postdata['land_size_wa'] = str(re.sub("[^0-9]", "", postdata['land_size_wa']))
        postdata['price_baht'] = str(re.sub("[^0-9]", "", postdata['price_baht']))

        data = {
            'find_broker':  (None, 'on'),
            'type_publish':  (None, post_type),
            'asset_type':  (None, type_mapping[int(postdata['property_type'])]),
            'location_home':  (None, 'on'),
            'publish_title':  (None, postdata['post_title_th']),
            'txtDescription':  (None, postdata['post_description_th']),
            'publish_special':  (None, postdata['prominent_point']),
            'location_detail':  (None, postdata['addr_province']),
            'province_id':  (None, province_id),
            'amphur_id':  (None, amphur_id),
            'use_map': (None, "0"),
            'latLngPublish':  (None, "({}, {})".format(str(postdata['geo_latitude']), str(postdata['geo_longitude']))), 
            'station_type':  (None, '0'),
            'station_id':  (None, '0'),
            'publish_price':  (None, postdata['price_baht']),
            'unit_price':  (None, '1'),
            'area_rai':  (None, postdata['land_size_rai']),
            'area_ngan':  (None, postdata['land_size_ngan']),
            'area_va2':  (None, postdata['land_size_wa']),
            'area_use':  (None, postdata['floorarea_sqm']),
            'contact_name':  (None, postdata['name']),
            'contact_tel': (None, postdata['mobile']),
            'contact_mobile':  (None, postdata['mobile']),
            'contact_email':  (None, postdata['email']),
            'contact_website': (None, ""),
        }

        return data


    def create_post(self, postdata):
        self.logout_user()
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.utcnow()

        if ('log_id' not in postdata or postdata['log_id'] == None or postdata['log_id'] == ""):
            log_id = ''

        else:
            log_id = int(postdata['log_id'])

        # login with user info first
        login = self.test_login(postdata)
    
        if login['success'] == False:
            return login



        url_detail = 'https://www.property2share.com/pageuser/submitNewPublish.php?type=2'
        # url_detail = 'https://www.property2share.com/pageuser/new_publish.php'
        data = self.datapost_detail(postdata)
        detail_res = self.httprequestObj.http_post(url_detail, data=data)
        print(detail_res.status_code)
        url = detail_res.url

        url_clean = url.split('?')
        post_id = str(url_clean[1][11:])
        

        url_upload_img = "https://www.property2share.com/pageuser/upload.php?type=1&publish_id={}".format(str(post_id))

        path_imgs = self.pull_imgs(postdata)
        files = {}
        for path in path_imgs:
            files["myfile[]"] = open(path, 'rb') 
            upload_img_res = self.httprequestObj.http_post(url_upload_img, data={}, files=files)
            
        for f in path_imgs:
            os.remove(f)

        url_submit = 'https://www.property2share.com/pageuser/preview_publish.php?id={}'.format(str(post_id))
        data['publish_id'] = int(post_id)
        register_res = self.httprequestObj.http_post(url_submit,data=data)
        print(register_res.status_code)

        
        posturl_submit = 'https://www.property2share.com/property-{}'.format(str(post_id))
        check_prop_res = self.httprequestObj.http_get(posturl_submit)

        success, posted = "false", "post not created"
        if check_prop_res.status_code == 200:
            success,posted = "true", "posted successfully"

        time_end = datetime.utcnow()
        return {
            "success": success,
            "time_usage": str(time_end - time_start),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": posturl_submit,
            "post_id": post_id,
            "log_id" : log_id,
            "ds_id": postdata["ds_id"],
            "detail": posted,
            "websitename": self.webname,
        }


    def check_posted(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')

        login = self.test_login(postdata)
        if(login['success'] == False):
            return login

        all_posts_response = self.httprequestObj.http_get('https://www.property2share.com/pageuser/publish_getAll2.php?type=0&flag=1&asset_type=0&page=1&limit=20000')
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
        success = login['success']
        if (login['success'] == False):
            return login

        try:
            response = self.httprequestObj.http_get('https://www.property2share.com/pageuser/set_move_up.php?id='+post_id)
            if(response.status_code == 200):
                success = True
                detail = "Post Boosted Successfully"

            else:
                success = False
                detail = "Unable to Boost the Boost"
        except:
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
            "log_id" : postdata['log_id'],
            "websitename": "property2share",
            "post_view": ""
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
        response = self.httprequestObj.http_get('https://www.property2share.com/pageuser/delete_publish.php?type=1&id='+ str(post_id) + '&flag=0')

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
        self.logout_user()
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.utcnow()

        post_id = postdata['post_id']
        posturl = ""
        posted = ""

        # login with user info first
        login = self.test_login(postdata)
        
        if login['success'] == False:
            return login

        check_posted = self.check_posted(postdata)

        if (check_posted == False):
            success = False
            detail = 'This Post is not created by user'

        
        else:
            url = 'https://www.property2share.com/pageuser/submitEdit_Publish.php?id={}&type=2'.format(str(post_id))
            data = self.datapost_detail(postdata)
            res = self.httprequestObj.http_post(url, data=data)

            r_ = self.httprequestObj.http_get('https://www.property2share.com/pageuser/addPicPublish.php?publish_id=' + str(post_id))
            soup = BeautifulSoup(r_.text, 'html.parser')
            all_img = soup.findAll('div', {'class':'divImg'})
            for del_id in all_img:
                del_id = del_id['id'].replace('divImg_','')
                u_ = 'https://www.property2share.com/pageuser/delete_pic.php'
                data_ = {
                    'id': int(del_id),
                    'type': 1
                }
                #delete all imgs
                res_ = self.httprequestObj.http_post(u_, data=data_)
     

            path_imgs = self.pull_imgs(postdata)
            url_edit_imgs = "https://www.property2share.com/pageuser/upload.php?type=1&publish_id={}".format(str(post_id))
            files = {}
            for path in path_imgs:
                files["myfile[]"] = open(path, 'rb') 
                upload_img_res = self.httprequestObj.http_post(url_edit_imgs, data={}, files=files)
                
            for f in path_imgs:
                os.remove(f)

            url_submit = 'https://www.property2share.com/pageuser/preview_publish.php?id={}'.format(str(post_id))
            data['publish_id'] = int(post_id)
            register_res = self.httprequestObj.http_post(url_submit,data=data)

            posturl = 'https://www.property2share.com/property-' + str(post_id)
            retc = self.httprequestObj.http_get(posturl)
            retc = retc.status_code
            success, posted = "false", "Unable to Edit the Post"
            if retc == 200:
                success, posted = "true", "Post Edited Successfully"

        time_end = datetime.utcnow()
        return {
            "success": success,
            "time_usage": str(time_end - time_start),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": posturl,
            "post_id": post_id,
            "detail": posted,
            'ds_id': postdata['ds_id'],
            "log_id" : postdata['log_id'],
            "websitename": self.webname
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
        all_posts_response = self.httprequestObj.http_get('https://www.property2share.com/pageuser/publish_getAll2.php?type=0&flag=1&asset_type=0&page=1&limit=20000')
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
