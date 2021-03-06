import requests
import os
from .lib_httprequest import *
import string
from bs4 import BeautifulSoup
import os.path
# from urlparse import urlparse
import re
from .lib_captcha import *
import json
import datetime
import time
import sys
import shutil
from urllib.parse import unquote

# options = Options()
# options.set_headless(True)

    # executable_path='/usr/bin/chromedriver', options=options)

# with open("./static/ploychao_province.json") as f:
#     provincedata = json.load(f)

captcha = lib_captcha()
class bankumka():

    name = 'bankumka'

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

    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']
        name_th = postdata["name_th"]
        surname_th = postdata["surname_th"]
        mobile_no = postdata["tel"]
        # start process
        success = "true"
        detail = ""
        # r = self.httprequestObj.http_get('https://bankumka.com/access/register/checker',verify = False)
        # print(r.content)
        r = self.httprequestObj.http_get(
            'https://bankumka.com/themes/default/assets/js/member/register.js', verify=False)
        # print(r.text)
        datapost = {
            'user_class': '2',
            'company': user,
            'email': user,
            'password': passwd,
            'password2': passwd,
            'first_name': name_th,
            'last_name': surname_th,
            'phone': mobile_no,
            'token': ''
        }
        r = self.httprequestObj.http_post(
            'https://bankumka.com/access/register/checker', data=datapost)
        # print(r.text)
        # r = self.httprequestObj.http_get('https://bankumka.com/access',verify= False)
        # print(type(r.text))
        # data = r.text
        data = json.loads(r.text)
        # print(data)
        # print(data["token"])
        if data['status'] == 'OK':
            datapost = {
                'user_class': '1',
                'company': '',
                'email': user,
                'password': passwd,
                'password2': passwd,
                'first_name': name_th,
                'last_name': surname_th,
                'phone': mobile_no,
                'token': data['token']
            }
            # for i in r.text:
            #     print(i.token)

            r = self.httprequestObj.http_post(
                'https://bankumka.com/access/register', data=datapost)
        # print("yes")
            # print(r.text)
        # print(data)
            if r.status_code == 404:
                detail = "Can't register"
                success = "false"
            else:
                detail = "Registered"
                # r = self.httprequestObj.http_get('https://bankumka.com/access/register/success',verify = False)
                # print(r.text)
        # # end process
        else:
            success = "false"
            detail = "Can't register. Is password >9 chars?"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename":"bankumka",
            "success": success,
            'ds_id': postdata['ds_id'],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "ds_id": postdata['ds_id']
        }

    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']

        success = "true"
        detail = ""

        datapost = {
            'email': user,
            'password': passwd,
            'submit': ''
        }

        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
        }

        res = self.httprequestObj.http_get('https://bankumka.com/access/logout', headers=headers)

        r = self.httprequestObj.http_post(
            'https://bankumka.com/access', data=datapost)
        
        data = r.text
        # print(data)
        # print(r.text)
        if data.find("????????????????????????????????????????????????????????????????????????????????? ???????????????????????????????????????????????????????????? !!") != -1:
            detail = "cannot login"
            success = "false"
        else:
            detail = "login successfull"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename":"bankumka",
            "success": success,
            "start_time": str(time_start),
            "ds_id": postdata['ds_id'],
            "end_time": str(time_end),
            "detail": detail,
            "ds_id": postdata['ds_id']
        }



    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        theurl = ""
        post_id = ""
        # print(postdata['mobile'])

        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        ashopname = test_login["detail"]

        getProdId = {'1': 2, '2': 1, '3': 1, '4': 3, '5': 4,
                     '6': 5, '7': 37, '8': 37, '9': 37, '10': 37, '25': 37}
        try:
            theprodid = getProdId[str(postdata['property_type'])]
        except:
            theprodid = ''
    
        province_id = '0'
        detail = "cannot login"
        amphur_id = '26'
        tumbon_id = '01'
        prod_address = ""
        for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
            if add is not None:
                prod_address += add
        prod_address = prod_address[:-1]
        print(success,"lol")
        if success == "true":
            detail = ""
            r = self.httprequestObj.http_get(
                'https://bankumka.com/property/announce', verify=False)
            data = r.text
            # print(data)
            soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
            alls = soup.findAll("option")

            province_found = False
            for i in alls:
                if postdata['addr_province'].replace(" ","").strip() == i.get_text().replace(" ","").strip():
                    province_id = i['value']
                    province_found = True
                    break
            if province_found is False:
                for i in alls:
                    if postdata['addr_province'].replace(" ","").find(i.get_text()) != -1 or i.get_text().replace(" ","").find(postdata['addr_province']) != -1:
                        province_id = i['value']
                        province_found = True
                        break
                if province_found is False:
                    province_id = data[0]['id']

                # print(i)
                # print(i.get_text())
                # print("data: "+i.text+" value: "+i.value)
            # print(province_id)
            query_string = 'https://bankumka.com/ajax/listcities/'+province_id
            r = self.httprequestObj.http_get(
                query_string, verify=False)
            data = json.loads(r.text)
            # print(data)
            amphur_found = False
            for i in data:
                if '?????????' in i['name']:
                        i['name'] = i['name'].replace('?????????', '')
                # print(i['name'])
                if postdata['addr_district'].replace(" ","") == i['name']:
                    amphur_found = True
                    amphur_id = i['id']
                    break
            if amphur_found is False:
                for i in data:
                    if postdata['addr_district'].replace(" ","").find(i['name']) != -1 or i['name'].find(postdata['addr_district'].replace(" ","")) != -1:
                        amphur_id = i['id']
                        amphur_found = True
                        break
                if amphur_found is False:
                    amphur_id = data[0]['id']

            # print(amphur_id)
            query_string = 'https://bankumka.com/ajax/listcities/'+amphur_id
            r = self.httprequestObj.http_get(
                query_string, verify=False)
            data = json.loads(r.text)
            # print(data)
            tumbon_found = False
            for i in data:
                if postdata['addr_sub_district'] == i['name']:
                    tumbon_id = i['id']
                    tumbon_found = True
                    break
            if tumbon_found is False:
                for i in data:
                    if postdata['addr_sub_district'].replace(" ","").find(i['name']) != -1 or i['name'].find(postdata['addr_sub_district'].replace(" ","")) != -1:
                        tumbon_id = i['id']
                        tumbon_found = True
                        break
                if tumbon_found is False:
                    tumbon_id = data[0]['id']


            # print(tumbon_id)
            # browser.get("https://bankumka.com/property/announce")
            # csrf_token = browser.find_element_by_name("csrf_token").get_attribute("value")
            # csrf_time = browser.find_element_by_name("csrf_time").get_attribute("value")
            # print(csrf_time)
            if 'web_project_name' in postdata and postdata['web_project_name'] is not None:
                project_n = postdata['web_project_name']
            elif 'project_name' in postdata and postdata['project_name'] is not None:
                project_n = postdata['project_name']
            else:
                project_n = postdata['post_title_th']

            mydata = {
                'query': project_n
            }
            resp = self.httprequestObj.http_post('https://bankumka.com/ajax/listproject/', data=mydata)
            allres = json.loads(resp.content.decode('utf-8'))["suggestions"]
            project_id = '0'

            if len(allres) != 0:
                project_id = allres[0]['data']
                project_n = allres[0]["value"]

                mydata = {'id':project_id}
                resp1 = self.httprequestObj.http_post("https://bankumka.com/ajax/getLocationProject/", data=mydata)
                res1 = json.loads(resp1.content.decode('utf-8'))['result']

                postdata["geo_longitude"] = res1["project_lng"]
                postdata["geo_latitude"] = res1["project_lat"]
                province_id = res1["project_province"]
                amphur_id = res1["project_district"]
                tumbon_id = res1["project_subdistrict"]
            
            r = self.httprequestObj.http_get('https://bankumka.com/property/announce')
            soup = BeautifulSoup(r.text, features=self.parser)
            csrf_time = soup.find(attrs={'name': 'csrf_time'})
            csrf_token = soup.find(attrs={'name': 'csrf_token'})
            if csrf_time:
                csrf_time = csrf_time.get('value')
            if csrf_token:
                csrf_token = csrf_token.get('value') 

            datapost = [
                ('timeout', '5'),
                ('prop_name', postdata['post_title_th'][:119]),
                ('prop_type', '32'),
                ('prop_cate', theprodid),
                ('prop_detail', postdata['post_description_th']),
                ('prop_show_email', '1'),
                ('prop_email', postdata['email']),
                ('prop_contact', str(postdata['mobile']).replace('-','')),
                ('prop_line_id', ''),
                ('prop_price', postdata['price_baht']),
                ('prop_price_attr', '47'),
                ('prop_pricerent', ''),
                ('prop_pricerent_attr', '51'),
                ('prop_bedroom_type', '0'),
                ('prop_bedroom', postdata['bed_room']),
                ('prop_bathroom', postdata['bath_room']),
                ('prop_livingroom', ''),
                ('prop_kitchen', ''),
                ('prop_parking', ''),
                ('prop_floor', postdata['floor_total']),
                ('prop_mainroad', '1'),
                ('prop_project_name', project_n),
                ('prop_project', project_id),
                ('prop_project_old', '0'),
                ('project_prop_province', province_id),
                ('project_prop_district', amphur_id),
                ('project_prop_subdistrict', tumbon_id),
                ('prop_soi', postdata['addr_soi']),
                ('prop_road', postdata['addr_road']),
                ('prop_province', province_id),
                ('prop_district', amphur_id),
                ('prop_subdistrict', tumbon_id),
                ('prop_zipcode', ''),
                ('prop_lat', postdata['geo_latitude']),
                ('prop_lng', postdata['geo_longitude']),
                ('facility[]', ''),
                ('prop_gallary1', ''),
                ('prop_gallary2', ''),
                ('prop_gallary3', ''),
                ('prop_gallary4', ''),
                ('prop_gallary5', ''),
                ('prop_gallary6', ''),
                ('prop_gallary7', ''),
                ('prop_gallary8', ''),
                ('prop_gallary9', ''),
                ('prop_gallary10', ''),
                ('drag', '0'),
                ('token', ''),
                ('csrf_time', csrf_time),
                ('csrf_token', csrf_token),
                ('action', 'insert'),
                ('prop_id', '0')
            ]

            if theprodid == 2:
                datapost.append(('prop_area_rai', ''))
                datapost.append(('prop_area_ngan', ''))
                datapost.append(('prop_area_sqm', ''))
                datapost.append(('prop_space', postdata['floor_area']))
            elif theprodid == 5:
                datapost.append(('prop_area_rai', postdata['land_size_rai']))
                datapost.append(('prop_area_ngan', postdata['land_size_ngan']))
                datapost.append(('prop_area_sqm', postdata['land_size_wa']))
                datapost.append(('prop_space', ''))
            else:
                datapost.append(('prop_area_rai', postdata['land_size_rai']))
                datapost.append(('prop_area_ngan', postdata['land_size_ngan']))
                datapost.append(('prop_area_sqm', postdata['land_size_wa']))
                datapost.append(('prop_space', postdata['floor_area']))
            if postdata['listing_type'] == '????????????':
                datapost[2] = ('prop_type', 33)
                datapost[9] = ('prop_price', '')
                datapost[11] = ('prop_pricerent', postdata['price_baht'])
            else:
                datapost[2] = ('prop_type', 32)
                datapost[11] = ('prop_pricerent', '')
                datapost[9] = ('prop_price', postdata['price_baht'])
            # print(datapost)
            r = self.httprequestObj.http_post(
                'https://bankumka.com/ajax/checkProperty', data=datapost)
            data = json.loads(r.text)
            print(data)
            if data['status'] == 'OK':
                g_response = captcha.reCaptcha('6Lfkov8cAAAAAOcHJBr2mND2B7xEKS3dJUJXlksm', 'https://bankumka.com')
                datapost = [
                    ('timeout', '5'),
                    ('prop_name', postdata['post_title_th'][:119]),
                    ('prop_type', '32'),
                    ('prop_cate', theprodid),
                    ('prop_detail', postdata['post_description_th']),
                    ('prop_show_email', '1'),
                    ('prop_email', postdata['user']),
                    ('prop_contact', str(postdata['mobile']).replace('-','')),
                    ('prop_line_id', ''),
                    ('prop_price', postdata['price_baht']),
                    ('prop_price_attr', '47'),
                    ('prop_pricerent', ''),
                    ('prop_pricerent_attr', '51'),
                    ('prop_bedroom_type', '0'),
                    ('prop_bedroom', postdata['bed_room']),
                    ('prop_bathroom', postdata['bath_room']),
                    ('prop_livingroom', ''),
                    ('prop_kitchen', ''),
                    ('prop_parking', ''),
                    ('prop_floor', postdata['floor_total']),
                    ('prop_mainroad', '1'),
                    ('prop_project_name', project_n),
                    ('prop_project', project_id),
                    ('prop_project_old', '0'),
                    ('project_prop_province', province_id),
                    ('project_prop_district', amphur_id),
                    ('project_prop_subdistrict', tumbon_id),
                    ('prop_soi', postdata['addr_soi']),
                    ('prop_road', postdata['addr_road']),
                    ('prop_province', province_id),
                    ('prop_district', amphur_id),
                    ('prop_subdistrict', tumbon_id),
                    ('prop_zipcode', ''),
                    ('prop_lat', postdata['geo_latitude']),
                    ('prop_lng', postdata['geo_longitude']),
                    ('facility[]', ''),
                    ('drag', '0'),
                    ('token', data['token']),
                    ('g_token',g_response),
                    ('csrf_time', csrf_time),
                    ('csrf_token', csrf_token),
                    ('action', 'insert'),
                    ('prop_id', '0')
                ]

                if theprodid == 2:
                    datapost.append(('prop_area_rai', ''))
                    datapost.append(('prop_area_ngan', ''))
                    datapost.append(('prop_area_sqm', ''))
                    datapost.append(('prop_space', postdata['floor_area']))
                elif theprodid == 5:
                    datapost.append(
                        ('prop_area_rai', postdata['land_size_rai']))
                    datapost.append(
                        ('prop_area_ngan', postdata['land_size_ngan']))
                    datapost.append(
                        ('prop_area_sqm', postdata['land_size_wa']))
                    datapost.append(('prop_space', ''))
                else:
                    datapost.append(
                        ('prop_area_rai', postdata['land_size_rai']))
                    datapost.append(
                        ('prop_area_ngan', postdata['land_size_ngan']))
                    datapost.append(
                        ('prop_area_sqm', postdata['land_size_wa']))
                    datapost.append(('prop_space', postdata['floor_area']))
                if postdata['listing_type'] == '????????????':
                    datapost[2] = ('prop_type', 33)
                    datapost[9] = ('prop_price', '')
                    datapost[11] = ('prop_pricerent', postdata['price_baht'])
                else:
                    datapost[2] = ('prop_type', 32)
                    datapost[11] = ('prop_pricerent', '')
                    datapost[9] = ('prop_price', postdata['price_baht'])
                files = {}
                # for i, myimg in enumerate(postdata['post_images'][:10]):
                for i in range(len(postdata['post_images'])):
                # for i in range(len(postdata["post_img_url_lists"])):
                    # resp = self.httprequestObj.http_get(
                    #     postdata["post_img_url_lists"][i], stream=True)
                    # resp.raw.decode_content = True
                    # with open('image'+str(i)+'.jpg', 'wb') as lfile:
                    #     shutil.copyfileobj(resp.raw, lfile)
                    # os.rename(postdata['post_images'][i],postdata['post_images'][i].replace('jpeg','jpg'))
                    r = (postdata['post_images'][i].replace('jpeg','jpg'), open(postdata['post_images'][i], 'rb'), "image/jpg")
                    print(r)
                    if i > 10:
                        break
                    # else:
                    files["prop_gallery"+str(i+1)] = r
                    val = {
                        "filename": postdata['post_images'][i].replace("jpeg","jpg"),
                        "Content-Type": 'image/jpg'
                    }
                    datapost.append(('prop_gallery'+str(i+1), val))
                
                r = self.httprequestObj.http_post(
                    'https://bankumka.com/property/save', data=datapost, files=files)
                # print(r.text)
                data = r.text
                soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
                post_id = soup.find("input", {"name": "prop_id"})['value']
                # print(post_id)
                if post_id != '':
                    r = self.httprequestObj.http_get(
                        'https://bankumka.com/member/properties', verify=False)
                    data = r.text
                    soup = BeautifulSoup(
                        data, self.parser, from_encoding='utf-8')
                    all = soup.findAll("a", {"class": "my-property-name"})
                    for i in all:
                        if (i.get_text()).find(post_id) != -1:
                            theurl += i['href']
            else:
                # print(data[message])
                success = "false"
                # if data['message'][0].find("10") != -1:
                #     detail = "Posts Limit Reached"
                # else:
                detail = str(data['message'])     
                theurl = ""
        else:

            # print("wrong_id")
            success = "false"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "websitename":"bankumka",
            "success": success,
            "detail": detail,
            "start_time": str(time_start),
            "ds_id": postdata['ds_id'],
            "end_time": str(time_end),
            "post_url": theurl,
            "post_id": post_id,
            "account_type": "null",
        }

    def edit_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        theurl = ""
        post_id = ""
        detail = ""
        posturl = ""
        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        getProdId = {'1': 2, '2': 1, '3': 1, '4': 3, '5': 4,
                     '6': 5, '7': 37, '8': 37, '9': 37, '10': 37, '25': 37}
        try:
            theprodid = getProdId[str(postdata['property_type'])]
        except:
            theprodid = ''

        # for (key, value) in provincedata.items():
        #     if type(value) is str and postdata['addr_province'].strip() in value.strip():
        #         province_id = key
        #         break

        # for (key, value) in provincedata[province_id+"_province"].items():
        #     if postdata['addr_district'].strip() in value.strip():
        #         amphur_id = key
        #         break
        province_id = '10'
        amphur_id = '26'
        prod_address = ""
        tumbon_id = '01'
        for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
            if add is not None:
                prod_address += add
        prod_address = prod_address[:-1]
        if 'web_project_name' in postdata and postdata['web_project_name'] is not None:
            project_n = postdata['web_project_name']
        elif 'project_name' in postdata and postdata['project_name'] is not None:
            project_n = postdata['project_name']
        else:
            project_n = postdata['post_title_th']
        mydata = {
            'query': project_n
        }
        resp = self.httprequestObj.http_post('https://bankumka.com/ajax/listproject/', data=mydata)
        allres = json.loads(resp.content.decode('utf-8'))["suggestions"]
        project_id = '0'
        # print( json.loads(resp.content.decode('utf-8')))
        if len(allres) != 0:
            project_id = allres[0]['data']
            project_n = allres[0]["value"]

            mydata = {'id':project_id}
            resp1 = self.httprequestObj.http_post("https://bankumka.com/ajax/getLocationProject/", data=mydata)
            res1 = json.loads(resp1.content.decode('utf-8'))['result']

            postdata["geo_longitude"] = res1["project_lng"]
            postdata["geo_latitude"] = res1["project_lat"]
            province_id = res1["project_province"]
            amphur_id = res1["project_district"]
            tumbon_id = res1["project_subdistrict"]
            # print(f'tumbon_id--{tumbon_id}')

        if success == "true":
            r = self.httprequestObj.http_get(
                'https://bankumka.com/member/properties', verify=False)
            data = r.content
            soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
            try:
                all_page=len(soup.find('select',{'name':'pageNo'}).find_all('option'))
            except:
                all_page = 1
            for i in range(1,all_page+1):
                r = self.httprequestObj.http_get(
                'https://bankumka.com/member/properties/page/{}'.format(i), verify=False)
                data = r.content
                soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
                all = soup.find_all("a", {"class": "my-property-name"})
                posturl = ""
                for i in all:
                    if postdata['post_id'] in i.get_text():
                        posturl += i['href']
                        break
                if (posturl != ''):
                    post_url = posturl
                    posturl += '/edit'
                    break
            if(posturl == '/edit'):
                success = False
                posturl = ''
                detail = "The post doesn't exist"
            else:
                r = self.httprequestObj.http_get(
                    posturl, verify=False)
                data = r.content
                soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
                alls = soup.find_all("option")
                province_found = False
                for i in alls:
                    if postdata['addr_province'].replace(" ","").strip() == i.get_text().replace(" ","").strip():
                        province_id = i['value']
                        province_found = True
                        break
                if province_found is False:
                    for i in alls:
                        if postdata['addr_province'].replace(" ","").find(i.get_text()) != -1 or i.get_text().replace(" ","").find(postdata['addr_province']) != -1:
                            province_id = i['value']
                            break
                    # print(i)
                    # print(i.get_text())
                    # print("data: "+i.text+" value: "+i.value)
                query_string = 'https://bankumka.com/ajax/listcities/'+province_id
                r = self.httprequestObj.http_get(
                    query_string, verify=False)
                data = json.loads(r.text)
                amphur_found = False
                for i in data:
                    #If '?????????' contain in data, need to be remove for more accuracy compare
                    if '?????????' in i['name']:
                        i['name'] = i['name'].replace('?????????', '')
                    if postdata['addr_district'].replace(" ","") == i['name']:      
                        amphur_found = True
                        amphur_id = i['id']
                        break
                if amphur_found is False:
                    for i in data:
                        if postdata['addr_district'].replace(" ","").find(i['name']) != -1 or i['name'].find(postdata['addr_district'].replace(" ","")) != -1:
                            amphur_id = i['id']
                            break
                query_string = 'https://bankumka.com/ajax/listcities/'+amphur_id
                r = self.httprequestObj.http_get(
                    query_string, verify=False)
                data = json.loads(r.text)
                tumbon_found = False
                for i in data:
                    print(i['name'])
                    if postdata['addr_sub_district'] == i['name']:
                        tumbon_id = i['id']
                        print('1' + i['name'])
                        tumbon_found = True
                        break
                if tumbon_found is False:
                    for i in data:
                        if postdata['addr_sub_district'].replace(" ","").find(i['name']) != -1 or i['name'].find(postdata['addr_sub_district'].replace(" ","")) != -1:
                            tumbon_id = i['id']
                            print('2' + i['name'])
                            break
                print(tumbon_id)
                # browser.get(posturl)
                # try:
                #     csrf_token = browser.find_element_by_name("csrf_token").get_attribute("value")
                #     csrf_time = browser.find_element_by_name("csrf_time").get_attribute("value")
                # except:
                #     csrf_time = 0
                #     csrf_token = ''
                r = self.httprequestObj.http_get('https://bankumka.com/property/announce')
                soup = BeautifulSoup(r.text, features=self.parser)
                csrf_time = soup.find(attrs={'name': 'csrf_time'})
                csrf_token = soup.find(attrs={'name': 'csrf_token'})
                if csrf_time:
                    csrf_time = csrf_time.get('value')
                if csrf_token:
                    csrf_token = csrf_token.get('value')
                # print(csrf_time)
                floor_area_sqm = 0
                datapost = [
                    ('timeout', '5'),
                    ('prop_name', postdata['post_title_th'][:119]),
                    ('prop_type', '32'),
                    ('prop_cate', theprodid),
                    ('prop_detail', postdata['post_description_th']),
                    ('prop_contact', postdata['mobile']),
                    ('prop_line_id', ''),
                    ('prop_price', postdata['price_baht']),
                    ('prop_price_attr', 'baht'),
                    ('prop_pricerent', ''),
                    ('prop_pricerent_attr', 'baht'),
                    ('prop_bedroom_type', '0'),
                    ('prop_bedroom', postdata['bed_room']),
                    ('prop_bathroom', postdata['bath_room']),
                    ('prop_livingroom', ''),
                    ('prop_kitchen', ''),
                    ('prop_parking', ''),
                    ('prop_floor', postdata['floor_total']),
                    ('prop_mainroad', '1'),
                    ('prop_active', 1),
                    ('prop_reason', ''),
                    ('prop_cancel', ''),
                    ('prop_project_name', project_n),
                    ('prop_project', project_id),
                    ('prop_project_old', '0'),
                    ('project_prop_province', province_id),
                    ('project_prop_district', amphur_id),
                    ('project_prop_subdistrict', tumbon_id),
                    ('prop_soi', postdata['addr_soi']),
                    ('prop_road', postdata['addr_road']),
                    ('prop_province', province_id),
                    ('prop_district', amphur_id),
                    ('prop_subdistrict', tumbon_id),
                    ('prop_zipcode', ''),
                    ('prop_lat', postdata['geo_latitude']),
                    ('prop_lng', postdata['geo_longitude']),

                    ('facility[]', ''),
                    ('prop_gallary1', ''),
                    ('prop_gallary2', ''),
                    ('prop_gallary3', ''),
                    ('prop_gallary4', ''),
                    ('prop_gallary5', ''),
                    ('prop_gallary6', ''),
                    ('prop_gallary7', ''),
                    ('prop_gallary8', ''),
                    ('prop_gallary9', ''),
                    ('prop_gallary10', ''),
                    ('drag', '0'),
                    ('token', ''),
                    ('csrf_time', csrf_time),
                    ('csrf_token', csrf_token),
                    ('action', 'update'),
                    ('prop_id', postdata['post_id'])
                ]
                if theprodid == 2:
                    datapost.append(('prop_area_rai', ''))
                    datapost.append(('prop_area_ngan', ''))
                    datapost.append(('prop_area_sqm', ''))
                    datapost.append(('prop_space', postdata['floor_area']))
                elif theprodid == 5:
                    datapost.append(
                        ('prop_area_rai', postdata['land_size_rai']))
                    datapost.append(
                        ('prop_area_ngan', postdata['land_size_ngan']))
                    datapost.append(
                        ('prop_area_sqm', postdata['land_size_wa']))
                    datapost.append(('prop_space', ''))
                else:
                    datapost.append(
                        ('prop_area_rai', postdata['land_size_rai']))
                    datapost.append(
                        ('prop_area_ngan', postdata['land_size_ngan']))
                    datapost.append(
                        ('prop_area_sqm', postdata['land_size_wa']))
                    datapost.append(('prop_space', postdata['floor_area']))
                if postdata['listing_type'] == '????????????':
                    datapost[2] = ('prop_type', 33)
                    datapost[7] = ('prop_price', '')
                    datapost[9] = ('prop_pricerent', postdata['price_baht'])
                else:
                    datapost[2] = ('prop_type', 32)
                    datapost[9] = ('prop_pricerent', '')
                    datapost[7] = ('prop_price', postdata['price_baht'])
                r = self.httprequestObj.http_post(
                    'https://bankumka.com/ajax/checkProperty', data=datapost)
                data = json.loads(r.text)
                if data['status'] == 'OK':
                    g_response = captcha.reCaptcha('6Lfkov8cAAAAAOcHJBr2mND2B7xEKS3dJUJXlksm', 'https://bankumka.com')
                    datapost = [
                        ('timeout', '5'),
                        ('prop_name', postdata['post_title_th'][:119]),
                        ('prop_type', '32'),
                        ('prop_cate', theprodid),
                        ('prop_detail', postdata['post_description_th']),
                        ('prop_contact', postdata['mobile']),
                        ('prop_line_id', ''),
                        ('prop_price', postdata['price_baht']),
                        ('prop_price_attr', ''),
                        ('prop_pricerent', ''),
                        ('prop_pricerent_attr', ''),
                        # ('prop_area_rai',postdata['land_size_rai']),
                        # ('prop_area_ngan',postdata['land_size_ngan']),
                        # ('prop_area_sqm',postdata['land_size_wa']),
                        # ('prop_space',postdata['floorarea_sqm']),
                        ('prop_bedroom_type', '0'),
                        ('prop_bedroom', postdata['bed_room']),
                        ('prop_bathroom', postdata['bath_room']),
                        ('prop_livingroom', '1'),
                        ('prop_kitchen', ''),
                        ('prop_parking', ''),
                        ('prop_floor', postdata['floor_total']),
                        ('prop_mainroad', '1'),
                        ('prop_project_name', project_n),
                        ('prop_project', project_id),
                        ('prop_project_old', '0'),
                        ('project_prop_province', province_id),
                        ('project_prop_district', amphur_id),
                        ('project_prop_subdistrict', tumbon_id),
                        ('prop_soi', postdata['addr_soi']),
                        ('prop_road', postdata['addr_road']),
                        ('prop_province', province_id),
                        ('prop_district', amphur_id),
                        ('prop_subdistrict', tumbon_id),
                        ('prop_zipcode', ''),
                        ('prop_lat', postdata['geo_latitude']),
                        ('prop_lng', postdata['geo_longitude']),
                        ('facility[]', ''),
                        ('prop_gallary1', ''),
                        ('prop_gallary2', ''),
                        ('prop_gallary3', ''),
                        ('prop_gallary4', ''),
                        ('prop_gallary5', ''),
                        ('prop_gallary6', ''),
                        ('prop_gallary7', ''),
                        ('prop_gallary8', ''),
                        ('prop_gallary9', ''),
                        ('prop_gallary10', ''),
                        ('prop_active', 1),
                        ('prop_reason', ''),
                        ('prop_cancel', ''),
                        ('drag', '0'),
                        ('token', data['token']),
                        ('csrf_time', csrf_time),
                        ('csrf_token', csrf_token),
                        ('g_token',g_response),
                        ('action', 'update'),
                        ('prop_id', postdata['post_id'])
                    ]
                    if theprodid == 2:
                        datapost.append(('prop_area_rai', ''))
                        datapost.append(('prop_area_ngan', ''))
                        datapost.append(('prop_area_sqm', ''))
                        datapost.append(('prop_space', postdata['floor_area']))
                    elif theprodid == 5:
                        datapost.append(
                            ('prop_area_rai', postdata['land_size_rai']))
                        datapost.append(
                            ('prop_area_ngan', postdata['land_size_ngan']))
                        datapost.append(
                            ('prop_area_sqm', postdata['land_size_wa']))
                        datapost.append(('prop_space', ''))
                    else:
                        datapost.append(
                            ('prop_area_rai', postdata['land_size_rai']))
                        datapost.append(
                            ('prop_area_ngan', postdata['land_size_ngan']))
                        datapost.append(
                            ('prop_area_sqm', postdata['land_size_wa']))
                        datapost.append(('prop_space', postdata['floor_area']))
                    if postdata['listing_type'] == '????????????':
                        datapost[2] = ('prop_type', 33)
                        datapost[7] = ('prop_price', '')
                        datapost[9] = ('prop_pricerent',
                                       postdata['price_baht'])
                    else:
                        datapost[2] = ('prop_type', 32)
                        datapost[9] = ('prop_pricerent', '')
                        datapost[7] = ('prop_price', postdata['price_baht'])
                    files = {}

                    for i, myimg in enumerate(postdata['post_images'][:10]):
                    # for i in range(len(postdata["post_img_url_lists"])):
                        # resp = self.httprequestObj.http_get(
                        #     postdata["post_img_url_lists"][i], stream=True)
                        # resp.raw.decode_content = True
                        # with open('image'+str(i)+'.jpg', 'wb') as lfile:
                        #     shutil.copyfileobj(resp.raw, lfile)

                        # os.rename(postdata['post_images'][i],postdata['post_images'][i].replace('jpeg','jpg'))
                        r = (postdata['post_images'][i].replace('jpeg','jpg'), open(postdata['post_images'][i], 'rb'), "image/jpg")
                        # r = open(postdata['post_images'][i].replace('jpeg','jpg'), 'rb')
                        print(r)
                        if i > 10:
                            break
                        # else:
                        files["prop_gallery"+str(i+1)] = r
                        val = {
                            "filename": postdata['post_images'][i].replace("jpeg","jpg"),
                            "Content-Type": 'image/jpg'
                        }
                        datapost.append(('prop_gallery'+str(i+1), val))
                    r = self.httprequestObj.http_post(
                        'https://bankumka.com/property/save', data=datapost, files=files)
                    success = 'true'
                    detail = 'Edit post successful'
                    # print(r.text)
                else:
                    detail = '\n'.join(data['message'])
                    posturl= ''
                    success = "false"

                # files = {}
                # for i in range(len(postdata["post_img_url_lists"])):
                #     resp = self.httprequestObj.http_get(
                #         postdata["post_img_url_lists"][i], stream=True)
                #     resp.raw.decode_content = True
                #     with open('image'+str(i)+'.jpg', 'wb') as lfile:
                #         shutil.copyfileobj(resp.raw, lfile)

                #     r = open('image'+str(i)+'.jpg', 'rb')
                #     print(r)
                #     if i > 20:
                #         break
                #     if i == 0:
                #         files['fileshow'] = r
                #     else:
                #         files["file"+str(i)] = r
                #     datapost.append(('file[]', postdata["post_img_url_lists"][i]))
                #     # datapost['file[]'] = i
                #     r = self.httprequestObj.http_post(
                #         'https://www.ddteedin.com/upload', datapost)

                # r = self.httprequestObj.http_post(
                #     'https://www.ddteedin.com/post-land-for-sale/?rf=mypost', data=datapost, files=files)
                # # print(r.text)
                # query_element = {
                #     'q': postdata['name'],
                #     'pv': '',
                #     'order': 'createdate',
                #     'btn_srch': 'search'
                # }
                # query_string = 'https://www.ddteedin.com/myposts/?q='+query_element['q'].replace(' ', '+')+'&pv='+query_element['pv'].replace(
                #     ' ', '+')+'&order='+query_element['order'].replace(' ', '+')+"&btn_srch="+query_element['btn_srch'].replace(' ', '+')
                # r = self.httprequestObj.http_get(
                #     query_string, verify=False)
                # data = r.text
                # soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
                # id = soup.find("div", {"class": "it st1"})['id']
                # id = id.replace('r', '')
                # post_id += id
                # print(r.text)
                # print(r.status_code)
        else:
            detail = "cannot login"
            success = "false"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "websitename":"bankumka",
            "success": success,
            "detail": detail,
            "start_time": str(time_start),
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "end_time": str(time_end),
            "post_url": '',
            "post_id": postdata['post_id'],
            "account_type": "null",
            "ds_id": postdata['ds_id']
        }

    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        theurl = ""
        post_id = ""
        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        ashopname = test_login["detail"]
        detail = "Unable to delete post"
       
        province_id = '10'
        amphur_id = '26'
        if success == "true":
            success = "false"
            page = 1
            posturl = ""
            found = False
            while True:
                r = self.httprequestObj.http_get(
                    'https://bankumka.com/member/properties/page/'+str(page), verify=False)
                data = r.text
                soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
                all_ = soup.findAll("a", {"class": "my-property-name"})
                for i in all_:
                    if i['href'].find(str(postdata['post_id'])) != -1:
                        posturl += i['href']
                        found = True
                        break
                page += 1
                if not all_ or found:
                    break
            posturl += '/edit'

            if posturl == '/edit':
                detail  = "No post found with given id"
                success = "false"
            else:
                r = self.httprequestObj.http_get(
                    posturl, verify=False)
                data = r.text
                # print(data)
                soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
                data1 = soup.find_all('script', type='text/javascript')[1].string
                data1 = data1.split('var prop =')[1].replace(' prop',' "prop').replace(': "','": "')
                data1 = json.loads(data1)

                """alls = soup.findAll("script")
                cnt = 0
                ans = ""
                for i in range(len(alls)):
                    if i == 2:
                        ans += str(alls[i])
                ans = ans[51:len(ans)-10]
                ans = ans.replace(" ", "")
                # ans = ans.replace("\n","")
                # print(ans)
                indices = []
                for i in range(len(ans)):
                    if(ans[i] == ":" and ans[i+1] == '\"'):
                        indices.append(i)
                    elif(ans[i] == ',' and ans[i+1] == '\n'):
                        indices.append(i+2)
                    # print(ans[i],i)
                strng = r""
                strng += ans[0:2]+"\""+ans[2:indices[0]]
                for i in range(len(indices)-1):
                    strng += "\""+ans[indices[i]:indices[i+1]]
                strng += "\""+ans[indices[len(indices)-1]:len(ans)]
                # print(strng)
                data1 = json.loads(strng)"""
                r = self.httprequestObj.http_get('https://bankumka.com/property/announce')
                soup = BeautifulSoup(r.text, features=self.parser)
                csrf_time = soup.find(attrs={'name': 'csrf_time'})
                csrf_token = soup.find(attrs={'name': 'csrf_token'})
                if csrf_time:
                    csrf_time = csrf_time.get('value')
                if csrf_token:
                    csrf_token = csrf_token.get('value')
                # floor_area_sqm = 4*(400*int(postdata['land_size_rai'])+100*int(postdata['land_size_ngan'])+int(postdata['land_size_wa']))
                datapost = [
                    ('timeout', '5'),
                    ('prop_name', data1['prop_name']),
                    ('prop_type', data1['prop_type']),
                    ('prop_cate', data1['prop_cate']),
                    ('prop_detail', data1['prop_detail']),
                    ('prop_contact', data1['prop_contact']),
                    ('prop_line_id', data1['prop_line_id']),
                    ('prop_price', data1['prop_price']),
                    ('prop_price_attr', data1['prop_price_attr']),
                    ('prop_pricerent', data1['prop_pricerent']),
                    ('prop_pricerent_attr', data1['prop_pricerent_attr']),
                    ('prop_area_rai', data1['prop_area_rai']),
                    ('prop_area_ngan', data1['prop_area_ngan']),
                    ('prop_area_sqm', data1['prop_area_sqm']),
                    ('prop_space', data1['prop_space']),
                    ('prop_bedroom_type', data1['prop_bedroom_type']),
                    ('prop_bedroom', data1['prop_bedroom']),
                    ('prop_bathroom', data1['prop_bathroom']),
                    ('prop_livingroom', data1['prop_livingroom']),
                    ('prop_kitchen', data1['prop_kitchen']),
                    ('prop_parking', data1['prop_parking']),
                    ('prop_floor', data1['prop_floor']),
                    ('prop_mainroad', data1['prop_mainroad']),
                    ('prop_active', 4),
                    ('prop_reason', ''),
                    ('prop_cancel', ''),
                    ('prop_project_name', data1['prop_project_name']),
                    ('prop_project', data1['prop_project']),
                    ('prop_project_old', data1['prop_project_old']),
                    ('project_prop_province', ''),
                    ('project_prop_district', ''),
                    ('project_prop_subdistrict', ''),
                    ('prop_soi', data1['prop_soi']),
                    ('prop_road', data1['prop_road']),
                    ('prop_province', data1["prop_province"]),
                    ('prop_district', data1["prop_district"]),
                    ('prop_subdistrict', data1["prop_subdistrict"]),
                    ('prop_zipcode', data1['prop_zipcode']),
                    ('prop_lat', data1['prop_lat']),
                    ('prop_lng', data1['prop_lng']),
                    ('facility[]', ''),
                    ('prop_gallary1', ''),
                    ('prop_gallary2', ''),
                    ('prop_gallary3', ''),
                    ('prop_gallary4', ''),
                    ('prop_gallary5', ''),
                    ('prop_gallary6', ''),
                    ('prop_gallary7', ''),
                    ('prop_gallary8', ''),
                    ('prop_gallary9', ''),
                    ('prop_gallary10', ''),
                    ('drag', '0'),
                    ('token', ''),
                    ('csrf_time', csrf_time),
                    ('csrf_token', csrf_token),
                    ('action', 'update'),
                    ('prop_id', data1['prop_id'])
                ]
                r = self.httprequestObj.http_post(
                    'https://bankumka.com/ajax/checkProperty', data=datapost)
                data = json.loads(r.text)

                if data['status'] == 'OK':
                    g_response = captcha.reCaptcha('6Lfkov8cAAAAAOcHJBr2mND2B7xEKS3dJUJXlksm', 'https://bankumka.com')
                    if g_response == 0:
                        detail = 'Recaptcha error'
                        success = "false"
                    else:
                        datapost = [
                            ('timeout', '5'),
                            ('prop_name', data1['prop_name']),
                            ('prop_type', data1['prop_type']),
                            ('prop_cate', data1['prop_cate']),
                            ('prop_detail', data1['prop_detail']),
                            ('prop_contact', data1['prop_contact']),
                            ('prop_line_id', data1['prop_line_id']),
                            ('prop_price', data1['prop_price']),
                            ('prop_price_attr', data1['prop_price_attr']),
                            ('prop_pricerent', data1['prop_pricerent']),
                            ('prop_pricerent_attr', data1['prop_pricerent_attr']),
                            ('prop_area_rai', data1['prop_area_rai']),
                            ('prop_area_ngan', data1['prop_area_ngan']),
                            ('prop_area_sqm', data1['prop_area_sqm']),
                            ('prop_space', data1['prop_space']),
                            ('prop_bedroom_type', data1['prop_bedroom_type']),
                            ('prop_bedroom', data1['prop_bedroom']),
                            ('prop_bathroom', data1['prop_bathroom']),
                            ('prop_livingroom', data1['prop_livingroom']),
                            ('prop_kitchen', data1['prop_kitchen']),
                            ('prop_parking', data1['prop_parking']),
                            ('prop_floor', data1['prop_floor']),
                            ('prop_mainroad', data1['prop_mainroad']),
                            ('prop_active', 4),
                            ('prop_reason', ''),
                            ('prop_cancel', ''),
                            ('prop_project_name', data1['prop_project_name']),
                            ('prop_project', data1['prop_project']),
                            ('prop_project_old', data1['prop_project_old']),
                            ('project_prop_province', ''),
                            ('project_prop_district', ''),
                            ('project_prop_subdistrict', ''),
                            ('prop_soi', data1['prop_soi']),
                            ('prop_road', data1['prop_road']),
                            ('prop_province', data1["prop_province"]),
                            ('prop_district', data1["prop_district"]),
                            ('prop_subdistrict', data1["prop_subdistrict"]),
                            ('prop_zipcode', data1['prop_zipcode']),
                            ('prop_lat', data1['prop_lat']),
                            ('prop_lng', data1['prop_lng']),
                            ('facility[]', ''),
                            ('prop_gallary1', ''),
                            ('prop_gallary2', ''),
                            ('prop_gallary3', ''),
                            ('prop_gallary4', ''),
                            ('prop_gallary5', ''),
                            ('prop_gallary6', ''),
                            ('prop_gallary7', ''),
                            ('prop_gallary8', ''),
                            ('prop_gallary9', ''),
                            ('prop_gallary10', ''),
                            ('drag', '0'),
                            ('token', data['token']),
                            ('g_token',g_response),
                            ('csrf_time', csrf_time),
                            ('csrf_token', csrf_token),
                            ('action', 'update'),
                            ('prop_id', data1['prop_id'])
                        ]
                        r = self.httprequestObj.http_post(
                            'https://bankumka.com/property/save', data=datapost)
                        if '???????????????????????????????????????????????????????????????????????????' in r.text:
                            detail  = "Post deleted successfully"
                        else:
                            success = "false"
                            detail = 'Something wrong'
                else:
                    success = "false"
        else:
            success = "false"
            detail = test_login["detail"]

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "websitename":"bankumka",
            "success": success,
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "post_id": postdata['post_id'],
            "account_type": "null",
            "ds_id": postdata['ds_id']
        }

    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        test_login = self.test_login(postdata)
        detail = "The post doesn't exist"
        success = test_login["success"]
        ashopname = test_login["detail"]
        # print(test_login)
        if success == "true":
            r = self.httprequestObj.http_get(
                'https://bankumka.com/member/properties', verify=False)
            data = r.text
            soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
            all = soup.findAll("a", {"class": "my-property-name"})
            posturl = ""
            for i in all:
                # print(i.get_text())
                if (i.get_text()).find(str(postdata['post_id'])) != -1:
                    posturl += i['href']
            posturl += '/edit'
            # print(posturl)
            if(posturl == '/edit'):
                success = False
            else:
                datapost = {
                    'prop_id': postdata['post_id']
                }
                r = self.httprequestObj.http_post(
                    'https://bankumka.com/member/api/pushProp', datapost)
                detail = 'Boost post success.'
        else:
            success = "false"
            detail = 'cannot login'
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_id": postdata['post_id'],
            "detail": detail,
            "account_type": "null",
            "websitename": "bankumka",
            "ds_id": postdata['ds_id'],
            "post_view": ""
        }


    def search_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        theurl = ""
        post_id = ""

        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        ashopname = test_login["detail"]
        found = "false"
        detail = 'Post not found'
        post_id = ""
        posturl = ""
        if success == "true":

            r = self.httprequestObj.http_get('https://bankumka.com/member/properties', verify = False)
            data = r.text
            soup = BeautifulSoup(data,self.parser, from_encoding='utf-8')
            alldiv = soup.findAll("div",{"class":"my-property-box"})
            for i in alldiv:
                # print
                a = i.find("a",{"class":"my-property-name"})
                if a['title'] == postdata['post_title_th'][:119]:
                    posturl = a['href']
                    id1 = a.find("strong").get_text()
                    flag = False
                    found = "true"
                    for j in id1:
                        if j == ']':
                            break
                        if flag == True:
                            post_id += j
                        if j == '[':
                            flag = True
                         
                    break
            post_id = post_id.replace("#","")
        else:
            detail  = 'cannot login'
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        log_id = ""
        if 'log_id' in postdata:
            log_id = postdata['log_id']
        
        return {
            "websitename": "bankumka",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_found": found,
            'ds_id': postdata['ds_id'],
            'log_id': log_id,
            "post_url": posturl,
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "account_type": "null",
            "detail":detail,
            "post_create_time":"",
            "post_modify_time":"",
            "post_view":"",
            "ds_id": postdata['ds_id']
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


# a = bankumka()
# # create_credentials = {
# #     'user': 'terrabkk@2go-mail.com',
# #     'pass': '123456789',
# #     'name_th': 'Raavan',
# #     'surname_th': 'Lankesh',
# #     'tel': '1234567890'
# # }
# # login_credentials = {
# #     'user': 'terrabkk@2go-mail.com',
# #     'pass': '123456789'
# # }
# # # ret = a.register_user(create_credentials)
# # # print(ret)
# # ret = a.test_login(login_credentials)
# # print(ret)
# # credentials = {
# #     "geo_latitude": "13.786862",
# #     "geo_longitude": "100.757815",
# #     "property_id": "4",
# #     "forid": "3",
# #     "typeid": "2",
# #     "isnew": "1",
# #     "post_title_th": "xxx",
# #     "short_post_title_th": "xxx",
# #     "post_description_th": "xxx",
# #     "post_title_en": "",
# #     "short_post_title_en": "xxx",
# #     "post_description_en": "",
# #     "price_baht": "3000",
# #     "listing_type": "?????????",
# #     "property_type": "???????????????",
# #     "floor_level  ": "11",
# #     "floor_total  ": "11",
# #     "floor_area  ": "11",
# #     "bath_room  ": "11",
# #     "bed_room  ": "11",
# #     "prominent_point  ": "?????????????????????",
# #     "view_type ": "11",
# #     "direction_type": "11",
# #     "addr_province": "???????????????????????????",
# #     "addr_district": "?????????????????????",
# #     "addr_sub_district": "?????????????????????",
# #     "addr_road": "?????????",
# #     "addr_soi": "?????????",
# #     "addr_near_by": "????????????????????????????????????????????????",
# #     "floorarea_sqm": "?????????????????????",
# #     "price": "1234",
# #     "product_details": "jslkfdklfjdfkldfjdflkdfjdflksjfklhgdfoewitogjdfjdlskfdsjfdklfgjfklgdhfdslkfdhfdlfhewioffhdlkghfdlkfdskjfdlkgjhglkdsfhlgdshkfefhioglshg",
# #     "options": {},
# #     "land_size_rai": "???????????????????????????????????????????????????",
# #     "land_size_ngan": "???????????????????????????????????????????????????",
# #     "land_size_wa": "????????????????????????????????????????????????",
# #     "name": "land on rent",
# #     "mobile": "9876543210",
# #     "email": "ramu@gmail.com",
# #     "line": "xxx",
# #     "post_title_th": "????????????????????????????????? ????????????????????????????????????????????????",
# #     "user": "terrabkk@2go-mail.com",
# #     "pass": "123456789"
# # }
# email = 'terrabkk2@2go-mail.com'
# site = 'bankumka.com'
# postid = '320343'
# # credentials = { "action": "edit_post", "timeout": "5", "post_title_th": "????????????????????????????????? ?????????????????????????????????????????????", "post_img_url_lists": [ "https://unsplash.com/photos/gZlycYbRtkk","https://zignnet.sgp1.digitaloceanspaces.com/livingjoin/classified/189689/big/210120235215500991.jpg", "https://zignnet.sgp1.digitaloceanspaces.com/livingjoin/classified/189689/other/big/210120235220317918.jpg"], "geo_latitude": "13.786862", "geo_longitude": "100.757815", "property_id" : "chu001", "post_title_th": "????????????????????? ?????????????????????????????? ?????????????????????????????????????????? 6 ????????? ??????????????????????????????????????? ????????????????????????", "post_description_th": "??????????????????????????????????????? ?????????????????????????????????????????? 6 ????????? ?????????????????????????????????\r\n??????????????????????????????\r\n??????????????????\r\n???????????? 6 ?????????\r\n??????????????????????????? 30 ???????????? ????????????????????????????????????????????????????????????\r\n?????????????????????????????????????????????????????????????????????????????????????????? 1 ????????????\r\n\r\n????????????????????????????????????????????????\r\n???????????????????????????5\r\n????????????????????????????????????\r\n\r\n?????????????????????????????????????????? 100,000 ????????? ????????????????????????\r\n\r\n?????????????????????????????? ??????????????? 0992899999\r\nline: 0992899999", "post_title_en": "Land for rent bangkloysainoi 6 rai suitable for developing", "post_description_en": "Land for rent bangkloysainoi 6 rai suitable for developing\r\nLand Size 6 rai\r\nWidth 30 meter", "price_baht": "100000", "listing_type": "????????????", "property_type": "6", "prominent_point " : "???????????????????????????????????? ???????????????????????????????????????", "direction_type" : "11", "addr_province": "?????????????????????", "addr_district": "????????????????????????????????????", "addr_sub_district": "????????????????????????", "addr_road": "?????????????????????-?????????????????????", "addr_soi": "??????????????????????????????-????????????????????? 34", "addr_near_by": "???????????????????????????5\r\n????????????????????????????????????", "land_size_rai": "6", "land_size_ngan": "0", "land_size_wa": "0", "name": "fdjsljfkl", "mobile": "0992899999", "email": email, "line": "0992899999","ds_name": site, "ds_id": "120", "user": email, "pass": "123456789", "post_id":"320302"}
# # # thedata = { "action": "delete_post", "timeout": "5","ds_name": site,"ds_id": "120","post_id": 123456,"log_id": "56","user": email,"pass": "123456789" }
# # ret = a.create_post(credentials)
# # print(ret)
# thedata = { "action": "edit_post", "timeout": "5", "post_title_th": "?????????????????????????????????", "post_img_url_lists": [ "https://zignnet.sgp1.digitaloceanspaces.com/livingjoin/classified/189689/big/210120235215500991.jpg", "https://zignnet.sgp1.digitaloceanspaces.com/livingjoin/classified/189689/other/big/210120235220317918.jpg" ], "geo_latitude": "13.786862", "geo_longitude": "100.757815", "property_id" : "chu001", "post_title_th": "new edited ????????????????????? ?????????????????????????????? ?????????????????????????????????????????? 6 ????????? ?????????????????????????????????", "post_description_th": "new edited ??????????????????????????????????????? ?????????????????????????????????????????? 6 ????????? ????????????????????????????????????????????????????????????????????????????????????????????? 6 ???????????????????????????????????? 30 ???????????? ?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????? 1 ???????????????????????????????????????????????????????????????????????????????????????5?????????????????????????????????????????????????????????????????????????????? 100,000 ????????? ?????????????????????????????????????????????????????? ??????????????? 0992899999line: 0992899999", "post_title_en": "Land for rent bangkloysainoi 6 rai suitable for developing", "post_description_en": "Land for rent bangkloysainoi 6 rai suita ble for developing", "price_baht": "100000", "listing_type": "????????????", "property_type": "6", "prominent_point " : "???????????????????????????????????? ???????????????????????????????????????", "direction_type" : "11", "addr_province": "?????????????????????", "addr_district": "????????????????????????????????????", "addr_sub_district": "????????????????????????", "addr_road": "?????????????????????-?????????????????????", "addr_soi": "??????????????????????????????-????????????????????? 34", "addr_near_by": "???????????????????????????5\n????????????????????????????????????", "land_size_rai": "6", "land_size_ngan": "0", "land_size_wa": "0", "name": "??????", "mobile": "0992899999", "email": "panuwat.ruangrak@gmail.com", "line": "0992899999","ds_name": site, "ds_id": "120", "user": email, "pass": "123456789", "post_id": postid, "log_id": "48791", "account_type" : "corperate" }
# ret = a.edit_post(thedata)
# print(ret)
# a = bankumka()
# data = {
#     "user":"watid49642@mailop7.com",
#     "pass":"123456789",
#     "post_id":"320998"
# }
# ret = a.boost_post(data)
# print(ret)
