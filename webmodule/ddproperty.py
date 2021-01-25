# -*- coding: utf-8 -*-

import logging
import logging.config
from .lib_httprequest import *
httprequestObj = lib_httprequest()
from bs4 import BeautifulSoup
import os.path
import re
import json
import datetime
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
import time
from urllib.parse import urlsplit
import string
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import numpy as np


try:
    import configs
except ImportError:
    configs = {}
'''
logging.config.dictConfig(getattr(configs, 'logging_config', {}))
log = logging.getLogger()'''


class ddproperty():

    name = 'ddproperty'

    def __init__(self):

        self.websitename = 'ddproperty'
        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.parser = 'html.parser'
        self.handled = False

    def register_user(self, postdata):
        #log.debug('')

        time_start = datetime.datetime.utcnow()

        # start process
        #
        datahandled = self.postdata_handle(postdata)
        user = datahandled['user']
        passwd = datahandled['pass']
        company_name = postdata['company_name']
        name_title = postdata["name_title"]
        name_th = postdata["name_th"]
        surname_th = postdata["surname_th"]
       
        tel = postdata["tel"]
        line = postdata["line"]
        tel = list(tel)
        del tel[0]
        newtel = ''.join(tel)

        # จะต้องไปหน้า from login ก่อน เพื่อเก็บ session อะไรซักอย่าง จึงจะสามารถ post ไป register ได้
        r = httprequestObj.http_get('https://www.ddproperty.com/agent-register?package=TRIAL', verify=False)
        data = r.text
        #f = open("debug_response/ddloginfrom.html", "wb")
        #f.write(data.encode('utf-8').strip())

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
            'lastname-en-text': '',
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
        #f = open("debug_response/ddregister.html", "wb")
        #f.write(data.encode('utf-8').strip())

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
            "websitename": "ddproperty",
            "success": register_success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
        }

    def test_login_httpreq(self, postdata):
        #log.debug('')

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
        #log.debug('email post')
        data = r.text
        # f = open("debug_response/ddauthentic.html", "wb")
        # f.write(data.encode('utf-8').strip())
        # f.close()
        try:
            datajson = r.json()
            # if logged in ,session is 0 cause  {"status":0,"name":"\u0e14\u0e39\u0e14\u0e35 \u0e14\u0e2d\u0e17\u0e04\u0e2d\u0e21","email":"kla.arnut@hotmail.com","profile":"https:\/\/th1-cdn.pgimgs.com\/agent\/10760807\/APHO.74655966.C100X100.jpg"}
            if datajson['status'] and datajson['status'] == 0:
                if datajson['email'] != user:
                    success = "false"
                    detail = data
        except:
            success = "false"
            detail = "Access denied"
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
            #log.debug('post login')
            data = r.text
            #f = open("debug_response/logindd.html", "wb")
            #f.write(data.encode('utf-8').strip())
            matchObj = re.search(r'success', data)
            if matchObj:
                agent_id = re.search(r'jwt_prod_(\d+)', data).group(1)
            else:
                success = "false"
                detail = "cannot login " + data

        #log.debug('login status %s', success)
        #
        # end process

        return {"success": success, "detail": detail, "agent_id": agent_id}

    def test_login_headless(self, postdata):
        #log.debug('')

        # ref https://developer.mozilla.org/en-US/docs/Web/WebDriver
        # รอจนกว่าจะมี element h3>a ขึ้นมา ค่อยทำงานต่อ
        # WebDriverWait(self.firefox, 5).until(presence_of_element_located((By.CSS_SELECTOR, "h3>a")))
        # results = driver.find_elements_by_css_selector("h3>a")

        # start process
        #
        success = "true"
        detail = ""
        agent_id = ""

        options = Options()
        # debug by comment option --headless
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('start-maximized')
        options.add_argument('disable-infobars')
        options.add_argument("--disable-extensions")
        options.add_argument("disable-gpu")
        options.add_argument("window-size=1024,768")
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # options.add_experimental_option("prefs", prefs)
        # chrome_driver_binary = "/usr/bin/chromedriver"

        self.firefox = webdriver.Chrome("./static/chromedriver", chrome_options=options)

        start_x = random.randint(0, 50)
        end_x = random.randint(0, 50)
        start_y = random.randint(0, 20)
        end_y = random.randint(0, 20)

        pos_rand_x = np.linspace(start_x, end_x, 5)
        pos_rand_y = np.linspace(start_y, end_y, 5)

        pos_list = []
        for i in range(0, 5):
            pos_tmp = []
            pos_tmp.append(pos_rand_x[i])
            pos_tmp.append(pos_rand_y[i])
            pos_list.append(pos_tmp)

        try:
            # self.firefox = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=options)
            # open login page
            # self.firefox = webdriver.Chrome("C:/Users/hp/Downloads/chromedriver_win32/chromedriver", chrome_options=options)

            self.firefox.get('https://agentnet.ddproperty.com/ex_login?w=1&redirect=/ex_home')

            action = ActionChains(self.firefox)
            for pos_item in pos_list:
                rand_time = random.uniform(0.00001, 0.001)
                #print(str(int(pos_item[0])) + ' ' + str(int(pos_item[1])))
                action.move_by_offset(int(pos_item[0]), int(pos_item[1]))
                action.perform()
                time.sleep(rand_time)

            # input email and enter
            emailtxt = WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("emailInput"))
            emailtxt.send_keys(postdata['user'])
            #log.debug('input email')
            WebDriverWait(self.firefox, 5).until(EC.element_to_be_clickable((By.ID, "next"))).click()
            #log.debug('click next')
            time.sleep(1.8)

            # input password and enter
            passtxt = WebDriverWait(self.firefox, 30).until(EC.presence_of_element_located((By.ID, "inputPassword")))
            passtxt.send_keys(postdata['pass'])
            #log.debug('input password')
            passtxt.send_keys(Keys.ENTER)
            #log.debug('click enter')
            time.sleep(3)
            
            matchObj = re.search(r'บัญชีผู้ใช้งานของท่านหมดอายุ', self.firefox.page_source)
            matchObj2 = re.search(r'User account is not active', self.firefox.page_source)
            if matchObj or matchObj2:
                success = "false"
                detail = 'User account is not active. Please contact cs@ddproperty.com or 02-204-9555 for more information.'
                #log.warning('User account is not active. Please contact cs@ddproperty.com or 02-204-9555 for more information.')
            matchObj = re.search(r'รหัสผ่านของคุณไม่ถูกต้อง', self.firefox.page_source)
            if matchObj:
                success = "false"
                detail = 'รหัสผ่านของคุณไม่ถูกต้อง กรุณาลองใส่รหัสที่ถูกต้องอีกครั้ง หรือกดปุ่ม "ลืมรหัสผ่าน" เพื่อทำการตั้งรหัสใหม่'
                #log.warning('รหัสผ่านของคุณไม่ถูกต้อง กรุณาลองใส่รหัสที่ถูกต้องอีกครั้ง หรือกดปุ่ม "ลืมรหัสผ่าน" เพื่อทำการตั้งรหัสใหม่')
            matchObj = re.search(r'มีข้อผิดพลาดเกิดขึ้น', self.firefox.page_source)
            if matchObj:
                success = "false"
                detail = 'มีข้อผิดพลาดเกิดขึ้น โปรดลองใหม่อีกครั้งในภายหลัง'
                #log.warning('มีข้อผิดพลาดเกิดขึ้น โปรดลองใหม่อีกครั้งในภายหลัง')
            matchObj = re.search(r'Incorrect Captcha', self.firefox.page_source)
            matchObj2 = re.search(r'ฉันไม่ใช่โปรแกรมอัตโนมัติ', self.firefox.page_source)
            matchObj3 = re.search(r'Captcha ไม่ถูกต้อง', self.firefox.page_source)
            if matchObj or matchObj2 or matchObj3:
                success = "false"
                detail = 'cannot login'
                #log.warning('cannot login')
            if success == "true":
                # agent_id = re.search(r'optimize_agent_id = (\d+);', self.firefox.page_source).group(1)
                agent_id = re.search(r'{"user":{"id":(\d+),', self.firefox.page_source).group(1)

        #log.debug("login status %s agent id %s", success, agent_id)

        finally:
            if (postdata['action'] == 'test_login'):
                # self.firefox.quit()
                self.firefox.close()
                self.firefox.quit()
        #
        # end process

        return {"success": success, "detail": detail, "agent_id": agent_id}

    def test_login(self, postdata):
        #log.debug('')

        time_start = datetime.datetime.utcnow()

        # start process
        #
        datahandled = self.postdata_handle(postdata)

        response = {}
        # if datahandled['action'] == 'create_post' or datahandled['action'] == 'edit_post':
        response = self.test_login_headless(datahandled)
        # else:
            # response = self.test_login_httpreq(datahandled)

        # end process
        #
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        response['usage_time'] = str(time_usage)
        response['start_time'] = str(time_start)
        response['end_time'] = str(time_end)
        response['websitename'] = self.websitename
        response['ds_id'] = datahandled['ds_id']
        
        return response

    def postdata_handle(self, postdata):
        #log.debug('')
        if self.handled == True:
            return postdata

        datahandled = {}

        # "SALE", "RENT", "OPT" ขาย ให้เช่า ขายดาวน์
        try:
            datahandled['listing_type'] = postdata['listing_type']
        except KeyError as e:
            datahandled['listing_type'] = "SALE"
            #log.warning(str(e))
        if datahandled['listing_type'] == "เช่า":
            datahandled['listing_type'] = "RENT"
        elif datahandled['listing_type'] == "ขายดาวน์":
            datahandled['listing_type'] = "OPT"
        else:
            datahandled['listing_type'] = "SALE"

        # "CONDO","BUNG","TOWN","LAND","APT","RET","OFF","WAR","BIZ","SHOP"]
        try:
            datahandled['property_type'] = postdata['property_type']
        except KeyError as e:
            datahandled['property_type'] = "CONDO"
            #log.warning(str(e))
        if datahandled['property_type'] == '2' or datahandled['property_type'] == 2 or datahandled['property_type'] == "บ้านเดี่ยว":
            datahandled['property_type'] = "BUNG"
        elif datahandled['property_type'] == '3' or datahandled['property_type'] == 3 or datahandled['property_type'] == "บ้านแฝด":
            datahandled['property_type'] = "BUNG"
        elif datahandled['property_type'] == '4' or datahandled['property_type'] == 4 or datahandled['property_type'] == "ทาวน์เฮ้าส์":
            datahandled['property_type'] = "TOWN"
        elif datahandled['property_type'] == '5' or datahandled['property_type'] == 5 or datahandled['property_type'] == "ตึกแถว-อาคารพาณิชย์":
            datahandled['property_type'] = "SHOP"
        elif datahandled['property_type'] == '6' or datahandled['property_type'] == 6 or datahandled['property_type'] == "ที่ดิน":
            datahandled['property_type'] = "LAND"
        elif datahandled['property_type'] == '7' or datahandled['property_type'] == 7 or datahandled['property_type'] == "อพาร์ทเมนท์":
            datahandled['property_type'] = "APT"
        elif datahandled['property_type'] == '8' or datahandled['property_type'] == 8 or datahandled['property_type'] == "โรงแรม":
            datahandled['property_type'] = "BIZ"
        elif datahandled['property_type'] == '9' or datahandled['property_type'] == 9 or datahandled['property_type'] == "ออฟฟิศสำนักงาน":
            datahandled['property_type'] = "OFF"
        elif datahandled['property_type'] == '10' or datahandled['property_type'] == 10 or datahandled['property_type'] == "โกดัง":
            datahandled['property_type'] = "WAR"
        elif datahandled['property_type'] == '25' or datahandled['property_type'] == 25 or datahandled['property_type'] == "โรงงาน":
            datahandled['property_type'] = "WAR"
        else:
            datahandled['property_type'] = "CONDO"

        try:
            datahandled['post_img_url_lists'] = postdata['post_img_url_lists']
        except KeyError as e:
            datahandled['post_img_url_lists'] = {}
            #log.warning(str(e))

        try:
            datahandled['price_baht'] = postdata['price_baht']
        except KeyError as e:
            datahandled['price_baht'] = 0
            #log.warning(str(e))

        try:
            datahandled['addr_province'] = postdata['addr_province']
        except KeyError as e:
            datahandled['addr_province'] = ''
            #log.warning(str(e))

        try:
            datahandled['addr_district'] = postdata['addr_district']
        except KeyError as e:
            datahandled['addr_district'] = ''
            #log.warning(str(e))

        try:
            datahandled['addr_sub_district'] = postdata['addr_sub_district']
        except KeyError as e:
            datahandled['addr_sub_district'] = ''
            #log.warning(str(e))

        try:
            datahandled['addr_road'] = postdata['addr_road']
            if datahandled['addr_road'] == None:
                datahandled['addr_road'] = ""
        except KeyError as e:
            datahandled['addr_road'] = ''
            #log.warning(str(e))

        try:
            datahandled['addr_near_by'] = postdata['addr_near_by']
        except KeyError as e:
            datahandled['addr_near_by'] = ''
            #log.warning(str(e))

        try:
            datahandled['addr_postcode'] = postdata['addr_postcode']
        except KeyError as e:
            datahandled['addr_postcode'] = ''
            #log.warning(str(e))

        try:
            datahandled['floor_area'] = postdata['floor_area']
        except KeyError as e:
            datahandled['floor_area'] = '0'
            #log.warning(str(e))

        try:
            datahandled['geo_latitude'] = str(postdata['geo_latitude'])
        except KeyError as e:
            datahandled['geo_latitude'] = ''
            #log.warning(str(e))

        try:
            datahandled['geo_longitude'] = str(postdata['geo_longitude'])
        except KeyError as e:
            datahandled['geo_longitude'] = ''
            #log.warning(str(e))

        try:
            datahandled['property_id'] = postdata['property_id']
        except KeyError as e:
            datahandled['property_id'] = ''
            #log.warning(str(e))

        try:
            datahandled['post_title_th'] = str(postdata['post_title_th'])
        except KeyError as e:
            datahandled['post_title_th'] = ''
            #log.warning(str(e))

        try:
            datahandled['post_description_th'] = str(postdata['post_description_th'])
        except KeyError as e:
            datahandled['post_description_th'] = ''
            #log.warning(str(e))

        try:
            datahandled['post_title_en'] = postdata['post_title_en']
        except KeyError as e:
            datahandled['post_title_en'] = ''
            #log.warning(str(e))

        try:
            datahandled['post_description_en'] = postdata['post_description_en']
        except KeyError as e:
            datahandled['post_description_en'] = ''
            #log.warning(str(e))

        try:
            datahandled['ds_id'] = postdata["ds_id"]
        except KeyError as e:
            datahandled['ds_id'] = ''
            #log.warning(str(e))

        try:
            datahandled['ds_name'] = postdata["ds_name"]
        except KeyError as e:
            datahandled['ds_name'] = ''
            #log.warning(str(e))

        try:
            datahandled['user'] = postdata['user']
        except KeyError as e:
            datahandled['user'] = ''
            #log.warning(str(e))

        try:
            datahandled['pass'] = postdata['pass']
        except KeyError as e:
            datahandled['pass'] = ''
            #log.warning(str(e))

        try:
            datahandled['project_name'] = postdata["project_name"]
        except KeyError as e:
            datahandled['project_name'] = ''
            #log.warning(str(e))

        try:
            datahandled['name'] = postdata["name"]
        except KeyError as e:
            datahandled['name'] = ''
            #log.warning(str(e))

        try:
            datahandled['mobile'] = postdata["mobile"]
        except KeyError as e:
            datahandled['mobile'] = ''
            #log.warning(str(e))

        try:
            datahandled['email'] = postdata["email"]
        except KeyError as e:
            datahandled['email'] = ''
            #log.warning(str(e))

        try:
            datahandled['web_project_name'] = postdata["web_project_name"]
        except KeyError as e:
            datahandled['web_project_name'] = ''
            #log.warning(str(e))

        try:
            datahandled['action'] = postdata["action"]
        except KeyError as e:
            datahandled['action'] = ''
            #log.warning(str(e))

        try:
            datahandled['bath_room'] = postdata["bath_room"]
        except KeyError as e:
            datahandled['bath_room'] = 0
            #log.warning(str(e))

        try:
            datahandled['bed_room'] = postdata["bed_room"]
        except KeyError as e:
            datahandled['bed_room'] = 0
            #log.warning(str(e))

        try:
            datahandled['floor_total'] = postdata["floor_total"]
        except KeyError as e:
            datahandled['floor_total'] = 0
            #log.warning(str(e))

        try:
            datahandled['floor_level'] = postdata["floor_level"]
        except KeyError as e:
            datahandled['floor_level'] = 0
            #log.warning(str(e))

        try:
            datahandled['direction_type'] = postdata["direction_type"]
        except KeyError as e:
            datahandled['direction_type'] = "ทิศเหนือ"
            #log.warning(str(e))
        if datahandled['direction_type'] == '11' or datahandled['direction_type'] == 11:
            datahandled['direction_type'] = "ทิศเหนือ"
        elif datahandled['direction_type'] == '12' or datahandled['direction_type'] == 12:
            datahandled['direction_type'] = "ทิศใต้"
        elif datahandled['direction_type'] == '13' or datahandled['direction_type'] == 13:
            datahandled['direction_type'] = "ทิศตะวันออก"
        elif datahandled['direction_type'] == '14' or datahandled['direction_type'] == 14:
            datahandled['direction_type'] = "ทิศตะวันตก"
        elif datahandled['direction_type'] == '21' or datahandled['direction_type'] == 21:
            datahandled['direction_type'] = "ทิศตะวันออกเฉียงเหนือ"
        elif datahandled['direction_type'] == '22' or datahandled['direction_type'] == 22:
            datahandled['direction_type'] = "ทิศตะวันออก"
        elif datahandled['direction_type'] == '23' or datahandled['direction_type'] == 23:
            datahandled['direction_type'] = "ทิศตะวันตกเฉียงเหนือ"
        elif datahandled['direction_type'] == '24' or datahandled['direction_type'] == 24:
            datahandled['direction_type'] = "ทิศตะวันตกเฉียงใต้"

        # image
        datahandled['post_images'] = postdata["post_images"]

        try:
            datahandled['post_id'] = postdata["post_id"]
        except KeyError as e:
            datahandled['post_id'] = ''
            #log.warning(str(e))

        try:
            datahandled['log_id'] = postdata["log_id"]
        except KeyError as e:
            datahandled['log_id'] = ''
            #log.warning(str(e))

        try:
            datahandled['land_size_rai'] = str(postdata["land_size_rai"])
            if(postdata["land_size_rai"]) == None:
                postdata["land_size_rai"] = '0'
        except KeyError as e:
            datahandled['land_size_rai'] = '0'
            #log.warning(str(e))

        try:
            datahandled['land_size_ngan'] = str(postdata["land_size_ngan"])
            if(postdata["land_size_ngan"]) == None:
                postdata["land_size_ngan"] = '0'
        except KeyError as e:
            datahandled['land_size_ngan'] = '0'
            #log.warning(str(e))

        try:
            datahandled['land_size_wa'] = str(postdata["land_size_wa"])
            if(postdata["land_size_wa"]) == None:
                postdata["land_size_wa"] = '0'
        except KeyError as e:
            datahandled['land_size_wa'] = '0'
            #log.warning(str(e))

        self.handled = True
        return datahandled

    def create_post(self, postdata):
        time_start = datetime.datetime.utcnow()
        datahandled = self.postdata_handle(postdata)
        
        # login
        test_login = self.test_login(datahandled)
        success = test_login["success"]
        detail = test_login["detail"]
        agent_id = test_login["agent_id"]
        post_id = ""
        account_type = "normal"

        if success == "true":
            self.firefox.get('https://agentnet.ddproperty.com/create-listing/location')
            time.sleep(1)
            WebDriverWait(self.firefox, 5).until(EC.presence_of_element_located((By.ID, "propertySearch"))) 
            # self.firefox.save_screenshot("debug_response/location.png")

            success, detail = self.inputpostgeneral(datahandled)
            if success == 'true':
                success, detail, post_id, account_type = self.inputpostdetail(datahandled)
                print(success, detail, post_id, account_type)
        try:
            self.firefox.quit()
        except:
            pass
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": datahandled['ds_id'],
            "post_url": "https://www.ddproperty.com/preview-listing/" + post_id if post_id else "",
            "post_id": post_id,
            "account_type": account_type,
            "detail": detail,
            "websitename": self.websitename
        }

    def inputpostgeneral(self, datahandled):
        #log.debug('')

        success = 'true'
        detail = ''

        # 1 use project_name
        # 2 if web_project_name, use web_project_name
        # 3 if web_project_name = '' or null , use post_title_th

        projectname = datahandled['project_name']
        if datahandled['web_project_name'] != '' and datahandled['web_project_name'] != 'null':
            projectname = datahandled['web_project_name']
        if projectname == '':
            projectname = datahandled['post_title_th']

        projectnametxt = WebDriverWait(self.firefox, 10).until(EC.presence_of_element_located((By.ID, "propertySearch")))
        time.sleep(1)
        if datahandled['action'] == 'edit_post':
            WebDriverWait(self.firefox, 10).until(lambda x: x.find_element_by_id("propertySearch")).send_keys(Keys.CONTROL + "a")  # clear for edit action
            WebDriverWait(self.firefox, 10).until(lambda x: x.find_element_by_id("propertySearch")).send_keys(Keys.DELETE)  # clear for edit action
        projectnametxt.send_keys(projectname)
        projectnametxt.send_keys(Keys.ENTER)
        WebDriverWait(self.firefox, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "open")))
        time.sleep(1)
        #self.firefox.save_screenshot("debug_response/location2.png")
        # f = open("debug_response/ddpost.html", "wb")
        # f.write(self.firefox.page_source.encode('utf-8').strip())

        # case no result projectname
        matchObj = re.search(r'ol class="no-match"', self.firefox.page_source)
        if matchObj:
            #log.debug('not found property name %s', projectname)
            if (datahandled['addr_province'] == '' or datahandled['addr_district'] == '' or datahandled['addr_sub_district'] == ''):
                success = 'false'
                detail = 'for a new project name, ddproperty must require province , district and sub_district'
            if success == 'true':
                WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_class_name("property-new-link")).click()
                time.sleep(0.2)
                # self.firefox.save_screenshot("debug_response/newp1.png")

                # listing type
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
                    cssselect = 'SHOP'
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
                elif datahandled['property_type'] == "BIZ":
                    linktxt = 'เชิงพาณิชย์'
                    cssselect = 'BIZ'
                else:  # CONDO
                    linktxt = 'คอนโด'
                    cssselect = 'CONDO'
                WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("propertyTypeSelect")).click()
                time.sleep(0.1)
                WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_link_text(linktxt)).click()
                time.sleep(0.1)
                WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_css_selector("input[type='radio'][value='" + cssselect + "']")).click()
                time.sleep(0.2)
                element = WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_xpath('//*[@id="app-listing-creation"]/div/div[2]/div/section/div/div[1]/div/div/div/div[4]/div/div[1]/div/div/div/div'))
                self.firefox.execute_script("arguments[0].style.display = 'none';", element)
                #self.firefox.save_screenshot("debug_response/newp3.png")

                # province district subdistrict
                try:
                    WebDriverWait(self.firefox, 5).until(EC.presence_of_element_located((By.ID, "form-field-region")))
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("form-field-region")).click()
                    time.sleep(0.1)
                    if re.search(r'กรุงเทพ', datahandled['addr_province']):
                        datahandled['addr_province'] = 'กรุงเทพ'
                    if re.search(r'ป้อมปราบ', datahandled['addr_sub_district']):
                        datahandled['addr_sub_district'] = 'ป้อมปราบศัตรูพ่าย'
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_link_text(datahandled['addr_province'])).click()
                    time.sleep(0.1)
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("form-field-district")).click()
                    time.sleep(0.1)
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_link_text(datahandled['addr_district'])).click()
                    time.sleep(0.1)
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("form-field-area")).click()
                    time.sleep(0.1)
                    try:
                        WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_link_text(datahandled['addr_sub_district'])).click()
                        time.sleep(0.1)
                    except:
                        f_select_itm = WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_xpath('//ul[@aria-labelledby="form-field-area"]'))
                        f_select_itm.find_element_by_tag_name('a').click()
                    # self.firefox.save_screenshot("debug_response/newp33.png")
                except Exception as e:
                    success = 'false'
                    detail = 'for a new project name, province , district , subdistrict error'
                    #log.error('area error ' + str(e))

                # road
                try:
                    WebDriverWait(self.firefox, 5).until(EC.presence_of_element_located((By.ID, "street-name-field")))
                    if datahandled['action'] == 'edit_post':
                        WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("street-name-field")).send_keys(Keys.CONTROL + "a")  # clear for edit action
                        WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("street-name-field")).send_keys(Keys.DELETE)  # clear for edit action
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("street-name-field")).send_keys(datahandled['addr_road'])
                except Exception as e:
                    pass
                    #log.warning('road error ' + str(e))
                # self.firefox.save_screenshot("debug_response/newp33.png")

                # longitude ,latitude
                # TODO
                try:
                    time.sleep(0.5)
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_class_name("btn-mark-googlemaps")).click()
                    time.sleep(2)
                    #debug
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_xpath('//*[@id="app-listing-creation"]/div/div[2]/div/section/div/div[1]/div/div/div/div[10]/div/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div[3]/div/div[3]/div')).click()
                    
                    #log.debug('input lat %s lng %s',datahandled['geo_latitude'],datahandled['geo_longitude'])
                    js = 'guruApp.createListing.formData.map.lat = ' + datahandled['geo_latitude'] + '; guruApp.createListing.formData.map.lng = ' + datahandled['geo_longitude'] + '; '
                    self.firefox.execute_script(js)
                    time.sleep(0.5)

                    #TODO debug
                    element = WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_xpath('//*[@id="app-listing-creation"]/div/div[2]/div/section/div/div[1]/div/div/div/div[10]/div/div[1]/div/div/div/div/div/div/div/div/div/div[2]/a'))
                    self.firefox.execute_script("arguments[0].setAttribute('href','https://maps.google.com/maps?ll=13.649778,100.362285&z=14&t=m&hl=en-US&gl=US&mapclient=apiv3');", element)
                    time.sleep(0.5)
                    element = WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_xpath('//*[@id="app-listing-creation"]/div/div[2]/div/section/div/div[1]/div/div/div/div[10]/div/div[1]/div/div/div/div/div/div/div/div/div/div[7]/div[2]/a'))
                    self.firefox.execute_script("arguments[0].setAttribute('href','https://www.google.com/maps/@13.649778,100.362285,14z/data=!10m1!1e1!12b1?source=apiv3&rapsrc=apiv3');", element)
                    time.sleep(0.5)
                    #TODO debug

                   
                except Exception as e:
                    #log.warning('lat lng error ' + str(e))
                    pass

                if (success == 'true'):
                    self.firefox.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)  # scroll to head page
                    WebDriverWait(self.firefox, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app-listing-creation"]/div/div[2]/div/header/div/div/div[2]/div/a[2]/div[2]')))
                    #self.firefox.save_screenshot("debug_response/newp33.png")
                    nextbttn = WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_xpath('//*[@id="app-listing-creation"]/div/div[2]/div/header/div/div/div[2]/div/a[2]/div[2]'))
                    self.firefox.execute_script("arguments[0].click();", nextbttn)

                    try:
                        cancel_plus_code = WebDriverWait(self.firefox, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'btn-default-outline')))
                        cancel_plus_code[-1].click()
                    except:
                        pass

        # case match choose first argument
        else:
            #log.debug('found property name %s', projectname)
            # self.firefox.save_screenshot("debug_response/newp3.png")
            # select li first
            WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_xpath('//*[@id="app-listing-creation"]/div/div[2]/div/section/div/div[1]/div/div/div/div[2]/div/div[1]/div/div/div/div/ol/li[1]/a')).click()
            time.sleep(0.2)
            # self.firefox.save_screenshot("debug_response/newp4.png")
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
                cssselect = 'SHOP'
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
            elif datahandled['property_type'] == "BIZ":
                linktxt = 'เชิงพาณิชย์'
                cssselect = 'BIZ'
            else:  # CONDO
                linktxt = 'คอนโด'
                cssselect = 'CONDO'
            WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("propertyTypeSelect")).click()
            time.sleep(0.1)
            WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_link_text(linktxt)).click()
            time.sleep(0.1)
            WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_css_selector("input[type='radio'][value='" + cssselect + "']")).click()
            time.sleep(0.1)
            # self.firefox.save_screenshot("debug_response/newp5.png")
            self.firefox.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)  # scroll to head page
            WebDriverWait(self.firefox, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app-listing-creation"]/div/div[2]/div/header/div/div/div[2]/div/a[2]/div[2]')))
            #self.firefox.save_screenshot("debug_response/newp33.png")
            nextbttn = WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_xpath('//*[@id="app-listing-creation"]/div/div[2]/div/header/div/div/div[2]/div/a[2]/div[2]'))
            self.firefox.execute_script("arguments[0].click();", nextbttn)

        return success, detail

    def inputpostdetail(self, datahandled):
        #log.debug('')

        success = "true"
        detail = ''
        post_id = ''
        account_type = "normal"

        # note ถ้าหากเป็นโครงการที่มีอยู่แล้ว จะมีจำนวนชั้นของตึกตามที่เว็บกำหนดมา ถ้า input floor total มามากกว่าจำนวนที่ web provide ให้ ก็จะใส่ไม่ได้

        # validate
        # CONDO,BUNG,TOWN,APT,BIZ,OFF,SHOP,WAR require พื้นที่ใช้สอย หัวข้อประกาศ (ไทย) รายละเอียดเกี่ยวกับประกาศ (ไทย)
        # LAND require ขนาดที่ดิน หัวข้อประกาศ (ไทย) รายละเอียดเกี่ยวกับประกาศ (ไทย)
        if datahandled['post_title_th'] == '' or datahandled['post_description_th'] == '':
            success = 'false'
            detail = 'post title th is and post description th required'
        if datahandled['property_type'] == 'CONDO' or datahandled['property_type'] == 'BUNG' or datahandled['property_type'] == 'TOWN' or datahandled['property_type'] == 'APT' or datahandled['property_type'] == 'OFF' or datahandled[
                'property_type'] == 'SHOP' or datahandled['property_type'] == 'BIZ':
            if datahandled['floor_area'] == None or datahandled['floor_area'] == '0':
                success = 'false'
                detail = 'floor area sqm is require and allow integer type only'
        if datahandled['property_type'] == 'LAND':
            if datahandled['land_size_rai'] == '0' and datahandled['land_size_ngan'] == '0' and datahandled['land_size_wa'] == '0':
                success = 'false'
                detail = 'property type land is require area data'
            # <=13 ตร.วา จะ error
            if datahandled['land_size_rai'] == '0' and datahandled['land_size_ngan'] == '0' and int(datahandled['land_size_wa']) <= 13:
                success = 'false'
                detail = 'property type land is require minimum >= 13 sqm'

        if success == 'true':
            # self.firefox.save_screenshot("debug_response/newp4.png")
            # WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_css_selector("input[type='radio'][id='listing-type-"+datahandled['listing_type']+"']")).find_element_by_tag_name('span').click()

            WebDriverWait(self.firefox, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'l-listing-create-basic')))
            self.firefox.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
            #self.firefox.save_screenshot("debug_response/newp44.png")

            # type
            #log.debug('input property type')
            if datahandled['listing_type'] == "SALE":
                element = WebDriverWait(self.firefox, 10).until(lambda x: x.find_element_by_id("listing-type-SALE"))
                self.firefox.execute_script("arguments[0].click();", element)
                #log.debug('input property type SALE')
            elif datahandled['listing_type'] == "RENT":
                element = WebDriverWait(self.firefox, 10).until(lambda x: x.find_element_by_id("listing-type-RENT"))
                self.firefox.execute_script("arguments[0].click();", element)                
                #log.debug('input property type RENT')
            else:
                element = WebDriverWait(self.firefox, 10).until(lambda x: x.find_element_by_id("listing-type-OPT"))
                self.firefox.execute_script("arguments[0].click();", element)  
                #log.debug('input property type OPT')
            #self.firefox.save_screenshot("debug_response/newp5.png")

            try:
                self.firefox.find_element_by_id("live-tour-radio-false").click()
            except:
                pass

            # price
            try:
                WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("input-listing-price")).send_keys(datahandled['price_baht'])
            except WebDriverException as e:
                #log.warning('cannot input price '+str(e))
                pass

            # bed room
            try:
                if datahandled['bed_room'] != None and datahandled['bed_room'].strip() != '' and int(datahandled['bed_room']) > 0:
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("bedRoomDropdown")).click()
                    if int(datahandled['bed_room']) >= 10:
                        WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_link_text('10+ ห้องนอน')).click()
                    else:
                        WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_link_text(str(datahandled['bed_room']) + ' ห้องนอน')).click()
            except WebDriverException as e:
                pass

            # bath room
            try:
                WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("bathRoomDropdown")).click()
                if datahandled['bath_room'] == None or datahandled['bath_room'].strip() == '' or int(datahandled['bath_room']) == 0:
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_link_text('ไม่มีห้องน้ำ')).click()
                elif int(datahandled['bath_room']) >= 1 and int(datahandled['bath_room']) < 9:
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_link_text(str(datahandled['bath_room']) + ' ห้องน้ำ')).click()
                else:
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_link_text('9 ห้องน้ำ')).click()
            except WebDriverException as e:
                #log.warning('cannot input bath room '+str(e))
                pass

            # floor area sqm
            try:
                if datahandled['action'] == 'edit_post':
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("input-floorarea_sqm")).send_keys(Keys.CONTROL + "a")  # clear for edit action
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("input-floorarea_sqm")).send_keys(Keys.DELETE)  # clear for edit action
                print(str(datahandled['floor_area']))
                WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("input-floorarea_sqm")).send_keys(str(datahandled['floor_area']))
            except WebDriverException as e:
                #log.warning('cannot input floor area sqm '+str(e))
                pass

            # total floor
            if datahandled['floor_total'] and str(datahandled['floor_total']).isdigit() and int(datahandled['floor_total']) > 0:
                try:
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("form-field-total-floor")).click()
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_link_text(str(datahandled['floor_total']))).click()
                except WebDriverException as e:
                    #log.warning('cannot input total floor '+str(e))
                    pass

            # floor position
            if datahandled['floor_level'] and str(datahandled['floor_level']).isdigit() and int(datahandled['floor_level']) > 0:
                try:
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("form-field-floorposition")).click()
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_link_text(str(datahandled['floor_level']))).click()
                except WebDriverException as e:
                    #log.warning('cannot input floor position '+str(e))
                    pass

            # title thai
            try:
                if datahandled['action'] == 'edit_post':
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("title-input")).send_keys(Keys.CONTROL + "a")  # clear for edit action
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("title-input")).send_keys(Keys.DELETE)
                WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("title-input")).send_keys(datahandled['post_title_th'])
                #log.debug('input title thai ')
            except WebDriverException as e:
                pass
                #log.warning('cannot input title thai '+str(e))

            # title en
            try:
                if datahandled['action'] == 'edit_post':
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("titleEn-input")).send_keys(Keys.CONTROL + "a")  # clear for edit action
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("titleEn-input")).send_keys(Keys.DELETE)  # clear for edit action
                WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("titleEn-input")).send_keys(datahandled['post_title_en'])
                #log.debug('input title en')
            except WebDriverException as e:
                pass
                #log.warning('cannot input title en '+str(e))
            #self.firefox.save_screenshot("debug_response/newp00.png")

            # desc thai
            try:
                if datahandled['action'] == 'edit_post':
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("description-th-input")).send_keys(Keys.CONTROL + "a")  # clear for edit action
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("description-th-input")).send_keys(Keys.DELETE)  # clear for edit action
                WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("description-th-input")).send_keys(datahandled['post_description_th'])
                #log.debug('input desc thai')
            except WebDriverException as e:
                pass
                #log.warning('cannot input desc thai '+str(e))
            #self.firefox.save_screenshot("debug_response/newp11.png")

            # desc en
            try:
                if datahandled['action'] == 'edit_post':
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("description-en-input")).send_keys(Keys.CONTROL + "a")  # clear for edit action
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("description-en-input")).send_keys(Keys.DELETE)  # clear for edit action
                WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("description-en-input")).send_keys(datahandled['post_description_en'])
                #log.debug('input desc en')
            except WebDriverException as e:
                pass
                #log.warning('cannot input post_description_en '+str(e))
            #self.firefox.save_screenshot("debug_response/newp22.png")

            # หันหน้าทางทิศ

            # try:
            #     element = WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_xpath('//*[@id="form-field-facing-type"]'))
            #     self.firefox.execute_script("arguments[0].click();", element)
            #     element = WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_link_text(str(datahandled['direction_type'])))
            #     self.firefox.execute_script("arguments[0].click();", element)
            #     #log.debug('input direction type')
            # except WebDriverException as e:
            #     #log.warning('cannot input direction type '+str(e))
            #     pass

            #self.firefox.save_screenshot("debug_response/newp33.png")

            # area
            # จะ auto calculate ให้ เช่น input เป็น rai 6.5 ngaan 5.4 sqw 4.3 จะคำนวณใหม่ให้เป็น 7ไร่ 3งาน 44.3ตรว
            try:
                if datahandled['action'] == 'edit_post':
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("input-landarea_rai")).send_keys(Keys.CONTROL + "a")  # clear for edit action
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("input-landarea_rai")).send_keys(Keys.DELETE)  # clear for edit action
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("input-landarea_ngaan")).send_keys(Keys.CONTROL + "a")  # clear for edit action
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("input-landarea_ngaan")).send_keys(Keys.DELETE)  # clear for edit action
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("input-landarea_sqw")).send_keys(Keys.CONTROL + "a")  # clear for edit action
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("input-landarea_sqw")).send_keys(Keys.DELETE)  # clear for edit action
                WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("input-landarea_rai")).send_keys(datahandled['land_size_rai'])
                WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("input-landarea_ngaan")).send_keys(datahandled['land_size_ngan'])
                WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("input-landarea_sqw")).send_keys(datahandled['land_size_wa'])
            except WebDriverException as e:
                pass

            # account type
            matchObj = re.search(r'รายละเอียดตัวแทน', self.firefox.page_source)
            if matchObj:
                account_type = 'corporate'
                try:
                    if datahandled['action'] == 'edit_post':
                        WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("corporate-name-field")).send_keys(Keys.CONTROL + "a")  # clear for edit action
                        WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("corporate-name-field")).send_keys(Keys.DELETE)  # clear for edit action
                        WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("input-corporate-mobile")).send_keys(Keys.CONTROL + "a")  # clear for edit action
                        WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("input-corporate-mobile")).send_keys(Keys.DELETE)  # clear for edit action
                        WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_css_selector("textarea[class='limit-text'][placeholder='ระบุหลายอีเมลล์ได้']")).send_keys(Keys.CONTROL + "a")
                        WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_css_selector("textarea[class='limit-text'][placeholder='ระบุหลายอีเมลล์ได้']")).send_keys(Keys.DELETE)
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("corporate-name-field")).send_keys(datahandled['name'])
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_id("input-corporate-mobile")).send_keys(datahandled['mobile'])
                    WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_css_selector("div[class='corporate-email-wrap']/textarea")).send_keys(datahandled['email'])
                    # WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_css_selector("textarea[class='limit-text'][placeholder='ระบุหลายอีเมลล์ได้']")).send_keys(datahandled['email'])
                except WebDriverException as e:
                    #log.warning('cannot input corporate data '+str(e))
                    print(e)
                    pass
            
            self.firefox.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)  # scroll to head page
            time.sleep(2)
            # next
            try:
                next_button = WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_class_name('step-next'))
                # self.firefox.execute_script("return arguments[0].scrollIntoView(true);", next_button)
                time.sleep(5)
                next_button.click()
            except WebDriverException as e:
                print('except 1')
                print(e)
                #log.debug('cannot click next , cause floor_area is too low OR price_baht is too low OR post_description_th,post_title_th not set '+str(e))
                success = 'false'
                detail = 'cannot click next , cause floor_area is too low OR price_baht is too low OR post_description_th,post_title_th not set OR account lacks credits'
                time.sleep(10)
                self.firefox.close()
                self.firefox.quit()
                try:
                    alert = self.firefox.switch_to.alert
                    alert.accept()
                    self.firefox.close()
                    self.firefox.quit()
                except:
                    pass
                return success, detail, post_id, account_type

            # image page
            time.sleep(5)
            WebDriverWait(self.firefox, 5).until(EC.presence_of_element_located((By.ID, 'tab-photo')))

            # ถ้า action edit และ ไม่มี รูปภาพส่งมาเลย ไม่ต้องทำอะไรกับรูปภาพ
            if (datahandled['action'] == 'edit_post' and len(datahandled['post_images']) < 0):
                #log.debug('edit image')
                imgdiv = WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_class_name("c-upload-file-grid"))
                imglis = imgdiv.find_elements_by_link_text("...")
                for imgli in imglis:
                    imgid = imgli.get_attribute("id")
                    if imgid != None:
                        imgli.click()
                        WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_link_text("ลบ")).click()
                        #log.debug('delete image')
                        alert = self.firefox.switch_to.alert
                        alert.accept()
                        time.sleep(1.5)

            # for img in datahandled['post_images']:
            #     time.sleep(1)
            #     WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_css_selector("input[accept='image/png,image/jpg,image/jpeg'][type='file']")).send_keys(os.path.abspath(img))
            #     #log.debug('post image %s', img)
            #     time.sleep(1)
            #     self.firefox.refresh()


            all_images = ""
            for count, pic in enumerate(datahandled['post_images']):
                if count < len(datahandled['post_images'])-1:
                    all_images += os.path.abspath(pic) + '\n'
                else:
                    all_images += os.path.abspath(pic)
        
            upload = WebDriverWait(self.firefox, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[accept='image/png,image/jpg,image/jpeg'][type='file']")))
            upload.send_keys(all_images)

            try:                  
                wait_upload = WebDriverWait(self.firefox, 60).until(EC.presence_of_element_located((By.XPATH, "//*[@id='step_media_photo']/div[1]/div[2]/ul/li["+str(len(datahandled['post_images']))+"]/div/div[2]/a")))
            except:
                pass




            #log.debug('image success')
            #print('here1')
            post_id = self.firefox.current_url.split("/")[-1]
            #log.debug('post post id %s', post_id)

            # next
            WebDriverWait(self.firefox, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app-listing-creation"]/div/div[2]/div/header/div/div/div[3]/div/div[2]/a')))
            WebDriverWait(self.firefox, 5).until(lambda x: x.find_element_by_xpath('//*[@id="app-listing-creation"]/div/div[2]/div/header/div/div/div[3]/div/div[2]/a')).click() 
            # self.firefox.save_screenshot("debug_response/newp10.png")
            time.sleep(1)
            #log.debug('click next')
            #print('here2')
            #TODO debug
            #js location inject
            if datahandled['action'] == 'edit_post':
                js = 'guruApp.createListing.listingData.listingDetail.result.location.latitude = ' + datahandled['geo_latitude'] + '; '
                js = js + 'guruApp.createListing.listingData.listingDetail.result.location.longitude = ' + datahandled['geo_longitude'] + '; '
                self.firefox.execute_script(js)
                time.sleep(0.5)
                js = 'guruApp.createListing.formData.map.lat = ' + datahandled['geo_latitude'] + '; '
                js = js + 'guruApp.createListing.formData.map.lng = ' + datahandled['geo_longitude'] + '; '
                self.firefox.execute_script(js)
                #print('here3')
                time.sleep(0.5)
            # debug jsalert = 'alert(guruApp.createListing.listingData.listingDetail.result.location.latitude + " " + guruApp.createListing.listingData.listingDetail.result.location.longitude)'
            # self.firefox.execute_script(jsalert)
            # time.sleep(1)
            #TODO debug
            
            if datahandled['action'] == 'edit_post':
                #บันทึกแล้วออก
                element = WebDriverWait(self.firefox, 10).until(lambda x: x.find_element_by_xpath('//*[@id="app-listing-creation"]/div/div[2]/div/header/div/div/div[3]/div/div[2]/button'))
                self.firefox.execute_script("arguments[0].click();", element)
                #quit      
                self.firefox.close()
                self.firefox.quit()
                try:
                    alert = self.firefox.switch_to.alert
                    alert.accept()
                    self.firefox.close()
                    self.firefox.quit()
                except:
                    pass
                return success, detail, post_id, account_type
            try:
                WebDriverWait(self.firefox, 15).until(lambda x: x.find_element_by_xpath('//*[@id="app-listing-creation"]/div/div[2]/div/section/div/div[1]/div/div/footer/div[1]/div[1]/button')).click()  # ลงประกาศ
                time.sleep(1.8)
            except WebDriverException:
                pass
            #print('here4')
            #log.debug('click publish')
            # self.firefox.save_screenshot("debug_response/newp11.png")

            # create post จะสำเร็จก็ต่อเมื่อ publish ได้ด้วย ถ้า editpost แค่ edit ได้ ก็ถือว่าสำเร็จ
            if datahandled['action'] == 'create_post':
                matchObj = re.search(r'Active Unit Listing quota exceeded', self.firefox.page_source)
                if matchObj:
                    success = "false"
                    detail = 'Active Unit Listing quota exceeded'
            #print('here5')
            #บันทึกแล้วออก
            try:
                element = WebDriverWait(self.firefox, 10).until(lambda x: x.find_element_by_xpath('//*[@id="app-listing-creation"]/div/div[2]/div/header/div/div/div[3]/div/div[2]/button'))
                self.firefox.execute_script("arguments[0].click();", element)
            except WebDriverException:
                pass
            #print('here6')
            #quit        
            self.firefox.close()
            self.firefox.quit()
            try:
                alert = self.firefox.switch_to.alert
                alert.accept()
                self.firefox.close()
                self.firefox.quit()
            except:
                pass
            # self.firefox.quit()
        print(success, detail, post_id, account_type)
        return success, detail, post_id, account_type


    def create_post_bak(self, postdata):
        #log.debug('')

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
            r = httprequestObj.http_get('https://services.propertyguru.com/v1/autocomplete?region=th&locale=th&limit=25&object_type=PROPERTY&query=' + datahandled['project_name'], verify=False)
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
                    "localizedTitle": datahandled['post_title_th'],
                    "description": datahandled['post_description_en'],
                    "localizedDescription": datahandled['post_description_th'],
                    "hasStream": "false",
                    "statusCode": "DRAFT",
                    "sourceCode": "",
                    "typeCode": datahandled['listing_type'],
                    "leaseTermCode": "",
                    "featureCode": "",
                    "externalId": '9999',
                    "event": "",
                    "location": {
                        "id": "626225",  # TODO ''
                        "block": "",
                        "unit": "",
                        "streetId": "",
                        "longitude": datahandled['geo_longitude'],
                        "latitude": datahandled['geo_latitude'],
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
                        "typeCode": datahandled['property_type'],
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
                            "text": ""
                        }
                    },
                    "sizes": {
                        "bedrooms": {
                            "value": datahandled['bed_room']
                        },
                        "bathrooms": {
                            "value": datahandled['bath_room']
                        },
                        "extrarooms": {
                            "value": ""
                        },
                        "floorArea": [{
                            "value": datahandled['floor_area'],
                            "unit": "sqm"
                        }],
                        "landArea": [{
                            "value": "",
                            "unit": "sqm"
                        }],
                        "floorX": [{
                            "unit": "m",
                            "value": ""
                        }],
                        "floorY": [{
                            "unit": "m",
                            "value": ""
                        }],
                        "landX": [{
                            "unit": "m",
                            "value": ""
                        }],
                        "landY": [{
                            "unit": "m",
                            "value": ""
                        }]
                    },
                    "agent": {
                        "id": agent_id,
                        "alternativePhone": "",
                        "alternativeAgent": datahandled['name'],
                        "alternativeMobile": datahandled['mobile'],
                        "alternativeEmail": datahandled['email']
                    },
                    "hasFloorplans": "false",
                    "boost": {
                        "boostActive": "false",
                        "boostDuration": 0
                    },
                    "dates": {
                        "timezone": "Asia/Singapore",
                        "available": ""
                    },
                    "descriptions": {
                        "th": datahandled['post_description_th']
                    },
                    "qualityScore": 0,
                    "localizedHeadline": "",
                    "headlines": {
                        "th": ""
                    },  # TODO short_post_title_th
                    "titles": {
                        "th": datahandled['post_title_th']
                    }
                }
                datastr = json.dumps(datapost)
                r = httprequestObj.http_post_json('https://agentnet.ddproperty.com/sf2-agent/ajax/listings', jsoncontent=datastr)
                data = r.text
                #f = open("debug_response/postdd.html", "wb")
                #f.write(data.encode('utf-8').strip())
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
            "post_url": "https://www.ddproperty.com/preview-listing/" + post_id if post_id != "" else "",
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
        }

    def boost_post(self, postdata):
        #log.debug('')

        time_start = datetime.datetime.utcnow()

        # start process
        #
        datahandled = self.postdata_handle(postdata)

        # login
        test_login = self.test_login(datahandled)
        success = test_login["success"]
        detail = test_login["detail"]
        agent_id = test_login["agent_id"]
      #log.debug('')
        
        try:
            if success == "true":
                # datapost = {
                #     "listing_id[]": datahandled['post_id'],
                #     "statusCode": "ACT",
                #     "expectedCredits[]": 0,
                # }

                self.firefox.get("https://agentnet.ddproperty.com/listing_management#ACT")
                search = self.firefox.find_element_by_id("listingId")
                search.send_keys(datahandled['post_id'])
                search.send_keys(Keys.ENTER)
                time.sleep(3)

                try:
                    all_rows = self.firefox.find_element_by_id('list-container')
                    myrow = all_rows.find_element_by_class_name('listing-item')
                    try:
                        iden = "listing-item-"+ datahandled['post_id'] +"-performance"
                        item_perform = self.firefox.find_element_by_id(iden)
                        perform_detail = item_perform.find_elements_by_class_name('component-listing-performance-detail-stats')
                        post_view = perform_detail[1].text.split(' ')[0]
                    except:
                        post_view = ""                      
                    try:
                        renew_input = myrow.find_elements_by_class_name('listingIdCheckbox')
                        if renew_input[0].get_attribute('data-list-id') == datahandled['post_id']:
                            renew_input[0].click()
                            WebDriverWait(self.firefox, 5).until(EC.presence_of_element_located((By.ID, 'bulkRepost'))).click()
                            time.sleep(5)
                            cssvalue = self.firefox.find_element_by_id('layerNotAllowToExtendListing').get_attribute('style')
                            time.sleep(1)
                            if cssvalue == '':
                                success = "true"
                                detail = "Post Renewed Successfully."                    
                            else:
                                success = "false"
                                detail = "This post already renewed in this week."                    
                        else:
                            success = "false"
                            detail = "Invalid Post Id."
                    except:
                        success = "false"
                        detail = "Can not detect element to renew post."
                except:
                    success = "false"
                    detail = "Can not detect element in thee page.."
        finally:
            # pass
            self.firefox.quit()

            # r = httprequestObj.http_post_with_headers('https://agentnet.ddproperty.com/repost_listing', datapost)
            # print(r.content)
            # print(r.status_code)
            # print(r.url)
            # datajson = r.json()
            #f = open("debug_response/ddboostpostresponse.html", "wb")
            #f.write(data.encode('utf-8').strip())
            # if datajson['status'] != 0:
            #     success = 'false'
            #     detail = datajson['message']

            #
            # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {"success": success, "usage_time": str(time_usage), "start_time": str(time_start), "end_time": str(time_end), "detail": detail, "log_id": datahandled['log_id'], "post_id": datahandled['post_id'], "websitename": self.websitename, "post_view": post_view}

    def delete_post(self, postdata):
        #log.debug('')

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
            detail = 'Post deleted successfully'
            matchObj = re.search(r'message":"deleted', data)
            if matchObj:
                # ใกล้ความจริง แต่จะ delete สำเร็จหรือไม่มันก็ return deleted หมด ดังนั้นต้องเช็คจาก post id อีกทีว่า response 404 ป่าว
                r = httprequestObj.http_get('https://agentnet.ddproperty.com/create-listing/detail/' + post_id, verify=False)
                data = r.text
                # f = open("debug_response/dddelete.html", "wb")
                # f.write(data.encode('utf-8').strip())
                if (r.status_code == 200):
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
            "websitename": self.websitename,
        }

    def edit_post_bak(self, post_id,datahandled):
        #log.debug('')

        # start proces
        #

        # login
        test_login = self.test_login_httpreq(datahandled)
        success = test_login["success"]
        detail = test_login["detail"]
        agent_id = test_login["agent_id"]

        if (success == "true"):
            datapost = {
                "id": post_id,
                # "statusCode": "DRAFT",
                # "daysUntilExpire": 0,
                # "isExpiring": "true",
                # "sourceCode": "",
                "typeCode": "SALE",
                # "typeText": "ขาย",
                # "subTypeCode": "",
                # "leaseTermCode": "",
                # "leaseTermText": "",
                # "featureCode": "",
                # "accountTypeCode": "NORMAL",
                # "accountSubTypeCode": "",
                # "isPremiumAccount": "false",
                # "isPropertySpecialistListing": "false",
                # "isMobilePropertySpotlightListing": "false",
                # "isTransactorListing": "false",
                # "isCommercial": "false",
                # "hasFloorplans": "false",
                # "hasStream": "true",
                # "featuredBy": [],
                # "localizedHeadline": "",
                # "headlines": {
                #     "th": "",
                #     "en": ""
                # },
                # "localizedTitle": post_title_th,
                # "titles": {
                #     "th": post_title_th
                # },
                # "localizedDescription": post_description_th,
                # "descriptions": {
                #     "th": post_description_th
                # },
                # "notes": "",
                # "externalId": 9999,
                # "cobroke": 0,
                # "price": {
                #     "value": 9999999,
                #     "pretty": "฿9,999,999",
                #     "periodCode": "",
                #     "pricePerArea": {
                #         "value": 227272.7045,
                #         "unit": "sqm",
                #         "reference": "floorArea"
                #     },
                #     "type": {
                #         "code": "BAH",
                #         "text": "",
                #         "pretty": "บาท"
                #     },
                #     "valuation": 0,
                #     "valuationText": "",
                #     "completed": 0,
                #     "currency": "฿"
                # },
                # "sizes": {
                #     "bedrooms": {
                #         "value": "",
                #         "text": ""
                #     },
                #     "bathrooms": {
                #         "value": "",
                #         "text": ""
                #     },
                #     "extrarooms": {
                #         "value": "",
                #         "text": ""
                #     },
                #     "floorArea": [{
                #         "unit": "sqm",
                #         "value": 44,
                #         "text": "44 ตร.ม."
                #     }],
                #     "landArea": [{
                #         "unit": "sqm",
                #         "value": "",
                #         "text": ""
                #     }],
                #     "floorX": [{
                #         "unit": "m",
                #         "value": ""
                #     }],
                #     "floorY": [{
                #         "unit": "m",
                #         "value": ""
                #     }],
                #     "landX": [{
                #         "unit": "m",
                #         "value": ""
                #     }],
                #     "landY": [{
                #         "unit": "m",
                #         "value": ""
                #     }]
                # },
                # "pricePerArea": {
                #     "floorArea": [{
                #         "unit": "sqm",
                #         "value": 227272.70454545,
                #         "text": "฿227,273 / ตารางเมตร"
                #     }],
                #     "landArea": [{
                #         "unit": "",
                #         "value": "",
                #         "text": ""
                #     }]
                # },
                # "dates": {
                #     "timezone": "Asia/Singapore",
                #     "firstPosted": "",
                #     "lastPosted": "",
                #     "expiry": "",
                #     "available": "",
                #     "created": {
                #         "date": "2020-03-11 01:14:38",
                #         "unix": 1583860478
                #     },
                #     "updated": {
                #         "date": "2020-03-11 01:14:38",
                #         "unix": 1583860478
                #     }
                # },
                # "urls": {
                #     "listing": {
                #         "api": "https://api.propertyguru.com/v1/listings/7788091?region=th",
                #         "internal": "http://listing.guruestate.com/v1/listings/7788091?region=th",
                #         "mobile": "https://www.ddproperty.com/property/xxx-ขาย-7788091",
                #         "desktop": "https://www.ddproperty.com/property/xxx-ขาย-7788091",
                #         "desktopByLocales": {
                #             "th": "https://www.ddproperty.com/property/xxx-ขาย-7788091",
                #             "en": "https://www.ddproperty.com/en/property/xxx-for-sale-7788091"
                #         },
                #         "preview": {
                #             "desktop": "https://www.ddproperty.com/preview-listing/7788091"
                #         }
                #     }
                # },
                # "_user": "",
                # "qualityScore": 70,
                # "finalScore": "",
                # "tier": 0,
                # "showAgentProfile": "false",
                # "event": "",
                # "mywebOrder": "",
                # "agent": {
                #     "id": agent_id,
                #     "name": "cccc cccc",
                #     "mobile": "+66839703921",
                #     "mobilePretty": "+66 83 970 3921",
                #     "phone": "",
                #     "phonePretty": "",
                #     "alternativePhone": "",
                #     "alternativeAgent": "",
                #     "alternativeMobile": "",
                #     "alternativeEmail": "",
                #     "jobTitle": "",
                #     "licenseNumber": "",
                #     "showProfile": "false",
                #     "website": "",
                #     "email": "kla.arnut@gmail.com",
                #     "blackberryPin": ""
                # },
                # "agency": {
                #     "id": 42297,
                #     "name": "aaaa",
                #     "ceaLicenseNumber": ""
                # },
                "location": {
                    "latitude": 13.8749,
                    "longitude": 100.413606,
                    # "distance": "",
                    # "regionCode": "TH12",
                    # "regionText": "นนทบุรี",
                    # "regionSlug": "นนทบุรี",
                    # "districtCode": "TH1203",
                    # "districtText": "บางใหญ่",
                    # "districtSlug": "บางใหญ่",
                    # "areaCode": "11",
                    # "areaText": "",
                    # "areaSlug": "",
                    # "fullAddress": ". ถนนรัตนาธิเบศร์ ตำบลเสาธงหิน อำเภอบางใหญ่ นนทบุรี, บางใหญ่, นนทบุรี",
                    # "hdbEstateCode": "",
                    # "hdbEstateText": "",
                    # "postalCode": "11110",
                    # "block": "",
                    # "unit": "",
                    # "streetId": "",
                    # "streetName1": "ถนนรัตนาธิเบศร์ ตำบลเสาธงหิน อำเภอบางใหญ่ นนทบุรี",
                    # "streetName2": "",
                    # "streetNumber": ".",
                    # "zoneIds": "",
                    # "subZoneIds": ""
                },
                # "property": {
                #     "id": 5987,
                #     "temporaryId": "",
                #     "statusCode": "6DML",
                #     "name": "Plum condo central station เฟส 1",
                #     "typeCode": "CONDO",
                #     "typeText": "คอนโด",
                #     "typeGroup": "N",
                #     "tenureCode": "F",
                #     "tenureText": "ขายขาด",
                #     "topMonth": 10,
                #     "topYear": 2018,
                #     "developer": "Pruksa Real Estate - พฤกษา เรียลเอสเตท จำกัด (มหาชน)",
                #     "totalUnits": 1208,
                #     "floors": 38,
                #     "amenities": [{
                #         "code": "CCAR"
                #     }, {
                #         "code": "CTV"
                #     }, {
                #         "code": "FIT"
                #     }, {
                #         "code": "OCAR"
                #     }, {
                #         "code": "PDEC"
                #     }, {
                #         "code": "SAUNA"
                #     }, {
                #         "code": "SEC"
                #     }, {
                #         "code": "SPA"
                #     }, {
                #         "code": "STE"
                #     }, {
                #         "code": "SWI"
                #     }, {
                #         "code": "WAD"
                #     }]
                # },
                # "propertyUnit": {
                #     "id": 7989636,
                #     "description": "",
                #     "furnishingCode": "",
                #     "furnishingText": "",
                #     "hdbTypeCode": "",
                #     "floorplanId": -1,
                #     "floorLevelCode": "",
                #     "floorLevelText": "",
                #     "floorPosition": "",
                #     "cornerUnit": "",
                #     "facingCode": "",
                #     "occupancyCode": "",
                #     "electricitySupply": "",
                #     "electricityPhase": "",
                #     "ceilingHeight": "",
                #     "floorLoading": "",
                #     "garages": "",
                #     "parkingSpaces": "",
                #     "parkingFees": "",
                #     "maintenanceFee": {
                #         "value": 0,
                #         "pretty": "฿0.00",
                #         "periodeCode": "MONTH"
                #     },
                #     "liftCargo": "",
                #     "liftPassenger": "",
                #     "liftCapacity": "",
                #     "centralAircon": "",
                #     "centralAirconHours": "",
                #     "ownerTypeCode": "",
                #     "sellerEthnic": "",
                #     "sellerResidency": "",
                #     "quotaEthnic": "true",
                #     "quotaSpr": "true",
                #     "telephoneLines": "",
                #     "features": [],
                #     "tenancy": {
                #         "value": "UNTENANTED",
                #         "tenantedUntilDate": {}
                #     },
                #     "tenureCode": "F"
                # },
                # "media": {
                #     "cover": {
                #         "id": 61330097,
                #         "caption": "",
                #         "statusCode": "CONF",
                #         "suspReason": "",
                #         "appealComment": "",
                #         "appealSent": "false",
                #         "sortOrder": 61330097,
                #         "V150": "https://th2-cdn.pgimgs.com/property/5987/PPHO.61330097.V150/Plum-condo-central-station-%E0%B9%80%E0%B8%9F%E0%B8%AA-1-%E0%B8%9A%E0%B8%B2%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88-Thailand.jpg",
                #         "V550": "https://th2-cdn.pgimgs.com/property/5987/PPHO.61330097.V550/Plum-condo-central-station-%E0%B9%80%E0%B8%9F%E0%B8%AA-1-%E0%B8%9A%E0%B8%B2%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88-Thailand.jpg"
                #     },
                #     "listing": [],
                #     "property": [{
                #         "id": 61330097,
                #         "caption": "",
                #         "statusCode": "CONF",
                #         "suspReason": "",
                #         "appealComment": "",
                #         "appealSent": "false",
                #         "sortOrder": 61330097,
                #         "V150": "https://th2-cdn.pgimgs.com/property/5987/PPHO.61330097.V150/Plum-condo-central-station-%E0%B9%80%E0%B8%9F%E0%B8%AA-1-%E0%B8%9A%E0%B8%B2%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88-Thailand.jpg",
                #         "V550": "https://th2-cdn.pgimgs.com/property/5987/PPHO.61330097.V550/Plum-condo-central-station-%E0%B9%80%E0%B8%9F%E0%B8%AA-1-%E0%B8%9A%E0%B8%B2%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88-Thailand.jpg"
                #     }, {
                #         "id": 61330098,
                #         "caption": "",
                #         "statusCode": "CONF",
                #         "suspReason": "",
                #         "appealComment": "",
                #         "appealSent": "false",
                #         "sortOrder": 61330098,
                #         "V150": "https://th1-cdn.pgimgs.com/property/5987/PPHO.61330098.V150/Plum-condo-central-station-%E0%B9%80%E0%B8%9F%E0%B8%AA-1-%E0%B8%9A%E0%B8%B2%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88-Thailand.jpg",
                #         "V550": "https://th1-cdn.pgimgs.com/property/5987/PPHO.61330098.V550/Plum-condo-central-station-%E0%B9%80%E0%B8%9F%E0%B8%AA-1-%E0%B8%9A%E0%B8%B2%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88-Thailand.jpg"
                #     }, {
                #         "id": 61330099,
                #         "caption": "",
                #         "statusCode": "CONF",
                #         "suspReason": "",
                #         "appealComment": "",
                #         "appealSent": "false",
                #         "sortOrder": 61330099,
                #         "V150": "https://th2-cdn.pgimgs.com/property/5987/PPHO.61330099.V150/Plum-condo-central-station-%E0%B9%80%E0%B8%9F%E0%B8%AA-1-%E0%B8%9A%E0%B8%B2%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88-Thailand.jpg",
                #         "V550": "https://th2-cdn.pgimgs.com/property/5987/PPHO.61330099.V550/Plum-condo-central-station-%E0%B9%80%E0%B8%9F%E0%B8%AA-1-%E0%B8%9A%E0%B8%B2%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88-Thailand.jpg"
                #     }, {
                #         "id": 61330104,
                #         "caption": "",
                #         "statusCode": "CONF",
                #         "suspReason": "",
                #         "appealComment": "",
                #         "appealSent": "false",
                #         "sortOrder": 61330104,
                #         "V150": "https://th1-cdn.pgimgs.com/property/5987/PPHO.61330104.V150/Plum-condo-central-station-%E0%B9%80%E0%B8%9F%E0%B8%AA-1-%E0%B8%9A%E0%B8%B2%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88-Thailand.jpg",
                #         "V550": "https://th1-cdn.pgimgs.com/property/5987/PPHO.61330104.V550/Plum-condo-central-station-%E0%B9%80%E0%B8%9F%E0%B8%AA-1-%E0%B8%9A%E0%B8%B2%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88-Thailand.jpg"
                #     }],
                #     "agent":
                #     "",
                #     "agentLogo": [],
                #     "agencyLogo": [],
                #     "excluded": [],
                #     "included": [],
                #     "listingDocuments": [],
                #     "propertyFloorplans": [],
                #     "listingFloorplans": [],
                #     "listingSiteplans": [],
                #     "listingVideos": [],
                #     "listingVirtualTours": []
                # },
                # "metas": {
                #     "title": "Xxx, . ถนนรัตนาธิเบศร์ ตำบลเสาธงหิน อำเภอบางใหญ่ นนทบุรี, บางใหญ่, นนทบุรี, 44 ตร.ม., คอนโด ขาย, โดย Cccc Cccc, ฿9,999,999, 7788091",
                #     "description": "ดูรายละเอียด, รูปภาพ และแผนที่ของประกาศอสังหาริมทรัพย์ 7788091 - ขาย - xxx - . ถนนรัตนาธิเบศร์ ตำบลเสาธงหิน อำเภอบางใหญ่ นนทบุรี, บางใหญ่, นนทบุรี, 44 ตร.ม., ฿9,999,999",
                #     "keywords": "ตัวแทน, ประกาศ, อสังหาริมทรัพย์, ทรัพย์สิน, ขาย, เช่า, อพาร์ทเม้นท์, บ้าน, ชาวต่างชาติ, ที่อยู่อาศัย, hdb, สถานที่ตั้ง, คอนโด, แผนที่"
                # },
                # "alertBatchId": "",
                # "unitTypes": [],
                # "qualityScoreData": {
                #     "price": 50,
                #     "location": 10,
                #     "3_user_photos": 0,
                #     "1_user_photo": 0,
                #     "videos_or_virtual_tours": 0,
                #     "bedrooms": 0,
                #     "description": 0,
                #     "bathrooms": 0,
                #     "floorarea": 5,
                #     "landarea": 3,
                #     "property": 1,
                #     "furnishing": 0,
                #     "unit_features": 0,
                #     "property_photo": 1,
                #     "raw_score": 70,
                #     "score": 70
                # },
                # "dependencyErrors": [],
                # "isRankedSpotlight": "false",
                # "isFeaturedListing": "false"
            }
            datastr = json.dumps(datapost)
            # print(datastr)
            r = httprequestObj.http_put_json('https://agentnet.ddproperty.com/sf2-agent/ajax/update/' + post_id, jsoncontent=datastr)
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

        return {"success": success}

    def edit_post(self, postdata):
        #log.debug('')

        time_start = datetime.datetime.utcnow()

        # start proces
        #

        datahandled = self.postdata_handle(postdata)

        # login
        test_login = self.test_login(datahandled)
        success = test_login["success"]
        detail = test_login["detail"]

        if (success == "true"):
            self.firefox.get('https://agentnet.ddproperty.com/create-listing/detail/' + str(datahandled['post_id']))
            #log.debug('search post id %s', str(datahandled['post_id']))
            # self.firefox.save_screenshot("debug_response/edit1.png")
            matchObj = re.search(r'500 Internal Server Error', self.firefox.page_source)
            if matchObj:
                success = 'false'
                detail = 'not found ddproperty post id ' + datahandled['post_id']
            if success == 'true':
                self.firefox.get('https://agentnet.ddproperty.com/create-listing/location/' + str(datahandled['post_id']))
                #log.debug('go to edit post %s', str(datahandled['post_id']))
                time.sleep(0.5)
                WebDriverWait(self.firefox, 5).until(EC.presence_of_element_located((By.ID, "propertySearch")))
                success, detail = self.inputpostgeneral(datahandled)
                if success == 'true':
                    success, detail, post_id, account_type = self.inputpostdetail(datahandled)

        #log.debug('edit post done')
        #
        # end process
        try:
            self.firefox.quit()
        except:
            pass

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {"success": success, "usage_time": str(time_usage), "start_time": str(time_start), "end_time": str(time_end), "detail": detail, "log_id": datahandled['log_id'], "websitename": self.websitename}

    def search_post(self,postdata):

        time_start = datetime.datetime.utcnow()

        datahandled = self.postdata_handle(postdata)


        # login
        test_login = self.test_login(datahandled)
        success = test_login["success"]
        detail = test_login["detail"]
        post_found = 'false'
        post_url = ''
        post_id = ''
        if (success == "true"):


            valid_ids = []
            valid_titles = []
            valid_urls = []
            flag = True
            page = 1
            while flag == True:

                url = 'https://agentnet.ddproperty.com/listing_management_data'
                data = {
                    'statusCode': 'ACT',
                    'params[listingSubTypeCode]': 'ALL',
                    'params[tierType]': 'ALL',
                    'params[propertyId]': '0',
                    'params[propertyType]': 'ALL',
                    'params[listType]': 'ALL',
                    'params[page]': str(page),
                    'params[featStatusCode]': 'CUR',
                    'params[limit]': '20',
                    'params[listingId]':'',
                    'sort[column]': 'end_date',
                    'sort[direction]': 'DESC'
                }
                page += 1
                headers = {
                    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
                }
                req = httprequestObj.http_get(url,data=data,headers=headers)

                soup = BeautifulSoup(req.text,'html.parser')
                print(soup.prettify())
                check = soup.find('div',{'id':'list-container'})
                print(check)
                if check is not None:
                    #print('here2')
                    posts = soup.find_all('div',{'class':'listing-item'})

                    for post in posts:
                        valid_ids.append(post['data-listing-id'])
                        valid_titles.append(post['data-listing-title'])
                        url = post.find('a')
                        valid_urls.append(url['href'])
                    #print(valid_ids)
                else:
                    flag = False



            if datahandled['post_title_th'] in valid_titles:
                post_found = 'true'
                for i in range(len(valid_titles)):
                    if valid_titles[i] == datahandled['post_title_th']:
                        post_url = valid_urls[i]
                        post_id = valid_ids[i]



        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        # print(f"{valid_ids}\n\n{valid_urls}\n\n{valid_titles}")
        res = {
            'success':success,
            'post_id':postdata['post_id'],
            'log_id':postdata['log_id'],
            'ds_id':postdata['ds_id'],
            'websitename': 'ddproperty',
            'start_time':str(time_start),
            'end_time':str(time_end),
            'usage_time':str(time_usage),
            'post_url':post_url,
            'account_type': '',
            'post_found':post_found,
            'post_create_time': '',
            'post_modify_time': '',
            'post_view': '',
            'detail':detail
        }
        return res
