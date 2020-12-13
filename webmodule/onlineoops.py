# -*- coding: utf-8 -*-
import random
from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
import re
import json
import datetime
import sys
import requests
import random

province_list = ['กรุงเทพมหานคร', 'สมุทรปราการ', 'นนทบุรี', 'ปทุมธานี', 'พระนครศรีอยุธยา', 'อ่างทอง', 'ลพบุรี', 'สิงห์บุรี', 'ชัยนาท', 'สระบุรี', 'ชลบุรี', 'ระยอง', 'จันทบุรี', 'ตราด', 'ฉะเชิงเทรา', 'ปราจีนบุรี', 'นครนายก', 'สระแก้ว', 'นครราชสีมา', 'บุรีรัมย์', 'สุรินทร์', 'ศรีสะเกษ', 'อุบลราชธานี', 'ยโสธร', 'ชัยภูมิ', 'อำนาจเจริญ', 'หนองบัวลำภู', 'ขอนแก่น', 'อุดรธานี', 'เลย', 'หนองคาย', 'มหาสารคาม', 'ร้อยเอ็ด', 'กาฬสินธุ์', 'สกลนคร', 'นครพนม', 'มุกดาหาร', 'เชียงใหม่', 'ลำพูน', 'ลำปาง', 'อุตรดิตถ์', 'แพร่', 'น่าน', 'พะเยา', 'เชียงราย', 'แม่ฮ่องสอน', 'นครสวรรค์', 'อุทัยธานี', 'กำแพงเพชร', 'ตาก', 'สุโขทัย', 'พิษณุโลก', 'พิจิตร', 'เพชรบูรณ์', 'ราชบุรี', 'กาญจนบุรี', 'สุพรรณบุรี', 'นครปฐม', 'สมุทรสาคร', 'สมุทรสงคราม', 'เพชรบุรี', 'ประจวบคีรีขันธ์', 'นครศรีธรรมราช', 'กระบี่', 'พังงา', 'ภูเก็ต', 'สุราษฎร์ธานี', 'ระนอง', 'ชุมพร', 'สงขลา', 'สตูล', 'ตรัง', 'พัทลุง', 'ปัตตานี', 'ยะลา', 'นราธิวาส', 'บึงกาฬ']
property_types = {
    '1': ('condominium', 'bed_room', '', '', '', '', 'floor_area','lat_long'),
    '5': ('commercial-building', 'floor_total', 'bed_room', '', 'floor_area', 'land_size', 'lat_long'),
    '4': ('townhouse', 'floor_total', 'bed_room', '', '', 'floor_area', 'land_size', 'lat_long'),
    '6': ('land', '', 'land_size', 'lat_long'),
    '2': ('home', 'floor_total', 'bed_room', '', '', '', 'floor_area', 'land_size', 'lat_long'),
    '9': ('office-space', '', 'floor_area', 'lat_long'),
    '7': ('apartment',),
    '3': ('others',),
    '8': ('others',),
    '10': ('others',),
    '25': ('others',)
}

httprequestObj = lib_httprequest()


