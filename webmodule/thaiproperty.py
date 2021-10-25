from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
import re
import json
import datetime
import sys
import requests
import shutil
from urllib.parse import unquote
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json
from json import JSONEncoder
from .lib_captcha import *

captcha = lib_captcha()


class thaiproperty():

    def __init__(self):

        try:
            import configs

        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.debug = 1
        self.debugresdata = 0
        self.parser = 'html.parser'
        self.authtoken = None
        self.webname = 'thaiproperty'
        self.session = lib_httprequest()

        self.sess = requests.Session()

    def print_debug(self, msg):
        if self.debug == 1:
            print(msg)
        return "true"

    def register_user(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']

        username = postdata['user'].split('@')[0]

        # start process
        #
        success = "true"
        detail = ""

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0',
            'Accept': '*/*',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Referer': 'https://www.thaiproperty.in.th/register',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'pragma': 'no-cache',
            'Origin': 'https://www.thaiproperty.in.th',
            'Connection': 'keep-alive',
            'DNT': '1',
            'TE': 'Trailers',
        }
        print('here')
        #ans = captcha.recaptcha('6LcLmboUAAAAADH3JCFgRjiBFh6gtuZeV9-mOjja', 'https://www.thaiproperty.in.th/register')
        #print(ans)

        datapost = '{"email":"' + user + '","firstName":"' + postdata['name_th'] + '","lastName":"' + postdata[
            'surname_th'] + '","password":"' + passwd + '","passwordConfirmation":"' + passwd + '","memberTypeId":"0","username":"' + \
                   username + '","agreement":"true"}'

        #g = captcha.reCaptcha('6LcLmboUAAAAADH3JCFgRjiBFh6gtuZeV9-mOjja', 'https://www.thaiproperty.in.th/register')
        #print(g)

        r = self.sess.post('https://api.thaiproperty.in.th/api/accounts/register',
                                     data=datapost.encode('utf-8'), headers=headers)
        print(r.url)
        print(r.status_code)
        if(r.status_code == 400):
            success = False
            detail = "Already registered"
        else:
            data = r.json()
            resp = data['status']

            if 'สร้างแอคเคาท์ใหม่เรียบร้อยแล้ว กรุณาเข้าสู่ระบบด้วยอีเมล์กับรหัสผ่านของคุณ' in resp:
                success = True
                detail = "Registered successfully"
            else:
                detail = False
                detail = "Couldnot register"

        time_end = datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "thaiproperty",
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": postdata['ds_id'],
            "detail": detail,
        }

    def test_login(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']
        # start process
        #
        success = "true"
        detail = "logged in"

        headers = {
            'authority': 'api.thaiproperty.in.th',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-fetch-dest': 'empty',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'content-type': 'application/json',
            'accept': '*/*',
            'origin': 'https://www.thaiproperty.in.th',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'referer': 'https://www.thaiproperty.in.th/login',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        # r = self.session.http_get('https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LcLmboUAAAAADH3JCFgRjiBFh6gtuZeV9-mOjja&co=aHR0cHM6Ly93d3cudGhhaXByb3BlcnR5LmluLnRoOjQ0Mw..&hl=en&type=image&v=nuX0GNR875hMLA1LR7ayD9tc&theme=light&size=normal&badge=bottomright&cb=oxm3bh97kk5x')
        # print(r.url)
        # print(r.status_code)

        r = self.sess.get('https://www.thaiproperty.in.th/login')
        print(r.url)
        print(r.status_code)

        #with open('/home/codelover/Desktop/rough.html', 'w') as f:
            #f.write(r.text)

        #g = captcha.reCaptcha('6LcLmboUAAAAADH3JCFgRjiBFh6gtuZeV9-mOjja', 'https://www.thaiproperty.in.th/login')
        #print(g)

        # with open('/home/codelover/Desktop/rough.html', 'w') as f:
        #     f.write(r.text)

        data = {
            "email": user,
            "password": passwd,
        }

        data = '{"userName":"' + postdata['user'] + '","password":"' + postdata['pass'] + '"}'

        r = self.sess.options('https://api.thaiproperty.in.th/api/auth/login')

        r = self.sess.post('https://api.thaiproperty.in.th/api/auth/login', data=data,
                           headers={'content-type': 'application/json'})

        print(r.url)
        print(r.status_code)
        print(r.text)

        # exit(0)
        authtoken = 'None'
        if r.status_code == 401:
            success = False
            detail = "Couldnot login"
        else:
            success = True
            self.authtoken = json.loads(r.text)['jwt']['auth_token']
            detail = "Login successful"

        r = self.sess.get('https://www.thaiproperty.in.th/', cookies={'auth_token': self.authtoken})
        print(r.url)
        print(r.status_code)

        #with open('/home/codelover/Desktop/rough.html', 'w') as f:
            #f.write(r.text)

        time_end = datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": self.webname,
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": postdata['ds_id'],
            "detail": detail,
        }

    def create_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.utcnow()

        datapost = {}
        # start process
        #

        # login
        if 'name' not in postdata:
            success = "False"
            detail = "Please fill name"
        elif 'mobile' not in postdata:
            success = "False"
            detail = "Please fill mobile number"
        elif 'email' not in postdata:
            success = "False"
            detail = "Please fill email"

        test_login = self.test_login(postdata)
        authtoken = self.authtoken
        # print(authtoken)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""

        print(success)
        print(detail)

        if success:

            print('Here')

            if 'web_project_name' not in postdata or postdata['web_project_name'] is None:
                if 'project_name' in postdata and postdata['project_name'] != None:
                    postdata['web_project_name'] = postdata['project_name']
                else:
                    postdata['web_project_name'] = postdata['post_title_th']

            print('1')

            proid = {
                'คอนโด': '1',
                'บ้านเดี่ยว': '2',
                'บ้านแฝด': '3',
                'ทาวน์เฮ้าส์': '4',
                'ตึกแถว-อาคารพาณิชย์': '5',
                'ที่ดิน': '6',
                'อพาร์ทเมนท์': '7',
                'โรงแรม': '8',
                'ออฟฟิศสำนักงาน': '9',
                'โกดัง': '10',
                'โรงงาน': '25'
            }
            getProdId = {'1': '4', '2': '2', '3': '3', '4': '3',
                         '5': '8', '6': '5', '7': '6', '8': '15', '9': '10', '10': '12', '25': '12'}

            print('2')

            try:
                theprodid = getProdId[proid[str(postdata['property_type'])]]
                postdata['property_type'] = str(proid[str(postdata['property_type'])])
            except:
                theprodid = getProdId[str(postdata['property_type'])]

            print('Fetching newpost webpage')

            r = self.sess.get('https://www.thaiproperty.in.th/newpost', cookies={'auth_token': self.authtoken})
            print(r.url)
            print(r.status_code)

            #with open('/home/codelover/Desktop/rough.html', 'w') as f:
                #f.write(r.text)

            headers = {
                'authority': 'api.thaiproperty.in.th',
                'accept': '*/*',
                'access-control-request-method': 'GET',
                'access-control-request-headers': 'authorization',
                'origin': 'https://www.thaiproperty.in.th',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.thaiproperty.in.th/newpost',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
            }

            # O1
            r = self.sess.options('https://api.thaiproperty.in.th/api/accounts/profile', headers=headers)
            print(r.status_code)

            headers = {
                'authority': 'api.thaiproperty.in.th',
                'accept': '*/*',
                'access-control-request-method': 'GET',
                'access-control-request-headers': 'authorization,content-type',
                'origin': 'https://www.thaiproperty.in.th',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.thaiproperty.in.th/newpost',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
            }

            # O2
            r = self.sess.options('https://api.thaiproperty.in.th/api/favorites', headers=headers)
            print(r.status_code)

            headers = {
                'authority': 'api.thaiproperty.in.th',
                'accept': '*/*',
                'access-control-request-method': 'GET',
                'access-control-request-headers': 'authorization,content-type',
                'origin': 'https://www.thaiproperty.in.th',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.thaiproperty.in.th/newpost',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
            }

            # O3
            r = self.sess.options('https://api.thaiproperty.in.th/api/notifications/user', headers=headers)
            print(r.status_code)

            headers = {
                'authority': 'api.thaiproperty.in.th',
                'accept': '*/*',
                'access-control-request-method': 'GET',
                'access-control-request-headers': 'authorization',
                'origin': 'https://www.thaiproperty.in.th',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.thaiproperty.in.th/newpost',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
            }

            # O4
            r = self.sess.options('https://api.thaiproperty.in.th/api/posts/check', headers=headers)
            print(r.status_code)

            headers = {
                'authority': 'api.thaiproperty.in.th',
                'accept': 'application/json',
                'authorization': 'Bearer ' + self.authtoken,
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                'origin': 'https://www.thaiproperty.in.th',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.thaiproperty.in.th/newpost',
                'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
            }

            # G1
            r = self.sess.get('https://api.thaiproperty.in.th/api/accounts/profile', headers=headers)
            print(r.status_code)
            print(r.text)

            headers = {
                'authority': 'api.thaiproperty.in.th',
                'accept': 'application/json',
                'authorization': 'Bearer ' + self.authtoken,
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                'content-type': 'application/json',
                'origin': 'https://www.thaiproperty.in.th',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.thaiproperty.in.th/newpost',
                'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
            }

            # G2
            r = self.sess.get('https://api.thaiproperty.in.th/api/favorites', headers=headers)
            print(r.status_code)

            headers = {
                'authority': 'api.thaiproperty.in.th',
                'accept': 'application/json',
                'authorization': 'Bearer ' + self.authtoken,
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                'content-type': 'application/json',
                'origin': 'https://www.thaiproperty.in.th',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.thaiproperty.in.th/newpost',
                'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
            }

            # G3
            r = self.sess.get('https://api.thaiproperty.in.th/api/notifications/user', headers=headers)
            print(r.status_code)

            headers = {
                'authority': 'api.thaiproperty.in.th',
                'authorization': 'Bearer ' + self.authtoken,
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                'accept': '*/*',
                'origin': 'https://www.thaiproperty.in.th',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.thaiproperty.in.th/newpost',
                'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
            }

            # G4
            r = self.sess.get('https://api.thaiproperty.in.th/api/posts/check', headers=headers)
            print(r.url)
            print(r.status_code)
            print(r.text)

            print(theprodid)
            province_id = '1'
            district_id = ''
            r = self.sess.get("https://api.thaiproperty.in.th/api/provinces")
            print(r.url)
            print(r.status_code)
            provinces = json.loads(r.text)

            print(provinces)

            for prov in provinces:
                if prov['name'].replace(' ', '') in postdata["addr_province"].replace(' ', '') or postdata[
                    "addr_province"].replace(' ', '') in prov['name'].replace(' ', ''):
                    province_id = str(prov['id'])
                    break

            print('Province_id = ' + province_id)

            r = self.sess.get("https://api.thaiproperty.in.th/api/districts")
            print(r.url)
            print(r.status_code)
            districts = json.loads(r.text)

            for district in districts:
                if str(district['provinceId']) == province_id and (
                        district['name'].replace(' ', '') in postdata['addr_district'].replace(' ', '') or postdata[
                    'addr_district'].replace(' ', '') in district['name'].replace(' ', '')):
                    print(district['name'])
                    district_id = str(district['id'])
                    break

            # prod_address = prod_address[:-1]
            print('District_id = ' + district_id)

            if str(postdata['property_type']) == '1':
                area = str(postdata['floorarea_sqm'])
                area_unit = '2'
            else:
                if 'land_size_rai' not in postdata.keys() or postdata['land_size_rai'] is None:
                    postdata['land_size_rai'] = 0.0
                if 'land_size_ngan' not in postdata.keys() or postdata['land_size_ngan'] is None:
                    postdata['land_size_ngan'] = 0.0
                if 'land_size_wa' not in postdata.keys() or postdata['land_size_wa'] is None:
                    postdata['land_size_wa'] = 0.0
                area = str(postdata['land_size_rai'] * 400 + postdata['land_size_ngan'] * 100 + postdata['land_size_wa'])
                area_unit = '1'

            # print('00')
            if 'floor_total' not in postdata:
                postdata['floor_total'] = ""

            if 'floor_level' not in postdata:
                postdata['floor_level'] = ""

            if 'bath_room' not in postdata:
                postdata['bath_room'] = ""

            if 'bed_room' not in postdata:
                postdata['bed_room'] = ""

            listing = 0
            # print('01')

            if postdata['listing_type'] != 'เช่า':
                # sell
                isForRent = 'false'
            else:
                # rent
                isForRent = 'true'

            # print(postdata)
            desc = '<p><span>' + postdata['post_description_th'].replace('\n', '</span><br><span>') + '</span></p>'
            # desc = '<p>' + 'the final description' + '</p>'

            datapost = [
                # ("title", (None, postdata['post_title_th'])),
                ("title", (None, postdata['post_title_th'])),
                ("price", (None, str(postdata['price_baht']))),
                ("area", (None, str(area))),
                ("areaUnit", (None, area_unit)),
                ("isSold", (None, 'false')),
                ("details", (None, desc)),
                ("category", (None, str(theprodid))),
                ("isForRent", (None, isForRent)),
                ("district", (None, district_id)),
                ("province", (None, province_id)),
                ("floor", (None, '1')),
                ("lat", (None, str(postdata['geo_latitude']))),
                ("lng", (None, str(postdata['geo_longitude']))),
                ("places", (None, ''))
            ]

            if postdata['property_type'] != '6':
                datapost.append(("bedRoom", (None, str(postdata['bed_room']))))
                datapost.append(("bathRoom", (None, str(postdata['bath_room']))))

                r = self.sess.get('https://api.thaiproperty.in.th/api/projects')
                print(r.url)
                print(r.status_code)
                projects = r.json()

                if postdata['web_project_name'] != '':
                    for project in projects:
                        if project['projectName'].replace(' ', '') in postdata['web_project_name'].replace(' ', '') or \
                                postdata['web_project_name'].replace(' ', '') in project['projectName'].replace(' ',
                                                                                                                ''):
                            datapost.append(('projectId', (None, project['projectId'])))
                            datapost.append(('project', (None, project)))
                            break

            # print(datapost)

            # files = {
            #     # "files":[]
            # }
            # print('04')

            # edit_image_url = 'https://www.thaiproperty.in.th/editimage/' + postdata['post_id']
            # r = sess.get(edit_image_url)
            # print(r.url)
            # print(r.status_code)
            #
            # soup = BeautifulSoup(r.content, self.parser)
            # old_images = soup.find_all('img', 'ant-upload-list-item-image')
            #
            # for img in old_images:
            #     info = img.get('src').split('/')
            #     del_url = 'https://api.thaiproperty.in.th/api/images/image/'+info[-2]+'/'+info[-1]+'?PostId='+postdata['post_id']
            #     r = sess.delete(del_url)

            # datapost = []
            # myfiles = []

            # postdata['post_images'] = ['/home/codelover/Desktop/Ignis/h1.jpeg', '/home/codelover/Desktop/Ignis/h2.jpeg']
            allimages = postdata["post_images"]

            for i in range(len(allimages)):
                # r = open(allimages[i], 'rb')
                filename = str(i) + '.jpeg'
                print(filename)
                # datapost['akbzkyacxeaa'+str(i+1)]=r
                # print(r.name)
                # datapost.append(("files",(r.name,r, 'image/'+r.name.split('.')[-1])))
                datapost.append(("files", (filename, open(allimages[i], 'rb'), 'image/jpeg')))
                # print(abc)
                # break
            # print(datapost)
            # print(myfiles)
            # print(json.dumps(datapost,cls=MyEncoder))
            # print(json.dumps(datapost,cls=MyEncoder).replace('akbzkyacxeaa1','file').replace('akbzkyacxeaa2','file'))
            # print(files)
            # with open('multiform.txt','r')as  f:
            #     datapost=f.read()
            # print('05')

            headers = {
                'authority': 'api.thaiproperty.in.th',
                'accept': '*/*',
                'access-control-request-method': 'POST',
                'access-control-request-headers': 'authorization',
                'origin': 'https://www.thaiproperty.in.th',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.thaiproperty.in.th/newpost',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
            }

            print(datapost)

            r = self.sess.options('https://api.thaiproperty.in.th/api/posts', headers=headers)
            print(r.url)
            print(r.status_code)

            token = 'eyJhbGciOiJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzA0L3htbGRzaWctbW9yZSNobWFjLXNoYTI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdGRyIiwianRpIjoiYzZmYjI4YzItNjY5My00NzZjLWI3ZmUtYmZkZjIzMThmZWYzIiwiaWF0IjoxNTk0ODkxMTg3LCJyb2wiOiJVc2VyIiwiaWQiOiJhMThhNzE4Yy0zZTA4LTRjZjAtOTM0ZS0wZWU1NGFlNzNmMzgiLCJuYmYiOjE1OTQ4OTExODcsImV4cCI6MTU5NTIzNjc4NywiaXNzIjoiVGhhaVByb3BlcnR5IiwiYXVkIjoiaHR0cHM6Ly9hcGkudGhhaXByb3BlcnR5LmluLnRoLyJ9.VYnM3gdX97XGaQbVAjjdiMlPDn41pLOZRaLLtqNnl4g'

            headers = {
                'authority': 'api.thaiproperty.in.th',
                'accept': 'application/json, text/plain, */*',
                'authorization': 'Bearer ' + self.authtoken,
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                'origin': 'https://www.thaiproperty.in.th',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.thaiproperty.in.th/newpost',
                'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
            }

            # print(headers)

            r = self.sess.post('https://api.thaiproperty.in.th/api/posts', headers=headers, data={}, files=datapost)
            data = r.json()
            print(r.url)
            print(r.status_code)
            print(data)
            # print(r)
            # print(r.raise_for_status())

            # with open('/home/codelover/Desktop/rough.html', 'w') as f:
            #     f.write(data)

            if 'post' in data:
                success = True
                detail = "Post created successfully"
                post_id = str(data['post']['postId'])
                tail = postdata['post_title_th'].replace(' ', '-') + '-' + post_id
                post_url = 'https://www.thaiproperty.in.th/p/' + tail
            elif 'message' in data:
                if 'คุณมีเหรียญไม่พอในการใช้ลงประกาศใหม่\n<br/>ต้องใช้เหรียญ 2 coin ในการโพสประกาศใหม่\n<br/>คุณสามารถขอรับเหรียญฟรีได้หากคุณเป็นนายหน้าที่มีคุณภาพ หรือมีการลงประกาศครบถ้วนสมบูรณ์\n<br/>หรือจากการเติมเหรียญผ่านระบบ\n<br/><a href="https://www.thaiproperty.in.th/account/topupcoin">คลิ้กที่เพื่ออ่านรายละเอียดการเติมเหรียญ</a>' in data["message"]:
                    success = False
                    detail = "You do not have enough coins to post a new listing."
                else:
                    success = False
                    detail = "Couldnot create post"
            else:
                success = False
                detail = "Couldnot create post"

        else:
            success = False
            detail = "Couldnot login"

        time_end = datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": self.webname,
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": postdata['ds_id'],
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
        }

    def edit_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.utcnow()

        datapost = {}
        # start process
        #

        # login
        if 'name' not in postdata:
            success = "False"
            detail = "Please fill name"
        elif 'mobile' not in postdata:
            success = "False"
            detail = "Please fill mobile number"
        elif 'email' not in postdata:
            success = "False"
            detail = "Please fill email"

        test_login = self.test_login(postdata)
        authtoken = self.authtoken
        # print(authtoken)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""

        if success:

            post_found = False

            if 'web_project_name' not in postdata or postdata['web_project_name'] is None:
                if 'project_name' in postdata and postdata['project_name'] != None:
                    postdata['web_project_name'] = postdata['project_name']
                else:
                    postdata['web_project_name'] = postdata['post_title_th']

            headers = {
                'authority': 'api.thaiproperty.in.th',
                'accept': '*/*',
                'access-control-request-method': 'GET',
                'access-control-request-headers': 'authorization',
                'origin': 'https://www.thaiproperty.in.th',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.thaiproperty.in.th/account/manage',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
            }

            params = (
                ('limit', '200'),
            )

            r = self.sess.options('https://api.thaiproperty.in.th/api/posts/manage', headers=headers,
                                        params=params)
            print(r.url)
            print(r.status_code)

            headers = {
                'authority': 'api.thaiproperty.in.th',
                'authorization': 'Bearer ' + self.authtoken,
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                'accept': '*/*',
                'origin': 'https://www.thaiproperty.in.th',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.thaiproperty.in.th/account/manage',
                'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
            }

            params = (
                ('limit', '200'),
            )

            r = self.sess.get('https://api.thaiproperty.in.th/api/posts/manage', headers=headers, params=params)
            print(r.url)
            print(r.status_code)
            all_posts = r.json()

            #with open('/home/codelover/Desktop/rough.html', 'w') as f:
            #    f.write(r.text)

            # soup = BeautifulSoup(r.content, self.parser)
            # all_posts = soup.find('div', 'mt-3 list-container row').findChildren('div', 'col-12 col-md-6 col-xl-4')
            # print(all_posts)

            for post in all_posts:
                post_id = str(post['postId'])
                print(post_id)
                if post_id == postdata['post_id']:
                    post_found = True
                    break

            if post_found:
                proid = {
                    'คอนโด': '1',
                    'บ้านเดี่ยว': '2',
                    'บ้านแฝด': '3',
                    'ทาวน์เฮ้าส์': '4',
                    'ตึกแถว-อาคารพาณิชย์': '5',
                    'ที่ดิน': '6',
                    'อพาร์ทเมนท์': '7',
                    'โรงแรม': '8',
                    'ออฟฟิศสำนักงาน': '9',
                    'โกดัง': '10',
                    'โรงงาน': '25'
                }
                getProdId = {'1': '4', '2': '2', '3': '3', '4': '3',
                             '5': '8', '6': '5', '7': '6', '8': '15', '9': '10', '10': '12', '25': '12'}

                try:
                    theprodid = getProdId[proid[postdata['property_type']]]
                    postdata['property_type'] = str(proid[str(postdata['property_type'])])
                except:
                    theprodid = getProdId[postdata['property_type']]

                edit_url = 'https://www.thaiproperty.in.th/editpost/' + post_id + '?rawDetails=1'
                r = self.sess.get(edit_url, cookies={'auth_token': self.authtoken})
                print(r.url)
                print(r.status_code)

                headers = {
                    'authority': 'api.thaiproperty.in.th',
                    'accept': '*/*',
                    'access-control-request-method': 'GET',
                    'access-control-request-headers': 'authorization',
                    'origin': 'https://www.thaiproperty.in.th',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://www.thaiproperty.in.th/newpost',
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                    'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                }

                # O1
                r = self.sess.options('https://api.thaiproperty.in.th/api/accounts/profile', headers=headers)
                print(r.status_code)

                headers = {
                    'authority': 'api.thaiproperty.in.th',
                    'accept': '*/*',
                    'access-control-request-method': 'GET',
                    'access-control-request-headers': 'authorization,content-type',
                    'origin': 'https://www.thaiproperty.in.th',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://www.thaiproperty.in.th/newpost',
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                    'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                }

                # O2
                r = self.sess.options('https://api.thaiproperty.in.th/api/favorites', headers=headers)
                print(r.status_code)

                headers = {
                    'authority': 'api.thaiproperty.in.th',
                    'accept': '*/*',
                    'access-control-request-method': 'GET',
                    'access-control-request-headers': 'authorization,content-type',
                    'origin': 'https://www.thaiproperty.in.th',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://www.thaiproperty.in.th/newpost',
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                    'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                }

                # O3
                r = self.sess.options('https://api.thaiproperty.in.th/api/notifications/user', headers=headers)
                print(r.status_code)

                headers = {
                    'authority': 'api.thaiproperty.in.th',
                    'accept': '*/*',
                    'access-control-request-method': 'GET',
                    'access-control-request-headers': 'authorization',
                    'origin': 'https://www.thaiproperty.in.th',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://www.thaiproperty.in.th/newpost',
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                    'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                }

                # O4
                r = self.sess.options('https://api.thaiproperty.in.th/api/posts/check', headers=headers)
                print(r.status_code)

                headers = {
                    'authority': 'api.thaiproperty.in.th',
                    'accept': 'application/json',
                    'authorization': 'Bearer ' + self.authtoken,
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                    'origin': 'https://www.thaiproperty.in.th',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://www.thaiproperty.in.th/newpost',
                    'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                }

                # G1
                r = self.sess.get('https://api.thaiproperty.in.th/api/accounts/profile', headers=headers)
                print(r.status_code)
                print(r.text)

                headers = {
                    'authority': 'api.thaiproperty.in.th',
                    'accept': 'application/json',
                    'authorization': 'Bearer ' + self.authtoken,
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                    'content-type': 'application/json',
                    'origin': 'https://www.thaiproperty.in.th',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://www.thaiproperty.in.th/newpost',
                    'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                }

                # G2
                r = self.sess.get('https://api.thaiproperty.in.th/api/favorites', headers=headers)
                print(r.status_code)

                headers = {
                    'authority': 'api.thaiproperty.in.th',
                    'accept': 'application/json',
                    'authorization': 'Bearer ' + self.authtoken,
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                    'content-type': 'application/json',
                    'origin': 'https://www.thaiproperty.in.th',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://www.thaiproperty.in.th/newpost',
                    'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                }

                # G3
                r = self.sess.get('https://api.thaiproperty.in.th/api/notifications/user', headers=headers)
                print(r.status_code)

                headers = {
                    'authority': 'api.thaiproperty.in.th',
                    'authorization': 'Bearer ' + self.authtoken,
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                    'accept': '*/*',
                    'origin': 'https://www.thaiproperty.in.th',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://www.thaiproperty.in.th/newpost',
                    'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                }

                # G4
                r = self.sess.get('https://api.thaiproperty.in.th/api/posts/check', headers=headers)
                print(r.url)
                print(r.status_code)
                print(r.text)

                print(theprodid)
                province_id = '1'
                district_id = ''
                r = self.sess.get("https://api.thaiproperty.in.th/api/provinces")
                provinces = json.loads(r.text)
                for prov in provinces:
                    if prov['name'].replace(' ', '') in postdata["addr_province"].replace(' ', '') or postdata[
                        "addr_province"].replace(' ', '') in prov['name'].replace(' ', ''):
                        province_id = str(prov['id'])
                        break

                r = self.sess.get("https://api.thaiproperty.in.th/api/districts")
                districts = json.loads(r.text)
                for district in districts:
                    if str(district['provinceId']) == province_id and (district['name'].replace(' ', '') in postdata['addr_district'].replace(' ', '') or postdata[
                        'addr_district'].replace(' ', '') in district['name'].replace(' ', '')):
                        district_id = str(district['id'])
                        break

                # prod_address = prod_address[:-1]

                if postdata['property_type'] == '1':
                    area = str(postdata['floorarea_sqm'])
                    area_unit = '2'
                else:
                    if 'land_size_rai' not in postdata.keys() or postdata['land_size_rai'] is None:
                        postdata['land_size_rai'] = 0.0
                    if 'land_size_ngan' not in postdata.keys() or postdata['land_size_ngan'] is None:
                        postdata['land_size_ngan'] = 0.0
                    if 'land_size_wa' not in postdata.keys() or postdata['land_size_wa'] is None:
                        postdata['land_size_wa'] = 0.0
                    area = str(postdata['land_size_rai'] * 400 + postdata['land_size_ngan'] * 100 + postdata['land_size_wa'])
                    area_unit = '1'

                # print('00')
                if 'floor_total' not in postdata:
                    postdata['floor_total'] = ""

                if 'floor_level' not in postdata:
                    postdata['floor_level'] = ""

                if 'bath_room' not in postdata:
                    postdata['bath_room'] = ""

                if 'bed_room' not in postdata:
                    postdata['bed_room'] = ""

                listing = 0
                # print('01')

                if postdata['listing_type'] != 'เช่า':
                    # sell
                    isForRent = 'false'
                else:
                    # rent
                    isForRent = 'true'



                # print(postdata)
                desc = '<p><span>' + postdata['post_description_th'].replace('\r\n', '</span><br><span>') + '</span></p>'
                # desc = '<p>' + 'the final description' + '</p>'

                datapost = [
                    ('formtype', (None, 'edit')),
                    ('postId', (None, post_id)),
                    ("title", (None, postdata['post_title_th'])),
                    ("price", (None, str(postdata['price_baht']))),
                    ("refId",(None,postdata["property_type"])),
                    ("area", (None, str(area))),
                    ("areaUnit", (None, area_unit)),
                    ("isSold", (None, 'false')),
                    ("details", (None, desc)),
                    ("category", (None, str(theprodid))),
                    ("isForRent", (None, isForRent)),
                    ("district", (None, district_id)),
                    ("province", (None, province_id)),
                    ("deposit",(None,"undefined")),
                    ("placesEducation",(None,"")),
                    ("placesBts", (None, "")),
                    ("placesMrt", (None, "")),
                    ("placesArl", (None, "")),
                    ("placesDepartment", (None, "")),
                    ("placesOfficeBuilding:", (None, "")),
                    ("floor", (None, '1')),
                    ("lat", (None, str(postdata['geo_latitude']))),
                    ("lng", (None, str(postdata['geo_longitude']))),
                    ("places", (None, ',,,,,'))
                ]

                if postdata['property_type'] != '6':
                    datapost.append(("bedRoom", (None, str(postdata['bed_room']))))
                    datapost.append(("bathRoom", (None, str(postdata['bath_room']))))

                    r = self.sess.get('https://api.thaiproperty.in.th/api/projects')
                    projects = r.json()

                    if postdata['web_project_name'] != '':
                        for project in projects:
                            if project['projectName'].replace(' ', '') in postdata['web_project_name'].replace(' ', '') or postdata['web_project_name'].replace(' ', '') in project['projectName'].replace(' ', ''):
                                datapost.append(('projectId', (None, project['projectId'])))
                                datapost.append(('project', (None, project)))
                                break


                # print(datapost)
                """
                headers = {
                    'authority': 'api.thaiproperty.in.th',
                    'accept': '*/*',
                    'access-control-request-method': 'POST',
                    'access-control-request-headers': 'authorization',
                    'origin': 'https://www.thaiproperty.in.th',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://www.thaiproperty.in.th/editpost/' + post_id,
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                    'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                }
                """
                headers = {
                    'authority': 'api.thaiproperty.in.th',
                    'accept': '*/*',
                    'access-control-request-method': 'PUT',
                    'access-control-request-headers': 'authorization',
                    'origin': 'https://www.thaiproperty.in.th',
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://www.thaiproperty.in.th/',
                    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                }
                print(datapost)

                post_url = 'https://api.thaiproperty.in.th/api/posts/' + post_id
                r = self.sess.options(post_url, headers=headers)
                print(r.status_code)

                # token = 'eyJhbGciOiJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzA0L3htbGRzaWctbW9yZSNobWFjLXNoYTI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdGRyIiwianRpIjoiYzZmYjI4YzItNjY5My00NzZjLWI3ZmUtYmZkZjIzMThmZWYzIiwiaWF0IjoxNTk0ODkxMTg3LCJyb2wiOiJVc2VyIiwiaWQiOiJhMThhNzE4Yy0zZTA4LTRjZjAtOTM0ZS0wZWU1NGFlNzNmMzgiLCJuYmYiOjE1OTQ4OTExODcsImV4cCI6MTU5NTIzNjc4NywiaXNzIjoiVGhhaVByb3BlcnR5IiwiYXVkIjoiaHR0cHM6Ly9hcGkudGhhaXByb3BlcnR5LmluLnRoLyJ9.VYnM3gdX97XGaQbVAjjdiMlPDn41pLOZRaLLtqNnl4g'
                """
                headers = {
                    'authority': 'api.thaiproperty.in.th',
                    'accept': 'application/json, text/plain, */*',
                    'authorization': 'Bearer ' + self.authtoken,
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                    'origin': 'https://www.thaiproperty.in.th',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://www.thaiproperty.in.th/editpost/' + post_id,
                    'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                }
                """
                # print(headers)

                headers = {
                    'authority': 'api.thaiproperty.in.th',
                    'accept': 'application/json, text/plain, */*',
                    'authorization': 'Bearer '+ self.authtoken,
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                    'content-type': 'multipart/form-data',
                    'origin': 'https://www.thaiproperty.in.th',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://www.thaiproperty.in.th/',
                    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                }
                print(post_url)
                r = self.sess.put(post_url, headers=headers, data={}, files=datapost)
                print(r.status_code)
                print(r.text)
                data = r.json()
                print(r.url)
                print(r.status_code)
                print(data)

                result = data['status']
                # print(r)
                # print(r.raise_for_status())

                # with open('/home/codelover/Desktop/rough.html', 'w') as f:
                #     f.write(data)

                edit_url = 'https://api.thaiproperty.in.th/api/posts/' + post_id
                r = self.sess.get(edit_url)
                print(r.url)
                print(r.status_code)

                # soup = BeautifulSoup(r.content, self.parser)
                # old_images = soup.find_all('img', 'ant-upload-list-item-image')
                # print(old_images)
                data = r.json()
                user_id = data['userId']
                print(user_id)
                old_logo = data['logoImageFile']
                del_url = 'https://api.thaiproperty.in.th/api/images/logoimage/' + user_id + '/' + old_logo
                params = {'PostID': postdata['post_id']}
                headers = {
                    'authority': 'api.thaiproperty.in.th',
                    'accept': '*/*',
                    'access-control-request-method': 'DELETE',
                    'access-control-request-headers': 'authorization',
                    'origin': 'https://www.thaiproperty.in.th',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://www.thaiproperty.in.th/editimage/' + post_id,
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                    'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                }

                print(del_url)
                r = self.sess.options(del_url, headers=headers, params=params)
                print(r.url)
                print(r.status_code)

                headers = {
                    'authority': 'api.thaiproperty.in.th',
                    'authorization': 'Bearer ' + self.authtoken,
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                    'accept': '*/*',
                    'origin': 'https://www.thaiproperty.in.th',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://www.thaiproperty.in.th/editimage/477022',
                    'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                }

                r = self.sess.delete(del_url, headers=headers, params=params)
                print(r.url)
                print(r.status_code)

                old_images = data['propImages']

                for i, img in enumerate(old_images):
                    filename = img['imageFileName']
                    del_url = 'https://api.thaiproperty.in.th/api/images/image/' + user_id + '/' + filename
                    print(del_url)
                    headers = {
                        'authority': 'api.thaiproperty.in.th',
                        'accept': '*/*',
                        'access-control-request-method': 'DELETE',
                        'access-control-request-headers': 'authorization',
                        'origin': 'https://www.thaiproperty.in.th',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'same-site',
                        'sec-fetch-dest': 'empty',
                        'referer': 'https://www.thaiproperty.in.th/editimage/' + post_id,
                        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                        'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                    }
                    params = {
                        'imageId': str(img['imageId'])
                    }

                    r = self.sess.options(del_url, headers=headers, params=params)
                    print(r.url)
                    print(r.status_code)

                    headers = {
                        'authority': 'api.thaiproperty.in.th',
                        'authorization': 'Bearer ' + self.authtoken,
                        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                        'accept': '*/*',
                        'origin': 'https://www.thaiproperty.in.th',
                        'sec-fetch-site': 'same-site',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-dest': 'empty',
                        'referer': 'https://www.thaiproperty.in.th/editimage/477022',
                        'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                    }

                    r = self.sess.delete(del_url, headers=headers, params=params)
                    print(r.url)
                    print(r.status_code)

                # datapost = []
                # myfiles = []

                # postdata['post_images'] = ['/home/codelover/Desktop/Ignis/h1.jpeg', '/home/codelover/Desktop/Ignis/h2.jpeg']
                allimages = postdata["post_images"]

                for i in range(len(allimages)):
                    # r = open(allimages[i], 'rb')
                    filename = str(i) + '.jpeg'
                    print(filename)
                    # datapost['akbzkyacxeaa'+str(i+1)]=r
                    # print(r.name)
                    # datapost.append(("files",(r.name,r, 'image/'+r.name.split('.')[-1])))
                    headers = {
                        'authority': 'api.thaiproperty.in.th',
                        'authorization': 'Bearer ' + self.authtoken,
                        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                        'accept': '*/*',
                        'origin': 'https://www.thaiproperty.in.th',
                        'sec-fetch-site': 'same-site',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-dest': 'empty',
                        'referer': 'https://www.thaiproperty.in.th/editimage/' + post_id,
                        'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                    }
                    datapost = [("files", (filename, open(allimages[i], 'rb'), 'image/jpeg'))]
                    if i == 0:
                        img_url = 'https://api.thaiproperty.in.th/api/images/logoimage/' + post_id
                    else:
                        img_url = 'https://api.thaiproperty.in.th/api/images/image/' + post_id
                    r = self.sess.post(img_url, headers=headers, data={}, files=datapost)
                    print(r.url)
                    print(r.status_code)

                # if len(allimages) == 1:
                #     img_url = 'https://api.thaiproperty.in.th/api/images/image/' + post_id
                #     r = self.session.http_post(img_url, headers=headers, data={}, files=[])
                #     print(r.url)
                #     print(r.status_code)

                if result:
                    success = True
                    detail = "Post edited successfully"
                else:
                    success = False
                    detail = "Couldnot edit post"
            else:
                success = False
                detail = "No post with given post_id"

        else:
            success = False
            detail = "Couldnot login"

        time_end = datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": self.webname,
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": postdata["post_id"],
            "account_type": "null",
            "detail": detail,
        }

    def boost_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.utcnow()

        test_login = self.test_login(postdata)
        authtoken = self.authtoken
        # print(authtoken)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""

        if success:

            post_found = False

            headers = {
                'authority': 'api.thaiproperty.in.th',
                'accept': '*/*',
                'access-control-request-method': 'GET',
                'access-control-request-headers': 'authorization',
                'origin': 'https://www.thaiproperty.in.th',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.thaiproperty.in.th/account/manage',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
            }

            params = (
                ('limit', '200'),
            )

            r = self.sess.options('https://api.thaiproperty.in.th/api/posts/manage', headers=headers,
                                        params=params)
            print(r.url)
            print(r.status_code)

            headers = {
                'authority': 'api.thaiproperty.in.th',
                'authorization': 'Bearer ' + self.authtoken,
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                'accept': '*/*',
                'origin': 'https://www.thaiproperty.in.th',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.thaiproperty.in.th/account/manage',
                'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
            }

            params = (
                ('limit', '200'),
            )

            r = self.sess.get('https://api.thaiproperty.in.th/api/posts/manage', headers=headers, params=params)
            print(r.url)
            print(r.status_code)
            all_posts = r.json()

            #with open('/home/codelover/Desktop/rough.html', 'w') as f:
            #    f.write(r.text)

            # soup = BeautifulSoup(r.content, self.parser)
            # all_posts = soup.find('div', 'mt-3 list-container row').findChildren('div', 'col-12 col-md-6 col-xl-4')
            # print(all_posts)

            for post in all_posts:
                post_id = str(post['postId'])
                print(post_id)
                if post_id == postdata['post_id']:
                    post_found = True
                    break

            if post_found:

                # headers = {
                #     'authority': 'api.thaiproperty.in.th',
                #     'accept': '*/*',
                #     'access-control-request-method': 'GET',
                #     'access-control-request-headers': 'authorization',
                #     'origin': 'https://www.thaiproperty.in.th',
                #     'sec-fetch-mode': 'cors',
                #     'sec-fetch-site': 'same-site',
                #     'sec-fetch-dest': 'empty',
                #     'referer': 'https://www.thaiproperty.in.th/newpost',
                #     'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                #     'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                # }
                #
                # # O1
                # r = self.sess.options('https://api.thaiproperty.in.th/api/accounts/profile', headers=headers)
                # print(r.status_code)
                #
                # headers = {
                #     'authority': 'api.thaiproperty.in.th',
                #     'accept': '*/*',
                #     'access-control-request-method': 'GET',
                #     'access-control-request-headers': 'authorization,content-type',
                #     'origin': 'https://www.thaiproperty.in.th',
                #     'sec-fetch-mode': 'cors',
                #     'sec-fetch-site': 'same-site',
                #     'sec-fetch-dest': 'empty',
                #     'referer': 'https://www.thaiproperty.in.th/newpost',
                #     'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                #     'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                # }
                #
                # # O2
                # r = self.sess.options('https://api.thaiproperty.in.th/api/favorites', headers=headers)
                # print(r.status_code)
                #
                # headers = {
                #     'authority': 'api.thaiproperty.in.th',
                #     'accept': '*/*',
                #     'access-control-request-method': 'GET',
                #     'access-control-request-headers': 'authorization,content-type',
                #     'origin': 'https://www.thaiproperty.in.th',
                #     'sec-fetch-mode': 'cors',
                #     'sec-fetch-site': 'same-site',
                #     'sec-fetch-dest': 'empty',
                #     'referer': 'https://www.thaiproperty.in.th/newpost',
                #     'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                #     'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                # }
                #
                # # O3
                # r = self.sess.options('https://api.thaiproperty.in.th/api/notifications/user', headers=headers)
                # print(r.status_code)
                #
                # headers = {
                #     'authority': 'api.thaiproperty.in.th',
                #     'accept': '*/*',
                #     'access-control-request-method': 'GET',
                #     'access-control-request-headers': 'authorization',
                #     'origin': 'https://www.thaiproperty.in.th',
                #     'sec-fetch-mode': 'cors',
                #     'sec-fetch-site': 'same-site',
                #     'sec-fetch-dest': 'empty',
                #     'referer': 'https://www.thaiproperty.in.th/newpost',
                #     'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                #     'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                # }
                #
                # # O4
                # r = self.sess.options('https://api.thaiproperty.in.th/api/posts/check', headers=headers)
                # print(r.status_code)
                #
                # headers = {
                #     'authority': 'api.thaiproperty.in.th',
                #     'accept': 'application/json',
                #     'authorization': 'Bearer ' + self.authtoken,
                #     'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                #     'origin': 'https://www.thaiproperty.in.th',
                #     'sec-fetch-site': 'same-site',
                #     'sec-fetch-mode': 'cors',
                #     'sec-fetch-dest': 'empty',
                #     'referer': 'https://www.thaiproperty.in.th/newpost',
                #     'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                # }
                #
                # # G1
                # r = self.sess.get('https://api.thaiproperty.in.th/api/accounts/profile', headers=headers)
                # print(r.status_code)
                # print(r.text)
                #
                # headers = {
                #     'authority': 'api.thaiproperty.in.th',
                #     'accept': 'application/json',
                #     'authorization': 'Bearer ' + self.authtoken,
                #     'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                #     'content-type': 'application/json',
                #     'origin': 'https://www.thaiproperty.in.th',
                #     'sec-fetch-site': 'same-site',
                #     'sec-fetch-mode': 'cors',
                #     'sec-fetch-dest': 'empty',
                #     'referer': 'https://www.thaiproperty.in.th/newpost',
                #     'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                # }
                #
                # # G2
                # r = self.sess.get('https://api.thaiproperty.in.th/api/favorites', headers=headers)
                # print(r.status_code)
                #
                # headers = {
                #     'authority': 'api.thaiproperty.in.th',
                #     'accept': 'application/json',
                #     'authorization': 'Bearer ' + self.authtoken,
                #     'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                #     'content-type': 'application/json',
                #     'origin': 'https://www.thaiproperty.in.th',
                #     'sec-fetch-site': 'same-site',
                #     'sec-fetch-mode': 'cors',
                #     'sec-fetch-dest': 'empty',
                #     'referer': 'https://www.thaiproperty.in.th/newpost',
                #     'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                # }
                #
                # # G3
                # r = self.sess.get('https://api.thaiproperty.in.th/api/notifications/user', headers=headers)
                # print(r.status_code)
                #
                # headers = {
                #     'authority': 'api.thaiproperty.in.th',
                #     'authorization': 'Bearer ' + self.authtoken,
                #     'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                #     'accept': '*/*',
                #     'origin': 'https://www.thaiproperty.in.th',
                #     'sec-fetch-site': 'same-site',
                #     'sec-fetch-mode': 'cors',
                #     'sec-fetch-dest': 'empty',
                #     'referer': 'https://www.thaiproperty.in.th/newpost',
                #     'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                # }
                #
                # # G4
                # r = self.sess.get('https://api.thaiproperty.in.th/api/posts/check', headers=headers)
                # print(r.url)
                # print(r.status_code)
                # print(r.text)
                #
                # datapost = [
                #     ('formtype', (None, 'edit')),
                #     ('postId', (None, post_id)),
                #     ("isSold", (None, 'false')),
                #     ("places", (None, ',,,,,'))
                # ]
                # #
                # # if postdata['property_type'] != '6':
                # #     datapost.append(("bedRoom", (None, str(postdata['bed_room']))))
                # #     datapost.append(("bathRoom", (None, str(postdata['bath_room']))))
                #
                # # print(datapost)
                #
                # headers = {
                #     'authority': 'api.thaiproperty.in.th',
                #     'accept': '*/*',
                #     'access-control-request-method': 'POST',
                #     'access-control-request-headers': 'authorization',
                #     'origin': 'https://www.thaiproperty.in.th',
                #     'sec-fetch-mode': 'cors',
                #     'sec-fetch-site': 'same-site',
                #     'sec-fetch-dest': 'empty',
                #     'referer': 'https://www.thaiproperty.in.th/editpost/' + post_id,
                #     'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                #     'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                # }
                #
                # print(datapost)
                #
                # post_url = 'https://api.thaiproperty.in.th/api/posts/' + post_id
                # r = self.sess.options(post_url, headers=headers)
                # print(r.url)
                # print(r.status_code)
                #
                # # token = 'eyJhbGciOiJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzA0L3htbGRzaWctbW9yZSNobWFjLXNoYTI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdGRyIiwianRpIjoiYzZmYjI4YzItNjY5My00NzZjLWI3ZmUtYmZkZjIzMThmZWYzIiwiaWF0IjoxNTk0ODkxMTg3LCJyb2wiOiJVc2VyIiwiaWQiOiJhMThhNzE4Yy0zZTA4LTRjZjAtOTM0ZS0wZWU1NGFlNzNmMzgiLCJuYmYiOjE1OTQ4OTExODcsImV4cCI6MTU5NTIzNjc4NywiaXNzIjoiVGhhaVByb3BlcnR5IiwiYXVkIjoiaHR0cHM6Ly9hcGkudGhhaXByb3BlcnR5LmluLnRoLyJ9.VYnM3gdX97XGaQbVAjjdiMlPDn41pLOZRaLLtqNnl4g'
                #
                # headers = {
                #     'authority': 'api.thaiproperty.in.th',
                #     'accept': 'application/json, text/plain, */*',
                #     'authorization': 'Bearer ' + self.authtoken,
                #     'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                #     'origin': 'https://www.thaiproperty.in.th',
                #     'sec-fetch-site': 'same-site',
                #     'sec-fetch-mode': 'cors',
                #     'sec-fetch-dest': 'empty',
                #     'referer': 'https://www.thaiproperty.in.th/editpost/' + post_id,
                #     'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                # }
                #
                # print(headers)
                #
                # r = self.sess.put(post_url, headers=headers, data={}, files=datapost)
                # data = r.json()
                # print(r.url)
                # print(r.status_code)
                # print(data)
                #
                # result = data['status']
                # print(r)
                # print(r.raise_for_status())

                # with open('/home/codelover/Desktop/rough.html', 'w') as f:
                #     f.write(data)

                # edit_url = 'https://api.thaiproperty.in.th/api/posts/' + post_id
                # r = self.sess.get(edit_url)
                # print(r.url)
                # print(r.status_code)

                # soup = BeautifulSoup(r.content, self.parser)
                # old_images = soup.find_all('img', 'ant-upload-list-item-image')
                # print(old_images)
                #
                # for i, img in enumerate(old_images):
                #     info = img.get('src').split('/')
                #     if i == 0:
                #         del_url = 'https://api.thaiproperty.in.th/api/images/logoimage/'+info[-2]+'/'+info[-1]+'?PostId='+postdata['post_id']
                #     else:
                #         del_url = 'https://api.thaiproperty.in.th/api/images/image/' + info[-2] + '/' + info[-1] + '?PostId=' + postdata['post_id']
                #     r = self.sess.delete(del_url)
                #     print(r.url)
                #     print(r.status_code)

                # datapost = []
                # myfiles = []

                # postdata['post_images'] = ['/home/codelover/Desktop/Ignis/h1.jpeg', '/home/codelover/Desktop/Ignis/h2.jpeg']
                # allimages = postdata["post_images"]
                #
                # for i in range(len(allimages)):
                #     # r = open(allimages[i], 'rb')
                #     filename = str(i) + '.jpeg'
                #     print(filename)
                #     # datapost['akbzkyacxeaa'+str(i+1)]=r
                #     # print(r.name)
                #     # datapost.append(("files",(r.name,r, 'image/'+r.name.split('.')[-1])))
                #     headers = {
                #         'authority': 'api.thaiproperty.in.th',
                #         'authorization': 'Bearer ' + self.authtoken,
                #         'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                #         'accept': '*/*',
                #         'origin': 'https://www.thaiproperty.in.th',
                #         'sec-fetch-site': 'same-site',
                #         'sec-fetch-mode': 'cors',
                #         'sec-fetch-dest': 'empty',
                #         'referer': 'https://www.thaiproperty.in.th/editimage/' + post_id,
                #         'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                #     }
                #     datapost = [("files", (filename, open(allimages[i], 'rb'), 'image/jpeg'))]
                #     if i == 0:
                #         img_url = 'https://api.thaiproperty.in.th/api/images/logoimage/' + post_id
                #     else:
                #         img_url = 'https://api.thaiproperty.in.th/api/images/image/' + post_id
                #     r = self.session.http_post(img_url, headers=headers, data={}, files=datapost)
                #     print(r.url)
                #     print(r.status_code)
                #
                # if len(allimages) == 1:
                #     img_url = 'https://api.thaiproperty.in.th/api/images/image/' + post_id
                #     r = self.session.http_post(img_url, headers=headers, data={}, files=[])
                #     print(r.url)
                #     print(r.status_code)

                success = False
                detail = "No option to boost post"
            else:
                success = False
                detail = "No post with given post_id"

        else:
            success = False
            detail = "Couldnot login"

        time_end = datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": self.webname,
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
        }

    def delete_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.utcnow()

        test_login = self.test_login(postdata)
        authtoken = self.authtoken
        # print(authtoken)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""

        if success:

            post_found = False

            headers = {
                'authority': 'api.thaiproperty.in.th',
                'accept': '*/*',
                'access-control-request-method': 'GET',
                'access-control-request-headers': 'authorization',
                'origin': 'https://www.thaiproperty.in.th',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.thaiproperty.in.th/account/manage',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
            }

            params = (
                ('limit', '200'),
            )

            r = self.sess.options('https://api.thaiproperty.in.th/api/posts/manage', headers=headers,
                                        params=params)
            print(r.url)
            print(r.status_code)

            headers = {
                'authority': 'api.thaiproperty.in.th',
                'authorization': 'Bearer ' + self.authtoken,
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                'accept': '*/*',
                'origin': 'https://www.thaiproperty.in.th',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.thaiproperty.in.th/account/manage',
                'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
            }

            params = (
                ('limit', '200'),
            )

            r = self.sess.get('https://api.thaiproperty.in.th/api/posts/manage', headers=headers, params=params)
            print(r.url)
            print(r.status_code)
            all_posts = r.json()

            #with open('/home/codelover/Desktop/rough.html', 'w') as f:
            #    f.write(r.text)

            # soup = BeautifulSoup(r.content, self.parser)
            # all_posts = soup.find('div', 'mt-3 list-container row').findChildren('div', 'col-12 col-md-6 col-xl-4')
            # print(all_posts)

            for post in all_posts:
                post_id = str(post['postId'])
                print(post_id)
                if post_id == postdata['post_id']:
                    post_found = True
                    break

            if post_found:

                headers = {
                    'authority': 'api.thaiproperty.in.th',
                    'accept': '*/*',
                    'access-control-request-method': 'GET',
                    'access-control-request-headers': 'authorization',
                    'origin': 'https://www.thaiproperty.in.th',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://www.thaiproperty.in.th/newpost',
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                    'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                }

                # O1
                r = self.sess.options('https://api.thaiproperty.in.th/api/accounts/profile', headers=headers)
                print(r.status_code)

                headers = {
                    'authority': 'api.thaiproperty.in.th',
                    'accept': '*/*',
                    'access-control-request-method': 'GET',
                    'access-control-request-headers': 'authorization,content-type',
                    'origin': 'https://www.thaiproperty.in.th',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://www.thaiproperty.in.th/newpost',
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                    'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                }

                # O2
                r = self.sess.options('https://api.thaiproperty.in.th/api/favorites', headers=headers)
                print(r.status_code)

                headers = {
                    'authority': 'api.thaiproperty.in.th',
                    'accept': '*/*',
                    'access-control-request-method': 'GET',
                    'access-control-request-headers': 'authorization,content-type',
                    'origin': 'https://www.thaiproperty.in.th',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://www.thaiproperty.in.th/newpost',
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                    'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                }

                # O3
                r = self.sess.options('https://api.thaiproperty.in.th/api/notifications/user', headers=headers)
                print(r.status_code)

                headers = {
                    'authority': 'api.thaiproperty.in.th',
                    'accept': '*/*',
                    'access-control-request-method': 'GET',
                    'access-control-request-headers': 'authorization',
                    'origin': 'https://www.thaiproperty.in.th',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://www.thaiproperty.in.th/newpost',
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                    'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                }

                # O4
                r = self.sess.options('https://api.thaiproperty.in.th/api/posts/check', headers=headers)
                print(r.status_code)

                headers = {
                    'authority': 'api.thaiproperty.in.th',
                    'accept': 'application/json',
                    'authorization': 'Bearer ' + self.authtoken,
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                    'origin': 'https://www.thaiproperty.in.th',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://www.thaiproperty.in.th/newpost',
                    'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                }

                # G1
                r = self.sess.get('https://api.thaiproperty.in.th/api/accounts/profile', headers=headers)
                print(r.status_code)
                print(r.text)

                headers = {
                    'authority': 'api.thaiproperty.in.th',
                    'accept': 'application/json',
                    'authorization': 'Bearer ' + self.authtoken,
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                    'content-type': 'application/json',
                    'origin': 'https://www.thaiproperty.in.th',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://www.thaiproperty.in.th/newpost',
                    'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                }

                # G2
                r = self.sess.get('https://api.thaiproperty.in.th/api/favorites', headers=headers)
                print(r.status_code)

                headers = {
                    'authority': 'api.thaiproperty.in.th',
                    'accept': 'application/json',
                    'authorization': 'Bearer ' + self.authtoken,
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                    'content-type': 'application/json',
                    'origin': 'https://www.thaiproperty.in.th',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://www.thaiproperty.in.th/newpost',
                    'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                }

                # G3
                r = self.sess.get('https://api.thaiproperty.in.th/api/notifications/user', headers=headers)
                print(r.status_code)

                headers = {
                    'authority': 'api.thaiproperty.in.th',
                    'authorization': 'Bearer ' + self.authtoken,
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                    'accept': '*/*',
                    'origin': 'https://www.thaiproperty.in.th',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://www.thaiproperty.in.th/newpost',
                    'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                }

                # G4
                r = self.sess.get('https://api.thaiproperty.in.th/api/posts/check', headers=headers)
                print(r.url)
                print(r.status_code)
                print(r.text)

                headers = {
                    'authority': 'api.thaiproperty.in.th',
                    'accept': '*/*',
                    'access-control-request-method': 'DELETE',
                    'access-control-request-headers': 'authorization',
                    'origin': 'https://www.thaiproperty.in.th',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://www.thaiproperty.in.th/editpost/' + post_id,
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                    'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                }

                post_url = 'https://api.thaiproperty.in.th/api/posts/' + post_id
                r = self.sess.options(post_url, headers=headers)
                print(r.url)
                print(r.status_code)

                # token = 'eyJhbGciOiJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzA0L3htbGRzaWctbW9yZSNobWFjLXNoYTI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdGRyIiwianRpIjoiYzZmYjI4YzItNjY5My00NzZjLWI3ZmUtYmZkZjIzMThmZWYzIiwiaWF0IjoxNTk0ODkxMTg3LCJyb2wiOiJVc2VyIiwiaWQiOiJhMThhNzE4Yy0zZTA4LTRjZjAtOTM0ZS0wZWU1NGFlNzNmMzgiLCJuYmYiOjE1OTQ4OTExODcsImV4cCI6MTU5NTIzNjc4NywiaXNzIjoiVGhhaVByb3BlcnR5IiwiYXVkIjoiaHR0cHM6Ly9hcGkudGhhaXByb3BlcnR5LmluLnRoLyJ9.VYnM3gdX97XGaQbVAjjdiMlPDn41pLOZRaLLtqNnl4g'

                headers = {
                    'authority': 'api.thaiproperty.in.th',
                    'authorization': 'Bearer ' + self.authtoken,
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                    'accept': '*/*',
                    'origin': 'https://www.thaiproperty.in.th',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://www.thaiproperty.in.th/editpost/' + post_id,
                    'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
                }

                r = self.sess.delete(post_url, headers=headers)
                data = r.json()
                print(r.url)
                print(r.status_code)
                print(data)

                result = data['status']

                if 'ทำการลบประกาศ' in result:
                    success = True
                    detail = "Post deleted successfully"
                else:
                    success = False
                    detail = "Couldnot delete post"
            else:
                success = False
                detail = "No post with given post_id"

        else:
            success = False
            detail = "Couldnot login"

        time_end = datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": self.webname,
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
        }

    def search_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.utcnow()

        test_login = self.test_login(postdata)
        authtoken = self.authtoken
        # print(authtoken)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""
        post_created = ''
        post_modified = ''
        post_viewed = ''

        if success:

            post_found = False

            headers = {
                'authority': 'api.thaiproperty.in.th',
                'accept': '*/*',
                'access-control-request-method': 'GET',
                'access-control-request-headers': 'authorization',
                'origin': 'https://www.thaiproperty.in.th',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.thaiproperty.in.th/account/manage',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
            }

            params = (
                ('limit', '200'),
            )

            r = self.sess.options('https://api.thaiproperty.in.th/api/posts/manage', headers=headers,
                                        params=params)
            print(r.url)
            print(r.status_code)

            headers = {
                'authority': 'api.thaiproperty.in.th',
                'authorization': 'Bearer ' + self.authtoken,
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                'accept': '*/*',
                'origin': 'https://www.thaiproperty.in.th',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.thaiproperty.in.th/account/manage',
                'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
            }

            params = (
                ('limit', '200'),
            )

            r = self.sess.get('https://api.thaiproperty.in.th/api/posts/manage', headers=headers, params=params)
            print(r.url)
            print(r.status_code)
            all_posts = r.json()

            #with open('/home/codelover/Desktop/rough.html', 'w') as f:
            #    f.write(r.text)

            # soup = BeautifulSoup(r.content, self.parser)
            # all_posts = soup.find('div', 'mt-3 list-container row').findChildren('div', 'col-12 col-md-6 col-xl-4')
            # print(all_posts)

            for post in all_posts:
                post_title = str(post['title'])
                print(post_title)
                if post_title in postdata['post_title_th'] or postdata['post_title_th'] in post_title:
                    post_found = True
                    post_id = str(post['postId'])
                    post_url = 'https://www.thaiproperty.in.th/p/' + post['title'].replace(' ', '-') + '-' + post_id
                    post_created = post['postDate']
                    post_viewed = str(post['totalView'])
                    post_modified = post['logoImageFile'].split('_')[0]
                    post_modified = post_modified[:4] + '-' + post_modified[4:6] + '-' + post_modified[6:]
                    success = True
                    detail = "Post Found"
                    break

            if not post_found:
                success = False
                detail = "No post with given post_title"

        else:
            success = False
            detail = "Couldnot login"

        time_end = datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": self.webname,
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "post_url": post_url,
            "post_created": post_created,
            "post_modified": post_modified,
            "post_view": post_viewed,
            "account_type": "null",
            "detail": detail,
        }

