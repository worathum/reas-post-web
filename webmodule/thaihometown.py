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

try:
    import configs
except ImportError:
    configs = {}
logging.config.dictConfig(getattr(configs, 'logging_config', {}))
log = logging.getLogger()


class thaihometown():

    name = 'thaihometown'

    def __init__(self):

        self.websitename = 'thaihometown'

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
            datahandled['listing_type'] = postdata['listing_type']
        except KeyError as e:
            datahandled['listing_type'] = "ประกาศขาย"
            log.warning(str(e))
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
            log.warning(str(e))
        if datahandled['property_type'] == '2' or datahandled['property_type'] == 2: #2 บ้านเดี่ยว
            datahandled['property_type'] = "บ้านเดี่ยว+Singlehouse"
        elif datahandled['property_type'] == '3' or datahandled['property_type'] == 3: #3 บ้านแฝด
            datahandled['property_type'] = "บ้าน+Home"
        elif datahandled['property_type'] == '4' or datahandled['property_type'] == 4: #4 ทาวน์เฮ้าส์
            datahandled['property_type'] = "ทาวน์เฮ้าส์+Townhouse"
        elif datahandled['property_type'] == '5' or datahandled['property_type'] == 5: #5 ตึกแถว-อาคารพาณิชย์
            datahandled['property_type'] = "อาคารพาณิชย์+Buildings"
        elif datahandled['property_type'] == '6' or datahandled['property_type'] == 6: #6 ที่ดิน
            datahandled['property_type'] = "ที่ดิน+Land"
        elif datahandled['property_type'] == '7' or datahandled['property_type'] == 7: #7 อพาร์ทเมนท์
            datahandled['property_type'] = "อพาร์ทเมนท์+Apartment"
        elif datahandled['property_type'] == '8' or datahandled['property_type'] == 8: #8 โรงแรม
            datahandled['property_type'] = "ธุรกิจ+Business"
        elif datahandled['property_type'] == '9' or datahandled['property_type'] == 9: #9 ออฟฟิศสำนักงาน
            datahandled['property_type'] = "สำนักงาน+Office"
        elif datahandled['property_type'] == '10' or datahandled['property_type'] == 10: #10 โกดัง
            datahandled['property_type'] = "โกดัง+Storehouse"
        elif datahandled['property_type'] == '25' or datahandled['property_type'] == 25: #25 โรงงาน
            datahandled['property_type'] = "โรงงาน+Factory"
        else:
            datahandled['property_type'] = "คอนโดมิเนียม+Condominiem" #1 คอนโด

        try:
            datahandled['post_img_url_lists'] = postdata['post_img_url_lists']
        except KeyError as e:
            datahandled['post_img_url_lists'] = {}
            log.warning(str(e))

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
            datahandled['floorarea_sqm'] = int(postdata['floorarea_sqm'])
        except KeyError as e:
            datahandled['floorarea_sqm'] = 0
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
            datahandled['land_size_rai'] = str(postdata["land_size_rai"])
        except KeyError as e:
            datahandled['land_size_rai'] = '0'
            log.warning(str(e))

        try:
            datahandled['land_size_ngan'] = str(postdata["land_size_ngan"])
        except KeyError as e:
            datahandled['land_size_ngan'] = '0'
            log.warning(str(e))

        try:
            datahandled['land_size_wa'] = str(postdata["land_size_wa"])
        except KeyError as e:
            datahandled['land_size_wa'] = '0'
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
            datahandled['addr_province'] = postdata['addr_province']
        except KeyError as e:
            datahandled['addr_province'] = ''
            log.warning(str(e))

        try:
            datahandled['addr_district'] = postdata['addr_district']
        except KeyError as e:
            datahandled['addr_district'] = ''
            log.warning(str(e))
        
        self.handled = True

        return datahandled

    def register_user(self, postdata):
        log.debug('')

        time_start = datetime.datetime.utcnow()

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
            firstname=name_th,
            mobile=tel,
        )
        r = httprequestObj.http_post('https://www.thaihometown.com/member/register', data=datapost)
        data = r.text
        # print (data)

        # if redirect to register page again
        if re.search('https://www.thaihometown.com/member/register', data):
            soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
            detail = soup.find('span').text
            success = "false"

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
        }

    def test_login(self, postdata):
        log.debug('')

        time_start = datetime.datetime.utcnow()

        # start process
        #
        datahandled = self.postdata_handle(postdata)
        user = datahandled['user']
        passwd = datahandled['pass']
        ds_name = "thaihometown"
        if (postdata["ds_name"]):
            ds_name = datahandled["ds_name"]
        ds_id = ""
        if (postdata["ds_id"]):
            ds_id = datahandled["ds_id"]
        
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
        log.debug('post login')
        data = r.text
        # print(data)
        matchObj = re.search(r'member\/[0-9]+', data)
        if not matchObj:
            success = "false"
            detail = "cannot login"

        log.debug('login status %s', success)

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

    def validatedatapost(self,datahandled):
        log.debug('')

        success = 'true'
        detail = ''

        #validate
        if datahandled['addr_province'] == None or  datahandled['addr_province'] == '' or datahandled['addr_district'] == None or datahandled['addr_district'] =='':
            detail = "addr_province or addr_district not defined"
        if datahandled['property_type'] == '' or datahandled['property_type'] == None:
            detail = "property_type not defined"
        if datahandled['listing_type'] == None or datahandled['listing_type'] == '':
            detail = "listing_type not defined"
        if datahandled['property_type'] == 'บ้านเดี่ยว+Singlehouse' or datahandled['property_type'] == 'บ้าน+Home' or ordatahandled['property_type'] == 'ทาวน์เฮ้าส์+Townhouse' or datahandled['property_type'] == 'คอนโดมิเนียม+Condominiem':
            if  datahandled['bath_room'] == 0 or datahandled['bed_room'] == 0:
                detail = 'บ้าน คอนโด ทาวน์เฮ้าส์ จำนวนห้องนอน และห้องน้ำต้องใส่ข้อมูล'
        if len(datahandled['post_description_th']) < 200 or len(datahandled['post_description_th']) > 5000:
            detail = 'post_description_th between 200 - 5000'
        if len(datahandled['post_title_th']) > 250:
            detail = 'post_title_th must < 250'
        

        if detail != "":
            success = 'false'
        
        return success,detail


    def create_post(self, postdata):
        log.debug('')

        time_start = datetime.datetime.utcnow()

        # start process
        #
        datahandled = self.postdata_handle(postdata)
        listing_type = datahandled['listing_type']
        property_type = datahandled['property_type']
        post_images = datahandled['post_images']
        price_baht = datahandled['price_baht']
        addr_province = datahandled['addr_province']
        addr_district = datahandled['addr_district']
        addr_sub_district = datahandled['addr_sub_district']
        addr_road = datahandled['addr_road']
        addr_near_by = datahandled['addr_near_by']
        floorarea_sqm = datahandled['floorarea_sqm']
        property_id = datahandled['property_id']
        post_title_th = datahandled['post_title_th']
        post_description_th = datahandled['post_description_th']
        post_title_en = datahandled['post_title_en']
        post_description_en = datahandled['post_description_en']
        ds_id = postdata["ds_id"]

        success = "true"
        detail = ""
        post_id = ""

        success,detail = self.validatedatapost(datahandled)
            
        # login
        test_login = self.test_login(datahandled)
        success = test_login["success"]
        detail = test_login["detail"]

        if success == "true":
            r = httprequestObj.http_get('https://www.thaihometown.com/addnew', verify=False)
            data = r.text
            soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
            string2 = soup.find("input", {"name": "string2"})['value']
            string1 = string2
            dasd = soup.find("input", {"name": "dasd"})['value']
            sas_name = soup.find("input", {"name": "sas_name"})['value']
            email = soup.find("input", {"name": "email"})['value']
            code_edit = soup.find("input", {"name": "code_edit"})['value']
            firstname = soup.find("input", {"name": "firstname"})['value']
            mobile = soup.find("input", {"name": "mobile"})['value']
            date_signup = soup.find("input", {"name": "date_signup"})['value']

            # https://www.thaihometown.com/addcontacts
            datapost = dict(
                        ActionForm2='',
                        Submit='Active',
                        ad_title=post_description_th.encode('cp874', 'ignore'),
                        carpark='',
                        code_edit=code_edit,
                        conditioning='',
                        contact_code='',
                        dasd=dasd,
                        date_signup=date_signup,
                        email=email,
                        firstname=firstname,
                        headtitle=post_title_th.encode('cp874', 'ignore'),
                        id='',
                        info=[' ตกแต่งห้องนอน ', ' ตกแต่งห้องนั่งเล่น ', ' ปูพื้นเซรามิค ', ' เฟอร์นิเจอร์ ', ' ไมโครเวฟ ', ' ชุดรับแขก '],
                        mobile=mobile,
                        notprice=1,
                        price_unit='',
                        property_area=floorarea_sqm,
                        property_bts='',
                        property_city_2='',
                        property_city_bkk='ยานนาวา+Yannawa',
                        property_country_2='',
                        property_mrt='',
                        property_purple='',
                        property_sqm=1,
                        property_type='บ้าน+Home',
                        rent_price='',
                        room1=2,
                        room2=3,
                        sas_name=sas_name,
                        selling_price='',
                        string1=string1,
                        string2=string2,
                        type_forrent='',
                        typepart='ประกาศขาย',
                        typeunit='ต่อตร.ม'
                    )
            # print(datapost)
            r = httprequestObj.http_post('https://www.thaihometown.com/addcontacts', data=datapost)
            data = r.text
            # print(data)
            f = open("thihomepost.html", "wb")
            f.write(data.encode('utf-8').strip())

            matchObj = re.search(r'https:\/\/www.thaihometown.com\/edit\/[0-9]+', data)
            if not matchObj:
                success = "false"
                soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
                txtresponse = soup.find("font").text
                detail = unquote(txtresponse)
            else:
                post_id = re.search(r'https:\/\/www.thaihometown.com\/edit\/(\d+)', data).group(1)

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": ds_id,
            "post_url": "https://www.thaihometown.com/home/" + post_id if post_id != "" else "",
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
        }

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

            r = httprequestObj.http_get('https://www.thaihometown.com/edit/' + post_id, verify=False)
            data = r.text
            f = open("editpostthaihometown.html", "wb")
            f.write(data.encode('utf-8').strip())

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
                f = open("boostthaihometown.html", "wb")
                f.write(data.encode('utf-8').strip())

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
        return {"success": success, "usage_time": str(time_usage), "start_time": str(time_start), "end_time": str(time_end), "detail": detail, "log_id": log_id, "post_id": post_id}

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

            r = httprequestObj.http_get('https://www.thaihometown.com/edit/' + post_id, verify=False)
            data = r.text
            # f = open("editpostthaihometown.html", "wb")
            # f.write(data.encode('utf-8').strip())

            # check respone py post id
            matchObj = re.search(r'' + post_id + '', data)
            if not matchObj:
                success = "false"
                detail = "not found this post_id " + post_id

            if success == "true":
                soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')

                sas_name = soup.find("input", {"name": "sas_name"})['value']
                #headtitle = soup.find("textarea", {"name": "headtitle"}).contents
                #headtitle = headtitle[0]

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

                    # headtitle2='888888',  # post_title_th.encode('cp874', 'ignore')
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
                    typeunit5='')

                r = httprequestObj.http_post('https://www.thaihometown.com/editcontacts', data=datapost)
                data = r.text
                f = open("editpostthaihometown.html", "wb")
                f.write(data.encode('utf-8').strip())

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
        return {"success": success, "usage_time": str(time_usage), "start_time": str(time_start), "end_time": str(time_end), "detail": detail, "log_id": log_id, "post_id": post_id}
