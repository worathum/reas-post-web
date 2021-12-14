from .lib_httprequest import *
from bs4 import BeautifulSoup
import datetime
import sys
import json

'''
    bug post web, may be use selenium is work? 13/12/2021 PIK
'''

class genie_property():

    name = 'genie_property'

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
        self.webname = 'genie_property'

    def print_debug(self, msg):
        if self.debug == 1:
            print(msg)
        return True


    # Error 401
    # def logout_user(self, postdata):

    #     url = "https://www.genie-property.com/api/logout?mode=production"
    #     r = self.httprequestObj.http_post(url, data=postdata)
    #     print("function [logout_user]")
    #     print(r.status_code)

    def register_details(self, postdata):
        register_data = {}

        
        register_data["first_name"] = postdata["name_en"]
        register_data["last_name"] = postdata["surname_en"]
        register_data["phone"] = postdata["tel"]
        register_data["email"] = postdata["user"]
        register_data["password"] = postdata["pass"]
        register_data["role"] = "seller"
        register_data["company"] = postdata["company_name"]

        return register_data

    def register_user(self, postdata):

        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        # start process
        #
        data_register = self.register_details(postdata)


        res = self.httprequestObj.http_post_with_headers('https://www.genie-property.com/api/signup?mode=production', data=data_register)
        print(res.status_code)
        try:
            res_j = res.json()
        except:
            res_j = {}
            res_j['message'] = '' 

        # print(res.text)
        # with open("debug_response/genie_property.txt", "w") as file:
        #     file.write(res.text)


        detail = ""
        register_success = False
        if res_j['message'] == "The given data was invalid.":
            register_success = False
        else:
            test_login = self.test_login(postdata)
            if test_login['success'] == False:
                register_success = False
            else:
                register_success = True


        # 
        # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "genie_property",
            "success": register_success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
        }

    def test_login(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()


        url = "https://www.genie-property.com/api/signin?mode=production"
        data_login = {
            'email' : postdata['user'],
            'password' : postdata['pass']
        }


        r = self.httprequestObj.http_put_json(url, data=data_login)
        print(r.status_code)
        try:
            res = r.json()
            res_profile = res['profile']
        except:
            res = {}
            res_profile = {}
            res_profile['id'] = False
            res_profile['account_id'] = False
            res['success'] = False

        detail = ""
        success = False
        if res['success'] == True:
            success = True
     

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": postdata['ds_id'],
            "detail": detail,
            "websitename": self.webname,
            "id": res_profile['id'],
            "account_id": res_profile['account_id']
        }



    def data_details(self, postdata, user_id, account_id):

        form_post = {
                    "th_desc_value":"testtest",
                    "en_desc_value":"testtest",
                    "bathrooms":"2",
                    "bedrooms":"2",
                    "type":"house", # condo, house, towmhouse
                    "land_size":"50",
                    "interior_size":"50",
                    "account_id":str(account_id),
                    "price_sale":"3000",
                    "price_rent":"",
                    "down_payment":"",
                    "reference":"",
                    "cars":"",
                    "user_id": user_id,
                    "storeys":"11",
                    "is_exclusive":False,
                    "is_hot_deal":False,
                    "status":"draft",
                    "formType":"general"
                        }

        translations = [
            {
                    "field":"title",
                    "language":"th",
                    "content":"xxx"
                },
                {
                    "field":"title",
                    "language":"en",
                    "content":"xxx"
                },
                {
                    "field":"highlight",
                    "language":"en",
                    "content":""
                },
                {
                    "field":"highlight",
                    "language":"th",
                    "content":""
                },
                {
                    "field":"desc",
                    "language":"en",
                    "content":"<p>xxx</p>\n"
                },
                {
                    "field":"desc",
                    "language":"th",
                    "content":"<p>xxx</p>\n"
                }
        ]
        
        put_location = {
                    "unit_number":"119/251",
                    "building":"",
                    "floor":"",
                    "street_address":"119/251 ซ.สายไหม",
                    "project_id":"",
                    "location_uids":[1000000073],
                    "type":"house",
                    "map_address":"Soi Sai Mai 15, Khwaeng Sai Mai, Khet Sai Mai, Krung Thep Maha Nakhon 10220, Thailand",
                    "gps_lat":13.9259609,
                    "gps_lon":100.6444385,
                    "formType":"location"
        }

        put_facilities = {
                    "formType":"feature",
                    "featureIds":[
                                  # Facilities
                                  1,2,3,4,5,6,7,
                                  8,9,10,11,12,13,
                                  14,15,16,
                                  # Common area
                                  17,18,19,20,21,22,
                                  23,24,25,26,27,28,29,
                                  30,31,32,33,34,35,
                                  36,37,38,39,40,41,
                                  42,43,44,45,46,47,48,
                                  49,50
                    ]
        }

        

        for items in translations:
            if items['language'] == 'th':
                if items['field'] == 'title':
                    items['content'] = postdata['post_title_th']
                if items['field'] == 'highlight':
                    items['content'] = postdata['short_post_title_th']
                if items['field'] == 'desc':
                    items['content'] = postdata['post_description_th']
            if items['language'] == 'en':
                if items['field'] == 'title':
                    items['content'] = postdata['post_title_en']
                if items['field'] == 'highlight':
                    items['content'] = postdata['short_post_title_en']
                if items['field'] == 'desc':
                    items['content'] = postdata['post_description_en']
        
        
        form_post["th_desc_value"] = postdata["post_description_th"]
        form_post["en_desc_value"] = postdata["post_description_en"]
        form_post["bathrooms"] = postdata["bath_room"]
        form_post["bedrooms"] = postdata["bed_room"]
        form_post["type"] = postdata["property_type"] # condo, house, towmhouse
        form_post["land_size"] = postdata["land_size_wa"]
        form_post["interior_size"] = postdata["land_size_wa"]
        form_post["price_sale"] = postdata["price_baht"]
        form_post["price_rent"] = "0"
        form_post["reference"] = postdata["property_id"]
        form_post["down_payment"] = "0"
        form_post["cars"] = "1"
        form_post["translations"] = translations

        
        return form_post

    def create_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success_login = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""
        account_type = "normal"


        # start process
        #
        
        
        url = 'https://www.genie-property.com/api/properties?mode=production'
        
        if success_login:
            if 'web_project_name' not in postdata or postdata['web_project_name'] is None:
                if 'project_name' in postdata and postdata['project_name'] is not None:
                    postdata['web_project_name'] = postdata['project_name']
                else:
                    postdata['web_project_name'] = postdata['post_title_th']
            
            
            payload = self.data_details(postdata, test_login['id'], test_login['account_id'])
            data = json.dumps(payload)


            r = self.httprequestObj.http_post(url, data=data)
            status = r.status_code
            print(r.encoding)
            print(status)

            #
            # end process

            success = False
            if status == 200:
                success = True
            else:
                success = False


        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": "xxx",
            "post_url": post_url,
            "post_id": post_id,
            "account_type": account_type,
            "detail": detail,
            "websitename": self.webname
        }
            

            
    
