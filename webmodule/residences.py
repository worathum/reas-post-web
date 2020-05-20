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
            if postdata.get('addr_number',None) == None: #apartment/condo required arr_number
                detail = detail + ' ' + 'apartment/condo required arr_number'
            if postdata['name'] == None:
                detail = detail + ' ' + 'name not defined'
            if postdata['mobile'] == None:
                detail = detail + ' ' + 'mobile not defined'
            if postdata['email'] == None:
                detail = detail + ' ' + 'email not defined'
            if postdata['listing_type'] != 'เช่า':
                detail = detail + ' ' + 'allow only RENT' 
            #title is not len > 60
            if len(postdata['post_title_th']) > 60:
                postdata['post_title_th'] = postdata['post_title_th'][:60]
                log.debug('split post_title_th to %s',str(postdata['post_title_th']))
            if postdata['property_type'] == 1:
                if postdata.get('floor_level',None) == None or postdata.get('floor_level','') == '':
                    detail = detail + ' ' + 'allow only condo and apartment' 
            
            if postdata.get('name',None) == None or postdata.get('name','') == '':
                detail = detail + ' ' + 'name not defined'
            if postdata.get('mobile',None) == None or postdata.get('mobile','') == '':
                detail = detail + ' ' + 'mobile not defined'
        
        if postdata['action'] == 'edit_post':
            if postdata.get('post_id',None) == None or postdata.get('post_id','') == '':
                detail = 'post_id is not defined'

        #direction
        direction = postdata.get('direction_type',None)
        if direction == int(11):
            postdata['direction_type'] = 'n'
        elif direction == int(12):
            postdata['direction_type'] = 's'
        elif direction == int(13):
            postdata['direction_type'] = 'e'
        elif direction == int(14):
            postdata['direction_type'] = 'w'
        elif direction == int(21):
            postdata['direction_type'] = 'ne'
        elif direction == int(22):
            postdata['direction_type'] = 'se'
        elif direction == int(23):
            postdata['direction_type'] = 'nw'
        else: #24 ทิศตะวันตกเฉียงใต้
            postdata['direction_type'] = 'sw'

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

            #clear session
            r = httprequestObj.http_get(self.primary_domain+'/users/sign_out',verify=False)

            r = httprequestObj.http_get(self.primary_domain+'/users',verify=False)
            #f = open("debug_response/loginpage.html", "wb")
            #f.write(r.text.encode('utf-8').strip())
            if re.search(r'Not authorized as an administrator', r.text) != None:
                success = 'false'
                detail = 'web login page error please try again'
            if success == 'true':
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
                success ,detail ,postid ,posturl = self.create_post_condo(postdata)


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
                'apartment[en_description]': postdata['post_description_en'],
                '_wysihtml5_mode': 1,
        }

        return datapost
    
    def uploadimage_apartment(self,postdata,token,newrelic,url,content):
        log.debug('')

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
            #log.debug(r.text)
            if re.search(r'image_\d+',r.text) != None:
                log.debug('image upload id %s',re.search(r'(image_\d+)',r.text).group(1))
            else:
                log.warning('upload image %s fail',str(i+1))

        return True
    
    def uploadimage_condo(self,postdata,token,newrelic,url,content):
        log.debug('')

        #delete if has old image
        if len(postdata['post_images']) > 0:
            soup = BeautifulSoup(content, self.parser, from_encoding='utf-8')
            oldimage = soup.find_all("li",id=re.compile('photo_'))
            for image in oldimage:
                imageid = image['id']
                imageid = imageid.replace("photo_", "")
                deleteurl = self.primary_domain + '/photos/' + str(imageid)
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
                'do_not_validation_listing_images': '0',
                'accepted[term_and_condition]': '1', 
                'listing[create_level]': '2',
                'ref_action': 'images',
                'listing[photos_attributes][][attachment]': ( str(i+1) + '.jpg', open(os.path.abspath(postdata['post_images'][i]), 'rb'), 'image/jpeg'),
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
            if r.status_code == 200:
                log.debug('image uploaded  %s',str(i+1))
            else:
                log.warning('upload image %s fail',str(i+1))

        return True
    
    def get_datapost_apartment_amenities(self):
        log.debug('')

        datapost = {
            'utf8': '✓',
            '_method': 'put',
            'apartment[facility_ids][]': '',
            'apartment[facility_ids][]': 2,
            'apartment[central_facility_ids][]': '',
            'apartment[central_facility_ids][]': 12,
            'do_not_validation_all_facility': 1,
            'do_not_validation_listing_images': 0,
            'apartment[create_level]': 3,
            'ref_action': 'amenities',
        }

        return datapost
    
    def get_datapost_apartment_roomtype(self,postdata):
        log.debug('')

        # attrcode = int(datetime.datetime.now().timestamp()*1000)
        # attrcode = str(attrcode)

        datapost = {
            'utf8': '✓',
            '_method': 'put',
            'apartment[rooms_attributes][0][name]': 'อพาร์ทเม้น',
            'apartment[rooms_attributes][0][room_type]': 'R0',
            'apartment[rooms_attributes][0][size]': postdata['floor_area'],
            'apartment[rooms_attributes][0][monthly]': 1,
            'apartment[rooms_attributes][0][min_price_permonth]': postdata['price_baht'],
            'apartment[rooms_attributes][0][max_price_permonth]': postdata['price_baht'],
            'apartment[rooms_attributes][0][daily]': 0,
            'apartment[rooms_attributes][0][min_price_perday]':'',
            'apartment[rooms_attributes][0][max_price_perday]': '',
            'apartment[rooms_attributes][0][available]': 1,
            'apartment[rooms_attributes][0][_destroy]': 'false',
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
            'accepted[term_and_condition]': '1',
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
            # f = open("debug_response/postgeneral.html", "wb")
            # f.write(r.text.encode('utf-8').strip())
            if re.search(r'amenities', r.url) == None:
                success = 'false'
                detail = 'cannot post in general wizard'
                if re.search(r'กรุณาคลิกเครื่องหมายถูกในช่อง',r.text) != None:
                    detail = 'cannot post in general wizard '+ '(google anti captcha block)'

            #image and amenities
            if success == 'true':
                postid = re.search(r'residences\.in\.th\/apartments\/(\d+)-', r.url).group(1)
                log.debug('postid %s',postid)
                soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
                authenticity_token = soup.find('input',{'name':'authenticity_token'})['value']
                newrelic = 'UA8CWVBUGwUHUlFVBAM='
                posturl = r.url.replace("/amenities", "")
                self.uploadimage_apartment(postdata,authenticity_token,newrelic,posturl,r.text)
                datapost = self.get_datapost_apartment_amenities()
                datapost['authenticity_token'] = authenticity_token
                r = httprequestObj.http_post(posturl, data=datapost)
                r = httprequestObj.http_get(posturl + '/roomtypes' ,verify=False)
                #f = open("debug_response/residentroomtype.html", "wb")
                #f.write(r.text.encode('utf-8').strip())
                if re.search(r'roomtypes', r.url) == None:
                    success = 'false'
                    detail = 'cannot post in image and amenities'
                
            if success == 'true':
                soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
                authenticity_token = soup.find('input',{'name':'authenticity_token'})['value']
                #TODO อาจจะต้องใช้ตอน edit apartment[rooms_attributes][0][id]: 17853
                datapost = self.get_datapost_apartment_roomtype(postdata)
                datapost['authenticity_token'] = authenticity_token
                datapost['accepted[term_and_condition]'] = '1'
                r = httprequestObj.http_post(posturl, data=datapost)       
                r = httprequestObj.http_get(posturl + '/verify' ,verify=False)
                if re.search(r'verify', r.url) == None:
                    success = 'false'
                    detail = 'cannot post in roomtype'
            
            if success == 'true':
                soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
                posturl = soup.find('a',{'class':'lightweight-line'})['href']
                posturl =  self.primary_domain+posturl          

            #TODO ยอมรับเงื่อนไขและลงประกาศ
        #
        # end process

        return success ,detail ,postid ,posturl
    
    def get_condo_listing_id(self,postdata):
        log.debug('')

        success = 'true'
        detail = ''

        listingname = postdata.get('project_name',None)
        if postdata.get('web_project_name',None) != None and postdata.get('web_project_name',None) != '':
            listingname = postdata.get('web_project_name',None)
        
        if listingname == None:
            success == "false"
            detail = 'projectname is not defined'
        
        if success == 'true':
            r = httprequestObj.http_get(self.primary_domain + '/listing_projects/searches.json?q='+str(listingname) ,verify=False)
            datajson = r.json()
            data = datajson['items']
            if len(data) < 1:
                success = 'false'
                detail = 'not found project name'
                log.warning('not found project name')
            else:
                postdata['project_id'] = data[0]['id']
                log.debug('project id %s',postdata['project_id'])
        
        return success,detail,postdata

    def get_datapost_condo_general(self,postdata):
        log.debug('')

        datapost = {
            'utf8': '✓',
            'listing[title]': postdata.get('post_title_th'),
            'listing[title_en]': postdata.get('post_title_en') ,
            'listing[listing_project_id]':postdata.get('project_id'),
            'listing[post_type]':1,
            'listing[remark]':'',
            'listing[title_deed]':0,
            'listing[room_type]':1,
            'listing[no_of_bedroom]':postdata.get('bed_room',1),
            'listing[no_of_bathroom]':postdata.get('bath_room',1),
            'listing[room_area]':float(postdata.get('floor_area',1)),
            'listing[floor]':postdata.get('floor_level'),
            'listing[building]':'',
            'listing[home_address]':postdata.get('addr_number'),
            'listing[room_no]':'',
            'listing[furnishing]':1,
            'listing[parking_spaces]':1,
            'listing[facing_direction]':postdata.get('direction_type'),
            'listing[facility_ids][]':2,
            'listing[rent_availability_status]':1,
            'listing[rental_price_type]':1,
            'listing[rent_price]':float(postdata.get('price_baht',1)),
            'listing[daily_rental_price]':'',
            'listing[daily_rental_price_type]':0,
            'listing[deposit_month]':'',
            'listing[deposit_bath]':'',
            'listing[rental_deposit_type]':4,
            'listing[advance_fee_month]':'',
            'listing[advance_fee_bath]':'',
            'listing[advance_fee_type]':4,
            'listing[common_service_fee_bath]':'',
            'listing[common_service_fee_type]':3,
            'listing[detail]':postdata.get('post_description_th',''),
            'listing[detail_en]': postdata.get('post_description_en',''),
            '_wysihtml5_mode': 1,
            'listing[contact_person]': postdata.get('name',''),
            'listing[line_user_id]': postdata.get('line',''),
            'listing[phone]': postdata.get('mobile',''),
            'listing[email]': postdata.get('email',''),
            'commit': 'สร้างประกาศและดำเนินการต่อ'
        }

        return datapost

    def get_datapost_condo_accept_term(self):
        datapost = {
            'utf8': '✓',
            '_method': 'put',
            'listing[photos_attributes][][attachment]': '(binary)',
            'do_not_validation_listing_images': '0',
            'accepted[term_and_condition]': '1',
            'listing[create_level]': '3',
            'ref_action': 'images',
        }

        return datapost

    def create_post_condo(self, postdata):
        log.debug('')

        success = "true"
        detail = ""
        postid = ""
        posturl = ""

        r = httprequestObj.http_get(self.primary_domain + '/listings/new' ,verify=False)
        soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
        authenticity_token = soup.find('input',{'name':'authenticity_token'})['value']
        
        success,detail,postdata = self.get_condo_listing_id(postdata)

        if success == 'true':
            datapost = self.get_datapost_condo_general(postdata)
            datapost['authenticity_token'] = authenticity_token
            datapost['ref_action'] = 'new'
            datapost['listing[create_level]'] = 1,
            r = httprequestObj.http_post(self.primary_domain + '/listings', data=datapost)
            if re.search(r'images', r.url) == None:
                success = 'false'
                detail = 'cannot post in general wizard'

            #image
            if success == 'true':
                postid = re.search(r'residences\.in\.th\/listings\/(\d+)-', r.url).group(1)
                log.debug('postid %s',postid)
                soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
                authenticity_token = soup.find('input',{'name':'authenticity_token'})['value']
                newrelic = 'UA8CWVBUGwUHUlFVBAM='
                posturl = r.url.replace("/images", "")
                self.uploadimage_condo(postdata,authenticity_token,newrelic,posturl,r.text)

            #accetp term and condition
            datapost = self.get_datapost_condo_accept_term()
            datapost['authenticity_token'] = authenticity_token
            r = httprequestObj.http_post(posturl, data=datapost)
            r = httprequestObj.http_get(posturl + '/verify' ,verify=False)
            if re.search(r'verify', r.url) == None:
                    success = 'false'
                    detail = 'cannot post condo images'
            
            #get post link
            if success == 'true':
                soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
                posturl = soup.find('a',{'class':'lightweight-line'})['href']
                posturl =  self.primary_domain+posturl
       
        return success ,detail ,postid ,posturl

    def boost_post(self, postdata):
        log.debug('')
        time_start = datetime.datetime.utcnow()

        # start process
        #
        success = "true"
        detail = ""
        
        success,detail = self.validator(postdata)

        if success == 'true':
            #login
            login = self.test_login(postdata)
            success = login['success']
            detail = login['detail']

        if success == 'true':
            #test post is condo or apartment
            success,detail,posttype,content = self.get_post_type(postdata)
        
        if success == 'true':
            if posttype == 'condo':
                success,detail = self.boost_post_condo(postdata,content)
            else:
                success,detail = self.boost_post_apartment(postdata,content)


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
            "log_id": postdata['log_id'],
            "websitename": self.websitename,
        }
        
    def boost_post_apartment(self, postdata,content):
        log.debug('')

        success = 'true'
        detail = ''
      
        soup = BeautifulSoup(content, self.parser, from_encoding='utf-8')
        authenticity_token = soup.find('meta',{'name':'csrf-token'})['content']
        posturl = self.primary_domain + '/apartments/' + postdata['post_id'] + '/moveon'
        #log.debug(posturl)
        datapost = {
            "utf8": "✓",
            "authenticity_token": authenticity_token,
            "commit": "เลื่อนตำแหน่ง"
        }

        r = httprequestObj.http_post(self.primary_domain + '/apartments/' + postdata['post_id'] + '/moveon', data=datapost)
        #f = open("debug_response/residentboost.html", "wb")
        #f.write(r.text.encode('utf-8').strip())
        if re.search(r'ได้ส่งคำสั่งเลื่อนอันดับเข้าระบบคิวแล้ว',r.text) == None:
            success = 'false'
            detail = 'cannot boost post'

        return success,detail

    def boost_post_condo(self, postdata,content):
        log.debug('')

        success = 'true'
        detail = ''

        soup = BeautifulSoup(content, self.parser, from_encoding='utf-8')
        authenticity_token = soup.find('meta',{'name':'csrf-token'})['content']
        posturl = soup.find('li',{'role':'presentation'}).find('a')['href']
        posturl = posturl.replace("/information", "/moveup")
        posturl = self.primary_domain + posturl
        #log.debug(posturl)
        datapost = {
            "utf8": "✓",
            "authenticity_token": authenticity_token,
            "commit": "เลื่อนตำแหน่ง"
        }

        r = httprequestObj.http_post(posturl, data=datapost)
        #f = open("debug_response/residentboost.html", "wb")
        #f.write(r.text.encode('utf-8').strip())
        if re.search(r'ได้ส่งคำสั่งเลื่อนอันดับเข้าระบบคิวแล้ว',r.text) == None:
            success = 'false'
            detail = 'cannot boost post'

        return success,detail

    def delete_post(self, postdata):
        log.debug('')
        time_start = datetime.datetime.utcnow()

        # start process
        #
        success = "true"
        detail = ""
        
        success,detail = self.validator(postdata)

        if success == 'true':
            #login
            login = self.test_login(postdata)
            success = login['success']
            detail = login['detail']

        if success == 'true':
            #test post is condo or apartment
            success,detail,posttype,content = self.get_post_type(postdata)
        
        if success == 'true':
            soup = BeautifulSoup(content, self.parser, from_encoding='utf-8')
            authenticity_token = soup.find('meta',{'name':'csrf-token'})['content']
            posturl = soup.find('li',{'role':'presentation'}).find('a')['href']
            posturl = posturl.replace("/information", "")
            posturl = self.primary_domain + posturl
            datapost = {
                '_method': 'delete',
                'authenticity_token': authenticity_token
            }
            r = httprequestObj.http_post(posturl, data=datapost)
            #f = open("debug_response/residentdelete.html", "wb")
            #f.write(r.text.encode('utf-8').strip())
            pid = postdata['post_id']
            if re.search(rf"{pid}",r.text) != None:
                success = 'false'
                detail = 'cannot delete post'

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
            "log_id": postdata['log_id'],
            "websitename": self.websitename,
        }

    def get_post_type(self,postdata):
        log.debug('')

        #test condo
        r = httprequestObj.http_get(self.primary_domain + '/listings/' + str(postdata['post_id']) + '/information',verify=False)
        if r.status_code == 200:
            log.debug('edit/boost/delete post type condo')
            return 'true','','condo',r.text
            
        
        #test apartment
        r = httprequestObj.http_get(self.primary_domain + '/apartments/' + str(postdata['post_id']) + '/information',verify=False)
        if r.status_code == 200:
            log.debug('edit/boost/delete post type apartment')
            return 'true','','apartment',r.text
        
        log.warning('not found post id %s',str(postdata['post_id']))
        return 'false','cannot found post by post_id','',''
        


    def edit_post(self, postdata):
        log.debug('')
        time_start = datetime.datetime.utcnow()

        # start process
        #
        success = "true"
        detail = ""
        
        success,detail = self.validator(postdata)

        #login
        login = self.test_login(postdata)
        success = login['success']
        detail = login['detail']

        if success == 'true':
            #test post is condo or apartment
            success,detail,posttype,content = self.get_post_type(postdata)
        
        if success == 'true':
            if posttype == 'condo':
                success,detail = self.edit_post_condo(postdata,content)
            else:
                success,detail = self.edit_post_apartment(postdata,content)


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
            "log_id": postdata['log_id'],
            "websitename": self.websitename,
        }
    
    def edit_post_condo(self,postdata,content):
        log.debug('')

        
        soup = BeautifulSoup(content, self.parser, from_encoding='utf-8')
        posturl = soup.find('li',{'role':'presentation'}).find('a')['href']
        posturl = self.primary_domain + posturl
        posturl = posturl.replace("/information", "")
        authenticity_token = soup.find('input',{'name':'authenticity_token'})['value']
        datapost = self.get_datapost_condo_general(postdata)
        datapost['authenticity_token'] = authenticity_token
        datapost['_method']= 'put'
        datapost['listing[create_level]']= 3
        datapost['ref_action']= 'information'

        #edit info
        r = httprequestObj.http_post(posturl, data=datapost)

        #upload image
        r = httprequestObj.http_get(posturl + '/images' ,verify=False)
        self.uploadimage_condo(postdata,authenticity_token,'UA8CWVBUGwUHUlFVBAM=',posturl,r.text)

        #confirm term
        datapost = self.get_datapost_condo_accept_term()
        r = httprequestObj.http_post(posturl, data=datapost)

        return 'true',''
    
    def edit_post_apartment(self,postdata,content):
        log.debug('')

        success = 'true'
        detail = ''

        soup = BeautifulSoup(content, self.parser, from_encoding='utf-8')
        success,detail,postdata = self.getareaid(postdata , content)
        posturl = soup.find('li',{'role':'presentation'}).find('a')['href']
        posturl = self.primary_domain + posturl
        posturl = posturl.replace("/information", "")
        authenticity_token = soup.find('input',{'name':'authenticity_token'})['value']
        datapost = self.get_datapost_apartment_general(postdata)
        datapost['_method']= 'put'
        datapost['authenticity_token'] = authenticity_token
        datapost['apartment[create_level]']= 4
        datapost['ref_action']= 'information'
        
        #post general
        r = httprequestObj.http_post(posturl, data=datapost)
        r = httprequestObj.http_get(posturl + '/amenities' ,verify=False)
        if re.search(r'amenities', r.url) == None:
            success = 'false'
            detail = 'cannot post in general wizard'
            if re.search(r'กรุณาคลิกเครื่องหมายถูกในช่อง',r.text) != None:
                detail = 'cannot post in general wizard '+ '(google anti captcha block)'

        #image and amenities
        if success == 'true':
            soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
            authenticity_token = soup.find('input',{'name':'authenticity_token'})['value']
            newrelic = 'UA8CWVBUGwUHUlFVBAM='
            self.uploadimage_apartment(postdata,authenticity_token,newrelic,posturl,r.text)
            datapost = self.get_datapost_apartment_amenities()
            datapost['authenticity_token'] = authenticity_token
            r = httprequestObj.http_post(posturl, data=datapost)
            r = httprequestObj.http_get(posturl + '/roomtypes' ,verify=False)
            #f = open("debug_response/residentroomtype.html", "wb")
            #f.write(r.text.encode('utf-8').strip())
            if re.search(r'roomtypes', r.url) == None:
                success = 'false'
                detail = 'cannot post in image and amenities'
            
        if success == 'true':
            soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
            authenticity_token = soup.find('input',{'name':'authenticity_token'})['value']
            datapost = self.get_datapost_apartment_roomtype(postdata)
            datapost['authenticity_token'] = authenticity_token
            datapost['accepted[term_and_condition]'] = '1'
            datapost['apartment[create_level]'] = 4
            roomid = soup.find('input',id=re.compile('apartment_rooms_attributes_0_id'))['value']
            log.debug(roomid)
            datapost['apartment[rooms_attributes][0][id]']: roomid
            #ต้องลบ งั้นจะกลายเป็นเพิ่ม ห้องพัก
            # del datapost['apartment[rooms_attributes][0][name]']
            # del datapost['apartment[rooms_attributes][0][room_type]']
            # del datapost['apartment[rooms_attributes][0][monthly]']
            # del datapost['apartment[rooms_attributes][0][daily]']
            # del datapost['apartment[rooms_attributes][0][min_price_perday]']
            # del datapost['apartment[rooms_attributes][0][max_price_perday]']
            # del datapost['apartment[rooms_attributes][0][available]']
            r = httprequestObj.http_post(posturl, data=datapost)       
  
        return success,detail