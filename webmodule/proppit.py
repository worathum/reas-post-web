from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
import re
import json
import datetime
import sys
import requests
import shutil
from urllib.parse import unquote
from requests_toolbelt.multipart.encoder import MultipartEncoder
import math
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

httprequestObj = lib_httprequest()

class proppit():

    name = 'proppit'

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

    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')

        time_start = datetime.datetime.utcnow()

        success = "false"
        detail = "can't connect to login."

        datapost = {
            "email": postdata['user'],
            "password": postdata['pass'],
        }

        headers = {"Content-type": "application/json"}
        url = "https://api.proppit.com/login"

        r = httprequestObj.http_post(url, data=json.dumps(datapost), headers=headers)
        ret = json.loads(r.text)

        if r.status_code == 200:
            success = "true"
            detail = "success login"
        else:
            success = "false"
            detail = "failed login"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "websitename": "proppit",
            "success": success,
            "detail": detail,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "usage_time": str(time_usage),
            "ds_id": postdata['ds_id']
        }

    def payload_data(self, postdata, pay_type, post_id):
        recdata = {}

        recdata['id'] = post_id

        recdata['operations'] = [{}]

        if postdata['listing_type'] == "ขาย":
            recdata['operations'][0]['type'] = "sell"
        else:
            recdata['operations'][0]['type'] = "rent"

        recdata['operations'][0]['price'] = {}

        recdata['operations'][0]['price']['amount'] = int(postdata["price_baht"])
        recdata['operations'][0]['price']['currency'] = "THB"

        if postdata['property_type'] == "1":
            recdata['propertyType'] = "condo"
        elif postdata['property_type'] == "2":
            recdata['propertyType'] = "house"
        elif postdata['property_type'] == "3":
            recdata['propertyType'] = "house"
        elif postdata['property_type'] == "4":
            recdata['propertyType'] = "townhouse"
        elif postdata['property_type'] == "5":
            recdata['propertyType'] = "commercial"
        elif postdata['property_type'] == "6":
            recdata['propertyType'] = "land"
        elif postdata['property_type'] == "7":
            recdata['propertyType'] = "apartment"
        elif postdata['property_type'] == "8":
            recdata['propertyType'] = "commercial"
        elif postdata['property_type'] == "9":
            recdata['propertyType'] = "office"
        elif postdata['property_type'] == "10":
            recdata['propertyType'] = "industrial unit"
        elif postdata['property_type'] == "25":
            recdata['propertyType'] = "industrial unit"

        recdata['titleMultiLanguage'] = [{}]

        recdata['titleMultiLanguage'][0]['text'] = postdata['post_title_th']
        recdata['titleMultiLanguage'][0]['locale'] = "th-TH"

        if (postdata['post_title_en'] == "") or (postdata['post_title_en'] is None):
            pass
        else:
            temp = {}
            temp['text'] = postdata['post_title_en']
            temp['locale'] = "en-US"

            recdata['titleMultiLanguage'].append(temp)

        recdata['descriptionMultiLanguage'] = [{}]

        recdata['descriptionMultiLanguage'][0]['text'] = postdata['post_description_th']
        recdata['descriptionMultiLanguage'][0]['locale'] = "th-TH"

        if (postdata['post_description_en'] == "") or (postdata['post_description_en'] is None):
            pass
        else:
            temp = {}
            temp['text'] = postdata['post_description_en']
            temp['locale'] = "en-US"

            recdata['descriptionMultiLanguage'].append(temp)

        recdata['bathrooms'] = postdata['bath_room']
        recdata['bedrooms'] = postdata['bed_room']
        recdata['toilets'] = None
        
        recdata['plotArea'] = None
        recdata['floorArea'] = postdata['floorarea_sqm']
        recdata['usableArea'] = postdata['floorarea_sqm']

        recdata['floor'] = postdata['floor_level']

        recdata['rules'] = []
        recdata['locationVisibility'] = "accurate"

        recdata['contactEmails'] = [postdata['email']]
        recdata['contactPhone'] = postdata['mobile']

        recdata['contactWhatsApp'] = None
        recdata['contactLine'] = None
        recdata['contactFacebookMessenger'] = None
        recdata['contactViber'] = None
        recdata['furnished'] = None
        recdata['ownership'] = None
        recdata['stratum'] = None
        
        date_now = (datetime.datetime.now()) - (datetime.timedelta(hours=7))
        recdata['creationDate'] = str(date_now.isoformat())

        recdata['video'] = ""
        recdata['nearbyLocations'] = []

        recdata['constructionYear'] = None
        recdata['tenureInYears'] = None
        recdata['communityFeesAmount'] = None
        recdata['tenure'] = None

        recdata['coordinates'] = {}
        recdata['coordinates']['latitude'] = postdata['geo_latitude']
        recdata['coordinates']['longitude'] = postdata['geo_longitude']

        recdata['communityFeesCurrency'] = "THB"
        recdata['mainImageIndex'] = 0

        recdata['propertyImages'] = []
        for i in range(0,len(postdata['post_images'])):
            temp = {}
            temp['ref'] = i
            recdata['propertyImages'].append(temp)

        r = httprequestObj.http_get("https://api.proppit.com/property-geolocations/coordinates?latitude="+ postdata['geo_latitude'] +"&longitude="+ postdata['geo_longitude'])
        ret = json.loads(r.text)

        recdata['placeId'] = ret['data']['placeId']
        recdata['address'] = ret['data']['address']
        recdata['geoLevels'] = ret['data']['geoLevels']

        recdata['published'] = True

        recdata['amenities'] = []
        recdata['project'] = None

        if (postdata['web_project_name'] is None) or (postdata['web_project_name'] == ''):
            pass
        else:
            r = httprequestObj.http_get("https://api.proppit.com/project-suggestions?query=" + postdata['web_project_name'])
            ret = json.loads(r.text)

            if len(ret['data']) == 0:
                pass
            else:
                check_project = False
                for data_t in ret['data']:
                    if postdata['web_project_name'].lower() in data_t['name'].lower():
                        if check_project == False:
                            recdata['project'] = {}
                            recdata['project']['id'] = data_t['id']
                            recdata['project']['name'] = data_t['name']
                            recdata['amenities'] = data_t['amenities']
                            check_project = True

        files = []
        for i in range(0,len(postdata['post_images'])):
            femp = ('propertyImagesToBeUploaded['+ str(i) +']',(postdata['post_images'][i].split('/')[-1],open(os.getcwd() + '/' + postdata['post_images'][i],'rb'),'image/jpeg'))
            files.append(femp)
        
        return (recdata,files)

    def gen_id(self, postdata):
        gen_id_bool = False
        
        path = './static/chromedriver'
        options = Options()

        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('start-maximized')
        options.add_argument('disable-infobars')
        options.add_argument("--disable-extensions")
        options.add_argument("disable-gpu")
        options.add_argument("window-size=1920,1080")

        driver = webdriver.Chrome(executable_path=path, options=options)

        try:
            driver.get("https://proppit.com/login")
            time.sleep(2)

            driver.find_element_by_id('email').send_keys(postdata['user'])
            driver.find_element_by_id('password').send_keys(postdata['pass'])
            time.sleep(1)

            try:
                find_login = driver.find_element_by_xpath("//span[text()='Log in']").click()
            except:
                find_login = driver.find_element_by_xpath("//span[text()='เข้าสู่ระบบ']").click()
            time.sleep(2)

            driver.get("https://proppit.com/properties/new-property")
            time.sleep(2)

            driver.find_element_by_xpath("//input[@class='MuiInputBase-input MuiInput-input jss7 jss10']").send_keys(postdata['email'])
            driver.find_element_by_xpath("//input[@data-test='p-title-main']").send_keys(postdata['post_title_th'])
            driver.find_element_by_xpath("//input[@data-test='p-contact-phone']").send_keys(Keys.CONTROL + "a")
            driver.find_element_by_xpath("//input[@data-test='p-contact-phone']").send_keys(Keys.DELETE)
            driver.find_element_by_xpath("//input[@data-test='p-contact-phone']").send_keys(postdata['mobile'])
            driver.find_element_by_xpath("//textarea[@data-test='p-description-main']").send_keys(postdata['post_description_th'])

            driver.find_element_by_xpath("//input[@data-test='p-address']").send_keys('กรุงเทพมหานคร')
            time.sleep(4)

            driver.find_element_by_xpath("//input[@data-test='p-address']").send_keys(Keys.ARROW_DOWN)
            driver.find_element_by_xpath("//input[@data-test='p-address']").send_keys(Keys.ENTER)
            time.sleep(2)

            find_submit = driver.find_element_by_xpath("//span[text()='บันทึก และ เผยแพร่ประกาศ']").click()
            time.sleep(5)
            post_url = ''
            post_url += (driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div/div[3]/div/div/div[1]/table/tbody/tr[1]/td[2]/div/div/span/a[1]').get_attribute('href'))+'|'
            post_url += (driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div/div[3]/div/div/div[1]/table/tbody/tr[1]/td[2]/div/div/span/a[2]').get_attribute('href'))+'|'
            post_url += (driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div/div[3]/div/div/div[1]/table/tbody/tr[1]/td[2]/div/div/span/a[3]').get_attribute('href'))+'|'
            post_url += (driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div/div[3]/div/div/div[1]/table/tbody/tr[1]/td[2]/div/div/span/a[4]').get_attribute('href'))+'|'
            post_url += (driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div/div[3]/div/div/div[1]/table/tbody/tr[1]/td[2]/div/div/span/a[5]').get_attribute('href'))
            gen_id_bool = True
        finally:
            driver.close()
            driver.quit()

        return {
            'gen_id_bool':gen_id_bool,
            'post_url':post_url
        }

    def sort_date_id(self):
        last_id = ""

        url = "https://api.proppit.com/properties"
        r = httprequestObj.http_get(url)
        ret = json.loads(r.text)

        sort_date = []
        for ret_t in ret['data']:
            temp = datetime.datetime.strptime(ret_t['date'], "%Y-%m-%dT%H:%M:%SZ")
            sort_date.append(temp)

        sort_date = sorted(sort_date)

        for ret_t in ret['data']:
            if sort_date[-1] == datetime.datetime.strptime(ret_t['date'], "%Y-%m-%dT%H:%M:%SZ"):
                last_id = ret_t['id']

        return last_id
            
    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')

        time_start = datetime.datetime.utcnow()

        success = "false"
        detail = "can't connect to create."

        post_url = ""
        post_id = ""

        gen_id = self.gen_id(postdata)

        if gen_id['gen_id_bool'] == True:
            test_login = self.test_login(postdata)
            if test_login["success"] == 'true':
                post_id = self.sort_date_id()

                temp_payload, files = self.payload_data(postdata,'create',post_id)
                payload = {'ad': json.dumps(temp_payload)}

                url = "https://api.proppit.com/properties"+"/"+post_id

                r = httprequestObj.http_post(url, data=payload , files=files)
                
                if (r.status_code == 200) or (r.status_code == 201):
                    success = "true"
                    detail = "Post created successfully!"
                    #post_url = "https://proppit.com/properties/"+ post_id +"/edit"
                    post_url = gen_id['post_url']
                    post_id = post_id
                else:
                    success = "false"
                    detail = "Post failed!"
            else:
                success = "false"
                detail = "cannot login."
        else:
            success = "false"
            detail = "cannot gen new id."

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "websitename": "proppit",
            "success": success,
            "detail": detail,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "usage_time": str(time_usage),
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "null"
        }

    def edit_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')

        time_start = datetime.datetime.utcnow()

        success = "false"
        detail = "can't connect to edit."

        post_id = postdata['post_id']
        post_url = "https://proppit.com/properties/"+ post_id +"/edit"

        test_login = self.test_login(postdata)
        search_post = self.search_post(postdata)
        if test_login["success"] == 'true':
            temp_payload, files = self.payload_data(postdata,'edit',post_id)
            payload = {'ad': json.dumps(temp_payload)}

            url = "https://api.proppit.com/properties"

            r = httprequestObj.http_post(url, data=payload , files=files)
            
            if (r.status_code == 200) or (r.status_code == 201):
                success = "true"
                detail = "Post edit successfully!"
                #post_url = "https://proppit.com/properties/"+ post_id +"/edit"
                post_url = search_post['post_url']
                post_id = post_id
            else:
                success = "false"
                detail = "Edit failed!"
                post_url = ""
                post_id = ""
        else:
            success = "false"
            detail = "cannot login."

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "websitename": "proppit",
            "success": success,
            "detail": detail,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "usage_time": str(time_usage),
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "null"
        }

    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')

        time_start = datetime.datetime.utcnow()

        req = requests.Session()

        success = "false"
        detail = "can't connect to delete."

        datapost = {
            "email": postdata['user'],
            "password": postdata['pass'],
        }

        headers = {"Content-type": "application/json"}
        url = "https://api.proppit.com/login"

        test_login = req.post(url, data=json.dumps(datapost), headers=headers)
        
        if test_login.status_code == 200:
            url = "https://api.proppit.com/properties/" + postdata['post_id']
            
            r = req.delete(url)
            
            if r.status_code == 200:
                success = "true"
                detail = "post deleted successfully."
            else:
                success = "false"
                detail = "cannot delete."
        else:
            success = "false"
            detail = "cannot login."

        req.close()

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "websitename": "proppit",
            "success": success,
            "detail": detail,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "usage_time": str(time_usage),
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": postdata['post_id']
        }

    def search_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')

        time_start = datetime.datetime.utcnow()

        success = "false"
        detail = "can't connect to search."

        post_id = ""
        post_url = ""
        post_modify_time = ""
        post_view = ""
        post_found = "false"
        exists = False
        path = './static/chromedriver'
        options = Options()

        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('start-maximized')
        options.add_argument('disable-infobars')
        options.add_argument("--disable-extensions")
        options.add_argument("disable-gpu")
        options.add_argument("window-size=1920,1080")

        driver = webdriver.Chrome(executable_path=path, options=options)

        try:
            driver.get("https://proppit.com/login")
            time.sleep(2)

            driver.find_element_by_id('email').send_keys(postdata['user'])
            driver.find_element_by_id('password').send_keys(postdata['pass'])
            time.sleep(1)

            try:
                find_login = driver.find_element_by_xpath("//span[text()='Log in']").click()
            except:
                find_login = driver.find_element_by_xpath("//span[text()='เข้าสู่ระบบ']").click()
            time.sleep(2)
            driver.get("https://proppit.com/properties")
            time.sleep(2)
            driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div/div[2]/div[1]/div/div/div[1]/div/div/div/input').send_keys(postdata['post_title_th'])
            driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div/div[2]/div[1]/div/div/div[1]/div/div/div/input').send_keys(Keys.ENTER)
            post_url = ''
            post_url += (driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div/div[3]/div/div/div[1]/table/tbody/tr[1]/td[2]/div/div/span/a[1]').get_attribute('href'))+'|'
            post_url += (driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div/div[3]/div/div/div[1]/table/tbody/tr[1]/td[2]/div/div/span/a[2]').get_attribute('href'))+'|'
            post_url += (driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div/div[3]/div/div/div[1]/table/tbody/tr[1]/td[2]/div/div/span/a[3]').get_attribute('href'))+'|'
            post_url += (driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div/div[3]/div/div/div[1]/table/tbody/tr[1]/td[2]/div/div/span/a[4]').get_attribute('href'))+'|'
            post_url += (driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div/div[3]/div/div/div[1]/table/tbody/tr[1]/td[2]/div/div/span/a[5]').get_attribute('href'))
        finally:
            driver.close()
            driver.quit()
        test_login = self.test_login(postdata)

        if test_login["success"] == 'true':
            url = "https://api.proppit.com/properties"

            r = httprequestObj.http_get(url)

            if r.status_code == 200:
                success = "true"

                ret = json.loads(r.text)
                for ret_t in ret['data']:
                    if exists == False:

                        for ret_t_multiland in ret_t['titleMultiLanguage']:
                            if ret_t_multiland['text'] == postdata['post_title_th']:
                                exists = True

                        if exists == True:
                            post_id = ret_t['id']
                            #post_url = "https://proppit.com/properties/"+ ret_t['id'] +"/edit"
                            post_modify_time = ret_t['date']

                            post_found = "true"
                            detail = "post found successfully"

                if exists == False:
                    post_found = "false"
                    detail = "No post found with given title."

            else:
                success = "false"
                detail = "can't get data"

        else:
            success = "false"
            detail = "cannot login."


        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "websitename": "proppit",
            "success": success,
            "detail": detail,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "usage_time": str(time_usage),
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "post_url": post_url,
            "post_modify_time": post_modify_time,
            "post_view": post_view,
            "post_found": post_found,
            "account_type": "null"
        }

    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')

        time_start = datetime.datetime.utcnow()

        success = "true"
        detail = "no boost option."

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "websitename": "proppit",
            "success": success,
            "detail": detail,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "usage_time": str(time_usage),
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": postdata['post_id'],
            "post_view": ""
        }

    def print_debug(self, msg):
        if(self.debug == 1):
            print(msg)
        return "true"

    def print_debug_data(self, data):
        if(self.debugdata == 1):
            print(data)
        return "true"

        if(self.debugdata == 1):
            print(data)
        return "true"