# -*- coding: utf-8 -*-
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
import os
from .lib_httprequest import *
import string
from bs4 import BeautifulSoup
import os.path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.common.by import By
# from urlparse import urlparse
import re
import json
import datetime
import time
import sys
import shutil
from urllib.parse import unquote

# options = Options()
# options.headless = True

options = Options()
options.set_headless(True)
browser = webdriver.Firefox(options=options)
# browser = webdriver.Chrome(
    # executable_path='/usr/bin/chromedriver',options=options)
wait = WebDriverWait(browser,10)
browser.implicitly_wait(100)
httprequestObj = lib_httprequest()


with open("./static/ddteedin_province.json") as f:
    provincedata = json.load(f)


class ddteedin():

    name = 'ddteedin'

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

        datapost = dict(
            email=user,
            password=passwd,
            password2=passwd,
            cname=name_th + " " + surname_th,
            mobile=mobile_no,
            action='save_register',
        )
        data1 = {
            'act':'check',
            'email':user
        }
        r = httprequestObj.http_post('https://www.ddteedin.com/apis/profile', data = data1)
        print(r.text)
        if r.text != 'Yes':
            success = "false"
            detail = "Can't register"
        data1 = {
            "mobile":mobile_no
        }
        r = httprequestObj.http_post('https://www.ddteedin.com/apis/user_check', data = data1)
        data = json.loads(r.text)
        print(data)
        if(data['result'] != 'yes'):
            success = "false",
            detail = 'Incorrect mobile number'
        r = httprequestObj.http_post(
            'https://www.ddteedin.com/register/', data=datapost)
        # print("yes")
        data = r.text
        if r.status_code == 404:
            detail = "Can't register"
            success = "false"
        else:
            detail = "Registered"
        # # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "ddteedin",
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
            'action': 'login',
            'log_u': user,
            'log_p': passwd,
            'login': 'Login'
        }

        r = httprequestObj.http_post(
            'https://www.ddteedin.com/login/', data=datapost)
        data = r.text
        # print(r.text)
        if data.find("ไม่ถูกต้องกรุณาตรวจสอบ") != -1:
            detail = "cannot login"
            success = "false"
        else:
            detail = "login successfull"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "ddteedin",
            "success": success,
            "ds_id": postdata['ds_id'],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail
        }

    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        theurl = ""
        post_id = ""
        detail = ""
        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        ashopname = test_login["detail"]
        print(test_login)
        getProdId = {'1': 2, '2': 4, '3': 4, '4': 12, '5': 11,
                     '6': 3, '7': 1, '8': 1, '9': 11, '10': 13, '25': 13}
        theprodid = getProdId[str(postdata['property_type'])]
        # theprodid = post
        province_id = '0'
        amphur_id = '26'
        tumbon_id = '01'
        for (key, value) in provincedata.items():
            if type(value) is str and postdata['addr_province'].strip().find(value.strip()) != -1:
                province_id = key
                break
        if province_id != '0':
            for (key, value) in provincedata[province_id+"_province"].items():
                if postdata['addr_district'].strip().find(value.strip()) != -1:
                    amphur_id = key
                    break
        if amphur_id != '26':
            for (key, value) in provincedata[amphur_id+"_amphur"].items():
                if postdata['addr_sub_district'].strip().find(value.strip()) != -1:
                    tumbon_id = key
                    break
        prod_address = ""
        for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
            if add is not None:
                prod_address += add
        prod_address = prod_address[:-1]
        print(province_id)
        print(amphur_id)
        print(tumbon_id)
        if province_id == '0' or amphur_id == '26' or tumbon_id == '01':
            # success = "false"
            # detail = "wrong Province or amphur or tumbon"
            province_id = '81'
            amphur_id = '03'
            tumbon_id = '03'
        if success == "true":
            try:
                r = httprequestObj.http_get(
                    'http://www.ddteedin.com/post-land-for-sale', verify=False)
                data = r.text
                soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
                try:
                    cverify = soup.find("input", {"name": "cverify"})['value']
                except:
                    cverify = ""    
                    success = "false"
                    detail = "wrong cverify"
                
            except:
                success = "false"
                detail = "request error"
            else:
                datapost = {
                    'action': 'create_post',
                    'timeout':'5',
                    'name':postdata['post_title_th'],
                    'code':'',
                    'typeid':theprodid,
                    'price':postdata['price_baht'],
                    'province':province_id,
                    'amphur':amphur_id,
                    'tumbon':tumbon_id,
                    'detail':postdata['post_description_th'],
                    'warning':'',
                    'lat':postdata['geo_latitude'],
                    'lng':postdata['geo_longitude'],
                    'opts[]':62,
                    'cverify':cverify
                }

                if postdata['listing_type'] == 'เช่า':
                    # datapost.append(('forid','3'))
                    datapost['forid'] = '3'
                else:
                    datapost['forid'] = '1'
                    # datapost.append(('forid','1'))
                for mykey in ['land_size_ngan','land_size_rai','land_size_wa']:
                    if postdata[mykey] is None or postdata[mykey] == '':
                        postdata[mykey] = 0

                if theprodid != 2:
                    datapost['sizerai']=postdata['land_size_rai']
                    datapost['sizewa2']=100*int(postdata['land_size_ngan'])+int(postdata['land_size_wa'])
                if theprodid != 3:
                    datapost['isnew'] ='2'
                    key = 'web_project_name'
                    if key in postdata.keys() and postdata['web_project_name'] is not None:
                        # datapost.append(('project',postdata['web_project_name']))
                        if postdata['web_project_name'].find('watermark') != -1:
                            postdata['web_project_name'] = 'Watermark Chaophraya River'
                        # print(postdata['web_project_name'])
                    elif 'project_name' in postdata.keys() and postdata['project_name'] is not None:
                        # datapost.append(('project',postdata['project_name']))
                        if postdata['project_name'].find('watermark') != -1:
                            postdata['web_project_name'] = 'Watermark Chaophraya River'
                        # print(postdata['project_name'])
                        else:
                            postdata['web_project_name'] = postdata['project_name']
                    else:
                        if postdata['post_title_th'].find('watermark') != -1:
                            print("yes")
                            postdata['web_project_name'] = 'Watermark Chaophraya River'
                        else:
                            postdata['web_project_name'] = postdata['post_title_th']
                        # datapost.append(('project',postdata['post_title_th']))
                    # datapost.append(('project', postdata['project_name']))
                    dataquery = {
                        "q":postdata['web_project_name']
                    }
                    r = httprequestObj.http_get('https://www.ddteedin.com/apis/project/?q='+dataquery["q"],verify = False)
                    # data = json.loads(r.text)
                    data = r.text
                    lis = data.split("],[")
                    j = []
                    for i in lis:
                        j = i.split(",")
                        for k in range(len(j)):
                            j[k] = j[k].replace("[","")
                            j[k] = j[k].replace("]","")
                            j[k] = j[k].replace('"',"")
                    print(j)
                    if len(j) > 1:
                        postdata['web_project_name'] = j[0]
                        postdata['project_id'] = j[1]
                    else:
                        postdata['project_id'] = '0'
                            # print(k)
                    # postdata['web_project_name'] = j[0]
                    datapost['project'] = postdata['web_project_name']
                    datapost['project_id'] = postdata['project_id']
                    # datapost.append(('project',postdata['web_project_name']))
                    # datapost.append(('project_id',postdata['project_id']))
                    # datapost.append(('project', postdata['project_name']))
                    datapost['rooms']=postdata['bed_room']
                    datapost['bathroom']=postdata['bath_room']
                    if theprodid != 2:
                        datapost['floor']= postdata['floor_total']
                    else:
                        datapost['floor'] = postdata['floor_level']
                    datapost['usagesize']= postdata['floor_area']

                datapost['files']= ''
                print(datapost)
                r = httprequestObj.http_post(
                    'https://www.ddteedin.com/post-land-for-sale/?rf=mypost', data=datapost)
                # print(r.text,r.status_code)
                data = r.text
                print(data,"ji")
                soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
                try:
                    a = soup.find("a", {"class": "green"})['href']
                    print(a)
                    post_id = a.replace('/', '')
                    theurl = 'https://www.ddteedin.com'+a
                    
                except:
                    post_id = ''
                    theurl = ''
                if data.find('ชื่อประกาศซ้ำ หากมั่นใจว่าไม่ได้ลงซ้ำ ลองใส่รายละเอียดเพิ่มในชื่อประกาศ') != -1:
                    success = "false"
                    print("sed")
                    detail = "duplicate title"
                if post_id != '' and theurl != '':
                    browser.get('https://www.ddteedin.com/login/')
                    time.sleep(2)
                    # global wait
                    # email = wait.until(presence_of_element_located(By.NAME,'log_u'))

                    email = browser.find_element_by_name('log_u')
                    # email.clear()
                    email.send_keys(postdata['user'])
                    password = browser.find_element_by_name('log_p')
                    # password.clear()
                    password.send_keys(postdata['pass'])
                    browser.find_element_by_name('login').click()
                    browser.get('https://www.ddteedin.com/post/edit/'+post_id+'/')
                    time.sleep(2)
                    j = 0
                    for i in postdata['post_images']:
                        print(i)
                        j += 1
                        if j > 10:
                            break
                        # browser.set_window_size(1200, 900)
                        # for p in range(10):
                        #     browser.set_window_size(1200-p, 900)
                        time.sleep(1)
                        # wait = WebDriverWait(browser,10)
                        # image = wait.until(presence_of_element_located(By.ID,'fileupload'))
                        image = browser.find_element_by_id('fileupload')
                        print(image.get_attribute('type'))
                        print(str(os.getcwd())+"/"+str(i))
                        image.send_keys(str(os.getcwd())+"/"+str(i))
                    time.sleep(2)
                    browser.find_element_by_name('btn_submit').click()
    
                    time.sleep(2)
                    browser.get('https://www.ddteedin.com/logout/')

                    # browser.close()
                # query_element = {
                #     'q': postdata['post_title_th'],
                #     'pv': '',
                #     'order': 'createdate',
                #     'btn_srch': 'search'
                # }
                # query_string = 'https://www.ddteedin.com/myposts/?q='+query_element['q'].replace(' ', '+')+'&pv='+query_element['pv'].replace(
                #     ' ', '+')+'&order='+query_element['order'].replace(' ', '+')+"&btn_srch="+query_element['btn_srch'].replace(' ', '+')
                # try:
                #     r = httprequestObj.http_get(query_string, verify=False)
                #     data = r.text
                #     # print(data)
                #     soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
                #     id = soup.find("div",{"class":"it st1"})['id']
                #     # theurl = div.find("a",{"class":"title"})['href']
                #     id = id.replace('r', '')
                # except:
                #     success = False
                #     id = ''
                # post_id += id
                # if(post_id != ''):
                #     theurl = 'https://www.ddteedin.com/'+post_id
            # print(r.text)
            # print(r.status_code)
        else:
            success = "false"

        try:
            browser.close()
            browser.quit()
            try:
                alert = browser.switch_to.alert
                alert.accept()
                browser.close()
                browser.quit()
            except:
                pass
        except:
            pass

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "websitename": "ddteedin",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": theurl,
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
            "account_type": "null",
        }

    def edit_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        theurl = ""
        post_id = ""

        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        ashopname = test_login["detail"]
        getProdId = {'1': 2, '2': 4, '3': 4, '4': 12, '5': 11,
                     '6': 3, '7': 1, '8': 1, '9': 11, '10': 13, '25': 13}
        theprodid = getProdId[str(postdata['property_type'])]

        print(theprodid)
        province_id = '0'
        amphur_id = '26'
        tumbon_id = '01'
        for (key, value) in provincedata.items():
            if type(value) is str and postdata['addr_province'].strip().find(value.strip()) != -1:
                province_id = key
                break
        if province_id != '0':
            for (key, value) in provincedata[province_id+"_province"].items():
                if postdata['addr_district'].strip().find(value.strip()) != -1:
                    amphur_id = key
                    break
        if amphur_id != '26':
            for (key, value) in provincedata[amphur_id+"_amphur"].items():
                if postdata['addr_sub_district'].strip().find(value.strip()) != -1:
                    tumbon_id = key
                    break
        prod_address = ""
        for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
            if add is not None:
                prod_address += add
        prod_address = prod_address[:-1]
        if success == "true":
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
            # # print(id)
            id = postdata['post_id']
            post_id += id
            query_element = {
                'q': postdata['post_id'],
                'pv': '',
                'order': 'createdate',
                'btn_srch': 'search'
            }
            query_string = 'https://www.ddteedin.com/myposts/?q='+query_element['q'].replace(' ', '+')+'&pv='+query_element['pv'].replace(
                ' ', '+')+'&order='+query_element['order'].replace(' ', '+')+"&btn_srch="+query_element['btn_srch'].replace(' ', '+')
            r = httprequestObj.http_get(
                query_string, verify=False)
            data = r.text
            query_string = 'https://www.ddteedin.com/post-land-for-sale/edit/'+id
            if data.find(" ไม่พบประกาศ") != -1:
                success = "false"
            else:
                r = httprequestObj.http_get(query_string, verify=False)
                data = r.text
                # print(data)
                soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
                try:
                    cverify = soup.find("input", {"name": "cverify"})['value']
                except:
                    success = "false"

                if tumbon_id == "01" or amphur_id == "26":
                    # success = "false"
                    province_id = '81'
                    amphur_id = '03'
                    tumbon_id = '03'
                datapost = [
                    ('action', 'edit_post'),
                    ('timeout', '5'),
                    ('name', postdata['post_title_th']),
                    ('code', ''),
                    ('typeid', theprodid),
                    ('price', postdata['price_baht']),
                    ('province', province_id),
                    ('amphur', amphur_id),
                    ('tumbon', tumbon_id),
                    ('detail', postdata['post_description_th']),
                    ('warning', ""),
                    ('lat', postdata['geo_latitude']),
                    ('lng', postdata['geo_longitude']),
                    ('opts[]', 62),
                    ('cverify', cverify)
                ]
                if postdata['listing_type'] == 'เช่า':
                    datapost.append(('forid','3'))
                else:
                    datapost.append(('forid','1'))

                for mykey in ['land_size_ngan','land_size_rai','land_size_wa']:
                    if postdata[mykey] is None or postdata[mykey] == '':
                        postdata[mykey] = 0

                if theprodid != 2:
                    datapost.append(('sizerai',postdata['land_size_rai']))
                    datapost.append(('sizewa2',100*int(postdata['land_size_ngan'])+int(postdata['land_size_wa'])))
                if theprodid != 3:
                    datapost.append(('isnew', '2'))
                    key = 'web_project_name'
                    if key in postdata.keys() and postdata['web_project_name'] is not None:
                        # datapost.append(('project',postdata['web_project_name']))
                        if postdata['web_project_name'].find('watermark') != -1:
                            postdata['web_project_name'] = 'Watermark Chaophraya River'
                        # print(postdata['web_project_name'])
                    elif 'project_name' in postdata.keys() and postdata['project_name'] is not None:
                        # datapost.append(('project',postdata['project_name']))
                        if postdata['project_name'].find('watermark') != -1:
                            postdata['web_project_name'] = 'Watermark Chaophraya River'
                        # print(postdata['project_name'])
                        else:
                            postdata['web_project_name'] = postdata['project_name']
                    else:
                        if postdata['post_title_th'].find('watermark') != -1:
                            postdata['web_project_name']  = 'Watermark Chaophraya River'
                        else:
                            postdata['web_project_name'] = postdata['post_title_th']
                        # datapost.append(('project',postdata['post_title_th']))
                    # datapost.append(('project', postdata['project_name']))
                    dataquery = {
                        "q":postdata['web_project_name']
                    }
                    r = httprequestObj.http_get('https://www.ddteedin.com/apis/project/?q='+dataquery["q"],verify = False)
                    # data = json.loads(r.text)
                    data = r.text
                    lis = data.split("],[")
                    j = []
                    for i in lis:
                        j = i.split(",")
                        for k in range(len(j)):
                            j[k] = j[k].replace("[","")
                            j[k] = j[k].replace("]","")
                            j[k] = j[k].replace('"',"")
                    print(j)
                    if len(j) > 1:
                        postdata['web_project_name'] = j[0]
                        postdata['project_id'] = j[1]
                    else:
                        postdata['project_id'] = '0'
                            # print(k)
                    # postdata['web_project_name'] = j[0]
                    datapost.append(('project',postdata['web_project_name']))
                    datapost.append(('project_id',postdata['project_id']))
                    datapost.append(('rooms', postdata['bed_room']))
                    datapost.append(('bathroom', postdata['bath_room']))
                    datapost.append(('floor', postdata['floor_total']))
                    datapost.append(('usagesize', postdata['floor_area']))
                query_string = 'https://www.ddteedin.com/post-land-for-sale/edit/'+id
                
                r = httprequestObj.http_post(
                    query_string, data=datapost)
                browser.get('https://www.ddteedin.com/login')
                time.sleep(2)
                email = browser.find_element_by_name('log_u')
                # email.clear()
                email.send_keys(postdata['user'])
                password = browser.find_element_by_name('log_p')
                password.clear()
                password.send_keys(postdata['pass'])
                browser.find_element_by_name('login').click()
                browser.get('https://www.ddteedin.com/post/edit/'+postdata['post_id']+'/')
                j = 0
                for i in postdata['post_images']:
                    print(i)
                    j += 1
                    if j > 10:
                        break
                    # browser.set_window_size(1200, 900)
                    # for p in range(10):
                    #     browser.set_window_size(1200-p, 900)
                    time.sleep(1)
                    image = browser.find_element_by_id('fileupload')
                    print(image.get_attribute('type'))
                    print(str(os.getcwd())+"/"+str(i))
                    image.send_keys(str(os.getcwd())+"/"+str(i))
                time.sleep(2)
                browser.find_element_by_name('btn_submit').click()
                browser.get('https://www.ddteedin.com/logout/')
                query_string = 'https://www.ddteedin.com/'+postdata['post_id']
            # print(r.text)
        else:
            success = "false"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        try:
            browser.close()
            browser.quit()
            try:
                alert = browser.switch_to.alert
                alert.accept()
                browser.close()
                browser.quit()
            except:
                pass

        except:
            pass
        return {
            "websitename": "ddteedin",
            "success": success,
            "log_id": postdata['log_id'],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": query_string,
            'ds_id': postdata['ds_id'],
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
        # print(ashopname)
        # for (key, value) in provincedata.items():
        #     if type(value) is str and postdata['addr_province'].strip() in value.strip():
        #         province_id = key
        #         break

        # for (key, value) in provincedata[province_id+"_province"].items():
        #     if postdata['addr_district'].strip() in value.strip():
        #         amphur_id = key
        #         break
        if success == "true":
            tumbon_id = '01'
            r = httprequestObj.http_get(
                'https://www.ddteedin.com/myposts/?rf=login', verify=False)
            data = r.text
            soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
            alls = soup.findAll('script')
            id1 = ""
            i = 0
            for x in alls:
                if i == 3:
                    id1 = id1 + (str(x))
                i += 1
            id1 = re.sub("[^0-9]", "", id1)
            print(id1)
            query_element = {
                'q': postdata['post_id'],
                'pv': '',
                'order': 'createdate',
                'btn_srch': 'search'
            }
            query_string = 'https://www.ddteedin.com/myposts/?q='+query_element['q'].replace(' ', '+')+'&pv='+query_element['pv'].replace(
                ' ', '+')+'&order='+query_element['order'].replace(' ', '+')+"&btn_srch="+query_element['btn_srch'].replace(' ', '+')
            r = httprequestObj.http_get(
                query_string, verify=False)
            data = r.text
            id = postdata['post_id']
            query_string = 'https://www.ddteedin.com/myposts/'+id1
            # print(r.text)
            if data.find(" ไม่พบประกาศ") != -1:
                success = "false"
            else:
                # soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
                # id = soup.find("div", {"class": "it st1"})['id']
                # id = id.replace('r', '')
                # print(id)
                # id1 = postdata['log_id']
                # query_element['q'] = ''
                datapost = {
                    'id': id,
                    'act': 'del'
                }
                r = httprequestObj.http_post(query_string, data=datapost)
                print(r.text)
                query_string = 'https://www.ddteedin.com/'+postdata['post_id']
            # print(r.text)
            # print(r.status_code)
        else:
            success = "false"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "websitename": "ddteedin",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": query_string,
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": id,
            "account_type": "null",
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
        # print(ashopname)
        # for (key, value) in provincedata.items():
        #     if type(value) is str and postdata['addr_province'].strip() in value.strip():
        #         province_id = key
        #         break

        # for (key, value) in provincedata[province_id+"_province"].items():
        #     if postdata['addr_district'].strip() in value.strip():
        #         amphur_id = key
        #         break
        found = "true"
        post_id = ""
        posturl = ""
        if success == "true":
            query_element = {
                "q":postdata['post_title_th'],
                "pv":'',
                "order":"createdate",
                "btn_srch":"search"
            }

            query_string = 'https://www.ddteedin.com/myposts/?q='+query_element['q'].replace(' ', '+')+'&pv='+query_element['pv'].replace(
                ' ', '+')+'&order='+query_element['order'].replace(' ', '+')+"&btn_srch="+query_element['btn_srch'].replace(' ', '+')
            r = httprequestObj.http_get(query_string, verify = False)    
            data = r.text
            soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
            if(data.find(" ไม่พบประกาศ") != -1):
                found = "false"
            else:
                found = "true"
                post_id = soup.find("strong").get_text().replace("#","")
                posturl = 'https://www.ddteedin.com/'+post_id
        else:
            success = "false"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        log_id = ""
        if 'log_id' in postdata:
            log_id = postdata['log_id']
        return {
            "websitename": "ddteedin",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_found": found,
            "ds_id": postdata['ds_id'],
            "log_id": log_id,
            "post_url": posturl,
            "post_id": post_id,
            "account_type": "null",
            "detail":"null",
            "post_create_time":"",
            "post_modify_time":"",
            "post_view":""
        }

    def boost_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        post_id = postdata['post_id']
        log_id = postdata['log_id']

        test_login = self.test_login(postdata)
        success = test_login["success"]
        ashopname = test_login["detail"]

        if success == "true":
            # tumbon_id = '01'
            r = httprequestObj.http_get('https://www.ddteedin.com/myposts/?rf=login', verify=False)

            query_element = {
                'q': postdata['post_id'],
                'pv': '',
                'order': 'createdate',
                'btn_srch': 'search'
            }
            query_string = 'https://www.ddteedin.com/myposts/?q='+query_element['q'].replace(' ', '+')+'&pv='+query_element['pv'].replace(
                ' ', '+')+'&order='+query_element['order'].replace(' ', '+')+"&btn_srch="+query_element['btn_srch'].replace(' ', '+')
            r = httprequestObj.http_get(query_string, verify=False)
            data = r.text
            id = postdata['post_id']
            # print(r.text)
            if data.find(" ไม่พบประกาศ") != -1:
                success = "false"
            else:
                query_string = 'https://www.ddteedin.com/post-land-for-sale/edit/'+str(id)
                r = httprequestObj.http_get(query_string, verify=False)
                data = r.text
                soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
                try:
                    cverify = soup.find("input", {"name": "cverify"})['value']

                    datapost = [
                        ('action', 'edit_post'),
                        ('act', 'edit'),
                        ('timeout', '5'),
                        ('code', ''),
                        ('warning', ""),
                        ('opts[]', 62),
                        ('cverify', cverify)
                        ('id', id),
                    ]

                    r = httprequestObj.http_post(query_string, data=datapost)

                except:
                    success = "false"
        else:
            success = "false"


        time_end = datetime.datetime.utcnow()
        return {
            "websitename": "ddteedin",
            "success": success,
            "time_usage": time_end - time_start,
            "start_time": time_start,
            "end_time": time_end,
            "detail": "",
            'ds_id': postdata['ds_id'],
            "log_id": log_id,
            "post_id": post_id,
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


# a = ddteedin()
# credentials = {
#     "action": "register_user",
#     "timeout": "7",
#     "web": [
#         {
#             "ds_name": "ddteedin",
#             "ds_id": "4",
#             "user": "amarin.ta@gmail.com",
#             "pass": "5k4kk3253434",
#             "company_name": "amarin inc",
#             "name_title": "mr",
#             "name_th": "อัมรินทร์",
#             "surname_th": "บุญเกิด",
#             "name_en": "Amarin",
#             "surname_en": "Boonkirt",
#             "tel": "0891999450",
#             "line": "amarin.ta",
#             "addr_province" : "nonthaburi"
#         }
#     ]
# }

# credentials = {
#     "geo_latitude": "13.786862",
#     "geo_longitude": "100.757815",
#     "property_id": "4",
#     "forid": "3",
#     "typeid": "2",
#     "isnew": "1",
#     "post_title_th": "xxx",
#     "short_post_title_th": "xxx",
#     "post_description_th": "xxx",
#     "post_title_en": "",
#     "short_post_title_en": "xxx",
#     "post_description_en": "",
#     "price_baht": "3000",
#     "listing_type": "ขาย",
#     "property_type": "คอนโด",
#     "floor_level  ": "11",
#     "floor_total  ": "11",
#     "floor_area  ": "11",
#     "bath_room  ": "11",
#     "bed_room  ": "11",
#     "prominent_point  ": "จุดเด่น",
#     "view_type ": "11",
#     "direction_type": "11",
#     "addr_province": "จังหวัด",
#     "addr_district": "เขต",
#     "addr_sub_district": "ตำบล แขวง",
#     "addr_road": "ถนน",
#     "addr_soi": "ซอย",
#     "addr_near_by": "สถานที่ใกล้เคียง",
#     "floor_area": "พื้นที่",
#     "price": "1234",
#     "product_details": "jslkfdklfjdfkldfjdflkdfjdflksjfklhgdfoewitogjdfjdlskfdsjfdklfgjfklgdhfdslkfdhfdlfhewioffhdlkghfdlkfdskjfdlkgjhglkdsfhlgdshkfefhioglshg",
#     "options": {},
#     "land_size_rai": "ขนาดที่ดินเป็นไร่",
#     "land_size_ngan": "ขนาดที่ดินเป็นงาน",
#     "land_size_wa": "ขนาดที่ดินเป็นวา",
#     "name": "land on rent",
#     "mobile": "9876543210",
#     "email": "ramu@gmail.com",
#     "line": "xxx",
#     "project_name": "ลุมพีนีวิลล รามอินทราหลักสี่",
#     "user": "ramu@gmail.com",
#     "pass": "raam1234"
# }
# ret = a.create_post(credentials)
# print(ret)
# login_credentials = {
#     "user":"reteh37681@fft-mail.com",
#     "pass":'12345678',
# }
# ret = a.test_login(login_credentials)
# print(ret)
# postdata = {
#     "action": "edit_post", "timeout": "5", "project_name": "ลุมพีนีวิลล", "post_img_url_lists": ["https://zignnet.sgp1.digitaloceanspaces.com/livingjoin/classified/189689/big/210120235215500991.jpg", "https://zignnet.sgp1.digitaloceanspaces.com/livingjoin/classified/189689/other/big/210120235220317918.jpg"], "geo_latitude": "13.786862", "geo_longitude": "100.757815", "property_id": "chu001", "post_title_th": "new edited ให้เช่า ที่ดินด่วน บางกรวยไทรน้อย 6 ไร่ เหมาะทำตลาด", "post_description_th": "What is description", "post_title_en": "Land for rent bangkloysainoi 6 rai suitable for developing", "post_description_en": "Land for rent bangkloysainoi 6 rai suita ble for developing", "price_baht": "100000", "listing_type": "เช่า", "property_type": "6", "prominent_point ": "หน้ากว้างมาก ให้เช่าถูกสุด", "direction_type": "11", "addr_province": "นนทบุรี", "addr_district": "เมืองนนทบุรี", "addr_sub_district": "บางกรวย", "addr_road": "บางกรวย-ไทรน้อย", "addr_soi": "ซอยบางกรวย-ไทรน้อย 34", "addr_near_by": "ถนนพระราม5\nถนนนครอินทร์", "land_size_rai": "6", "land_size_ngan": "0", "land_size_wa": "0", "name": "ชู", "mobile": "0992899999", "email": "panuwat.ruangrak@gmail.com", "line": "0992899999", "ds_name": "ddteedin", "ds_id": "120", "user": "reteh37681@fft-mail.com", "pass": "12345678", "post_id": "484916", "log_id": "48791", "account_type": "corperate"
# }
# a = ddteedin()
# # ret = a.edit_post(postdata)
# # print(ret)
# email = "reteh37681@fft-mail.com"
# site = "ddteedin.com"
# thedata = { "action": "edit_post", "timeout": "5", "project_name": "ลุมพีนีวิลล รามอินทราหลักสี", "post_img_url_lists": [ "https://unsplash.com/photos/gZlycYbRtkk","https://zignnet.sgp1.digitaloceanspaces.com/livingjoin/classified/189689/big/210120235215500991.jpg", "https://zignnet.sgp1.digitaloceanspaces.com/livingjoin/classified/189689/other/big/210120235220317918.jpg"], "geo_latitude": "13.786862", "geo_longitude": "100.757815", "property_id" : "chu001", "post_title_th": "ให้เช่า ที่ดินด่วน บางกรวยไทรน้อย 6 ไร่ เหมาะทำตลาดสด เปิดท้าย", "post_description_th": "ขายที่ดินด่วน บางกรวยไทรน้อย 6 ไร่ เหมาะทำตลาด\r\nรายละเอียด\r\nที่ดิน\r\nขนาด 6 ไร่\r\nหน้ากว้าง 30 เมตร ติดถนนบางกรวยไทรน้อย\r\nที่ดินยังไม่ถมต่ำกว่าถนนประมาณ 1 เมตร\r\n\r\nสถานที่ใกล้เคียง\r\nถนนพระราม5\r\nถนนนครอินทร์\r\n\r\nให้เช่าระยะยาว 100,000 บาท ต่อเดือน\r\n\r\nสนใจติดต่อ คุณชู 0992899999\r\nline: 099289999", "post_title_en": "Land for rent bangkloysainoi 6 rai suitable for developing", "post_description_en": "Land for rent bangkloysainoi 6 rai suitable for developing\r\nLand Size 6 rai\r\nWidth 30 meter", "price_baht": "100000", "listing_type": "เช่า", "property_type": "6", "prominent_point " : "หน้ากว้างมาก ให้เช่าถูกสุด", "direction_type" : "11", "addr_province": "นนทบุรี", "addr_district": "เมืองนนทบุรี", "addr_sub_district": "บางกระสอ", "addr_road": "บางกรวย-ไทรน้อย", "addr_soi": "ซอยบางกรวย-ไทรน้อย 34", "addr_near_by": "ถนนพระราม5\r\nถนนนครอินทร์", "land_size_rai": "6", "land_size_ngan": "0", "land_size_wa": "0", "name": "fdjsljfkl", "mobile": "0992899999", "email": email, "line": "0992899999","ds_name": site, "ds_id": "120", "user": email, "pass": "12345678", "post_id":"486628"}
# # a = ddteedin()
# ret = a.edit_post(thedata)
# print(ret)
