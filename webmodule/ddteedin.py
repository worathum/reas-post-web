# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
import os
import re
from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from urlparse import urlparse
import json
import datetime
from time import sleep
import sys
from urllib.parse import unquote

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
        self.httprequestObj = lib_httprequest()

    def logout_user(self):
        url = 'https://www.ddteedin.com/logout/'
        self.httprequestObj.http_get(url)


    def register_user(self, postdata):
        self.logout_user()
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
        r = self.httprequestObj.http_post('https://www.ddteedin.com/apis/profile', data = data1)
        print(r.text)
        if r.text != 'Yes':
            success = "false"
            detail = "Can't register"
        data1 = {
            "mobile":mobile_no
        }
        r = self.httprequestObj.http_post('https://www.ddteedin.com/apis/user_check', data = data1)
        data = json.loads(r.text)
        print(data)
        if(data['result'] != 'yes'):
            success = "false",
            detail = 'Incorrect mobile number'
        r = self.httprequestObj.http_post(
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
        self.logout_user()
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        success = False
        detail = 'Something wrong'

        options = Options()
        # debug by comment option --headless
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome("./static/chromedriver", chrome_options=options)
        try:
            self.driver.get('https://www.ddteedin.com/login')
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, 'log_u'))).send_keys(postdata['user'])
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'log_p'))).send_keys(postdata['pass'])
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.NAME, 'login'))).click()
            sleep(2)
            matchObj = re.search(r'Username หรือ Password ไม่ถูกต้องกรุณาตรวจสอบ', self.driver.page_source)
            matchObj2 = re.search(r'ออกจากระบบ', self.driver.page_source)
            if matchObj:
                success = False
                detail = 'Wrong username or password'
            elif matchObj2:
                success = True
                detail = 'Login successful'
        finally:
            if postdata['action'] == 'test_login':
                self.driver.close()
                self.driver.quit()

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "ddteedin",
            "success": success,
            "ds_id": postdata['ds_id'],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "usage_time": str(time_usage),
            "detail": detail
        }

    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        success = False
        detail = 'Something wrong'
        post_id = ''
        post_url = ''
        test_login = self.test_login(postdata)
        success = test_login["success"]

        if success:
            success = False
            self.driver.get('https://www.ddteedin.com/post/?rf=topbtn')
            matchObj = re.search(r'ยืนยันหมายเลขโทรศัพท์', self.driver.page_source)
            if matchObj:
                detail = 'Login successful.But if you need to post please verify your phone number first'
            elif len(postdata['post_title_th'])<50:
                detail = 'The post title should have an alphabet of more than 50 alphabet'
            elif len(postdata['post_description_th'])<150:
                detail = 'The post description should have an alphabet of more than 150 alphabet'
            else:
                success = True

        if success:
            success = False
            try:
                
                for i in postdata['post_images']:
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'fileupload'))).send_keys(os.path.abspath(i))

                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'name'))).send_keys(postdata['post_title_th'])
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'code'))).send_keys(postdata['property_id'])

                if postdata['listing_type'] == 'ขาย':
                    WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="g_for"]/label[1]/input'))).click()
                    WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="g_isnew"]/label[2]/input'))).click()
                else:
                    WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="g_for"]/label[2]/input'))).click()

                property = {
                    '1': 'คอนโด',
                    '2': 'บ้าน',
                    '3': 'บ้าน',
                    '4': 'ทาวน์เฮาส์',
                    '5': 'อาคารพาณิชย์ / สำนักงาน',
                    '6': 'ที่ดิน',
                    '7': 'อพาร์ทเม้นท์ / โรงแรม',
                    '8': 'อพาร์ทเม้นท์ / โรงแรม',
                    '9': 'อาคารพาณิชย์ / สำนักงาน',
                    '10': 'โรงงาน / โกดัง',
                    '25': 'โรงงาน / โกดัง'
                }

                property_type = property[postdata['property_type']]
                x = self.driver.find_element_by_id('typeid')
                drop=Select(x)
                drop.select_by_visible_text(property_type)

                if 'web_project_name' not in postdata:
                    postdata['web_project_name'] = postdata['project_name']

                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'project'))).send_keys(postdata['web_project_name'])
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'rooms'))).send_keys(postdata['bed_room'])
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'bathroom'))).send_keys(postdata['bath_room'])

                if ('floor_level' not in postdata) or (postdata['floor_level'] == ''):
                    postdata['floor_level'] = postdata['floor_total']

                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'floor'))).send_keys(postdata['floor_level'])
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'usagesize'))).send_keys(postdata['floorarea_sqm'])
                try:
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'sizerai'))).send_keys(postdata['land_size_rai'])
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'sizewa2'))).send_keys(postdata['land_size_wa'])
                except:
                    pass
                if postdata['listing_type'] == 'ขาย':
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'pricesale'))).send_keys(postdata['price_baht'])
                else:
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'pricerent'))).send_keys(postdata['price_baht'])

                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'email'))).send_keys(postdata['email'])
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'phone'))).send_keys(postdata['mobile'])
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'lineid'))).send_keys(postdata['line'])
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'street'))).send_keys(postdata['addr_road'])
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'soi'))).send_keys(postdata['addr_soi'])

                x = self.driver.find_element_by_id('province')
                drop=Select(x)
                drop.select_by_visible_text(postdata['addr_province'])

                x = self.driver.find_element_by_id('amphur')
                drop=Select(x)
                drop.select_by_visible_text(postdata['addr_district'])

                x = self.driver.find_element_by_id('tumbon')
                drop=Select(x)
                drop.select_by_visible_text(postdata['addr_sub_district'])

                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'detail'))).send_keys(postdata['post_description_th'])
                
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="opts_list_group_2"]/label[9]/input'))).click()
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, 'btn_submit'))).click()
                sleep(3)
                matchObj = re.search(r'ประกาศนี้มีรายละเอียดคล้ายกับประกาศที่มีอยู่แล้วมากเกินไป', self.driver.page_source)
                if matchObj:
                    detail = 'Post unsuccessful.This post contains details that are too similar to existing posts.'
                else:
                    post_url = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-contain"]/div/div/a[2]'))).get_attribute('href')
                    post_id = post_url.split('/')[3]
                    success = True
                    detail = 'Post successful'
            finally:
                self.driver.close()
                self.driver.quit()
        else:
            if test_login["success"] == False:
                detail = test_login["detail"]
            self.driver.close()
            self.driver.quit()

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "websitename": "ddteedin",
            "success": success,
            "detail":detail,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "usage_time": str(time_usage),
            "post_url": post_url,
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
            # r = self.httprequestObj.http_get(
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
            r = self.httprequestObj.http_get(
                query_string, verify=False)
            data = r.text
            query_string = 'https://www.ddteedin.com/post-land-for-sale/edit/'+id
            if data.find(" ไม่พบประกาศ") != -1:
                success = "false"
            else:
                r = self.httprequestObj.http_get(query_string, verify=False)
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
                    r = self.httprequestObj.http_get('https://www.ddteedin.com/apis/project/?q='+dataquery["q"],verify = False)
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
                options = Options()
                options.set_headless(True)
                options.add_argument('--no-sandbox')
                try:
                    browser = webdriver.Chrome("./static/chromedriver", chrome_options=options)
                    # browser = webdriver.Chrome(
                        # executable_path='/usr/bin/chromedriver',options=options)
                    wait = WebDriverWait(browser,10)
                    browser.implicitly_wait(100)


                    r = self.httprequestObj.http_post(
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
                finally:
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

            # print(r.text)
        else:
            success = "false"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

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
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]

        if success == "true":
            r = self.httprequestObj.http_get(
                'https://www.ddteedin.com/myposts/?rf=login', verify=False)
            time.sleep(1)
            print(r.url)
            user_id = r.url.split('/')[-2]
            query_element = {
                'q': postdata['post_id'],
                'pv': '',
                'order': 'createdate',
                'btn_srch': 'search'
            }
            query_string = 'https://www.ddteedin.com/myposts/' + user_id + '/?q='+query_element['q'].replace(' ', '+')+'&pv='+query_element['pv'].replace(
                ' ', '+')+'&order='+query_element['order'].replace(' ', '+')+"&btn_srch="+query_element['btn_srch'].replace(' ', '+')
            r = self.httprequestObj.http_get(query_string, verify=False)
            data = r.text
            if data.find(" ไม่พบประกาศ") != -1:
                success = "false"
                detail = 'Your post id not found.'
            else:
                del_link = 'https://www.ddteedin.com/myposts/' + user_id +'/?rf=login'
                datapost = {
                    'id': postdata['post_id'],
                    'act': 'del'
                }
                r = self.httprequestObj.http_post(del_link, data=datapost)
                detail = 'Deleted post succesful'
        else:
            success = "false"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "websitename": "ddteedin",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "usage_time": str(time_usage),
            "detail": detail,
            "ds_id": postdata['ds_id'],
            "post_id": postdata['post_id'],
            "log_id": postdata['log_id'],
            "account_type": "",
            "ds_name": "hipflat"
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
            r = self.httprequestObj.http_get(query_string, verify = False)    
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


        if success == "true":
            options = Options()
            options.set_headless(True)
            options.add_argument('--no-sandbox')
            try:
                browser = webdriver.Chrome("./static/chromedriver",chrome_options=options)
                #browser = webdriver.Chrome("./static/chromedriver")
                wait = WebDriverWait(browser, 10)
                browser.implicitly_wait(100)

                browser.get('https://www.ddteedin.com/login/')
                time.sleep(2)
                email = browser.find_element_by_name('log_u')
                email.clear()
                email.send_keys(postdata['user'])
                password = browser.find_element_by_name('log_p')
                password.clear()
                password.send_keys(postdata['pass'])
                browser.find_element_by_name('login').click()
                time.sleep(2)

                search = browser.find_element_by_name('q')
                search.send_keys(post_id + Keys.ENTER)
                time.sleep(2)

                soup = BeautifulSoup(browser.page_source, "html5lib")
                if "ไม่พบประกาศ" not in soup.text:
                    boost = browser.find_element_by_class_name('reindex')
                    boost.click()
                    time.sleep(10)
                    soup1 = BeautifulSoup(browser.page_source, "html5lib")

                    res=soup1.find("a", attrs={"class": "success"})

                    if res != None:
                        success=True
                        detail="Post Boosted Successfully."
                    elif soup1.find("a", attrs={"class": "disabled"}):
                        success=False
                        detail="Post already Boosted wait for another day."
                    else:
                        success=False
                        detail="Post can't be Boosted."

                else:
                    success = False
                    detail = "Post not found."

            except:
                success = False
                detail = "Post can't be Boosted."

            finally:
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

            """
            # tumbon_id = '01'
            r = self.httprequestObj.http_get('https://www.ddteedin.com/myposts/?rf=login', verify=False)

            query_element = {
                'q': postdata['post_id'],
                'pv': '',
                'order': 'createdate',
                'btn_srch': 'search'
            }
            query_string = 'https://www.ddteedin.com/myposts/?q='+query_element['q'].replace(' ', '+')+'&pv='+query_element['pv'].replace(
                ' ', '+')+'&order='+query_element['order'].replace(' ', '+')+"&btn_srch="+query_element['btn_srch'].replace(' ', '+')
            print(query_string)
            r = self.httprequestObj.http_get(query_string, verify=False)
            data = r.text

            id = postdata['post_id']
            # print(r.text)
            if "ไม่พบประกาศ" in data:
                success = "false"
            else:

                query_string = 'https://www.ddteedin.com/post-land-for-sale/edit/'+str(id)
                r = self.httprequestObj.http_get(query_string, verify=False)
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
                        ('cverify', cverify),
                        ('id', id),
                        ('btn_submit',"บันทึกแก้ไข")
                    ]

                    r = self.httprequestObj.http_post(query_string, data=datapost)

                except Exception as e:
                    success = "false"
            """
        else:
            success = "false"
            detail="Can't Login."


        time_end = datetime.datetime.utcnow()
        return {
            "websitename": "ddteedin",
            "success": success,
            "time_usage": time_end - time_start,
            "start_time": time_start,
            "end_time": time_end,
            "detail": detail,
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
