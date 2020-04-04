# -*- coding: utf-8 -*-

from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
import re
import json
import datetime
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
from urllib.parse import urlsplit
import string
import random


httprequestObj = lib_httprequest()


class ddproperty():

    name = 'ddproperty'

    def __init__(self):

        try:
            import configs
        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.debug = 1
        self.debugresdata = 0
        self.parser = 'html.parser'
        self.handled = False

        options = Options()
        options.add_argument("--headless")  # Runs Chrome in headless mode.
        options.add_argument('--no-sandbox')  # Bypass OS security model
        options.add_argument('start-maximized')
        options.add_argument('disable-infobars')
        options.add_argument("--disable-extensions")
        options.add_argument("window-size=1024,768")
        chromedriver_binary = "/bin/chromedriver"
        self.chrome = webdriver.Chrome(chromedriver_binary, options=options)

    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']
        company_name = postdata['company_name']
        name_title = postdata["name_title"]
        name_th = postdata["name_th"]
        surname_th = postdata["surname_th"]
        name_en = postdata["name_en"]
        surname_en = postdata["surname_en"]
        tel = postdata["tel"]
        line: postdata["amarin.ta"]
        addr_province = postdata["addr_province"]

        # start process
        #
        tel = list(tel)
        del tel[0]
        newtel = ''.join(tel)

        # จะต้องไปหน้า from login ก่อน เพื่อเก็บ session อะไรซักอย่าง จึงจะสามารถ post ไป register ได้
        r = httprequestObj.http_get('https://www.ddproperty.com/agent-register?package=TRIAL', verify=False)
        data = r.text
        f = open("debug_response/ddloginfrom.html", "wb")
        f.write(data.encode('utf-8').strip())

        datapost = {
            'agency_id': 'OTHER',
            'otheragency-th-text': company_name,
            'otheragency-en-text': company_name,
            'otheragency': '',
            'job_title-th-text': '',
            'job_title-en-text': '',
            'job_title': '',
            'title': name_title,
            'firstname-th-text': name_th,
            'firstname-en-text': '',
            'firstname': '',
            'lastname-th-text': surname_th,
            'lastname-en-text':  '',
            'lastname': '',
            'birthDay': 10,
            'birthMonth': 10,
            'birthYear': 1986,
            'email': user,
            'mobile': newtel,
            'region': 'TH37',
            'city_area': '',
            'password': passwd,
            'password_confirm': passwd,
            'communication_us': 1,
            'submit': 'Submit',
            'months': ''
        }

        r = httprequestObj.http_post('https://www.ddproperty.com/agent-register', data=datapost)
        data = r.text
        f = open("debug_response/ddregister.html", "wb")
        f.write(data.encode('utf-8').strip())

        register_success = "true"
        detail = ""
        if re.search('distil_r_captcha.html', data):
            register_success = "false"
            detail = "Operation die by Google reCAPTCHA"
        #
        # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": register_success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
        }

    def test_login_httpreq(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')

        user = postdata['user']
        passwd = postdata['pass']
        ds_name = "ddproperty"
        if (postdata["ds_name"]):
            ds_name = postdata["ds_name"]
        ds_id = ""
        if (postdata["ds_id"]):
            ds_id = postdata["ds_id"]

        # start process
        #
        success = "true"
        detail = ""
        agent_id = ""

        datapost = {
            'email': user,
        }
        r = httprequestObj.http_post('https://agentnet.ddproperty.com/is_authentic_user', data=datapost)
        data = r.text
        f = open("debug_response/ddauthentic.html", "wb")
        f.write(data.encode('utf-8').strip())
        datajson = r.json()
        # if logged in ,session is 0 cause  {"status":0,"name":"\u0e14\u0e39\u0e14\u0e35 \u0e14\u0e2d\u0e17\u0e04\u0e2d\u0e21","email":"kla.arnut@hotmail.com","profile":"https:\/\/th1-cdn.pgimgs.com\/agent\/10760807\/APHO.74655966.C100X100.jpg"}
        if datajson['status'] and datajson['status'] == 0:
            if datajson['email'] != user:
                success = "false"
                detail = data
        if success == "true":
            datapost = {
                'password': passwd,
                'recapchaResponse': '',
                'remember_me': 'true',
                'submit': 'true',
                '': 'true',
                'userid': user,
            }
            r = httprequestObj.http_post('https://agentnet.ddproperty.com/ex_login_ajax', data=datapost)
            data = r.text
            f = open("debug_response/logindd.html", "wb")
            f.write(data.encode('utf-8').strip())
            matchObj = re.search(r'success', data)
            if matchObj:
                agent_id = re.search(r'jwt_prod_(\d+)', data).group(1)
            else:
                success = "false"
                detail = "cannot login"
        #
        # end process

        return {
            "success": success,
            "detail": detail,
            "agent_id": agent_id
        }

    def test_login_headless(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')

        # start process
        #
        success = "true"
        detail = ""
        agent_id = ""

        # open login page
        self.chrome.get('https://agentnet.ddproperty.com/ex_login?w=1&redirect=/ex_home')

        # input email and enter
        emailtxt = WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_id("emailInput"))
        emailtxt.send_keys(postdata['user'])
        nextbttn = WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_id("next"))
        nextbttn.click()
        time.sleep(1)

        # input password and enter
        passtxt = WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_id("inputPassword"))
        passtxt.send_keys(postdata['pass'])
        passtxt.send_keys(Keys.ENTER)
        time.sleep(1)
        # f = open("debug_response/loginpassdd2.html", "wb")
        # f.write(self.chrome.page_source.encode('utf-8').strip())

        # find text
        soup = BeautifulSoup(self.chrome.page_source, self.parser, from_encoding='utf-8')
        titletxt = soup.find('title').text
        matchObj = re.search(r'Dashboard', titletxt)
        if not matchObj:
            success = "false"
            detail = 'cannot login'
        if success == "true":
            # agent_id = re.search(r'optimize_agent_id = (\d+);', self.chrome.page_source).group(1)
            agent_id = re.search(r'{"user":{"id":(\d+),', self.chrome.page_source).group(1)

        #
        # end process

        return {
            "success": success,
            "detail": detail,
            "agent_id": agent_id
        }

    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        #
        datahandled = self.postdata_handle(postdata)

        response = {}
        if datahandled['action'] == 'create_post':
            response = self.test_login_headless(datahandled)
        else:
            response = self.test_login_httpreq(datahandled)

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        response['usage_time'] = str(time_usage)
        response['start_time'] = str(time_start)
        response['end_time'] = str(time_end)

        return response

    def postdata_handle(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')

        if self.handled == True:
            return postdata

        datahandled = {}

        # "SALE", "RENT", "OPT" ขาย ให้เช่า ขายดาวน์
        try:
            datahandled['listing_type'] = postdata['listing_type']
        except KeyError:
            datahandled['listing_type'] = "SALE"
        if datahandled['listing_type'] == "ให้เช่า":
            datahandled['listing_type'] = "RENT"
        elif datahandled['listing_type'] == "ขายดาวน์":
            datahandled['listing_type'] = "OPT"
        else:
            datahandled['listing_type'] = "SALE"

        # "CONDO","BUNG","TOWN","LAND","APT","RET","OFF","WAR","BIZ","SHOP"]
        try:
            datahandled['property_type'] = postdata['property_type']
        except KeyError:
            datahandled['property_type'] = "CONDO"
        if datahandled['property_type'] == 2 or datahandled['property_type'] == "บ้านเดี่ยว":
            datahandled['property_type'] = "BUNG"
        elif datahandled['property_type'] == 3 or datahandled['property_type'] == "บ้านแฝด":
            datahandled['property_type'] = "BUNG"
        elif datahandled['property_type'] == 4 or datahandled['property_type'] == "ทาวน์เฮ้าส์":
            datahandled['property_type'] = "TOWN"
        elif datahandled['property_type'] == 5 or datahandled['property_type'] == "ตึกแถว-อาคารพาณิชย์":
            datahandled['property_type'] = "SHOP"
        elif datahandled['property_type'] == 6 or datahandled['property_type'] == "ที่ดิน":
            datahandled['property_type'] = "LAND"
        elif datahandled['property_type'] == 7 or datahandled['property_type'] == "อพาร์ทเมนท์":
            datahandled['property_type'] = "APT"
        elif datahandled['property_type'] == 8 or datahandled['property_type'] == "โรงแรม":
            datahandled['property_type'] = "BIZ"
        elif datahandled['property_type'] == 9 or datahandled['property_type'] == "ออฟฟิศสำนักงาน":
            datahandled['property_type'] = "OFF"
        elif datahandled['property_type'] == 10 or datahandled['property_type'] == "โกดัง":
            datahandled['property_type'] = "WAR"
        elif datahandled['property_type'] == 25 or datahandled['property_type'] == "โรงงาน":
            datahandled['property_type'] = "WAR"
        else:
            datahandled['property_type'] = "CONDO"

        try:
            datahandled['post_img_url_lists'] = postdata['post_img_url_lists']
        except KeyError:
            datahandled['post_img_url_lists'] = {}

        try:
            datahandled['price_baht'] = postdata['price_baht']
        except KeyError:
            datahandled['price_baht'] = 0

        try:
            datahandled['addr_province'] = postdata['addr_province']
        except KeyError:
            datahandled['addr_province'] = ''

        try:
            datahandled['addr_district'] = postdata['addr_district']
        except KeyError:
            datahandled['addr_district'] = ''

        try:
            datahandled['addr_sub_district'] = postdata['addr_sub_district']
        except KeyError:
            datahandled['addr_sub_district'] = ''

        try:
            datahandled['addr_road'] = postdata['addr_road']
        except KeyError:
            datahandled['addr_road'] = ''

        try:
            datahandled['addr_near_by'] = postdata['addr_near_by']
        except KeyError:
            datahandled['addr_near_by'] = ''

        try:
            datahandled['addr_postcode'] = postdata['addr_postcode']
        except KeyError:
            datahandled['addr_postcode'] = ''

        try:
            datahandled['floorarea_sqm'] = postdata['floorarea_sqm']
        except KeyError:
            datahandled['floorarea_sqm'] = 99

        try:
            datahandled['geo_latitude'] = postdata['geo_latitude']
        except KeyError:
            datahandled['geo_latitude'] = ''

        try:
            datahandled['geo_longitude'] = postdata['geo_longitude']
        except KeyError:
            datahandled['geo_longitude'] = ''

        try:
            datahandled['property_id'] = postdata['property_id']
        except KeyError:
            datahandled['property_id'] = ''

        try:
            datahandled['post_title_th'] = postdata['post_title_th']
        except KeyError:
            datahandled['post_title_th'] = ''

        try:
            datahandled['post_description_th'] = postdata['post_description_th']
        except KeyError:
            datahandled['post_description_th'] = ''

        try:
            datahandled['post_title_en'] = postdata['post_title_en']
        except KeyError:
            datahandled['post_title_en'] = ''

        try:
            datahandled['post_description_en'] = postdata['post_description_en']
        except KeyError:
            datahandled['post_description_en'] = ''

        try:
            datahandled['ds_id'] = postdata["ds_id"]
        except KeyError:
            datahandled['ds_id'] = ''

        try:
            datahandled['ds_name'] = postdata["ds_name"]
        except KeyError:
            datahandled['ds_name'] = ''

        try:
            datahandled['user'] = postdata['user']
        except KeyError:
            datahandled['user'] = ''

        try:
            datahandled['pass'] = postdata['pass']
        except KeyError:
            datahandled['pass'] = ''

        try:
            datahandled['project_name'] = postdata["project_name"]
        except KeyError:
            datahandled['project_name'] = ''

        try:
            datahandled['name'] = postdata["name"]
        except KeyError:
            datahandled['name'] = ''

        try:
            datahandled['mobile'] = postdata["mobile"]
        except KeyError:
            datahandled['mobile'] = ''

        try:
            datahandled['email'] = postdata["email"]
        except KeyError:
            datahandled['email'] = ''

        try:
            datahandled['web_project_name'] = postdata["web_project_name"]
        except KeyError:
            datahandled['web_project_name'] = ''

        try:
            datahandled['action'] = postdata["action"]
        except KeyError:
            datahandled['action'] = ''

        try:
            datahandled['bath_room'] = postdata["bath_room"]
        except KeyError:
            datahandled['bath_room'] = 0

        try:
            datahandled['bed_room'] = postdata["bed_room"]
        except KeyError:
            datahandled['bed_room'] = 0

        try:
            datahandled['floor_total'] = postdata["floor_total"]
        except KeyError:
            datahandled['floor_total'] = 1

        try:
            datahandled['floor_level'] = postdata["floor_level"]
        except KeyError:
            datahandled['floor_level'] = 1

        try:
            datahandled['direction_type'] = postdata["direction_type"]
        except KeyError:
            datahandled['direction_type'] = "ทิศเหนือ"
        if datahandled['direction_type'] == '11':
            datahandled['direction_type'] = "ทิศเหนือ"
        elif datahandled['direction_type'] == '12':
            datahandled['direction_type'] = "ทิศใต้"
        elif datahandled['direction_type'] == '13':
            datahandled['direction_type'] = "ทิศตะวันออก"
        elif datahandled['direction_type'] == '14':
            datahandled['direction_type'] = "ทิศตะวันตก"
        elif datahandled['direction_type'] == '21':
            datahandled['direction_type'] = "ทิศตะวันออกเฉียงเหนือ"
        elif datahandled['direction_type'] == '22':
            datahandled['direction_type'] = "ทิศตะวันออก"
        elif datahandled['direction_type'] == '23':
            datahandled['direction_type'] = "ทิศตะวันตกเฉียงเหนือ"
        elif datahandled['direction_type'] == '24':
            datahandled['direction_type'] = "ทิศตะวันตกเฉียงใต้"

        # image
        datahandled['post_images'] = postdata["post_images"]

        self.handled = True

        return datahandled

    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        #
        datahandled = self.postdata_handle(postdata)

        # login
        test_login = self.test_login(datahandled)
        success = test_login["success"]
        detail = test_login["detail"]
        agent_id = test_login["agent_id"]
        post_id = ""

        if success == "true":
            projectname = datahandled['project_name']
            if datahandled['web_project_name'] != '':
                projectname = datahandled['web_project_name']

            self.chrome.get('https://agentnet.ddproperty.com/create-listing/location')
            time.sleep(1)
            # self.chrome.save_screenshot("debug_response/location.png")
            projectnametxt = WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_id("propertySearch"))
            projectnametxt.send_keys(projectname)
            projectnametxt.send_keys(Keys.ENTER)
            time.sleep(1)
            # self.chrome.save_screenshot("debug_response/location2.png")
            # f = open("debug_response/ddpost.html", "wb")
            # f.write(self.chrome.page_source.encode('utf-8').strip())

            # case no result
            matchObj = re.search(r'ol class="no-match"', self.chrome.page_source)
            if matchObj:
                if(datahandled['addr_province'] == '' or datahandled['addr_district'] == '' or datahandled['addr_sub_district'] == ''):
                    success = 'false'
                    detail = 'for a new project name, ddproperty must require province , district and sub_district'
                if success == 'true':
                    WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_class_name("property-new-link")).click()
                    time.sleep(0.1)
                    # self.chrome.save_screenshot("debug_response/newp1.png")
                    linktxt = ''
                    cssselect = ''
                    if datahandled['property_type'] == "BUNG":
                        linktxt = 'บ้านเดี่ยว'
                        cssselect = 'BUNG'
                    elif datahandled['property_type'] == "TOWN":
                        linktxt = 'ทาวน์เฮ้าส์'
                        cssselect = 'TOWN'
                    elif datahandled['property_type'] == "SHOP":
                        linktxt = 'เชิงพาณิชย์'
                        cssselect = 'RET'
                    elif datahandled['property_type'] == "LAND":
                        linktxt = 'ที่ดิน'
                        cssselect = 'LAND'
                    elif datahandled['property_type'] == "APT":
                        linktxt = 'อพาร์ทเมนท์'
                        cssselect = 'APT'
                    elif datahandled['property_type'] == "OFF":
                        linktxt = 'เชิงพาณิชย์'
                        cssselect = 'OFF'
                    elif datahandled['property_type'] == "WAR":
                        linktxt = 'เชิงพาณิชย์'
                        cssselect = 'WAR'
                    else:  # CONDO
                        linktxt = 'คอนโด'
                        cssselect = 'CONDO'
                    WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_id("propertyTypeSelect")).click()
                    time.sleep(0.1)
                    WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_link_text(linktxt)).click()
                    time.sleep(0.1)
                    WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_css_selector("input[type='radio'][value='"+cssselect+"']")).click()
                    time.sleep(0.1)
                    # self.chrome.save_screenshot("debug_response/newp3.png")

                    try:
                        WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_id("form-field-region")).click()
                        time.sleep(0.1)
                        WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_link_text(datahandled['addr_province'])).click()
                        time.sleep(0.1)
                        WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_id("form-field-district")).click()
                        time.sleep(0.1)
                        WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_link_text(datahandled['addr_district'])).click()
                        time.sleep(0.1)
                        WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_id("form-field-area")).click()
                        time.sleep(0.1)
                        WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_link_text(datahandled['addr_sub_district'])).click()
                        time.sleep(0.5)
                        # self.chrome.save_screenshot("debug_response/newp3.png")
                    except Exception as e:
                        success = 'false'
                        detail = 'for a new project name, province , district , subdistrict error'

                    if (success == 'true'):
                        res = self.inputpostattr(datahandled)

                        # case match choose first argument
            else:
                # dddd
                aaa = 11111

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": datahandled['ds_id'],
            "post_url": "https://www.ddproperty.com/preview-listing/"+post_id if post_id != "" else "",
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
        }

    def inputpostattr(self, datahandled):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')

        WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_class_name('step-next')).click()
        time.sleep(1)
        # self.chrome.save_screenshot("debug_response/newp4.png")
        # WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_css_selector("input[type='radio'][id='listing-type-"+datahandled['listing_type']+"']")).find_element_by_tag_name('span').click()
        if datahandled['listing_type'] == "SALE":
            WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_xpath('//*[@id="app-listing-creation"]/div/div[2]/div/section/div/div[1]/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/label/span')).click()
        elif datahandled['listing_type'] == "RENT":
            WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_xpath('//*[@id="app-listing-creation"]/div/div[2]/div/section/div/div[1]/div/div/div/div[2]/div/div[1]/div/div/div/div[2]/label/span')).click()
        else:
            WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_xpath('//*[@id="app-listing-creation"]/div/div[2]/div/section/div/div[1]/div/div/div/div[2]/div/div[1]/div/div/div/div[3]/label/span')).click()
        # self.chrome.save_screenshot("debug_response/newp5.png")
        WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_id("input-listing-price")).send_keys(datahandled['price_baht'])
        if int(datahandled['bed_room']) > 0:
            WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_id("bedRoomDropdown")).click()
            if int(datahandled['bed_room']) >= 10:
                WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_link_text('10 + ห้องนอน')).click()
            else:
                WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_link_text(str(datahandled['bed_room'])+' ห้องนอน')).click()
        WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_id("bathRoomDropdown")).click()
        if int(datahandled['bath_room']) == 0:
            WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_link_text('ไม่มีห้องน้ำ')).click()
        elif int(datahandled['bath_room']) >= 1 and int(datahandled['bath_room']) < 9:
            WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_link_text(str(datahandled['bath_room'])+' ห้องน้ำ')).click()
        else:
            WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_link_text('9 ห้องน้ำ')).click()
        WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_id("input-floorarea_sqm")).send_keys(str(datahandled['floorarea_sqm']))
        WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_id("form-field-total-floor")).click()
        WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_link_text(str(datahandled['floor_total']))).click()
        WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_id("form-field-floorposition")).click()
        WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_link_text(str(datahandled['floor_level']))).click()
        WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_id("title-input")).send_keys(datahandled['post_title_th'])
        WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_id("titleEn-input")).send_keys(datahandled['post_title_en'])
        WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_id("description-th-input")).send_keys(datahandled['post_description_th'])
        WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_id("description-en-input")).send_keys(datahandled['post_description_en'])
        WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_id("form-field-facing-type")).click()
        WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_link_text(datahandled['direction_type'])).click()
        time.sleep(0.5)
        self.chrome.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)  # scroll to head page
        time.sleep(0.5)
        WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_xpath('//*[@id="app-listing-creation"]/div/div[2]/div/header/div/div/div[3]/div/div[2]/a')).click()  # next
        time.sleep(1)

        for img in datahandled['post_images']:
            WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_css_selector("input[accept='image/png,image/jpg,image/jpeg'][type='file']")).send_keys(os.path.abspath('imgtmp/'+img))

        WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_xpath('//*[@id="app-listing-creation"]/div/div[2]/div/header/div/div/div[3]/div/div[2]/a')).click()  # next
        time.sleep(1)
        self.chrome.save_screenshot("debug_response/newp10.png")
        exit()

    def create_post_bak(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        #
        datahandled = self.postdata_handle(postdata)

        # login
        test_login = self.test_login(datahandled)
        success = test_login["success"]
        detail = test_login["detail"]
        agent_id = test_login["agent_id"]
        post_id = ""

        if success == "true":
            # TODO ใช้การ get create-listing/location ก่อนเพื่อไปหน้า create-listing/detail
            # เพื่อตรวจสอบ หา account_type normal/corperate ไม่ได้
            # เพราะ response html เป็น js render ทีหลัง html ทำให้ไม่ได้ content มาเพื่อตรวจสอบ account type
            # ดังนั้น จะ get account_type ไม่ได้ แต่เวลา post จะใส่ name,mobile,email ให้หมด
            # get รายละเอียดตัวแทน
            # r = httprequestObj.http_get('https://agentnet.ddproperty.com/create-listing/location', verify=r=httprequestObj.http_get('https://agentnet.ddproperty.com/sf2-agent/ajax/media/property/7015/photo', verify=False))
            # r = httprequestObj.http_get('https://agentnet.ddproperty.com/sf2-agent/ajax/project-net/property/7015?language=th', verify=False)
            # r = httprequestObj.http_get('https://agentnet.ddproperty.com/sf2-agent/ajax/media/property/7015/photo', verify=False)
            # r = httprequestObj.http_get('https://agentnet.ddproperty.com/create-listing/detail', verify=False)
            # data = r.text
            # f = open("debug_response/ddcreatelist.html", "wb")
            # f.write(data.encode('utf-8').strip())

            # get property attr
            r = httprequestObj.http_get('https://services.propertyguru.com/v1/autocomplete?region=th&locale=th&limit=25&object_type=PROPERTY&query='+datahandled['project_name'], verify=False)
            # data = r.text
            # f = open("debug_response/ddcreatelist.html", "wb")
            # f.write(data.encode('utf-8').strip())
            datajson = r.json()
            propertyattr = {}
            # if not found , new project
            if len(datajson) == 0:
                # จะต้องมา map หา จังหวัด อำเภอ ตำบล อีก response error ไปเลยดีกว่า
                # จังหวัด TH01 อำเภอ TH0101 ตำบล TH010101 รหัส ปณ 11110
                success = 'false'
                detail = 'ชื่อโครงการไม่มีใน list และไม่มีระบุ จังหวัด  อำเภอ  ตำบล รหัสปณ มา '
            # if found < 0 , choose array 0
            else:
                propertyattr['postalCode'] = re.search(r'.*(\d{5}).*', datajson[0]['displayDescription']).group(1)
                propertyattr['districtCode'] = datajson[0]['properties']['district']
                propertyattr['regionCode'] = re.search(r'(TH\d{2})', datajson[0]['properties']['district']).group(1)
                propertyattr['objectId'] = datajson[0]['objectId']

            if success == 'true':
                # postdata
                agent_id = agent_id
                datapost = {
                    "id": "",
                    "title": datahandled['post_title_en'],
                    "localizedTitle":  datahandled['post_title_th'],
                    "description":  datahandled['post_description_en'],
                    "localizedDescription":  datahandled['post_description_th'],
                    "hasStream": "false",
                    "statusCode": "DRAFT",
                    "sourceCode": "",
                    "typeCode":  datahandled['listing_type'],
                    "leaseTermCode": "",
                    "featureCode": "",
                    "externalId": '9999',
                    "event": "",
                    "location": {
                        "id": "626225",  # TODO ''
                        "block": "",
                        "unit": "",
                        "streetId": "",
                        "longitude":  datahandled['geo_longitude'],
                        "latitude":  datahandled['geo_latitude'],
                        "hdbEstateCode": "",
                        "streetName1": "",
                        "streetName2": "",
                        "streetNumber": "",
                        "postalCode": propertyattr['postalCode'],
                        "regionCode": propertyattr['regionCode'],
                        "districtCode": propertyattr['districtCode'],
                        "areaCode": "",
                        "zoneIds": ""
                    },
                    "media": {
                        "cover": {
                            "id": ""
                        },
                        "excluded": [],
                        "included": []
                    },
                    "property": {
                        "id": propertyattr['objectId'],
                        "name": datahandled['project_name'],
                        "temporaryId": "",
                        "typeCode":  datahandled['property_type'],
                        "typeGroup": "",
                        "tenureCode": "",
                        "topYear": "",
                        "totalUnits": '',
                        "floors": "",
                        "amenities": []
                    },
                    "propertyUnit": {
                        "tenureCode": "",
                        "furnishingCode": "",
                        "description": "",
                        "hdbTypeCode": "",
                        "floorplanId": -1,
                        "floorLevelCode": "",
                        "floorPosition": "",
                        "telephoneLines": "",
                        "cornerUnit": "",
                        "facingCode": "",
                        "features": [],
                        "occupancyCode": "",
                        "electricitySupply": "",
                        "electricityPhase": "",
                        "ceilingHeight": "",
                        "floorLoading": "",
                        "parkingSpaces": "",
                        "parkingFees": "",
                        "maintenanceFee": "",
                        "liftCargo": "",
                        "liftPassenger": "",
                        "liftCapacity": "",
                        "centralAircon": "",
                        "centralAirconHours": "",
                        "ownerTypeCode": "",
                        "sellerEthnic": "",
                        "sellerResidency": "",
                        "quotaEthnic": "false",
                        "quotaSpr": "false",
                        "tenancy": {
                            "value": "",
                            "tenantedUntilDate": {}
                        }
                    },
                    "price": {
                        "value": datahandled['price_baht'],  # price_baht ใช้ price bath 3000 แล้ว error,
                        "periodCode": "",
                        "valuation": "",
                        "type": {
                            "code": "BAH",
                            "text": ""}},
                    "sizes": {
                        "bedrooms": {
                            "value": datahandled['bed_room']},
                        "bathrooms": {
                            "value": datahandled['bath_room']},
                        "extrarooms": {
                            "value": ""},
                        "floorArea": [{"value": datahandled['floorarea_sqm'], "unit": "sqm"}],
                        "landArea": [{"value": "", "unit": "sqm"}],
                        "floorX": [{"unit": "m", "value": ""}],
                        "floorY": [{"unit": "m", "value": ""}],
                        "landX": [{"unit": "m", "value": ""}],
                        "landY": [{"unit": "m", "value": ""}]},
                    "agent": {
                        "id": agent_id,
                        "alternativePhone": "",
                        "alternativeAgent": datahandled['name'],
                        "alternativeMobile": datahandled['mobile'],
                        "alternativeEmail": datahandled['email']
                    },
                    "hasFloorplans": "false",
                    "boost": {"boostActive": "false", "boostDuration": 0},
                    "dates": {"timezone": "Asia/Singapore", "available": ""},
                    "descriptions": {
                        "th":  datahandled['post_description_th']},
                    "qualityScore": 0,
                    "localizedHeadline": "",
                    "headlines": {"th": ""},  # TODO short_post_title_th
                    "titles": {
                        "th":  datahandled['post_title_th']
                    }
                }
                datastr = json.dumps(datapost)
                r = httprequestObj.http_post_json('https://agentnet.ddproperty.com/sf2-agent/ajax/listings', jsoncontent=datastr)
                data = r.text
                f = open("debug_response/postdd.html", "wb")
                f.write(data.encode('utf-8').strip())
                matchObj = re.search(r'errors', data)
                if matchObj:
                    success = "false"
                    detail = data
                else:
                    post_id = re.search(r'{"id":(\d+)', data).group(1)

                # # TODO post image
                # if success == 'true':
                #     datapost = {
                #         'ownerId': 7841959,
                #         'mediaType': 'IMAGE',
                #         'mediaClass': 'UPHO',
                #         'source': 'AgentNet',
                #         'userId': 10760807,
                #         'caption': '',
                #         'sortOrder': 1,
                #         'mediaFile': '''

                #         ''',
                #     }
                #     r = httprequestObj.http_post('https://agentnet.ddproperty.com/sf2-agent/ajax/listings/7841959/media', data=data)
                #     data = r.text
                #     f = open("debug_response/uploadimg.html", "wb")
                #     f.write(data.encode('utf-8').strip())
        #
        # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": datahandled['ds_id'],
            "post_url": "https://www.ddproperty.com/preview-listing/"+post_id if post_id != "" else "",
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
        }

    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        post_id = postdata['post_id']
        log_id = postdata['log_id']
        user = postdata['user']
        passwd = postdata['pass']

        # start process
        #

        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        agent_id = test_login["agent_id"]
        if success == "true":
            datapost = {
                "country": "th",
                "session": "3B7EC6629ADB7BD3ADEA8CFD4F91E7D3"  # TODO จะใช้ได้ตลอดไปมั้ย
            }
            datajson = json.dumps(datapost)
            headerreg = {"content-type": "application/json"}
            r = httprequestObj.http_post_with_multi_options('https://auth.propertyguru.com/session-to-jwt', headerreg=headerreg, jsoncontent=datajson)
            data = r.text
            # f = open("debug_response/ddsessiontojwt.html", "wb")
            # f.write(data.encode('utf-8').strip())
            jsonres = r.json()
            if not jsonres["token"]:
                success == "false"
                detail = jsonres
            if success == "true":
                headerreg = {
                    "content-type": "application/json",
                    "authorization": "Bearer " + jsonres["token"]
                }
                # r = httprequestObj.http_post_with_multi_options('https://ads-products.propertyguru.com/api/v1/listing/7797845/product/ranked-spotlight/add?region=th&agentId=10760807', headerreg=headerreg, jsoncontent={})
                r = httprequestObj.http_post_with_multi_options('https://ads-products.propertyguru.com/api/v1/listing/'+post_id+'/product/ranked-spotlight/add?region=th&agentId='+agent_id, headerreg=headerreg, jsoncontent={})
                data = r.text
                f = open("debug_response/ddboostpostresponse.html", "wb")
                f.write(data.encode('utf-8').strip())

                # TODO ถ้า boost สำเร็จ response จะเป็นยังไง
                success = "false"
                detail = data + " ต้องมี credit จริง เพื่อเก็บ response เวลา boost post สำเร็จ"

            #
            # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "log_id": log_id,
            "post_id": post_id,
        }

    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        log_id = postdata['log_id']
        # postdata['post_id'] = '7790593'
        post_id = postdata['post_id']
        # postdata['user'] = 'kla.arnut@gmail.com'
        user = postdata['user']
        # postdata['pass'] = 'vkIy9b'
        passwd = postdata['pass']

        # start process
        #
        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]

        if success == "true":
            # จะต้องไปหน้า listing_management เพื่อเก็บ session อะไรซักอย่าง จึงจะสามารถ post ไป delete ได้
            r = httprequestObj.http_get('https://agentnet.ddproperty.com/listing_management#DRAFT', verify=False)
            data = r.text
            # f = open("debug_response/ddpostlistdraft.html", "wb")
            # f.write(data.encode('utf-8').strip())

            # listing_id%5B%5D=7788093&remove=Delete%20selected&selecteds=7788093
            datapost = {
                "listing_id[]": post_id,
                "remove": "Delete selected",
                "selecteds": post_id,
            }
            r = httprequestObj.http_post('https://agentnet.ddproperty.com/remove_listing', data=datapost)
            data = r.text
            # f = open("debug_response/dddelete.html", "wb")
            # f.write(data.encode('utf-8').strip())
            matchObj = re.search(r'message":"deleted', data)
            if matchObj:
                # ใกล้ความจริง แต่จะ delete สำเร็จหรือไม่มันก็ return deleted หมด ดังนั้นต้องเช็คจาก post id อีกทีว่า response 404 ป่าว
                r = httprequestObj.http_get('https://agentnet.ddproperty.com/create-listing/detail/'+post_id, verify=False)
                data = r.text
                # f = open("debug_response/dddelete.html", "wb")
                # f.write(data.encode('utf-8').strip())
                if(r.status_code == 200):
                    success = "false"
                    detail = r.text

        #
        # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "log_id": log_id,
        }

    def edit_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # post_img_url_lists = postdata['post_img_url_lists']
        price_baht = postdata['price_baht']
        # county = postdata["county"]
        # district = postdata["district"]
        # addr_province = postdata['addr_province']
        # addr_district = postdata['addr_district']
        # addr_sub_district = postdata['addr_sub_district']
        # addr_road = postdata['addr_road']
        # addr_near_by = postdata['addr_near_by']
        # floorarea_sqm = postdata['floorarea_sqm']
        # geo_latitude = postdata['geo_latitude']
        # geo_longitude = postdata['geo_longitude']
        # property_id = postdata['property_id']
        post_title_th = postdata['post_title_th']
        post_description_th = postdata['post_description_th']
        # post_title_en = postdata['post_title_en']
        # post_description_en = postdata['post_description_en']
        # postdata["post_id"] = '7788091'
        post_id = postdata["post_id"]
        # postdata['user'] = 'kla.arnut@gmail.com'
        user = postdata['user']
        # postdata['pass'] = 'vkIy9b'
        passwd = postdata['pass']
        log_id = postdata["log_id"]

        # start proces
        #

        # login
        self.test_login(postdata)
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        agent_id = test_login["agent_id"]

        if (success == "true"):
            datapost = {
                "id": post_id,
                "statusCode": "DRAFT",
                "daysUntilExpire": 0,
                "isExpiring": "true",
                "sourceCode": "",
                "typeCode": "SALE",
                "typeText": "ขาย",
                "subTypeCode": "",
                "leaseTermCode": "",
                "leaseTermText": "",
                "featureCode": "",
                "accountTypeCode": "NORMAL",
                "accountSubTypeCode": "",
                "isPremiumAccount": "false",
                "isPropertySpecialistListing": "false",
                "isMobilePropertySpotlightListing": "false",
                "isTransactorListing": "false",
                "isCommercial": "false",
                "hasFloorplans": "false",
                "hasStream": "true",
                "featuredBy": [

                ],
                "localizedHeadline": "",
                "headlines": {
                    "th": "",
                    "en": ""
                },
                "localizedTitle": post_title_th,
                "titles": {
                    "th": post_title_th
                },
                "localizedDescription": post_description_th,
                "descriptions": {
                    "th": post_description_th
                },
                "notes": "",
                "externalId": 9999,
                "cobroke": 0,
                "price": {
                    "value": 9999999,
                    "pretty": "฿9,999,999",
                    "periodCode": "",
                    "pricePerArea": {
                        "value": 227272.7045,
                        "unit": "sqm",
                        "reference": "floorArea"
                    },
                    "type": {
                        "code": "BAH",
                        "text": "",
                        "pretty": "บาท"
                    },
                    "valuation": 0,
                    "valuationText": "",
                    "completed": 0,
                    "currency": "฿"
                },
                "sizes": {
                    "bedrooms": {
                        "value": "",
                        "text": ""
                    },
                    "bathrooms": {
                        "value": "",
                        "text": ""
                    },
                    "extrarooms": {
                        "value": "",
                        "text": ""
                    },
                    "floorArea": [
                        {
                            "unit": "sqm",
                            "value": 44,
                            "text": "44 ตร.ม."
                        }
                    ],
                    "landArea": [
                        {
                            "unit": "sqm",
                            "value": "",
                            "text": ""
                        }
                    ],
                    "floorX": [
                        {
                            "unit": "m",
                            "value": ""
                        }
                    ],
                    "floorY": [
                        {
                            "unit": "m",
                            "value": ""
                        }
                    ],
                    "landX": [
                        {
                            "unit": "m",
                            "value": ""
                        }
                    ],
                    "landY": [
                        {
                            "unit": "m",
                            "value": ""
                        }
                    ]
                },
                "pricePerArea": {
                    "floorArea": [
                        {
                            "unit": "sqm",
                            "value": 227272.70454545,
                            "text": "฿227,273 / ตารางเมตร"
                        }
                    ],
                    "landArea": [
                        {
                            "unit": "",
                            "value": "",
                            "text": ""
                        }
                    ]
                },
                "dates": {
                    "timezone": "Asia/Singapore",
                    "firstPosted": "",
                    "lastPosted": "",
                    "expiry": "",
                    "available": "",
                    "created": {
                        "date": "2020-03-11 01:14:38",
                        "unix": 1583860478
                    },
                    "updated": {
                        "date": "2020-03-11 01:14:38",
                        "unix": 1583860478
                    }
                },
                "urls": {
                    "listing": {
                        "api": "https://api.propertyguru.com/v1/listings/7788091?region=th",
                        "internal": "http://listing.guruestate.com/v1/listings/7788091?region=th",
                        "mobile": "https://www.ddproperty.com/property/xxx-ขาย-7788091",
                        "desktop": "https://www.ddproperty.com/property/xxx-ขาย-7788091",
                        "desktopByLocales": {
                            "th": "https://www.ddproperty.com/property/xxx-ขาย-7788091",
                            "en": "https://www.ddproperty.com/en/property/xxx-for-sale-7788091"
                        },
                        "preview": {
                            "desktop": "https://www.ddproperty.com/preview-listing/7788091"
                        }
                    }
                },
                "_user": "",
                "qualityScore": 70,
                "finalScore": "",
                "tier": 0,
                "showAgentProfile": "false",
                "event": "",
                "mywebOrder": "",
                "agent": {
                    "id": agent_id,
                    "name": "cccc cccc",
                    "mobile": "+66839703921",
                    "mobilePretty": "+66 83 970 3921",
                    "phone": "",
                    "phonePretty": "",
                    "alternativePhone": "",
                    "alternativeAgent": "",
                    "alternativeMobile": "",
                    "alternativeEmail": "",
                    "jobTitle": "",
                    "licenseNumber": "",
                    "showProfile": "false",
                    "website": "",
                    "email": "kla.arnut@gmail.com",
                    "blackberryPin": ""
                },
                "agency": {
                    "id": 42297,
                    "name": "aaaa",
                    "ceaLicenseNumber": ""
                },
                "location": {
                    "id": 626225,
                    "latitude": 13.8749,
                    "longitude": 100.413606,
                    "distance": "",
                    "regionCode": "TH12",
                    "regionText": "นนทบุรี",
                    "regionSlug": "นนทบุรี",
                    "districtCode": "TH1203",
                    "districtText": "บางใหญ่",
                    "districtSlug": "บางใหญ่",
                    "areaCode": "11",
                    "areaText": "",
                    "areaSlug": "",
                    "fullAddress": ". ถนนรัตนาธิเบศร์ ตำบลเสาธงหิน อำเภอบางใหญ่ นนทบุรี, บางใหญ่, นนทบุรี",
                    "hdbEstateCode": "",
                    "hdbEstateText": "",
                    "postalCode": "11110",
                    "block": "",
                    "unit": "",
                    "streetId": "",
                    "streetName1": "ถนนรัตนาธิเบศร์ ตำบลเสาธงหิน อำเภอบางใหญ่ นนทบุรี",
                    "streetName2": "",
                    "streetNumber": ".",
                    "zoneIds": "",
                    "subZoneIds": ""
                },
                "property": {
                    "id": 5987,
                    "temporaryId": "",
                    "statusCode": "6DML",
                    "name": "Plum condo central station เฟส 1",
                    "typeCode": "CONDO",
                    "typeText": "คอนโด",
                    "typeGroup": "N",
                    "tenureCode": "F",
                    "tenureText": "ขายขาด",
                    "topMonth": 10,
                    "topYear": 2018,
                    "developer": "Pruksa Real Estate - พฤกษา เรียลเอสเตท จำกัด (มหาชน)",
                    "totalUnits": 1208,
                    "floors": 38,
                    "amenities": [
                        {
                            "code": "CCAR"
                        },
                        {
                            "code": "CTV"
                        },
                        {
                            "code": "FIT"
                        },
                        {
                            "code": "OCAR"
                        },
                        {
                            "code": "PDEC"
                        },
                        {
                            "code": "SAUNA"
                        },
                        {
                            "code": "SEC"
                        },
                        {
                            "code": "SPA"
                        },
                        {
                            "code": "STE"
                        },
                        {
                            "code": "SWI"
                        },
                        {
                            "code": "WAD"
                        }
                    ]
                },
                "propertyUnit": {
                    "id": 7989636,
                    "description": "",
                    "furnishingCode": "",
                    "furnishingText": "",
                    "hdbTypeCode": "",
                    "floorplanId": -1,
                    "floorLevelCode": "",
                    "floorLevelText": "",
                    "floorPosition": "",
                    "cornerUnit": "",
                    "facingCode": "",
                    "occupancyCode": "",
                    "electricitySupply": "",
                    "electricityPhase":  "",
                    "ceilingHeight": "",
                    "floorLoading": "",
                    "garages": "",
                    "parkingSpaces": "",
                    "parkingFees": "",
                    "maintenanceFee": {
                        "value": 0,
                        "pretty": "฿0.00",
                        "periodeCode": "MONTH"
                    },
                    "liftCargo": "",
                    "liftPassenger": "",
                    "liftCapacity": "",
                    "centralAircon": "",
                    "centralAirconHours": "",
                    "ownerTypeCode": "",
                    "sellerEthnic": "",
                    "sellerResidency":  "",
                    "quotaEthnic": "true",
                    "quotaSpr": "true",
                    "telephoneLines": "",
                    "features": [

                    ],
                    "tenancy": {
                        "value": "UNTENANTED",
                        "tenantedUntilDate": {

                        }
                    },
                    "tenureCode": "F"
                },
                "media": {
                    "cover": {
                        "id": 61330097,
                        "caption": "",
                        "statusCode": "CONF",
                        "suspReason": "",
                        "appealComment": "",
                        "appealSent": "false",
                        "sortOrder": 61330097,
                        "V150": "https://th2-cdn.pgimgs.com/property/5987/PPHO.61330097.V150/Plum-condo-central-station-%E0%B9%80%E0%B8%9F%E0%B8%AA-1-%E0%B8%9A%E0%B8%B2%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88-Thailand.jpg",
                        "V550": "https://th2-cdn.pgimgs.com/property/5987/PPHO.61330097.V550/Plum-condo-central-station-%E0%B9%80%E0%B8%9F%E0%B8%AA-1-%E0%B8%9A%E0%B8%B2%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88-Thailand.jpg"
                    },
                    "listing": [

                    ],
                    "property": [
                        {
                            "id": 61330097,
                            "caption": "",
                            "statusCode": "CONF",
                            "suspReason": "",
                            "appealComment": "",
                            "appealSent": "false",
                            "sortOrder": 61330097,
                            "V150": "https://th2-cdn.pgimgs.com/property/5987/PPHO.61330097.V150/Plum-condo-central-station-%E0%B9%80%E0%B8%9F%E0%B8%AA-1-%E0%B8%9A%E0%B8%B2%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88-Thailand.jpg",
                            "V550": "https://th2-cdn.pgimgs.com/property/5987/PPHO.61330097.V550/Plum-condo-central-station-%E0%B9%80%E0%B8%9F%E0%B8%AA-1-%E0%B8%9A%E0%B8%B2%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88-Thailand.jpg"
                        },
                        {
                            "id": 61330098,
                            "caption": "",
                            "statusCode": "CONF",
                            "suspReason": "",
                            "appealComment": "",
                            "appealSent": "false",
                            "sortOrder": 61330098,
                            "V150": "https://th1-cdn.pgimgs.com/property/5987/PPHO.61330098.V150/Plum-condo-central-station-%E0%B9%80%E0%B8%9F%E0%B8%AA-1-%E0%B8%9A%E0%B8%B2%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88-Thailand.jpg",
                            "V550": "https://th1-cdn.pgimgs.com/property/5987/PPHO.61330098.V550/Plum-condo-central-station-%E0%B9%80%E0%B8%9F%E0%B8%AA-1-%E0%B8%9A%E0%B8%B2%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88-Thailand.jpg"
                        },
                        {
                            "id": 61330099,
                            "caption": "",
                            "statusCode": "CONF",
                            "suspReason": "",
                            "appealComment": "",
                            "appealSent": "false",
                            "sortOrder": 61330099,
                            "V150": "https://th2-cdn.pgimgs.com/property/5987/PPHO.61330099.V150/Plum-condo-central-station-%E0%B9%80%E0%B8%9F%E0%B8%AA-1-%E0%B8%9A%E0%B8%B2%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88-Thailand.jpg",
                            "V550": "https://th2-cdn.pgimgs.com/property/5987/PPHO.61330099.V550/Plum-condo-central-station-%E0%B9%80%E0%B8%9F%E0%B8%AA-1-%E0%B8%9A%E0%B8%B2%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88-Thailand.jpg"
                        },
                        {
                            "id": 61330104,
                            "caption": "",
                            "statusCode": "CONF",
                            "suspReason": "",
                            "appealComment": "",
                            "appealSent": "false",
                            "sortOrder": 61330104,
                            "V150": "https://th1-cdn.pgimgs.com/property/5987/PPHO.61330104.V150/Plum-condo-central-station-%E0%B9%80%E0%B8%9F%E0%B8%AA-1-%E0%B8%9A%E0%B8%B2%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88-Thailand.jpg",
                            "V550": "https://th1-cdn.pgimgs.com/property/5987/PPHO.61330104.V550/Plum-condo-central-station-%E0%B9%80%E0%B8%9F%E0%B8%AA-1-%E0%B8%9A%E0%B8%B2%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88-Thailand.jpg"
                        }
                    ],
                    "agent": "",
                    "agentLogo": [

                    ],
                    "agencyLogo": [

                    ],
                    "excluded": [

                    ],
                    "included": [

                    ],
                    "listingDocuments": [

                    ],
                    "propertyFloorplans": [

                    ],
                    "listingFloorplans": [

                    ],
                    "listingSiteplans": [

                    ],
                    "listingVideos": [

                    ],
                    "listingVirtualTours": [

                    ]
                },
                "metas": {
                    "title": "Xxx, . ถนนรัตนาธิเบศร์ ตำบลเสาธงหิน อำเภอบางใหญ่ นนทบุรี, บางใหญ่, นนทบุรี, 44 ตร.ม., คอนโด ขาย, โดย Cccc Cccc, ฿9,999,999, 7788091",
                    "description": "ดูรายละเอียด, รูปภาพ และแผนที่ของประกาศอสังหาริมทรัพย์ 7788091 - ขาย - xxx - . ถนนรัตนาธิเบศร์ ตำบลเสาธงหิน อำเภอบางใหญ่ นนทบุรี, บางใหญ่, นนทบุรี, 44 ตร.ม., ฿9,999,999",
                    "keywords": "ตัวแทน, ประกาศ, อสังหาริมทรัพย์, ทรัพย์สิน, ขาย, เช่า, อพาร์ทเม้นท์, บ้าน, ชาวต่างชาติ, ที่อยู่อาศัย, hdb, สถานที่ตั้ง, คอนโด, แผนที่"
                },
                "alertBatchId": "",
                "unitTypes": [

                ],
                "qualityScoreData": {
                    "price": 50,
                    "location": 10,
                    "3_user_photos": 0,
                    "1_user_photo": 0,
                    "videos_or_virtual_tours": 0,
                    "bedrooms": 0,
                    "description": 0,
                    "bathrooms": 0,
                    "floorarea": 5,
                    "landarea": 3,
                    "property": 1,
                    "furnishing": 0,
                    "unit_features": 0,
                    "property_photo": 1,
                    "raw_score": 70,
                    "score": 70
                },
                "dependencyErrors": [

                ],
                "isRankedSpotlight": "false",
                "isFeaturedListing": "false"
            }
            datastr = json.dumps(datapost)
            # print(datastr)
            r = httprequestObj.http_put_json('https://agentnet.ddproperty.com/sf2-agent/ajax/update/'+post_id, jsoncontent=datastr)
            data = r.text
            f = open("debug_response/editpostdd.html", "wb")
            f.write(data.encode('utf-8').strip())

            matchObj = re.search(r'errors', data)
            if matchObj:
                success = "false"
                detail = data
            matchObj = re.search(r'Oops!', data)
            if matchObj:
                success = "false"
                detail = data

        #
        # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "log_id": log_id
        }

    def print_debug(self, msg):
        if(self.debug == 1):
            print(msg)
        return True

    def print_debug_data(self, data):
        if(self.debugdata == 1):
            print(data)
        return True
