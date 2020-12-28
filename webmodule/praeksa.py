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

httprequestObj = lib_httprequest()

def set_end_time(start_time):
    time_end = datetime.utcnow()
    time_usage = time_end - start_time
    return time_end, time_usage

class praeksa():

    name = 'praeksa'
    property_dict={
    '1': '1149', 
    '2': '1147',
    '3': '1147', 
    '4': '1154', 
    '5': '1153', 
    '6': '1148', 
    '7': '1150', 
    '8':'1156', 
    '9': '1151', 
    '10': '1155',
    '25': '1155'
    }

    def __init__(self):

        try:
            import configs
        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.primarydomain = 'http://xn--12c1dpz9b3e.com/'
        self.debug = 0
        self.debugresdata = 0
        self.parser = 'html.parser'

    def logout_user(self):
        url = 'http://www.แพรกษา.com/logout.php'
        httprequestObj.http_get(url)

    def register_user(self, userdata):
        #self.print_debug('function ['+sys._getframe().f_code.co_name+']')

        self.logout_user()
        reqst_url = "http://www.xn--12c1dpz9b3e.com/register.php"
        start_time = datetime.utcnow()
        res={'websitename':'praeksa', 'success':'False', 'start_time': str(start_time), 'end_time': '0', 'usage_time': '0', 'detail': '','ds_id':userdata['ds_id']}
        username = str(userdata['name_th']+" "+userdata['surname_th'])
        if 'addr_soi' in userdata and userdata['addr_soi']!=None:
                pass
        else:
            userdata['addr_soi']=''
        if 'addr_road' in userdata and userdata['addr_soi']!=None:
                pass
        else:
            userdata['addr_road']=''
        prod_address = ""

        print(userdata)
        for add in [userdata['addr_soi'], userdata['addr_road'], userdata['addr_sub_district'], userdata['addr_district'], userdata['addr_province']]:
            if add is not None and add!="" and add!=" ":
                prod_address += add + ","
        prod_address = prod_address[:-1]
        payload = {
            
            'email': userdata['user'],
            'password': userdata['pass'],
            'repassword': userdata['pass'],
            'name': username,
            'phone': userdata['tel'],
            'address': prod_address,
            'province': '',
            'amphur': '',
            'zipcode': userdata['addr_zip_code'],
            'title': '',
            'description': '',
            'keyword': '',
            'website': '',
            'answer': '',
            'hiddenanswer': '',
            'accept': 1
        }

        userpass_regex=re.compile(r'^([a-zA-Z0-9_]{4,15})$')
        email_regex=re.compile(r'^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$')
        '''
        if(userpass_regex.search(payload[''])==None):
            res['detail']+='User Name must be in az, AZ, 0-9 or _ only and should be 4-15 characters only. '
        '''
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
        
        
        province = ''.join(map(str,str(userdata['addr_province']).split(' ')))
        find_province = httprequestObj.http_get('http://www.xn--12c1dpz9b3e.com/register.php').text
        sou = soup(find_province,features = "html5lib")
        payload['save'] = str(sou.find('input',attrs = {'name':'save'})['value'])
        payload['answer'] = str(sou.find('input',attrs = {'name':'hiddenanswer'})['value'])
        payload['hiddenanswer'] = payload['answer']
        abc = sou.find('select',attrs = {'name':'province'})

        for pq in abc.find_all('option'):
            if(str(pq.text) in str(province) or str(province) in str(pq.text)):
                payload['province'] = str(pq['value'])
                break
        
        
        
        district = ''.join(map(str,str(userdata['addr_district']).split(' ')))
        url_district = str('http://www.xn--12c1dpz9b3e.com/lib/amphur.php?province='+str(payload['province']))

        find_district = httprequestObj.http_get(url_district).text
        sou = soup(find_district,features = "html5lib")

        abc = sou.find('select',attrs = {'name':'amphur'})
        
        cnt=0
        for pq in abc.find_all('option'):
            if(str(pq.text) in str(district) or str(district) in str(pq.text)):
                payload['amphur'] = str(pq['value'])
                cnt +=1
                break
        
        if cnt==0:
            amp = abc.find('option')
            if amp:
                payload['amphur'] = str(amp['value'])

        #postal service not given
        #data[]
        r1 = httprequestObj.http_post('http://www.xn--12c1dpz9b3e.com/lib/checkuser.php',data = payload)
        sou = BeautifulSoup(r1.text, 'html5lib')

        errors = None
        check=sou.find("body").text

        if check=="-1" or check=="-2":
            errors=True

        if errors is None:
            r = httprequestObj.http_post('http://www.xn--12c1dpz9b3e.com/register.php', data=payload)
            
            #print(r.text)
            #parsedHtml = soup(r.text,'html5lib')

            #if len(parsedHtml.text)!=0:
            res['success']='true'
            res['detail'] = 'User Registered Successfully'
            
        else :
            res['success']='false'
            res['detail'] = 'USer '+ userdata['user']+' already exists\n'
        
        
        res['end_time'],res['usage_time']=set_end_time(start_time)
        return res
        
    def test_login(self, postdata):
        self.logout_user()
        httprequestObj.http_get('http://www.xn--12c1dpz9b3e.com/logout.php')
        #self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.utcnow()

        email = postdata['user']
        passwd = postdata['pass']
        
        success = "true"
        detail = ""

        data = {
            'action': 'login.php',
            'email': email,
            'password': passwd
        }
        rget = httprequestObj.http_get('http://www.xn--12c1dpz9b3e.com/member.php')
        sou = soup(rget.text,'html5lib')
        data['save'] = str(sou.find('input',attrs={'name':'save'})['value'])
        r = httprequestObj.http_post('http://www.xn--12c1dpz9b3e.com/member.php', data=data)
        #print(r.url)
        r_url = str(r.url).split('=')

        if len(r_url)==1:
            success = 'true'
            detail = "logged in"
        else :
            success = 'false'
            detail = 'Invalid User id or Password'

        time_end = datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "praeksa",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "ds_id": postdata['ds_id']
        }

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
            
            data = {
                'type':'guest',
                'want':'',
                'status':'2hand',
                'duration':'-1',
                'category':'1009',
                'subcategory':str(self.property_dict[str(postdata['property_type'])]),
                'city':'',
                'district':'',
                'name':postdata['post_title_th'],
                'price':postdata['price_baht'],
                'detail':'', 
                'checkdetail': postdata['post_description_th'],
                'maplat':postdata['geo_latitude'], 
                'maplon': postdata['geo_longitude'],
                'mapzoom':'',
                'website':''
           }
            if postdata['listing_type']=='ขาย':
                data['want'] = 'sale'
            else :
                data['want'] = 'forrent'

                        
            rget = httprequestObj.http_get('http://www.xn--12c1dpz9b3e.com/post-add.php')
            sou = soup(rget.text,'html5lib')
            


            data['save'] = str(sou.find('input',attrs={'name':'save'})['value'])
            
            data['contact'] = str(sou.find('input',attrs={'name':'contact'})['value'])
            data['email'] = str(sou.find('input',attrs={'name':'email'})['value'])
            
            data['hiddenemail'] = str(sou.find('input',attrs={'name':'hiddenemail'})['value'])
            data['phone']=str(sou.find('input',attrs={'name':'phone'})['value'])
            data['address']= str(sou.find('input',attrs={'name':'address'})['value'])
            data['amphur']= str(sou.find('input',attrs={'name':'amphur'})['value'])
            
            data['province']= str(sou.find('input',attrs={'name':'province'})['value'])
            data['zipcode']= str(sou.find('input',attrs={'name':'zipcode'})['value'])
            
            
            province = ''.join(map(str,str(postdata['addr_province']).split(' ')))
            #print(province)
            abc = sou.find('select',attrs = {'name':'city'})
            #print(abc)
            for pq in abc.find_all('option'):
                if(str(pq.text) in str(province) or str(province) in str(pq.text)):
                    data['city'] = str(pq['value'])
                    break
                      
            if(data['city']==''):
                data['city'] = '1'
            #print(data['city'])
            district = ''.join(map(str,str(postdata['addr_district']).split(' ')))
            url_district = str('http://www.xn--12c1dpz9b3e.com/lib/district.php?province='+str(data['city']))
            


            find_district = httprequestObj.http_get(url_district)
            sou = soup(find_district.text,features = "html5lib")

           

            abc = sou.find('select',attrs = {'name':'district'})
            #print(abc)
            cnt=0
            for pq in abc.find_all('option'):
                #print(pq.text)
                if(str(pq.text) in str(district) or str(district) in str(pq.text)):
                    data['district'] = str(pq['value'])
                    cnt +=1
                    break
            
            if cnt==0:
                data['district'] = '1'
        

                
                    
            
            if 'post_images' in postdata and len(postdata['post_images']) > 0:
                pass
            else:
                postdata['post_images'] = ['./imgtmp/default/white.jpg']


            file = []     
            file_name = []
            cnt = 1
            for i in postdata['post_images']:
                y=str(datetime.utcnow()).replace('-','').replace(":","").replace(".","").replace(" ","")+".jpg"
                file.append(('file'+str(cnt),(y, open(i, "rb"), "image/jpeg")))
                file.append(('photo'+str(cnt),(y, open(i, "rb"), "image/jpeg")))
                file_name.append(y)
                if cnt==6:
                    break
                cnt+=1
            #data['filename']=file_name
            #print(data)
            check_file = httprequestObj.http_post('http://www.xn--12c1dpz9b3e.com/lib/checkpost.php',data = data,headers = headers)
            
            data['detail'] = "<p> "+data['checkdetail']+" </p>"
            loop = 1
            upload_url = []
            #while(loop!=0 and loop<=5):
            #    try:
            upload_file = httprequestObj.http_post('http://www.xn--12c1dpz9b3e.com/post-add.php',data = data,files= file,headers = headers)
            upload_url.append(upload_file.url)
            #        loop = 0
            #    except :
            #        loop+=1
            #        print("connection timeout.Trying again for "+str(loop)+' time')

           
            url = str(upload_url[0])
            #print(upload_file.history)
            
            urlList = url.split('?')
        
            #print()
            if len(urlList)<=1:
                success = 'false'
                detail = 'missing or duplicate entry'
                post_url = '' 
                post_id= ''
            else:
                
                post_id = str(urlList[1].split('&')[1].split('=')[1])
                #print(post_id)
                post_url = 'http://www.xn--12c1dpz9b3e.com/view'+post_id+'/'+data['name']
                success = "true"
                detail = "Post created successfully"
                #print(post_url)
   
        else:
            success = "false"
            detail = "Can not log in"
            
        end_time,usage_time=set_end_time(start_time)
        
        return {
            "websitename": "praeksa",
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
        post_url = 'http://www.xn--12c1dpz9b3e.com/manage-post.php?delete='+post_id
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }

        if (login["success"] == "true"):
            del_data = {
                'post_id':post_id
            }
            res = httprequestObj.http_get(post_url,data = del_data,headers = headers)
            #print(res.text)
            if "You have an error in your SQL syntax;" in res.text :
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
            "websitename": "praeksa",
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

            success="false"
            post_found = "false"
            post_id = ''
            post_url = ''
            post_view = ''
            post_modify_time = ''
            post_create_time = ''
            detail = 'No post with this title'
            #title = ''
            nextpage = True
            p_no = 1
            postdata['post_title_th']=re.sub(r'\.|,',"",postdata['post_title_th'])

            while nextpage:

                url = 'http://www.xn--12c1dpz9b3e.com/manage-post.php?page={}'.format(p_no)
                #all_posts_url = 'http://www.xn--12c1dpz9b3e.com/manage-post.php'
                all_posts = httprequestObj.http_get(url)
                page = soup(all_posts.content, features = "html5lib")

                p = page.find("div", attrs={'class': 'pagination'}).find('ul').findAll("li")
                for i in p:
                    if i.text == "Next »":
                        nextpage = True
                        p_no = p_no + 1
                        break
                else:
                    nextpage = False


                divi = page.find('div', attrs = {'class':'postlist'})
                xyz = divi.findAll('a')
                #print(xyz,len(xyz))

                if xyz == None:
                    detail = "Post Not Found"
                else:
                    flag= 0
                    for one in xyz:
                        if one.has_attr('title') and (one['title'] in postdata['post_title_th'] or postdata['post_title_th'] in one['title']):
                            nextpage=False
                            post_url = one['href']

                            #print(post_url,end = '\n')
                            post_found = "true"
                            time = divi.find('li',attrs={'class':'date'}).findAll('span')
                            post_create_time = time[2].text
                            #post_id = time[-1].text.split(' ')[1]
                            post_id=re.findall(r'\d{6}',post_url)[0]
                            post_view = divi.find('li',attrs={'class':'price'}).findAll('span')[-1].text.split(' ')[1]

                            detail = "Post Found "
                            success="true"
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
            "websitename": self.name,
            "success": success,
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
            "post_create_time" : post_create_time,
            "post_view": post_view,
            "post_found": post_found
        }

    def boost_post(self,postdata):

        #self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.utcnow()

        login = self.test_login(postdata)

        post_id = postdata['post_id']
        post_url = 'http://www.xn--12c1dpz9b3e.com/manage-post.php'
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }

        if (login["success"] == "true"):
            nextpage = True
            p_no = 1

            while nextpage:
                url = 'http://www.xn--12c1dpz9b3e.com/manage-post.php?page={}'.format(p_no)

                res = httprequestObj.http_get(url,headers = headers)
                posts = soup(res.text,'html5lib')

                pages = posts.find("div", attrs={'class': 'pagination'}).find('ul').findAll("li")
                for page in pages:
                    if page.text == "Next »":
                        nextpage = True
                        p_no = p_no + 1
                        break
                else:
                    nextpage = False

                flag=0
                post = posts.find('div',attrs={'class':'postlist'}).findAll('ul')
                for p in post:
                    code = p.find('li',attrs={'class':'date'}).find('span',attrs={'class':'code'}).text.split(' ')[1]
                    ind = 0
                    for i in code:
                        if i=='0':
                            ind+=1
                        else:
                            break
                    code = code[ind:]
                    ret_url = p.find('li',attrs={'class':'title'}).find('a')['href']
                    ret_url=self.primarydomain+ret_url[22:]
                    #print(code)
                    if code == post_id :
                        nextpage=False
                        flag=1
                        httprequestObj.http_get(post_url+'?update='+post_id)

                        success = "true"
                        detail = "Post Postponed successfully"
                        break

                if flag == 0:
                    success = "false"
                    detail = "Cannot Post a Thread/ Post Not Found"
                    ret_url=''
        else:
            success = "false"
            detail = "Can not log in"
            ret_url=''
            
        end_time,usage_time=set_end_time(start_time)

        return {
            "websitename": "praeksa",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(usage_time),
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_url":ret_url,
            "post_id": post_id,
            "detail": detail
        }

    def edit_post(self,postdata):

        #self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.utcnow()
        login = self.test_login(postdata)

        post_id = postdata['post_id']
        post_url = 'http://www.xn--12c1dpz9b3e.com/manage-post.php'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }
        cookies = {
            'Cookie':' PHPSESSID=e4a80cc23ca449f75fbcbb9c921a431f; __atuvc=15%7C28; __atuvs=5f042c7fa3ec6e57005; sc_is_visitor_unique=rx8377448.1594112439.190741BB71924FEF4A194736D37872BE.8.5.3.3.3.2.2.2.2'
        }

        if (login["success"] == "true"):
            nextpage=True
            p_no=1

            while nextpage:

                url = 'http://www.xn--12c1dpz9b3e.com/manage-post.php?page={}'.format(p_no)
                res = httprequestObj.http_get(url,headers = headers)
                posts = soup(res.text,'html5lib')

                pages=posts.find("div",attrs={'class':'pagination'}).find('ul').findAll("li")
                for page in pages:
                    if page.text=="Next »":
                        nextpage=True
                        p_no=p_no+1
                        break
                else:
                    nextpage=False


                flag=0
                post = posts.find('div',attrs={'class':'postlist'}).findAll('ul')

                for p in post:
                    code = p.find('li',attrs={'class':'date'}).find('span',attrs={'class':'code'}).text.split(' ')[1][0:]
                    ind = 0
                    for i in code:
                        if i=='0':
                            ind+=1
                        else:
                            break
                    code = code[ind:]
                    #print(code)
                    if code == post_id :
                        nextpage=False
                        flag=1
                        data = {
                            'type':'guest',
                            'want':'',
                            'status':'2hand',
                            'duration':'90',
                            'category':'1009',
                            'subcategory':str(self.property_dict[str(postdata['property_type'])]),
                            'city':'',
                            'district':'',
                            'name':postdata['post_title_th'],
                            'price':postdata['price_baht'],
                            'detail':'',
                            'checkdetail': postdata['post_description_th'],
                            'maplat':postdata['geo_latitude'],
                            'maplon': postdata['geo_longitude'],
                            'mapzoom':'',
                            'website':''
                        }
                        if postdata['listing_type']=='ขาย':
                            data['want'] = 'sale'
                        else :
                            data['want'] = 'forrent'


                        rget = httprequestObj.http_get('http://www.xn--12c1dpz9b3e.com/post-edit.php?id='+postdata['post_id'])
                        sou = soup(rget.text,'html5lib')
                        data['save'] = str(sou.find('input',attrs={'name':'save'})['value'])

                        data['contact'] = str(sou.find('input',attrs={'name':'contact'})['value'])
                        data['email'] = str(sou.find('input',attrs={'name':'email'})['value'])
                        data['detail'] = str(sou.find('textarea',attrs={'name':'detail'}).text)
                        data['hiddenname'] = str(sou.find('input',attrs={'name':'hiddenname'})['value'])
                        data['phone']=str(sou.find('input',attrs={'name':'phone'})['value'])
                        data['address']= str(sou.find('input',attrs={'name':'address'})['value'])
                        data['amphur']= str(sou.find('input',attrs={'name':'amphur'})['value'])

                        data['province']= str(sou.find('input',attrs={'name':'province'})['value'])
                        data['zipcode']= str(sou.find('input',attrs={'name':'zipcode'})['value'])

                        spn = sou.findAll('span',attrs= {'class':'notic'})

                        for sp in spn:

                            imgs = sp.findAll('a')
                            #print(imgs)
                            #print(sou.find('span'))

                            for img in imgs:
                                if img.has_attr('target'):
                                    continue
                                else :
                                    im_url = img['href']
                                    res =httprequestObj.http_get(im_url)
                                    #print(im_url)
                                    break

                        province = ''.join(map(str,str(postdata['addr_province']).split(' ')))
                        #print("#"+province)
                        abc = sou.find('select',attrs = {'name':'city'})
                        #print(abc)
                        for pq in abc.find_all('option'):
                            if(str(pq.text) in str(province) or str(province) in str(pq.text)):
                                data['city'] = str(pq['value'])
                                break

                        if(data['city']==''):
                            data['city'] = '1'

                        #print("##"+data['city'])
                        district = ''.join(map(str,str(postdata['addr_district']).split(' ')))
                        url_district = str('http://www.xn--12c1dpz9b3e.com/lib/district.php?province='+str(data['city']))

                        find_district = httprequestObj.http_get(url_district)
                        sou = soup(find_district.text,features = "html5lib")

                        abc = sou.find('select',attrs = {'name':'district'})
                        #print(abc)
                        cnt=0
                        for pq in abc.find_all('option'):
                            #print(pq.text)
                            if(str(pq.text) in str(district) or str(district) in str(pq.text)):
                                data['district'] = str(pq['value'])
                                cnt +=1
                                break

                        if cnt==0:
                            data['district'] = '1'





                        if 'post_images' in postdata and len(postdata['post_images']) > 0:
                            pass
                        else:
                            postdata['post_images'] = ['./imgtmp/default/white.jpg']


                        file = []
                        file_name = []
                        cnt = 1
                        for i in postdata['post_images']:
                            y=str(datetime.utcnow()).replace('-','').replace(":","").replace(".","").replace(" ","")+".jpg"
                            file.append(('file'+str(cnt),(y, open(i, "rb"), "image/jpeg")))
                            file.append(('photo'+str(cnt),(y, open(i, "rb"), "image/jpeg")))

                            file_name.append(y)
                            if cnt==6:
                                break
                            cnt+=1
                        #data['filename']=file_name
                        #print(data)

                        check_file = httprequestObj.http_post('http://www.xn--12c1dpz9b3e.com/lib/checkpost.php',data = data,headers = headers)
                        print(data)
                        data['detail'] = "<p> "+data['checkdetail']+" </p>"
                        upload_file = httprequestObj.http_post('http://www.xn--12c1dpz9b3e.com/post-edit.php?id='+post_id,data = data,files= file,headers = headers)
                        #print(upload_file.history)
                        #http://www.xn--12c1dpz9b3e.com/post-add.php?status=1&newid=99529&name=n%20nknn
                        url = str(upload_file.url)
                        #print(upload_file.history)
                        #print("###",url,"$$$")
                        urlList = url.split('?')

                        #print()
                        if len(urlList)<=1:
                            success = 'false'
                            detail = 'missing or duplicate entry'
                            post_url = ''
                            post_id= ''
                            break
                        else:
                            #print(urlList[1])
                            post_id = str(urlList[1].split('&')[1].split('=')[1])
                            #print(post_id)
                            post_url = 'http://www.xn--12c1dpz9b3e.com/view'+post_id+'/'+data['name']
                            success = "true"
                            detail = "Post Edited successfully"
                            #print(post_url)
                            break

                if flag == 0:
                    success = "false"
                    detail = "Post Not Found"
                    post_url=''
   
        else:
            success = "false"
            detail = "Can not log in"
            post_url=''
            
        end_time,usage_time=set_end_time(start_time)
        
        return {
            "websitename": "praeksa",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(usage_time),
            "post_url": post_url,
            "ds_id": postdata['ds_id'],
            "log_id":postdata['log_id'],
            "post_id": post_id,
            "detail": detail,
            "account_type": "null"
        }
