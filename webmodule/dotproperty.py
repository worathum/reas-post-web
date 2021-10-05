# -*- coding: utf-8 -*-

from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
# from urlparse import urlparse
import re
import json
import datetime
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image

httprequestObj = lib_httprequest()

'''
https://www.dotproperty.co.th/login
'''


class dotproperty():

    name = 'dotproperty'

    def __init__(self):

        try:
            import configs
        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.primary_domain = 'https://www.dotproperty.co.th'
        self.debug = 0
        self.debugresdata = 0
        self.PARSER = 'html.parser'

# _token=zTBJM5ODToev1CyL1fA6y2FwYf3hjYi6pgwHF61d&agency_id=&company_name=&email=amarin_ta@hotmail.com&mail_list=yes&name=amarin%20boonkirt&password=5k4kk3253434&phone=&phone-full=&seller_type=private&type_register=buyer&username=
    def register_user(self, data):
        #self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()

        r = httprequestObj.http_get_with_headers(self.primary_domain + '/signup', verify=False)
        data1 = r.text
        soup = BeautifulSoup(data1, self.PARSER)

        frm_token = soup.find("input", {"name": "_token"})['value']
        #print(frm_token)

        postdata = {
            '_token': frm_token,
            'username':'',
            'name': data['name_th'],
            'email': data['user'],
            'password': data['pass'],
            'type_register': 'agent',
            'seller_type': 'private',
            'phone': data['tel'],
            'phone-full': '+66'+str(data['tel']),
            'agency_id':'',
            'company_name':'',
            'inter_seller': '1',
            'mail_list': 'yes'
        }
        ##print('there')
        success = ''
        detail = ''
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
        elif len(data['pass'])<6:
            success = 'false'
            detail = 'Password length must be at least 6'
        else:
            r = httprequestObj.http_post_with_headers(self.primary_domain + '/signup', data=postdata)
            txt = str(r.text)

            if txt.find('ประเทศไทย เช่าอสังหาริมทรัพย')==-1:
                success = 'true'
                detail = 'Successfully registered'
            else:
                success = 'false'
                detail = 'Already a user'

        # bot process end
        end_time = datetime.datetime.utcnow()
        result = {'websitename': 'dotproperty',
                  'success': success,
                  'start_time': str(start_time),
                  'end_time': str(end_time),
                  'usage_time': str(end_time - start_time),
                  'detail': detail,
                  'ds_id': data['ds_id']}
        return result

# https://www.dotproperty.co.th/login
# https://www.dotproperty.co.th/ajaxLogin  _token=I3saeeA5CnOvCAdnCeNi9YssrAg4XNdSWhFbuzNf&email=amarin_ta@hotmail.com&password=5k4kk3253434&refer_type=login&remember=on

    def test_login(self, data):
        start_time = datetime.datetime.utcnow()

        success = ''
        detail = ''
        
        path = './static/chromedriver'
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-notifications')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-infobars')
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(executable_path=path, options=options)

        #driver.maximize_window()
        try:
            driver.get('https://www.dotproperty.co.th/login')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'email'))).send_keys(data['user'])
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'password'))).send_keys(data['pass'])
            login_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'loginPopupBtn')))
            actions = ActionChains(driver)
            actions.move_to_element(login_btn).click().perform()
            time.sleep(3.5)
            txt = str(driver.page_source)
            if txt.find('อีเมลและ/หรือรหัสผ่านของคุณไม่ตรงกัน โปรดลองใหม่อีกครั้ง')!=-1:
                success = 'false'
                detail = 'อีเมลและ/หรือรหัสผ่านของคุณไม่ตรงกัน โปรดลองใหม่อีกครั้ง'
            elif txt.find('email ต้องเป็นอีเมลแอดเดรสที่มีอยู่จริงเท่านั้น') != -1:
                success = 'false'
                detail = 'Your usename needs to be email pattern.'
            else:
                success = 'true'
                detail = 'Log in success'
        finally:
            driver.close()
            driver.quit()
        
        end_time = datetime.datetime.utcnow()
        result = {'websitename': 'dotproperty',
                  'success': success,
                  'start_time': str(start_time),
                  'end_time': str(end_time),
                  'usage_time': str(end_time - start_time),
                  'ds_id': data['ds_id'],
                  'detail': detail}
        return result


# https://www.dotproperty.co.th/my-dashboard/properties
# PUT https://www.dotproperty.co.th/dashboard-api/user/check-verified/1524090
# requestBody: {"data":{}}

# 1 ask to gen post id
# PUT https://www.dotproperty.co.th/dashboard-api/properties/store
# requestBody: {"data":{"user_id":1524090,"property_type":"property","name":""}}

# 2 return post id
# GET https://www.dotproperty.co.th/dashboard/properties/4817126/edit

