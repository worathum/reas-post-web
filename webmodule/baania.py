# -*- coding: utf-8 -*-

from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
import re
import json
import datetime
import sys
import requests
import shutil
from urllib.parse import unquote
from requests_toolbelt.multipart.encoder import MultipartEncoder


httprequestObj = lib_httprequest()


class baania():

    name = 'baania'

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

    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']

        # start process
        #
        success = "true"
        detail = "Registered"

        datapost = {
            "confirmPassword": passwd,
            "password": passwd,
            "name": postdata['name_th']+' '+postdata['surname_th'],
            "email": user,
        }

        try:
            r = httprequestObj.http_post(
                'https://api.baania.com/api/v1/register', data=datapost)
            # print(r.text)
            ret = json.loads(r.text)
            if ret["status"] != 200:
                success = "False"
                detail = ret['message']

        except:
            success = "False"
            detail = "Check password and email"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "baania",
            'ds_id': postdata['ds_id'],
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "ds_id": postdata['ds_id']
        }

    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']
        # start process
        #
        success = "true"
        detail = "logged in"

        datapost = {
            "email": user,
            "password": passwd,
        }
        r = httprequestObj.http_post(
            'https://api.baania.com/api/v1/login', data=datapost)
        ret = json.loads(r.text)
        # print(ret)
        if ret["status"] != 200:
            success = "False"
            detail = ret['message']
        #
        # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        if success == "true":
            return {
                "websitename": "baania",
                "success": success,
                "usage_time": str(time_usage),
                "ds_id": postdata['ds_id'],
                "start_time": str(time_start),
                "end_time": str(time_end),
                "detail": detail,
                "login_token": ret['token']
            }
        else:
            return {
                "websitename": "baania",
                "success": success,
                "ds_id": postdata['ds_id'],
                "usage_time": str(time_usage),
                "start_time": str(time_start),
                "end_time": str(time_end),
                "detail": detail
            }

    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        datapost = {}
        # start process
        #

        # login

        # print(postdata)

        if 'name' not in postdata:
            success = "False"
            detail = "Please fill name"
        elif 'mobile' not in postdata:
            success = "False"
            detail = "Please fill mobile number"
        elif 'email' not in postdata:
            success = "False"
            detail = "Please fill email"

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""

        proid = {
            'คอนโด': '1',
            'บ้านเดี่ยว': '2',
            'บ้านแฝด': '3',
            'ทาวน์เฮ้าส์': '4',
            'ตึกแถว-อาคารพาณิชย์': '5',
            'ที่ดิน': '6',
            'อพาร์ทเมนท์': '7',
            'โรงแรม': '8',
            'ออฟฟิศสำนักงาน': '9',
            'โกดัง': '10',
            'โรงงาน': '25'
        }
        getProdId = {'1': 2, '2': 1, '3': 10753, '4': 3,
                     '5': 4, '6': 7, '7': 5, '8': 2362, '9': 6, '10': 8, '25': 10753}

        try:
            theprodid = getProdId[proid[postdata['property_type']]]
        except:
            theprodid = getProdId[postdata['property_type']]

        address = {
            "websitename": "baania",
            "address_no": "",
            "building": "",
            "floor": "",
            "soi": postdata["addr_soi"],
            "road": postdata["addr_road"],
            "post_code": ""
        }
        r = requests.get("https://api.baania.com/api/v1/provinces")
        prov = json.loads(r.text)
        for i in prov:
            if i['data']['title']['title_th'].strip() == postdata["addr_province"].strip():
                province_id = i['data']['id']
                address["province"] = {
                    "id": i['data']['id'],
                    "name": postdata["addr_province"]
                }
        if 'province' not in address:
            for i in prov:
                if i['data']['title']['title_th'].strip() in postdata["addr_province"].strip() or postdata["addr_province"] in i['data']['title']['title_th']:
                    province_id = i['data']['id']
                    address["province"] = {
                        "id": i['data']['id'],
                        "name": postdata["addr_province"]
                    }

        r = requests.get(
            "https://api.baania.com/api/v1/provinces/"+province_id+"/districts")
        prov = json.loads(r.text)
        
        for j in prov:
            if j['data']['title']['title_th'].strip() == postdata['addr_district'].strip():
                amphur_id = j['data']['id']
                address["district"] = {
                    "id": j['data']['id'],
                    "name": postdata["addr_district"]
                }
        if 'district' not in address:
            for j in province:
                if j['data']['title']['title_th'].strip() in postdata['addr_district'].strip() or postdata['addr_district'] in j['data']['title']['title_th']:
                    amphur_id = j['data']['id']
                    address["district"] = {
                        "id": j['data']['id'],
                        "name": postdata["addr_district"]
                    }

        r = requests.get(
            "https://api.baania.com/api/v1/districts/"+amphur_id+"/subdistricts")
        prov = json.loads(r.text)
        
        for j in prov:
            if j['data']['title']['title_th'].strip() == postdata["addr_sub_district"].strip():
                address["sub_district"] = {
                    "id": i['data']['id'],
                    "name": postdata["addr_sub_district"]
                }
        if 'sub_district' not in address:
            for j in province:
                if j['data']['title']['title_th'].strip() in postdata["addr_sub_district"].strip() or postdata["addr_sub_district"].strip() in j['data']['title']['title_th']:
                    address["sub_district"] = {
                        "id": i['data']['id'],
                        "name": postdata["addr_sub_district"]
                    }

        address["post_code"] = "88888"
        if postdata['land_size_rai'] is None or postdata['land_size_rai'] == '':
            postdata['land_size_rai'] = 0

        if postdata['land_size_ngan'] is None or postdata['land_size_ngan'] == '': 
            postdata['land_size_ngan'] = 0

        if postdata['land_size_wa'] is None or postdata['land_size_wa'] == '' :
            postdata['land_size_wa'] = 0

        area = 1600*int(postdata['land_size_rai']) + 400 *int(postdata['land_size_ngan']) + 4*int(postdata['land_size_wa'])

        # if theprodid == 2:
        if 'floor_area' in postdata:
            area = postdata['floor_area']
        else:
            if 'floorarea_sqm' in postdata:
                area = postdata['floorarea_sqm']
            else:
                area = 0
                
        if 'floor_total' not in postdata:
            postdata['floor_total'] = 0
        elif postdata['floor_total'] == None or postdata['floor_total'] == '':
            postdata['floor_total'] = 0

        if 'floor_level' not in postdata:
            postdata['floor_level'] = 0
        elif postdata['floor_level'] == None or postdata['floor_level'] == '':
            postdata['floor_level'] = 0

        if 'bath_room' not in postdata:
            postdata['bath_room'] = 0
        elif postdata['bath_room'] == None or postdata['bath_room'] == '':
            postdata['bath_room'] = 0

        if 'bed_room' not in postdata:
            postdata['bed_room'] = 0
        elif postdata['bed_room'] == None or postdata['bed_room'] == '':
            postdata['bed_room'] = 0

        if 'web_project_name' not in postdata or postdata['web_project_name']!=None:
            if 'project_name' in postdata and postdata['project_name']!=None:
                postdata['web_project_name'] = postdata['project_name']
            else:
                postdata['web_project_name'] = postdata['post_title_th']




    # flag = True

    # while flag:
        mydata = {
            "q":postdata['web_project_name'],
            "size":1,
            "filter":{
                "propertyType":"2"
                }
            }
        resp = requests.post('https://search.baania.com/api/v1/project', data=mydata)
        try:
            allres = json.loads(resp.content.decode('utf-8'))["hits"]["hits"]
        except:
            
            return {
            "websitename": "baania",
            "success": "false",
            "detail": str(resp.content.decode('utf-8')),
            "start_time": str(time_start),
            "end_time": str(datetime.datetime.utcnow()),
            "ds_id": postdata['ds_id'],
            "post_url": "",
            "post_id": ""
            }


        project_id = None
        if len(allres) != 0:
            project_id = allres[0]["_id"]
            postdata['web_project_name'] = allres[0]["_source"]["view_data"]["title"]["th"]
            postdata["geo_longitude"] = allres[0]["_source"]["location"]["lon"]
            postdata["geo_latitude"] = allres[0]["_source"]["location"]["lat"]
            address = {}
            address['province'] = {"name":allres[0]["_source"]["address"]["province"]["title"]["th"],"id":allres[0]["_source"]["address"]["province"]["code"]}
            address['district'] = {"name":allres[0]["_source"]["address"]["district"]["title"]["th"],"id":allres[0]["_source"]["address"]["district"]["code"]}
            address['sub_district'] = {"name":allres[0]["_source"]["address"]["subdistrict"]["title"]["th"],"id":allres[0]["_source"]["address"]["subdistrict"]["code"]}
            address['post_code'] = allres[0]["_source"]["address"]["postcode"]


        listing = 0

        if postdata['listing_type'] != 'ขาย':
            listing = 'for-rent'
            datapost["price_renting"] = postdata["price_baht"]
        else:
            listing = 'for-sale'
            datapost["price_listing"] = postdata["price_baht"]

        if success == "true":
            datapost = {
                "listing_type": listing,
                "project_keyId": project_id,
                "property_type_id": theprodid,
                "project": {
                    "name": postdata["web_project_name"],
                    "id": project_id,
                    "keyId": project_id
                },
                "address": address,
                "geo_point": {
                    "lng": postdata["geo_longitude"],
                    "lat": postdata["geo_latitude"]
                },
                "area_land":{
                    "rai":postdata["land_size_rai"],
                    "ngan":postdata["land_size_ngan"],
                    "wa":postdata["land_size_wa"],
                },
                "area_usable": area
            }
            if postdata['listing_type'] != 'ขาย':
                listing = 'for-rent'
                datapost["price_renting"] = postdata["price_baht"]
            else:
                listing = 'for-sale'
                datapost["price_listing"] = postdata["price_baht"]
            headers = {
                'authorization': 'Bearer ' + test_login['login_token'],
                'content-type': 'application/json',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
            }

            r = httprequestObj.http_post(
                'https://api.baania.com/api/v1/users/listings', data=json.dumps(datapost).encode('utf-8'), headers=headers)

            data = json.loads(r.text)
            # print(r)
            # print(data)
            if r.status_code != 200 and r.status_code != 201:
                success = "false"
                detail = data["message"]

            if success == "true":
                pid = data['_id']

                datapost['_id'] = pid
                datapost['num_bed'] = postdata['bed_room']
                datapost['num_bath'] = postdata['bath_room']
                datapost['num_floor'] = postdata['floor_total']
                datapost['keyId'] = pid

                r = requests.patch('https://api.baania.com/api/v1/users/listings/' +
                                   pid+'/2', data=json.dumps(datapost).encode('utf-8'), headers=headers)
                data = json.loads(r.text)
                if r.status_code != 200:
                    success = "false"
                    detail = data["message"]
            # print(data)

            if success == "true":

                files = {
                    "cover": "",
                    "images": []
                }
                # print(postdata["post_images"])
                # print(postdata)
                allimages = postdata["post_images"][:21]

                if len(allimages) != 0:

                    for i in range(len(allimages)):
                        im = open(os.getcwd()+"/"+allimages[i], 'rb')
                        # print(allimages[i])
                        mr = MultipartEncoder(
                            fields={
                                "type": "listing",
                                "uploadImages": (im.name, im, 'image/'+im.name[-1])
                            }
                        )
                        headers['content-type'] = mr.content_type
                        r = httprequestObj.http_post(
                            'https://api.baania.com/api/v1/uploadImages', data=mr, headers=headers)
                        res = json.loads(r.text)
                        if r.status_code != 200:
                            success = "false"
                            detail = "Problem in images"

                        if success == "false":
                            break
                        temp = {
                            "_source": "FRONTEND_API_SOURCE",
                            "source": res[0]["source"],
                            "main": res[0]["main"],
                            "thumbnail": res[0]["thumbnail"]
                        }
                        if i == 0:
                            files["cover"] = temp
                        else:
                            files["images"].append(temp)
                else:
                    im = open(os.getcwd()+"/imgtmp/default/white.jpg", 'rb')

                    mr = MultipartEncoder(
                        fields={
                            "type": "listing",
                            "uploadImages": (im.name, im, 'image/'+im.name[-1])
                        }
                    )
                    headers['content-type'] = mr.content_type
                    r = httprequestObj.http_post(
                        'https://api.baania.com/api/v1/uploadImages', data=mr, headers=headers)
                    res = json.loads(r.text)
                    if r.status_code != 200:
                        success = "false"
                        detail = "Problem in images"

                    temp = {
                        "_source": "FRONTEND_API_SOURCE",
                        "source": res[0]["source"],
                        "main": res[0]["main"],
                        "thumbnail": res[0]["thumbnail"]
                    }
                    files["cover"] = temp


            if success == "true":
                headers['content-type'] = 'application/json'
                # print(files)
                r = requests.patch('https://api.baania.com/api/v1/users/listings/' +
                                   pid+'/3', data=json.dumps(files).encode('utf-8'), headers=headers)
                data = json.loads(r.text)
                # print(data)
                if r.status_code != 200:
                    success = "false"
                    detail = data["message"]

            if success == "true":
                datapost = {
                    "website": "baania.com",
                    "title_th": postdata["post_title_th"],
                    "contact_name": postdata["name"],
                    "contact_tel": postdata["mobile"],
                    "description_th": postdata["post_description_th"].replace('\n','<br>'),
                    "is_publish": 1
                }
                # print(postdata["post_description_th"].replace('\n','<br>'))
                # print(postdata["post_description_th"])
                r = requests.patch('https://api.baania.com/api/v1/users/listings/' +
                                   pid+'/4', data=json.dumps(datapost).encode('utf-8'), headers=headers)
                data = json.loads(r.text)
                # print(data)
                if r.status_code != 200:
                    success = "false"
                    detail = data["message"]

                post_id = pid
                post_url = 'https://www.baania.com/th/listing/' + \
                    postdata["post_title_th"]+'-'+pid

        else:
            detail = "cannot login"
        # print(detail)resp.contentresp.content
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "baania",
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "ds_id": postdata['ds_id'],
            "end_time": str(time_end),
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "null",
            "detail": detail
        }

  

    def edit_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        datapost = {}
        # start process
        #

        # login
        if 'name' not in postdata:
            success = "False"
            detail = "Please fill name"
        elif 'mobile' not in postdata:
            success = "False"
            detail = "Please fill mobile number"
        elif 'email' not in postdata:
            success = "False"
            detail = "Please fill email"

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""

        proid = {
            'คอนโด': '1',
            'บ้านเดี่ยว': '2',
            'บ้านแฝด': '3',
            'ทาวน์เฮ้าส์': '4',
            'ตึกแถว-อาคารพาณิชย์': '5',
            'ที่ดิน': '6',
            'อพาร์ทเมนท์': '7',
            'โรงแรม': '8',
            'ออฟฟิศสำนักงาน': '9',
            'โกดัง': '10',
            'โรงงาน': '25'
        }
        getProdId = {'1': 2, '2': 1, '3': 10753, '4': 3,
                     '5': 4, '6': 7, '7': 5, '8': 2362, '9': 6, '10': 8, '25': 10753}

        try:
            theprodid = getProdId[proid[postdata['property_type']]]
        except:
            theprodid = getProdId[postdata['property_type']]

        address = {
            "address_no": "",
            "building": "",
            "floor": "",
            "soi": postdata["addr_soi"],
            "road": postdata["addr_road"],
            "post_code": ""
        }


        r = requests.get("https://api.baania.com/api/v1/provinces")
        prov = json.loads(r.text)
        for i in prov:
            if i['data']['title']['title_th'].strip() == postdata["addr_province"].strip():
                province_id = i['data']['id']
                address["province"] = {
                    "id": i['data']['id'],
                    "name": postdata["addr_province"]
                }
        if 'province' not in address:
            for i in prov:
                if i['data']['title']['title_th'].strip() in postdata["addr_province"].strip() or postdata["addr_province"] in i['data']['title']['title_th']:
                    province_id = i['data']['id']
                    address["province"] = {
                        "id": i['data']['id'],
                        "name": postdata["addr_province"]
                    }

        r = requests.get(
            "https://api.baania.com/api/v1/provinces/"+province_id+"/districts")
        prov = json.loads(r.text)
        
        for j in prov:
            if j['data']['title']['title_th'].strip() == postdata['addr_district'].strip():
                amphur_id = j['data']['id']
                address["district"] = {
                    "id": j['data']['id'],
                    "name": postdata["addr_district"]
                }
        if 'district' not in address:
            for j in prov:
                if j['data']['title']['title_th'].strip() in postdata['addr_district'].strip() or postdata['addr_district'] in j['data']['title']['title_th']:
                    amphur_id = j['data']['id']
                    address["district"] = {
                        "id": j['data']['id'],
                        "name": postdata["addr_district"]
                    }

        r = requests.get(
            "https://api.baania.com/api/v1/districts/"+amphur_id+"/subdistricts")
        prov = json.loads(r.text)
        
        for j in prov:
            if j['data']['title']['title_th'].strip() == postdata["addr_sub_district"].strip():
                address["sub_district"] = {
                    "id": i['data']['id'],
                    "name": postdata["addr_sub_district"]
                }
        if 'sub_district' not in address:
            for j in prov:
                if j['data']['title']['title_th'].strip() in postdata["addr_sub_district"].strip() or postdata["addr_sub_district"].strip() in j['data']['title']['title_th']:
                    address["sub_district"] = {
                        "id": i['data']['id'],
                        "name": postdata["addr_sub_district"]
                    }


        address["post_code"] = "88888"
        if postdata['land_size_rai'] is None or postdata['land_size_rai'] == '':
            postdata['land_size_rai'] = 0

        if postdata['land_size_ngan'] is None or postdata['land_size_ngan'] == '': 
            postdata['land_size_ngan'] = 0

        if postdata['land_size_wa'] is None or postdata['land_size_wa'] == '' :
            postdata['land_size_wa'] = 0

        area = 1600*int(postdata['land_size_rai']) + 400 *int(postdata['land_size_ngan']) + 4*int(postdata['land_size_wa'])

        if theprodid == 2:
            if 'floor_area' in postdata:
                area = postdata['floor_area']
            else:
                if 'floorarea_sqm' in postdata:
                    area = postdata['floorarea_sqm']
                else:
                    area = 0

        if 'floor_total' not in postdata:
            postdata['floor_total'] = 0
        elif postdata['floor_total'] == None or postdata['floor_total'] == '':
            postdata['floor_total'] = 0

        if 'floor_level' not in postdata:
            postdata['floor_level'] = 0
        elif postdata['floor_level'] == None or postdata['floor_level'] == '':
            postdata['floor_level'] = 0

        if 'bath_room' not in postdata:
            postdata['bath_room'] = 0
        elif postdata['bath_room'] == None or postdata['bath_room'] == '':
            postdata['bath_room'] = 0

        if 'bed_room' not in postdata:
            postdata['bed_room'] = 0
        elif postdata['bed_room'] == None or postdata['bed_room'] == '':
            postdata['bed_room'] = 0

        if 'web_project_name' not in postdata or postdata['web_project_name']!=None:
            if 'project_name' in postdata and postdata['project_name']!=None:
                postdata['web_project_name'] = postdata['project_name']
            else:
                postdata['web_project_name'] = postdata['post_title_th']


        mydata = {
            "q":postdata['web_project_name'],
            "size":1,
            "filter":{
                "propertyType":"2"
                }
            }
        resp = requests.post('https://search.baania.com/api/v1/project', data=mydata)
        try:
            allres = json.loads(resp.content.decode('utf-8'))["hits"]["hits"]
        except:
            
            return {
            "websitename": "baania",
            "success": "false",
            "detail": str(resp.content.decode('utf-8')),
            "start_time": str(time_start),
            "end_time": str(datetime.datetime.utcnow()),
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_url": "",
            "post_id": ""
            }


        project_id = None
        if len(allres) != 0:
            project_id = allres[0]["_id"]
            postdata['web_project_name'] = allres[0]["_source"]["view_data"]["title"]["th"]
            postdata["geo_longitude"] = allres[0]["_source"]["location"]["lon"]
            postdata["geo_latitude"] = allres[0]["_source"]["location"]["lat"]
            address = {}
            address['province'] = {"name":allres[0]["_source"]["address"]["province"]["title"]["th"],"id":allres[0]["_source"]["address"]["province"]["code"]}
            address['district'] = {"name":allres[0]["_source"]["address"]["district"]["title"]["th"],"id":allres[0]["_source"]["address"]["district"]["code"]}
            address['sub_district'] = {"name":allres[0]["_source"]["address"]["subdistrict"]["title"]["th"],"id":allres[0]["_source"]["address"]["subdistrict"]["code"]}
            address['post_code'] = allres[0]["_source"]["address"]["postcode"]


        if success == "true":
            datapost = {
                "project_keyId": project_id,
                "project": {
                    "name": postdata["web_project_name"],
                    "id": project_id,
                    "keyId": project_id
                },
                "property_type_id": theprodid,
                "address": address,
                "geo_point": {
                    "lng": postdata["geo_longitude"],
                    "lat": postdata["geo_latitude"]
                },
                "area_usable": area
            }
            if postdata['listing_type'] != 'ขาย':
                datapost['listing_type'] = 'for-rent'
                datapost["price_renting"] = postdata["price_baht"]
                datapost["price_listing"] = ''
            else:
                datapost['listing_type'] = 'for-sale'
                datapost["price_listing"] = postdata["price_baht"]
                datapost['price_renting'] = ''
            headers = {
                'authorization':  'Bearer ' + test_login['login_token'],
                'content-type': 'application/json',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
            }

            r = requests.patch(
                'https://api.baania.com/api/v1/users/listings/'+postdata['post_id']+'/1', data=json.dumps(datapost).encode('utf-8'), headers=headers)

            data = json.loads(r.text)
            if r.status_code != 200 and r.status_code != 201:
                success = "false"
                detail = data["message"]

            if r.status_code == 500:
                success = "false"
                detail = "Wrong Post Id"
            if success == "true":
                pid = data['_id']

                datapost['_id'] = pid
                datapost['num_bed'] = postdata['bed_room']
                datapost['num_bath'] = postdata['bath_room']
                datapost['num_floor'] = postdata['bath_room']
                datapost['keyId'] = pid

                r = requests.patch('https://api.baania.com/api/v1/users/listings/' +
                                   pid+'/2', data=json.dumps(datapost).encode('utf-8'), headers=headers)
                data = json.loads(r.text)
                if r.status_code != 200:
                    success = "false"
                    detail = data["message"]
            # print(data)
            allimages = postdata["post_images"][:20]
            if success == "true" and len(allimages) != 0:
                # print(data['cover'])
                # print(data['images'])
                if data['cover'] != None:
                    files = {
                        "cover": data['cover'],
                        "images": data['images']
                    }
                    for i in range(len(allimages)):
                        im = open(os.getcwd()+"/"+allimages[i], 'rb')
                        mr = MultipartEncoder(
                            fields={
                                "type": "listing",
                                "uploadImages": (im.name, im, 'image/'+im.name[-1])
                            }
                        )
                        headers['content-type'] = mr.content_type
                        r = httprequestObj.http_post(
                            'https://api.baania.com/api/v1/uploadImages', data=mr, headers=headers)
                        res = json.loads(r.text)
                        if r.status_code != 200:
                            success = "false"
                            detail = "Problem in images"

                        if success == "false":
                            break
                        temp = {
                            "_source": "FRONTEND_API_SOURCE",
                            "source": res[0]["source"],
                            "main": res[0]["main"],
                            "thumbnail": res[0]["thumbnail"]
                        }
                        files["images"].append(temp)
                        if len(files["images"]) == 20:
                            break
                else:
                    files = {
                        "cover": "",
                        "images": []
                    }
                    allimages = postdata["post_images"][:21]
                    for i in range(len(allimages)):
                        im = open(os.getcwd()+"/"+allimages[i], 'rb')
                        mr = MultipartEncoder(
                            fields={
                                "type": "listing",
                                "uploadImages": (im.name, im, 'image/'+im.name[-1])
                            }
                        )
                        headers['content-type'] = mr.content_type
                        r = httprequestObj.http_post(
                            'https://api.baania.com/api/v1/uploadImages', data=mr, headers=headers)
                        res = json.loads(r.text)
                        if r.status_code != 200:
                            success = "false"
                            detail = "Problem in images"

                        if success == "false":
                            break
                        temp = {
                            "_source": "FRONTEND_API_SOURCE",
                            "source": res[0]["source"],
                            "main": res[0]["main"],
                            "thumbnail": res[0]["thumbnail"]
                        }
                        if i == 0:
                            files["cover"] = temp
                        else:
                            files["images"].append(temp)

            if success == "true" and len(allimages) != 0:
                headers['content-type'] = 'application/json'
                # print(files)
                r = requests.patch('https://api.baania.com/api/v1/users/listings/' +
                                   pid+'/3', data=json.dumps(files).encode('utf-8'), headers=headers)
                data = json.loads(r.text)
                # print(r)
                # print(r)
                # print(data)
                if r.status_code != 200:
                    success = "false"
                    detail = data["message"]

            if success == "true":
                datapost = {
                    "title_th": postdata["post_title_th"],
                    "contact_name": postdata["name"],
                    "contact_tel": postdata["mobile"],
                    "description_th": postdata["post_description_th"],
                    "is_publish": 1
                }

                r = requests.patch('https://api.baania.com/api/v1/users/listings/' +
                                   pid+'/4', data=json.dumps(datapost).encode('utf-8'), headers=headers)
                data = json.loads(r.text)
                # print(r)
                # print(data)
                if r.status_code != 200:
                    success = "false"
                    detail = data["message"]

                post_id = pid
                post_url = 'https://www.baania.com/th/listing/' + \
                    postdata["post_title_th"]+'-'+pid

        else:
            detail = "cannot login"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "baania",
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "end_time": str(time_end),
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
        }

    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process

        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]

        if success == "true":

            datapost = {
                'delete': {
                    'type': "other",
                    'remark': "specific"
                }
            }
            headers = {
                'authorization':  'Bearer ' + test_login['login_token'],
                'content-type': 'application/json',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
            }
            r = requests.delete(
                'https://api.baania.com/api/v1/users/listings/'+postdata['post_id'], data=json.dumps(datapost), headers=headers)
            data = r.text
            if r.status_code != 200:
                success = "false"
                detail = "Wrong Post Id"

        else:
            success = "false"
            detail = "cannot login"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "baania",
            "success": success,
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": postdata['post_id'],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail
        }
    def search_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""
        post_modify_time = ""
        post_view = ""
        post_found = "false"
            
        if success == "true":
            post_title = postdata['post_title_th']
            # exists, authenticityToken, post_title = self.check_post(post_id)
            # print(test_login['login_token'])
            headers = {
                'authorization':  'Bearer ' + test_login['login_token'],
                'content-type': 'application/json',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
            }

            url = "https://api.baania.com/api/v1/users/listings?filter[filter_query]={%22$or%22:%20[{%22code%22:%20{%22$regex%22:%22"+post_title+"%22}},%20{%22title_th%22:%20{%22$regex%22:%22"+post_title+"%22}},%20{%22keyId%22:%20{%22$regex%22:%22"+post_title+"%22}}]}&sort=-updated_at"
            r = requests.get(url,headers=headers)
            myans = json.loads(r.content.decode('utf-8'))
            if len(myans['data']) > 0 and post_title==myans['data'][0]['title_th']:
                post_id=myans['data'][0]['keyId']
                post_found='true'
                detail = "post found successfully"
                exists = True
                post_modify_time = myans['data'][0]['updated_at']
                post_view = myans['data'][0]['pageviews']
                post_url = "https://www.baania.com/th/listing/"+post_title+"-"+post_id
            else:
                exists = False
            if not exists:
                success = "false"
                detail = "No post found with given title."

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": "true",
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": "baania",
            "account_type":None,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "post_modify_time": post_modify_time,
            "post_view": post_view,
            "post_url": post_url,
            "post_found": post_found,
            "ds_id": postdata['ds_id']
        }


    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        post_id = postdata['post_id']
        log_id = postdata['log_id']

        #
        #

        time_end = datetime.datetime.utcnow()
        return {
            "websitename": "baania",
            "success": "false",
            "time_usage": time_end - time_start,
            "start_time": time_start,
            "end_time": time_end,
            "detail": "Cannot Edit & Save the post",            
            'ds_id': postdata['ds_id'],
            "log_id": log_id,
            "post_id": post_id,
            "ds_id": postdata['ds_id']
        }

    def print_debug(self, msg):
        if(self.debug == 1):
            print(msg)
        return "true"

    def print_debug_data(self, data):
        if(self.debugdata == 1):
            print(data)
        return "true"

        if(self.debugdata == 1):
            print(data)
        return "true"


