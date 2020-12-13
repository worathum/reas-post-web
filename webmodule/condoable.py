# -*- coding: utf-8 -*-
import threading

from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
# from urlparse import urlparse
import re
import json
import datetime
import sys
from urllib.parse import unquote
import os


httprequestObj = lib_httprequest()


class condoable():

    name = 'condoable'

    def __init__(self):

        try:
            import configs
        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.primarydomain = 'http://www.condoable.com/'
        self.debug = 0
        self.debugresdata = 0
        self.parser = 'html.parser'


    def logout_user(self):
        url = 'http://condoable.com/logout.jsp'
        httprequestObj.http_get(url)

    def register_user(self, userdata):
        self.logout_user()
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        # print("here in register")
        httprequestObj.http_get('http://condoable.com/logout.jsp')

        email = userdata['user']
        passwd = userdata['pass']
        first_name = userdata['name_th']
        last_name = userdata['surname_th']
        mobile = userdata['tel']
        
        
        datapost={
            "email": email,
            "password": passwd,
            "checkPassword": passwd,
            "firstName": first_name,
            "lastName": last_name,
            "phone": mobile,
            "homePhone": "",
            "officePhone": "",
            "agree": "on"
        }



        r = httprequestObj.http_get('http://condoable.com/checkUserId.do?function=register&userId='+email)
        data = r.text
        print(data)
        success = ""
        detail = ""
        if(data == "true"):
            r = httprequestObj.http_post('http://condoable.com/signupMember.do', data = datapost)
            data = r.text
            success = "True"
            detail = "Registered Successfully"
        else:
            success = "False"
            detail = "User already exists"
       
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "condoable",
            'ds_id': userdata['ds_id'],
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "ds_id": userdata['ds_id']
        }

    def test_login(self, logindata):
        self.logout_user()
        # print("Here in test_login")
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        httprequestObj.http_get('http://condoable.com/logout.jsp')
        email_user = logindata['user']
        email_pass = logindata['pass']
        
        datapost = {
            "userId": email_user,
            "password": email_pass
        }
        # print(datapost)
        r = httprequestObj.http_post('http://condoable.com/login.do', data=datapost)
        data = r.text
        # print(data)
        # print("Data Printed")
        matchObj = re.search(r'logout.jsp', data)
        # print(matchObj)
        if matchObj:
            success = "True"
            detail = "Sucessful Login"
        else:
            success = "False"
            detail = "Login Unsucessful"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": self.name,
            "ds_id": logindata['ds_id'],
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
        # addr_sub_district = postdata['addr_sub_district']
        # addr_road, addr_near_by, floorarea_sqm = ['','','']
        # if 'addr_road' in postdata:
            # addr_road = postdata['addr_road']
        # if 'addr_near_by' in postdata:
            # addr_near_by = postdata['addr_near_by']
        # if 'floorarea_sqm' in postdata:
            # floorarea_sqm = postdata['floorarea_sqm']
        
        geo_latitude = postdata['geo_latitude']
        geo_longitude = postdata['geo_longitude']
        property_id = postdata['property_id']
        post_title_th = postdata['post_title_th']
        post_description_th = postdata['post_description_th']
        # post_title_en = postdata['post_title_en']
        # post_description_en = postdata['post_description_en']
        # floor_no = postdata['floor_level']
        # bedroom = postdata['bed_room']
        # bathroom = postdata['bath_room']
        # ds_id = postdata["ds_id"]
        name = postdata["name"]
        mobile = postdata["mobile"]
        email = postdata["email"]
        # account_type = postdata["account_type"]
        user = postdata["user"]
        password = postdata["pass"]
        # project_name = postdata["project_name"]
        land_size_rai = postdata['land_size_rai']
        land_size_ngan = postdata['land_size_ngan']
        land_size_wah = postdata['land_size_wa']
        floorarea = "10"
        try:
            floorarea = postdata['floor_area']
            temp = int(floorarea)
        except:
            floorarea = "10"
        try:
            floorlevel = postdata['floor_level']
        except:
            floorlevel = ""
        # post_description_en =  post_description_en.replace("\r\n","<br>")
        post_description_th =  post_description_th.replace("\r\n","<br>")
        post_description_th =  post_description_th.replace("\n","<br>")

        try:
            project_name = postdata['web_project_name']
            if project_name == "":
                raise Exception

        except:
            try : 
                project_name = postdata['project_name']
                if project_name == "":
                    raise Exception
            except :
                project_name = postdata['post_title_th']
        resp = httprequestObj.http_get('http://condoable.com/action/advertise/searchCondoProject.jsp?term=' + project_name)
        allres = json.loads(resp.content.decode('utf-8').replace('""', '"'), strict = False)
        condoprojectid = None
        if len(allres) != 0:
            condoprojectid = allres[0]['id']

        price = "0"
        rent = "0"
        if(listing_type == "เช่า"):
            listing_type = "RENT"
            rent = price_baht
        else:
            listing_type = "SALE"
            price = price_baht

        login = self.test_login(postdata)
        success = login["success"]
        detail = login["detail"]
        post_id = ""
        post_url = ""
        
        if success == "True":
            if condoprojectid is None:
             
                data_Test = {
                    "name": project_name ,
                    "buildOn": "5/5/20",
                    "addressLine1": "province : "+addr_province+"; District : "+addr_district ,
                    "latitude": geo_latitude,
                    "longitude": geo_longitude,
                }
                r = httprequestObj.http_post('http://condoable.com/advertise/addOtherCondoProject.do?zoneId=20', data=data_Test)
                condoprojectid = ""
                for i in r.json():
                    if str(i['latitude']) == str(data_Test["latitude"]) and str(i['longitude']) == str(data_Test["longitude"]):
                        print(i)
                        condoprojectid = i["id"]
                        break
    
            datapost = {
                "size": floorarea,
                "typeOfAd": listing_type,
                "price": price,
                "beginAvailable":" 09/05/2020",
                "rentalPerTerm": rent,
                "beginPublish": "09/05/2020",
                "publishDay": "120",
                "firstName": name,
                "phone": mobile,
                "email": email,
                "zoneId": "", 
                "condoProjectId": condoprojectid,
                "condoBuildingId":"", 
                "roomTypeId": "",
                "publish": "false",
                "next": "true"
            }
            print(datapost)
            r = httprequestObj.http_post('http://condoable.com/addAdvertiseDetail.do', data=datapost)
            print(r.status_code)
            
            soup = BeautifulSoup(r.text, self.parser)
            authenticityToken = soup.find("input", {"name": "token"})
            post_id = soup.find("input",{"name":"advertiseId"})
            if authenticityToken and post_id:
                authenticityToken = authenticityToken.get('value')
                post_id = post_id.get('value')
                print(authenticityToken)
                print(post_id)
                datapost = {
                    "advertiseId": post_id,
                    "token": authenticityToken,
                    "publish": "true",
                    "title": post_title_th,
                    "description": post_description_th,
                    "size": floorarea,
                    "floor": floorlevel,
                    "roomNumber": ""
                }
                
                filestoup = {}
                for i in postdata['post_images']:
                    filestoup['files[]'] = open(os.getcwd() + "/"+ i,'rb')
                    r = httprequestObj.http_post('http://condoable.com/uploadFile.do?type=advertiseImage8/'+post_id +'&advertiseId='+post_id,data="",files=filestoup)
                r = httprequestObj.http_post('http://condoable.com/addAdvertiseMoreDetail.do',data=datapost)
                if(re.search(r'ลงประกาศเรียบร้อยแล้ว',r.text)):
                    success = "true"
                    detail = "Sucessfully posted"
                    post_url = "http://condoable.com/viewAdvertise.do?advertiseId="+str(post_id)
                else:
                    success = "false"
                    detail = "Could not post" 
                    post_id = ""
            else:
                success = "False"
                detail  = "Unable to create post"
                post_id = ""
        else :
            success = "False"
            detail = "Login Error"
        time_end = datetime.datetime.utcnow()
        
        return {
            "websitename": "condoable",
            "success": success,
            "usage_time": time_end - time_start,
            "start_time": time_start,
            "end_time": time_end,
            "ds_id": postdata['ds_id'],
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "",
            "detail": detail,
            "ds_id": postdata['ds_id']
        }

    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        post_id = postdata['post_id']
        log_id = postdata['log_id']
        email_user = postdata['user']
        email_pass = postdata['pass']
        #https://www.condoable.com/member
        #
        #
        #
        datapost = {
            "product_id" : post_id
        }
        login = self.test_login(postdata)
        success = login["success"]
        detail = login["detail"]
        # print(login)
        if success == "True":
            r = httprequestObj.http_get('https://www.condoable.com/member', verify=False)
            data = r.text
            print(data)
            csrf = re.findall(r'csrf_token:"\w+',data)
            datapost["csrf_token"] = csrf[0].replace("csrf_token:\"", "")
            if(re.search(r''+post_id,data)):
                r = httprequestObj.http_post('https://www.condoable.com/member/product_postpone', data=datapost)
                if r.status_code != 200:
                    success = "False"
                    detail = "Cannot boost post with id"+post_id
                else:
                    success = "True"
                    detail = "Post sucessfully boosted"
            else:
                success = "False"
                detail = "Wrong Post ID"
          
        time_end = datetime.datetime.utcnow()
        return {
            "websitename": "condoable",
            "success": success ,
            "usage_time": time_end - time_start,
            "start_time": time_start,
            "end_time": time_end,
            "detail": detail,
            'ds_id': postdata['ds_id'],
            "log_id": log_id,
            "post_id": post_id,
            "post_view": ""
        }

    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        
        datapost = {}
        login = self.test_login(postdata)
        success = login["success"]
        detail = login["detail"]
        post_id = postdata['post_id']
        post_url = "http://condoable.com/viewAdvertise.do?advertiseId="+str(post_id)
        
        if(success == "True"):
            # print()
            r = httprequestObj.http_get(post_url)
            print(r.status_code)
            if r.status_code == 500:
                success = "False"
                detail = "Invalid post id"
            else:
                if(re.search(r'ไม่พบประกาศนี้ หรือประกาศถูกลบไปแล้ว!',r.text)):
                    success = "Flase"
                    detail = "The Post has already been deleted"
                else:    
                    r = httprequestObj.http_post("http://condoable.com/action/advertise/deleteAdvertise.jsp",data={"advertiseId": post_id})
                    if(re.search(r'ลบประกาศเลขที่',r.text)):
                        success = "true"
                        detail = "Announcement deleted"
                    else:
                        success = "False"
                        detail = "Announcement can not be deleted"

        #
        #
        #

        time_end = datetime.datetime.utcnow()
        return {
            "websitename": "condoable",
            "success": success,
            "usage_time": time_end - time_start,
            "start_time": time_start,
            "end_time": time_end,
            "detail": detail,
            "post_id": post_id,
            "log_id": postdata['log_id'],
            "ds_id": postdata['ds_id']
        }

    def del_img(self, all_img):
        for i, img in enumerate(all_img):
            link = img['onclick'].split(',')[1].replace('\r\n\t\t\t        url: "', '').replace('"', '')
            try:
                del_ = httprequestObj.http_post('http://condoable.com/' + str(link), '')
                print(i, del_.text)
            except:
                pass
    def edit_post(self, postdata):
        # https://www.condoable.com/post/get_json_district?province_id=13   ->     for district
        #http://condoable.com/advertise-condo.jsp?advertiseId=288236
        # https://www.condoable.com/post/get_json_district?province_id=13   ->     for district
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        # print(postdata)
        # postdata = postdata
        listing_type = postdata['listing_type']
        property_type = postdata['property_type']
        post_img_url_lists = postdata['post_img_url_lists']
        price_baht = postdata['price_baht']
        addr_province = postdata['addr_province']
        addr_district = postdata['addr_district']
        # addr_sub_district = postdata['addr_sub_district']
        # addr_road, addr_near_by, floorarea_sqm = ['','','']
        # if 'addr_road' in postdata:
            # addr_road = postdata['addr_road']
        # if 'addr_near_by' in postdata:
            # addr_near_by = postdata['addr_near_by']
        # if 'floorarea_sqm' in postdata:
            # floorarea_sqm = postdata['floorarea_sqm']
        
        geo_latitude = postdata['geo_latitude']
        geo_longitude = postdata['geo_longitude']
        property_id = postdata['property_id']
        post_title_th = postdata['post_title_th']
        post_description_th = postdata['post_description_th']
        # post_title_en = postdata['post_title_en']
        # post_description_en = postdata['post_description_en']
        # floor_no = postdata['floor_level']
        # bedroom = postdata['bed_room']
        # bathroom = postdata['bath_room']
        # ds_id = postdata["ds_id"]
        name = postdata["name"]
        mobile = postdata["mobile"]
        email = postdata["email"]
        # account_type = postdata["account_type"]
        user = postdata["user"]
        password = postdata["pass"]
        # project_name = postdata["project_name"]
        land_size_rai = postdata['land_size_rai']
        land_size_ngan = postdata['land_size_ngan']
        land_size_wah = postdata['land_size_wa']
        try:
            floorarea = postdata['floor_area']
            print("The floor area is ", floorarea)
            temp = int(floorarea)
        except:
            print("here in floorare except")
            floorarea = "10"
        try:
            floorlevel = postdata['floor_level']
        except:
            floorlevel = ""
        # post_description_en =  post_description_en.replace("\r\n","<br>")
        post_description_th =  post_description_th.replace("\r\n","<br>")
        post_description_th =  post_description_th.replace("\n","<br>")
        try:
            project_name = postdata['web_project_name']
        except:
            try : 
                project_name = postdata['project_name']
            except :
                project_name = postdata['post_title_th']

        resp = httprequestObj.http_get('http://condoable.com/action/advertise/searchCondoProject.jsp?term=' + project_name)
        allres = json.loads(resp.content.decode('utf-8').replace('""', '"'), strict = False)
        condoprojectid = None
        if len(allres) != 0:
            condoprojectid = allres[0]['id']

        price = "0"
        rent = "0"
        if(listing_type == "เช่า"):
            listing_type = "RENT"
            rent = price_baht
        else:
            listing_type = "SALE"
            price = price_baht

        post_id = postdata['post_id']         

        login = self.test_login(postdata)
        success = login["success"]
        detail = login["detail"]
        post_url = ""


        if condoprojectid is None:
         
            data_Test = {
                "name": project_name ,
                "buildOn": "5/5/20",
                "addressLine1": "province : "+addr_province+"; District : "+addr_district ,
                "latitude": geo_latitude,
                "longitude": geo_longitude,
            }
            r = httprequestObj.http_post('http://condoable.com/advertise/addOtherCondoProject.do?zoneId=20', data=data_Test)
            condoprojectid = ""
            for i in r.json():
                if str(i['latitude']) == str(data_Test["latitude"]) and str(i['longitude']) == str(data_Test["longitude"]):
                    print(i)
                    condoprojectid = i["id"]
                    break

        datapost = {
            "advertiseId": post_id,
            "size": floorarea,
            "typeOfAd": listing_type,
            "price": price,
            "beginAvailable":" 09/05/2020",
            "rentalPerTerm": rent,
            "beginPublish": "09/05/2020",
            "publishDay": "120",
            "firstName": name,
            "phone": mobile,
            "email": email,
            "zoneId": "", 
            "condoProjectId": condoprojectid,
            "condoBuildingId":"", 
            "roomTypeId": "",
            "publish": "false",
            "next": "true"
        }
        r = httprequestObj.http_post('http://condoable.com/addAdvertiseDetail.do', data=datapost)
        soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
        authenticityToken = soup.find("input", {"name": "token"})
        if authenticityToken:
            authenticityToken = authenticityToken.get('value')
            print(authenticityToken)
            datapost = {
                "advertiseId": post_id,
                "token": authenticityToken,
                "publish": "true",
                "title": post_title_th,
                "description": post_description_th,
                "size": floorarea,
                "floor": floorlevel,
                "roomNumber": ""
            }
            # http://condoable.com/uploadFile.do?type=advertiseImage8/288227&advertiseId=288227
            filestoup = {}
            r_ = httprequestObj.http_post('http://condoable.com/listImage.do?id='+ str(post_id) + '&type=advertiseImage&atc=' + str(authenticityToken) + '&sid=78','')
            soup = BeautifulSoup(r_.content, self.parser)
            # f'listImage.do?id={post_id}&type=advertiseImage&atc={authenticityToken}&sid=78'
            # print(r_.text)
            all_img = soup.findAll('div', {'class': 'delete'})
            print(len(all_img))
            self.del_img(all_img)
            # del_ =[]



            # print(len(all_img),del_)

            for i in postdata['post_images']:
                filestoup['files[]'] = open(os.getcwd() + "/"+ i,'rb')
                r = httprequestObj.http_post('http://condoable.com/uploadFile.do?type=advertiseImage8/'+post_id +'&advertiseId='+post_id,data="",files=filestoup)
            r = httprequestObj.http_post('http://condoable.com/addAdvertiseMoreDetail.do',data=datapost)
            if(re.search(r'ลงประกาศเรียบร้อยแล้ว',r.text)):
                success = "true"
                detail = "Sucessfully Edited post with id "+post_id
            else:
                success = "false"
                detail = "Could not edit post with id "+post_id
            post_url = "http://condoable.com/viewAdvertise.do?advertiseId="+str(post_id)
        else:
            success = "false"
            detail = "Unable to edit post"
        time_end = datetime.datetime.utcnow()
            
        return {
            "websitename": "condoable",
            "success": success,
            "usage_time": time_end - time_start,
            "start_time": time_start,
            "end_time": time_end,
            "ds_id": postdata['post_id'],
            "post_url": post_url,
            "post_id": post_id,
            "log_id": postdata['log_id'],
            "account_type": "",
            "detail": detail,
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

    def search_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_url = ""
        post_id = ""
        post_created = ""

        if success:
            r = httprequestObj.http_get('http://condoable.com/myAdvertise.jsp')
            # print(r.url)
            # print(r.status_code)

            soup = BeautifulSoup(r.content, self.parser)
            all_posts = soup.find_all('tr')[1:]
            # print(all_posts[0])

            post_found = False

            for post in all_posts:
                info = post.find_all('td')
                title = info[3].find('a').string
                if title == postdata['post_title_th']:
                    # print('Post Found')
                    post_found = True
                    post_id = info[1].string.strip()
                    post_url = 'http://condoable.com/viewAdvertise.do?advertiseId='+post_id
                    r = httprequestObj.http_get(post_url)
                    # print(r.url)
                    # print(r.status_code)
                    soup = BeautifulSoup(r.content, self.parser)
                    post_created = str(soup.find('div', 'createdOn').contents[-1])
                    break

            if post_found:
                detail = "Post Found"
            else:
                detail = "No post with given title"
        else:
            success = False
            detail = "Couldnot login"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": "condoable",
            "account_type": None,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "post_created": post_created,
            "post_modified": "",
            "post_view": "",
            "post_url": post_url,
        }

