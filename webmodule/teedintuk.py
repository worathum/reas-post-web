from .lib_httprequest import *
from bs4 import BeautifulSoup as soup
import os.path
# from urlparse import urlparse
import re
import json
import sys
from urllib.parse import unquote
from datetime import datetime
import random

httprequestObj = lib_httprequest()
httprequestObj.timeout = 60


def set_end_time(start_time):
    time_end = datetime.utcnow()
    time_usage = time_end - start_time
    return time_end, time_usage


class teedintuk():
    name = 'teedintuk'
    property_dict = {
        '1': '2',
        '2': '3',
        '3': '4',
        '4': '1',
        '5': '7',
        '6': '5',
        '7': '6',
        '8': '6',
        '9': '10',
        '10': '8',
        '25': '9'
    }

    def __init__(self):

        try:
            import configs
        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.primarydomain = 'https://teedintuk.com/'
        self.debug = 0
        self.debugresdata = 0
        self.parser = 'html.parser'

    def logout_user(self):
        url = 'https://teedintuk.com/logout'
        httprequestObj.http_get(url)

    def register_user(self, userdata):
        # self.print_debug('function ['+sys._getframe().f_code.co_name+']')

        self.logout_user()
        reqst_url = "https://teedintuk.com/register"
        start_time = datetime.utcnow()
        res = {'websitename': 'teedintuk', 'success': 'false', 'start_time': str(start_time), 'end_time': '0',
               'usage_time': '0', 'detail': '', 'ds_id': userdata['ds_id']}
        username = str(userdata['name_th'] + " " + userdata['surname_th'])
        payload = {
            # 'username': userdata["user"].split('@')[0] ,
            'name': username,
            'email': userdata['user'],
            'phone': userdata['tel'],
            'password': userdata['pass'],
            'password_confirmation': userdata['pass'],
            'city': '',
            'usertype': 'Owner',
            '_token': '',
            'submit': ''
        }

        userpass_regex = re.compile(r'^([a-zA-Z0-9_]{4,15})$')
        email_regex = re.compile(r'^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$')
        # if(userpass_regex.search(payload['username'])==None):
        # res['detail']+='User Name must be in az, AZ, 0-9 or _ only and should be 4-15 characters only. '
        if (userpass_regex.search(payload['password']) == None):
            res['detail'] += 'Password must be in az, AZ, 0-9 or _ only and should be 4-15 characters only. '
        if (email_regex.search(payload['email']) == None):
            res['detail'] += 'Invalid email. '

        phone_regex = re.compile(r'^([0-9]{8,10})$')
        if (phone_regex.search(payload['phone']) == None):
            res['detail'] += 'Invalid phone number. '
        if (res['detail'] != ''):
            res['end_time'], res['usage_time'] = set_end_time(start_time)
            return res

        province = ''.join(map(str, str(userdata['addr_province']).split(' ')))
        resp = httprequestObj.http_get(reqst_url)
        token = soup(resp.text, 'html5lib')

        abc = token.find('select', attrs={'name': 'city'})

        for pq in abc.find_all('option'):
            if (str(pq.text) in str(province) or str(province) in str(pq.text)):
                payload['city'] = str(pq['value'])
                break
        payload['_token'] = str(token.find('input', attrs={'name': '_token'})['value'])

        r = httprequestObj.http_post(reqst_url, data=payload)

        parsedHtml = soup(r.text, 'html5lib')
        divd = parsedHtml.find('div', attrs={'class': 'alert alert-success'})
        if divd == None:
            res['success'] = 'false'
            res['detail'] = 'User already exists\n'
        else:
            res['success'] = 'true'
            res['detail'] = 'User Registered Successfully. Activation Mail Sent\n'
        endT, usage_time = set_end_time(start_time)
        res['end_time'] = str(endT)
        res['usage_time'] = str(usage_time)
        return res

    def test_login(self, userdata):

        self.logout_user()
        login_url = "https://teedintuk.com/login"
        start_time = datetime.utcnow()
        res = {'websitename': 'teedintuk', 'success': 'false', 'start_time': str(start_time), 'end_time': '0',
               'usage_time': '0', 'detail': '', 'ds_id': userdata['ds_id']}
        login_pload = {
            '_token': '',
            'email': userdata['user'],
            'password': userdata['pass'],
            'submit': ''
        }

        resp = httprequestObj.http_get(login_url)
        token = soup(resp.text, 'html5lib')

        login_pload['_token'] = str(token.find('input', attrs={'name': '_token'})['value'])

        r = httprequestObj.http_post(login_url, data=login_pload)

        parsedHtml = soup(r.text, 'html5lib')
        err = parsedHtml.find('div', attrs={'class': 'alert alert-danger'})
        if err == None:
            res['success'] = 'true'
            res['detail'] = 'User Logged In Successfully\n'
        else:
            res['success'] = 'false'
            res['detail'] = 'Wrong Email or Password'
        endT, usage_time = set_end_time(start_time)
        res['end_time'] = str(endT)
        res['usage_time'] = str(usage_time)
        return res

    def create_post(self, postdata):
        # self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.utcnow()
        # print(postdata)
        # postdata = postdata
        # print(self.max_image)

        login = self.test_login(postdata)

        post_id = ''
        post_url = ''

        if (login["success"] == "true"):
            listing_type = postdata['listing_type']
            property_type = postdata['property_type']
            post_img_url_lists = postdata['post_img_url_lists']
            price_baht = postdata['price_baht']
            addr_province = postdata['addr_province']
            addr_district = postdata['addr_district']
            addr_sub_district = postdata['addr_sub_district']
            addr_road, addr_near_by, floorarea_sqm = ['-', '', '1']
            addr_number = '1'

            if 'addr_road' in postdata and postdata['addr_road'] != None:
                addr_road = postdata['addr_road']
            else:
                addr_road = "-"
            if 'addr_near_by' in postdata:
                addr_near_by = postdata['addr_near_by']
            if 'floorarea_sqm' in postdata:
                floorarea_sqm = postdata['floorarea_sqm']
            if 'addr_number' in postdata:
                addr_number = postdata['addr_number']

            geo_latitude = postdata['geo_latitude']
            geo_longitude = postdata['geo_longitude']
            property_id = postdata['property_id']
            post_title_th = postdata['post_title_th']
            post_description_th = postdata['post_description_th']
            post_title_en = postdata['post_title_en']
            try:
                bedroom = postdata['bed_room']
                if bedroom == None:
                    bedroom = '0'
            except:
                bedroom = '0'
            try:
                bathroom = postdata['bath_room']
                if bathroom == None:
                    bathroom = '0'
            except:
                bathroom = '0'
            # ds_id = postdata["ds_id"]
            name = postdata["name"]
            mobile = postdata["mobile"]
            email = postdata["email"]
            # account_type = postdata["account_type"]
            user = postdata["user"]
            password = postdata["pass"]
            # project_name = postdata["project_name"]
            land_size_rai = postdata['land_size_rai']
            land_size_ngan = postdata['land_size_ngan']
            land_size_wah = postdata['land_size_wa']
            print("printing create")
            print(land_size_ngan, land_size_rai, land_size_wah)
            if (post_title_en == ''):
                post_title_en = post_title_th
            try:
                # land_size_ngan = land_size_ngan.srtip()
                temp1 = int(land_size_ngan)
                if temp1 == None:
                    temp1 = 0
            except:
                land_size_ngan = '0'
            try:
                # land_size_rai = land_size_rai.srtip()
                temp1 = int(land_size_rai)
                if temp1 == None:
                    temp1 = 0
            except:
                land_size_rai = '0'
            try:
                # land_size_wah = land_size_wah.srtip()
                temp1 = int(land_size_wah)
                if temp1 == None:
                    temp1 = 0
            except:
                land_size_wah = '0'
            print(land_size_ngan, land_size_rai, land_size_wah)

            # post_description_en =  post_description_en.replace("\r\n","<br>")
            post_description_th = post_description_th.replace("\r\n", "<br>")
            post_description_th = post_description_th.replace("\n", "<br>")

            # print(post_description_th)

            reqst_url = 'https://teedintuk.com/admin/properties/addproperty'

            prod_address = ""
            for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'],
                        postdata['addr_district'], postdata['addr_province']]:
                if add is not None:
                    prod_address += add + " "
            prod_address = prod_address[:-1]

            cookies = {
                'HstCfa4248993': '1595077149116',
                'HstCmu4248993': '1595077149116',
                '_ga': 'GA1.2.1099008652.1595077149',
                '_gid': 'GA1.2.1737558448.1595077149',
                '__dtsu': '6D0015943150553C303F1543554130A6',
                'HstCnv4248993': '7',
                'HstCla4248993': '1595243904513',
                'HstPn4248993': '4',
                'HstPt4248993': '46',
                'HstCns4248993': '15',
                'XSRF-TOKEN': 'eyJpdiI6IjJIa1hTUG9TUG5QNGJIM2hYQmozMVE9PSIsInZhbHVlIjoiUExIMjhCTmtyOTRBeXJKT01xTjdwTjRmaFJKQWpCbEhQSUxNN2JIbmdSQnQ5UUhrcmxCTGxKMzVmUDN6K0s5ZUR6XC85bmF1T1lcL2lLVFpJMEh3VUlBdz09IiwibWFjIjoiYTIwNjYwODY4MzhiNDYwMzI2Njc2ODJlNWE2YTZlZjZiMDFlZjFkODIyZjcyMWUyZmZiYjk5YWI1N2JhNDAxMSJ9',
                'laravel_session': 'eyJpdiI6IkwzNmlrRGQ2T2Q3bEZpemxMemE2bGc9PSIsInZhbHVlIjoiMUUrWlJHNlorb3h3YnlnMmVlZ0grY3FtYWJjdXpTc0FhaFdCaVlSVWNlcjFSUm9DblwvXC9JbmtaT2FZVEJQTFBLbHE1cTVnMU1qNk4zUWtFYWtyM1pndz09IiwibWFjIjoiOGUyYjlmNDVkZmJjMDg1YTZhN2QxYjcxMzJmZWVjYjczMTE3M2QzZDAyOWQzNDNkZWYxMGMyM2U4YmZiM2NmYSJ9',
            }

            headers = {
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Dest': 'document',
                'Referer': 'https://teedintuk.com/admin/properties/now',
                'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
            }

            data = {
                'property_name': postdata['post_title_th'].replace("%", "เปอร์เซ็นต์"),
                'id': '',
                'property_slug': '',
                'property_type': self.property_dict[str(postdata['property_type'])],

                'property_purpose': '',
                'property_features': '',
                'description': post_description_th,
                'city_id': '',

                'user_post': '',
                'featured_property': '',
                'bedrooms': bedroom,
                'bathrooms': bathroom,
                'area': '',
                'sale_price': '',
                'rent_price': '',
                'address': prod_address,

                'map_latitude': geo_latitude,
                'map_longitude': geo_longitude
            }

            if listing_type == 'เช่า':
                data['property_purpose'] = 'Rent'
                data['rent_price'] = price_baht
            else:
                data['property_purpose'] = 'Sale'
                data['sale_price'] = price_baht

            land_area_sq = str(400 * int(land_size_rai) + 100 * int(land_size_ngan) + 1 * int(land_size_wah))
            if (str(property_type) == str(1)):
                data['area'] = postdata['floor_area']
            else:
                data['area'] = land_area_sq

            resp = httprequestObj.http_get('https://teedintuk.com/admin/properties/now', headers=headers,
                                           cookies=cookies)
            pid = BeautifulSoup(resp.text, 'html5lib')

            if pid.find('tbody').find('tr') == None:
                post_id_old = None
            else:
                post_id_old = pid.find('tbody').find('tr').find('td').text
            print('ye find chla')

            province = ''.join(map(str, str(postdata['addr_province']).split(' ')))
            find_province = httprequestObj.http_get(reqst_url)
            # print("yha\n",find_province.text)
            provlist = BeautifulSoup(find_province.text, features="html5lib")

            data['_token'] = str(provlist.find('input', attrs={'name': '_token'})['value'])
            abc = provlist.find('select', attrs={'id': 'basic'})
            # print(abc)
            if abc == None:
                data['city_id'] = '1'
            else:
                for pq in abc.find_all('option'):
                    if (str(pq.text) in str(province) or str(province) in str(pq.text)):
                        data['city_id'] = str(pq['value'])
                        break

            if data['city_id'] == '':
                data['city_id'] = '1'

            if 'post_images' in postdata and len(postdata['post_images']) > 0:
                pass
            else:
                postdata['post_images'] = ['./imgtmp/default/white.jpg']

            file = []

            y = str(datetime.utcnow()).replace('-', '').replace(":", "").replace(".", "").replace(" ", "") + ".jpg"
            file.append(('featured_image', (y, open(postdata['post_images'][0], "rb"), "image/jpeg")))
            file.append(('files', (y, open(postdata['post_images'][0], "rb"), "image/jpeg")))
            file_name = []
            cnt = 1
            for i in postdata['post_images'][1:]:
                y = str(datetime.utcnow()).replace('-', '').replace(":", "").replace(".", "").replace(" ", "") + ".jpg"
                file.append(('property_images' + str(cnt), (y, open(i, "rb"), "image/jpeg")))
                file.append(('files', (y, open(i, "rb"), "image/jpeg")))
                file_name.append(y)
                if cnt == 5:
                    break
                cnt += 1

            r = httprequestObj.http_post("https://teedintuk.com/admin/properties/addproperty", data=data, files=file)
            print(r.text)
            resp = httprequestObj.http_get('https://teedintuk.com/admin/properties/now')
            pid = BeautifulSoup(resp.text, 'html5lib')
            # print('ye nahi chla')
            post_id = pid.find('tbody').find('tr').find('td').text
            # print('ye bhi chla')
            if post_id_old == post_id:
                success = 'false'
                detail = 'Post not created. Limit of 5 Posts Reached maybe!'
                post_id = ''
            else:
                post_url = 'https://teedintuk.com/properties/' + str(post_id)
                success = 'true'
                detail = 'Post Created'
            end_time, usage_time = set_end_time(start_time)

            return {
                "websitename": "teedintuk",
                "success": success,
                "start_time": str(start_time),
                "end_time": str(end_time),
                "usage_time": str(usage_time),
                "post_url": post_url,
                "ds_id": postdata['ds_id'],
                "post_id": post_id,
                "detail": detail,
                "account_type": "null"
            }
        else:
            return login

    def delete_post(self, postdata):

        # self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.utcnow()

        login = self.test_login(postdata)

        post_id = postdata['post_id']
        post_url = 'https://teedintuk.com/admin/properties/delete/' + post_id

        if (login["success"] == "true"):
            # del_data = {'post_id':post_id}
            res = httprequestObj.http_get('https://teedintuk.com/admin/properties/now')
            sou = soup(res.text, 'html5lib')
            trs = sou.find('tbody').findAll('tr')
            flag = 0
            for tr in trs:
                pid = tr.find('td').text
                if pid == post_id:
                    r = httprequestObj.http_get(post_url)
                    success = "true"
                    detail = "Post Deleted successfully"
                    flag = 1
            if flag == 0:
                success = "false"
                detail = "Post Not Found"

        else:
            success = "false"
            detail = "Can not log in"

        end_time, usage_time = set_end_time(start_time)

        return {
            "websitename": "teedintuk",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(usage_time),
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "detail": detail
        }

    def search_post(self, postdata):

        # self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.utcnow()

        login = self.test_login(postdata)

        post_id = ''
        post_url = ''
        post_found = ''
        post_create = ''
        post_view = ''
        post_modify = ''
        acc_t = ''
        if (login["success"] == "true"):

            res = httprequestObj.http_get('https://teedintuk.com/admin/properties/now')
            sou = soup(res.text, 'html5lib')
            trs = sou.find('tbody').findAll('tr')
            try:
                acc_t = postdata['account_type']
            except:
                acc_t = "Null"
            flag = 0
            for tr in trs:
                pid = tr.findAll('td')
                titl = pid[1].text
                if titl in postdata['post_title_th'] or postdata['post_title_th'] in titl:
                    post_found = "true"
                    post_id = pid[0].text
                    post_url = 'https://teedintuk.com/properties/' + str(post_id)
                    r = httprequestObj.http_get(post_url)
                    sou = BeautifulSoup(r.text, 'html5lib')
                    vd = sou.find('div', attrs={'class': 'meta-info'}).findAll('span')
                    post_create = vd[0].text
                    post_view = vd[1].text

                    success = "true"
                    detail = "Post Found"
                    flag = 1
            if flag == 0:
                success = "false"
                post_found = "false"
                detail = "Post Not Found"

        else:
            success = "false"
            post_found = "false"
            detail = "Can not log in"

        end_time, usage_time = set_end_time(start_time)

        return {
            "websitename": "teedintuk",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(usage_time),
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_found": post_found,
            "post_title_th": postdata['post_title_th'],
            "post_url": post_url,
            "post_id": post_id,
            "detail": detail,
            "post_create_time": post_create,
            "post_modify_time": post_modify,
            "post_view": post_view,
            "account_type": acc_t,
        }

    def edit_post(self, postdata):
        # self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.utcnow()
        login = self.test_login(postdata)

        post_id = str(postdata['post_id'])
        post_url = ''

        if (login["success"] == "true"):

            listing_type = postdata['listing_type']
            property_type = str(postdata['property_type'])
            post_img_url_lists = postdata['post_img_url_lists']
            price_baht = postdata['price_baht']
            addr_province = postdata['addr_province']
            addr_district = postdata['addr_district']
            addr_sub_district = postdata['addr_sub_district']

            if 'addr_road' in postdata and postdata['addr_road'] != None:
                addr_road = postdata['addr_road']
            else:
                addr_road = "-"
            if 'addr_near_by' in postdata:
                addr_near_by = postdata['addr_near_by']
            if 'floorarea_sqm' in postdata:
                floorarea_sqm = postdata['floorarea_sqm']
            if 'addr_number' in postdata:
                addr_number = postdata['addr_number']

            geo_latitude = postdata['geo_latitude']
            geo_longitude = postdata['geo_longitude']
            property_id = postdata['property_id']
            post_title_th = postdata['post_title_th']
            post_description_th = postdata['post_description_th']
            post_title_en = postdata['post_title_en']
            try:
                bedroom = postdata['bed_room']
            except:
                bedroom = '0'
            try:
                bathroom = postdata['bath_room']
            except:
                bathroom = '0'
            # ds_id = postdata["ds_id"]
            name = postdata["name"]
            mobile = postdata["mobile"]
            email = postdata["email"]
            # account_type = postdata["account_type"]
            user = postdata["user"]
            password = postdata["pass"]
            # project_name = postdata["project_name"]
            land_size_rai = postdata['land_size_rai']
            land_size_ngan = postdata['land_size_ngan']
            land_size_wah = postdata['land_size_wa']
            print("printing create")
            print(land_size_ngan, land_size_rai, land_size_wah)
            if (post_title_en == ''):
                post_title_en = post_title_th
            try:
                # land_size_ngan = land_size_ngan.srtip()
                temp1 = int(land_size_ngan)
                if temp1 == None:
                    temp1 = 0
            except:
                land_size_ngan = '0'
            try:
                # land_size_rai = land_size_rai.srtip()
                temp1 = int(land_size_rai)
                if temp1 == None:
                    temp1 = 0
            except:
                land_size_rai = '0'
            try:
                # land_size_wah = land_size_wah.srtip()
                temp1 = int(land_size_wah)
                if temp1 == None:
                    temp1 = 0
            except:
                land_size_wah = '0'
            print(land_size_ngan, land_size_rai, land_size_wah)

            # post_description_en =  post_description_en.replace("\r\n","<br>")
            post_description_th = post_description_th.replace("\r\n", "<br>")
            post_description_th = post_description_th.replace("\n", "<br>")

            print(post_description_th)

            reqst_url = str('https://teedintuk.com/admin/properties/addproperty/' + post_id)

            prod_address = ""
            for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'],
                        postdata['addr_district'], postdata['addr_province']]:
                if add is not None:
                    prod_address += add + " "
            prod_address = prod_address[:-1]
            data = {
                'property_name': postdata['post_title_th'],
                'id': post_id,
                'property_slug': post_id,
                'property_type': self.property_dict[str(postdata['property_type'])],

                'property_purpose': '',
                'property_features': '',
                'description': post_description_th,
                'city_id': '',

                'user_post': '',
                'featured_property': '',
                'bedrooms': bedroom,
                'bathrooms': bathroom,
                'area': '',
                'sale_price': '',
                'rent_price': '',
                'address': prod_address,

                'map_latitude': geo_latitude,
                'map_longitude': geo_longitude
            }

            if listing_type == 'เช่า':
                data['property_purpose'] = 'Rent'
                data['rent_price'] = price_baht
            else:
                data['property_purpose'] = 'Sale'
                data['sale_price'] = price_baht

            land_area_sq = str(400 * int(land_size_rai) + 100 * int(land_size_ngan) + 1 * int(land_size_wah))
            if (str(property_type) == str(1)):
                data['area'] = postdata['floor_area']
            else:
                data['area'] = land_area_sq

            res = httprequestObj.http_get('https://teedintuk.com/admin/properties/now')
            sou = soup(res.text, 'html5lib')
            trs = sou.find('tbody').findAll('tr')
            flag = 0
            for tr in trs:
                pid = tr.find('td').text
                if pid == post_id:

                    province = ''.join(map(str, str(postdata['addr_province']).split(' ')))
                    find_province = httprequestObj.http_get(reqst_url)
                    print(find_province.url)
                    provlist = BeautifulSoup(find_province.text, features="html5lib")

                    data['_token'] = str(provlist.find('input', attrs={'name': '_token'})['value'])
                    data['user_post'] = provlist.find('input', attrs={'name': 'user_post'})['value']
                    print(data['user_post'])
                    data['featured_property'] = provlist.find('input', attrs={'name': 'featured_property'})['value']
                    print(data['featured_property'])
                    abc = provlist.find('select', attrs={'id': 'basic'})
                    # print(abc)

                    for pq in abc.find_all('option'):
                        if (str(pq.text) in str(province) or str(province) in str(pq.text)):
                            data['city_id'] = str(pq['value'])
                            break

                    if data['city_id'] == '':
                        data['city_id'] = '1'

                    if 'post_images' in postdata and len(postdata['post_images']) > 0:
                        pass
                    else:
                        postdata['post_images'] = ['./imgtmp/default/white.jpg']

                    file = []

                    y = str(datetime.utcnow()).replace('-', '').replace(":", "").replace(".", "").replace(" ",
                                                                                                          "") + ".jpg"
                    file.append(('featured_image', (y, open(postdata['post_images'][0], "rb"), "image/jpeg")))
                    file.append(('files', (y, open(postdata['post_images'][0], "rb"), "image/jpeg")))
                    file_name = []
                    cnt = 1
                    for i in postdata['post_images'][1:]:
                        y = str(datetime.utcnow()).replace('-', '').replace(":", "").replace(".", "").replace(" ",
                                                                                                              "") + ".jpg"
                        file.append(('property_images' + str(cnt), (y, open(i, "rb"), "image/jpeg")))
                        file.append(('files', (y, open(i, "rb"), "image/jpeg")))
                        file_name.append(y)
                        if cnt == 5:
                            break
                        cnt += 1

                    r = httprequestObj.http_post("https://teedintuk.com/admin/properties/addproperty", data=data,
                                                 files=file)

                    flag = 1
            if flag == 0:
                success = 'false'
                detail = 'Post not found'
            else:
                success = 'true'
                detail = 'Post Edited Successfully'
                post_url = str('https://teedintuk.com/properties/' + str(post_id))

            end_time, usage_time = set_end_time(start_time)

            return {
                "websitename": "teedintuk",
                "success": success,
                "start_time": str(start_time),
                "end_time": str(end_time),
                "usage_time": str(usage_time),
                "post_url": post_url,
                "ds_id": postdata['ds_id'],
                "post_id": post_id,
                "detail": detail,
                "account_type": "null"
            }

        else:
            return login

    def boost_post(self, postdata):
        strt = (datetime.utcnow())
        end_time, usage_time = set_end_time(strt)
        return {
            "websitename": "teedintuk",
            "success": 'true',
            "start_time": str(strt),
            "end_time": str(end_time),
            "usage_time": str(usage_time),
            "ds_id": postdata['ds_id'],
            "post_id": postdata['post_id'],
            "detail": "cannot boost, because it's paid on this website",
            "account_type": "null"
        }