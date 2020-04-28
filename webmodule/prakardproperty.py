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
        r = self.httprequestObj.http_post('http://www.prakardproperty.com/login/checkmember', data=datapost)
        # r = requests.post('http://www.prakardproperty.com/login/checkmember', data=datapost)
        data = r.text
        # print(data)
        matchObj = re.search(r'/member/account', data)
        # print(matchObj)
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
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": self.websitename
        }
        #
        #
        #

    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        # print(postdata)
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
            bathroom = postdata['bed_room']
        except:
            bathroom = ""
        ds_id = webdata["ds_id"]
        # account_type = webdata["account_type"]
        user = webdata["user"]
        password = webdata["pass"]
        project_name = postdata["project_name"]
        land_size_rai = postdata['land_size_rai']
        land_size_ngan = postdata['land_size_ngan']
        land_size_wah = postdata['land_size_wa']
        
        postdata = {
            'data[Properties][running_number]':"",
'data[Properties][title]': post_title_th,
'data[Properties][property_type_id]': property_type, # number between 1-9
'data[Properties][property_post_type_id]': listing_type,               #number between 1-9
'data[Properties][sell_price]': price_baht,
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
'data[Properties][youtube]':"", 
'data[PropertyDetails][detail]':post_description_th, 
'propertyConfirm1': 'on',
        }
        list_dict = {'ขาย' : 1, 'เช่า':2,'ขายดาวน์':3,'เซ้ง':4,'ขาย/ให้เช่า':5, 'ให้เช่า': 1}
        listing_type = list_dict[listing_type]
        postdata['data[Properties][property_post_type_id]'] = listing_type
        if(listing_type == 1):
            postdata['data[Properties][rental_price]'] = price_baht
            postdata['data[Properties][unit_type_id1]'] = ""
            postdata['data[Properties][unit_type_id2]']= 1
        else:
            postdata['data[Properties][sell_price]'] = price_baht
            postdata['data[Properties][unit_type_id1]'] = 1
            postdata['data[Properties][unit_type_id2]']= ""
        if(listing_type == 4):
            postdata['data[Properties][rental_price]'] = price_baht
            postdata['data[Properties][unit_type_id1]'] = 1
            postdata['data[Properties][unit_type_id2]']= 1
            
        # login
        login = self.test_login(webdata)
        success = login["success"]
        detail = login["detail"]
        post_id = ""
        post_url = ""
        if(success == "True"):
            r = self.httprequestObj.http_get('http://www.prakardproperty.com/properties/add', verify=False)
            data = r.text
            soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
            authenticityToken = soup.find("input", {"name": "data[Properties][running_number]"})['value']
            postdata['data[Properties][running_number]'] = authenticityToken
            contents =[[str(x.text),str(x['value'])] for x in soup.find("select", {"name" :"data[Properties][province_id]" }).find_all('option')]
            # print(contents)
            for i in contents:
                if(i[0] == addr_province):
                    postdata['data[Properties][province_id]'] = i[1]
                    r = self.httprequestObj.http_get('http://www.prakardproperty.com/location/getdistrict/mode:geomap/province_id:'+postdata['data[Properties][province_id]'])
                    # print(r.text)
                    soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
                    districtcontent = [[str(x.text),str(x['value'])] for x in soup.find_all('option')]
                    for i in districtcontent:
                        if(i[0] == addr_district):
                            postdata['data[Properties][district_id]'] = i[1]
                            r = self.httprequestObj.http_get('http://www.prakardproperty.com/location/getsubdistrict/mode:geomap/province_id:'+postdata['data[Properties][province_id]']+'/district_id:'+postdata['data[Properties][district_id]'])
                            # print(r.text)   
                            soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
                            subdistrictcontent = [[str(x.text),str(x['value'])] for x in soup.find_all('option')]
                            for i in subdistrictcontent:
                                if(i[0] == addr_sub_district):
                                    postdata['data[Properties][sub_district_id]'] = i[1]
                                    break
                            break       
                    break
            # print()
            # postdata['files[]'] = r.json()['files']
            # print(postdata)
            for i in range(len(allimages)):
                # print("here in image part")
                # print(os.getcwd())
                filestoup = {'files[]':open(os.getcwd() + '/' + allimages[i] ,'rb')}
                postdata['caption'] = ""
                r = self.httprequestObj.http_post('http://www.prakardproperty.com/filesupload/temp/id:'+str(authenticityToken),data=postdata, files = filestoup)
                # print(r.json())
                postdata['files[]'] = r.json()['files']
            r = self.httprequestObj.http_post('http://www.prakardproperty.com/properties/addsave', data = postdata)#/property/show
            data = r.text
            # print(data)
            matchObj = re.search(r'/property/show', data)
            if not matchObj:
                success = "False"
                detail = "Cannot post to prakardproperty"
            else:
                post_id = re.search(r'/property/show/(\d+)',data).group(1)
                post_url = 'http://www.prakardproperty.com/property/show/'+post_id
        #
        #
        #

        time_end = datetime.datetime.utcnow()
        return {
            "websitename": "prakardproperty",
            "success": success,
            "time_usage": str(time_end - time_start),
            "time_start": str(time_start),
            "time_end": str(time_end),
            "ds_id": "4",
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "",
            "detail": detail
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
            "websitename": "prakardproperty",
            "success": "true",
            "time_usage": time_end - time_start,
            "time_start": time_start,
            "time_end": time_end,
            "detail": "",
            "log_id": log_id,
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
            # print()
            postdata['data[Properties][id]'] = post_id
            # print(postdata)
            
            r = self.httprequestObj.http_post('http://www.prakardproperty.com/properties/delete/'+post_id,data="")#/property/show
            data = r.text
            r = self.httprequestObj.http_get('http://www.prakardproperty.com/member/posted/msg:success')
            # print(r.status_code,r.text)
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
            "time_start": time_start,
            "time_end": time_end,
            "detail": detail,
            "log_id": post_id,
        }


    
    def edit_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        # print(postdata)
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
        project_name = postdata["project_name"]
        land_size_rai = postdata['land_size_rai']
        land_size_ngan = postdata['land_size_ngan']
        land_size_wah = postdata['land_size_wa']
        
        postdata = {
            'data[Properties][id]':webdata['post_id'],
'data[Properties][title]': post_title_en,
'data[Properties][property_type_id]': property_type, # number between 1-9
'data[Properties][property_post_type_id]': listing_type,               #number between 1-9
'data[Properties][sell_price]': price_baht,
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
        if(listing_type == 1):
            postdata['data[Properties][rental_price]'] = price_baht
            postdata['data[Properties][unit_type_id1]'] = ""
            postdata['data[Properties][unit_type_id2]']= 1
        else:
            postdata['data[Properties][sell_price]'] = price_baht
            postdata['data[Properties][unit_type_id1]'] = 1
            postdata['data[Properties][unit_type_id2]']= ""
        if(listing_type == 4):
            postdata['data[Properties][rental_price]'] = price_baht
            postdata['data[Properties][unit_type_id1]'] = 1
            postdata['data[Properties][unit_type_id2]']= 1
            
        # file_list = []
        # for i in post_img_url_lists:
        #     file_list.append(open(i,'rb'))
        # print(file_list)
        # login
        login = self.test_login(webdata)
        success = login["success"]
        detail = login["detail"]
        post_id = webdata['post_id']
        post_url = ""
        if(success == "True"):
            r = self.httprequestObj.http_get('http://www.prakardproperty.com/properties/edit/'+post_id)
            data = r.text
            soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
            try:
                contents =[[str(x.text),str(x['value'])] for x in soup.find("select", {"name" :"data[Properties][province_id]" }).find_all('option')]
                # print(contents)
                for i in contents:
                    if(i[0] == addr_province):
                        postdata['data[Properties][province_id]'] = i[1]
                        r = self.httprequestObj.http_get('http://www.prakardproperty.com/location/getdistrict/mode:geomap/province_id:'+postdata['data[Properties][province_id]'])
                        # print(r.text)
                        soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
                        districtcontent = [[str(x.text),str(x['value'])] for x in soup.find_all('option')]
                        for i in districtcontent:
                            if(i[0] == addr_district):
                                postdata['data[Properties][district_id]'] = i[1]
                                r = self.httprequestObj.http_get('http://www.prakardproperty.com/location/getsubdistrict/mode:geomap/province_id:'+postdata['data[Properties][province_id]']+'/district_id:'+postdata['data[Properties][district_id]'])
                                # print(r.text)   
                                soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
                                subdistrictcontent = [[str(x.text),str(x['value'])] for x in soup.find_all('option')]
                                for i in subdistrictcontent:
                                    if(i[0] == addr_sub_district):
                                        postdata['data[Properties][sub_district_id]'] = i[1]
                                        break
                                break       
                        break
                # print()
                for i in range(len(allimages)):
                    print("here in image part")
                    print(os.getcwd())
                    filestoup = {'files[]':open(os.getcwd() + '/' + allimages[i] ,'rb')}
                    postdata['caption'] = ""
                    r = self.httprequestObj.http_post('http://www.prakardproperty.com/filesupload/properties/id:'+post_id,data=postdata, files = filestoup)
                    # print(r.json())
                postdata['files[]'] = r.json()['files']
                # print(postdata)
                r = self.httprequestObj.http_post('http://www.prakardproperty.com/properties/editsave', data = postdata)#/property/show
                data = r.text
                # print(data)
                matchObj = data
                if not matchObj:
                    success = "False"
                    detail = "Edit Unsuccessful"
                else:
                    post_url = 'http://www.prakardproperty.com/property/show/'+post_id
                    detail = "Edit Successful"
            except:
                success = "False"
                detail = "Edit Unsuccessful"
        #
        #

        time_end = datetime.datetime.utcnow()
        return {
            "websitename": "prakardproperty",
            "success": success,
            "time_usage": str(time_end - time_start),
            "time_start": str(time_start),
            "time_end": str(time_end),
            "ds_id": "4",
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "",
            "detail": detail
        }



    def print_debug(self, msg):
        if(self.debug == 1):
            print(msg)
        return True

    def print_debug_data(self, data):
        if(self.debugdata == 1):
            print(data)
        return True
