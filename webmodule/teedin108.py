# -*- coding: utf-8 -*-
import codecs

from .lib_httprequest import *

from bs4 import BeautifulSoup
import os.path
import re
import json
import datetime
import sys
from urllib.parse import unquote
import requests

httprequestObj = lib_httprequest()

with open("./static/teedin108_provincedata.json") as f:
    # ./static/teedin108_provincedata.json

    provincedata = json.load(f)

# sess = requests.session()

class teedin108():

    name = 'teedin108'

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

    def logout_user(self):
        url = 'https://www.teedin108.com/member/logout/'
        httprequestObj.http_get(url)

    def register_user(self, postdata):
        self.logout_user()
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')

        time_start = datetime.datetime.utcnow()
        # start process
        #
        # set required urls
        url_register = "https://www.teedin108.com/member/ajaxregister/"
        url_email = "https://www.teedin108.com/member/emailexist/"

        # set form data from the loaded file
        name = postdata["name_th"] + " " + postdata["surname_th"]
        email = postdata["user"]
        tel_no = postdata["tel"]
        password = postdata["pass"]

        data = {
            "email": email,
            "name": name,
            "telephone": tel_no,
            "password": password
        }
        email_data = {
            "email": email
        }
        
        #initialize outputs
        success = False

        # check if email already exists
        resp_email = httprequestObj.http_post(url_email, data=email_data)

        # note usage time and end time
        time_end = datetime.datetime.utcnow()
        
        # parse response
        '''
        A     - email already exists
        S     - email exists but isnt registered
        false - email doesn't exist
        '''
        try:
            if resp_email.json()["data"]["status_code"] == 'A': 
                detail = "This email already exists. Please login" 
            elif resp_email.json()["data"]["status_code"] == 'S': 
                detail = "This email already exists. Please confirm your email subscription."
            else:
                # send POST request for registering
                resp_reg = httprequestObj.http_post(url_register, data=data)

                # parse register response
                if resp_reg.json()["data"]["sended"]:
                    success = True
                detail = "Membership is successful. Please confirm your email subscription"
                
                # note end and usage time
                time_end = datetime.datetime.utcnow()
        except:
            success = False
            detail = "Unexpected error"

        time_usage = str(time_end - time_start)
       
        #
        # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "teedin108",
            'ds_id': postdata['ds_id'],
            "success": success,
            "usage_time": time_usage,
            "start_time": time_start,
            "end_time": time_end,
            "detail": detail,
        }

    def test_login(self, postdata):
        self.logout_user()
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # set required urls
        url_verify = "https://www.teedin108.com/member/ajaxverify/"

        # generate form data
        data = {
            "email": postdata["user"],
            "password": postdata["pass"]
        }
        # data = {
            # "email": postdata["web"][0]["user"],
            # "password": postdata["web"][0]["pass"]
        # }

        # initialize outputs
        success = False
        detail = "Email or password is incorrect."

        # note start time
        start = datetime.datetime.utcnow()

        # send POST request
        # r = httprequestObj.http_post(url_verify, data)
        r = httprequestObj.http_post(url_verify, data)

        # parse response received and set outputs accordingly
        try:
            if r.json()["data"]["status"] == "A":
                success = True
                detail = "Login successful" 
            if r.json()["data"]["status"] == "S":
                success = True
                detail = "You have not confirmed your email subscription." 
        except:
            success = False
            detail = "Unexpected error"
        #
        # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "teedin108",
            "ds_id": postdata['ds_id'],
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
        }
        


    def create_post(self, postdata):

        time_start = datetime.datetime.utcnow()
        # print("In create")
        # login
        login = self.test_login(postdata)
        success = login["success"]
        detail = login["detail"]
        post_id = ""
        post_url = ""
        
        if not success:
            detail = "Invalid credentials to login"
        else:
            # poster details
            p_name = postdata["name"]
            p_tel = postdata["mobile"]
            p_email = postdata["email"]

            datapost = {
                "description": postdata["post_description_th"],
                "posterEmail": p_email,
                "posterTelephone": p_tel,
            }
            r = httprequestObj.http_post('https://www.teedin108.com/post/bancheck/', data=datapost)
            data = r.text
            datajson = r.json()

            #f = open("debug_response/teedinajax.html", "wb")
            # f.write(data.encode('utf-8').strip())

            # print("Post bancheck")

            if datajson["success"] != True:
                success = False
                detail = data

            else:

                #parse province
                prov = postdata["addr_province"].strip()
                distr = postdata["addr_district"].strip()
                sect = ""

                # test

                # set default values
                if prov == "":
                    prov = "กรุงเทพ"
                if distr == "":
                    distr = "พญาไท"

                s_found = 0
                prov_val = 1
                prov_found = ""
                for s in provincedata:
                    for p in provincedata[s]:
                        if (prov in p) or (p in prov):
                            prov_val = provincedata[s][p]["value"]
                            prov_found = p
                            sect = s
                            s_found = 1

                if sect == "":
                    s=provincedata[0]
                    p=provincedata[s]
                    prov_val = provincedata[s][p]["value"]
                    prov_found = p
                    sect=s
                    # detail = "Given province does not exist in any sector"
                    # success = False

                # if not (distr in provincedata[sect][prov]):
                    # detail = "Given district does not exist in the province"
                    # success = False

                # print("Sector selected")

                distr_val = 33
                try:
                    for d in provincedata[sect][prov_found]:
                        if (distr in d) or (d in distr):
                            distr_val = provincedata[sect][prov_found][d]
                except:
                    distr_val = 33

                try:
                    sect_val = provincedata[sect]["value"]
                except:
                    sect_val = 2
                # try:
                    # prov_val = provincedata[sect][prov]["value"]
                # except:
                    # prov_val = 1
                # try:
                    # distr_val = provincedata[sect][prov][distr]
                # except:
                    # distr_val = 33

                # listing type
                post_type = "S" #default value
                if (postdata["listing_type"] == "เช่า"):
                    post_type = "R"
                elif (postdata["listing_type"] == "ซื้อ"):
                    post_type = "B"
                elif (postdata["listing_type"] == "เช่า"):
                    post_type = "L"

                # property type code
                property_type_code = "L" #default value
                if postdata["property_type"] == "1":
                    property_type_code = "C"
                if postdata["property_type"] in ["2", "3", "4"]:
                    property_type_code = "H"

                # subject
                subject = ""
                # description
                desc = str(postdata['post_description_th'])

                if "post_title_th" in postdata:
                    subject = str(postdata["post_title_th"])
                # if "project_name" in postdata:
                    # subject = postdata["project_name"]
                # if "web_project_name" in postdata:
                    # subject = postdata["web_project_name"]

                if subject == "":
                    success = False
                    detail = "Empty subject"
                elif desc == "":
                    success = False
                    detail = "Empty description"
                else:
                    #images
                    # img = postdata["post_images"][0]
                    try:
                        img_path = os.getcwd()+"/"+postdata["post_images"][0]
                    except:
                        img_path = os.getcwd()+"/"+"imgtmp/default/white.png"

                    files = {
                        "files[]": open(img_path, "rb")
                    }

                    # print("Before file upload")

                    r = httprequestObj.http_post("https://www.teedin108.com/post/ajaxupload/", data={}, files = files)
                    r_json = r.json()

                    try:
                        img = r_json["files"][0]["name"]
                    except:
                        img = ""
                    #map use
                    if postdata["geo_latitude"] == "" or postdata["geo_longitude"] == "":
                        map_use = "0"
                    else:
                        map_use = "1"

                    data = {
                        "data[lat_lng]": str(postdata["geo_latitude"])+", "+str(postdata["geo_longitude"]),
                        "data[post_type_code]": post_type,
                        "data[property_type_code]": property_type_code,
                        "data[geo_id]":sect_val,
                        "data[province_id]":prov_val,
                        "data[amphur_id]":distr_val,
                        "data[district_id]":"",
                        "data[subject]": subject,
                        "data[price]": postdata["price_baht"],
                        "data[description]": desc,
                        "files[]": "(binary)",
                        "photos[name][]": img,
                        "photos[angle][]": 0,
                        "data[map_use]": map_use,
                        "data[poster_name]": p_name,
                        "data[poster_telephone]": p_tel,
                        "data[poster_email]": p_email,
                        "data[poster_lineid]":"",
                        "data[password]": postdata["pass"][:10]
                    }

                    if img == "":
                        del data["photos[name][]"]
                        del data["photos[angle][]"]

                    url = ""     
                    resp = httprequestObj.http_post("https://www.teedin108.com/post/add", data=data)
                    soup = BeautifulSoup(resp.text, 'html.parser')

                    url = soup.find("meta", property="og:url")
                    # print(f'url ---> {url}')

                    if url:
                        print(url["content"])
                        post_url = url["content"]
                        temp = post_url.split("/")
                        for i in range(len(temp)):
                            if temp[i] == "view":
                                post_id = temp[i+1]
                        detail = "Posted successfully"
                    else:
                        success = False
                        detail = soup.find("div", {'id':'content'}).text

        # # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "websitename": "teedin108",
            "success": success,
            "ds_id": postdata['ds_id'],
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": post_url,
            "post_id": post_id,
            "detail": detail
        }

    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        log_id = postdata['log_id']
        post_id = postdata['post_id']
        user = postdata['user']
        passwd = postdata['pass']

        # start process
        #
        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]

        if success == True:
            datapost = {
                "post_id": post_id,
                "password": passwd
            }
            r = httprequestObj.http_post('https://www.teedin108.com/post/trash/', data=datapost)
            data = r.text
            datajson = r.json()
            detail = "Successfully deleted"
            try:
                if datajson["data"]["trash"] == False:
                    success = "false"
                    detail = "cannot delete, not found post id "+str(post_id)
            except:
                detail = "Unexpected error occured"
            # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "websitename": "teedin108",
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            'ds_id': postdata['ds_id'],
            "log_id": log_id,
            "post_id": postdata['post_id']
        }

    def edit_post(self, postdata):

        time_start = datetime.datetime.utcnow()
        post_id = postdata["post_id"]
        detail = ""

        data = {
                "post_id": postdata["post_id"],
                "password": postdata["pass"]
        }

        r = httprequestObj.http_post("https://www.teedin108.com/post/verify/", data=data)
        r = httprequestObj.http_get("https://www.teedin108.com/post/edit/"+str(post_id))

        p_name = postdata["name"]
        p_tel = postdata["mobile"]
        p_email = postdata["email"]

        #parse province
        prov = postdata["addr_province"].strip()
        distr = postdata["addr_district"].strip()
        sect = ""

        # test

        # set default values
        if prov == "":
            prov = "กรุงเทพ"
        if distr == "":
            distr = "พญาไท"


        s_found = 0
        prov_val = 1
        prov_found = ""
        for s in provincedata:
            for p in provincedata[s]:
                if (prov in p) or (p in prov):
                    prov_val = provincedata[s][p]["value"]
                    prov_found = p
                    sect = s
                    s_found = 1

        if sect == "":
            detail = "Given province does not exist in any sector"
            # success = False


        # if s_found:
        #     if not (distr in provincedata[sect][prov]):
        #         detail = "Given district does not exist in the province"
        #         # success = False
        distr_val = 33

        try:
            for d in provincedata[sect][prov_found]:
                if (distr in d) or (d in distr):
                    distr_val = provincedata[sect][prov_found][d]
        #     sect_val = provincedata[sect]["value"]
        # except:
        #     sect_val = 2
        # try:
        #     prov_val = provincedata[sect][prov]["value"]
        except:
            distr_val = 33
            # prov_val = 1
        try:
            sect_val = provincedata[sect]["value"]
        except:
            sect_val = 2


        # listing type
        post_type = "S" #default value
        if (postdata["listing_type"] == "เช่า"):
            post_type = "R"
        elif (postdata["listing_type"] == "ซื้อ"):
            post_type = "B"
        elif (postdata["listing_type"] == "เช่า"):
            post_type = "L"


        # property type code
        property_type_code = "L" #default value
        if postdata["property_type"] == "1":
            property_type_code = "C"
        if postdata["property_type"] in ["2", "3", "4"]:
            property_type_code = "H"

        # subject
        subject = ""

        if "post_title_th" in postdata:
            subject = postdata["post_title_th"]
        # if "project_name" in postdata:
            # subject = postdata["project_name"]
        # if "web_project_name" in postdata:
            # subject = postdata["web_project_name"]

        if subject == "":
            success = False
            detail = "Empty subject"

        # description
        desc = postdata["post_description_th"]
        if desc == "":
            success = False
            detail = "Empty description"

        #images
        img = ""
        try:
            img = postdata["post_images"][0]
        except:
            pass
        
        if img != "":
                files = {
                    "files[]": open(os.getcwd()+'/'+img, "rb")  
                }
                r = httprequestObj.http_post("https://www.teedin108.com/post/ajaxupload/", data={}, files = files)
                r_json = r.json()

                try:
                    img = r_json["files"][0]["name"]
                except:
                    img = ""


        #map use
        map_data = ""
        map_use = 0
        if postdata["geo_latitude"] == "" or postdata["geo_longitude"] == "":
            map_use = "0"
        else:
            map_use = "1"
            map_data = str(postdata["geo_latitude"])+", "+str(postdata["geo_longitude"])

        data = {
            "data[lat_lng]": map_data, 
            "data[is_ads]":"",
            "data[post_type_code]": post_type,
            "data[property_type_code]": property_type_code,
            "data[geo_id]":sect_val,
            "data[province_id]": prov_val,
            "data[amphur_id]": distr_val,
            "data[district_id]": "0",
            "data[subject]": subject,
            "data[price]": postdata["price_baht"],
            "data[description]": desc,
            "files[]": "(binary)",
            "photos[name][]": img,
            "photos[angle][]": 0,
            "data[map_use]": map_use,
            "data[poster_name]": p_name,
            "data[poster_telephone]": p_tel,
            "data[poster_email]": p_email
        }
        if img == "":
            del data["photos[name][]"]
            del data["photos[angle][]"]

        data = httprequestObj.http_post('https://www.teedin108.com/post/save/'+str(post_id), data=data)
        success = True
        detail = "Successfully Edited"
        if not data.text:
            success = False
            detail = "Couldn't edit"
        # # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "websitename":"teedin108",
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id
        }

    def search_post(self, postdata):

        time_start = datetime.datetime.utcnow()
        data = {
            "search[post_type_code]": "A",
            "search[property_type_code]": "A",
            "search[geo_id]": 0,
            "search[subject]": postdata["post_title_th"],
            "search[price_begin]": ""
        }

        title = postdata["post_title_th"]

        r = httprequestObj.http_post("https://www.teedin108.com/search/", data)
        soup = BeautifulSoup(r.text, 'html.parser')

        div_container = []
        try:
            div_container = soup.find_all('div', class_='col-xs-12 postlist')
        except:
            pass

        sites = []
        # try:
        for post in div_container:
            div_title = post.find('div', 'row').find('div', 'col-xs-12').find('a').get('title')
            post_url = post.find('div', 'row').find('div', 'col-xs-12').find('a').get('href')
            # print(title)
            if (div_title == title):
                sites.append(post_url)
        # except:
        #     pass
        
        success = True
        post_found = False
        post_url = ""
        post_id = ""
        post_modify_time = ''
        post_view = ''

        for site in sites:
            r = httprequestObj.http_get(site)
            soup = BeautifulSoup(r.text, 'html.parser')
            div_container = soup.find_all('div', class_='poster-detail')[1]
            # print(postdata['user'])
            info = div_container.contents
            # print(info)
            # print(a.contents[0])
            if True:
                post_found = True
                post_url = site
                success = True
                post_modify_time = str(info[5])
                post_view = str(info[9].string)
                try:
                    post_id = post_url.split("/")[5]
                except:
                    pass

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        ret = {
                "websitename": "teedin108",
                "success": success,
                "post_found": post_found,
                "ds_id": postdata['ds_id'],
                "log_id": postdata['log_id'],
                "usage_time": str(time_usage),
                "start_time": str(time_start),
                "end_time": str(time_end),
                "post_found": post_found,
                "post_url": post_url,
                "post_id": post_id,
                "post_create_time": '',
                "post_modify_time": post_modify_time,
                "post_view": post_view
                }
        return ret

    def boost_post(self, postdata):
        time_start = datetime.datetime.utcnow()

        post_id = postdata["post_id"]
        user = postdata['user']
        passwd = postdata['pass']
        log_id = postdata["log_id"]

        data = {
                "post_id": postdata["post_id"],
                "password": postdata["pass"]
        }

        r = httprequestObj.http_post("https://www.teedin108.com/post/verify/", data=data)

        r = httprequestObj.http_get('https://www.teedin108.com/post/edit/'+str(post_id)+'/')

        data = {}
        resp = httprequestObj.http_post('https://www.teedin108.com/post/save/'+post_id+'/', data=data)

        detail = "Boosted successfully"
        success = True
        # end process
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "websitename": "teedin108",
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            'ds_id': postdata['ds_id'],
            "log_id": log_id,
            "post_id": post_id,
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

