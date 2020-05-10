# -*- coding: utf-8 -*-

import logging
import logging.config
from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
# from urlparse import urlparse
import re
import json
import datetime
import sys
from urllib.parse import unquote
httprequestObj = lib_httprequest()
from requests_toolbelt import MultipartEncoder
import string
import random

try:
    import configs
except ImportError:
    configs = {}
logging.config.dictConfig(getattr(configs, 'logging_config', {}))
log = logging.getLogger()


class renthub():

    name = 'renthub'

    def __init__(self):

        self.websitename = 'renthub'
        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.debug = 0
        self.debugresdata = 0
        self.parser = 'html.parser'
        self.handled = False
    
    def postdata_handle(self, postdata):
        log.debug('')

        if self.handled == True:
            return postdata

        datahandled = {}

        try:
            datahandled['price_baht'] = postdata['price_baht']
        except KeyError as e:
            datahandled['price_baht'] = 0
            log.warning(str(e))

        try:
            datahandled['addr_province'] = postdata['addr_province']
        except KeyError as e:
            datahandled['addr_province'] = ''
            log.warning(str(e))

        try:
            datahandled['addr_district'] = postdata['addr_district']
        except KeyError as e:
            datahandled['addr_district'] = ''
            log.warning(str(e))

        try:
            datahandled['addr_sub_district'] = postdata['addr_sub_district']
        except KeyError as e:
            datahandled['addr_sub_district'] = ''
            log.warning(str(e))

        try:
            datahandled['addr_road'] = postdata['addr_road']
        except KeyError as e:
            datahandled['addr_road'] = ''
            log.warning(str(e))

        try:
            datahandled['addr_near_by'] = postdata['addr_near_by']
        except KeyError as e:
            datahandled['addr_near_by'] = ''
            log.warning(str(e))

        try:
            datahandled['addr_postcode'] = postdata['addr_postcode']
        except KeyError as e:
            datahandled['addr_postcode'] = ''
            log.warning(str(e))

        try:
            datahandled['floor_area'] = postdata['floor_area']
        except KeyError as e:
            datahandled['floor_area'] = 0
            log.warning(str(e))

        try:
            datahandled['geo_latitude'] = postdata['geo_latitude']
        except KeyError as e:
            datahandled['geo_latitude'] = ''
            log.warning(str(e))

        try:
            datahandled['geo_longitude'] = postdata['geo_longitude']
        except KeyError as e:
            datahandled['geo_longitude'] = ''
            log.warning(str(e))

        try:
            datahandled['property_id'] = postdata['property_id']
        except KeyError as e:
            datahandled['property_id'] = ''
            log.warning(str(e))

        try:
            datahandled['post_title_th'] = postdata['post_title_th']
        except KeyError as e:
            datahandled['post_title_th'] = ''
            log.warning(str(e))

        try:
            datahandled['post_description_th'] = postdata['post_description_th']
        except KeyError as e:
            datahandled['post_description_th'] = ''
            log.warning(str(e))

        try:
            datahandled['post_title_en'] = postdata['post_title_en']
        except KeyError as e:
            datahandled['post_title_en'] = ''
            log.warning(str(e))

        try:
            datahandled['post_description_en'] = postdata['post_description_en']
        except KeyError as e:
            datahandled['post_description_en'] = ''
            log.warning(str(e))

        try:
            datahandled['ds_id'] = postdata["ds_id"]
        except KeyError as e:
            datahandled['ds_id'] = ''
            log.warning(str(e))

        try:
            datahandled['ds_name'] = postdata["ds_name"]
        except KeyError as e:
            datahandled['ds_name'] = ''
            log.warning(str(e))

        try:
            datahandled['user'] = postdata['user']
        except KeyError as e:
            datahandled['user'] = ''
            log.warning(str(e))

        try:
            datahandled['pass'] = postdata['pass']
        except KeyError as e:
            datahandled['pass'] = ''
            log.warning(str(e))

        try:
            datahandled['project_name'] = postdata["project_name"]
        except KeyError as e:
            datahandled['project_name'] = ''
            log.warning(str(e))

        try:
            datahandled['name'] = postdata["name"]
        except KeyError as e:
            datahandled['name'] = ''
            log.warning(str(e))

        try:
            datahandled['mobile'] = postdata["mobile"]
        except KeyError as e:
            datahandled['mobile'] = ''
            log.warning(str(e))

        try:
            datahandled['email'] = postdata["email"]
        except KeyError as e:
            datahandled['email'] = ''
            log.warning(str(e))

        try:
            datahandled['web_project_name'] = postdata["web_project_name"]
        except KeyError as e:
            datahandled['web_project_name'] = ''
            log.warning(str(e))

        try:
            datahandled['action'] = postdata["action"]
        except KeyError as e:
            datahandled['action'] = ''
            log.warning(str(e))

        try:
            datahandled['bath_room'] = postdata["bath_room"]
        except KeyError as e:
            datahandled['bath_room'] = 0
            log.warning(str(e))

        try:
            datahandled['bed_room'] = postdata["bed_room"]
        except KeyError as e:
            datahandled['bed_room'] = 0
            log.warning(str(e))

        try:
            datahandled['floor_total'] = postdata["floor_total"]
        except KeyError as e:
            datahandled['floor_total'] = 1
            log.warning(str(e))

        try:
            datahandled['floor_level'] = postdata["floor_level"]
        except KeyError as e:
            datahandled['floor_level'] = 1
            log.warning(str(e))

        

        # image
        datahandled['post_images'] = postdata["post_images"]

        try:
            datahandled['post_id'] = postdata["post_id"]
        except KeyError as e:
            datahandled['post_id'] = ''
            log.warning(str(e))

        try:
            datahandled['log_id'] = postdata["log_id"]
        except KeyError as e:
            datahandled['log_id'] = ''
            log.warning(str(e))

       

        try:
            datahandled['addr_road'] = postdata["addr_road"]
        except KeyError as e:
            datahandled['addr_road'] = ''
            log.warning(str(e))

        try:
            datahandled['company_name'] = postdata["company_name"]
        except KeyError as e:
            datahandled['company_name'] = ''
            log.warning(str(e))

        try:
            datahandled['name_title'] = postdata["name_title"]
        except KeyError as e:
            datahandled['name_title'] = ''
            log.warning(str(e))

        try:
            datahandled['name_th'] = postdata["name_th"]
        except KeyError as e:
            datahandled['name_th'] = ''
            log.warning(str(e))

        try:
            datahandled['surname_th'] = postdata["surname_th"]
        except KeyError as e:
            datahandled['surname_th'] = ''
            log.warning(str(e))

        try:
            datahandled['name_en'] = postdata["name_en"]
        except KeyError as e:
            datahandled['name_en'] = ''
            log.warning(str(e))

        try:
            datahandled['surname_en'] = postdata["surname_en"]
        except KeyError as e:
            datahandled['surname_en'] = ''
            log.warning(str(e))

        try:
            datahandled['tel'] = postdata["tel"]
        except KeyError as e:
            datahandled['tel'] = ''
            log.warning(str(e))

        try:
            datahandled['line'] = postdata["line"]
        except KeyError as e:
            datahandled['line'] = ''
            log.warning(str(e))
        
        try:
            datahandled['addr_number'] = postdata["addr_number"]
        except KeyError as e:
            datahandled['addr_number'] = None
            log.warning(str(e))

        try:
            datahandled['direction_type'] = postdata["direction_type"]     
        except KeyError as e:
            datahandled['direction_type'] = 'East'
            log.warning(str(e))
        # 11 เหนือ north
        # 12 ใต้ south
        # 13 ออก east
        # 14 ตก west
        # 21 ตอฉน north east 
        # 22 ตอฉต south ease
        # 23 ตตฉน north west
        # 24 ตตฉต south west
        if datahandled['direction_type'] == 11:
            datahandled['direction_type'] = 'North'
        if datahandled['direction_type'] == 12:
            datahandled['direction_type'] = 'South'
        if datahandled['direction_type'] == 13:
            datahandled['direction_type'] = 'East'
        if datahandled['direction_type'] == 14:
            datahandled['direction_type'] = 'West'
        if datahandled['direction_type'] == 21:
            datahandled['direction_type'] = 'NorthEast'
        if datahandled['direction_type'] == 22:
            datahandled['direction_type'] = 'SouthEast'
        if datahandled['direction_type'] == 23:
            datahandled['direction_type'] = 'NorthWest'
        else: #24
            datahandled['direction_type'] = 'SouthWest'
        
        try:
            datahandled['property_type'] = postdata["property_type"]
        except KeyError as e:
            datahandled['property_type'] = 1
            log.warning(str(e))
        
        try:
            datahandled['listing_type'] = postdata["listing_type"]
        except KeyError as e:
            datahandled['listing_type'] = 'ขาย'
            log.warning(str(e))
        
        try:
            datahandled['addr_soi'] = postdata["addr_soi"]
        except KeyError as e:
            datahandled['addr_soi'] = ''
            log.warning(str(e))

        
        datahandled['use_project_name'] = datahandled['project_name']
        if datahandled['web_project_name'] != None and datahandled['web_project_name'] != '':
            datahandled['use_project_name'] = datahandled['web_project_name']
        
        #fix null, renthub error 500
        for key, val in datahandled.items():
            if val == None:
                datahandled[key] = ''
        
        self.handled = True

        return datahandled
    
    def getareaid(self,datahandled):
        
        datahandled['province_code'] = ""
        datahandled['district_code'] = ""
        datahandled['subdistrict_code'] = ""
        success = "true"
        detail =  ''

        # get province id
        # ที่ต้อง get จาก file เพราะ renthub ไม่ provide selectbox province มาให้ตั้งแต่ต้น และ ไม่มี ajax เพื่อ get select province id
        with open("./static/renthub_province.json") as f:
            province = json.load(f)
        for key, value in province.items():
            if datahandled['addr_province'] == value:
                datahandled['province_code'] = key
                log.debug('province is  %s' % (datahandled['province_code'],))
                break
        if datahandled['province_code'] == "":
            success = "false"
            detail = "not found code for province  %s" % (datahandled['addr_province'],)
            log.warning("not found code for province  %s" % (datahandled['addr_province'],))
        
        # get district id
        if success == "true":
            datapost = {'province_code': datahandled['province_code'] , 'model_class':'condo_project'}
            r = httprequestObj.http_post('https://renthub.in.th/misc/on_select_province_changed',data=datapost)
            data = r.text
            soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
            try:
                datahandled['district_code'] = soup.find('select',{'class':'short'}).find('option',text=re.compile(datahandled['addr_district']))['value']
                log.debug('district is  %s' % (datahandled['district_code'],))
            except:
                success = "false"
                detail = "not found code for district  %s" % (datahandled['addr_district'],)
                log.warning("not found code for district  %s" % (datahandled['addr_district'],))
                pass
        
        # get subdistrict id
        if success == "true":
            datapost = {'district_code': datahandled['district_code'] , 'model_class':'condo_project'}
            r = httprequestObj.http_post('https://renthub.in.th/misc/on_select_district_changed',data=datapost)
            data = r.text
            soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
            try:
                datahandled['subdistrict_code'] = soup.find('select',{'class':'short'}).find('option',text=re.compile(datahandled['addr_sub_district']))['value']
                log.debug('district is  %s' % (datahandled['subdistrict_code'],))
            except:
                success = "false"
                detail = "not found code for subdistrict  %s" % (datahandled['addr_sub_district'],)
                log.warning("not found code for subdistrict  %s" % (datahandled['addr_sub_district'],))
                pass           

        if datahandled['province_code'] == '' or  datahandled['district_code'] == '' or datahandled['subdistrict_code'] == '':
            return 'false','wrong province or district or subdistrict '+datahandled['addr_province']+' '+datahandled['addr_district']+' '+datahandled['addr_sub_district'],datahandled

        return 'true','',datahandled



    def register_user(self, postdata):
        log.debug('')
        time_start = datetime.datetime.utcnow()

        # start process
        #
        datahandled = self.postdata_handle(postdata)
        user = datahandled['user']
        passwd = datahandled['pass']
        company_name = datahandled['company_name']
        name_title = datahandled["name_title"]
        name_th = datahandled["name_th"]
        surname_th = datahandled["surname_th"]
        name_en = datahandled["name_en"]
        surname_en = datahandled["surname_en"]
        tel = datahandled["tel"]
        line: datahandled["amarin.ta"]
        addr_province = datahandled["addr_province"]

        # POST
        # https://renthub.in.th/signup
        # authenticity_token=/Ha+oc+M/vFof/rlvlbJdNOtw4/drQPvVs+/VKazQvE=&commit=%E0%B8%AA%E0%B8%A1%E0%B8%B1%E0%B8%84%E0%B8%A3%E0%B8%AA%E0%B8%A1%E0%B8%B2%E0%B8%8A%E0%B8%B4%E0%B8%81&user%5Bemail%5D=kla.arnut@hotmail.com&user%5Bname%5D=arnut&user%5Bpassword%5D=vkIy9b&user%5Bpassword_confirmation%5D=vkIy9b&user%5Bphone%5D=0887779999&user%5Bprovince_code%5D=&user%5Broles%5D=apartment_manager&user%5Bsubscribe_newsletter%5D=0&utf8=%E2%9C%93

        success = "false"
        detail = "Under construction"

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
        }

    def test_login(self, postdata):
        log.debug('')
        time_start = datetime.datetime.utcnow()

        # start process
        #
        datahandled = self.postdata_handle(postdata)
        user = datahandled['user']
        passwd = datahandled['pass']

        success = "true"
        detail = ""

        #clear session
        r = httprequestObj.http_get('https://renthub.in.th/logout', verify=False)

        r = httprequestObj.http_get('https://renthub.in.th/login', verify=False)
        data = r.text
        soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
        authenticity_token = soup.find("input", {"name": "authenticity_token"})['value']

        datapost = {
            "user[email]": user,
            "user[password]": passwd,
            "user[remember_me]": 0,
            "utf8": "✓",
            "commit": "Sign in",
            "authenticity_token": authenticity_token
        }
        # authenticity_token=Gck8I7dhK778QqLcKkEcAAH2J+BAKVgltsLafwoRm20=
        # &commit=Sign%20in
        # &user%5Bemail%5D=kla.arnut@hotmail.com
        # &user%5Bpassword%5D=vkIy9b
        # &user%5Bremember_me%5D=0
        # &utf8=%E2%9C%93

        r = httprequestObj.http_post('https://renthub.in.th/login', data=datapost)
        data = r.text
        #f = open("debug_response/renthublogin.html", "wb")
        #f.write(data.encode('utf-8').strip())

        matchObj = re.search(r'ประกาศของคุณ', data)
        if not matchObj:
            success = "false"
            detail = "cannot login"
            log.debug('login fail')

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
        }

    def validatedata(self,datahandled):
        log.debug('')

        success = "true"
        detail = ""

        if datahandled['property_type'] != 1 and datahandled['property_type'] != 7:
            detail = "website not support property type "+ str(datahandled['property_type'])
        if datahandled['listing_type'] != 'เช่า':
            detail = "website not support listing type "+ str(datahandled['listing_type'])
        if datahandled['addr_number'] == None or datahandled['addr_number'] == "":
            if datahandled['property_type'] == 7:
                detail = "property type apartment is required addr_number"
        if datahandled['use_project_name'] == '' or datahandled['use_project_name'] == None:
            detail = "webprojectname or projectname is not defined "
        

        #remove link
        datahandled['post_title_th'] = re.sub(r'^https?:\/\/.*[\r\n]*', '', datahandled['post_title_th'], flags=re.MULTILINE)
        datahandled['post_title_en'] = re.sub(r'^https?:\/\/.*[\r\n]*', '', datahandled['post_title_en'], flags=re.MULTILINE)
        datahandled['post_description_th'] = re.sub(r'^https?:\/\/.*[\r\n]*', '', datahandled['post_description_th'], flags=re.MULTILINE)
        datahandled['post_description_en'] = re.sub(r'^https?:\/\/.*[\r\n]*', '', datahandled['post_description_en'], flags=re.MULTILINE)

        #title length is not more than 150char
        if len(datahandled['post_title_th']) > 150:
            datahandled['post_title_th'] = datahandled['post_title_th'][:150]
        if len(datahandled['post_title_en']) > 150:
            datahandled['post_title_en'] = datahandled['post_title_en'][:150]


        if detail != "":
            success =  "false"
        
        return success,detail
        

    def create_post(self, postdata):
        log.debug('')
        time_start = datetime.datetime.utcnow()

       
        # start process
        #
        success = ""
        detail = ""
        post_id = ""
        post_url = ""

        datahandled = self.postdata_handle(postdata)

        #validate
        success,detail = self.validatedata(datahandled)

        # login
        if success == "true":
            login = self.test_login(datahandled)
            success = login["success"]
            detail = login["detail"]

        #get area
        if success == "true":
            success,detail,datahandled = self.getareaid(datahandled)

        #go go go
        if success == "true":
            if datahandled['property_type'] == 1:
                success,detail,post_id,post_url = self.create_post_condo(datahandled)
            elif datahandled['property_type'] == 7:
                success,detail,post_id,post_url = self.create_post_apartment(datahandled)
            

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": datahandled['ds_id'],
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
            "websitename": self.websitename
            
        }
    
    def create_post_apartment(self,datahandled):
        log.debug("")

        success = "true"
        detail = ""
        post_id = ''
        posturl = ''

        # require login again , why why why ???????????
        r = httprequestObj.http_get('https://renthub.in.th/login', verify=False)
        data = r.text
        soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
        authenticity_token = soup.find("input", {"name": "authenticity_token"})['value']
        user = datahandled['user']
        passwd = datahandled['pass']
        datapost = {
            "user[email]": user,
            "user[password]": passwd,
            "user[remember_me]": 0,
            "utf8": "✓",
            "commit": "Sign in",
            "authenticity_token": authenticity_token
        }
        r = httprequestObj.http_post('https://renthub.in.th/login', data=datapost)
        data = r.text
        #f = open("debug_response/renthublogin.html", "wb")
        #f.write(data.encode('utf-8').strip())
        #


        r = httprequestObj.http_get('https://renthub.in.th/apartments/new', verify=False)
        data = r.text
        #f = open("debug_response/renthubcreate.html", "wb")
        #f.write(data.encode('utf-8').strip())
        soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
        authenticity_token = soup.find("input", {"name": "authenticity_token"})['value']

        arrimg = self.uploadimage('apartment',authenticity_token,datahandled)
        
        datapost = {
            '_wysihtml5_mode':1,
            'apartment[address]':datahandled['addr_number'],
            'apartment[air]':0,
            'apartment[allow_pet]':0,
            'apartment[allow_smoking]':0,
            'apartment[cctv]':0,
            'apartment[contact_person]':datahandled['name'],
            'apartment[detail]':'<div>' + datahandled['post_description_th'] + '</div>',
            'apartment[direct_phone]':0,
            'apartment[district_code]':datahandled['district_code'],
            'apartment[email]':datahandled['email'],
            'apartment[fan]':0,
            'apartment[fitness]':0,
            'apartment[furniture]':0,
            'apartment[has_promotion]':0,
            'apartment[internet]':0,
            'apartment[keycard]':0,
            'apartment[laundry]':0,
            'apartment[lift]':0,
            'apartment[line_id]':datahandled['line'],
            'apartment[name]':datahandled['post_title_th'],
            'apartment[parking]':0,
            'apartment[pool]':0,
            'apartment[postcode]':datahandled['addr_postcode'],
            'apartment[promotion]':'',
            'apartment[promotion_end]':'',
            'apartment[promotion_start]':'',
            'apartment[province_code]':datahandled['province_code'],
            'apartment[road]':datahandled['addr_road'],
            'apartment[salon]':0,
            'apartment[satellite]':0,
            'apartment[street]':datahandled['addr_soi'],
            'apartment[subdistrict_code]':datahandled['subdistrict_code'],
            'apartment[ubc]':0,
            'apartment[water_heater]':0,
            'apartment[wifi]':0,
            'apartment_phone[0]':datahandled['mobile'],
            'authenticity_token':authenticity_token,
            'commit':'ยอมรับเงื่อนไข และ ลงประกาศ',
            'fee[advance_fee_bath]':'',
            'fee[advance_fee_month]':'',
            'fee[advance_fee_type]':0,
            'fee[deposit_bath]':'',
            'fee[deposit_month]':'',
            'fee[deposit_type]':0,
            'fee[electric_price]':'',
            'fee[electric_price_minimum]':'',
            'fee[electric_price_type]':3,
            'fee[internet_price_bath]':'',
            'fee[internet_price_type]':0,
            'fee[phone_price_minute]':'',
            'fee[phone_price_minute_unit]':'',
            'fee[phone_price_time]':'',
            'fee[phone_price_type]':0,
            'fee[service_fee_price]':'',
            'fee[service_fee_type]':0,
            'fee[water_price]':'',
            'fee[water_price_minimum]':'',
            'fee[water_price_monthly_per_person]':'',
            'fee[water_price_monthly_per_person_remark]':'',
            'fee[water_price_monthly_per_room]':'',
            'fee[water_price_monthly_per_room_remark]':'',
            'fee[water_price_per_person_exceed]':'',
            'fee[water_price_per_room_exceed]':'',
            'fee[water_price_type]':5,
            'room_available[0]':1,
            'room_daily[0]':0,
            'room_has_rental[0]':1,
            'room_max_price_perday[0]':'',
            'room_max_price_permonth[0]':datahandled['price_baht'],
            'room_min_price_perday[0]':'',
            'room_min_price_permonth[0]':datahandled['price_baht'],
            'room_monthly[0]':1,
            'room_name[0]':'อพาร์ทเม้นท์',
            'room_size[0]':datahandled['floor_area'],
            'room_type[0]':0, #studio
            'temp[eng_detail]': '<div>' + datahandled['post_description_en'] + '</div>',
            'temp[eng_name]': datahandled['post_title_en'],
            'temp[is_service_apartment]':'false',
            'temp[lat]':datahandled['geo_latitude'],#16.3836649195804,
            'temp[lng]':datahandled['geo_longitude'],#102.8049505179853,
            'temp[no_eng_name]':'',
            'temp[nofacility]':1,
            'temp[nopicture]':'',
            'temp[picture_order]':','.join(arrimg),
            'temp[review_eng_detail]':'',
            'temp[review_thai_detail]':'',
            'utf8':'✓'
        }
        # print(datapost)
        r = httprequestObj.http_post('https://www.renthub.in.th/apartments', data=datapost)
        data = r.text
        # print(data)
        #f = open("debug_response/renthubpost.html", "wb")
        #f.write(data.encode('utf-8').strip())

        success,post_id,posturl,detail = self.getpostdataapartment(datahandled)

        
        return success,detail,post_id,posturl
    
    def create_post_condo(self,datahandled):
        log.debug("")

        success = "true"
        detail = ""
        post_id = ''
        posturl = ''

        # require login again , why why why ???????????
        r = httprequestObj.http_get('https://renthub.in.th/login', verify=False)
        data = r.text
        soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
        authenticity_token = soup.find("input", {"name": "authenticity_token"})['value']
        user = datahandled['user']
        passwd = datahandled['pass']
        datapost = {
            "user[email]": user,
            "user[password]": passwd,
            "user[remember_me]": 0,
            "utf8": "✓",
            "commit": "Sign in",
            "authenticity_token": authenticity_token
        }
        r = httprequestObj.http_post('https://renthub.in.th/login', data=datapost)
        data = r.text
        #f = open("debug_response/renthublogin.html", "wb")
        #f.write(data.encode('utf-8').strip())
        #


        r = httprequestObj.http_get('https://renthub.in.th/condo_listings/new', verify=False)
        data = r.text
        #f = open("debug_response/renthubcreate.html", "wb")
        #f.write(data.encode('utf-8').strip())
        soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
        authenticity_token = soup.find("input", {"name": "authenticity_token"})['value']

        arrimg = self.uploadimage('condo',authenticity_token,datahandled)
        
        # https://renthub.in.th/condo_listings
        datapost = {
            'authenticity_token': authenticity_token,
            'amenities[air]': 0,
            'amenities[digital_door_lock]': 0,
            'amenities[furniture]': 0,
            'amenities[hot_tub]': 0,
            'amenities[internet]': 0,
            'amenities[kitchen_hood]': 0,
            'amenities[kitchen_stove]': 0,
            'amenities[phone]': 0,
            'amenities[refrigerator]': 0,
            'amenities[tv]': 0,
            'amenities[washer]': 0,
            'amenities[water_heater]': 0,
            'commit': 'ยอมรับเงื่อนไข และ ลงประกาศ',
            'condo_listing[condo_project_id]': self.getprojectid(datahandled['use_project_name']),
            'condo_listing[contact_person]': datahandled['name'],
            'condo_listing[detail]': '<div>' + datahandled['post_description_th'] + '</div>',
            'condo_listing[email]': datahandled['email'],  # email,
            'condo_listing[phone[0]]': datahandled['mobile'],
            'condo_listing[post_type]': 2, # 2 คือ ให้เช่า
            'condo_listing[title]': datahandled['post_title_th'],
            'english[detail]': '<div>' + datahandled['post_description_en'] + '</div>',
            'english[title]': datahandled['post_title_en'],
            'rental[advance_fee_bath]': '',
            'rental[advance_fee_month]': 0,
            'rental[advance_fee_type]': 0,
            'rental[daily_price_type]': 2,
            'rental[deposit_bath]': '',
            'rental[deposit_month]': '',
            'rental[deposit_type]': 0,
            'rental[min_daily_rental_price]': '',
            'rental[min_rental_price]': datahandled['price_baht'],
            'rental[price_type]': 1,
            'room_information[building]': '',
            'room_information[direction]': datahandled['direction_type'],
            'room_information[no_of_bath]': datahandled['bath_room'],
            'room_information[no_of_bed]': datahandled['bed_room'],
            'room_information[on_floor]': datahandled['floor_level'],
            'room_information[remark]': '',
            'room_information[room_area]': datahandled['floor_area'],
            'room_information[room_home_address]': '',
            'room_information[room_no]': '',
            'room_information[room_type]': 0,
            'sale[existing_rental_contract_end]': '',
            'sale[existing_rental_price]': '',
            'sale[existing_renter_nationality]': '',
            'sale[price_type]': 1,
            'sale[sale_price]': '',
            'sale[with_rental_contract]': 0,
            'sale_deposit[price_type]': 1,
            'sale_deposit[sale_deposit_price]': '',
            'sale_right[contract_price]': '',
            'sale_right[price_type]': 1,
            'sale_right[remaining_downpayment]': '',
            'sale_right[remaining_downpayment_months]': '',
            'sale_right[remaining_payment]': '',
            'sale_right[sale_right_price]': '',
            'temp[no_eng_title_check]': '',
            'temp[noamenity]': 1,
            'temp[nopicture]': '',#1,
            'temp[picture_order]': ','.join(arrimg),#'',
            'temp[room_no_picture_id_input]': '',
            'temp[subscribe_newsletter]':0,
            'utf8': '✓',
            'condo_project[lat]': datahandled['geo_latitude'],#16.432115710705236,
            'condo_project[lng]': datahandled['geo_longitude'],#103.57590562193461,
            'condo_project[road]':datahandled['addr_road'],
            'condo_project[street]':datahandled['addr_soi'],
            'condo_project[province_code]': datahandled['province_code'],
            'condo_project[district_code]':datahandled['district_code'],
            'condo_project[subdistrict_code]':datahandled['subdistrict_code'],
            'condo_project[postcode]':datahandled['addr_postcode'],
        }
        # print(datapost)
        r = httprequestObj.http_post('https://renthub.in.th/condo_listings', data=datapost)
        data = r.text
        # print(data)
        #f = open("debug_response/renthubpost.html", "wb")
        #f.write(data.encode('utf-8').strip())

        success,post_id,posturl,detail = self.getpostdatacondo(datahandled)

        
        return success,detail,post_id,posturl
    
    def getprojectid(self,projectname):
        log.debug('')
        projectid = projectname
        r = httprequestObj.http_get('https://renthub.in.th/condo_listings/search_project?name='+str(projectname), verify=False)
        log.debug(r.text)
        data = json.loads(r.text)

        if len(data) > 0:
            projectid = data[0]['id']

        return projectid

    def uploadimage(self,listingtype,authenticity_token,datahandled):
        log.debug('')

        urlupload = 'https://renthub.in.th/condo_listing_pictures'
        prefixfileid = 'p1e7'
        if listingtype == 'apartment':
            urlupload = 'https://renthub.in.th/apartment_pictures'
            prefixfileid = 'p1e8'
        
        arrimg = []

        imgcount = len(datahandled['post_images'])
        for i in range(imgcount):
            datapost = {
                        'name':str(i+1) + '.jpg',
                        'authenticity_token': str(authenticity_token),
                        'fileid': prefixfileid + ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(24)),
                        'file':( str(i+1) + '.jpg', open(os.path.abspath(datahandled['post_images'][i]), 'rb'), 'image/jpeg'),
            }
            encoder = MultipartEncoder(fields=datapost)
            r = httprequestObj.http_post(
            urlupload,
            data=encoder,
            headers={'Content-Type': encoder.content_type}
            )
            data = r.json()
            log.debug(data)
            arrimg.append('pic_'+str(data['id']))
        
        return arrimg


    def getpostdataapartment(self,datahandled):
        log.debug('')

        postid = ''
        posturl = ''
        detail = ''
        success = 'true'

        #get from not publish
        r = httprequestObj.http_get('https://renthub.in.th/dashboard/apartments', verify=False)
        data = r.text
        soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
        try:
            lis = soup.find_all('li',id=re.compile('apartment_'))
            for li in lis:
                if li.find('a',text=re.compile(datahandled['post_title_th'])) != None:
                    posturl = 'https://renthub.in.th' + li.find('a',text=re.compile(datahandled['post_title_th']))['href']
                    postid = re.search(r'apartment_(\d+)',li['id']).group(1)
                    log.debug('posturl %s postid %s detail %s',str(posturl),str(postid),str(detail))
                    break
        except:
            success = 'false'
            log.debug('not found apartment post in dashboard')
            detail = 'not found apartment post in dashboard'
        
        if postid == '' or posturl == '':
            success = 'false'
            log.debug('not found apartment post in dashboard')
            detail = 'not found apartment post in dashboard'

        
        return success,postid,posturl,detail


    def getpostdatacondo(self,datahandled):
        log.debug('')

        postid = ''
        posturl = ''
        detail = ''
        success = 'true'

        #get from not publish
        r = httprequestObj.http_get('https://renthub.in.th/dashboard/condo_listings?need_revise=true', verify=False)
        data = r.text
        soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
        try:
            lis = soup.find_all('li',id=re.compile('condo_listing_'))
            for li in lis:
                if li.find('a',text=re.compile(datahandled['post_title_th'])) != None:
                    posturl = 'https://renthub.in.th' + li.find('a',text=re.compile(datahandled['post_title_th']))['href']
                    postid = re.search(r'condo_listing_(\d+)',li['id']).group(1)
                    success = 'false'
                    detail = 'ประกาศนี้ยังไม่ได้แสดงในเวป RentHub กรุณากดแก้ไขและระบุโครงการให้ครบถ้วน หากไม่พบโครงการที่ต้องการลงประกาศ สามารถแจ้งเพิ่มโครงการใหม่ได้ที่ content@renthub.in.th'
                    log.debug('posturl %s postid %s detail %s',str(posturl),str(postid),str(detail))
                    break
        except:
            log.debug('not found in ประกาศรอแก้ไข')

        #get from current publish
        r = httprequestObj.http_get('https://renthub.in.th/dashboard/condo_listings', verify=False)
        data = r.text
        soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
        try:
            lis = soup.find_all('li',id=re.compile('condo_listing_'))
            for li in lis:
                if li.find('a',text=re.compile(datahandled['post_title_th'])) != None:
                    posturl = 'https://renthub.in.th' + li.find('a',text=re.compile(datahandled['post_title_th']))['href']
                    postid = re.search(r'condo_listing_(\d+)',li['id']).group(1)
                    log.debug('posturl %s postid %s detail %s',str(posturl),str(postid),str(detail))
                    break
        except:
            log.debug('not found in ประกาศที่แสดงปัจจุบัน')

        if postid == '' or posturl == '':
            success = 'false'
            detail = 'cannot find new post attribute'
        
        return success,postid,posturl,detail


  

    def boost_post(self, postdata):
        log.debug('')
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

            r = httprequestObj.http_get('https://www.thaihometown.com/edit/'+post_id, verify=False)
            data = r.text
            #f = open("editpostthaihometown.html", "wb")
            #f.write(data.encode('utf-8').strip())

            # check respone py post id
            matchObj = re.search(r''+post_id+'', data)
            if not matchObj:
                success = "false"
                detail = "not found this post_id "+post_id

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
                    # ad_title=ad_title.encode('cp874','ignore'),  # + "\n" + datenow,
                    ad_title=ad_title + "\n" + datenow,
                    Action_ad_title=1,
                    Action_headtitle=1,
                    Submit='Active',


                    # Name_Project2='',
                    # Owner_Project2='',
                    # Status_Project2=0,
                    # headtitle=post_title_th.encode('cp874','ignore'),
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

                matchObj = re.search(r'https:\/\/www.thaihometown.com\/edit\/'+post_id, data)
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
            "log_id": log_id,
            "post_id": post_id
        }

    def delete_post(self, postdata):
        log.debug('')
        time_start = datetime.datetime.utcnow()

        # TODO ประกาศที่ทดสอบไป ยังไม่ครบ 7 วัน ทำทดสอบการลบไม่ได้ วันหลังค่อยมาทำใหม่
        log_id = postdata['log_id']
        post_id = postdata['post_id']
        user = postdata['user']
        passwd = postdata['pass']

        # start process
        #
        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]

        # if success == "true":

        #
        # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            # "detail": detail,
            "detail": "under construction",
            "log_id": log_id,
        }

    def edit_post(self, postdata):
        log.debug('')
        time_start = datetime.datetime.utcnow()

        post_img_url_lists = postdata['post_img_url_lists']
        price_baht = postdata['price_baht']
        county = postdata["county"]
        district = postdata["district"]
        # addr_province = postdata['addr_province']
        # addr_district = postdata['addr_district']
        # addr_sub_district = postdata['addr_sub_district']
        # addr_road = postdata['addr_road']
        # addr_near_by = postdata['addr_near_by']
        # floorarea_sqm = postdata['floorarea_sqm']
        geo_latitude = postdata['geo_latitude']
        geo_longitude = postdata['geo_longitude']
        # property_id = postdata['property_id']
        post_title_th = postdata['post_title_th']
        post_description_th = postdata['post_description_th']
        post_title_en = postdata['post_title_en']
        post_description_en = postdata['post_description_en']
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

            r = httprequestObj.http_get('https://www.thaihometown.com/edit/'+post_id, verify=False)
            data = r.text
            # f = open("editpostthaihometown.html", "wb")
            # f.write(data.encode('utf-8').strip())

            # check respone py post id
            matchObj = re.search(r''+post_id+'', data)
            if not matchObj:
                success = "false"
                detail = "not found this post_id "+post_id

            if success == "true":
                soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')

                sas_name = soup.find("input", {"name": "sas_name"})['value']
                # headtitle = soup.find("textarea", {"name": "headtitle"}).contents
                # headtitle = headtitle[0]

                code_edit = soup.find("input", {"name": "code_edit"})['value']
                firstname = soup.find("input", {"name": "firstname"})['value']
                mobile = soup.find("input", {"name": "mobile"})['value']
                date_signup = soup.find("input", {"name": "date_signup"})['value']
                email = soup.find("input", {"name": "email"})['value']
                contact_code = soup.find("input", {"name": "contact_code"})['value']

                datapost = dict(
                    code_edit=code_edit,
                    email=email,
                    mobile=mobile,
                    sas_name=sas_name,
                    contact_code=contact_code,
                    date_signup=date_signup,
                    firstname=firstname,
                    headtitle=post_title_th.encode('cp874', 'ignore'),

                    id=post_id,

                    ActionForm2='',

                    Action_ad_title=1,
                    Action_headtitle=1,
                    Name_Project2='',
                    Owner_Project2='',
                    Status_Project2=0,
                    Submit='Active',
                    ad_title=post_description_th.encode('cp874', 'ignore'),
                    carpark='',
                    carpark2=0,
                    conditioning='',
                    conditioning2=0,

                    # headtitle2='888888',  # post_title_th.encode('cp874','ignore'),
                    info=[],
                    infomation2=[' ตกแต่งห้องนอน ', ' ตกแต่งห้องนั่งเล่น ', ' ปูพื้นเซรามิค ', ' เฟอร์นิเจอร์ ', ' ไมโครเวฟ ', ' ชุดรับแขก '],
                    notprice=1,
                    price_number_unit2=0,
                    price_unit='',
                    promotion_bonus2=0,
                    promotion_discount2=0,
                    property_area=55,
                    property_area2=0.00,
                    property_bts='',
                    property_bts2='',
                    property_city2='ราษฎร์บูรณะ',
                    property_city_2='',
                    property_city_bkk='ยานนาวา+Yannawa',
                    property_country2='กรุงเทพมหานคร',
                    property_country_2='',
                    property_mrt='',
                    property_mrt2='',
                    property_purple='',
                    property_purple2='',
                    property_sqm=1,
                    property_sqm4=1,
                    property_type='บ้าน+Home',
                    property_type2='บ้าน+Home',
                    rent_price='',
                    rent_price_number2=0,
                    room1=2,
                    room12=2,
                    room2=3,
                    room22=3,
                    selling_price='',
                    selling_price_number2=0,
                    type_forrent='',
                    type_forrent2=0,
                    typepart='ประกาศขาย',
                    typeunit5=''
                )

                r = httprequestObj.http_post('https://www.thaihometown.com/editcontacts', data=datapost)
                data = r.text
                #f = open("editpostthaihometown.html", "wb")
                #f.write(data.encode('utf-8').strip())

                matchObj = re.search(r'https:\/\/www.thaihometown.com\/edit\/'+post_id, data)
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
            "log_id": log_id,
            "post_id": post_id
        }

