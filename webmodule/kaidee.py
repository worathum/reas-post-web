# -*- coding: utf-8 -*-

from requests.adapters import Response
from .lib_httprequest import *
from bs4 import BeautifulSoup
from .lib_captcha import *
import os.path
import re
import json
import datetime
import sys
import requests
from time import sleep
import cloudscraper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys

# 'listing_type': (category_id, [(attr_id, unit_id), (attr_id, unit_id), (attr_id, unit_id)] )
authorization = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI1IiwianRpIjoiOTA5ZmUwNTEzZjhiMGUwZmYzNmFlZTdhZjI3MjllNTI3MDBmYmQzYTkyMzI3MTFhMjU3NDY1MzQ3NDEzNTU4N2I1MjdmNTRjYTZjOThlZDYiLCJpYXQiOjE2MTMxMzkwMzIsIm5iZiI6MTYxMzEzOTAzMiwiZXhwIjoxOTI4NjcxODMyLCJzdWIiOiIiLCJzY29wZXMiOltdfQ.QV3bJInxMEs-arTC7KBdj_wCFAGiVlLbG98vo5g4Gqf0zq3PUjiolUWKJGyI5u_79PPhrq2u3O8R-i5jt-EF1kVvkiwXgWOgGJ9qAEGaxVlRTK_MiGiyeOO5DY9rYdrbZfQsrdZBUPBNDTgU7tVZD5QLpzw-FhHzGCqIReCkK_8gtBv308qtKzJs7VKp6mTYhdms6kXF3xIQYNUwVacOKTCB3ZpGCSR68ATvphX2ZMsXju9PI532NqKwyn5DaXODYi2X0eO4kVZW7VCbdjWTS9viJvRCLCMO_Jo0h5hEZqXyh1kc-Y6FeQ-yGvY5g00KCFR97CeuibO4RS0UkMMTNyTs3g_rbrTf6LF7L12ahAln_CjHHZoPSSrqkbAK_82JXuchcvDwHJzUpRaDKA_3dX8UIuoYsXmlPohyuxQ0KqIjOVTEBov0zemqBytPBYnYcYVTDD4dBAPRAR8X8zNCVaOTTiXIS7ykxCLssPBziy8r2_BGzTyrTlTbrazE4sUi17SLX1Na_XhxMSg_sG1nhQ94aK8cTk4lxSV2mSed-2vIZ02LqoeNX9alcSISdDW_vbfxVXGMLVeQX8ZaWj6ebybR0ok82b0jSHSPyKCN-uu_QZkUiUj4civ1RgaWpr2mxxdYx_VXpq5D_NL7OMwFwRc3wS8qufl2nwu9E6gQM7o'
categories_list = {                
    '1': (17, [(13, 8), (14, 35), (15, 36)] ),
    '2': (15, [(7, 1), (8, 31), (9, 32)] ),
    '3': (15, [(7, 1), (8, 31), (9, 32)] ),
    '4': (16, [(10, 4), (11, 33), (12, 34)] ),
    '5': (134, [] ),
    '6': (19, [(19, 13)] ),
    '7': (18, [(16, 10), (17, 37), (18, 38)] ),
    '8': (138, [(28, 25)] ),
    '9': (137, [(27, 22)] ),
    '10': (133, [(26, 19)] ),
    '25': (133, [(26, 19)] )
}

