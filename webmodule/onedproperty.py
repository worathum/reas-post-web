from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
import re
import json
import datetime
import sys
import requests
import random

httprequestObj = lib_httprequest()

class onedproperty():
   
    name = 'onedproperty'

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
        self.baseurl = 'https://www.onedproperty.com'
        self.parser = 'html.parser'
   
    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        
        start_time = datetime.datetime.utcnow()

        data = {
            'email': postdata['user'],
            'password': postdata['pass'],
            'confirm_password': postdata['pass'],
            'name' : postdata['name_title'] + '. ' + postdata['name_th'] + ' ' + postdata['surname_th'],
            'tel' : postdata['tel'],
            'company_name' : postdata['company_name'],
            'address' : '',
            'line_id' : postdata['line'],
            'facebook' : '',
            'website' : '',
            'introduce' : '',
            'btn_submit': '1'
        }
        
        success = "false"
        detail = ""
        
        headers = {
            'user_agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36'
        }
        
        if data['email'] == "":
            detail = "Invalid email"
        elif data['password'] == "":
            detail = "Invalid Password"
        elif data['password'] != data['confirm_password']:
            detail = "Invalid Password Confirmation"
        elif data['name'] == "":
            detail = "Please enter your name"
        elif data['tel'] == "":
            detail = "Please enter your phone number"
        elif len(str(data['password'])) < 6 :
            detail = "Password must be atleast 6 characters long"
        else:
            try:
                response = httprequestObj.http_post('http://www.onedproperty.com/register', data = data,headers = headers)
                if response.text.find("มีอยู่ในระบบแล้ว") != -1:
                #if response.url == 'http://www.onedproperty.com/register' :
                    success = "false"
                    detail = "Email Already registered"
                else :
                    success = "true"
                    detail = "Registered Successfully"
                    
            except requests.exceptions.RequestException:
                detail = "Network Problem occured"
            
        end_time = datetime.datetime.utcnow()    
          

        return {
            "websitename": "onedproperty",
            "success": success,
            'ds_id': postdata['ds_id'],
            "start_time": str(start_time),
            "end_time": str(end_time),
            "ds_id": str(postdata['ds_id']),
            "usage_time": str(end_time - start_time),
            "detail": detail
        }
        
        
        
        
        

    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        
        start_time = datetime.datetime.utcnow()

        data = {
            'email': postdata['user'],
            'password': postdata['pass'],
            'btn_login': '1'
        }
        
        success = "false"
        detail = ""
        
        headers = {
            'user_agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36'
        }
        
        if data['email'] == "":
            detail = "Invalid username"
        elif data['password'] == "":
            detail = "Invalid Password"
        else:
            try:
                response = httprequestObj.http_post('http://www.onedproperty.com/login', data = data, headers = headers)
                if response.text.find("Email หรือ Password ไม่ถูกต้อง") !=-1:
                    success = "false"
                    detail = 'Incorrect Username or Password !!'
                else:
                    success = "true"
                    detail = 'Logged in successfully'
            
            except requests.exceptions.RequestException:
                detail = "Network Problem occured"

        end_time = datetime.datetime.utcnow()

        return {
            "websitename": 'onedproperty',
            "success": success,
            "ds_id" : str(postdata['ds_id']),
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(end_time - start_time),
            "detail": detail
        }
        
        
        
        
        
        
    def create_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()

        login = self.test_login(postdata)
        
        headers = {
            'user_agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36'
        }
        post_url = ""
        post_id = ""

        if (login["success"] == "true"):
            post_page = httprequestObj.http_get("http://www.onedproperty.com/property/add",headers = headers)
        
            if 'web_project_name' not in postdata or postdata['web_project_name'] =="":
                if 'project_name' in postdata and postdata['project_name'] != "":
                    postdata['web_project_name'] = postdata['project_name']
                else:
                    postdata['web_project_name'] = postdata['post_title_th']
                    
            prod_address = ""
            for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
                if add is not None:
                    prod_address += add + " "
            prod_address = prod_address[:-1]

            
            data = {
                'category_id' : '',
                'type_id' : '',
                'province_id' : '64',
                'amphoe_id' : '867',
                'property_name' : str(postdata['post_title_th'].replace("\r\n","<br>")),
                'detail' : str(postdata['post_description_th'].replace("\r\n","<br>")),
                'address' : str(postdata['web_project_name']),
                'price' : str(postdata['price_baht']),
                'email' : str(postdata['email']),
                'tel' : str(postdata['mobile']),
                'facebook' : '-',
                'line_id' : str(postdata['line']),
                'bts_id' : '',
                'mrt_id' : '',
                'brt_id' : '',
                'airport_id' : '',
                'btn_submit' : '1'
            }
            
            if postdata['listing_type'] == 'เช่า':
                data['type_id'] = '2'
            else:
                data['type_id'] = '1'
                
            pd_properties = {
                '1': '1',
                '2': '2',
                '3': '2',
                '4': '3',
                '5': '7',
                '6': '5',
                '7': '4',
                '8': '4',
                '9': '6',
                '10': '8',
                '25': '8' 
            }
            
            data['category_id'] = pd_properties[str(postdata['property_type'])]
            
            #post_id = httprequestObj.http_post("http://www.onedproperty.com/property/add", data = data, headers = headers)
            #success = "re"
            
            fp = open('./static/onedproperty_province.json')
            provinces = json.load(fp)
            
            try:
                province = ''.join(map(str,str(postdata['addr_province']).split(' ')))
                data['province_id'] = provinces[province]                
            except:
                pass
                
            params = (
                ('province_id',data['province_id'])
            )
            
            url_pro = str('http://www.onedproperty.com/getAmphoe/'+data['province_id']+'/0?province_id='+data['province_id'])
            
            all_amphoe = httprequestObj.http_get(url_pro, headers = headers).text
            
            soup = BeautifulSoup(all_amphoe,features = self.parser)
            
            district = ''.join(map(str,str(postdata['addr_district']).split(' ')))
            #print(district)
            try:
                for abc in soup.find_all('option'):
                    #print(abc.text)
                    if (str(abc.text) in str(district) or str(district) in str(abc.text)):
                        data['amphoe_id'] = str(abc['value'])
                        break
            except:
                data['amphoe_id'] = str(soup.find('option')['value'])
                
                
            if 'post_images' in postdata and len(postdata['post_images']) > 0:
                pass
            else:
                postdata['post_images'] = ['./imgtmp/default/white.jpg']

            first_image = postdata["post_images"][0]
            
            file = []
            y=str(random.randint(0,100000000000000000))+".jpg"
            file.append(('image', (y, open(first_image, "rb"), "image/jpg")))
            
            filename = "image_gallery[]"
            
            for i in postdata['post_images'][1:]:
                y=str(random.randint(0,100000000000000000))+".jpg"
                #print(y)
                file.append(('image_gallery[]', (y, open(i, "rb"), "image/jpg")))

                
            post_create = httprequestObj.http_post("http://www.onedproperty.com/property/add", data = data, files = file, headers = headers)
            success = "true"
            detail = "Post created successfully"
            
            post_info = httprequestObj.http_get('http://www.onedproperty.com/member/property', headers = headers).text
            
            soup = BeautifulSoup(post_info,features = self.parser)
            
            post_in = soup.find('div',attrs={'class':"btn-line"}).a
            
            post_id = str(((post_in['href']).split('/'))[5])
            
            post_url = str('http://www.onedproperty.com/property/'+post_id)

            
        else:
            success = "false"
            detail = "Can not log in"
            
        end_time = datetime.datetime.utcnow()
        
        return {
            "websitename": "onedproperty",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(end_time - start_time),
            "post_url": post_url,
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
            "detail": detail,
            "account_type": "null"
        }
        
        
        
        
        
    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        
        start_time = datetime.datetime.utcnow()
        
        headers = {
            'user_agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36'
        }

        login = self.test_login(postdata)
        
        if login['success'] == 'true':
            all_posts = httprequestObj.http_get('http://www.onedproperty.com/member/property', headers = headers).text
            
            soup = BeautifulSoup(all_posts,features = self.parser)
            
            all_post_id = []
            
            success = 'true'
            
            for post_in in soup.find_all('div',attrs={'class':"btn-line"}):
                post_in_a = (post_in.a)['href']
                post_id = str((post_in_a.split('/'))[5])
                all_post_id.append(post_id)

            print(all_post_id)
                
            req_post_id = str(postdata['post_id'])
            if req_post_id in all_post_id:
                post_url = str('http://www.onedproperty.com/property/update/'+str(req_post_id))
                
                pqr = httprequestObj.http_get(post_url, headers = headers).text
                
                soup = BeautifulSoup(pqr,features = "html")
                
                for ab in soup.find_all('button',attrs={'class':'btn btn-red btn-sm deleteImage'}):
                    image_id = ab['data-image-id']
                    #print(image_id)
                    image_delete_url = str('http://www.onedproperty.com/property/deleteImage/'+str(image_id))
                    pqr1 = httprequestObj.http_get(image_delete_url, headers = headers)

                data = {
                'category_id' : '1',
                'type_id' : '1',
                'province_id' : '64',
                'amphoe_id' : '867',
                'property_name' : '-',
                'detail' : '',
                'address' : '',
                'price' : '',
                'email' : '',
                'tel' : '',
                'facebook' : '',
                'line_id' : '',
                'bts_id' : '',
                'mrt_id' : '',
                'brt_id' : '',
                'airport_id' : '',
                'btn_submit' : '1'
                }

                edit_url = str('http://www.onedproperty.com/property/update/'+req_post_id)

                edit_save = httprequestObj.http_post(edit_url, data = data, headers = headers)

                #print(edit_save.url)
                
                success = "true"
                detail = "Post details deleted successfully"

            else:
                success = "false"
                detail = "post_id is incorrect"  
        else :
            success = "false"
            detail = "Login failed"

        end_time = datetime.datetime.utcnow()

        
        return {
            "websitename": "onedproperty",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(end_time - start_time),
            "detail": detail,
            "post_id": str(postdata['post_id']),
            "ds_id": str(postdata['ds_id']),
            "log_id": postdata['log_id']
        }
        
        
        
        
    def boost_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()
        
        headers = {
            'user_agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36'
        }

        login = self.test_login(postdata)
        
        if(login['success'] == "true"):
            all_posts = httprequestObj.http_get('http://www.onedproperty.com/member/property', headers = headers).text
            
            soup = BeautifulSoup(all_posts,features = self.parser)
            
            all_post_id = []
            
            success = 'true'
            
            for post_in in soup.find_all('div',attrs={'class':"btn-line"}):
                post_in = (post_in.a)['href']
                post_id = str((post_in.split('/'))[5])
                all_post_id.append(post_id)
                
            req_post_id = str(postdata['post_id'])
            if req_post_id in all_post_id:
                edit_url = str('http://www.onedproperty.com/property/update/'+req_post_id)
                
                data = {
                    'btn-submit' : '1'
                }
                
                edit_save = httprequestObj.http_post(edit_url, data = data, headers = headers)
                
                success = "true"
                detail = "Post boosted successfully"
                
                
            else:
                success = "false"
                detail = "post_id is incorrect"
            
            
            
        else :
            success = "false"
            detail = "Login failed"

        end_time = datetime.datetime.utcnow()
        
        return {
            "websitename": "onedproperty",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(end_time - start_time),
            "detail": detail,
            "post_id": str(postdata['post_id']),
            "ds_id": str(postdata['ds_id']),
            "log_id": postdata['log_id']
        }




        
    def edit_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        
        start_time = datetime.datetime.utcnow()
        
        headers = {
            'user_agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36'
        }

        login = self.test_login(postdata)
        
        if login['success'] == 'true':
            all_posts = httprequestObj.http_get('http://www.onedproperty.com/member/property', headers = headers).text
            soup = BeautifulSoup(all_posts,features = self.parser).find(class_='property-list')
            all_post_id = []
            
            for post_in in soup.find_all('div', attrs={'class':"btn-line"}):
                post_id = str((post_in.a)['href']).split('/')[-1]
                if post_id.isdigit():
                    all_post_id.append(post_id)
                
            req_post_id = str(postdata['post_id'])
            if req_post_id in all_post_id:
                #success = 'true'
                #detail = 'post found'
                
                post_url = str('http://www.onedproperty.com/property/update/'+str(req_post_id))
                
                pqr = httprequestObj.http_get(post_url, headers = headers).text
                
                soup = BeautifulSoup(pqr,features = "html")
                
                for ab in soup.find_all('button',attrs={'class':'btn btn-red btn-sm deleteImage'}):
                    image_id = ab['data-image-id']
                    #print(image_id)
                    image_delete_url = str('http://www.onedproperty.com/property/deleteImage/'+str(image_id))
                    pqr1 = httprequestObj.http_get(image_delete_url, headers = headers)
                
                if 'web_project_name' not in postdata or postdata['web_project_name'] == "":
                    if 'project_name' in postdata and postdata['project_name'] != "":
                        postdata['web_project_name'] = postdata['project_name']
                    else:
                        postdata['web_project_name'] = postdata['post_title_th']
                        
                prod_address = ""
                for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
                    if add is not None:
                        prod_address += add + " "
                prod_address = prod_address[:-1]
                
                data = {
                    'category_id' : '',
                    'type_id' : '',
                    'province_id' : '64',
                    'amphoe_id' : '867',
                    'property_name' : str(postdata['post_title_th'].replace("\r\n","<br>")),
                    'detail' : str(postdata['post_description_th'].replace("\r\n","<br>")),
                    'address' : str(postdata['web_project_name']),
                    'price' : str(postdata['price_baht']),
                    'email' : str(postdata['email']),
                    'tel' : str(postdata['mobile']),
                    'facebook' : '-',
                    'line_id' : str(postdata['line']),
                    'bts_id' : '',
                    'mrt_id' : '',
                    'brt_id' : '',
                    'airport_id' : '',
                    'btn_submit' : '1'
                }
                
                if postdata['listing_type'] == 'เช่า':
                    data['type_id'] = '2'
                else:
                    data['type_id'] = '1'
                
                pd_properties = {
                    '1': '1',
                    '2': '2',
                    '3': '2',
                    '4': '3',
                    '5': '7',
                    '6': '5',
                    '7': '4',
                    '8': '4',
                    '9': '6',
                    '10': '8',
                    '25': '8' 
                }
            
                data['category_id'] = pd_properties[str(postdata['property_type'])]
                
                fp = open('./static/onedproperty_province.json')
                provinces = json.load(fp)
            
                try:
                    province = ''.join(map(str,str(postdata['addr_province']).split(' ')))
                    data['province_id'] = provinces[province]                
                except:
                    pass
                
                params = (
                    ('province_id',data['province_id'])
                )
            
                url_pro = str('http://www.onedproperty.com/getAmphoe/'+data['province_id']+'/0?province_id='+data['province_id'])
            
                all_amphoe = httprequestObj.http_get(url_pro, headers = headers).text
            
                soup = BeautifulSoup(all_amphoe,features = self.parser)
            
                district = ''.join(map(str,str(postdata['addr_district']).split(' ')))
            
                try:
                    for abc in soup.find_all('option'):
                        if (str(abc.text) in str(district) or str(district) in str(abc.text)):
                            data['amphoe_id'] = str(abc['value'])
                            break
                except:
                    data['amphoe_id'] = str(soup.find('option')['value'])
                    
                if 'post_images' in postdata and len(postdata['post_images']) > 0:
                    pass
                else:
                    postdata['post_images'] = ['./imgtmp/default/white.jpg']

                first_image = postdata["post_images"][0]
            
                file = []
                y=str(random.randint(0,100000000000000000))+".jpg"
                file.append(('image', (y, open(first_image, "rb"), "image/jpg")))
            
                filename = "image_gallery[]"
            
                for i in postdata['post_images'][1:]:
                    y=str(random.randint(0,100000000000000000))+".jpg"
                    #print(y)
                    file.append(('image_gallery[]', (y, open(i, "rb"), "image/jpg")))
                    
                edit_url = str('http://www.onedproperty.com/property/update/'+str(postdata['post_id']))
                    
                post_create = httprequestObj.http_post(edit_url, data = data, files = file, headers = headers)
                success = "true"
                detail = "Post edited successfully"
    
            else:
                success = 'false'
                detail = 'No such post_id exist for this user'
        
        else :
            success = 'false'
            detail = 'Can not log in'
            
        end_time = datetime.datetime.utcnow()
        
        return {
            "websitename": "onedproperty",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(end_time - start_time),
            "log_id": postdata['log_id'],
            "account_type": "null",
            "post_id": str(postdata['post_id']),
            "ds_id": str(postdata['ds_id']),
            "detail": detail
        }
        
        
        
        
        
    def search_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()
        
        headers = {
            'user_agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36'
        }

        login = self.test_login(postdata)
        
        if(login['success'] == 'true'):
            data = {
                "filter_name" : postdata['post_title_th'],
                "btn_search" : "1"
            }
            post_found = "false"
            post_id = ''
            post_url = ''
            post_view = ''
            detail = 'No post with this title'
            
            res = httprequestObj.http_post('http://www.onedproperty.com/property/search', data = data, headers = headers)
            
            soup = BeautifulSoup(res.content ,features = "html")
            
            for abc in soup.find_all('div',attrs={'class':'item-title'}):
                if(str(abc.a.text) == postdata['post_title_th']):
                    post_id = str((((abc.a)['href']).split('/'))[-1])
                    post_url = str('http://www.onedproperty.com/property/'+post_id)
                    post_found = "true"
                    detail = 'Post found'
                    find_view = httprequestObj.http_get(post_url, headers = headers).text
                    soup1 = BeautifulSoup(find_view,features = "html")
                    post_v = soup1.find('ul',attrs={'class':'mb-0'})
                    pqr = 0
                    for xyz in post_v.find_all('li'):
                        pqr = pqr + 1
                        if (pqr == 3):
                            lis = xyz.text.split(' ')
                        if(pqr == 2):
                            ct = xyz.text.split(' ')
                            
                    post_view = lis[-1]
                    post_create_time = str(ct[-1])

                    if(post_view == ""):
                        post_view = '0'
                    
                    break
                    
            
        else :
            detail = 'Can not log in'
        
        end_time = datetime.datetime.utcnow()
        
        return {
            "websitename": "onedproperty",
            "success": login['success'],
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(end_time - start_time),
            "detail": detail,
            "account_type":'null',
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "post_url": post_url,
            "post_modify_time": 'No post modify time on website',
            "post_create_time": post_create_time,
            "post_view": post_view,
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
        
