# -*- coding: utf-8 -*-

import logging
import logging.config
from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
# from urlparse import urlparse
import re,requests
import json, os
import datetime
import sys
from urllib.parse import unquote,urlparse,parse_qs
httprequestObj = lib_httprequest()
from requests_toolbelt import MultipartEncoder
import random
from python3_anticaptcha import ImageToTextTask
from python3_anticaptcha import errors
from python3_anticaptcha import AntiCaptchaControl


try:
    import configs
except ImportError:
    configs = {}
'''
logging.config.dictConfig(getattr(configs, 'logging_config', {}))
log = logging.getLogger()
'''


class thaihometown():

    def __init__(self):

        self.websitename = 'thaihometown'

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.debug = 0
        self.logid = ''
        self.debugresdata = 0
        self.parser = 'html.parser'
        self.handled = False
        self.captchascret = getattr(configs, 'captcha_secret', '')

    def postdata_handle(self, postdata):
        #log.debug('')

        if self.handled == True:
            return postdata

        datahandled = {}

        try:
            datahandled['listing_type'] = postdata['listing_type']
        except KeyError as e:
            datahandled['listing_type'] = "ประกาศขาย"
            #log.warning(str(e))
        if datahandled['listing_type'] == "เช่า":
            datahandled['listing_type'] = "ประกาศให้เช่า"
        elif datahandled['listing_type'] == "ขายดาวน์":
            datahandled['listing_type'] = "ประกาศขายดาวน์"
        else:
            datahandled['listing_type'] = "ประกาศขาย"

        # "CONDO","BUNG","TOWN","LAND","APT","RET","OFF","WAR","BIZ","SHOP"]
        try:
            datahandled['property_type'] = postdata['property_type']
        except KeyError as e:
            datahandled['property_type'] = "คอนโดมิเนียม+Condominiem"
            datahandled['property_type3'] = "condo"
            #log.warning(str(e))
        if datahandled['property_type'] == '2' or datahandled['property_type'] == 2: #2 บ้านเดี่ยว
            datahandled['property_type'] = "บ้านเดี่ยว+Singlehouse"
            datahandled['property_type3'] = "singlehouse"
        elif datahandled['property_type'] == '3' or datahandled['property_type'] == 3: #3 บ้านแฝด
            datahandled['property_type'] = "บ้าน+Home"
            datahandled['property_type3'] = "home"
        elif datahandled['property_type'] == '4' or datahandled['property_type'] == 4: #4 ทาวน์เฮ้าส์
            datahandled['property_type'] = "ทาวน์เฮ้าส์+Townhouse"
            datahandled['property_type3'] = "townhouse"
        elif datahandled['property_type'] == '5' or datahandled['property_type'] == 5: #5 ตึกแถว-อาคารพาณิชย์
            datahandled['property_type'] = "อาคารพาณิชย์+Buildings"
            datahandled['property_type3'] = "buildings"
        elif datahandled['property_type'] == '6' or datahandled['property_type'] == 6: #6 ที่ดิน
            datahandled['property_type'] = "ที่ดิน+Land"
            datahandled['property_type3'] = "land"
        elif datahandled['property_type'] == '7' or datahandled['property_type'] == 7: #7 อพาร์ทเมนท์
            datahandled['property_type'] = "อพาร์ทเมนท์+Apartment"
            datahandled['property_type3'] = "apartment"
        elif datahandled['property_type'] == '8' or datahandled['property_type'] == 8: #8 โรงแรม
            datahandled['property_type'] = "ธุรกิจ+Business"
            datahandled['property_type3'] = "business"
        elif datahandled['property_type'] == '9' or datahandled['property_type'] == 9: #9 ออฟฟิศสำนักงาน
            datahandled['property_type'] = "สำนักงาน+Office"
            datahandled['property_type3'] = "office"
        elif datahandled['property_type'] == '10' or datahandled['property_type'] == 10: #10 โกดัง
            datahandled['property_type'] = "โกดัง+Storehouse"
            datahandled['property_type3'] = "storehouse"
        elif datahandled['property_type'] == '25' or datahandled['property_type'] == 25: #25 โรงงาน
            datahandled['property_type'] = "โรงงาน+Factory"
            datahandled['property_type3'] = "factory"
        else:
            datahandled['property_type'] = "คอนโดมิเนียม+Condominiem" #1 คอนโด
            datahandled['property_type3'] = "condo"

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
            datahandled['floor_area'] = 0
            #log.warning(str(e))

        try:
            datahandled['geo_latitude'] = postdata['geo_latitude']
        except KeyError as e:
            datahandled['geo_latitude'] = ''
            #log.warning(str(e))

        try:
            datahandled['geo_longitude'] = postdata['geo_longitude']
        except KeyError as e:
            datahandled['geo_longitude'] = ''
            #log.warning(str(e))

        try:
            datahandled['property_id'] = postdata['property_id']
        except KeyError as e:
            datahandled['property_id'] = ''
            #log.warning(str(e))

        try:
            datahandled['post_title_th'] = postdata['post_title_th']
        except KeyError as e:
            datahandled['post_title_th'] = ''
            #log.warning(str(e))

        try:
            datahandled['post_description_th'] = postdata['post_description_th']
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
            datahandled['floor_total'] = 1
            #log.warning(str(e))

        try:
            datahandled['floor_level'] = postdata["floor_level"]
        except KeyError as e:
            datahandled['floor_level'] = 1
            #log.warning(str(e))

        

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
        except KeyError as e:
            datahandled['land_size_rai'] = '0'
            #log.warning(str(e))

        try:
            datahandled['land_size_ngan'] = str(postdata["land_size_ngan"])
        except KeyError as e:
            datahandled['land_size_ngan'] = '0'
            #log.warning(str(e))

        try:
            datahandled['land_size_wa'] = str(postdata["land_size_wa"])
        except KeyError as e:
            datahandled['land_size_wa'] = '0'
            #log.warning(str(e))

        try:
            datahandled['addr_road'] = postdata["addr_road"]
        except KeyError as e:
            datahandled['addr_road'] = ''
            #log.warning(str(e))

        try:
            datahandled['company_name'] = postdata["company_name"]
        except KeyError as e:
            datahandled['company_name'] = ''
            #log.warning(str(e))

        try:
            datahandled['name_title'] = postdata["name_title"]
        except KeyError as e:
            datahandled['name_title'] = ''
            #log.warning(str(e))

        try:
            datahandled['name_th'] = postdata["name_th"]
        except KeyError as e:
            datahandled['name_th'] = ''
            #log.warning(str(e))

        try:
            datahandled['surname_th'] = postdata["surname_th"]
        except KeyError as e:
            datahandled['surname_th'] = ''
            #log.warning(str(e))

        try:
            datahandled['name_en'] = postdata["name_en"]
        except KeyError as e:
            datahandled['name_en'] = ''
            #log.warning(str(e))

        try:
            datahandled['surname_en'] = postdata["surname_en"]
        except KeyError as e:
            datahandled['surname_en'] = ''
            #log.warning(str(e))

        try:
            datahandled['tel'] = postdata["tel"]
        except KeyError as e:
            datahandled['tel'] = ''
            #log.warning(str(e))

        try:
            datahandled['line'] = postdata["line"]
        except KeyError as e:
            datahandled['line'] = ''
            #log.warning(str(e))
        
        for key, val in datahandled.items():
            if val == None:
                datahandled[key] = ''

     
        
        self.handled = True

        return datahandled

    def register_user(self, postdata):
        #log.debug('')

        time_start = datetime.datetime.utcnow()
        #print('start')
        # start process
        #
        datahandled = self.postdata_handle(postdata)
        user = datahandled['user']
        passwd = datahandled['pass']
        tel = datahandled["tel"]

        success = "true"
        detail = ""

        datapost = dict(
            Form_accept=1,
            Submit='register',
            register='active',
            code_edit=passwd,
            code_edit2=passwd,
            email=user,
            firstname=datahandled['name_th'],
            mobile=tel,
        )
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        }
        r = httprequestObj.http_post('https://www.thaihometown.com/member/register', data=datapost)
        data = r.text
        # print (data)

        # if redirect to register page again
        if re.search('https://www.thaihometown.com/member/register', data):
            soup = BeautifulSoup(data, self.parser,from_encoding='utf-8')
            detail = soup.find('span').text
            success = "false"

        #
        # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        #print('here')
        return {
            "websitename": "thaihometown",
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            'ds_id': postdata['ds_id'],
            "end_time": str(time_end),
            "detail": detail,
        }

    def test_login(self, postdata):
        #log.debug('')

        time_start = datetime.datetime.utcnow()

        # start process
        #
        datahandled = self.postdata_handle(postdata)
        user = datahandled['user']
        passwd = datahandled['pass']
        
        success = "true"
        detail = ""

        datapost = {
            'Submit': '',
            'Submit2.x': 26,
            'Submit2.y': 13,
            'part': '/addnew',
            'pwd_login': passwd,
            'user_login': user,
        }
        r = httprequestObj.http_post('https://www.thaihometown.com/member/check', data=datapost)
        #log.debug('post login')
        data = r.text
        # print(data)
        matchObj = re.search(r'member\/[0-9]+', data)
        if not matchObj:
            success = "false"
            detail = "cannot login"
        else:

            txt = str(r.text)
            ind = txt.find('member')+7
            self.logid = ''
            while txt[ind]!="'":
                self.logid+=txt[ind]
                ind+=1

        #log.debug('login status %s', success)

        #
        # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": self.websitename,
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "ds_id": datahandled['ds_id']
        }

    def validatedatapost(self,datahandled):
        #log.debug('')

        success = 'true'
        detail = ''

        #validate
        if datahandled['addr_province'] == None or  datahandled['addr_province'] == '' or datahandled['addr_district'] == None or datahandled['addr_district'] =='':
            detail = "addr_province or addr_district not defined"
        if datahandled['property_type'] == '' or datahandled['property_type'] == None:
            detail = "property_type not defined"
        if datahandled['listing_type'] == None or datahandled['listing_type'] == '':
            detail = "listing_type not defined"
        if datahandled['property_type'] == 'บ้านเดี่ยว+Singlehouse' or datahandled['property_type'] == 'บ้าน+Home' or datahandled['property_type'] == 'ทาวน์เฮ้าส์+Townhouse' or datahandled['property_type'] == 'คอนโดมิเนียม+Condominiem':
            if  datahandled['bath_room'] == 0 or datahandled['bed_room'] == 0:
                detail = 'บ้าน คอนโด ทาวน์เฮ้าส์ จำนวนห้องนอน และห้องน้ำต้องใส่ข้อมูล'
        if len(datahandled['post_description_th']) < 200 or len(datahandled['post_description_th']) > 5000:
            detail = 'post_description_th between 200 - 5000'
        if len(datahandled['post_title_th']) > 250:
            detail = 'post_title_th must < 250'
        if datahandled['floor_area'] == 0:
            detail = 'floor_area not defined'
        

        if detail != "":
            success = 'false'
        
        return success,detail

    def getprovincedistrictid(self,datahandled):
        #log.debug('')

        datahandled['property_city_bkk'] = ''
        datahandled['property_city_2'] = ''
        datahandled['property_country_2'] = ''

        #print(datahandled['addr_province'])
        #กรุงเทพ
        if datahandled['addr_province'] == 'กรุงเทพมหานคร' or datahandled['addr_province'] == 'กรุงเทพ':
            r = httprequestObj.http_get('https://www.thaihometown.com/addnew', encoder='cp874',verify=False)
            data = r.content
            soup = BeautifulSoup(data, self.parser,from_encoding='utf-8')
            try:
                datahandled['property_city_bkk'] = soup.find('select',{'id':'property_city_bkk'}).find('option',text=re.compile(datahandled['addr_district']))['value']
                #log.debug('bkk district is '+datahandled['property_city_bkk'])
            except:
                pass
                
        #ต่างจังหวัด
        else:
            r = httprequestObj.http_get('https://www.thaihometown.com/addnew', encoder='cp874',verify=False)
            data = r.content
            #print(data)
            """ f = open('file.html','w')
            f.write(data)
            f.close() """
            soup = BeautifulSoup(data, self.parser,from_encoding='utf-8')
            try:
                datahandled['property_country_2'] = soup.find('select',{'id':'property_country_2'}).find('option',text=re.compile(datahandled['addr_province']))['value']
                #print('here',datahandled['property_country_2'])
                #log.debug('province is '+datahandled['property_country_2'])
            except:
                pass
            if datahandled['property_country_2'] != "":                
                r = httprequestObj.http_get('https://www.thaihometown.com/search/state2012_addnew.php?PID='+str(datahandled['property_country_2']),verify=False)
                data = r.text
                soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
                try:
                    datahandled['property_city_2'] = soup.find('option',text=re.compile(datahandled['addr_district']))['value']
                    #log.debug('district is '+datahandled['property_city_2'])
                except:
                    pass

        if datahandled['property_country_2'] == '' and datahandled['property_city_bkk'] == '':
            datahandled['property_country_2'] = '2'
        if datahandled['property_city_2'] == '' and datahandled['property_city_bkk'] == '':
            datahandled['property_city_2'] = '53'

        if datahandled['property_city_bkk'] == '' and (datahandled['property_city_2'] == '' or datahandled['property_country_2'] == ''):
            return 'false','wrong province or district '+datahandled['addr_province']+' '+datahandled['addr_district'],datahandled

        return 'true','',datahandled

    def getsizeunit(self,datahandled):
        #log.debug('')

        #type unit 1 = ตรม
        #type unit 2 = ตรว

        size = 0
        typeunit = 1

        #condo / office is sqm first
        if datahandled['property_type'] == 'คอนโดมิเนียม+Condominiem' or datahandled['property_type'] == 'สำนักงาน+Office':
            typeunit = 1
            #if defined floor_area
            if datahandled.get('floor_area',None) != None and datahandled.get('floor_area','') != '' and int(datahandled.get('floor_area',0)) > 0:
                size = datahandled['floor_area']
            #if not defined floor_area
            else:
                try:
                    rai = float(datahandled['land_size_rai'])
                    size = rai*1600
                except ValueError:
                    #log.debug('cannot convert area rai to sqm')
                    pass
                try:
                    ngan = float(datahandled['land_size_ngan'])
                    size = size + (ngan*400)
                except ValueError:
                    #log.debug('cannot convert area ngan to sqm')
                    pass
                try:
                    wa = float(datahandled['land_size_wa'])
                    size = size + (wa*4)
                except ValueError:
                    #log.debug('cannot convert area wa to sqm')
                    pass    
        # not condo / office
        else:
            typeunit = 2
            try:
                rai = float(datahandled['land_size_rai'])
                size = rai*400
            except ValueError:
                #log.debug('cannot convert area rai')
                pass
            try:
                ngan = float(datahandled['land_size_ngan'])
                size = size + (ngan*100)
            except ValueError:
                #log.debug('cannot convert area ngan')
                pass
            try:
                wa = float(datahandled['land_size_wa'])
                size = size + wa
            except ValueError:
                #log.debug('cannot convert area wa')
                pass    
            
            # if rai ngan wa not defined
            if size == 0:
                try:
                    size = float(datahandled['floor_area']) / 4
                except:
                    size = datahandled['floor_area']
                    typeunit = 1
                    #log.debug('cannot convert area to sqw')
        #last
        if size == 0: 
            size = datahandled.get('floor_area',0)
            typeunit = 1
                
        #log.debug('size %s type %s',size,typeunit)

        return size,typeunit


    def create_post(self, postdata):
        #log.debug('')

        time_start = datetime.datetime.utcnow()
        #print('here')
        # start process
        #
        datahandled = self.postdata_handle(postdata)
        ds_id = postdata["ds_id"]
        #print('here1')
        rent_price=''
        selling_price=''
        if datahandled['listing_type'] == 'ประกาศขาย' or datahandled['listing_type'] == 'ประกาศขายดาวน์':
            selling_price = datahandled['price_baht']
        elif datahandled['listing_type'] == 'ประกาศให้เช่า':
            rent_price = datahandled['price_baht']
        
        #area detect
        size,typeunit = self.getsizeunit(datahandled)

        success = "true"
        detail = ""
        post_id = ""
        post_url = ""
        #print('here2')
        success,detail = self.validatedatapost(datahandled)
            
        # login
        if success == "true":
            test_login = self.test_login(datahandled)
            success = test_login["success"]
            detail = test_login["detail"]
        #print('here3')
        if success == "true":
            #get provice district id
            success,detail,datahandled = self.getprovincedistrictid(datahandled)
            #print('got')
            if success == 'true':
                #get post authen value
                r = httprequestObj.http_get('https://www.thaihometown.com/addnew', verify=False)
                data = r.text
                soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
                #print('here4')
                #f = open("thihomepost.html", "wb")
                #f.write(data.encode('utf-8').strip())
                postlimit = soup.find("div",{"id":"posted_limit2"})
                if postlimit:
                    success = "false"
                    detail = 'คุณประกาศครบ 10 รายการแล้ว กรุณาใช้บริการฝากประกาศใหม่อีกครั้งในวันถัดไป'
                    #log.debug('คุณประกาศครบ 10 รายการแล้ว กรุณาใช้บริการฝากประกาศใหม่อีกครั้งในวันถัดไป')
                #print('here5')
                if success == 'true':
                    string2 = soup.find("input", {"name": "string2"})['value']
                    string1 = string2
                    dasd = soup.find("input", {"name": "dasd"})['value']
                    sas_name = soup.find("input", {"name": "sas_name"})['value']
                    email = soup.find("input", {"name": "email"})['value']
                    code_edit = soup.find("input", {"name": "code_edit"})['value']
                    firstname = soup.find("input", {"name": "firstname"})['value']
                    mobile = soup.find("input", {"name": "mobile"})['value']
                    date_signup = soup.find("input", {"name": "date_signup"})['value']
                    #print('here6')

                    # https://www.thaihometown.com/addcontacts

                    datapost = {
                        'ActionForm2':'',
                        'Submit':'Active',
                        'ad_title':datahandled['post_description_th'].encode('cp874', 'ignore'),
                        'carpark':'',
                        'code_edit':code_edit,
                        'conditioning':'',
                        'contact_code':'',
                        'dasd':dasd,
                        'date_signup':date_signup,
                        'email':email,
                        'firstname':firstname,
                        'headtitle':datahandled['post_title_th'].encode('cp874', 'ignore'),
                        'id':'',
                        'info[0]' :'ตกแต่งห้องนอน'.encode('cp874', 'ignore'),
                        'info[1]' :'ตกแต่งห้องนั่งเล่น'.encode('cp874', 'ignore'),
                        'info[2]' :'ปูพื้นเซรามิค'.encode('cp874', 'ignore'),
                        'info[3]' :'เฟอร์นิเจอร์'.encode('cp874', 'ignore'),
                        'info[4]' :'ไมโครเวฟ'.encode('cp874', 'ignore'),
                        'info[5]' :'ชุดรับแขก'.encode('cp874', 'ignore'),
                        'mobile':mobile,
                        'price_unit':'',
                        'property_area':size,
                        'property_bts':'',
                        'property_city_2':datahandled['property_city_2'].encode('cp874', 'ignore'),
                        'property_city_bkk':datahandled['property_city_bkk'].encode('cp874', 'ignore'),
                        'property_country_2':datahandled['property_country_2'].encode('cp874', 'ignore'),
                        'property_mrt':'',
                        'property_purple':'',
                        'property_sqm':typeunit,
                        'property_type':datahandled['property_type'].encode('cp874', 'ignore'),
                        'room1':datahandled['bed_room'],
                        'room2':datahandled['bath_room'],
                        'sas_name':sas_name,
                        'rent_price':rent_price,
                        'selling_price':selling_price,
                        'type_forrent':'',
                        'string1':string1,
                        'string2':string2,
                        'typepart':datahandled['listing_type'].encode('cp874', 'ignore'),
                        'typeunit':'ต่อตร.ม'.encode('cp874', 'ignore'),
                        'notprice': 1 if datahandled['price_baht'] == 0 or datahandled['price_baht'] == None else 0,
                    }
                    #log.debug(datapost)
                    #print('here7')
                    r = httprequestObj.http_post('https://www.thaihometown.com/addcontacts', data=datapost)
                    data = r.text
                    # print(data)
                    #f = open("thihomepost.html", "wb")
                    #f.write(data.encode('utf-8').strip())
                    # print(str(datahandled['property_type']))
                    matchObj = re.search(r'https:\/\/www.thaihometown.com\/edit\/[0-9]+', data)
                    if not matchObj:
                        success = "false"
                        soup = BeautifulSoup(data, self.parser,from_encoding='utf-8')
                        txtresponse = soup.find("font").text
                        detail = unquote(txtresponse)
                    else:
                        post_id = re.search(r'https:\/\/www.thaihometown.com\/edit\/(\d+)', data).group(1)
                     
                        #get post url
                        post_url = self.getposturl(post_id,datahandled['property_type3'])
                        # print(str(datahandled['property_type']))
                        #upload image
                        self.uploadimage(datahandled,post_id)

        #print('finish')
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": ds_id,
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
            "websitename": self.websitename
        }
    
    def getposturl(self,post_id,prop_type):
        #log.debug('')
        post_url = 'https://www.thaihometown.com/'+str(prop_type)+'/'+str(post_id)

        r = httprequestObj.http_get('https://www.thaihometown.com/edit/'+str(post_id),encoder='cp874', verify=False)
        data = r.text
        soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
        # post is publish
        try:
            #https://www.thaihometown.com/storehouse/2225810
            if soup.find('a',text=re.compile('ดูประกาศที่ใช้งานหน้าเว็บ')):
                post_url = soup.find('a',text=re.compile('ดูประกาศที่ใช้งานหน้าเว็บ'))['href']
        except:
            pass
        # post is not publish
        try:
            #https://www.thaihometown.com/singlehouse/2226300/idcode/e8859755bce1195f9746e244789dd023
            if soup.find('a',text=re.compile('ดูตัวอย่างประกาศของคุณ')):
                post_url = soup.find('a',text=re.compile('ดูตัวอย่างประกาศของคุณ'))['href']
                #log.debug(re.search(r'(https:\/\/www.thaihometown.com\/\w+\/\d+)',post_url))
                post_url = re.search(r'(https:\/\/www.thaihometown.com\/\w+\/\d+)',post_url).group(1)
        except:
            pass

        return post_url

    
    def uploadimage(self,datahandled,post_id):
        #log.debug('')

        r = httprequestObj.http_get('https://www.thaihometown.com/edit/'+str(post_id), verify=False)
        data = r.text
        soup = BeautifulSoup(data, self.parser,from_encoding='utf-8')
        uploadcode = ''
        uploadlink = ''
        try:
            uploadlink = soup.find('a',href=re.compile('memberupload'))['href']
            #log.debug('upload link ' +uploadlink)
            uploadcode = parse_qs(urlparse(uploadlink).query)['Mag'][0]
        except:
            pass
            #log.warning('cannot get uploadlink and uploadcode')
        #log.debug('uploadcode ' +uploadcode)

        #if find image when editpost , to delete before new upload
        try:
            r = httprequestObj.http_get(uploadlink, verify=False)
            data = r.text
            soup = BeautifulSoup(data, self.parser,from_encoding='utf-8')
            allimage = soup.find_all('img',src=re.compile('small.jpg'))
            #log.debug('find all old image '+str(len(allimage)))
            if len(datahandled['post_images']) > 0:
                for img in allimage:
                    imgid = re.search(r'-(\d+)_small',str(img)).group(1)
                    datapost = {
                        'id': str(imgid),
                        'contact': str(post_id),
                        'code': str(uploadcode),
                        'datesing': '',
                        'maction':'',
                        }
                    r = httprequestObj.http_post(
                    'https://www.thaihometown.com/form/memberupload/delete.php',
                    data=datapost,
                    )
                    #log.debug('remove image id '+str(imgid))
        except:
            pass

        #upload image ,MultipartEncoder is very HARD, I use 24hr. for wrestle with it
        allowupload =len(datahandled['post_images'][:11])
        for i in range(allowupload):
            datapost = {
                        'id':str(i+1),
                        'contact': str(post_id), #post id
                        'code': str(uploadcode),
                        'datesing': str(datetime.datetime.utcnow().strftime('%Y-%m-%d')), #'2020-04-27'
                        'maction':'2',
                        'uploadfile':( str(i+1) + '.jpg', open(os.path.abspath(datahandled['post_images'][i]), 'rb'), 'image/jpeg'),
            }
            encoder = MultipartEncoder(fields=datapost)
            r = httprequestObj.http_post(
            'https://www.thaihometown.com/form/memberupload/upload-file.php?id='+str(i+1)+'&contact='+str(post_id)+'&code='+str(uploadcode)+'&datesing='+str(datetime.datetime.utcnow().strftime('%Y-%m-%d'))+'&maction=2',
            data=encoder,
            headers={'Content-Type': encoder.content_type}
            )
            #log.debug('image upload '+r.text)
        
        #fix black image //thaihometown bug
        try:
            #log.debug('fix black image')
            r = httprequestObj.http_get('https://www.thaihometown.com/form/memberupload/image_update_copy.php?code='+str(uploadcode)+'&id='+str(post_id), verify=False)
            #log.debug(r.text)
            soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
            is_total = soup.find('input',{'name':'is_total'})['value']
            #log.debug('image total '+is_total)
            allimage = soup.find_all('input',id=re.compile('imag'))
            #log.debug(allimage)
            datapost = {
                'UPDATE':'[object Object]',
                'status_active':1,
                'is_total':is_total
            }
            for img in allimage:
                #log.debug("image name %s image value %s",img['id'],img['value'])
                datapost[img['id']] = img['value']
            #log.debug(datapost)
            r = httprequestObj.http_post('https://www.thaihometown.com/form/memberupload/image_update_copy.php?code='+str(uploadcode)+'&id='+str(post_id), data=datapost)
            matchObj = re.search(r'&#3649;&#3585;&#3657;&#3652;&#3586;&#3619;&#3641;&#3611;&#3616;&#3634;&#3614;&#3648;&#3619;&#3637;&#3618;&#3610;&#3619;&#3657;&#3629;&#3618;', r.text) #แก้ไขรูปภาพเรียบร้อย
            #if matchObj:
                #log.debug('fixed black image success')
        except:
            #log.debug('post edit black image error')
            pass
         
        return True

    def boost_post_bak(self, postdata):
        #log.debug('')

        time_start = datetime.datetime.utcnow()

        post_id = postdata["post_id"]
        user = postdata['user']
        passwd = postdata['pass']
        log_id = postdata["log_id"]

        # start proces
        #

        # login
        self.test_login(postdata)
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]

        if (success == "true"):

            r = httprequestObj.http_get('https://www.thaihometown.com/edit/' + post_id, verify=False)
            data = r.text
            #f = open("editpostthaihometown.html", "wb")
            #f.write(data.encode('utf-8').strip())

            # check respone py post id
            matchObj = re.search(r'' + post_id + '', data)
            if not matchObj:
                success = "false"
                detail = "not found this post_id " + post_id

            # check edit 10 times
            matchObj = re.search(r'�ѹ���! �س��䢢����Ż�С�ȷ����ҹ���� �ú��˹� 10', data)
            if matchObj:
                success = "false"
                detail = "today you is edited post 10 times วันนี้! คุณแก้ไขข้อมูลประกาศที่ใช้งานแล้ว ครบกำหนด 10 ครั้ง/วัน กรุณาใช้งานอีกครั้งในวันถัดไป"

            if success == "true":
                soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
                contact_code = soup.find("input", {"name": "contact_code"})['value']

                sas_name = soup.find("input", {"name": "sas_name"})['value']
                code_edit = soup.find("input", {"name": "code_edit"})['value']
                firstname = soup.find("input", {"name": "firstname"})['value']
                mobile = soup.find("input", {"name": "mobile"})['value']
                date_signup = soup.find("input", {"name": "date_signup"})['value']
                email = soup.find("input", {"name": "email"})['value']
                ad_title = soup.find("textarea", {"name": "ad_title"}).contents
                ad_title = ad_title[0]
                datenow = str(datetime.datetime.utcnow())

                datapost = dict(
                    code_edit=code_edit,
                    email=email,
                    mobile=mobile,
                    sas_name=sas_name,
                    contact_code=contact_code,
                    date_signup=date_signup,
                    firstname=firstname,
                    id=post_id,
                    # ad_title=ad_title.encode('cp874', 'ignore'),  # + "\n" + datenow,
                    ad_title=ad_title + "\n" + datenow,
                    Action_ad_title=1,
                    Action_headtitle=1,
                    Submit='Active',

                    # Name_Project2='',
                    # Owner_Project2='',
                    # Status_Project2=0,
                    # headtitle=post_title_th.encode('cp874', 'ignore')
                    # ActionForm2='',
                    # carpark2=0,
                    # conditioning2=0,
                    # promotion_bonus2=0,
                    # promotion_discount2=0,
                    # property_area=55,
                    # property_area2=0.00,
                    # property_bts='',
                    # property_bts2='',
                    # property_city2='ราษฎร์บูรณะ',
                    # property_city_2='',
                    # property_city_bkk='ยานนาวา+Yannawa',
                    # property_country2='กรุงเทพมหานคร',
                    # property_country_2='',
                    # property_mrt='',
                    # property_mrt2='',
                    # property_purple='',
                    # property_purple2='',
                    # property_sqm=1,
                    # property_sqm4=1,
                    # property_type='บ้าน+Home',
                    # property_type2='บ้าน+Home',
                    # rent_price='',
                    # rent_price_number2=0,
                    # room1=2,
                    # room12=2,
                    # room2=3,
                    # room22=3,
                    # selling_price='',
                    # selling_price_number2=0,
                    # type_forrent='',
                    # type_forrent2=0,
                    # typepart='ประกาศขาย',
                    # typeunit5=''
                )

                r = httprequestObj.http_post('https://www.thaihometown.com/editcontacts', data=datapost)
                data = r.text
                #f = open("boostthaihometown.html", "wb")
                #f.write(data.encode('utf-8').strip())

                matchObj = re.search(r'https:\/\/www.thaihometown.com\/edit\/' + post_id, data)
                if matchObj:
                    success = "true"
                else:
                    success = "false"
                    detail = unquote(data)

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
            "ds_id": postdata['ds_id'], 
            "log_id": log_id, 
            "post_id": post_id}

    def delete_post(self, postdata):
        #log.debug('')
        time_start = datetime.datetime.utcnow()

        # TODO ประกาศที่ทดสอบไป ยังไม่ครบ 7 วัน ทำทดสอบการลบไม่ได้ วันหลังค่อยมาทำใหม่
        # start proces
        #
        datahandled = self.postdata_handle(postdata)

        success = "true"
        detail = ""

        if datahandled['post_id'] == '' or datahandled['post_id'] == None:
            success = 'false'
            detail = 'post_id not defined'

        # login
        if success == 'true':
            self.test_login(postdata)
            test_login = self.test_login(postdata)
            success = test_login["success"]
            detail = test_login["detail"]

        if (success == "true"):
            #get code , it same upload code
            r = httprequestObj.http_get('https://www.thaihometown.com/edit/'+str(datahandled['post_id']), verify=False)
            data = r.content
            soup = BeautifulSoup(data, self.parser)
            uploadcode = ''
            try:
                uploadlink = soup.find('a',href=re.compile('memberupload'))['href']
                #log.debug('upload link ' +uploadlink)
                uploadcode = parse_qs(urlparse(uploadlink).query)['Mag'][0]
                #log.debug('uploadcode ' +uploadcode)
            except:
                #log.error("cannot get post code , not found post id "+datahandled['post_id'])
                success = "false"
                detail = "cannot get post code , not found post id "+datahandled['post_id']

        if success == "true":
            #try 5 times
            for i in range(5):
                success = "true"

                #log.debug('try solve captcha image loop '+str(i+1))

                #go to delete page
                r = httprequestObj.http_get('https://www.thaihometown.com/member/delete/'+datahandled['post_id']+'/'+uploadcode,verify=False)
                data = r.content
                soup = BeautifulSoup(data, self.parser)
                #log.debug(data)
                #detect if post can delete
                checkform = soup.find("form", {"name": "checkForm"})
                if not checkform:
                    success = "false"
                    detail = soup.text
                    #log.debug(soup.text)
                    break
            
                if success == "true":
                    idcode = soup.find("input", {"name": "idcode"})['value']
                    scode = soup.find("input", {"name": "scode"})['value']
                    contacts_id = soup.find("input", {"name": "contacts_id"})['value']
                    imgurl  =  soup.find("img",src=re.compile('securimage_show'))['src']
                    
                    res = httprequestObj.http_get(imgurl, verify=False)
                    imgname = "/imgtmp/captchatmp/" + str(random.randint(1, 999999999)) + '.png'
                    with open(os.getcwd()+imgname, 'wb') as f:
                        f.write(res.content)
                        f.close()
                    #log.debug('download image '+imgname)
                    imgnum = self.ImgToTextResolve(imgname)
                    os.unlink(imgname)
                    #log.debug(imgnum)
                    #if anti captcha is error
                    if imgnum['errorId'] < 0:
                        success = 'false'
                        detail = imgnum['errorDescription']
                        #log.debug(imgnum['errorDescription'])
                        if imgnum['errorCode'] == 'ERROR_KEY_DOES_NOT_EXIST' or imgnum['errorCode'] == 'ERROR_ZERO_BALANCE' or imgnum['errorCode'] == 'ERROR_IP_NOT_ALLOWED' or imgnum['errorCode'] == 'ERROR_IP_BLOCKED':
                            #log.debug('break')
                            break
                        continue

                    datapost = {
                        'CKcode' : imgnum['solution']['text'],
                        'idcode' : idcode,
                        'scode' : scode,
                        'contacts_id' : contacts_id
                    }

                    r = httprequestObj.http_post('https://www.thaihometown.com/member/delete/'+datahandled['post_id']+'/'+uploadcode, data=datapost)
                    data = r.text
                    # f = open("editpostthaihometown.html", "wb")
                    # f.write(data.encode('utf-8').strip())
                    matchObj = re.search(r'ใส่รหัสไม่ถูกต้อง', data)
                    if matchObj:
                        success = "false"
                        detail = "ใส่รหัส captcha image ไม่ถูกต้อง"
                        continue
                    else:
                        success = "true"
                        #log.debug("post id %s deleted success",datahandled['post_id'])
                        #log.debug('break')
                        break
                    

        #
        # end process
        #print('finish')
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "log_id": datahandled['log_id'],
            "ds_id": datahandled['ds_id'],
            "post_id": datahandled['post_id'],
            "websitename": self.websitename
        }
    
    def ImgToTextResolve(self,imgname):
        #log.debug('')

        #{'errorId': 0, 'balance': 1.9321}
        #{'errorId': 1, 'errorCode': 'ERROR_KEY_DOES_NOT_EXIST', 'errorDescription': 'Account authorization key not found in the system'}
        
        #check balance first
        try:
            user_ans = AntiCaptchaControl.AntiCaptchaControl(anticaptcha_key = self.captchascret).get_balance()
        except Exception as err:
            return {'errorId':9999,'errorDescription' :str(err)}
        
        if user_ans['balance'] <= 0.001000:
            return {'errorId':9999,'errorDescription' :'balance not enough '+user_ans['balance']}
     
        #resolve captcha
        try:
            user_ans = ImageToTextTask.ImageToTextTask(anticaptcha_key = self.captchascret).captcha_handler(captcha_file=imgname)
            return user_ans
        except Exception as err:
            return {'errorId':9999,'errorDescription' :str(err)}
        

    def boost_post(self,postdata):
        #log.debug('')
        time_start = datetime.datetime.utcnow()

        # start proces
        #
        datahandled = self.postdata_handle(postdata)

        success = "true"
        detail = ""

        if datahandled['post_id'] == '' or datahandled['post_id'] == None:
            success = 'false'
            detail = 'post_id not defined'

        # login
        if success == 'true':
            self.test_login(postdata)
            test_login = self.test_login(postdata)
            success = test_login["success"]
            detail = test_login["detail"]

        if (success == "true"):

            try:
                res = httprequestObj.http_get('https://www.thaihometown.com/member/?Keyword=&Msid=' + datahandled['post_id'] + '&SearchMember.x=43&SearchMember.y=8')
                soup = BeautifulSoup(res.text, self.parser)
                code_div = soup.find('div', {'class': 'Show_isView'})
                code = code_div.get('onclick').split(',')[-1].replace(')', '').replace("'", '')
                response = httprequestObj.http_get('https://www.thaihometown.com/member/ajaxView.php?code=' + code + '&ided=' + datahandled['post_id'])
                post_view = response.text.split(' ')[1]
            except:
                post_view = ''

            r = httprequestObj.http_get('https://www.thaihometown.com/edit/' + datahandled['post_id'], encoder='cp874',verify=False)
            data = r.text
            # f = open("editpostthaihometown.html", "wb")
            # f.write(data.encode('utf-8').strip())

            # check respone py post id
            pid = datahandled['post_id']
            matchObj = re.search(r"{}".format(pid), data)
            if not matchObj:
                success = "false"
                detail = "not found this post_id " + datahandled['post_id']
            
            # check edit 10 times
            matchObj = re.search(r'ครบกำหนด 10 ครั้ง', data)
            if matchObj:
                success = "false"
                detail = "today you is edited post 10 times วันนี้! คุณแก้ไขข้อมูลประกาศที่ใช้งานแล้ว ครบกำหนด 10 ครั้ง/วัน กรุณาใช้งานอีกครั้งในวันถัดไป"


            if success == "true":
                soup = BeautifulSoup(r.content, self.parser)
                sas_name = soup.find("input", {"name": "sas_name"})
                if sas_name:
                    sas_name = sas_name.get('value')
                code_edit = soup.find("input", {"name": "code_edit"})
                if code_edit: 
                    code_edit = code_edit.get('value')
                firstname = soup.find("input", {"name": "firstname"})
                if firstname:
                    firstname = firstname.get('value')
                mobile = soup.find("input", {"name": "mobile"})
                if mobile:
                    mobile = mobile.get('value')
                date_signup = soup.find("input", {"name": "date_signup"})
                if date_signup:
                    date_signup = date_signup.get('value')
                email = soup.find("input", {"name": "email"})
                if email:
                    email = email.get('value')
                contact_code = soup.find("input", {"name": "contact_code"})
                if contact_code:
                    contact_code = contact_code.get('value')
                ad_title = soup.find("textarea", {"name": "ad_title"})
                if ad_title:
                    ad_title = ad_title.contents[0]
                #for province in bangkok
                property_city_bkk = ''
                try:
                    property_city_bkk = soup.find("select", {"id": "property_city_bkk"}).find("option",{'selected':True})['value']
                except:
                    pass
                #for province not bangkok
                property_country_2 = ''
                property_city_2 = ''
                try:
                    property_country_2 = soup.find("select", {"id": "property_country_2"}).find("option",{'selected':True})['value']
                    property_city_2 = soup.find("select", {"id": "property_city_2"}).find("option",{'selected':True})['value']
                except:
                    pass
                #log.debug(ad_title)
                ad_title = ad_title + "\n" + str(datetime.datetime.utcnow())
                ad_title = ad_title.encode('cp874', 'ignore')
                
                datapost = dict(
                    code_edit=code_edit,
                    email=email,
                    mobile=mobile,
                    sas_name=sas_name,
                    contact_code=contact_code,
                    date_signup=date_signup,
                    firstname=firstname,
                    id=datahandled['post_id'],
                    ad_title=ad_title ,
                    Action_ad_title=1,
                    Action_headtitle=1,
                    Submit='Active',
                    property_city2=property_city_2.encode('cp874', 'ignore'),
                    property_city_2=property_city_2.encode('cp874', 'ignore'),
                    property_city_bkk=property_city_bkk.encode('cp874', 'ignore'),
                    property_country2=property_country_2.encode('cp874', 'ignore'),
                    property_country_2=property_country_2.encode('cp874', 'ignore'),
                )

                r = httprequestObj.http_post('https://www.thaihometown.com/editcontacts', data=datapost)
                data = r.text
                #f = open("editpostthaihometown.html", "wb")
                #f.write(data.encode('utf-8').strip())

                matchObj = re.search(r'https:\/\/www.thaihometown.com\/edit\/' + datahandled['post_id'], data)
                if matchObj:
                    success = "true"
                else:
                    success = "false"
                    detail = unquote(data)

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
            "log_id": datahandled['log_id'], 
            "post_id": datahandled['post_id'],
            "websitename": self.websitename,
            "post_view": post_view
        }


    def edit_post(self, postdata):
        #log.debug('')
        time_start = datetime.datetime.utcnow()

        # start proces
        #
        datahandled = self.postdata_handle(postdata)

        rent_price=0
        selling_price=0
        if datahandled['listing_type'] == 'ประกาศขาย' or datahandled['listing_type'] == 'ประกาศขายดาวน์':
            selling_price = datahandled['price_baht']
        elif datahandled['listing_type'] == 'ประกาศให้เช่า':
            rent_price = datahandled['price_baht']

        success = "true"
        detail = ""
        post_url = ''

        #area detect
        size,typeunit = self.getsizeunit(datahandled)

        success,detail = self.validatedatapost(datahandled)

        if datahandled['post_id'] == '' or datahandled['post_id'] == None:
            success = 'false'
            detail = 'post_id not defined'

        # login
        if success == 'true':
            self.test_login(postdata)
            test_login = self.test_login(postdata)
            success = test_login["success"]
            detail = test_login["detail"]

        if (success == "true"):
            #get provice district id
            success,detail,datahandled = self.getprovincedistrictid(datahandled)
            
            if success == 'true':
                r = httprequestObj.http_get('https://www.thaihometown.com/edit/' + datahandled['post_id'], verify=False)
                data = r.text
                # f = open("editpostthaihometown.html", "wb")
                # f.write(data.encode('utf-8').strip())

                # check respone py post id
                pid = datahandled['post_id']
                matchObj = re.search(r"{}".format(pid), data)
                if not matchObj:
                    success = "false"
                    detail = "not found this post_id " + datahandled['post_id']
                
                # check edit 10 times
                matchObj = re.search(r'�ѹ���! �س��䢢����Ż�С�ȷ����ҹ���� �ú��˹� 10', data)
                if matchObj:
                    success = "false"
                    detail = "today you have edited post 10 times วันนี้! คุณแก้ไขข้อมูลประกาศที่ใช้งานแล้ว ครบกำหนด 10 ครั้ง/วัน กรุณาใช้งานอีกครั้งในวันถัดไป"


                if success == "true":
                    soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')

                    sas_name = soup.find("input", {"name": "sas_name"})['value']
                    code_edit = soup.find("input", {"name": "code_edit"})['value']
                    firstname = soup.find("input", {"name": "firstname"})['value']
                    mobile = soup.find("input", {"name": "mobile"})['value']
                    date_signup = soup.find("input", {"name": "date_signup"})['value']
                    email = soup.find("input", {"name": "email"})['value']
                    contact_code = soup.find("input", {"name": "contact_code"})['value']
                    old_price = soup.find("input", {"name": "selling_price"})['value']

                    datapost = {
                        'code_edit':code_edit,
                        'email':email,
                        'mobile':mobile,
                        'sas_name':sas_name,
                        'contact_code':contact_code,
                        'date_signup':date_signup,
                        'firstname':firstname,
                        'headtitle':datahandled['post_title_th'].encode('cp874', 'ignore'),
                        'id':datahandled['post_id'],
                        'ActionForm2':'',
                        'Action_ad_title':1,
                        'Action_headtitle':1,
                        'Name_Project2':'',
                        'Owner_Project2':'',
                        'Status_Project2':0,
                        'Submit':'Active',
                        'ad_title':datahandled['post_description_th'].encode('cp874', 'ignore'),
                        'carpark':'',
                        'carpark2':0,
                        'conditioning':'',
                        'conditioning2':0,
                        'info[0]' :'ตกแต่งห้องนอน'.encode('cp874', 'ignore'),
                        'info[1]' :'ตกแต่งห้องนั่งเล่น'.encode('cp874', 'ignore'),
                        'info[2]' :'ปูพื้นเซรามิค'.encode('cp874', 'ignore'),
                        'info[3]' :'เฟอร์นิเจอร์'.encode('cp874', 'ignore'),
                        'info[4]' :'ไมโครเวฟ'.encode('cp874', 'ignore'),
                        'info[5]' :'ชุดรับแขก'.encode('cp874', 'ignore'),
                        'infomation2[0]' :'ตกแต่งห้องนอน'.encode('cp874', 'ignore'),
                        'infomation2[1]' :'ตกแต่งห้องนั่งเล่น'.encode('cp874', 'ignore'),
                        'infomation2[2]' :'ปูพื้นเซรามิค'.encode('cp874', 'ignore'),
                        'infomation2[3]' :'เฟอร์นิเจอร์'.encode('cp874', 'ignore'),
                        'infomation2[4]' :'ไมโครเวฟ'.encode('cp874', 'ignore'),
                        'infomation2[5]' :'ชุดรับแขก'.encode('cp874', 'ignore'),
                        'price_number_unit2':0,
                        'price_unit':'',
                        'promotion_bonus2':0,
                        'promotion_discount2':0,
                        'property_area': size, 
                        'property_area2': size,
                        'property_sqm': typeunit,
                        'property_sqm4': typeunit,
                        'property_bts':'',
                        'property_bts2':'',
                        'property_city2':datahandled['property_city_2'].encode('cp874', 'ignore'),
                        'property_city_2':datahandled['property_city_2'].encode('cp874', 'ignore'),
                        'property_city_bkk':datahandled['property_city_bkk'].encode('cp874', 'ignore'),
                        'property_country2':datahandled['property_country_2'].encode('cp874', 'ignore'),
                        'property_country_2':datahandled['property_country_2'].encode('cp874', 'ignore'),
                        'property_mrt':'',
                        'property_mrt2':'',
                        'property_purple':'',
                        'property_purple2':'',
                        'property_type':datahandled['property_type'].encode('cp874', 'ignore'),
                        'property_type2':datahandled['property_type'].encode('cp874', 'ignore'),
                        'rent_price':rent_price,
                        'rent_price_number2':rent_price,
                        'room1':datahandled['bed_room'],
                        'room12':datahandled['bed_room'],
                        'room2':datahandled['bath_room'],
                        'room22':datahandled['bath_room'],
                        'selling_price':selling_price,
                        'selling_price_number2':old_price,
                        'type_forrent':'',
                        'type_forrent2':0,
                        'typepart':datahandled['listing_type'].encode('cp874', 'ignore'),
                        'typeunit5':'ต่อตร.ม'.encode('cp874', 'ignore'),
                        'notprice' : 1 if datahandled['price_baht'] == 0 or datahandled['price_baht'] == None else 0,
                    }

                    print('----------------------')
                    print(datapost)
                    print('----------------------')

                    #log.debug(datapost)

                    r = httprequestObj.http_post('https://www.thaihometown.com/editcontacts', data=datapost)
                    data = r.text
                    #f = open("debug_response/editpostthaihometown.html", "wb")
                    #f.write(data.encode('utf-8').strip())

                    matchObj = re.search(r'https:\/\/www.thaihometown.com\/edit\/' + datahandled['post_id'], data)
                    if matchObj:
                        success = "true"
                        #get post url
                        post_url = self.getposturl(datahandled['post_id'],datahandled['property_type3'])
                        #upload image
                        self.uploadimage(datahandled,datahandled['post_id'])
                    else:
                        success = "false"
                        detail = unquote(data)
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success, 
            "usage_time": str(time_usage), 
            "start_time": str(time_start), 
            "end_time": str(time_end), 
            "detail": detail, 
            "ds_id": postdata['ds_id'],
            "log_id": datahandled['log_id'],
            "ds_id": postdata['ds_id'], 
            "post_id": datahandled['post_id'],
            "websitename": self.websitename
        }

    def search_post(self,data):
        start_time = datetime.datetime.utcnow()

        test_login = self.test_login(data)
        # print('in')
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ''
        post_url = ''
        post_found = ''
        post_title = data['post_title_th']
        if success == 'true':

            url = 'https://www.thaihometown.com/member/'+str(self.logid)
            req = httprequestObj.http_get(url)
            soup = BeautifulSoup(req.content,'html.parser')
            posts = soup.find('div',{'id':'show_listings'}).findAll('div')[2:]
            valid_ids = []
            valid_urls = []
            valid_titles = []
            for post in posts:
                #print('id' in post)
                if post.has_attr('id') and post['id'] is not None and str(post['id'])[:9] == 'indivList':
                    id = str(post['id'])[13:]
                    valid_ids.append(str(post['id'])[13:])
                    # print('here1')
                    urls = post.findAll('a')
                    if str(urls[0]).find('member')!=-1:
                        valid_titles.append(str(urls[1].text).strip())
                    else:
                        valid_titles.append(str(urls[0].text).strip())
                    # print('here2')
                    for url in urls:
                        # print(url)
                        if str(url['href']).find(id)+len(id) == len(url['href']):
                            valid_urls.append(str(url['href']))
                            # print('here3')
                            break
            # print('out')
            print(valid_titles)
            # print(valid_urls)
            # print(valid_ids)
            if post_title.strip() in valid_titles:
                post_found = 'true'
                detail = 'Post found'
                for i in range(len(valid_titles)):
                    if valid_titles[i] == post_title:
                        post_id = valid_ids[i]
                        post_url = valid_urls[i]
                        break
            else:
                post_found = 'false'
                detail = 'Post not found'


        end_time = datetime.datetime.utcnow()
        result = {
            "success": "true",
            "usage_time": str(end_time - start_time),
            "start_time": str(start_time),
            "end_time": str(end_time),
            "detail": detail,
            'ds_id': data['ds_id'],
            "log_id": data['log_id'],
            "post_found": post_found,
            "post_id": post_id,
            'post_url': post_url,
            "post_create_time": '',
            "post_modify_time": '',
            "post_view": '',
            'websitename': 'thaihometown'
        }
        return result


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
            "log_id": datahandled['log_id'], 
            "post_id": datahandled['post_id'],
            "websitename": self.websitename,
            #"post_url": post_url
        }
