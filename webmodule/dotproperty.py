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
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
# from PIL import Image

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
        r = httprequestObj.http_get_with_headers('https://www.dotproperty.co.th/login', verify=False)
        data1 = r.text
        soup = BeautifulSoup(data1, self.PARSER)

        frm_token = soup.find("input", {"name": "_token"})['value']
        postdata = {
            '_token': frm_token,
            'email': data['user'],
            'password': data['pass'],
            'refer_type': 'login',
            'remember': 'on'
        }

        url = 'https://www.dotproperty.co.th/ajaxLogin?pv_id='+str(soup.find('body')['data-pvid'])
        #print(url)

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        }
        req = httprequestObj.http_post(url, data=postdata, headers=headers)
        txt = str(req.text)

        if txt.find('true') == -1:
            success = 'false'
            detail = 'Invalid credentials'

        else:
            success = 'true'
            detail = 'Login successful'

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
        start_time = datetime.datetime.utcnow()
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        }
        success = ''
        detail = ''
        post_id = ''
        post_url = ''
        print('-4')
        if 'post_images' in data and len(data['post_images']) > 0:
            pass
        else:
            data['post_images'] = ['./imgtmp/default/white.jpg']
        try:
            options = Options()
            prefs = {"profile.default_content_setting_values.notifications": 2}
            # options.add_experimental_option("prefs", prefs)
            options.headless = True
            #chrome_options.add_argument('headless')
            driver = webdriver.Firefox(options=options)
            print('-3')
            driver.maximize_window()
            print('-2')
            url = 'https://www.dotproperty.co.th/login'
            driver.get(url)
            print('-1')

            #print('blocked')
            element = driver.find_element_by_name("email")
            element.send_keys(data['user'])
            #print('done')
            element = driver.find_element_by_name("password")
            element.send_keys(data['pass'])
            #print('done')
            time.sleep(2)

            submit = driver.find_element_by_id("loginPopupBtn")
            submit.click()
            time.sleep(2)
            txt = str(driver.page_source)
            success = ''
            detail = ''
            print('0')
            if txt.find('อีเมลและ/หรือรหัสผ่านของคุณไม่ตรงกัน โปรดลองใหม่อีกครั้ง')!=-1:
                success = 'false'
                detail = 'Invalid credentials'
            else:
                url = 'https://www.dotproperty.co.th/my-dashboard/properties'
                driver.get(url)
                #block create-btn
                time.sleep(2)
                submit = driver.find_elements_by_tag_name("button")[0]
                submit.click()
                # submit.click()
                # submit.click()
                time.sleep(7)
                #driver.switch_to_window(driver.window_handles[0])
                print('1')

                #driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)

                '''element = driver.find_elements_by_css_selector("button[class='ui basic button edit-btn']")
                #print(element)
                #submit = div.find_element_by_tag_name('button')
                submit = element[3]
                action = ActionChains(driver)
                action.move_to_element(submit)
                action.click().perform()
                action.click().perform()
                action.click().perform()'''
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
                #print(options)
                time.sleep(2)
                options.click()
                time.sleep(5)
                options = options.find_elements_by_class_name('item')
                for opt in options:
                    #print(opt.text)
                    if str(opt.text) == p_type:
                        opt.click()
                        break

                print('2')
                #print('property type done')
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
                    data['web_project_name'] = ''.join(map(str, str(data['web_project_name']).split(' ')))
                    pro = data['web_project_name']
                    '''url = 'https://www.dotproperty.co.th/dashboard-api/dropdown-filter-project?term='+str(data['web_project_name'])[:2]
                    pro = ''
                    req = httprequestObj.http_get(url)
                    if str(req.text) != '[]':
                        projects = []
                        txt = str(req.text)
                        ind = txt.find('text')
                        while ind!=-1:
                            ind+=7
                            proj = ''
                            while txt[ind]!='"':
                                proj+=txt[ind]
                                ind+=1
                            projects.append(proj.replace(' ',''))
                            txt = txt[ind:]
                            ind = txt.find('text')
                        for proj in projects:
                            if proj.find(data['web_project_name'])!=-1:
                                pro = proj
                                break'''
                    print('3')
                    if pro!='':
                        #print('click')
                        options = driver.find_element_by_id('my_project')
                        time.sleep(2)
                        options.click()
                        time.sleep(5)
                        #print('clicked')
                        inp = options.find_elements_by_xpath('//input[@class="search"]')[2]
                        if data['listing_type'] == 'ขาย':
                            #print('sell')
                            inp = options.find_elements_by_xpath('//input[@class="search"]')[1]

                        time.sleep(2)
                        inp.send_keys(str(data['web_project_name'])[:6])
                        time.sleep(2)
                        #inp.send_keys(Keys.TAB)
                        inp.send_keys(Keys.ENTER)
                        inp.send_keys(Keys.ARROW_DOWN)
                        #print('typed')
                        options = options.find_elements_by_class_name('item')
                        for opt in options:
                            #print(opt.text)
                            if str(opt.text).replace(' ','').find(pro)!=-1:
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
                    print('4')
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
                    print('5')
                    #print('clicked')

                    options = driver.find_element_by_id('my_geoType').find_element_by_class_name('on-off')
                    options.click()
                    print('6')
                    #print('clicked')

                    elem = driver.find_element_by_name("latitude")
                    elem.clear()
                    elem.send_keys(str(data['geo_latitude']), Keys.ARROW_DOWN)
                    elem = driver.find_element_by_name("longitude")
                    elem.clear()
                    elem.send_keys(str(data['geo_longitude']), Keys.ARROW_DOWN)
                    #print('done map')
                    print('6')


                elem = driver.find_element_by_name("title_th")
                elem.clear()
                elem.send_keys(str(data['post_title_th'])[:120], Keys.ARROW_DOWN)
                elem = driver.find_element_by_xpath('//div[@id="my_description_th"]')
                time.sleep(2)
                elem.click()
                time.sleep(5)
                elem = driver.find_element_by_name("description_th")
                elem.clear()
                data['post_description_th'] = str(data['post_description_th']).replace('\r','')
                for i in range(10,0,-1):

                    if i==1:
                        data['post_description_th'] = str(data['post_description_th']).replace('\n'*i, '<br>')
                    else:
                        data['post_description_th'] = str(data['post_description_th']).replace('\n' * i, '<br>'+'<p><br></p>'*(i-1))

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

                    elem.send_keys(data['post_description_en'], Keys.ARROW_DOWN)

                #print('going to save')
                driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)

                btn = driver.find_element_by_xpath('//button[@class="ui green button"]')
                time.sleep(2)
                btn.click()
                time.sleep(3)
                driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
                driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
                driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
                time.sleep(2)
                elem = driver.find_element_by_xpath('//div[@id="photoGallery"]').click()
                total = 15

                if len(data['post_images'])<15:
                    total = len(data['post_images'])
                image = ''
                count=1
                for img in data['post_images'][:total]:
                    image = Image.open(img)
                    new_image = image.resize((600, 400))
                    new_image.save(img)
                image = ''
                #time.sleep(60)
                for img in data['post_images'][:total]:
                    #print(str(img))
                    if count!=total:
                        image+=(str(os.getcwd())+'/'+str(img)+' \n')
                    else:
                        image += (str(os.getcwd()) + '/' + str(img))
                    count+=1
                uploader = driver.find_element_by_class_name('input-file').send_keys(image)
                time.sleep(20)
                btn = driver.find_element_by_class_name('tgl').click()
                time.sleep(2)
                txt = str(driver.current_url)
                post_id = ''
                ind = txt.find('properties')+11
                while txt[ind]!='/':
                    post_id+=txt[ind]
                    ind+=1
                url = 'https://www.dotproperty.co.th/my-dashboard/properties'
                driver.get(url)
                time.sleep(10)
                print('7')

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



            end_time = datetime.datetime.utcnow()
            result = {'success': success,
                      'usage_time': str(end_time - start_time),
                      'start_time': str(start_time),
                      'end_time': str(end_time),
                      'post_url': post_url,
                      'post_id': post_id,
                      'account_type': 'null',
                      'ds_id': data['ds_id'],
                      'detail': detail,
                      'websitename': 'dotproperty'}
            return result
        except Exception as e:
            end_time = datetime.datetime.utcnow()
            result = {'success': "false",
                      'usage_time': str(end_time - start_time),
                      'start_time': str(start_time),
                      'end_time': str(end_time),
                      'post_url': "",
                      'post_id': "",
                      'account_type': 'null',
                      'ds_id': data['ds_id'],
                      'detail': str(e),
                      'websitename': 'dotproperty'}
            return result

    def boost_post(self, data):
        start_time = datetime.datetime.utcnow()
        log_id = str(data['log_id'])
        post_id = str(data['post_id'])
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        }
        success = ''
        detail = ''


        options = Options()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.add_experimental_option("prefs", prefs)
        options.add_argument('headless')
        driver = webdriver.Firefox(options=options)
        #driver.maximize_window()
        url = 'https://www.dotproperty.co.th/login'
        driver.get(url)

        #print('blocked')
        element = driver.find_element_by_name("email")
        element.send_keys(data['user'])
        #print('done')
        element = driver.find_element_by_name("password")
        element.send_keys(data['pass'])
        #print('done')
        time.sleep(2)

        submit = driver.find_element_by_id("loginPopupBtn")
        submit.click()
        time.sleep(2)
        txt = str(driver.page_source)
        success = ''
        detail = ''
        if txt.find('อีเมลและ/หรือรหัสผ่านของคุณไม่ตรงกัน โปรดลองใหม่อีกครั้ง') != -1:
            success = 'false'
            detail = 'Invalid credentials'
        else:
            url = 'https://www.dotproperty.co.th/my-dashboard/properties'
            driver.get(url)
            # block create-btn
            time.sleep(2)
            valid_ids = []
            try:
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

    def delete_post(self, data):
        start_time = datetime.datetime.utcnow()
        log_id = str(data['log_id'])
        post_id = str(data['post_id'])
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        }
        success = ''
        detail = ''

        options = Options()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.add_experimental_option("prefs", prefs)
        options.add_argument('headless')
        driver = webdriver.Firefox(options=options)
        # driver.maximize_window()
        url = 'https://www.dotproperty.co.th/login'
        driver.get(url)

        #print('blocked')
        element = driver.find_element_by_name("email")
        element.send_keys(data['user'])
        #print('done')
        element = driver.find_element_by_name("password")
        element.send_keys(data['pass'])
        #print('done')
        time.sleep(2)

        submit = driver.find_element_by_id("loginPopupBtn")
        submit.click()
        time.sleep(2)
        txt = str(driver.page_source)
        success = ''
        detail = ''
        if txt.find('อีเมลและ/หรือรหัสผ่านของคุณไม่ตรงกัน โปรดลองใหม่อีกครั้ง') != -1:
            success = 'false'
            detail = 'Invalid credentials'
        else:
            url = 'https://www.dotproperty.co.th/my-dashboard/properties'
            driver.get(url)
            # block create-btn
            time.sleep(2)
            valid_ids = []
            try:
                while True:
                    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
                    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
                    time.sleep(2)
                    posts = driver.find_element_by_xpath(
                        '//table[@class="ui celled table unstackable"]').find_element_by_tag_name(
                        'tbody').find_elements_by_tag_name('tr')
                    #print('here1')
                    count = 0
                    for post in posts:
                        count+=1
                        tds = post.find_elements_by_tag_name('td')
                        #print('here2')
                        if str(tds[2].text) in valid_ids:
                            raise Exception
                        #print(str(tds[2].text))
                        if str(tds[2].text) == post_id:
                            #print('in')
                            btn = tds[8].find_elements_by_xpath('//a[@class="ui negative basic button"]')[count-1]
                            time.sleep(2)
                            btn.click()
                            time.sleep(3)
                            btn = tds[8].find_element_by_xpath('//a[@class="item"]')
                            time.sleep(2)
                            btn.click()
                            time.sleep(3)

                            page = 0
                            #elem = driver.find_element_by_xpath('//div[@class="ui pagination menu container"]').find_elements_by_xpath('//div[@class="item"]')
                            while True:
                                driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
                                driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
                                posts = driver.find_element_by_xpath(
                                    '//table[@class="ui celled table unstackable"]').find_element_by_tag_name(
                                    'tbody').find_elements_by_tag_name('tr')
                                count = 0
                                for post in posts:
                                    count += 1
                                    tds = post.find_elements_by_tag_name('td')
                                    #print('here2')

                                    #print(str(tds[2].text))
                                    if str(tds[2].text) == post_id:
                                        btn = tds[7].find_elements_by_xpath('//a[@class="ui negative basic button"]')[
                                            count - 1]
                                        #print('gonna delete')
                                        time.sleep(2)
                                        btn.click()
                                        time.sleep(3)
                                        btn = driver.find_element_by_xpath('//button[@class="swal-button swal-button--confirm swal-button--danger"]')
                                        btn.click()
                                        time.sleep(2)
                                        # Retrieve the message on the Alert window

                                        end_time = datetime.datetime.utcnow()
                                        result = {
                                            "success": "true",
                                            "usage_time": str(end_time - start_time),
                                            "start_time": str(start_time),
                                            "end_time": str(end_time),
                                            "detail": "Post deleted",
                                            'ds_id': data['ds_id'],
                                            "log_id": log_id,
                                            "post_id": post_id,
                                            'websitename': 'dotproperty'
                                        }
                                        return result
                                driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                                driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                                elem = driver.find_element_by_xpath(
                                    '//div[@class="ui pagination menu container"]').find_elements_by_class_name('item')
                                if page>len(elem)-1:
                                    raise Exception
                                btn = elem[page]
                                page+=1
                                time.sleep(2)
                                btn.click()
                                time.sleep(3)



                        valid_ids.append(str(tds[2].text))
                        #print('here3')
                    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)

                    btn = driver.find_elements_by_xpath('//div[@class="item btn"]')
                    if len(btn) >= 2:
                        btn = btn[1]
                    else:
                        btn = btn[0]
                    time.sleep(2)
                    btn.click()
                    time.sleep(5)
                    #print('done')
            except Exception as e:
                #print(e)
                detail = 'Post not found'
                end_time = datetime.datetime.utcnow()
                result = {
                    "success": "false",
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

        options = webdriver.Options()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.add_experimental_option("prefs", prefs)
        options.add_argument('headless')
        driver = webdriver.Firefox(options=options)
        driver.maximize_window()
        url = 'https://www.dotproperty.co.th/login'
        driver.get(url)

        #print('blocked')
        element = driver.find_element_by_name("email")
        element.send_keys(data['user'])
        #print('done')
        element = driver.find_element_by_name("password")
        element.send_keys(data['pass'])
        #print('done')
        time.sleep(2)

        submit = driver.find_element_by_id("loginPopupBtn")
        submit.click()
        time.sleep(2)
        txt = str(driver.page_source)
        success = ''
        detail = ''
        if txt.find('อีเมลและ/หรือรหัสผ่านของคุณไม่ตรงกัน โปรดลองใหม่อีกครั้ง')!=-1:
            success = 'false'
            detail = 'Invalid credentials'
        else:
            url = 'https://www.dotproperty.co.th/my-dashboard/properties'
            driver.get(url)
            #block create-btn
            time.sleep(2)
            '''submit = driver.find_elements_by_tag_name("button")[2]
            submit.click()
            submit.click()
            submit.click()
            time.sleep(7)'''
            #driver.switch_to_window(driver.window_handles[0])

            #driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)

            '''element = driver.find_elements_by_css_selector("button[class='ui basic button edit-btn']")
            #print(element)
            #submit = div.find_element_by_tag_name('button')
            submit = element[3]
            action = ActionChains(driver)
            action.move_to_element(submit)
            action.click().perform()
            action.click().perform()
            action.click().perform()'''
            try:
                valid_ids = []
                x=1
                while x<5:
                    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
                    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
                    time.sleep(2)
                    posts = driver.find_element_by_xpath(
                        '//table[@class="ui celled table unstackable"]').find_element_by_tag_name(
                        'tbody').find_elements_by_tag_name('tr')
                    #print('here1')
                    flag = False
                    for post in posts:
                        tds = post.find_elements_by_tag_name('td')
                        #print('here2')
                        #print(str(tds[2].text))
                        if str(tds[2].text) == post_id:
                            btn = tds[8].find_element_by_class_name('block')
                            time.sleep(2)
                            btn.click()
                            time.sleep(3)
                            flag = True
                            break
                        if str(tds[2].text) in valid_ids:
                            raise Exception
                        valid_ids.append(str(tds[2].text))
                        #print('here3')
                    if flag == True:
                        break
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
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(3)
                #print('switched')
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
                #print(options)
                time.sleep(2)
                options.click()
                time.sleep(5)
                options = options.find_elements_by_class_name('item')
                for opt in options:
                    #print(opt.text)
                    if str(opt.text) == p_type:
                        opt.click()
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
                    data['web_project_name'] = ''.join(map(str, str(data['web_project_name']).split(' ')))
                    pro = data['web_project_name']
                    #print(pro)
                    '''url = 'https://www.dotproperty.co.th/dashboard-api/dropdown-filter-project?term='+str(data['web_project_name'])[:2]
                    pro = ''
                    req = httprequestObj.http_get(url)
                    if str(req.text) != '[]':
                        projects = []
                        txt = str(req.text)
                        ind = txt.find('text')
                        while ind!=-1:
                            ind+=7
                            proj = ''
                            while txt[ind]!='"':
                                proj+=txt[ind]
                                ind+=1
                            projects.append(proj.replace(' ',''))
                            txt = txt[ind:]
                            ind = txt.find('text')
                        for proj in projects:
                            if proj.find(data['web_project_name'])!=-1:
                                pro = proj
                                break'''
                    if pro!='':
                        #print('click')
                        btn = driver.find_element_by_xpath('//i[@class="remove icon project"]')
                        try:
                            btn.click()
                            time.sleep(3)
                            #print('cross')
                        except:
                            print('no cress')
                        options = driver.find_element_by_id('my_project')
                        time.sleep(2)
                        options.click()
                        time.sleep(5)
                        #print('clicked')
                        inp = options.find_elements_by_xpath('//input[@class="search"]')[2]
                        time.sleep(2)
                        inp.clear()

                        inp.send_keys(str(data['web_project_name'])[:4])
                        time.sleep(2)
                        inp.send_keys(Keys.TAB)
                        inp.send_keys(Keys.ENTER)
                        inp.send_keys(Keys.ARROW_DOWN)
                        #print('typed')
                        options = options.find_elements_by_class_name('item')
                        for opt in options:
                            #print(opt.text)
                            if str(opt.text).replace(' ','').find(pro)!=-1:
                                opt.click()
                                new_proj = False
                                break
                #print('project name done')

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

                    #my_showMap
                    '''options = driver.find_element_by_id('my_showMap').find_element_by_class_name('on-off')
                    time.sleep(2)
                    options.click()
                    time.sleep(5)
                    #print('clicked')'''
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
                time.sleep(2)
                btn.click()
                time.sleep(5)
                driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
                driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
                driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
                time.sleep(2)
                elem = driver.find_element_by_xpath('//div[@id="photoGallery"]').click()
                time.sleep(2)
                total = 15
                imgs = driver.find_elements_by_xpath('//div[@class="grid-item"]')
                for img in imgs:

                    btn = driver.find_elements_by_xpath('//div[@class="grid-item"]')[0]
                    time.sleep(2)
                    #print('here')
                    action = ActionChains(driver)
                    action.move_to_element(btn).perform()
                    #print('there')
                    time.sleep(2)
                    btn = driver.find_elements_by_xpath('//i[@class="fa fa-trash"]')[1]
                    btn.click()
                    time.sleep(3)
                    btn = driver.find_element_by_xpath('//button[@class="swal-button swal-button--confirm"]')
                    time.sleep(2)
                    btn.click()
                    time.sleep(3)

                if len(data['post_images'])<15:
                    total = len(data['post_images'])
                image = ''
                count=1
                for img in data['post_images'][:total]:
                    if count!=total:
                        image+=str(os.getcwd())+'/'+img+' \n'
                    else:
                        image += str(os.getcwd()) + '/' + img
                    count+=1
                uploader = driver.find_element_by_class_name('input-file').send_keys(image)
                time.sleep(20)
                btn = driver.find_element_by_class_name('tgl').click()
                time.sleep(2)
                txt = str(driver.current_url)
                post_id = ''
                ind = txt.find('properties')+11
                while txt[ind]!='/':
                    post_id+=txt[ind]
                    ind+=1
                url = 'https://www.dotproperty.co.th/my-dashboard/properties'
                driver.get(url)
                time.sleep(10)

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

                detail = 'Post edited'
            except Exception as e:
                #print(e)
                detail = 'Post cannot be edited'
                end_time = datetime.datetime.utcnow()
                result = {'success': success,
                          'usage_time': str(end_time - start_time),
                          'start_time': str(start_time),
                          'end_time': str(end_time),
                          'post_url': post_url,
                          'post_id': post_id,
                          'account_type': 'null',
                          'ds_id': data['ds_id'],
                          'detail': detail,
                          'websitename': 'dotproperty'}
                return result



        end_time = datetime.datetime.utcnow()
        result = {'success': success,
                  'usage_time': str(end_time - start_time),
                  'start_time': str(start_time),
                  'end_time': str(end_time),
                  'post_url': post_url,
                  'post_id': post_id,
                  'account_type': 'null',
                  'ds_id': data['ds_id'],
                  'log_id':data['log_id'],
                  'detail': detail,
                  'websitename': 'dotproperty'}
        return result

# https://www.dotproperty.co.th/my-dashboard/properties/4817078/edit



    def print_debug(self, msg):

        return True

    def print_debug_data(self, data):

        return True
