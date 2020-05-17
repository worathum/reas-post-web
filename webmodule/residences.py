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
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
from requests_toolbelt import MultipartEncoder


httprequestObj = lib_httprequest()

try:
    import configs
except ImportError:
    configs = {}
logging.config.dictConfig(getattr(configs, 'logging_config', {}))
log = logging.getLogger()


class residences():

    name = 'residences'

    def __init__(self):

        try:
            import configs
        except ImportError:
            configs = {}

        self.websitename = 'residences'
        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.primary_domain = 'https://www.residences.in.th'
        self.debug = 0
        self.debugresdata = 0
        self.parser = 'html.parser'



    '''
    Method:    POST
    URL:    https://www.residences.in.th/users
    Request Body:   authenticity_token=yvcIuGwXogGW+epiaSMNKE6FyJI7Gaz6nV0iWw/mc8A=&commit=%E0%B8%AA%E0%B8%A1%E0%B8%B1%E0%B8%84%E0%B8%A3%E0%B8%AA%E0%B8%A1%E0%B8%B2%E0%B8%8A%E0%B8%B4%E0%B8%81&user%5Bemail%5D=amarin.ta@gmail.com&user%5Bemail_notice%5D=0&user%5Bemail_notice%5D=1&user%5Bmember_type%5D=0&user%5Bname%5D=amarin%20boonkirt&user%5Bpassword%5D=5k4kk3253434&user%5Bpassword_confirmation%5D=5k4kk3253434&user%5Btelephone%5D=0891999450&utf8=%E2%9C%93
    '''
    def register_user(self, postdata):
        log.debug('')
        time_start = datetime.datetime.utcnow()

        # start process
        #

        success = "true"
        detail = "success register user"

        success,detail = self.validator(postdata)
        
        if success == 'true':
            full_name = postdata["name_th"] + " " + postdata["surname_th"]
            r = httprequestObj.http_get(self.primary_domain+'/users',verify=False)
            soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
            authenticity_token = soup.find('input',{'name':'authenticity_token'})['value']
            
            datapost = {
                "authenticity_token": authenticity_token,
                "commit": "สมัครสมาชิก",
                "user[email]": postdata['user'],
                "user[email_notice]": 0,
                "user[email_notice]": 1,
                "user[member_type]": 1,
                "user[name]": full_name,
                "user[password]": postdata['pass'],
                "user[password_confirmation]":postdata['pass'],
                "user[telephone]": postdata["tel"],
                "utf8": "✓"
            }
            r = httprequestObj.http_post(self.primary_domain + '/users', data=datapost)
            #f = open("debug_response/resregister.html", "wb")
            #f.write(r.text.encode('utf-8').strip())      
            if re.search(r'กรุณาตรวจดูปัญหาที่ด้านล่าง', r.text) != None:
                success = 'false'
                if re.search(r'สั้นเกินไป', r.text) != None:
                    detail = 'passwd สั้นเกินไป (ต้องยาวกว่า 8 ตัวอักษร)'
                elif re.search(r'ถูกใช้ไปแล้ว',r.text) != None:
                    detail = 'email ถูกใช้ไปแล้ว'
                else:
                    detail = 'register error'
            elif re.search(r'เราได้ส่งลิงค์',r.text) != None:
                detail = 'เราได้ส่งลิงค์ คำยืนยันไปยังอีเมล์ของคุณ'
        
        #
        # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "websitename": self.websitename,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "ds_id": postdata['ds_id']
        }
    
    def validator(self,postdata):
        log.debug('')

        #TODO handle keyerror https://realpython.com/python-keyerror/

        success = 'true'
        detail = ''

        for key, val in postdata.items():
            if val == '':
                postdata[key] = None

        if postdata['user'] == None:
            detail = detail + ' ' + 'user not defined'
        
        if postdata['pass'] == None:
            detail = detail + ' ' + 'pass not defined'
        
        if postdata['ds_id'] == None:
            detail = detail + ' ' + 'ds_id not defined'
        
        if postdata['action'] == 'register_user':
            if (postdata['name_th'] == None and postdata['surname_th'] == None) and (postdata['name_en'] == None and postdata['surname_en'] == None):
                detail = detail + ' ' + 'name,surname not defined'
            if postdata['tel'] == None or re.search(r'0\d{9}', postdata['tel']) == None or len(str(postdata['tel'])) > 10:
                detail = detail + ' ' + 'tel number invalid'
        
        if postdata['action'] == 'create_post' or postdata['action'] == 'edit_post':
            if postdata['post_title_th'] == None:
                detail = detail + ' ' + 'project name not defined'
            if postdata['property_type'] != 1 and postdata['property_type'] != 7:
                detail = detail + ' ' + 'allow only condo and apartment'
            if postdata['addr_province'] == None:
                detail = detail + ' ' + 'addr_province not defined'
            if postdata['addr_district'] == None:
                detail = detail + ' ' + 'addr_district not defined'
            if postdata['addr_sub_district'] == None:
                detail = detail + ' ' + 'addr_sub_district not defined'
            if postdata['property_type'] == 7 and postdata.get('addr_number',None) == None: #apartment required arr_number
                detail = detail + ' ' + 'apartment required arr_number'
            if postdata['name'] == None:
                detail = detail + ' ' + 'name not defined'
            if postdata['mobile'] == None:
                detail = detail + ' ' + 'mobile not defined'
            if postdata['email'] == None:
                detail = detail + ' ' + 'email not defined'
            if postdata['listing_type'] != 'เช่า':
                detail = detail + ' ' + 'allow only RENT' 


        if detail != "":
            success = 'false'
        
        return success,detail


    '''
    Method:    POST
    URL:    https://www.residences.in.th/users/sign_in
    Request Body:   authenticity_token=vndE2khGfIByWf1IkPZdqlcuUnDwfe4xv87ouKLY/jM=&commit=%E0%B9%80%E0%B8%82%E0%B9%89%E0%B8%B2%E0%B8%AA%E0%B8%B9%E0%B9%88%E0%B8%A3%E0%B8%B0%E0%B8%9A%E0%B8%9A&user%5Bemail%5D=amarin.ta@gmail.com&user%5Bpassword%5D=5k4kk3253434&user%5Bremember_me%5D=0&utf8=%E2%9C%93
    '''
    def test_login(self, postdata):
        log.debug('')
        time_start = datetime.datetime.utcnow()

        # start process
        #

        success = 'true'
        detail = ''

        success,detail = self.validator(postdata)

        if success == 'true':

            r = httprequestObj.http_get(self.primary_domain+'/users',verify=False)
            soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
            authenticity_token = soup.find('input',{'name':'authenticity_token'})['value']
            datapost = {
                "authenticity_token":authenticity_token,
                "commit":"เข้าสู่ระบบ",
                "user[email]":postdata['user'],
                "user[password]":postdata['pass'],
                "user[remember_me]":"0",
                "utf8":"✓"
            }

            r = httprequestObj.http_post(self.primary_domain + '/users/sign_in', data=datapost)
            if re.search(r'คุณได้ลงชื่อเข้าใช้สำเร็จแล้ว', r.text) == None:
                success = 'false'
                if re.search(r'อีเมล์หรือรหัสผ่าน', r.text) != None:
                    detail = 'email or password invalid'
                elif re.search(r'กรุณายืนยันบัญชีของคุณก่อน',r.text) != None:
                    detail = 'please confirm email before login'
                elif re.search(r'บัญชีของคุณถูกระงับการใช้งาน',r.text) != None:
                    detail = 'บัญชีของคุณถูกระงับการใช้งาน'
                else:
                    detail = 'login error'

        # end process
        #
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": self.websitename,
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "ds_id": postdata['ds_id']
        }

   

   

    def create_post(self, postdata):
        log.debug('')
        time_start = datetime.datetime.utcnow()

        # start process
        #
        success = "true"
        detail = ""
        postid = ""
        posturl = ""
        
        success,detail = self.validator(postdata)

        #login
        login = self.test_login(postdata)
        success = login['success']
        detail = login['detail']

        if success == 'true':
            #test verify by otp
            r = httprequestObj.http_get(self.primary_domain + '/apartments/new' ,verify=False)
            if re.search(r'ยืนยันเบอร์โทรศัพท์', r.text) != None:
                success = 'false'
                detail = 'ยังไม่ได้ยืนยัน OTP ที่ส่งให้ทางเบอร์โทรศัพท์'

        if success == 'true':
            #apartment
            if postdata['property_type'] == 7:
                success ,detail ,postid ,posturl = self.create_post_apartment(postdata)
            #condo
            else: #1
                self.create_post_condo(postdata)


        #check condo or apartment

        #
        # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": postdata['ds_id'],
            "post_url": posturl,
            "post_id": postid,
            "account_type": "null",
            "detail": detail,
            "websitename": self.websitename,
        }
    
    def getareaid(self,postdata,provinceoption):
        log.debug('')

        success = 'true'
        detail = ''

        soup = BeautifulSoup(provinceoption, self.parser, from_encoding='utf-8')

        try:
            #get province id
            postdata['provinceid'] = soup.find("select",{'id':'apartment_province_id'}).find("option",text=re.compile(postdata['addr_province']))['value']
            log.debug('province  %s id %s' ,str(postdata['addr_province']),str(postdata['provinceid']))

            #get district id 
            datapost = {str(postdata['provinceid']):''}
            r = httprequestObj.http_post(self.primary_domain+'/dynamic_amphurs/'+str(postdata['provinceid']), data=datapost)
            #f = open("debug_response/residencesprovince.html", "wb")
            #f.write(r.text.encode('utf-8').strip())
            postdata['districtid'] = re.search(r"attr\(\"value\", (\d+)\).text\(\'"+postdata['addr_district'], r.text).group(1)
            log.debug('district %s id %s',str(postdata['addr_district']),str(postdata['districtid']))

            #get subdistrict id
            datapost = {str(postdata['districtid']):''}
            r = httprequestObj.http_post(self.primary_domain+'/dynamic_districts/'+str(postdata['districtid']), data=datapost)
            #f = open("debug_response/residencesprovince.html", "wb")
            #f.write(r.text.encode('utf-8').strip())
            postdata['subdistrictid'] = re.search(r"attr\(\"value\",(\d+)\).text\(\'"+postdata['addr_sub_district'], r.text).group(1)
            log.debug('subdistrict %s id %s',str(postdata['addr_sub_district']),str(postdata['subdistrictid']))
        except:
            log.warning('cannot get province district subdistrict')
            detail = 'cannot get province district subdistrict'
            success = 'false'

        return success,detail,postdata
    
    def get_datapost_apartment_general(self,postdata):
        datapost = {
                'utf8': '✓',
                'apartment[name]': postdata['post_title_th'],
                'apartment[en_name]': postdata['post_title_en'],
                'apartment[apartment_type]': 0,
                'apartment[province_id]': postdata['provinceid'],
                'apartment[amphur_id]': postdata['districtid'],
                'apartment[district_id]': postdata['subdistrictid'],
                'ignore_reverse_district_id': 0,
                'apartment[postcode]': postdata.get('addr_postcode',''),
                'apartment[address]': postdata['addr_number'],
                'apartment[road]': postdata['addr_road'],
                'apartment[street]': postdata['addr_soi'],
                'apartment[latitude]': postdata['geo_latitude'],
                'apartment[longitude]': postdata['geo_longitude'],
                'apartment[gmaps_zoom]': '',
                'apartment[staff]': postdata['name'],
                'apartment[telephone]': postdata['mobile'],
                'apartment[en_telephone]': '' ,
                'apartment[email]': postdata['email'],
                'apartment[line_user_id]': postdata['line'],
                'apartment[facebook_url]': '' ,
                'apartment[description]': postdata['post_description_th'],
                '_wysihtml5_mode': 1,
                'apartment[en_description]': postdata['post_description_en'],
                '_wysihtml5_mode': 1,
        }

        return datapost
    
    def uploadimage(self,postdata,token,newrelic,url,content):
        log.debug('')

        url = url.replace("amenities", "")

        #delete if has old image
        if len(postdata['post_images']) > 0:
            soup = BeautifulSoup(content, self.parser, from_encoding='utf-8')
            oldimage = soup.find_all("li",id=re.compile('image_'))
            for image in oldimage:
                imageid = image['id']
                imageid = imageid.replace("image_", "")
                deleteurl = url + '/images/' + str(imageid)
                datapost = {
                    '_method': 'delete',
                    'authenticity_token': token
                }
                r = httprequestObj.http_post(
                deleteurl,
                data=datapost,
                )
                log.debug('deleted image %s',str(image['id']))


        #add
        uploadurl = url
        imgcount = len(postdata['post_images'])
        for i in range(imgcount):
            datapost = {
                'utf8': '✓',
                '_method': 'put',
                'authenticity_token': str(token),
                'apartment[facility_ids][]': '',
                'apartment[central_facility_ids][]': '',
                'do_not_validation_all_facility': '0',
                'do_not_validation_listing_images': '0',
                'apartment[create_level]': '2',
                'ref_action': 'amenities',
                'apartment[images_attributes][][attachment]': ( str(i+1) + '.jpg', open(os.path.abspath(postdata['post_images'][i]), 'rb'), 'image/jpeg'),
            }

            encoder = MultipartEncoder(fields=datapost)
            headers = {
                'x-csrf-token': token,
                'x-newrelic-id': newrelic,
                'Content-Type': encoder.content_type
            }
            r = httprequestObj.http_post(
            uploadurl,
            data=encoder,
            headers=headers
            )
            if re.search(r'id=\"image_\d+\"',r.text) != None:
                log.debug('image upload id %s',re.search(r'id=\"image_(\d+)\"',r.text).group(1))
            else:
                log.warning('upload image %s fail',str(i+1))

        return True
    
    def get_datapost_apartment_amenities(self):
        log.debug('')

        datapost = {
            'utf8': '✓',
            '_method': 'put',
            'apartment[facility_ids][]': '',
            'apartment[central_facility_ids][]': '',
            'do_not_validation_all_facility': 1,
            'do_not_validation_listing_images': 0,
            'apartment[create_level]': 3,
            'ref_action': 'amenities',
        }

        return datapost
    
    def get_datapost_apartment_roomtype(self,postdata,content):
        log.debug('')

        soup = BeautifulSoup(content, self.parser, from_encoding='utf-8')
        roomattr = soup.find_all("input",id=re.compile('apartment_rooms_attributes_'))['id']
        attrcode = re.search(r'apartment_rooms_attributes_(\d+)_name',roomattr).group(1)

        datapost = {
            'utf8': '✓',
            '_method': 'put',
            'apartment[rooms_attributes]['+attrcode+'][name]': 'อพาร์ทเม้น',
            'apartment[rooms_attributes]['+attrcode+'][room_type]': 'R0',
            'apartment[rooms_attributes]['+attrcode+'][size]': postdata['floor_area'],
            'apartment[rooms_attributes]['+attrcode+'][monthly]': 0,
            'apartment[rooms_attributes]['+attrcode+'][monthly]': 1,
            'apartment[rooms_attributes]['+attrcode+'][min_price_permonth]': postdata['price_baht'],
            'apartment[rooms_attributes]['+attrcode+'][max_price_permonth]': postdata['price_baht'],
            'apartment[rooms_attributes]['+attrcode+'][daily]': 0,
            'apartment[rooms_attributes]['+attrcode+'][min_price_perday]':'',
            'apartment[rooms_attributes]['+attrcode+'][max_price_perday]': '',
            'apartment[rooms_attributes]['+attrcode+'][available]': 0,
            'apartment[rooms_attributes]['+attrcode+'][_destroy]': 'false',
            'apartment[water_price]':'' ,
            'apartment[water_price_monthly_per_person]': '',
            'apartment[water_price_monthly_per_room]': '',
            'apartment[water_price_remark]': '',
            'apartment[water_price_type]': 6,
            'apartment[water_price_note]': '',
            'apartment[electric_price]': '',
            'apartment[electric_price_remark]': '',
            'apartment[electric_price_type]': 4,
            'apartment[electric_price_note]':'' ,
            'apartment[deposit_month]':'' ,
            'apartment[deposit_bath]': '',
            'apartment[deposit_type]': 4,
            'apartment[deposit]': '',
            'apartment[advance_fee_month]': '',
            'apartment[advance_fee_bath]': '',
            'apartment[advance_fee_type]': 4,
            'apartment[advance_fee]': '',
            'apartment[phone_price_minute]': '',
            'apartment[phone_price_minute_unit]': '',
            'apartment[phone_price_per_time]': '',
            'apartment[phone_price_type]': 4,
            'apartment[phone_price]': '',
            'apartment[internet_price_bath]': '',
            'apartment[internet_price_unit]': '',
            'apartment[internet_price_type]': 4,
            'apartment[internet_price]': '',
            'apartment[has_promotion]': 0,
            'apartment[promotion_start]':'' ,
            'apartment[promotion_end]': '',
            'apartment[promotion_description]': '',
            '_wysihtml5_mode': 1,
            'apartment[create_level]': 3,
            'ref_action': 'roomtypes',
        }

        return datapost

    def create_post_apartment(self, postdata):
        log.debug('')

       
        success = "true"
        detail = ""
        postid = ""
        posturl = ""

        r = httprequestObj.http_get(self.primary_domain + '/apartments/new' ,verify=False)
        soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
        authenticity_token = soup.find('input',{'name':'authenticity_token'})['value']
        success,detail,postdata = self.getareaid(postdata , r.text)

        if success == 'true':
            #general
            datapost = self.get_datapost_apartment_general(postdata)
            datapost['authenticity_token'] = authenticity_token
            datapost['apartment[create_level]'] = 1
            datapost['ref_action'] = 'new'
            r = httprequestObj.http_post(self.primary_domain + '/apartments', data=datapost)

            #image and amenities
            if re.search(r'amenities', r.url) == None:
                success = 'false'
                detail = 'cannot post in general wizard'

            if success == 'true':
                postid = re.search(r'residences\.in\.th\/apartments\/(\d+)-', r.url).group(1)
                log.debug('postid %s',postid)
                soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
                authenticity_token = soup.find('input',{'name':'authenticity_token'})['value']
                newrelic = 'UA8CWVBUGwUHUlFVBAM='
                
                self.uploadimage(postdata,authenticity_token,newrelic,r.url,r.text)

                datapost = self.get_datapost_apartment_amenities()
                datapost['authenticity_token'] = authenticity_token
                posturl = r.url.replace("amenities", "")
                r = httprequestObj.http_post(posturl, data=datapost)
                #TODO
                if re.search(r'roomtypes', r.url) == None:
                    success = 'false'
                    detail = 'cannot post in image and amenities'
                
            if success == 'true':
                datapost = self.get_datapost_apartment_roomtype(postdata,r.text)
                datapost['authenticity_token'] = authenticity_token
                r = httprequestObj.http_post(posturl, data=datapost)
                if re.search(r'verify', r.url) == None:
                    success = 'false'
                    detail = 'cannot post in roomtype'
            
            if success == 'true':
                soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
                posturl = soup.find('a',{'class':'lightweight-line'})['href']
                posturl =  self.primary_domain+posturl          
    

        #
        # end process

        return success ,detail ,postid ,posturl

    def create_post_condo(self, postdata):
        log.debug('')
        time_start = datetime.datetime.utcnow()

        # start process
        #
        datahandled = self.postdata_handle(postdata)
        success = "true"
        detail = ""
        postid = ""

        #TODO 1 first post
        datapost = {            
            "utf8": "✓",
            "authenticity_token": "dv4lzOLDo4iu5i5xNGKn0AITatN9pHDAv3YUk10gA8Q=",
            "listing": {
                "title": "title thai",
                "title_en": "title eng",
                "listing_project_id": "14",
                "post_type": "1",
                "remark": "",
                "title_deed": "0",
                "room_type": "3",
                "no_of_bedroom": "2",
                "no_of_bathroom": "1",
                "room_area": "11",
                "floor": "11",
                "building": "",
                "home_address": "111",
                "room_no": "111",
                "furnishing": "3",
                "parking_spaces": "2",
                "facing_direction": "n",
                "facility_ids": [
                "14",
                "3",
                "4"
                ],
                "rent_availability_status": "1",
                "rental_price_type": "1",
                "rent_price": "10000",
                "daily_rental_price": "",
                "daily_rental_price_type": "2",
                "deposit_month": "",
                "deposit_bath": "",
                "rental_deposit_type": "4",
                "advance_fee_month": "",
                "advance_fee_bath": "",
                "advance_fee_type": "4",
                "common_service_fee_bath": "",
                "common_service_fee_type": "3",
                "detail": "detail thai",
                "detail_en": "detail eng",
                "contact_person": "amarin boonkirt",
                "line_user_id": "amarin.ta",
                "phone": "0891999450",
                "email": "amarin.ta@gmail.com",
                "create_level": "1"
            },
            "_wysihtml5_mode": "1",
            "ref_action": "new",
            "commit": "สร้างประกาศและดำเนินการต่อ"
        }

        
        r = httprequestObj.http_post(self.primary_domain + '/listings', data=datapost)
        data = r.text

        #TODO 2 edit https://www.residences.in.th/listings/31157-title-thai/images
        # รูปภาพที่พัก
        # ajax post image

        datapost = {
            "utf8": "✓",
            "_method": "put",
            "authenticity_token": "dv4lzOLDo4iu5i5xNGKn0AITatN9pHDAv3YUk10gA8Q=",
            "do_not_validation_listing_images": "0",
            "accepted": {
                "term_and_condition": "1"
            },
            "listing": {
                "create_level": "2"
            },
            "ref_action": "images"
        }
        
        r = httprequestObj.http_post(self.primary_domain + '/listings/31157-title-thai', data=datapost)
        data = r.text

        # if datahandled['web_project_name'] != '' , MUST use datahandled['web_project_name']

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
            "post_url": "https://www.ddproperty.com/preview-listing/"+post_id if post_id != "" else "",
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
        }        

    # not have boost post , use edit_post
    def boost_post(self, postdata):
        log.debug('')
        time_start = datetime.datetime.utcnow()

        # start process
        #
        datahandled = self.postdata_handle(postdata)
        success = "true"
        detail = ""
        post_id = ""
        log_id = ""

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
            "post_id": post_id,
        }
        
    def boost_post_apartment(self, postdata):
        log.debug('')
        time_start = datetime.datetime.utcnow()

        # start process
        #
        datahandled = self.postdata_handle(postdata)
        success = "true"
        detail = ""
        post_id = ""
        log_id = ""

        # action="/apartments/114489/moveon"

        datapost = {
            "utf8": "✓",
            "authenticity_token": "dv4lzOLDo4iu5i5xNGKn0AITatN9pHDAv3YUk10gA8Q=",
            "commit": "เลื่อนตำแหน่ง"
        }

        r = httprequestObj.http_post(self.primary_domain + '/apartments/' + post_id + '/moveon', data=datapost)
        data = r.text

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
            "post_id": post_id,
        }      

    #TODO ยังไม่ได้ทำ
    def boost_post_condo(self, postdata):
        log.debug('')
        time_start = datetime.datetime.utcnow()

        # start process
        #
        datahandled = self.postdata_handle(postdata)
        success = "true"
        detail = ""
        post_id = ""
        log_id = ""

        # action="/apartments/114489/moveon"

        datapost = {
            "utf8": "✓",
            "authenticity_token": "dv4lzOLDo4iu5i5xNGKn0AITatN9pHDAv3YUk10gA8Q=",
            "commit": "เลื่อนตำแหน่ง"
        }

        r = httprequestObj.http_post(self.primary_domain + '/apartments/' + post_id + '/moveon', data=datapost)
        data = r.text

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
            "post_id": post_id,
        }    

    def delete_post(self, postdata):
        log.debug('')
        time_start = datetime.datetime.utcnow()

        # start process
        #
        datahandled = self.postdata_handle(postdata)
        success = "true"
        detail = ""
        log_id = ""

        datapost = {
            "_method": "delete",
            "authenticity_token": "dv4lzOLDo4iu5i5xNGKn0AITatN9pHDAv3YUk10gA8Q="
        }
        
        r = httprequestObj.http_post(self.primary_domain + '/apartments/114489-%E0%B9%83%E0%B8%AB%E0%B9%89%E0%B9%80%E0%B8%8A%E0%B9%88%E0%B8%B2-%E0%B8%84%E0%B8%AD%E0%B8%99%E0%B9%82%E0%B8%94-watermark-%E0%B9%80%E0%B8%88%E0%B9%89%E0%B8%B2%E0%B8%9E%E0%B8%A3%E0%B8%B0%E0%B8%A2%E0%B8%B2%E0%B8%A3%E0%B8%B4%E0%B9%80%E0%B8%A7%E0%B8%A7%E0%B8%AD%E0%B8%AD%E0%B8%A3%E0%B9%8C-105-%E0%B8%95%E0%B8%A3%E0%B8%A1-2-%E0%B8%99%E0%B8%AD%E0%B8%99-2', data=datapost)
        data = r.text
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
        }

    def edit_post(self, postdata):
        log.debug('')
        time_start = datetime.datetime.utcnow()

        # start proces
        #
        datahandled = self.postdata_handle(postdata)
        success = "true"
        detail = ""
        log_id = ""

        post_id = ""
        datapost = {
            "data": {
                #"lat_lng": datahandled['geo_latitude'], datahandled['geo_longitude'],
                "post_type_code": datahandled['listing_type'],
                "property_type_code": datahandled['property_type'],
                "geo_id": "2",
                "province_id": "1",
                "amphur_id": "33",
                "district_id": "192",
                "subject": datahandled['post_title_th'],
                "price": datahandled['price_baht'],
                "description": datahandled['post_description_th'],
                "map_use": "1",
                "poster_name": datahandled['name'],
                "poster_telephone": datahandled['mobile'],
                "poster_email": datahandled['email'],
                "poster_lineid": "amarin.ta",
                "password": datahandled['pass']
            },
            "photos": {
                "name": [
                    "20200502124232_6821785ead08482d618.jpg"
                ],
                "angle": [
                    "0"
                ]
            }
        }
        
        r = httprequestObj.http_post(self.primary_domain + '/post/save/' + post_id + '/', data=datapost)
        data = r.text

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
            "log_id": log_id
        }