class kaidee():
    name = 'kaidee'
    site_name = "https://www.kaidee.com"
    api_name = "https://api.kaidee.com/0.18"

    def __init__(self):
        try:
            import configs
        except ImportError:
            configs = {}
        self.httprequestObj = lib_httprequest()
        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.debug = 0
        self.debugresdata = 0
        self.parser = 'html.parser'
        self.scraper = cloudscraper.create_scraper()
        self.options = Options()
        #self.options.add_argument("--headless")  # Runs Firefox in headless mode.
        self.options.add_argument('--no-sandbox')  # Bypass OS security model
        self.options.add_argument('start-maximized')
        self.options.add_argument('disable-infobars')
        self.options.add_argument("--disable-extensions")


    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        success = "false"
        detail = 'Registration not allowed as mobile number verification is required. Please register manually!'

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": self.name,
            "ds_id": postdata['ds_id']
        }

    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        success = False
        detail = 'An Error has Occurred'
        member_id = ''
        privateToken = ''

        datapost = {
            "email": postdata['user'],
            "password": postdata['pass']
        }
        count = 0
        while count<10:
            try:
                r = self.scraper.post('https://api.kaidee.com/0.18/member/login', data=json.dumps(datapost))
                response = r.json()
                break
            except:
                count+=1
        if count != 10:
            if r.status_code==200:
                if "member" in response:
                    success = True
                    detail = "Login Successful"
                    member_id = response["member"]["id"]
                    privateToken = response["member"]["privateToken"]
            else:
                if 'error' in response:
                    detail = response['error']['message']
                else:
                    detail = 'Status code: {}'.format(r.status_code)
        else:
            detail = 'Something wrong'

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
                "success": success,
                "usage_time": str(time_usage),
                "start_time": str(time_start),
                "end_time": str(time_end),
                "detail": detail,
                'member_id': member_id,
                "privateToken": privateToken,
                "websitename": self.name,
                "ds_id": postdata['ds_id'],
            }

    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = "Unable to create post"
        post_id = ""
        post_url = ""
        
        if 'web_project_name' not in postdata or postdata['web_project_name'] is None:
            if 'project_name' in postdata and postdata['project_name'] is not None:
                postdata['web_project_name'] = postdata['project_name']
            else:
                postdata['web_project_name'] = postdata['post_title_th']
                postdata['project_name'] = "-" 

        if success:
            member_id = test_login["member_id"]
            privateToken = test_login["privateToken"]           
            success = False
            
            address = ''
            for i in ['addr_number','addr_road','addr_soi']:
                if postdata[i] in ['-',' ']:
                    postdata[i] = ''
                address += postdata[i]
                if i != 'addr_soi':
                    address += ' '

            property_type = {
            '1': [1,6],
            '2': [1,4],
            '3': [1,4],
            '4': [1,5],
            '5': [2,10],
            '6': [1,8],
            '7': [1,7],
            '8': [2,12],
            '9': [2,11],
            '10': [2,9],
            '25': [2,9]
            }

            purposeId = {
                'ขาย': 1,
                'เช่า': 2
            }

            for i in ['land_size_rai','land_size_ngan','land_size_wa']:
                postdata[i] = int(postdata[i])

            if postdata['property_type'] in ['6','25','10','8','2','3']:
                area = (postdata['land_size_rai']*1600) + (postdata['land_size_ngan']*400) + (postdata['land_size_wa']*4)                
            else:
                area = postdata['floorarea_sqm']

            postdata['property_type'] = property_type[postdata['property_type']]

            with open('./static/kaidee_project_id.json') as f:
                project_data = json.load(f)

            if 'web_project_name' not in postdata:
                if 'project_name' in postdata:
                    postdata['web_project_name'] = postdata['project_name']
                else:
                    postdata['web_project_name'] = 'None'

            project_id = 0
            province_id = 0
            subdistrict_id = 0
            for key in project_data:
                if postdata['web_project_name'] in project_data[key]['Zone name English']:
                    project_id = key
                    break
                elif postdata['web_project_name'] in project_data[key]['Zone name ไทย']:
                    project_id = key
                    break
            
            if project_id == 0:
                with open('./static/kaidee_province_id.json') as f:
                    province_data = json.load(f)
                for key in province_data:
                    if postdata['addr_province'] in province_data[key]['\ufeffprovince']:
                        province_id = key
                        break
                if province_id != 0:
                    with open('./static/kaidee_subdistrict_id.json') as f:
                        subdistrict_data = json.load(f)
                    for key in subdistrict_data:
                        if (postdata['addr_sub_district'] in subdistrict_data[key]['\ufeffsubdistrict']) and (province_id == subdistrict_data[key]['province_id']):
                            subdistrict_id = key
                            break
            if postdata['property_type'] == [1,6]:
                location_area = project_id
            else:
                location_area = subdistrict_id

            datapost = {
                'id': None,
                'categoryId': postdata['property_type'][1],
                'parentCategoryId': postdata['property_type'][0],
                'purposeId': purposeId[postdata['listing_type']],
                'residenceType': '',
                'referenceNumber': postdata['property_id'],
                'title': {'en': postdata['post_title_en'],'th': postdata['post_title_th']},
                'description': {'en': postdata['post_description_en'],'th': postdata['post_description_th']},
                'locationId': location_area,
                'area': area,
                'address': address,
                'latitude': postdata['geo_latitude'],
                'longitude': postdata['geo_longitude'],
                'bedrooms': postdata['bed_room'],
                'bathrooms': postdata['bath_room'],
                'constructionStatus': 'completed',
                'ownershipStatus': 'freehold',
                'financingAvailable': '',
                'financialInstitutions': '',
                'occupancyStatus': '',
                'agentId': member_id,
                'completionDate': '',
                'minContractPeriod': '',
                'noticePeriod': '',
                'maintenanceFee': '',
                'maintenanceFeePayer': '',
                'adAttributes': {"condition":"used"},
                'product': '',
                'adLocations': [],
                'amenities': [],##################*******************************
                "source":"profolio"
            }

            if purposeId[postdata['listing_type']] == 1:
                datapost['price'] = postdata['price_baht']
                datapost['rentPrice'] = ''
                datapost['rentFrequency'] = ''
            else:
                datapost['price'] = ''
                datapost['rentPrice'] = postdata['price_baht']
                datapost['rentFrequency'] = 'monthly'


            """addr_province = postdata['addr_province']
            addr_district = postdata['addr_district']
            province = "9"
            district = {
                "id": 1, 
                "province": {"id": 9}
            }
            
            with open('./static/kaidee_province.json', 'r') as f:
                province_data = json.loads(f.read())
            for key in province_data["provinces"]:
                if (addr_province.find(str(key)) != -1) or (str(key).find(addr_province) != -1):
                    district["province"]["id"] = province_data["provinces"][key]
                    province = str(province_data["provinces"][key])
                    break
            for key in province_data["districts"][province]:
                if(addr_district.find(str(key)) != -1)  or (str(key).find(addr_district) != -1):
                    district["id"] = province_data["districts"][province][key]
                    break
            
            if postdata["listing_type"]=="ขาย":
                ad_type = 2
            else:
                ad_type = 4

            contacts = [
                {"value": postdata['mobile'], "type":"telephone"},
                {"value": postdata['email'], "type":"email"}
            ]

            if str(postdata['property_type'])=='1':
                postdata['area'] = postdata['floor_area']
            else:
                if 'land_size_ngan' not in postdata or postdata['land_size_ngan']==None:
                    postdata['land_size_ngan'] = 0
                if 'land_size_rai' not in postdata or postdata['land_size_rai']==None:
                    postdata['land_size_rai'] = 0
                if 'land_size_wa' not in postdata or postdata['land_size_wa']==None:
                    postdata['land_size_wa'] = 0
                try:
                    postdata['land_size_ngan'] = int(postdata['land_size_ngan'])
                except ValueError:
                    postdata['land_size_ngan'] = 0
                try:
                    postdata['land_size_rai'] = int(postdata['land_size_rai'])
                except ValueError:
                    postdata['land_size_rai'] = 0
                try:
                    postdata['land_size_wa'] = int(postdata['land_size_wa'])
                except ValueError:
                    postdata['land_size_wa'] = 0
                postdata['area'] = 400 * postdata['land_size_rai'] + 100 * postdata['land_size_ngan'] + postdata['land_size_wa']
            
            attributes = []
            postdata_vars = ['area', 'bed_room', 'bath_room']
            for i, attr in enumerate(categories_list[str(postdata['property_type'])][1]):
                attributes.append({
                    "attribute": {"id": attr[0]},
                    "value": str(postdata[postdata_vars[i]]),
                    "unit": {"id": attr[1]}
                })

            datapost = {
                "title": str(postdata['post_title_th']),
                "price": int(postdata['price_baht']),
                "ad_type":{"id": ad_type},
                "category": {"id": categories_list[str(postdata['property_type'])][0] },
                "member":{"id": member_id},
                "condition":{"id":2}, # second hand
                "district": district,
                "description": str(postdata['post_description_th']),
                "contacts": contacts,
                "attributes": attributes
            }
            
            if len(postdata['post_images'])==0:
                postdata['post_images'] = ['imgtmp/default/white.jpg']"""

            headers = {
                'content-type': 'application/json',
                'http-authorization': 'undefined',
                'authorization': authorization
            }

            images = []
            for i in postdata['post_img_url_lists']:
                images.append(i)
            """for i,image in enumerate(postdata['post_images']):
                files = {"image": open(os.getcwd()+"/"+image, 'rb')} 
                r = self.scraper.post('https://kaidee-images-live.s3.amazonaws.com', data={}, files=files)
                if r.status_code==200:
                    r = json.loads(r.text)
                    detail_img = {   
                        'name': image,
                        "size": 52569,###################
                        "type":"image/jpeg",
                        "lastModifiedDate":"2021-10-01T02:29:26.450Z",#########################
                        "uploadedDate":"2021-10-07T04:26:50.061Z",#######################
                        "percent":100,
                        "id":"id-1633580810061-0",#####################
                        "status":"done",
                        "previewUrl":"blob:https://profolio.baan.kaidee.com/b22b55fc-9462-4abe-8353-65c04480a308",####################
                        "width":450,######################
                        "height":253,#####################
                        "filename":"GDIDpXzUZD3cQAYDzmr6SkvoDiG5Xchujm0KtsaE",########################
                        "fileUrl":"https://kaidee-images-live.s3.amazonaws.com/temp/GDIDpXzUZD3cQAYDzmr6SkvoDiG5Xchujm0KtsaE",###################
                        "path":"https://assets.baan.kaidee.com/temp/GDIDpXzUZD3cQAYDzmr6SkvoDiG5Xchujm0KtsaE",#################
                        "_id":"1633580810061-0",#########################
                        "title":""
                        }
                    if i == 0:
                        detail_img['isMain'] = True
                    else:
                        detail_img['isMain'] = False
                    images.append(detail_img)"""

            datapost["images"] = images

            response = self.scraper.post('https://api.baan.kaidee.com/listings', headers=headers, data={}, json=datapost)
            json_response = json.loads(response.text)
            print(json_response)
            if response.status_code==200:
               
                if json_response['legacy_id'] is not None:
                    post_id = json_response['legacy_id']
                    post_url = "https://baan.kaidee.com/product-"+str(post_id)
                    
                    h={
                        "memberid": str(member_id),
                        "origin": "https://www.kaidee.com",
                        "platform": "web",
                        "privatetoken": privateToken
                    }
                    data = {
                        "ads":[
                            {"ad_id": post_id,
                            "product_id": 1420
                            }
                        ]
                    }
                    r = self.httprequestObj.http_post(self.api_name+'/ven/buy/products/ads', headers=h, data={}, json=data)
                    json_r = json.loads(r.text)

                    if r.status_code==200:
                        success = "true"
                        detail = "Post created successfully! Order id: "+str(json_r["results"]["order"]["order_number"])
                    else:
                        detail = "Post has been created, but failed to make payment with response_code "+str(r.status_code) 
            else:
                detail = 'An Error has occurred with response_code '+str(response.status_code)

        else:
            detail = "cannot login"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": post_url,
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
            "websitename": self.name
        }
    


    def edit_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        # login

        test_login = self.test_login(postdata, True)
        success = test_login["success"]
        detail = "Unable to update post"
        post_id = ""
        post_url = ""
        
        if 'web_project_name' not in postdata or postdata['web_project_name'] is None:
            if 'project_name' in postdata and postdata['project_name'] is not None:
                postdata['web_project_name'] = postdata['project_name']
            else:
                postdata['web_project_name'] = postdata['post_title_th']
                postdata['project_name'] = "-"

        if success=="true":
            member_id = test_login["member_id"]
            privateToken = test_login["privateToken"]           
            success = "false"
            
            addr_province = postdata['addr_province']
            addr_district = postdata['addr_district']
            province = "9"
            district = {
                "id": 1, 
                "province": {"id": 9}
            }
            
            with open('./static/kaidee_province.json', 'r') as f:
                province_data = json.loads(f.read())
            for key in province_data["provinces"]:
                if (addr_province.find(str(key)) != -1) or (str(key).find(addr_province) != -1):
                    district["province"]["id"] = province_data["provinces"][key]
                    province = str(province_data["provinces"][key])
                    break
            for key in province_data["districts"][province]:
                if(addr_district.find(str(key)) != -1)  or (str(key).find(addr_district) != -1):
                    district["id"] = province_data["districts"][province][key]
                    break
            
            if postdata["listing_type"]=="ขาย":
                ad_type = 2
            else:
                ad_type = 4

            contacts = [
                {"value": postdata['mobile'], "type":"telephone"},
                {"value": postdata['email'], "type":"email"}
            ]
            
            if str(postdata['property_type'])=='1':
                postdata['area'] = int(postdata['floor_area'])
            else:
                if 'land_size_ngan' not in postdata or postdata['land_size_ngan']==None:
                    postdata['land_size_ngan'] = 0
                if 'land_size_rai' not in postdata or postdata['land_size_rai']==None:
                    postdata['land_size_rai'] = 0
                if 'land_size_wa' not in postdata or postdata['land_size_wa']==None:
                    postdata['land_size_wa'] = 0
                try:
                    postdata['land_size_ngan'] = int(postdata['land_size_ngan'])
                except ValueError:
                    postdata['land_size_ngan'] = 0
                try:
                    postdata['land_size_rai'] = int(postdata['land_size_rai'])
                except ValueError:
                    postdata['land_size_rai'] = 0
                try:
                    postdata['land_size_wa'] = int(postdata['land_size_wa'])
                except ValueError:
                    postdata['land_size_wa'] = 0
                postdata['area'] = 400 * postdata['land_size_rai'] + 100 * postdata['land_size_ngan'] + postdata['land_size_wa']
           
            attributes = []
            postdata_vars = ['area', 'bed_room', 'bath_room']
            for i, attr in enumerate(categories_list[str(postdata['property_type'])][1]):
                attributes.append({
                    "attribute": {"id": attr[0]},
                    "value": str(postdata[postdata_vars[i]]),
                    "unit": {"id": attr[1]}
                })

            datapost = {
                "title": str(postdata['post_title_th']),
                "price": int(postdata['price_baht']),
                "ad_type":{"id": ad_type},
                "category": {"id": categories_list[str(postdata['property_type'])][0] },
                "member":{"id": member_id},
                "condition":{"id": 2}, # second hand
                "district": district,
                "description": str(postdata['post_description_th']),
                "contacts": contacts,
                "attributes": attributes
            }

            r = self.httprequestObj.http_get(self.api_name+'/ads/'+postdata['post_id'])
            json_r = json.loads(r.text)
           
            if r.status_code==200:
                datapost["id"] = json_r["id"]
                datapost["legacy_id"] = json_r["legacy_id"]
                
                if len(postdata['post_images'])==0:
                    datapost["images"] = json_r["images"]
                else:
                    images = []
                    for i, image in enumerate(postdata['post_images'][:18]):
                        files = {"image": open(os.getcwd()+"/"+image, 'rb')} 
                        r = self.httprequestObj.http_post(self.api_name+'/images/upload', data={}, files=files)
                        if r.status_code==200:
                            r = json.loads(r.text)
                            images.append({
                                "sequence": i+1, 
                                "sizes": {
                                    "tmp": {
                                        "resolution": r["resolution"],
                                        "link": r["link"]
                                    }
                                }
                            })
                    datapost["images"] = images
                
                headers = {
                    "privatetoken": privateToken
                }
                
                response = self.httprequestObj.http_post(self.api_name+'/ads/'+postdata['post_id']+'/edit', headers=headers, data={}, json=datapost)
                json_response = json.loads(response.text)
                
                if response.status_code==200:
                    if "version" in json_response:                  
                        h = {
                            "memberid": str(member_id),
                            "origin": "https://www.kaidee.com",
                            "platform": "web",
                            "referer": "https://www.kaidee.com/posting/done/"+str(postdata['post_id']),
                            "privatetoken": privateToken
                        }
                        data = {
                            "ads":[
                                {"ad_id": int(postdata['post_id']),
                                "product_id": 1420
                                }
                            ]
                        }
                        r = self.httprequestObj.http_post(self.api_name+'/ven/buy/products/ads', headers=h, data={}, json=data)
                        json_r = json.loads(r.text)
                        if r.status_code==200:
                            success = "true"
                            detail = "Post updated successfully! Order id: "+str(json_r["results"]["order"]["order_number"])
                        else:
                            detail = "Post has been updated, but failed to make payment with response_code "+str(r.status_code) 
                    elif "error" in json_response:
                        detail = json_response["error"]["message"]
                else:
                    if "error" in json_response:
                        detail = json_response["error"]["message"]
                    else:
                        detail = 'An Error has occurred while fetching page with response_code '+str(response.status_code)
            else:
                if "error" in json_r:
                    detail = json_r["error"]["message"]
                else:
                    detail = 'An Error has occurred while fetching page with response_code '+str(r.status_code)
        else:
            detail = "cannot login"
        
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_id": postdata['post_id'],
            "log_id": postdata['log_id'],
            "account_type": "null",
            "detail": detail,
            "websitename": self.name,
            "ds_id": postdata['ds_id']
        }



    def selenium_login(self, chrome, username, password):
       
        delay = 10
        changed_url = self.site_name
        chrome.get(self.site_name+'/login/mobile')
        try:
            form = WebDriverWait(chrome, delay).until(EC.presence_of_element_located((By.ID, 'form-register-via-phone-number')))
            email_in = form.find_element_by_id('email_phone')
            email_in.send_keys(username)
            password_in = WebDriverWait(form, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='password-input']")))
            password_in.send_keys(password) 
            login_btn = WebDriverWait(form, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-testid='submit-login-btn']")))
            login_btn.click()
            WebDriverWait(chrome, delay).until(EC.url_changes(changed_url))
            time.sleep(2)
            return True
        except TimeoutException:
            return False

    

    def search_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata, True)
        success = test_login["success"]
        post_url = ""
        post_id = ""
        post_found = ""
        post_modify_time = ""
        post_create_time = ""
        post_view = ""
        post_found = False
        if success == "true":
            member_id = test_login["member_id"]
            privateToken = test_login["privateToken"] 
            post_found = "false"
            detail = "No post found with given title"
            try:
                chrome = webdriver.Chrome("./static/chromedriver", chrome_options=self.options)

                delay = 10

                if self.selenium_login(chrome, postdata['user'], postdata['pass']):
                    post_title_th = str(postdata['post_title_th'])

                    chrome.get(self.site_name+'/member/listing/')
                    main_element = WebDriverWait(chrome, delay).until(EC.presence_of_element_located((By.ID, 'main')))
                    search_in = WebDriverWait(main_element, delay).until(EC.presence_of_element_located((By.NAME, 'q')))
                    search_in.send_keys(post_title_th)
                    time.sleep(5)
                    page_source = chrome.page_source
            finally:
                try:
                    alert = chrome.switch_to.alert
                    alert.accept()
                    chrome.close()
                    chrome.quit()
                except:
                    pass

                soup = BeautifulSoup(page_source, features=self.parser)
                result_posts = soup.find_all(class_='owner-ads-preview')
                for post in result_posts:
                    title = post.find('span', attrs={'type': 'title'})
                    if title and title.getText().strip()==post_title_th:
                        post_found = "true"
                        detail = "Post found successfully!"
                        post_id = str(post.find('a').get('href').split('-')[-1])
                        post_url = 'https://baan.kaidee.com/product-'+ post_id
                        break
            """ except:
                detail = "An error occurred while logging in through selenium" """
        else:
            detail = "cannot login"
        
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": self.name,
            "account_type": None,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "post_create_time": post_create_time,
            "post_modify_time": post_modify_time,
            "post_view": post_view,
            "post_url": post_url,
            "post_found": post_found
        }


    
    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata, True)
        success = test_login["success"]
        detail = "Unable to delete post"

        if success=="true":
            member_id = test_login["member_id"]
            privateToken = test_login["privateToken"] 
            success = "false"

            datapost = {
                "adId": postdata['post_id'],
                "reason_code": 9,
                "reason_note":""
            }
            
            headers = {
                "memberid": str(member_id),
                "privatetoken": privateToken
            }
            response = self.httprequestObj.http_post(self.api_name+'/ads/'+postdata['post_id']+'/close', headers=headers, data={}, json=datapost)
            json_response = json.loads(response.text)
            
            if response.status_code==200:
                if "version" in json_response and json_response["status"]=="deleted":
                    success = "true"
                    detail = "Post deleted successfully"
                elif "error" in json_response:
                    detail = json_response["error"]["message"]
            else:
                if "error" in json_response:
                    detail = json_response["error"]["message"]
                else:
                    detail = 'An Error has occurred with response_code '+str(response.status_code)
        else:
            detail = "cannot login"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": self.name,
            "post_id": postdata['post_id'],
            "log_id": postdata['log_id'],
            "ds_id": postdata['ds_id']
        }



    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata, True)
        success = test_login["success"]
        
        if success=="true":
            success = "false"
            detail = "Unable to boost post"
            member_id = test_login["member_id"]
            privateToken = test_login["privateToken"] 

            datapost = {
                # "orders": [
                #     {
                #         "ad_id": postdata['post_id'], 
                #         "packages":[
                #             {
                #                 "egg": 0, 
                #                 "package_id": 1403,
                #                 "type": "dummy_republish_ad"
                #             }
                #         ]
                #     }
                # ]
            }

            headers = {
                "memberid": str(member_id),
                "privatetoken": privateToken
            }
            response = self.httprequestObj.http_post(self.api_name+'/ads/'+str(postdata['post_id'])+'/extend', headers=headers, data={}, json=datapost)
            json_response = json.loads(response.text)
            
            if response.status_code==200:
                if 'text' in json_response and json_response['text']['title']=='ต่ออายุเรียบร้อยแล้ว':
                    success = "true"
                    detail = "Post boosted successfully"
                elif "error" in json_response:
                    detail = json_response["error"]["message"]
            else:
                if "error" in json_response:
                    detail = json_response["error"]["message"]
                else:
                    detail = 'An Error has occurred with response_code '+str(response.status_code)
        else:
            detail = "Cannot login"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "post_id": postdata['post_id'],
            "log_id": postdata['log_id'],
            "websitename": self.name,
            "ds_id": postdata['ds_id'],
            "post_view": ""
        }


    def print_debug(self, msg):
        if(self.debug == 1):
            print(msg)
        return True

    def print_debug_data(self, data):
        if(self.debugdata == 1):
            print(data)
        return True

        if(self.debugdata == 1):
            print(data)
        return True
