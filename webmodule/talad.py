# -*- coding: utf-8 -*-

import requests, re, random
from bs4 import BeautifulSoup
import json, datetime
from .lib_httprequest import *
from .lib_captcha import  *
import datetime
import time,math
import lxml
from lxml.html.soupparser import fromstring

class talad:

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

    def register_user(self, data):
        req = self.httprequestObj.http_get('http://talad.me/user/logout')

        start_time = datetime.datetime.utcnow()

        success = 'false'
        detail = ''

        postdata = {
            'email': data['user'],
            'displayname': data['name_th'],
            'password': data['pass'],
            'confirm_password': data['pass'],
            'captcha': ''
        }

        url = 'http://talad.me/user/register'

        headers = {
        	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        }

        f1 = True
        regex = '^\\w+([\\.-]?\\w+)*@\\w+([\\.-]?\\w+)*$'

        if re.search(regex, postdata['email']):
            f1 = True
        else:
            f1 = False

        if len(data['pass']) <= 6:
            success = 'false'
            detail = 'Password length should be greater than 6'
        elif f1 == False:
            success = 'false'
            detail = 'Invalid email id'
        else:
            url = 'http://talad.me/user/register'
            req = self.httprequestObj.http_get(url,headers=headers)
            soup = BeautifulSoup(req.text,'html.parser')

            url = soup.find('div',{'class':'controls'}).find('img')['src']
            response = self.httprequestObj.http_get(url)
            file = open('tmp.jpeg', 'wb')
            file.write(response.content)
            file.close()

            captcha_solver = lib_captcha()

            result = captcha_solver.imageCaptcha('tmp.jpeg')

            if result[0] == 1:
                captcha_code = result[1]
                postdata['captcha'] = captcha_code

                url = 'http://talad.me/user/register'
                req = self.httprequestObj.http_post(url,data=postdata,headers=headers)
                txt = str(req.text)

                if txt.find('อีเมลล์นี้มีอยู่ในระบบแล้ว')!=-1:
                    success = 'false'
                    detail = 'User already exists'
                elif txt.find('CAPTCHA') != -1 :
                    success = 'false'
                    detail = 'CAPTCHA error'
                else:
                    success = 'true'
                    detail = 'Successfully registered'
            else:
                success = 'false'
                detail = 'Problem with captcha'

        end_time = datetime.datetime.utcnow()
        result = {'websitename':'talad',
            'success':success,
            'start_time':str(start_time),
            'end_time':str(end_time),
            'usage_time':str(end_time - start_time),
            'detail':detail,
            'ds_id':data['ds_id']
        }

        return result

    def test_login(self, data):
        req = self.httprequestObj.http_get('http://talad.me/user/logout')

        start_time = datetime.datetime.utcnow()

        success = 'false'
        detail = ''

        postdata = {
        	'email':data['user'],
        	'password':data['pass']
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        }

        url = 'http://talad.me/user/login'
        
        req = self.httprequestObj.http_post(url,data=postdata,headers=headers)
        txt = req.text
        if txt.find('ไม่สามารถเข้าสู่ระบบได้, โปรดตรวจสอบอีเมล์และรหัสผ่านอีกครั้ง') == -1:
            success = 'true'
            detail = 'Login Successful'
        else:
            success = 'false'
            detail = 'Invalid credentials'

        end_time = datetime.datetime.utcnow()

        result = {'websitename':'talad',
            'success':success,
            'start_time':str(start_time),
            'end_time':str(end_time),
            'usage_time':str(end_time - start_time),
            'ds_id':data['ds_id'],
            'detail':detail
        }

        return result

    def create_post(self, data):
        start_time = datetime.datetime.utcnow()
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        }
        result = self.test_login(data)
        success = result['success']
        detail = result['detail']
        post_url = ''
        post_id = ''
        if success == 'true':

            postdata = {}
            postdata['title'] = data['post_title_th']
            ids = {'คอนโด': '1',
                   'บ้านเดี่ยว': '2',
                   'บ้านแฝด': '3',
                   'ทาวน์เฮ้าส์': '4',
                   'ตึกแถว-อาคารพาณิชย์': '5',
                   'ที่ดิน': '6',
                   'อพาร์ทเมนท์': '7',
                   'โรงแรม': '8',
                   'ออฟฟิศสำนักงาน': '9',
                   'โกดัง-โรงงาน': '10',
                   'โรงงาน': '25'}
            property_tp = {'1': '23,208',
                           '2': '23,205',
                           '3': '23,205',
                           '4': '23,206',
                           '5': '23,207',
                           '6': '23,210',
                           '7': '23,209',
                           '8': '23,211',
                           '9': '23,211',
                           '10': '23,211',
                           '25': '23,211'}
            if str(data['property_type']) in property_tp:
                postdata['category'] = property_tp[str(data['property_type'])]
            else:
                postdata['category'] = property_tp[ids[str(data['property_type'])]]

            postdata['price'] = data['price_baht']
            #postdata['files[]'] = ''
            #postdata['mobile_upload[]'] = ''
            postdata['detail'] = str(data['post_description_th'])
            postdata['province'] = ''
            postdata['district'] = ''
            #print(data['addr_province'],data['addr_district'])
            url = 'http://talad.me/post'
            req = self.httprequestObj.http_get(url,headers=headers)
            soup = BeautifulSoup(req.text,'html.parser')
            options = soup.find('select',{'name':'province'}).findAll('option')
            #print(options)
            provinces = []
            prov_id = []
            count = 0
            for opt in options:
                if count>0:
                    #print(opt.text)
                    #print(opt['value'])
                    provinces.append(str(opt.text))
                    prov_id.append(str(opt['value']))
                count+=1
            for i in range(len(provinces)):
                if provinces[i].find(str(data['addr_province']))!=-1:
                    postdata['province'] = prov_id[i]
            if postdata['province'] == '':
                postdata['province'] = prov_id[0]

            with open('./static/talad_province.json') as data1_file:
                prov_data = json.load(data1_file)
            #print('loaded')
            districts = prov_data[postdata['province']]
            #print(districts)
            for i in range(len(districts)):
                dist = districts[i]['text']
                #dist = dist.encode().decode("unicode-escape")
                #print('here',dist)
                if str(dist).find(str(data['addr_district']))!=-1:
                    postdata['district'] = str(districts[i]['id'])
                    break
            if postdata['district'] == '':
                postdata['district'] = str(districts[0]['id'])


            if 'addr_postcode' not in data or data['addr_postcode'] is None:
                data['addr_postcode'] = '-'
            postdata['postcode'] = data['addr_postcode']
            postdata['phone'] = data['mobile']
            # images
            if 'post_images' in data and len(data['post_images']) > 0:
                pass
            else:
                data['post_images'] = ['./imgtmp/default/white.jpg']

            file = []
            files = {}
            temp = 1
            postdata['uploadpic[]'] = []

            if len(data['post_images']) <= 8:
                for i in data['post_images']:
                    #y = str(random.randint(0, 100000000000000000)) + ".jpg"

                    r = open(os.getcwd() + '/' + i, 'rb')
                    files['files[]'] = r
                    response = self.httprequestObj.http_post('http://talad.me/upload', data=postdata,
                                                        files=files)

                    y = ''
                    txt = response.text
                    ind = txt.find('file_name')+12
                    while txt[ind]!='"':
                        y+=txt[ind]
                        ind+=1
                    #print(y)
                    postdata['uploadpic[]'].append(y)

                    file.append((str('uploadpic[]'), (y, open(i, "rb"), "image/jpg")))
                    temp = temp + 1

            else:
                for i in data['post_images'][:8]:
                    #y = str(random.randint(0, 100000000000000000)) + ".jpg"

                    r = open(os.getcwd() + '/' + i, 'rb')
                    files['files[]'] = r
                    response = self.httprequestObj.http_post('http://talad.me/upload', data=postdata,
                                                        files=files)

                    y = ''
                    txt = response.text
                    ind = txt.find('file_name') + 12
                    while txt[ind] != '"':
                        y += txt[ind]
                        ind += 1
                    #print(y)
                    postdata['uploadpic[]'].append(y)

                    file.append((str('uploadpic[]'), (y, open(i, "rb"), "image/jpg")))
                    temp = temp + 1

            url = 'http://talad.me/post'

            req = self.httprequestObj.http_post(url,data=postdata,files=file,headers=headers)

            soup = BeautifulSoup(req.text,'html5lib')
            try:
                url = str(soup.find('form')['action'])
                ind = url.find('success')+8
                while url[ind]!='?':
                    post_id+=url[ind]
                    ind+=1
            except:
                success = 'false'
                detail = 'Something wrong happened'
                end_time = datetime.datetime.utcnow()
                result = {'success': success,
                          'usage_time': str(end_time - start_time),
                          'start_time': str(start_time),
                          'end_time': str(end_time),
                          'post_url': post_url,
                          'post_id': post_id,
                          'account_type': 'null',
                          'ds_id': data['ds_id'],
                          'detail': detail,
                          'websitename': 'talad'}
                return result
            if post_id == '':
                success = 'false'
                detail = 'Something wrong happened'
            else:
                success = 'true'
                detail = 'Post created successfully'
                #data['post_title_th'] = (data['post_title_th']).encode().decode("unicode-escape")
                #print((data['post_title_th']).decode('utf-8'))
                #print(data['post_title_th'])
                post_url = 'http://talad.me/detail/'+str(post_id)

        end_time = datetime.datetime.utcnow()
        result = {'success': success,
                  'usage_time': str(end_time - start_time),
                  'start_time': str(start_time),
                  'end_time': str(end_time),
                  'post_url': post_url,
                  'post_id': post_id,
                  'account_type': 'null',
                  'ds_id': data['ds_id'],
                  'detail': detail,
                  'websitename': 'talad'}
        return result

    def delete_post(self, data):
        ##print('in')
        test_login = self.test_login(data)
        success = test_login["success"]
        start_time = datetime.datetime.utcnow()
        end_time = datetime.datetime.utcnow()
        post_id = str(data["post_id"])
        detail = test_login["detail"]

        if success == "true":
            url = 'http://talad.me/user/post'
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
            }
            req = self.httprequestObj.http_get(url,headers=headers)
            valid_ids = []
            soup = BeautifulSoup(req.text,'html5lib')
            total_pages = int(soup.find('span',{'class':'badge'}).text)
            total_pages = int(math.ceil(total_pages/12))
            for i in range(total_pages):
                url = 'http://talad.me/user/post?page='+str(i+1)
                req = self.httprequestObj.http_get(url, headers=headers)

                soup = BeautifulSoup(req.text, 'html5lib')

                posts = soup.find('tbody').findAll('tr')
                for post in posts:
                    url = str(post.find('a')['href'])
                    ind = url.find('detail')+7
                    id = ''
                    while url[ind]!='-':
                        id+=url[ind]
                        ind+=1
                    valid_ids.append(id)

            #print(valid_ids)
            if post_id in valid_ids:
                url = 'http://talad.me/user/post/?action=delete&id='+str(post_id)
                req = self.httprequestObj.http_get(url,headers=headers)
                success = 'true'
                detail = 'Post deleted'
            else:
                success = 'false'
                detail = 'Post not found'

        end_time = datetime.datetime.utcnow()
        result = {
            "success": success,
            "usage_time": str(end_time - start_time),
            "start_time": str(start_time),
            "end_time": str(end_time),
            "log_id": data['log_id'],
            'ds_id': data['ds_id'],
            "post_id": data['post_id'],
            "detail": detail,
            "websitename": "talad"
        }
        return result

    def search_post(self, data):
        ##print('in')
        test_login = self.test_login(data)
        success = test_login["success"]
        start_time = datetime.datetime.utcnow()
        end_time = datetime.datetime.utcnow()
        post_title = str(data["post_title_th"])
        detail = test_login["detail"]
        post_id = ''
        post_url = ''
        post_found = ''

        if success == "true":
            url = 'http://talad.me/user/post'
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
            }
            req = self.httprequestObj.http_get(url,headers=headers)
            valid_ids = []
            valid_titles = []
            valid_urls = []
            soup = BeautifulSoup(req.text,'html5lib')
            total_pages = int(soup.find('span',{'class':'badge'}).text)
            total_pages = int(math.ceil(total_pages/12))
            for i in range(total_pages):
                url = 'http://talad.me/user/post?page='+str(i+1)
                req = self.httprequestObj.http_get(url, headers=headers)

                soup = BeautifulSoup(req.text, 'html5lib')

                posts = soup.find('tbody').findAll('tr')
                for post in posts:
                    url = str(post.find('a')['href'])
                    ind = url.find('detail')+7
                    id = ''
                    while url[ind]!='-':
                        id+=url[ind]
                        ind+=1
                    valid_ids.append(id)
                    urls = post.findAll('a')
                    valid_titles.append(str(urls[1].text).strip())
                    valid_urls.append(urls[0]['href'])

            #print(valid_ids)
            #print(valid_urls)
            #print(valid_titles)
            if post_title in valid_titles:
                for i in range(len(valid_titles)):
                    if valid_titles[i] == post_title:
                        post_id = valid_ids[i]
                        post_url = valid_urls[i]
                        break
                post_found = 'true'
                detail = 'Post found'
            else:
                post_found = 'false'
                detail = 'Post not found'
                post_title = ''
                success = 'false'

        end_time = datetime.datetime.utcnow()
        result = {
            "success": success,
            "usage_time": str(end_time - start_time),
            "start_time": str(start_time),
            "end_time": str(end_time),
            "detail": detail,
            'ds_id': data['ds_id'],
            "log_id": data['log_id'],
            "post_found": post_found,
            "post_id": post_id,
            'post_url': post_url,
            "post_create_time": '',
            "post_modify_time": '',
            "post_view": '',
            'websitename': 'talad',
            'post_title_th': post_title
        }
        return result

    def boost_post(self, data):
        start_time = datetime.datetime.utcnow()
        # #print('start')
        post_id = str(data['post_id'])
        log_id = str(data['log_id'])
        result = self.test_login(data)
        success = result['success']
        detail = result['detail']

        if success == 'true':
            url = 'http://talad.me/user/post'
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
            }
            """req = self.httprequestObj.http_get(url, headers=headers)
            valid_ids = []
            soup = BeautifulSoup(req.text, 'html5lib')
            total_pages = int(soup.find('span', {'class': 'badge'}).text)
            total_pages = int(math.ceil(total_pages / 12))
            for i in range(total_pages):
                url = 'http://talad.me/user/post?page=' + str(i + 1)
                req = self.httprequestObj.http_get(url, headers=headers)

                soup = BeautifulSoup(req.text, 'html5lib')

                posts = soup.find('tbody').findAll('tr')
                for post in posts:
                    url = str(post.find('a')['href'])
                    ind = url.find('detail') + 7
                    id = ''
                    while url[ind] != '-':
                        id += url[ind]
                        ind += 1
                    valid_ids.append(id)"""

            #print(valid_ids)
            try:

                url = 'http://talad.me/user/post/?action=renew&id='+str(post_id)
                req = self.httprequestObj.http_get(url,headers=headers)
                success = 'true'
                detail = 'Post edited and saved'

            except:
                success = 'false'
                detail = 'Post not found'

        end_time = datetime.datetime.utcnow()
        result = {
            "success": success,
            "usage_time": str(end_time - start_time),
            "start_time": str(start_time),
            "end_time": str(end_time),
            "detail": detail,
            'ds_id': data['ds_id'],
            "log_id": log_id,
            "post_id": post_id,
            'websitename': 'talad'
        }
        # https://ilovecondo.net/new-post/topicid/910653/trk/78
        return result

    def edit_post(self, data):
        start_time = datetime.datetime.utcnow()
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        }
        result = self.test_login(data)
        success = result['success']
        detail = result['detail']
        post_url = ''
        post_id = str(data['post_id'])
        if success == 'true':
            url = 'http://talad.me/user/post'
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
            }
            req = self.httprequestObj.http_get(url, headers=headers)
            valid_ids = []
            soup = BeautifulSoup(req.text, 'html5lib')
            total_pages = int(soup.find('span', {'class': 'badge'}).text)
            total_pages = int(math.ceil(total_pages / 12))
            for i in range(total_pages):
                url = 'http://talad.me/user/post?page=' + str(i + 1)
                req = self.httprequestObj.http_get(url, headers=headers)

                soup = BeautifulSoup(req.text, 'html5lib')

                posts = soup.find('tbody').findAll('tr')
                for post in posts:
                    url = str(post.find('a')['href'])
                    ind = url.find('detail') + 7
                    id = ''
                    while url[ind] != '-':
                        id += url[ind]
                        ind += 1
                    valid_ids.append(id)
            if post_id in valid_ids:
                postdata = {}
                postdata['line_id'] = ''
                postdata['website'] = ''
                postdata['product_status'] = '1'
                postdata['title'] = data['post_title_th']
                ids = {'คอนโด': '1',
                       'บ้านเดี่ยว': '2',
                       'บ้านแฝด': '3',
                       'ทาวน์เฮ้าส์': '4',
                       'ตึกแถว-อาคารพาณิชย์': '5',
                       'ที่ดิน': '6',
                       'อพาร์ทเมนท์': '7',
                       'โรงแรม': '8',
                       'ออฟฟิศสำนักงาน': '9',
                       'โกดัง-โรงงาน': '10',
                       'โรงงาน': '25'}
                property_tp = {'1': '23,208',
                               '2': '23,205',
                               '3': '23,205',
                               '4': '23,206',
                               '5': '23,207',
                               '6': '23,210',
                               '7': '23,209',
                               '8': '23,211',
                               '9': '23,211',
                               '10': '23,211',
                               '25': '23,211'}
                if str(data['property_type']) in property_tp:
                    postdata['category'] = property_tp[str(data['property_type'])]
                else:
                    postdata['category'] = property_tp[ids[str(data['property_type'])]]

                postdata['price'] = data['price_baht']
                # postdata['files[]'] = ''
                # postdata['mobile_upload[]'] = ''
                postdata['detail'] = str(data['post_description_th'])
                postdata['province'] = ''
                postdata['district'] = ''
                # print(data['addr_province'],data['addr_district'])
                url = 'http://talad.me/post/edit/'+str(post_id)
                req = self.httprequestObj.http_get(url, headers=headers)
                soup = BeautifulSoup(req.text, 'html.parser')
                options = soup.find('select', {'name': 'province'}).findAll('option')
                # print(options)
                provinces = []
                prov_id = []
                count = 0
                for opt in options:
                    if count > 0:
                        # print(opt.text)
                        # print(opt['value'])
                        provinces.append(str(opt.text))
                        prov_id.append(str(opt['value']))
                    count += 1
                for i in range(len(provinces)):
                    if provinces[i].find(str(data['addr_province'])) != -1:
                        postdata['province'] = prov_id[i]
                if postdata['province'] == '':
                    postdata['province'] = prov_id[0]

                with open('./static/talad_province.json') as data1_file:
                    prov_data = json.load(data1_file)
                #print('loaded')
                districts = prov_data[postdata['province']]
                #print(districts)
                for i in range(len(districts)):
                    dist = districts[i]['text']
                    # dist = dist.encode().decode("unicode-escape")
                    #print('here', dist)
                    if str(dist).find(str(data['addr_district'])) != -1:
                        postdata['district'] = str(districts[i]['id'])
                        break
                if postdata['district'] == '':
                    postdata['district'] = str(districts[0]['id'])

                if 'addr_postcode' not in data or data['addr_postcode'] is None:
                    data['addr_postcode'] = '-'
                postdata['postcode'] = data['addr_postcode']
                postdata['phone'] = data['mobile']

                # remove previous images
                url = 'http://talad.me/post/edit/'+str(post_id)
                req = self.httprequestObj.http_get(url,headers=headers)
                soup = BeautifulSoup(req.text,'html5lib')
                del_images = soup.find('div',{'class':'row fileupload-buttonbar'}).findAll('div',{'class':'col-sm-3 col-md-3 col-xs-6'})[:-1]
                for img in del_images:
                    url = 'http://talad.me/upload/del_pic'
                    #print(img['id'])
                    imgdata = {
                        'pic':str(img['id'])[4:]
                    }
                    #print(imgdata['pic'])
                    req = self.httprequestObj.http_post(url,data=imgdata,headers=headers)



                # images
                if 'post_images' in data and len(data['post_images']) > 0:
                    pass
                else:
                    data['post_images'] = ['./imgtmp/default/white.jpg']

                file = []
                files = {}
                temp = 1
                postdata['uploadpic[]'] = []

                if len(data['post_images']) <= 8:
                    for i in data['post_images']:
                        # y = str(random.randint(0, 100000000000000000)) + ".jpg"

                        r = open(os.getcwd() + '/' + i, 'rb')
                        files['files[]'] = r
                        response = self.httprequestObj.http_post('http://talad.me/upload', data=postdata,
                                                            files=files)

                        y = ''
                        txt = response.text
                        ind = txt.find('file_name') + 12
                        while txt[ind] != '"':
                            y += txt[ind]
                            ind += 1
                        #print(y)
                        postdata['uploadpic[]'].append(y)

                        file.append((str('uploadpic[]'), (y, open(i, "rb"), "image/jpg")))
                        temp = temp + 1

                else:
                    for i in data['post_images'][:8]:
                        # y = str(random.randint(0, 100000000000000000)) + ".jpg"

                        r = open(os.getcwd() + '/' + i, 'rb')
                        files['files[]'] = r
                        response = self.httprequestObj.http_post('http://talad.me/upload', data=postdata,
                                                            files=files)

                        y = ''
                        txt = response.text
                        ind = txt.find('file_name') + 12
                        while txt[ind] != '"':
                            y += txt[ind]
                            ind += 1
                        #print(y)
                        postdata['uploadpic[]'].append(y)

                        file.append((str('uploadpic[]'), (y, open(i, "rb"), "image/jpg")))
                        temp = temp + 1

                url = 'http://talad.me/post/edit/' + str(post_id)

                req = self.httprequestObj.http_post(url, data=postdata, files=file, headers=headers)

                soup = BeautifulSoup(req.text, 'html5lib')

                if post_id == '':
                    success = 'false'
                    detail = 'Something wrong happened'
                else:
                    success = 'true'
                    detail = 'Post edited successfully'
                    # data['post_title_th'] = (data['post_title_th']).encode().decode("unicode-escape")
                    # print((data['post_title_th']).decode('utf-8'))
                    #print(data['post_title_th'])
                    post_url = 'http://talad.me/detail/' + str(post_id)
            else:
                success = 'false'
                detail = 'Post not found'

        end_time = datetime.datetime.utcnow()
        result = {'success': success,
                  'usage_time': str(end_time - start_time),
                  'start_time': str(start_time),
                  'end_time': str(end_time),
                  'post_url': post_url,
                  'post_id': post_id,
                  'account_type': 'null',
                  'ds_id': data['ds_id'],
                  'log_id':data['log_id'],
                  'detail': detail,
                  'websitename': 'talad'}
        return result