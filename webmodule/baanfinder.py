# -*- coding: utf-8 -*-

from selenium.webdriver.common import action_chains
from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
import hashlib
# from urlparse import urlparse
import re
import json
import datetime
import time
import sys
import requests
import calendar
import shutil
from urllib.parse import unquote

# =================== Selenium imports for upload image =====================


from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import os

import undetected_chromedriver.v2 as uc

# ===========================================================================

httprequestObj = lib_httprequest()

class baanfinder():

    name = 'baanfinder'

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
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }

    def logout_user(self):
        url = 'https://www.baanfinder.com/logout'
        httprequestObj.http_get(url)


    def register_user(self, postdata):
        self.logout_user()
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        register_data = postdata

        datapost = {
            'displayName': register_data['name_th'] + " " + register_data['surname_th'],
            'email': register_data['user'],
            'password': register_data['pass'],
            'passwordConfirmation': register_data['pass'],
            'isAgent': 'true'
        }

        url = 'https://www.baanfinder.com/signup'
        r = httprequestObj.http_get(url, headers=self.headers)
        soup = BeautifulSoup(r.content, 'lxml')
        datapost['authenticityToken'] = soup.find('input', attrs={'name': 'authenticityToken'})['value']

        r = httprequestObj.http_post(url, data=datapost, headers = self.headers)
        data = r.text
        # print(data)

        success = "true"
        detail = ""

        if data.find("ขออภัยมีคนสมัครด้วยอีเมล์นี้แล้วค่") != -1:
            success = "false"
            detail = "Email Already registered"
        elif data.find("อีเมล์ไม่ถูกต้อง") != -1:
            success = "false"
            detail = "Invalid email"
        else:
            detail = "Successfully Registered. Check For Verification Email."
        # #
        # # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            'ds_id': postdata['ds_id'],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": "baanfinder",
        }

    def test_login(self, postdata):
        self.logout_user()
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        success = "true"
        detail = "Login Successful"

        options = uc.ChromeOptions()
        #options.headless = True
        self.driver = uc.Chrome('./static/chromedriver', options=options)
        #driver = webdriver.Chrome('./static/chromedriver', options=options)

        self.driver.get('https://www.baanfinder.com/login')

        """ driver.save_screenshot('debug_response/1.png')
        print(postdata) """
        email = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.ID,'username')))
        email.send_keys(postdata['user'])

        password = WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.ID,'password')))
        password.send_keys(postdata['pass'])

        login = WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.ID,'js-login-submit')))
        login.click()

        try:
            check_login = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,'alert.alert-success')))
            if 'เข้าสู่ระบบเรียบร้อยแล้ว' in check_login.text:
                print('testpass1')
                success = 'true'
                detail = 'login success'
            else:
                print('not pass')
                success = 'false'
                detail = 'maybe web is change'
        except:
            print('loginfailed')
            success = 'false'
            detail = 'login false'
        finally:
            if postdata['action'] == 'test_login':
                self.driver.close()
                self.driver.quit()
        # end processlogin
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": postdata['ds_id'],
            "detail": detail,
            "websitename": "baanfinder",
        }
        

    def check_post(self, postid):
        post_id = postid
        url = "https://www.baanfinder.com/me/my-properties"
        r = httprequestObj.http_get(url, headers=self.headers)
        exists = False
        soup = BeautifulSoup(r.content, 'lxml')
        authenticityToken = soup.find('input', attrs={'name': 'authenticityToken'})['value']

        post_entry_div = None
        for entry in soup.find_all('div', attrs={'class':'resEntry'}):
            id_div = entry.find('div', attrs={'class':'res-urlId'})
            if id_div is not None and str(post_id) in id_div.text:
                exists = True
                post_entry_div = entry

        post_title = ""
        if exists:
            post_title = post_entry_div.find('div', attrs={'class':'resTitle row'}).find('a')['title']

        return exists, authenticityToken, post_title

    def get_project_name_id(self,postdata, project_name):

        login = self.test_login(postdata)

        response = httprequestObj.http_get('https://www.baanfinder.com/api/search/projects/alphabet?search='+project_name, headers = self.headers)
        project_id = ""
        for project in json.loads(response.content):
            if project['text'] == project_name:
                project_id = project['id']
        return project_id

    def dict_data(self, postdata, field):
        fieldData = ""
        if field in postdata and postdata[field] is not None:
            fieldData = str(postdata[field])
        return fieldData

    def make_post_data(self, postdata):
        prop_type_map = {
            "1":"CONDOMINIUM",
            "2":"HOUSE",
            "3":"TWIN_HOUSE",
            "4":"TOWNHOUSE",
            "5":"SHOPHOUSE",
            "6":"LAND",
            "7":"APARTMENT",
            "8":"HOTEL",
            "9":"OFFICE",
            "10":"FACTORY",
            "25":"FACTORY"
        }

        direction_type_map = {
            "00":"NORTH",
            "01":"EAST",
            "10":"WEST",
            "11":"SOUTH"
        }

        adType = "RENT"
        if postdata["listing_type"] != "เช่า":
            adType = "SALE"

        try:
            if(self.dict_data(postdata, "direction_type") == ""):
                direction = ""

            else:
                direction = direction_type_map[self.dict_data(postdata, "direction_type")]
        except:
            direction = ""

        datapost = {
            "res.ownershipStatus": "IS_AGENT",
            "res.adTypes": adType,
            "res.type": prop_type_map[str(postdata["property_type"])],
            "res.name": self.dict_data(postdata, "post_title_th")[:99],
            "res.enName": self.dict_data(postdata, "post_title_en")[:99],
            "residenceGroupId": '',
            "res.price": postdata["price_baht"],
            "res.priceUnit": "BAHT",
            "res.priceRent": postdata["price_baht"],
            "res.priceRentUnit": "BAHT",
            "res.priceDownPaymentResale": "",
            "res.minimumRentalContractMonths": "",
            "res.refId": self.dict_data(postdata, "property_id"),
            "res.bedrooms": self.dict_data(postdata, "bed_room"),
            "res.bathrooms": self.dict_data(postdata, "bath_room"),
            "res.carSpaces": "",
            "res.area": self.dict_data(postdata, "floor_area"),
            "res.landAreaRai": self.dict_data(postdata, "land_size_rai"),
            "res.landAreaNgan": self.dict_data(postdata, "land_size_ngan"),
            "res.landAreaWaSq": self.dict_data(postdata, "land_size_wa"),
            "res.totalFloors": self.dict_data(postdata, "floor_total"),
            "res.floorNumbering": self.dict_data(postdata, "floor_level"),
            "res.isNewProperty": "false",
            "constructionCompletedDate": "",
            "res.facingDirection": direction ,
            "res.feeDeposit": "",
            "res.feeAdvancePayment": "",
            "res.feeElectricity": "",
            "res.feeWater": "",
            "res.feePhone": "",
            "res.feeInternet": "",
            "res.feeParking": "",
            "res.detailedInfo": self.dict_data(postdata, "post_description_th"),
            "res.enDetailedInfo": self.dict_data(postdata, "post_description_en"),
            "res.youtubeVideoId": "",
            "res.howToFind": self.dict_data(postdata, "addr_near_by")[:450],
            "res.address": self.dict_data(postdata, "addr_soi") + "\r\n" + self.dict_data(postdata, "addr_road") + "\r\n" + self.dict_data(postdata, "addr_sub_district") + "\r\n" + self.dict_data(postdata, "addr_district") + "\r\n" + self.dict_data(postdata, "addr_province") + "\r\n",
            "res.enAddress": "",
            "res.province": self.dict_data(postdata, "addr_province"),
            "res.lat": self.dict_data(postdata, "geo_latitude"),
            "res.lng": self.dict_data(postdata, "geo_longitude"),
            # "file": "",
            # "photoIds": [
            #     "36lz15k1hr",
            #     "8j7nsdh51w",
            #     "j0b2w97rr7",
            #     "gwrb37bgw5"
            # ],
            "res.promotionType": "",
            "res.promotionStartDate": "",
            "res.promotionEndDate": "",
            "res.promotionDetails": "",
            "res.enPromotionDetails": "",
            "res.contactName": self.dict_data(postdata, "name"),
            "res.contactPhoneNumber": self.dict_data(postdata, "mobile"),
            "res.contactEmail": self.dict_data(postdata, "email"),
            "res.contactLineId": self.dict_data(postdata, "line"),
            "isPublished": "true",
            # "upload_ref": [
            #     "image/private/v1589970940/ppiunp8x6nhxwj3dz2j4.jpg#c5a06f1d004107acec702657db21233f50e17b19",
            #     "image/private/v1589970940/lloyygvdyjgnqnahxjah.jpg#27eeddb906ae7ca5e777392cf017c039a3c76c65",
            #     "image/private/v1589970940/qwyccx9kq37qgwesmnkc.jpg#1d6d45c863f34d7ba87146622aa4548748288ea7",
            #     "image/private/v1589970940/mojnzzgyyepudpkr27af.jpg#246098b2854e1200bf6fd8f74e79d5828334cda1",
            # ]
        }

        #print(datapost)

        if datapost["res.adTypes"] == "RENT":
            datapost["res.price"] = ""
        else:
            datapost["res.priceRent"] = ""

        for i in datapost:
            if datapost[i] == None:
                datapost[i] = ""

        return datapost

    def match_addr(self, addrToMatch, field, soup):
        addr_word = ""

        a = soup.find('select', attrs={'name': 'res.province'})
        for i in a.find_all('option'):
            try:
                if addrToMatch == i['value']:
                    addr_word = i['value']
            except:
                pass

        if addr_word == '':
            for i in a.find_all('option'):
                try:
                    if addrToMatch in i['value'] or i['value'] in addrToMatch:
                        addr_word = i['value']
                except:
                    pass

        return addr_word


    def upload_images(self, postdata, post_id):

        image_paths = []

        images_req = postdata['post_images']

        for i in range(len(images_req)):
            image_paths.append(os.getcwd() + "/" + images_req[i])

        image_paths = image_paths[:5]
        options = Options()
        options.set_headless(True)
        options.add_argument('--no-sandbox')

        driver = webdriver.Chrome("./static/chromedriver", chrome_options=options)
        wait = WebDriverWait(driver, 30)

        url = 'https://www.baanfinder.com/login'
        driver.get(url)
        username_input = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/main/div[2]/div/div[1]/div/div[1]/form/div[1]/div/input")))
        username_input.send_keys(postdata['user'])
        password_input = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/main/div[2]/div/div[1]/div/div[1]/form/div[2]/div/input")))
        password_input.send_keys(postdata['pass'])
        current_url = driver.current_url
        driver.find_element_by_id('js-login-submit').click()
        #time.sleep(5)
        WebDriverWait(driver, 15).until(EC.url_changes(current_url))
        #url = "https://www.baanfinder.com/property/"+str(post_id)+"_"+postdata['post_title_th']+"/edit"
        url = "https://www.baanfinder.com/th/property/" + str(post_id) + "/edit"
        driver.get(url)        
        #print(url)

        sub_dis = wait.until(EC.presence_of_element_located((By.ID, 'sublocality')))
        sub_dis = Select(sub_dis)
        try:
            sub_dis.select_by_value(postdata['addr_sub_district'])
        except:
            sub_dis.select_by_index(1)

        #choose_files_button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/main/form/div/div[3]/div[22]/div[1]/div[1]/label")))
        choose_files_button = wait.until(EC.presence_of_element_located((By.ID, "photos")))

        # upload_string = ''
        # for i in image_paths:
        #     upload_string += i
        #     upload_string += "\n"
        #
        # upload_string = upload_string[:-2] + 'g'
        # print(upload_string)

        for upload_string in image_paths:

            driver.find_element_by_id('file').send_keys(upload_string)
            iterations = 0
            progress_bar = driver.find_element_by_class_name('progress-bar')
            # print(progress_bar.get_attribute(("style")))
            while (progress_bar.get_attribute("style") != "width: 100%;"):
                time.sleep(5)
                iterations += 1

                if (iterations == 10):
                    break
            time.sleep(2)

        # for i in image_paths:
        #     # print(i)
        #     choose_files_button.click()
        #     time.sleep(0.5)
        #     # driver.find_element_by_tag_name('body').send_keys(i + Keys.ENTER)
        #     driver.switch_to.active_element.send_keys(i)
        #     driver.implicitly_wait(10)
        #     # actions.send_keys(i + Keys.ENTER)
        #     # actions.perform()
        #     time.sleep(2)



        #time.sleep(10)
        # submit_button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/main/form/div/div[5]/button")))
        # submit_button.click()
        #print("done")

        # wait.until(EC.presence_of_element_located((By.ID, "file")))
        # image_file = driver.find_element_by_id('file')
        # print(image_file)
        # image_file.send_keys(image_paths[0])
        # driver.find_elements_by_class_name('cloudinary-fileupload').send_keys(image_paths[0])
        # time.sleep(10)

        current_url = driver.current_url
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, 'js-acceptAgentOrCoAgentTrue'))).click()
        submit_button = wait.until(EC.presence_of_element_located((By.ID, "res-publish-btn")))
        submit_button.click()
        WebDriverWait(driver, 15).until(EC.url_changes(current_url))
        driver.close()

    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # login
        test_login = self.test_login(postdata)
        #print(test_login)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""

        if success == "true":
            time_start = datetime.datetime.utcnow()
            #Go to create post form
            self.driver.get('https://www.baanfinder.com/th/new?ref=my-properties')
            #Select agent type
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'js-is-agent'))).click()
            except:
                self.driver.quit()
                time_end = datetime.datetime.now()
                time_usage = time_end - time_start
                return {
                    "success": False,
                    "usage_time": str(time_usage),
                    "start_time": str(time_start),
                    "end_time": str(time_end),
                    "post_url": '',
                    "post_id": '',
                    "account_type": "null",
                    "detail": 'คุณยังไม่ได้ยืนยันอีเมลล์ หรือบัญชีของท่านลงประกาศครบ 10 ประกาศแล้ว',
                    "websitename": "baanfinder",
                }
            #Select listing type
            if postdata['listing_type'] == 'ขาย':
                sel_type = 'sale'
            elif postdata['list_type'] == 'เช่า':
                sel_type = 'rent'
            else:
                sel_type = 'ขาย'
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, sel_type))).click()
            #Select property type
            prop_type_map = {
                "1": 4,     #CONDOMINIUM    -> '
                "2": 1,     #HOUSE          -> '
                "3": 2,     #TWIN_HOUSE     -> '
                "4": 3,     #TOWNHOUSE      -> '
                "5": 6,     #SHOPHOUSE      -> '
                "6": 9,     #LAND           ->No project
                "7": 5,     #APARTMENT      ->No project
                "8": 11,    #HOTEL          ->No project
                "9": 7,     #OFFICE         -> '
                "10": 10,   #FACTORY        ->No project
                "25": 10    #FACTORY        ->No project
            }
            sel_proptype = prop_type_map[postdata['property_type']]
            select_proptype = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'res.type')))
            select_proptype.click()
            select_proptype.find_elements_by_tag_name('option')[sel_proptype].click()
            #Post title th and en
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'res_name'))).send_keys(postdata['post_title_th'])
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'res_enName'))).send_keys(postdata['post_title_en'])
            #Select Project
            if postdata['property_type'] != '6' and postdata['property_type'] != '7' and postdata['property_type'] != '8' and postdata['property_type'] != '10' and postdata['property_type'] != '25':
                #Select project
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'select2-js-resGroup-container'))).click()
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'select2-search__field'))).send_keys(postdata['project_name'])
                type_ul = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'select2-js-resGroup-results')))
                time.sleep(3)
                type_li =  type_ul.find_elements_by_tag_name('li')[0]
                print(type_li.text)
                if type_li.text == 'ไม่พบข้อมูล':
                    self.driver.quit()
                    time_end = datetime.datetime.now()
                    time_usage = time_end - time_start
                    return {
                        "success": False,
                        "usage_time": str(time_usage),
                        "start_time": str(time_start),
                        "end_time": str(time_end),
                        "post_url": '',
                        "post_id": '',
                        "account_type": "null",
                        "detail": 'ไม่เจอโครงการที่ท่านต้องการจะลงประกาศ',
                        "websitename": "baanfinder",
                    }
                else:
                    type_li.click()
            #Post price
            if postdata['listing_type'] == 'ขาย':
                price_ele = 'js-price-sale'
            else:
                price_ele = 'js-price-rent'
            chck_price = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, price_ele))).send_keys(postdata['price_baht'].replace(',',''))
            print("-------------")
            print(chck_price)

            #Detail
            #For condominium
            if postdata['property_type'] == '1' :
                #Bath room
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'res_floorNumbering'))).send_keys(postdata['floor_level'])
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'res_totalFloors'))).send_keys(postdata['floor_total'])
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'res_area'))).send_keys(postdata['floor_area'])
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'res_bathrooms'))).send_keys(postdata['bath_room'])
                bed_room = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="js-bedroom-section"]/div/div/span')))
                bed_room.click()
                bed_put = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/span[2]/span/span[1]/input')))
                bed_put.send_keys(postdata['bed_room'])
                bed_put.send_keys(Keys.ENTER)
                post_detail = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.ID, 'additionalDetails')))
                post_detail[0].send_keys(postdata['post_description_th'])
                post_detail[1].send_keys(postdata['post_description_th'])            
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'res_howToFind'))).send_keys(postdata['addr_near_by'])
                address = postdata['addr_sub_district'] + ' ' + postdata['addr_district'] + ' ' + postdata['addr_province']
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'address'))).send_keys(address)

            #for apartment
            elif postdata['property_type'] == '7' :
                self.driver.quit()
                time_end = datetime.datetime.now()
                time_usage = time_end - time_start
                return {
                    "success": False,
                    "usage_time": str(time_usage),
                    "start_time": str(time_start),
                    "end_time": str(time_end),
                    "post_url": '',
                    "post_id": '',
                    "account_type": "null",
                    "detail": 'The propertytype of this website is on the maintance period',
                    "websitename": "baanfinder",
                }

            
            #for house,twinhouse,townhouse,shophouse,office
            elif postdata['property_type'] == '2' or postdata['property_type'] == '3' or postdata['property_type'] == '4' or postdata['property_type'] == '5' or postdata['property_type'] == '9':
                #Bath room
                #WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'res_floorNumbering'))).send_keys(postdata['floor_level'])
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'res_totalFloors'))).send_keys(postdata['floor_total'])
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'res_area'))).send_keys(postdata['floor_area'])
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'res_bathrooms'))).send_keys(postdata['bath_room'])
                bed_room = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="js-bedroom-section"]/div/div/span')))
                bed_room.click()
                bed_put = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/span[2]/span/span[1]/input')))
                bed_put.send_keys(postdata['bed_room'])
                bed_put.send_keys(Keys.ENTER)
                post_detail = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.ID, 'additionalDetails')))
                post_detail[0].send_keys(postdata['post_description_th'])
                post_detail[1].send_keys(postdata['post_description_th'])            
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'res_howToFind'))).send_keys(postdata['addr_near_by'])
                address = postdata['addr_sub_district'] + ' ' + postdata['addr_district'] + ' ' + postdata['addr_province']
                """ print("++++")
                print(address) """
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'address'))).send_keys(address)
    
            #for land
            elif postdata['property_type'] == '6':
                #Area
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'res_area'))).send_keys(postdata['floor_area'])
                post_detail = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.ID, 'additionalDetails')))
                post_detail[0].send_keys(postdata['post_description_th'])
                post_detail[1].send_keys(postdata['post_description_th'])            
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'res_howToFind'))).send_keys(postdata['addr_near_by'])
                address = postdata['addr_sub_district'] + ' ' + postdata['addr_district'] + ' ' + postdata['addr_province']
                """ print("++++")
                print(address) """
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'address'))).send_keys(address)

            #for hotel
            elif postdata['property_type'] == '8':
                #area size
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'res_area'))).send_keys(postdata['floor_area'])
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'res_bathrooms'))).send_keys(postdata['bath_room'])
                bed_room = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="js-bedroom-section"]/div/div/span')))
                bed_room.click()
                bed_put = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/span[2]/span/span[1]/input')))
                bed_put.send_keys(postdata['bed_room'])
                bed_put.send_keys(Keys.ENTER)
                post_detail = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.ID, 'additionalDetails')))
                post_detail[0].send_keys(postdata['post_description_th'])
                post_detail[1].send_keys(postdata['post_description_th'])            
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'res_howToFind'))).send_keys(postdata['addr_near_by'])
                address = postdata['addr_sub_district'] + ' ' + postdata['addr_district'] + ' ' + postdata['addr_province']
                """ print("++++")
                print(address) """
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'address'))).send_keys(address)

            #for factory
            elif postdata['property_type'] == '10' or postdata['property_type'] == '25':
                #bath room
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'res_area'))).send_keys(postdata['floor_area'])
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'res_bathrooms'))).send_keys(postdata['bath_room'])
                bed_room = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="js-bedroom-section"]/div/div/span')))
                bed_room.click()
                post_detail = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.ID, 'additionalDetails')))
                post_detail[0].send_keys(postdata['post_description_th'])
                post_detail[1].send_keys(postdata['post_description_th'])            
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'res_howToFind'))).send_keys(postdata['addr_near_by'])
                address = postdata['addr_sub_district'] + ' ' + postdata['addr_district'] + ' ' + postdata['addr_province']
                """ print("++++")
                print(address) """
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'address'))).send_keys(address)
            

            
            
             
            else:
                self.driver.quit()
                time_end = datetime.datetime.now()
                time_usage = time_end - time_start
                return {
                    "success": False,
                    "usage_time": str(time_usage),
                    "start_time": str(time_start),
                    "end_time": str(time_end),
                    "post_url": '',
                    "post_id": '',
                    "account_type": "null",
                    "detail": 'The posting of this website is on the maintance period',
                    "websitename": "baanfinder",
                }

            if postdata['property_type'] != '1':
                try:
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="addressArea"]/div[1]/div[1]/div/div/span'))).click()
                    province = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'select2-search__field')))
                    province.send_keys(postdata['addr_province'])
                    province.send_keys(Keys.ENTER)
                    time.sleep(1)
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="addressArea"]/div[1]/div[2]/div/div/span/span[1]/span'))).click()
                    district = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'select2-search__field')))
                    district.send_keys(postdata['addr_district'])
                    district.send_keys(Keys.ENTER)
                    time.sleep(1)
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="addressArea"]/div[2]/div[1]/div/div/span/span[1]/span'))).click()
                    subdis = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'select2-search__field')))
                    subdis.send_keys(postdata['addr_sub_district'])
                    subdis.send_keys(Keys.ENTER)
                    try:
                        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'res_lat'))).send_keys(postdata['geo_latitude'])
                        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'res_lng'))).send_keys(postdata['geo_longitude'])
                    except:
                        pass
                except:
                    self.driver.quit()
                    time_end = datetime.datetime.now()
                    time_usage = time_end - time_start
                    return {
                        "success": False,
                        "usage_time": str(time_usage),
                        "start_time": str(time_start),
                        "end_time": str(time_end),
                        "post_url": '',
                        "post_id": '',
                        "account_type": "null",
                        "detail": 'ไม่สามารถลงประกาศได้เนื่องจากไม่พบตำแหน่งทรัพย์ของท่าน',
                        "websitename": "baanfinder",
                    }

            try:
                upload = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'file')))
                all_images = ""
                for count, pic in enumerate(postdata['post_images'][:5]):
                    if count < len(postdata['post_images'][:5])-1:
                        all_images += os.path.abspath(pic) + '\n'
                    else:
                        all_images += os.path.abspath(pic)
                upload.send_keys(all_images)
            except:
                pass

            time.sleep(5)

            try:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'acceptAgentOrCoAgentFalse'))).click()
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'res-publish-btn'))).click()
                time.sleep(8)
                if 'https://www.baanfinder.com/th/new?ref=my-properties' == str(self.driver.current_url):
                    success = 'false'
                    detail = 'ไม่สามารถลงประกาศได้เนื่องจากข้อมูลไม่ทราบถ้วน'
                    post_url = ''
                    post_id = ''
                else:
                    success = 'true'
                    detail = 'ลงประกาศสำเร็จ'
                    post_url = self.driver.current_url
                    post_id = post_url.split('_')[0].split('/')[-1]
            except:
                success = 'false'
                detail = 'ไม่สามารถลงประกาศได้เนื่องจากข้อมูลไม่ทราบถ้วน'
                post_url = ''
                post_id = ''
        
        self.driver.close()
        self.driver.quit()

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
            "ds_id": postdata['ds_id'],
            "websitename": "baanfinder",
        }

    def edit_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""

        if success == "true":
            post_id = postdata['post_id']
            exists, authenticityToken, post_title = self.check_post(post_id)

            if exists:
                datapost = self.make_post_data(postdata)

                url = "https://www.baanfinder.com/property/"+str(post_id)+"_"+post_title+"/edit"
                r = httprequestObj.http_get(url, headers=self.headers)
                soup = BeautifulSoup(r.content, 'lxml')
                datapost['authenticityToken'] = soup.find('input', attrs={'name': 'authenticityToken'})['value']
                datapost['res.province'] = self.match_addr(postdata['addr_province'], 'res.province', soup)
                datapost['res.district'] = postdata['addr_district']
                datapost['res.sublocality'] = postdata['addr_sub_district']

                image_upload_url = "https://api.cloudinary.com/v1_1/baanfinder/auto/upload"
                image_upload_data = json.loads(str(soup.find('input', attrs={'type':'file', 'class':'cloudinary-fileupload'})['data-form-data']))

                r = httprequestObj.http_post(url, data=datapost, headers=self.headers)
                self.upload_images(postdata, post_id)
                detail = "Post Edited"
            else:
                success = "false"
                detail = "No post found with given id."
        self.driver.close()
        self.driver.quit()
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": post_url,
            "post_id": post_id,
            "ds_id": postdata['ds_id'],
            "account_type": "null",
            "detail": detail,
            "websitename": "baanfinder",
        }

    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        if success == "true":
            post_id = postdata['post_id']
            exists, authenticityToken, post_title = self.check_post(post_id)

            if exists:
                post_data = {}
                post_data['authenticityToken'] = authenticityToken
                delete_url = "https://www.baanfinder.com/property/"+str(post_id)+"_"+post_title+"/delete?showDraft=false&isExpired=false&x-http-method-override=DELETE"
                r = httprequestObj.http_post(delete_url, data=post_data, headers=self.headers)
                success = "true"
                detail = "post deleted successfully"
            else:
                success = "false"
                detail = "No post found with given id."
        self.driver.close()
        self.driver.quit()
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": "baanfinder",
            "log_id": postdata['log_id'],
            "ds_id": postdata['ds_id'],
            "post_id": post_id
        }

    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        if success == "true":
            post_id = postdata['post_id']
            exists, authenticityToken, post_title = self.check_post(post_id)

            if exists:
                post_data = {}
                post_data['authenticityToken'] = authenticityToken
                bump_url = "https://www.baanfinder.com/property/"+str(post_id)+"/bump"
                r = httprequestObj.http_post(bump_url, data=post_data, headers=self.headers)

                success = "true"
                detail = "post bumped successfully"
            else:
                success = "false"
                detail = "No post found with given id."
        self.driver.close()
        self.driver.quit()
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "ds_id": postdata['ds_id'],
            "websitename": "baanfinder",
            "log_id": postdata['log_id'],
        }

    def search_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        if success == "true":
            post_title = postdata['post_title_th']
            # exists, authenticityToken, post_title = self.check_post(post_id)

            url = "https://www.baanfinder.com/me/my-properties"
            r = httprequestObj.http_get(url, headers=self.headers)
            exists = False
            soup = BeautifulSoup(r.content, 'lxml')

            post_url = ""
            post_modify_time = ""
            post_view = ""
            post_found = "false"
            post_id = ""

            for entry in soup.find_all('div', attrs={'class':'resEntry'}):
                if entry is None:
                    continue
                title_row = entry.find('div', attrs={'class':'resTitle row'})
                if title_row is None:
                    continue
                title = title_row.find('a')['title']
                if post_title in title or title in post_title:
                    exists = True
                    post_id = str(entry.find('div', attrs={'class':'res-urlId'}).text).split(',')[0].split(' ')[-1][:-1]
                    post_url = "https://www.baanfinder.com/th/property/"+post_id
                    post_modify_time = ':'.join(str(entry.find('div', attrs={'class':'resPostedDate'}).text).split(':')[1:])
                    post_view = str(entry.find('div', attrs={'class':'res-analytics'}).text).split(',')[0].replace(' ', '').split(':')[-1]
                    post_found = "true"
                    detail = "post found successfully"
                    break

            if not exists:
                success = "false"
                detail = "No post found with given title."

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": "baanfinder",
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "post_create_time": '',
            "post_modify_time": post_modify_time,
            "post_view": post_view,
            "post_url": post_url,
            "post_found": post_found
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

