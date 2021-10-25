# -*- coding: utf-8 -*-

from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
import re
import json
import datetime
import sys
import requests
import random
import pytz


category_types = {
    '1': ['คอนโด', 
        {
            "bathroom": "bath_room",
            "bedroom": "bed_room",
            "district": {},
            "floor_no": "floor_level",
            "is_sale": "listing_type",
            "lat_lng": {
                "lat": "geo_latitude", 
                "lng": "geo_longitude"
            },
            "parking_slot": 1,
            "project_name": "web_project_name",
            "ref_code": "",
            "room_type": "simplex",
            "search_val": "addr_province",
            "sub_district": {},
            "usable_area": "floor_area"
        }
    ],
    '2': ['บ้าน',
        {
            "bathroom": "bath_room",
            "bedroom": "bed_room",
            "district": {},
            "is_sale": "listing_type",
            "lat_lng": {
                "lat": "geo_latitude", 
                "lng": "geo_longitude"
            },
            "floor": "floor_level",
            "parking_slot": 1,
            "project_name": "web_project_name",
            "ref_code": "",
            "search_val": "addr_province",
            "sub_district": {},
            "usable_area": "floor_area",
            "building_area": "floor_area",
            "land_area": "total_area"
        }
    ],
    '3': ['บ้าน',
        {
            "bathroom": "bath_room",
            "bedroom": "bed_room",
            "district": {},
            "is_sale": "listing_type",
            "lat_lng": {
                "lat": "geo_latitude", 
                "lng": "geo_longitude"
            },
            "floor": "floor_level",
            "parking_slot": 1,
            "project_name": "web_project_name",
            "ref_code": "",
            "search_val": "addr_province",
            "sub_district": {},
            "usable_area": "floor_area",
            "building_area": "floor_area",
            "land_area": "total_area"
        }
    ],    
    '4': ['บ้าน',
        {
            "bathroom": "bath_room",
            "bedroom": "bed_room",
            "district": {},
            "is_sale": "listing_type",
            "lat_lng": {
                "lat": "geo_latitude", 
                "lng": "geo_longitude"
            },
            "floor": "floor_level",
            "parking_slot": 1,
            "project_name": "web_project_name",
            "ref_code": "",
            "search_val": "addr_province",
            "sub_district": {},
            "usable_area": "floor_area",
            "building_area": "floor_area",
            "land_area": "total_area"
        }
    ],
    '5': ['ตึกแถว',
        {   
            "bathroom": "bath_room",
            "bedroom": "bed_room",
            "district": "",
            "is_sale": "listing_type",
            "building_area": "floor_area",
            "lat_lng": {
                "lat": "geo_latitude", 
                "lng": "geo_longitude"
            },
            "floor": "floor_level",
            "land_area": "total_area",
            "parking_slot": 1,
            "project_name": "web_project_name",
            "ref_code": "",
            "search_val": "addr_province",
            "sub_district": {},
            "storey": "floor_total",
            "usable_area": "floor_area"
        }
    ],
    '6': ['ที่ดิน',
        {
            "district": "",
            "is_empty_land": True,
            "is_sale": "listing_type",
            "land_area": "total_area",
            "land_classification": "สีน้ำตาล",
            "lat_lng": {
                "lat": "geo_latitude", 
                "lng": "geo_longitude"
            },
            "ref_code": "",
            "search_val": "addr_province",
            "sub_district": {}
        }
    ],
    '7': ['ตึกแถว',
        {
            "bathroom": "bath_room",
            "bedroom": "bed_room",
            "district": {},
            "is_sale": "listing_type",
            "building_area": "total_area",
            "floor": "floor_level",
            "lat_lng": {
                "lat": "geo_latitude", 
                "lng": "geo_longitude"
            },
            "parking_slot": 1,
            "project_name": "web_project_name",
            "ref_code": "",
            "search_val": "addr_province",
            "sub_district": {},
            "storey": "floor_total",
            "land_area": "floor_area",
            "usable_area": "floor_area"
        }
    ],
    '8': ['ตึกแถว',
        {
            "bedroom": "bed_room",
            "bathroom": "bath_room",
            "district": {},
            "is_sale": "listing_type",
            "building_area": "total_area",
            "floor": "floor_level",
            "lat_lng": {
                "lat": "geo_latitude", 
                "lng": "geo_longitude"
            },
            "parking_slot": 1,
            "project_name": "web_project_name",
            "ref_code": "",
            "search_val": "addr_province",
            "sub_district": {},
            "storey": "floor_total",
            "land_area": "floor_area",
            "usable_area": "floor_area"
        }
    ],
    '9': ['ตึกแถว',
        {
            "bathroom": "bed_room",
            "bedroom": "bath_room",
            "district": {},
            "is_sale": "listing_type",
            "building_area": "total_area",
            "floor": "floor_level",
            "lat_lng": {
                "lat": "geo_latitude", 
                "lng": "geo_longitude"
            },
            "parking_slot": 1,
            "project_name": "web_project_name",
            "ref_code": "",
            "search_val": "addr_province",
            "sub_district": {},
            "storey": "floor_total",
            "land_area": "floor_area",
            "usable_area": "floor_area"
        }
    ],
    '10': ['โกดัง',
        {   "bathroom": "bath_room",
            "district": "",
            "is_sale": "listing_type",
            "land_area": "total_area",
            "lat_lng": {
                "lat": "geo_latitude", 
                "lng": "geo_longitude"
            },
            "parking_slot": 1,
            "project_name": "web_project_name",
            "ref_code": "",
            "search_val": "addr_province",
            "sub_district": {},
            "truck_parking_slot": 0,
            "usable_area": "floor_area"
        }
    ],
    '25': ['โกดัง',
        {   "bathroom": "bath_room",
            "district": "",
            "is_sale": "listing_type",
            "land_area": "total_area",
            "lat_lng": {
                "lat": "geo_latitude", 
                "lng": "geo_longitude"
            },
            "parking_slot": 1,
            "project_name": "web_project_name",
            "ref_code": "",
            "search_val": "addr_province",
            "sub_district": {},
            "truck_parking_slot": 0,
            "usable_area": "floor_area"
        }
    ]
}



