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

class bogie2():

    name = 'Bogie2'
    property_dict={
    '1': '35', 
    '2': '75',
    '3': '77', 
    '4': '77', 
    '5': '78', 
    '6': '79', 
    '7': '118', 
    '8':'118', 
    '9': '86', 
    '10': '101',
    '25': '101'
    }

    def __init__(self):

        try:
            import configs
        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.primarydomain = 'https://bogie2.com/'
        self.debug = 0
        self.debugresdata = 0
        self.parser = 'html.parser'
        self.session = lib_httprequest()

    def register_user(self, userdata):
        #self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        
        reqst_url = "https://bogie2.com/process.php?process=createUserPost"
        start_time = datetime.utcnow()
        res={'websitename':'bogie2', 'success':False, 'start_time': str(start_time), 'end_time': '0', 'usage_time': '0', 'detail': '','ds_id':userdata['ds_id']}
        username = str(userdata['name_th']+" "+userdata['surname_th'])
        payload = {
            'username': userdata["user"].split('@')[0] ,
            'your_name': username,
            'email': userdata['user'],
            'phone': userdata['tel'],
            'password': userdata['pass'],
            'confirmpassword': userdata['pass']
        }

        userpass_regex=re.compile(r'^([a-zA-Z0-9_]{4,15})$')
        email_regex=re.compile(r'^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$')
        if(userpass_regex.search(payload['username'])==None):
            res['detail']+='User Name must be in az, AZ, 0-9 or _ only and should be 4-15 characters only. '
        if(userpass_regex.search(payload['password'])==None):
            res['detail']+='Password must be in az, AZ, 0-9 or _ only and should be 4-15 characters only. '
        if(email_regex.search(payload['email'])==None):
            res['detail']+='Invalid email. '
    
        phone_regex=re.compile(r'^([0-9]{8,10})$')
        if(phone_regex.search(payload['phone'])==None):
            res['detail']+='Invalid phone number. '
        if(res['detail']!=''):
            res['end_time'],res['usage_time']=set_end_time(start_time)
            return res

        r = self.session.http_post(reqst_url, data=payload)

        parsedHtml = soup(r.text,'html5lib')

        if len(parsedHtml.text)!=0:
            res['success']='false'
            res['detail'] = 'User already exists\n'
        else :
            res['success']='true'
            res['detail'] = 'User Registered Successfully\n'
        endT,usage_time=set_end_time(start_time)
        res['end_time'] = str(endT)
        res['usage_time'] = str(usage_time)
        return res


    def test_login(self,userdata):
        
        login_url = "https://bogie2.com/process.php?process=userLogin"
        start_time = datetime.utcnow()
        res={'websitename':'bogie2', 'success':False, 'start_time': str(start_time), 'end_time': '0', 'usage_time': '0', 'detail': '','ds_id':userdata['ds_id']}
        login_pload = {
            'username': userdata['user'],
            'password': userdata['pass']
        }
        
        r= self.session.http_post(login_url, data=login_pload)

        parsedHtml = soup(r.text, 'html5lib')

        if parsedHtml.text=="user-not-found":
            res['success']='false'
            res['detail'] = 'User not Found'
        elif parsedHtml.text=="password-not-match":
            res['success']='false'
            res['detail'] = 'Wrong Password'
        else :
            res['success']='true'
            res['detail'] = 'User Logged In Successfully\n'
        endT,usage_time=set_end_time(start_time)
        res['end_time'] = str(endT)
        res['usage_time'] = str(usage_time)
        return res

    def create_post(self,postdata):

        #self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.utcnow()

        login = self.test_login(postdata)

        post_id = ''
        post_url = ''
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }

        if (login["success"] == "true"):
            if 'web_project_name' not in postdata or postdata['web_project_name'] == "":
                if 'project_name' in postdata and postdata['project_name'] != "":
                    postdata['web_project_name'] = postdata['project_name']
                else:
                    postdata['web_project_name'] = postdata['post_title_th']
                    
            prod_address = ""
            for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
                if add is not None:
                    prod_address += add + " "
            prod_address = prod_address[:-1]
            '''
            desc = postdata['post_description_th']
            sz = len(desc)
            i=0
            sendStr = ''
            prev = 0
            while i < sz:
                if desc[i]=='\\':
                    if i!= sz-1 and (desc[i+1] == 'r'  or desc[i+1] == 'n'):
                        sendStr = desc[prev:i]+'<br>'
                        prev = i+2
                        i = i+1
                i+=1
                
            sendStr = sendStr + desc[prev:]
            print(sendStr)
            '''
            data = {
                'post_type':'',
                'product_type':'buy',
                'title': str(postdata['post_title_th'].replace("\n","<br>")),
                'category_id': '2',
                'category_id_2':str(self.property_dict[str(postdata["property_type"])]),
                'category_id_3':'ขายคอนโด',
                'price': postdata['price_baht'],
                'description': postdata['post_description_th'].replace('\n','<br>'),
                'phone': str(postdata['mobile']),
                'email': str(postdata['email']),
                'line': str(postdata['line']),
                'address': '-',
                'amphur_id': '',
                'province_id' : ''
            }

            if postdata['listing_type'] == 'เช่า':
                data['post_type'] = 'rent'
            else:
                data['post_type'] = 'sale'


            
            cat = self.session.http_post('https://bogie2.com/process.php?process=getCategoryStep',data = data['category_id'], headers = headers).text
            cat2 = self.session.http_post('https://bogie2.com/process.php?process=getCategoryStep2',data = data['category_id_2'], headers = headers).text

            if 'post_images' in postdata and len(postdata['post_images']) > 0:
                pass
            else:
                postdata['post_images'] = ['./imgtmp/default/white.jpg']


            
            # temp = 1
            file_name=[]
            send_file = [] 
            print("imgs start")    
            for ind, i in enumerate(postdata['post_images']):
                # y=str(datetime.utcnow()).replace('-','').replace(":","").replace(".","").replace(" ","")+".jpg"
                #print(y)
                file = {'files[]': (i, open(i, "rb"), "image/jpeg")}
                if ind > 0:
                    send_file.append(('files[]', file['files[]']))
                print(file)
                upload_file = self.session.http_post_with_headers('https://bogie2.com/php/upload.php',data = {},files=file)
                print(upload_file.text)
                file_name.append(upload_file.text)
                # temp = temp + 1

            data['img[]'] = file_name
            
            # up_data = {
            #     "files[]":file,
            #     "filename": file_name,
            # }
            # head_upload = {
            #     "Content-Type": "image/jpeg",
            #     "Content-Disposition": "form-data",
            #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
            # }
            
            # print(upload_file.text,end='\n')

            province = ''.join(map(str,str(postdata['addr_province']).split(' ')))
            find_province = self.session.http_get('https://bogie2.com/post', headers = headers).text
            sou = soup(find_province,features = "html5lib")

            abc = sou.find('select',attrs = {'name':'province_id'})
    
            for pq in abc.find_all('option'):
                if(str(pq.text) in str(province) or str(province) in str(pq.text)):
                    data['province_id'] = str(pq['value'])
                    break

            dist_data = {
                'provinceId': data['province_id'],
                'amphurId':''

            }
            url_district = 'https://bogie2.com/process.php?process=getAmphur'

            find_district = self.session.http_post(url_district, data = dist_data,headers = headers).text
            sou = soup(find_district,features = "html5lib")

            try:

                for pqr in sou.find_all('option'):
                    if(str(pqr.text) in str(district) or str(district) in str(pqr.text)):
                        data['amphur_id'] = str(pqr['value'])
                        break

            except:
                data['amphur_id'] = str(sou.find('option')['value'])

            
            
            
            crt_post = self.session.http_post_with_headers('https://bogie2.com/process.php?process=createPost',data=data,files=send_file)
            print(crt_post.text,end = '\n')
            
            create = BeautifulSoup(crt_post.content, features = "html5lib")
            print(create)
            post_id_ind = create.text.find('redirect')
            end_ind = create.text.find(',',post_id_ind)
            post_id = create.text[post_id_ind+11:end_ind-1]
            post_url = str('https://bogie2.com/detail/'+post_id+'/'+data['title'].replace("%","เปอร์เซ็นต์")+'.html').replace(' ','-')

            
            success = "true"
            detail = "Post created successfully"
    
        else:
            success = "false"
            detail = "Can not log in"
            
        end_time,usage_time=set_end_time(start_time)
        
        return {
            "websitename": "bogie2",
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

        #self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.utcnow()

        login = self.test_login(postdata)

        post_id = postdata['post_id']
        post_url = 'https://bogie2.com/process.php?process=deletePost'
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }

        if (login["success"] == "true"):
            del_data = {
                'post_id':post_id
            }
            res = self.session.http_post(post_url,data = del_data,headers = headers)
            print(res.text)
            if res.text == 'ไม่สามารถลบโพสได้':
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
            "websitename": "bogie2",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(usage_time),
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "detail": detail
        }
    
    def boost_post(self,postdata):

        #self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.utcnow()

        login = self.test_login(postdata)

        post_id = postdata['post_id']
        post_url = 'https://bogie2.com/process.php?process=addRenew'
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }

        if (login["success"] == "true"):
            del_data = {
                'post_id':post_id
            }
            res = self.session.http_post(post_url,data = del_data,headers = headers)
            print(res.text)
            if res.text == 'ไม่สามารถเลื่อนกระทู้ได้':
                success = "false"
                detail = "Cannot Post a Thread/ Post Not Found"
            else:
                success = "true"
                detail = "Post Postponed successfully"
        else:
            success = "false"
            detail = "Can not log in"
            
        end_time,usage_time=set_end_time(start_time)

        return {
            "websitename": "bogie2",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(usage_time),
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "detail": detail
        }

    def search_post(self,postdata):
        #self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        #search
        start_time = datetime.utcnow()

        login = self.test_login(postdata)
        
        if (login['success'] == 'true'):

            post_found = "false"
            post_id = ''
            post_url = ''
            post_view = ''
            post_modify_time = ''
            detail = 'No post with this title'
            title = ''
            all_posts_url = 'https://bogie2.com/allpost/all'

            all_posts = self.session.http_get(all_posts_url)

            page = soup(all_posts.content, features = "html5lib")


            xyz = page.find('a', attrs = {'target':'_blank','title':postdata['post_title_th']})
            #print(xyz,len(xyz))
            
            if xyz == None:
                detail = "Post Not Found"
            else:
                post_url = xyz['href']
                #print(post_url,end = '\n')
                post_found = "true"
                post_by = page.find(class_='postby')
                #print(post_by.text)
                
                fonts = post_by.findAll('i')
                #print(fonts[0].contents)
                print(fonts)
                
                for f in fonts:
                    fns = str(f.next_sibling).replace("\t","").replace("\n","")
                    #print(type(fns))
                    
                    if 'ที่ผ่านมา' in fns:
                        post_modify_time = fns
                    if 'ครั้ง' in fns:
                        post_view = fns
                    
                detail = "Post Found "
                post_id = post_url.split('/')[4]  
                      
                    
        else :
            detail = 'Can not log in'
            post_found = 'false'

        end_time = datetime.utcnow()
        

        return {
            "websitename": "bogie2",
            "success": login['success'],
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(end_time - start_time),
            "detail": detail,
            "account_type":"null",
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "post_url": post_url,
            "post_modify_time": post_modify_time,
            "post_create_time" : "",
            "post_view": post_view,
            "post_found": post_found
        }


    def edit_post(self,postdata):

        #self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.utcnow()

        login = self.test_login(postdata)

        post_id = ''
        post_url = ''
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }

        if (login["success"] == "true"):
            print('login')
            if 'web_project_name' not in postdata or postdata['web_project_name'] == "":
                if 'project_name' in postdata and postdata['project_name'] != "":
                    postdata['web_project_name'] = postdata['project_name']
                else:
                    postdata['web_project_name'] = postdata['post_title_th']
                    
            prod_address = ""
            for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
                if add is not None:
                    prod_address += add + " "
            prod_address = prod_address[:-1]
            post_id = postdata['post_id']
            data = {
                'id':post_id,
                'post_type':'',
                'product_type':'buy',
                'title': str(postdata['post_title_th'].replace("\n","<br>")),
                'price': postdata['price_baht'],
                'description': str(postdata['post_description_th'].replace("\n","<br>")),
                'phone': str(postdata['mobile']),
                'email': str(postdata['email']),
                'line': str(postdata['line']),
                'address': '-',
                'amphur_id': '',
                'province_id' : ''
            }

            if postdata['listing_type'] == 'เช่า':
                data['post_type'] = 'rent'
            else:
                data['post_type'] = 'sale'

            pg = self.session.http_get("https://bogie2.com/edit_post/"+post_id)
            page = soup(pg.text,'html5lib')
            imgList = page.findAll('input',attrs = {'name':'img[]'})
            print(imgList)
            for i in imgList:
                self.session.http_post('https://bogie2.com/php/remove_file.php',data={'file':str(i['value'])})
            
            if 'post_images' in postdata and len(postdata['post_images']) > 0:
                pass
            else:
                postdata['post_images'] = ['./imgtmp/default/white.jpg']


            
            # temp = 1
            file_name=[]
            send_file = [] 
            print("imgs start")    
            for ind, i in enumerate(postdata['post_images']):
                # y=str(datetime.utcnow()).replace('-','').replace(":","").replace(".","").replace(" ","")+".jpg"
                #print(y)
                file = {'files[]': (i, open(i, "rb"), "image/jpeg")}
                if ind > 0:
                    send_file.append(('files[]', file['files[]']))
                #print(file)
                upload_file = self.session.http_post_with_headers('https://bogie2.com/php/upload.php',data = {},files=file)
                file_name.append(upload_file.text)
                # temp = temp + 1

            data['img[]'] = file_name
            
            

            province = ''.join(map(str,str(postdata['addr_province']).split(' ')))
            find_province = self.session.http_get("https://bogie2.com/edit_post/"+post_id, headers = headers).text
            sou = soup(find_province,features = "html5lib")

            abc = sou.find('select',attrs = {'name':'province_id'})
    
            for pq in abc.find_all('option'):
                if(str(pq.text) in str(province) or str(province) in str(pq.text)):
                    data['province_id'] = str(pq['value'])
                    break

            dist_data = {
                'provinceId': data['province_id'],
                'amphurId':''

            }
            url_district = 'https://bogie2.com/process.php?process=getAmphur'

            find_district = self.session.http_post(url_district, data = dist_data,headers = headers).text
            sou = soup(find_district,features = "html5lib")

            try:

                for pqr in sou.find_all('option'):
                    if(str(pqr.text) in str(district) or str(district) in str(pqr.text)):
                        data['amphur_id'] = str(pqr['value'])
                        break

            except:
                data['amphur_id'] = str(sou.find('option')['value'])

            
            
            
            crt_post = self.session.http_post_with_headers('https://bogie2.com/process.php?process=updatePost',data=data,files=send_file)
           
            create = BeautifulSoup(crt_post.content, features = "html5lib")
            post_id_ind = create.text.find('redirect')
            end_ind = create.text.find(',',post_id_ind)
            post_url = str('https://bogie2.com/detail/'+post_id+'/'+data['title'].replace(' ','-').replace("%","เปอร์เซ็นต์")+'/.html')

            
            success = "true"
            detail = "Post Edited successfully"
    
        else:
            success = "false"
            detail = "Can not log in"
            
        end_time,usage_time=set_end_time(start_time)
        
        return {
            "websitename": "bogie2",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(usage_time),
            "post_url": post_url,
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
            "log_id":postdata['log_id'],
            "detail": detail,
            "account_type": "null"
        }






