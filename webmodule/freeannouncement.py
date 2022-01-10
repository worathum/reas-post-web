import requests,re,random
from bs4 import BeautifulSoup
import json
import datetime
from .lib_httprequest import *


class freeannouncement():

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
        self.httprequestObj = lib_httprequest()

    def logout_user(self):
        url = 'http://www.xn--12c5cnoc2a8cr4a.com/logout.php'
        self.httprequestObj.http_get(url)

    def register_user(self,data):
        self.logout_user()
        start_time = datetime.datetime.utcnow()
        headers = {
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        }
        req = self.httprequestObj.http_get_with_headers('http://www.xn--12c5cnoc2a8cr4a.com/register.php',headers = headers)
        soup = BeautifulSoup(req.text,'html.parser')
        save = soup.find('input',{'name':'save'})['value']
        ##print(save)
        email = data['user']
        password = data['pass']
        repassword = data['pass']
        name = data['name_th'] + ' ' + data['surname_th']
        phone = data['tel']
        address = data['tel']
        province = '2'
        amphur = '22'
        zipcode = '10400'
        title = ''
        description = ''
        keyword = ''
        website = ''
        soup = BeautifulSoup(req.text, 'html.parser')
        hiddenanswer = soup.find('input', {'name': 'hiddenanswer'})['value']
        ##print(hiddenanswer)
        answer = hiddenanswer
        accept = '1'

        postdata = {
            'save':save,
            'email':email,
            'password':password,
            'repassword':repassword,
            'name':name,
            'phone':phone,
            'address':address,
            'province':province,
            'amphur':amphur,
            'zipcode':zipcode,
            'title':title,
            'description':description,
            'keyword':keyword,
            'website':website,
            'answer':answer,
            'hiddenanswer':hiddenanswer,
            'accept':accept
        }


        success = 'true'
        detail = ''

        # validation

        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*$'
        f1 = True

        # Check validity of an email ID
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*$'
        if (re.search(regex, postdata["email"])):
            f1 = True
        else:
            f1 = False

        if len(password)<=5:
            success = 'false'
            detail = 'Password length should be greater than 5'
        elif f1 == False:
            success = 'false'
            detail = 'Invalid email'



        if success == 'true':
            url = 'http://www.xn--12c5cnoc2a8cr4a.com/lib/checkuser.php'
            req = self.httprequestObj.http_post(url,data=postdata,headers=headers)
            ##print(req.text)
            if str(req.text) == '-1':
                success = 'false'
                detail = 'user already exist'
            else:
                url = 'http://www.xn--12c5cnoc2a8cr4a.com/register.php'
                req = self.httprequestObj.http_post(url,data=postdata,headers=headers)
                success = 'true'
                detail = 'User registered'
        end_time = datetime.datetime.utcnow()
        result = {
            'websitename': 'freeannouncement',
            'success': success,
            'start_time': str(start_time),
            'end_time': str(end_time),
            'usage_time': str(end_time - start_time),
            'ds_id':data['ds_id'],
            'detail': detail
        }
        return result

    def test_login(self, data):
        start_time = datetime.datetime.utcnow()
        end_time = datetime.datetime.utcnow()
        return {
            'websitename': 'freeannouncement',
            'success': "false",
            'start_time': str(start_time),
            'end_time': str(end_time),
            'usage_time': str(end_time - start_time),
            'ds_id': data['ds_id'],
            'detail': "Can't Login due to website problem. Please try again later."
        }
        self.logout_user()
        start_time = datetime.datetime.utcnow()
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        }
        req = self.httprequestObj.http_get_with_headers('http://www.xn--12c5cnoc2a8cr4a.com/member.php', headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        try:
            save = soup.find('input', {'name': 'save'})['value']
        except:
            end_time = datetime.datetime.utcnow()
            return {
            'websitename': 'freeannouncement',
            'success': "false",
            'start_time': str(start_time),
            'end_time': str(end_time),
            'usage_time': str(end_time - start_time),
            'ds_id': data['ds_id'],
            'detail': "Can't Login due to website problem. Please try again later."
        }

        # #print(save)
        email = data['user']
        password = data['pass']
        postdata = {
            'save':save,
            'email':email,
            'password':password
        }
        url = 'http://www.xn--12c5cnoc2a8cr4a.com/member.php'
        req = self.httprequestObj.http_post(url,data=postdata,headers=headers)

        ind = str(req.text).find('ขออภัยค่ะ ไม่สามารถเข้าระบบได้ในขณะนี้ กรุณาติดต่อผู้ดูแลเว็บไซต์ค่ะ')
        success = ''
        detail = ''

        if ind != -1:
            success = 'false'
            detail = 'Invalid Credentials'

        else:
            success = 'true'
            detail = 'Login Successful'

        end_time = datetime.datetime.utcnow()
        # creating the final result object
        result = {
            'websitename': 'freeannouncement',
            'success': success,
            'start_time': str(start_time),
            'end_time': str(end_time),
            'usage_time': str(end_time - start_time),
            'ds_id': data['ds_id'],
            'detail': detail
        }

        return result

    def create_post(self, data):

        start_time = datetime.datetime.utcnow()

        # login
        result = self.test_login(data)
        success = result['success']
        detail = result['detail']
        ##print(success, detail)
        post_url = ''
        post_id = ''
        if success == 'true':

            postdata1 = {}

            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
            }
            req = self.httprequestObj.http_get_with_headers('http://www.xn--12c5cnoc2a8cr4a.com/post-add.php', headers=headers)
            soup = BeautifulSoup(req.text, 'html.parser')
            ##print('here1',success)
            postdata1['save'] = soup.find('input', {'name': 'save'})['value']
            postdata1['type'] = 'guest'
            if data['listing_type'] == 'ขาย':
                postdata1['want'] = 'sale'
            else:
                postdata1['want'] = 'forrent'

            postdata1['status'] = '2hand'
            postdata1['duration'] = '-1'
            postdata1['category'] = '1009'
            proid = {
                '1':'1149',
                '2':'1147',
                '3':'1147',
                '4':'1154',
                '5':'1153',
                '6':'1148',
                '7':'1157',
                '8':'1156',
                '9':'1151',
                '10':'1155',
                '25':'1155'
            }
            ##print('here2',success)
            ##print(data['property_type'])
            postdata1['subcategory'] = proid[str(data['property_type'])]
            provinces = []
            values = []
            ##print('here22')
            select = soup.find('select',{'name':'city'})
            ##print(select)
            options = select.findAll('option')
            count = 0
            for opt in options:
                if count>0:
                    provinces.append(opt.text)
                    values.append(opt['value'])
                count+=1
            postdata1['city'] = ''
            for i in range(len(provinces)):
                if provinces[i] == data['addr_province']:
                    postdata1['city'] = values[i]
                    break
            if postdata1['city'] == '':
                for i in range(len(provinces)):
                    if provinces[i].find(data['addr_province'])!=-1:
                        postdata1['city'] = values[i]
                        break
            if postdata1['city'] == '':
                postdata1['city'] = values[0]

            ##print('here3',success)
            url = 'http://www.xn--12c5cnoc2a8cr4a.com/lib/district.php?province='+postdata1['city']
            req = self.httprequestObj.http_get_with_headers(url,headers=headers)
            soup = BeautifulSoup(req.text,'html.parser')
            options = soup.findAll('option')
            districts = []
            values = []
            for opt in options:
                districts.append(opt.text)
                values.append(opt['value'])

            postdata1['district'] = ''
            for i in range(len(districts)):
                if districts[i] == data['addr_district']:
                    postdata1['district'] = values[i]
                    break
            if postdata1['district'] == '':
                for i in range(len(districts)):
                    if districts[i].find(data['addr_district']) != -1:
                        postdata1['district'] = values[i]
                        break
            if postdata1['district'] == '':
                postdata1['district'] = values[0]

            ##print('here4',success)
            postdata1['name'] = data['post_title_th']
            postdata1['price'] = data['price_baht']
            postdata1['detail'] = ''
            postdata1['checkdetail'] = data['post_description_th']
            postdata1['maplat'] = postdata1['maplon'] = postdata1['mapzoom'] = ''
            postdata1['contact'] = data['name']
            postdata1['email'] = data['email']
            postdata1['phone'] = postdata1['address'] = data['mobile']

            provinces = []
            values = []
            req = self.httprequestObj.http_get_with_headers('http://www.xn--12c5cnoc2a8cr4a.com/post-add.php',
                                                       headers=headers)

            soup = BeautifulSoup(req.text, 'html.parser')
            select = soup.find('select', {'name': 'province'})
            if select is not None:
                options = select.findAll('option')
                count = 0
                for opt in options:
                    if count > 0:
                        provinces.append(opt.text)
                        values.append(opt['value'])
                    count += 1
                postdata1['province'] = ''
                for i in range(len(provinces)):
                    if provinces[i] == data['addr_province']:
                        postdata1['province'] = values[i]
                        break
                if postdata1['province'] == '':
                    for i in range(len(provinces)):
                        if provinces[i].find(data['addr_province']) != -1:
                            postdata1['province'] = values[i]
                            break
                if postdata1['province'] == '':
                    postdata1['province'] = values[0]

                ##print('here5',success)
                url = 'http://www.xn--12c5cnoc2a8cr4a.com/lib/amphur.php?province=' + postdata1['province']
                req = self.httprequestObj.http_get_with_headers(url, headers=headers)
                soup = BeautifulSoup(req.text, 'html.parser')
                options = soup.findAll('option')
                districts = []
                values = []
                for opt in options:
                    districts.append(opt.text)
                    values.append(opt['value'])

                postdata1['amphur'] = ''
                for i in range(len(districts)):
                    if districts[i] == data['addr_district']:
                        postdata1['amphur'] = values[i]
                        break
                if postdata1['amphur'] == '':
                    for i in range(len(districts)):
                        if districts[i].find(data['addr_district']) != -1:
                            postdata1['amphur'] = values[i]
                            break
                if postdata1['amphur'] == '':
                    postdata1['amphur'] = values[0]

                ##print('here6',success)
                postdata1['zipcode'] = '10400'
                postdata1['website'] = '11111'
                postdata1['password'] = data['pass']
                req = self.httprequestObj.http_get_with_headers('http://www.xn--12c5cnoc2a8cr4a.com/post-add.php',
                                                           headers=headers)
                soup = BeautifulSoup(req.text, 'html.parser')
                postdata1['answer']=postdata1['hiddenanswer'] = soup.find('input', {'name': 'hiddenanswer'})['value']

                postdata1['accept'] = 'on'
            else:
                ##print('here')
                req = self.httprequestObj.http_get_with_headers('http://www.xn--12c5cnoc2a8cr4a.com/post-add.php',headers=headers)
                soup = BeautifulSoup(req.text,'html.parser')
                postdata1['contact'] = soup.find('input',{'name':'contact'})['value']
                postdata1['email'] = soup.find('input', {'name': 'email'})['value']
                postdata1['phone'] = soup.find('input', {'name': 'phone'})['value']
                postdata1['address'] = soup.find('input', {'name': 'address'})['value']
                postdata1['province'] = soup.find('input', {'name': 'province'})['value']
                postdata1['amphur'] = soup.find('input', {'name': 'amphur'})['value']
                postdata1['zipcode'] = soup.find('input', {'name': 'zipcode'})['value']
                postdata1['website'] = soup.find('input', {'name': 'website'})['value']


            postdata = postdata1
            url = 'http://www.xn--12c5cnoc2a8cr4a.com/lib/checkpost.php'
            req = self.httprequestObj.http_post(url,data=postdata1,headers=headers)
            txt = str(req.text)
            ##print(txt)

            if len(txt)>0 and txt[0]=='-':
                success = 'false'
                detail = 'Post already exists'
            else:
                postdata['detail'] = '<p>'+postdata['checkdetail']+'</p>'
                postdata['maplat'] = data['geo_latitude']
                postdata['maplon'] = data['geo_longitude']
                postdata['mapzoom'] = '0'

                if 'post_images' in data and len(data['post_images']) > 0:
                    pass
                else:
                    data['post_images'] = ['./imgtmp/default/white.jpg']

                file = []
                temp = 1

                if len(data['post_images']) <= 6:
                    for i in data['post_images']:
                        y = str(random.randint(0, 100000000000000000)) + ".jpg"
                        # #print(y)
                        file.append((str('photo' + str(temp)), (y, open(i, "rb"), "image/jpg")))
                        temp = temp + 1

                else:
                    for i in data['post_images'][:6]:
                        y = str(random.randint(0, 100000000000000000)) + ".jpg"
                        # #print(y)
                        file.append((str('photo' + str(temp)), (y, open(i, "rb"), "image/jpg")))
                        temp = temp + 1

                url = 'http://www.xn--12c5cnoc2a8cr4a.com/post-add.php'
                req = self.httprequestObj.http_post(url,data=postdata,files=file,headers=headers)
                soup = BeautifulSoup(req.text,'html.parser')
                succ = soup.find('h3',{'class','success'})
                if succ != None:
                    a = succ.find('a')
                    post_url = a['href']
                    post_id = ''
                    ind = post_url.find('view')+4
                    while post_url[ind]!='/':
                        post_id+=post_url[ind]
                        ind+=1
                    success = 'true'
                    detail = 'Successfully created a post'
                else:
                    sucess = 'false'
                    detail = 'Network Problem'

        end_time = datetime.datetime.utcnow()
        result = {
            "success": success,
            "usage_time": str(end_time - start_time),
            "start_time": str(start_time),
            "end_time": str(end_time),
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "null",
            'ds_id': data['ds_id'],
            "detail": detail,
            "websitename": "freeannouncement"
        }
        return result

    def delete_post(self, postdata):

        test_login = self.test_login(postdata)
        success = test_login["success"]
        start_time = datetime.datetime.utcnow()
        end_time = datetime.datetime.utcnow()
        post_id = int(postdata["post_id"])
        detail = test_login["detail"]

        if success == "true":
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
            }
            url = 'http://www.xn--12c5cnoc2a8cr4a.com/manage-post.php?delete='+str(post_id)
            ##print(url)
            req = self.httprequestObj.http_get_with_headers(url,headers=headers)

            if str(req.text).find('ยินดีด้วยค่ะ ระบบได้ทำการลบประกาศให้ท่านเรียบร้อยแล้ว')!=-1:
                detail = 'Successfully deleted'
            else:
                success = 'false'
                detail = 'Invalid id'


        end_time = datetime.datetime.utcnow()
        result = {
            "success": success,
            "usage_time": str(end_time - start_time),
            "start_time": str(start_time),
            "end_time": str(end_time),
            "log_id": postdata['log_id'],
            'ds_id':postdata['ds_id'],
            "post_id":postdata['post_id'],
            "detail": detail,
            "websitename": "freeannouncement"
        }
        return result

    def search_post(self, postdata):

        start_time = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_url = ""
        post_id = ""
        post_modify_time = ""
        post_view = ""
        post_found = "false"

        if success == "true":
            post_title = postdata['post_title_th']
            post_title= re.sub("\.","",post_title)
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
            }
            url = 'http://www.xn--12c5cnoc2a8cr4a.com/manage-post.php'
            req = self.httprequestObj.http_get_with_headers(url,headers=headers)

            soup = BeautifulSoup(req.text,'html.parser')
            if soup.find('div', {'class': 'pagination'}) == None:
                total_pages = 1
            else:
                total_pages = len(soup.find('div', {'class': 'pagination'}).findAll('li'))
                if total_pages>2:
                    total_pages-=2
                elif total_pages == 0:
                    total_pages += 1
            ##print(total_pages)
            valid_ids = []
            valid_titles = []
            valid_urls = []
            for i in range(total_pages):
                url = 'http://www.xn--12c5cnoc2a8cr4a.com/manage-post.php?page='+str(i+1)
                req = self.httprequestObj.http_get_with_headers(url,headers=headers)

                soup = BeautifulSoup(req.text,'html.parser')
                posts = soup.find('div',{'class':'postlist'}).findAll('ul')
                for post in posts:
                    code = (post.find('span',{'class':'code'}).text).split(" ")
                    code = int(code[1])
                    valid_ids.append(code)
                    li = post.find('li',{'class':'title'})
                    title = li.find('a')['title']
                    url = li.find('a')['href']
                    valid_urls.append(url)
                    valid_titles.append(title)


            for i in range(len(valid_titles)):
                if valid_titles[i] in post_title or post_title in valid_titles[i]:
                    post_url = valid_urls[i]
                    post_id = str(valid_ids[i])
                    post_found = 'true'
                    detail = 'Post found with given title'
                    break
            if post_found == 'false':
                success=False
                detail = 'Invalid post title'

        end_time = datetime.datetime.utcnow()
        result = {
            "success": success,
            "usage_time": str(end_time - start_time),
            "start_time": str(start_time),
            "end_time": str(end_time),
            "detail": detail,
            "websitename": "freeannouncement",
            "account_type": None,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "post_url": post_url,
            "post_found": post_found
        }
        return result

    def edit_post(self, data):

        start_time = datetime.datetime.utcnow()
        post_id = data['post_id']
        # login
        result = self.test_login(data)
        success = result['success']
        detail = result['detail']
        #print(success, detail)
        post_url = ''

        if success == 'true':

            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
            }
            url = 'http://www.xn--12c5cnoc2a8cr4a.com/manage-post.php'
            req = self.httprequestObj.http_get_with_headers(url, headers=headers)

            soup = BeautifulSoup(req.text, 'html.parser')
            if soup.find('div', {'class': 'pagination'}) == None:
                total_pages = 1
            else:
                total_pages = len(soup.find('div', {'class': 'pagination'}).findAll('li'))
                if total_pages>2:
                    total_pages-=2
                elif total_pages == 0:
                    total_pages += 1
            # #print(total_pages)
            valid_ids = []

            for i in range(total_pages):
                url = 'http://www.xn--12c5cnoc2a8cr4a.com/manage-post.php?page=' + str(i + 1)
                req = self.httprequestObj.http_get_with_headers(url, headers=headers)

                soup = BeautifulSoup(req.text, 'html.parser')
                posts = soup.find('div', {'class': 'postlist'}).findAll('ul')
                for post in posts:
                    code = (post.find('span', {'class': 'code'}).text).split(" ")
                    code = int(code[1])
                    valid_ids.append(code)
            if post_id == '':
                post_id = 0
            print(int(post_id),valid_ids)
            if int(post_id) in valid_ids:
                postdata1 = {}

                headers = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
                }
                req = self.httprequestObj.http_get_with_headers('http://www.xn--12c5cnoc2a8cr4a.com/post-edit.php?id='+str(post_id), headers=headers)
                soup = BeautifulSoup(req.text, 'html.parser')
                #print('here1',success)
                postdata1['save'] = soup.find('input', {'name': 'save'})['value']
                postdata1['type'] = 'guest'
                if data['listing_type'] == 'ขาย':
                    postdata1['want'] = 'sale'
                else:
                    postdata1['want'] = 'forrent'

                postdata1['status'] = '2hand'
                postdata1['duration'] = '-1'
                postdata1['category'] = '1009'
                ids = {
                    'คอนโด': '1',
                    'บ้านเดี่ยว': '2',
                    'บ้านแฝด': '3',
                    'ทาวน์เฮ้าส์': '4',
                    'ตึกแถว-อาคารพาณิชย์': '5',
                    'ที่ดิน': '6',
                    'อพาร์ทเมนท์': '7',
                    'โรงแรม': '8',
                    'ออฟฟิศสำนักงาน': '9',
                    'โกดัง-โรงงาน': '10',
                    'โรงงาน': '25'
                }
                proid = {
                    '1':'1149',
                    '2':'1147',
                    '3':'1147',
                    '4':'1154',
                    '5':'1153',
                    '6':'1148',
                    '7':'1157',
                    '8':'1156',
                    '9':'1151',
                    '10':'1155',
                    '25':'1155'
                }
                ##print('here2',success)
                ##print(data['property_type'])
                if data['property_type'] not in proid:
                    postdata1['subcategory'] = proid[ids[str(data['property_type'])]]
                else:
                    postdata1['subcategory'] = proid[str(data['property_type'])]
                provinces = []
                values = []
                #print('here22')
                select = soup.find('select',{'name':'city'})
                ##print(select)
                options = select.findAll('option')
                count = 0
                for opt in options:
                    if count>0:
                        provinces.append(opt.text)
                        values.append(opt['value'])
                    count+=1
                postdata1['city'] = ''
                for i in range(len(provinces)):
                    if provinces[i] == data['addr_province']:
                        postdata1['city'] = values[i]
                        break
                if postdata1['city'] == '':
                    for i in range(len(provinces)):
                        if provinces[i].find(data['addr_province'])!=-1:
                            postdata1['city'] = values[i]
                            break
                if postdata1['city'] == '':
                    postdata1['city'] = values[0]

                #print('here3',success)
                url = 'http://www.xn--12c5cnoc2a8cr4a.com/lib/district.php?province='+postdata1['city']
                req = self.httprequestObj.http_get_with_headers(url,headers=headers)
                soup = BeautifulSoup(req.text,'html.parser')
                options = soup.findAll('option')
                districts = []
                values = []
                for opt in options:
                    districts.append(opt.text)
                    values.append(opt['value'])

                postdata1['district'] = ''
                for i in range(len(districts)):
                    if districts[i] == data['addr_district']:
                        postdata1['district'] = values[i]
                        break
                if postdata1['district'] == '':
                    for i in range(len(districts)):
                        if districts[i].find(data['addr_district']) != -1:
                            postdata1['district'] = values[i]
                            break
                if postdata1['district'] == '':
                    postdata1['district'] = values[0]

                #print('here4',success)
                postdata1['name'] = data['post_title_th']
                postdata1['price'] = data['price_baht']
                postdata1['detail'] = ''
                postdata1['checkdetail'] = data['post_description_th']
                postdata1['maplat'] = postdata1['maplon'] = postdata1['mapzoom'] = ''
                postdata1['contact'] = data['name']
                postdata1['email'] = data['email']
                postdata1['phone'] = postdata1['address'] = data['mobile']

                provinces = []
                values = []
                req = self.httprequestObj.http_get_with_headers('http://www.xn--12c5cnoc2a8cr4a.com/post-edit.php?id='+str(post_id),
                                                           headers=headers)

                soup = BeautifulSoup(req.text, 'html.parser')
                select = soup.find('select', {'name': 'province'})
                if select is not None:
                    options = select.findAll('option')
                    count = 0
                    for opt in options:
                        if count > 0:
                            provinces.append(opt.text)
                            values.append(opt['value'])
                        count += 1
                    postdata1['province'] = ''
                    for i in range(len(provinces)):
                        if provinces[i] == data['addr_province']:
                            postdata1['province'] = values[i]
                            break
                    if postdata1['province'] == '':
                        for i in range(len(provinces)):
                            if provinces[i].find(data['addr_province']) != -1:
                                postdata1['province'] = values[i]
                                break
                    if postdata1['province'] == '':
                        postdata1['province'] = values[0]

                    ##print('here5',success)
                    url = 'http://www.xn--12c5cnoc2a8cr4a.com/lib/amphur.php?province=' + postdata1['province']
                    req = self.httprequestObj.http_get_with_headers(url, headers=headers)
                    soup = BeautifulSoup(req.text, 'html.parser')
                    options = soup.findAll('option')
                    districts = []
                    values = []
                    for opt in options:
                        districts.append(opt.text)
                        values.append(opt['value'])

                    postdata1['amphur'] = ''
                    for i in range(len(districts)):
                        if districts[i] == data['addr_district']:
                            postdata1['amphur'] = values[i]
                            break
                    if postdata1['amphur'] == '':
                        for i in range(len(districts)):
                            if districts[i].find(data['addr_district']) != -1:
                                postdata1['amphur'] = values[i]
                                break
                    if postdata1['amphur'] == '':
                        postdata1['amphur'] = values[0]

                    ##print('here6',success)
                    postdata1['zipcode'] = '10400'
                    postdata1['website'] = '11111'
                    postdata1['password'] = data['pass']
                    req = self.httprequestObj.http_get_with_headers('http://www.xn--12c5cnoc2a8cr4a.com/post-edit.php?id='+str(post_id),
                                                               headers=headers)
                    soup = BeautifulSoup(req.text, 'html.parser')
                    postdata1['answer']=postdata1['hiddenanswer'] = soup.find('input', {'name': 'hiddenanswer'})['value']

                    postdata1['accept'] = 'on'
                else:
                    ##print('here')
                    req = self.httprequestObj.http_get_with_headers('http://www.xn--12c5cnoc2a8cr4a.com/post-edit.php?id='+str(post_id),headers=headers)
                    soup = BeautifulSoup(req.text,'html.parser')
                    postdata1['contact'] = soup.find('input',{'name':'contact'})['value']
                    postdata1['email'] = soup.find('input', {'name': 'email'})['value']
                    postdata1['phone'] = soup.find('input', {'name': 'phone'})['value']
                    postdata1['address'] = soup.find('input', {'name': 'address'})['value']
                    postdata1['province'] = soup.find('input', {'name': 'province'})['value']
                    postdata1['amphur'] = soup.find('input', {'name': 'amphur'})['value']
                    postdata1['zipcode'] = soup.find('input', {'name': 'zipcode'})['value']
                    postdata1['website'] = soup.find('input', {'name': 'website'})['value']


                postdata = postdata1
                url = 'http://www.xn--12c5cnoc2a8cr4a.com/lib/checkpost.php'
                req = self.httprequestObj.http_post(url,data=postdata1,headers=headers)
                txt = str(req.text)
                ##print(txt)

                if len(txt)>0 and txt[0]=='-':
                    success = 'false'
                    detail = 'Post already exists'
                else:
                    postdata['detail'] = '<p>'+postdata['checkdetail']+'</p>'
                    postdata['maplat'] = data['geo_latitude']
                    postdata['maplon'] = data['geo_longitude']
                    postdata['mapzoom'] = '0'

                    if 'post_images' in data and len(data['post_images']) > 0:
                        pass
                    else:
                        data['post_images'] = ['./imgtmp/default/white.jpg']

                    file = []
                    temp = 1

                    if len(data['post_images']) <= 6:
                        for i in data['post_images']:
                            y = str(random.randint(0, 100000000000000000)) + ".jpg"
                            # #print(y)
                            file.append((str('photo' + str(temp)), (y, open(i, "rb"), "image/jpg")))
                            temp = temp + 1

                    else:
                        for i in data['post_images'][:6]:
                            y = str(random.randint(0, 100000000000000000)) + ".jpg"
                            # #print(y)
                            file.append((str('photo' + str(temp)), (y, open(i, "rb"), "image/jpg")))
                            temp = temp + 1

                    url = 'http://www.xn--12c5cnoc2a8cr4a.com/post-edit.php?id='+str(post_id)
                    req = self.httprequestObj.http_post(url,data=postdata,files=file,headers=headers)
                    soup = BeautifulSoup(req.text,'html.parser')
                    succ = soup.find('h3',{'class','success'})
                    if succ != None:
                        a = succ.find('a')
                        post_url = a['href']
                        success = 'true'
                        detail = 'Successfully edited post'
                    else:
                        sucess = 'false'
                        detail = 'Network Problem'
            else:
                post = self.create_post(data)
                success = post['success']
                if success == 'true':
                    detail = 'Successfully edited post'
                    post_id = post['post_id']
                    post_url = post['post_url']
                else:
                    detail = post['detail']
                """success = 'false'
                detail = 'Invalid post id'"""

        end_time = datetime.datetime.utcnow()
        result = {
            "success": success,
            "usage_time": str(end_time - start_time),
            "start_time": str(start_time),
            "end_time": str(end_time),
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "null",
            'ds_id':data['ds_id'],
            'log_id': data['log_id'],
            "detail": detail,
            "websitename": "freeannouncement"
        }
        return result

    def boost_post(self, data):
        start_time = datetime.datetime.utcnow()
        #print('start')
        post_id = data['post_id']
        log_id = data['log_id']
        result = self.test_login(data)
        success = result['success']
        detail = result['detail']
        if success == 'true':
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
            }
            url = 'http://www.xn--12c5cnoc2a8cr4a.com/manage-post.php'
            req = self.httprequestObj.http_get_with_headers(url, headers=headers)

            soup = BeautifulSoup(req.text, 'html.parser')
            if soup.find('div', {'class': 'pagination'}) == None:
                total_pages = 1
            else:
                total_pages = len(soup.find('div', {'class': 'pagination'}).findAll('li'))
                if total_pages>2:
                    total_pages-=2
                elif total_pages==0:
                    total_pages+=1
            # #print(total_pages)

            valid_ids = []

            for i in range(total_pages):
                url = 'http://www.xn--12c5cnoc2a8cr4a.com/manage-post.php?page=' + str(i + 1)
                req = self.httprequestObj.http_get_with_headers(url, headers=headers)

                soup = BeautifulSoup(req.text, 'html.parser')
                posts = soup.find('div', {'class': 'postlist'}).findAll('ul')
                for post in posts:
                    code = (post.find('span', {'class': 'code'}).text).split(" ")
                    code = int(code[1])
                    valid_ids.append(code)
            #print(valid_ids)
            #print('finish')
            if post_id == '':
                post_id = 0
            if int(post_id) in valid_ids:
                url = 'http://www.xn--12c5cnoc2a8cr4a.com/manage-post.php?update='+str(post_id)
                req = self.httprequestObj.http_get_with_headers(url,headers=headers)
                success = 'true'
                detail = 'Post boosted successfully'
            else:
                success = 'false'
                detail = 'Post not found'

        end_time = datetime.datetime.utcnow()
        result = {
            "success": success,
            "usage_time": str(end_time - start_time),
            "start_time": str(start_time),
            "end_time": str(end_time),
            "detail": detail,
            'ds_id':data['ds_id'],
            "log_id": log_id,
            "post_id": data['post_id'],
            'websitename':'freeannouncement'
        }
        return result
