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


class proppit():

    name = 'proppit'

    def __init__(self):

        try:
            import configs

        except ImportError:
            configs = {}

        self.httprequestObj = lib_httprequest()
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

        r = self.httprequestObj.http_post(url, data=json.dumps(datapost), headers=headers)
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
        if 'line' in postdata:
            recdata['contactLine'] = postdata['line']
        else:
            recdata['contactLine'] = None
        if 'property_id' in postdata:
            recdata['referenceId'] = postdata['property_id']
        else:
            recdata['referenceId'] = None

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

        temp = {}
        if (postdata['post_title_en'] == "") or (postdata['post_title_en'] is None):
            temp['text'] = ' '
        else:
            temp['text'] = postdata['post_title_en']
        
        temp['locale'] = "en-US"
        recdata['titleMultiLanguage'].append(temp)

        recdata['descriptionMultiLanguage'] = [{}]

        recdata['descriptionMultiLanguage'][0]['text'] = postdata['post_description_th']
        recdata['descriptionMultiLanguage'][0]['locale'] = "th-TH"
        
        temp = {}
        if (postdata['post_description_en'] == "") or (postdata['post_description_en'] is None):
            temp['text'] = ' '
        else:
            temp['text'] = postdata['post_description_en']
        temp['locale'] = "en-US"
        recdata['descriptionMultiLanguage'].append(temp)

        recdata['bathrooms'] = None
        recdata['bedrooms'] = postdata['bed_room']
        if postdata['bath_room'] == '':
            recdata['toilets'] = None
        else:
            recdata['toilets'] = postdata['bath_room']

        area = ['land_size_rai','land_size_ngan','land_size_wa']
        for i in area:
            if (i not in postdata) or (postdata[i] == ''):
                postdata[i] = 0
            else:
                postdata[i] = int(postdata[i])
        area_sqm = (postdata['land_size_rai'] * 1600)+(postdata['land_size_ngan'] * 400)+(postdata['land_size_wa'] * 4)

        if recdata['propertyType'] == "land":
            #recdata['plotAreaSqm'] = area_sqm
            recdata['floorArea'] = None
            recdata['plotArea'] = [{"value":postdata['land_size_rai'],"unit":"rai"},{"value":postdata['land_size_ngan'],"unit":"ngan"},{"value":postdata['land_size_wa'],"unit":"sqw"}]
        else:
            recdata['plotAreaSqm'] = None
            recdata['floorArea'] = area_sqm
        recdata['usableArea'] = postdata['floorarea_sqm']

        if ('floor_level' not in postdata) or (postdata['floor_level'] == ''):
            postdata['floor_level'] = postdata['floor_total']
        recdata['floor'] = postdata['floor_level']

        recdata['rules'] = []
        recdata['locationVisibility'] = "accurate"

        recdata['contactEmails'] = [postdata['email']]
        recdata['contactPhone'] = postdata['mobile']

        recdata['contactWhatsApp'] = None
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

        r = self.httprequestObj.http_get("https://api.proppit.com/property-geolocations/coordinates?latitude="+ postdata['geo_latitude'] +"&longitude="+ postdata['geo_longitude'])
        ret = json.loads(r.text)

        recdata['placeId'] = ret['data']['placeId']
        recdata['address'] = ret['data']['address']
        recdata['geoLevels'] = ret['data']['geoLevels']

        recdata['published'] = True

        recdata['amenities'] = []
        recdata['project'] = None
        if 'web_project_name' not in postdata:
            if 'project_name' in postdata:
                postdata['web_project_name'] = postdata['project_name']
            else:
                postdata['web_project_name'] = ''
        if (postdata['web_project_name'] is None) or (postdata['web_project_name'] == ''):
            pass
        else:
            r = self.httprequestObj.http_get("https://api.proppit.com/project-suggestions?query=" + postdata['web_project_name'])
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
        detail = ''
        post_url = ''
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
            WebDriverWait(driver, 30).until(lambda x: x.find_element_by_id("email")).send_keys(postdata['user'])
            WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("password")).send_keys(postdata['pass'])
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Log in']"))).click()
            except:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='เข้าสู่ระบบ']"))).click()

            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div[1]/nav/div/div[3]/a"))).click()
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div[1]/div/div/a"))).click()
            
            WebDriverWait(driver, 30).until(lambda x: x.find_element_by_xpath("//input[@class='MuiInputBase-input MuiInput-input jss7 jss10']")).send_keys(postdata['email'])
            #driver.find_element_by_xpath("//input[@class='MuiInputBase-input MuiInput-input jss7 jss10']").send_keys(postdata['email'])
            driver.find_element_by_xpath("//input[@data-test='p-title-main']").send_keys(postdata['post_title_th'])
            driver.find_element_by_xpath("//input[@data-test='p-contact-phone']").send_keys(Keys.CONTROL + "a")
            driver.find_element_by_xpath("//input[@data-test='p-contact-phone']").send_keys(Keys.DELETE)
            driver.find_element_by_xpath("//input[@data-test='p-contact-phone']").send_keys(postdata['mobile'])
            driver.find_element_by_xpath("//textarea[@data-test='p-description-main']").send_keys(postdata['post_description_th'])

            driver.find_element_by_xpath("//input[@data-test='p-address']").send_keys('กรุงเทพมหานคร')
            time.sleep(4)

            driver.find_element_by_xpath("//input[@data-test='p-address']").send_keys(Keys.ARROW_DOWN)
            driver.find_element_by_xpath("//input[@data-test='p-address']").send_keys(Keys.ENTER)
            time.sleep(3)

            find_submit = driver.find_element_by_name("publish").click()
            time.sleep(5)
            try:
                popup = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("confirmation-dialog-title")).text
                print(popup=='อัปเกรดแพ็กเกจของคุณเพื่อ Boost ประกาศได้มากขึ้น')
                if popup=='อัปเกรดแพ็กเกจของคุณเพื่อ Boost ประกาศได้มากขึ้น':
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/div/div[2]/button"))).click()
            except:
                pass
            post_url = ''
            num_web= 5
            for i in range(num_web):
                try:
                    url = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div/div[3]/div/div/div[1]/table/tbody/tr[1]/td[2]/div/div[2]/span/a[{}]'.format(i+1)))
                except:
                    url = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div/div[3]/div/div/div[1]/table/tbody/tr[1]/td[1]/div/div[2]/span/a[{}]'.format(i+1)))
                post_url += url.get_attribute('href')
                if i+1 != num_web:
                    post_url += '|'
            gen_id_bool = True
                
        finally:
            driver.close()
            driver.quit()

        return {
            'gen_id_bool':gen_id_bool,
            'post_url':post_url,
            'detail':detail
        }

    def sort_date_id(self):
        last_id = ""

        url = "https://api.proppit.com/properties"
        r = self.httprequestObj.http_get(url)
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

                r = self.httprequestObj.http_post(url, data=payload , files=files)

                if (r.status_code == 200) or (r.status_code == 201):
                    success = "true"
                    detail = "Post created successfully!"
                    #post_url = "https://proppit.com/properties/"+ post_id +"/edit"
                    post_url = gen_id['post_url']
                    post_id = post_id
                else:
                    success = "false"
                    detail = "Post failed!" + r.text
            else:
                success = "false"
                detail = "cannot login."
        else:
            success = "false"
            detail = gen_id['detail']

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
        #post_url = "https://proppit.com/properties/"+ post_id +"/edit"

        test_login = self.test_login(postdata)
        try:
            search_post = self.search_post(postdata)
            post_url = search_post['post_url']
        except:
            post_url = ''
        if test_login["success"] == 'true':
            temp_payload, files = self.payload_data(postdata,'edit',post_id)
            payload = {'ad': json.dumps(temp_payload)}

            url = "https://api.proppit.com/properties"

            r = self.httprequestObj.http_post(url, data=payload , files=files)
            
            if (r.status_code == 200) or (r.status_code == 201):
                success = "true"
                detail = "Post edit successfully!"
                #post_url = "https://proppit.com/properties/"+ post_id +"/edit"
                #post_url = search_post['post_url']
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
            WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("email")).send_keys(postdata['user'])
            WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("password")).send_keys(postdata['pass'])
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Log in']"))).click()
            except:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='เข้าสู่ระบบ']"))).click()
            time.sleep(5)
            driver.get("https://proppit.com/properties")
            search_field = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div/div[2]/div[1]/div/div/div[1]/div/div/div/input'))
            search_field.send_keys(postdata['property_id'])
            search_field.send_keys(Keys.ENTER)
            time.sleep(5)
            try:
                post_url = ''
                num_web= 5
                for i in range(num_web):
                    url = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div/div[3]/div/div/div[1]/table/tbody/tr[1]/td[2]/div/div/span/a[{}]'.format(i+1)))
                    post_url += url.get_attribute('href')
                    if i+1 != num_web:
                        post_url += '|'
                """post_url += (driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div/div[3]/div/div/div[1]/table/tbody/tr[1]/td[2]/div/div/span/a[2]').get_attribute('href'))+'|'
                post_url += (driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div/div[3]/div/div/div[1]/table/tbody/tr[1]/td[2]/div/div/span/a[3]').get_attribute('href'))+'|'
                post_url += (driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div/div[3]/div/div/div[1]/table/tbody/tr[1]/td[2]/div/div/span/a[4]').get_attribute('href'))+'|'
                post_url += (driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div/div[3]/div/div/div[1]/table/tbody/tr[1]/td[2]/div/div/span/a[5]').get_attribute('href'))"""
            except:
                detail = "No post found with given title."
        finally:
            driver.close()
            driver.quit()
        test_login = self.test_login(postdata)

        if test_login["success"] == 'true':
            url = "https://api.proppit.com/properties"

            r = self.httprequestObj.http_get(url)

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