'''
{
	    "action": "create_post",
	    "timeout": "7",
		 "post_img_url_lists": [
		"https://www.bangkokassets.com/property/250064/2199952_83636pic8.jpg",
		"https://www.bangkokassets.com/property/250064/2199945_83636pic1.jpg",
		"https://www.bangkokassets.com/property/250064/2199946_83636pic2.jpg",
		"https://www.bangkokassets.com/property/250067/2199969_83635pic1.jpg"
		],
	    "geo_latitude": "13.786862",
	    "geo_longitude": "100.757815",
	    "property_id" : "chu001",
	    "post_title_th": "ให้เช่า ที่ดินด่วน บางกรวยไทรน้อย 6 ไร่ เหมาะทำตลาด",
		"post_description_th": "ให้เช่า ที่ดินด่วน บางกรวยไทรน้อย 6 ไร่ เหมาะทำตลาดให้เช่า ที่ดินด่วน บางกรวยไทรน้อย 6 ไร่ เหมาะทำตลาด\nรายละเอียด\nที่ดินขนาด6ไร่\nหน้ากว้าง 30 เมตร\nสถานที่ใกล้เคียง\nถนนนครอินทร์\nถนนพระราม5\n\nให้เช่า 100,000 บาท\n\nสนใจติดต่อ ช่อทิพย์ 091829384",
	    "price_baht": "100000",
	    "listing_type": "เช่า",
	    "property_type": "1",
	    "prominent_point  " : "หน้ากว้างมาก ให้เช่าถูกสุด",
	    "direction_type" : "11",
	    "addr_province": "นนทบุรี",
	    "addr_district": "เมืองนนทบุรี",
	    "addr_sub_district": "บางกร่าง",
	    "addr_road": "บางกรวย-ไทรน้อย",
	    "addr_soi": "ซอยบางกรวย-ไทรน้อย 34",
	    "addr_near_by": "ถนนพระราม5\r\nถนนนครอินทร์",
	    "bed_room": "3",
	    "bath_room": "2",
	    "floor_total": "10",
	    "floor_level": "4",
	    "floor_area": "90",
	    "land_size_rai": "1",
	    "land_size_ngan": "6",
	    "land_size_wa": "0",
	    "name": "createname",
	    "mobile": "0992899991",
	    "email": "createpost@email.com",
	    "line": "0992899991",
	    "project_name": "ที่ดิน บางกรวยไทย-น้อย",
        "web": [
        {
            "ds_name": "Bogie2",
            "ds_id": "4",              
            "user": "email@demon.com",
            "pass": "12345678",
            "web_project_name": "ลุมพีนี รามอินทราหลักสี่"   
        }
    ]
}
'''