# 3 redirect to edit view
# GET https://www.dotproperty.co.th/my-dashboard/properties/4817126/edit
    def create_post(self, data):
        time_start = datetime.datetime.utcnow()

        path = './static/chromedriver'
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-notifications')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-infobars')
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(executable_path=path, options=options)

        #driver.maximize_window()
        driver.get('https://www.dotproperty.co.th/login')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'email'))).send_keys(data['user'])
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'password'))).send_keys(data['pass'])
        login_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'loginPopupBtn')))
        actions = ActionChains(driver)
        actions.move_to_element(login_btn).click().perform()
        time.sleep(3.5)
        txt = str(driver.page_source)
        if txt.find('อีเมลและ/หรือรหัสผ่านของคุณไม่ตรงกัน โปรดลองใหม่อีกครั้ง')!=-1:
            success = 'false'
            detail = 'Invalid credentials'
        elif txt.find('email ต้องเป็นอีเมลแอดเดรสที่มีอยู่จริงเท่านั้น') != -1:
            success = 'false'
            detail = 'Your usename needs to be email pattern.'
        else:
            success = 'true'
            detail = 'Log in success'

        if success == 'true':
            if data['listing_type'] == 'เช่า' and int(data['price_baht']) > 700000:
                success = 'false'
                detail = 'ประเภททรัพย์ของท่านเป็นประเภทเช่า ซึงเว็บไซต์ไม่รองรับราคาเช่าที่เกินกว่า 700,000 บาท' #The list is rental type so the price can not be over than 700,000 bath.
                driver.close()
                driver.quit()
            else:
                success = 'true'
            
            if success == 'true':
                try:
                    time.sleep(3)
                    #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'ประกาศทั้งหมด')))
                    driver.get('https://www.dotproperty.co.th/my-dashboard/properties')
                    time.sleep(5)

                    try:
                        ActionChains(driver).move_by_offset(10 , 10).click().perform()
                    except:
                        pass
                    
                    try:
                        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'upload-btn'))).click()
                    except:
                        pass
                    try:
                        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[3]/div/div[2]/div[1]/div[2]/button"))).click()
                    except Exception as e:
                        success = 'false'
                        detail = str(e)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    if soup.find('button', {'data-tooltip': 'คุณได้ออนไลน์ประกาศครบตามจำนวนที่กำหนดแล้ว'}):
                        print('false')
                        success = 'false'
                        detail = 'คุณได้ออนไลน์ประกาศครบตามจำนวนที่กำหนดแล้ว'
                        post_url = ''
                        post_id = ''
                    else: 
                        print('true')
                        success = 'true'

                    if success == 'true':
                        try:
                            try:
                                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'photos_container'))).click()
                            except:
                                route_link = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'router-link-active')))
                                route_link[0].click()
                                time.sleep(2)
                                route_link[1].click()
                                time.sleep(2)
                                try:
                                    button = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'button')))
                                    button[2].click()
                                except:
                                    button = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'button')))
                                    button[1].click()
                                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'photos_container'))).click()
                        except:
                            return {
                                "success": "false",
                                "usage_time": str(datetime.datetime.utcnow() - time_start),
                                "start_time": str(time_start),
                                "end_time": str(datetime.datetime.utcnow()),
                                "ds_id": data['ds_id'],
                                "post_url": '',
                                "post_id": '',
                                "account_type": None,
                                "detail": 'กรูณายืนยัน เบอร์มือถือ และอีเมลล์ ในบัญชีของคุณ',
                                "websitename": "dotproperty"
                            }   
                        cur_url = driver.current_url
                        #Image process
                        pic_post = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'photos')))
                        if len(data['post_images'])<15:
                            total = len(data['post_images'])
                        image = ''
                        count=1
                        for img in data['post_images'][:total]:
                            image = Image.open(img)
                            new_image = image.resize((600, 400))
                            new_image.save(img)
                        all_images = ""
                        for count, pic in enumerate(data['post_images']):
                            if count < len(data['post_images'])-1:
                                all_images += os.path.abspath(pic) + '\n'
                            else:
                                all_images += os.path.abspath(pic)
                        pic_post.send_keys(all_images)
                        #Information process
                        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'infomation'))).click()
                        #Select type
                        if data['listing_type'] != 'ขาย':
                            elem = driver.find_element_by_xpath('//div[@class="ui item menu three"]')
                            spans = elem.find_elements_by_tag_name('span')
                            spans[1].click()
                            elem = driver.find_element_by_name("rentPrice")
                            elem.clear()
                            elem.send_keys(data['price_baht'], Keys.ARROW_DOWN)
                        else:
                            elem = driver.find_element_by_name("salePrice")
                            elem.clear()
                            elem.send_keys(data['price_baht'], Keys.ARROW_DOWN)

                        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'propertyType'))).click()
                        property_tp = {
                            "1": "คอนโด",
                            "2": "บ้านเดี่ยว",
                            "3": "ทาวน์เฮ้าส์",
                            "4": "ทาวน์เฮ้าส์",
                            "5": "เชิงพาณิชย์",
                            "6": "ที่ดิน",
                            "7": "อพาร์ทเม้นท์",
                            "8": "เชิงพาณิชย์",
                            "9": "เชิงพาณิชย์",
                            "10": "เชิงพาณิชย์",
                            "25": "เชิงพาณิชย์"
                        }
                        p_type = property_tp[str(data['property_type'])]
                        options = driver.find_element_by_id('my_propertyType')
                        items = options.find_elements_by_class_name('item')
                        for item in items:
                            if item.text == p_type:
                                item.click()
                                break

                        if data['land_size_rai'] is None:
                            data['land_size_rai'] = ''
                        if data['land_size_ngan'] is None:
                            data['land_size_ngan'] = ''
                        if data['land_size_wa'] is None:
                            data['land_size_wa'] = ''
                        if data['bed_room'] is None:
                            data['bed_room'] = ''
                        if data['bath_room'] is None:
                            data['bath_room'] = ''
                        if data['floor_total'] is None:
                            data['floor_total'] = ''
                        if 'floorarea_sqm' not in data or data['floorarea_sqm'] is None or data['floorarea_sqm'] == '':
                            if 'floor_area' not in data or data['floor_area'] is None:
                                data['floor_area'] = ''
                            data['floorarea_sqm'] = data['floor_area']
                        data['land_size_rai'] = str(data['land_size_rai'])
                        data['land_size_ngan'] = str(data['land_size_ngan'])
                        data['land_size_wa'] = str(data['land_size_wa'])
                        data['floorarea_sqm'] = str(data['floorarea_sqm'])
                        if p_type == 'คอนโด':
                            elem = driver.find_element_by_name("bedroom")
                            elem.clear()
                            elem.send_keys(data['bed_room'], Keys.ARROW_DOWN)
                            elem = driver.find_element_by_name("bathroom")
                            elem.clear()
                            elem.send_keys(data['bath_room'], Keys.ARROW_DOWN)
                            elem = driver.find_element_by_name("floor")
                            elem.clear()
                            elem.send_keys(data['floor_level'], Keys.ARROW_DOWN)
                            elem = driver.find_element_by_name("usableArea")
                            elem.clear()
                            elem.send_keys(data['floorarea_sqm'], Keys.ARROW_DOWN)
                        elif p_type == 'บ้านเดี่ยว' or p_type == 'ทาวน์เฮ้าส์':
                            elem = driver.find_element_by_name("bedroom")
                            elem.clear()
                            elem.send_keys(data['bed_room'], Keys.ARROW_DOWN)
                            elem = driver.find_element_by_name("bathroom")
                            elem.clear()
                            elem.send_keys(data['bath_room'], Keys.ARROW_DOWN)
                            elem = driver.find_element_by_name("floor")
                            elem.clear()
                            elem.send_keys(data['floor_total'], Keys.ARROW_DOWN)
                            elem = driver.find_element_by_name("usableArea")
                            elem.clear()
                            elem.send_keys(data['floorarea_sqm'], Keys.ARROW_DOWN)
                            elem = driver.find_element_by_name("rai")
                            elem.clear()
                            elem.send_keys(data['land_size_rai'], Keys.ARROW_DOWN)
                            elem = driver.find_element_by_name("ngan")
                            elem.clear()
                            elem.send_keys(data['land_size_ngan'], Keys.ARROW_DOWN)
                            elem = driver.find_element_by_name("sqw")
                            elem.clear()
                            elem.send_keys(data['land_size_wa'], Keys.ARROW_DOWN)
                        elif p_type == 'อพาร์ทเม้นท์':
                            elem = driver.find_element_by_name("bedroom")
                            elem.clear()
                            elem.send_keys(data['bed_room'], Keys.ARROW_DOWN)
                            elem = driver.find_element_by_name("bathroom")
                            elem.clear()
                            elem.send_keys(data['bath_room'], Keys.ARROW_DOWN)
                            elem = driver.find_element_by_name("floor")
                            elem.clear()
                            elem.send_keys(data['floor_total'], Keys.ARROW_DOWN)
                            elem = driver.find_element_by_name("usableArea")
                            elem.clear()
                            elem.send_keys(data['floorarea_sqm'], Keys.ARROW_DOWN)
                        elif p_type == 'ที่ดิน':
                            elem = driver.find_element_by_name("rai")
                            elem.clear()
                            elem.send_keys(data['land_size_rai'], Keys.ARROW_DOWN)
                            elem = driver.find_element_by_name("ngan")
                            elem.clear()
                            elem.send_keys(data['land_size_ngan'], Keys.ARROW_DOWN)
                            elem = driver.find_element_by_name("sqw")
                            elem.clear()
                            elem.send_keys(data['land_size_wa'], Keys.ARROW_DOWN)
                        else:
                            elem = driver.find_element_by_name("bedroom")
                            elem.clear()
                            elem.send_keys(data['bed_room'], Keys.ARROW_DOWN)
                            elem = driver.find_element_by_name("bathroom")
                            elem.clear()
                            elem.send_keys(data['bath_room'], Keys.ARROW_DOWN)
                            elem = driver.find_element_by_name("floor")
                            elem.clear()
                            elem.send_keys(data['floor_total'], Keys.ARROW_DOWN)
                            elem = driver.find_element_by_name("usableArea")
                            elem.clear()
                            elem.send_keys(data['floorarea_sqm'], Keys.ARROW_DOWN)
                            elem = driver.find_element_by_name("rai")
                            elem.clear()
                            elem.send_keys(data['land_size_rai'], Keys.ARROW_DOWN)
                            elem = driver.find_element_by_name("ngan")
                            elem.clear()
                            elem.send_keys(data['land_size_ngan'], Keys.ARROW_DOWN)
                            elem = driver.find_element_by_name("sqw")
                            elem.clear()
                            elem.send_keys(data['land_size_wa'], Keys.ARROW_DOWN)

                        new_proj = True
                        if p_type != 'ที่ดิน':
                            #print('in project')
                            if 'web_project_name' not in data or data['web_project_name'] is None or data['web_project_name'] == "":
                                if 'project_name' in data and data['project_name'] is not None:
                                    data['web_project_name'] = data['project_name']
                                else:
                                    data['web_project_name'] = ''
                            
                            if data['web_project_name'] != '':
                                #print('click')
                                options = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'my_project')))
                                actions = ActionChains(driver)
                                actions.move_to_element(options).click().perform()
                                #print('clicked')
                                inp = options.find_elements_by_xpath('//input[@class="search"]')[2]
                                if data['listing_type'] == 'ขาย':
                                    #print('sell')
                                    inp = options.find_elements_by_xpath('//input[@class="search"]')[1]
                                time.sleep(2)
                                inp.send_keys(str(data['web_project_name'].split('(')[0].strip()))
                                time.sleep(2)
                                #inp.send_keys(Keys.TAB)
                                #inp.send_keys(Keys.ENTER)
                                #inp.send_keys(Keys.ARROW_DOWN)
                                #print('typed')
                                options = options.find_elements_by_class_name('item')
                                for opt in options:
                                    #print(opt.text)
                                    if str(opt.text).replace(' ','').find(data['web_project_name'].replace(' ', ''))!=-1:
                                        opt.click()
                                        #print(str(opt.text))
                                        #print(pro)
                                        new_proj = False
                                        break
                        #print('project name done')
                        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                        if new_proj == True:
                            options = driver.find_element_by_id('my_province')
                            time.sleep(2)
                            options.click()
                            time.sleep(5)
                            #print('clicked')
                            flag = False
                            options = options.find_elements_by_class_name('item')
                            for opt in options:
                                #print(opt.text)
                                if str(opt.text).replace(' ', '').find(data['addr_province']) != -1 or data['addr_province'].find(str(opt.text).replace(' ', ''))!=-1:
                                    opt.click()
                                    flag = True
                                    break
                            if flag == False:
                                for opt in options:
                                    #print(opt.text)
                                    opt.click()
                                    break
                            #print('province done')

                            options = driver.find_element_by_id('my_city')
                            time.sleep(2)
                            options.click()
                            time.sleep(5)
                            #print('clicked')
                            flag = False
                            options = options.find_elements_by_class_name('item')
                            for opt in options:
                                #print(opt.text)
                                if str(opt.text).replace(' ', '').find(data['addr_district']) != -1 or data['addr_district'].find(str(opt.text).replace(' ', ''))!=-1:
                                    opt.click()
                                    flag = True
                                    break
                            if flag == False:
                                for opt in options:
                                    #print(opt.text)
                                    opt.click()
                                    break
                            #print('district done')
                            #print('4')
                            options = driver.find_element_by_id('my_area')
                            time.sleep(2)
                            options.click()
                            time.sleep(5)
                            #print('clicked')
                            flag = False
                            options = options.find_elements_by_class_name('item')
                            for opt in options:
                                #print(opt.text)
                                if str(opt.text).replace(' ', '').find(data['addr_sub_district']) != -1 or data['addr_sub_district'].find(str(opt.text).replace(' ', ''))!=-1:
                                    opt.click()
                                    flag = True
                                    break
                            if flag == False:
                                for opt in options:
                                    #print(opt.text)
                                    opt.click()
                                    break
                            #print('sub district done')
                            driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                            driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)

                            #my_showMap
                            options = driver.find_element_by_id('my_showMap').find_element_by_class_name('on-off')
                            time.sleep(2)
                            options.click()
                            time.sleep(5)
                            #print('5')
                            #print('clicked')

                            options = driver.find_element_by_id('my_geoType').find_element_by_class_name('on-off')
                            options.click()
                            #print('6')
                            #print('clicked')

                            elem = driver.find_element_by_name("latitude")
                            elem.clear()
                            elem.send_keys(str(data['geo_latitude']), Keys.ARROW_DOWN)
                            elem = driver.find_element_by_name("longitude")
                            elem.clear()
                            elem.send_keys(str(data['geo_longitude']), Keys.ARROW_DOWN)
                            #print('done map')
                            #print('6')

                        #Descriptions phrase
                        elem = driver.find_element_by_name("title_th")
                        elem.clear()
                        if data['post_title_en'] is not None and data['post_title_en']!='' and data['post_description_en'] is not None and data['post_description_en'] != '':
                            print('There is english description')
                            elem.send_keys(str(data['post_title_th'])[:120], Keys.TAB, str(data['post_description_th']).replace('\r',''), Keys.TAB, str(data['post_title_en'])[:120], Keys.TAB, str(data['post_description_en']).replace('\r', ''))
                        else:    
                            elem.send_keys(str(data['post_title_th'])[:120], Keys.TAB, str(data['post_description_th']).replace('\r',''))
                        """ elem = driver.find_element_by_xpath('//div[@id="my_description_th"]')
                        time.sleep(2)
                        elem.click()
                        time.sleep(5)
                        elem = driver.find_element_by_name("description_th")
                        elem.clear()
                        data['post_description_th'] = str(data['post_description_th']).replace('\r','')
                        for i in range(10,0,-1):
                            if i == 1:
                                data['post_description_th'] = str(data['post_description_th']).replace('\n' * i, '<br>')
                            else:
                                data['post_description_th'] = str(data['post_description_th']).replace('\n' * i,
                                                                                                        '<br>' + '<p><br></p>' * (
                                                                                                                    i - 1))

                        #print(data['post_description_th'])
                        elem.send_keys(data['post_description_th'], Keys.ARROW_DOWN)
                        if 'post_title_en' in data and data['post_title_en'] is not None and data['post_title_en']!='':
                            elem = driver.find_element_by_name("title_en")
                            elem.clear()
                            elem.send_keys(str(data['post_title_en'])[:120], Keys.ARROW_DOWN)
                        if 'post_description_en' in data and data['post_description_en'] is not None and data['post_description_en'] != '':
                            elem = driver.find_element_by_name("description_en")
                            elem.clear()
                            data['post_description_en'] = str(data['post_description_en']).replace('\r', '')
                            for i in range(10, 0, -1):
                                if i == 1:
                                    data['post_description_en'] = str(data['post_description_en']).replace('\n' * i, '<br>')
                                else:
                                    data['post_description_en'] = str(data['post_description_en']).replace('\n' * i,
                                                                                                            '<br>' + '<p><br></p>' * (
                                                                                                                        i - 1))
                            elem.send_keys(data['post_description_en'], Keys.ARROW_DOWN) """

                        #print('going to save')
                        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)

                        time.sleep(2)
                        btn = driver.find_element_by_xpath('//button[@class="ui green button"]')
                        time.sleep(1)
                        btn.click()
                        try:
                            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'vue-notification-wrapper')))
                            time.sleep(3)
                        except:
                            time_end = datetime.datetime.utcnow()
                            time_usage = time_end - time_start
                            return {
                                "success": 'false',
                                "usage_time": str(time_usage),
                                "start_time": str(time_start),
                                "end_time": str(time_end),
                                "ds_id": data['ds_id'],
                                "post_url": '',
                                "post_id": '',
                                "account_type": None,
                                "detail": 'เว็บไซต์เกิดข้อผิดพลาด และไม่สามารถบันทึกรายละเอียดทั้งหมดของทรัพย์ของท่านได้ ระบบของเราจะดำเนินการโพสต์ประกาศให้ใหม่อีกครั้ง',
                                "websitename": "dotproperty"
                            }
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'tgl'))).click()
                        time.sleep(3)
                        txt = str(driver.current_url)
                        post_id = ''
                        ind = txt.find('properties')+11
                        while txt[ind]!='/':
                            post_id+=txt[ind]
                            ind+=1
                        url = 'https://www.dotproperty.co.th/my-dashboard/properties'
                        driver.get(url)
                        time.sleep(10)
                        #print('7')

                        posts = driver.find_element_by_xpath('//table[@class="ui celled table unstackable"]').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
                        #print('here1')
                        for post in posts:
                            tds = post.find_elements_by_tag_name('td')
                            #print('here2')

                            #print('here3')
                            if str(tds[2].text)==post_id:
                                #print('here4')
                                if len((tds[8].find_elements_by_tag_name('a')))>2:
                                    post_url = str((tds[8].find_elements_by_tag_name('a'))[1].get_attribute('href'))
                                    break
                        detail = 'Post created'

                except Exception as e:
                    success = 'false'
                    detail = 'Can not create post ' + str(e)
                    post_url = ''
                    post_id = ''
        
                finally:
                    driver.close()
                    driver.quit()
            else:
                post_url = ''
                post_id = ''
        else:
            post_url = ''
            post_id = ''
            driver.quit()

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": data['ds_id'],
            "post_url": post_url,
            "post_id": post_id,
            "account_type": None,
            "detail": detail,
            "websitename": "dotproperty"
        }

    def boost_post(self, data):
        start_time = datetime.datetime.utcnow()
        """log_id = str(data['log_id'])
        post_id = str(data['post_id'])

        path = './static/chromedriver'
        options = Options()
        #options.add_argument('--headless')
        options.add_argument('--disable-notifications')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-infobars')
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1024,768")
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(executable_path=path, options=options)

        driver.get('https://www.dotproperty.co.th/login')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'email'))).send_keys(data['user'])
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'password'))).send_keys(data['pass'])
        login_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'loginPopupBtn')))
        actions = ActionChains(driver)
        actions.move_to_element(login_btn).click().perform()
        time.sleep(3.5)
        txt = str(driver.page_source)
        if txt.find('อีเมลและ/หรือรหัสผ่านของคุณไม่ตรงกัน โปรดลองใหม่อีกครั้ง')!=-1:
            success = 'false'
            detail = 'Invalid credentials'
        elif txt.find('email ต้องเป็นอีเมลแอดเดรสที่มีอยู่จริงเท่านั้น') != -1:
            success = 'false'
            detail = 'Your usename needs to be email pattern.'
        else:
            success = 'true'
            detail = 'Log in success'


        if success == 'true':
            try:
                time.sleep(3)
                url = 'https://www.dotproperty.co.th/my-dashboard/properties'
                driver.get(url)
                # block create-btn
                time.sleep(2)

                valid_ids = []
                while True:
                    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
                    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
                    time.sleep(2)
                    posts = driver.find_element_by_xpath(
                        '//table[@class="ui celled table unstackable"]').find_element_by_tag_name(
                        'tbody').find_elements_by_tag_name('tr')
                    #print('here1')
                    for post in posts:
                        tds = post.find_elements_by_tag_name('td')
                        #print('here2')
                        if str(tds[2].text) in valid_ids:
                            raise Exception
                        valid_ids.append(str(tds[2].text))
                        #print('here3')
                    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)

                    btn = driver.find_elements_by_xpath('//div[@class="item btn"]')
                    if len(btn)>=2:
                        btn = btn[1]
                    else:
                        btn = btn[0]
                    time.sleep(2)
                    btn.click()
                    time.sleep(5)
                    #print('done')
            except:
                #print(valid_ids)
                if post_id in valid_ids:
                    detail = 'post edited and saved'
                else:
                    detail = 'Post not found'
            finally:
                driver.close()
                driver.quit()
        else:
            driver.close()
            driver.quit()"""

        end_time = datetime.datetime.utcnow()
        result = {
            "success": "true",
            "usage_time": str(end_time - start_time),
            "start_time": str(start_time),
            "end_time": str(end_time),
            "detail": 'No option boost in this site',
            'ds_id': data['ds_id'],
            "log_id": str(data['log_id']),
            "post_id": str(data['post_id']),
            'websitename': 'dotproperty',
            "post_view": ""
        }
        # https://ilovecondo.net/new-post/topicid/910653/trk/78
        return result

    def delete_post(self, data):
        start_time = datetime.datetime.utcnow()
        log_id = str(data['log_id'])
        post_id = str(data['post_id'])
        
        path = './static/chromedriver'
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-notifications')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-infobars')
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1024,768")
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(executable_path=path, options=options)

        driver.get('https://www.dotproperty.co.th/login')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'email'))).send_keys(data['user'])
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'password'))).send_keys(data['pass'])
        login_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'loginPopupBtn')))
        actions = ActionChains(driver)
        actions.move_to_element(login_btn).click().perform()
        time.sleep(3.5)
        txt = str(driver.page_source)
        if txt.find('อีเมลและ/หรือรหัสผ่านของคุณไม่ตรงกัน โปรดลองใหม่อีกครั้ง')!=-1:
            success = 'false'
            detail = 'Invalid credentials'
        elif txt.find('email ต้องเป็นอีเมลแอดเดรสที่มีอยู่จริงเท่านั้น') != -1:
            success = 'false'
            detail = 'Your usename needs to be email pattern.'
        else:
            success = 'true'
            detail = 'Log in success'

        if success == 'true':
            #try:
            time.sleep(3)
            url = 'https://www.dotproperty.co.th/my-dashboard/properties'
            driver.get(url)
            time.sleep(5)

            try:
                ActionChains(driver).move_by_offset(10 , 10).click().perform()
            except:
                pass

            # block create-btn
            inputs = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'input')))
            for search in inputs:
                if search.get_attribute('placeholder') == 'ค้นหาโดย ID ,เลขอ้างอิง':
                    search.send_keys(data['post_id'])
            time.sleep(5)
            table = driver.find_element_by_tag_name('tbody')
            items = table.find_elements_by_tag_name('tr')
            if len(items) == 0:
                success = 'false'
                detail = 'Post not found'
            else:
                for item in items:
                    ref = item.find_elements_by_tag_name('td')
                    if data['post_id'] == ref[2].text:
                        btn = ref[8].find_elements_by_tag_name('i')
                        btn[len(btn)-1].click()
                        success = 'true'
                        detail = 'Delete post success'

            """ except:
                pass
            finally:
                driver.close()
                driver.quit() """
        
        time.sleep(10)
        driver.close()
        driver.quit()

        end_time = datetime.datetime.utcnow()
        result = {
            "success": "true",
            "usage_time": str(end_time - start_time),
            "start_time": str(start_time),
            "end_time": str(end_time),
            "detail": detail,
            'ds_id': data['ds_id'],
            "log_id": log_id,
            "post_id": post_id,
            'websitename': 'dotproperty'
        }
        # https://ilovecondo.net/new-post/topicid/910653/trk/78
        return result


    def edit_post(self, data):
        start_time = datetime.datetime.utcnow()
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        }
        success = ''
        detail = ''
        post_id = data['post_id']
        post_url = ''
        if 'post_images' in data and len(data['post_images']) > 0:
            pass
        else:
            data['post_images'] = ['./imgtmp/default/white.jpg']

        path = './static/chromedriver'
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-notifications')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-infobars')
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(executable_path=path, options=options)

        driver.get('https://www.dotproperty.co.th/login')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'email'))).send_keys(data['user'])
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'password'))).send_keys(data['pass'])
        login_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'loginPopupBtn')))
        actions = ActionChains(driver)
        actions.move_to_element(login_btn).click().perform()
        time.sleep(3.5)
        txt = str(driver.page_source)
        if txt.find('อีเมลและ/หรือรหัสผ่านของคุณไม่ตรงกัน โปรดลองใหม่อีกครั้ง')!=-1:
            success = 'false'
            detail = 'Invalid credentials'
        elif txt.find('email ต้องเป็นอีเมลแอดเดรสที่มีอยู่จริงเท่านั้น') != -1:
            success = 'false'
            detail = 'Your usename needs to be email pattern.'
        else:
            success = 'true'
            detail = 'Log in success'

        if success == 'true':
            try:
                time.sleep(3)
                url = 'https://www.dotproperty.co.th/my-dashboard/properties/' + data['post_id'] + '/edit'
                driver.get(url)
                #Image
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'photos_container'))).click()
                driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
                imgs = driver.find_elements_by_xpath('//div[@class="grid-item"]')
                for img in imgs:
                    btn = driver.find_elements_by_xpath('//div[@class="grid-item"]')[0]
                    time.sleep(1)
                    #print('here')
                    action = ActionChains(driver)
                    action.move_to_element(btn).perform()
                    #print('there')
                    time.sleep(1)
                    del_btn = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//i[@class="fa fa-trash"]')))
                    del_btn[1].click()
                    """ btn = driver.find_elements_by_xpath('//i[@class="fa fa-trash"]')[1]
                    btn.click() """
                    time.sleep(1.5)
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//button[@class="swal-button swal-button--confirm"]'))).click()
                #Image process
                pic_post = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'photos')))
                if len(data['post_images'])<15:
                    total = len(data['post_images'])
                image = ''
                count=1
                for img in data['post_images'][:total]:
                    image = Image.open(img)
                    new_image = image.resize((600, 400))
                    new_image.save(img)
                all_images = ""
                for count, pic in enumerate(data['post_images']):
                    if count < len(data['post_images'])-1:
                        all_images += os.path.abspath(pic) + '\n'
                    else:
                        all_images += os.path.abspath(pic)
                pic_post.send_keys(all_images)
                #Information
                elem = driver.find_element_by_xpath('//div[@id="infomation"]').click()
                time.sleep(5)

                if data['listing_type'] != 'ขาย':
                    elem = driver.find_element_by_xpath('//div[@class="ui item menu three"]')
                    spans = elem.find_elements_by_tag_name('span')
                    spans[1].click()
                    elem = driver.find_element_by_name("rentPrice")
                    elem.clear()
                    elem.send_keys(data['price_baht'], Keys.ARROW_DOWN)
                else:
                    elem = driver.find_element_by_name("salePrice")
                    elem.clear()
                    elem.send_keys(data['price_baht'], Keys.ARROW_DOWN)
                #print('listing type and price done')
                driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                #propertyType
                p_type = ''
                property_tp = {
                    "1": "คอนโด",
                    "2": "บ้านเดี่ยว",
                    "3": "ทาวน์เฮ้าส์",
                    "4": "ทาวน์เฮ้าส์",
                    "5": "เชิงพาณิชย์",
                    "6": "ที่ดิน",
                    "7": "อพาร์ทเม้นท์",
                    "8": "เชิงพาณิชย์",
                    "9": "เชิงพาณิชย์",
                    "10": "เชิงพาณิชย์",
                    "25": "เชิงพาณิชย์"
                }
                p_type = property_tp[str(data['property_type'])]
                options = driver.find_element_by_id('my_propertyType')
                items = options.find_elements_by_class_name('item')
                for item in items:
                    if item.text == p_type:
                        item.click()
                        break

                #print('property type done')
                if data['land_size_rai'] is None:
                    data['land_size_rai'] = ''
                if data['land_size_ngan'] is None:
                    data['land_size_ngan'] = ''
                if data['land_size_wa'] is None:
                    data['land_size_wa'] = ''
                if 'floorarea_sqm' not in data or data['floorarea_sqm'] is None or data['floorarea_sqm'] == '':
                    data['floorarea_sqm'] = data['floor_area']
                if p_type == 'คอนโด':
                    elem = driver.find_element_by_name("bedroom")
                    elem.clear()
                    elem.send_keys(data['bed_room'], Keys.ARROW_DOWN)
                    elem = driver.find_element_by_name("bathroom")
                    elem.clear()
                    elem.send_keys(data['bath_room'], Keys.ARROW_DOWN)
                    elem = driver.find_element_by_name("floor")
                    elem.clear()
                    elem.send_keys(data['floor_level'], Keys.ARROW_DOWN)
                    elem = driver.find_element_by_name("usableArea")
                    elem.clear()
                    elem.send_keys(data['floorarea_sqm'], Keys.ARROW_DOWN)
                elif p_type == 'บ้านเดี่ยว' or p_type == 'ทาวน์เฮ้าส์':
                    #print('in')
                    elem = driver.find_element_by_name("bedroom")
                    elem.clear()
                    elem.send_keys(str(data['bed_room']), Keys.ARROW_DOWN)
                    elem = driver.find_element_by_name("bathroom")
                    elem.clear()
                    elem.send_keys(str(data['bath_room']), Keys.ARROW_DOWN)
                    elem = driver.find_element_by_name("floor")
                    elem.clear()
                    elem.send_keys(str(data['floor_total']), Keys.ARROW_DOWN)
                    #print('area')
                    elem = driver.find_element_by_name("usableArea")
                    elem.clear()
                    elem.send_keys(str(data['floorarea_sqm']), Keys.ARROW_DOWN)
                    #print('mid')
                    #print('here1',data['land_size_rai'])
                    elem = driver.find_element_by_name("rai")
                    elem.clear()
                    elem.send_keys(data['land_size_rai'], Keys.ARROW_DOWN)
                    #print('here2',data['land_size_ngan'])
                    elem = driver.find_element_by_name("ngan")
                    elem.clear()
                    elem.send_keys(data['land_size_ngan'], Keys.ARROW_DOWN)
                    #print('here3',data['land_size_wa'])
                    elem = driver.find_element_by_name("sqw")
                    elem.clear()
                    elem.send_keys(data['land_size_wa'], Keys.ARROW_DOWN)
                    #print('here4')
                elif p_type == 'อพาร์ทเม้นท์':
                    elem = driver.find_element_by_name("bedroom")
                    elem.clear()
                    elem.send_keys(data['bed_room'], Keys.ARROW_DOWN)
                    elem = driver.find_element_by_name("bathroom")
                    elem.clear()
                    elem.send_keys(data['bath_room'], Keys.ARROW_DOWN)
                    elem = driver.find_element_by_name("floor")
                    elem.clear()
                    elem.send_keys(data['floor_total'], Keys.ARROW_DOWN)
                    elem = driver.find_element_by_name("usableArea")
                    elem.clear()
                    elem.send_keys(data['floorarea_sqm'], Keys.ARROW_DOWN)
                elif p_type == 'ที่ดิน':
                    elem = driver.find_element_by_name("rai")
                    elem.clear()
                    elem.send_keys(data['land_size_rai'], Keys.ARROW_DOWN)
                    elem = driver.find_element_by_name("ngan")
                    elem.clear()
                    elem.send_keys(data['land_size_ngan'], Keys.ARROW_DOWN)
                    elem = driver.find_element_by_name("sqw")
                    elem.clear()
                    elem.send_keys(data['land_size_wa'], Keys.ARROW_DOWN)
                else:
                    elem = driver.find_element_by_name("bedroom")
                    elem.clear()
                    elem.send_keys(data['bed_room'], Keys.ARROW_DOWN)
                    elem = driver.find_element_by_name("bathroom")
                    elem.clear()
                    elem.send_keys(data['bath_room'], Keys.ARROW_DOWN)
                    elem = driver.find_element_by_name("floor")
                    elem.clear()
                    elem.send_keys(data['floor_total'], Keys.ARROW_DOWN)
                    elem = driver.find_element_by_name("usableArea")
                    elem.clear()
                    elem.send_keys(data['floorarea_sqm'], Keys.ARROW_DOWN)
                    elem = driver.find_element_by_name("rai")
                    elem.clear()
                    elem.send_keys(data['land_size_rai'], Keys.ARROW_DOWN)
                    elem = driver.find_element_by_name("ngan")
                    elem.clear()
                    elem.send_keys(data['land_size_ngan'], Keys.ARROW_DOWN)
                    elem = driver.find_element_by_name("sqw")
                    elem.clear()
                    elem.send_keys(data['land_size_wa'], Keys.ARROW_DOWN)

                new_proj = True
                if p_type != 'ที่ดิน':
                    #print('in project')
                    if 'web_project_name' not in data or data['web_project_name'] is None or data['web_project_name'] == "":
                        if 'project_name' in data and data['project_name'] is not None:
                            data['web_project_name'] = data['project_name']
                        else:
                            data['web_project_name'] = ''
                    
                    #print(pro)
                    if data['web_project_name'] != '':
                        #print('click')
                        options = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'my_project')))
                        actions = ActionChains(driver)
                        actions.move_to_element(options).click().perform()
                        #print('clicked')
                        inp = options.find_elements_by_xpath('//input[@class="search"]')[2]
                        if data['listing_type'] == 'ขาย':
                            #print('sell')
                            inp = options.find_elements_by_xpath('//input[@class="search"]')[1]
                        time.sleep(2)
                        inp.send_keys(str(data['web_project_name']))
                        time.sleep(2)
                        #inp.send_keys(Keys.TAB)
                        inp.send_keys(Keys.ENTER)
                        inp.send_keys(Keys.ARROW_DOWN)
                        #print('typed')
                        options = options.find_elements_by_class_name('item')
                        for opt in options:
                            #print(opt.text)
                            if str(opt.text).replace(' ','').find(data['web_project_name'])!=-1:
                                opt.click()
                                #print(str(opt.text))
                                #print(pro)
                                new_proj = False
                                break
                #print('project name done')
                #driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)

                if new_proj == True:
                    options = driver.find_element_by_id('my_province')
                    time.sleep(2)
                    options.click()
                    time.sleep(5)
                    #print('clicked')
                    flag = False
                    options = options.find_elements_by_class_name('item')
                    for opt in options:
                        #print(opt.text)
                        if str(opt.text).replace(' ', '').find(data['addr_province']) != -1:
                            opt.click()
                            flag = True
                            break
                    if flag == False:
                        for opt in options:
                            #print(opt.text)
                            opt.click()
                            break
                    #print('province done')

                    options = driver.find_element_by_id('my_city')
                    time.sleep(2)
                    options.click()
                    time.sleep(5)
                    #print('clicked')
                    flag = False
                    options = options.find_elements_by_class_name('item')
                    for opt in options:
                        #print(opt.text)
                        if str(opt.text).replace(' ', '').find(data['addr_district']) != -1:
                            opt.click()
                            flag = True
                            break
                    if flag == False:
                        for opt in options:
                            #print(opt.text)
                            opt.click()
                            break
                    #print('district done')

                    options = driver.find_element_by_id('my_area')
                    time.sleep(2)
                    options.click()
                    time.sleep(5)
                    #print('clicked')
                    flag = False
                    options = options.find_elements_by_class_name('item')
                    for opt in options:
                        #print(opt.text)
                        if str(opt.text).replace(' ', '').find(data['addr_sub_district']) != -1:
                            opt.click()
                            flag = True
                            break
                    if flag == False:
                        for opt in options:
                            #print(opt.text)
                            opt.click()
                            break
                    #print('sub district done')
                    #driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                    #driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)

                    try:
                        options = driver.find_element_by_id('my_geoType').find_element_by_class_name('on-off')
                        options.click()
                        #print('clicked')
                    except:
                        options = driver.find_element_by_id('my_showMap').find_element_by_class_name('on-off')
                        time.sleep(2)
                        options.click()
                        time.sleep(5)
                        #print('clicked')
                        options = driver.find_element_by_id('my_geoType').find_element_by_class_name('on-off')
                        options.click()
                        #print('clicked')

                    elem = driver.find_element_by_name("latitude")
                    elem.clear()
                    elem.send_keys(data['geo_latitude'], Keys.ARROW_DOWN)
                    elem = driver.find_element_by_name("longitude")
                    elem.clear()
                    elem.send_keys(data['geo_longitude'], Keys.ARROW_DOWN)
                    #print('done map')

                elem = driver.find_element_by_name("title_th")
                elem.clear()
                elem.send_keys(str(data['post_title_th'])[:120], Keys.ARROW_DOWN)
                elem = driver.find_element_by_xpath('//div[@id="my_description_th"]')
                time.sleep(2)
                elem.click()
                time.sleep(5)
                elem = driver.find_element_by_name("description_th")
                elem.clear()
                data['post_description_th'] = str(data['post_description_th']).replace('\r', '')
                for i in range(10, 0, -1):

                    if i == 1:
                        data['post_description_th'] = str(data['post_description_th']).replace('\n' * i, '<br>')
                    else:
                        data['post_description_th'] = str(data['post_description_th']).replace('\n' * i,
                                                                                                '<br>' + '<p><br></p>' * (
                                                                                                            i - 1))

                ##print(data['post_description_th'])
                elem.send_keys(data['post_description_th'], Keys.ARROW_DOWN)
                if 'post_title_en' in data and data['post_title_en'] is not None and data['post_title_en'] != '':
                    elem = driver.find_element_by_name("title_en")
                    elem.clear()
                    elem.send_keys(str(data['post_title_en'])[:120], Keys.ARROW_DOWN)
                if 'post_description_en' in data and data['post_description_en'] is not None and data[
                    'post_description_en'] != '':
                    elem = driver.find_element_by_name("description_en")
                    elem.clear()
                    data['post_description_en'] = str(data['post_description_en']).replace('\r', '')
                    for i in range(10, 0, -1):

                        if i == 1:
                            data['post_description_en'] = str(data['post_description_en']).replace('\n' * i, '<br>')
                        else:
                            data['post_description_en'] = str(data['post_description_en']).replace('\n' * i,
                                                                                                    '<br>' + '<p><br></p>' * (
                                                                                                            i - 1))

                    elem.send_keys(data['post_description_en'], Keys.ARROW_DOWN)

                #print('going to save')
                driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)

                btn = driver.find_element_by_xpath('//button[@class="ui green button"]')
                time.sleep(1.5)
                btn.click()
                time.sleep(8)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'tgl'))).click()
                time.sleep(2)
                txt = str(driver.current_url)
                post_id = ''
                ind = txt.find('properties')+11
                while txt[ind]!='/':
                    post_id+=txt[ind]
                    ind+=1
                url = 'https://www.dotproperty.co.th/my-dashboard/properties'
                driver.get(url)
                time.sleep(5)
                #print('7')

                posts = driver.find_element_by_xpath('//table[@class="ui celled table unstackable"]').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
                #print('here1')
                for post in posts:
                    tds = post.find_elements_by_tag_name('td')
                    #print('here2')

                    #print('here3')
                    if str(tds[2].text)==post_id:
                        #print('here4')
                        if len((tds[8].find_elements_by_tag_name('a')))>2:
                            post_url = str((tds[8].find_elements_by_tag_name('a'))[1].get_attribute('href'))
                            break
                detail = 'Post Edited'
                
            except Exception as e:
                #print(e)
                detail = 'Post cannot be edited' + str(e)
                end_time = datetime.datetime.utcnow()
                result = {'success': 'false',
                            'usage_time': str(end_time - start_time),
                            'start_time': str(start_time),
                            'end_time': str(end_time),
                            'post_url': post_url,
                            'post_id': post_id,
                            'account_type': 'null',
                            'ds_id': data['ds_id'],
                            'detail': detail,
                            'websitename': 'dotproperty'}

            finally:
                driver.close()
                driver.quit()

        else:
            post_url = ''
            driver.quit()

        end_time = datetime.datetime.utcnow()
        result = {'success': success,
                  'usage_time': str(end_time - start_time),
                  'start_time': str(start_time),
                  'end_time': str(end_time),
                  'post_url': post_url,
                  'post_id': data['post_id'],
                  'account_type': 'null',
                  'ds_id': data['ds_id'],
                  'log_id':data['log_id'],
                  'detail': detail,
                  'websitename': 'dotproperty'}
        return result

# https://www.dotproperty.co.th/my-dashboard/properties/4817078/edit

    def search_post(self, postdata):

        time_start = datetime.datetime.utcnow()

        detail = 'Can not search post with title'
        post_found = 'false'

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": "true",
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_found": post_found,
            "post_id": '',
            'post_url': '',
            "post_create_time": '',
            "post_modify_time": '',
            "post_view": '',
            'websitename': 'dotproperty'
        }



    def print_debug(self, msg):

        return True

    def print_debug_data(self, data):

        return True
