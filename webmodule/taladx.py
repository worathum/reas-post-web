from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
import re
import json
import datetime
import sys
import requests
import random
import urllib.parse as urlparse
from urllib.parse import parse_qs

httprequestObj = lib_httprequest()

class taladx():
   
    name = 'taladx'

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
        self.baseurl = 'http://www.taladx.com'
        self.parser = 'html.parser'



    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        
        start_time = datetime.datetime.utcnow()
        httprequestObj.http_get('http://www.taladx.com/logout.php')
        

        headers = {
            'user_agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36'
        }

        data = {
            'save': "82r5i3p4j4rli9rb7sbpve9a16",
            'email': postdata['user'],
            'password': postdata['pass'],
            'repassword': postdata['pass'],
            'name': str(postdata['name_title'] + '. ' + postdata['name_th'] + ' ' + postdata['surname_th']),
            'phone': str(postdata['tel']),
            'address': 'พญาไท กรุงเทพ',
            'province': '2',
            'amphur': '22',
            'zipcode': '10400',
            'title': '',
            'description': '',
            'keyword': '',
            'website': '',
            'answer': '',
            'hiddenanswer': '',
            'accept': '1'
        }

        response = httprequestObj.http_get('http://www.taladx.com/register.php').text

        soup = BeautifulSoup(response,features = self.parser)

        req = soup.find('input', attrs={'name' : 'hiddenanswer'})

        ans = str(req['value'])

        data['answer'] = ans
        data['hiddenanswer'] = ans

        success = "false"
        detail = ""

        if data['email'] == "":
            detail = "Invalid email"
        elif data['password'] == "":
            detail = "Invalid Password"
        elif data['password'] != data['repassword']:
            detail = "Invalid Password Confirmation"
        elif data['name'] == "":
            detail = "Please enter your name"
        elif data['phone'] == "":
            detail = "Please enter your phone number"
        elif len(str(data['password'])) < 6 :
            detail = "Password must be atleast 6 characters long"
        else:
            try:
                response = httprequestObj.http_post('http://www.taladx.com/register.php', data = data, headers = headers)
                #if response.text.find("มีอยู่ในระบบแล้ว") != -1:
                if response.url == 'http://www.taladx.com/register.php':
                    success = "false"
                    detail = "Email Already registered"
                else :
                    success = "true"
                    detail = "Registered Successfully"

                #print(response.url)
                    
            except requests.exceptions.RequestException:
                detail = "Network Problem occured"
            
        end_time = datetime.datetime.utcnow()

        return {
            "websitename": "taladx",
            'ds_id': postdata['ds_id'],
            "success": success,
            "ds_id": str(postdata['ds_id']),
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(end_time - start_time),
            "detail": detail
        }



    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        
        start_time = datetime.datetime.utcnow()
        httprequestObj.http_get('http://www.taladx.com/logout.php')

        data = {
            'save': 'pr1sb7ul4pvmuaogt7pk3aepj5',
            'email': postdata['user'],
            'password': postdata['pass']
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
                response = httprequestObj.http_post('http://www.taladx.com/member.php', data = data, headers = headers)
                #print(response.url) 
                
                soup = BeautifulSoup(response.content , features = self.parser)
                if soup.find_all("h3", attrs={'class':"fail"}):
                #if (response.url == 'http://www.estate.in.th/login.php' or response.url == 'http://www.estate.in.th/signup.php'):
                    success = "false"
                    detail = 'Incorrect Username or Password !!'
                else:
                    success = "true"
                    detail = 'Logged in successfully'
            
            except requests.exceptions.RequestException:
                detail = "Network Problem occured"

        end_time = datetime.datetime.utcnow()

        return {
            "websitename": 'taladx',
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
                "save":'v0i7vqffc5r14r14rgqtsnb011',
                "type":'guest',
                "want":'',
                "status":'2hand',
                "duration":'-1',
                "category":'1009',
                "subcategory":'',
                "city":'1',
                "district":'4',
                "name":str(postdata['post_title_th'].replace("\r\n","\n")),
                "price": str(postdata['price_baht']),
                "detail":str(postdata['post_description_th'].replace("\r\n","\n")),
                "maplat":str(postdata['geo_latitude']),
                "maplon":str(postdata['geo_longitude'])
            }

            if postdata['listing_type'] == 'เช่า':
                data['want'] = 'forrent'
            else:
                data['want'] = 'sale'

            pd_properties = {
                '1': '1149',
                '2': '1147',
                '3': '1154',
                '4': '1154',
                '5': '1153',
                '6': '1148',
                '7': '1150',
                '8': '1156',
                '9': '1151',
                '10': '1155',
                '25': '1155' 
            }

            data['subcategory'] = pd_properties[str(postdata['property_type'])]

            province = ''.join(map(str,str(postdata['addr_province']).split(' ')))

            find_province = httprequestObj.http_get('http://www.taladx.com/post-add.php', headers = headers).text

            soup = BeautifulSoup(find_province,features = self.parser)

            abc = soup.find('select',attrs = {'name':'city'})

            for pq in abc.find_all('option'):
                if(str(pq.text) in str(province) or str(province) in str(pq.text)):
                    data['city'] = str(pq['value'])
                    break

            district = ''.join(map(str,str(postdata['addr_district']).split(' ')))

            url_district = str('http://www.taladx.com/lib/district.php?province='+data['city'])

            find_district = httprequestObj.http_get(url_district, headers = headers).text

            soup = BeautifulSoup(find_district,features = self.parser)

            if 'เมือง' in  district:
                district = district.replace('เมือง', '')
            try:

                for pqr in soup.find_all('option'):
                    if(str(pqr.text) in str(district) or str(district) in str(pqr.text)):
                        data['district'] = str(pqr['value'])
                        break

            except:
                data['district'] = str(soup.find('option')['value'])

            if 'post_images' in postdata and len(postdata['post_images']) > 0:
                pass
            else:
                postdata['post_images'] = ['./imgtmp/default/white.jpg']


            file = []
            temp = 1


            if len(postdata['post_images']) <= 6:
                for i in postdata['post_images']:
                    y=str(random.randint(0,100000000000000000))+".jpg"
                    #print(y)
                    file.append((str('photo'+str(temp)), (y, open(i, "rb"), "image/jpg")))
                    temp = temp + 1

            else:
                for i in postdata['post_images'][:6]:
                    y=str(random.randint(0,100000000000000000))+".jpg"
                    #print(y)
                    file.append((str('photo'+str(temp)), (y, open(i, "rb"), "image/jpg")))
                    temp = temp + 1

            post_create = httprequestObj.http_post("http://www.taladx.com/post-add.php", data = data, files = file, headers = headers)
            success = "true"
            detail = "Post created successfully"
            #print(post_create.url)

            url = post_create.url

            parsed = urlparse.urlparse(url)

            #print(str(parse_qs(parsed.query)['newid']))

            post_id = str((parse_qs(parsed.query)['newid'])[0])
            #print(post_id)

            post_title = str((parse_qs(parsed.query)['name'])[0])

            #print(post_title)

            post_url = str('http://www.taladx.com/view'+post_id+'/'+post_title)



        else:
            success = "false"
            detail = "Can not log in"
            
        end_time = datetime.datetime.utcnow()
        
        return {
            "websitename": "taladx",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(end_time - start_time),
            "post_url": post_url,
            "ds_id": str(postdata['ds_id']),
            "post_id": post_id,
            "detail": detail,
            "account_type": "null"
        }




    def boost_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()
        
        headers = {
            'user_agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36'
        }

        login = self.test_login(postdata)
        
        if login['success'] == "true":
            page = 1
            req_post_id = str(postdata['post_id'])
            all_post_ids = set([])
            found = False
            flag = False
            while True:
                requ = httprequestObj.http_get("http://www.taladx.com/manage-post.php?page=" + str(page), headers=headers).content
                soup = BeautifulSoup(requ, features = "html.parser")
                all_post = soup.find_all('span',attrs={'class':"code"})
                for abc in all_post:
                    total_text = abc.text.split()
                    if str(total_text[-1].strip())==req_post_id:
                        found = True
                        break
                    if str(total_text[-1].strip()) in all_post_ids:
                        flag = True
                        break
                    all_post_ids.add(str(total_text[-1].strip()))
                page += 1
                if (not all_post) or found or flag:
                    break

            if found:
                boost_url = str('http://www.taladx.com/manage-post.php?update='+req_post_id)
                res = httprequestObj.http_get(boost_url, headers = headers)
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
            "websitename": "taladx",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(end_time - start_time),
            "detail": detail,
            "post_id": str(postdata['post_id']),
            "ds_id": str(postdata['ds_id']),
            "log_id": postdata['log_id'],
            "post_view": ""
        }



    def delete_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()
        
        headers = {
            'user_agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36'
        }

        login = self.test_login(postdata)
        
        if login['success'] == "true":
            page = 1
            req_post_id = str(postdata['post_id'])
            all_post_ids = set([])
            found = False
            flag = False
            while True:
                requ = httprequestObj.http_get("http://www.taladx.com/manage-post.php?page=" + str(page), headers=headers).content
                soup = BeautifulSoup(requ, features = "html.parser")
                all_post = soup.find_all('span',attrs={'class':"code"})
                for abc in all_post:
                    total_text = abc.text.split()
                    if str(total_text[-1].strip())==req_post_id:
                        found = True
                        break
                    if str(total_text[-1].strip()) in all_post_ids:
                        flag = True
                        break
                    all_post_ids.add(str(total_text[-1].strip()))
                page += 1
                if (not all_post) or found or flag:
                    break

            if found:
                delete_url = str('http://www.taladx.com/manage-post.php?delete='+req_post_id)
                res = httprequestObj.http_get(delete_url, headers = headers)
                success = "true"
                detail = "Post deleted successfully"
            else:
                success = "false"
                detail = "post_id is incorrect"
        else :
            success = "false"
            detail = "Login failed"

        end_time = datetime.datetime.utcnow()
        return {
            "websitename": "taladx",
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
            page = 1
            req_post_id = str(postdata['post_id'])
            all_post_ids = set([])
            found = False
            flag = False
            while True:
                requ = httprequestObj.http_get("http://www.taladx.com/manage-post.php?page=" + str(page), headers=headers).content
                soup = BeautifulSoup(requ, features = "html.parser")
                all_post = soup.find_all('span',attrs={'class':"code"})
                for abc in all_post:
                    total_text = abc.text.split()
                    if str(total_text[-1].strip())==req_post_id:
                        found = True
                        break
                    if str(total_text[-1].strip()) in all_post_ids:
                        flag = True
                        break
                    all_post_ids.add(str(total_text[-1].strip()))
                page += 1
                if (not all_post) or found or flag:
                    break

            if found:
                post_url = str('http://www.taladx.com/post-edit.php?id='+req_post_id)

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
                    "save":'kbhkruqefscukcu7pv03011814',
                    "type":'guest',
                    "want":'',
                    "status":'2hand',
                    "duration":'-1',
                    "category":'1009',
                    "subcategory":'',
                    "city":'1',
                    "district":'4',
                    "name":str(postdata['post_title_th'].replace("\r\n","\n")),
                    "price": str(postdata['price_baht']),
                    "detail":str(postdata['post_description_th'].replace("\r\n","\n")),
                    "maplat":str(postdata['geo_latitude']),
                    "maplon":str(postdata['geo_longitude'])
                }


                if postdata['listing_type'] == 'เช่า':
                    data['want'] = 'forrent'
                else:
                    data['want'] = 'sale'

                pd_properties = {
                    '1': '1149',
                    '2': '1147',
                    '3': '1154',
                    '4': '1154',
                    '5': '1153',
                    '6': '1148',
                    '7': '1150',
                    '8': '1156',
                    '9': '1151',
                    '10': '1155',
                    '25': '1155' 
                }

                data['subcategory'] = pd_properties[str(postdata['property_type'])]

                province = ''.join(map(str,str(postdata['addr_province']).split(' ')))

                find_province = httprequestObj.http_get(post_url, headers = headers).text

                soup = BeautifulSoup(find_province,features = self.parser)

                abc = soup.find('select',attrs = {'name':'city'})

                for pq in abc.find_all('option'):
                    if(str(pq.text) in str(province) or str(province) in str(pq.text)):
                        data['city'] = str(pq['value'])
                        break



                district = ''.join(map(str,str(postdata['addr_district']).split(' ')))

                url_district = str('http://www.taladx.com/lib/district.php?province='+data['city'])

                find_district = httprequestObj.http_get(url_district, headers = headers).text

                soup = BeautifulSoup(find_district,features = self.parser)

                try:

                    for pqr in soup.find_all('option'):
                        if(str(pqr.text) in str(district) or str(district) in str(pqr.text)):
                            data['district'] = str(pqr['value'])
                            break

                except:
                    data['district'] = str(soup.find('option')['value'])


                if 'post_images' in postdata and len(postdata['post_images']) > 0:
                    for i in range(1,7):
                        delete_image_url = str('http://www.taladx.com/post-edit.php?id='+req_post_id+'&o=photo'+str(i)+'&n='+req_post_id+'-'+str(i)+'.png')
                        delete_image = httprequestObj.http_get(delete_image_url, headers = headers)

                    for i in range(1,7):
                        delete_image_url = str('http://www.taladx.com/post-edit.php?id='+req_post_id+'&o=photo'+str(i)+'&n='+req_post_id+'-'+str(i)+'.jpg')
                        delete_image = httprequestObj.http_get(delete_image_url, headers = headers)

                    for i in range(1,7):
                        delete_image_url = str('http://www.taladx.com/post-edit.php?id='+req_post_id+'&o=photo'+str(i)+'&n='+req_post_id+'-'+str(i)+'.gif')
                        delete_image = httprequestObj.http_get(delete_image_url, headers = headers)

                    file = []
                    temp = 1


                    if len(postdata['post_images']) <= 6:
                        for i in postdata['post_images']:
                            y=str(random.randint(0,100000000000000000))+".jpg"
                            #print(y)
                            file.append((str('photo'+str(temp)), (y, open(i, "rb"), "image/jpg")))
                            temp = temp + 1

                    else:
                        for i in postdata['post_images'][:6]:
                            y=str(random.randint(0,100000000000000000))+".jpg"
                            #print(y)
                            file.append((str('photo'+str(temp)), (y, open(i, "rb"), "image/jpg")))
                            temp = temp + 1

                    post_create = httprequestObj.http_post(post_url, data = data, files = file, headers = headers)
                    success = "true"
                    detail = "Post edited successfully"

                else:
                    post_create = httprequestObj.http_post(post_url, data = data, headers = headers)
                    success = "true"
                    detail = "Post edited successfully"

            else:
                success = "false"
                detail = "post_id is incorrect"

        else :
            success = "false"
            detail = "Login failed"

        end_time = datetime.datetime.utcnow()

        return {
            "websitename": "taladx",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(end_time - start_time),
            "post_id": str(postdata['post_id']),
            "log_id": postdata['log_id'],
            "account_type": "null",
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

            post_found = "false"
            post_id = ''
            post_url = ''
            post_view = ''
            post_create_time = ''
            post_modify_time = ''
            detail = 'No post with this title'

            urls = str('http://www.taladx.com/post-search.php?keyword='+str(postdata['post_title_th']).replace('.','').replace(' ', "+")+'&category=&subcategory=&province=&price=')

            res = httprequestObj.http_get(urls, headers = headers)
            #print(res.url)

            soup = BeautifulSoup(res.content ,features = self.parser)
            # print(soup.prettify())

            soup = soup.find('div', attrs={'class': 'postlist'})
            # print(soup.prettify())
            temp = str(postdata['post_title_th']).replace('.  ', '')
            temp = temp.replace('. ', ' ').replace('.', '')
            for abc in soup.find_all('ul',attrs={'class': 'lileft'}):
                l = abc.find('li', attrs={'class' : 'title'})
                # print(f'title---{l.a.text}')
                # print(f'temp---{temp}')
                # print(f"posttitle---{postdata['post_title_th']}")


                if (str(l.a.text) == temp):
                    post_url = str(l.a['href'])
                    post_found = 'true'
                    detail = 'Post found'
                    temp_id = str(post_url.split('/')[3])
                    post_id = str(temp_id[4:])
                    find_info = httprequestObj.http_get(post_url, headers = headers).text
                    soup1 = BeautifulSoup(find_info,features = self.parser)

                    ab = soup1.find('div',attrs = {'class':'data'})

                    temp1 = 1
                    for pq in ab.find_all('p'):
                        if(temp1 == 7):
                            #post_create_time = ' '.join(map(str,))
                            post_create_time = str(pq.text[13:])
                        elif(temp1 == 8):
                            post_modify_time = str(pq.text[14:])
                        elif(temp1 == 12):
                            post_view = str(pq.text.split(' ')[-1])
                            if(post_view == ""):
                                post_view = '0'

                        temp1 = temp1 + 1

                    break





        else :
            detail = 'Can not log in'
        
        end_time = datetime.datetime.utcnow()
        
        return {
            "websitename": "taladx",
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
            "post_modify_time": post_modify_time,
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
