
# -*- coding: utf-8 -*-

import os
from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
# from urlparse import urlparse
import re
import json
import datetime
import time
import sys
from urllib.parse import unquote
from urllib.request import urlopen

httprequestObj = lib_httprequest()


with open("./static/teesuay.json",encoding='utf-8') as f:
    provincedata = json.load(f)


class teesuay():

    name = 'teesuay'
    httprequestObj = lib_httprequest()
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
        httprequestObj.http_get("http://www.teesuay.com/member/logout.php")

        province_id=0
        amphur_id=0
        success = "true"
        detail = ""
        passwd = postdata['pass']
        add = "กรุงเทพ"
        tel = postdata["tel"]
        email = postdata["user"]
        website = ""
        for (key, value) in provincedata.items():
            if type(value) is str and "กรุงเทพ" in value.strip():
                province_id = key
                break
        for (key, value) in provincedata[str(province_id)+"_province"].items():
            if "พญาไท" in value.strip():
                amphur_id = key
                break
        datapost = dict(
            email=email,
            repass=passwd,
            name=postdata['name_th']+" "+postdata['surname_th'],
            action='p-member-register.php',
            province=province_id,
            amphur=amphur_id,
            website=website,
            tel=tel
        )
        datapost['pass']=passwd
        datapost['Submit.x']='43'
        datapost['Submit.y']='11'
        datapost['capcha']=datapost['rands']="ABCD"
        url_n="http://www.teesuay.com/p-member-register.php"
        with requests.Session() as s:
            r=s.post(url_n,data=datapost)
        # print(r.content)
        # print(r.text)
        data = r.text
        if data == '':
            success = "false"
        else:
            detail = "registered"  

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "teesuay",
            "success": success,
            'ds_id': postdata['ds_id'],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
        }


    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        httprequestObj.http_get("http://www.teesuay.com/member/logout.php")
        email = postdata['user']
        passwd = postdata['pass']
        btloginx=22
        btloginy=21
        success = "true"
        detail = ""

        datapost = {
            'action': 'login.php',
            'email': email,
            'pass': passwd,
            'btlogin.x':btloginx,
            'btlogin.y':btloginy
        }

        r = httprequestObj.http_post('http://www.teesuay.com/login.php', data=datapost)
        data = r.text
        print(data)
        if data.find("ขออภัยครับ") != -1 or email == "" or passwd == "":
            success = "false"
        else:
            detail = "logged in"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "teesuay",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "ds_id": postdata['ds_id'],
        }


    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()


        theurl = ""
        post_id = ""

        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        ashopname = test_login["detail"]
        



        # getProdId = {'1':24,'2':25,'3':26,'4':27,'5':29,'6':34,'7':28,'8':14,'9':31,'10':33}
        # theprodid = getProdId[postdata['property_id']]
        province_id=""
        amphur_id=""
        postdata['addr_province']=postdata['addr_province'].replace(" ","")
        postdata['addr_district']=postdata['addr_district'].replace(" ","")
        for (key, value) in provincedata.items():
            if type(value) is str and (postdata['addr_province'].strip() in value.strip() or value.strip() in postdata['addr_province'].strip()):
                province_id = key
                break
        if province_id=="":
            return{
                'websitename':'teesuay',
                'success': 'False',
                'ret': "wrong province id",
                'post_url': "",
                'post_id': "",
                "ds_id": postdata['ds_id']

            }
        for (key, value) in provincedata[province_id+"_province"].items():
            if postdata['addr_district'].strip() in value.strip() or value.strip() in postdata['addr_district'].strip():
                amphur_id = key
                break

        if amphur_id=="":
            return{
                'websitename':'teesuay',
                'success': 'false',
                'ret': "wrong amphur id",
                'post_url': "",
                'post_id': "",
                "ds_id": postdata['ds_id']

            }
        if 'addr_soi' in postdata and postdata['addr_soi']!=None:
                pass
        else:
            postdata['addr_soi']=''
        if 'addr_road' in postdata and postdata['addr_soi']!=None:
                pass
        else:
            postdata['addr_road']=''
        prod_address = ""
        for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
            if add is not None and add!="" and add!=" ":
                prod_address += add + ","
        prod_address = prod_address[:-1]

        propertytype={
            '6':1,
            '2':2,
            '4':3,
            '1':4,
            '7':5,
            '5':6,
            # 'Resort hotel':7,
            '9':8,
            '10':9,
            '25':9,
            '8':7,
            '3':2
            }
        #property type is being expected to be a number in the code
        try:
            postdata['cate_id']=propertytype[str(postdata['property_type'])]
        except:
            return{
                'websitename':'teesuay',
                'success': 'false',
                'ret': "Wrong Property type",
                'post_url': "",
                'post_id': "",
                "ds_id": postdata['ds_id']

            }
        post_url = ""
        if success == "true":
            postdata['post_title_th']=postdata['post_title_th'].replace('%','')
            floor_total, bedroom, bathroom = [''] * 3
            if 'floor_total' in postdata and postdata['floor_total']!=None: 
                floor_total = str(postdata['floor_total'])
            else:
                if postdata['property_type']=='6' or postdata['property_type']=='10'or postdata['property_type']=='25':
                    pass
                else:
                    floor_total = '0'
            if 'bed_room' in postdata and postdata['bed_room']!=None: 
                bedroom = str(postdata['bed_room'])
            else:
                if postdata['property_type']=='6' or postdata['property_type']=='9' or postdata['property_type']=='10'or postdata['property_type']=='25':
                    pass
                else:
                    bedroom='0'
            if 'bath_room' in postdata and postdata['bath_room']!=None: 
                bathroom = str(postdata['bath_room'])
            else:
                if postdata['property_type']=='6' or postdata['property_type']=='9'or postdata['property_type']=='10'or postdata['property_type']=='25':
                    pass
                else:
                    bathroom='0'
            if 'land_size_ngan' not in postdata or postdata['land_size_ngan']==None or postdata['land_size_ngan'] == "": 
                postdata['land_size_ngan']=0
            if 'land_size_rai' not in postdata or postdata['land_size_rai']==None or postdata['land_size_rai'] == "":
                postdata['land_size_rai']=0
            if 'land_size_wa' not in postdata or postdata['land_size_wa']==None or postdata['land_size_wa'] == "":
                postdata['land_size_wa']=0

            if 'web_project_name' in postdata and postdata['web_project_name'] != '' and postdata['web_project_name'] is not None:
                postdata['project_name']=postdata['web_project_name']
            elif 'project_name' not in postdata or postdata['project_name'] == '' and postdata['project_name'] is None:
                postdata['project_name']=postdata['post_title_th']



            if len(postdata['post_images'])==0:
                postdata['post_images']=['imgtmp/default/white.jpg']
            # if 'floor_area' in postdata: floor_area = postdata['floor_area']
            floorarea='0'
            print(postdata['property_type'])
            if postdata['property_type']=='1' or postdata['property_type']=='9' or postdata['property_type']=='10' or postdata['property_type']=='25':
                if 'floor_area' not in postdata:
                    postdata['floor_area']=0
                floorarea=str(postdata['floor_area'])+" ตรม"
            else:
                floorarea=str(400*int(postdata['land_size_rai']) + 100 * int(postdata['land_size_ngan']) + int(postdata['land_size_wa'])) +" ตรว"
            postdata['post_project_name'] = postdata['project_name']
            postdata['post_description_th']=postdata['post_description_th'].replace('\r\n','<br>')
            postdata['post_description_th']=postdata['post_description_th'].replace('\n','<br>')
            datapost = {
                'class_type_id':'1', # 1 for sell 2 for rent
                'cate_id':postdata['cate_id'], #the property tye
                'action': 'p-edit-property.php',
                'status': '1',
                'title': postdata['post_title_th'],
                'project': postdata['post_project_name'],
                'price':postdata['price_baht'],
                'add':prod_address,
                'province':province_id,
                'amphur':amphur_id,
                'map_lat':postdata['geo_latitude'],
                'map_zoom':'',
                'map_lng':postdata['geo_longitude'],
                'bedroom':bedroom,
                'bathroom':bathroom,
                'floors':floor_total,
                'input':postdata['post_description_th'],
                'area':floorarea,
                'capcha':"ABCD",
                'rands':"ABCD",
                'fileshow': '(binary)',
                'opshow':'',
                'op_s_show':'',
                'file1': '(binary)',
                'op1': '',
                'file2':'(binary)',
                'op2': '',
                'file3': '(binary)',
                'op3': '',
                'file4': '(binary)',
                'op4':'',
                'name':postdata['name'],
                'email':postdata['email'],
                'website':'',
                'tel': postdata['mobile'],
                'Submit':'Continue >>'
            }
            if postdata['listing_type']!='ขาย':
                datapost['class_type_id']=2
            arr = ["fileshow", "file1", "file2", "file3", "file4"]
            files={}
            for i in range(len(postdata['post_images'][:5])):
                datapost[arr[i]] = postdata['post_images'][i]
                files[arr[i]] = (postdata['post_images'][i], open(postdata['post_images'][i], "rb"), "image/jpg")

            r = httprequestObj.http_post(
                'http://www.teesuay.com/member/p-post-property.php', data=datapost,files=files)

            data = r.text
            if 'รูปภาพโชว์ เฉพาะไฟล์ภาพ .jpg หรือ .jpeg เท่านั้น' in r.text:
                success='false'
            if data == '1':
                success = "false"
            else:
                list_url = 'http://www.teesuay.com/member/list-property.php'
                r = httprequestObj.http_get(list_url)
                soup = BeautifulSoup(r.content, features = self.parser)
                var = soup.find('a', attrs={'title': postdata['post_title_th']})['href']
                # for i in '../property/':
                i = len('../property/')
                # post_id=''
                post_id = ''

                while var[i] != '/':
                    post_id += var[i]
                    i += 1
                post_url = 'http://www.teesuay.com/property-' + \
                    post_id+"/"+postdata['post_title_th'].replace(' ','-')+'.html'
            detail = 'created post'
        else:
            success = "False"
            detail = "cannot login"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "websitename": "teesuay",
            "success": success,
            "ret":success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": post_url,
            "post_id": post_id,
            'detail': detail,
            "ds_id": postdata['ds_id']
        }


    def edit_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        # print(test_login)
        success = test_login["success"]
        ashopname = test_login["detail"]
        post_url = ""
        detail = ""
        post_id = ""
        detail = ""
        province_id=-1
        amphur_id=-1

        page = 1
        found = False
        temp = len('property-')
        while True:
            r = httprequestObj.http_get('http://www.teesuay.com/member/list-property.php?QueryString=value&Page='+str(page))
            soup = BeautifulSoup(r.content, features = self.parser)
            count = 0
            for i in soup.findAll('a'):
                var = i['href']
                if 'property-' in var:
                    count += 1
                var = var.split('/')
                if len(var)>1:
                    if var[1][temp:].strip()==str(postdata['post_id']):
                        found = True
                        break
            page += 1
            if found or count==0:
                break
        if not found:
            return {
                'websitename':'teesuay',
                'success':'false',
                "detail": "no post found with given id",
                "log_id": postdata['log_id']
            }

        for (key, value) in provincedata.items():
            if type(value) is str and postdata['addr_province'].strip() in value.strip():
                province_id = key
                break

        if province_id=="":
            return{
                'websitename':'teesuay',
                'success': 'false',
                'ret': "",
                'ds_id': postdata['ds_id'],
                'post_url': "",
                'post_id': "",
                "log_id": postdata['log_id']
            }

        for (key, value) in provincedata[province_id+"_province"].items():
            if postdata['addr_district'].strip() in value.strip():
                amphur_id = key
                break

        if amphur_id==-1:
            return{
                'websitename':'teesuay',
                'success': 'false',
                'ret': "",
                'post_url': "",
                'ds_id': postdata['ds_id'],
                'post_id': "",
                "log_id": postdata['log_id']

            }
        no = 0
        # img_arr = {}
        # for i in range(len(postdata['post_img_url_lists'])):
        #     img_arr[i] = str(no)+".jpg"
        #     print("imagefs ", postdata['post_img_url_lists'][i])
        #     urllib.request.urlretrieve(
        #         postdata['post_img_url_lists'][i], str(no)+".jpg")
        #     no += 1

        prod_address = ""
        for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
            if add is not None and add=="" and add==" ":
                prod_address += add + ","
        prod_address = prod_address[:-1]

        propertytype={
            '6':1,
            '2':2,
            '4':3,
            '1':4,
            '7':5,
            '5':6,
            # 'Resort hotel':7,
            '9':8,
            '10':9,
            '25':9,
            '8':7,
            '3':2
        }
        try:
            postdata['cate_id']=propertytype[str(postdata['property_type'])]
        except:
            return{
                'websitename':'teesuay',
                'success': 'false',
                'detail':'wrong propertytype',
                'ret': '',
                'post_url': '',
                'post_id': '',
                "log_id": postdata['log_id'],
                "ds_id": postdata['ds_id']

            }
        if success == "true":
            postdata['post_title_th']=postdata['post_title_th'].replace('%','')
            postdata['post_description_th']=postdata['post_description_th'].replace('\r\n','<br>')
            postdata['post_description_th']=postdata['post_description_th'].replace('\n','<br>')
            floor_total, bedroom, bathroom = [''] * 3
            if 'floor_total' in postdata and postdata['floor_total']!=None: 
                floor_total = str(postdata['floor_total'])
            else:
                if postdata['property_type']=='6' or postdata['property_type']=='10'or postdata['property_type']=='25':
                    pass
                else:
                    floor_total = '2'
            if 'bed_room' in postdata and postdata['bed_room']!=None: 
                bedroom = str(postdata['bed_room'])
            else:
                if postdata['property_type']=='6' or postdata['property_type']=='9' or postdata['property_type']=='10'or postdata['property_type']=='25':
                    pass
                else:
                    bedroom='2'
            if 'bath_room' in postdata and postdata['bath_room']!=None: 
                bathroom = str(postdata['bath_room'])
            else:
                if postdata['property_type']=='6' or postdata['property_type']=='9' or postdata['property_type']=='10'or postdata['property_type']=='25':
                    pass
                else:
                    bathroom='2'
            if 'land_size_ngan' not in postdata or postdata['land_size_ngan']==None or postdata['land_size_ngan'] == "": 
                postdata['land_size_ngan']=0
            if 'land_size_rai' not in postdata or postdata['land_size_rai']==None or postdata['land_size_rai'] == "":
                postdata['land_size_rai']=0
            if 'land_size_wa' not in postdata or postdata['land_size_wa']==None or postdata['land_size_wa'] == "":
                postdata['land_size_wa']=0

            if 'web_project_name' in postdata and postdata['web_project_name'] != '' and postdata['web_project_name'] is not None:
                postdata['project_name']=postdata['web_project_name']
            elif 'project_name' not in postdata or postdata['project_name'] == '' and postdata['project_name'] is None:
                postdata['project_name']=postdata['post_title_th']
            postdata['post_project_name'] = postdata['project_name']
            

            if len(postdata['post_images'])==0:
                postdata['post_images']=['imgtmp/default/white.jpg']
            # if 'floor_area' in postdata: floor_area = postdata['floor_area']
            floorarea='0'
            #print(postdata['property_type'])
            if postdata['property_type']=='1' or postdata['property_type']=='9' or postdata['property_type']=='10' or postdata['property_type']=='25':
                if 'floor_area' not in postdata:
                    postdata['floor_area']=0
                floorarea=str(postdata['floor_area'])+ " ตรม"
            else:
                floorarea=str(400*int(postdata['land_size_rai']) + 100 * int(postdata['land_size_ngan']) + int(postdata['land_size_wa'])) +" ตรว"
            
            datapost = {
                'post_id':postdata['post_id'],
                # 'class_type_id':postdata['class_type_id'], # 1 for sell 2 for rent
                'cate_id':postdata['cate_id'], #the property tye
                'action': 'p-edit-property.php',
                'status': '1',
                'title': postdata['post_title_th'],
                'project': postdata['post_project_name'],
                'price':postdata['price_baht'],
                'add':prod_address,
                'province':province_id,
                'amphur':amphur_id,
                'map_lat':postdata['geo_latitude'],
                'map_zoom':'',
                'map_lng':postdata['geo_longitude'],
                'input':'',
                'bedroom':'',
                'bathroom':'',
                'floors':'',
                'area':floorarea,
                'capcha':"ABCD",
                'rands':"ABCD",
                'fileshow': '(binary)',
                'opshow':'',
                'op_s_show':'',
                'file1': '(binary)',
                'op1': '',
                'file2':'(binary)',
                'op2': '',
                'file3': '(binary)',
                'op3': '',
                'file4': '(binary)',
                'op4':'',
                'name':postdata['name'],
                'email':postdata['email'],
                'website':'',
                'Submit':'Continue >>',
                'tel': postdata['mobile']
            }
            if postdata['listing_type']!='ขาย':
                datapost['class_type_id']=2
            else:    
                datapost['class_type_id']=1    
            arr = ["fileshow", "file1", "file2", "file3", "file4"]
            files={}
            for i in range(min(len(arr), len(postdata['post_images']))):
                datapost[arr[i]] = postdata['post_images'][i]
                files[arr[i]] = (postdata['post_images'][i], open(postdata['post_images'][i], "rb"), "image/jpg")

            url_n='http://www.teesuay.com/member/p-edit-property.php'
            
            r=httprequestObj.http_post(url_n,datapost)
            if r.status_code==200:
                detail = "Post edited successfully"
                success="true"
            else:
                success = "false"
                detail = "cannot edit post. "+r.text
        else:
            success = "false"
       
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "teesuay",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id":postdata["post_id"]

        }



    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        # login
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        page = 1
        found = False
        temp = len('property-')
        while True:
            r = httprequestObj.http_get('http://www.teesuay.com/member/list-property.php?QueryString=value&Page='+str(page))
            soup = BeautifulSoup(r.content, features = self.parser)
            count = 0
            for i in soup.findAll('a'):
                var = i['href']
                if 'property-' in var:
                    count += 1
                var = var.split('/')
                if len(var)>1:
                    if var[1][temp:].strip()==str(postdata['post_id']):
                        found = True
                        break
            page += 1
            if found or count==0:
                break

        if not found:
            return {
                "websitename":'teesuay',
                "success":'false',
                "detail": "post not found",
                "log_id": postdata['log_id'],
                "ds_id": postdata['ds_id']
            }

        r = httprequestObj.http_get('http://www.teesuay.com/member/list-property.php')
        soup = BeautifulSoup(r.content, features = self.parser)
        var = soup.find('input', attrs={'name': 'hdnCount'})['value']
        if len(var) == 0:
            return{
                'websitename':'teesuay',
                'success': 'false',
                'detail': "",
                'post_url': "",
                'post_id': "",
                'ds_id': postdata['ds_id']
            }
        if success == "true":
            datapost = {
                'action':'manage-property-not-sale.php',
                'chkDel[]': str(postdata['post_id']),
                'type':'2',
                'Submit':'Proceed',
                'hdncount':var,
                'ds_id': postdata['ds_id'],
                "log_id": postdata['log_id']
            }
            r = httprequestObj.http_post('http://www.teesuay.com/member/manage-property-not-sale.php', data=datapost)
            data = r.text
            if data == '':
                success = "false"
            else:
                detail = "Post deleted successfully"
        else:
            success = "false"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "teesuay",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            'ds_id': postdata['ds_id'],
            "detail": detail,
            "log_id":postdata['log_id'],
        }

    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        post_id = postdata['post_id']
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]

        if success=='true':
            page = 1
            found = False
            temp = len('property-')
            while True:
                r = httprequestObj.http_get('http://www.teesuay.com/member/list-property.php?QueryString=value&Page='+str(page))
                soup = BeautifulSoup(r.content, features = self.parser)
                count = 0
                for i in soup.findAll('a'):
                    var = i['href']
                    if 'property-' in var:
                        count += 1
                    var = var.split('/')
                    if len(var)>1:
                        if var[1][temp:].strip()==str(postdata['post_id']):
                            found = True
                            break
                page += 1
                if found or count==0:
                    break

            if not found:
                time_end = datetime.datetime.utcnow()
                return {
                    'websitename':'teesuay',
                    'success':'false',
                    "start_time": str(time_start),
                    'ds_id': postdata['ds_id'],
                    "end_time": str(time_end),
                    "detail": "wrong post id",
                    "log_id": postdata['log_id']

                }
            posturl="http://www.teesuay.com/member/slide-property.php?post_id="+postdata['post_id']
            r=httprequestObj.http_get(posturl)
            time_end = datetime.datetime.utcnow()
            return {
                "websitename": "teesuay",
                "success": "true",
                "time_usage": time_end - time_start,
                "start_time": time_start,
                "end_time": time_end,
                'ds_id': postdata['ds_id'],
                "detail": "Boosted Successfully",
                "post_id": post_id,
                "log_id": postdata['log_id']
                
            }
        else:
            success = "false"
            time_end = datetime.datetime.utcnow()
            time_usage = time_end - time_start
            return {
                'ds_id': postdata['ds_id'],
                "websitename": "teesuay",
                "success": success,
                "start_time": str(time_start),
                "end_time": str(time_end),
                "detail": detail,
                "log_id":postdata['log_id'],
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

        return {
            "websitename": "teesuay",
            "success": "true",
            "time_usage": time_end - time_start,
            "start_time": time_start,
            "end_time": time_end,
            "detail": ""
        }

    #search post
    def search_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        ds_name=postdata['ds_name']
        Title = postdata['post_title_th']
        ds_id = postdata['ds_id']
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        if(not success):
            time_end = datetime.datetime.utcnow()
            return {
                'websitename' : 'teesuay',
                "ds_name":ds_name,
                "success":"true",
                "start_time":str(time_start),
                "end_time":str(time_end),
                "log_id": postdata['log_id'],
                "ds_id":ds_id,
                "post_found" : "false",
                "post_url":"",
                "post_id":"",
                "account_type": None,
                "detail":"cannot login",
                "post_create_time":"",
                "post_modify_time":"",
                "post_view":""
            }
        url_list='http://www.teesuay.com/member/list-property.php'
        r=httprequestObj.http_get(url_list)
        soup = BeautifulSoup(r.content, features = self.parser)
        post_id = ''
        detail = ''
        post_url = ''
        post_found = 'false'
        account_type = ''
        detail = ''
        post_create_time = ''
        post_modify_time = ''
        post_view = ''
        target = soup.find('a', attrs={'title': Title})
        if(target):
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            post_id=''
            post_url=target['href']
            temp = ''
            temp += 'http://www.teesuay.com'
            temp += post_url[2:]
            post_url = temp
            post_found = 'true'
            var=target['href']
            j = len('../property/')
            while j<len(var) and var[j] != '/':
                post_id += var[j]
                j += 1
            html = requests.get(post_url, verify=False).content
            soup = BeautifulSoup(html, "html.parser")
            table = soup.findAll('table')
            data = table[9].findAll('tr')[2].text
            data = data.strip()
            post_create_time = data[14:30]
            post_modify_time = data[45:73]
            post_view = data[81:83]
            detail = table[37].findAll('td')[0].get_text().strip()
            time_end = datetime.datetime.utcnow()
        
        time_end = datetime.datetime.utcnow()
        return {
            'websitename' : 'teesuay',
            "ds_name" : ds_name,
            "success": "true",
            "start_time":str(time_start),
            "end_time":str(time_end),
            "ds_id": ds_id,
            "log_id": postdata['log_id'],
            "post_found" : post_found,
            "post_url":post_url,
            "post_id":post_id,
            "account_type": None,
            "detail": detail,
            "post_create_time": post_create_time ,
            "post_modify_time": post_modify_time ,
            "post_view": post_view        
        }
