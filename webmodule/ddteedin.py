# -*- coding: utf-8 -*-
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 
# from urlparse import urlparse
import re
import json
import datetime
from time import sleep 
import sys
from urllib.parse import unquote


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
        self.Partner_user = 'vinvestor.online@gmail.com'
        self.Partner_pwd = 'vinvestor'

    def logout_user(self):
        url = 'https://www.ddteedin.com/logout/'
        httprequestObj.http_get(url)


    def register_user(self, postdata):
        self.logout_user()
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        name_th = postdata["name_th"]
        surname_th = postdata["surname_th"]
        mobile_no = postdata["tel"]
        # start process
        success = False
        detail = ""
        data = {
            'Partner_user':self.Partner_user,
            'Partner_pwd':self.Partner_pwd,
            'cname':name_th+ ' '+surname_th,
            'email':postdata['user'],
            'mobile':mobile_no,
            'password':postdata['pass']
        }
        url = 'https://www.ddteedin.com/register'
        r = httprequestObj.http_post(url, data = data)
        print(r.text)
        response = (r.text).split('code')[1][1:-2]
        if response=='r001':
            detail = 'Register successful'
            success = True
        elif response == 'r003':
            detail = 'This phone number is already used'
        elif response == 'r004':
            detail = 'This email is already used'
        elif response == 'r005':
            detail = 'Wrong data.Please recheck it again'
        else:
            detail = 'response = {}.Please tell your developer to know this problem'.format(response)
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
        detail = 'Something wrong in this website.Please tell your developer to know this problem.'
        options = Options()
        options.set_headless(True)
        options.add_argument('--no-sandbox')
        try:
            self.driver = webdriver.Chrome("./static/chromedriver", chrome_options=options)
            self.driver.get('https://www.ddteedin.com/login')

            WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.NAME,'log_u'))).send_keys(postdata['user'])
            WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.NAME,'log_p'))).send_keys(postdata['pass'])
            WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.NAME,'login'))).click()
            sleep(2)
            try:
                alert = WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[4]/div/div[2]/form/div[1]'))).text
                if 'Username หรือ Password ไม่ถูกต้องกรุณาตรวจสอบ' in alert:
                    success = False
                    detail = "Wrong username or password"
            except:
                webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                alert = WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[4]/div/h1'))).text
                if 'ประกาศทั้งหมดของคุณ' in alert:
                    self.driver.get('https://www.ddteedin.com/post/?rf=topbtn')
                    try:
                        alert = WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[4]/div[1]/div/div/h2'))).text
                        if 'เงื่อนไขการลงประกาศฟรี' in alert:
                            success = True
                            detail = "Login successful"
                        elif 'เลือกรูปแบบการยืนยัน' in alert:
                            success = True
                            detail = "Login successful.But if you need to post please verify your phone number first"
                    except:
                        alert = WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[4]/div/h1'))).text
                        if 'กรุณายืนยันหมายเลขโทรศัพท์' in alert:
                            success = True
                            detail = "Login successful.But if you need to post please verify your phone number first"

        finally:
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
            "detail": detail
        }

    def post_prop(self,action,postdata):

        if postdata['listing_type'] == 'ขาย':
            postdata['listing_type'] = '1'
        else:
            postdata['listing_type'] = '3'

        property_type = {'1':'2','2':'4','3':'4','4':'12','5':'11','6':'3','7':'1','8':'1','9':'11','10':'13','25':'13','30':'3'}
        postdata['property_type'] = property_type[postdata['property_type']]
        
        if ('floor_level' not in postdata) or (postdata['floor_level'] == ''):
            postdata['floor_level'] = postdata['floor_total']
        
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
        if province_id == '0' or amphur_id == '26' or tumbon_id == '01':
            province_id = '81'
            amphur_id = '03'
            tumbon_id = '03'
        
        if postdata['property_type'] != '2':
            postdata['land_size_rai']=postdata['land_size_rai']
            postdata['land_size_wa']=100*int(postdata['land_size_ngan'])+int(postdata['land_size_wa'])
        isnew = None
        postdata['web_project_name'] = None
        if postdata['property_type'] != '3':
            isnew = '2'
            if 'web_project_name' not in postdata:
                postdata['web_project_name'] = postdata['project_name']

        if action == 'create':
            url = 'https://www.ddteedin.com/post/'
        elif action =='edit':
            url = 'https://www.ddteedin.com/post-land-for-sale/edit/{}'.format(postdata['post_id'])

        data = [
            ('Partner_user',self.Partner_user),
            ('Partner_pwd',self.Partner_pwd),
            ('Owner_user',postdata['user']),
            ('Owner_pwd',postdata['pass']),
            ('name',postdata['post_title_th']),
            ('code',postdata['property_id']),
            ('forid',postdata['listing_type']),
            ('typeid',postdata['property_type']),
            ('isnew',isnew),
            ('project',postdata['web_project_name']),
            ('rooms',postdata['bed_room']),
            ('bathroom',postdata['bath_room']),
            ('floor',postdata['floor_level']),
            ('usagesize',postdata['floorarea_sqm']),
            ('sizerai',postdata['land_size_rai']),
            ('sizewa2',postdata['land_size_wa']),
            ('price',postdata['price_baht']),
            ('email',postdata['user']),
            ('phone',postdata['mobile']),
            ('lineid',postdata['line']),
            ('street',postdata['addr_road']),
            ('soi',postdata['addr_soi']),
            ('warning',''),
            ('lat',postdata['geo_latitude']),
            ('lng',postdata['geo_longitude']),
            ('opts[]',62),
            ('province',province_id),
            ('amphur',amphur_id),
            ('tumbon',tumbon_id),
            ('detail',postdata['post_description_th'])
        ]

        url_upload = 'https://www.ddteedin.com/upload/'
        for i, image in enumerate(postdata['post_images'][:10]):
            files = {'files': open(os.getcwd()+"/"+image, 'rb')}
            r = httprequestObj.http_post(url_upload, data = data,files=files)
            img_path = r.json()['images'][0][0]
            data.append(('pid[]', ''))
            data.append(('file[]', img_path))
            if i == 0:
                data.append(('df[]', '1'))
            else:
                data.append(('df[]', ''))

        r = httprequestObj.http_post(url, data = data)
        response = (r.text).split('code')[1][1:-2]
        if response =='p001' or response =='p002':
            post_id = (r.text).split('post_id')[1][1:-2]
            post_url = (r.text).split('messages')[1][1:-2].split(' ')[1]
        else:
            post_id = ''
            post_url = ''
        return {
            'response':response,
            'post_id':post_id,
            'post_url':post_url
        }
    
    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        success = False
        detail = ''
        post_url = ''
        post_id = ''
        login = self.test_login(postdata)
        if (login['success'] == True) and (login['detail'] == "Login successful"):
            post = self.post_prop('create',postdata)
            response = post['response']
            post_id = post['post_id']
            post_url = post['post_url']
            
            if response=='p001':
                detail = 'Post successful'
                success = True
            elif response == 'p002':
                success = True
                detail = 'Post successful. Please wait website to verify your post'
            elif response == 'p003':
                detail = 'Your account is temporarily suspended. Because you have some posts are waiting to verify more than the agreement'
            elif response == 'p004':
                detail = 'Please verify your phone number'
            elif response == 'p005':
                detail = 'Your account has posted the daily quota.'
            elif response == 'p006':
                detail = 'Wrong data.Please recheck it again'
            elif response == 'p007':
                detail = "You don't have the right to manage this property or this property is already deleted"
            elif response == 'u001':
                detail = "Wrong username or password"
            else:
                detail = 'response = {}.Please tell your developer to know this problem.'.format(response)
        else:
            detail = login['detail']

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

        success = False
        detail = ''
        post_url = ''
        post_id = ''
        edit = self.post_prop('edit',postdata)
        response = edit['response']
        post_id = edit['post_id']
        post_url = edit['post_url']
            
        if response=='p001':
            detail = 'Edit successful'
            success = True
        elif response == 'p002':
            success = True
            detail = 'Edit successful. Please wait website to verify your post'
        elif response == 'p003':
            detail = 'Your account is temporarily suspended. Because you have some posts are waiting to verify more than the agreement'
        elif response == 'p004':
            detail = 'Please verify your phone number'
        elif response == 'p005':
            detail = 'Your account has posted the daily quota.'
        elif response == 'p006':
            detail = 'Wrong data.Please recheck it again'
        elif response == 'p007':
            detail = "You don't have the right to manage this property or this property is already deleted"
        elif response == 'u001':
            detail = "Wrong username or password"
        else:
            detail = 'response = {}.Please tell your developer to know this problem'.format(response)

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

    def manage_prop(self,action,postdata):
        act = {'delete':'del','boost':'reindex'}
        data = {
            'Partner_user':self.Partner_user,
            'Partner_pwd':self.Partner_pwd,
            'Owner_user':postdata['user'],
            'Owner_pwd':postdata['pass'],
            'act':act[action],
            'id':postdata['post_id']
        }
        url = 'https://www.ddteedin.com/myposts/'
        r = httprequestObj.http_post(url, data = data)
        print(r.text)
        response = (r.text).split('code')[1][1:-2]
        return response

    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        success = False
        detail = ''
        response = self.manage_prop('delete',postdata)

        if response=='p001':
            detail = 'Post deleted'
            success = True
        elif response == 'p007':
            detail = "You don't have the right to manage this property or this property is already deleted"
        elif response == 'u001':
            detail = "Wrong username or password"
        else:
            detail = 'response = {}.Please tell your developer to know this problem'.format(response)

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
            "ds_name": "ddteedin"
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
        found = False
        post_id = ""
        posturl = ""
        if success == True:
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
                found = False
            else:
                found = True
                post_id = soup.find("strong").get_text().replace("#","")
                posturl = 'https://www.ddteedin.com/'+post_id
        else:
            success = False
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
        success = False
        detail = ''
        response = self.manage_prop('boost',postdata)

        if response=='p001':
            detail = 'Boost successful'
            success = True
        elif response == 'p007':
            detail = "You don't have the right to manage this property or this property is already deleted"
        elif response == 'u001':
            detail = "Wrong username or password"
        else:
            detail = 'response = {}.Please tell your developer to know this problem'.format(response)
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
            "ds_name": "ddteedin"
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