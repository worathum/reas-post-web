# -*- coding: utf-8 -*-

from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
# from urlparse import urlparse
import re
import json
import datetime
import sys
from urllib.parse import unquote
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
options = Options()
options.headless = True
options.incognito = True


class prakardproperty():

    name = 'prakardproperty'

    def __init__(self):

        try:
            import configs
        except ImportError:
            configs = {}

        self.httprequestObj = lib_httprequest()
        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.primarydomain = 'http://www.prakardproperty.com/'
        self.debug = 0
        self.debugresdata = 0
        self.parser = 'html.parser'


    def register_user(self, userdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        email = userdata['user']
        passwd = userdata['pass']
        display_name = userdata['name_th']
        mobile = userdata['tel']
        
        datapost={
            'data[Members][email]':email,
            'data[Members][password]':passwd,
            'data[Members][re-password]':passwd,
            'data[Members][display_name]':display_name,
            'data[Members][mobile]': mobile,
            'data[Members][accept_newsletter]' : 0
        }
        
        r = self.httprequestObj.http_post('http://www.prakardproperty.com/register/save', data=datapost)
        data = r.text
        matchObj = re.search(r'/register/resentmail', data)
        if matchObj:
            success = "True"
            detail = "Sucessful Registration"
        else:
            success = "False"
            detail = "Not Registered"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "prakardproperty",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
        }

    def test_login(self, logindata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        

        email_user = logindata['user']
        email_pass = logindata['pass']
        
        datapost = {
            'login_email' : email_user,
            'login_password' : email_pass
        }
        #datapost)
        i = 0
        matchObj = False
        while i < 8 and not matchObj:

            r = self.httprequestObj.http_post('http://www.prakardproperty.com/login/checkmember', data=datapost)
            # r = requests.post('http://www.prakardproperty.com/login/checkmember', data=datapost)
            self.httprequestObj.http_get('http://www.prakardproperty.com/properties/add')
            data = r.text
            # print(data)
            # #data)
            matchObj = re.search(r'/member/account', data)
            # #matchObj)
            i += 1
        if matchObj:
            success = "True"
            detail = "Successful Login"
        else:
            success = "False"
            detail = "Login Unsuccessful"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        
        return {
            "websitename": "prakardproperty",
            "success": success,
            "ds_id": logindata['ds_id'],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
        }
        #
        #
        #

    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        # #postdata)
        webdata = postdata

        listing_type = postdata['listing_type']
        property_type = postdata['property_type']
        allimages = postdata['post_images']
        price_baht = postdata['price_baht']
        addr_province = postdata['addr_province']
        addr_district = postdata['addr_district']
        addr_sub_district = postdata['addr_sub_district']
        addr_road = postdata['addr_road']
        addr_near_by = postdata['addr_near_by']
        prod_address = ""
        for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
            if add is not None:
                prod_address += add + ","
        prod_address = prod_address[:-1]
        try:
            floorarea_sqm = postdata['floorarea_sqm']
        except:
            floorarea_sqm = ''
        geo_latitude = postdata['geo_latitude']
        geo_longitude = postdata['geo_longitude']
        property_id = postdata['property_id']
        post_title_th = postdata['post_title_th']
        post_description_th = postdata['post_description_th']
        post_title_en = postdata['post_title_en']
        post_description_en = postdata['post_description_en']
        try:
            floor_no = postdata['floor_level']
        except:
            floor_no = ""
        try:
            bedroom = postdata['bed_room']
        except:
            bedroom = ""
        try:
            bathroom = postdata['bath_room']
        except:
            bathroom = ""
        ds_id = webdata["ds_id"]
        # account_type = webdata["account_type"]
        user = webdata["user"]
        password = webdata["pass"]
        project_name = ""
        try:
            project_name = postdata["web_project_name"]
        except:
            try:
                project_name = postdata["project_name"]
            except:
                project_name = postdata["post_title_th"]

        proj_url = "http://www.prakardproperty.com/autocomplete/project/?term=" + project_name
        resp = self.httprequestObj.http_get(proj_url, verify=False)
        try:
            allres = json.loads(resp.content.decode('utf-8'))
        except:
            allres = []
        project_id = ""
        isProject = False
        if len(allres) != 0:
            isProject = True
            project_id = allres[0]['id']
            project_name = allres[0]['value']
            geo_latitude = allres[0]['google_map_latitude']
            geo_longitude = allres[0]['google_map_longitude']
            addr_province = allres[0]['province_id']
            addr_district = allres[0]['district_id']
            addr_sub_district = allres[0]['sub_district_id']


        land_size_rai = postdata['land_size_rai']
        land_size_ngan = postdata['land_size_ngan']
        land_size_wah = postdata['land_size_wa']
        #property_type)
        #property_type == "6")
        #property_type == 6)
        if(str(property_type) == "6"):# land
            property_type = "6"
        elif(str(property_type) == "1"): # condo
            property_type = "3"
        elif(str(property_type) == 3):
            property_type = "1"
        elif(str(property_type) == "4"): # townhouses
            property_type = "2"
        elif(str(property_type) == "5"): # commercial building
            property_type = "4"
        elif(str(property_type) == "7"): # Apartment
            property_type = "5"
        elif(str(property_type) == "9"): # office
            property_type = "9"
        elif(str(property_type) == "10" or str(property_type) == "25"): # factory
            property_type = "7"
        else :
            property_type = "8"


        #property_type)    
        postdata = {
            'data[Properties][running_number]':"",
'data[Properties][title]': post_title_th,
'data[Properties][property_type_id]': property_type, # number between 1-9
'data[Properties][property_post_type_id]': listing_type, 
'data[Properties][size_square_metre]': floorarea_sqm,
'data[Properties][land_size_rai]': land_size_rai ,
'data[Properties][land_size_ngan]': land_size_ngan,
'data[Properties][land_size_wah]':land_size_wah, 
'data[Properties][floor_no]': floor_no,
'data[Properties][bedroom]': bedroom,
'data[Properties][bathroom]': bathroom,
'data[Properties][living_room]':0 ,
'data[Properties][maid_room]': 0,
'data[Properties][parking_space]':0 ,
'data[Properties][air_conditioner]':0 ,
'data[Properties][age_of_property]':0 ,
'data[Properties][project_name]': project_name,
'data[Properties][project_id]':project_id,
'data[PropertyDetails][address]':prod_address, 
'data[PropertyDetails][street]': "",
'data[PropertyDetails][road]': addr_road,
'data[Properties][province_id]': addr_province,
'data[Properties][district_id]': addr_district,
'data[Properties][sub_district_id]':addr_sub_district,
'data[PropertyDetails][google_map_latitude]': geo_latitude,
'data[PropertyDetails][google_map_longitude]': geo_longitude,
'data[PropertyDetails][location_datail]': "",
'data[Properties][youtube]':"", 
'data[PropertyDetails][detail]':post_description_th, 
'propertyConfirm1': 'on',
        }
        list_dict = {'ขาย' : 1, 'เช่า':2,'ขายดาวน์':3,'เซ้ง':4,'ขาย/ให้เช่า':5, 'ให้เช่า': 1}
        listing_type = list_dict[listing_type]
        postdata['data[Properties][property_post_type_id]'] = listing_type
        if(listing_type == "เช่า"):
            postdata['data[Properties][rental_price]'] = price_baht
            postdata['data[Properties][unit_type_id1]'] = ""
            postdata['data[Properties][unit_type_id2]']= 1
        else:
            postdata['data[Properties][sell_price]'] = price_baht
            postdata['data[Properties][unit_type_id1]'] = 1
            postdata['data[Properties][unit_type_id2]']= ""
            
        # if(listing_type == 4):
        #     postdata['data[Properties][rental_price]'] = price_baht
        #     postdata['data[Properties][unit_type_id1]'] = 1
        #     postdata['data[Properties][unit_type_id2]']= 1
            
        # login
        
        login = self.test_login(webdata)
        success = login["success"]
        detail = login["detail"]
        post_id = ""
        post_url = ""
        if success == "True":
            if not isProject:
                r = self.httprequestObj.http_get('http://www.prakardproperty.com/properties/add', verify=False)
                
                data = r.text
                
                soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
                
                authenticityToken = soup.find("input", {"name": "data[Properties][running_number]"})['value']
                
                postdata['data[Properties][running_number]'] = authenticityToken
                
                contents =[[str(x.text),str(x['value'])] for x in soup.find("select", {"name" :"data[Properties][province_id]" }).find_all('option')]
                # #contents)
                for i in contents:
                    if(addr_province.find(i[0]) != -1):
                        postdata['data[Properties][province_id]'] = i[1]
                        r = self.httprequestObj.http_get('http://www.prakardproperty.com/location/getdistrict/mode:geomap/province_id:'+postdata['data[Properties][province_id]'])
                        # #r.text)
                        soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
                        districtcontent = [[str(x.text),str(x['value'])] for x in soup.find_all('option')]
                        for j in districtcontent:
                            if(addr_district.find(j[0]) != -1):
                                postdata['data[Properties][district_id]'] = j[1]
                                r = self.httprequestObj.http_get('http://www.prakardproperty.com/location/getsubdistrict/mode:geomap/province_id:'+postdata['data[Properties][province_id]']+'/district_id:'+postdata['data[Properties][district_id]'])
                                # #r.text)   
                                soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
                                subdistrictcontent = [[str(x.text),str(x['value'])] for x in soup.find_all('option')]
                                for k in subdistrictcontent:
                                    if(addr_sub_district.find(k[0])!= -1):
                                        postdata['data[Properties][sub_district_id]'] = k[1]
                                        break
                                break       
                        break

            r = self.httprequestObj.http_post('http://www.prakardproperty.com/properties/addsave', data = postdata)#/property/show
            data = r.text
            # print(data)
            # #data)
            matchObj = re.search(r'/property/show', data)
            if not matchObj:
                success = "False"
                detail = "Cannot post to prakardproperty"
            else:
                post_id = re.search(r'/property/show/(\d+)',data).group(1)
                post_url = 'http://www.prakardproperty.com/property/show/'+post_id
            if(success == "True" ):
                #"Image time")
                driver = webdriver.Firefox(options=options)
                try:
                    driver.get('http://www.prakardproperty.com/')
                    email = webdata["user"]
                    password = webdata["pass"]
                    newbut = driver.find_element_by_class_name('prakard-link')
                    newbut.click()
                    try:
                        user = driver.find_element_by_id('login_email')
                        passs = driver.find_element_by_id('login_password')
                        user.send_keys(email)
                        passs.send_keys(password)
                        login = driver.find_element_by_class_name('login-button')
                        login.click()
                    except:
                        print("Login Error?: "+str(e))

                        pass
                    driver.get('http://www.prakardproperty.com/properties/edit/'+post_id)
                    for i in range(len(webdata['post_images'])) :
                        fileupload = driver.find_element_by_id('file_upload')
                        filepath = os.getcwd() + "/"+ webdata['post_images'][i]
                        #filepath)
                        fileupload.send_keys(filepath)
                        while(True):
                            try:
                                elements = driver.find_elements_by_class_name('item')
                                if(len(elements) == i+1):
                                    break
                            except NoSuchElementException:
                                continue
                        time.sleep(1)
                    #"uploaded images")
                    submit = driver.find_element_by_class_name('prakard-button')
                    submit.click()
                    detail += " \n Images uploaded successfully"
                    driver.quit()
                except Exception as e:
                    print(e)
                    driver.quit()
                    detail += " \n Images not uploaded successfully"
                
            #
        #
        #

        time_end = datetime.datetime.utcnow()
        # #{
        #     "websitename": "prakardproperty",
        #     "success": success,
        #     "time_usage": str(time_end - time_start),
        #     "start_time": str(time_start),
        #     "end_time": str(time_end),
        #     "ds_id": "4",
        #     "post_url": post_url,
        #     "post_id": post_id,
        #     "account_type": "",
        #     "detail": detail
        # }
        return {
            "websitename": "prakardproperty",
            "success": success,
            "time_usage": str(time_end - time_start),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": webdata['ds_id'],
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "",
            "detail": detail
        }

    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        
        login = self.test_login(postdata)
        success = login["success"]
        detail = login["detail"]
        post_id = postdata['post_id']
        post_url = ""
        if(success == "True"):
            # #)
            postdata['data[Properties][id]'] = post_id
            # #postdata)
            r = self.httprequestObj.http_get('http://www.prakardproperty.com/property/show/'+post_id)
            data = r.text
            if(re.search(r'404',data)):
                time_end = datetime.datetime.utcnow()
                return {
                    "websitename": "prakardproperty",
                    "log_id": postdata['log_id'],
                    "success": "False",
                    "time_usage": time_end - time_start,
                    "start_time": time_start,
                    "end_time": time_end,
                    "detail": "PostId not Found"
                }
            
            r = self.httprequestObj.http_post('http://www.prakardproperty.com/properties/updatedate/'+post_id,data="")#/property/show
            data = r.text
            if r.status_code != 200:
                success = "False"
                detail = "Cannot Boost post with id"+post_id
            else:
                success = "True"
                detail = "Post sucessfully Boosted"


        time_end = datetime.datetime.utcnow()
        return {
            "websitename": "prakardproperty",
            "success": success,
            "time_usage": time_end - time_start,
            "start_time": time_start,
            "end_time": time_end,
            "detail": detail,
            "log_id": postdata['log_id'],
            "post_id": post_id,
        }

    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        
        login = self.test_login(postdata)
        success = login["success"]
        detail = login["detail"]
        post_id = postdata['post_id']
        post_url = ""
        if(success == "True"):
            # #)
            postdata['data[Properties][id]'] = post_id
            # #postdata)
            r = self.httprequestObj.http_get('http://www.prakardproperty.com/property/show/'+post_id)
            data = r.text
            if(re.search(r'404',data)):
                time_end = datetime.datetime.utcnow()
                return {
                    "success": "False",
                    "log_id": postdata['log_id'],
                    "websitename": "prakardproperty",
                    "time_usage": time_end - time_start,
                    "start_time": time_start,
                    "end_time": time_end,
                    "detail": "PostId not Found"
                }
            
            r = self.httprequestObj.http_post('http://www.prakardproperty.com/properties/delete/'+post_id,data="")#/property/show
            data = r.text
            r = self.httprequestObj.http_get('http://www.prakardproperty.com/member/posted/msg:success')
            # #r.status_code,r.text)
            if r.status_code != 200:
                success = "False"
                detail = "Cannot delete post with id"+post_id
            else:
                success = "True"
                detail = "Post sucessfully deleted"

        #
        #
        #

        time_end = datetime.datetime.utcnow()
        return {
            "websitename": "prakardproperty",
            "success": success,
            "time_usage": time_end - time_start,
            "start_time": time_start,
            "end_time": time_end,
            "detail": detail,
            "log_id": postdata['log_id'],
        }


    
    def edit_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        # #postdata)
        webdata = postdata

        listing_type = postdata['listing_type']
        property_type = postdata['property_type']
        allimages = postdata['post_images']
        price_baht = postdata['price_baht']
        addr_province = postdata['addr_province']
        addr_district = postdata['addr_district']
        addr_sub_district = postdata['addr_sub_district']
        addr_road = postdata['addr_road']
        addr_near_by = postdata['addr_near_by']
        geo_latitude = postdata['geo_latitude']
        geo_longitude = postdata['geo_longitude']
        property_id = postdata['property_id']
        post_title_th = postdata['post_title_th']
        post_description_th = postdata['post_description_th']
        post_title_en = postdata['post_title_en']
        post_description_en = postdata['post_description_en']
        prod_address = ""
        for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
            if add is not None:
                prod_address += add + ","
        prod_address = prod_address[:-1]
        try:
            floor_no = postdata['floor_level']
            floorarea_sqm = postdata['floorarea_sqm']
            bedroom = postdata['bed_room']
            bathroom = postdata['bath_room']
        except:
            floor_no = ""
            floorarea_sqm = ""
            bedroom = ""
            bathroom = ""
        ds_id = webdata["ds_id"]

        # account_type = webdata["account_type"]
        user = webdata["user"]
        password = webdata["pass"]
        project_name = ""
        try:
            project_name = postdata["web_project_name"]
        except:
            try:
                project_name = postdata["project_name"]
            except:
                project_name = postdata["post_title_th"]
        proj_url = "http://www.prakardproperty.com/autocomplete/project/?term=" + project_name
        resp = self.httprequestObj.http_get(proj_url, verify=False)
        try:
            allres = json.loads(resp.content.decode('utf-8'))
        except:
            allres = []

        project_id = ""
        isProject = False
        if len(allres) != 0:
            isProject = True
            project_id = allres[0]['id']
            project_name = allres[0]['value']
            geo_latitude = allres[0]['google_map_latitude']
            geo_longitude = allres[0]['google_map_longitude']
            addr_province = allres[0]['province_id']
            addr_district = allres[0]['district_id']
            addr_sub_district = allres[0]['sub_district_id']

        land_size_rai = postdata['land_size_rai']
        land_size_ngan = postdata['land_size_ngan']
        land_size_wah = postdata['land_size_wa']
        if(str(property_type) == "6"):# land
            property_type = "6"
        elif(str(property_type) == "1"): # condo
            property_type = "3"
        elif(str(property_type) == 3):
            property_type = "1"
        elif(str(property_type) == "4"): # townhouses
            property_type = "2"
        elif(str(property_type) == "5"): # commercial building
            property_type = "4"
        elif(str(property_type) == "7"): # Apartment
            property_type = "5"
        elif(str(property_type) == "9"): # office
            property_type = "9"
        elif(str(property_type) == "10" or str(property_type) == "25"): # factory
            property_type = "7"
        else :
            property_type = "8"
        postdata = {
            'data[Properties][id]':webdata['post_id'],
'data[Properties][title]': post_title_en,
'data[Properties][property_type_id]': property_type, # number between 1-9
'data[Properties][property_post_type_id]': listing_type,               #number between 1-9
'data[Properties][size_square_metre]': floorarea_sqm,
'data[Properties][land_size_rai]': land_size_rai ,
'data[Properties][land_size_ngan]': land_size_ngan,
'data[Properties][land_size_wah]':land_size_wah, 
'data[Properties][floor_no]': floor_no,
'data[Properties][bedroom]': bedroom,
'data[Properties][bathroom]': bathroom,
'data[Properties][living_room]':0 ,
'data[Properties][maid_room]': 0,
'data[Properties][parking_space]':0 ,
'data[Properties][air_conditioner]':0 ,
'data[Properties][age_of_property]':0 ,
'data[Properties][project_name]': project_name,
'data[Properties][project_id]':"" ,
'data[PropertyDetails][address]':prod_address, 
'data[PropertyDetails][street]': "",
'data[PropertyDetails][road]': addr_road,
'data[Properties][province_id]': addr_province,
'data[Properties][district_id]': addr_district,
'data[Properties][sub_district_id]':addr_sub_district,
'data[PropertyDetails][google_map_latitude]': geo_latitude,
'data[PropertyDetails][google_map_longitude]': geo_longitude,
'data[PropertyDetails][location_datail]': "",
'files[]': [],
'data[Properties][youtube]':"", 
'data[PropertyDetails][detail]':post_description_en
        }
        list_dict = {'ขาย' : 1, 'เช่า':2,'ขายดาวน์':3,'เซ้ง':4,'ขาย/ให้เช่า':5}
        listing_type = list_dict[listing_type]
        postdata['data[Properties][property_post_type_id]'] = listing_type
        if(listing_type == "เช่า"):
            postdata['data[Properties][rental_price]'] = price_baht
            postdata['data[Properties][unit_type_id1]'] = ""
            postdata['data[Properties][unit_type_id2]']= 1
        else:
            postdata['data[Properties][sell_price]'] = price_baht
            postdata['data[Properties][unit_type_id1]'] = 1
            postdata['data[Properties][unit_type_id2]']= ""
        # file_list = []
        # for i in post_img_url_lists:
        #     file_list.append(open(i,'rb'))
        # #file_list)
        # login
        login = self.test_login(webdata)
        success = login["success"]
        detail = login["detail"]
        post_id = webdata['post_id']
        post_url = ""
        if(success == "True"):
            r = self.httprequestObj.http_get('http://www.prakardproperty.com/properties/edit/'+post_id)
            data = r.text
            if(re.search(r'404',data)):
                time_end = datetime.datetime.utcnow()
                return {
                    "success": "False",
                    "time_usage": str(time_end - time_start),
                    "start_time": str(time_start),
                    "end_time": str(time_end),
                    "ds_id": "4",
                    "post_url": post_url,
                    "post_id": post_id,
                    "account_type": "",
                    "detail": "Post_ID not found",
                    "websitename":"prakardproperty"
                }
                
            if not isProject:
                soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
                try:
                    contents =[[str(x.text),str(x['value'])] for x in soup.find("select", {"name" :"data[Properties][province_id]" }).find_all('option')]
                    # #contents)
                    for i in contents:
                        if(i[0] == addr_province):
                            postdata['data[Properties][province_id]'] = i[1]
                            r = self.httprequestObj.http_get('http://www.prakardproperty.com/location/getdistrict/mode:geomap/province_id:'+postdata['data[Properties][province_id]'])
                            # #r.text)
                            soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
                            districtcontent = [[str(x.text),str(x['value'])] for x in soup.find_all('option')]
                            for i in districtcontent:
                                if(i[0] == addr_district):
                                    postdata['data[Properties][district_id]'] = i[1]
                                    r = self.httprequestObj.http_get('http://www.prakardproperty.com/location/getsubdistrict/mode:geomap/province_id:'+postdata['data[Properties][province_id]']+'/district_id:'+postdata['data[Properties][district_id]'])
                                    # #r.text)   
                                    soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
                                    subdistrictcontent = [[str(x.text),str(x['value'])] for x in soup.find_all('option')]
                                    for i in subdistrictcontent:
                                        if(i[0] == addr_sub_district):
                                            postdata['data[Properties][sub_district_id]'] = i[1]
                                            break
                                    break       
                            break
                    # #)
                # #postdata)
                    r = self.httprequestObj.http_post('http://www.prakardproperty.com/properties/editsave', data = postdata)#/property/show
                    data = r.text
                    # #data)
                    matchObj = data
                    if not matchObj:
                        success = "False"
                        detail = "Edit Unsuccessful"
                    else:
                        post_url = 'http://www.prakardproperty.com/property/show/'+post_id
                        detail = "Edit Successful"
                    if(success == "True" ):
                        try:
                            driver = webdriver.Firefox(options=options)

                            #"Driver On")
                            driver.get('http://www.prakardproperty.com/')
                            email = webdata["user"]
                            password = webdata["pass"]
                            user = driver.find_element_by_id('login_email')
                            passs = driver.find_element_by_id('login_password')
                            user.send_keys(email)
                            passs.send_keys(password)
                            login = driver.find_element_by_class_name('login-button')
                            login.click()
                            newbut = driver.find_element_by_class_name('prakard-link')
                            newbut.click()
                            driver.get('http://www.prakardproperty.com/properties/edit/'+post_id)
                            elements = driver.find_elements_by_class_name('item')
                            temp = len(elements)
                            #temp)
                            for i in range(len(webdata['post_images'])) :
                                fileupload = driver.find_element_by_id('file_upload')
                                filepath = os.getcwd() + "/"+ webdata['post_images'][i]
                                #i,filepath)
                                fileupload.send_keys(filepath)
                                while(True):
                                    try:
                                        elements = driver.find_elements_by_class_name('item')
                                        # #elements)
                                        if(len(elements) == temp + i+1):
                                            break
                                    except NoSuchElementException:
                                        continue
                                time.sleep(1)
                            #"uploaded images")
                            submit = driver.find_element_by_class_name('prakard-button')
                            submit.click()
                            detail += " \n Images uploaded successfully"
                            driver.close()
                        except:
                            detail += " \n Images not uploaded successfully"
                    
                except:
                    success = "False"
                    detail = "Edit Unsuccessful"
        #
        #

        time_end = datetime.datetime.utcnow()
        # #{
        #     "websitename": "prakardproperty",
        #     "success": success,
        #     "time_usage": str(time_end - time_start),
        #     "start_time": str(time_start),
        #     "end_time": str(time_end),
        #     "ds_id": "4",
        #     "post_url": post_url,
        #     "post_id": post_id,
        #     "account_type": "",
        #     "detail": detail
        # }
        return {
            "websitename": "prakardproperty",
            "success": success,
            "time_usage": str(time_end - time_start),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "log_id": webdata['log_id'],
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "",
            "detail": detail
        }
    def search_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        if success == "True":
            post_title = postdata['post_title_th']
            # exists, authenticityToken, post_title = self.check_post(post_id)

            url = "http://www.prakardproperty.com/member/posted"
            r = self.httprequestObj.http_get(url)
            exists = False
            soup = BeautifulSoup(r.content, 'lxml')
            post_url = ""
            post_modify_time = ""
            post_view = ""
            post_found = "false"
            entry = soup.find('div', attrs={'id':'member-list'})
            for title_row in entry.find_all('div', attrs={'class':'c3'}):
                if title_row is None:
                    continue
                title = title_row.find('a')
                title_1=title.text.strip()
                if post_title == title_1:
                    exists = True
                    post_id = title['href'][-6:]
                    post_url = "https://www.prakardproperty.com/property/show/"+post_id
                    post_modify_time = title_row.find('span', attrs={'class':'update'}).text[13:-2]
                    post_view = title_row.find('p', attrs={'class':'stat'}).text[7:]
                    post_found = "true"
                    detail = "post found successfully"

            if not exists:
                success = "false"
                detail = "No post found with given title."

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": "true",
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": "prakardproperty",
            "account_type":None,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
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
