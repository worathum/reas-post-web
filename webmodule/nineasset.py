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
import os



class nineasset():

    name = 'nineasset'

    def __init__(self):

        try:
            import configs
        except ImportError:
            configs = {}
        self.httprequestObj = lib_httprequest()
        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.primarydomain = 'http://www.9asset.com'
        self.debug = False
        self.debugresdata = 0
        self.parser = 'html.parser'

    def register_user(self, userdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        # print("here in register")

        email = userdata['user']
        passwd = userdata['pass']
        
        datapost={
            'first_name': userdata['name_th'],
            'last_name': userdata['surname_th'],
            'user_email': email,
            'password': passwd,
            'password_confirmation': passwd,
            'phone':userdata['tel']            
        }

        r = self.httprequestObj.http_get('http://9asset.com/register')
        data = r.text
        soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
        authenticityToken = soup.find("input", {"name": "_token"})['value']
        datapost['_token'] = authenticityToken
        r = self.httprequestObj.http_post('http://9asset.com/register', data = datapost)
        data = r.json()
        # print(data)
        
        # print(matchObj)
        if data["status"] == "success":
            success = "True"
            detail = "Successful Registration"
        else:
            success = "False"
            detail = "Registration Unsuccessful"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "nineasset",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            'ds_id':userdata['ds_id']
        }

    def test_login(self, logindata):
        # print("Here in test_login")
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        email_user = logindata['user']
        email_pass = logindata['pass']
        datapost = {
            'email' : email_user,
            'password' : email_pass,
        }
        r = self.httprequestObj.http_get('https://9asset.com/login')
        data = r.text
        soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
        authenticityToken = soup.find("input", {"name": "_token"})['value']
        datapost['_token'] = authenticityToken
        
        
        
        # print(datapost)
        r = self.httprequestObj.http_post('https://9asset.com/loginMember', data=datapost)
        data = r.text
        matchObj = re.search(r'???????????????????????????????????????????????????', data)
        # print(data)
        # print("Data Printed")
        # print(matchObj)
        if r.url=='https://9asset.com/profile':
            success = "True"
            detail = "Sucessful Login"
        else:
            success = "False"
            detail = "Login Unsucessful"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        # print({
        #     "websitename": "nineasset",
        #     "success": success,
        #     "start_time": str(time_start),
        #     "end_time": str(time_end),
        #     "detail": detail,
        # })
        return {
            "websitename": "nineasset",
            "success": success,
            "ds_id": logindata['ds_id'],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
        }
        #
        #
        #

    def create_post(self, postdata):
        # https://www.thaisecondhand.com/post/get_json_district?province_id=13   ->     for district
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
        try:
            direction = str(int(postdata['direction_type']))
        except:
            direction = "-1"
        try:
            view = str(int(postdata['view_type']))
        except:
            view = "-1"
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
        post_title_th = postdata['post_title_th']
        post_description_th = postdata['post_description_th']
        # post_title_en = postdata['post_title_en']
        # post_description_en = postdata['post_description_en']
        try:
            floor_no = postdata['floor_level']
        except:
            floor_no = ""
        try:
            bedroom = postdata['bed_room']
        except:
            bedroom = ""
        try:
            bathroom = postdata['bath_room']
        except:
            bathroom = ""
        # ds_id = postdata["ds_id"]
        # name = postdata["name"]
        # mobile = postdata["mobile"]
        # email = postdata["email"]
        # account_type = postdata["account_type"]
        user = postdata["user"]
        password = postdata["pass"]
        if 'web_project_name' in postdata and postdata['web_project_name'] is not None:
            project_n = postdata['web_project_name']
        elif 'project_name' in postdata and postdata['project_name'] is not None:
            project_n = postdata['project_name']
        else:
            project_n = postdata['post_title_th']
        # project_name = postdata["project_name"]
        land_size_rai = postdata['land_size_rai']
        land_size_ngan = postdata['land_size_ngan']
        land_size_wah = postdata['land_size_wa']
        # post_description_en =  post_description_en.replace("\r\n","<br>")
        # post_description_th =  post_description_th.replace("\r\n","<br>")
        # print(post_description_th)
        try:
            floorarea = postdata['floor_area'] # Calc floor area
        except :
            floorarea = ""
        direction_type = {"-1":"",  "11" :"2",  "12" : "3", "13" : "1", "14" : "4", "21":"5","23":"6", "22":"8","24":"9"}
        # 12 ????????? south
        # 13 ????????? east
        # 14 ?????? west
        # 21 ???????????? north east 
        # 22 ???????????? south ease
        # 23 ???????????? north west
        # 24 ???????????? south west 
        # print(direction)
        try:
            direction = str(int(direction_type[str(direction)]))
        except:
            direction = ""
        view_type = {"-1":"","15" :"6", "16":"1", "17":"3", "18":"2", "19":"7", "20":"5" } 
        try:
            view = str(int(view_type[str(view)]))
        except:
            view = ""
        # 15 rivers
        # 16 gardens
        # 17 cities
        # 18 swimming pool
        # 19 mountains
        # 20 sea     
        province = {}
        with open('./static/9asset_province.json') as f:
            province = json.load(f)

        '''for i,j in province.items():
            print(f"{i}:{j}")
        exit(1)'''
        for key in province.keys():
            if 'province' not in key:
                if (addr_province.find(str(province[key]).strip()) != -1) or (str(province[key]).find(addr_province) != -1):
                    addr_province = key
                    break

        for key in province[addr_province+"_province"]:
            if(addr_district.find(province[addr_province+"_province"][key].strip()) != -1) or (str(province[addr_province+"_province"][key]).find(addr_district) != -1):
                addr_district = key
                break

        #print("<<<>>>", addr_province, "<<<>>>")
        #print("<<<>>>", addr_district, "<<<>>>")

        datapost = [
            ("status_upload","true"),
            ("TypePosted[]","2" if (listing_type == "?????????" ) else "1"),
            ("category_ID", 1),
            ("property_Name", post_title_th),
            ("project_Name", project_n),
            ("project_ID", ""),
            ("Bedroom", bedroom),
            ("Bathroom-hidden",""),
            ("Bathroom",bathroom),
            ("property_Size", floorarea), #usable area
            ("Land_Rai",land_size_rai),
            ("Land_Nga", land_size_ngan),
            ("Land_Sqw", land_size_wah),
            ("Land_Size" , ""),#str(400*int(land_size_rai) + 100 * int(land_size_ngan) + 1*int(land_size_wa)),#calc using formula,
            ("property_Floor", floor_no),
            ("property_Facing",direction),
            ("property_View",view),
            ("province", addr_province),
            ("city", addr_district),
            ("Road", ""),
            ("Alley", ""),
            ("House_No",""),
            ("location-lat", geo_latitude),
            ("location-lng", geo_longitude),
            ("zoom_map",16),
            ("others", post_description_th),
            ("agent", 2),
            ("AgentsSub", 2-3),
            ("House_Type", ""),
            ("StatusPosted", 1),
            ("Issubmit","posted"),
        ]
        
        if (listing_type == "?????????" ):
            datapost.append(("Sell", "1"))
            datapost.append(("property_Sell", price_baht))
            datapost.append(("property_PriceSq-hidden" , ""))
        else :
            datapost.append(("Rent" , "1"))
            datapost.append(("Price_Rent", price_baht))
        
        
        if(property_type == "1"):
            #Condo
            datapost.append(("category_ID" , "1"))
            
        elif(property_type == "2"):
            #Single House
            datapost.append(("category_ID", "3"))
            
        elif(property_type == "3"):
            #twin house
            datapost.append(("category_ID" , "24"))
            
        elif(property_type == "4"):
            #Townhouse-Home
            datapost.append(("category_ID", "2"))
            
        elif(property_type == "5"):
            #commercial building
            datapost.append(("category_ID", "9"))
            datapost.append(("Usable_Area", floorarea))
            datapost.append(("Shop", ""))
            datapost.append(("Shop-hidden", ""))

        elif(property_type == "6"):
            #land
            datapost.append(("Fill", "yes"))
            datapost.append(("category_ID", "5"))

        elif(property_type == "7"):
            #Apartment
            datapost.append(("Building", ""))
            datapost.append(("Unit",""))
            datapost.append(("category_ID", "7"))

        elif(property_type == "8"):
            #hotel
            datapost.append(("Unit", ""))
            datapost.append(("Building", ""))
            datapost.append(("Hotel_Style", "")) 
            datapost.append(("category_ID", "11"))

        elif(property_type == "9"):
            #Office Space
            datapost.append(("Building",""))
            datapost.append(("Ceiling_heigh", ""))
            datapost.append(("category_ID", "6"))
            
        elif(property_type == "10"):
            #warehouse
            datapost.append(("category_ID", "8"))
            
        elif(property_type == "25"):
            #factory
            datapost.append(("category_ID", "16"))

        # login
        login = self.test_login(postdata)
        success = login["success"]
        detail = login["detail"]
        post_id = ""
        post_url = ""
        filestoup = {}
        # print("postimages",postdata['post_images'])
        imagename = []
        
        # print(datapost["first"])
        # print("debug")
        # print(filestoup)
        if success == "True":
            for i in range(len(postdata['post_images'][:10])):
                # print(i)
                filestoup["images[0]"] = open(os.getcwd() + "/"+ postdata['post_images'][i],'rb')
                r = self.httprequestObj.http_post('https://www.9asset.com/file/upload',data="", files = filestoup)
                imagename.append(r.json()[0]["full"])
                datapost.append(('images[]', r.json()[0]["full"]))
            # print(imagename)
            # print("debug2")
            r = self.httprequestObj.http_post('http://9asset.com/getDistrictAjax', data = {"city" : addr_district })
            soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
            districtcontent = [[str(x.text),str(x['value'])] for x in soup.find_all('option')]
            for i in districtcontent:
                if(i[0] == addr_district):
                    datapost.append(('district', i[1]))
                    break
            # print(datapost)
            r = self.httprequestObj.http_post('https://www.9asset.com/posted/save', data = datapost)#/property/show
            data = r.text
            link = re.findall(r'Posted form success',data)
            # print("printing link",link)
            if len(link) == 0:
                success = "False"
                detail = "Cannot post to 9asset"
            else:
                r = self.httprequestObj.http_get('http://9asset.com/profile')
                soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
                for a in soup.find_all('a'):
                    try:   
                        # print(a["class"]) 
                        if("btn-info" in a["class"]):
                            post_url = a["href"]
                            temp = 0
                            post_id = ""
                            for i in post_url :
                                if(temp == 4 and i != '/'):
                                    post_id += i
                                if(i == '/'):
                                    temp += 1
                            detail = 'Successful Post'
                            break
                    except :
                        continue
                if post_url=="":
                    success = "False"
                    detail = "Cannot find post on dashboard"
                    post_id = ""

        time_end = datetime.datetime.utcnow()
        return {
            "websitename": "nineasset",
            "success": success,
            "time_usage": time_end - time_start,
            "start_time": time_start,
            "end_time": time_end,
            "ds_id": postdata['ds_id'],
            # "ds_id": "4",
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "",
            "detail": detail
        }

    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        post_id = postdata['post_id']
        log_id = postdata['log_id']
        email_user = postdata['user']
        email_pass = postdata['pass']

        #
        #
        #

        time_end = datetime.datetime.utcnow()
        return {
            "websitename": "nineasset",
            "success": "false",
            "time_usage": time_end - time_start,
            "start_time": time_start,
            "end_time": time_end,
            "detail": "boost post is paid",
            'ds_id': postdata['ds_id'],
            "log_id": log_id,
            "post_id": post_id,
            "post_view": ""
        }

    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        login = self.test_login(postdata)
        success = login["success"]
        detail = login["detail"]
        post_id = postdata['post_id']

        if success == "True":
            # r = self.httprequestObj.http_get("http://9asset.com/myposted")
            # data = r.text
            # if re.search(str(post_id), data):  
            r = self.httprequestObj.http_get("http://9asset.com/posted/"+str(post_id)+"/delete")#/property/show
            data = r.text           
            if re.search("??????????????????????????????????????????????????????????????????????????????",data):
                detail = "Post sucessfully deleted"   
            elif re.search("Whoops, looks like something went wrong", data):
                success = "False"
                detail  = "No post found with given id"
            else:
                success = "False"
                detail = "Cannot delete post with id "+post_id 
        time_end = datetime.datetime.utcnow()
        return {
            "websitename": "nineasset",
            "success": success,
            "time_usage": time_end - time_start,
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            'post_id': postdata['post_id'],
            "start_time": time_start,
            "end_time": time_end,
            "detail": detail,

        }

    def edit_post(self, postdata):
        # https://www.thaisecondhand.com/post/get_json_district?province_id=13   ->     for district
        #print('start')
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
        try:
            direction = str(int(postdata['direction_type']))
        except:
            direction = "-1"
        try:
            view = str(int(postdata['view_type']))
        except:
            view = "-1"
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
        post_title_th = postdata['post_title_th']
        post_description_th = postdata['post_description_th']
        if 'web_project_name' in postdata and postdata['web_project_name'] is not None:
            project_n = postdata['web_project_name']
        elif 'project_name' in postdata and postdata['project_name'] is not None:
            project_n = postdata['project_name']
        else:
            project_n = postdata['post_title_th']
        # post_title_en = postdata['post_title_en']
        # post_description_en = postdata['post_description_en']

        try:
            floor_no = postdata['floor_level']
        except:
            floor_no = ""
        try:
            bedroom = postdata['bed_room']
        except:
            bedroom = ""
        try:
            bathroom = postdata['bath_room']
        except:
            bathroom = ""
        # ds_id = postdata["ds_id"]
        # name = postdata["name"]
        # mobile = postdata["mobile"]
        # email = postdata["email"]
        # account_type = postdata["account_type"]
        user = postdata["user"]
        password = postdata["pass"]
        # project_name = postdata["project_name"]
        land_size_rai = postdata['land_size_rai']
        land_size_ngan = postdata['land_size_ngan']
        land_size_wah = postdata['land_size_wa']
        # post_description_en =  post_description_en.replace("\r\n","<br>")
        # post_description_th =  post_description_th.replace("\r\n","<br>")
        # print(post_description_th)
        try:
            floorarea = postdata['floor_area'] # Calc floor area
        except :
            floorarea = ""
        direction_type = {"-1":"",  "11" :"2",  "12" : "3", "13" : "1", "14" : "4", "21":"5","23":"6", "22":"8","24":"9"}
        # 12 ????????? south
        # 13 ????????? east
        # 14 ?????? west
        # 21 ???????????? north east 
        # 22 ???????????? south ease
        # 23 ???????????? north west
        # 24 ???????????? south west 
        # print(direction)
        # try:
        #     direction = direction_type[direction]
        # except
        #     direction = ""
        view_type = {"-1":"","15" :"6", "16":"1", "17":"3", "18":"2", "19":"7", "20":"5" } 
        # try:
        #     view = view_type[view]
        # else:
        #     view = ""
        # 15 rivers
        # 16 gardens
        # 17 cities
        # 18 swimming pool
        # 19 mountains
        # 20 sea     
        province = {}
        with open('./static/9asset_province.json') as f:
            province = json.load(f)
        # print(province)
        for key in province:
            if 'province' not in key:
            # print("bleh")
                if (addr_province.find(str(province[key]).strip()) != -1) or str(province[key]).find(addr_province) != -1:
                    addr_province = key
                    print(addr_province)
                    break
        for key in province[addr_province+"_province"]:
            if(addr_district.find(province[addr_province+"_province"][key].strip()) != -1)  or str(province[addr_province+"_province"][key]).find(addr_district) != -1:
                addr_district = key
                break
            
        datapost = [
            ("status_upload","true"),
            ("TypePosted[]","2" if (listing_type == "?????????" ) else "1"),
            ("category_ID", 1),
            ("property_Name", post_title_th),
            ("project_Name", project_n),
            ("property_Unit", 1), #Default as of now
            ("Bedroom", bedroom),
            ("Bathroom-hidden",""),
            ("Bathroom",bathroom),
            ("property_Size", floorarea), #usable area
            ("Land_Rai",land_size_rai),
            ("Land_Nga", land_size_ngan),
            ("Land_Sqw", land_size_wah),
            ("Land_Size" , ""),#str(400*int(land_size_rai) + 100 * int(land_size_ngan) + 1*int(land_size_wa)),#calc using formula,
            ("property_Floor", floor_no),
            ("property_Facing", direction_type[direction]),
            ("property_View", view_type[view]),
            ("province", addr_province),
            ("city", addr_district),
            ("Road", ""),
            ("Alley", ""),
            ("House_No",""),
            ("location-lat", geo_latitude),
            ("location-lng", geo_longitude),
            ("zoom_map",16),
            ("others", post_description_th),
            ("agent", 2),
            ("AgentsSub", 2-3),
            ("House_Type", ""),
            ("StatusPosted", 1),
            ("Issubmit","posted"),
        ]  
        #print('sw')
        if (listing_type == "?????????" ):
            datapost.append(("Sell", "1"))
            datapost.append(("property_Sell", price_baht))
            datapost.append(("property_PriceSq-hidden" , ""))
        else:
            datapost.append(("Rent", "1"))
            datapost.append(("Price_Rent", price_baht))
        
        #print('mid')
        if(property_type == "1"):
            #Condo
            datapost.append(("category_ID" , "1"))
            
        elif(property_type == "2"):
            #Single House
            datapost.append(("category_ID", "3"))
            
        elif(property_type == "3"):
            #twin house
            datapost.append(("category_ID" , "24"))
            
        elif(property_type == "4"):
            #Townhouse-Home
            datapost.append(("category_ID", "2"))
            
        elif(property_type == "5"):
            #commercial building
            datapost.append(("category_ID", "9"))
            datapost.append(("Usable_Area", floorarea))
            datapost.append(("Shop", ""))
            datapost.append(("Shop-hidden", ""))

        elif(property_type == "6"):
            #land
            datapost.append(("Fill", "yes"))
            datapost.append(("category_ID", "5"))

        elif(property_type == "7"):
            #Apartment
            datapost.append(("Building", ""))
            datapost.append(("Unit",""))
            datapost.append(("category_ID", "7"))

        elif(property_type == "8"):
            #hotel
            datapost.append(("Unit", ""))
            datapost.append(("Building", ""))
            datapost.append(("Hotel_Style", "")) 
            datapost.append(("category_ID", "11"))

        elif(property_type == "9"):
            #Office Space
            datapost.append(("Building",""))
            datapost.append(("Ceiling_heigh", ""))
            datapost.append(("category_ID", "6"))
            
        elif(property_type == "10"):
            #warehouse
            datapost.append(("category_ID", "8"))
            
        elif(property_type == "25"):
            #factory
            datapost.append(("category_ID", "16"))

        #print('here')

        # login
        login = self.test_login(postdata)
        success = login["success"]
        detail = login["detail"]
        post_id = postdata["post_id"]
        post_url = ""
        filestoup = {}
        # print("postimages",postdata['post_images'])
        imagename = []

        # print(datapost["first"])
        #print("debug")
        #print(success)
        # print(filestoup)
        if(success == "True"):
            for i in range(len(postdata['post_images'][:10])):
                filestoup["images[0]"] = open(os.getcwd() + "/"+ postdata['post_images'][i],'rb')
                r = self.httprequestObj.http_post('https://www.9asset.com/file/upload',data="", files = filestoup)
                imagename.append(r.json()[0]["full"])
                datapost.append(('images[]', r.json()[0]["full"]))
            # print(imagename)

            r = self.httprequestObj.http_post('https://www.9asset.com/getDistrictAjax', data = {"city" : addr_district })
            soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
            districtcontent = [[str(x.text),str(x['value'])] for x in soup.find_all('option')]
            for i in districtcontent:
                if(i[0] == addr_district):
                    datapost.append(('district', i[1]))
                    break
            r = self.httprequestObj.http_get('https://www.9asset.com/form/'+str(post_id)+'/edit')
            soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
            project_id = soup.find("input", {"name": "project_ID"})
            if project_id:
                project_id = project_id.get('value')
                datapost.append(("project_ID", project_id))
                # print(datapost)
                r = self.httprequestObj.http_post('https://www.9asset.com/posted/save/'+str(post_id), data = datapost)#/property/show
                data = r.text
                # print(data)
                link = re.findall(r'????????????????????????????????????',data)
                # print("printing link",link)
                if len(link) == 0:
                    success = "False"
                    detail = "Cannot edit to 9asset"
                else:
                    # r = self.httprequestObj.http_get('http://9asset.com/profile')
                    # soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
                    # for a in soup.find_all('a'):
                    #     try:   
                    #         # print(a["class"]) 
                    #         if("btn-info" in a["class"]):
                    #             post_url = a["href"]
                    #             if(re.search(str(post_id),post_url)):
                    #                 break
                    #     except:
                    #         continue
                    success = "true"
                    detail = "Post edited successfully"
            else:
                success = "false"
                detail = "No post found with given id"
        time_end = datetime.datetime.utcnow()
        return {
            "websitename": "nineasset",
            "success": success,
            "time_usage": time_end - time_start,
            "start_time": time_start,
            "end_time": time_end,
            # "ds_id": "4",
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            # "post_url": postdata['post_url'],
            "post_id": post_id,
            "account_type": "",
            "detail": detail
        }

    def search_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()
        test_login = self.test_login(postdata)
        post_create=""
        post_view = ""
        my_res = dict()
        my_res.update({
                'websitename':'nineasset',
                'ds_id':postdata['ds_id'],
                'start_time':str(start_time)
        })
        if test_login['success'] == "True":
            post_title = str(postdata['post_title_th'])
            r = self.httprequestObj.http_get('https://www.9asset.com/profile')
            soup = BeautifulSoup(r.content, 'html.parser')
            pages = soup.find('ul', attrs={'class': 'pagination'})
            last = pages.find_all('li')[-1]
            max_p = int(str(last.find('a')['href']).split('=')[-1])
            post_found = 'false'
            for page in range(1, max_p+1):
                tURL = dict()
                url = "https://www.9asset.com/profile?page=%d" % page
                if post_found == 'True':
                    break
                r = self.httprequestObj.http_get(url)
                soup = BeautifulSoup(r.content, 'html.parser')
                soup = soup.find('table', attrs={'class':'table', 'id':'customers'})
                if soup == None:
                    break
                result_posts = soup("tr")
                result_posts = [row.findAll('td') for row in result_posts]
                tURL.update({post[1].string : str(post[-1].find('a', attrs={'class':'btn btn-info'})['href']) for post in result_posts if len(post)>=2})

                flag = 0
                ind = 0

                for i in tURL.keys():

                    if str(i) == post_title:
                        pg = self.httprequestObj.http_get(tURL[i])
                        page = BeautifulSoup(pg.text,'html.parser')

                        date = page.findAll('div',attrs = {'class':'col-xs-8 nopadding'})

                        post_create = (date[-1].text).replace('\n','').replace('\t','')
                        post_found = 'True'
                        my_res.update({
                            'success':'true',
                            'post_found': post_found,
                            'post_url':tURL[post_title],
                            'detail':'Post found',
                            'post_id':tURL[post_title].split('/')[-2],
                            'post_create_time':post_create[13:],
                            'post_view':post_view,
                            'websitename': 'nineasset'
                        })
                        flag=1
                        break
                    ind+=1

            if flag==1:
                pass
            else:
                my_res.update({
                    'success':'true',
                    'post_found':'false',
                    'detail': 'Post not found',
                    'post_url':'',
                    'post_id':'',
                    'post_create_time':'',
                    'post_view':''
                })
            my_res.update({
                    
                    'log_id':postdata['log_id'],
                    'end_time':str(datetime.datetime.utcnow()),
                    'account_type':'',
                    'post_modify_time':''
                })
        return my_res

    def print_debug(self, msg):
        if(self.debug):
            print(msg)
        return True