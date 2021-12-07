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
        #options.add_argument("--headless")
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

                if postdata['listing_type'] == 'ขาย':
                    WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="g_for"]/label[1]/input'))).click()
                    WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="g_isnew"]/label[2]/input'))).click()
                else:
                    WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="g_for"]/label[2]/input'))).click()

                if 'web_project_name' not in postdata:
                    if 'project_name' not in postdata:
                        postdata['project_name'] = ''
                    postdata['web_project_name'] = postdata['project_name']
                try:
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'project'))).send_keys(postdata['web_project_name'])
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'rooms'))).send_keys(postdata['bed_room'])
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'bathroom'))).send_keys(postdata['bath_room'])
                except:
                    pass

                if ('floor_level' not in postdata) or (postdata['floor_level'] == ''):
                    postdata['floor_level'] = postdata['floor_total']

                try:
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'floor'))).send_keys(postdata['floor_level'])
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'usagesize'))).send_keys(postdata['floorarea_sqm'])
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

                if '.' in postdata['line']:
                    postdata['line'] = ''

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
    
    def edit_info(self,path,namepath,info):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((path, namepath))).send_keys(Keys.CONTROL + "a")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((path, namepath))).send_keys(info)

    def edit_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        success = False
        detail = 'Something wrong'
        test_login = self.test_login(postdata)
        success = test_login["success"]

        if success:
            success = False
            try:
                try:
                    webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                except:
                    pass
                sleep(2)
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, 'srch'))).send_keys(postdata['property_id'])
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, 'btn_srch'))).click()
                sleep(3)
                if len(self.driver.find_elements_by_partial_link_text('แก้ไข')) ==0:
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, 'srch'))).send_keys(Keys.CONTROL + "a")
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, 'srch'))).send_keys(postdata['post_id'])
                    WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, 'btn_srch'))).click()
                    sleep(3)
                if len(self.driver.find_elements_by_partial_link_text('แก้ไข')) ==0:
                    search = self.search_post(postdata)
                    if search['post_id'] == '':
                        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, 'srch'))).send_keys(Keys.CONTROL + "a")
                        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, 'srch'))).send_keys(search['post_id'])
                        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, 'btn_srch'))).click()
                        sleep(3)
                if len(self.driver.find_elements_by_partial_link_text('แก้ไข')) ==0:
                    detail = 'Cannot found post id'
                else:
                    success = True
                    links = self.driver.find_elements_by_partial_link_text('แก้ไข')[0].get_attribute('href')
                    self.driver.get(links)
                if success:
                    success = False
                    while True:
                        try:
                            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="photos"]/div/a[3]/i'))).click()
                            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
                            alert = self.driver.switch_to.alert
                            alert.accept()
                            sleep(1)
                        except:
                            break
                    for i in postdata['post_images']:
                        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'fileupload'))).send_keys(os.path.abspath(i))
                        sleep(1)
                    
                    self.edit_info(By.ID,'name',postdata['post_title_th'])
                    self.edit_info(By.ID,'code',postdata['property_id'])

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

                    if postdata['listing_type'] == 'ขาย':
                        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="g_for"]/label[1]/input'))).click()
                        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="g_isnew"]/label[2]/input'))).click()
                    else:
                        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="g_for"]/label[2]/input'))).click()

                    if 'web_project_name' not in postdata:
                        if 'project_name' not in postdata:
                            postdata['project_name'] = ''
                        postdata['web_project_name'] = postdata['project_name']

                    try:
                        self.edit_info(By.ID,'project',postdata['web_project_name'])
                        self.edit_info(By.ID,'rooms',postdata['bed_room'])
                        self.edit_info(By.ID,'bathroom',postdata['bath_room'])
                    except:
                        pass

                    if ('floor_level' not in postdata) or (postdata['floor_level'] == ''):
                        postdata['floor_level'] = postdata['floor_total']

                    try:
                        self.edit_info(By.ID,'floor',postdata['floor_level'])
                        self.edit_info(By.ID,'usagesize',postdata['floorarea_sqm'])
                        self.edit_info(By.ID,'sizerai',postdata['land_size_rai'])
                        self.edit_info(By.ID,'sizewa2',postdata['land_size_wa'])
                    except:
                        pass
                    
                    if postdata['listing_type'] == 'ขาย':
                        self.edit_info(By.ID,'pricesale',postdata['price_baht'])
                    else:
                        self.edit_info(By.ID,'pricerent',postdata['price_baht'])

                    self.edit_info(By.ID,'email',postdata['email'])
                    self.edit_info(By.ID,'phone',postdata['mobile'])

                    if '.' in postdata['line']:
                        postdata['line'] = ''

                    self.edit_info(By.ID,'lineid',postdata['line'])
                    self.edit_info(By.ID,'street',postdata['addr_road'])
                    self.edit_info(By.ID,'soi',postdata['addr_soi'])

                    x = self.driver.find_element_by_id('province')
                    drop=Select(x)
                    drop.select_by_visible_text(postdata['addr_province'])

                    x = self.driver.find_element_by_id('amphur')
                    drop=Select(x)
                    drop.select_by_visible_text(postdata['addr_district'])

                    x = self.driver.find_element_by_id('tumbon')
                    drop=Select(x)
                    drop.select_by_visible_text(postdata['addr_sub_district'])

                    self.edit_info(By.ID,'detail',postdata['post_description_th'])

                    WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, 'btn_submit'))).click()
                    sleep(3)
                    matchObj = re.search(r'ห้ามใช้สัญลักษณ์พิเศษมากกว่า 1 ในชื่อประกาศ', self.driver.page_source)
                    if matchObj:
                        detail = 'Do not use more than one special symbol in the post title.'
                    matchObj = re.search(r'ประกาศถูกบันทึกแล้ว', self.driver.page_source)
                    if matchObj:
                        success = True
                        detail = 'Post edited'
            finally:
                self.driver.close()
                self.driver.quit()
        else:
            detail = test_login["detail"]
            self.driver.close()
            self.driver.quit()

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "websitename": "ddteedin",
            "success": success,
            "log_id": postdata['log_id'],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "post_url": '',
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

        success = False
        post_found = False
        post_url = ''
        post_id = ''
        test_login = self.test_login(postdata)
        success = test_login["success"]
        if success:
            if success:
                success = False
                try:
                    try:
                        webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                    except:
                        pass
                    sleep(2)
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'srch'))).send_keys(postdata['post_title_th'])
                    WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, 'btn_srch'))).click()
                    sleep(3)
                    try:
                        elems = self.driver.find_elements_by_xpath("//a[@href]")
                        for i in elems:
                            if postdata['post_title_th'] in i.text:
                                post_url = i.get_attribute('href')
                                post_id = post_url.split('/')[-1]
                                success = True
                                post_found = True
                                break
                    except:
                        pass
                finally:
                    self.driver.close()
                    self.driver.quit()
        else:
            self.driver.close()
            self.driver.quit()

        time_end = datetime.datetime.utcnow()
        time_usage = str(time_end - time_start)

        return {
            "websitename": "ddteedin",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "usage_time": time_usage,
            "post_found": post_found,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_url": post_url,
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
