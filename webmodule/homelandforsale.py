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

class homelandforsale():
   
    name = 'homelandforsale'

    def __init__(self):
   
        try:
            import configs

        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.primarydomain = ''
        self.debug = 1
        self.debugresdata = 0
        self.baseurl = 'http://รับขายบ้านที่ดิน.com'
        self.parser = 'html.parser'
        self.httprequestObj = lib_httprequest()

    def logout_user(self):
        url = 'http://xn--22c0bihcbb7dg4lnac3am9zla.com/member/logout.php'
        self.httprequestObj.http_get(url)

    def register_user(self, postdata):

        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        
        start_time = datetime.datetime.utcnow()

        print('1')

        headers = {
            'user_agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36'
        }

        print('2')

        data1 = {
            'check': '1',
            'submit': 'ถัดไป | Next &gt;&gt;'
        }

        print('3')

        response = self.httprequestObj.http_post('http://รับขายบ้านที่ดิน.com/member-register.php', data = data1)
        print(response.url)
        print(response.status_code)

        soup = BeautifulSoup(response.content,features = 'html.parser')

        abc = str(soup.find('input', attrs={'name' : 'rands'})['value'])


        data = {
            'name': str(postdata['name_title'] + '. ' + postdata['name_th'] + ' ' + postdata['surname_th']),
            'add': 'พญาไท กรุงเทพ',
            'province': '1',
            'amphur': '14',
            'tel': str(postdata['tel']),
            'website': '',
            'email': str(postdata['user']),
            'pass': postdata['pass'],
            'rands': abc,
            'capcha': abc,
            'Submit': 'สมัครสมาชิก'
        }


        if data['email'] == "":
            detail = "Invalid email"
        elif data['pass'] == "":
            detail = "Invalid Password"
        elif data['name'] == "":
            detail = "Please enter your name"
        elif data['tel'] == "":
            detail = "Please enter your phone number"
        else:
            try:
                res = self.httprequestObj.http_post('http://รับขายบ้านที่ดิน.com/p-member-register.php', data = data, headers = headers)

                if 'มีอยู่ในระบบแล้วครับ' in res.text:
                    success = "false"
                    detail = "Email Already registered"

                else :
                    success = "true"
                    detail = "Registered Successfully"


            except requests.exceptions.RequestException:
                detail = "Network Problem occured"

        end_time = datetime.datetime.utcnow()

        return {
            "websitename": "homelandforsale",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(end_time - start_time),
            "ds_id" : str(postdata['ds_id']),
            "detail": detail
        }




    def test_login(self, postdata):
        self.logout_user()
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        
        start_time = datetime.datetime.utcnow()

        data = {
            'email': postdata['user'],
            'pass': postdata['pass']
        }
        
        success = "false"
        detail = ""
        
        headers = {
            'user_agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36'
        }

        if data['email'] == "":
            detail = "Invalid username"
        elif data['pass'] == "":
            detail = "Invalid Password"
        else:
            try:
                response = self.httprequestObj.http_post('http://รับขายบ้านที่ดิน.com/login.php', data = data, headers = headers)
                
                if 'ขออภัยครับ ท่านกรอก Email และ/หรือ Password ไม่ถูกต้องครับ' in response.text:
                    success = "false"
                    detail = 'Incorrect Username or Password !!'
                elif 'ขออภัยครับ ทางเว็บไซต์ยังไม่ได้ยืนยันการใช้งานระบบตัวแทนขายโครงการให้กับท่านครับ' in response.text:
                    success = "false"
                    detail = 'ทางเว็บไซต์ยังไม่ได้ยืนยันการใช้งานระบบตัวแทนขายโครงการให้กับท่าน'
                else:
                    success = "true"
                    detail = 'Logged in successfully'
                    res = self.httprequestObj.http_get('http://รับขายบ้านที่ดิน.com/member/index.php')
                    #print(res.text)
            
            except requests.exceptions.RequestException:
                detail = "Network Problem occured"

        end_time = datetime.datetime.utcnow()

        return {
            "websitename": 'homelandforsale',
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

        post_id = ''
        post_url = ''
        
        headers = {
            'user_agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36'
        }

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
                'class_type_id':'',
                'cate_id': '',
                'title': str(postdata['post_title_th'].replace("\n","<br>")),
                'project': str(postdata['web_project_name'].replace("\n","<br>")),
                'add': '-',
                'province': '64',
                'amphur': '864',
                'map_lat': str(postdata['geo_latitude']),
                'map_lng': str(postdata['geo_longitude']),
                'map_zoom': '',
                'detail': str(postdata['post_description_th'].replace("\n","<br>")),
                'area': '',
                'bedroom': '',
                'bathroom': '',
                'floors': '',
                'price': str(postdata['price_baht']),
                'name': str(postdata['name']),
                'tel': str(postdata['mobile']),
                'email': str(postdata['email']),
                'website': '',
                'rands': '',
                'capcha': '',
                'submit': 'ดำเนินการต่อ &gt;&gt;'
            }
            #print(data['detail']) 

            #print('abcdef')

            #print(str(postdata['post_description_th'].replace("\n","<br>")))

            if postdata['listing_type'] == 'เช่า':
                data['class_type_id'] = '2'
            else:
                data['class_type_id'] = '1'


            pd_properties = {
                '1': '4',
                '2': '2',
                '3': '3',
                '4': '3',
                '5': '6',
                '6': '1',
                '7': '5',
                '8': '7',
                '9': '8',
                '10': '9',
                '25': '9' 
            }

            data['cate_id'] = pd_properties[str(postdata['property_type'])]

            if (data['cate_id'] == '4'):
                data['area'] = str(str(postdata['floor_area']) + 'ตรม.')
                data['bedroom'] = str(postdata['bed_room'])
                data['bathroom'] = str(postdata['bath_room'])
                data['floors'] = str(postdata['floor_level'])

            else:
                if(postdata['land_size_rai'] == "" or postdata['land_size_rai'] == "null" or 'land_size_rai' not in postdata or postdata['land_size_rai'] == None):
                    postdata['land_size_rai'] = 0

                if(postdata['land_size_ngan'] == "" or postdata['land_size_ngan'] == "null" or 'land_size_ngan' not in postdata or postdata['land_size_ngan'] == None):
                    postdata['land_size_ngan'] = 0

                if(postdata['land_size_wa'] == "" or postdata['land_size_wa'] == "null" or 'land_size_wa' not in postdata or postdata['land_size_wa'] == None):
                    postdata['land_size_wa'] = 0

                #print(postdata['land_size_rai'])


                data['area'] = str(str(float(postdata['land_size_rai'])*400 + float(postdata['land_size_ngan'])*100 + float(postdata['land_size_wa'])) + 'ตรว.')
                data['bedroom'] = str(postdata['bed_room'])
                data['bathroom'] = str(postdata['bath_room'])
                data['floors'] = str(postdata['floor_total'])

            province = ''.join(map(str,str(postdata['addr_province']).split(' ')))

            find_province = self.httprequestObj.http_get('https://www.xn--22c0bihcc9cwhcxj2ui.com/post', headers = headers).text

            soup = BeautifulSoup(find_province,features = "html.parser")

            abc = soup.find('select',{'name':'province'})

            for pq in abc.find_all('option'):
                if(str(pq.text) in str(province) or str(province) in str(pq.text)):
                    data['province'] = str(pq['value'])
                    break

            district = ''.join(map(str,str(postdata['addr_district']).split(' ')))

            url_district = str('https://www.xn--22c0bihcc9cwhcxj2ui.com/data_for_list3.php?province='+data['province'])

            find_district = self.httprequestObj.http_get(url_district, headers = headers).text
            #print(find_district)

            soup = BeautifulSoup(find_district,features = "html.parser")

            #data['amphur'] = '-1'

            
            try:
                for pqr in soup.find_all('option'):
                    if(str(pqr.text) in str(district) or str(district) in str(pqr.text)):
                        data['amphur'] = str(pqr['value'])
                        break

            except:
                data['amphur'] = str(soup.find('option')['value'])


            respo = self.httprequestObj.http_get('http://รับขายบ้านที่ดิน.com/member/post-property.php', headers = headers)
        

            soup = BeautifulSoup(respo.content,features = 'html.parser')

            abc = str(soup.find('input', attrs={'name' : 'rands'})['value'])

            data['rands'] = abc
            data['capcha'] = abc



            if 'post_images' in postdata and len(postdata['post_images']) > 0:
                pass
            else:
                postdata['post_images'] = ['./imgtmp/default/white.jpg']


            file = []
            temp = 1

            first_image = postdata["post_images"][0]
            
            y=str(random.randint(0,100000000000000000))+".jpg"
            file.append(('fileshow', (y, open(first_image, "rb"), "image/jpg")))

            if len(postdata['post_images']) <= 5 and len(postdata['post_images']) >=2:
                for i in postdata['post_images'][1:]:
                    y=str(random.randint(0,100000000000000000))+".jpg"
                    #print(y)
                    file.append((str('file'+str(temp)), (y, open(i, "rb"), "image/jpg")))
                    temp = temp + 1

            else:
                for i in postdata['post_images'][1:5]:
                    y=str(random.randint(0,100000000000000000))+".jpg"
                    #print(y)
                    file.append((str('file'+str(temp)), (y, open(i, "rb"), "image/jpg")))
                    temp = temp + 1

            crt_post = self.httprequestObj.http_post('http://รับขายบ้านที่ดิน.com/member/p-post-property.php', data = data, files = file, headers = headers)
            #print(crt_post.text)

            soup = BeautifulSoup(crt_post.content, features = "html.parser")

            abc = soup.find('meta',attrs = {'http-equiv':'refresh'})
            post_id = str((abc['content'])[39:])

            r = self.httprequestObj.http_get('http://xn--22c0bihcbb7dg4lnac3am9zla.com/member/list-property.php')
            soup = BeautifulSoup(r.content, features = "html.parser")
            for a in soup.find_all('a', href=True):
               if post_id in a['href']:
                   post_url = 'http://รับขายบ้านที่ดิน.com{}'.format((a['href'])[2:])
                   break

            sec_step_url = str('http://รับขายบ้านที่ดิน.com/member/real-estate-features.php?post_id='+post_id)

            sec_step = self.httprequestObj.http_get(sec_step_url, headers = headers)

            success = "true"
            detail = "Post created successfully"
        else:
            success = "false"
            detail = "Can not log in"
            
        end_time = datetime.datetime.utcnow()
        
        return {
            "websitename": "homelandforsale",
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






    def boost_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()
        
        headers = {
            'user_agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36'
        }

        login = self.test_login(postdata)

        if(login['success'] == "true"):

            req_post_id = str(postdata['post_id'])

            boost_url = str('http://รับขายบ้านที่ดิน.com/member/slide-property.php?post_id='+req_post_id)

            boo_post = self.httprequestObj.http_get(boost_url, headers = headers)

            #print(boo_post.text)

            if 'ขอโทษครับ คุณได้เลื่อนประกาศนี้ในวันนี้แล้วครับ' in boo_post.text:
                success = "false"
                detail = "This announcement was postponed today, so cannot be postponed now"

            else:
                success = "true"
                detail = "Announcement postponed successfully"


        else :
            success = "false"
            detail = "Login failed"

        end_time = datetime.datetime.utcnow()
        
        return {
            "websitename": "homelandforsale",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(end_time - start_time),
            "detail": detail,
            "ds_id" : str(postdata['ds_id']),
            "post_id": str(postdata['post_id']),
            "log_id": postdata['log_id']
        }







    def delete_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()
        
        headers = {
            'user_agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36'
        }

        login = self.test_login(postdata)
        
        if(login['success'] == "true"):

            all_posts_url = 'http://รับขายบ้านที่ดิน.com/member/list-property.php'

            all_posts = self.httprequestObj.http_get(all_posts_url, headers = headers)

            soup = BeautifulSoup(all_posts.content, features = "html")

            pages=len(soup.find("div",attrs={"class":"text-center"}).find_all("a"))

            all_post_ids = []

            for i in range(pages):
                url="http://xn--22c0bihcbb7dg4lnac3am9zla.com/member/list-property.php?QueryString=value&Page="+str(i+1)
                posts=self.httprequestObj.http_get(url, headers = headers)
                soup = BeautifulSoup(posts.text,"html5lib")

                for abc in soup.find_all('input', attrs = {'name':'chkDel[]'}):
                    all_post_ids.append(str(abc['value']))

            #print(all_post_ids)

            req_post_id = str(postdata['post_id'])

            if req_post_id in all_post_ids:
                data = {
                    'chkDel[]' : req_post_id,
                    'type' : '2',
                    'Submit' : 'ดำเนินการ',
                    'hdnCount' : str(len(all_post_ids))
                }

                delete_post = self.httprequestObj.http_post('http://รับขายบ้านที่ดิน.com/member/manage-property-not-sale.php', data = data, headers = headers)

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
            "websitename": "homelandforsale",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(end_time - start_time),
            "detail": detail,
            "ds_id" : str(postdata['ds_id']),
            "post_id": str(postdata['post_id']),
            "log_id": postdata['log_id']
        }







    def edit_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        
        start_time = datetime.datetime.utcnow()
        
        headers = {
            'user_agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36'
        }

        login = self.test_login(postdata)
        
        if (login['success'] == 'true'):

            """all_posts_url = 'http://รับขายบ้านที่ดิน.com/member/list-property.php'

            all_posts = self.httprequestObj.http_get(all_posts_url, headers = headers)

            soup = BeautifulSoup(all_posts.content, self.parser)
            #soup = BeautifulSoup(all_posts.content, features = "html")

            pages=len(soup.find("div",attrs={"class":"text-center"}).find_all("a"))

            all_post_ids = []

            for i in range(pages):
                url="http://xn--22c0bihcbb7dg4lnac3am9zla.com/member/list-property.php?QueryString=value&Page="+str(i+1)
                posts=self.httprequestObj.http_get(url, headers = headers)
                soup = BeautifulSoup(posts.text,"html5lib")

                for abc in soup.find_all('input', attrs = {'name':'chkDel[]'}):
                    all_post_ids.append(str(abc['value']))"""


            req_post_id = str(postdata['post_id'])
            all_post_ids = [req_post_id]
            if req_post_id in all_post_ids:

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
                    'post_id': req_post_id,
                    'class_type_id':'',
                    'cate_id': '',
                    'status': '1',
                    'title': str(postdata['post_title_th'].replace("\n","<br>")),
                    'project': str(postdata['web_project_name'].replace("\n","<br>")),
                    'add': '-',
                    'province': '64',
                    'amphur': '864',
                    'map_lat': str(postdata['geo_latitude']),
                    'map_lng': str(postdata['geo_longitude']),
                    'map_zoom': '',
                    'detail': str(postdata['post_description_th'].replace("\n","<br>")),
                    'area': '',
                    'bedroom': '',
                    'bathroom': '',
                    'floors': '',
                    'price': str(postdata['price_baht']),
                    'name': str(postdata['name']),
                    'tel': str(postdata['mobile']),
                    'email': str(postdata['email']),
                    'website': '',
                    'submit': 'ดำเนินการต่อ &gt;&gt;'
                }


                if postdata['listing_type'] == 'เช่า':
                    data['class_type_id'] = '2'
                else:
                    data['class_type_id'] = '1'


                pd_properties = {
                    '1': '4',
                    '2': '2',
                    '3': '3',
                    '4': '3',
                    '5': '6',
                    '6': '1',
                    '7': '5',
                    '8': '7',
                    '9': '8',
                    '10': '9',
                    '25': '9' 
                }

                data['cate_id'] = pd_properties[str(postdata['property_type'])]

                if (data['cate_id'] == '4'):
                    data['area'] = str(str(postdata['floor_area']) + 'ตรม.')
                    data['bedroom'] = str(postdata['bed_room'])
                    data['bathroom'] = str(postdata['bath_room'])
                    data['floors'] = str(postdata['floor_level'])

                else:
                    if(postdata['land_size_rai'] == "" or postdata['land_size_rai'] == "null" or 'land_size_rai' not in postdata or postdata['land_size_rai'] == None):
                        postdata['land_size_rai'] = 0

                    if(postdata['land_size_ngan'] == "" or postdata['land_size_ngan'] == "null" or 'land_size_ngan' not in postdata or postdata['land_size_ngan'] == None):
                        postdata['land_size_ngan'] = 0

                    if(postdata['land_size_wa'] == "" or postdata['land_size_wa'] == "null" or 'land_size_wa' not in postdata or postdata['land_size_wa'] == None):
                        postdata['land_size_wa'] = 0

                    #print(postdata['land_size_rai'])


                    data['area'] = str(str(float(postdata['land_size_rai'])*400 + float(postdata['land_size_ngan'])*100 + float(postdata['land_size_wa'])) + 'ตรว.')
                    data['bedroom'] = str(postdata['bed_room'])
                    data['bathroom'] = str(postdata['bath_room'])
                    data['floors'] = str(postdata['floor_total'])


                province = ''.join(map(str,str(postdata['addr_province']).split(' ')))

                pro_url = str('http://รับขายบ้านที่ดิน.com/member/edit-property.php?post_id='+req_post_id)

                find_province = self.httprequestObj.http_get(pro_url, headers = headers).text

                soup = BeautifulSoup(find_province,self.parser)

                abc = soup.find('select',attrs = {'name':'province'})

                for pq in abc.find_all('option'):
                    if(str(pq.text) in str(province) or str(province) in str(pq.text)):
                        data['province'] = str(pq['value'])
                        break


                district = ''.join(map(str,str(postdata['addr_district']).split(' ')))

                url_district = str('http://รับขายบ้านที่ดิน.com/data_for_list3.php?province='+data['province'])

                find_district = self.httprequestObj.http_get(url_district, headers = headers).text

                soup = BeautifulSoup(find_district,self.parser)

                try:

                    for pqr in soup.find_all('option'):
                        if(str(pqr.text) in str(district) or str(district) in str(pqr.text)):
                            data['amphur'] = str(pqr['value'])
                            break

                except:
                    data['amphur'] = str(soup.find('option')['value'])

                if 'post_images' in postdata and len(postdata['post_images']) > 0:

                    file = []
                    temp = 1

                    first_image = postdata["post_images"][0]
                    
                    y=str(random.randint(0,100000000000000000))+".jpg"
                    file.append(('fileshow', (y, open(first_image, "rb"), "image/jpg")))

                    if len(postdata['post_images']) <= 5 and len(postdata['post_images']) >=2:
                        for i in postdata['post_images'][1:]:
                            y=str(random.randint(0,100000000000000000))+".jpg"
                            #print(y)
                            file.append((str('file'+str(temp)), (y, open(i, "rb"), "image/jpg")))
                            temp = temp + 1

                    else:
                        for i in postdata['post_images'][1:5]:
                            y=str(random.randint(0,100000000000000000))+".jpg"
                            #print(y)
                            file.append((str('file'+str(temp)), (y, open(i, "rb"), "image/jpg")))
                            temp = temp + 1


                    edit_post_url = str('http://รับขายบ้านที่ดิน.com/member/p-edit-property.php')

                    edit_post = self.httprequestObj.http_post(edit_post_url, data = data, files = file, headers = headers)

                    success = "true"
                    detail = "Post edited successfully"


                else:
                    edit_post_url = str('http://รับขายบ้านที่ดิน.com/member/p-edit-property.php')

                    edit_post = self.httprequestObj.http_post(edit_post_url, data = data, headers = headers)

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
            "websitename": "homelandforsale",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(end_time - start_time),
            "log_id": postdata['log_id'],
            "account_type": "null",
            "ds_id" : str(postdata['ds_id']),
            "post_id": str(postdata['post_id']),
            "detail": detail
        }







    def search_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        
        start_time = datetime.datetime.utcnow()
        
        headers = {
            'user_agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36'
        }

        login = self.test_login(postdata)
        
        if (login['success'] == 'true'):

            post_found = "false"
            post_id = ''
            post_url = ''
            post_view = ''
            post_create_time = ''
            post_modify_time = ''
            detail = 'No post with this title'

            req_post_title = str(postdata['post_title_th'])

            all_posts_url = 'http://รับขายบ้านที่ดิน.com/member/list-property.php'

            all_posts = self.httprequestObj.http_get(all_posts_url, headers = headers)

            soup = BeautifulSoup(all_posts.content, features = "html")

            pages = len(soup.find("div", attrs={"class": "text-center"}).find_all("a"))

            for i in range(pages):
                url="http://xn--22c0bihcbb7dg4lnac3am9zla.com/member/list-property.php?QueryString=value&Page="+str(i+1)
                posts=self.httprequestObj.http_get(url, headers = headers)
                soup = BeautifulSoup(posts.text,"html5lib")

                xyz = soup.find('table', attrs={'class':'table table-hover'})

                for abc in xyz.find_all('tr')[1:-1]:

                    if req_post_title in str(abc.find('a', attrs = {'target':'_blank'})['title']):
                        post_id = str(abc.input['value'])
                        post_url = str('http://รับขายบ้านที่ดิน.com/property-'+str(post_id)+'/.html')
                        post_found = "true"
                        post_modify_time = abc.span.text[13:]
                        detail = "Post found"

                        find_info = self.httprequestObj.http_get(post_url, headers = headers)

                        sou = BeautifulSoup(find_info.content, features = "html")

                        pqr = sou.find('div', attrs = {'class': 'news-time'}).text.split(' ')

                        post_create_time = str(str(pqr[1]) +' '+ str(pqr[2]) +' '+ str(pqr[3]))

                        post_view = str(pqr[-3])
                        if(post_view == ""):
                            post_view = '0'

                        break

                if post_found=="true":
                    break
            

        else :
            detail = 'Can not log in'
        
        end_time = datetime.datetime.utcnow()
        
        return {
            "websitename": "homelandforsale",
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