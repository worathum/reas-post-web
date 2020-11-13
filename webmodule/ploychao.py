# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
# from urlparse import urlparse
import re
import json
import datetime
import time
import sys
from urllib.parse import unquote


httprequestObj = lib_httprequest()



class element_has_css_class(object):
  """An expectation for checking that an element has a particular css class.

  locator - used to find the element
  returns the WebElement once it has the particular css class
  """
  def __init__(self, locator, css_class):
    self.locator = locator
    self.css_class = css_class

  def __call__(self, driver):
    element = driver.find_element(*self.locator)   # Finding the referenced element
    if self.css_class in element.get_attribute("class"):
        return element
    else:
        return False


class ploychao():

    name = 'ploychao'

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
        with open("./static/ploychao_province.json") as f:
            self.provincedata = json.load(f)
        # product categ id
        self.getProdId = {'1':24,'2':25,'3':26,'4':27,'5':29,'6':34,'7':28,'8':14,'9':31,'10':33}

    


    def upload_file(self,postdata,theid,ashopname):

        # download file
        options = Options()
        options.headless = True
        options.add_argument('--no-sandbox')
        try:
            driver = webdriver.Chrome("./static/chromedriver", chrome_options=options)
            driver.implicitly_wait(4)


            loginUrl = "https://www.ploychao.com/auth/"
            driver.get(loginUrl)
            driver.find_element_by_name("email").send_keys(postdata['user'])
            driver.find_element_by_name("password").send_keys(postdata['pass'])
            driver.find_element_by_id("btlogin").click()
            waiting = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'box-product')))

            posturl = "https://www.ploychao.com/"+ashopname+"/#editproduct/"+theid
            driver.get(posturl)
            while len(driver.find_elements_by_class_name("delete_img_upload")):
                try:
                    waiting1 = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'delete_img_upload')))
                    driver.find_elements_by_class_name("delete_img_upload")[0].click()
                    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
                    driver.switch_to.alert.accept()
                except:
                    continue
            


            allimages = postdata['post_images'][:10]

            dropzone = driver.find_element_by_id("dropzone")

            files = [os.getcwd() + "/" + img for img in allimages]

            isLocal = not driver._is_remote or '127.0.0.1' in driver.command_executor._url

            JS_DROP_FILES = "var c=arguments,b=c[0],k=c[1];c=c[2];for(var d=b.ownerDocument||document,l=0;;){var e=b.getBoundingClientRect(),g=e.left+(k||e.width/2),h=e.top+(c||e.height/2),f=d.elementFromPoint(g,h);if(f&&b.contains(f))break;if(1<++l)throw b=Error('Element not interactable'),b.code=15,b;b.scrollIntoView({behavior:'instant',block:'center',inline:'center'})}var a=d.createElement('INPUT');a.setAttribute('type','file');a.setAttribute('multiple','');a.setAttribute('style','position:fixed;z-index:2147483647;left:0;top:0;');a.onchange=function(b){a.parentElement.removeChild(a);b.stopPropagation();var c={constructor:DataTransfer,effectAllowed:'all',dropEffect:'none',types:['Files'],files:a.files,setData:function(){},getData:function(){},clearData:function(){},setDragImage:function(){}};window.DataTransferItemList&&(c.items=Object.setPrototypeOf(Array.prototype.map.call(a.files,function(a){return{constructor:DataTransferItem,kind:'file',type:a.type,getAsFile:function(){return a},getAsString:function(b){var c=new FileReader;c.onload=function(a){b(a.target.result)};c.readAsText(a)}}}),{constructor:DataTransferItemList,add:function(){},clear:function(){},remove:function(){}}));['dragenter','dragover','drop'].forEach(function(a){var b=d.createEvent('DragEvent');b.initMouseEvent(a,!0,!0,d.defaultView,0,0,0,g,h,!1,!1,!1,!1,0,null);Object.setPrototypeOf(b,null);b.dataTransfer=c;Object.setPrototypeOf(b,DragEvent.prototype);f.dispatchEvent(b)})};d.documentElement.appendChild(a);a.getBoundingClientRect();return a;"

            elm_input = driver.execute_script(JS_DROP_FILES, dropzone, 0, 0)
            value = '\n'.join(files)
            elm_input._execute('sendKeysToElement', {'value': [value], 'text': value})
            
            for ind,file in enumerate(files):
                myelement = WebDriverWait(driver, 5).until(element_has_css_class((By.XPATH, "//*[@id='viewupload']/div["+str(ind+1)+"]"), "dz-success"))

            driver.find_element_by_xpath("//*[@id='viewupload']/div/div[2]/div[3]/span/input").click()

            time.sleep(1)    

            driver.find_element_by_id('btn-save-sale').click()
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
            driver.switch_to.alert.accept()
            waiting = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'box-product')))
        finally:
            driver.close()
            driver.quit()
            try:
                alert = driver.switch_to.alert
                alert.accept()
                driver.close()
                driver.quit()
            except:
                pass



    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()


        user = postdata['user']
        passwd = postdata['pass']
        name_th = postdata["name_th"]
        surname_th = postdata["surname_th"]
        try:
            company_name = postdata['company_name']
        except:
            company_name = name_th
        # start process
        success = "true"
        detail = ""

        datapost = dict(
            email=user,
            passwd=passwd,
            con_passwd=passwd,
            fullname=name_th+" "+surname_th,
            shopname=company_name,
            action='save_register',
        )
        r = httprequestObj.http_post(
            'https://www.ploychao.com/register/', data=datapost)

        data = r.text
        if data == '' or data == '0':
            success = "false"
        else:
            detail = data  

        # # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "start_time": str(time_start),
            "usage_time": str(time_usage),
            "websitename": "ploychao",
            "end_time": str(time_end),
            "detail": detail,
        }


    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']

        success = "true"
        detail = ""

        datapost = {
            'action': 'login',
            'password': passwd,
            'email': user,
        }

        r = httprequestObj.http_post('https://www.ploychao.com/auth/', data=datapost)
        data = r.text
        if str(data) == '1':
            success = "false"
            detail = "cannot login"
        elif str(data) == '2':
            success = "false"
            detail = "account suspended"
        else:
            detail = data
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "start_time": str(time_start),
            "websitename": "ploychao",
            "end_time": str(time_end),
            "detail": detail,
        }


    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        success = "true"
        detail = ""
        post_url = ""
        post_id = ""



        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]

        if success == "true":

            ashopname = test_login["detail"]

            theprodid = self.getProdId[postdata['property_type']]
            for (key, value) in self.provincedata.items():
                if type(value) is str and postdata['addr_province'].strip() in value.strip():
                    province_id = key
                    break
            
            for (key, value) in self.provincedata[province_id+"_province"].items():
                if postdata['addr_district'].strip() in value.strip():
                    amphur_id = key
                    break                
            
            prod_address = ""               
            for add in [postdata['addr_soi'],postdata['addr_road'],postdata['addr_sub_district'],postdata['addr_district'],postdata['addr_province']]:
                if add is not None:
                    prod_address += add 
            prod_address = prod_address[:-1]                



            datapost = [
                ('action', 'saveproduct'),
                ('hidproduct_id', '0'),
                ('savetype', 'R'),
                ('myshopname', ashopname),
                ('product_cat_id',theprodid),
                ('product_name',postdata['post_title_th']),
                ('product_description',postdata['post_description_th']),
                ('product_price[]',postdata['price_baht']),
                ('product_unit[]',''),
                ('product_warranty_price',''),
                ('shipping_id',''),
                ('product_address',prod_address),
                ('product_province_id',province_id),
                ('product_amphur_id',amphur_id),
                ('product_latitude',postdata['geo_latitude']),
                ('product_longitude',postdata['geo_longitude']),
                ('payment_method',''),
                ('productcondition',''),
            ]

            r = httprequestObj.http_post(
                'https://www.ploychao.com/member/', data=datapost)


            data = r.text
            
            if data == '1':
                success = "false"
                detail = "Post could not be created."
            else:
                r2 = httprequestObj.http_get('https://www.ploychao.com/'+ashopname+'/',verify=False)
                data2 = r2.text
                soup = BeautifulSoup(data2, self.parser, from_encoding='utf-8')
                string2 = soup.find("div", {"id": "box-product"}).find_all("div")
                post_id = string2[2]['id'][-5:]

                post_url = "https://www.ploychao.com/product/" + postdata['post_title_th'].lower().replace(" ","%20")+"/"+post_id+"/"
                if postdata['post_img_url_lists'] != []:
                    self.upload_file(postdata,post_id,ashopname)

        else:
            detail = test_login["detail"]    
                 
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "success": success,
            "start_time": str(time_start),
            "websitename": "ploychao",
            "end_time": str(time_end),
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "null",
            "detail":detail,
        }


    def edit_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()



        success = "true"
        detail = ""
        post_url = ""
        post_id = ""

        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]

        if success == "true":
            ashopname = test_login["detail"]

            theprodid = self.getProdId[postdata['property_type']]
            for (key, value) in self.provincedata.items():
                if type(value) is str and postdata['addr_province'].strip() in value.strip():
                    province_id = key
                    break
            
            for (key, value) in self.provincedata[province_id+"_province"].items():
                if postdata['addr_district'].strip() in value.strip():
                    amphur_id = key
                    break                
            
            prod_address = ""               
            for add in [postdata['addr_soi'],postdata['addr_road'],postdata['addr_sub_district'],postdata['addr_district'],postdata['addr_province']]:
                if add is not None:
                    prod_address += add 
            prod_address = prod_address[:-1]                



            datapost = [
                ('action', 'saveproduct'),
                ('hidproduct_id', postdata['post_id']),
                ('savetype', 'R'),
                ('myshopname', ashopname),
                ('product_cat_id',theprodid),
                ('product_name',postdata['post_title_th']),
                ('product_description',postdata['post_description_th']),
                ('product_price[]',postdata['price_baht']),
                ('product_unit[]',''),
                ('product_warranty_price',''),
                ('shipping_id',''),
                ('product_address',prod_address),
                ('product_province_id',province_id),
                ('product_amphur_id',amphur_id),
                ('product_latitude',postdata['geo_latitude']),
                ('product_longitude',postdata['geo_longitude']),
                ('payment_method',''),
                ('productcondition',''),
            ]

            r = httprequestObj.http_post(
                'https://www.ploychao.com/member/', data=datapost)

            data = r.text
            if data == '1':
                success = "false"
                detail = "Post could not be edited."
            else:
                r2 = httprequestObj.http_get('https://www.ploychao.com/'+ashopname+'/',verify=False)
                data2 = r2.text
                soup = BeautifulSoup(data2, self.parser, from_encoding='utf-8')
                string2 = soup.find("div", {"id": "box-product"}).find_all("div")
                for s in string2:
                    try:
                        post_id = s['id'][-5:]
                        break
                    except:
                        continue    

                post_url = "https://www.ploychao.com/product/" + postdata['post_title_th'].lower().replace(" ","%20")+"/"+post_id+"/"
                if postdata['post_img_url_lists'] != []:
                    self.upload_file(postdata,post_id,ashopname)

        else:
            detail = "cannot login"

                 
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "start_time": str(time_start),
            "websitename": "ploychao",
            "end_time": str(time_end),
            "detail": detail,
            "log_id": postdata['log_id']
        }



    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process

        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]

        if success == "true":

            datapost = [
                ('action', 'delete_product'),
                ('product_id', postdata['post_id']),
            ]
            r = httprequestObj.http_post(
                'https://www.ploychao.com/member/', data=datapost)
            data = r.text
            if data == '':
                success = "false"
                detail = "post not deleted"
            else:
                detail = "deleted"   
        else:
            success = "false" 
            detail = "cannot login"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "start_time": str(time_start),
            "websitename": "ploychao",
            "end_time": str(time_end),
            "detail": detail,
            "log_id":postdata['log_id'],
        }


    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        post_id = postdata['post_id']
        log_id = postdata['log_id']

        #
        #
        #

        time_end = datetime.datetime.utcnow()
        return {
            "success": "false",
            "time_usage": time_end - time_start,
            "time_start": time_start,
            "time_end": time_end,
            "detail": "",
            "log_id": log_id,
            "post_id": post_id,
            "websitename": "ploychao",
            "post_view": ""
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