class ennxo():
    name = 'ennxo'
    site_name = "https://www.ennxo.com"

    def __init__(self):
        try:
            import configs
        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.debug = 0
        self.debugresdata = 0
        self.parser = 'html.parser'
        self.httprequestObj = lib_httprequest()


    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        success = "false"
        detail = 'An Error has Occurred'
        if len(postdata['pass'])<6 or len(postdata['pass'])>12:
            detail = "Password should be of 6-12 characters only"
        else:
            datapost = {
                "email": postdata['user'],
                "password": postdata['pass'],
                "confirm_password": postdata['pass'],
                "telephone": postdata['tel'],
                "line": postdata['line'],
                "firstname": postdata['name_th'],
                "lastname": postdata['surname_th']
            }

            response = self.httprequestObj.http_post(self.site_name+'/api/signup', data={}, json=datapost)  
            json_response = response.json()
            if response.status_code==200:
                if 'user_id' in json_response:
                    success = "true"
                    detail = "User registered successfully!"
            else:
                if "user_dup" in json_response:
                    detail = "This email is already registered in the system"
                else:
                    detail = "An error occurred in following field "+str(json_response)+", with response code "+str(response.status_code)

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



    def test_login(self, postdata, from_function=False):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        
        # start process
        success = "false"
        detail = 'An Error has Occurred'
        auth = ''
        user_id = ''

        datapost = {
            "email": postdata['user'],
            "password": postdata['pass']
        }

        response = self.httprequestObj.http_post(self.site_name+'/api/next_login', data={}, json=datapost)    
        json_response = response.json()
        if response.status_code==200:
            if 'user_id' in json_response:
                    success = "true"
                    detail = "Logged in successfully!"
                    if from_function:
                        auth = json_response['access_token']
                        user_id = json_response['user_id']
                        sms_verified = json_response['sms_verified']
        else:
            if "message" in json_response:
                detail = json_response['message']
            else:
                detail = "An error occurred in following field "+str(json_response)+", with response code "+str(response.status_code)

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return_data =  {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": self.name,
            "ds_id": postdata['ds_id']
        }
        if from_function:
            return_data['auth'] = auth
            return_data['user_id'] = user_id
            return_data['sms_verified'] = sms_verified
        return return_data



    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        # login

        test_login = self.test_login(postdata, True)
        success = test_login["success"]
        detail = "Unable to create post"
        post_id = ""
        post_url = ""
        
        if 'web_project_name' not in postdata or postdata['web_project_name'] is None:
            if 'project_name' in postdata and postdata['project_name'] is not None:
                postdata['web_project_name'] = postdata['project_name']
            else:
                postdata['web_project_name'] = postdata['post_title_th']
        if test_login['sms_verified'] == False:
            success = 'false'
        if success=="true":
            auth = test_login['auth']
            success = "false"

            addr_province = "".join(str(postdata['addr_province']).strip().split())
            province = 'กรุงเทพมหานคร'
          
            with open('./static/ennxo_province.json') as f:
                province_data = json.load(f)
            for key in province_data["provinces"]:
                if (addr_province.find(str(key)) != -1) or (str(key).find(addr_province) != -1):
                    province = province_data["provinces"][key]
                    break

            if postdata['land_size_ngan'] is None:
                    postdata['land_size_ngan'] = 0
            if postdata['land_size_rai'] is None:
                postdata['land_size_rai'] = 0
            if postdata['land_size_wa'] is None:
                postdata['land_size_wa'] = 0
            try:
                postdata['land_size_ngan'] = float(postdata['land_size_ngan'])
            except ValueError:
                postdata['land_size_ngan'] = 0
            try:
                postdata['land_size_rai'] = float(postdata['land_size_rai'])
            except ValueError:
                postdata['land_size_rai'] = 0
            try:
                postdata['land_size_wa'] = float(postdata['land_size_wa'])
            except ValueError:
                postdata['land_size_wa'] = 0
            postdata["total_area"] = int(4*(400 * postdata["land_size_rai"] + 100 * postdata["land_size_ngan"] + postdata["land_size_wa"]))
            
            if postdata["listing_type"]=="ขาย":
                postdata["listing_type"] = True
            else:
                postdata["listing_type"] = False

            if "bath_room" not in postdata or ("bath_room" in postdata and postdata["bath_room"].isnumeric()==False):
                postdata["bath_room"] = 1
            postdata["bath_room"] = int(postdata["bath_room"])
            if postdata["bath_room"]>3:
                postdata["bath_room"] = "3+"
            if "bed_room" not in postdata or ("bed_room" in postdata and postdata["bed_room"].isnumeric()==False):
                postdata["bed_room"] = 1
            postdata["bed_room"] = int(postdata["bed_room"])
            if postdata["bed_room"]>3:
                postdata["bed_room"] = "3+" 
            if "floor_total" not in postdata or ("floor_total" in postdata and postdata["floor_total"].isnumeric()==False):
                postdata["floor_total"] = 1
            postdata["floor_total"] = int(postdata["floor_total"])
            if postdata["floor_total"]>10:
                postdata["floor_total"] = 10
            if "floor_level" not in postdata or ("floor_level" in postdata and postdata["floor_level"].isnumeric()==False):
                postdata["floor_level"] = 1
            postdata["floor_level"] = int(postdata["floor_level"])
            if "floor_area" not in postdata or ("floor_area" in postdata and postdata["floor_area"].isnumeric()==False):
                postdata["floor_area"] = 1
            postdata["floor_area"] = int(postdata["floor_area"])
            subfields = category_types[str(postdata['property_type'])][1]
            for field in subfields:
                if str(subfields[field]) in postdata:
                    subfields[field] = postdata[str(subfields[field])]
            subfields["lat_lng"] = {
                "lat": postdata["geo_latitude"], 
                "lng": postdata["geo_longitude"]
            }

            datapost = {
                "name": str(postdata['post_title_th'])[:120],
                "price": int(postdata['price_baht']),
                "detail": str(postdata['post_description_th']),
                "main_category": "อสังหาริมทรัพย์",
                "sub_category": category_types[str(postdata['property_type'])][0],
                "is_second_handed": True,
                "subfields": subfields
            } 

            headers= {
                "authorization": auth
            }

            images = []
            flag = True
            if len(postdata['post_images'])==0:
                postdata['post_images'] = ['imgtmp/default/white.jpg']

            for count,file in enumerate(postdata['post_images']):
                r = self.httprequestObj.http_post(self.site_name+'/api/presigned_url', headers=headers, data={},json={'filename':os.getcwd()+"/"+file})
                json_r = r.json()
                if r.status_code==200:
                    main_data = {
                        'key':json_r['presigned_url']['fields']['key'],
                        'policy':json_r['presigned_url']['fields']['policy'],
                        'x-amz-algorithm':json_r['presigned_url']['fields']['x-amz-algorithm'],
                        'x-amz-credential':json_r['presigned_url']['fields']['x-amz-credential'],
                        'x-amz-date':json_r['presigned_url']['fields']['x-amz-date'],
                        'x-amz-signature':json_r['presigned_url']['fields']['x-amz-signature']
                        }
                else:
                    flag = False
                r = self.httprequestObj.http_post('https://storage.googleapis.com/ennxo_main',data=main_data, files={'file': open(os.getcwd()+"/"+file, 'rb')})
                if r.status_code==204:
                    r = self.httprequestObj.http_post(self.site_name+'/api/upload_photo',headers=headers,data={},json={'_id':json_r['_id']})
                    upload_json = r.json()
                    if count == 0:
                        images.append({"_id":json_r['_id'],"newUploaded":True,"isMainPhoto":True})
                    else:
                        images.append({"_id":json_r['_id'],"newUploaded":True})
                else:
                    flag = False
            datapost["photos"] = images
            #print(datapost)
            if flag:
                response = self.httprequestObj.http_post(self.site_name+'/api/add_product', headers=headers, data={}, json=datapost)
                json_response = response.json()
                if response.status_code==200:
                    if 'product_id' in json_response:
                        success = "true"
                        detail = "Post created successfully!"
                        post_id = str(json_response['product_id'])
                        post_url = self.site_name+'/product/'+post_id
                else:
                    if "message" in json_response:
                        detail = json_response['message']
                    else:
                        detail = "An error occurred in following field "+str(json_response)+", with response code "+str(response.status_code)
            else:
                detail = "An error occurred while uplaoding images. Error is: "+str(json_r)
        else:
            detail = "cannot login"
            if test_login['sms_verified'] == False:
                detail = 'Your post can not create. Please make sure your data is completed or make sure that you already verify you phone number via OTP.'

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
        if test_login['sms_verified'] == False:
            success = 'false'
        if success=="true":
            auth = test_login['auth']
            success = "false"

            addr_province = "".join(str(postdata['addr_province']).strip().split())
            province = 'กรุงเทพมหานคร'
          
            with open('./static/ennxo_province.json') as f:
                province_data = json.load(f)
            for key in province_data["provinces"]:
                if (addr_province.find(str(key)) != -1) or (str(key).find(addr_province) != -1):
                    province = province_data["provinces"][key]
                    break

            if postdata['land_size_ngan'] is None:
                    postdata['land_size_ngan'] = 0
            if postdata['land_size_rai'] is None:
                postdata['land_size_rai'] = 0
            if postdata['land_size_wa'] is None:
                postdata['land_size_wa'] = 0
            try:
                postdata['land_size_ngan'] = float(postdata['land_size_ngan'])
            except ValueError:
                postdata['land_size_ngan'] = 0
            try:
                postdata['land_size_rai'] = float(postdata['land_size_rai'])
            except ValueError:
                postdata['land_size_rai'] = 0
            try:
                postdata['land_size_wa'] = float(postdata['land_size_wa'])
            except ValueError:
                postdata['land_size_wa'] = 0
            postdata["total_area"] = int(4*(400 * postdata["land_size_rai"] + 100 * postdata["land_size_ngan"] + postdata["land_size_wa"]))
            
            if postdata["listing_type"]=="ขาย":
                postdata["listing_type"] = True
            else:
                postdata["listing_type"] = False

            if "bath_room" not in postdata or ("bath_room" in postdata and postdata["bath_room"].isnumeric()==False):
                postdata["bath_room"] = 1
            postdata["bath_room"] = int(postdata["bath_room"])
            if postdata["bath_room"]>3:
                postdata["bath_room"] = "3+"
            if "bed_room" not in postdata or ("bed_room" in postdata and postdata["bed_room"].isnumeric()==False):
                postdata["bed_room"] = 1
            postdata["bed_room"] = int(postdata["bed_room"])
            if postdata["bed_room"]>3:
                postdata["bed_room"] = "3+" 
            if "floor_total" not in postdata or ("floor_total" in postdata and postdata["floor_total"].isnumeric()==False):
                postdata["floor_total"] = 1
            postdata["floor_total"] = int(postdata["floor_total"])
            if postdata["floor_total"]>10:
                postdata["floor_total"] = 10
            if "floor_level" not in postdata or ("floor_level" in postdata and postdata["floor_level"].isnumeric()==False):
                postdata["floor_level"] = 1
            postdata["floor_level"] = int(postdata["floor_level"])
            if "floor_area" not in postdata or ("floor_area" in postdata and postdata["floor_area"].isnumeric()==False):
                postdata["floor_area"] = 1
            postdata["floor_area"] = int(postdata["floor_area"])

            subfields = category_types[str(postdata['property_type'])][1]
            for field in subfields:
                if str(subfields[field]) in postdata:
                    subfields[field] = postdata[str(subfields[field])]
            subfields["lat_lng"] = {
                "lat": postdata["geo_latitude"], 
                "lng": postdata["geo_longitude"]
            }

            datapost = {
                "name": str(postdata['post_title_th'])[:120],
                "price": int(postdata['price_baht']),
                "detail": str(postdata['post_description_th']),
                "main_category": "อสังหาริมทรัพย์",
                "sub_category": category_types[str(postdata['property_type'])][0],
                "is_second_handed": True,
                "subfields": subfields,
                "product_id": str(postdata['post_id'])
            }

            headers= {
                "Authorization": auth
            }
            images = []
            flag = True
            r = self.httprequestObj.http_get(self.site_name+'/api/product/'+str(postdata['post_id']), headers=headers)
            json_r = r.json()
            if r.status_code==200:
                for image in json_r['photos']:
                    if 'cover' in image.keys():
                        images.append({
                            "_id": image['_id']['$oid'],
                            "newUploaded": False,
                            "isMainPhoto": True
                        })
                    else:
                        images.append({
                            "_id": image['_id']['$oid'],
                            "newUploaded": False
                        })
            else:
                flag = False
            """
            if len(postdata['post_images'])==0:
                r = self.httprequestObj.http_get(self.site_name+'/api/product/'+str(postdata['post_id']), headers=headers)
                json_r = r.json()
                if r.status_code==200:
                    for i, image in enumerate(json_r['photos']):
                        if i==0:
                            images.append({
                                "_id": image['_id']['$oid'],
                                "newUploaded": False,
                                "isMainPhoto": True
                            })
                        else:
                            images.append({
                                "_id": image['_id']['$oid'],
                                "newUploaded": False
                            })
                else:
                    flag = False
            else:
                for count,file in enumerate(postdata['post_images']):
                    r = self.httprequestObj.http_post(self.site_name+'/api/presigned_url', headers=headers, data={},json={'filename':os.getcwd()+"/"+file})
                    json_r = r.json()
                    if r.status_code==200:
                        main_data = {
                            'key':json_r['presigned_url']['fields']['key'],
                            'policy':json_r['presigned_url']['fields']['policy'],
                            'x-amz-algorithm':json_r['presigned_url']['fields']['x-amz-algorithm'],
                            'x-amz-credential':json_r['presigned_url']['fields']['x-amz-credential'],
                            'x-amz-date':json_r['presigned_url']['fields']['x-amz-date'],
                            'x-amz-signature':json_r['presigned_url']['fields']['x-amz-signature']
                            }
                    r = self.httprequestObj.http_post('https://storage.googleapis.com/ennxo_main',data=main_data, files={'file': open(os.getcwd()+"/"+file, 'rb')})
                    if r.status_code==204:
                        r = self.httprequestObj.http_post(self.site_name+'/api/upload_photo',headers=headers,data={},json={'_id':json_r['_id']})
                        upload_json = r.json()
                        if count == 0:
                            images.append({"_id":json_r['_id'],"newUploaded":True,"isMainPhoto":True})
                        else:
                            images.append({"_id":json_r['_id'],"newUploaded":True})"""
            datapost["photos"] = images
            #print(datapost)
            if flag:
                response = self.httprequestObj.http_post(self.site_name+'/api/edit_product', headers=headers, data={}, json=datapost)
                json_response = response.json()
                if response.status_code==200:
                    if 'product_id' in json_response:
                        success = "true"
                        detail = "Post updated successfully!"
                else:
                    if "message" in json_response:
                        detail = json_response['message']
                    else:
                        detail = "An error occurred in following field "+str(json_response)+", with response code "+str(response.status_code)
            else:
                detail = "An error occurred while uplaoding images. Error is: "+str(json_r)
        else:
            detail = "cannot login"
            if test_login['sms_verified'] == False:
                detail = 'Your post can not create. Please make sure your data is completed or make sure that you already verify you phone number via OTP.'
        
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

        if success == "true":
            user_id = str(test_login['user_id'])
            post_found = "false"
            detail = "No post found with given title"
            post_title = " ".join(str(postdata['post_title_th']).strip()[:120].split())
            page_num = 1
            flag = True

            while flag:
                response = self.httprequestObj.http_get(self.site_name+'/api/get_user_products/'+user_id+'/'+str(page_num))
                json_response = response.json()
                if response.status_code==200:
                    if json_response['count']> page_num*24:
                        page_num += 1
                    else:
                        flag = False
                    if 'products' in json_response:
                        for post in json_response['products']:
                            if " ".join(str(post['name']).strip().split())==post_title:
                                post_found = "true"
                                detail = "Post found successfully!"
                                post_id = str(post['id'])
                                post_create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(post['create_date']['$date']//1000)) 
                                flag = False
                                post_url = self.site_name+"/product/"+post_id
                                break
                else:
                    success = "false"
                    detail = 'An Error has occurred with response_code '+str(response.status_code)
                    flag = False
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
            success = "false"
            auth = test_login['auth']
            detail = "Unable to delete post"

            headers= {
                "Authorization": auth,
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
                "referer": "https://www.ennxo.com/product/"+str(postdata['post_id'])
            }

            r = self.httprequestObj.http_get("https://www.ennxo.com/product/" + str(postdata['post_id']))
            data_id = r.text.split("/_buildManifest")[0].split("/")[-1]
            r = self.httprequestObj.http_get(self.site_name + '/_next/data/'+data_id+'/edit/' + str(postdata['post_id']) + ".json?id=" + str(postdata['post_id']))
            json_r = r.json()["pageProps"]["product"]
            # print(json_r)
            if r.status_code==200:
                datapost = {
                    "name": json_r['name'][:109]+ ' ปิดประกาศ',
                    "price": json_r['price'],
                    "detail": json_r['detail'],
                    "main_category": "อสังหาริมทรัพย์",
                    "sub_category": json_r['sub_category'],
                    "is_second_handed": True,
                    "province": json_r['province'],
                    "product_id": json_r['id'],
                    "subfields": json_r['subfields']
                }

                images = []
                for i, image in enumerate(json_r['photos']):
                    if i==0:
                        images.append({
                            "_id": image['_id']['$oid'],
                            "newUploaded": False,
                            "isMainPhoto": True
                        })
                    else:
                        images.append({
                            "_id": image['_id']['$oid'],
                            "newUploaded": False
                        })
                datapost['photos'] = images

                response = self.httprequestObj.http_post(self.site_name+'/api/edit_product', headers=headers, data={}, json=datapost)
                json_response = response.json()
                if response.status_code==200:
                    if 'product_id' in json_response:
                        success = "true"
                        detail = "Post deleted successfully!"
                else:
                    if "message" in json_response:
                        detail = json_response['message']
                    else:
                        detail = "An error occurred in following field "+str(json_response)+", with response code "+str(response.status_code)
            else:
                detail = 'An Error has occurred while fetching page with response_code '+str(r.status_code)

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
            auth = test_login['auth']
            detail = "Unable to boost post"

            headers= {
                "Authorization": auth,
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
                "referer": "https://www.ennxo.com/product/"+str(postdata['post_id'])
            }

            r = self.httprequestObj.http_get("https://www.ennxo.com/product/" + str(postdata['post_id']))
            data_id = r.text.split("/_buildManifest")[0].split("/")[-1]

            r = self.httprequestObj.http_get(self.site_name + '/_next/data/'+data_id+'/edit/' + str(postdata['post_id']) + ".json?id=" + str(postdata['post_id']))

            json_r = r.json()["pageProps"]["product"]
            if r.status_code==200:
                datapost = {
                    "name": json_r['name'],
                    "price": json_r['price'],
                    "detail": json_r['detail'],
                    "main_category": "อสังหาริมทรัพย์",
                    "sub_category": json_r['sub_category'],
                    "is_second_handed": True,
                    "province": json_r['province'],
                    "product_id": json_r['id'],
                    "subfields": json_r['subfields']
                }

                images = []
                for i, image in enumerate(json_r['photos']):
                    if i==0:
                        images.append({
                            "_id": image['_id']['$oid'],
                            "newUploaded": False,
                            "isMainPhoto": True
                        })
                    else:
                        images.append({
                            "_id": image['_id']['$oid'],
                            "newUploaded": False
                        })
                datapost['photos'] = images

                response = self.httprequestObj.http_post(self.site_name+'/api/edit_product', headers=headers, data={}, json=datapost)
                json_response = response.json()
                if response.status_code==200:
                    if 'product_id' in json_response:
                        success = "true"
                        detail = "Post boosted successfully!"
                else:
                    if "message" in json_response:
                        detail = json_response['message']
                    else:
                        detail = "An error occurred in following field "+str(json_response)+", with response code "+str(response.status_code)
            else:
                detail = 'An Error has occurred while fetching page with response_code '+str(r.status_code)

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
            "ds_id": postdata['ds_id']
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






