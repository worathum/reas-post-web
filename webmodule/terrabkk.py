# -*- coding: utf-8 -*-

from .lib_httprequest import *
from .lib_captcha import *
from bs4 import BeautifulSoup
import os.path
# from urlparse import urlparse
import re
import json
import datetime
import sys
from urllib.parse import unquote
import os


httprequestObj = lib_httprequest()
captcha = lib_captcha()

class terrabkk():

    name = 'terrabkk'

    def __init__(self):

        try:
            import configs
        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.primarydomain = 'http://www.terrabkk.com/'
        self.debug = 0
        self.debugresdata = 0
        self.parser = 'html.parser'

    def register_user(self, userdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        # print("here in register")

        email = userdata['user']
        passwd = userdata['pass']
        name_title = userdata['name_title']
        name_th = userdata['name_th']
        surname_th = userdata['surname_th']
        tel = userdata['tel']
        line = userdata['line']
        nmaetitledic = { "ms": 'นางสาว', "mrs":'นาง', "mr" : 'นาย'}
        try:
            prefix = nmaetitledic[name_title]
        except:
            prefix = 'นาย'
        datapost={
            "hid_mode": "add",
            "txt_prefix": prefix,
            "txt_prefix_more" : "",
            "txt_firstname": name_th,
            "txt_lastname": surname_th,
            "txt_birthday": '04/05/2020',
            "telephone": tel,
            "txt_email": email,
            "line" : line,
            "id_no":"",
            "txt_address" : " ",
            "agent_type" : "2",
            "cert_id" : "",
            "txt_company" : "",
            "txt_company_name" : "",
            "txt_company_website" : "",
            "txt_insurance" : "",
            "province_id[1]" : '1',
            "amphur_id[1]" : "",
            "district_id[1]" : "",
            "street_name[1]" : " ",
            "txt_pass" : passwd,
            "txt_pass2" : passwd,
            "agree": "yes"
        }
        # userfile ofr photo
        filetoup = {
            "userfile" : open(os.getcwd() + "/"+ 'imgtmp/default/white.jpg')
        }
        r = httprequestObj.http_post('https://www.terrabkk.com/member/submit_profile_agent', data = datapost, files=filetoup)
        data = r.text
        matchobj = re.search(r'Terrabkk โปรดยืนยันอีเมล', data)
        # print(matchObj)
        if matchobj:
            success = "True"
            detail = "Successful Registration"
        else:
            success = "False"
            detail = "Registration Unsuccessful"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "terrabkk",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "ds_id":userdata['ds_id']
        }

    def test_login(self, logindata):
        # print("Here in test_login")
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        email_user = logindata['user']
        email_pass = logindata['pass']
        r = httprequestObj.http_get('https://www.terrabkk.com/member/login', verify=False)
        data = r.text
        # with open("/home/maxslide/Real_Estate/temp.html",'w') as f:
        #     f.write(data)
        
        # print(data)
        soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
        recaptcha_token = ""
        print(soup.find("iframe"))
        print(recaptcha_token)
        print()
        datapost = {
            'redirect': "https://www.terrabkk.com/member",
            'email': email_user,
            'password': email_pass
        }
        
        sitekey = "6LdrH6IUAAAAAOG7H98SJ7wv9diFEBuJuPlrDCL1"
        
        g_response = captcha.reCaptcha(sitekey, "https://www.terrabkk.com/member/login")
        if g_response != 0:
            print ("g-response: "+g_response)
            datapost["g-recaptcha-response"] = g_response
            r = httprequestObj.http_post('https://www.terrabkk.com/member/login_ajax', data=datapost)
            success = str(r.json()["state"])
            detail = r.json()["msg"]
        else:
            success = "False"
            detail = "reCaptcha error"
        print(datapost)
        # จำนวนประกาศ this is for login check
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        
        return {
            "websitename": "terrabkk",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "usage_time": str(time_end-time_start),
            "ds_id": logindata['ds_id'],
            "detail": detail,
            "ds_id":logindata['ds_id']
        }
        #
        #
        #
    



    def create_post(self, postdata):
        # https://www.terrabkk.com/post/get_json_district?province_id=13   ->     for district
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        # print(postdata)
        # postdata = postdata
        # print(self.max_image)
        listing_type = postdata['listing_type']
        property_type = postdata['property_type']
        post_img_url_lists = postdata['post_img_url_lists']
        price_baht = postdata['price_baht']
        addr_province = postdata['addr_province']
        addr_district = postdata['addr_district']
        addr_sub_district = postdata['addr_sub_district']
        addr_road, addr_near_by, floorarea_sqm = ['-','','1']
        addr_number = '1'


        '''

        'addr_number' = "1"
        'addr_road' = "-"
        land_size_rai = 0
        land_size_ngang = 0
        land_size_wah = 0
        no of bedroom 
        no of bathroom
        usable sqare mt area 0 not allowed
        no of parking sace
        '''
        if 'addr_road' in postdata and postdata['addr_road']!=None:
            addr_road = postdata['addr_road']
        else:
            addr_road = "-"
        if 'addr_near_by' in postdata:
            addr_near_by = postdata['addr_near_by']
        if 'floorarea_sqm' in postdata:
            floorarea_sqm = postdata['floorarea_sqm']
        if 'addr_number' in postdata:
            addr_number = postdata['addr_number']
        
        geo_latitude = postdata['geo_latitude']
        geo_longitude = postdata['geo_longitude']
        property_id = postdata['property_id']
        post_title_th = postdata['post_title_th']
        post_description_th = postdata['post_description_th']
        post_title_en = postdata['post_title_en']
        # post_description_en = postdata['post_description_en']
        # floor_no = postdata['floor_level']
        # bedroom = postdata['bed_room']
        # bathroom = postdata['bath_room']
        # ds_id = postdata["ds_id"]
        name = postdata["name"]
        mobile = postdata["mobile"]
        email = postdata["email"]
        # account_type = postdata["account_type"]
        user = postdata["user"]
        password = postdata["pass"]
        # project_name = postdata["project_name"]
        land_size_rai = postdata['land_size_rai']
        land_size_ngan = postdata['land_size_ngan']
        land_size_wah = postdata['land_size_wa']
        print("printing create")
        print(land_size_ngan,land_size_rai,land_size_wah)
        if(post_title_en == ''):
            post_title_en = post_title_th
        try :
            # land_size_ngan = land_size_ngan.srtip()
            temp1 = int(land_size_ngan)
            if temp1==None:
                temp1 = 0
        except:
            land_size_ngan = '0'
        try :
            # land_size_rai = land_size_rai.srtip()
            temp1 = int(land_size_rai)
            if temp1==None:
                temp1 = 0
        except:
            land_size_rai = '0'   
        try :
            # land_size_wah = land_size_wah.srtip()
            temp1 = int(land_size_wah)
            if temp1==None:
                temp1 = 0
        except:
            land_size_wah = '0'
        print(land_size_ngan,land_size_rai,land_size_wah)
            
        # post_description_en =  post_description_en.replace("\r\n","<br>")
        # post_description_th =  post_description_th.replace("\r\n","<br>")
        # post_description_th =  post_description_th.replace("\n","<br>")
        
        print(post_description_th)
        province = {}
        # print(addr_province)
        # print(province[addr_province])
        datapost = {
           'act': 'ACT',
            'freepost-id': '',
            'case': '1',
            'freepost-title_th': post_title_th,
            'freepost-title_en': post_title_en + '.',
            'freepost-property_id':'' ,
            'freepost-other_property_name':'' ,
            'freepost-permission': '1',
            'freepost-post_type':'',#check for sell or rent and assign a number
            'freepost-house_type': '', # Assign the property type here
            'freepost_detail-post_by': '12',
            'freepost_detail-build_type': '15',# check for what this build type correcponds to
            'freepost_detail-address_street': addr_number,#check if adress is to be added
            'freepost_detail-address_streetname': addr_road,#check if streetname is to be added
            'freepost_detail-province_id':'',#Add the province id
            'freepost_detail-amphur_id': '',#Add District accordingly
            'freepost_detail-district_id': '',# subdistrict
            'freepost_detail-postcode': '', # check if postal code is generated by some req and then assign it accordingly
            'freepost-lat': geo_latitude,
            'freepost-lng': geo_longitude,
            'freepost-landarea_total_sqw':'', 
            'freepost_detail-landsize_x': '',  #These might be only for land, since no field like this came for condo
            'freepost_detail-landsize_y':'', 
            'freepost_detail-property_condition': '0',
            'freepost_detail-house_style': '0',
            'freepost_detail-tenant': 'yes', 
            'freepost_detail-detail_th': post_description_th,
            'path': 'images/freepost/'
        }
        print(property_type)
        land_area_sq = str(400*int(land_size_rai) + 100*int(land_size_ngan) + 1*int(land_size_wah))
        if(str(property_type) == str(1)):
            datapost['freepost-house_type'] = '7'
            datapost['freepost_detail-landarea_sqw'] = land_area_sq
            try :
                datapost['freepost-areasize_sqm'] = postdata['floor_area']
                a = int(datapost['freepost-areasize_sqm'])
                if datapost['freepost-areasize-sqm'] == None or datapost['freepost-areasize-sqm'] == 0:
                    datapost['freepost-areasize-sqm'] = '1'
            except:
                datapost['freepost-areasize_sqm'] = '1'
            try :
                datapost['freepost_detail-numberoffloors'] = postdata['floor_total']
                a = int(datapost['freepost_detail-numberoffloors'])
            except : 
                datapost['freepost_detail-numberoffloors'] = '1'
            try :
                datapost['freepost_detail-room_type'] = str(43 + min(int(postdata['bed_room']),10))
                a = int(datapost['freepost_detail-room_type'])
            except : 
                datapost['freepost_detail-room_type'] = '44'
            try : 
                datapost['freepost_detail-bathrooms'] = postdata['bath_room']
                a = int(datapost['freepost_detail-bathrooms'])
            except :
                datapost['freepost_detail-bathrooms'] = '1'
            datapost['freepost_detail-livingrooms']='0'  
            datapost['freepost_detail-parking'] = '1'
            datapost['freepost_detail-extrarooms']= '0'
            datapost['freepost_detail-property_finished_year']= '0'
            datapost['freepost_detail-property_buy_year']= '0'
            datapost['freepost_detail-facing']='0'
            
        elif(str(property_type) == str(2)):
            datapost['freepost-house_type'] = '6'
            datapost['freepost-landarea_total_sqw'] = land_area_sq
            datapost['freepost_detail-landarea_sqw'] = land_area_sq
            try :
                datapost['freepost-areasize_sqm'] = postdata['floor_area']
                if datapost['freepost-areasize-sqm'] ==None or datapost['freepost-areasize-sqm'] == 0:
                    datapost['freepost-areasize-sqm'] = '1'
                a = int(datapost['freepost-areasize-sqm'])
            except:
                datapost['freepost-areasize_sqm'] = '1'
            try :
                datapost['freepost_detail-numberoffloors'] = postdata['floor_total']
                a = int(datapost['freepost_detail-numberoffloors'])
            except : 
                datapost['freepost_detail-numberoffloors'] = '1'
            try :
                datapost['freepost_detail-room_type'] = str(43 + min(int(postdata['bed_room']),10))
                a = int(datapost['freepost_detail-room_type'])
            except : 
                datapost['freepost_detail-room_type'] = '44'
            try : 
                datapost['freepost_detail-bathrooms'] = postdata['bath_room']
                a = int(datapost['freepost_detail-bathrooms'])
            except :
                datapost['freepost_detail-bathrooms'] = '1'
            datapost['freepost_detail-livingrooms']='0'  
            datapost['freepost_detail-parking'] = '1'
            #datapost['freepost_detail-parking'] = '0'
            datapost['freepost_detail-extrarooms']= '0'
            datapost['freepost_detail-property_finished_year']= '0'
            datapost['freepost_detail-property_buy_year']= '0'
            datapost['freepost_detail-facing']='0'
        elif(str(property_type) == str(3)):
            datapost['freepost-house_type'] = '197'
            datapost['freepost_detail-landarea_sqw'] = land_area_sq
            datapost['freepost-landarea_total_sqw'] = land_area_sq
            try :
                datapost['freepost-areasize_sqm'] = postdata['floor_area']
                if datapost['freepost-areasize-sqm'] ==None or datapost['freepost-areasize-sqm'] == 0:
                    datapost['freepost-areasize-sqm'] = '1'
                a = int(datapost['freepost-areasize-sqm'])
                
            except:
                datapost['freepost-areasize_sqm'] = '1'
            try :
                datapost['freepost_detail-numberoffloors'] = postdata['floor_total']
                a = int(datapost['freepost_detail-numberoffloors'])
            except : 
                datapost['freepost_detail-numberoffloors'] = '1'
            try :
                datapost['freepost_detail-room_type'] = str(43 + min(int(postdata['bed_room']),10))
                a = int(datapost['freepost_detail-room_type'])
            except : 
                datapost['freepost_detail-room_type'] = '44'
            try : 
                datapost['freepost_detail-bathrooms'] = postdata['bath_room']
                a = int(datapost['freepost_detail-bathrooms'])
            except :
                datapost['freepost_detail-bathrooms'] = '1'
            datapost['freepost_detail-livingrooms']=''  
            datapost['freepost_detail-parking'] = '1'
            #datapost['freepost_detail-parking'] = '0'
            datapost['freepost_detail-extrarooms']= '0'
            datapost['freepost_detail-property_finished_year']= '0'
            datapost['freepost_detail-property_buy_year']= '0'
            datapost['freepost_detail-facing']='0'
        
        elif(str(property_type) == str(4)):
            datapost['freepost-house_type'] = '9'
            datapost['freepost_detail-landarea_sqw'] = land_area_sq
            datapost['freepost-landarea_total_sqw'] = land_area_sq
            try :
                datapost['freepost-areasize_sqm'] = postdata['floor_area']
                if datapost['freepost-areasize-sqm'] ==None or datapost['freepost-areasize-sqm'] == 0:
                    datapost['freepost-areasize-sqm'] = '1'
                a = int(datapost['freepost-areasize-sqm'])
            except:
                datapost['freepost-areasize_sqm'] = '1'    
            try :
                datapost['freepost_detail-numberoffloors'] = postdata['floor_total']
                a = int(datapost['freepost_detail-numberoffloors'])
            except : 
                datapost['freepost_detail-numberoffloors'] = '1'
            try :
                datapost['freepost_detail-room_type'] = str(43 + min(int(postdata['bed_room']),10))
                a = int(datapost['freepost_detail-room_type'])
            except : 
                datapost['freepost_detail-room_type'] = '44' 
            try : 
                datapost['freepost_detail-bathrooms'] = postdata['bath_room']
                a = int(datapost['freepost_detail-bathrooms'])
            except :
                datapost['freepost_detail-bathrooms'] = '1'
            datapost['freepost_detail-livingrooms']=''  
            datapost['freepost_detail-parking'] = '1'
            #datapost['freepost_detail-parking'] = '0'
            datapost['freepost_detail-extrarooms']= '0'
            datapost['freepost_detail-property_finished_year']= '0'
            datapost['freepost_detail-property_buy_year']= '0'
            datapost['freepost_detail-facing']='0',
            datapost['detail-sell_price_type']=''
        elif(str(property_type) == str(5)):
            datapost['freepost-house_type'] = '10'
            datapost['freepost_detail-landarea_sqw'] = land_area_sq
            datapost['freepost-landarea_total_sqw'] = land_area_sq
            try :
                datapost['freepost-areasize_sqm'] = str(postdata['floor_area'])
                if datapost['freepost-areasize-sqm'] ==None or datapost['freepost-areasize-sqm'] == 0:
                    datapost['freepost-areasize-sqm'] = '1'
                a = int(datapost['freepost-areasize-sqm'])
                
            except:
                datapost['freepost-areasize_sqm'] = '1'
            try :
                datapost['freepost_detail-numberoffloors'] = postdata['floor_total']
                a = int(datapost['freepost_detail-numberoffloors'])
            except : 
                datapost['freepost_detail-numberoffloors'] = '1'
            try :
                datapost['freepost_detail-room_type'] = str(43 + min(int(postdata['bed_room']),10))
                a = int(datapost['freepost_detail-room_type'])
            except : 
                datapost['freepost_detail-room_type'] = '44'
            try : 
                datapost['freepost_detail-bathrooms'] = postdata['bath_room']
                a = int(datapost['freepost_detail-bathrooms'])
            except :
                datapost['freepost_detail-bathrooms'] = '1'
            datapost['freepost_detail-livingrooms']=''  
            datapost['freepost_detail-parking'] = '1'
            datapost['freepost_detail-extrarooms']= '0'
            datapost['freepost_detail-property_finished_year']= '0'
            datapost['freepost_detail-property_buy_year']= '0'
            datapost['freepost_detail-facing']='0'
            datapost['freepost_detail-sell_discount_price']=''
            datapost['freepost-sell_price_type'] = ''
            del datapost['freepost_detail-build_type']
        
        elif(str(property_type) == str(6)):
            datapost['freepost-house_type'] = '8'
            datapost['freepost_detail-landarea_rai'] = land_size_rai
            datapost['freepost_detail-landarea_ngaan'] = land_size_ngan
            datapost['freepost_detail-landarea_sqw'] = land_size_wah
            try:
                datapost['freepost-landarea_total_sqw'] = str(400*int(land_size_rai) + 100*int(land_size_ngan) + 1*int(land_size_wah))
                a = int(datapost['freepost-landarea_total_sqw'])
            except:
                datapost['freepost-landarea_total_sqw'] = '0'
                
            datapost['freepost-sell_price_type'] = '26'
        
        elif(str(property_type) == str(7)):
            datapost['freepost-house_type'] = '209'
            datapost['freepost_detail-landarea_rai'] = land_size_rai
            datapost['freepost_detail-landarea_ngaan'] = land_size_ngan
            datapost['freepost_detail-landarea_sqw'] = land_size_wah
            
            try :
                datapost['freepost-areasize_sqm'] = postdata['floor_area']
                if datapost['freepost-areasize-sqm'] ==None or datapost['freepost-areasize-sqm'] == 0:
                    datapost['freepost-areasize-sqm'] = '1'
                a = int(datapost['freepost-areasize-sqm'])
            except:
                datapost['freepost-areasize_sqm'] = '1'
            
            try:
                datapost['freepost-landarea_total_sqw'] = str(400*int(land_size_rai) + 100*int(land_size_ngan) + 1*int(land_size_wah))
                a = int(datapost['freepost-landarea_total_sqw'])
            except:
                datapost['freepost-landarea_total_sqw'] = '0'
            try :
                datapost['freepost_detail-numberoffloors'] = postdata['floor_total']
                a = int(datapost['freepost_detail-numberoffloors'])
            except : 
                datapost['freepost_detail-numberoffloors'] = '0'
            try :
                datapost['freepost_detail-room_type'] = str(43 + min(int(postdata['bed_room']),10))
                a = int(datapost['freepost_detail-room_type'])
            except : 
                datapost['freepost_detail-room_type'] = '0'
            try : 
                datapost['freepost_detail-bathrooms'] = postdata['bath_room']
                a = int(datapost['freepost_detail-bathrooms'])
            except :
                datapost['freepost_detail-bathrooms'] = '0'
            datapost['freepost_detail-livingrooms']=''  
            datapost['freepost_detail-parking'] = '0'
            datapost['freepost_detail-extrarooms']= '0'
            datapost['freepost_detail-property_finished_year']= '0'
            datapost['freepost_detail-property_buy_year']= '0'
            datapost['freepost_detail-facing']='0'
            datapost['freepost-sell_price_type'] = ''
            datapost['freepost_detail-sell_discount_price']=''
            
        elif(str(property_type) == str(8)):
            datapost['freepost-house_type'] = '210'
            datapost['freepost_detail-landarea_rai'] = land_size_rai
            datapost['freepost_detail-landarea_ngaan'] = land_size_ngan
            datapost['freepost_detail-landarea_sqw'] = land_size_wah
            try :
                datapost['freepost-are  asize_sqm'] = postdata['floor_area']
                if datapost['freepost-areasize-sqm'] ==None or datapost['freepost-areasize-sqm'] == 0:
                    datapost['freepost-areasize-sqm'] = '1'
                a = int(datapost['freepost-areasize-sqm'])
            except:
                datapost['freepost-areasize_sqm'] = '1'
            try:
                datapost['freepost-landarea_total_sqw'] = str(400*int(land_size_rai) + 100*int(land_size_ngan) + 1*int(land_size_wah))
                a = int(datapost['freepost-landarea_total_sqw'])
            except:
                datapost['freepost-landarea_total_sqw'] = '0'
            try :
                datapost['freepost_detail-numberoffloors'] = postdata['floor_total']
                a = int(datapost['freepost_detail-numberoffloors'])
            except : 
                datapost['freepost_detail-numberoffloors'] = '0'
            try :
                datapost['freepost_detail-room_type'] = str(43 + min(int(postdata['bed_room']),10))
                a = int(datapost['freepost_detail-room_type'])
            except : 
                datapost['freepost_detail-room_type'] = '0'
            try : 
                datapost['freepost_detail-bathrooms'] = postdata['bath_room']
                a = int(datapost['freepost_detail-bathrooms'])
            except :
                datapost['freepost_detail-bathrooms'] = '0'
            datapost['freepost_detail-livingrooms']=''  
            datapost['freepost_detail-parking'] = '0'
            datapost['freepost_detail-extrarooms']= '0'
            datapost['freepost_detail-property_finished_year']= '0'
            datapost['freepost_detail-property_buy_year']= '0'
            datapost['freepost_detail-facing']='0'
            
        elif(str(property_type) == str(9)):
            datapost['freepost_detail-landarea_rai'] = land_size_rai
            datapost['freepost_detail-landarea_ngaan'] = land_size_ngan
            datapost['freepost-house_type'] = '208'
            datapost['freepost_detail-landarea_sqw'] = land_area_sq
            datapost['freepost-landarea_total_sqw'] = land_area_sq
            try :
                datapost['freepost-areasize_sqm'] = postdata['floor_area']
                if datapost['freepost-areasize-sqm'] ==None or datapost['freepost-areasize-sqm'] == 0:
                    datapost['freepost-areasize-sqm'] = '1'
                a = int(datapost['freepost-areasize-sqm'])
                
            except:
                datapost['freepost-areasize_sqm'] = '1'
            try :
                datapost['freepost_detail-numberoffloors'] = postdata['floor_total']
                a = int(datapost['freepost_detail-numberoffloors'])
            except : 
                datapost['freepost_detail-numberoffloors'] = '0'
            try : 
                datapost['freepost_detail-bathrooms'] = postdata['bath_room']
                a = int(datapost['freepost_detail-bathrooms'])
            except :
                datapost['freepost_detail-bathrooms'] = '0'
            datapost['freepost_detail-parking'] = '0'
            datapost['freepost-sell_price_type'] = '26'
            datapost['freepost_detail-livingrooms']='' 
            datapost['freepost_detail-parking']=''
            datapost['freepost_detail-extrarooms']='' 
            datapost['freepost_detail-property_finished_year']= '0'
            datapost['freepost_detail-property_buy_year']= '0'
            datapost['freepost_detail-facing']='0'
            

        elif(str(property_type) == str(10)):
            datapost['freepost-house_type'] = '207'
            datapost['freepost_detail-landarea_sqw'] = land_area_sq
            datapost['freepost-landarea_total_sqw'] = land_area_sq
            try :
                datapost['freepost-areasize_sqm'] = postdata['floor_area']
                if datapost['freepost-areasize-sqm'] ==None or datapost['freepost-areasize-sqm'] == 0:
                    datapost['freepost-areasize-sqm'] = '1'
                a = int(datapost['freepost-areasize-sqm'])
            except:
                datapost['freepost-areasize_sqm'] = '1'
            try :
                datapost['freepost_detail-numberoffloors'] = postdata['floor_total']
                a = int(datapost['freepost_detail-numberoffloors'])
            except : 
                datapost['freepost_detail-numberoffloors'] = '0'
            try :
                datapost['freepost_detail-room_type'] = str(43 + min(int(postdata['bed_room']),10))
                a = int(datapost['freepost_detail-room_type'])
            except : 
                datapost['freepost_detail-room_type'] = '0'
            try : 
                datapost['freepost_detail-bathrooms'] = postdata['bath_room']
                a = int(datapost['freepost_detail-bathrooms'])
            except :
                datapost['freepost_detail-bathrooms'] = '0'
            datapost['freepost_detail-parking'] = '0'
            datapost['freepost-sell_price_type'] = '26'

        elif(str(property_type) == str(25)):
            datapost['freepost-house_type'] = '206'
            datapost['freepost_detail-landarea_sqw'] = land_area_sq
            datapost['freepost-landarea_total_sqw'] = land_area_sq
            try :
                datapost['freepost-areasize_sqm'] = postdata['floor_area']
                if datapost['freepost-areasize-sqm'] ==None or datapost['freepost-areasize-sqm'] == 0:
                    datapost['freepost-areasize-sqm'] = '1'
                a = int(datapost['freepost-areasize-sqm'])
            except:
                datapost['freepost-areasize_sqm'] = '1'
            try :
                datapost['freepost_detail-numberoffloors'] = postdata['floor_total']
                a = int(datapost['freepost_detail-numberoffloors'])
            except : 
                datapost['freepost_detail-numberoffloors'] = '0'
            datapost['freepost_detail-parking'] = '0'
            datapost['freepost-sell_price_type'] = '26'
            
            
        
        else:
            datapost['freepost-house_type'] = '11'
            
            
            
        if(listing_type == 'ขาย'):
            datapost['freepost-post_type'] = '1'
            datapost['freepost-sell_price']= price_baht
            datapost['freepost-sell_price_type']='26'
            datapost['freepost_detail-sell_discount_price']=''
        else:
            datapost['freepost-post_type'] = '4'
            datapost['freepost_detail-rent_year'] = '34' #1 year rent
            datapost['freepost-rent_price'] = price_baht
            
        with open('./static/9asset_province.json',encoding='utf-8') as f:
            province = json.load(f)
        # print(province)
        for key in province:
            # print("bleh")
            # print(province[key])
            if (addr_province.find(str(province[key]).strip()) != -1) :
                # print("equuaallll")
                addr_province = key
                datapost['freepost_detail-province_id'] = '1' #addr_province
        # login
        login = self.test_login(postdata)
        success = login["success"]
        detail = login["detail"]
        post_id = ""
        post_url = ""
        filestoup = {}
        print(success)
        print(success=="True")
        if(success == "True"):
            datapost['freepost_detail-province_id'] = '1'
            datapost['freepost_detail-district_id'] = '1' #i["id"]
            datapost['freepost_detail-district_id'] = '1' #i["id"]
            # print("debug2")
            # for i in range(len(postdata['post_images'][:10])):
            #     filestoup.append(('imgs', open(os.getcwd() + "/"+ postdata['post_images'][i],'rb')))
            #     filestoup.append(('imgs[]', open(os.getcwd() + "/"+ postdata['post_images'][i],'rb')))

            r = httprequestObj.http_get('https://www.terrabkk.com/freepost/get_amphur_ajax/'+str(datapost['freepost_detail-province_id']), verify=False)
            data = r.json()
            print(data)
            print("sent district : ",addr_district)
            addr_district = addr_district.replace(' ','')
            for i in data:
                if(addr_district.find(i["name"]) != -1 or i["name"].find(addr_district) != -1):
                    datapost['freepost_detail-amphur_id'] = '1' #i["id"]
                    break
            r = httprequestObj.http_get('https://www.terrabkk.com/freepost/get_district_ajax/'+str(datapost['freepost_detail-amphur_id']), verify=False)    
            data = r.json()
            addr_sub_district = addr_sub_district.replace(' ','')
            for i in data:
                if(addr_sub_district.find(i["name"]) != -1 or i["name"].find(addr_sub_district) != -1):
                    datapost['freepost_detail-district_id'] ='1' #  i["id"]
                    break
            r = httprequestObj.http_get('https://www.terrabkk.com/freepost/get_postcode_ajax/'+str(datapost['freepost_detail-district_id']),verify=False)
            datapost['freepost_detail-postcode'] = r.text.replace("\"",'')
            r = httprequestObj.http_post('https://www.terrabkk.com/freepost/add_freepost_draft', data = datapost)#/property/show
            print(r)
            # print(r.text)
            data = r.json()
            # print(data)
            check = data['state']
            datapost['freepost-id'] = str(data['freepost_id'])
            print("The data to be posted \n",datapost)
            newdatapost = []
            for key in datapost:
                newdatapost.append((key,datapost[key]))
            temp = []
            for i in range(len(postdata['post_images'][:10])):
                filestoup['imgs']=  open(os.getcwd() + "/"+ postdata['post_images'][i],'rb')
                filestoup['imgs[]'] = open(os.getcwd() + "/"+ postdata['post_images'][i],'rb')
                r = httprequestObj.http_post('https://www.terrabkk.com/uploader_front/freepost_img_upload/'+datapost['freepost-id'],data = newdatapost,files=filestoup)
                data = r.json()
                # print(r.text)
                soup = BeautifulSoup(r.json()['text'], self.parser, from_encoding='utf-8')
                r = soup.find('input',{"name" : "allpic[]"})["value"]
                print(r)
                temp.append(('allpic[]',r))
                
            # print(data)
            # newdatapost = []
            # for key in datapost:
            #     newdatapost.append((key,datapost[key]))
            # newdatapost.append(('freepost-id',datapost['freepost-id']))
            # print(str(data["status"]))
            print(check)
            if(check) :
                # soup = BeautifulSoup(data['text'], self.parser, from_encoding='utf-8')
                # r = soup.findAll('input',{"name" : "allpic[]"})
                # # print(r)
                for i in temp:
                    newdatapost.append(i)
                print(newdatapost)
                r = httprequestObj.http_post('https://www.terrabkk.com/free-post/'+datapost['freepost-id'],data=newdatapost)
                with open('b.html','w') as f:
                    f.write(r.text)
                # print("Written")
                if(re.search(r'โพสสำเร็จ',r.text)):
                    success = "True"
                    detail = "posted"
                    post_id = datapost['freepost-id']
                    post_url = 'https://www.terrabkk.com/freepost/show/'+post_id
                else:
                    success = "False"
                    detail = "Post unsuccessful"
            else :
                success = "False"
                detail = "Image not uploaded"
             
        else:
           success = "False"
           detail = "Unsuccessful Login"
        
        time_end = datetime.datetime.utcnow()
        print({
            "websitename": "terrabkk",
            "success": success,
            "time_usage": time_end - time_start,
            "time_start": time_start,
            "time_end": time_end,
            "ds_id": postdata['ds_id'],
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "",
            "detail": detail
        }
        )
        return {
            "websitename": "terrabkk",
            "success": success,
            "time_usage": time_end - time_start,
            "time_start": time_start,
            "time_end": time_end,
            "ds_id": postdata['ds_id'],
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
        email_user = postdata['user']
        email_pass = postdata['pass']
        #https://www.terrabkk.com/member
        #
        #
        #
        login = self.test_login(postdata)
        success = login["success"]
        detail = login["detail"]
        if(success == "True"):
            
            r = httprequestObj.http_get('https://www.terrabkk.com/freepost/push/'+str(post_id),verify=False)
            # with open('/home/maxslide/Real_Estate/temp.html','w') as f:
            #     f.write(r.text)
            # print("Written")
            if(r.text):
                success = "True"
                detail = "Boosted"
            else:
                success = "False"
                detail = "Not boosted"
        time_end = datetime.datetime.utcnow()
        return {
            "websitename": "terrabkk",
            "success": success ,
            "time_usage": time_end - time_start,
            "time_start": time_start,
            "time_end": time_end,
            "ds_id": postdata['ds_id'],
            "detail": detail,
            "log_id": log_id,
            "post_id": post_id,
        }

    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        
        datapost = {'onsubmit': 'return remove_checkform();',
        'freepost_id': '',
        'remove-course': '3',
        'remove-sellprice':'', 
        'remove-date': '',
        'remove-desc': 'dets'}
        login = self.test_login(postdata)
        success = login["success"]
        detail = login["detail"]
        post_id = postdata['post_id']
        post_url = ''+post_id
        if(success == "True"):
            # print()
            # print(postdata)
            r = httprequestObj.http_post('https://www.terrabkk.com/freepost/client_cancel/'+str(post_id),data=datapost)#/property/show
            data = r.json()
            # print(data)
            # print(r.status_code)
            success = str(data["state"])
            detail = data["msg"]

        #
        #
        #

        time_end = datetime.datetime.utcnow()
        return {
            "websitename": "terrabkk",
            "success": success,
            "usage_time": time_end - time_start,
            "start_time": time_start,
            "end_time": time_end,
            "detail": detail,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
        }

    def edit_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        # print(postdata)
        # postdata = postdata
        # print(self.max_image)
        listing_type = postdata['listing_type']
        property_type = postdata['property_type']
        post_img_url_lists = postdata['post_img_url_lists']
        price_baht = postdata['price_baht']
        addr_province = postdata['addr_province']
        addr_district = postdata['addr_district']
        addr_sub_district = postdata['addr_sub_district']
        addr_road, addr_near_by, floorarea_sqm = ['','','']
        addr_number = '1'
        if 'addr_road' in postdata:
            addr_road = postdata['addr_road']
        if 'addr_near_by' in postdata:
            addr_near_by = postdata['addr_near_by']
        if 'floorarea_sqm' in postdata:
            floorarea_sqm = postdata['floorarea_sqm']
        if 'addr_number' in postdata:
            addr_number = postdata['addr_number']
        
        
        geo_latitude = postdata['geo_latitude']
        geo_longitude = postdata['geo_longitude']
        property_id = postdata['property_id']
        post_title_th = postdata['post_title_th']
        post_description_th = postdata['post_description_th']
        post_title_en = postdata['post_title_th']
        # post_description_en = postdata['post_description_en']
        # floor_no = postdata['floor_level']
        # bedroom = postdata['bed_room']
        # bathroom = postdata['bath_room']
        # ds_id = postdata["ds_id"]
        name = postdata["name"]
        mobile = postdata["mobile"]
        email = postdata["email"]
        # account_type = postdata["account_type"]
        user = postdata["user"]
        password = postdata["pass"]
        # project_name = postdata["project_name"]
        land_size_rai = postdata['land_size_rai']
        land_size_ngan = postdata['land_size_ngan']
        land_size_wah = postdata['land_size_wa']
        print("printing create")
        print(land_size_ngan,land_size_rai,land_size_wah)
        if(post_title_en == ''):
            post_title_en = post_title_th
        try :
            # land_size_ngan = land_size_ngan.srtip()
            temp1 = int(land_size_ngan)
        except:
            land_size_ngan = '0'
        try :
            # land_size_rai = land_size_rai.srtip()
            temp1 = int(land_size_rai)
        except:
            land_size_rai = '0'   
        try :
            # land_size_wah = land_size_wah.srtip()
            temp1 = int(land_size_wah)
        except:
            land_size_wah = '0'
        print(land_size_ngan,land_size_rai,land_size_wah)
            
        # post_description_en =  post_description_en.replace("\r\n","<br>")
        # post_description_th =  post_description_th.replace("\r\n","<br>")
        # post_description_th =  post_description_th.replace("\n","<br>")
        
        print(post_description_th)
        province = {}
        # print(addr_province)
        # print(province[addr_province])
        datapost = {
           'act': 'ACT',
            'freepost-id': '',
            'case': '1',
            'freepost-title_th': post_title_th,
            'freepost-title_en': post_title_en + '.',
            'freepost-property_id':'' ,
            'freepost-other_property_name':'' ,
            'freepost-permission': '1',
            'freepost-post_type':'',#check for sell or rent and assign a number
            'freepost-house_type': '', # Assign the property type here
            'freepost_detail-post_by': '12',
            'freepost_detail-build_type': '15',# check for what this build type correcponds to
            'freepost_detail-address_street': addr_number,#check if adress is to be added
            'freepost_detail-address_streetname': addr_road,#check if streetname is to be added
            'freepost_detail-province_id':'',#Add the province id
            'freepost_detail-amphur_id': '',#Add District accordingly
            'freepost_detail-district_id': '',# subdistrict
            'freepost_detail-postcode': '', # check if postal code is generated by some req and then assign it accordingly
            'freepost-lat': geo_latitude,
            'freepost-lng': geo_longitude,
            'freepost-landarea_total_sqw':'', 
            'freepost_detail-landsize_x': '',  #These might be only for land, since no field like this came for condo
            'freepost_detail-landsize_y':'', 
            'freepost_detail-property_condition': '0',
            'freepost_detail-house_style': '0',
            'freepost_detail-tenant': 'yes', 
            'freepost_detail-detail_th': post_description_th,
            'path': 'images/freepost/'
        }
        print(property_type)
        land_area_sq = str(400*int(land_size_rai) + 100*int(land_size_ngan) + 1*int(land_size_wah))
        if(str(property_type) == str(1)):
            datapost['freepost-house_type'] = '7'
            datapost['freepost_detail-landarea_sqw'] = land_area_sq
            try :
                datapost['freepost-areasize_sqm'] = postdata['floor_area']
                a = int(datapost['freepost-areasize_sqm'])
                if datapost['freepost-areasize-sqm'] == None or datapost['freepost-areasize-sqm'] == 0:
                    datapost['freepost-areasize-sqm'] = '1'
            except:
                datapost['freepost-areasize_sqm'] = '1'
            try :
                datapost['freepost_detail-numberoffloors'] = postdata['floor_total']
                a = int(datapost['freepost_detail-numberoffloors'])
            except : 
                datapost['freepost_detail-numberoffloors'] = '1'
            try :
                datapost['freepost_detail-room_type'] = str(43 + min(int(postdata['bed_room']),10))
                a = int(datapost['freepost_detail-room_type'])
            except : 
                datapost['freepost_detail-room_type'] = '44'
            try : 
                datapost['freepost_detail-bathrooms'] = postdata['bath_room']
                a = int(datapost['freepost_detail-bathrooms'])
            except :
                datapost['freepost_detail-bathrooms'] = '1'
            datapost['freepost_detail-livingrooms']='0'  
            datapost['freepost_detail-parking'] = '1'
            datapost['freepost_detail-extrarooms']= '0'
            datapost['freepost_detail-property_finished_year']= '0'
            datapost['freepost_detail-property_buy_year']= '0'
            datapost['freepost_detail-facing']='0'
            
        elif(str(property_type) == str(2)):
            datapost['freepost-house_type'] = '6'
            datapost['freepost-landarea_total_sqw'] = land_area_sq
            datapost['freepost_detail-landarea_sqw'] = land_area_sq
            try :
                datapost['freepost-areasize_sqm'] = postdata['floor_area']
                if datapost['freepost-areasize-sqm'] ==None or datapost['freepost-areasize-sqm'] == 0:
                    datapost['freepost-areasize-sqm'] = '1'
                a = int(datapost['freepost-areasize-sqm'])
            except:
                datapost['freepost-areasize_sqm'] = '1'
            try :
                datapost['freepost_detail-numberoffloors'] = postdata['floor_total']
                a = int(datapost['freepost_detail-numberoffloors'])
            except : 
                datapost['freepost_detail-numberoffloors'] = '1'
            try :
                datapost['freepost_detail-room_type'] = str(43 + min(int(postdata['bed_room']),10))
                a = int(datapost['freepost_detail-room_type'])
            except : 
                datapost['freepost_detail-room_type'] = '44'
            try : 
                datapost['freepost_detail-bathrooms'] = postdata['bath_room']
                a = int(datapost['freepost_detail-bathrooms'])
            except :
                datapost['freepost_detail-bathrooms'] = '1'
            datapost['freepost_detail-livingrooms']='0'  
            datapost['freepost_detail-parking'] = '1'
            #datapost['freepost_detail-parking'] = '0'
            datapost['freepost_detail-extrarooms']= '0'
            datapost['freepost_detail-property_finished_year']= '0'
            datapost['freepost_detail-property_buy_year']= '0'
            datapost['freepost_detail-facing']='0'
        elif(str(property_type) == str(3)):
            datapost['freepost-house_type'] = '197'
            datapost['freepost_detail-landarea_sqw'] = land_area_sq
            datapost['freepost-landarea_total_sqw'] = land_area_sq
            try :
                datapost['freepost-areasize_sqm'] = postdata['floor_area']
                if datapost['freepost-areasize-sqm'] ==None or datapost['freepost-areasize-sqm'] == 0:
                    datapost['freepost-areasize-sqm'] = '1'
                a = int(datapost['freepost-areasize-sqm'])
                
            except:
                datapost['freepost-areasize_sqm'] = '1'
            try :
                datapost['freepost_detail-numberoffloors'] = postdata['floor_total']
                a = int(datapost['freepost_detail-numberoffloors'])
            except : 
                datapost['freepost_detail-numberoffloors'] = '1'
            try :
                datapost['freepost_detail-room_type'] = str(43 + min(int(postdata['bed_room']),10))
                a = int(datapost['freepost_detail-room_type'])
            except : 
                datapost['freepost_detail-room_type'] = '44'
            try : 
                datapost['freepost_detail-bathrooms'] = postdata['bath_room']
                a = int(datapost['freepost_detail-bathrooms'])
            except :
                datapost['freepost_detail-bathrooms'] = '1'
            datapost['freepost_detail-livingrooms']=''  
            datapost['freepost_detail-parking'] = '1'
            #datapost['freepost_detail-parking'] = '0'
            datapost['freepost_detail-extrarooms']= '0'
            datapost['freepost_detail-property_finished_year']= '0'
            datapost['freepost_detail-property_buy_year']= '0'
            datapost['freepost_detail-facing']='0'
        
        elif(str(property_type) == str(4)):
            datapost['freepost-house_type'] = '9'
            datapost['freepost_detail-landarea_sqw'] = land_area_sq
            datapost['freepost-landarea_total_sqw'] = land_area_sq
            try :
                datapost['freepost-areasize_sqm'] = postdata['floor_area']
                if datapost['freepost-areasize-sqm'] ==None or datapost['freepost-areasize-sqm'] == 0:
                    datapost['freepost-areasize-sqm'] = '1'
                a = int(datapost['freepost-areasize-sqm'])
            except:
                datapost['freepost-areasize_sqm'] = '1'    
            try :
                datapost['freepost_detail-numberoffloors'] = postdata['floor_total']
                a = int(datapost['freepost_detail-numberoffloors'])
            except : 
                datapost['freepost_detail-numberoffloors'] = '1'
            try :
                datapost['freepost_detail-room_type'] = str(43 + min(int(postdata['bed_room']),10))
                a = int(datapost['freepost_detail-room_type'])
            except : 
                datapost['freepost_detail-room_type'] = '44' 
            try : 
                datapost['freepost_detail-bathrooms'] = postdata['bath_room']
                a = int(datapost['freepost_detail-bathrooms'])
            except :
                datapost['freepost_detail-bathrooms'] = '1'
            datapost['freepost_detail-livingrooms']=''  
            datapost['freepost_detail-parking'] = '1'
            #datapost['freepost_detail-parking'] = '0'
            datapost['freepost_detail-extrarooms']= '0'
            datapost['freepost_detail-property_finished_year']= '0'
            datapost['freepost_detail-property_buy_year']= '0'
            datapost['freepost_detail-facing']='0',
            datapost['detail-sell_price_type']=''
        elif(str(property_type) == str(5)):
            datapost['freepost-house_type'] = '10'
            datapost['freepost_detail-landarea_sqw'] = land_area_sq
            datapost['freepost-landarea_total_sqw'] = land_area_sq
            try :
                datapost['freepost-areasize_sqm'] = str(postdata['floor_area'])
                if datapost['freepost-areasize-sqm'] ==None or datapost['freepost-areasize-sqm'] == 0:
                    datapost['freepost-areasize-sqm'] = '1'
                a = int(datapost['freepost-areasize-sqm'])
                
            except:
                datapost['freepost-areasize_sqm'] = '1'
            try :
                datapost['freepost_detail-numberoffloors'] = postdata['floor_total']
                a = int(datapost['freepost_detail-numberoffloors'])
            except : 
                datapost['freepost_detail-numberoffloors'] = '1'
            try :
                datapost['freepost_detail-room_type'] = str(43 + min(int(postdata['bed_room']),10))
                a = int(datapost['freepost_detail-room_type'])
            except : 
                datapost['freepost_detail-room_type'] = '44'
            try : 
                datapost['freepost_detail-bathrooms'] = postdata['bath_room']
                a = int(datapost['freepost_detail-bathrooms'])
            except :
                datapost['freepost_detail-bathrooms'] = '1'
            datapost['freepost_detail-livingrooms']=''  
            datapost['freepost_detail-parking'] = '1'
            datapost['freepost_detail-extrarooms']= '0'
            datapost['freepost_detail-property_finished_year']= '0'
            datapost['freepost_detail-property_buy_year']= '0'
            datapost['freepost_detail-facing']='0'
            datapost['freepost_detail-sell_discount_price']=''
            datapost['freepost-sell_price_type'] = ''
            del datapost['freepost_detail-build_type']
        
        elif(str(property_type) == str(6)):
            datapost['freepost-house_type'] = '8'
            datapost['freepost_detail-landarea_rai'] = land_size_rai
            datapost['freepost_detail-landarea_ngaan'] = land_size_ngan
            datapost['freepost_detail-landarea_sqw'] = land_size_wah
            try:
                datapost['freepost-landarea_total_sqw'] = str(400*int(land_size_rai) + 100*int(land_size_ngan) + 1*int(land_size_wah))
                a = int(datapost['freepost-landarea_total_sqw'])
            except:
                datapost['freepost-landarea_total_sqw'] = '0'
                
            datapost['freepost-sell_price_type'] = '26'
        
        elif(str(property_type) == str(7)):
            datapost['freepost-house_type'] = '209'
            datapost['freepost_detail-landarea_rai'] = land_size_rai
            datapost['freepost_detail-landarea_ngaan'] = land_size_ngan
            datapost['freepost_detail-landarea_sqw'] = land_size_wah
            
            try :
                datapost['freepost-areasize_sqm'] = postdata['floor_area']
                if datapost['freepost-areasize-sqm'] ==None or datapost['freepost-areasize-sqm'] == 0:
                    datapost['freepost-areasize-sqm'] = '1'
                a = int(datapost['freepost-areasize-sqm'])
            except:
                datapost['freepost-areasize_sqm'] = '1'
            
            try:
                datapost['freepost-landarea_total_sqw'] = str(400*int(land_size_rai) + 100*int(land_size_ngan) + 1*int(land_size_wah))
                a = int(datapost['freepost-landarea_total_sqw'])
            except:
                datapost['freepost-landarea_total_sqw'] = '0'
            try :
                datapost['freepost_detail-numberoffloors'] = postdata['floor_total']
                a = int(datapost['freepost_detail-numberoffloors'])
            except : 
                datapost['freepost_detail-numberoffloors'] = '0'
            try :
                datapost['freepost_detail-room_type'] = str(43 + min(int(postdata['bed_room']),10))
                a = int(datapost['freepost_detail-room_type'])
            except : 
                datapost['freepost_detail-room_type'] = '0'
            try : 
                datapost['freepost_detail-bathrooms'] = postdata['bath_room']
                a = int(datapost['freepost_detail-bathrooms'])
            except :
                datapost['freepost_detail-bathrooms'] = '0'
            datapost['freepost_detail-livingrooms']=''  
            datapost['freepost_detail-parking'] = '0'
            datapost['freepost_detail-extrarooms']= '0'
            datapost['freepost_detail-property_finished_year']= '0'
            datapost['freepost_detail-property_buy_year']= '0'
            datapost['freepost_detail-facing']='0'
            datapost['freepost-sell_price_type'] = ''
            datapost['freepost_detail-sell_discount_price']=''
            
        elif(str(property_type) == str(8)):
            datapost['freepost-house_type'] = '210'
            datapost['freepost_detail-landarea_rai'] = land_size_rai
            datapost['freepost_detail-landarea_ngaan'] = land_size_ngan
            datapost['freepost_detail-landarea_sqw'] = land_size_wah
            try :
                datapost['freepost-are  asize_sqm'] = postdata['floor_area']
                if datapost['freepost-areasize-sqm'] ==None or datapost['freepost-areasize-sqm'] == 0:
                    datapost['freepost-areasize-sqm'] = '1'
                a = int(datapost['freepost-areasize-sqm'])
            except:
                datapost['freepost-areasize_sqm'] = '1'
            try:
                datapost['freepost-landarea_total_sqw'] = str(400*int(land_size_rai) + 100*int(land_size_ngan) + 1*int(land_size_wah))
                a = int(datapost['freepost-landarea_total_sqw'])
            except:
                datapost['freepost-landarea_total_sqw'] = '0'
            try :
                datapost['freepost_detail-numberoffloors'] = postdata['floor_total']
                a = int(datapost['freepost_detail-numberoffloors'])
            except : 
                datapost['freepost_detail-numberoffloors'] = '0'
            try :
                datapost['freepost_detail-room_type'] = str(43 + min(int(postdata['bed_room']),10))
                a = int(datapost['freepost_detail-room_type'])
            except : 
                datapost['freepost_detail-room_type'] = '0'
            try : 
                datapost['freepost_detail-bathrooms'] = postdata['bath_room']
                a = int(datapost['freepost_detail-bathrooms'])
            except :
                datapost['freepost_detail-bathrooms'] = '0'
            datapost['freepost_detail-livingrooms']=''  
            datapost['freepost_detail-parking'] = '0'
            datapost['freepost_detail-extrarooms']= '0'
            datapost['freepost_detail-property_finished_year']= '0'
            datapost['freepost_detail-property_buy_year']= '0'
            datapost['freepost_detail-facing']='0'
            
        elif(str(property_type) == str(9)):
            datapost['freepost_detail-landarea_rai'] = land_size_rai
            datapost['freepost_detail-landarea_ngaan'] = land_size_ngan
            datapost['freepost-house_type'] = '208'
            datapost['freepost_detail-landarea_sqw'] = land_area_sq
            datapost['freepost-landarea_total_sqw'] = land_area_sq
            try :
                datapost['freepost-areasize_sqm'] = postdata['floor_area']
                if datapost['freepost-areasize-sqm'] ==None or datapost['freepost-areasize-sqm'] == 0:
                    datapost['freepost-areasize-sqm'] = '1'
                a = int(datapost['freepost-areasize-sqm'])
                
            except:
                datapost['freepost-areasize_sqm'] = '1'
            try :
                datapost['freepost_detail-numberoffloors'] = postdata['floor_total']
                a = int(datapost['freepost_detail-numberoffloors'])
            except : 
                datapost['freepost_detail-numberoffloors'] = '0'
            try : 
                datapost['freepost_detail-bathrooms'] = postdata['bath_room']
                a = int(datapost['freepost_detail-bathrooms'])
            except :
                datapost['freepost_detail-bathrooms'] = '0'
            datapost['freepost_detail-parking'] = '0'
            datapost['freepost-sell_price_type'] = '26'
            datapost['freepost_detail-livingrooms']='' 
            datapost['freepost_detail-parking']=''
            datapost['freepost_detail-extrarooms']='' 
            datapost['freepost_detail-property_finished_year']= '0'
            datapost['freepost_detail-property_buy_year']= '0'
            datapost['freepost_detail-facing']='0'
            

        elif(str(property_type) == str(10)):
            datapost['freepost-house_type'] = '207'
            datapost['freepost_detail-landarea_sqw'] = land_area_sq
            datapost['freepost-landarea_total_sqw'] = land_area_sq
            try :
                datapost['freepost-areasize_sqm'] = postdata['floor_area']
                if datapost['freepost-areasize-sqm'] ==None or datapost['freepost-areasize-sqm'] == 0:
                    datapost['freepost-areasize-sqm'] = '1'
                a = int(datapost['freepost-areasize-sqm'])
            except:
                datapost['freepost-areasize_sqm'] = '1'
            try :
                datapost['freepost_detail-numberoffloors'] = postdata['floor_total']
                a = int(datapost['freepost_detail-numberoffloors'])
            except : 
                datapost['freepost_detail-numberoffloors'] = '0'
            try :
                datapost['freepost_detail-room_type'] = str(43 + min(int(postdata['bed_room']),10))
                a = int(datapost['freepost_detail-room_type'])
            except : 
                datapost['freepost_detail-room_type'] = '0'
            try : 
                datapost['freepost_detail-bathrooms'] = postdata['bath_room']
                a = int(datapost['freepost_detail-bathrooms'])
            except :
                datapost['freepost_detail-bathrooms'] = '0'
            datapost['freepost_detail-parking'] = '0'
            datapost['freepost-sell_price_type'] = '26'

        elif(str(property_type) == str(25)):
            datapost['freepost-house_type'] = '206'
            datapost['freepost_detail-landarea_sqw'] = land_area_sq
            datapost['freepost-landarea_total_sqw'] = land_area_sq
            try :
                datapost['freepost-areasize_sqm'] = postdata['floor_area']
                if datapost['freepost-areasize-sqm'] ==None or datapost['freepost-areasize-sqm'] == 0:
                    datapost['freepost-areasize-sqm'] = '1'
                a = int(datapost['freepost-areasize-sqm'])
            except:
                datapost['freepost-areasize_sqm'] = '1'
            try :
                datapost['freepost_detail-numberoffloors'] = postdata['floor_total']
                a = int(datapost['freepost_detail-numberoffloors'])
            except : 
                datapost['freepost_detail-numberoffloors'] = '0'
            datapost['freepost_detail-parking'] = '0'
            datapost['freepost-sell_price_type'] = '26'
            
            
        
        else:
            datapost['freepost-house_type'] = '11'

            
            
        if(listing_type == 'ขาย'):
            datapost['freepost-post_type'] = '1'
            datapost['freepost-sell_price']= price_baht
            datapost['freepost-sell_price_type']='26'
            datapost['freepost_detail-sell_discount_price']=''
        else:
            datapost['freepost-post_type'] = '4'
            datapost['freepost_detail-rent_year'] = '34' #1 year rent
            datapost['freepost-rent_price'] = price_baht
            
        with open('./static/9asset_province.json',encoding='utf-8') as f:
            province = json.load(f)
        # print(province)
        for key in province:
            # print("bleh")
            # print(province[key])
            if (addr_province.find(str(province[key]).strip()) != -1) :
                # print("equuaallll")
                addr_province = key
                datapost['freepost_detail-province_id'] = '1'
        # login
        login = self.test_login(postdata)
        success = login["success"]
        detail = login["detail"]
        post_id = postdata["post_id"]
        post_url = ""
        filestoup = {}
        print(success)
        print(success=="True")
        if(success == "True"):
            # print("debug2")
            # for i in range(len(postdata['post_images'][:10])):
            #     filestoup.append(('imgs', open(os.getcwd() + "/"+ postdata['post_images'][i],'rb')))
            #     filestoup.append(('imgs[]', open(os.getcwd() + "/"+ postdata['post_images'][i],'rb')))

            r = httprequestObj.http_get('https://www.terrabkk.com/freepost/get_amphur_ajax/'+str(datapost['freepost_detail-province_id']), verify=False)
            data = r.json()
            print(data)
            print("sent district : ",addr_district)
            addr_district = addr_district.replace(' ','')
            for i in data:
                if(addr_district.find(i["name"]) != -1 or i["name"].find(addr_district) != -1):
                    datapost['freepost_detail-amphur_id'] = '1'#i["id"]
                    break
            r = httprequestObj.http_get('https://www.terrabkk.com/freepost/get_district_ajax/'+str(datapost['freepost_detail-amphur_id']), verify=False)    
            data = r.json()
            addr_sub_district = addr_sub_district.replace(' ','')
            for i in data:
                if(addr_sub_district.find(i["name"]) != -1 or i["name"].find(addr_sub_district) != -1):
                    datapost['freepost_detail-district_id'] = '1' #i["id"]
                    break
            r = httprequestObj.http_get('https://www.terrabkk.com/freepost/get_postcode_ajax/'+str(datapost['freepost_detail-district_id']),verify=False)
            datapost['freepost_detail-postcode'] = r.text.replace("\"",'')
            # r = httprequestObj.http_post('https://www.terrabkk.com/freepost/add_freepost_draft', data = datapost)#/property/show
            # print(r)
            # # print(r.text)
            # data = r.json()
            # print(data)
            datapost['freepost_detail-province_id'] = '1'
            datapost['freepost_detail-district_id'] = '1' #i["id"]
            datapost['freepost_detail-district_id'] = '1' #i["id"]

            datapost['freepost-id'] = str(post_id)
            print("The data to be posted \n",datapost)
            newdatapost = []
            for key in datapost:
                newdatapost.append((key,datapost[key]))
            temp = []
            for i in range(len(postdata['post_images'][:10])):
                filestoup['imgs']=  open(os.getcwd() + "/"+ postdata['post_images'][i],'rb')
                filestoup['imgs[]'] = open(os.getcwd() + "/"+ postdata['post_images'][i],'rb')
                r = httprequestObj.http_post('https://www.terrabkk.com/uploader_front/freepost_img_upload/'+datapost['freepost-id'],data = newdatapost,files=filestoup)
                data = r.json()
                # print(r.text)
                soup = BeautifulSoup(r.json()['text'], self.parser, from_encoding='utf-8')
                r = soup.find('input',{"name" : "allpic[]"})["value"]
                print(r)
                temp.append(('allpic[]',r))
                
            for i in temp:
                newdatapost.append(i)
            print(newdatapost)
            r = httprequestObj.http_post('https://www.terrabkk.com/free-post/'+datapost['freepost-id'],data=newdatapost)
            with open('b.htm;','w') as f:
                f.write(r.text)
            print("Written")
            if 'พสสำเร็จ' in r.text:
                success = "True"
                detail = "edited"
                post_id = datapost['freepost-id']
                post_url = 'https://www.terrabkk.com/freepost/show/'+post_id
            else:
                success = "False"
                detail = "Post unsuccessful"
            
             
        else:
           success = "False"
           detail = "Unsuccessful Login"
        
        time_end = datetime.datetime.utcnow()
        print({
            "websitename": "terrabkk",
            "success": success,
            "time_usage": time_end - time_start,
            "time_start": time_start,
            "time_end": time_end,
            "ds_id": postdata['ds_id'],
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "",
            "detail": detail
        }
        )
        return {
            "websitename": "terrabkk",
            "success": success,
            "time_usage": time_end - time_start,
            "time_start": time_start,
            "time_end": time_end,
            "ds_id": postdata['ds_id'],
            "log_id":postdata['log_id'],
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "",
            "detail": detail
        }


    def search_post(self,postdata):
        #self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        #search
        start_time = datetime.datetime.utcnow()

        login = self.test_login(postdata)
        post_found = "False"
        post_id = ""
        post_url = ''
        post_view = ''
        post_modify_time = ''
        post_create_time = ''
        detail = 'No post with this title'
        title = ''
        print(login['success']+"##")
        if (login['success'] == 'True'):
            try:
                account = postdata['account_type']
            except:
                account = 'null'
            
            all_posts_url = 'https://www.terrabkk.com/member/my-freepost?status=1'

            all_posts = httprequestObj.http_get(all_posts_url)

            page = BeautifulSoup(all_posts.content, features = "html5lib")


            divi = page.find('div', attrs = {'class':'row pt-3'})
            xyz = divi.findAll('a',attrs={'target':'_blank'})
            #print(xyz,len(xyz))
            
            if xyz == None:
                detail = "Post Not Found"
            else:
                flag= 0
                for one in xyz:
                    #if one.has_attr('target') and one['target']=='_blank':
                    post_url = one['href']
                    
                    titl = one.find('h4')
                    if titl == None:
                        continue
                    #print(titl.text.strip(),' : ',postdata['post_title_th'].strip())
                    if titl.text.strip() == postdata['post_title_th'].strip():
                        
                        post_found = "true"
                        r = httprequestObj.http_get(post_url)
                        sou = BeautifulSoup(r.text,'html5lib')
                        datv = sou.find('div',attrs={'class':'item-share row'}).findAll('a',attrs={'class':'col-auto'})
                        print(datv[1].text + "date")
                        print(datv[2].text+"view")
                        post_create_time = datv[1].text.split(' ')[-1]
                        post_id = post_url.split('/')[-2]
                        post_view = datv[2].text.split(' ')[0]        
                        detail = "Post Found "
                        flag=1
                        break
                if flag==0:
                    detail = "Post Not Found"
                    post_url=''
                    post_found = 'False'
                                  
        else :
            detail = 'Can not log in'
            post_found = 'False'

        end_time = datetime.datetime.utcnow()
        

        return {
            "websitename": "Terrabkk",
            "success": login['success'],
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(end_time - start_time),
            "detail": detail,
            "account_type":account,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "post_url": post_url,
            "post_modify_time": post_modify_time,
            "post_create_time" : post_create_time,
            "post_view": post_view,
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