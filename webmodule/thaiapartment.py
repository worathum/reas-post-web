# -*- coding: utf-8 -*-

from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
# from urlparse import urlparse
import re
import json
import datetime
import sys
import requests
import shutil
from urllib.parse import unquote



class thaiapartment():

    def __init__(self):

        try:
            import configs

        except ImportError:
            configs = {}

        self.httprequestObj = lib_httprequest()
        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.debug = 1
        self.debugresdata = 0
        self.parser = 'html.parser'
        self.webname = 'thaiapartment'

    def print_debug(self, msg):
        if self.debug == 1:
            print(msg)
        return True

    def logout_user(self):
        url = 'https://www.thaiapartment.com/logout.aspx'
        self.httprequestObj.http_get(url)

    # Funtion to Calculate value of title to be sent with form data
    def title_value(self,title):
        if title == "Mr":
            return 1
        elif title == "Mrs":
            return 2
        elif title == "Ms":
            return 3
        elif title == "นาย":
            return 4
        elif title == "นาง":
            return 5
        elif title == "นางสาว":
            return 6
        else:
            return 0

    # Function that prepare form data for registration and returns a dictionary with form data to be sent along with post request
    def register_details(self,response, postdata):
        register_data = {}
        soup = BeautifulSoup(response.text, "html5lib")

        captcha = soup.find("span", attrs={"id": "ContentPlaceHolder1_lblCaptcha"}).text
        viewState = soup.find("input", attrs={"id": "__VIEWSTATE"})["value"]
        viewStateGenerator = soup.find("input", attrs={"id": "__VIEWSTATEGENERATOR"})["value"]

        register_data["__EVENTTARGET"] = ""
        register_data["__EVENTARGUMENT"] = ""
        register_data["__VIEWSTATE"] = viewState
        register_data["__VIEWSTATEGENERATOR"] = viewStateGenerator
        register_data["ctl00$ContentPlaceHolder1$lblTitle"] = self.title_value(postdata["name_title"])
        register_data["ctl00$ContentPlaceHolder1$lblName"] = postdata["name_th"]
        register_data["ctl00$ContentPlaceHolder1$lblSurName"] = postdata["surname_th"]
        register_data["ctl00$ContentPlaceHolder1$lblEmail"] = postdata["user"]
        register_data["ctl00$ContentPlaceHolder1$lblMobile"] = postdata["tel"]
        register_data["ctl00$ContentPlaceHolder1$lblPassword"] = postdata["pass"]
        register_data["ctl00$ContentPlaceHolder1$lblPasswordconfirm"] = postdata["pass"]
        register_data["ctl00$ContentPlaceHolder1$RadioType"] = 2
        register_data["ctl00$ContentPlaceHolder1$lblEnew"] = "on"
        register_data["ctl00$ContentPlaceHolder1$Privacy"] = "on"
        register_data["ctl00$ContentPlaceHolder1$txtCaptcha"] = captcha
        register_data["ctl00$ContentPlaceHolder1$BtnRegister"] = "สมัครสมาชิก"

        return register_data

    # Funtion that register user on website

    def register_user(self,postdata):
        self.logout_user()
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()
        url = "https://www.thaiapartment.com/register"

        #session = requests.session()
        #r = session.get(url)
        r=self.httprequestObj.http_get(url)
        register_data = self.register_details(r, postdata)
        #response = session.post(url, data=register_data)
        response=self.httprequestObj.http_post(url,data=register_data)
        soup = BeautifulSoup(response.text, "html5lib")
        txt = soup.find("script", attrs={"type": "text/javascript"}).text
        detail = re.findall(r"'.*?'", txt)[0]
        detail = re.sub("'", "", detail)


        if detail == "ท่านได้ทำการสมัครสมาชิกแล้วระบบได้ส่งลิงค์เพื่อยืนยันไปทางอีเมลของท่านโปรดตรวจสอบเมลหากไม่พบกรุณาตรวจสอบใน junk mail ด้วยครับ":
            detail = "Registered successfully, Please check mail for activation"
            success = "true"
        else:
            detail = detail+ " Can't register."
            success = "false"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            'ds_id': postdata['ds_id'],
            "detail": detail,
            "websitename": self.webname,
        }

    """
    def register_user(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']

        r = self.httprequestObj.http_get('https://www.thaiapartment.com/register')
        print(r.url)
        print(r.status_code)

        ##with open('/home/codelover/Desktop/rough.html', 'w') as f:
        #   #f.write(r.text)

        soup = BeautifulSoup(r.text, 'html5lib')
        # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
        # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
        viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
        viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')

        # print(event_target)
        # print(event_argument)
        print(viewstate)
        print(viewstate_gen)

        captcha = soup.find('span', {'id': 'ContentPlaceHolder1_lblCaptcha'}).text
        print(captcha)

        datapost = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': viewstate_gen,
            'ctl00$ContentPlaceHolder1$lblTitle': '1',
            'ctl00$ContentPlaceHolder1$lblName': postdata['name_th'],
            'ctl00$ContentPlaceHolder1$lblSurName': postdata['surname_th'],
            'ctl00$ContentPlaceHolder1$lblEmail': postdata['user'],
            'ctl00$ContentPlaceHolder1$lblMobile': postdata['tel'],
            'ctl00$ContentPlaceHolder1$lblPassword': postdata['pass'],
            'ctl00$ContentPlaceHolder1$lblPasswordconfirm': postdata['pass'],
            'ctl00$ContentPlaceHolder1$RadioType': '3',
            "ctl00$ContentPlaceHolder1$lblEnew": 'on',
            'ctl00$ContentPlaceHolder1$Privacy': 'on',
            'ctl00$ContentPlaceHolder1$txtCaptcha': captcha,
            'ctl00$ContentPlaceHolder1$BtnRegister': 'สมัครสมาชิก'
        }

        res = self.httprequestObj.http_post('http://thaiapartment.com/register',data=datapost)
        print(res.url)
        print(res.status_code)

        #with open('/home/aymaan/Desktop/rough.html', 'w') as f:
        #  f.write(res.text)

        soup1 = BeautifulSoup(res.text, "html5lib")
        txt = soup1.find("script", attrs={"type": "text/javascript"}).text
        print(txt)
        result = re.findall(r"'.*?'", txt)[0]
        result = re.sub("'", "", result)

        if 'ท่านได้ทำการสมัครสมาชิกแล้วระบบได้ส่งลิงค์เพื่อยืนยันไปทางอีเมลของท่านโปรดตรวจสอบเมลหากไม่พบกรุณาตรวจสอบใน junk mail ด้วยครับั' in result:
            success = True
            detail = "Registered successfully, Please check mail for activation"
        else:
            success = False
            detail = "Couldnot register"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            'ds_id': postdata['ds_id'],
            "detail": detail,
            "websitename": self.webname,
        }
    """


    def test_login(self, postdata):
        self.logout_user()
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']

        r = self.httprequestObj.http_get('https://www.thaiapartment.com/login')
        print(r.url)
        print(r.status_code)

        ##with open('/home/codelover/Desktop/rough.html', 'w') as f:
        #    #f.write(r.text)

        soup = BeautifulSoup(r.content, self.parser)
        # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
        # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
        viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
        viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')

        # print(event_target)
        # print(event_argument)
        print(viewstate)
        print(viewstate_gen)

        # captcha = soup.find('span', {'id': 'ContentPlaceHolder1_lblCaptcha'}).string
        # print(captcha)

        datapost = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': viewstate_gen,
            'ctl00$ContentPlaceHolder1$lblEmail': postdata['user'],
            'ctl00$ContentPlaceHolder1$lblPassword': postdata['pass'],
            'ctl00$ContentPlaceHolder1$submit': 'Sign in'
        }

        r = self.httprequestObj.http_post('https://www.thaiapartment.com/login', data=datapost)
        print(r.url)
        print(r.status_code)

        ##with open('/home/codelover/Desktop/rough.html', 'w') as f:
         #   #f.write(r.text)

        if 'Logout' in r.text:
            success = True
            detail = "Login successful"
        else:
            success = False
            detail = "Couldnot login"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            'ds_id': postdata['ds_id'],
            "detail": detail,
            "websitename": self.webname,
        }

    def create_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        # start process
        #

        # login

        # print(postdata)
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""

        if success:
            if 'web_project_name' not in postdata or postdata['web_project_name'] is None:
                if 'project_name' in postdata and postdata['project_name'] is not None:
                    postdata['web_project_name'] = postdata['project_name']
                else:
                    postdata['web_project_name'] = postdata['post_title_th']

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
                'โกดัง-โรงงาน': '10',
                'โรงงาน': '25'
            }
            getProdId = {'1': 159, '2': 156, '3': 156, '4': 157,
                         '5': 158, '6': 161, '7': 162, '8': 162, '9': 162, '10': 162, '25': 162}

            try:
                theprodid = getProdId[proid[str(postdata['property_type'])]]
                postdata['property_type'] = proid[str(postdata['property_type'])]
            except:
                theprodid = getProdId[str(postdata['property_type'])]

            prod_address = ""
            for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'],
                        postdata['addr_district'], postdata['addr_province']]:
                if add is not None:
                    prod_address += add + " "
            prod_address = prod_address[:-1]

            r = self.httprequestObj.http_get('https://www.thaiapartment.com/agree')
            print(r.url)
            print(r.status_code)

            soup = BeautifulSoup(r.content, self.parser)
            # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
            # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
            viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
            viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
            event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')

            # print(event_target)
            # print(event_argument)
            print(viewstate)
            print(viewstate_gen)

            captcha = soup.find('span', {'id': 'ContentPlaceHolder1_lblCaptcha'}).string
            print(captcha)

            datapost = {
                '__EVENTTARGET': '',
                '__EVENTARGUMENT': '',
                '__VIEWSTATE': viewstate,
                '__VIEWSTATEGENERATOR': viewstate_gen,
                '__EVENTVALIDATION': event_validation,
                'ctl00$ContentPlaceHolder1$txtCaptcha': captcha,
                'ctl00$ContentPlaceHolder1$BtnSubmit': 'ยอมรับเงื่อนไขและลงประกาศ'
            }

            r = self.httprequestObj.http_post('https://www.thaiapartment.com/agree', data=datapost)
            print(r.url)
            print(r.status_code)

            print('Agreement signed')

            if postdata['property_type'] == '7':
                r = self.httprequestObj.http_get('https://www.thaiapartment.com/postadd')
                #print(r.url)
                #print(r.status_code)

                ##with open('/home/codelover/Desktop/rough.html', 'w') as f:
                #   #f.write(r.text)

                soup = BeautifulSoup(r.content, self.parser)
                # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
                # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
                viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
                viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
                # event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')

                data = '{"knownCategoryValues":"","category":"PROVINCE_ID"}'

                r = self.httprequestObj.http_post('https://www.thaiapartment.com/propertyupdateservice.asmx/GetProvince',
                                             headers={'content-type': 'application/json; charset=UTF-8'}, data=data)
                #print(r.url)
                #print(r.status_code)

                data = r.json()['d']
                #print(data)
                province_id = data[0]['value']
                province_name = data[0]['name']

                for row in data:
                    area = row['name']
                    if area.replace(' ', '') in postdata['addr_province'].replace(' ', '') or postdata[
                        'addr_province'].replace(' ', '') in area.replace(' ', ''):
                        province_id = row['value']
                        province_name = area
                        break

                #print('Province_id = ' + province_id)

                data = '{"knownCategoryValues":"PROVINCE_ID:' + province_id + ';","category":"AMPHUR_ID"}'

                r = self.httprequestObj.http_post('https://www.thaiapartment.com/propertyupdateservice.asmx/GetAmphur', headers= {'content-type': 'application/json; charset=UTF-8'}, data=data)
                #print(r.url)
                #print(r.status_code)

                data = r.json()['d']
                district_id = data[0]['value']
                district_name = data[0]['name']

                for row in data:
                    area = row['name']
                    if area.replace(' ', '') in postdata['addr_district'].replace(' ', '') or postdata[
                        'addr_district'].replace(' ', '') in area.replace(' ', ''):
                        district_id = row['value']
                        district_name = area
                        break

                #print('District_id = ' + district_id)

                data = '{"knownCategoryValues":"PROVINCE_ID:'+province_id+';AMPHUR_ID:'+district_id+';","category":"DISTRICT_ID"}'

                r = self.httprequestObj.http_post('https://www.thaiapartment.com/propertyupdateservice.asmx/GetDistrict',
                                             headers={'content-type': 'application/json; charset=UTF-8'}, data=data)
                #print(r.url)
                #print(r.status_code)

                data = r.json()['d']
                sub_district_id = data[0]['value']
                sub_district_name = data[0]['name']

                for row in data:
                    area = row['name']
                    if area.replace(' ', '') in postdata['addr_sub_district'].replace(' ', '') or postdata[
                        'addr_sub_district'].replace(' ', '') in area.replace(' ', ''):
                        sub_district_id = row['value']
                        sub_district_name = area
                        break

                #print('Subdistrict_id = ' + sub_district_id)

                # print(event_target)
                # print(event_argument)
                #print(viewstate)
                #print(viewstate_gen)
                datapost = [
                    ('__EVENTTARGET', ''),
                    ('__EVENTARGUMENT', ''),
                    ('__VIEWSTATE', viewstate),
                    ('__VIEWSTATEGENERATOR', viewstate_gen),
                    ('ctl00$ContentPlaceHolder1$lblProjectNameTH', postdata['web_project_name']),
                    ('ctl00$ContentPlaceHolder1$lblProjectName', ''),
                    ('ctl00$ContentPlaceHolder1$lblName', postdata['name']),
                    ('ctl00$ContentPlaceHolder1$lblPhone', postdata['mobile']),
                    ('ctl00$ContentPlaceHolder1$lblEmail', postdata['email']),
                    ('ctl00$ContentPlaceHolder1$lblAddress', ''),
                    ('ctl00$ContentPlaceHolder1$lblSoi', postdata['addr_soi']),
                    ('ctl00$ContentPlaceHolder1$lblRoad', postdata['addr_road']),
                    ('ctl00$ContentPlaceHolder1$lblprovince', province_id),
                    ('ctl00$ContentPlaceHolder1$cdlProvince_ClientState', province_id+':::'+province_name+':::'),
                    ('ctl00$ContentPlaceHolder1$lblamphur', district_id),
                    ('ctl00$ContentPlaceHolder1$cdlAmphur_ClientState', district_id+':::'+district_name+':::'),
                    ('ctl00$ContentPlaceHolder1$lbldistrict', sub_district_id),
                    ('ctl00$ContentPlaceHolder1$cdlDistrict_ClientState', sub_district_id+':::'+sub_district_name+':::'),
                    ('ctl00$ContentPlaceHolder1$lblDetailTH', postdata['post_description_th'].replace('\r\n', '&lt;div&gt;')),
                    ('FontName', 'arial,helvetica,sans-serif'),
                    ('FontName', 'arial,helvetica,sans-serif'),
                    ('FontSize', '1'),
                    ('FontSize', '1'),
                    ('ctl00$ContentPlaceHolder1$HtmlEditorExtender1_ClientState', ''),
                    ('ctl00$ContentPlaceHolder1$lblDetailENG', ''),
                    ('ctl00$ContentPlaceHolder1$HtmlEditorExtender2_ClientState', ''),
                    ('ctl00$ContentPlaceHolder1$BtnRegister', 'ขั้นตอนต่อไป'),
                    ('hiddenInputToUpdateATBuffer_CommonToolkitScripts', '0'),
                ]

                r = self.httprequestObj.http_post('https://www.thaiapartment.com/postadd', data=datapost)

                post_id = r.url.split('=')[-1]

                r = self.httprequestObj.http_get('https://www.thaiapartment.com/post2?id=' + post_id, data=datapost)

                soup = BeautifulSoup(r.content, self.parser)
                # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
                # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
                viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
                viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')

                datapost = {
                    '__EVENTTARGET': '',
                    '__EVENTARGUMENT': '',
                    '__VIEWSTATE': viewstate,
                    '__VIEWSTATEGENERATOR': viewstate_gen,
                    '__VIEWSTATEENCRYPTED': '',
                    'ctl00$ContentPlaceHolder1$apRoomName': '',
                    'ctl00$ContentPlaceHolder1$apRoomType': postdata['bed_room'],
                    'ctl00$ContentPlaceHolder1$apRoomSize': postdata['floorarea_sqm'],
                    'ctl00$ContentPlaceHolder1$apDaily': '',
                    'ctl00$ContentPlaceHolder1$apMonthly': postdata['price_baht'],
                    'ctl00$ContentPlaceHolder1$BtnSave': 'บันทึกราคา',
                    'ctl00$ContentPlaceHolder1$lblWaterCharge': '',
                    'ctl00$ContentPlaceHolder1$lblElectricityCharge': '',
                    'ctl00$ContentPlaceHolder1$lblDeposit': '',
                    'ctl00$ContentPlaceHolder1$lblPayinadvance': '',
                    'ctl00$ContentPlaceHolder1$lblInternetCharge': '',
                    'ctl00$ContentPlaceHolder1$lblPromotionDetail': '',
                    'FontName': 'arial,helvetica,sans-serif',
                    'FontSize': '1',
                    'ctl00$ContentPlaceHolder1$HtmlEditorExtender2_ClientState': ''
                }

                r = self.httprequestObj.http_post('https://www.thaiapartment.com/post2?id=' + post_id, data=datapost)

                r = self.httprequestObj.http_get('https://www.thaiapartment.com/post2?id=' + post_id)

                soup = BeautifulSoup(r.content, self.parser)
                # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
                # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
                viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
                viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')

                datapost = {
                    '__EVENTTARGET': '',
                    '__EVENTARGUMENT': '',
                    '__VIEWSTATE': viewstate,
                    '__VIEWSTATEGENERATOR': viewstate_gen,
                    '__VIEWSTATEENCRYPTED': '',
                    'ctl00$ContentPlaceHolder1$apRoomName': '',
                    'ctl00$ContentPlaceHolder1$apRoomType': '',
                    'ctl00$ContentPlaceHolder1$apRoomSize': '',
                    'ctl00$ContentPlaceHolder1$apDaily': '',
                    'ctl00$ContentPlaceHolder1$apMonthly': '',
                    'ctl00$ContentPlaceHolder1$lblWaterCharge': '',
                    'ctl00$ContentPlaceHolder1$lblElectricityCharge': '',
                    'ctl00$ContentPlaceHolder1$lblDeposit': '',
                    'ctl00$ContentPlaceHolder1$lblPayinadvance': '',
                    'ctl00$ContentPlaceHolder1$lblInternetCharge': '',
                    'ctl00$ContentPlaceHolder1$lblPromotionDetail': '',
                    'FontName': 'arial,helvetica,sans-serif',
                    'FontSize': '1',
                    'ctl00$ContentPlaceHolder1$HtmlEditorExtender2_ClientState': '',
                    'ctl00$ContentPlaceHolder1$BtnRegister': 'ขั้นตอนต่อไป'
                }

                r = self.httprequestObj.http_post('https://www.thaiapartment.com/post2?id=' + post_id, data=datapost)

                # r = self.httprequestObj.http_get('https://www.thaiapartment.com/post3?id=3326', data=datapost)
                # print(r.url)
                # print(r.status_code)
                #
                # soup = BeautifulSoup(r.content, self.parser)
                # # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
                # # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
                # viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
                # viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
                # event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')

                r = self.httprequestObj.http_get('https://www.thaiapartment.com/post3?id=' + post_id)

                ##with open('/home/codelover/Desktop/rough.html', 'w') as f:
                #   #f.write(r.text)

                for i, img in enumerate(postdata['post_images']):
                    r = self.httprequestObj.http_get('https://www.thaiapartment.com/post3?id=' + post_id)

                    # #with open('/home/codelover/Desktop/rough.html', 'w') as f:
                    #     #f.write(r.text)

                    soup = BeautifulSoup(r.content, self.parser)
                    # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
                    # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
                    viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
                    viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
                    event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')

                    filename = str(i) + '.jpeg'
                    datapost = [
                        ('__EVENTTARGET', (None, '')),
                        ('__EVENTARGUMENT', (None, '')),
                        ('__VIEWSTATE', (None, viewstate)),
                        ('__VIEWSTATEGENERATOR', (None, viewstate_gen)),
                        ('__EVENTVALIDATION', (None, event_validation)),
                        ('ctl00$ContentPlaceHolder1$UploadImages', (filename, open(img, 'rb'), 'image/jpeg')),
                        ('ctl00$ContentPlaceHolder1$uploadedFile', (None, 'Upload'))
                    ]

                    r = self.httprequestObj.http_post('https://www.thaiapartment.com/post3?id=' + post_id, data={}, files=datapost)

                r = self.httprequestObj.http_get('https://www.thaiapartment.com/post3?id=' + post_id)

                soup = BeautifulSoup(r.content, self.parser)
                # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
                # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
                viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
                viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
                event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')

                datapost = [
                    ('__EVENTTARGET', (None, '')),
                    ('__EVENTARGUMENT', (None, '')),
                    ('__VIEWSTATE', (None, viewstate)),
                    ('__VIEWSTATEGENERATOR', (None, viewstate_gen)),
                    ('__EVENTVALIDATION', (None, event_validation)),
                    ('ctl00$ContentPlaceHolder1$UploadImages', (None, '')),
                    ('ctl00$ContentPlaceHolder1$uploadedFile', (None, 'โพสประกาศอพาร์ทเม้นท์'))
                ]

                r = self.httprequestObj.http_post('https://www.thaiapartment.com/post3?id=' + post_id, data={}, files=datapost)

                # #with open('/home/codelover/Desktop/rough.html', 'w') as f:
                #     #f.write(r.text)

                success = True
                post_url="https://www.thaiapartment.com/post?id="+post_id
                detail = 'xxx'

            elif postdata['property_type'] == '1':
                r = self.httprequestObj.http_get('https://www.thaiapartment.com/condoadd')
                ######with open('/home/codelover/Desktop/rough.html', 'w') as f:
                #    #f.write(r.text)

                soup = BeautifulSoup(r.content, self.parser)
                # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
                # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
                viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
                viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
                # event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')

                project_names = soup.find('select', {'name': 'ctl00$ContentPlaceHolder1$lblProjectID'}).findChildren('option')[1:]

                project_id = 0
                for project in project_names:
                    name = project.string
                    if name.replace(' ', '') in postdata['web_project_name'].replace(' ', '') or postdata['web_project_name'].replace(' ', '') in name.replace(' ', ''):
                        project_id = project.get('value')
                        break

                # data = '{"knownCategoryValues":"","category":"PROVINCE_ID"}'

                # r = self.httprequestObj.http_post('https://www.thaiapartment.com/propertyupdateservice.asmx/GetProvince',
                #                              headers={'content-type': 'application/json; charset=UTF-8'}, data=data)
                # print(r.url)
                # print(r.status_code)
                #
                # data = r.json()['d']
                # print(data)
                # province_id = data[0]['value']
                # province_name = data[0]['name']
                #
                # for row in data:
                #     area = row['name']
                #     if area.replace(' ', '') in postdata['addr_province'].replace(' ', '') or postdata[
                #         'addr_province'].replace(' ', '') in area.replace(' ', ''):
                #         province_id = row['value']
                #         province_name = area
                #         break
                #
                # print('Province_id = ' + province_id)
                #
                # data = '{"knownCategoryValues":"PROVINCE_ID:' + province_id + ';","category":"AMPHUR_ID"}'
                #
                # r = self.httprequestObj.http_post('https://www.thaiapartment.com/propertyupdateservice.asmx/GetAmphur',
                #                              headers={'content-type': 'application/json; charset=UTF-8'}, data=data)
                # print(r.url)
                # print(r.status_code)
                #
                # data = r.json()['d']
                # district_id = data[0]['value']
                # district_name = data[0]['name']
                #
                # for row in data:
                #     area = row['name']
                #     if area.replace(' ', '') in postdata['addr_district'].replace(' ', '') or postdata[
                #         'addr_district'].replace(' ', '') in area.replace(' ', ''):
                #         district_id = row['value']
                #         district_name = area
                #         break
                #
                # print('District_id = ' + district_id)
                #
                # data = '{"knownCategoryValues":"PROVINCE_ID:' + province_id + ';AMPHUR_ID:' + district_id + ';","category":"DISTRICT_ID"}'
                #
                # r = self.httprequestObj.http_post('https://www.thaiapartment.com/propertyupdateservice.asmx/GetDistrict',
                #                              headers={'content-type': 'application/json; charset=UTF-8'}, data=data)
                # print(r.url)
                # print(r.status_code)
                #
                # data = r.json()['d']
                # sub_district_id = data[0]['value']
                # sub_district_name = data[0]['name']
                #
                # for row in data:
                #     area = row['name']
                #     if area.replace(' ', '') in postdata['addr_sub_district'].replace(' ', '') or postdata[
                #         'addr_sub_district'].replace(' ', '') in area.replace(' ', ''):
                #         sub_district_id = row['value']
                #         sub_district_name = area
                #         break
                #
                # print('Subdistrict_id = ' + sub_district_id)

                # print(event_target)
                # print(event_argument)
                datapost = [
                    ('__EVENTTARGET', ''),
                    ('__EVENTARGUMENT', ''),
                    ('__VIEWSTATE', viewstate),
                    ('__VIEWSTATEGENERATOR', viewstate_gen),
                    ('ctl00$ContentPlaceHolder1$lblProjectID', project_id),
                    ('ctl00$ContentPlaceHolder1$lblProjectName', postdata['web_project_name']),
                    ('ctl00$ContentPlaceHolder1$lblPropertyTitle', postdata['post_title_th']),
                    ('ctl00$ContentPlaceHolder1$lblPropertyTitleEng', ''),
                    ('ctl00$ContentPlaceHolder1$lblDescription', postdata['post_description_th'].replace('\r\n', '&lt;div&gt;')),
                    ('FontName', 'arial,helvetica,sans-serif'),
                    ('FontName', 'arial,helvetica,sans-serif'),
                    ('FontSize', '1'),
                    ('FontSize', '1'),
                    ('ctl00$ContentPlaceHolder1$HtmlEditorExtender1_ClientState', ''),
                    ('ctl00$ContentPlaceHolder1$lblDescriptionEng', ''),
                    ('ctl00$ContentPlaceHolder1$HtmlEditorExtender2_ClientState', ''),
                    ('ctl00$ContentPlaceHolder1$lblProjectHighlight', ''),
                    ('ctl00$ContentPlaceHolder1$lblProjectHighlightEng', ''),
                    ('ctl00$ContentPlaceHolder1$lblFurniture', ''),
                    ('ctl00$ContentPlaceHolder1$lblFurnitureEng', ''),
                    ('ctl00$ContentPlaceHolder1$lblPriceMonth', postdata['price_baht']),
                    ('ctl00$ContentPlaceHolder1$lblPeriod', '12'),
                    ('ctl00$ContentPlaceHolder1$lblArea', postdata['floorarea_sqm']),
                    ('ctl00$ContentPlaceHolder1$lblFloorNo', postdata['floor_level']),
                    ('ctl00$ContentPlaceHolder1$lblTower', ''),
                    ('ctl00$ContentPlaceHolder1$lblBedroom', postdata['bed_room']),
                    ('ctl00$ContentPlaceHolder1$lblBathroom', postdata['bath_room']),
                    ('ctl00$ContentPlaceHolder1$BtnRegister', 'ขั้นตอนต่อไป'),
                ]

                r = self.httprequestObj.http_post('https://www.thaiapartment.com/condoadd', data=datapost)
                print(r.url)
                print(r.status_code)


                post_id = r.url.split('=')[-1]

                r = self.httprequestObj.http_get('https://www.thaiapartment.com/condo2?id=' + post_id, data=datapost)
                print(r.url)
                print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
                # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
                viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
                viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
                event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')

                # datapost = {
                #     '__EVENTTARGET': '',
                #     '__EVENTARGUMENT': '',
                #     '__VIEWSTATE': viewstate,
                #     '__VIEWSTATEGENERATOR': viewstate_gen,
                #     '__VIEWSTATEENCRYPTED': '',
                #     'ctl00$ContentPlaceHolder1$apRoomName': '',
                #     'ctl00$ContentPlaceHolder1$apRoomType': postdata['bed_room'],
                #     'ctl00$ContentPlaceHolder1$apRoomSize': postdata['floorarea_sqm'],
                #     'ctl00$ContentPlaceHolder1$apDaily': '',
                #     'ctl00$ContentPlaceHolder1$apMonthly': postdata['price_baht'],
                #     'ctl00$ContentPlaceHolder1$BtnSave': 'บันทึกราคา',
                #     'ctl00$ContentPlaceHolder1$lblWaterCharge': '',
                #     'ctl00$ContentPlaceHolder1$lblElectricityCharge': '',
                #     'ctl00$ContentPlaceHolder1$lblDeposit': '',
                #     'ctl00$ContentPlaceHolder1$lblPayinadvance': '',
                #     'ctl00$ContentPlaceHolder1$lblInternetCharge': '',
                #     'ctl00$ContentPlaceHolder1$lblPromotionDetail': '',
                #     'FontName': 'arial,helvetica,sans-serif',
                #     'FontSize': '1',
                #     'ctl00$ContentPlaceHolder1$HtmlEditorExtender2_ClientState': ''
                # }
                #
                # r = self.httprequestObj.http_post('https://www.thaiapartment.com/post2?id=' + post_id, data=datapost)
                # print(r.url)
                # print(r.status_code)
                #
                # r = self.httprequestObj.http_get('https://www.thaiapartment.com/post2?id=' + post_id)
                # print(r.url)
                # print(r.status_code)
                #
                # soup = BeautifulSoup(r.content, self.parser)
                # # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
                # # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
                # viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
                # viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')

                # datapost = {
                #     '__EVENTTARGET': '',
                #     '__EVENTARGUMENT': '',
                #     '__VIEWSTATE': viewstate,
                #     '__VIEWSTATEGENERATOR': viewstate_gen,
                #     '__EVENTVALIDATION': event_validation,
                #     'ctl00$ContentPlaceHolder1$apRoomName': '',
                #     'ctl00$ContentPlaceHolder1$apRoomType': '',
                #     'ctl00$ContentPlaceHolder1$apRoomSize': '',
                #     'ctl00$ContentPlaceHolder1$apDaily': '',
                #     'ctl00$ContentPlaceHolder1$apMonthly': '',
                #     'ctl00$ContentPlaceHolder1$lblWaterCharge': '',
                #     'ctl00$ContentPlaceHolder1$lblElectricityCharge': '',
                #     'ctl00$ContentPlaceHolder1$lblDeposit': '',
                #     'ctl00$ContentPlaceHolder1$lblPayinadvance': '',
                #     'ctl00$ContentPlaceHolder1$lblInternetCharge': '',
                #     'ctl00$ContentPlaceHolder1$lblPromotionDetail': '',
                #     'FontName': 'arial,helvetica,sans-serif',
                #     'FontSize': '1',
                #     'ctl00$ContentPlaceHolder1$HtmlEditorExtender2_ClientState': '',
                #     'ctl00$ContentPlaceHolder1$BtnRegister': 'ขั้นตอนต่อไป'
                # }
                #
                # r = self.httprequestObj.http_post('https://www.thaiapartment.com/post2?id=' + post_id, data=datapost)
                # print(r.url)
                # print(r.status_code)

                # r = self.httprequestObj.http_get('https://www.thaiapartment.com/post3?id=3326', data=datapost)
                # print(r.url)
                # print(r.status_code)
                #
                # soup = BeautifulSoup(r.content, self.parser)
                # # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
                # # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
                # viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
                # viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
                # event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')

                # r = self.httprequestObj.http_get('https://www.thaiapartment.com/post3?id=' + post_id)
                # print(r.url)
                # print(r.status_code)
                #
                # #with open('/home/codelover/Desktop/rough.html', 'w') as f:
                #     #f.write(r.text)

                for i, img in enumerate(postdata['post_images']):
                    r = self.httprequestObj.http_get('https://www.thaiapartment.com/condo2?id=' + post_id)
                    print(r.url)
                    print(r.status_code)

                    # #with open('/home/codelover/Desktop/rough.html', 'w') as f:
                    #     #f.write(r.text)

                    soup = BeautifulSoup(r.content, self.parser)
                    # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
                    # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
                    viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
                    viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
                    event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')

                    index_name = 'ctl00$ContentPlaceHolder1$FileUpload' + str(i+1)
                    filename = str(i) + '.jpeg'
                    datapost = [
                        ('__EVENTTARGET', (None, '')),
                        ('__EVENTARGUMENT', (None, '')),
                        ('__VIEWSTATE', (None, viewstate)),
                        ('__VIEWSTATEGENERATOR', (None, viewstate_gen)),
                        ('__EVENTVALIDATION', (None, event_validation)),
                        (index_name, (filename, open(img, 'rb'), 'image/jpeg')),
                        ('ctl00$ContentPlaceHolder1$lblPackage', (None, '0'))
                    ]

                    r = self.httprequestObj.http_post('https://www.thaiapartment.com/condo2?id=' + post_id, data={},
                                                 files=datapost)
                    print(r.url)
                    print(r.status_code)

                r = self.httprequestObj.http_get('https://www.thaiapartment.com/condo2?id=' + post_id)
                print(r.url)
                print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
                # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
                viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
                viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
                event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')

                datapost = [
                    ('__EVENTTARGET', (None, '')),
                    ('__EVENTARGUMENT', (None, '')),
                    ('__VIEWSTATE', (None, viewstate)),
                    ('__VIEWSTATEGENERATOR', (None, viewstate_gen)),
                    ('__EVENTVALIDATION', (None, event_validation)),
                    ('ctl00$ContentPlaceHolder1$FileUpload1', (None, '')),
                    ('ctl00$ContentPlaceHolder1$FileUpload2', (None, '')),
                    ('ctl00$ContentPlaceHolder1$FileUpload3', (None, '')),
                    ('ctl00$ContentPlaceHolder1$FileUpload4', (None, '')),
                    ('ctl00$ContentPlaceHolder1$FileUpload5', (None, '')),
                    ('ctl00$ContentPlaceHolder1$FileUpload6', (None, '')),
                    ('ctl00$ContentPlaceHolder1$lblPackage', (None, '0')),
                    ('ctl00$ContentPlaceHolder1$BtnRegister', (None, 'โพสต์ประกาศคอนโด'))
                ]

                r = self.httprequestObj.http_post('https://www.thaiapartment.com/condo2?id=' + post_id, data={},
                                             files=datapost)
                print(r.url)
                print(r.status_code)

                # #with open('/home/codelover/Desktop/rough.html', 'w') as f:
                #     #f.write(r.text)

                success = True
                detail = 'Post created successfully'
                post_url="https://www.thaiapartment.com/condo?id="+post_id
            else:
                success = False
                detail = "Only condo/apartment posts allowed"

        else:
            success = False
            detail = "Couldnot login"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": post_url,
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
            "websitename": self.webname,
        }

    def edit_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""

        if success:

            post_found = False

            r = self.httprequestObj.http_get('https://www.thaiapartment.com/allpost')
            print(r.url)
            print(r.status_code)

            soup = BeautifulSoup(r.content, self.parser)
            all_posts = soup.find_all('a', 'img-responsive img-thumbnail')

            for post in all_posts:
                post_id = post.get('href').split('=')[-1]
                print(post_id)
                if post_id == postdata['post_id']:
                    post_found = True
                    break

            if post_found:
                if 'web_project_name' not in postdata or postdata['web_project_name'] is None:
                    if 'project_name' in postdata and postdata['project_name'] is not None:
                        postdata['web_project_name'] = postdata['project_name']
                    else:
                        postdata['web_project_name'] = postdata['post_title_th']

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
                    'โกดัง-โรงงาน': '10',
                    'โรงงาน': '25'
                }
                getProdId = {'1': 159, '2': 156, '3': 156, '4': 157,
                             '5': 158, '6': 161, '7': 162, '8': 162, '9': 162, '10': 162, '25': 162}

                try:
                    theprodid = getProdId[proid[str(postdata['property_type'])]]
                    postdata['property_type'] = proid[str(postdata['property_type'])]
                except:
                    theprodid = getProdId[str(postdata['property_type'])]

                prod_address = ""
                for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'],
                            postdata['addr_district'], postdata['addr_province']]:
                    if add is not None:
                        prod_address += add + " "
                prod_address = prod_address[:-1]



                # captcha = soup.find('span', {'id': 'ContentPlaceHolder1_lblCaptcha'}).string
                # print(captcha)

                if postdata['property_type'] == '7':

                    r = self.httprequestObj.http_get('https://www.thaiapartment.com/post', params={'id': post_id})
                    print(r.url)
                    print(r.status_code)

                    soup = BeautifulSoup(r.content, self.parser)
                    # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
                    # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
                    viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
                    viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
                    # event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')

                    # print(event_target)
                    # print(event_argument)
                    print(viewstate)
                    print(viewstate_gen)

                    data = '{"knownCategoryValues":"","category":"PROVINCE_ID"}'

                    r = self.httprequestObj.http_post('https://www.thaiapartment.com/propertyupdateservice.asmx/GetProvince',
                                                 headers={'content-type': 'application/json; charset=UTF-8'}, data=data)
                    print(r.url)
                    print(r.status_code)

                    data = r.json()['d']
                    print(data)
                    province_id = data[0]['value']
                    province_name = data[0]['name']

                    for row in data:
                        area = row['name']
                        if area.replace(' ', '') in postdata['addr_province'].replace(' ', '') or postdata[
                            'addr_province'].replace(' ', '') in area.replace(' ', ''):
                            province_id = row['value']
                            province_name = area
                            break

                    print('Province_id = ' + province_id)

                    data = '{"knownCategoryValues":"PROVINCE_ID:' + province_id + ';","category":"AMPHUR_ID"}'

                    r = self.httprequestObj.http_post('https://www.thaiapartment.com/propertyupdateservice.asmx/GetAmphur', headers= {'content-type': 'application/json; charset=UTF-8'}, data=data)
                    print(r.url)
                    print(r.status_code)

                    data = r.json()['d']
                    district_id = data[0]['value']
                    district_name = data[0]['name']

                    for row in data:
                        area = row['name']
                        if area.replace(' ', '') in postdata['addr_district'].replace(' ', '') or postdata[
                            'addr_district'].replace(' ', '') in area.replace(' ', ''):
                            district_id = row['value']
                            district_name = area
                            break

                    print('District_id = ' + district_id)

                    data = '{"knownCategoryValues":"PROVINCE_ID:'+province_id+';AMPHUR_ID:'+district_id+';","category":"DISTRICT_ID"}'

                    r = self.httprequestObj.http_post('https://www.thaiapartment.com/propertyupdateservice.asmx/GetDistrict',
                                                 headers={'content-type': 'application/json; charset=UTF-8'}, data=data)
                    print(r.url)
                    print(r.status_code)

                    data = r.json()['d']
                    sub_district_id = data[0]['value']
                    sub_district_name = data[0]['name']

                    for row in data:
                        area = row['name']
                        if area.replace(' ', '') in postdata['addr_sub_district'].replace(' ', '') or postdata[
                            'addr_sub_district'].replace(' ', '') in area.replace(' ', ''):
                            sub_district_id = row['value']
                            sub_district_name = area
                            break

                    print('Subdistrict_id = ' + sub_district_id)

                    # print(event_target)
                    # print(event_argument)
                    print(viewstate)
                    print(viewstate_gen)

                    datapost = [
                        ('__EVENTTARGET', ''),
                        ('__EVENTARGUMENT', ''),
                        ('__VIEWSTATE', viewstate),
                        ('__VIEWSTATEGENERATOR', viewstate_gen),
                        ('ctl00$ContentPlaceHolder1$lblProjectNameTH', postdata['web_project_name']),
                        ('ctl00$ContentPlaceHolder1$lblProjectName', ''),
                        ('ctl00$ContentPlaceHolder1$lblName', postdata['name']),
                        ('ctl00$ContentPlaceHolder1$lblPhone', postdata['mobile']),
                        ('ctl00$ContentPlaceHolder1$lblEmail', postdata['email']),
                        ('ctl00$ContentPlaceHolder1$lblAddress', ''),
                        ('ctl00$ContentPlaceHolder1$lblSoi', postdata['addr_soi']),
                        ('ctl00$ContentPlaceHolder1$lblRoad', postdata['addr_road']),
                        ('ctl00$ContentPlaceHolder1$lblprovince', province_id),
                        ('ctl00$ContentPlaceHolder1$cdlProvince_ClientState', province_id+':::'+province_name+':::'),
                        ('ctl00$ContentPlaceHolder1$lblamphur', district_id),
                        ('ctl00$ContentPlaceHolder1$cdlAmphur_ClientState', district_id+':::'+district_name+':::'),
                        ('ctl00$ContentPlaceHolder1$lbldistrict', sub_district_id),
                        ('ctl00$ContentPlaceHolder1$cdlDistrict_ClientState', sub_district_id+':::'+sub_district_name+':::'),
                        ('ctl00$ContentPlaceHolder1$lblDetailTH', postdata['post_description_th'].replace('\r\n', '&lt;div&gt;')),
                        ('FontName', 'arial,helvetica,sans-serif'),
                        ('FontName', 'arial,helvetica,sans-serif'),
                        ('FontSize', '1'),
                        ('FontSize', '1'),
                        ('ctl00$ContentPlaceHolder1$HtmlEditorExtender1_ClientState', ''),
                        ('ctl00$ContentPlaceHolder1$lblDetailENG', ''),
                        ('ctl00$ContentPlaceHolder1$HtmlEditorExtender2_ClientState', ''),
                        ('ctl00$ContentPlaceHolder1$BtnRegister', 'ขั้นตอนต่อไป'),
                        ('hiddenInputToUpdateATBuffer_CommonToolkitScripts', '0'),
                    ]

                    r = self.httprequestObj.http_post('https://www.thaiapartment.com/post', params={'id': post_id}, data=datapost)
                    print(r.url)
                    print(r.status_code)

                    r = self.httprequestObj.http_get('https://www.thaiapartment.com/post2', params={'id': post_id})
                    print(r.url)
                    print(r.status_code)

                    soup = BeautifulSoup(r.content, self.parser)
                    # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
                    # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
                    viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
                    viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')

                    datapost = {
                        '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$ListViewPrice$ctrl0$HyperDelete',
                        '__EVENTARGUMENT': '',
                        '__VIEWSTATE': viewstate,
                        '__VIEWSTATEGENERATOR': viewstate_gen,
                        '__VIEWSTATEENCRYPTED': '',
                        'ctl00$ContentPlaceHolder1$apRoomName': '',
                        'ctl00$ContentPlaceHolder1$apRoomType': '',
                        'ctl00$ContentPlaceHolder1$apRoomSize': '',
                        'ctl00$ContentPlaceHolder1$apDaily': '',
                        'ctl00$ContentPlaceHolder1$apMonthly': '',
                        'ctl00$ContentPlaceHolder1$lblWaterCharge': '',
                        'ctl00$ContentPlaceHolder1$lblElectricityCharge': '',
                        'ctl00$ContentPlaceHolder1$lblDeposit': '',
                        'ctl00$ContentPlaceHolder1$lblPayinadvance': '',
                        'ctl00$ContentPlaceHolder1$lblInternetCharge': '',
                        'ctl00$ContentPlaceHolder1$lblPromotionDetail': '',
                        'FontName': 'arial,helvetica,sans-serif',
                        'FontSize': '1',
                        'ctl00$ContentPlaceHolder1$HtmlEditorExtender2_ClientState': ''
                    }
                    r = self.httprequestObj.http_post('https://www.thaiapartment.com/post2', params={'id': post_id},
                                                 data=datapost)
                    print(r.url)
                    print(r.status_code)

                    r = self.httprequestObj.http_get('https://www.thaiapartment.com/post2', params={'id': post_id})
                    print(r.url)
                    print(r.status_code)

                    soup = BeautifulSoup(r.content, self.parser)
                    # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
                    # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
                    viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
                    viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')

                    datapost = {
                        '__EVENTTARGET': '',
                        '__EVENTARGUMENT': '',
                        '__VIEWSTATE': viewstate,
                        '__VIEWSTATEGENERATOR': viewstate_gen,
                        '__VIEWSTATEENCRYPTED': '',
                        'ctl00$ContentPlaceHolder1$apRoomName': '',
                        'ctl00$ContentPlaceHolder1$apRoomType': postdata['bed_room'],
                        'ctl00$ContentPlaceHolder1$apRoomSize': postdata['floorarea_sqm'],
                        'ctl00$ContentPlaceHolder1$apDaily': '',
                        'ctl00$ContentPlaceHolder1$apMonthly': postdata['price_baht'],
                        'ctl00$ContentPlaceHolder1$BtnSave': 'บันทึกราคา',
                        'ctl00$ContentPlaceHolder1$lblWaterCharge': '',
                        'ctl00$ContentPlaceHolder1$lblElectricityCharge': '',
                        'ctl00$ContentPlaceHolder1$lblDeposit': '',
                        'ctl00$ContentPlaceHolder1$lblPayinadvance': '',
                        'ctl00$ContentPlaceHolder1$lblInternetCharge': '',
                        'ctl00$ContentPlaceHolder1$lblPromotionDetail': '',
                        'FontName': 'arial,helvetica,sans-serif',
                        'FontSize': '1',
                        'ctl00$ContentPlaceHolder1$HtmlEditorExtender2_ClientState': ''
                    }

                    r = self.httprequestObj.http_post('https://www.thaiapartment.com/post2', params={'id': post_id}, data=datapost)
                    print(r.url)
                    print(r.status_code)

                    r = self.httprequestObj.http_get('https://www.thaiapartment.com/post2', params={'id': post_id})
                    print(r.url)
                    print(r.status_code)

                    soup = BeautifulSoup(r.content, self.parser)
                    # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
                    # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
                    viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
                    viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')

                    datapost = {
                        '__EVENTTARGET': '',
                        '__EVENTARGUMENT': '',
                        '__VIEWSTATE': viewstate,
                        '__VIEWSTATEGENERATOR': viewstate_gen,
                        '__VIEWSTATEENCRYPTED': '',
                        'ctl00$ContentPlaceHolder1$apRoomName': '',
                        'ctl00$ContentPlaceHolder1$apRoomType': '',
                        'ctl00$ContentPlaceHolder1$apRoomSize': '',
                        'ctl00$ContentPlaceHolder1$apDaily': '',
                        'ctl00$ContentPlaceHolder1$apMonthly': '',
                        'ctl00$ContentPlaceHolder1$lblWaterCharge': '',
                        'ctl00$ContentPlaceHolder1$lblElectricityCharge': '',
                        'ctl00$ContentPlaceHolder1$lblDeposit': '',
                        'ctl00$ContentPlaceHolder1$lblPayinadvance': '',
                        'ctl00$ContentPlaceHolder1$lblInternetCharge': '',
                        'ctl00$ContentPlaceHolder1$lblPromotionDetail': '',
                        'FontName': 'arial,helvetica,sans-serif',
                        'FontSize': '1',
                        'ctl00$ContentPlaceHolder1$HtmlEditorExtender2_ClientState': '',
                        'ctl00$ContentPlaceHolder1$BtnRegister': 'ขั้นตอนต่อไป'
                    }

                    r = self.httprequestObj.http_post('https://www.thaiapartment.com/post2', params={'id': post_id}, data=datapost)
                    print(r.url)
                    print(r.status_code)

                    # r = self.httprequestObj.http_get('https://www.thaiapartment.com/post3?id=3326', data=datapost)
                    # print(r.url)
                    # print(r.status_code)
                    #
                    # soup = BeautifulSoup(r.content, self.parser)
                    # # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
                    # # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
                    # viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
                    # viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
                    # event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')

                    r = self.httprequestObj.http_get('https://www.thaiapartment.com/post3', params={'id': post_id})
                    print(r.url)
                    print(r.status_code)

                    soup = BeautifulSoup(r.content, self.parser)
                    old_images = soup.find_all('a', {'onclick': 'return ConfRemove(this);'})

                    for img in old_images:
                        del_url = 'https://www.thaiapartment.com/' + img.get('href')
                        r = self.httprequestObj.http_get(del_url)
                        print(r.url)
                        print(r.status_code)
                    #
                    # #with open('/home/codelover/Desktop/rough.html', 'w') as f:
                    #     #f.write(r.text)

                    for i, img in enumerate(postdata['post_images']):
                        r = self.httprequestObj.http_get('https://www.thaiapartment.com/post3', params={'id': post_id})
                        print(r.url)
                        print(r.status_code)

                        # #with open('/home/codelover/Desktop/rough.html', 'w') as f:
                        #     #f.write(r.text)

                        soup = BeautifulSoup(r.content, self.parser)
                        # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
                        # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
                        viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
                        viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
                        event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')

                        filename = str(i) + '.jpeg'
                        datapost = [
                            ('__EVENTTARGET', (None, '')),
                            ('__EVENTARGUMENT', (None, '')),
                            ('__VIEWSTATE', (None, viewstate)),
                            ('__VIEWSTATEGENERATOR', (None, viewstate_gen)),
                            ('__EVENTVALIDATION', (None, event_validation)),
                            ('ctl00$ContentPlaceHolder1$UploadImages', (filename, open(img, 'rb'), 'image/jpeg')),
                            ('ctl00$ContentPlaceHolder1$uploadedFile', (None, 'Upload'))
                        ]

                        r = self.httprequestObj.http_post('https://www.thaiapartment.com/post3', params={'id': post_id}, data={}, files=datapost)
                        print(r.url)
                        print(r.status_code)

                    r = self.httprequestObj.http_get('https://www.thaiapartment.com/post3', params={'id': post_id})
                    print(r.url)
                    print(r.status_code)

                    soup = BeautifulSoup(r.content, self.parser)
                    # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
                    # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
                    viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
                    viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
                    event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')

                    datapost = [
                        ('__EVENTTARGET', (None, '')),
                        ('__EVENTARGUMENT', (None, '')),
                        ('__VIEWSTATE', (None, viewstate)),
                        ('__VIEWSTATEGENERATOR', (None, viewstate_gen)),
                        ('__EVENTVALIDATION', (None, event_validation)),
                        ('ctl00$ContentPlaceHolder1$UploadImages', (None, '')),
                        ('ctl00$ContentPlaceHolder1$uploadedFile', (None, 'โพสประกาศอพาร์ทเม้นท์'))
                    ]

                    r = self.httprequestObj.http_post('https://www.thaiapartment.com/post3', params={'id': post_id}, data={}, files=datapost)
                    print(r.url)
                    print(r.status_code)

                    # #with open('/home/codelover/Desktop/rough.html', 'w') as f:
                    #     #f.write(r.text)

                    success = True
                    detail = "Post edited successfully"

                elif postdata['property_type'] == '1':

                    r = self.httprequestObj.http_get('https://www.thaiapartment.com/condo', params={'id': post_id})
                    print(r.url)
                    print(r.status_code)

                    soup = BeautifulSoup(r.content, self.parser)
                    # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
                    # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
                    viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
                    viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
                    # event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')

                    # print(event_target)
                    # print(event_argument)
                    # print(viewstate)
                    # print(viewstate_gen)

                    project_names = soup.find('select',
                                              {'name': 'ctl00$ContentPlaceHolder1$lblProjectID'}).findChildren(
                        'option')[1:]

                    project_id = 0
                    for project in project_names:
                        name = project.string
                        if name.replace(' ', '') in postdata['web_project_name'].replace(' ', '') or postdata[
                            'web_project_name'].replace(' ', '') in name.replace(' ', ''):
                            project_id = project.get('value')
                            break

                    datapost = [
                        ('__EVENTTARGET', ''),
                        ('__EVENTARGUMENT', ''),
                        ('__VIEWSTATE', viewstate),
                        ('__VIEWSTATEGENERATOR', viewstate_gen),
                        ('ctl00$ContentPlaceHolder1$lblProjectID', project_id),
                        ('ctl00$ContentPlaceHolder1$lblProjectName', postdata['web_project_name']),
                        ('ctl00$ContentPlaceHolder1$lblPropertyTitle', postdata['post_title_th']),
                        ('ctl00$ContentPlaceHolder1$lblPropertyTitleEng', ''),
                        ('ctl00$ContentPlaceHolder1$lblDescription',
                         postdata['post_description_th'].replace('\r\n', '&lt;div&gt;')),
                        ('FontName', 'arial,helvetica,sans-serif'),
                        ('FontName', 'arial,helvetica,sans-serif'),
                        ('FontSize', '1'),
                        ('FontSize', '1'),
                        ('ctl00$ContentPlaceHolder1$HtmlEditorExtender1_ClientState', ''),
                        ('ctl00$ContentPlaceHolder1$lblDescriptionEng', ''),
                        ('ctl00$ContentPlaceHolder1$HtmlEditorExtender2_ClientState', ''),
                        ('ctl00$ContentPlaceHolder1$lblProjectHighlight', ''),
                        ('ctl00$ContentPlaceHolder1$lblProjectHighlightEng', ''),
                        ('ctl00$ContentPlaceHolder1$lblFurniture', ''),
                        ('ctl00$ContentPlaceHolder1$lblFurnitureEng', ''),
                        ('ctl00$ContentPlaceHolder1$lblPriceMonth', postdata['price_baht']),
                        ('ctl00$ContentPlaceHolder1$lblPeriod', '12'),
                        ('ctl00$ContentPlaceHolder1$lblArea', postdata['floorarea_sqm']),
                        ('ctl00$ContentPlaceHolder1$lblFloorNo', postdata['floor_level']),
                        ('ctl00$ContentPlaceHolder1$lblTower', ''),
                        ('ctl00$ContentPlaceHolder1$lblBedroom', postdata['bed_room']),
                        ('ctl00$ContentPlaceHolder1$lblBathroom', postdata['bath_room']),
                        ('ctl00$ContentPlaceHolder1$BtnRegister', 'ขั้นตอนต่อไป'),
                    ]

                    r = self.httprequestObj.http_post('https://www.thaiapartment.com/condo', params={'id': post_id}, data=datapost)
                    print(r.url)
                    print(r.status_code)

                    post_id = r.url.split('=')[-1]

                    r = self.httprequestObj.http_get('https://www.thaiapartment.com/condo2?id=' + post_id, data=datapost)
                    print(r.url)
                    print(r.status_code)

                    soup = BeautifulSoup(r.content, self.parser)
                    # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
                    # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
                    viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
                    viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
                    event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')
                    old_images = soup.find_all('a', {'onclick': 'return ConfRemove(this);'})

                    for img in old_images:
                        del_url = 'https://www.thaiapartment.com/' + img.get('href')
                        r = self.httprequestObj.http_get(del_url)
                        print(r.url)
                        print(r.status_code)

                    for i, img in enumerate(postdata['post_images']):
                        r = self.httprequestObj.http_get('https://www.thaiapartment.com/condo2?id=' + post_id)
                        print(r.url)
                        print(r.status_code)

                        # #with open('/home/codelover/Desktop/rough.html', 'w') as f:
                        #     #f.write(r.text)

                        soup = BeautifulSoup(r.content, self.parser)
                        # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
                        # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
                        viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
                        viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
                        event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')

                        index_name = 'ctl00$ContentPlaceHolder1$FileUpload' + str(i + 1)
                        filename = str(i) + '.jpeg'
                        datapost = [
                            ('__EVENTTARGET', (None, '')),
                            ('__EVENTARGUMENT', (None, '')),
                            ('__VIEWSTATE', (None, viewstate)),
                            ('__VIEWSTATEGENERATOR', (None, viewstate_gen)),
                            ('__EVENTVALIDATION', (None, event_validation)),
                            (index_name, (filename, open(img, 'rb'), 'image/jpeg')),
                            ('ctl00$ContentPlaceHolder1$lblPackage', (None, '0'))
                        ]

                        r = self.httprequestObj.http_post('https://www.thaiapartment.com/condo2?id=' + post_id, data={},
                                                     files=datapost)
                        print(r.url)
                        print(r.status_code)

                    r = self.httprequestObj.http_get('https://www.thaiapartment.com/condo2?id=' + post_id)
                    print(r.url)
                    print(r.status_code)

                    soup = BeautifulSoup(r.content, self.parser)
                    # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
                    # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
                    viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
                    viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
                    event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')

                    datapost = [
                        ('__EVENTTARGET', (None, '')),
                        ('__EVENTARGUMENT', (None, '')),
                        ('__VIEWSTATE', (None, viewstate)),
                        ('__VIEWSTATEGENERATOR', (None, viewstate_gen)),
                        ('__EVENTVALIDATION', (None, event_validation)),
                        ('ctl00$ContentPlaceHolder1$FileUpload1', (None, '')),
                        ('ctl00$ContentPlaceHolder1$FileUpload2', (None, '')),
                        ('ctl00$ContentPlaceHolder1$FileUpload3', (None, '')),
                        ('ctl00$ContentPlaceHolder1$FileUpload4', (None, '')),
                        ('ctl00$ContentPlaceHolder1$FileUpload5', (None, '')),
                        ('ctl00$ContentPlaceHolder1$FileUpload6', (None, '')),
                        ('ctl00$ContentPlaceHolder1$lblPackage', (None, '0')),
                        ('ctl00$ContentPlaceHolder1$BtnRegister', (None, 'โพสต์ประกาศคอนโด'))
                    ]

                    r = self.httprequestObj.http_post('https://www.thaiapartment.com/condo2?id=' + post_id, data={},
                                                 files=datapost)
                    print(r.url)
                    print(r.status_code)

                    # #with open('/home/codelover/Desktop/rough.html', 'w') as f:
                    #     #f.write(r.text)

                    success = True
                    detail = 'Post edited successfully'

                else:
                    success = False
                    detail = "Only condo/apartment posts allowed"
            else:
                success = False
                detail = "No post with given post_id"

        else:
            success = False
            detail = "Couldnot login"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": post_url,
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
            "websitename": self.webname,
        }

    def boost_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""

        if success:

            post_found = False

            r = self.httprequestObj.http_get('https://www.thaiapartment.com/allpost')
            print(r.url)
            print(r.status_code)

            soup = BeautifulSoup(r.content, self.parser)
            all_posts = soup.find_all('a', 'img-responsive img-thumbnail')

            for post in all_posts:
                post_id = post.get('href').split('=')[-1]
                print(post_id)
                if post_id == postdata['post_id']:
                    post_found = True
                    break

            if post_found:
                # if 'web_project_name' not in postdata or postdata['web_project_name'] is None:
                #     if 'project_name' in postdata and postdata['project_name'] is not None:
                #         postdata['web_project_name'] = postdata['project_name']
                #     else:
                #         postdata['web_project_name'] = postdata['post_title_th']
                #
                # proid = {
                #     'คอนโด': '1',
                #     'บ้านเดี่ยว': '2',
                #     'บ้านแฝด': '3',
                #     'ทาวน์เฮ้าส์': '4',
                #     'ตึกแถว-อาคารพาณิชย์': '5',
                #     'ที่ดิน': '6',
                #     'อพาร์ทเมนท์': '7',
                #     'โรงแรม': '8',
                #     'ออฟฟิศสำนักงาน': '9',
                #     'โกดัง-โรงงาน': '10',
                #     'โรงงาน': '25'
                # }
                # getProdId = {'1': 159, '2': 156, '3': 156, '4': 157,
                #              '5': 158, '6': 161, '7': 162, '8': 162, '9': 162, '10': 162, '25': 162}
                #
                # try:
                #     theprodid = getProdId[proid[str(postdata['property_type'])]]
                #     postdata['property_type'] = proid[str(postdata['property_type'])]
                # except:
                #     theprodid = getProdId[str(postdata['property_type'])]
                #
                # prod_address = ""
                # for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'],
                #             postdata['addr_district'], postdata['addr_province']]:
                #     if add is not None:
                #         prod_address += add + " "
                # prod_address = prod_address[:-1]

                r = self.httprequestObj.http_get('https://www.thaiapartment.com/post', params={'id': post_id})
                print(r.url)
                print(r.status_code)

                soup = BeautifulSoup(r.content, self.parser)
                # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
                # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
                viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
                viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
                # event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')

                # print(event_target)
                # print(event_argument)
                print(viewstate)
                print(viewstate_gen)

                # captcha = soup.find('span', {'id': 'ContentPlaceHolder1_lblCaptcha'}).string
                # print(captcha)
                # print(event_target)
                # print(event_argument)
                print(viewstate)
                print(viewstate_gen)

                datapost = [
                    ('__EVENTTARGET', ''),
                    ('__EVENTARGUMENT', ''),
                    ('__VIEWSTATE', viewstate),
                    ('__VIEWSTATEGENERATOR', viewstate_gen),
                    ('FontName', 'arial,helvetica,sans-serif'),
                    ('FontName', 'arial,helvetica,sans-serif'),
                    ('FontSize', '1'),
                    ('FontSize', '1'),
                    ('ctl00$ContentPlaceHolder1$HtmlEditorExtender1_ClientState', ''),
                    ('ctl00$ContentPlaceHolder1$lblDetailENG', ''),
                    ('ctl00$ContentPlaceHolder1$HtmlEditorExtender2_ClientState', ''),
                    ('ctl00$ContentPlaceHolder1$BtnRegister', 'ขั้นตอนต่อไป'),
                    ('hiddenInputToUpdateATBuffer_CommonToolkitScripts', '0'),
                ]

                r = self.httprequestObj.http_post('https://www.thaiapartment.com/post', params={'id': post_id}, data=datapost)
                print(r.url)
                print(r.status_code)

                #with open('/home/codelover/Desktop/rough.html', 'w') as f:
                    #f.write(r.text)

                # r = self.httprequestObj.http_get('https://www.thaiapartment.com/post2', params={'id': post_id})
                # print(r.url)
                # print(r.status_code)
                #
                # soup = BeautifulSoup(r.content, self.parser)
                # # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
                # # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
                # viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
                # viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
                #
                # datapost = {
                #     '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$ListViewPrice$ctrl0$HyperDelete',
                #     '__EVENTARGUMENT': '',
                #     '__VIEWSTATE': viewstate,
                #     '__VIEWSTATEGENERATOR': viewstate_gen,
                #     '__VIEWSTATEENCRYPTED': '',
                #     'ctl00$ContentPlaceHolder1$apRoomName': '',
                #     'ctl00$ContentPlaceHolder1$apRoomType': '',
                #     'ctl00$ContentPlaceHolder1$apRoomSize': '',
                #     'ctl00$ContentPlaceHolder1$apDaily': '',
                #     'ctl00$ContentPlaceHolder1$apMonthly': '',
                #     'ctl00$ContentPlaceHolder1$lblWaterCharge': '',
                #     'ctl00$ContentPlaceHolder1$lblElectricityCharge': '',
                #     'ctl00$ContentPlaceHolder1$lblDeposit': '',
                #     'ctl00$ContentPlaceHolder1$lblPayinadvance': '',
                #     'ctl00$ContentPlaceHolder1$lblInternetCharge': '',
                #     'ctl00$ContentPlaceHolder1$lblPromotionDetail': '',
                #     'FontName': 'arial,helvetica,sans-serif',
                #     'FontSize': '1',
                #     'ctl00$ContentPlaceHolder1$HtmlEditorExtender2_ClientState': ''
                # }
                # r = self.httprequestObj.http_post('https://www.thaiapartment.com/post2', params={'id': post_id},
                #                              data=datapost)
                # print(r.url)
                # print(r.status_code)
                #
                # r = self.httprequestObj.http_get('https://www.thaiapartment.com/post2', params={'id': post_id})
                # print(r.url)
                # print(r.status_code)
                #
                # soup = BeautifulSoup(r.content, self.parser)
                # # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
                # # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
                # viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
                # viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
                #
                # datapost = {
                #     '__EVENTTARGET': '',
                #     '__EVENTARGUMENT': '',
                #     '__VIEWSTATE': viewstate,
                #     '__VIEWSTATEGENERATOR': viewstate_gen,
                #     '__VIEWSTATEENCRYPTED': '',
                #     'ctl00$ContentPlaceHolder1$apRoomName': '',
                #     'ctl00$ContentPlaceHolder1$apRoomType': postdata['bed_room'],
                #     'ctl00$ContentPlaceHolder1$apRoomSize': postdata['floorarea_sqm'],
                #     'ctl00$ContentPlaceHolder1$apDaily': '',
                #     'ctl00$ContentPlaceHolder1$apMonthly': postdata['price_baht'],
                #     'ctl00$ContentPlaceHolder1$BtnSave': 'บันทึกราคา',
                #     'ctl00$ContentPlaceHolder1$lblWaterCharge': '',
                #     'ctl00$ContentPlaceHolder1$lblElectricityCharge': '',
                #     'ctl00$ContentPlaceHolder1$lblDeposit': '',
                #     'ctl00$ContentPlaceHolder1$lblPayinadvance': '',
                #     'ctl00$ContentPlaceHolder1$lblInternetCharge': '',
                #     'ctl00$ContentPlaceHolder1$lblPromotionDetail': '',
                #     'FontName': 'arial,helvetica,sans-serif',
                #     'FontSize': '1',
                #     'ctl00$ContentPlaceHolder1$HtmlEditorExtender2_ClientState': ''
                # }
                #
                # r = self.httprequestObj.http_post('https://www.thaiapartment.com/post2', params={'id': post_id}, data=datapost)
                # print(r.url)
                # print(r.status_code)
                #
                # r = self.httprequestObj.http_get('https://www.thaiapartment.com/post2', params={'id': post_id})
                # print(r.url)
                # print(r.status_code)
                #
                # soup = BeautifulSoup(r.content, self.parser)
                # # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
                # # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
                # viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
                # viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
                #
                # datapost = {
                #     '__EVENTTARGET': '',
                #     '__EVENTARGUMENT': '',
                #     '__VIEWSTATE': viewstate,
                #     '__VIEWSTATEGENERATOR': viewstate_gen,
                #     '__VIEWSTATEENCRYPTED': '',
                #     'ctl00$ContentPlaceHolder1$apRoomName': '',
                #     'ctl00$ContentPlaceHolder1$apRoomType': '',
                #     'ctl00$ContentPlaceHolder1$apRoomSize': '',
                #     'ctl00$ContentPlaceHolder1$apDaily': '',
                #     'ctl00$ContentPlaceHolder1$apMonthly': '',
                #     'ctl00$ContentPlaceHolder1$lblWaterCharge': '',
                #     'ctl00$ContentPlaceHolder1$lblElectricityCharge': '',
                #     'ctl00$ContentPlaceHolder1$lblDeposit': '',
                #     'ctl00$ContentPlaceHolder1$lblPayinadvance': '',
                #     'ctl00$ContentPlaceHolder1$lblInternetCharge': '',
                #     'ctl00$ContentPlaceHolder1$lblPromotionDetail': '',
                #     'FontName': 'arial,helvetica,sans-serif',
                #     'FontSize': '1',
                #     'ctl00$ContentPlaceHolder1$HtmlEditorExtender2_ClientState': '',
                #     'ctl00$ContentPlaceHolder1$BtnRegister': 'ขั้นตอนต่อไป'
                # }
                #
                # r = self.httprequestObj.http_post('https://www.thaiapartment.com/post2', params={'id': post_id}, data=datapost)
                # print(r.url)
                # print(r.status_code)
                #
                # # r = self.httprequestObj.http_get('https://www.thaiapartment.com/post3?id=3326', data=datapost)
                # # print(r.url)
                # # print(r.status_code)
                # #
                # # soup = BeautifulSoup(r.content, self.parser)
                # # # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
                # # # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
                # # viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
                # # viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
                # # event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')
                #
                # r = self.httprequestObj.http_get('https://www.thaiapartment.com/post3', params={'id': post_id})
                # print(r.url)
                # print(r.status_code)
                #
                # soup = BeautifulSoup(r.content, self.parser)
                # old_images = soup.find_all('a', {'onclick': 'return ConfRemove(this);'})
                #
                # for img in old_images:
                #     del_url = 'https://www.thaiapartment.com/' + img.get('href')
                #     r = self.httprequestObj.http_get(del_url)
                #     print(r.url)
                #     print(r.status_code)
                # #
                # # #with open('/home/codelover/Desktop/rough.html', 'w') as f:
                # #     #f.write(r.text)
                #
                # for i, img in enumerate(postdata['post_images']):
                #     r = self.httprequestObj.http_get('https://www.thaiapartment.com/post3', params={'id': post_id})
                #     print(r.url)
                #     print(r.status_code)
                #
                #     # #with open('/home/codelover/Desktop/rough.html', 'w') as f:
                #     #     #f.write(r.text)
                #
                #     soup = BeautifulSoup(r.content, self.parser)
                #     # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
                #     # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
                #     viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
                #     viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
                #     event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')
                #
                #     filename = str(i) + '.jpeg'
                #     datapost = [
                #         ('__EVENTTARGET', (None, '')),
                #         ('__EVENTARGUMENT', (None, '')),
                #         ('__VIEWSTATE', (None, viewstate)),
                #         ('__VIEWSTATEGENERATOR', (None, viewstate_gen)),
                #         ('__EVENTVALIDATION', (None, event_validation)),
                #         ('ctl00$ContentPlaceHolder1$UploadImages', (filename, open(img, 'rb'), 'image/jpeg')),
                #         ('ctl00$ContentPlaceHolder1$uploadedFile', (None, 'Upload'))
                #     ]
                #
                #     r = self.httprequestObj.http_post('https://www.thaiapartment.com/post3', params={'id': post_id}, data={}, files=datapost)
                #     print(r.url)
                #     print(r.status_code)
                #
                # r = self.httprequestObj.http_get('https://www.thaiapartment.com/post3', params={'id': post_id})
                # print(r.url)
                # print(r.status_code)
                #
                # soup = BeautifulSoup(r.content, self.parser)
                # # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
                # # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
                # viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
                # viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
                # event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')
                #
                # datapost = [
                #     ('__EVENTTARGET', (None, '')),
                #     ('__EVENTARGUMENT', (None, '')),
                #     ('__VIEWSTATE', (None, viewstate)),
                #     ('__VIEWSTATEGENERATOR', (None, viewstate_gen)),
                #     ('__EVENTVALIDATION', (None, event_validation)),
                #     ('ctl00$ContentPlaceHolder1$UploadImages', (None, '')),
                #     ('ctl00$ContentPlaceHolder1$uploadedFile', (None, 'โพสประกาศอพาร์ทเม้นท์'))
                # ]
                #
                # r = self.httprequestObj.http_post('https://www.thaiapartment.com/post3', params={'id': post_id}, data={}, files=datapost)
                # print(r.url)
                # print(r.status_code)
                #
                # # #with open('/home/codelover/Desktop/rough.html', 'w') as f:
                # #     #f.write(r.text)

                success = True
                detail = "Post boosted successfully"
            else:
                success = False
                detail = "No post with given post_id"

        else:
            success = False
            detail = "Couldnot login"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": post_url,
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
            "websitename": self.webname,
        }

    def delete_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""

        if success:

            post_found = False

            r = self.httprequestObj.http_get('https://www.thaiapartment.com/allpost')
            print(r.url)
            print(r.status_code)

            soup = BeautifulSoup(r.content, self.parser)
            all_posts = soup.find_all('div', 'boxes agencies_widget')
            soup = BeautifulSoup(r.content, self.parser)
            event_target = ''
            # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
            # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
            viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
            viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
            event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')
            previous_page = soup.find('input', {'name': '__PREVIOUSPAGE'}).get('value')

            #with open('/home/codelover/Desktop/rough.html', 'w') as f:
                #f.write(r.text)

            print(all_posts)

            for post in all_posts:
                print(post.find_all('div')[2])
                post_id = post.find_all('div', recursive=False)[1].find('div', recursive=False).find('h3').find('a').get('href').split(
                    '=')[-1]
                print(post_id)
                if post_id == postdata['post_id']:
                    event_target = post.find_all('div', recursive=False)[1].find('div').find('a', {
                        'onclick': "javascript:return confirm('คุณต้องการลบข้อมูลนี้ใช่หรือไม่?');"}).get('href').split(
                        '\'')[1]
                    # print(event_target)
                    post_found = True
                    break

            if post_found:

                datapost = [
                    ('__EVENTTARGET', event_target),
                    ('__EVENTARGUMENT', ''),
                    ('__VIEWSTATE', viewstate),
                    ('__VIEWSTATEGENERATOR', viewstate_gen),
                    ('__VIEWSTATEENCRYPTED', ''),
                    ('__PREVIOUSPAGE', previous_page),
                    ('__EVENTVALIDATION', event_validation),
                ]

                r = self.httprequestObj.http_post('https://www.thaiapartment.com/allpost', data=datapost)
                print(r.url)
                print(r.status_code)

                success = True
                detail = "Post deleted successfully"
            else:
                success = False
                detail = "No post with given post_id"

        else:
            success = False
            detail = "Couldnot login"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": post_url,
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
            "websitename": self.webname,
        }

    def search_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""
        post_modified = ""
        post_view = ""

        if success:

            post_found = False

            r = self.httprequestObj.http_get('https://www.thaiapartment.com/allpost')
            print(r.url)
            print(r.status_code)

            soup = BeautifulSoup(r.content, self.parser)
            all_posts = soup.find_all('div', 'boxes agencies_widget')
            soup = BeautifulSoup(r.content, self.parser)
            event_target = ''
            # event_target = soup.find('input', {'name': '__EVENTTARGET'}).get('value')
            # event_argument = soup.find('input', {'name': '__EVENTARGUMENT'}).get('value')
            viewstate = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
            viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
            event_validation = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')
            previous_page = soup.find('input', {'name': '__PREVIOUSPAGE'}).get('value')

            #with open('/home/codelover/Desktop/rough.html', 'w') as f:
                #f.write(r.text)

            print(all_posts)

            for post in all_posts:
                # print(post.find_all('div')[2])
                # post_title = post.find_all('div', recursive=False)[1].find('div', recursive=False).find('h3').find('a').string
                purl=post.find_all('div', recursive=False)[1].find('div', recursive=False).find('h3').find('a')["href"]
                purl="https://www.thaiapartment.com/"+purl
                r=self.httprequestObj.http_get(purl)
                soup1=BeautifulSoup(r.text,"html5lib")
                try:
                    post_title=soup1.find("input",attrs={"name":"ctl00$ContentPlaceHolder1$lblPropertyTitle"})["value"]
                except:
                    continue

                print(post_id)
                if post_title in postdata['post_title_th'] or postdata['post_title_th'] in post_title:
                    post_id = post.find_all('div', recursive=False)[1].find('div', recursive=False).find('h3').find('a').get(
                        'href').split(
                        '=')[-1]
                    try:
                        post_modified = post.find_all('div', recursive=False)[1].find('div', recursive=False).find_all('p')[1].find('span').string[21:]
                    except:
                        pass
                    post_url=purl
                    post_found = True
                    success = True
                    detail = "Post Found"
                    break

            if not post_found:
                success = False
                detail = "No post with given title"

        else:
            success = False
            detail = "Couldnot login"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": post_url,
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
            "post_created": "",
            "post_modified": post_modified,
            "post_view": post_view,
            "account_type": "null",
            "detail": detail,
            "websitename": self.webname,
        }









