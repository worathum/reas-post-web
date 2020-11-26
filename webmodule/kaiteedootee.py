import requests, re, random
from bs4 import BeautifulSoup
import json, datetime
from selenium import webdriver
from .lib_httprequest import *
from .lib_captcha import  *
httprequestObj = lib_httprequest()
import datetime
import time,math

class kaiteedootee:

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

    def register_user(self, data):
        start_time = datetime.datetime.utcnow()

        success = ''
        detail = ''
        postdata = {
        	'email': data['user'],
			'name': data['name_th'],
			'tel': data['tel'],
			'password': data['pass']
        }
        url = 'http://kaiteedootee.com/Admin/NiSK.php?ACT=Add_Users_Index'
        headers = {
        	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        }
        req = httprequestObj.http_post(url,data=postdata,headers=headers)
        txt = req.text
        if txt.find('มีอีเมลนี้ในระบบแล้ว')!=-1:
            success = 'false'
            detail = 'Email already exists'
        else:
            success = 'true'
            detail = 'Successfully registered'



        end_time = datetime.datetime.utcnow()
        result = {'websitename':'kaiteedootee',
         'success':success,
         'start_time':str(start_time),
         'end_time':str(end_time),
         'usage_time':str(end_time - start_time),
         'detail':detail,
         'ds_id':data['ds_id']}
        return result

    def test_login(self, data):
        start_time = datetime.datetime.utcnow()

        success = ''
        detail = ''
        postdata = {
        	'email':data['user'],
        	'password':data['pass']
        }

        url = 'http://kaiteedootee.com/NiSK.php?ACT=Member_login'
        headers = {
        	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        }
        req = httprequestObj.http_post(url,data=postdata,headers=headers)
        txt = req.text
        if txt.find('Username หรือ Password ไม่ถูกต้อง') == -1:
            success = 'true'
            detail = 'Login Successful'
        else:
            success = 'false'
            detail = 'Invalid credentials'

        end_time = datetime.datetime.utcnow()
        result = {'websitename':'kaiteedootee',
         'success':success,
         'start_time':str(start_time),
         'end_time':str(end_time),
         'usage_time':str(end_time - start_time),
         'ds_id':data['ds_id'],
         'detail':detail}
        return result

    def create_post(self, data):
        start_time = datetime.datetime.utcnow()
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        }
        result = self.test_login(data)
        success = result['success']
        detail = result['detail']
        post_url = ''
        post_id = ''
        if success == 'true':

            postdata = {}
            postdata['data[lat_lng]'] = ''
            postdata['data[post_type_code]'] = 'R'
            if data['listing_type'] == 'ขาย':
                postdata['data[post_type_code]'] = 'S'
            ids = {'คอนโด': '1',
                   'บ้านเดี่ยว': '2',
                   'บ้านแฝด': '3',
                   'ทาวน์เฮ้าส์': '4',
                   'ตึกแถว-อาคารพาณิชย์': '5',
                   'ที่ดิน': '6',
                   'อพาร์ทเมนท์': '7',
                   'โรงแรม': '8',
                   'ออฟฟิศสำนักงาน': '9',
                   'โกดัง-โรงงาน': '10',
                   'โรงงาน': '25'}
            property_tp = {'1': 'C',
                           '2': 'H',
                           '3': 'H',
                           '4': 'H',
                           '5': 'H',
                           '6': 'L',
                           '7': 'H',
                           '8': 'H',
                           '9': 'H',
                           '10': 'H',
                           '25': 'H'}
            if str(data['property_type']) in property_tp:
                postdata['data[property_type_code]'] = property_tp[str(data['property_type'])]
            else:
                postdata['data[property_type_code]'] = property_tp[ids[str(data['property_type'])]]

            postdata['data[geo_id]'] = ''
            postdata['data[province_id]'] = ''
            postdata['data[amphur_id]'] = ''
            postdata['data[district_id]'] = ''

            temp_data = {
                'geo':''
            }
            url = 'http://kaiteedootee.com/NiSK.php?ACT=SearchGeo'
            req = httprequestObj.http_post(url,data=temp_data,headers=headers)
            txt = str(req.text)
            #print('here',txt)
            ind = 13
            provinces_list = []
            while ind<len(txt):
                if txt[ind] == ':':
                    ind+=2
                    prov = ''
                    while txt[ind] != '"':
                        prov+=txt[ind]
                        ind+=1
                    provinces_list.append(prov)
                ind+=1


            for prov in provinces_list:
                if prov.find(data['addr_province'])!=-1:
                    postdata['data[province_id]'] = prov
                    break
            if postdata['data[province_id]'] == '':
                postdata['data[province_id]'] = provinces_list[0]

            postdata['data[province_id]'] = (postdata['data[province_id]']).encode().decode("unicode-escape")
            #print((postdata['data[province_id]']).decode('unicode_escape'))
            #print(translator.translate(postdata['data[province_id]'], dest='th'))

            temp_data = {
                'province': postdata['data[province_id]']
            }
            url = 'http://kaiteedootee.com/NiSK.php?ACT=SearchProvince'
            req = httprequestObj.http_post(url, data=temp_data, headers=headers)
            txt = str(req.text)
            #print(txt)
            ind = 11
            districts_list = []
            while ind < len(txt):
                if txt[ind] == ':':
                    ind += 2
                    prov = ''
                    while txt[ind] != '"':
                        prov += txt[ind]
                        ind += 1
                    districts_list.append(prov)
                ind += 1

            for prov in districts_list:
                if prov.find(data['addr_district']) != -1:
                    postdata['data[amphur_id]'] = prov
                    break
            if postdata['data[amphur_id]'] == '':
                postdata['data[amphur_id]'] = districts_list[0]

            postdata['data[amphur_id]'] = (postdata['data[amphur_id]']).encode().decode("unicode-escape")
            #print(districts_list)
            temp_data = {
                'amphur': postdata['data[amphur_id]']
            }
            url = 'http://kaiteedootee.com/NiSK.php?ACT=SearchAmphur'
            req = httprequestObj.http_post(url, data=temp_data, headers=headers)
            txt = str(req.text)
            ind = 9
            subdistricts_list = []
            while ind < len(txt):
                if txt[ind] == '"':
                    ind += 1
                    prov = ''
                    while txt[ind] != '"':
                        prov += txt[ind]
                        ind += 1
                    subdistricts_list.append(prov)
                ind += 1

            for prov in subdistricts_list:
                if prov.find(data['addr_sub_district']) != -1:
                    postdata['data[district_id]'] = prov
                    break
            if postdata['data[district_id]'] == '':
                postdata['data[district_id]'] = subdistricts_list[0]
            #print(subdistricts_list)
            postdata['data[district_id]'] = (postdata['data[district_id]']).encode().decode("unicode-escape")


            postdata['data[subject]'] = str(data['post_title_th'])
            postdata['data[price]'] = str(data['price_baht'])
            postdata['data[description]'] = str(data['post_description_th'])

            # images
            if 'post_images' in data and len(data['post_images']) > 0:
                pass
            else:
                data['post_images'] = ['./imgtmp/default/white.jpg']

            file = []
            temp = 1

            if len(data['post_images']) <= 3:
                for i in data['post_images']:
                    y = str(random.randint(0, 100000000000000000)) + ".jpg"
                    # ##print(y)
                    if temp == 1:
                        file.append((str('files[]'), (y, open(i, "rb"), "image/jpg")))
                    else:
                        file.append((str('files_more[]'), (y, open(i, "rb"), "image/jpg")))
                    temp = temp + 1
                y = str(random.randint(0, 100000000000000000)) + ".jpg"
                file.append((str('files_more[]'), (y, open(data['post_images'][0], "rb"), "image/jpg")))

            else:
                for i in data['post_images'][:3]:
                    y = str(random.randint(0, 100000000000000000)) + ".jpg"
                    # ##print(y)
                    if temp == 1:
                        file.append((str('files[]'), (y, open(i, "rb"), "image/jpg")))
                    else:
                        file.append((str('files_more[]'), (y, open(i, "rb"), "image/jpg")))
                    temp = temp + 1
                y = str(random.randint(0, 100000000000000000)) + ".jpg"
                file.append((str('files_more[]'), (y, open(data['post_images'][0], "rb"), "image/jpg")))

            url = 'http://kaiteedootee.com/post.php'
            req = httprequestObj.http_get(url,headers=headers)
            soup = BeautifulSoup(req.text,'html.parser')
            postdata['data[poster_name]'] = soup.find('input',{'name':'data[poster_name]'})['value']
            postdata['data[poster_telephone]'] = soup.find('input',{'name':'data[poster_telephone]'})['value']
            postdata['data[poster_email]'] = soup.find('input',{'name':'data[poster_email]'})['value']
            postdata['data[poster_lineid]'] = data['line']
            postdata['data[password]'] = soup.find('input',{'name':'data[password]'})['value']

            url = 'http://kaiteedootee.com/NiSK.php?ACT=PostKai'

            req = httprequestObj.http_post(url,data=postdata,files=file,headers=headers)
            url = 'http://kaiteedootee.com/index.php'
            req = httprequestObj.http_get(url,headers=headers)
            soup = BeautifulSoup(req.text,'html.parser')
            div = soup.findAll('div',{'class':'container'})[2]
            latests = div.findAll('div',{'class':'col-md-6'})
            #print(len(latests))
            #print(data['post_title_th'])
            for latest in latests:
                a = str(latest.find('a').text)
                #print(a)
                if str(a).strip() == str(data['post_title_th']).strip():
                    #print('in')
                    post_url = 'http://kaiteedootee.com/'+str(latest.find('a')['href'])
                    url = str(latest.find('a')['href'])
                    ind = url.find('ID=')+3
                    while ind<len(url):
                        post_id+=url[ind]
                        ind+=1
                    break
            if post_url == '':
                success = 'false'
                detail = 'Something went wrong'
            else:
                success = 'true'
                detail = 'Successfully posted'



        end_time = datetime.datetime.utcnow()
        result = {'success': success,
                  'usage_time': str(end_time - start_time),
                  'start_time': str(start_time),
                  'end_time': str(end_time),
                  'post_url': post_url,
                  'post_id': post_id,
                  'account_type': 'null',
                  'ds_id': data['ds_id'],
                  'detail': detail,
                  'websitename': 'kaiteedootee'}
        return result

    def delete_post(self, data):
        ##print('in')
        test_login = self.test_login(data)
        success = test_login["success"]
        start_time = datetime.datetime.utcnow()
        end_time = datetime.datetime.utcnow()
        post_id = str(data["post_id"])
        detail = test_login["detail"]

        if success == "true":
            url = 'http://kaiteedootee.com/profile.php'
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
            }
            req = httprequestObj.http_get(url,headers=headers)
            soup = BeautifulSoup(req.text,'html.parser')
            valid_ids = []
            delete_ids = []
            posts = soup.find('div',{'id':'my_post'}).findAll('div',{'class':'col-xs-12 padding-0'})
            for post in posts:
                id = str(post.find('a',{'class':'clk-delete'})['data-post_id'])
                delete_ids.append(str(id))
                url = str(post.find('a')['href'])
                id = ''
                ind = url.find('ID=') + 3
                while ind < len(url):
                    id += url[ind]
                    ind += 1
                valid_ids.append(id)
            #print(valid_ids)
            #print(delete_ids)

            if str(post_id) in valid_ids:
                del_id = ''
                for i in range(len(valid_ids)):
                    if valid_ids[i] == str(post_id):
                        del_id = delete_ids[i]
                        break
                success = 'true'
                url = 'http://kaiteedootee.com/NiSK.php?ACT=Delete_Post&PID='+str(del_id)
                postdata = {
                    'txtPassword':data['pass']
                }
                #print(data['pass'])
                req = httprequestObj.http_post(url,data=postdata,headers=headers)
                detail = 'Post deleted'
            else:
                success = 'false'
                detail = 'Post not found'


        end_time = datetime.datetime.utcnow()
        result = {
            "success": success,
            "usage_time": str(end_time - start_time),
            "start_time": str(start_time),
            "end_time": str(end_time),
            "log_id": data['log_id'],
            'ds_id': data['ds_id'],
            "post_id": data['post_id'],
            "detail": detail,
            "websitename": "kaiteedootee"
        }
        return result


    def search_post(self, data):
        ##print('in')
        test_login = self.test_login(data)
        success = test_login["success"]
        start_time = datetime.datetime.utcnow()
        end_time = datetime.datetime.utcnow()
        post_title = str(data["post_title_th"])
        detail = test_login["detail"]
        post_id = ''
        post_url = ''
        post_found = ''
        post_create_time = ''
        post_view = ''

        if success == "true":
            url = 'http://kaiteedootee.com/profile.php'
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
            }
            req = httprequestObj.http_get(url, headers=headers)
            soup = BeautifulSoup(req.text, 'html.parser')
            valid_ids = []
            valid_titles = []
            create = []
            views = []
            posts = soup.find('div', {'id': 'my_post'}).findAll('div', {'class': 'col-xs-12 padding-0'})
            for post in posts:

                url = str(post.find('a')['href'])
                id = ''
                ind = url.find('ID=') + 3
                while ind < len(url):
                    id += url[ind]
                    ind += 1
                valid_ids.append(id)
                title = str(post.find('a').text)
                valid_titles.append(title.strip())
                fonts = post.find('div',{'class':'col-xs-12 col-sm-8 viewcount'})
                #print(fonts)
                create.append((str(fonts.text)[:-18]).strip())
                views.append((str(fonts.text)[-16:]).strip())

            #print(create)
            #print(views)

            if str(post_title).strip() in valid_titles:

                for i in range(len(valid_titles)):
                    if str(valid_titles[i]) == str(post_title):
                        post_id = valid_ids[i]
                        post_create_time = create[i]
                        post_view = views[i]
                        post_url = 'http://kaiteedootee.com/blog.php?ID='+str(post_id)
                        break
                post_found = 'true'
                detail = 'Post found'
            else:
                post_found = 'false'
                detail = 'Post not found'




        end_time = datetime.datetime.utcnow()
        result = {
            "success": "true",
            "usage_time": str(end_time - start_time),
            "start_time": str(start_time),
            "end_time": str(end_time),
            "detail": detail,
            'ds_id': data['ds_id'],
            "log_id": data['log_id'],
            "post_found": post_found,
            "post_id": post_id,
            'post_url': post_url,
            "post_create_time": post_create_time,
            "post_modify_time": '',
            "post_view": post_view,
            'websitename': 'kaiteedootee'
        }
        return result

    def edit_post(self, data):
        start_time = datetime.datetime.utcnow()
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        }
        result = self.test_login(data)
        success = result['success']
        detail = result['detail']
        post_url = ''
        post_id = str(data['post_id'])
        if success == 'true':

            url = 'http://kaiteedootee.com/profile.php'
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
            }
            req = httprequestObj.http_get(url, headers=headers)
            soup = BeautifulSoup(req.text, 'html.parser')
            valid_ids = []
            edit_ids = []
            posts = soup.find('div', {'id': 'my_post'}).findAll('div', {'class': 'col-xs-12 padding-0'})
            for post in posts:
                id = str(post.find('a', {'class': 'clk-delete'})['data-post_id'])
                edit_ids.append(str(id))
                url = str(post.find('a')['href'])
                id = ''
                ind = url.find('ID=') + 3
                while ind < len(url):
                    id += url[ind]
                    ind += 1
                valid_ids.append(id)

            if post_id in valid_ids:
                edit_id = ''
                for i in range(len(valid_ids)):
                    if valid_ids[i] == post_id:
                        edit_id = edit_ids[i]
                        break
                postdata = {}
                postdata['data[lat_lng]'] = ''
                postdata['data[post_type_code]'] = 'R'
                if data['listing_type'] == 'ขาย':
                    postdata['data[post_type_code]'] = 'S'
                ids = {'คอนโด': '1',
                       'บ้านเดี่ยว': '2',
                       'บ้านแฝด': '3',
                       'ทาวน์เฮ้าส์': '4',
                       'ตึกแถว-อาคารพาณิชย์': '5',
                       'ที่ดิน': '6',
                       'อพาร์ทเมนท์': '7',
                       'โรงแรม': '8',
                       'ออฟฟิศสำนักงาน': '9',
                       'โกดัง-โรงงาน': '10',
                       'โรงงาน': '25'}
                property_tp = {'1': 'C',
                               '2': 'H',
                               '3': 'H',
                               '4': 'H',
                               '5': 'H',
                               '6': 'L',
                               '7': 'H',
                               '8': 'H',
                               '9': 'H',
                               '10': 'H',
                               '25': 'H'}
                if str(data['property_type']) in property_tp:
                    postdata['data[property_type_code]'] = property_tp[str(data['property_type'])]
                else:
                    postdata['data[property_type_code]'] = property_tp[ids[str(data['property_type'])]]

                postdata['data[geo_id]'] = ''
                postdata['data[province_id]'] = ''
                postdata['data[amphur_id]'] = ''
                postdata['data[district_id]'] = ''

                temp_data = {
                    'geo':''
                }
                url = 'http://kaiteedootee.com/NiSK.php?ACT=SearchGeo'
                req = httprequestObj.http_post(url,data=temp_data,headers=headers)
                txt = str(req.text)
                #print('here',txt)
                ind = 13
                provinces_list = []
                while ind<len(txt):
                    if txt[ind] == ':':
                        ind+=2
                        prov = ''
                        while txt[ind] != '"':
                            prov+=txt[ind]
                            ind+=1
                        provinces_list.append(prov)
                    ind+=1


                for prov in provinces_list:
                    if prov.find(data['addr_province'])!=-1:
                        postdata['data[province_id]'] = prov
                        break
                if postdata['data[province_id]'] == '':
                    postdata['data[province_id]'] = provinces_list[0]

                postdata['data[province_id]'] = (postdata['data[province_id]']).encode().decode("unicode-escape")
                #print((postdata['data[province_id]']).decode('unicode_escape'))
                #print(translator.translate(postdata['data[province_id]'], dest='th'))

                temp_data = {
                    'province': postdata['data[province_id]']
                }
                url = 'http://kaiteedootee.com/NiSK.php?ACT=SearchProvince'
                req = httprequestObj.http_post(url, data=temp_data, headers=headers)
                txt = str(req.text)
                #print(txt)
                ind = 11
                districts_list = []
                while ind < len(txt):
                    if txt[ind] == ':':
                        ind += 2
                        prov = ''
                        while txt[ind] != '"':
                            prov += txt[ind]
                            ind += 1
                        districts_list.append(prov)
                    ind += 1

                for prov in districts_list:
                    if prov.find(data['addr_district']) != -1:
                        postdata['data[amphur_id]'] = prov
                        break
                if postdata['data[amphur_id]'] == '':
                    postdata['data[amphur_id]'] = districts_list[0]

                postdata['data[amphur_id]'] = (postdata['data[amphur_id]']).encode().decode("unicode-escape")
                #print(districts_list)
                temp_data = {
                    'amphur': postdata['data[amphur_id]']
                }
                url = 'http://kaiteedootee.com/NiSK.php?ACT=SearchAmphur'
                req = httprequestObj.http_post(url, data=temp_data, headers=headers)
                txt = str(req.text)
                ind = 9
                subdistricts_list = []
                while ind < len(txt):
                    if txt[ind] == '"':
                        ind += 1
                        prov = ''
                        while txt[ind] != '"':
                            prov += txt[ind]
                            ind += 1
                        subdistricts_list.append(prov)
                    ind += 1

                for prov in subdistricts_list:
                    if prov.find(data['addr_sub_district']) != -1:
                        postdata['data[district_id]'] = prov
                        break
                if postdata['data[district_id]'] == '':
                    postdata['data[district_id]'] = subdistricts_list[0]
                #print(subdistricts_list)
                postdata['data[district_id]'] = (postdata['data[district_id]']).encode().decode("unicode-escape")


                postdata['data[subject]'] = str(data['post_title_th'])
                postdata['data[price]'] = str(data['price_baht'])
                postdata['data[description]'] = str(data['post_description_th'])

                # images
                if 'post_images' in data and len(data['post_images']) > 0:
                    pass
                else:
                    data['post_images'] = ['./imgtmp/default/white.jpg']

                file = []
                temp = 1

                if len(data['post_images']) <= 3:
                    for i in data['post_images']:
                        y = str(random.randint(0, 100000000000000000)) + ".jpg"
                        # ##print(y)
                        if temp == 1:
                            file.append((str('files[]'), (y, open(i, "rb"), "image/jpg")))
                        else:
                            file.append((str('files_more[]'), (y, open(i, "rb"), "image/jpg")))
                        temp = temp + 1
                    y = str(random.randint(0, 100000000000000000)) + ".jpg"
                    file.append((str('files_more[]'), (y, open(data['post_images'][0], "rb"), "image/jpg")))

                else:
                    for i in data['post_images'][:3]:
                        y = str(random.randint(0, 100000000000000000)) + ".jpg"
                        # ##print(y)
                        if temp == 1:
                            file.append((str('files[]'), (y, open(i, "rb"), "image/jpg")))
                        else:
                            file.append((str('files_more[]'), (y, open(i, "rb"), "image/jpg")))
                        temp = temp + 1
                    y = str(random.randint(0, 100000000000000000)) + ".jpg"
                    file.append((str('files_more[]'), (y, open(data['post_images'][0], "rb"), "image/jpg")))


                url = 'http://kaiteedootee.com/NiSK.php?ACT=Edit_post_data&PID='+str(post_id)

                req = httprequestObj.http_post(url,data=postdata,files=file,headers=headers)
                post_url = 'http://kaiteedootee.com/blog.php?ID='+str(post_id)
                success = 'true'
                detail = 'Successfully edited'
            else:
                success = 'false'
                detail = 'Post not found'




        end_time = datetime.datetime.utcnow()
        result = {'success': success,
                  'usage_time': str(end_time - start_time),
                  'start_time': str(start_time),
                  'end_time': str(end_time),
                  'post_url': post_url,
                  'post_id': post_id,
                  'account_type': 'null',
                  'log_id':data['log_id'],
                  'ds_id': data['ds_id'],
                  'detail': detail,
                  'websitename': 'kaiteedootee'}
        return result

    def boost_post(self, data):
        start_time = datetime.datetime.utcnow()
        # #print('start')
        post_id = str(data['post_id'])
        log_id = str(data['log_id'])
        result = self.test_login(data)
        success = result['success']
        detail = result['detail']

        if success == 'true':
            url = 'http://kaiteedootee.com/profile.php'
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
            }
            req = httprequestObj.http_get(url, headers=headers)
            soup = BeautifulSoup(req.text, 'html.parser')
            valid_ids = []
            edit_ids = []
            posts = soup.find('div', {'id': 'my_post'}).findAll('div', {'class': 'col-xs-12 padding-0'})
            for post in posts:
                id = str(post.find('a', {'class': 'clk-delete'})['data-post_id'])
                edit_ids.append(str(id))
                url = str(post.find('a')['href'])
                id = ''
                ind = url.find('ID=') + 3
                while ind < len(url):
                    id += url[ind]
                    ind += 1
                valid_ids.append(id)

            if post_id in valid_ids:
                success = 'true'
                detail = 'Edited and saved'
            else:
                success = 'false'
                detail = 'Post not found'

        end_time = datetime.datetime.utcnow()
        result = {
            "success": "true",
            "usage_time": str(end_time - start_time),
            "start_time": str(start_time),
            "end_time": str(end_time),
            "detail": detail,
            'ds_id': data['ds_id'],
            "log_id": log_id,
            "post_id": post_id,
            'websitename': 'kaiteedootee'
        }
        # https://ilovecondo.net/new-post/topicid/910653/trk/78
        return result