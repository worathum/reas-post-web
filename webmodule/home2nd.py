from .lib_httprequest import *
from bs4 import BeautifulSoup as soup
import os.path
import re
import json
import sys
from urllib.parse import unquote
from datetime import datetime
import random
import sys
import codecs
        

httprequestObj = lib_httprequest()
httprequestObj.timeout=50

def set_end_time(start_time):
    time_end = datetime.utcnow()
    time_usage = time_end - start_time
    return time_end, time_usage

class home2nd():

    name = 'home2nd'
    property_dict={
    '1': 'CD', 
    '2': 'HO',
    '3': 'TH', 
    '4': 'TH', 
    '5': 'SH', 
    '6': 'LA', 
    '7': 'AM', 
    '8':'CB', 
    '9': 'HOF', 
    '10': 'WA',
    '25': 'WA'
    }
    property_name = {
        '1': 'คอนโด', 
        '2': 'บ้าน',
        '3': 'ทาวน์เฮ้าส์', 
        '4': 'ทาวน์เฮ้าส์', 
        '5': 'ตึกแถว-อาคารพาณิชย์', 
        '6': 'ที่ดิน', 
        '7': 'อพาร์ทเม้นท์', 
        '8':'เชิงพาณิชย์', 
        '9': 'โฮมออฟฟิศ', 
        '10': 'โกดัง-โรงงาน',
        '25': 'โกดัง-โรงงาน'
    }
    def __init__(self):

        try:
            import configs
        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.primarydomain = 'https://www.home2nd.com/'
        self.debug = 0
        self.debugresdata = 0
        self.parser = 'html.parser'

    def register_user(self,userdata):
        start_time = datetime.utcnow()
        try:
            account = userdata['account_type']
        except:
            account = 'null'
        print("entry")

        r = httprequestObj.http_get("https://www.home2nd.com/",verify=False)
        sou = BeautifulSoup(r.text,'html5lib')
        
        url = sou.find('iframe',attrs = {'id':'homeidlogin'})['src']
        r = httprequestObj.http_get(url)
        page = BeautifulSoup(r.text,'html5lib')
        scrpt = page.findAll('script',attrs = {'type':'text/javascript'})
        csrf = scrpt[-2].text
        csrftoken = ''
        print(csrf)
    
        csrftoken = csrf.split('"')[3]

        string = r.text


        fname = str(userdata['name_th'])
        sname = str(userdata['surname_th'])
        data = {
            '_csrf': csrftoken,
            'firstname': fname,
            'lastname': sname,
            'email': userdata['user'],
            'password': userdata['pass'],
            'policy_checkbox': 'on'
        }
        reg_url = 'https://id.home.co.th/register'
        r = httprequestObj.http_post(reg_url,data = data)
        print(r)
        jr = json.loads(r.text)
        
        if 'success' not in jr or jr['success'] == False:
            success=False
            detail = 'Cannot Register'
        else :
            success=True
            detail = 'User Registered Successfully'
        
        end_time,usage_time=set_end_time(start_time)
        
        return {
            "websitename": "home2nd",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(usage_time),
            "ds_id": userdata['ds_id'],
            "detail": detail,
            "account_type": account
        }

    def test_login(self,userdata):
        
        login_url = "https://id.home.co.th/login"
        start_time = datetime.utcnow()
        res={'websitename':'home2nd', 'success':False, 'start_time': str(start_time), 'end_time': '0', 'usage_time': '0', 'detail': '','ds_id':userdata['ds_id']}
        try:
            account = userdata['account_type']
        except:
            account = 'null'
        print("entry")
        
        r = httprequestObj.http_get("https://www.home2nd.com/")
        sou = BeautifulSoup(r.text,'html5lib')

        url = sou.find('iframe',attrs = {'id':'homeidlogin'})['src']
        urls = url.split('&')
        r = httprequestObj.http_get(url)
        page = BeautifulSoup(r.text,'html5lib')
        scrpt = page.findAll('script',attrs = {'type':'text/javascript'})
        csrf = scrpt[-2].text
        csrftoken = ''
        print(csrf)
    
        csrftoken = csrf.split('"')[3]
        
        
        login_pload = {
            '_csrf': csrftoken,
            '_redirect_uri': urls[1].split('=')[-1],
            '_client_id': urls[2].split('=')[-1],
            '_state': urls[-2].split('=')[-1],
            '_nonce':'', 
            '_scope':'', 
            'username': userdata['user'],
            'password': userdata['pass']
        }
        #print(login_pload)
        r= httprequestObj.http_post(login_url, data=login_pload)
        
        
        if '<h1>Login complete</h1>' in r.text:
            res['success']= True
            res['detail'] = 'User Logged In Successfully'

        else :
            res['success']= False
            res['detail'] = 'Login Failed'
        endT,usage_time=set_end_time(start_time)
        res['end_time'] = str(endT)
        res['usage_time'] = str(usage_time)
        
        if sys._getframe().f_back.f_code.co_name == 'create_post' or sys._getframe().f_back.f_code.co_name == 'delete_post' or sys._getframe().f_back.f_code.co_name == 'search_post' or sys._getframe().f_back.f_code.co_name == 'edit_post':
            res['ret'] = r
        return res

    def create_post(self,postdata):
        start_time = datetime.utcnow()

        login = self.test_login(postdata)

        post_id = ''
        post_url = ''
        print(login)
        try:
            account = postdata['account_type']
        except:
            account = 'null'
        if (login["success"] == True):
            
            try:
                subdist = postdata['addr_sub_district']
                if subdist == None:
                    subdist = ""
            except:
                subdist = ""
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
                bathroom = postdata['bath_room']
                if bathroom == None:
                    bathroom = 0
            except:
                bathroom = 0
            try:
                bedroom = (postdata['bed_room'])
                if bedroom == None:
                    bedroom = 0
            except:
                bedroom = 0

            try:
                zipc = postdata['addr_postcode']
                if zipc == None:
                    zipc = '00'
            except:
                zipc = '00'

            
            
            r = login['ret']
            
            cookies = r.cookies
            headers = r.headers
            
            url = r.url
            fixurl = r.url
            datamenu = {
                'data_tab': 'search',
                'listingType': 'listing',
                'page': '1',
                'filterListing': '0',
                'filterProperty': '0',
                'sort': '2',
                'limit': '20',
                'txtSearch':''
            }
            
            
            
            
            pold = '0'
            token = url.split('&')[0].split('?')[1].split('=')[1]
            r = httprequestObj.http_get(url)
            cookies = r.cookies
            headers = r.headers
            newUrl = 'https://www.home2nd.com/homeid-login?'+url.split('&')[0].split('?')[1]+'&redirect_uri=https://www.home2nd.com/'
            print(newUrl)
            r = httprequestObj.http_get(newUrl,cookies = cookies,headers = headers)
            cookies = r.cookies
            headers = r.headers
            
            resp = httprequestObj.http_post('https://www.home2nd.com/profile/getmenu',data = datamenu)

            jr = resp.text[46:-2].replace('\n','<br>').replace('\r\n','<br>').replace('\/','').replace('\"','')
            sou = BeautifulSoup(jr,'html5lib')
            body = sou.find('tbody')
            pold = '0'
            if body != None:
                
                row = body.find('tr')
                if row != None:
                    pold = row['data-listing'].replace('\\','').replace('\"','')

            #print("******",pold)
            r = httprequestObj.http_get('https://www.home2nd.com/',cookies = cookies, headers = headers)
            
            cookies = r.cookies
            headers = r.headers

            sou = BeautifulSoup(r.text,'html5lib')
           
            url = sou.find('div',attrs = {'class':'item','data-value':'link-profile'})['data-url']
            agentId = url.split('/')[-1] 

            r1 = httprequestObj.http_get('https://www.home2nd.com/settings/tab?form=name',cookies = cookies, headers = headers)
            sou1 = BeautifulSoup(r1.text,'html5lib')

   
            firstnameEN = sou1.find('input',attrs = {'name':'info_firstnameEN'})['value']
            lastnameEN = sou1.find('input',attrs = {'name':'info_lastnameEN'})['value']
            firstnameTH = sou1.find('input',attrs = {'name':'info_firstnameTH'})['value']
            lastnameTH = sou1.find('input',attrs = {'name':'info_lastnameTH'})['value']
            
            nameurl = 'https://www.home2nd.com/settings/updateinfo'
            namedata = {
                'form': 'name',
                'agentid': agentId,
                'info_firstnameEN': firstnameEN,
                'info_lastnameEN': lastnameEN,
                'info_nicknameEN': postdata['name'],
                'info_firstnameTH': firstnameTH,
                'info_lastnameTH': lastnameTH,
                'info_nicknameTH': postdata['name']
            }
            rname = httprequestObj.http_post(nameurl,data = namedata)
            #print(rname.text)
            #add phone number
            phonedata = {
                'form': 'phone',
                'agentid': agentId,
                'info_phone_type[]': 'mobile',
                'info_phone_country[]': 'TH',
                'info_phone_number[]': postdata['mobile']
            }
            rphone = httprequestObj.http_post(nameurl,data = phonedata)
            #print(rphone.text)
            province_url = 'https://www.home2nd.com/submit-listing/geolocation'
            get_url = 'https://www.home2nd.com/submit-listing/step1'

            
            data = {
                'authenticity_token':'', 
                'listingType': '',
                'propertyType': self.property_dict[str(postdata['property_type'])],
                'number': '',
                'buildingName': postdata['post_title_th'],
                'buildingNameId': '', 
                'province': '',
                'provinceName':'', 
                'district': '',
                'districtName':'', 
                'subDistrict': '',
                'subDistrictName':'', 
                'zipcode': zipc,
                'houseNumber':'', 
                'streetTH': '', 
                'streetEN': '',
                'lat': postdata['geo_latitude'],
                'lng': postdata['geo_longitude'],
                'markerPolicy': '1'
            }
            lt = ''
            #Item type
            if postdata['listing_type'] == 'เช่า':
                data['listingType'] = 'FR'
                lt = 'เช่า'
            else:
                data['listingType'] = 'FS'
                lt = 'ขาย'

            #province
            province = ''.join(map(str,str(postdata['addr_province']).split(' ')))
            print("province")
            r3 = httprequestObj.http_get(get_url,cookies = cookies, headers = headers)
            
            print(r3.url)
            cookies = r3.cookies
            headers = r3.headers

            sou3 = BeautifulSoup(r3.text,'html5lib')
            abc = sou3.find('select',attrs = {'name':'province'})
            #print(abc)
            if(abc!=None):
                for pq in abc.find_all('option'):
                    
                    if (str(pq.text) in str(province)) or (str(province) in str(pq.text)):
                        print('andar')
                        data['province'] = str(pq['value'])
                        data['provinceName'] = pq.text.replace(' ','')
                        break
            if abc==None or  data['province']=='':
                data['province'] = '1'
                data['provinceName'] = 'กรุงเทพ'
            r4 = httprequestObj.http_post(province_url,data = {'type': 'province','id': data['province']})
            jr = json.loads(r4.text)
            #print(jr)
            sou4 = BeautifulSoup(str(jr['response']).replace('\"','"').replace('\/','/'),'html5lib')
            
            dist = ''.join(map(str,str(postdata['addr_district']).split(' ')))
                #print(province)
            
            for pq in sou4.find_all('option'):  
                if(str(pq.text) in str(dist) or str(dist) in str(pq.text)):
                    data['district'] = str(pq['value'])
                    data['districtName'] = pq.text.replace(' ','')
                    break
            
            r5 = httprequestObj.http_post(province_url,data = {'type': 'district','id': data['district']})
            #print(r5)
            jr = json.loads(r5.text)
            sou5 = BeautifulSoup(str(jr['response']).replace('\"','"').replace('\/','/'),'html5lib')
            
            sub_dist = ''.join(map(str,str(postdata['addr_sub_district']).split(' ')))
                #print(province)
            
            for pq in sou5.find_all('option'):
                if(str(pq.text) in str(dist) or str(dist) in str(pq.text)):
                    data['subDistrict'] = str(pq['value'])
                    break
            print(data)
            res = httprequestObj.http_post(get_url+'?',data = data)
            print(res.url)
            cookies = res.cookies
            headers = res.headers
            resp1 = httprequestObj.http_get('https://www.home2nd.com/submit-listing/step2',cookies = cookies, headers = headers)
            print(resp1.url)

        #step 2 
            step2data = {
                'authenticity_token':'', 
                'priceSale': '',
                'priceRent':'', 
                'commonFee':'', 
                'commonFeePer': '12',
                'contract': '', 
                'size': '',
                'rai': land_size_rai,
                'ngan': land_size_ngan,
                'wah': land_size_wa,
                'bed': bedroom,
                'bath': bathroom,
                'parking': '',
                'maidRoom':'', 
                'stories':'', 
                'furniture': 'NI',
                'frontDoor': 'NK',
                'descriptionTH': postdata['post_description_th'].replace('\r\n','<br>').replace('\n','<br>'),
                'descriptionEN': postdata['post_description_en'].replace('\r\n','<br>').replace('\n','<br>')
            }
            if postdata['listing_type'] == 'เช่า':
                step2data['priceRent'] = postdata['price_baht']
            else:
                step2data['priceSale'] = postdata['price_baht']
            r = httprequestObj.http_post('https://www.home2nd.com/submit-listing/step2?',data = step2data)
            cookies = r.cookies
            headers = r.headers
            print(r.url)
            resp = httprequestObj.http_get('https://www.home2nd.com/submit-listing/step3',cookies = cookies, headers = headers)
            
        # upload images
            print('upload Images')
            if 'post_images' in postdata and len(postdata['post_images']) > 0:
                pass
            else:
                postdata['post_images'] = ['./imgtmp/default/white.jpg']
            post_uri = 'https://in.hotjar.com/api/v2/client/sites/1378724/visit-data?sv=7'

            
            

            imgs = []

            for ind, i in enumerate(postdata['post_images']):
                file = {'file': (i, open(i, "rb"), "image/jpeg")}
                upload_file = httprequestObj.http_post('https://www.home2nd.com/uploadImg/upload_img',data = {},files = file)
                print(upload_file.text)
                jr = json.loads(upload_file.text)
                imgs.append(jr['imgName'])

            step3data = {
                'authenticity_token': '',
                'imageSort[]': imgs,
                'listing_video_show[]':'',
                'listing_video_path[]':'' 
            }
            r = httprequestObj.http_post('https://www.home2nd.com/submit-listing/step3?',data = step3data,cookies = cookies, headers = headers)
            cookies = r.cookies
            headers = r.headers
            print("##",r.url)
            resp = httprequestObj.http_get('https://www.home2nd.com/submit-listing/step4',cookies = cookies, headers = headers)
            
            
            
            #step 4
            r = httprequestObj.http_post('https://www.home2nd.com/submit-listing/step4?',data = {'assistantAgent': '1'})
            cookies = r.cookies
            headers = r.headers
            
            resp = httprequestObj.http_get('https://www.home2nd.com/submit-listing/complete',cookies = cookies, headers = headers)
            
            datamenu = {
                'data_tab': 'search',
                'listingType': 'listing',
                'page': '1',
                'filterListing': '0',
                'filterProperty': '0',
                'sort': '2',
                'limit': '20',
                'txtSearch':''
            }
            resp = httprequestObj.http_post('https://www.home2nd.com/profile/getmenu',data = datamenu)
            

            jr = resp.text[46:-2].replace('\n','<br>').replace('\r\n','<br>').replace('\/','/').replace('\"','"')
            sou = BeautifulSoup(jr,'html5lib')
            row = sou.find('tbody').find('tr')
            print(row)
            pnew = '0'
            if row != None:
                pnew = row['data-listing'].replace('\\','').replace('\"','')

            #print("******",pnew)
            
            if pnew == pold:
                success = False
                detail = "Post creation Failed"
            else:
                post_url = 'https://www.home2nd.com/ประกาศ/'+lt+'/'+self.property_name[str(postdata['property_type'])]+'/'+data['provinceName']+'/'+data['districtName']+'/'+pnew+'/1'
                success = True
                detail = "Post created successfully"
        else:
            success = False
            detail = "Can not log in"
            
        end_time,usage_time=set_end_time(start_time)
        
        return {
            "websitename": "home2nd",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(usage_time),
            "post_url": post_url,
            "ds_id": postdata['ds_id'],
            "post_id": pnew,
            "detail": detail,
            "account_type": account
        }


    def delete_post(self,postdata):
        start_time = datetime.utcnow()

        login = self.test_login(postdata)

        post_id = ''
        post_url = ''
        print(login)
        try:
            account = postdata['account_type']
        except:
            account = 'null'
        if (login["success"] == True):
            print("in")
            data = {
                'listingId[]': postdata['post_id'],
                'closedType': 'DU'
            }
            r = login['ret']
            url = r.url
            cookies = r.cookies
            headers = r.headers

            token = url.split('&')[0].split('?')[1].split('=')[1]
            r = httprequestObj.http_get(url)
            cookies = r.cookies
            headers = r.headers
            newUrl = 'https://www.home2nd.com/homeid-login?'+url.split('&')[0].split('?')[1]+'&redirect_uri=https://www.home2nd.com/'
            print(newUrl)
            r = httprequestObj.http_get(newUrl,cookies = cookies,headers = headers)
            cookies = r.cookies
            headers = r.headers
            
            
            r = httprequestObj.http_get('https://www.home2nd.com/',cookies = cookies, headers = headers)
            datamenu = {
                'data_tab': 'search',
                'listingType': 'listing',
                'page': '1',
                'filterListing': '0',
                'filterProperty': '0',
                'sort': '2',
                'limit': '100',
                'txtSearch':''
            }
            resp = httprequestObj.http_post('https://www.home2nd.com/profile/getmenu',data = datamenu)
            

            jr = resp.text[46:-2].replace('\n','<br>').replace('\r\n','<br>').replace('\/','/').replace('\"','"')
            sou = BeautifulSoup(jr,'html5lib')
            rows = sou.find('tbody').findAll('tr')
            flag = 0
            for row in rows:
                print(row)
                
                pnew = row['data-listing'].replace('\\','').replace('\"','')

                if pnew == postdata['post_id']:
                    
                    resp = httprequestObj.http_post('https://www.home2nd.com/listing/listingclosed', data = data)
                    success = True
                    detail = "Post Deleted successfully"
                    flag =1


            if flag == 0:
                success = False
                detail = "Post Not Found"
        else:
            success = False
            detail = "Can not log in"
            
        end_time,usage_time=set_end_time(start_time)

        return {
            "websitename": "home2nd",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(usage_time),
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": postdata['post_id'],
            "detail": detail
        }

    def search_post(self,postdata):
        ptype = {
            '1': '2', 
            '2': '1',
            '3': '3', 
            '4': '3', 
            '5': '12', 
            '6': '7', 
            '7': '5', 
            '8':'4', 
            '9': '16', 
            '10': '10',
            '25': '10'
        }
        start_time = datetime.utcnow()

        login = self.test_login(postdata)

        pnew = ''
        post_url = ''
        dateT = ''
        view = ''
        post_found=False
        success = False
        print(login)
        try:
            account = postdata['account_type']
        except:
            account = 'null'
        if (login["success"] == True):
            print("in")
            r = login['ret']
            url = r.url
            cookies = r.cookies
            headers = r.headers

            token = url.split('&')[0].split('?')[1].split('=')[1]
            r = httprequestObj.http_get(url)
            cookies = r.cookies
            headers = r.headers
            newUrl = 'https://www.home2nd.com/homeid-login?'+url.split('&')[0].split('?')[1]+'&redirect_uri=https://www.home2nd.com/'
            print(newUrl)
            r = httprequestObj.http_get(newUrl,cookies = cookies,headers = headers)
            cookies = r.cookies
            headers = r.headers
            
            
            r = httprequestObj.http_get('https://www.home2nd.com/',cookies = cookies, headers = headers)
            datamenu = {
                'data_tab': 'search',
                'listingType': 'listing',
                'page': '1',
                'filterListing': '0',
                'filterProperty':'0',
                'sort': '2',
                'limit': '100',
                'txtSearch':''
            }
            resp = httprequestObj.http_post('https://www.home2nd.com/profile/getmenu',data = datamenu)
            

            jr = resp.text[46:-2].replace('\/','/').replace('\"','"')
            sou = BeautifulSoup(jr,'html5lib')
            rows = sou.find('tbody').findAll('tr')
            flag = 0
            pnew = ''
            for row1 in rows:
               
                row = str(row1)
                print(row)
                pnew = row1['data-listing'].replace('\\','').replace('\"','')
                print(pnew)
                start = row.find('<a')+10
                if start == 9:
                    continue
                text = row
                i=start+1
                post_url = ''
                while True:
                    print(text[i])
                    if text[i]=='"':
                        break
                    post_url = post_url+text[i]
                    i+=1
                post_url = post_url[:-1]
                                
                new_str = codecs.unicode_escape_decode(post_url)[0]
                post_url = new_str.encode('utf-8', 'surrogatepass').decode('utf-8')
                print(post_url)
                r = httprequestObj.http_get(post_url)
                print(r)
                sou = BeautifulSoup(r.text,'html5lib')
                title = sou.find('h1',attrs = {'class':'feature-listing-title head_size_font'})
                if title == None:
                    continue
                title = title.text
                print(title,' : ',postdata['post_title_th'])
                if postdata['post_title_th'] in title:
                    dateT = sou.find('div', attrs = {'class':'m-t-md'}).find('p').text[24:].replace('\t','').replace('\n','')
                    success = True
                    post_found = True
                    detail = "Post Found"
                    flag =1
                    break            
            if flag==0:
                success = False
                post_found = False
                detail = "Post Not Found"
                post_url = ''
                pnew = ''

        end_time,usage_time=set_end_time(start_time)
        return {
            "websitename": "home2nd",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(end_time - start_time),
            "detail": detail,
            "account_type":account,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": pnew,
            "post_url": post_url,
            "post_modify_time": dateT,
            "post_create_time" : "",
            "post_view": view,
            "post_found": post_found
        }

    def edit_post(self,postdata):

        start_time = datetime.utcnow()

        login = self.test_login(postdata)

        pnew = ''
        post_url = ''
        post_id = postdata['post_id']
        
        success = False
        print(login)
        try:
            account = postdata['account_type']
        except:
            account = 'null'
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
            bathroom = postdata['bath_room']
            if bathroom == None:
                bathroom = 0
        except:
            bathroom = 0
        try:
            bedroom = (postdata['bed_room'])
            if bedroom == None:
                bedroom = 0
        except:
            bedroom = 0
        if (login["success"] == True):
            print("in")
            r = login['ret']
            url = r.url
            cookies = r.cookies
            headers = r.headers

            token = url.split('&')[0].split('?')[1].split('=')[1]
            r = httprequestObj.http_get(url)
            cookies = r.cookies
            headers = r.headers
            newUrl = 'https://www.home2nd.com/homeid-login?'+url.split('&')[0].split('?')[1]+'&redirect_uri=https://www.home2nd.com/'
            print(newUrl)
            r = httprequestObj.http_get(newUrl,cookies = cookies,headers = headers)
            cookies = r.cookies
            headers = r.headers
            
            
            r = httprequestObj.http_get('https://www.home2nd.com/',cookies = cookies, headers = headers)
            datamenu = {
                'data_tab': 'search',
                'listingType': 'listing',
                'page': '1',
                'filterListing': '0',
                'filterProperty':'0',
                'sort': '2',
                'limit': '100',
                'txtSearch':''
            }
            resp = httprequestObj.http_post('https://www.home2nd.com/profile/getmenu',data = datamenu)
            

            jr = resp.text[46:-2].replace('\/','/').replace('\"','"')
            sou = BeautifulSoup(jr,'html5lib')
            rows = sou.find('tbody').findAll('tr')
            flag = 0
            pnew = ''
            for row1 in rows:
               
                row = str(row1)
                print(row)
                pnew = row1['data-listing'].replace('\\','').replace('\"','')
                
                if post_id == pnew:
                    start = row.find('<a')+10
                    if start == 9:
                        continue
                    text = row
                    i=start+1
                    while True:
                        print(text[i])
                        if text[i]=='"':
                            break
                        post_url = post_url+text[i]
                        i+=1
                    post_url = post_url[:-1]
                                    
                    new_str = codecs.unicode_escape_decode(post_url)[0]
                    post_url = new_str.encode('utf-8', 'surrogatepass').decode('utf-8')
                    print(post_url)
                    data = {
                        'listingType': '',
                        'number':'', 
                        'streetTH':'', 
                        'streetEN':'', 
                        'priceSale': '',
                        'priceRent': '',
                        'commonFee':'', 
                        'commonFeePer': '12',
                        'lat': postdata['geo_latitude'],
                        'lng': postdata['geo_longitude'],
                        'contract':'', 
                        'size':'', 
                        'rai': land_size_rai,
                        'ngan': land_size_ngan, 
                        'wah': land_size_wa, 
                        'bed': bedroom,
                        'bath': bathroom,
                        'parking':'', 
                        'maidRoom': '',
                        'stories': '0',
                        'frontDoor': 'NK',
                        'furniture': 'NI',
                        'descriptionTH': postdata['post_description_th'].replace('\r\n','<br>').replace('\n','<br>'),
                        'descriptionEN': postdata['post_description_en'].replace('\r\n','<br>').replace('\n','<br>'),
                        'imageSort[]': [],
                        'linkVideo[]': '',
                        'linkVideoSort[]':''
                    }
                    if postdata['listing_type'] == 'เช่า':
                        data['priceRent'] = postdata['price_baht']
                        data['listingType'] = 'FR'
                    else:
                        data['priceSale'] = postdata['price_baht']
                        data['listingType'] = 'FS'
                    
                    url = 'https://www.home2nd.com/listing/edit/'+pnew
                    r = httprequestObj.http_get(url,cookies=cookies,headers = headers)
                    cookies = r.cookies
                    headers = r.headers
                    sou = BeautifulSoup(r.text,'html5lib')
                    imgs = sou.findAll('input',attrs = {'name':'imageSort[]'})
                    print(imgs)
                    delUrl = 'https://www.home2nd.com/listing/deleteimagedraft'
                    
                    
                    

                    if 'post_images' in postdata and len(postdata['post_images']) > 0:
                        pass
                    else:
                        postdata['post_images'] = ['./imgtmp/default/white.jpg']
                    imgsName = []
                    
                    for ind, i in enumerate(postdata['post_images']):
                        file = {'file': (i, open(i, "rb"), "image/jpeg")}
                        upload_file = httprequestObj.http_post('https://www.home2nd.com/uploadImg/uploadImg/'+post_id,data = {},files = file)
                        print(upload_file.text)
                        jr = json.loads(upload_file.text)
                        imgsName.append(jr['imgName'])
                    data['imageSort[]'] = imgsName

                    for img in imgs:
                        
                        del_data = {
                            'type': 'listing',
                            'imageName': img['value'],
                            'listingId': pnew
                        }
                        resp = httprequestObj.http_post(delUrl,data = del_data)
                        print(resp.text)
                    
                    r = httprequestObj.http_post(url, data = data)
                    success = True
                    detail = 'Post Edited Successfully'
                    flag = 1
                    break
            
            if flag ==0 :
                success = False
                detail = 'Post Not Found'

        else :
            success = False
            detail = 'Cannot Log In'
                      
        end_time,usage_time=set_end_time(start_time)
        
        return {
            "websitename": "home2nd",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(usage_time),
            "post_url": post_url,
            "ds_id": postdata['ds_id'],
            "post_id": pnew,
            "detail": detail,
            "log_id":postdata['log_id'],
            "account_type": account
        }

    def boost_post(self,postdata):
        strt = (datetime.utcnow())
        end_time,usage_time = set_end_time(strt)
        return {
            "websitename": "home2nd",
            "success": True,
            "start_time": str(strt),
            "end_time": str(end_time),
            "usage_time": str(usage_time),    
            "ds_id": postdata['ds_id'],
            "post_id": postdata['post_id'],
            "log_id":postdata['log_id'],
            "detail": "No boost Post option",
            "account_type": "null"
        }