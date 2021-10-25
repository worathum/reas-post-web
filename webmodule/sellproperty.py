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

class sellproperty():

    name = 'sellproperty'
    property_dict={
    '1': '4', 
    '2': '2',
    '3': '15', 
    '4': '3', 
    '5': '6', 
    '6': '1', 
    '7': '5', 
    '8':'7', 
    '9': '8', 
    '10': '9',
    '25': '9'
    }

    def __init__(self):

        try:
            import configs
        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.primarydomain = 'https://www.xn--22ck4f6agj3aeg.com/'
        self.debug = 0
        self.debugresdata = 0
        self.parser = 'html.parser'
        self.session = lib_httprequest()

    def register_user(self,userdata):
        start_time = datetime.utcnow()
        try:
            account = postdata['account_type']
        except:
            account = 'null'
        
        checkData = {
            'check' : '1',
            'submit' : 'Next | Next >>'
        }
        self.session.http_get("https://www.xn--22ck4f6agj3aeg.com/member-register.php")
        r = self.session.http_post("https://www.xn--22ck4f6agj3aeg.com/member-register.php",data = checkData)
        
        username = str(userdata['name_th']+"-"+userdata['surname_th'])
        if 'addr_soi' in userdata and userdata['addr_soi']!=None:
                pass
        else:
            userdata['addr_soi']=''
        if 'addr_road' in userdata and userdata['addr_soi']!=None:
                pass
        else:
            userdata['addr_road']=''
        prod_address = ""
        for add in [userdata['addr_soi'], userdata['addr_road'], userdata['addr_sub_district'], userdata['addr_district'], userdata['addr_province']]:
            if add is not None and add!="" and add!=" ":
                prod_address += add + ","
        prod_address = prod_address[:-1]
        data = {
            "name" : username,
            "add": prod_address,
            "province":"",
            "amphur":"",
            "tel":userdata['tel'],
            "website":"",
            "email":userdata['user'],
            "pass":userdata['pass'],
            "rands":"",
            "capcha":"",
            "submit":"Become a member"
        }
        province = ''.join(map(str,str(userdata['addr_province']).split(' ')))
        find_province = r.text
        sou = soup(find_province,features = "html5lib")
        #print(find_province)
        abc = sou.find('select',attrs = {'name':'province'})
        #print(abc)
        for pq in abc.find_all('option'):
            if(str(pq.text) in str(province) or str(province) in str(pq.text)):
                data['province'] = str(pq['value'])
                break
        
        district = ''.join(map(str,str(userdata['addr_district']).split(' ')))
        url_district = str('https://www.xn--22ck4f6agj3aeg.com/data_for_list3.php?province='+str(data['province']))
        find_district = self.session.http_get(url_district).text
        print(find_district)
        abc = soup(find_district,features = "html5lib")
        
        cnt=0
        for pq in abc.find_all('option'):
            if(str(pq.text) in str(district) or str(district) in str(pq.text)):
                data['amphur'] = str(pq['value'])
                cnt +=1
                break
        
        if cnt==0:
            amp = abc.find('option')
            data['amphur'] = str(amp['value'])

        capRow = sou.find('input',attrs={'id':'rands'})['value']
        print(capRow)
        data['rands'] = capRow
        data['capcha'] = data['rands']
        res = self.session.http_post('https://www.xn--22ck4f6agj3aeg.com/p-member-register.php',data = data)
        print(res.text)
        sou = soup(res.text,'html5lib')
        err = sou.find("script")

        if err == None:
            success = "true"
            detail = 'User Registered Successfully'
            
        else :
            success='false'
            detail = 'User '+ userdata['user']+' already exists'
        
        
        end_time,usage_time=set_end_time(start_time)
        
        return {
            "websitename": "sellproperty",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(usage_time),
            "ds_id": userdata['ds_id'],
            "detail": detail,
            "account_type": account
        }



    def test_login(self, postdata):
        #self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.utcnow()

        email = postdata['user']
        passwd = postdata['pass']
        try:
            account = postdata['account_type']
        except:
            account = 'null'
        
        
        success = "true"
        detail = ""

        data = {
            'email': email,
            'pass': passwd
        }
        print(email,passwd)
        r = self.session.http_post('https://www.xn--22ck4f6agj3aeg.com/login.php', data=data)
        #print(r.url)
        sou = soup(r.text,'html5lib')
        print(r.text)
        '''
        resp = self.session.http_get("https://www.xn--22ck4f6agj3aeg.com/member/edit-personal.php")
        sou = soup(resp.text,'html5lib')
        '''
        err = sou.find("script")

        if err == None:
            success = 'true'
            detail = "logged in"
        else :
            success = 'false'
            detail = 'Invalid User id or Password'

        time_end = datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "sellproperty",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "ds_id": postdata['ds_id'],
            "account_type":account
        }

    def delete_post(self,postdata):

        #self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.utcnow()

        login = self.test_login(postdata)

        post_id = postdata['post_id']
        try:
            account = postdata['account_type']
        except:
            account = 'null'
                
        

        if (login["success"] == "true"):
            
            data = {
                "chkDel[]":post_id,
                "type":"2",
                "Submit":"Proceed",
                "hdnCount":"1"    
            }

            all_posts_url = 'https://www.xn--22ck4f6agj3aeg.com/member/list-property.php'

            all_posts = self.session.http_get(all_posts_url)
            
            page = soup(all_posts.content, features = "html5lib")
            
            divi = page.find('form', attrs = {'name':'frmMain'})
            tr = divi.findAll('tr')
            data['hdnCount'] = str(len(tr)-2)
            xyz = divi.findAll('a')
            #print(xyz,len(xyz))
            
            if xyz == None:
                detail = "Post Not Found"
            else:
                flag= 0
                for one in xyz:
                    
                    if one.has_attr('title') and one['title']=='แก้ไข' :
                        pid = str(one['href'].split('=')[-1])
                        if pid == post_id :
                            post_url = "https://www.xn--22ck4f6agj3aeg.com/member/manage-property-not-sale.php"
                            res = self.session.http_post(post_url,data = data)
                            print(res.text)
                            sou = soup(res.text,'html5lib')
                            url = sou.find('meta',attrs = {'http-equiv':'refresh'})['content']
                            print(url)
                            flag = 1
                            break
                            
            if flag==0 :
                success = "false"
                detail = "Post Not Found"
            else:
                success = "true"
                detail = "Post Deleted successfully"
        else:
            success = "false"
            detail = "Can not log in"
            
        end_time,usage_time=set_end_time(start_time)

        return {
            "websitename": "sellproperty",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(usage_time),
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "detail": detail,
            "account_type":account
        }         


    def create_post(self,postdata):

        #self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.utcnow()
        login = self.test_login(postdata)

        post_id = ''
        post_url = ''
        try:
            account = postdata['account_type']
        except:
            account = 'null'
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }

        if (login["success"] == "true"):
            print("yha Phunch gya")
            try :
                project = postdata['web_project_name']
            except:
                project = ""                

            try:
                subdist = postdata['addr_sub_district']
            except:
                subdist = ""

            try:
                bathroom = str(postdata['bath_room'])
            except:
                bathroom = '0'
            try:
                bedroom = str(postdata['bed_room'])
            except:
                bedroom = '0'

            try:
                floors = str(postdata['floor_total'])
            except:
                floors = '0'

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

            print(land_size_ngan,land_size_rai,land_size_wa)

            if str(postdata['property_type'])=='1':
                try:
                    print(postdata['floorarea_sqm'])
                    area = str(postdata['floorarea_sqm'])+" ตรม."
                except:
                    area = "0 ตรม."
            else :
                try:
                    print(land_size_ngan,land_size_rai,land_size_wa)
                    area = (land_size_rai*400) + (land_size_ngan*100)+ land_size_wa
                    area = str(area) + "ตรว."
                except:
                    area = "0 ตรว."
            data = {
                'class_type_id': '',
                'cate_id': self.property_dict[str(postdata['property_type'])],
                'title': postdata['post_title_th'],
                'project': project,
                'add': subdist, 
                'province': '',
                'amphur': '',
                'map_lat': str(postdata['geo_latitude']),
                'map_lng': str(postdata['geo_longitude']),
                'map_zoom':'', 
                'detail': postdata['post_description_th'].replace('\r','<br>').replace('\n','<br>'),
                'area': area,
                'bedroom': bedroom,
                'bathroom': bathroom,
                'floors': floors,
                'price': postdata['price_baht'],
                'name': str(postdata['name']),
                'tel': postdata['mobile'],
                'email': postdata['email'],
                'website': '',
                'rands': '',
                'capcha': '',
                'submit': 'Continue >>'
            }
            if postdata['listing_type']=='ขาย':
                data['class_type_id'] = '1'
            else :
                data['class_type_id'] = '2'

                        
            rget = self.session.http_get('https://www.xn--22ck4f6agj3aeg.com/member/post-property.php')
            sou = soup(rget.text,'html5lib')
            


            
            #data['name'] = str(sou.find('input',attrs={'name':'name'})['value'])
            #data['email'] = str(sou.find('input',attrs={'name':'email'})['value'])
            #data['tel']=str(sou.find('input',attrs={'name':'tel'})['value'])
            
            
            province = ''.join(map(str,str(postdata['addr_province']).split(' ')))
            #print(province)
            abc = sou.find('select',attrs = {'name':'province'})
            #print(abc)
            for pq in abc.find_all('option'):
                if(str(pq.text) in str(province) or str(province) in str(pq.text)):
                    data['province'] = str(pq['value'])
                    break
                      
            if(data['province']==''):
                data['province'] = '1'
            #print(data['city'])
            district = ''.join(map(str,str(postdata['addr_district']).split(' ')))
            #https://www.xn--22ck4f6agj3aeg.com/data_for_list3.php?province=11

            #https://www.xn--22ck4f6agj3aeg.com/member/p-post-property.php   post reqst no data  id in return url
            url_district = str('https://www.xn--22ck4f6agj3aeg.com/data_for_list3.php?province='+str(data['province']))
            


            find_district = self.session.http_get(url_district)
            abc = soup(find_district.text,features = "html5lib")
          
            cnt=0
            for pq in abc.find_all('option'):
                if(str(pq.text) in str(district) or str(district) in str(pq.text)):
                    data['amphur'] = str(pq['value'])
                    cnt +=1
                    break
            
            if cnt==0:
                amp = abc.find('option')
                data['amphur'] = str(amp['value'])
        

                
            capRow = sou.find('input',attrs={'id':'rands'})['value']
            print(capRow)
            data['rands'] = capRow
            data['capcha'] = data['rands']       
            
            if 'post_images' in postdata and len(postdata['post_images']) > 0:
                pass
            else:
                postdata['post_images'] = ['./imgtmp/default/white.jpg']


            file = []
            y=str(datetime.utcnow()).replace('-','').replace(":","").replace(".","").replace(" ","")+".jpg"
            file.append(('fileshow',(y, open(postdata['post_images'][0], "rb"), "image/jpeg")))
            cnt = 1
            for i in postdata['post_images'][1:]:
                y=str(datetime.utcnow()).replace('-','').replace(":","").replace(".","").replace(" ","")+".jpg"
                file.append(('file'+str(cnt),(y, open(i, "rb"), "image/jpeg")))
                if cnt==4:
                    break
                cnt+=1
            #data['filename']=file_name
            #print(data)
            upload_file = self.session.http_post('https://www.xn--22ck4f6agj3aeg.com/member/p-post-property.php',data = data,files = file)
            
            url = soup(upload_file.text,'html5lib')
            urlList = url.find('meta',attrs = {'http-equiv':'refresh'})['content']  
            
            
            urlList = urlList.split('=')
        
            #print()
            if len(urlList)<=2:
                success = 'false'
                detail = 'missing or duplicate entry'
                post_url = '' 
                post_id= ''
            else:
                
                post_id = str(urlList[2])
                #print(post_id)
                post_url = 'https://www.xn--22ck4f6agj3aeg.com/property-'+post_id+'/'+data['title'].replace(' ','-').replace("%","เปอร์เซ็นต์")+'.html'
                success = "true"
                detail = "Post created successfully"
                #print(post_url)
            
        else:
            success = "false"
            detail = "Can not log in"
            
        end_time,usage_time=set_end_time(start_time)
        
        return {
            "websitename": "sellproperty",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(usage_time),
            "post_url": post_url,
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
            "detail": detail,
            "account_type": account
        }

    def search_post(self,postdata):
        #self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        #search
        start_time = datetime.utcnow()

        login = self.test_login(postdata)
        try:
            account = postdata['account_type']
        except:
            account = 'null'
        
        if (login['success'] == 'true'):

            post_found = "false"
            post_id = ''
            post_url = ''
            post_view = ''
            post_modify_time = ''
            post_create_time = ''
            detail = 'No post with this title'
            title = ''
            all_posts_url = 'https://www.xn--22ck4f6agj3aeg.com/member/list-property.php'

            all_posts = self.session.http_get(all_posts_url)

            page = soup(all_posts.content, features = "html5lib")
            print(page,"###")
            #purl = page.find('meta',attrs={'http-equiv':'refresh'})['content']
            #print(purl,"$$$")
            #purl = purl.split('=')[-1]
            #print(purl,"###")
            divi = page.find('form', attrs = {'name':'frmMain'})
            xyz = divi.findAll('a')
            #print(xyz,len(xyz))
            
            if xyz == None:
                detail = "Post Not Found"
            else:
                flag= 0
                print(postdata['post_title_th'])
                for one in xyz:
                    print(one['title'])
                    
                    if one.has_attr('title') and one['title']==postdata['post_title_th'] :
                        ind=0
                        for i in one['href']:
                            if i =='/':
                                ind+=1
                                break
                            ind += 1
                        
                        post_url = str(self.primarydomain) + one['href'][ind:]
                    
                        #print(post_url,end = '\n')
                        post_found = "true"
                        time = one.findNext('span')
                        
                        post_modify_time = time.text[14:]
                        post_id = post_url.split('/')[-2].split('-')[1]

                        #post_view = divi.find('li',attrs={'class':'price'}).findAll('span')[-1].text.split(' ')[1]
                        detail = "Post Found "
                        flag=1
                        break
                if flag==0:
                    detail = "Post Not Found"
                    post_found = 'false'
                    
                    #print("yha se gya")
        else :
            detail = 'Can not log in'
            post_found = 'false'

        end_time = datetime.utcnow()
        

        return {
            "websitename": "sellproperty",
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

        #self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.utcnow()

        login = self.test_login(postdata)

        post_id = postdata['post_id']
        try:
            account = postdata['account_type']
        except:
            account = 'null'
        

        if (login["success"] == "true"):
            
            all_posts_url = 'https://www.xn--22ck4f6agj3aeg.com/member/list-property.php'

            all_posts = self.session.http_get(all_posts_url)
            
            page = soup(all_posts.content, features = "html5lib")
            
            divi = page.find('form', attrs = {'name':'frmMain'})
            
            xyz = divi.findAll('a')
            #print(xyz,len(xyz))
            
            if xyz == None:
                detail = "Post Not Found"
            else:
                flag= 0
                for one in xyz:
                    
                    if one.has_attr('title') and one['title']=='แก้ไข' :
                        pid = str(one['href'].split('=')[-1])
                        if pid == post_id :
                            post_url = "https://www.xn--22ck4f6agj3aeg.com/member/slide-property.php?post_id="+pid
                            res = self.session.http_get(post_url)
                            flag = 1
                            break
                            
            if flag==0 :
                success = "false"
                detail = "Post Not Found"
            else:
                success = "true"
                detail = "Post Boosted successfully"
        else:
            success = "false"
            detail = "Can not log in"
            
        end_time,usage_time=set_end_time(start_time)

        return {
            "websitename": "sellproperty",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(usage_time),
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "detail": detail,
            "account_type":account
        }             


    def edit_post(self,postdata):
        start_time = datetime.utcnow()

        login = self.test_login(postdata)

        post_id = postdata['post_id']
        
        if (login["success"] == "true"):
            delete = self.delete_post(postdata)
            if delete['success']=='true':
                cpost = self.create_post(postdata)
                if cpost['success']=='true':
                    cpost['detail'] = 'Post Edited (delete + create new)'
                    
                else:
                    cpost['detail'] = 'Post creation step could not be completed'
                cpost['log_id'] = postdata['log_id']
                end_time,usage_time=set_end_time(start_time)
                cpost['end_time'] = str(end_time)
                cpost['usage_time'] = str(usage_time)
                cpost['start_time'] = str(start_time)
                return cpost
            else:
                delete['log_id'] = postdata['log_id']
                end_time,usage_time=set_end_time(start_time)
                delete['end_time'] = str(end_time)
                delete['usage_time'] = str(usage_time)
                delete['start_time'] = str(start_time)
                return delete
        else:
            end_time,usage_time=set_end_time(start_time)
            login['log_id'] = postdata['log_id']
            login['end_time'] = str(end_time)
            login['usage_time'] = str(usage_time)
            login['start_time'] = str(start_time)
            return login
                
