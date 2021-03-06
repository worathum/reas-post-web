import requests, json, re, os, time, sys
from datetime import datetime
import shutil
from .lib_httprequest import *



class homedd():

    name = 'homedd'

    def __init__(self):

        try:
            import configs
        except ImportError:
            configs = {}

        encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.debug = 0
        self.debugresdata = 0
        self.parse = 'html.parser'
        self.httprequestObj = lib_httprequest()

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
            "websitename": "homedd",
            "success": "true",
            "time_usage": time_end - time_start,
            "time_start": time_start,
            "time_end": time_end,
            "detail": ""
        }

    def logout_user(self):
        url = 'http://homedd.co.th/logoff.php'
        self.httprequestObj.http_get(url)

    # To register a user
    def register_user(self,userdata):
        self.logout_user()
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')

        datapost = {
            "tname" : userdata["name_th"] + " " + userdata["surname_th"],
            "tphone" : userdata["tel"],
            "tmyemail" : userdata["user"],
            "tmypassword" : userdata["pass"],
            "tconfirmpassword" : userdata["pass"]
        }

        headers = {
            'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
        }

        success = False
        detail = ""

        start_time = datetime.utcnow()
        end_time = datetime.utcnow()
        
        f1 = True

        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*$'
        if(re.search(regex,datapost["tmyemail"])):  
            f1 = True
        else:  
            f1 = False

        if f1 == False:
            detail = "Invalid email-id"
        elif datapost["tname"] == "" :
            detail = "Please enter user's name"
        elif datapost["tmyemail"] == "" :
            detail = "Please enter user's email"            
        elif datapost["tmypassword"] == "" :
            detail = "Please enter user's password"     
        else:
            url = "http://homedd.co.th/member_register_aed.php?typ=add"
            try:
                start_time = datetime.utcnow()
                request = self.httprequestObj.http_post(url,data=datapost,headers=headers)
                end_time = datetime.utcnow()
                
                if '??????????????????????????????????????????????????????????????? ???????????????????????????????????????????????????????????????' in str(request.text):
                    detail = "The user is already registered!"
                else:
                    detail = "Successfully Registered !"
                    success = True

            except requests.exceptions.RequestException as e: 
                end_time = datetime.utcnow()
                detail = "Network Problem"

        return {
            "websitename" : 'homedd',
            "success" : success,
            "start_time" : start_time,
            "end_time" : end_time,
            "usage_time" : end_time - start_time,
            "ds_id": userdata['ds_id'],
            "detail" : detail
        }

    # To login a user
    def test_login(self,postdata):
        self.logout_user()
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')

        datapost = {
            'tlogin_email': postdata['user'],
            'tlogin_password': postdata['pass']
        }
        headers = {
            'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
        }

        success = False
        detail = ""

        start_time = datetime.utcnow()
        end_time = datetime.utcnow()

        f1 = True
        
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*$'
        if(re.search(regex,datapost["tlogin_email"])):  
            f1 = True
        else:  
            f1 = False

        if f1 == False:
            detail = "Invalid email-id"
        elif datapost["tlogin_email"] == "":
            detail = "Please enter user's email"
        elif datapost["tlogin_password"] == "":
            detail = "Please enter user's password"
        else:
            url = 'http://homedd.co.th/login_aed.php'
            try:
                start_time = datetime.utcnow()
                request = self.httprequestObj.http_post(url,data=datapost,headers=headers)
                end_time = datetime.utcnow()

                if '????????????????????????????????????' in str(request.text):
                    success = True
                    detail = "Successfully logged in!"
                else:
                    detail = "Unsucessful Login !"
                
            except requests.exceptions.RequestException as e:
                end_time = datetime.utcnow()
                detail = "Network Problem"
        
        return {
            "websitename" : "homedd",
            "success" : success,
            "start_time" : start_time,
            "end_time" : end_time,
            "usage_time" : end_time - start_time,
            "ds_id": postdata['ds_id'],
            "detail" : detail
        }

    def create_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')

        test_login = self.test_login(postdata)
        success= test_login["success"]
        detail = test_login["detail"]
        start_time = test_login["start_time"]
        end_time = test_login["end_time"]
        post_id = ""
        post_url = ""

        headers = {
                    'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
                  }

        # filename = "response.txt"

        # print(json.dumps(postdata, indent=4, sort_keys=True,default=str)) 

        if success == True:

            if 'web_project_name' not in postdata or postdata['web_project_name']!=None:
                if 'project_name' in postdata and postdata['project_name']!=None:
                    postdata['web_project_name'] = postdata['project_name']
                else:
                    postdata['web_project_name'] = postdata['post_title_th']
    

            proid = {
                '???????????????': '1',
                '??????????????????????????????': '2',
                '?????????????????????': '3',
                '?????????????????????????????????': '4',
                '??????????????????-????????????????????????????????????': '5',
                '??????????????????': '6',
                '?????????????????????????????????': '7',
                '??????????????????': '8',
                '??????????????????????????????????????????': '9',
                '???????????????-??????????????????': '10',
                '??????????????????':'25'
            }
            getProdId = {'1': 4, '2': 1, '3': 3, '4': 2,
                            '5': 6, '6': 8, '7': 5, '8': 9, '9': 6, '10': 7, '25': 7 }

            property_type = postdata["property_type"]
            try:
                theprodid = getProdId[proid[str(postdata['property_type'])]]
            except:
                theprodid = getProdId[str(postdata['property_type'])]
                for i in proid :
                    if proid[i] == str(postdata['property_type']):
                        property_type = i

            area = postdata["floor_area"]
            if property_type == "8":
                area = (400 * int(postdata["land_size_rai"])) + (100 * int(postdata["land_size_ngan"])) + int(postdata["land_size_wa"])


            taddress = ""
            for add in [postdata['addr_soi'],postdata['addr_road'],postdata['addr_sub_district'],postdata['addr_district'],postdata['addr_province']]:
                if add is not None:
                    taddress += add + " "

            listing_type = ""
            if postdata['listing_type'] == '?????????':
                listing_type = "2"
            else:
                listing_type = "3"

            addr_province = postdata['addr_province']
            addr_district = postdata['addr_district']

            provinnce = {}
            with open('./static/homedd_province.json') as f:
                province = json.load(f)
            for key in province:
                if (addr_province.find(str(province[key]).strip()) != -1) or str(province[key]).find(addr_province) != -1:
                    addr_province = key
                    break
            
            for key in province[addr_province+"_province"]:
                if(addr_district.find(province[addr_province+"_province"][key].strip()) != -1)  or str(province[addr_province+"_province"][key]).find(addr_district) != -1:
                    addr_district = key
                    break

            # if addr_province == postdata['addr_province']:
            #     addr_province = ""
            # if addr_district == postdata['addr_district']:
            #     addr_district = ""

            url = "http://homedd.co.th/member_property_add.php"
            request = self.httprequestObj.http_get(url)
            soup = BeautifulSoup(request.text, 'html5lib')
            
            tpCode = soup.find('input',attrs = {'name': 'tpCode'})['value']
            
            
            addr_sub_district = postdata['addr_sub_district'] 
            sub_district_data = ""       
            for name_list in soup.find_all('script',attrs = {'language' : 'javascript'}):
                sub_district_data += str(name_list)

            sub_district_data = '"' + str(sub_district_data) + '"'

            district_regex = "case '" + addr_district + "':.*?break;"
            result = re.findall(district_regex,sub_district_data)
            result = '"' + str(result) + "'"

            sub_district_regex = "new Option\('" + postdata["addr_sub_district"] + "[\s]*','[0-9]+'\);"
            r2 = re.findall(sub_district_regex,result)
            regex = "[0-9]+"
            if str(r2)!= "":
                if not re.findall(regex,str(r2)):
                    addr_sub_district = ""
                else:
                    addr_sub_district = re.findall(regex,str(r2))[0]


            # print(addr_province)
            # print(addr_district)
            # print(addr_sub_district)

            if addr_province == "" or addr_province == postdata["addr_province"]:
                addr_province = "0"
            if addr_district == "" or addr_district == postdata["addr_district"]:
                addr_district = "0"
            if addr_sub_district == "" or addr_sub_district == postdata["addr_sub_district"]:
                addr_sub_district = "0"



            for key,value in postdata.items():
                if value is None:
                    postdata[key] = " "

            if area is None:
                area = ""

            datapost = {
            "tpCode" : tpCode,
            "tproperty_type" : listing_type,
            "tproperty_formart" : property_type,
            "ttitle" : postdata["post_title_th"],
            "tproject_asset" : postdata["web_project_name"],
            "taddress" : taddress,
            "tstreet_name" : postdata["addr_road"],
            "tprovince" : addr_province,
            "tamphur" : addr_district,
            "tdistrict" : addr_sub_district,
            "tdetail" : postdata["post_description_th"].replace('\u2013','-').replace('\u00a0'," ").replace('\/','/'),
            "tfloor" : postdata["floor_total"],
            "tbedroom" : postdata["bed_room"],
            "tbathroom" : postdata["bath_room"],
            "tortherroom" : "0",
            "tspace" : postdata["floor_area"],
            "tarea" : area,
            "tprice" : postdata["price_baht"],
            "towner" : postdata["name"],
            "tphone" : postdata["mobile"],
            "lat_value" : postdata["geo_latitude"],
            "lon_value" : postdata["geo_longitude"],
        }




            files = {}
            allimages = postdata["post_images"][:10]
            # print(allimages)
            for i in range(len(allimages)):
                r = open(os.getcwd()+"/"+allimages[i], 'rb')
                files["testimage"+str(i+1)] = r

            # print(json.dumps(datapost, indent=4, sort_keys=True,default=str)) 

            if str(datapost["tproperty_type"]).strip() == "":
                detail = "Enter the Announcement Type"
                success = False
            elif str(datapost["tproperty_formart"]).strip() == "":
                detail = "Enter the Property Type"
                success = False
            elif datapost["ttitle"] == "":
                detail = "Enter the Topic"
                success = False
            # elif datapost["tprovince"] == "":
            #     detail = "Enter the Province name"
            #     success = False
            # elif datapost["tamphur"] == "":
            #     detail = "Enter the District name"
            #     success = False
            # elif not addr_sub_district or datapost["tdistrict"] == "":            
            #     detail = "Enter the Sub-District name"
            #     success = False
            elif datapost["tprice"] == "":
                detail = "Enter the Price"
                success = False
            elif datapost["towner"] == "":
                detail = "Enter the Seller's name"
                success = False
            elif datapost["tphone"] == "":
                detail = "Enter the Seller's Phone Number"
                success = False
            
            if success == True:
                newurl = "http://homedd.co.th/member_property_aed.php?typ=add"
                
                request = self.httprequestObj.http_post(newurl, data=datapost,headers=headers,files=files)


                # f = open(filename,"w+")
                # f.write(str(request.text))
                # f.close()
                # print(request.text)
                # with open(filename,'r') as file:
                if '???????????????????????????????????????????????????????????????' in str(request.text):
                    detail = "Successfully created the post"
                    success = True
                else:
                    # print(request.text)
                    detail = " Unsuccessful post creation !"
                    success = False

                #     file.close()

                # os.remove(filename)

                if success == True:
                    url = "http://homedd.co.th/member_property_list.php"
                    r = self.httprequestObj.http_get("http://homedd.co.th/member_property_list.php")

                    post_url = "http://www.homedd.co.th/property_display.php?id="
                    soup = BeautifulSoup(r.text,'lxml')

                    data = ""
                    for a in soup.find_all('a'):
                        data += str(a['href'])
                    
                    
                    regex = "javascript:confirmdelete\('[0-9]+'\);"
                    r = re.findall(regex,data)[0]

                    regex = "[0-9]+"
                    post_id = re.findall(regex,r)[0]
                    post_url += post_id
        end_time = datetime.utcnow()
        return {
            "success": success,
            "usage_time": str(end_time - start_time),
            "start_time": str(start_time),
            "end_time": str(end_time),
            "post_url": post_url,
            "post_id": post_id,
            "ds_id": postdata['ds_id'],
            "account_type": "null",
            "detail": detail,
            "websitename": "homedd",
        }



    def edit_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')

        test_login = self.test_login(postdata)
        success= test_login["success"]
        detail = test_login["detail"]
        start_time = test_login["start_time"]
        post_id = ""
        post_url = ""

        headers = {
                    'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
                  }

        # filename = "response.txt"
    


        if success == True:

            if 'web_project_name' not in postdata or postdata['web_project_name']!=None:
                if 'project_name' in postdata and postdata['project_name']!=None:
                    postdata['web_project_name'] = postdata['project_name']
                else:
                    postdata['web_project_name'] = postdata['post_title_th']
    

            proid = {
                '???????????????': '1',
                '??????????????????????????????': '2',
                '?????????????????????': '3',
                '?????????????????????????????????': '4',
                '??????????????????-????????????????????????????????????': '5',
                '??????????????????': '6',
                '?????????????????????????????????': '7',
                '??????????????????': '8',
                '??????????????????????????????????????????': '9',
                '???????????????-??????????????????': '10',
                '??????????????????':'25'
            }
            getProdId = {'1': 4, '2': 1, '3': 3, '4': 2,
                            '5': 6, '6': 8, '7': 5, '8': 9, '9': 6, '10': 7, '25': 7 }

            property_type = postdata["property_type"]
            try:
                theprodid = getProdId[proid[str(postdata['property_type'])]]
            except:
                theprodid = getProdId[str(postdata['property_type'])]
                for i in proid :
                    if proid[i] == str(postdata['property_type']):
                        property_type = i

            area = postdata["floor_area"]
            if property_type == "8":
                area = (400 * int(postdata["land_size_rai"])) + (100 * int(postdata["land_size_ngan"])) + int(postdata["land_size_wa"])


            taddress = ""
            for add in [postdata['addr_soi'],postdata['addr_road'],postdata['addr_sub_district'],postdata['addr_district'],postdata['addr_province']]:
                if add is not None:
                    taddress += add + " "


            listing_type = ""
            if postdata['listing_type'] == '?????????':
                listing_type = "2"
            else:
                listing_type = "3"

            addr_province = postdata['addr_province']
            addr_district = postdata['addr_district']

            provinnce = {}
            with open('./static/homedd_province.json') as f:
                province = json.load(f)


            for key in province:
                if (addr_province.find(str(province[key]).strip()) != -1) or str(province[key]).find(addr_province) != -1:
                    addr_province = key
                    break
            
            for key in province[addr_province+"_province"]:
                if(addr_district.find(province[addr_province+"_province"][key].strip()) != -1)  or str(province[addr_province+"_province"][key]).find(addr_district) != -1:
                    addr_district = key
                    break

            # if addr_province == postdata['addr_province']:
            #     addr_province = ""
            # if addr_district == postdata['addr_district']:
            #     addr_district = ""
            
            url = "http://homedd.co.th/member_property_add.php"
            request = self.httprequestObj.http_get(url)
            soup = BeautifulSoup(request.text, 'lxml')
            
            tpCode = soup.find('input',attrs = {'name': 'tpCode'})['value']
            
            
            addr_sub_district = postdata['addr_sub_district'] 
            sub_district_data = ""       
            for name_list in soup.find_all('script',attrs = {'language' : 'javascript'}):
                
                sub_district_data += str(name_list)


            sub_district_data = '"' + str(sub_district_data) + '"'

            district_regex = "case '" + addr_district + "':.*?break;"
            result = re.findall(district_regex,sub_district_data)
            result = '"' + str(result) + "'"

            sub_district_regex = "new Option\('" + postdata["addr_sub_district"] + "[\s]*','[0-9]+'\);"
            r2 = re.findall(sub_district_regex,result)
            regex = "[0-9]+"

            if str(r2)!= "":
                if not re.findall(regex,str(r2)):
                    addr_sub_district = ""
                else:
                    addr_sub_district = re.findall(regex,str(r2))[0]

            # print(addr_province)
            # print(addr_district)
            # print(addr_sub_district)
            if addr_province == "" or addr_province == postdata["addr_province"]:
                addr_province = "0"
            if addr_district == "" or addr_district == postdata["addr_district"]:
                addr_district = "0"
            if addr_sub_district == "" or addr_sub_district == postdata["addr_sub_district"]:
                addr_sub_district = "0"
            

            for key,value in postdata.items():
                # print(value)
                if value is None:
                    postdata[key] = " "
                # print(value)

            if area is None:
                area = ""



            datapost = {
            "tpCode" : tpCode,
            "tproperty_type" : listing_type,
            "tproperty_formart" : property_type,
            "ttitle" : postdata["post_title_th"],
            "tproject_asset" : postdata["web_project_name"],
            "taddress" : taddress,
            "tstreet_name" : postdata["addr_road"],
            "tprovince" : addr_province,
            "tamphur" : addr_district,
            "tdistrict" : addr_sub_district,
            "tdetail" : postdata["post_description_th"].replace('\u2013','-').replace('\u00a0'," ").replace('\/','/'),
            "tfloor" : postdata["floor_total"],
            "tbedroom" : postdata["bed_room"],
            "tbathroom" : postdata["bath_room"],
            "tortherroom" : "0",
            "tspace" : postdata["floor_area"],
            "tarea" : area,
            "tprice" : postdata["price_baht"],
            "towner" : postdata["name"],
            "tphone" : postdata["mobile"],
            "lat_value" : postdata["geo_latitude"],
            "lon_value" : postdata["geo_longitude"],
        }


        # print(datapost["area"])

            files = {}
            allimages = postdata["post_images"][:10]
            # print(allimages)
            for i in range(len(allimages)):
                r = open(os.getcwd()+"/"+allimages[i], 'rb')
                files["testimage"+str(i+1)] = r



            if str(datapost["tproperty_type"]).strip() == "":
                detail = "Enter the Announcement Type"
                success = False
            elif str(datapost["tproperty_formart"]).strip() == "":
                detail = "Enter the Property Type"
                success = False
            elif datapost["ttitle"] == "":
                detail = "Enter the Topic"
                success = False
            # elif datapost["tprovince"] == "":
            #     detail = "Enter the Province name"
            #     success = False
            # elif datapost["tamphur"] == "":
            #     detail = "Enter the District name"
            #     success = False
            # elif not addr_sub_district or datapost["tdistrict"] == "":
            #     detail = "Enter the Sub-District name"
                success = False
            elif datapost["tprice"] == "":
                detail = "Enter the Price"
                success = False
            elif datapost["towner"] == "":
                detail = "Enter the Seller's name"
                success = False
            elif datapost["tphone"] == "":
                detail = "Enter the Seller's Phone Number"
                success = False
            
            if success == True:
                newurl = "http://homedd.co.th/member_property_aed.php?typ=edit&id=" + postdata["post_id"]

                request = self.httprequestObj.http_post(newurl, data=datapost,headers=headers,files=files)

                # f = open(filename,"w+")
                # f.write(str(request.text))
                # print(request.text)
                # f.close()
                # with open(filename,'r') as file:
                if '??????????????????????????????????????????????????????????????????????????????' in str(request.text):
                    post = self.create_post(postdata)
                    if post['success']:
                        post_id = post['post_id']
                        post_url = post['post_url']
                        success = True
                        detail = 'Successfully Modified the Post !'
                    else:
                        success = False
                        post_id = postdata['post_id']
                        post_url = ''
                        detail = post['detail']
                    """detail = "Cannot Edit due to wrong post id"
                    success = False"""
                else:
                    detail = "Successfully Modified the Post !"
                    success = True
                    post_id = postdata['post_id']
                    post_url = ''
                    # file.close()
                # os.remove(filename)

                """if success == True:
                    url = "http://homedd.co.th/member_property_list.php"
                    r = self.httprequestObj.http_get("http://homedd.co.th/member_property_list.php")  

                    post_url = "http://www.homedd.co.th/property_display.php?id="
                    soup = BeautifulSoup(r.text,'lxml')

                    data = ""
                    for a in soup.find_all('a'):
                        data += str(a['href'])
                    
                    
                    regex = "javascript:confirmdelete\('[0-9]+'\);"
                    r = re.findall(regex,data)[0]

                    regex = "[0-9]+"
                    post_id = re.findall(regex,r)[0]
                    post_url += post_id"""

        end_time = datetime.utcnow()
        return {
            "success": success,
            "usage_time": str(end_time - start_time),
            "start_time": str(start_time),
            "end_time": str(end_time),
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_url": post_url,
            "post_id": post_id,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "account_type": "null",
            "detail": detail,
            "websitename": "homedd",
        }




    def delete_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')

        test_login = self.test_login(postdata)
        success= test_login["success"]
        start_time = test_login["start_time"]
        end_time = test_login["end_time"]
        post_id = postdata["post_id"]
        detail = ""

        # filename = "response.txt"
        headers = {
                'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
                }

        if success == True:
            url = "http://homedd.co.th/member_property_aed.php?typ=delete&id=" + postdata["post_id"]
            end_time = datetime.utcnow()
            

            request = self.httprequestObj.http_get(url)
            # f = open(filename,"w+")
            # f.write(str(request.text))
            # f.close()

            # print(request.text)

            # with open(filename,'r') as file:
            if '????????????????????????????????????????????????????????????????????????' in str(request.text):
                detail = "Successfully deleted"
                success = True
            else:
                detail = "Cannot Delete the Post due to wrong id!"
                success = False
                # file.close()

            # os.remove(filename)


        return {
            "success": success,
            "usage_time": str(end_time - start_time),
            "start_time": str(start_time),
            "end_time": str(end_time),
            "post_id": postdata['post_id'],
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "detail": detail,
            "websitename": "homedd",
        }



    def boost_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')

        test_login = self.test_login(postdata)
        success= test_login["success"]
        detail = test_login["detail"]
        start_time = test_login["start_time"]
        end_time = test_login["end_time"]

        headers = {
                    'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
                  }

        # filename = "response.txt"

        if success == True:

            datapost = {
            "tpCode" : "",
            "tproperty_type" : "",
            "tproperty_formart" : "",
            "ttitle" : "",
            "tproject_asset" : "",
            "taddress" : "",
            "tstreet_name" : "",
            "tprovince" : "",
            "tamphur" : "",
            "tdistrict" : "",
            "tdetail" : "",
            "tfloor" : "",
            "tbedroom" : "",
            "tbathroom" : "",
            "tortherroom" : "",
            "tspace" : "",
            "tarea" : "",
            "tprice" : "",
            "towner" : "",
            "tphone" : "",
            "lat_value" : "",
            "lon_value" : "",
        }

            files = {}
            newurl = "http://homedd.co.th/member_property_aed.php?typ=edit&id=" + postdata["post_id"]

            request = self.httprequestObj.http_post(newurl, data=datapost,headers=headers,files=files)
            end_time = datetime.utcnow()
            detail = "Post edited and saved"
            success = True

        return {
            "success": success,
            "usage_time": str(end_time - start_time),
            "log_id": postdata['log_id'],
            "start_time": str(start_time),
            "end_time": str(end_time),
            "post_id": postdata['post_id'],
            "ds_id": postdata['ds_id'],
            "account_type": "null",
            "detail": detail,
            "websitename": "homedd",
            "post_view": ""
        }

    def search_post(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_url = ""
        post_id = ""
        post_modified = ""
        post_view = ""
        post_found = False

        if success:
            r = self.httprequestObj.http_get('http://www.homedd.co.th/member_property_list.php')
            # print(r.url)
            # print(r.status_code)
            soup = BeautifulSoup(r.content, 'html.parser')
            pages = soup.find('ul',attrs={'class':'pagination'})
            last = pages.find_all('li')[-1]
            max_p=int(str(last.find('a')['href']).split('=')[-1])
            page = 1
            while page <= max_p:

                if post_found:
                    break
                r = self.httprequestObj.http_get('http://www.homedd.co.th/member_property_list.php?&nowpage=%d' % page)
                soup = BeautifulSoup(r.content, 'html.parser')

                all_posts = soup.find_all('tr')[2:]
                # print(all_posts[0])
                for post in all_posts:
                    info = post.find_all('td')
                    title = info[1].string
                    if title == None:
                        continue
                    if title == postdata['post_title_th']:
                        # print('Post Found')
                        post_found = True
                        post_id = info[3].find('a').get('href').split('=')[-1]
                        # print(post_id)
                        post_url = 'http://www.homedd.co.th/property_display.php?id='+post_id
                        r = self.httprequestObj.http_get(post_url)
                        # print(r.url)
                        # print(r.status_code)
                        soup = BeautifulSoup(r.content, 'html.parser')
                        post_modified = soup.find('font', {'style': 'color:#888; font-size:14px;'}).string.split(' ')[2:]
                        post_modified = post_modified[0] + ' ' + post_modified[1]
                        post_view = soup.find('h2', {'style': 'margin:0px; font-size:20px;'}).string.split(' ')[-14]
                        break
                page += 1

            if post_found:
                detail = "Post Found"
            else:
                detail = "No post with given title"
        else:
            success = False
            detail = "Couldnot login"

        time_end = datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_found": post_found,
            "detail": detail,
            "websitename": "homedd",
            "account_type": None,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "post_create_time": "",
            "post_modify_time": post_modified,
            "post_view": post_view,
            "post_url": post_url,
        }