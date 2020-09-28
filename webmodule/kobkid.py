# import numpy as np
# from PIL import Image
import base64

from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
# from urlparse import urlparse
import re
import json
import datetime
import sys
import requests
import shutil
from urllib.parse import unquote

httprequestObj = lib_httprequest()


class kobkid():
    name = 'kobkid'

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
        # URL for Login/ Register
        self.url_reg = 'https://www.kobkid.com/market/memberaction.php'
        self.sell_url = 'https://www.kobkid.com/market/post/sell'
        self.rent_url = 'https://www.kobkid.com/market/post/rental'
        # Headers used in the request
        self.headers = {
            'Accept': '*/*',
            'Origin': 'https: // www.kobkid.com',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/79.0.3945.79 Chrome/79.0.3945.79 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

    def register_user(self, passdata):

        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        start_time = datetime.datetime.now()

        username = passdata['user']
        email = passdata['user']
        password = passdata['pass']

        # Data for checking email
        email_check_data = {
            'action': 'inputcheck',
            'email': email,
            'input': 'email',
        }

        # Data for checking username
        uname_check = {
            'action': 'inputcheck',
            'uname': username,
            'input': 'username',
        }

        # Data for registering the user
        register_data = {
            'action': 'regis',
            'email': email,
            'passwd': password,
            'uname': username,
        }

        result = httprequestObj.http_post(self.url_reg, data=email_check_data, headers=self.headers)
        decoded_result = result.content.decode('utf-8')
        final_output = json.loads(decoded_result)

        # If Email is not valid/ Already Registered
        if (final_output['validEMail'] == 0):
            end_time = datetime.datetime.utcnow()
            detail = 'Email already exists'
            return {
                "success": False,
                "start_time": str(start_time),
                "end_time": str(end_time),
                "usage_time": str(end_time - start_time),
                'ds_id': passdata['ds_id'],
                "detail": detail,
                "websitename": "kobkid",
            }

        result = httprequestObj.http_post(self.url_reg, data=uname_check, headers=self.headers)
        decoded_result = result.content.decode('utf-8')
        final_output = json.loads(decoded_result)

        # If Username is not valid/ Already Registered
        if (final_output['validUName'] == 0):
            end_time = datetime.datetime.utcnow()
            detail = 'User Name already available'
            return {
                "success": False,
                "start_time": str(start_time),
                'ds_id': passdata['ds_id'],
                "end_time": str(end_time),
                "usage_time": str(end_time - start_time),
                "detail": detail,
                "websitename": "kobkid",
            }

        result = httprequestObj.http_post(self.url_reg, data=register_data, headers=self.headers)
        decoded_result = result.content.decode('utf-8')
        final_output = json.loads(decoded_result)

        # If User registeration is successful
        if (final_output['result']['actionSuccess'] == True and final_output['result']['newMember'] == True):
            end_time = datetime.datetime.utcnow()
            detail = 'User Registration Successful'
            return {
                "success": True,
                "start_time": str(start_time),
                'ds_id': passdata['ds_id'],
                "end_time": str(end_time),
                "usage_time": str(end_time - start_time),
                "detail": detail,
                "websitename": "kobkid",
            }

        else:
            end_time = datetime.datetime.utcnow()
            detail = 'User Registration UnSuccessful'
            return {
                "success": False,
                "start_time": str(start_time),
                'ds_id': passdata['ds_id'],
                "end_time": str(end_time),
                "usage_time": str(end_time - start_time),
                "detail": detail,
                "websitename": "kobkid",
            }

    def test_login(self, postdata):

        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        username = postdata['user']
        password = postdata['pass']

        # Data for User Login
        login_data = {
            'action': 'login',
            'lmode': 'uname',
            'passwd': password,
            'uname': username,
            'rememe': '0',
        }
        # print(login_data)
        result = httprequestObj.http_post(self.url_reg, data=login_data, headers=self.headers)
        decoded_result = result.content.decode('utf-8')
        final_output = json.loads(decoded_result)

        # Status of the Login Action
        status = final_output['result']['actionSuccess']
        end_time = datetime.datetime.utcnow()

        if (status == True):
            detail = 'User Login Successful'

        else:
            detail = 'Unable to Login'

        return {
            "success": status,
            "start_time": str(time_start),
            "end_time": str(end_time),
            "ds_id": postdata['ds_id'],
            "usage_time": str(end_time - time_start),
            "detail": detail,
            "websitename": "kobkid",
        }

    def create_post(self, postdata):

        result = self.test_login(postdata)
        if(result['success'] == False):
            result['post_url'] = ''
            return result
        post_type = ''
        start_time = datetime.datetime.utcnow()
        #print(postdata['listing_type'])
        if(postdata['listing_type'] == 'เช่า'):
            post_type = 'RENTAL'

        else:
            post_type = 'SELL'

            #Condo CHeck
        if(postdata['property_type'] == '1' or postdata['property_type'] == 1):

            if ('web_project_name' not in postdata) or (postdata['web_project_name'] == None):
                if 'project_name' in postdata and postdata['project_name'] != None:
                    postdata['web_project_name'] = postdata['project_name']
                else:
                    postdata['web_project_name'] = postdata['post_title_th']

                #Propert Search by name
            pid_data = {
                'term': postdata['web_project_name'],
                'page': '1',
                'page_limit': '1'
            }

            response = httprequestObj.http_post('https://www.kobkid.com/market/resource/php/condo_list.php',
                                                    data=pid_data)
            result = json.loads(response.content.decode('utf-8', errors="ignore"))['condos']
            if(len(result) != 0):
                condo_id = result[0]['id']

                #print(condo_id)
                zoneid_data = {
                    'condoid': condo_id
                }

                response = httprequestObj.http_post('https://www.kobkid.com/market/resource/php/condoZoneSearch.php',
                                                        data=zoneid_data)
                #print(response.content)
                try:
                    result_zone = json.loads(response.content.decode('utf-8', errors="ignore"))['zoneid']
                except:

                    zones = ['สุขุมวิท/นานา/อโศก/พร้อมพงษ์/ทองหล่อ/เอกมัย', 'ราชดำริ/ชิดลม/เพลินจิต/วิทยุ/ร่วมฤดี/สวนลุมพินี', 'สีลม/สาทร/สุรศักดิ์/สี่พระยา/เจริญกรุง',
                             'สยาม/ปทุมวัน/พญาไท/ราชเทวี', 'ประตูน้ำ/มักกะสัน/ราชปรารภ', 'หัวลำโพง/เยาวราช/จุฬาฯ/สามย่าน', 'พระราม4/คลองเตย/กล้วยน้ำไท', 'อนุสาวรีย์ชัยฯ/ดินแดง/สนามเป้า/อารีย์/สะพานควาย',
                             'เพชรบุรี/พระราม9/อาร์ซีเอ', 'รัชดาฯ/ศูนย์วัฒนธรรมฯ/ห้วยขวาง/สุทธิสาร', 'พระโขนง/อ่อนนุช', 'นราธิวาสราชนครินทร์/พระราม3/ยานนาวา', 'สวนจตุจักร/แยกลาดพร้าว/ลาดพร้าว 1-26',
                             'ลาดพร้าว 26 ขึ้นไป/โชคชัย4/เกษตร-นวมินทร์/รามอินทรา', 'วิภาวดี/ดอนเมือง/สะพานใหม่/รังสิต', 'งามวงศ์วาน/รัตนาธิเบศร์/ติวานนท์/แจ้งวัฒนะ/เมืองทอง/ปากเกร็ด', 'รัชโยธิน/เสนานิคม/ม.เกษตรฯ',
                             'บางซื่อ/บางโพ/เกียกกาย/ประชาชื่น', 'รามคำแหง/พัฒนาการ/คลองตัน', 'บางจาก/ปุณณวิถี/อุดมสุข/แบริ่ง', 'บางนา/ศรีนครินทร์/เทพารักษ์/สวนหลวง ร.9', 'สุวรรณภูมิ/ร่มเกล้า/ลาดกระบัง',
                             'เจริญนคร/กรุงธนบุรี/วงเวียนใหญ่/สมเด็จพระเจ้าตากสิน', 'โพธิ์นิมิตร/ท่าพระ/ตลาดพลู/วุฒากาศ', 'เพชรเกษม/บางหว้า/บางแค', 'จรัญสนิทวงศ์/พระราม8/ปิ่นเกล้า/พรานนก/บรมราชชนนี']

                    result_zone = 0
                    for i in range(len(zones)):

                        if(postdata['addr_province'] in zones[i] or postdata['addr_district'] in zones[i] or postdata['addr_sub_district'] in zones[i]):
                            result_zone = i+1
                            break

            else:
                condo_id = result[0]['id']
                zones = ['สุขุมวิท/นานา/อโศก/พร้อมพงษ์/ทองหล่อ/เอกมัย',
                         'ราชดำริ/ชิดลม/เพลินจิต/วิทยุ/ร่วมฤดี/สวนลุมพินี', 'สีลม/สาทร/สุรศักดิ์/สี่พระยา/เจริญกรุง',
                         'สยาม/ปทุมวัน/พญาไท/ราชเทวี', 'ประตูน้ำ/มักกะสัน/ราชปรารภ', 'หัวลำโพง/เยาวราช/จุฬาฯ/สามย่าน',
                         'พระราม4/คลองเตย/กล้วยน้ำไท', 'อนุสาวรีย์ชัยฯ/ดินแดง/สนามเป้า/อารีย์/สะพานควาย',
                         'เพชรบุรี/พระราม9/อาร์ซีเอ', 'รัชดาฯ/ศูนย์วัฒนธรรมฯ/ห้วยขวาง/สุทธิสาร', 'พระโขนง/อ่อนนุช',
                         'นราธิวาสราชนครินทร์/พระราม3/ยานนาวา', 'สวนจตุจักร/แยกลาดพร้าว/ลาดพร้าว 1-26',
                         'ลาดพร้าว 26 ขึ้นไป/โชคชัย4/เกษตร-นวมินทร์/รามอินทรา', 'วิภาวดี/ดอนเมือง/สะพานใหม่/รังสิต',
                         'งามวงศ์วาน/รัตนาธิเบศร์/ติวานนท์/แจ้งวัฒนะ/เมืองทอง/ปากเกร็ด', 'รัชโยธิน/เสนานิคม/ม.เกษตรฯ',
                         'บางซื่อ/บางโพ/เกียกกาย/ประชาชื่น', 'รามคำแหง/พัฒนาการ/คลองตัน',
                         'บางจาก/ปุณณวิถี/อุดมสุข/แบริ่ง', 'บางนา/ศรีนครินทร์/เทพารักษ์/สวนหลวง ร.9',
                         'สุวรรณภูมิ/ร่มเกล้า/ลาดกระบัง',
                         'เจริญนคร/กรุงธนบุรี/วงเวียนใหญ่/สมเด็จพระเจ้าตากสิน', 'โพธิ์นิมิตร/ท่าพระ/ตลาดพลู/วุฒากาศ',
                         'เพชรเกษม/บางหว้า/บางแค', 'จรัญสนิทวงศ์/พระราม8/ปิ่นเกล้า/พรานนก/บรมราชชนนี']

                result_zone = 0
                for i in range(len(zones)):

                    if (postdata['addr_province'] in zones[i] or postdata['addr_district'] in zones[i] or postdata[
                        'addr_sub_district'] in zones[i]):
                        result_zone = i + 1
                        break

            if(post_type == 'SELL'):
                posttag = '11'

            else:
                posttag = '0'

            post_data = {
                'posttitle': postdata['post_title_th'],
                'postcondo': condo_id,
                'postzone': result_zone,
                'postprice': postdata['price_baht'],
                'postcontact': postdata['name'],
                'posttel': postdata['mobile'],
                'postemail': postdata['user'],
                'posttype': post_type,
                'posttag': posttag
            }

            #print(post_data)

            response = httprequestObj.http_post('https://www.kobkid.com/market/resource/php/createMarketItem.php', data=post_data)
            result = json.loads(response.content.decode('utf-8', errors="ignore"))
            #print(result)
            post_id = result['postid']



            if (postdata['post_images'] != None):
                allimages = postdata['post_images']
                for i in range(len(allimages)):

                    image_data = {
                        'post-id': post_id,
                        'file': (allimages[i], open(os.getcwd() + "/" + allimages[i], 'rb'), 'image/png')
                    }

                    response = httprequestObj.http_post('https://www.kobkid.com/market/imgUpload.php', files=image_data,
                                                        data=image_data)
                    result = json.loads(response.content.decode('utf-8'))
                    if (result['success'] == False):
                        end_time = datetime.datetime.now
                        return {
                            "ds_id": postdata['ds_id'],
                            "success": False,
                            "start_time": str(start_time),
                            "end_time": str(end_time),
                            "usage_time": str(end_time - start_time),
                            "detail": "Unable To Post Images",
                            "websitename": "kobkid",
                            'post_url' : ''
                        }


            if(postdata['bed_room'] == 1):
                room_type = 2

            elif (postdata['bed_room'] == 2):
                room_type = 3

            elif (postdata['bed_room'] == 3):
                room_type = 4

            else:
                room_type = 5

            if(postdata['floor_level'] == None):
                floor_level = ''

            else:
                floor_level = (postdata['floor_level'])

            if('building' not in postdata or postdata['building'] == None):
                building_name = ''

            else:
                building_name = postdata['building']

            postdata['post_id'] = post_id

            publish_obj = {
                'postid' : post_id,
                'postrt' : room_type,
                'postdt' : postdata['post_description_th'],
                'condolat': postdata['geo_latitude'],
                'postrs': postdata['floor_area'],
                'condolng': postdata['geo_longitude'],
                'postnb' : floor_level,
                'postbn' : building_name,
            }

            #print(publish_obj)
            response = httprequestObj.http_post('https://www.kobkid.com/market/resource/php/publishMarketItem.php',data=publish_obj)
            result = json.loads(response.content.decode('utf-8'))
            end_time = datetime.datetime.utcnow()
            if(result['success'] == True):
                detail = 'Post Created Successfully'

                postdata['post_id'] = post_id
                self.edit_post(postdata)

                return {
                    "success": result['success'],
                    "ds_id": postdata['ds_id'],
                    "start_time": str(start_time),
                    "end_time": str(end_time),
                    "usage_time": str(end_time - start_time),
                    "detail": detail,
                    "post_url": 'https://www.kobkid.com/market/'+str(post_id),
                    "post_id" : post_id,
                    "websitename": "kobkid"
                }

            else:
                detail = 'Unable to create the Post'

            return {
                    "success": result['success'],
                    "ds_id": postdata['ds_id'],
                    "start_time": str(start_time),
                    "end_time": str(end_time),
                    "usage_time": str(end_time - start_time),
                    "detail": detail,
                    "websitename": "kobkid",
                    'post_url': ''
            }

        else:
            end_time = datetime.datetime.utcnow()
            return {
                    "success": False,
                    "ds_id": postdata['ds_id'],
                    "start_time": str(start_time),
                    "end_time": str(end_time),
                    "usage_time": str(end_time - start_time),
                    "detail": "Only Condo Property Can Be Posted",
                    "websitename": "kobkid",
                    'post_url' : ''
            }

    def boost_post(self, postdata):

        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        start_time = datetime.datetime.utcnow()

        login = self.test_login(postdata)
        if(login['success'] == False):
            return login
        post_id = postdata['post_id']

        boost_data = {
            'action': 'tagedit',
            'postid': post_id,
            'tagid': '11'
        }

        response = httprequestObj.http_post('https://www.kobkid.com/market/postaction.php', data=boost_data)
        result = json.loads(response.content.decode('utf-8'))['actionSuccess']

        if(result == True):
            detail = "Post Boosted"

        else:
            detail = "Unable to Boost The Post"
        end_time = datetime.datetime.utcnow()

        return {
            "success": result,
            "start_time": str(start_time),
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "end_time": str(end_time),
            "usage_time": str(end_time - start_time),
            "detail": detail,
            "post_url": "https://www.kobkid.com/market/" + str(post_id),
            "post_id": post_id,
            "websitename": "kobkid"
        }

    def delete_post(self, postdata):

        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        start_time = datetime.datetime.utcnow()

        login = self.test_login(postdata)
        if(login['success'] == False):
            result = False
            detail = "cannot login"
        else:
            post_id = postdata['post_id']

            delete_post = {
              'action': 'delpost',
              'postid': post_id
            }

            response = httprequestObj.http_post('https://www.kobkid.com/market/postaction.php', data=delete_post)
            result = json.loads(response.content.decode('utf-8'))['actionSuccess']

            if(result == True):
                detail = "Post Deleted"
            else:
                detail = "Could not delete the post"

        end_time = datetime.datetime.utcnow()
        return {
            "success": result,
            "start_time": str(start_time),
            "end_time": str(end_time),
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id":postdata['post_id'],
            "usage_time": str(end_time - start_time),
            "detail": detail,
            "websitename": "kobkid"
        }

    def check_current_post(self, postdata):
        login = self.test_login(postdata)

        if(login['success'] == False):
            return login

        response = httprequestObj.http_get('https://www.kobkid.com/member/post')
        soup = BeautifulSoup(response.content, 'html.parser')
        id = soup.find_all("div", {"class": "market-item-edit"})
        list_of_orders = []

        for i in range(len(id)):
            list_of_orders.append((id[i].attrs['data-postid']))
        return list_of_orders

    def edit_post(self, postdata):

        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        start_time = datetime.datetime.utcnow()

        orders = self.check_current_post(postdata)

        login = self.test_login(postdata)
        if(login['success'] == False):
            end_time = datetime.datetime.utcnow()
            return login
        post_id = postdata['post_id']

        if(str(post_id) not in orders):
            result = False
            detail = 'Post Not Created By User'
            end_time = datetime.datetime.utcnow()
            return {
                "success": result,
                "start_time": str(start_time),
                "end_time": str(end_time),
                'ds_id': postdata['ds_id'],
                "log_id": postdata['log_id'],
                "usage_time": str(end_time - start_time),
                "detail": detail,
                "websitename": "kobkid"
            }

        if (postdata['listing_type'] == 'เช่า'):
            post_type = 'RENTAL'

        else:
            post_type = 'SELL'

        if (post_type == 'SELL'):
            posttag = '11'

        else:
            posttag = '0'

        if (postdata['bed_room'] == 1):
            room_type = 2

        elif (postdata['bed_room'] == 2):
            room_type = 3

        elif (postdata['bed_room'] == 3):
            room_type = 4

        else:
            room_type = 5
        if(postdata['post_images'] != None):
            allimages = postdata['post_images']
            for i in range(len(allimages)):

                image_data = {
                    'post-id': post_id,
                    'file': (allimages[i], open(os.getcwd()+"/"+allimages[i], 'rb'), 'image/png')
                }

                response = httprequestObj.http_post('https://www.kobkid.com/market/imgUpload.php', files=image_data,
                                                    data=image_data)
                result = json.loads(response.content.decode('utf-8'))
                if (result['success'] == False):
                    end_time = datetime.datetime.now
                    return {
                        "success": False,
                        "start_time": str(start_time),
                        "end_time": str(end_time),
                        'ds_id': postdata['ds_id'],
                        "log_id": postdata['log_id'],
                        "usage_time": str(end_time - start_time),
                        "detail": "Unable To Post Images",
                        "websitename": "kobkid"
                    }
        if('building' not in postdata or postdata['building'] == None):
            building_name = ''

        else:
            building_name = postdata['building']

        if("floor_level" not in postdata or postdata['floor_level'] == None):
            floor_level = ''
        else:
            floor_level = postdata['floor_level']

        #print(floor_level)

        if 'floor_level' not in postdata or postdata['floor_level'] is None:
            postdata['floor_level'] = ''
        edit_data = {
            'action': 'postedit',
            'postid': post_id,
            'posttitle': postdata['post_title_th'],
            'posttag': posttag,
            'contactname': postdata['name'],
            'contacttel': postdata['mobile'],
            'contactemail': postdata['email'],
            'postdetail': postdata['post_description_th'],
            'roomtype': room_type,
            'roomsize': postdata['floor_area'],
            'buildingno': building_name,
            'floorno': floor_level,
            'postprice': postdata['price_baht'],
            'postdeposit': '0',
            'postfac': ''
        }
        response = httprequestObj.http_post('https://www.kobkid.com/market/postaction.php', data=edit_data)
        result = json.loads(response.content.decode('utf-8'))['actionSuccess']

        if(result == True):
            detail = "Post Edited"

        else:
            detail = "Unable to Edit The Post"

        end_time = datetime.datetime.utcnow()
        try:
            log_id = postdata['log_id']
        except:
            log_id = ""
        return {
            "success": result,
            "start_time": str(start_time),
            'ds_id': postdata['ds_id'],
            "log_id": log_id,
            "end_time": str(end_time),
            "usage_time": str(end_time - start_time),
            "detail": detail,
            "post_url": "https://www.kobkid.com/market/"+str(post_id),
            "post_id": post_id,
            "websitename": "kobkid"
        }


    def search_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        post_id = ""
        post_url = ""
        post_modify_time = ""
        post_view = ""
        post_found = "false"
        user = postdata['user']
        passwd = postdata['pass']

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        
        if success == True:
            post_title = postdata['post_title_th']
            # exists, authenticityToken, post_title = self.check_post(post_id)
            url = "https://www.kobkid.com/member/post"
            r = httprequestObj.http_get(url)
            exists = False
            soup = BeautifulSoup(r.content, features='html.parser')
            for title_row in soup.find_all('div', attrs={'class':'market-item-wrapper'}):
                if title_row is None:
                    continue
                title = title_row.find_all('div',{'class':'col-md-4'})[1].find("div").text
                # .text.split("Views:")[1].split("times")[0]
                # .text.strip()[-11:]
                # title = title_row.find('div', attrs={'style':'text-align:left;border-right:1px solid #CCF0FF;border-left:1px solid #CCF0FF;cursor:pointer;min-height:150px;'}).find('div', attrs={'style':'font-weight:bold;font-size:20px;'}).text
                # print(f'postt--{post_title}\ntitle--{title}\n\n')
                if post_title == title:
                    exists = True
                    post_id = title_row.find('div', attrs={'class':'market-item-edit'})['data-postid']
                    post_url = "https://www.kobkid.com/market/"+post_id
                    post_modify_time = title_row.find('div',{'class':'col-md-4 market-item-col1'}).text.strip()[-10:]
                    post_view = title_row.find('div',{'class':'col-md-4 market-item-col1'}).text[24:-31]
                    post_found = "true"
                    detail = "post found successfully"
                    break

            if not exists:
                success = "false"
                detail = "No post found with given title."

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        log_id = ""
        if 'log_id' in postdata:
            log_id = postdata['log_id']
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": "kobkid",
            "ds_id": postdata['ds_id'],
            "log_id": log_id,
            "post_id": post_id,
            "post_modify_time": post_modify_time,
            "post_view": post_view,
            "post_url": post_url,
            "post_found": post_found
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

