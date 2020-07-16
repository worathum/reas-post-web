import requests
import os
from .lib_httprequest import *
import string
from bs4 import BeautifulSoup
import os.path
# from urlparse import urlparse
import re
import json
import datetime
import time
import sys
import shutil
from urllib.parse import unquote


httprequestObj = lib_httprequest()
# options = Options()
# options.set_headless(True)
# browser = webdriver.Chrome(
    # executable_path='/usr/bin/chromedriver', options=options)

# with open("./static/ploychao_province.json") as f:
#     provincedata = json.load(f)


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
        # r = httprequestObj.http_get('https://bankumka.com/access/register/checker',verify = False)
        # print(r.content)
        r = httprequestObj.http_get(
            'https://bankumka.com/themes/default/assets/js/member/register.js', verify=False)
        # print(r.text)
        datapost = {
            'user_class': '1',
            'company': '',
            'email': user,
            'password': passwd,
            'password2': passwd,
            'first_name': name_th,
            'last_name': surname_th,
            'phone': mobile_no,
            'token': ''
        }
        r = httprequestObj.http_post(
            'https://bankumka.com/access/register/checker', data=datapost)
        # print(r.text)
        # r = httprequestObj.http_get('https://bankumka.com/access',verify= False)
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

            r = httprequestObj.http_post(
                'https://bankumka.com/access/register', data=datapost)
        # print("yes")
            # print(r.text)
        # print(data)
            if r.status_code == 404:
                detail = "Can't register"
                success = "false"
            else:
                detail = "Registered"
                # r = httprequestObj.http_get('https://bankumka.com/access/register/success',verify = False)
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

        r = httprequestObj.http_post(
            'https://bankumka.com/access', data=datapost)
        data = r.text
        # print(data)
        # print(r.text)
        if data.find("ข้อมูลการเข้าระบบไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง !!") != -1:
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
        # print(theprodid)
        # theprodid = post
        # for (key, value) in provincedata.items():
        #     if type(value) is str and postdata['addr_province'].strip() in value.strip():
        #         province_id = key
        #         break

        # for (key, value) in provincedata[province_id+"_province"].items():
        #     if postdata['addr_district'].strip() in value.strip():
        #         amphur_id = key
        #         break
        province_id = '0'
        detail = ""
        amphur_id = '26'
        tumbon_id = '01'
        prod_address = ""
        for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
            if add is not None:
                prod_address += add
        prod_address = prod_address[:-1]
        print(success,"lol")
        if success == "true":

            r = httprequestObj.http_get(
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
                        break

                # print(i)
                # print(i.get_text())
                # print("data: "+i.text+" value: "+i.value)
            # print(province_id)
            query_string = 'https://bankumka.com/ajax/listcities/'+province_id
            r = httprequestObj.http_get(
                query_string, verify=False)
            data = json.loads(r.text)
            # print(data)
            amphur_found = False
            for i in data:
                # print(i['name'])
                if postdata['addr_district'].replace(" ","") == i['name']:
                    amphur_found = True
                    amphur_id = i['id']
                    break
            if amphur_found is False:
                for i in data:
                    if postdata['addr_district'].replace(" ","").find(i['name']) != -1 or i['name'].find(postdata['addr_district'].replace(" ","")) != -1:
                        amphur_id = i['id']
                        break
            # print(amphur_id)
            query_string = 'https://bankumka.com/ajax/listcities/'+amphur_id
            r = httprequestObj.http_get(
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
                        break

            # print(tumbon_id)
            # browser.get("https://bankumka.com/property/announce")
            # csrf_token = browser.find_element_by_name("csrf_token").get_attribute("value")
            # csrf_time = browser.find_element_by_name("csrf_time").get_attribute("value")
            # print(csrf_time)
            csrf_time = 0
            csrf_token = ''


            if 'web_project_name' in postdata and postdata['web_project_name'] is not None:
                project_n = postdata['web_project_name']
            elif 'project_name' in postdata and postdata['project_name'] is not None:
                project_n = postdata['project_name']
            else:
                project_n = postdata['post_title_th']

            mydata = {
                'query': project_n
            }
            resp = requests.post('https://bankumka.com/ajax/listproject/', data=mydata)
            print("ji")
            allres = json.loads(resp.content.decode('utf-8'))["suggestions"]
            project_id = '0'

            if len(allres) != 0:
                project_id = allres[0]['data']
                project_n = allres[0]["value"]

                mydata = {'id':project_id}
                resp1 = requests.post("https://bankumka.com/ajax/getLocationProject/", data=mydata)
                res1 = json.loads(resp1.content.decode('utf-8'))['result']

                postdata["geo_longitude"] = res1["project_lng"]
                postdata["geo_latitude"] = res1["project_lat"]
                province_id = res1["project_province"]
                amphur_id = res1["project_district"]
                tumbon_id = res1["project_subdistrict"]


            datapost = [
                ('timeout', '5'),
                ('prop_name', postdata['post_title_th']),
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
            if postdata['listing_type'] == 'เช่า':
                datapost[2] = ('prop_type', 33)
                datapost[7] = ('prop_price', '')
                datapost[9] = ('prop_pricerent', postdata['price_baht'])
            else:
                datapost[2] = ('prop_type', 32)
                datapost[9] = ('prop_pricerent', '')
                datapost[7] = ('prop_price', postdata['price_baht'])
            r = httprequestObj.http_post(
                'https://bankumka.com/ajax/checkProperty', data=datapost)
            data = json.loads(r.text)
            print(data)
            if data['status'] == 'OK':
                datapost = [
                    ('timeout', '5'),
                    ('prop_name', postdata['post_title_th']),
                    ('prop_type', '32'),
                    ('prop_cate', theprodid),
                    ('prop_detail', postdata['post_description_th']),
                    ('prop_contact', postdata['mobile']),
                    ('prop_line_id', ''),
                    ('prop_price', postdata['price_baht']),
                    ('prop_price_attr', ''),
                    ('prop_pricerent', ''),
                    ('prop_pricerent_attr', ''),
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
                if postdata['listing_type'] == 'เช่า':
                    datapost[2] = ('prop_type', 33)
                    datapost[7] = ('prop_price', '')
                    datapost[9] = ('prop_pricerent', postdata['price_baht'])
                else:
                    datapost[2] = ('prop_type', 32)
                    datapost[9] = ('prop_pricerent', '')
                    datapost[7] = ('prop_price', postdata['price_baht'])
                files = {}
                # for i, myimg in enumerate(postdata['post_images'][:10]):
                for i in range(len(postdata['post_images'])):
                # for i in range(len(postdata["post_img_url_lists"])):
                    # resp = requests.get(
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
                r = httprequestObj.http_post(
                    'https://bankumka.com/property/save', data=datapost, files=files)
                # print(r.text)
                data = r.text
                soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
                post_id = soup.find("input", {"name": "prop_id"})['value']
                # print(post_id)
                if post_id != '':
                    r = httprequestObj.http_get(
                        'https://bankumka.com/member/properties', verify=False)
                    data = r.text
                    soup = BeautifulSoup(
                        data, self.parser, from_encoding='utf-8')
                    all = soup.findAll("a", {"class": "my-property-name"})
                    for i in all:
                        if (i.get_text()).find(post_id) != -1:
                            theurl += i['href']
            else:
                post_url = ""
                success = "false"
                if data['message'][0].find("10") != -1:
                    detail = "Posts Limit Reached"

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
        resp = requests.post('https://bankumka.com/ajax/listproject/', data=mydata)
        allres = json.loads(resp.content.decode('utf-8'))["suggestions"]
        project_id = '0'

        if len(allres) != 0:
            project_id = allres[0]['data']
            project_n = allres[0]["value"]

            mydata = {'id':project_id}
            resp1 = requests.post("https://bankumka.com/ajax/getLocationProject/", data=mydata)
            res1 = json.loads(resp1.content.decode('utf-8'))['result']

            postdata["geo_longitude"] = res1["project_lng"]
            postdata["geo_latitude"] = res1["project_lat"]
            province_id = res1["project_province"]
            amphur_id = res1["project_district"]
            tumbon_id = res1["project_subdistrict"]


        if success == "true":
            r = httprequestObj.http_get(
                'https://bankumka.com/member/properties', verify=False)
            data = r.text
            soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
            all = soup.findAll("a", {"class": "my-property-name"})
            posturl = ""
            for i in all:
                if (i.get_text()).find(postdata['post_id']) != -1:
                    posturl += i['href']
            posturl += '/edit'
            # print(posturl)
            if(posturl == '/edit'):
                success = False
            else:
                r = httprequestObj.http_get(
                    posturl, verify=False)
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
                            break

                    # print(i)
                    # print(i.get_text())
                    # print("data: "+i.text+" value: "+i.value)
                # print(province_id)
                query_string = 'https://bankumka.com/ajax/listcities/'+province_id
                r = httprequestObj.http_get(
                    query_string, verify=False)
                data = json.loads(r.text)
                # print(data)
                amphur_found = False
                for i in data:
                    # print(i['name'])
                    if postdata['addr_district'].replace(" ","") == i['name']:
                        amphur_found = True
                        amphur_id = i['id']
                        break
                if amphur_found is False:
                    for i in data:
                        if postdata['addr_district'].replace(" ","").find(i['name']) != -1 or i['name'].find(postdata['addr_district'].replace(" ","")) != -1:
                            amphur_id = i['id']
                            break
                # print(amphur_id)
                query_string = 'https://bankumka.com/ajax/listcities/'+amphur_id
                r = httprequestObj.http_get(
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
                            break
                # print(tumbon_id)
                # browser.get(posturl)
                # try:
                #     csrf_token = browser.find_element_by_name("csrf_token").get_attribute("value")
                #     csrf_time = browser.find_element_by_name("csrf_time").get_attribute("value")
                # except:
                #     csrf_time = 0
                #     csrf_token = ''
                csrf_time = 0
                csrf_token = ''
                # print(csrf_time)
                floor_area_sqm = 0
                datapost = [
                    ('timeout', '5'),
                    ('prop_name', postdata['post_title_th']),
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
                if postdata['listing_type'] == 'เช่า':
                    datapost[2] = ('prop_type', 33)
                    datapost[7] = ('prop_price', '')
                    datapost[9] = ('prop_pricerent', postdata['price_baht'])
                else:
                    datapost[2] = ('prop_type', 32)
                    datapost[9] = ('prop_pricerent', '')
                    datapost[7] = ('prop_price', postdata['price_baht'])
                r = httprequestObj.http_post(
                    'https://bankumka.com/ajax/checkProperty', data=datapost)
                data = json.loads(r.text)
                print(data)
                if data['status'] == 'OK':
                    datapost = [
                        ('timeout', '5'),
                        ('prop_name', postdata['post_title_th']),
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
                    if postdata['listing_type'] == 'เช่า':
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
                        # resp = requests.get(
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
                    r = httprequestObj.http_post(
                        'https://bankumka.com/property/save', data=datapost, files=files)
                    # print(r.text)
                else:
                    success = "false"
                # files = {}
                # for i in range(len(postdata["post_img_url_lists"])):
                #     resp = requests.get(
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
                #     r = httprequestObj.http_post(
                #         'https://www.ddteedin.com/upload', datapost)

                # r = httprequestObj.http_post(
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
                # r = httprequestObj.http_get(
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
            "post_url": posturl,
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
        # print(test_login)
        province_id = '10'
        amphur_id = '26'
        if success == "true":
            r = httprequestObj.http_get(
                'https://bankumka.com/member/properties', verify=False)
            data = r.text
            soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
            all = soup.findAll("a", {"class": "my-property-name"})
            posturl = ""
            for i in all:
                if (i.get_text()).find(str(postdata['post_id'])) != -1:
                    posturl += i['href']
            posturl += '/edit'
            # print(posturl)
            if(posturl == '/edit'):
                success = "false"
            else:
                r = httprequestObj.http_get(
                    posturl, verify=False)
                data = r.text
                # print(data)
                soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
                alls = soup.findAll("script")
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
                data1 = json.loads(strng)
                csrf_time = 0
                csrf_token = ''
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
                r = httprequestObj.http_post(
                    'https://bankumka.com/ajax/checkProperty', data=datapost)
                data = json.loads(r.text)
                print(data)
                if data['status'] == 'OK':
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
                        ('csrf_time', csrf_time),
                        ('csrf_token', csrf_token),
                        ('action', 'update'),
                        ('prop_id', data1['prop_id'])
                    ]
                    r = httprequestObj.http_post(
                        'https://bankumka.com/property/save', data=datapost)
                    # print(r.text)
                else:
                    success = "false"
            # files = {}
            # for i in range(len(postdata["post_img_url_lists"])):
            #     resp = requests.get(
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
            #     r = httprequestObj.http_post(
            #         'https://www.ddteedin.com/upload', datapost)

        else:
            success = "false"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "websitename":"bankumka",
            "success": success,
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": posturl,
            "post_id": postdata['post_id'],
            "account_type": "null",
            "ds_id": postdata['ds_id']
        }

    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        test_login = self.test_login(postdata)
        success = test_login["success"]
        ashopname = test_login["detail"]
        # print(test_login)
        if success == "true":
            r = httprequestObj.http_get(
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
                r = httprequestObj.http_post(
                    'https://bankumka.com/member/api/pushProp', datapost)
        else:
            success = "false"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_id": postdata['post_id'],
            "account_type": "null",
            "websitename": "bankumka",
            "ds_id": postdata['ds_id']
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
        post_id = ""
        posturl = ""
        if success == "true":
            r = httprequestObj.http_get('https://bankumka.com/member/properties', verify = False)
            data = r.text
            soup = BeautifulSoup(data,self.parser, from_encoding='utf-8')
            alldiv = soup.findAll("div",{"class":"my-property-box"})
            for i in alldiv:
                # print
                a = i.find("a",{"class":"my-property-name"})
                if a['title'] == postdata['post_title_th']:
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
            success = "false"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        log_id = ""
        if 'log_id' in postdata:
            log_id = postdata['log_id']
        
        return {
            "websitename": "bankumka",
            "success": "true",
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_found": found,
            'ds_id': postdata['ds_id'],
            'log_id': log_id,
            "post_url": posturl,
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "account_type": "null",
            "detail":"null",
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
# #     "listing_type": "ขาย",
# #     "property_type": "คอนโด",
# #     "floor_level  ": "11",
# #     "floor_total  ": "11",
# #     "floor_area  ": "11",
# #     "bath_room  ": "11",
# #     "bed_room  ": "11",
# #     "prominent_point  ": "จุดเด่น",
# #     "view_type ": "11",
# #     "direction_type": "11",
# #     "addr_province": "กาญจนบุรี",
# #     "addr_district": "บ่อพลอย",
# #     "addr_sub_district": "บ่อพลอย",
# #     "addr_road": "ถนน",
# #     "addr_soi": "ซอย",
# #     "addr_near_by": "สถานที่ใกล้เคียง",
# #     "floorarea_sqm": "พื้นที่",
# #     "price": "1234",
# #     "product_details": "jslkfdklfjdfkldfjdflkdfjdflksjfklhgdfoewitogjdfjdlskfdsjfdklfgjfklgdhfdslkfdhfdlfhewioffhdlkghfdlkfdskjfdlkgjhglkdsfhlgdshkfefhioglshg",
# #     "options": {},
# #     "land_size_rai": "ขนาดที่ดินเป็นไร่",
# #     "land_size_ngan": "ขนาดที่ดินเป็นงาน",
# #     "land_size_wa": "ขนาดที่ดินเป็นวา",
# #     "name": "land on rent",
# #     "mobile": "9876543210",
# #     "email": "ramu@gmail.com",
# #     "line": "xxx",
# #     "post_title_th": "ลุมพีนีวิลล รามอินทราหลักสี่",
# #     "user": "terrabkk@2go-mail.com",
# #     "pass": "123456789"
# # }
# email = 'terrabkk2@2go-mail.com'
# site = 'bankumka.com'
# postid = '320343'
# # credentials = { "action": "edit_post", "timeout": "5", "post_title_th": "ลุมพีนีวิลล รามอินทราหลักสี", "post_img_url_lists": [ "https://unsplash.com/photos/gZlycYbRtkk","https://zignnet.sgp1.digitaloceanspaces.com/livingjoin/classified/189689/big/210120235215500991.jpg", "https://zignnet.sgp1.digitaloceanspaces.com/livingjoin/classified/189689/other/big/210120235220317918.jpg"], "geo_latitude": "13.786862", "geo_longitude": "100.757815", "property_id" : "chu001", "post_title_th": "ให้เช่า ที่ดินด่วน บางกรวยไทรน้อย 6 ไร่ เหมาะทำตลาดสด เปิดท้าย", "post_description_th": "ขายที่ดินด่วน บางกรวยไทรน้อย 6 ไร่ เหมาะทำตลาด\r\nรายละเอียด\r\nที่ดิน\r\nขนาด 6 ไร่\r\nหน้ากว้าง 30 เมตร ติดถนนบางกรวยไทรน้อย\r\nที่ดินยังไม่ถมต่ำกว่าถนนประมาณ 1 เมตร\r\n\r\nสถานที่ใกล้เคียง\r\nถนนพระราม5\r\nถนนนครอินทร์\r\n\r\nให้เช่าระยะยาว 100,000 บาท ต่อเดือน\r\n\r\nสนใจติดต่อ คุณชู 0992899999\r\nline: 0992899999", "post_title_en": "Land for rent bangkloysainoi 6 rai suitable for developing", "post_description_en": "Land for rent bangkloysainoi 6 rai suitable for developing\r\nLand Size 6 rai\r\nWidth 30 meter", "price_baht": "100000", "listing_type": "เช่า", "property_type": "6", "prominent_point " : "หน้ากว้างมาก ให้เช่าถูกสุด", "direction_type" : "11", "addr_province": "นนทบุรี", "addr_district": "เมืองนนทบุรี", "addr_sub_district": "บางกระสอ", "addr_road": "บางกรวย-ไทรน้อย", "addr_soi": "ซอยบางกรวย-ไทรน้อย 34", "addr_near_by": "ถนนพระราม5\r\nถนนนครอินทร์", "land_size_rai": "6", "land_size_ngan": "0", "land_size_wa": "0", "name": "fdjsljfkl", "mobile": "0992899999", "email": email, "line": "0992899999","ds_name": site, "ds_id": "120", "user": email, "pass": "123456789", "post_id":"320302"}
# # # thedata = { "action": "delete_post", "timeout": "5","ds_name": site,"ds_id": "120","post_id": 123456,"log_id": "56","user": email,"pass": "123456789" }
# # ret = a.create_post(credentials)
# # print(ret)
# thedata = { "action": "edit_post", "timeout": "5", "post_title_th": "ลุมพีนีวิลล", "post_img_url_lists": [ "https://zignnet.sgp1.digitaloceanspaces.com/livingjoin/classified/189689/big/210120235215500991.jpg", "https://zignnet.sgp1.digitaloceanspaces.com/livingjoin/classified/189689/other/big/210120235220317918.jpg" ], "geo_latitude": "13.786862", "geo_longitude": "100.757815", "property_id" : "chu001", "post_title_th": "new edited ให้เช่า ที่ดินด่วน บางกรวยไทรน้อย 6 ไร่ เหมาะทำตลาด", "post_description_th": "new edited ขายที่ดินด่วน บางกรวยไทรน้อย 6 ไร่ เหมาะทำตลาดรายละเอียดที่ดินขนาด 6 ไร่หน้ากว้าง 30 เมตร ติดถนนบางกรวยไทรน้อยที่ดินยังไม่ถมต่ำกว่าถนนประมาณ 1 เมตรสถานที่ใกล้เคียงถนนพระราม5ถนนนครอินทร์ให้เช่าระยะยาว 100,000 บาท ต่อเดือนสนใจติดต่อ คุณชู 0992899999line: 0992899999", "post_title_en": "Land for rent bangkloysainoi 6 rai suitable for developing", "post_description_en": "Land for rent bangkloysainoi 6 rai suita ble for developing", "price_baht": "100000", "listing_type": "เช่า", "property_type": "6", "prominent_point " : "หน้ากว้างมาก ให้เช่าถูกสุด", "direction_type" : "11", "addr_province": "นนทบุรี", "addr_district": "เมืองนนทบุรี", "addr_sub_district": "บางกระสอ", "addr_road": "บางกรวย-ไทรน้อย", "addr_soi": "ซอยบางกรวย-ไทรน้อย 34", "addr_near_by": "ถนนพระราม5\nถนนนครอินทร์", "land_size_rai": "6", "land_size_ngan": "0", "land_size_wa": "0", "name": "ชู", "mobile": "0992899999", "email": "panuwat.ruangrak@gmail.com", "line": "0992899999","ds_name": site, "ds_id": "120", "user": email, "pass": "123456789", "post_id": postid, "log_id": "48791", "account_type" : "corperate" }
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