# tri = baanfinder()
# dic = {"user":"ss@gmail.com", "pass":"ass", "name_th":"meow", "surname_th":"meow"}
# dic = {"user":"test7@gmail.com", "pass":"easypass", "name_th":"test6", "surname_th":""}
# print(tri.test_login(dic))
# print(tri.register_user(dic))

# postdata = {
#     "user":"test7@gmail.com",
#     "pass":"easypass",
#     "action": "create_post",
#     "timeout": "7",
#      "post_img_url_lists": [
#         "https://www.bangkokassets.com/property/250064/2199952_83636pic8.jpg",
#         "https://www.bangkokassets.com/property/250064/2199945_83636pic1.jpg",
#         "https://www.bangkokassets.com/property/250064/2199946_83636pic2.jpg",
#         "https://www.bangkokassets.com/property/250067/2199969_83635pic1.jpg"
#     ],
#     "geo_latitude": "13.786862",
#     "geo_longitude": "100.757815",
#     "property_id" : "chu001",
#     "post_title_th": "ให้เช่า ที่ดินด่วน บางกรวยไทรน้อย 6 ไร่ เหมาะทำตลาด",
#     "post_title_en": "Land for rent in Bang Kruai, Sai Noi, 6 rai, suitable for marketing",
#     "post_description_th": "ให้เช่า ที่ดินด่วน บางกรวยไทรน้อย 6 ไร่ เหมาะทำตลาดให้เช่า ที่ดินด่วน บางกรวยไทรน้อย 6 ไร่ เหมาะทำตลาด\nรายละเอียด\nที่ดินขนาด6ไร่\nหน้ากว้าง 30 เมตร\nสถานที่ใกล้เคียง\nถนนนครอินทร์\nถนนพระราม5\n\nให้เช่า 100,000 บาท\n\nสนใจติดต่อ ช่อทิพย์ 091829384",
#     "price_baht": "100000",
#     "listing_type": "เช่า",    
#     "property_type": "1",
#     "prominent_point" : "หน้ากว้างมาก ให้เช่าถูกสุด",    
#     "direction_type" : "11",
#     "addr_province": "นนทบุรี",
#     "addr_district": "เมืองนนทบุรี",
#     "addr_sub_district": "บางกร่าง",
#     "addr_road": "บางกรวย-ไทรน้อย",
#     "addr_soi": "ซอยบางกรวย-ไทรน้อย 34",
#     "addr_near_by": "ถนนพระราม5\r\nถนนนครอินทร์",
#     "bed_room": "3",
#     "bath_room": "2",
#     "floor_total": "10",
#     "floor_level": "4",
#     "floor_area": "90",
#     "land_size_rai": None,
#     "land_size_ngan": "6",
#     "land_size_wa": 0,
#     # "name": "from there yay -- edited!",
#     "name": "newest post!",
#     "mobile": "0992899991",
#     "email": "createpost@email.com",
#     "line": "0992899991",
#     # "project_name": "ที่ดิน บางกรวยไทย-น้อย",
#     "project_name": 'ชวนชมรัตน์ บางกรวย-ไทรน้อย',
#     "post_id": "3986808",
# }

# print(tri.create_post(postdata))
# print(tri.delete_post(postdata))
# print(tri.edit_post(postdata))
# print(tri.check_post("1991530", postdata))
# print(tri.boost_post(postdata))
# print(tri.get_project_name_id('ชวนชมรัตน์ บางกรวย-ไทรน้อย'))
# print(tri.search_post(postdata))
# tri.download_image("https://www.bangkokassets.com/property/250064/2199952_83636pic8.jpg")
# tri.upload_images(postdata)
