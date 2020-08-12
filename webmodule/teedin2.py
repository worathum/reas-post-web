from urllib.parse import unquote
import sys
import time
import requests
from .lib_httprequest import *
import os
# import lib_httprequest
from bs4 import BeautifulSoup
import os.path
from urllib import parse
import re
import json
import datetime


with open("./static/teedin2.json") as f:
    provincedata = json.load(f)


class teedin2():

    name = 'teedin2'

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

        return {
            "success": "true",
            "time_usage": end_time - start_time,
            "start_time": start_time,
            "end_time": end_time,
            "detail": ""
        }

    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()

        success = "false"
        detail = "Website does not have Registration"

        end_time = datetime.datetime.utcnow()
        time_usage = end_time - start_time
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(start_time),
            "end_time": str(end_time),
            "detail": detail,
            "websitename": "teedin2",
        }

    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()

        success = "true"
        detail = "No Login Option in site"


        end_time = datetime.datetime.utcnow()
        time_usage = end_time - start_time
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(start_time),
            "end_time": str(end_time),
            "detail": detail,
            "ds_id": postdata['ds_id'],
            "websitename": "teedin2",
        }

    def edit_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()

        post_url = 'https://www.teedin2.com/detail/' + \
            postdata['post_id']+'.html'
        with requests.Session() as s:
            r = s.post(post_url)
        if postdata['post_id'] not in r.text:
            detail = "wrong post id"
            end_time = datetime.datetime.utcnow()
            time_usage = end_time - start_time
            return {
                'websitename': 'teedin2',
                'success': 'False',
                "start_time": str(start_time),
                "end_time": str(end_time),
                "detail": detail,
                "log_id": postdata['log_id']
            }
        ul_test = "https://www.teedin2.com/topic3Update.php"
        test = {
            'ID': postdata['post_id'],
            'action': '2',
            'thisCPasswordField': postdata['pass']
        }
        with requests.Session() as s:
            r = s.post(ul_test, data=test)
        if "A Database Error Occured while counting result Rows" in r.text:
            detail = "wrong post id"
            end_time = datetime.datetime.utcnow()
            time_usage = end_time - start_time
            return {
                'websitename': 'teedin2',
                'success': 'False',
                "start_time": str(start_time),
                "end_time": str(end_time),
                "detail": detail,
                "log_id": postdata['log_id']
            }
        subcategory = {
            '6': 1,
            '2': 2,
            '3': 2,
            '1': 3,
            '7': 3,
            '5': 3,
            '9': 3,
            '10': 3,
            '4': 2,
            '8': 3,
            '25': 3
        }
        try:
            postdata['cate_id'] = subcategory[str(postdata['property_type'])]
        except:
            return{
                'success': 'false',
                'websitename': 'teedin2',
                'detail': 'wrong propertytype',
                'ret': '',
                'post_url': '',
                'post_id': '',
                "log_id": postdata['log_id']
            }
        success = "true"
        post_id = ""
        detail = ""
        post_id = ""
        detail = ""
        url_n = "https://www.teedin2.com/topic2Create.php"
        postparams = {
            'acceptBTN': 'Accept all terms and conditions'
        }
        r = requests.post(url_n, data=postparams)
        soup = BeautifulSoup(r.content, 'html5lib')
        amphur_id = -1

        finalRegion = ""
        for i in range(6):
            province_id = str(i)
            for (key, value) in provincedata[province_id+"_province"].items():
                if postdata['addr_province'].strip() in value.strip():
                    amphur_id = key
                    finalRegion = str(i)
                    break
            if finalRegion != "":
                break
        # print(postdata['addr_province'])
        # print(finalRegion)
        if amphur_id == -1 or finalRegion == "":
            return{
                'websitename': 'teedin2',
                'success': 'false',
                'ret': "wrong province",
                'post_url': "",
                'post_id': "",
                "log_id": postdata['log_id']

            }
        province_id = amphur_id
        postdata['addr_province'] = province_id
        postdata['addr_region'] = finalRegion

        url_district = 'https://www.teedin2.com/data/amphurs.php'
        r = requests.post(url_district, data={
                          'ProvinceID': postdata['addr_province']})
        soup = BeautifulSoup(r.content, 'html5lib')
        var = soup.findAll('option')
        for i in var:
            if i.text == postdata['addr_district']:
                postdata['addr_amphurs'] = i['value']
                print(i.text)
        if 'addr_amphurs' not in postdata:
            return{
                'websitename': 'teedin2',
                'success': 'false',
                'ret': "wrong district",
                'post_url': "",
                'post_id': "",
                "log_id": postdata['log_id']

            }

        url_district = 'https://www.teedin2.com/data/districts.php'
        r = requests.post(url_district, data={
                          'AmphurID': postdata['addr_amphurs']})
        soup = BeautifulSoup(r.content, 'html5lib')
        var = soup.findAll('option')
        for i in var:
            # print(i.text)
            if i.text == postdata['addr_sub_district']:
                postdata['addr_districts'] = i['value']
                # print(i.text)
        if 'addr_districts' not in postdata:
            for i in var[1:]:
                postdata['addr_districts'] = i['value']
                break

        prod_address = ""
        for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
            if add is not None or add == "" or add == " ":
                prod_address += add + ","
        prod_address = prod_address[:-1]
        postdata['address'] = prod_address
        print(var)
        s = requests.Session()
        datapost = {
            'thisIDField': postdata['post_id'],
            'action': '4',
            'thisForSaleField': '1',
            'thisTypeField': subcategory[str(postdata['property_type'])],
            'thisTitleField': postdata['post_title_th'],
            'thisRegionIDField': postdata['addr_region'],
            'thisProvinceIDField': postdata['addr_province'],
            'thisAmphurIDField': postdata['addr_amphurs'],
            'thisDistrictIDField': postdata['addr_districts'],
            'thisDetailField': postdata['post_description_th'],
            'thisSize1Field': postdata['land_size_wa'],
            'thisSize2Field': postdata['land_size_rai'],
            'thisSize3Field': postdata['land_size_ngan'],
            'thisDeedTypeField': 20,
            'thisLatitudeField': postdata['geo_latitude'],
            'thisLongitudeField': postdata['geo_longitude'],
            'thisCNameField': postdata['name'],
            'thisCPhoneField': postdata['mobile'],
            'thisCEmailField': postdata['user'],
            'thisCPasswordField': postdata['pass'],
        }
        if float(postdata['geo_longitude']) < float(postdata['geo_latitude']):
            pass
        else:
            datapost['thisHasMapField'] = 1
        arr = ["pictureField1", "pictureField2",
               "pictureField3", "pictureField4", "pictureField5"]
        files = {}
        for i in range(len(postdata['post_images'])):
            datapost[arr[i]] = postdata['post_images'][i]
            files[arr[i]] = (postdata['post_images'][i], open(
                postdata['post_images'][i], "rb"), "image/jpeg")
            if i == 4:
                break
        detail = ""
        with requests.Session() as s:
            r = s.post(url_n, data=datapost, files=files)
            detail = r.text
        post_url = 'https://www.teedin2.com/detail/' + \
            postdata['post_id']+'.html'
        with requests.Session() as s:
            r = s.post(post_url)
        success = "true"
        end_time = datetime.datetime.utcnow()
        time_usage = end_time - start_time
        return {
            "success": success,
            'websitename': 'teedin2',
            "start_time": str(start_time),
            "end_time": str(end_time),
            "detail": "Edited ",
            "log_id": postdata['log_id']

        }

    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()

        subcategory = {
            '6': 1,
            '2': 2,
            '3': 2,
            '1': 3,
            '7': 3,
            '5': 3,
            '9': 3,
            '10': 3,
            '4': 2,
            '8': 3,
            '25': 3
        }
        try:
            postdata['cate_id'] = subcategory[str(postdata['property_type'])]
        except:
            return{
                'success': 'false',
                'websitename': 'teedin2',
                'ret': 'wrong propertytype',
                'post_url': '',
                'post_id': '',
                "ds_id": postdata['ds_id']
            }
        if 'name' not in postdata:
            return{
                'websitename': 'teedin2',
                'success': 'false',
                'ret': 'Missing required field name',
                'post_url': '',
                'post_id': '',
                "ds_id": postdata['ds_id']

            }
        if 'mobile' not in postdata:
            return{
                'websitename': 'teedin2',
                'success': 'false',
                'ret': 'Missing required field mobile',
                'post_url': '',
                'post_id': '',
                "ds_id": postdata['ds_id']

            }
        if 'pass' not in postdata:
            return{
                'websitename': 'teedin2',
                'success': 'false',
                'ret': 'Missing required field pass',
                'post_url': '',
                'post_id': '',
                "ds_id": postdata['ds_id'],

            }
        if 'user' not in postdata:
            return{
                "ds_id": postdata['ds_id'],
                'websitename': 'teedin2',
                'success': 'false',
                'ret': 'Missing required field email',
                'post_url': '',
                'post_id': ''
            }
        if 'property_type' not in postdata:
            return{
                "ds_id": postdata['ds_id'],
                'websitename': 'teedin2',
                'success': 'false',
                'ret': 'Missing required field property_type',
                'post_url': '',
                'post_id': ''
            }
        if 'listing_type' not in postdata:
            return{
                "ds_id": postdata['ds_id'],
                'websitename': 'teedin2',
                'success': 'false',
                'ret': 'Missing required field listing_type',
                'post_url': '',
                'post_id': ''
            }
        if 'price_baht' not in postdata:
            return{
                "ds_id": postdata['ds_id'],
                'websitename': 'teedin2',
                'success': 'false',
                'ret': 'Missing required field price',
                'post_url': '',
                'post_id': ''
            }
        if 'post_title_th' not in postdata:
            return{
                "ds_id": postdata['ds_id'],
                'websitename': 'teedin2',
                'success': 'false',
                'detail': 'Missing required field title',
                'ret': '',
                'post_url': '',
                'post_id': ''
            }
        if 'post_description_th' not in postdata:
            return{
                "ds_id": postdata['ds_id'],
                'websitename': 'teedin2',
                'success': 'false',
                'ret': 'Missing required field description',
                'post_url': '',
                'post_id': ''
            }

        success = "true"
        post_id = ""
        detail = ""
        post_id = ""
        detail = ""
        url_n = "https://www.teedin2.com/topic2Create.php"
        postparams = {
            'acceptBTN': 'Accept all terms and conditions'
        }
        r = requests.post(url_n, data=postparams)
        soup = BeautifulSoup(r.content, 'html5lib')
        amphur_id = -1

        finalRegion = ""
        postdata['addr_province'] = postdata['addr_province'].replace(' ', '')
        for i in range(7):
            province_id = str(i)
            for (key, value) in provincedata[province_id+"_province"].items():
                if postdata['addr_province'].strip() in value.strip():
                    amphur_id = key
                    finalRegion = str(i)
                    break
            if finalRegion != "":
                break
        if amphur_id == -1 or finalRegion == "":
            return{
                'websitename': 'teedin2',
                'success': 'false',
                'ret': "wrong province",
                'post_url': "",
                "ds_id": postdata['ds_id'],
                'post_id': ""
            }
        province_id = amphur_id
        print(postdata['addr_province'])
        postdata['addr_province'] = province_id
        postdata['addr_region'] = finalRegion
        postdata['addr_district'] = postdata['addr_district'].replace(' ', '')
        print(postdata['addr_district'])
        print(postdata['addr_sub_district'])
        url_district = 'https://www.teedin2.com/data/amphurs.php'
        r = requests.post(url_district, data={
                          'ProvinceID': postdata['addr_province']})
        soup = BeautifulSoup(r.content, 'html5lib')
        var = soup.findAll('option')
        for i in var:
            if i.text in postdata['addr_district']:
                postdata['addr_amphurs'] = i['value']
                # print(i.text)
        if 'addr_amphurs' not in postdata:
            postdata['addr_amphurs'] = var[0].value
        postdata['addr_sub_district'] = postdata['addr_sub_district'].replace(
            ' ', '')
        url_district = 'https://www.teedin2.com/data/districts.php'
        r = requests.post(url_district, data={
                          'AmphurID': postdata['addr_amphurs']})
        soup = BeautifulSoup(r.content, 'html5lib')
        var = soup.findAll('option')
        print(var)
        for i in var:
            if i.text in postdata['addr_sub_district']:
                postdata['addr_districts'] = i['value']
                break

        if 'addr_districts' not in postdata:
            for i in var[1:]:
                postdata['addr_districts'] = i['value']
                break
        prod_address = ""
        for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
            if add is not None or add == "" or add == " ":
                prod_address += add + ","
        prod_address = prod_address[:-1]
        postdata['address'] = prod_address
        s = requests.Session()
        if 'land_size_ngan' not in postdata or postdata['land_size_ngan'] == None:
            postdata['land_size_ngan'] = 0
        if 'land_size_rai' not in postdata or postdata['land_size_rai'] == None:
            postdata['land_size_rai'] = 0
        if 'land_size_wa' not in postdata or postdata['land_size_wa'] == None:
            postdata['land_size_wa'] = 0
        if 'project_name' not in postdata:
            postdata['project_name'] = postdata['post_title_th']
        if len(postdata['post_images']) == 0:
            postdata['post_images'] = ['img/tmp/default/white.jpg']

        datapost = {
            'thisIDField': '',
            'action': '2',
            'thisForSaleField': '1',
            'thisTypeField': subcategory[str(postdata['property_type'])],
            'thisTitleField': postdata['post_title_th'],
            'thisRegionIDField': postdata['addr_region'],
            'thisProvinceIDField': postdata['addr_province'],
            'thisAmphurIDField': postdata['addr_amphurs'],
            'thisDistrictIDField': postdata['addr_districts'],
            'thisDetailField': postdata['post_description_th'],
            'thisSize3Field': postdata['land_size_wa'],
            'thisSize1Field': postdata['land_size_rai'],
            'thisSize2Field': postdata['land_size_ngan'],
            'thisDeedTypeField': 20,
            'thisLatitudeField': postdata['geo_latitude'],
            'thisLongitudeField': postdata['geo_longitude'],
            'thisCNameField': postdata['name'],
            'thisCPhoneField': postdata['mobile'],
            'thisCEmailField': postdata['user'],
            'thisCPasswordField': postdata['pass'],
        }
        if postdata['geo_longitude'] < postdata['geo_latitude']:
            pass
        else:
            datapost['thisHasMapField'] = 1

        arr = ["pictureField1"]
        files = {}
        for i in range(len(postdata['post_images'])):
            datapost[arr[i]] = postdata['post_images'][i]
            files[arr[i]] = (postdata['post_images'][i], open(
                postdata['post_images'][i], "rb"), "image/jpeg")
            if i == 0:
                break
        detail = ""
        s = requests.Session()
        r = s.post(url_n, data=datapost, files=files)
        content = r.content
        detail = r.text
        data = detail
        success = "true"
        if data == '1':
            success = "False"
        else:
            soup = BeautifulSoup(r.content, 'html5lib')
            # print(soup)
            var = soup.find('input', attrs={'class': 'button', 'type': 'button'})['onclick']
            # print(var)
            i = len("window.location = 'https://www.teedin2.com/detail/")
            post_id = ''
            while var[i] != ".":
                post_id += var[i]
                i += 1
            post_url = 'https://www.teedin2.com/detail/' + \
                post_id+'.html'
            end_time = datetime.datetime.utcnow()
            time_usage = end_time - start_time
            return {
                'websitename': 'teedin2',
                'success': 'true',
                "start_time": str(start_time),                
                "end_time": str(end_time),
                'ret': var,
                'post_url': post_url,
                "ds_id": postdata['ds_id'],
                'post_id': post_id
            }
        end_time = datetime.datetime.utcnow()
        time_usage = end_time - start_time
        return {
            'websitename': 'teedin2',
            "success": success,
            "start_time": str(start_time),
            "ds_id": postdata['ds_id'],
            "end_time": str(end_time),
            "detail": "Failed to Create Post",
        }

    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()

        end_time = datetime.datetime.utcnow()
        time_usage = end_time - start_time

        success = "true"
        detail = ""
        ul_test = "https://www.teedin2.com/topic3Update.php"
        test = {
            'ID': postdata['post_id'],
            'action': '2',
            'thisCPasswordField': postdata['pass']
        }
        with requests.Session() as s:
            r = s.post(ul_test, data=test)
        if "A Database Error Occured while counting result Rows" in r.text:
            detail = "wrong post id"
            end_time = datetime.datetime.utcnow()
            time_usage = end_time - start_time
            return {
                'websitename': 'teedin2',
                'success': 'False',
                "start_time": str(start_time),
                "log_id": postdata['log_id'],
                "end_time": str(end_time),
                "detail": detail,
            }

        if success == "true":
            datapost = {
                'action': '2',
                'ID': postdata['post_id'],
                'thisCPasswordField': postdata['pass']
            }
            url_n = 'https://www.teedin2.com/topic6Delete.php'
            with requests.Session() as s:
                r = s.post(url_n, data=datapost)

            data = r.text
            # print(data,"teedin2")
            post_url = 'https://www.teedin2.com/detail/' + \
                postdata['post_id']+'.html'
            with requests.Session() as s:
                r = s.post(post_url)
            if postdata['post_id'] not in r.text:
                success = "false"
                detail = "Failed to delete"
            else:
                detail = "Successfully deleted"

        else:
            success = "false"
        end_time = datetime.datetime.utcnow()
        time_usage = end_time - start_time
        return {
            "log_id": postdata['log_id'],
            'websitename': 'teedin2',
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "detail": detail,
        }

    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()

        post_id = postdata['post_id']
        ul_test = "https://www.teedin2.com/topic3Update.php"
        test = {
            'ID': postdata['post_id'],
            'action': '2',
            'thisCPasswordField': postdata['pass']
        }
        with requests.Session() as s:
            r = s.post(ul_test, data=test)
        if "A Database Error Occured while counting result Rows" in r.text:
            detail = "wrong post id or wrong password"
            end_time = datetime.datetime.utcnow()
            time_usage = end_time - start_time
            return {
                "log_id": postdata['log_id'],
                'websitename': 'teedin2',
                'success': 'False',
                "start_time": str(start_time),
                "end_time": str(end_time),
                "detail": detail,
            }
        posturl = "https://www.teedin2.com/topic4Moveup.php"
        datapost = {
            'ID': postdata['post_id'],
            'action': 2,
            'thisCPasswordField': postdata['pass']
        }
        r = s.post(posturl, data=datapost)

        end_time = datetime.datetime.utcnow()
        return {
            "websitename": "teedin2",
            "success": "true",
            "log_id": postdata['log_id'],
            "time_usage": end_time - start_time,
            "start_time": start_time,
            "end_time": end_time,
            "detail": "",
            "post_id": post_id,
        }

    def search_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        log_id = postdata['log_id']

        #
        #
        #

        time_end = datetime.datetime.utcnow()
        return {
            "websitename": "teedin2",
            "success": "false",
            "time_usage": time_end - time_start,
            "start_time": time_start,
            "end_time": time_end,
            "detail": "Search Post is not possible, since no registration",
            'ds_id': postdata['ds_id'],
            "log_id": log_id,
        }

# obj = teedin2()

# postdata=dict(
#     post_id='389921',
#     password='12345678'
# )

# postdata = {
#     'post_id': '391511',
#     'property_type': '3',
#     'post_title_th': 'fasfs',
#     'post_description_th': 'fasdjnsldjnflflasnkflasdflksdfklalskd',
#     "addr_province": "กรุงเทพมหานคร",
#     "addr_district": "คลองเตย",
#     "addr_sub_district": "คลองตัน",
#     "addr_road": "",
#     "addr_soi": "",
#     "geo_latitude": "23",
#     "geo_longitude": "32",
#     'listing_type': '',
#     'land_size_rai': '5234',
#     'land_size_wa': '5234',
#     'land_size_ngan': '5234',
#     'name': 'temptemp',
#     'pass': '12345678',
#     'mobile': '523452',
#     'price_baht': '234523',
#     'user': 'temp@gmail.com',
#     'post_images': ['../Desktop/download.jpeg']
# }
# r = obj.create_post(postdata)
# r=obj.edit_post(postdata)
# r = obj.delete_post(postdata)
# print(r)
