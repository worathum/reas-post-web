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

httprequestObj = lib_httprequest()

class evaphukettown():

    name = 'evaphukettown'

    def __init__(self):
        try:
            import configs

        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.debug = 0
        self.debugresdata = 0
        self.baseurl = 'http://www.evaphukettown.com/classified/'

    def register_user(self,postdata):
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

        url = "http://www.evaphukettown.com/classified/register.php"
        r = httprequestObj.http_get(url)
        soup = BeautifulSoup(r.content,'lxml')
        save = soup.find('input',attrs={'id':'save'}).attrs.get('value')
        answer = soup.find('input',attrs={'id':'hiddenanswer'}).attrs.get('value')

        data = {
            'save': save,
            'email': postdata['user'],
            'password': postdata['pass'],
            'repassword': postdata['pass'],
            'name': postdata['name_th'] + ' ' + postdata['surname_th'],
            'phone': postdata['tel'],
            'address': 'พญาไท กรุงเทพ 10400',
            'province': '2',
            'amphur': '22',
            'zipcode': '10400',
            'title': '',
            'description': '',
            'keyword': '',
            'website': '',
            'answer': answer,
            'hiddenanswer': answer,
            'accept': '1'
        }

        r = httprequestObj.http_post('http://www.evaphukettown.com/classified/lib/checkuser.php', data=data)
        if str(r.text) == '-1':
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

        r = httprequestObj.http_post('http://www.evaphukettown.com/classified/register.php', data=data)
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
        r = httprequestObj.http_get('http://www.evaphukettown.com/classified/logout.php')
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

        url = "http://www.evaphukettown.com/classified/member.php"
        r = httprequestObj.http_get(url)
        soup = BeautifulSoup(r.content,'lxml')
        save = soup.find('input',attrs={'id':'save'}).attrs.get('value')

        data = {
            'save' : save,
            'email' : postdata['user'],
            'password' : postdata['pass']
        }
        r = httprequestObj.http_post(url, data=data)
        soup = BeautifulSoup(r.content,'lxml')

        if soup.find('h3').attrs.get('class')[0] == 'fail':
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
            
            url = "http://www.evaphukettown.com/classified/post-add.php"
            r = httprequestObj.http_get(url)
            soup = BeautifulSoup(r.content,'lxml')
            save = soup.find('input',attrs={'id':'save'}).attrs.get('value')

            if 'web_project_name' not in postdata or postdata['web_project_name'] is None:
                if 'project_name' in postdata and postdata['project_name'] is not None:
                    postdata['web_project_name'] = postdata['project_name']
                else:
                    postdata['web_project_name'] = postdata['post_title_th']
            
            pd_properties = {
                '1': '1149', #condo
                '2': '1147', #detached house
                '3': '1147', #twin house
                '4': '1154', #townhouse
                '5': '1153', #commercial building
                '6': '1148', #land
                '7': '1150', #apartment
                '8': '1156', #hotel
                '9': '1151', #office
                '10': '1155',#factory warehouse
                '25': '1155' #factory 
            }
            
            data = {
                'save' : (None, save),
                'type' : (None, 'guest'),
                'want' : '',
                'status' : (None, '2hand'),
                'duration' : (None, '-1'),
                'category' : (None, '1009'),
                'subcategory' : (None,int(pd_properties[str(postdata['property_type'])])),
                'city' : '1',
                'district' : '4',
                'name' : (None, str(postdata['post_title_th'])),
                'price' : (None, str(postdata['price_baht'])),
                'detail' : (None, str(postdata['post_description_th'])),
                'maplat' : (None,str(postdata['geo_latitude'])),
                'maplon' : (None,str(postdata['geo_longitude']))
            }

            if postdata['listing_type'] == 'ขาย':
                data['want'] = (None,'sale')
            else:
                data['want'] = (None,'forrent')

            fp = open('./static/evaphukettown_province.json')
            provinces = json.load(fp)
            province = ''.join(map(str,str(postdata['addr_province']).split(' ')))
            for item in provinces.items():
                if province in ''.join(map(str,str(item[0]).split(' '))):
                    data['city'] = (None,item[1])  
                    break
            
            params = (
                ('province', data['city']),
            )

            districts = requests.get('http://www.evaphukettown.com/classified/lib/district.php', params=params)
            districts = BeautifulSoup(districts.content, 'lxml').find_all('option')
            district = ''.join(map(str,str(postdata['addr_district']).split(' ')))
            for d in districts:
                if district in ''.join(map(str,str(d.text.split(' ')[0]).split(' '))):
                    data['district'] = (None, d.attrs.get('value'))
                    break

            files = {}
            try:
                allimages = postdata["post_images"][:6]    
            except:
                allimages = postdata["post_images"]
            #print(allimages)
            for i in range(len(allimages)):
                r = open(os.getcwd()+"/"+allimages[i], 'rb')
                name = 'photo{}'.format(i+1)
                files[name] = ("{}".format(allimages[i]),r,"image/jpeg")
            
            response = httprequestObj.http_post('http://www.evaphukettown.com/classified/post-add.php', data=data, files=files)
            soup = BeautifulSoup(response.content, 'lxml')
            post_url = soup.find('h3',attrs={'class':'success'}).find('a').attrs.get('href')
            result['post_url'] = post_url
            result['post_id'] = post_url.split('/')[-1][2:]
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

        test_login = self.test_login(postdata)
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
            
            url = "http://www.evaphukettown.com/classified/post-edit.php?id={}".format(postdata['post_id'])
            r = httprequestObj.http_get(url)
            soup = BeautifulSoup(r.content,'lxml')
            save = soup.find('input',attrs={'id':'save'}).attrs.get('value')

            if 'web_project_name' not in postdata or postdata['web_project_name'] is None:
                if 'project_name' in postdata and postdata['project_name'] is not None:
                    postdata['web_project_name'] = postdata['project_name']
                else:
                    postdata['web_project_name'] = postdata['post_title_th']
            
            pd_properties = {
                '1': '1149', #condo
                '2': '1147', #detached house
                '3': '1147', #twin house
                '4': '1154', #townhouse
                '5': '1153', #commercial building
                '6': '1148', #land
                '7': '1150', #apartment
                '8': '1156', #hotel
                '9': '1151', #office
                '10': '1155',#factory warehouse
                '25': '1155' #factory 
            }
            
            data = {
                'save' : (None, save),
                'type' : (None, 'guest'),
                'want' : '',
                'status' : (None, '2hand'),
                'duration' : (None, '-1'),
                'category' : (None, '1009'),
                'subcategory' : (None,int(pd_properties[str(postdata['property_type'])])),
                'city' : '1',
                'district' : '4',
                'name' : (None, str(postdata['post_title_th'])),
                'price' : (None, str(postdata['price_baht'])),
                'detail' : (None, str(postdata['post_description_th'])),
                'maplat' : (None,str(postdata['geo_latitude'])),
                'maplon' : (None,str(postdata['geo_longitude']))
            }

            if postdata['listing_type'] == 'ขาย':
                data['want'] = (None,'sale')
            else:
                data['want'] = (None,'forrent')

            fp = open('./static/evaphukettown_province.json')
            provinces = json.load(fp)
            province = ''.join(map(str,str(postdata['addr_province']).split(' ')))
            for item in provinces.items():
                if province in ''.join(map(str,str(item[0]).split(' '))):
                    data['city'] = (None,item[1])  
                    break
            
            params = (
                ('province', data['city']),
            )

            districts = requests.get('http://www.evaphukettown.com/classified/lib/district.php', params=params)
            districts = BeautifulSoup(districts.content, 'lxml').find_all('option')
            district = ''.join(map(str,str(postdata['addr_district']).split(' ')))
            for d in districts:
                if district in ''.join(map(str,str(d.text.split(' ')[0]).split(' '))):
                    data['district'] = (None, d.attrs.get('value'))
                    break

            files = {}
            try:
                allimages = postdata["post_images"][:6]    
            except:
                allimages = postdata["post_images"]
            #print(allimages)
            for i in range(len(allimages)):
                r = open(os.getcwd()+"/"+allimages[i], 'rb')
                name = 'photo{}'.format(i+1)
                files[name] = ("{}".format(allimages[i]),r,"image/jpeg")
            
            response = httprequestObj.http_get(url)
            if response.text.find('กฏสำคัญการลงประกาศ') == -1:
                result['detail'] = 'Invalid Post ID'
                result['success'] = 'false'
            else:
                response = httprequestObj.http_post(url, data=data, files=files)
                result['detail'] = "Post Edited Succesfully"
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
            "log_id": postdata['log_id'],
            "ds_id": str(postdata['ds_id']),
            "account_type": "null",
            "detail": result['detail'],
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
            "log_id": postdata['log_id']
        }

        if test_login['success'] == "true":
            
            url = "http://www.evaphukettown.com/classified/manage-post.php?delete={}".format(postdata['post_id'])
            response = httprequestObj.http_get(url)
            soup = BeautifulSoup(response.content,'lxml')
            if soup.find('h3',attrs={'class':'success'}) == None:
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
            "log_id": result['log_id']
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
            "post_found": "false"
        }

        if test_login['success'] == "true":
            
            page = 0
            post_found = False
            tot_pages = 100

            while True:
                page += 1
                if page > tot_pages:
                    break
                r = httprequestObj.http_get('http://www.evaphukettown.com/classified/manage-post.php', params={'page': str(page)})
                print(r.url)
                # print(r.status_code)

                soup = BeautifulSoup(r.content, 'lxml')
                tot_pages = int(len(soup.find('div', 'pagination').find('ul').find_all('li'))) - 2
                all_posts = soup.find('div', 'postlist').findChildren('ul')

                for post in all_posts:
                    print(post.find('li',attrs={'class':'title'}).find('a').text)
                    if postdata['post_title_th'].strip().replace('.', '').replace(',', '')[:100] in post.find('li',attrs={'class':'title'}).find('a').text:
                        post_found = True
                        result['post_url'] = post.find('li',attrs={'class':'title'}).find('a').attrs.get('href')
                        result['post_id'] = post.find('li',attrs={'class':'title'}).find('a').attrs.get('href').split('/')[-1][2:]
                        result['detail'] = "Post Found"
                        result['post_view'] = post.find('span',attrs={'class':'pageview'}).text[-1]
                        result['post_modify_time'] = post.find('li',attrs={'class':'date'}).find_all('span')[1].text + ' ' +  post.find('li',attrs={'class':'date'}).find_all('span')[2].text
                        break
                if post_found:
                    break
            
            if not post_found:
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
            "post_modify_time": result['post_modify_time'],
            "post_view": result['post_view'],
            "post_url": result['post_url'],
            "post_found": post_found,
            'post_title_th': postdata['post_title_th']
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

            page = 0
            post_found = False
            tot_pages = 100

            while True:
                page += 1
                if page > tot_pages:
                    break
                r = httprequestObj.http_get('http://www.evaphukettown.com/classified/manage-post.php', params={'page': str(page)})
                print(r.url)
                # print(r.status_code)

                soup = BeautifulSoup(r.content, 'lxml')
                tot_pages = int(len(soup.find('div', 'pagination').find('ul').find_all('li'))) - 2
                all_posts = soup.find('div', 'postlist').findChildren('ul')
                # print(tot_pages)

                # if len(all_posts) == 0:
                #     break

                for post in all_posts:
                    post_id = post.find('li', 'title').find('a').get('href').split('/')[-1][2:]
                    print(post_id)

                    if post_id == postdata['post_id']:
                        post_found = True
                        break

                if post_found:
                    break
            
            if post_found:
                result['success'] = "true"
                httprequestObj.http_get("http://www.evaphukettown.com/classified/manage-post.php?update={}".format(postdata['post_id']))
                result['detail'] = "Post boosted successfully."

            else:
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
