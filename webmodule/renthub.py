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


httprequestObj = lib_httprequest()


class renthub():

    name = 'renthub'

    def __init__(self):

        self.websitename = 'renthub'

        try:
            import configs
        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.debug = 0
        self.debugresdata = 0
        self.parser = 'html.parser'

    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']
        company_name = postdata['company_name']
        name_title = postdata["name_title"]
        name_th = postdata["name_th"]
        surname_th = postdata["surname_th"]
        name_en = postdata["name_en"]
        surname_en = postdata["surname_en"]
        tel = postdata["tel"]
        line: postdata["amarin.ta"]
        addr_province = postdata["addr_province"]

        # start process
        #
        success = "true"
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
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']
        ds_name = "renthub"
        if (postdata["ds_name"]):
            ds_name = postdata["ds_name"]
        ds_id = ""
        if (postdata["ds_id"]):
            ds_id = postdata["ds_id"]

        # start process
        #

        # clear session

        success = "true"
        detail = ""

        r = httprequestObj.http_get('https://www.renthub.in.th/login', verify=False)
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

        r = httprequestObj.http_post('https://www.renthub.in.th/login', data=datapost)
        data = r.text
        #f = open("renthub.html", "wb")
        #f.write(data.encode('utf-8').strip())

        matchObj = re.search(r'ประกาศของคุณ', data)
        if not matchObj:
            success = "false"
            detail = "cannot login"

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

    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        listing_type = postdata['listing_type']
        property_type = postdata['property_type']
        post_img_url_lists = postdata['post_img_url_lists']
        price_baht = postdata['price_baht']
        addr_province = postdata['addr_province']
        addr_district = postdata['addr_district']
        addr_sub_district = postdata['addr_sub_district']
        addr_road = postdata['addr_road']
        addr_near_by = postdata['addr_near_by']
        floorarea_sqm = postdata['floorarea_sqm']
        geo_latitude = postdata['geo_latitude']
        geo_longitude = postdata['geo_longitude']
        property_id = postdata['property_id']
        post_title_th = postdata['post_title_th']
        post_description_th = postdata['post_description_th']
        post_title_en = postdata['post_title_en']
        post_description_en = postdata['post_description_en']
        ds_id = postdata["ds_id"]
        user = postdata['user']
        passwd = postdata['pass']
        name = postdata['name']
        mobile = postdata['mobile']
        email = postdata['email']
        line = postdata['line']

        # start process
        #
        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""

        if success == "true":
            r = httprequestObj.http_get('https://renthub.in.th/condo_listings/new', verify=False)
            data = r.text
            soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
            authenticity_token = soup.find("input", {"name": "authenticity_token"})['value']

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
                'condo_listing[condo_project_id]': 1158,
                'condo_listing[contact_person]': name,
                'condo_listing[detail]': '<div>' + post_description_th + '<div>',
                'condo_listing[email]': user,  # email,
                'condo_listing[phone[0]]': mobile,
                'condo_listing[post_type]': 2,
                'condo_listing[title]': post_title_th,
                'english[detail]': '<div>' + post_description_en + '<div>',
                'english[title]': post_title_en,
                'rental[advance_fee_bath]': '',
                'rental[advance_fee_month]': 0,
                'rental[advance_fee_type]': 1,
                'rental[daily_price_type]': 2,
                'rental[deposit_bath]': '',
                'rental[deposit_month]': 0,
                'rental[deposit_type]': 1,
                'rental[min_daily_rental_price]': '',
                'rental[min_rental_price]': 5000,
                'rental[price_type]': 1,
                'room_information[building]': '',
                'room_information[direction]': 'East',
                'room_information[no_of_bath]': 1,
                'room_information[no_of_bed]': 1,
                'room_information[on_floor]': 44,
                'room_information[remark]': '',
                'room_information[room_area]': 22,
                'room_information[room_home_address]': 55,
                'room_information[room_no]': 55,
                'room_information[room_type]': 1,
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
                'temp[nopicture]': 1,
                'temp[picture_order]': '',
                'temp[room_no_picture_id_input]': '',
                'utf8': '✓'
            }
            # print(datapost)
            r = httprequestObj.http_post('https://renthub.in.th/condo_listings', data=datapost)
            data = r.text
            # print(data)
            f = open("renthubpost.html", "wb")
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
            "post_url": "https://www.thaihometown.com/home/"+post_id if post_id != "" else "",
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
        }

    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
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
            f = open("editpostthaihometown.html", "wb")
            f.write(data.encode('utf-8').strip())

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
                f = open("boostthaihometown.html", "wb")
                f.write(data.encode('utf-8').strip())

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
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
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
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
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
                f = open("editpostthaihometown.html", "wb")
                f.write(data.encode('utf-8').strip())

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

    def print_debug(self, msg):
        if(self.debug == 1):
            print(msg)
        return True

    def print_debug_data(self, data):
        if(self.debugdata == 1):
            print(data)
        return True