# tri = baania()
# dic = {
#     "action": "create_post",
#     "timeout": "5",
#     "post_images": [
#         '../../../../../Pictures/cafeTerrance.jpg',
#         '../../../../../Pictures/cafeTerrance.jpg'
#     ],
#     "name_th": "อัมรินทร์",
#     "surname_th": "บุญเกิด",
#     "geo_latitude": "13.786862",
#     "geo_longitude": "100.757815",
#     "property_id": "",
#     "post_title_th": "newxxxx",
#     "short_post_title_th": "xxx",
#     "post_description_th": "ขายที่ดินด่วน บางกรวยไทรน้อย 6 ไร่ เหมาะทำตลาดรายละเอียดที่ดินขนาด 6 ไร่หน้ากว้าง 30 เมตร ติดถนนบางกรวยไทรน้อยที่ดินยังไม่ถมต่ำกว่าถนนประมาณ 1 เมตรสถานที่ใกล้เคียงถนนพระราม5ถนนนครอินทร์ให้เช่าระยะยาว 100,000 บาท ต่อเดือนสนใจติดต่อ คุณชู 0992899999line: 0992899999",
#     "post_title_en": "",
#     "short_post_title_en": "xxx",
#     "post_description_en": "",
#     "price_baht": "3000",
#     "project_name": "ลุมพีนีวิลล รามอินทราหลักสี่",

