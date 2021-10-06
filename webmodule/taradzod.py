import requests, re, random
from bs4 import BeautifulSoup
import json, datetime
from .lib_httprequest import *
from .lib_captcha import  *
import datetime
import time,math
import lxml
import html5lib
from lxml.html.soupparser import fromstring

class taradzod:

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
        self.httprequestObj = lib_httprequest()
        
    def register_user(self, data):
        start_time = datetime.datetime.utcnow()

        success = ''
        detail = ''
        postdata = {
            'email': data['user'],
            'password': data['pass'],
            'confirmPassword': data['pass'],
            'name': data['name_th']+'-'+data['surname_th'],
            'address': '',
            'tel': data['tel'],
            'province_id': '',
            'captcha': '',
            'checkcon': '',
            'action': 'save'
        }
        url = 'http://taradzod.me/user/register'
        headers = {
        	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        }
        regex = '^\\w+([\\.-]?\\w+)*@\\w+([\\.-]?\\w+)*$'
        f1 = True
        regex = '^\\w+([\\.-]?\\w+)*@\\w+([\\.-]?\\w+)*$'
        if re.search(regex, postdata['email']):
            f1 = True
        else:
            f1 = False

        if f1 == False:
            success = 'false'
            detail = 'Invalid email id'
        else:
            url = 'http://www.taradzod.com/members/register.php'
            req = self.httprequestObj.http_get(url,headers=headers)

            soup = BeautifulSoup(req.text,'html.parser')
            if 'addr_province' in data and 'addr_district' in data and data['addr_province'] is not None and data['addr_district'] is not None and data['addr_province']!='' and data['addr_district']!='':
                data['addr_province'] = ''.join(map(str, str(data['addr_province']).split(' ')))
                postdata['address'] = data['addr_district']
                provinces = []
                prov_ids = []
                options = soup.find('select',{'name':'province_id'}).findAll('option')[1:]
                for opt in options:
                    provinces.append(str(opt.text).replace(' ',''))
                    prov_ids.append(opt['value'])
                for i in range(len(provinces)):
                    prov = provinces[i]
                    if prov.find(data['addr_province'])!=-1 or data['addr_province'].find(prov)!=-1:
                        postdata['province_id'] = prov_ids[i]
                        break
                if postdata['province_id'] == '':
                    postdata['province_id'] = prov_ids[0]
            else:
                postdata['address'] = 'พญาไท'
                postdata['province_id'] = '2'

            postdata['checkcon'] = soup.find('input',{'name':'checkcon'})['value']
            capt = lib_captcha()
            key = str(postdata['checkcon'])

            result = capt.reCaptcha(key, url)
            #print('here',result)
            postdata['captcha'] = result
            url = 'http://www.taradzod.com/members/register-complete.php'
            req = self.httprequestObj.http_post(url,data=postdata,headers=headers)
            txt = str(req.text)
            if txt.find('สมัครสมาชิกสำเร็จ')!=-1:
                success = 'true'
                detail = 'Successfully registered'
            else:
                success = 'false'
                detail = 'Already a user'

        end_time = datetime.datetime.utcnow()
        result = {'websitename':'taradzod',
         'success':success,
         'start_time':str(start_time),
         'end_time':str(end_time),
         'usage_time':str(end_time - start_time),
         'detail':detail,
         'ds_id':data['ds_id']}
        return result

    def test_login(self, data):
        # ไม่สามารถเข้าสู่ระบบได้, โปรดตรวจสอบอีเมล์และรหัสผ่านอีกครั้ง
        start_time = datetime.datetime.utcnow()

        success = ''
        detail = ''
        postdata = {
            'username': data['user'],
            'tPassword': data['pass'],
            'checkcon': ''
        }
        url = 'http://www.taradzod.com/login/'
        req = self.httprequestObj.http_get(url)
        soup = BeautifulSoup(req.text,'html.parser')
        postdata['checkcon'] = soup.find('input',{'name':'checkcon'})['value']
        url = 'http://www.taradzod.com/login/login_check.php'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        }
        req = self.httprequestObj.http_post(url,data=postdata,headers=headers)
        txt = str(req.text)
        if txt.find('ชื่อเข้าใช้งาน หรือ รหัสผ่าน ไม่ถูกต้อง')!=-1:
            success = 'false'
            detail = 'Invalid credentials'
        elif txt.find('ยังไม่ได้ยืนยันสมาชิก กรุณากลับไปยืนยันสมาชิกที่ email ที่สมัครไว้') != -1:
            success = 'false'
            detail = 'Unverified account'
        else:
            success = 'true'
            detail = 'Login successful'

        end_time = datetime.datetime.utcnow()
        result = {'websitename':'taradzod',
         'success':success,
         'start_time':str(start_time),
         'end_time':str(end_time),
         'usage_time':str(end_time - start_time),
         'ds_id':data['ds_id'],
         'detail':detail}
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
            #print(data['addr_province'],data['addr_district'])
            postdata['sapap'] = '2hand'
            postdata['car_name'] = str(data['post_title_th'])[:90]
            if data['listing_type'] == 'ขาย':
                postdata['want'] = 'sale'
            else:
                postdata['want'] = 'forrent'
            postdata['b_id'] = '73'
            postdata['v_id'] = ''
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
            property_tp = {'1': '76',
                           '2': '74',
                           '3': '75',
                           '4': '75',
                           '5': '78',
                           '6': '79',
                           '7': '77',
                           '8': '80',
                           '9': '80',
                           '10': '80',
                           '25': '80'}
            if str(data['property_type']) in property_tp:
                postdata['v_id'] = property_tp[str(data['property_type'])]
            else:
                postdata['v_id'] = property_tp[ids[str(data['property_type'])]]
            postdata['price'] = data['price_baht']
            url = 'http://www.taradzod.com/post.php'
            req = self.httprequestObj.http_get(url)
            soup = BeautifulSoup(req.text,'html.parser')
            postdata['p_ssid'] = str(soup.find('input',{'name':'p_ssid'})['value'])
            postdata['p_time'] = str(soup.find('input',{'name':'p_time'})['value'])
            postdata['p_maxImg'] = '9'
            postdata['detailBox'] = str(data['post_description_th'])
            postdata['seller'] = data['name']
            postdata['tel'] = data['mobile']
            data['addr_province'] = ''.join(map(str, str(data['addr_province']).split(' ')))
            data['addr_district'] = ''.join(map(str, str(data['addr_district']).split(' ')))
            provinces = []
            prov_ids = []
            districts = []
            dist_ids = []
            postdata['province_id'] = ''
            options = soup.find('select', {'name': 'province_id'}).findAll('option')[1:]
            for opt in options:
                provinces.append(str(opt.text).replace(' ', ''))
                prov_ids.append(opt['value'])
            for i in range(len(provinces)):
                prov = provinces[i]
                if prov.find(data['addr_province']) != -1 or data['addr_province'].find(prov) != -1:
                    postdata['province_id'] = prov_ids[i]
                    break
            if postdata['province_id'] == '':
                postdata['province_id'] = prov_ids[0]
            url = 'http://www.taradzod.com/aj_select_province.php?province_id='+str(postdata['province_id'])
            req = self.httprequestObj.http_get(url)
            #print('here')

            soup = BeautifulSoup(req.text,'html.parser')
            options = soup.find('select', {'name': 'amphur_id'}).findAll('option')[1:]
            postdata['amphur_id'] = ''
            for opt in options:
                districts.append(str(opt.text).replace(' ', ''))
                dist_ids.append(opt['value'])
            for i in range(len(districts)):
                prov = districts[i]
                if prov.find(data['addr_district']) != -1 or data['addr_district'].find(prov) != -1:
                    postdata['amphur_id'] = dist_ids[i]
                    break
            if postdata['amphur_id'] == '':
                postdata['amphur_id'] = dist_ids[0]
            postdata['status'] = 'yes'
            postdata['action'] = 'save'
            postdata['Submit'] = ''

            if 'post_images' in data and len(data['post_images']) > 0:
                pass
            else:
                data['post_images'] = ['./imgtmp/default/white.jpg']


            files = {}
            temp = 0


            if len(data['post_images']) <= 9:
                for i in data['post_images']:
                    # y = str(random.randint(0, 100000000000000000)) + ".jpg"

                    r = open(os.getcwd() + '/' + i, 'rb')
                    files['files[]'] = r
                    imgdata = {
                        'SubmitFromUpload': 'Upload!',
                        'ssid': postdata['p_ssid'],
                        'time': postdata['p_time'],
                        'numImg': str(temp),
                        'maxImg': '9'
                    }
                    response = self.httprequestObj.http_post('http://www.taradzod.com/ajax/upload.php', data=imgdata,
                                                        files=files)
                    #print(response.text)
                    temp = temp + 1

            else:
                for i in data['post_images'][:9]:
                    # y = str(random.randint(0, 100000000000000000)) + ".jpg"

                    r = open(os.getcwd() + '/' + i, 'rb')
                    files['files[]'] = r
                    imgdata = {
                        'SubmitFromUpload': 'Upload!',
                        'ssid': postdata['p_ssid'],
                        'time': postdata['p_time'],
                        'numImg': str(temp),
                        'maxImg': '9'
                    }
                    response = self.httprequestObj.http_post('http://www.taradzod.com/ajax/upload.php', data=imgdata,
                                                        files=files)
                    #print(response.text)
                    temp = temp + 1


            url = 'http://www.taradzod.com/addprakad-complete.php?tok=yes'
            req = self.httprequestObj.http_post(url,data=postdata,headers=headers)

            txt = str(req.text)
            if txt.find('เพิ่มประกาศสำเร็จ') == -1:
                #print('in')
                success = 'true'
                detail = 'Post created'
                postdata['car_name'] = 'abcd'
                postdata['detailBox'] = 'abcd'

                url = 'http://www.taradzod.com/addprakad-complete.php?tok=yes'
                req = self.httprequestObj.http_post(url, data=postdata, headers=headers)

                url = 'http://www.taradzod.com/prakad.php'
                req = self.httprequestObj.http_get(url)
                soup = BeautifulSoup(req.text, 'html.parser')

                # #print(soup.find('table',{'class':'table table-hover'}).find('tbody'))
                post = soup.find('table', {'class': 'table table-hover'}).find('tbody').findAll('a')[0]
                post_id = ''
                url = str(post['data-url'])
                #print(url)
                ind = url.find('id=') + 3
                while ind < len(url):
                    post_id += url[ind]
                    ind += 1
                post_url = 'http://www.taradzod.com/prakad-' + post_id + '.html'
                data['post_id'] = post_id
                #print('to_edit')
                self.edit_post(data,1)
                #print('edited')
            else:
                success = 'true'
                detail = 'Post created'
                url = 'http://www.taradzod.com/prakad.php'
                req = self.httprequestObj.http_get(url)
                soup = BeautifulSoup(req.text,'html.parser')

                #print(soup.find('table',{'class':'table table-hover'}).find('tbody'))
                post = soup.find('table',{'class':'table table-hover'}).find('tbody').findAll('a')[0]
                post_id = ''
                url = str(post['data-url'])
                #print(url)
                ind = url.find('id=')+3
                while ind<len(url):
                    post_id+=url[ind]
                    ind+=1
                post_url = 'http://www.taradzod.com/prakad-'+post_id+'.html'




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
                  'websitename': 'taradzod'}
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
            url = 'http://www.taradzod.com/prakad.php'
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
            }
            
            req = self.httprequestObj.http_get(url, headers=headers)
            valid_ids = []
            valid_titles = []
            valid_urls = []
            soup = BeautifulSoup(req.text, 'html5lib')
            if soup.find('ul', {'class': 'pagination'}) is None:
                total_pages = 1
            else:
                total_pages = int(len(soup.find('ul', {'class': 'pagination'}).findAll('li')))
                if total_pages>1:
                    total_pages-=1
            #print(total_pages)
            for i in range(total_pages):
                url = 'http://www.taradzod.com/prakad.php?page=' + str(i + 1)
                req = self.httprequestObj.http_get(url, headers=headers)

                soup = BeautifulSoup(req.text, 'html5lib')

                posts = soup.find('tbody').findAll('tr')
                for post in posts:
                    row = post.findAll('td')
                    url = str(row[2].find('a')['href'])
                    ind = url.find('edit-post.php?id=') + 17
                    id = ''
                    while ind < len(url):
                        id += url[ind]
                        ind += 1
                    valid_ids.append(id)
            if post_id in valid_ids:
                url = 'http://www.taradzod.com/action_process.php?task=yes'
                headers = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
                }
                postdata = {
                    'action_id[]': post_id,
                    'action': 'del'
                }
                req = self.httprequestObj.http_post(url,data=postdata, headers=headers)
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
            "websitename": "taradzod"
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
            url = 'http://www.taradzod.com/prakad.php'
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
            }
            
            """req = self.httprequestObj.http_get(url, headers=headers)
            valid_ids = []
            valid_titles = []
            valid_urls = []
            soup = BeautifulSoup(req.text, 'html5lib')
            if soup.find('ul', {'class': 'pagination'}) is None:
                total_pages = 1
            else:
                total_pages = int(len(soup.find('ul', {'class': 'pagination'}).findAll('li')))
                if total_pages>1:
                    total_pages-=1
            #print(total_pages)
            boosted = 0
            for i in range(total_pages):
                url = 'http://www.taradzod.com/prakad.php?page=' + str(i + 1)
                req = self.httprequestObj.http_get(url, headers=headers)

                soup = BeautifulSoup(req.text, 'html5lib')

                posts = soup.find('tbody').findAll('tr')
                for post in posts:
                    row = post.findAll('td')
                    url = str(row[2].find('a')['href'])
                    ind = url.find('edit-post.php?id=') + 17
                    id = ''
                    while ind < len(url):
                        id += url[ind]
                        ind += 1
                    valid_ids.append(id)
                if post_id in valid_ids:"""
            try:
                url = 'http://www.taradzod.com/ajax/update-prakad.php?id='+post_id
                headers = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
                }   
                req = self.httprequestObj.http_get(url, headers=headers)
                detail = 'Announcement postponed'
                success = 'true'
            except:
                detail = 'Post not found'
                success = 'false'

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
            'websitename': 'taradzod'
        }
        # https://ilovecondo.net/new-post/topicid/910653/trk/78
        return result

    def search_post(self, data):
        ##print('in')
        test_login = self.test_login(data)
        success = test_login["success"]
        start_time = datetime.datetime.utcnow()
        end_time = datetime.datetime.utcnow()
        post_title = str(data["post_title_th"]).replace(' ','')
        detail = test_login["detail"]
        post_id = ''
        post_url = ''
        post_found = ''

        if success == "true":
            url = 'http://www.taradzod.com/prakad.php'
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
            }
            req = self.httprequestObj.http_get(url, headers=headers)
            valid_ids = []
            valid_titles = []
            valid_urls = []
            soup = BeautifulSoup(req.text, 'html5lib')
            if soup.find('ul', {'class': 'pagination'}) is None:
                total_pages = 1
            else:
                total_pages = int(len(soup.find('ul', {'class': 'pagination'}).findAll('li')))
                if total_pages>1:
                    total_pages-=1
            #print(total_pages)
            for i in range(total_pages):
                url = 'http://www.taradzod.com/prakad.php?page=' + str(i + 1)
                req = self.httprequestObj.http_get(url, headers=headers)

                soup = BeautifulSoup(req.text, 'html5lib')

                posts = soup.find('tbody').findAll('tr')
                for post in posts:
                    title = str(post.findAll('td')[1].text).replace(' ','').split('|')[0].replace('สถานะ','').replace('\t','').replace('\n','')

                    # print(title)
                    # print(post_title)
                    # print()
                    # print()
                    if title in post_title:
                        # print('true')
                        url = str(post.find('a')['data-url'])
                        id = url.split('=')[-1]
                        post_url = 'http://www.taradzod.com/prakad-'+id+'.html'
                        post_found = 'true'
                        detail = 'Post found'
                        success = 'true'
                        break
                    else:
                        post_found = 'false'
                        detail = 'Post not found'
                        success = 'false'
                        title = ''

        else:
            title = ''


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
            'websitename': 'taradzod',
            "post_title_th": title
        }
        return result
    def edit_post(self, data,to_create=0):
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
            url = 'http://www.taradzod.com/prakad.php'
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
            }
            
            req = self.httprequestObj.http_get(url, headers=headers)
            valid_ids = []
            valid_titles = []
            valid_urls = []
            soup = BeautifulSoup(req.text, 'html5lib')
            if soup.find('ul', {'class': 'pagination'}) is None:
                total_pages = 1
            else:
                total_pages = int(len(soup.find('ul', {'class': 'pagination'}).findAll('li')))
                if total_pages>1:
                    total_pages-=1
            #print(total_pages)
            for i in range(total_pages):
                url = 'http://www.taradzod.com/prakad.php?page=' + str(i + 1)
                req = self.httprequestObj.http_get(url, headers=headers)

                soup = BeautifulSoup(req.text, 'html5lib')

                posts = soup.find('tbody').findAll('tr')
                for post in posts:
                    row = post.findAll('td')
                    url = str(row[2].find('a')['href'])
                    ind = url.find('edit-post.php?id=') + 17
                    id = ''
                    while ind < len(url):
                        id += url[ind]
                        ind += 1
                    valid_ids.append(id)
            if post_id in valid_ids:
                postdata = {}
                #print(data['addr_province'],data['addr_district'])
                postdata['sapap'] = '2hand'
                postdata['car_name'] = str(data['post_title_th'])[:90]
                if data['listing_type'] == 'ขาย':
                    postdata['want'] = 'sale'
                else:
                    postdata['want'] = 'forrent'
                postdata['b_id'] = '73'
                postdata['v_id'] = ''
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
                property_tp = {'1': '76',
                            '2': '74',
                            '3': '75',
                            '4': '75',
                            '5': '78',
                            '6': '79',
                            '7': '77',
                            '8': '80',
                            '9': '80',
                            '10': '80',
                            '25': '80'}
                if str(data['property_type']) in property_tp:
                    postdata['v_id'] = property_tp[str(data['property_type'])]
                else:
                    postdata['v_id'] = property_tp[ids[str(data['property_type'])]]
                postdata['price'] = data['price_baht']
                url = 'http://www.taradzod.com/edit-post.php?id='+post_id
                req = self.httprequestObj.http_get(url)
                soup = BeautifulSoup(req.text,'html.parser')
                postdata['p_ssid'] = str(soup.find('input',{'name':'p_ssid'})['value'])
                postdata['p_time'] = str(soup.find('input',{'name':'p_time'})['value'])
                postdata['p_maxImg'] = '9'
                postdata['detailBox'] = str(data['post_description_th'])
                postdata['seller'] = data['name']
                postdata['tel'] = data['mobile']
                data['addr_province'] = ''.join(map(str, str(data['addr_province']).split(' ')))
                data['addr_district'] = ''.join(map(str, str(data['addr_district']).split(' ')))
                provinces = []
                prov_ids = []
                districts = []
                dist_ids = []
                postdata['province_id'] = ''
                options = soup.find('select', {'name': 'province_id'}).findAll('option')[1:]
                for opt in options:
                    provinces.append(str(opt.text).replace(' ', ''))
                    prov_ids.append(opt['value'])
                for i in range(len(provinces)):
                    prov = provinces[i]
                    if prov.find(data['addr_province']) != -1 or data['addr_province'].find(prov) != -1:
                        postdata['province_id'] = prov_ids[i]
                        break
                if postdata['province_id'] == '':
                    postdata['province_id'] = prov_ids[0]
                url = 'http://www.taradzod.com/aj_select_province.php?province_id='+str(postdata['province_id'])
                req = self.httprequestObj.http_get(url)
                #print('here')

                soup = BeautifulSoup(req.text,'html.parser')
                options = soup.find('select', {'name': 'amphur_id'}).findAll('option')[1:]
                postdata['amphur_id'] = ''
                for opt in options:
                    districts.append(str(opt.text).replace(' ', ''))
                    dist_ids.append(opt['value'])
                for i in range(len(districts)):
                    prov = districts[i]
                    if prov.find(data['addr_district']) != -1 or data['addr_district'].find(prov) != -1:
                        postdata['amphur_id'] = dist_ids[i]
                        break
                if postdata['amphur_id'] == '':
                    postdata['amphur_id'] = dist_ids[0]
                url = 'http://www.taradzod.com/edit-post.php?id=' + post_id
                req = self.httprequestObj.http_get(url)
                soup = BeautifulSoup(req.text, 'html.parser')
                postdata['update_date'] = soup.find('input',{'name':'update_date'})['value']
                postdata['status'] = 'yes'
                postdata['action'] = 'save'
                postdata['Submit'] = ''
                if to_create == 0:
                    images = soup.findAll('div',{'class':'pvImg'})[:-1]
                    for img in images:
                        url = 'http://www.taradzod.com/ajax/del_img.php'
                        imgdata = {
                            'filename':img.find('img')['imgname']
                        }
                        req = self.httprequestObj.http_post(url,data=imgdata,headers=headers)

                    if 'post_images' in data and len(data['post_images']) > 0:
                        pass
                    else:
                        data['post_images'] = ['./imgtmp/default/white.jpg']


                    files = {}
                    temp = 0


                    if len(data['post_images']) <= 9:
                        for i in data['post_images']:
                            # y = str(random.randint(0, 100000000000000000)) + ".jpg"

                            r = open(os.getcwd() + '/' + i, 'rb')
                            files['files[]'] = r
                            imgdata = {
                                'SubmitFromUpload': 'Upload!',
                                'ssid': postdata['p_ssid'],
                                'time': postdata['p_time'],
                                'numImg': str(temp),
                                'maxImg': '9'
                            }
                            response = self.httprequestObj.http_post('http://www.taradzod.com/ajax/upload.php', data=imgdata,
                                                                files=files)
                            #print(response.text)
                            temp = temp + 1

                    else:
                        for i in data['post_images'][:9]:
                            # y = str(random.randint(0, 100000000000000000)) + ".jpg"

                            r = open(os.getcwd() + '/' + i, 'rb')
                            files['files[]'] = r
                            imgdata = {
                                'SubmitFromUpload': 'Upload!',
                                'ssid': postdata['p_ssid'],
                                'time': postdata['p_time'],
                                'numImg': str(temp),
                                'maxImg': '9'
                            }
                            response = self.httprequestObj.http_post('http://www.taradzod.com/ajax/upload.php', data=imgdata,
                                                                files=files)
                            #print(response.text)
                            temp = temp + 1


                url = 'http://www.taradzod.com/updateprakad-complete.php?action=yes&id='+post_id
                req = self.httprequestObj.http_post(url,data=postdata,headers=headers)

                txt = str(req.text)

                success = 'true'
                detail = 'Post edited'

                post_url = 'http://www.taradzod.com/prakad-'+post_id+'.html'
            else:
                success = 'false'
                detail = 'Post not found'

        if to_create ==0:
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
                      'websitename': 'taradzod'}
            return result
