from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
import re
import json
import datetime
import random
import requests
import urllib3
import sys
import json
import re


class bannforsale():

    name = 'bannforsale'

    def __init__(self):
        try:
            import configs

        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.debug = 0
        self.debugresdata = 0
        self.baseurl = 'https://bannforsale.com/'
        self.parser = 'html.parser'
        self.session = lib_httprequest()

    def register_user(self,postdata):
        self.session.http_get("https://bannforsale.com/front/logout")
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()
        
        result = {
            "websitename": self.name,
            "success": "false",
            "start_time": str(start_time),
            "ds_id": postdata["ds_id"],
            "end_time": '',
            "usage_time": '',
            "detail": ''
        }

        checkmailurl = "https://bannforsale.com/register/check-email?email={}".format(postdata['user'])
        if self.session.http_get(checkmailurl).json() == 'no':
            result['success'] = "false"
            result['detail'] = "User already registered!!"
            end_time = datetime.datetime.utcnow()     
            result['end_time'] = str(end_time)
            result['usage_time'] = str(end_time - start_time)

            return {
                "websitename": self.name,
                "success": result['success'],
                "start_time": result['start_time'],
                "ds_id": result["ds_id"],
                "end_time": result['end_time'],
                "usage_time": result['usage_time'],
                "detail": result['detail']
            }

        r = self.session.http_get("https://bannforsale.com/registers")
        soup = BeautifulSoup(r.content,'lxml')
        token = soup.find('input',attrs={'name':'_token'}).attrs.get('value')

        data = {
            '_token': token,
            'fullname': postdata['name_th'] + ' ' + postdata['surname_th'],
            'tel': postdata['tel'],
            'email': postdata['user'],
            'password': postdata['pass'],
            'repassword': postdata['pass']
        }
        
        self.session.http_post('https://bannforsale.com/register/regis', data=data)
  
        end_time = datetime.datetime.utcnow()     
        result['end_time'] = str(end_time)
        result['usage_time'] = str(end_time - start_time)

        return {
            "websitename": self.name,
            "success": "true",
            "start_time": result['start_time'],
            "ds_id": result["ds_id"],
            "end_time": result['end_time'],
            "usage_time": result['usage_time'],
            "detail": "Registered Successfully !!"
        }

    def test_login(self,postdata):
        self.session.http_get("https://bannforsale.com/front/logout")
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()

        result = {
            "websitename": self.name,
            "success": "false",
            "start_time": str(start_time),
            "ds_id": postdata["ds_id"],
            "end_time": '',
            "usage_time": '',
            "detail": '',
        }

        r = self.session.http_get("https://bannforsale.com/registers")
        soup = BeautifulSoup(r.content,'lxml')
        token = soup.find('input',attrs={'name':'_token'}).attrs.get('value')

        data = {
            '_token': token,
            'email': postdata['user'],
            'passwords': postdata['pass']
        }

        response = self.session.http_post('https://bannforsale.com/front/login', data=data)
        #soup = BeautifulSoup(response.content,'lxml')
        #if soup.text.find("ท่านต้องยืนยันการสมัครสมาชิก ในอีเมล์ของท่านก่อน") != -1:
        if response.text.find("ท่านต้องยืนยันการสมัครสมาชิก ในอีเมล์ของท่านก่อน") != -1:
            result['success'] = 'false'
            result['detail'] = "Wrong username or password"
        else:
            result['success'] = "true"
            result['detail'] = "Logged in successfully"
        
        end_time = datetime.datetime.utcnow()     
        result['end_time'] = str(end_time)
        result['usage_time'] = str(end_time - start_time)

        return {
            "websitename": self.name,
            "success": result['success'],
            "start_time": result['start_time'],
            "end_time": result['end_time'],
            "usage_time": result['usage_time'],
            "detail": result['detail'],
            "ds_id": result["ds_id"],
        }
    
    def create_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        result =  {
            "success": test_login['success'],
            "usage_time": '',
            "start_time": str(start_time),
            "end_time": '',
            "post_url": '',
            "ds_id": str(postdata['ds_id']),
            "post_id": '',
            "account_type": "null",
            "detail": '',
            "websitename": self.name
        }

        if test_login['success'] == "true":

            r = self.session.http_get("https://bannforsale.com/post")
            soup = BeautifulSoup(r.content,'lxml')
            token = soup.find('input',attrs={'name':'_token'}).attrs.get('value')
            
            if 'web_project_name' not in postdata or postdata['web_project_name'] is None:
                if 'project_name' in postdata and postdata['project_name'] is not None:
                    postdata['web_project_name'] = postdata['project_name']
                else:
                    postdata['web_project_name'] = postdata['post_title_th']
            
            prod_address = ""
            for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
                if add is not None:
                    prod_address += add + " "
            prod_address = prod_address[:-1]

            if postdata['land_size_wa'] == None or postdata['land_size_wa'] == "":
                postdata['land_size_wa'] = '0'
            if postdata['land_size_rai'] == None or postdata['land_size_rai'] == "":
                postdata['land_size_rai'] = '0'
            if postdata['land_size_ngan'] == None or postdata['land_size_ngan'] == "":
                postdata['land_size_ngan'] = '0'
            if postdata['bed_room'] == None or postdata['bed_room'] == "":
                postdata['bed_room'] = '0'

            postdata['post_description_th']=postdata['post_description_th'].replace("\n","<br>")
            data = {
                '_token' : (None,token),
                'typesale' : (None,1),
                'topic' : (None,str(postdata['post_title_th'])),
                'project' : (None,str(postdata['web_project_name'])),
                'typehome' : (None,2),
                'size' : (None,str(postdata['land_size_wa'])),
                'unitsize' : (None,"ตารางเมตร"),
                'cost' : (None,str(postdata['price_baht'])),
                'address' : (None,prod_address),
                'province' : '',
                'district' : '',
                'tel' : (None,str(postdata['mobile'])),
                'mobile' : (None,str(postdata['mobile'])),
                'sizeground' : '',
                'costarea' : (None,str(postdata['price_baht'])),
                'bed' : (None,str(postdata['bed_room'])),
                'toilet' : (None,str(postdata['bath_room'])),
                'detail' : (None,str(postdata['post_description_th'])),
                'lat' : (None,str(postdata['geo_latitude'])),
                'lng' : (None,str(postdata['geo_longitude']))
            }

            rai = str(postdata['land_size_rai']) + 'ไร่'
            ngan = str(postdata['land_size_ngan']) + 'งาน'
            square_wah = str(postdata['land_size_wa']) + 'ตารางวา'
            data['sizeground'] = (None,rai + ngan + square_wah)

            pd_properties = {
                '1': '2',
                '2': '3',
                '3': '12',
                '4': '6',
                '5': '10',
                '6': '4',
                '7': '11',
                '8': '15',
                '9': '13',
                '10': '14',
                '25': '14' 
            }
            data['typehome'] = (None,int(pd_properties[str(postdata['property_type'])]))

            if postdata['property_type'] == '1':
                data['size'] = postdata['floor_area']
                data['unitsize'] = 'ตร.ม.'

            else:
                data['size'] = (400 * int(postdata['land_size_rai'])) + (100 * int(postdata['land_size_ngan'])) + (1*float(str(postdata['land_size_wa'])))
                data['unitsize'] = 'ตร.ว.'

            if postdata['listing_type'] == 'ขาย':
                data['typesale'] = (None,1)
            else:
                data['typesale'] = (None,2)
            
            fp = open('./static/bannforsale_province.json')
            provinces = json.load(fp)
            province = ''.join(map(str,str(postdata['addr_province']).split(' ')))
            for item in provinces.items():
                if province in ''.join(map(str,str(item[0]).split(' '))):
                    data['province'] = (None,item[1])  
                    break
            
            params = (
                ('province', data['province']),
                ('_token', token),
            )
            districts = requests.get('https://bannforsale.com/product/post/aumphure', params=params).json()
            district = ''.join(map(str,str(postdata['addr_district']).split(' ')))
            for d in districts:
                if district in ''.join(map(str,str(d['name'].split(' ')[0]).split(' '))):
                    data['district'] = (None,d['id'])
                    break
            
            if len(postdata['post_images']) > 0:
                files = [('imgtopic', open(os.getcwd()+"/"+postdata["post_images"][0], 'rb'))]    
            else:
                files = [('imgtopic', open('imgtmp/default/white.jpg', 'rb'))]         

            allimages = postdata["post_images"]
            #print(allimages)
            theimgs = []
            for ind, i in enumerate(allimages):
                r = (i, open(i, "rb"), "image/jpeg")
                theimgs.append(('photo[]',r))
                files.append(('upgal[]',r))

            response = self.session.http_post('https://bannforsale.com/product/test/sendimg', data={}, files=theimgs)
            #print(response.text)


            response = self.session.http_post('https://bannforsale.com/member/addproduct', data=data, files=files)
            #print(response.status_code)

            r = self.session.http_get("https://bannforsale.com/view-post")
            soup = BeautifulSoup(r.content, 'lxml')
            post_url = soup.find('tbody').find('tr').find('a').attrs.get('href')
            result['post_url'] = post_url
            result['post_id'] = post_url.split('/')[-2]
            result['detail'] = "Post Created Succesfully"
            result['success'] = "true" 

        else:
            result['success'] = "false"
            result['detail'] = 'cannot login'

        end_time = datetime.datetime.utcnow()     
        result['end_time'] = str(end_time)
        result['usage_time'] = str(end_time - start_time)

        return {
            "success": result['success'],
            "usage_time": result['usage_time'],
            "start_time": result['start_time'],
            "end_time": result['end_time'],
            "post_url": result['post_url'],
            "ds_id": result['ds_id'],
            "post_id": result['post_id'],
            "account_type": result['account_type'],
            "detail": result['detail'],
            "websitename": result['websitename']
        }
    
    def edit_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()
        detail = ''
        post_id = postdata['post_id']
        post_url = ''
        success = 'false'
        delete = self.delete_post(postdata)
        post_id = postdata['post_id']
        if delete['success']== 'true':
            post = self.create_post(postdata)
            post_url = post['post_url']
            post_id = post['post_id']
            success = post['success']
            detail = post['detail']
            if success == 'true':
                detail = "Post Edited Succesfully"
        else:
            detail = delete['detail']
        """test_login = self.test_login(postdata)
        result =  {
            "success": test_login['success'],
            "usage_time": '',
            "start_time": str(start_time),
            "end_time": '',
            "log_id": postdata['log_id'],
            "ds_id": str(postdata['ds_id']),
            "account_type": "null",
            "detail": '',
            "websitename": self.name
        }

        if test_login['success'] == "true":
            url = 'https://bannforsale.com/post/{}/edit'.format(postdata['post_id'])
            r = self.session.http_get(url)
            if r.status_code == 500:
                end_time = datetime.datetime.utcnow()     
                result['end_time'] = str(end_time)
                result['usage_time'] = str(end_time - start_time)
                return {
                    "success": "false",
                    "usage_time": result["usage_time"],
                    "start_time": str(start_time),
                    "end_time": result['end_time'],
                    "log_id": postdata['log_id'],
                    "account_type": "null",
                    "ds_id": str(postdata['ds_id']),
                    "detail": "No post to edit with given id",
                    "websitename": self.name
                }
            
            if 'bed_room' not in postdata:
                postdata['bed_room'] = 0
            if 'bath_room' not in postdata:
                postdata['bath_room'] = 0
            
            r = self.session.http_get("https://bannforsale.com/post")
            soup = BeautifulSoup(r.content,'lxml')
            token = soup.find('input',attrs={'name':'_token'}).attrs.get('value')
            
            if 'web_project_name' not in postdata or postdata['web_project_name'] is None:
                if 'project_name' in postdata and postdata['project_name'] is not None:
                    postdata['web_project_name'] = postdata['project_name']
                else:
                    postdata['web_project_name'] = postdata['post_title_th']
            
            prod_address = ""
            for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
                if add is not None:
                    prod_address += add + " "
            prod_address = prod_address[:-1]

            if postdata['land_size_wa'] == None or postdata['land_size_wa'] == "":
                postdata['land_size_wa'] = 0
            if postdata['land_size_rai'] == None or postdata['land_size_rai'] == "":
                postdata['land_size_rai'] = '0'
            if postdata['land_size_ngan'] == None or postdata['land_size_ngan'] == "":
                postdata['land_size_ngan'] = '0'

            data = {
                '_token' : (None,token),
                'id' : (None, postdata['post_id']),
                'typesale' : (None,1),
                'topic' : (None,str(postdata['post_title_th'])),
                'project' : (None,str(postdata['web_project_name'])),
                'typehome' : (None,2),
                'size' : (None,str(postdata['land_size_wa'])),
                'unitsize' : (None,"ตารางเมตร"),
                'cost' : (None,str(postdata['price_baht'])),
                'address' : (None,prod_address),
                'province' : '',
                'district' : '',
                'tel' : (None,str(postdata['mobile'])),
                'mobile' : (None,str(postdata['mobile'])),
                'sizeground' : '',
                'costarea' : (None,str(postdata['price_baht'])),
                'bed' : (None,str(postdata['bed_room'])),
                'toilet' : (None,str(postdata['bath_room'])),
                'detail' : (None,str(postdata['post_description_th'])),
                'lat' : (None,str(postdata['geo_latitude'])),
                'lng' : (None,str(postdata['geo_longitude']))
            }

            rai = str(postdata['land_size_rai']) + 'ไร่'
            ngan = str(postdata['land_size_ngan']) + 'งาน'
            square_wah = str(postdata['land_size_wa']) + 'ตารางวา'
            data['sizeground'] = (None,rai + ngan + square_wah)

            pd_properties = {
                '1': '2',
                '2': '3',
                '3': '12',
                '4': '6',
                '5': '10',
                '6': '4',
                '7': '11',
                '8': '15',
                '9': '13',
                '10': '14',
                '25': '14' 
            }
            data['typehome'] = (None,int(pd_properties[str(postdata['property_type'])]))

            if postdata['property_type'] == '1':
                data['size'] = postdata['floor_area']
                data['unitsize'] = 'ตร.ม.'

            else:
                data['size'] = (400 * int(postdata['land_size_rai'])) + (100 * int(postdata['land_size_ngan'])) + (1*float(str(postdata['land_size_wa'])))
                data['unitsize'] = 'ตร.ว.'

            if postdata['listing_type'] == 'ขาย':
                data['typesale'] = (None,1)
            else:
                data['typesale'] = (None,2)
            
            fp = open('./static/bannforsale_province.json')
            provinces = json.load(fp)
            province = ''.join(map(str,str(postdata['addr_province']).split(' ')))
            for item in provinces.items():
                if province in ''.join(map(str,str(item[0]).split(' '))):
                    data['province'] = (None,item[1])  
                    break
            
            params = (
                ('province', data['province']),
                ('_token', token),
            )
            districts = requests.get('https://bannforsale.com/product/post/aumphure', params=params).json()
            district = ''.join(map(str,str(postdata['addr_district']).split(' ')))
            for d in districts:
                if district in ''.join(map(str,str(d['name'].split(' ')[0]).split(' '))):
                    data['district'] = (None,d['id'])
                    break
            if len(postdata['post_images']) > 0:
                files = [('imgtopic', open(os.getcwd()+"/"+postdata["post_images"][0], 'rb'))]    
            else:
                files = [('imgtopic', open('imgtmp/default/white.jpg', 'rb'))]        
            allimages = postdata["post_images"]
            #print(allimages)
            theimgs = []
            for ind, i in enumerate(allimages):
                r = (i, open(i, "rb"), "image/jpeg")
                theimgs.append(('photo[]',r))
                files.append(('upgal[]',r))

            response = self.session.http_post('https://bannforsale.com/product/test/sendimg', data={}, files=theimgs)
            #print(response.text)


            response = self.session.http_post('https://bannforsale.com/member/editproduct', data=data, files=files)
            
            result['detail'] = "Post Edited Succesfully"
            result['success'] = "true"

        else:
            result['success'] = "false"
            result['detail'] = 'cannot login'"""

        end_time = datetime.datetime.utcnow()     

        return {
            "success": success,
            "usage_time": str(end_time - start_time),
            "start_time": str(start_time),
            "end_time": str(end_time),
            "log_id": postdata['log_id'],
            "ds_id": str(postdata['ds_id']),
            "post_id": post_id,
            'post_url':post_url,
            "account_type": "null",
            "detail": detail,
            "websitename": self.name
        }

    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        
        result = {
            "success": test_login["success"],
            "usage_time": '',
            "start_time": str(start_time),
            "end_time": '',
            "detail": '',
            "websitename": self.name,
            "ds_id": str(postdata['ds_id']),
            "log_id": postdata['log_id'],
            "post_id": postdata['post_id']
        }

        if test_login['success'] == "true":

            params = (
                ('id', postdata['post_id']),
            )

            response = requests.get('https://bannforsale.com/post/{}/deledata'.format(postdata['post_id']), params=params)
            if response.status_code == 500:
                result['success'] = "false"
                result['detail'] = "No post found with given id."
            else:
                result['success'] = "true"
                result['detail'] = "Post deleted successfully."
        
        else:
            result['success'] = "false"
            detail = "cannot login"

        end_time = datetime.datetime.utcnow()     
        result['end_time'] = str(end_time)
        result['usage_time'] = str(end_time - start_time)

        return {
            "success": result["success"],
            "usage_time": result["usage_time"],
            "start_time": result["start_time"],
            "end_time": result["end_time"],
            "detail": result['detail'],
            "websitename": self.name,
            "ds_id": str(postdata['ds_id']),
            "log_id": result['log_id'],
            "post_id": postdata['post_id']
        }

    def search_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)

        result = {
            "success": test_login['success'],
            "usage_time": '',
            "start_time": str(start_time),
            "end_time": '',
            "detail": '',
            "websitename": self.name,
            "account_type":None,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": '',
            "post_modify_time": '',
            "post_view": '',
            "post_url": '',
            "post_found": "false",
            "post_title_th": postdata['post_title_th']
        }

        if test_login['success'] == "true":
            flag = True
            r = self.session.http_get("https://bannforsale.com/view-post")
            x = 2
            while(flag):
                soup = BeautifulSoup(r.content, 'lxml')
                rows = soup.find('tbody').find_all('tr')
                found = 0
                for row in rows:
                    tds = row.find_all('td')
                    if postdata['post_title_th'] in tds[2].text:
                        found = 1
                        result['post_id'] = tds[2].find('a').attrs.get('href').split('/')[-2]
                        result['post_url'] = tds[2].find('a').attrs.get('href')
                        result['detail'] = "Post Found"
                        result['post_found'] = "true"
                        result['post_view'] = tds[5].text
                        result['post_modify_time'] = tds[4].text
                        flag = False
                        break

                if found == 0:
                    r = self.session.http_get('https://bannforsale.com/view-post?page={}'.format(x))
                    x = x+1
                    soup2 = BeautifulSoup(r.content, 'lxml')
                    if len(soup2.find('tbody').find_all('tr')) == 0:
                        flag = False
                          
            if not found:
                result['success'] = "false"
                result['detail'] = "No post found with given title"

        else:
            result['success'] = "false"
            result['detail'] = "cannot login"
        
        end_time = datetime.datetime.utcnow()     
        result['end_time'] = str(end_time)
        result['usage_time'] = str(end_time - start_time)

        return {
            "success": result['success'],
            "usage_time": result['usage_time'],
            "start_time": result['start_time'],
            "end_time": result['end_time'],
            "detail": result['detail'],
            "websitename": self.name,
            "account_type":None,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": result['post_id'],
            "post_create_time": '',
            "post_modify_time": result['post_modify_time'],
            "post_view": result['post_view'],
            "post_url": result['post_url'],
            "post_found": result['post_found'],
            "post_title_th": postdata['post_title_th']
        }
    
    def boost_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        
        result = {
            "success": test_login["success"],
            "usage_time": '',
            "start_time": str(start_time),
            "end_time": '',
            "detail": '',
            "websitename": self.name,
            "ds_id": str(postdata['ds_id']),
            "log_id": postdata['log_id']
        }

        if test_login['success'] == "true":
            flag = True
            r = self.session.http_get("https://bannforsale.com/view-post")
            x = 2
            while(flag):
                soup = BeautifulSoup(r.content, 'lxml')
                rows = soup.find('tbody').find_all('tr')
                found = 0
                for row in rows:
                    tds = row.find_all('td')
                    if str(postdata['post_id']) == str(tds[2].find('a').attrs.get('href').split('/')[-2]):
                        found = 1
                        result['success'] = "true"
                        result['detail'] = "Post boosted successfully."
                        flag = False
                        break

                if found == 0:
                    r = self.session.http_get('https://bannforsale.com/view-post?page={}'.format(x))
                    x = x+1
                    soup2 = BeautifulSoup(r.content, 'lxml')
                    if len(soup2.find('tbody').find_all('tr')) == 0:
                        flag = False
                        break

            if not found:
                result['success'] = "false"
                result['detail'] = "No post found with given id"
        
        else:
            result['success'] = "false"
            detail = "cannot login"

        end_time = datetime.datetime.utcnow()     
        result['end_time'] = str(end_time)
        result['usage_time'] = str(end_time - start_time)

        return {
            "success": result["success"],
            "usage_time": result["usage_time"],
            "start_time": result["start_time"],
            "end_time": result["end_time"],
            "detail": result['detail'],
            "websitename": self.name,
            "ds_id": str(postdata['ds_id']),
            "log_id": result['log_id']
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