#     "listing_type": "ข",
#     "property_type": "คอนโด",
#     "floor_level": None,
#     "floor_total": None,
#     "floor_area": None,
#     "bath_room": None,
#     "bed_room": None,
#     "prominent_point": "จุดเด่น",
#     "view_type": "11",
#     "direction_type": "11",
#     "addr_province": "กระบี่",
#     "addr_district": "เกาะลันตา",
#     "addr_sub_district": "คลองยาง",
#     "addr_road": "ถนน",
#     "addr_soi": "ซอย",
#     "addr_near_by": "สถานที่ใกล้เคียง",
#     "floorarea_sqm": "พื้นที่",

#     "land_size_rai": "10",
#     "land_size_ngan": "1",
#     "land_size_wa": "12",

#     "name": "namehaha",
#     "mobile": "9899999999",
#     "tel": "9899999999",
#     "email": "reh37681@fft-mal.com",
#     "line": "9899999999",
#     "ds_name": "thaihometown",
#     "ds_id": "4",
#     "user": "reh37681@fft-mal.com",
#     "pass": "12345678",
#     "post_id": "5e9e069b20aaba0019a465b8"
# }

# dic = {'ds_name': 'baania',
#        'ds_id': '120',
#        'user': 'reh37681@fft-mal.com',
#        'pass': '12345678', 'action': 'create_post',
#        'timeout': '5',
#        'project_name': 'ลุมพีนีวิลล รามอินทราหลักสี่',
#        'post_img_url_lists':
#        ['https://www.bangkokassets.com/property/250064/2199951_83636pic7.jpg',
#         'https://www.bangkokassets.com/property/250064/2199952_83636pic8.jpg'],
#        'geo_latitude': '13.786862',
#        'geo_longitude': '100.757815',
#        'property_id': 'chu001',
#        'post_title_th': 'ให้เช่า ที่ดินด่วน บางกรวยไทรน้อย 6 ไร่ เหมาะทำตลาดสด เปิดท้าย',
#        'post_description_th': 'ขายที่ดินด่วน บางกรวยไทรน้อย 6 ไร่ เหมาะทำตลาดรายละเอียดที่ดินขนาด 6 ไร่หน้ากว้าง 30 เมตร ติดถนนบางกรวยไทรน้อยที่ดินยังไม่ถมต่ำกว่าถนนประมาณ 1 เมตรสถานที่ใกล้เคียงถนนพระราม5ถนนนครอินทร์ให้เช่าระยะยาว 100,000 บาท ต่อเดือนสนใจติดต่อ คุณชู 0992899999line: 0992899999',
#        'post_title_en': 'Land for rent bangkloysainoi 6 rai suitable for developing',
#        'post_description_en': 'Land for rent bangkloysainoi 6 rai suitable for developingLand Size 6 raiWidth 30 meter',
#        'price_baht': '100000',
#        'listing_type': 'เช่า',
#        'property_type': '6',
#        'prominent_point ': 'หน้ากว้างมาก ให้เช่าถูกสุด',
#        'direction_type': '11',
#        'addr_province': 'นนทบุรี',
#        'addr_district': 'เมืองนนทบุรี',
#        'addr_sub_district': 'สวนใหญ่',
#        'addr_road': 'บางกรวย-ไทรน้อย',
#        'addr_soi': 'ซอยบางกรวย-ไทรน้อย 34',
#        'addr_near_by': 'ถนนพระราม5ถนนนครอินทร์',
#        'land_size_rai': '6',
#        'land_size_ngan': '0',
#        'land_size_wa': '0',
#        'name': 'ชู',
#        'mobile': '0992899999',
#        'email': 'reh37681@fft-mal.com',
#        'line': '0992899999',
#        'post_images': ['../../../../../Pictures/cafeTerrance.jpg',
#                        '../../../../../Pictures/cafeTerrance.jpg']
#        }
# # dic={"action": "register_user", "timeout": "7", "ds_name": "home2all", "ds_id": "4", "user": "kaxiye5250@johnderasia.com", "pass": "123456aa",
# #  "company_name": "whatthefycj", "name_title": "", "name_th": "\u0e4c", "surname_th": "uea", "name_en": "", "surname_en": "", "tel": "9865345889", "line": "1234567899", "post_id":"788747"}
# # dic = {"user": "sobif61866@homedepinst.com", "email": "sobif61866@homedepinst.com", "post_id": "82860", "pass": '123456aa', "addr_soi": "xyz", 'post_images': [],
# #        "addr_road": "123", "addr_sub_district": "abc", "addr_district": "bbc", 'addr_province': "กระบี่", 'property_type': 'ที่ดิน',
# #        "post_title_th": "ppppppppp", "post_description_th": "ahhahahaha", "price_baht": "128", 'name': 'shikhar',
# #        'mobile': '', "tel": "0891999450", "name_th": "อัมรินทร์", "surname_th": "บุญเกิด", }
# print(tri.create_post(dic))
# {"user":"shikhar100mit@gmail.com","email": "rohibe8488@gotkmail.com", "id": "823", "pass": 12345678, "addr_soi": "xyz", "post_img_url_lists": ["http://pngimg.com/uploads/birds/birds_PNG115.png","http://pngimg.com/uploads/birds/birds_PNG111.png"],
# "addr_road": "123", "addr_sub_district": "abc", "addr_district": "bbc","addr_province": "กระบี่", "property_type": "1","post_title_th": "ppppppppp", "post_description_th": "ahhahahaha", "price_baht": "128", "name": "shikhar",        "mobile": ""}