class onlineoops():
    name = 'onlineoops'
    site_name = "https://market.onlineoops.com"
   
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

    def logout_user(self):
        url = 'https://market.onlineoops.com/user/logout'
        httprequestObj.http_get(url)

    def register_user(self, postdata):
        self.logout_user()
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        httprequestObj.http_get(self.site_name+'/user/logout')

        # start process
        success = "false"
        detail = 'An Error has Occurred'

        r = httprequestObj.http_get(self.site_name+'/user/register')
        soup = BeautifulSoup(r.content, features=self.parser)
        csrf  = soup.find(attrs={"name": "_csrf"}).get('value')
        
        datapost = {
            "_csrf": csrf,
            "Member[email]": postdata['user'],
            "Member[mobile]": postdata['tel'],
            "Member[username]": postdata['user'],
            "Member[newPassword]": postdata['pass'],
            "Member[isconfirm]": "1"
        }

        response = httprequestObj.http_post(self.site_name+'/user/register', data=datapost)
    
        if response.status_code==200:
            soup = BeautifulSoup(response.content, features=self.parser)
            confirmation_message = soup.find(class_='alert alert-success')
            error_message = soup.find(class_='help-block')
            
            if confirmation_message:
                success = "true"
                detail = "Successfully registered! Please check your email to confirm your account"
            elif error_message:
                detail = "This email is already in use"
        else:
            detail = 'An Error has occurred with response_code '+str(response.status_code) 
        # # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            'ds_id': postdata['ds_id'],
            "end_time": str(time_end),
            "detail": detail,
            "websitename": self.name,
        }


    def test_login(self, postdata):
        self.logout_user()
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        
        # start process
        success = "false"
        detail = 'An Error has Occurred'
        httprequestObj.http_get(self.site_name+'/user/logout')


        r = httprequestObj.http_get(self.site_name+'/user/login')
        soup = BeautifulSoup(r.content, features=self.parser)
        csrf  = soup.find(attrs={"name": "_csrf"}).get('value')
        
        datapost = {
            "_csrf": csrf,
            "LoginForm[username]": postdata['user'],
            "LoginForm[password]": postdata['pass'],
            "LoginForm[rememberMe]": 0
        }

        response = httprequestObj.http_post(self.site_name+'/user/login', data=datapost)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, features=self.parser)
            username = soup.find(class_='field-loginform-username')
            password = soup.find(class_='field-loginform-password')
            
            if username and 'has-error' in username.get('class'):
                detail = "An error has occurred. This user cannot be found."
            elif password and 'has-error' in password.get('class'):
                detail = "An error has occurred. Incorrect password."
            elif soup.find(class_='userImg'):
                success = "true"
                detail = "Login successful!"
        else:
            detail = 'An Error has occurred with response_code '+str(response.status_code) 

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



    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        # login

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = "An Error occurred. Unable to create post."
        post_id = ""
        post_url = ""

        if 'web_project_name' not in postdata or postdata['web_project_name'] is None:
            if 'project_name' in postdata and postdata['project_name'] is not None:
                postdata['web_project_name'] = postdata['project_name']
            else:
                postdata['web_project_name'] = postdata['post_title_th']

        if success=="true":
            r = httprequestObj.http_get(self.site_name+'/post/free')
            soup = BeautifulSoup(r.text, features=self.parser)
            csrf = soup.find(attrs={'name':'_csrf'}).get('value')
            province = province_list[0]
            for pr in province_list:
                if postdata['addr_province'] in pr:
                    province = pr
                    break

            postdata['lat_long'] = str(postdata['geo_latitude'])+','+str(postdata['geo_longitude'])
            if ('floor_total' not in postdata) or ('floor_total' in postdata and not str(postdata['floor_total']).isnumeric()):
                postdata['floor_total'] = '1'
            if ('bed_room' not in postdata) or ('bed_room' in postdata and not str(postdata['bed_room']).isnumeric()):
                postdata['bed_room'] = '1'
            
            if 'land_size_ngan' not in postdata or postdata['land_size_ngan'] == None:
                postdata['land_size_ngan'] = 0
            if 'land_size_rai' not in postdata or postdata['land_size_rai'] == None:
                postdata['land_size_rai'] = 0
            if 'land_size_wa' not in postdata or postdata['land_size_wa'] == None:
                postdata['land_size_wa'] = 0
            try:
                postdata['land_size_ngan'] = int(postdata['land_size_ngan'])
            except:
                postdata['land_size_ngan'] = 0
            try:
                postdata['land_size_rai'] = int(postdata['land_size_rai'])
            except:
                postdata['land_size_rai'] = 0
            try:
                postdata['land_size_wa'] = int(postdata['land_size_wa'])
            except:
                postdata['land_size_wa'] = 0
            postdata['land_size'] = 400*postdata['land_size_rai'] + 100*postdata['land_size_ngan'] + postdata['land_size_wa']
            if postdata['land_size']==0:
                if (postdata['floor_area']).isnumeric() and int(postdata['floor_area'])>0:
                    postdata['land_size'] = postdata['floor_area']
                else:
                    postdata['land_size'] = 1

            files = {}
            if len(postdata['post_images'])>0:
                files["PostmarketthTH[images][]"] = open(os.getcwd()+"/"+postdata['post_images'][0], 'rb')
            
            datapost= {
                "_csrf": csrf,
                "PostmarketthTH[name]": postdata['post_title_th'], 
                "PostmarketthTH[quality_type]": "second", # new or second
                "PostmarketthTH[price]": postdata['price_baht'],
                "PostCategory[cate_class]": "property",
                "PostCategory[subcate_class]": property_types[str(postdata['property_type'])][0],
                "PostmarketthTH[detail]": postdata['post_description_th'].replace('\r\n','<br>'),
                "PostContact[province]": province,
                "PostContact[district]": postdata['addr_district'],
                "PostContact[mobile]": postdata['mobile'].replace('-',''),
                "ajax": "post-form"   
            }
            
            for i, eachdata in enumerate(property_types[str(postdata['property_type'])][1:]):
                if eachdata:
                    datapost['Attr['+str(i)+'][tmpvalue]'] = postdata[eachdata]      
                else:
                    datapost['Attr['+str(i)+'][tmpvalue]'] = eachdata
            
            response = httprequestObj.http_post(self.site_name+'/post/free', data=datapost, files = files)
            
            success = "false"
            if response.status_code==200:
                soup = BeautifulSoup(response.text, features=self.parser)
                confirmation_message = soup.find(id="w0")
                if confirmation_message and 'alert-success' in confirmation_message.get('class'):
                    success = "true"
                    detail = "Post created successfully"
                    post_id = confirmation_message.find('a').get('href')[1:]
                    post_url = self.site_name + '/' + post_id
                    files = {}
                    for image in postdata['post_images'][1:6]:
                        files["PostmarketthTH[images][]"] = open(os.getcwd()+"/"+image, 'rb')
                        r = httprequestObj.http_post(self.site_name+'/post/free?id='+post_id, data=datapost, files = files)
            else:
                detail += "Error code "+ str(response.status_code)+"     detail:"+response.text
        else:
            detail = "Unable to login"
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
        detail = "An Error occurred. Unable to update post."
        post_id = ""
        post_url = ""

        if 'web_project_name' not in postdata or postdata['web_project_name'] is None:
            if 'project_name' in postdata and postdata['project_name'] is not None:
                postdata['web_project_name'] = postdata['project_name']
            else:
                postdata['web_project_name'] = postdata['post_title_th']
        
        if success=="true":
            r = httprequestObj.http_get(self.site_name+'/post/free?id='+str(postdata['post_id']))
            soup = BeautifulSoup(r.text, features=self.parser)
            site_error = soup.find(class_ = 'site-error')
            soup_ = soup

            if site_error:
                success = "false"
                detail  = "No post found with given id"
            else:
                csrf = soup.find(attrs={'name':'_csrf'}).get('value')
                header = {
                    'x-csrf-token': csrf
                }
                script = soup_.find('script', {'type': 'text/javascript'})
                script = str(script).split('var')
                data = []
                for i in script:
                    if 'fileinput_' in i:
                        data.append((i))
                data[0] = data[0].split('=')[3].split('initialPreview":[')[1].split(']')[0]
                data[0] = data[0].replace('"', '')
                data[0] = data[0].replace('\\', '')
                data[1] = data[1].split('=')[2].split('initialPreview":[')[1].split(']')[0].split(',')
                temp = []
                for i in data[1]:
                    m = i.replace('"', '')
                    m = m.replace('\\', '')
                    temp.append(m)
                data[1] = temp
                # print('\n\n\n----------->>',data)
                d_ = {
                    'key': str(data[0]) + ':' + str(postdata["post_id"])
                }
                r_ = httprequestObj.http_post('https://market.onlineoops.com/post/file-delete-thumb', data=d_, headers=header)
                # print(r_.url,d_,r_.text)

                for i in data[1]:
                    d_ = {
                        'key': str(i) + ':' + str(postdata["post_id"])
                    }
                    r_ = httprequestObj.http_post('https://market.onlineoops.com/post/file-delete', data=d_, headers=header)
                    # text is false but pic will be deleted
                    # print(r_.url, d_, r_.text)
                province = province_list[0]
                for pr in province_list:
                    if postdata['addr_province'] in pr:
                        province = pr
                        break

                postdata['lat_long'] = str(postdata['geo_latitude'])+','+str(postdata['geo_longitude'])
                if ('floor_total' not in postdata) or ('floor_total' in postdata and not str(postdata['floor_total']).isnumeric()):
                    postdata['floor_total'] = '1'
                if ('bed_room' not in postdata) or ('bed_room' in postdata and not str(postdata['bed_room']).isnumeric()):
                    postdata['bed_room'] = '1'

                if 'land_size_ngan' not in postdata or postdata['land_size_ngan'] == None:
                        postdata['land_size_ngan'] = 0
                if 'land_size_rai' not in postdata or postdata['land_size_rai'] == None:
                    postdata['land_size_rai'] = 0
                if 'land_size_wa' not in postdata or postdata['land_size_wa'] == None:
                    postdata['land_size_wa'] = 0
                try:
                    postdata['land_size_ngan'] = int(postdata['land_size_ngan'])
                except:
                    postdata['land_size_ngan'] = 0
                try:
                    postdata['land_size_rai'] = int(postdata['land_size_rai'])
                except:
                    postdata['land_size_rai'] = 0
                try:
                    postdata['land_size_wa'] = int(postdata['land_size_wa'])
                except:
                    postdata['land_size_wa'] = 0
                postdata['land_size'] = 400*postdata['land_size_rai'] + 100*postdata['land_size_ngan'] + postdata['land_size_wa']
                if (postdata['floor_area']).isnumeric() and int(postdata['floor_area'])>0:
                    postdata['land_size'] = postdata['floor_area']
                else:
                    postdata['land_size'] = 1
                    
                datapost= {
                    "_csrf": csrf,
                    "PostmarketthTH[name]": postdata['post_title_th'], 
                    "PostmarketthTH[quality_type]": "second", # new or second
                    "PostmarketthTH[price]": postdata['price_baht'],
                    "PostCategory[cate_class]": "property",
                    "PostCategory[subcate_class]": property_types[str(postdata['property_type'])][0],
                    "PostmarketthTH[detail]": postdata['post_description_th'].replace('\r\n','<br>'),
                    "PostContact[province]": province,
                    "PostContact[district]": postdata['addr_district'],
                    "PostContact[mobile]": postdata['mobile'].replace('-',''),
                    "ajax": "post-form"   
                }

                for i, eachdata in enumerate(property_types[str(postdata['property_type'])][1:]):
                    try:
                        if eachdata:
                            datapost['Attr['+str(i)+'][tmpvalue]'] = postdata[eachdata]
                        else:
                            datapost['Attr['+str(i)+'][tmpvalue]'] = eachdata
                    except:
                        datapost['Attr['+str(i)+'][tmpvalue]'] = '1'
                
                files = {}
                if len(postdata['post_images'])>0:
                    files["PostmarketthTH[image]"] = open(os.getcwd()+"/"+postdata['post_images'][0], 'rb')
                if len(postdata['post_images']) <= 1:
                    response = httprequestObj.http_post(self.site_name+'/post/free?id='+str(postdata['post_id']), data=datapost, files = files)
                        
                for image in postdata['post_images'][1:6]:
                    files["PostmarketthTH[images][]"] = open(os.getcwd()+"/"+image, 'rb')
                    response = httprequestObj.http_post(self.site_name+'/post/free?id='+str(postdata['post_id']), data=datapost, files = files)
                    files = {}
                    if response.status_code!=200:
                        success = "false"
                        detail = "Unable to upload image"
                        break
                
                success = "false"
                if response.status_code==200:
                    soup = BeautifulSoup(response.text, features=self.parser)
                    confirmation_message = soup.find(id="w0")
    
                    if confirmation_message and 'alert-success' in confirmation_message.get('class'):
                        success = "true"
                        detail = "Post updated successfully"
                        post_id = confirmation_message.find('a').get('href')[1:]
                        post_url = self.site_name + '/' + post_id
                else:
                    success = "false"
                    detail = "Unable to upload image"
        else:
            detail = "Unable to login"

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
            response = httprequestObj.http_get(self.site_name+'/post/close?id='+str(postdata['post_id']))
            if response.status_code==200:
                soup = BeautifulSoup(response.text, features=self.parser)
                confirmation_message = soup.find(id='w0')

                if confirmation_message and 'alert-error' in confirmation_message.get('class'):
                    success = "false"
                    detail = "No post found with given id"
                elif confirmation_message and 'alert-success' in confirmation_message.get('class'):
                    success = "true"
                    detail = "Post deleted successfully"
            else:
                success = "false"
                detail = "Unble to delete post. An Error has occurred with response_code "+str(response.status_code)
        else:
            detail = "Unable to login"

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
        post_create_time = ""
        post_view = ""

        if success == "true":
            post_found = "false"
            detail = "No post found with given title"

            response = httprequestObj.http_get(self.site_name+'/post/my-classified')
            if response.status_code == 200:
                class_ = 'dfghj'
                url_ =  '/post/my-classified'
                while class_ != None:
                    if post_found == "true":
                        break
                    r = httprequestObj.http_get('https://market.onlineoops.com/%s' % url_)
                    soup = BeautifulSoup(r.content, 'html.parser')
                    pages = soup.find('ul', attrs={'class': 'pagination'})
                    if pages:
                        last = pages.find_all('li')[-1]
                        try:
                            class_ = last['class'][0]
                            if class_ == 'next':
                                url_ = last.find('a')['href']
                            else:
                                class_ = None
                        except:
                            class_ = None
                    else:
                        class_ = None

                    soup = BeautifulSoup(r.text, features=self.parser)
                    res_div = soup.find(id='allAds')

                    if res_div:
                        all_posts = res_div.find_all(class_='item-list')
                        for post in all_posts:
                            try:
                                title = post.find(class_ = 'add-title').a.getText().split('#')
                                if title[1].strip()==postdata['post_title_th']:
                                    post_found = "true"
                                    post_id = title[0]
                                    post_url = self.site_name + '/' + post_id
                                    detail = "Post found successfully"
                                    break
                            except :
                                pass
        else:
            detail = "Unable to login"
            
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
        detail = "An Error occurred. Unable to boost post."
        
        if success=="true":
            r = httprequestObj.http_get(self.site_name+'/post/free?id='+str(postdata['post_id']))
            soup = BeautifulSoup(r.text, features=self.parser)
            site_error = soup.find(class_ = 'site-error')
            
            if site_error:
                success = "false"
                detail  = "No post found with given id"
            else:
                success = "false"
                detail = "Unable to boost post"
                csrf = soup.find(attrs={'name':'_csrf'}).get('value')
                datapost = {
                    "_csrf": csrf,
                    "PostmarketthTH[name]": soup.find(attrs={'name':'PostmarketthTH[name]'}).get('value'), 
                    "PostmarketthTH[quality_type]": "second", # new or second
                    "PostmarketthTH[price]": soup.find(attrs={'name':'PostmarketthTH[price]'}).get('value'),
                    "PostmarketthTH[detail]": soup.find(attrs={'name':'PostmarketthTH[detail]'}).getText().replace('\n','<br>'),
                    "PostContact[mobile]": soup.find(attrs={'name':'PostContact[mobile]'}).get('value'),
                    "ajax": "post-form"   
                }

                for i in range(7):
                    attr = soup.find(attrs={'name': 'Attr['+str(i)+'][tmpvalue]'})
                    if attr and attr.get('value'):
                        datapost['Attr['+str(i)+'][tmpvalue]'] = attr.get('value')
                    if attr and attr.get('id')=='info':
                        try:
                            scripts = soup.find(id='div_attribute').find_all('script')   
                            lat = re.split("var lat_val=",scripts[1].string)[1]
                            lng = re.split("var long_val=",scripts[1].string)[1]
                            lat_val = lat[:lat.index(';')].strip()
                            lng_val = lng[:lng.index(';')].strip()
                            datapost['Attr['+str(i)+'][tmpvalue]'] = lat_val+','+lng_val
                        except:
                            pass
                files = {}
                response = httprequestObj.http_post(self.site_name+'/post/free?id='+str(postdata['post_id']), data=datapost, files = files)
                if response.status_code==200:
                    soup = BeautifulSoup(response.text, features=self.parser)
                    confirmation_message = soup.find(id="w0")
                    if confirmation_message and 'alert-success' in confirmation_message.get('class'):
                        success = "true"
                        detail = "Post boosted successfully"
                else:
                    success = "false"
                    detail = "Unble to boost post. An Error has occurred with response_code "+str(response.status_code)
        else:
            detail = "Unable to login"

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
            "ds_id": postdata['ds_id'],
            "post_view": ""
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
