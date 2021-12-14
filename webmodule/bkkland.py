from .lib_httprequest import *
from bs4 import BeautifulSoup
import datetime
import sys
import json

with open("./static/bkkland_province.json",encoding = 'utf-8') as f:
    provincedata = json.load(f)

class bkkland():

    name = 'bkkland'

    def __init__(self):

        try:
            import configs

        except ImportError:
            configs = {}

        self.httprequestObj = lib_httprequest()
        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.debug = 1
        self.debugresdata = 0
        self.parser = 'html.parser'
        self.webname = 'bkkland'

    def print_debug(self, msg):
        if self.debug == 1:
            print(msg)
        return True


    def logout_user(self):
        url = "http://www.bkkland.com/auth/logout"
        self.httprequestObj.http_get(url)


    def test_login(self, postdata):

        self.logout_user
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        url = "http://www.bkkland.com/auth/login"
        data_login = {
            'f_login_email' : postdata['user'],
            'f_login_pass' : postdata['pass'],
            'process' : 'login'
        }

        # start process
        #
        
        r = self.httprequestObj.http_post(url, data=data_login)
        print(r.status_code)

        r = self.httprequestObj.http_get("http://www.bkkland.com/member")
        print(r.status_code)

        detail = ""
        login_success = False
        soup_web = BeautifulSoup(r.content,'lxml')
        if soup_web:
            verify = soup_web.find("div", attrs={"class":"personal_info"}).text
            if postdata['user'] in verify.split():
                login_success = True
                

        # 
        # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": self.webname,
            "success": login_success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
        }

    def datapost_details(self, postdata):


        pd_condition = {
            '1': 'ขาย', #1 ขาย 
            '2': 'เช่า', #2 เช่า
            '3': 'ซื้อ', #3 ซื้อ
        }

        pd_properties = {
                '1': 'land', 
                '2': 'house', 
                '3': 'townhouse', 
                '4': 'building', 
                '5': 'condo', 
                '6': 'office', 
            }

        province_id = ''
        amphur_id = ''

        for (key, value) in provincedata.items():
            if type(value) is str and postdata['addr_province'].strip() in value.strip():
                province_id = key
                break

        for (key, value) in provincedata[province_id+"_province"].items():
                if postdata['addr_district'].strip() in value.strip() or value.strip() in postdata['addr_district'].strip():
                    amphur_id = key
                    break


        files = {
            'f_topic' : (None, postdata['post_title_th']),
            'f_condition' : (None, int(pd_condition[str(postdata['listing_type'])])),
            'f_typepost' : (None, int(pd_properties[str(postdata['property_type'])])),
            'f_province' : (None, int(pd_properties[str(postdata['addr_province'])])),
            'f_amphur' : (None, province_id),
            'f_district' : (None, amphur_id),
            'f_land_area' : (None, postdata['land_size_wa']),

        }

        return files
        

    def create_post(self, postdata):
        # http://www.bkkland.com/post/add ?? may be

        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        result =  {
            "success": test_login['success'],
            "usage_time": '',
            "start_time": str(start_time),
            "end_time": '',
            "post_url": '',
            "ds_id": str(postdata['ds_id']),
            "post_id": '',
            "account_type": "null",
            "detail": '',
            "websitename": self.name
        }

        payload = self.datapost_details(postdata)

        if test_login['success'] == "true":
            url = "http://www.bkkland.com/post/add"
            r = self.httprequestObj.http_post(url, data=payload)
            print(r.text)
            print(r.status_code)
    


