# -*- coding: utf-8 -*-

from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
# from urlparse import urlparse
import re
import json
import datetime
import sys

httprequestObj = lib_httprequest()


class ddproperty():

    name = 'ddproperty'

    def __init__(self):

        try:
            import configs
        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.debug = 0
        self.debugresdata = 0

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
        tel = list(tel)
        del tel[0]
        newtel = ''.join(tel)

        # จะต้องไปหน้า from login ก่อน เพื่อเก็บ session อะไรซักอย่าง จึงจะสามารถ post ไป register ได้
        r = httprequestObj.http_get('https://www.ddproperty.com/agent-register?package=TRIAL', verify=False)
        data = r.text
        f = open("ddloginfrom.html", "wb")
        f.write(data.encode('utf-8').strip())

        datapost = {
            'agency_id': 'OTHER',
            'otheragency-th-text': company_name,
            'otheragency-en-text': company_name,
            'otheragency': '',
            'job_title-th-text': '',
            'job_title-en-text': '',
            'job_title': '',
            'title': name_title,
            'firstname-th-text': name_th,
            'firstname-en-text': '',
            'firstname': '',
            'lastname-th-text': surname_th,
            'lastname-en-text':  '',
            'lastname': '',
            'birthDay': 10,
            'birthMonth': 10,
            'birthYear': 1986,
            'email': user,
            'mobile': newtel,
            'region': 'TH37',
            'city_area': '',
            'password': passwd,
            'password_confirm': passwd,
            'communication_us': 1,
            'submit': 'Submit',
            'months': ''
        }

        r = httprequestObj.http_post('https://www.ddproperty.com/agent-register', data=datapost)
        data = r.text
        f = open("ddregister.html", "wb")
        f.write(data.encode('utf-8').strip())

        register_success = "true"
        detail = ""
        if re.search('distil_r_captcha.html', data):
            register_success = "false"
            detail = "Operation die by Google reCAPTCHA"
        #
        # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": register_success,
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
        ds_name = "ddproperty"
        if (postdata["ds_name"]):
            ds_name = postdata["ds_name"]
        ds_id = ""
        if (postdata["ds_id"]):
            ds_id = postdata["ds_id"]

        # start process
        #
        success = "true"
        detail = ""
        agent_id = ""

        datapost = {
            'email': user,
        }
        r = httprequestObj.http_post('https://agentnet.ddproperty.com/is_authentic_user', data=datapost)
        data = r.text
        f = open("ddauthentic.html", "wb")
        f.write(data.encode('utf-8').strip())
        datajson = r.json()
        # if logged in ,session is 0 cause  {"status":0,"name":"\u0e14\u0e39\u0e14\u0e35 \u0e14\u0e2d\u0e17\u0e04\u0e2d\u0e21","email":"kla.arnut@hotmail.com","profile":"https:\/\/th1-cdn.pgimgs.com\/agent\/10760807\/APHO.74655966.C100X100.jpg"}
        if datajson['status'] and datajson['status'] == 0:
            if datajson['email'] != user:
                success = "false"
                detail = data
        if success == "true":
            datapost = {
                'password': passwd,
                'recapchaResponse': '',
                'remember_me': 'true',
                'submit': 'true',
                '': 'true',
                'userid': user,
            }
            r = httprequestObj.http_post('https://agentnet.ddproperty.com/ex_login_ajax', data=datapost)
            data = r.text
            f = open("logindd.html", "wb")
            f.write(data.encode('utf-8').strip())
            matchObj = re.search(r'success', data)
            if matchObj:
                agent_id = re.search(r'jwt_prod_(\d+)', data).group(1)
            else:
                success = "false"
                detail = "cannot login"
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
            "agent_id": agent_id
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
        # account_type = postdata["account_type"]
        # postdata['user'] = 'kla.arnut@gmail.com'
        user = postdata['user']
        # postdata['pass'] = 'vkIy9b'
        passwd = postdata['pass']
        # project_name = postdata["project_name"]

        # start process
        #

        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        agent_id = test_login["agent_id"]
        post_id = ""

        if success == "true":
            # post
            agent_id = agent_id
            datapost = {
                "id": "",
                "title": post_title_en,
                "localizedTitle": post_title_th,
                "description": post_description_en,
                "localizedDescription": post_description_th,
                "hasStream": "false",
                "statusCode": "DRAFT",
                "sourceCode": "",
                "typeCode": "SALE",
                "leaseTermCode": "",
                "featureCode": "",
                "externalId": 9999,
                "event": "",
                "location": {
                    "id": "626225",
                    "block": "",
                    "unit": "",
                    "streetId": "",
                    "longitude": geo_longitude,
                    "latitude": geo_latitude,
                    "hdbEstateCode": "",
                    "streetName1": "",
                    "streetName2": "",
                    "streetNumber": "",
                    "postalCode": "11110",
                    "regionCode": "TH12",
                    "districtCode": "TH1203",
                    "areaCode": "11",
                    "zoneIds": ""
                },
                "media": {
                    "cover": {
                        "id": ""
                    },
                    "excluded": [],
                    "included": []
                },
                "property": {
                    "id": 5987,
                    "name": "Plum condo central station เฟส 1",
                    "temporaryId": "",
                    "typeCode": "CONDO",
                    "typeGroup": "N",
                    "tenureCode": "",
                    "topYear": "",
                    "totalUnits": 1208,
                    "floors": 38,
                    "amenities": []
                },
                "propertyUnit": {
                    "tenureCode": "",
                    "furnishingCode": "",
                    "description": "",
                    "hdbTypeCode": "",
                    "floorplanId": -1,
                    "floorLevelCode": "",
                    "floorPosition": "",
                    "telephoneLines": "",
                    "cornerUnit": "",
                    "facingCode": "",
                    "features": [],
                    "occupancyCode": "",
                    "electricitySupply": "",
                    "electricityPhase": "",
                    "ceilingHeight": "",
                    "floorLoading": "",
                    "parkingSpaces": "",
                    "parkingFees": "",
                    "maintenanceFee": "",
                    "liftCargo": "",
                    "liftPassenger": "",
                    "liftCapacity": "",
                    "centralAircon": "",
                    "centralAirconHours": "",
                    "ownerTypeCode": "",
                    "sellerEthnic": "",
                    "sellerResidency": "",
                    "quotaEthnic": "false",
                    "quotaSpr": "false",
                    "tenancy": {
                        "value": "",
                        "tenantedUntilDate": {}
                    }
                },
                "price": {
                    "value": 9999999,  # price_baht ใช้ price bath 3000 แล้ว error,
                    "periodCode": "",
                    "valuation": "",
                    "type": {
                        "code": "BAH",
                        "text": ""}},
                "sizes": {
                    "bedrooms": {
                        "value": ""},
                    "bathrooms": {
                        "value": ""},
                    "extrarooms": {
                        "value": ""},
                    "floorArea": [{"value": 44, "unit": "sqm"}],
                    "landArea": [{"value": "", "unit": "sqm"}],
                    "floorX": [{"unit": "m", "value": ""}],
                    "floorY": [{"unit": "m", "value": ""}],
                    "landX": [{"unit": "m", "value": ""}],
                    "landY": [{"unit": "m", "value": ""}]},
                "agent": {"id": agent_id,
                          "alternativePhone": "",
                          "alternativeAgent": "",
                          "alternativeMobile": "",
                          "alternativeEmail": ""},
                "hasFloorplans": "false",
                "boost": {"boostActive": "false", "boostDuration": 0},
                "dates": {"timezone": "Asia/Singapore", "available": ""},
                "descriptions": {
                    "th": post_description_th},
                "qualityScore": 0,
                "localizedHeadline": "",
                "headlines": {"th": ""},
                "titles": {"th": post_title_th}
            }
            datastr = json.dumps(datapost)
            r = httprequestObj.http_post_json('https://agentnet.ddproperty.com/sf2-agent/ajax/listings', jsoncontent=datastr)
            data = r.text
            # f = open("postdd.html", "wb")
            # f.write(data.encode('utf-8').strip())
            matchObj = re.search(r'errors', data)
            if matchObj:
                success = "false"
                detail = data
            else:
                post_id = re.search(r'{"id":(\d+)', data).group(1)
            #
            # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": ds_id,
            "post_url": "https://www.ddproperty.com/preview-listing/"+post_id if post_id != "" else "",
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
        }

    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        post_id = postdata['post_id']
        log_id = postdata['log_id']
        user = postdata['user']
        passwd = postdata['pass']

        # start process
        #

        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        agent_id = test_login["agent_id"]
        if success == "true":
            datapost = {
                "country": "th",
                "session": "3B7EC6629ADB7BD3ADEA8CFD4F91E7D3"  # TODO จะใช้ได้ตลอดไปมั้ย
            }
            datajson = json.dumps(datapost)
            headerreg = {"content-type": "application/json"}
            r = httprequestObj.http_post_with_multi_options('https://auth.propertyguru.com/session-to-jwt', headerreg=headerreg, jsoncontent=datajson)
            data = r.text
            #f = open("ddsessiontojwt.html", "wb")
            # f.write(data.encode('utf-8').strip())
            jsonres = r.json()
            if not jsonres["token"]:
                success == "false"
                detail = jsonres
            if success == "true":
                headerreg = {
                    "content-type": "application/json",
                    "authorization": "Bearer " + jsonres["token"]
                }
                #r = httprequestObj.http_post_with_multi_options('https://ads-products.propertyguru.com/api/v1/listing/7797845/product/ranked-spotlight/add?region=th&agentId=10760807', headerreg=headerreg, jsoncontent={})
                r = httprequestObj.http_post_with_multi_options('https://ads-products.propertyguru.com/api/v1/listing/'+post_id+'/product/ranked-spotlight/add?region=th&agentId='+agent_id, headerreg=headerreg, jsoncontent={})
                data = r.text
                f = open("ddboostpostresponse.html", "wb")
                f.write(data.encode('utf-8').strip())

                # TODO ถ้า boost สำเร็จ response จะเป็นยังไง
                success = "false"
                detail = data + " ต้องมี credit จริง เพื่อเก็บ response เวลา boost post สำเร็จ"

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
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        log_id = postdata['log_id']
        #postdata['post_id'] = '7790593'
        post_id = postdata['post_id']
        #postdata['user'] = 'kla.arnut@gmail.com'
        user = postdata['user']
        #postdata['pass'] = 'vkIy9b'
        passwd = postdata['pass']

        # start process
        #
        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]

        if success == "true":
            # จะต้องไปหน้า listing_management เพื่อเก็บ session อะไรซักอย่าง จึงจะสามารถ post ไป delete ได้
            r = httprequestObj.http_get('https://agentnet.ddproperty.com/listing_management#DRAFT', verify=False)
            data = r.text
            #f = open("ddpostlistdraft.html", "wb")
            # f.write(data.encode('utf-8').strip())

            # listing_id%5B%5D=7788093&remove=Delete%20selected&selecteds=7788093
            datapost = {
                "listing_id[]": post_id,
                "remove": "Delete selected",
                "selecteds": post_id,
            }
            r = httprequestObj.http_post('https://agentnet.ddproperty.com/remove_listing', data=datapost)
            data = r.text
            f = open("dddelete.html", "wb")
            f.write(data.encode('utf-8').strip())
            matchObj = re.search(r'message":"deleted', data)
            if matchObj:
                # ใกล้ความจริง แต่จะ delete สำเร็จหรือไม่มันก็ return deleted หมด ดังนั้นต้องเช็คจาก post id อีกทีว่า response 404 ป่าว
                r = httprequestObj.http_get('https://agentnet.ddproperty.com/create-listing/detail/'+post_id, verify=False)
                data = r.text
                f = open("dddelete.html", "wb")
                f.write(data.encode('utf-8').strip())
                if(r.status_code == 200):
                    success = "false"
                    detail = r.text

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
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # post_img_url_lists = postdata['post_img_url_lists']
        price_baht = postdata['price_baht']
        # county = postdata["county"]
        # district = postdata["district"]
        # addr_province = postdata['addr_province']
        # addr_district = postdata['addr_district']
        # addr_sub_district = postdata['addr_sub_district']
        # addr_road = postdata['addr_road']
        # addr_near_by = postdata['addr_near_by']
        # floorarea_sqm = postdata['floorarea_sqm']
        # geo_latitude = postdata['geo_latitude']
        # geo_longitude = postdata['geo_longitude']
        # property_id = postdata['property_id']
        post_title_th = postdata['post_title_th']
        post_description_th = postdata['post_description_th']
        # post_title_en = postdata['post_title_en']
        # post_description_en = postdata['post_description_en']
        # postdata["post_id"] = '7788091'
        post_id = postdata["post_id"]
        # postdata['user'] = 'kla.arnut@gmail.com'
        user = postdata['user']
        # postdata['pass'] = 'vkIy9b'
        passwd = postdata['pass']
        log_id = postdata["log_id"]

        # start proces
        #

        # login
        self.test_login(postdata)
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        agent_id = test_login["agent_id"]

        if (success == "true"):
            datapost = {
                "id": post_id,
                "statusCode": "DRAFT",
                "daysUntilExpire": 0,
                "isExpiring": "true",
                "sourceCode": "",
                "typeCode": "SALE",
                "typeText": "ขาย",
                "subTypeCode": "",
                "leaseTermCode": "",
                "leaseTermText": "",
                "featureCode": "",
                "accountTypeCode": "NORMAL",
                "accountSubTypeCode": "",
                "isPremiumAccount": "false",
                "isPropertySpecialistListing": "false",
                "isMobilePropertySpotlightListing": "false",
                "isTransactorListing": "false",
                "isCommercial": "false",
                "hasFloorplans": "false",
                "hasStream": "true",
                "featuredBy": [

                ],
                "localizedHeadline": "",
                "headlines": {
                    "th": "",
                    "en": ""
                },
                "localizedTitle": post_title_th,
                "titles": {
                    "th": post_title_th
                },
                "localizedDescription": post_description_th,
                "descriptions": {
                    "th": post_description_th
                },
                "notes": "",
                "externalId": 9999,
                "cobroke": 0,
                "price": {
                    "value": 9999999,
                    "pretty": "฿9,999,999",
                    "periodCode": "",
                    "pricePerArea": {
                        "value": 227272.7045,
                        "unit": "sqm",
                        "reference": "floorArea"
                    },
                    "type": {
                        "code": "BAH",
                        "text": "",
                        "pretty": "บาท"
                    },
                    "valuation": 0,
                    "valuationText": "",
                    "completed": 0,
                    "currency": "฿"
                },
                "sizes": {
                    "bedrooms": {
                        "value": "",
                        "text": ""
                    },
                    "bathrooms": {
                        "value": "",
                        "text": ""
                    },
                    "extrarooms": {
                        "value": "",
                        "text": ""
                    },
                    "floorArea": [
                        {
                            "unit": "sqm",
                            "value": 44,
                            "text": "44 ตร.ม."
                        }
                    ],
                    "landArea": [
                        {
                            "unit": "sqm",
                            "value": "",
                            "text": ""
                        }
                    ],
                    "floorX": [
                        {
                            "unit": "m",
                            "value": ""
                        }
                    ],
                    "floorY": [
                        {
                            "unit": "m",
                            "value": ""
                        }
                    ],
                    "landX": [
                        {
                            "unit": "m",
                            "value": ""
                        }
                    ],
                    "landY": [
                        {
                            "unit": "m",
                            "value": ""
                        }
                    ]
                },
                "pricePerArea": {
                    "floorArea": [
                        {
                            "unit": "sqm",
                            "value": 227272.70454545,
                            "text": "฿227,273 / ตารางเมตร"
                        }
                    ],
                    "landArea": [
                        {
                            "unit": "",
                            "value": "",
                            "text": ""
                        }
                    ]
                },
                "dates": {
                    "timezone": "Asia/Singapore",
                    "firstPosted": "",
                    "lastPosted": "",
                    "expiry": "",
                    "available": "",
                    "created": {
                        "date": "2020-03-11 01:14:38",
                        "unix": 1583860478
                    },
                    "updated": {
                        "date": "2020-03-11 01:14:38",
                        "unix": 1583860478
                    }
                },
                "urls": {
                    "listing": {
                        "api": "https://api.propertyguru.com/v1/listings/7788091?region=th",
                        "internal": "http://listing.guruestate.com/v1/listings/7788091?region=th",
                        "mobile": "https://www.ddproperty.com/property/xxx-ขาย-7788091",
                        "desktop": "https://www.ddproperty.com/property/xxx-ขาย-7788091",
                        "desktopByLocales": {
                            "th": "https://www.ddproperty.com/property/xxx-ขาย-7788091",
                            "en": "https://www.ddproperty.com/en/property/xxx-for-sale-7788091"
                        },
                        "preview": {
                            "desktop": "https://www.ddproperty.com/preview-listing/7788091"
                        }
                    }
                },
                "_user": "",
                "qualityScore": 70,
                "finalScore": "",
                "tier": 0,
                "showAgentProfile": "false",
                "event": "",
                "mywebOrder": "",
                "agent": {
                    "id": agent_id,
                    "name": "cccc cccc",
                    "mobile": "+66839703921",
                    "mobilePretty": "+66 83 970 3921",
                    "phone": "",
                    "phonePretty": "",
                    "alternativePhone": "",
                    "alternativeAgent": "",
                    "alternativeMobile": "",
                    "alternativeEmail": "",
                    "jobTitle": "",
                    "licenseNumber": "",
                    "showProfile": "false",
                    "website": "",
                    "email": "kla.arnut@gmail.com",
                    "blackberryPin": ""
                },
                "agency": {
                    "id": 42297,
                    "name": "aaaa",
                    "ceaLicenseNumber": ""
                },
                "location": {
                    "id": 626225,
                    "latitude": 13.8749,
                    "longitude": 100.413606,
                    "distance": "",
                    "regionCode": "TH12",
                    "regionText": "นนทบุรี",
                    "regionSlug": "นนทบุรี",
                    "districtCode": "TH1203",
                    "districtText": "บางใหญ่",
                    "districtSlug": "บางใหญ่",
                    "areaCode": "11",
                    "areaText": "",
                    "areaSlug": "",
                    "fullAddress": ". ถนนรัตนาธิเบศร์ ตำบลเสาธงหิน อำเภอบางใหญ่ นนทบุรี, บางใหญ่, นนทบุรี",
                    "hdbEstateCode": "",
                    "hdbEstateText": "",
                    "postalCode": "11110",
                    "block": "",
                    "unit": "",
                    "streetId": "",
                    "streetName1": "ถนนรัตนาธิเบศร์ ตำบลเสาธงหิน อำเภอบางใหญ่ นนทบุรี",
                    "streetName2": "",
                    "streetNumber": ".",
                    "zoneIds": "",
                    "subZoneIds": ""
                },
                "property": {
                    "id": 5987,
                    "temporaryId": "",
                    "statusCode": "6DML",
                    "name": "Plum condo central station เฟส 1",
                    "typeCode": "CONDO",
                    "typeText": "คอนโด",
                    "typeGroup": "N",
                    "tenureCode": "F",
                    "tenureText": "ขายขาด",
                    "topMonth": 10,
                    "topYear": 2018,
                    "developer": "Pruksa Real Estate - พฤกษา เรียลเอสเตท จำกัด (มหาชน)",
                    "totalUnits": 1208,
                    "floors": 38,
                    "amenities": [
                        {
                            "code": "CCAR"
                        },
                        {
                            "code": "CTV"
                        },
                        {
                            "code": "FIT"
                        },
                        {
                            "code": "OCAR"
                        },
                        {
                            "code": "PDEC"
                        },
                        {
                            "code": "SAUNA"
                        },
                        {
                            "code": "SEC"
                        },
                        {
                            "code": "SPA"
                        },
                        {
                            "code": "STE"
                        },
                        {
                            "code": "SWI"
                        },
                        {
                            "code": "WAD"
                        }
                    ]
                },
                "propertyUnit": {
                    "id": 7989636,
                    "description": "",
                    "furnishingCode": "",
                    "furnishingText": "",
                    "hdbTypeCode": "",
                    "floorplanId": -1,
                    "floorLevelCode": "",
                    "floorLevelText": "",
                    "floorPosition": "",
                    "cornerUnit": "",
                    "facingCode": "",
                    "occupancyCode": "",
                    "electricitySupply": "",
                    "electricityPhase":  "",
                    "ceilingHeight": "",
                    "floorLoading": "",
                    "garages": "",
                    "parkingSpaces": "",
                    "parkingFees": "",
                    "maintenanceFee": {
                        "value": 0,
                        "pretty": "฿0.00",
                        "periodeCode": "MONTH"
                    },
                    "liftCargo": "",
                    "liftPassenger": "",
                    "liftCapacity": "",
                    "centralAircon": "",
                    "centralAirconHours": "",
                    "ownerTypeCode": "",
                    "sellerEthnic": "",
                    "sellerResidency":  "",
                    "quotaEthnic": "true",
                    "quotaSpr": "true",
                    "telephoneLines": "",
                    "features": [

                    ],
                    "tenancy": {
                        "value": "UNTENANTED",
                        "tenantedUntilDate": {

                        }
                    },
                    "tenureCode": "F"
                },
                "media": {
                    "cover": {
                        "id": 61330097,
                        "caption": "",
                        "statusCode": "CONF",
                        "suspReason": "",
                        "appealComment": "",
                        "appealSent": "false",
                        "sortOrder": 61330097,
                        "V150": "https://th2-cdn.pgimgs.com/property/5987/PPHO.61330097.V150/Plum-condo-central-station-%E0%B9%80%E0%B8%9F%E0%B8%AA-1-%E0%B8%9A%E0%B8%B2%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88-Thailand.jpg",
                        "V550": "https://th2-cdn.pgimgs.com/property/5987/PPHO.61330097.V550/Plum-condo-central-station-%E0%B9%80%E0%B8%9F%E0%B8%AA-1-%E0%B8%9A%E0%B8%B2%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88-Thailand.jpg"
                    },
                    "listing": [

                    ],
                    "property": [
                        {
                            "id": 61330097,
                            "caption": "",
                            "statusCode": "CONF",
                            "suspReason": "",
                            "appealComment": "",
                            "appealSent": "false",
                            "sortOrder": 61330097,
                            "V150": "https://th2-cdn.pgimgs.com/property/5987/PPHO.61330097.V150/Plum-condo-central-station-%E0%B9%80%E0%B8%9F%E0%B8%AA-1-%E0%B8%9A%E0%B8%B2%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88-Thailand.jpg",
                            "V550": "https://th2-cdn.pgimgs.com/property/5987/PPHO.61330097.V550/Plum-condo-central-station-%E0%B9%80%E0%B8%9F%E0%B8%AA-1-%E0%B8%9A%E0%B8%B2%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88-Thailand.jpg"
                        },
                        {
                            "id": 61330098,
                            "caption": "",
                            "statusCode": "CONF",
                            "suspReason": "",
                            "appealComment": "",
                            "appealSent": "false",
                            "sortOrder": 61330098,
                            "V150": "https://th1-cdn.pgimgs.com/property/5987/PPHO.61330098.V150/Plum-condo-central-station-%E0%B9%80%E0%B8%9F%E0%B8%AA-1-%E0%B8%9A%E0%B8%B2%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88-Thailand.jpg",
                            "V550": "https://th1-cdn.pgimgs.com/property/5987/PPHO.61330098.V550/Plum-condo-central-station-%E0%B9%80%E0%B8%9F%E0%B8%AA-1-%E0%B8%9A%E0%B8%B2%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88-Thailand.jpg"
                        },
                        {
                            "id": 61330099,
                            "caption": "",
                            "statusCode": "CONF",
                            "suspReason": "",
                            "appealComment": "",
                            "appealSent": "false",
                            "sortOrder": 61330099,
                            "V150": "https://th2-cdn.pgimgs.com/property/5987/PPHO.61330099.V150/Plum-condo-central-station-%E0%B9%80%E0%B8%9F%E0%B8%AA-1-%E0%B8%9A%E0%B8%B2%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88-Thailand.jpg",
                            "V550": "https://th2-cdn.pgimgs.com/property/5987/PPHO.61330099.V550/Plum-condo-central-station-%E0%B9%80%E0%B8%9F%E0%B8%AA-1-%E0%B8%9A%E0%B8%B2%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88-Thailand.jpg"
                        },
                        {
                            "id": 61330104,
                            "caption": "",
                            "statusCode": "CONF",
                            "suspReason": "",
                            "appealComment": "",
                            "appealSent": "false",
                            "sortOrder": 61330104,
                            "V150": "https://th1-cdn.pgimgs.com/property/5987/PPHO.61330104.V150/Plum-condo-central-station-%E0%B9%80%E0%B8%9F%E0%B8%AA-1-%E0%B8%9A%E0%B8%B2%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88-Thailand.jpg",
                            "V550": "https://th1-cdn.pgimgs.com/property/5987/PPHO.61330104.V550/Plum-condo-central-station-%E0%B9%80%E0%B8%9F%E0%B8%AA-1-%E0%B8%9A%E0%B8%B2%E0%B8%87%E0%B9%83%E0%B8%AB%E0%B8%8D%E0%B9%88-Thailand.jpg"
                        }
                    ],
                    "agent": "",
                    "agentLogo": [

                    ],
                    "agencyLogo": [

                    ],
                    "excluded": [

                    ],
                    "included": [

                    ],
                    "listingDocuments": [

                    ],
                    "propertyFloorplans": [

                    ],
                    "listingFloorplans": [

                    ],
                    "listingSiteplans": [

                    ],
                    "listingVideos": [

                    ],
                    "listingVirtualTours": [

                    ]
                },
                "metas": {
                    "title": "Xxx, . ถนนรัตนาธิเบศร์ ตำบลเสาธงหิน อำเภอบางใหญ่ นนทบุรี, บางใหญ่, นนทบุรี, 44 ตร.ม., คอนโด ขาย, โดย Cccc Cccc, ฿9,999,999, 7788091",
                    "description": "ดูรายละเอียด, รูปภาพ และแผนที่ของประกาศอสังหาริมทรัพย์ 7788091 - ขาย - xxx - . ถนนรัตนาธิเบศร์ ตำบลเสาธงหิน อำเภอบางใหญ่ นนทบุรี, บางใหญ่, นนทบุรี, 44 ตร.ม., ฿9,999,999",
                    "keywords": "ตัวแทน, ประกาศ, อสังหาริมทรัพย์, ทรัพย์สิน, ขาย, เช่า, อพาร์ทเม้นท์, บ้าน, ชาวต่างชาติ, ที่อยู่อาศัย, hdb, สถานที่ตั้ง, คอนโด, แผนที่"
                },
                "alertBatchId": "",
                "unitTypes": [

                ],
                "qualityScoreData": {
                    "price": 50,
                    "location": 10,
                    "3_user_photos": 0,
                    "1_user_photo": 0,
                    "videos_or_virtual_tours": 0,
                    "bedrooms": 0,
                    "description": 0,
                    "bathrooms": 0,
                    "floorarea": 5,
                    "landarea": 3,
                    "property": 1,
                    "furnishing": 0,
                    "unit_features": 0,
                    "property_photo": 1,
                    "raw_score": 70,
                    "score": 70
                },
                "dependencyErrors": [

                ],
                "isRankedSpotlight": "false",
                "isFeaturedListing": "false"
            }
            datastr = json.dumps(datapost)
            # print(datastr)
            r = httprequestObj.http_put_json('https://agentnet.ddproperty.com/sf2-agent/ajax/update/'+post_id, jsoncontent=datastr)
            data = r.text
            f = open("editpostdd.html", "wb")
            f.write(data.encode('utf-8').strip())

            matchObj = re.search(r'errors', data)
            if matchObj:
                success = "false"
                detail = data
            matchObj = re.search(r'Oops!', data)
            if matchObj:
                success = "false"
                detail = data

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

    def print_debug(self, msg):
        if(self.debug == 1):
            print(msg)
        return True

    def print_debug_data(self, data):
        if(self.debugdata == 1):
            print(data)
        return True
