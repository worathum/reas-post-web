from .lib_httprequest import *
from bs4 import BeautifulSoup as soup
import os.path
# from urlparse import urlparse
import re
import json
import sys
from urllib.parse import unquote
from datetime import datetime
import random



def set_end_time(start_time):
    time_end = datetime.utcnow()
    time_usage = time_end - start_time
    return time_end, time_usage

class adscondo():

    name = 'adscondo'
    property_dict={
    '1': '71', 
    '2': '233',
    '3': '234', 
    '4': '234', 
    '5': '235', 
    '6': '237', 
    '7': '238', 
    '8':'238', 
    '9': '236', 
    '10': '235',
    '25': '235'
    }

    def __init__(self):

        try:
            import configs
        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.primarydomain = 'https://www.adscondo.com/'
        self.debug = 0
        self.debugresdata = 0
        self.httprequestObj = lib_httprequest()
        self.httprequestObj.timeout = 150
        self.parser = 'html.parser'

    def register_user(self, userdata):
        #self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        
        reqst_url = "https://www.adscondo.com/wp-admin/admin-ajax.php"
        start_time = datetime.utcnow()
        res={'websitename':'adscondo', 'success':False, 'start_time': str(start_time), 'end_time': '0', 'usage_time': '0', 'detail': '','ds_id':userdata['ds_id']}
        username = str(userdata['name_th']+" "+userdata['surname_th'])
        payload = {
            'username': userdata["user"].split('@')[0] ,
            'useremail': userdata['user'],
            'register_pass': userdata['pass'],
            'register_pass_retype': userdata['pass'],
            'term_condition': 'on',
            'privacy_policy': 'on',
            'houzez_register_security': '',
            '_wp_http_referer': '',
            'action': 'houzez_register'
        }

        userpass_regex=re.compile(r'^([a-zA-Z0-9_]{4,15})$')
        email_regex=re.compile(r'^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$')
        if(userpass_regex.search(payload['username'])==None):
            res['detail']+='User Name must be in az, AZ, 0-9 or _ only and should be 4-15 characters only. '
        if(userpass_regex.search(payload['register_pass'])==None):
            res['detail']+='Password must be in az, AZ, 0-9 or _ only and should be 4-15 characters only. '
        if(email_regex.search(payload['useremail'])==None):
            res['detail']+='Invalid email. '
    
        r = self.httprequestObj.http_get('https://www.adscondo.com/')
        sou = BeautifulSoup(r.text,'html5lib')
        payload['houzez_register_security'] = sou.find('input',attrs = {'name':'houzez_register_security'})['value']
        payload['_wp_http_referer'] = (sou.findAll('form')[1]).find('input',attrs = {'name':'_wp_http_referer'})['value']
        print(payload)
        r = self.httprequestObj.http_post(reqst_url, data=payload)
        jr = json.loads(r.text)
        
        if jr['success'] == False:
            res['success']=False
            res['detail'] = jr['msg']+' !Not Registered'
        else :
            res['success']=True
            res['detail'] = 'User Registered Successfully\n'
        endT,usage_time=set_end_time(start_time)
        res['end_time'] = str(endT)
        res['usage_time'] = str(usage_time)
        return res


    def test_login(self,userdata):
        
        #login_url = "https://www.adscondo.com/wp-admin/admin-ajax.php"
        login_url="https://api.adscondo.com/api/login"
        start_time = datetime.utcnow()
        res={'websitename':'adscondo', 'success':False, 'start_time': str(start_time), 'end_time': '0', 'usage_time': '0', 'detail': '','ds_id':userdata['ds_id']}
        """
        login_pload = {
            'username': userdata['user'],
            'password': userdata['pass'],
            'houzez_login_security': '',
            '_wp_http_referer': '',
            'action': 'houzez_login'
        }
        
        r = self.httprequestObj.http_get('https://www.adscondo.com/')
        sou = BeautifulSoup(r.text,'html5lib')
        login_pload['houzez_login_security'] = sou.find('input',attrs = {'name':'houzez_login_security'})['value']
        login_pload['_wp_http_referer'] = sou.findAll('form')[0].find('input',attrs = {'name':'_wp_http_referer'})['value']

        r= self.httprequestObj.http_post(login_url, data=login_pload)

        jr = json.loads(r.text)
        
        if jr['success'] == False:
            res['success']= False
            res['detail'] = 'Login Failed'
        else :
            res['success']= True
            res['detail'] = 'User Logged In Successfully\n'
        endT,usage_time=set_end_time(start_time)
        res['end_time'] = str(endT)
        res['usage_time'] = str(usage_time)
        """

        login_pload = {
            'email': userdata['user'],
            'password': userdata['pass'],
        }

        r = self.httprequestObj.http_post(login_url, data=login_pload)
        jr = json.loads(r.text)
        r = self.httprequestObj.http_get("https://www.adscondo.com/user/"+jr["auth"]["id"])
        print(r.text)
        if "ออกจากระบบ" in r.text:
            res['success'] = True
            res['detail'] = 'User Logged In Successfully\n'
        else:
            res['success'] = False
            res['detail'] = 'Login Failed'
        return res


    def create_post(self,postdata):

        #self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.utcnow()

        login = self.test_login(postdata)

        post_id = ''
        post_url = ''
        

        if (login["success"] == True):
            reqst_url = 'https://www.adscondo.com/%e0%b8%a5%e0%b8%87%e0%b8%9b%e0%b8%a3%e0%b8%b0%e0%b8%81%e0%b8%b2%e0%b8%a8%e0%b8%82%e0%b8%b2%e0%b8%a2%e0%b8%84%e0%b8%ad%e0%b8%99%e0%b9%82%e0%b8%94%e0%b8%9f%e0%b8%a3%e0%b8%b5/'
            pt = str(postdata['property_type'])
            try:
                subdist = postdata['addr_sub_district']
                if subdist == None:
                    subdist = ""
            except:
                subdist = ""

            try:
                bathroom = str(postdata['bath_room'])
                if bathroom == None:
                    bathroom = ''
            except:
                bathroom = ''
            try:
                bedroom = str(postdata['bed_room'])
                if bedroom == None:
                    bedroom = ''
            except:
                bedroom = ''

            try:
                land_size_rai = postdata['land_size_rai']
                if land_size_rai==None:
                    land_size_rai=0
            except:
                land_size_rai = 0
        
            try:
                land_size_ngan = postdata['land_size_ngan']
                if land_size_ngan == None:
                    land_size_ngan=0
            except:
                land_size_ngan = 0
            try:
                land_size_wa = postdata['land_size_wa']
                if land_size_wa==None:
                    land_size_wa=0
            except:
                land_size_wa = 0
            
            try:
                zipc = postdata['addr_postcode']
                if zipc == None:
                    zipc = ''
            except:
                zipc = ''
            
            pref = 'ตารางวา'
            if str(postdata['property_type'])=='1':
                try:
                    area = postdata['floorarea_sqm']
                    
                except:
                    area = 0
                pref = 'm²'
            else :
                try:
                    area = (land_size_rai*400) + (land_size_ngan*100)+ land_size_wa
                except:
                    area = 0


            data = {
                'prop_title': postdata['post_title_th'],
                'prop_des': postdata['post_description_th'].replace('\r\n','<br>').replace('\n','<br>'),
                'prop_type': self.property_dict[str(postdata['property_type'])],
                'prop_status': '',
                'prop_labels': '227',
                'prop_price': postdata['price_baht'],
                'prop_size': area,
                'prop_size_prefix': pref,
                'prop_beds': bedroom,
                'prop_baths': bathroom,
                'prop_year_built':'', 
                'prop_video_url':'', 
                'propperty_image_ids[]':[],
                'property_map_address': subdist,
                'postal_code': zipc,
                'country_short': 'TH',
                'administrative_area_level_1': '',
                'locality': '',
                'neighborhood':'', 
                'lat': postdata['geo_latitude'],
                'lng': postdata['geo_longitude'],
                'prop_google_street_view': 'show',
                'virtual_tour':'', 
                'gdpr_agreement': 'on',
                'property_nonce':'',
                '_wp_http_referer': '/%e0%b8%a5%e0%b8%87%e0%b8%9b%e0%b8%a3%e0%b8%b0%e0%b8%81%e0%b8%b2%e0%b8%a8%e0%b8%82%e0%b8%b2%e0%b8%a2%e0%b8%84%e0%b8%ad%e0%b8%99%e0%b9%82%e0%b8%94%e0%b8%9f%e0%b8%a3%e0%b8%b5/',
                'action': 'add_property',
                'prop_featured': '0',
                'prop_payment': 'not_paid'      
            }     
            
            if postdata['listing_type'] == 'เช่า':
                data['prop_status'] = '86'
            else:
                data['prop_status'] = '85'

            r = self.httprequestObj.http_get(reqst_url)
            sou = BeautifulSoup(r.text,'html5lib')
            
            pattern = re.compile('var houzezProperty = {.*?};')
            
            scripts = sou.findAll('script')
            
            var = {}
            for script in scripts:
                if script.has_attr('src'):
                    continue
                
                if(pattern.search(str(script.text))):
                    
                    datat = script.text
                    st_ind = datat.find('{')
                    end_ind = datat.find('}')
                    #print(datat)
                    var = json.loads(datat[st_ind:end_ind+1])
                    #print(var)
                    break
            ver_nonce = var['verify_nonce']
            print(ver_nonce)
            prop_nonce = str(sou.find('input',attrs={'name':'property_nonce'})['value'])
            print(prop_nonce)
            data['property_nonce'] = prop_nonce

            
            province = ''.join(map(str,str(postdata['addr_province']).split(' ')))
            #print(province)
            abc = sou.find('select',attrs = {'name':'administrative_area_level_1'})
            #print(abc)
            for pq in abc.find_all('option'):
                if(str(pq.text) in str(province) or str(province) in str(pq.text)):
                    data['administrative_area_level_1'] = str(pq['value'])
                    break
                      
            if(data['administrative_area_level_1']=='' or data['administrative_area_level_1'] == 'กรุงเทพ' ):
                data['administrative_area_level_1'] = 'กรุงเทพ'
                dist = ''.join(map(str,str(postdata['addr_district']).split(' ')))
                #print(province)
                abc = sou.find('select',attrs = {'name':'locality'})
                #print(abc)
                for pq in abc.find_all('option'):
                    if(str(pq.text) in str(dist) or str(dist) in str(pq.text)):
                        data['locality'] = str(pq['value'])
                        break
            
            img_upload = 'https://www.adscondo.com/wp-admin/admin-ajax.php?action=houzez_property_img_upload&verify_nonce='+ver_nonce
            at_id = []
            
            for ind, i in enumerate(postdata['post_images']):
                # y=str(datetime.utcnow()).replace('-','').replace(":","").replace(".","").replace(" ","")+".jpg"
                #print(y)
                file = {'property_upload_file': (i, open(i, "rb"), "image/jpeg")}
                upload_file = self.httprequestObj.http_post(img_upload,data = {'name':i},files=file)
                print(upload_file.text)
                jr = json.loads(upload_file.text)
                at_id.append(jr['attachment_id'])
                
              
            for i in range(len(postdata['post_images'])):
                data['propperty_image_ids[]'].append(at_id[i])
            
            url = 'https://www.adscondo.com/%E0%B8%AD%E0%B8%AA%E0%B8%B1%E0%B8%87%E0%B8%AB%E0%B8%B2%E0%B8%AF%E0%B8%82%E0%B8%AD%E0%B8%87%E0%B8%89%E0%B8%B1%E0%B8%99%E0%B8%82%E0%B8%B2%E0%B8%A2%E0%B8%84%E0%B8%AD%E0%B8%99%E0%B9%82%E0%B8%94/'
            
            r = self.httprequestObj.http_post(reqst_url,data = data)
            
            page = self.httprequestObj.http_get(url)
            sou = soup(page.text,'html5lib')
            delt = sou.find('a',attrs= {'class':'delete-property'})
            divi = sou.find('div', attrs = {'class':'item-wrap'})
            
            
            if divi == None:
                success = False
                detail = "Post creation Failed 1"
            else:
                flag= 0
                print(postdata['post_title_th'])
                    
                title = divi.find('h4',attrs = {'class':'my-heading'})
                print(title.text)
                if postdata['post_title_th'].replace(' ','') == title.text.replace(' ','') :
                    
                    post_id = delt['data-id']
                    post_url = 'https://www.adscondo.com/คอนโด/'+postdata['post_title_th']
                    success = True
                    detail = "Post created successfully"
                    flag = 1
                else :
                    success = False
                    detail = "Post creation Failed 2"
    
        else:
            success = False
            detail = "Can not log in"
            
        end_time,usage_time=set_end_time(start_time)
        
        return {
            "websitename": "adscondo",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(usage_time),
            "post_url": post_url,
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
            "detail": detail,
            "account_type": "null"
        }


    def edit_post(self,postdata):

        #self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.utcnow()

        login = self.test_login(postdata)

        post_id = ''
        post_url = ''
        

        if (login["success"] == True):
            post_id = str(postdata['post_id'])
            p_title = ''
            get_url = 'https://www.adscondo.com/%E0%B8%AD%E0%B8%AA%E0%B8%B1%E0%B8%87%E0%B8%AB%E0%B8%B2%E0%B8%AF%E0%B8%82%E0%B8%AD%E0%B8%87%E0%B8%89%E0%B8%B1%E0%B8%99%E0%B8%82%E0%B8%B2%E0%B8%A2%E0%B8%84%E0%B8%AD%E0%B8%99%E0%B9%82%E0%B8%94/'
            r = self.httprequestObj.http_get(get_url)
            sou = BeautifulSoup(r.text,'html5lib')
            security = sou.findAll('a',attrs = {'class':'delete-property'})
            heading = sou.findAll('h4',attrs = {'class':'my-heading'})
            ind = 0
            for delt in security:
                print(delt['data-id'])
                if delt['data-id'] == post_id:
                    post_url = heading[ind].find('a')['href']
                    break
                ind+=1
            reqst_url = 'https://www.adscondo.com/%e0%b8%a5%e0%b8%87%e0%b8%9b%e0%b8%a3%e0%b8%b0%e0%b8%81%e0%b8%b2%e0%b8%a8%e0%b8%82%e0%b8%b2%e0%b8%a2%e0%b8%84%e0%b8%ad%e0%b8%99%e0%b9%82%e0%b8%94%e0%b8%9f%e0%b8%a3%e0%b8%b5/?edit_property='+post_id
            pt = str(postdata['property_type'])
            try:
                subdist = postdata['addr_sub_district']
            except:
                subdist = ""

            try:
                bathroom = str(postdata['bath_room'])
            except:
                bathroom = ''
            try:
                bedroom = str(postdata['bed_room'])
            except:
                bedroom = ''

            try:
                land_size_rai = postdata['land_size_rai']
                if land_size_rai==None:
                    land_size_rai=0
            except:
                land_size_rai = 0
         
            try:
                land_size_ngan = postdata['land_size_ngan']
                if land_size_ngan == None:
                    land_size_ngan=0
            except:
                land_size_ngan = 0
            try:
                land_size_wa = postdata['land_size_wa']
                if land_size_wa==None:
                    land_size_wa=0
            except:
                land_size_wa = 0
            
            try:
                zipc = postdata['addr_postcode']
            except:
                zipc = ''
            
            pref = 'ตารางวา'
            if str(postdata['property_type'])=='1':
                try:
                    area = postdata['floorarea_sqm']
                    
                except:
                    area = 0
                pref = 'm²'
            else :
                try:
                    area = (land_size_rai*400) + (land_size_ngan*100)+ land_size_wa
                except:
                    area = 0


            data = {
                'draft_prop_id': post_id,
                'prop_title': postdata['post_title_th'],
                'prop_des': postdata['post_description_th'].replace('\r\n','<br>').replace('\n','<br>'),
                'prop_type': self.property_dict[str(postdata['property_type'])],
                'prop_status': '',
                'prop_labels': '227',
                'prop_price': postdata['price_baht'],
                'prop_size': area,
                'prop_size_prefix': pref,
                'prop_beds': bedroom,
                'prop_baths': bathroom,
                'prop_year_built':'', 
                'prop_video_url':'', 
                'propperty_image_ids[]':[],
                'featured_image_id':'',
                'property_map_address': subdist,
                'postal_code': zipc,
                'country_short': 'TH',
                'administrative_area_level_1': '',
                'locality2': '',
                'neighborhood2':'', 
                'lat': postdata['geo_latitude'],
                'lng': postdata['geo_longitude'],
                'prop_google_street_view': 'show',
                'virtual_tour':'', 
                'property_nonce':'',
                '_wp_http_referer': '/%e0%b8%a5%e0%b8%87%e0%b8%9b%e0%b8%a3%e0%b8%b0%e0%b8%81%e0%b8%b2%e0%b8%a8%e0%b8%82%e0%b8%b2%e0%b8%a2%e0%b8%84%e0%b8%ad%e0%b8%99%e0%b9%82%e0%b8%94%e0%b8%9f%e0%b8%a3%e0%b8%b5/?edit_property='+post_id,
                'action': 'update_property',
                'prop_id': post_id,
                'prop_featured': '0',
                'prop_payment': 'not_paid'      
            }     

            if postdata['listing_type'] == 'เช่า':
                data['prop_status'] = '86'
            else:
                data['prop_status'] = '85'

            r = self.httprequestObj.http_get(reqst_url)
            sou = BeautifulSoup(r.text,'html5lib')
            
            pattern = re.compile('var houzezProperty = {.*?};')
            print("yha bhi nhi")
            scripts = sou.findAll('script')
            print(len(scripts))
            var = {}
            for script in scripts:
                if script.has_attr('src'):
                    continue
                #print(script.text)
                if(pattern.search(str(script.text))):
                    datat = script.text
                    st_ind = datat.find('{')
                    end_ind = datat.find('}')
                    print(datat)
                    var = json.loads(datat[st_ind:end_ind+1])
                    #print(var)
                    break
            removeNonce = var['verify_nonce']
            print(removeNonce)
            prop_nonce = str(sou.find('input',attrs={'name':'property_nonce'})['value'])
            print(prop_nonce)
            data['property_nonce'] = prop_nonce

            print("aya")
            province = ''.join(map(str,str(postdata['addr_province']).split(' ')))
            #print(province)
            abc = sou.find('select',attrs = {'name':'administrative_area_level_1'})
            #print(abc)
            for pq in abc.find_all('option'):
                if(str(pq.text) in str(province) or str(province) in str(pq.text)):
                    data['administrative_area_level_1'] = str(pq['value'])
                    break
                      
            if(data['administrative_area_level_1']=='' or data['administrative_area_level_1'] == 'กรุงเทพ' ):
                data['administrative_area_level_1'] = 'กรุงเทพ'
                dist = ''.join(map(str,str(postdata['addr_district']).split(' ')))
                #print(province)
                abc = sou.find('select',attrs = {'name':'locality2'})
                #print(abc)
                for pq in abc.find_all('option'):
                    if(str(pq.text) in str(dist) or str(dist) in str(pq.text)):
                        data['locality2'] = str(pq['value'])
                        break
                
            print("aya1")
            img_upload = 'https://www.adscondo.com/wp-admin/admin-ajax.php'
            at_id = []
            deltAll = sou.findAll('a',attrs = {'class':'icon icon-delete'})
            print(deltAll)

            #delete all images
            print('before delete')
            print(len(deltAll))
            print('length')
            if len(deltAll)>0:
                for delt in deltAll:
                    print(delt)
                    del_data={
                        'action': 'houzez_remove_property_thumbnail',
                        'prop_id': delt['data-property-id'],
                        'thumb_id': delt['data-attachment-id'],
                        'removeNonce': removeNonce
                    }
                    r=self.httprequestObj.http_post(img_upload,data=del_data)
                    print(r.text)

            #upload all images    
            print("before upload")
            img_upload = 'https://www.adscondo.com/wp-admin/admin-ajax.php?action=houzez_property_img_upload&verify_nonce='+removeNonce
            for ind, i in enumerate(postdata['post_images']):
                file = {'property_upload_file': (i, open(i, "rb"), "image/jpeg")} 
                upload_file = self.httprequestObj.http_post(img_upload,data = {'name':i},files=file)
                jr = json.loads(upload_file.text)
                at_id.append(jr['attachment_id'])
            print('yha')
            data['featured_image_id'] = at_id[0]     
            for i in range(len(postdata['post_images'])):
                data['propperty_image_ids[]'].append(at_id[i])

            
            r = self.httprequestObj.http_post(reqst_url,data = data)
            #post_url = 'https://www.adscondo.com/คอนโด/'+p_title
            success = True
            detail = "Post edited successfully"
        
        else:
            success = False
            detail = "Can not log in"
            
        end_time,usage_time=set_end_time(start_time)
        
        return {
            "websitename": "adscondo",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(usage_time),
            "post_url": post_url,
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
            "detail": detail,
            "account_type": "null"
        }


    def delete_post(self,postdata):
        start_time = datetime.utcnow()

        post_id = postdata['post_id']
        url = 'https://www.adscondo.com/wp-admin/admin-ajax.php'
        login = self.test_login(postdata)

        if (login["success"] == True):
            data = {
                'action': 'houzez_delete_property', 
                'prop_id': post_id
            }
            try:
                account = postdata['account_type']
            except:
                account = 'null'
            get_url = 'https://www.adscondo.com/%E0%B8%AD%E0%B8%AA%E0%B8%B1%E0%B8%87%E0%B8%AB%E0%B8%B2%E0%B8%AF%E0%B8%82%E0%B8%AD%E0%B8%87%E0%B8%89%E0%B8%B1%E0%B8%99%E0%B8%82%E0%B8%B2%E0%B8%A2%E0%B8%84%E0%B8%AD%E0%B8%99%E0%B9%82%E0%B8%94/'
            r = self.httprequestObj.http_get(get_url)
            sou = BeautifulSoup(r.text,'html5lib')
            security = sou.findAll('a',attrs = {'class':'delete-property'})
            
            #delete all images
            flag = 0
            for delt in security:
                print(delt['data-id'])
                if delt['data-id'] == post_id:
                    data['security'] = delt['data-nonce']
                    flag = 1
                    break 
            
            if flag==0:
                success = False
                detail = 'Post Not Found'

            else:
                r = self.httprequestObj.http_post(url,data = data)
                jr = json.loads(r.text)
        
                if jr['success'] == False:
                    success= False
                    detail = 'Delete Failed'
                else :
                    success= True
                    detail = 'Post Deleted Successfully\n'
        else:
            success = False
            detail = "Can not log in"
            
        end_time,usage_time=set_end_time(start_time)
        
        return {
            "websitename": "adscondo",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(usage_time),
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
            "log_id":postdata['log_id'],
            "detail": detail,
            "account_type": account
        }
    
    def search_post(self,postdata):
        start_time = datetime.utcnow()

        login = self.test_login(postdata)
        try:
            account = postdata['account_type']
        except:
            account = 'null'
        post_found = "false"
        post_id = ''
        post_url = ''
        post_view = ''
        post_modify_time = ''
        post_create_time = ''
        detail = 'No post with this title'
        title = ''
        if (login['success'] == True):

            pages = ["", "page/2", "page/3"]
            tURL = dict()
            flag1 = 0
            for page in pages:
                print(page)
                all_posts_url = 'https://www.adscondo.com/%e0%b8%ad%e0%b8%aa%e0%b8%b1%e0%b8%87%e0%b8%ab%e0%b8%b2%e0%b8%af%e0%b8%82%e0%b8%ad%e0%b8%87%e0%b8%89%e0%b8%b1%e0%b8%99%e0%b8%82%e0%b8%b2%e0%b8%a2%e0%b8%84%e0%b8%ad%e0%b8%99%e0%b9%82%e0%b8%94/' + page

                all_posts = self.httprequestObj.http_get(all_posts_url)

                page = soup(all_posts.text, features = "html5lib")
                #print(page,"###")
                divi = page.findAll('div', attrs = {'class':'item-wrap'})
               
                
                if divi == None:
                    detail = "Post Not Found"
                    continue

                else:
                    flag= 0
                    print(postdata['post_title_th'])
                    for one in divi:
                        
                        title = one.find('h4',attrs = {'class':'my-heading'})
                        
                        if postdata['post_title_th'].strip() == title.text.strip() :
                            
                            post_url = title.find('a')['href']
                        
                            #print(post_url,end = '\n')
                            post_found = "true"
                            
                            post_id = one.find('a',attrs = {'class':'delete-property'})['data-id']
                            r = self.httprequestObj.http_get(post_url)
                            sou = BeautifulSoup(r.text,'html5lib')

                            post_modify_time =  sou.findAll('div',attrs = {'class':'title-right'})[1].find('p').text[15:]
                            #post_view = divi.find('li',attrs={'class':'price'}).findAll('span')[-1].text.split(' ')[1]
                            detail = "Post Found "
                            flag=1
                            break
                    if flag==0:
                        detail = "Post Not Found"
                        post_found = 'false'
                    else:
                        break
                        #print("yha se gya")
        else :  
            detail = 'Can not log in'
            post_found = 'false'

        end_time = datetime.utcnow()
        

        return {
            "websitename": "adscondo",
            "success": login['success'],
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(end_time - start_time),
            "detail": detail,
            "account_type":account,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "post_url": post_url,
            "post_modify_time": post_modify_time,
            "post_create_time" : post_create_time,
            "post_view": post_view,
            "post_found": post_found
        }

    def boost_post(self,postdata):
        strt = (datetime.utcnow())
        end_time,usage_time = set_end_time(strt)
        return {
            "websitename": "adscondo",
            "success": True,
            "start_time": str(strt),
            "end_time": str(end_time),
            "usage_time": str(usage_time),    
            "ds_id": postdata['ds_id'],
            "post_id": postdata['post_id'],
            "detail": "No boost Post option",
            "account_type": "null"
        }