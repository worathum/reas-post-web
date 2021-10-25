# SEND username for login, not email
import requests, re, random
from bs4 import BeautifulSoup
import json, datetime
from .lib_httprequest import *

class house4post:

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
        url = "https://www.house4post.com/logout_member"
        self.httprequestObj.http_get(url)

    def register_user(self, data):
        self.logout_user()
        start_time = datetime.datetime.utcnow()
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}
        success = 'true'
        detail = ''
        postdata = {}
        postdata['username'] = data['user'].split('@')[0]
        postdata['pass'] = postdata['conpass'] = data['pass']
        postdata['email'] = data['user']
        postdata['name'] = data['name_th']
        postdata['lastname'] = data['surname_th']
        postdata['phone'] = data['tel']
        postdata['address'] = 'พญาไท,กรุงเทพ'
        postdata['submit'] = ''
        regex = '^\\w+([\\.-]?\\w+)*@\\w+([\\.-]?\\w+)*$'
        f1 = True
        regex = '^\\w+([\\.-]?\\w+)*@\\w+([\\.-]?\\w+)*$'
        if re.search(regex, postdata['email']):
            f1 = True
        else:
            f1 = False
        if f1 == False:
            success = 'false'
            detail = 'Invalid email'
        if postdata['username'] == '' or postdata['pass'] == '' or postdata['name'] == '' or postdata['lastname'] == '' or postdata['phone'] == '':
            success = 'false'
            detail = 'Empty credentials'
        if success == 'true':
            url = 'https://www.house4post.com/signup_member.php'
            req = self.httprequestObj.http_post(url, data=postdata, headers=headers)
            txt = str(req.text)
            if txt.find('สมัครสมาชิกเรียบร้อยแล้ว') == -1:
                success = 'false'
                detail = 'Already a user'
            else:
                success = 'true'
                detail = 'Successfully Registered'
        end_time = datetime.datetime.utcnow()
        result = {'websitename':'house4post',
         'success':success,
         'start_time':str(start_time),
         'end_time':str(end_time),
         'usage_time':str(end_time - start_time),
         'detail':detail,
         'ds_id':data['ds_id']}
        return result

    def test_login(self, data):
        self.logout_user()
        start_time = datetime.datetime.utcnow()
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}
        postdata = {}
        postdata['log_u'] = data['user']
        postdata['log_p'] = data['pass']
        postdata['submit'] = 'Login'
        success = ''
        detail = ''
        url = 'https://www.house4post.com/login.php'
        req = self.httprequestObj.http_post(url, data=postdata, headers=headers)
        txt = req.text
        if txt.find('Username หรือ Password ไม่ถูกต้อง') == -1:
            success = 'true'
            detail = 'Successfully login'
        else:
            success = 'false'
            detail = 'User not registered yet'
        end_time = datetime.datetime.utcnow()
        result = {'websitename':'house4post',
         'success':success,
         'start_time':str(start_time),
         'end_time':str(end_time),
         'usage_time':str(end_time - start_time),
         'ds_id':data['ds_id'],
         'detail':detail}
        return result

    def create_post(self, data, to_edit=0):
        start_time = datetime.datetime.utcnow()
        result = self.test_login(data)
        success = result['success']
        detail = result['detail']
        post_url = ''
        post_id = ''
        if success == 'true':
            postdata = {}
            postdata['name'] = data['post_title_th']
            postdata['project'] = ''
            if 'project_name' in data:
                postdata['project'] = data['project_name']
            if 'web_project_name' in data and data['web_project_name'] != None:
                if data['web_project_name'] != '':
                    postdata['project'] = data['web_project_name']
            if 'project' in postdata and postdata['project'] == '':
                postdata['project'] = data['post_title_th']
            else:
                postdata['web_project_name'] = data['post_title_th']
            postdata['cate'] = '2'
            if data['listing_type'] == 'ขาย':
                postdata['cate'] = '1'
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}
            ids = {'คอนโด':'1',
             'บ้านเดี่ยว':'2',
             'บ้านแฝด':'3',
             'ทาวน์เฮ้าส์':'4',
             'ตึกแถว-อาคารพาณิชย์':'5',
             'ที่ดิน':'6',
             'อพาร์ทเมนท์':'7',
             'โรงแรม':'8',
             'ออฟฟิศสำนักงาน':'9',
             'โกดัง-โรงงาน':'10',
             'โรงงาน':'25'}
            property_tp = {'1':'1',
             '2':'5',
             '3':'15',
             '4':'3',
             '5':'2',
             '6':'4',
             '7':'7',
             '8':'13',
             '9':'9',
             '10':'8',
             '25':'10'}
            if str(data['property_type']) in ids:
                postdata['section'] = property_tp[ids[str(data['property_type'])]]
            else:
                postdata['section'] = property_tp[str(data['property_type'])]
            postdata['number'] = ''
            postdata['soi'] = data['addr_soi']
            postdata['road'] = data['addr_road']
            postdata['Province'] = ''
            req = self.httprequestObj.http_get_with_headers('https://www.house4post.com/add_property', headers=headers)
            soup = BeautifulSoup(req.text, 'html.parser')
            options = soup.find('select', {'name': 'Province'}).findAll('option')
            count = 0
            provinces = []
            ids = []
            for opt in options:
                if count > 0:
                    ids.append(opt['value'])
                    provinces.append(opt.text)
                count += 1

            for i in range(len(provinces)):
                if provinces[i] == data['addr_province']:
                    postdata['Province'] = ids[i]
                    break

            if postdata['Province'] == '':
                for i in range(len(provinces)):
                    if provinces[i].find(data['addr_province']) != -1:
                        postdata['Province'] = ids[i]
                        break

            if postdata['Province'] == '':
                postdata['Province'] = ids[0]
            postdata['District'] = ''
            url = 'https://www.house4post.com/getaddress.php?ID=' + str(postdata['Province']) + '&TYPE=District'
            req = self.httprequestObj.http_get_with_headers(url, headers=headers)
            txt = str(req.text)
            districts = []
            ids = []
            while txt.find('amphur_id') != -1:
                ind = txt.find('amphur_id')
                c = 0
                while c != 1 or txt[ind] != '"':
                    if txt[ind] == '"':
                        c += 1
                    ind += 1

                id = ''
                ind += 1
                while txt[ind] != '"':
                    id += txt[ind]
                    ind += 1

                ids.append(id)
                txt = txt[ind:]
                ind = txt.find('amphur_name')
                c = 0
                while c != 1 or txt[ind] != '"':
                    if txt[ind] == '"':
                        c += 1
                    ind += 1

                dist = ''
                ind += 1
                while txt[ind] != '"':
                    dist += txt[ind]
                    ind += 1

                districts.append(dist)
                txt = txt[ind:]

            for i in range(len(districts)):
                if districts[i] == data['addr_district']:
                    postdata['District'] = ids[i]
                    break

            if postdata['District'] == '':
                for i in range(len(districts)):
                    if districts[i].find(data['addr_district']) != -1:
                        postdata['District'] = ids[i]
                        break

            if postdata['District'] == '':
                postdata['District'] = ids[0]
            postdata['Subdistrict'] = ''
            url = 'https://www.house4post.com/getaddress.php?ID=' + str(postdata['District']) + '&TYPE=Subdistrict'
            req = self.httprequestObj.http_get_with_headers(url, headers=headers)
            txt = str(req.text)
            subdistricts = []
            ids = []
            while txt.find('district_id') != -1:
                ind = txt.find('district_id')
                c = 0
                while c != 1 or txt[ind] != '"':
                    if txt[ind] == '"':
                        c += 1
                    ind += 1

                id = ''
                ind += 1
                while txt[ind] != '"':
                    id += txt[ind]
                    ind += 1

                ids.append(id)
                txt = txt[ind:]
                ind = txt.find('district_name')
                c = 0
                while c != 1 or txt[ind] != '"':
                    if txt[ind] == '"':
                        c += 1
                    ind += 1

                subdist = ''
                ind += 1
                while txt[ind] != '"':
                    subdist += txt[ind]
                    ind += 1

                subdistricts.append(subdist)
                txt = txt[ind:]

            for i in range(len(subdistricts)):
                if subdistricts[i] == data['addr_sub_district']:
                    postdata['Subdistrict'] = ids[i]
                    break

            if postdata['Subdistrict'] == '':
                for i in range(len(subdistricts)):
                    if subdistricts[i].find(data['addr_sub_district']) != -1:
                        postdata['Subdistrict'] = ids[i]
                        break

            if postdata['Subdistrict'] == '':
                postdata['Subdistrict'] = ids[0]
            postdata['price'] = str(data['price_baht'])
            postdata['area'] = ''
            if data['land_size_rai'] == '' or data['land_size_rai'] == None:
                data['land_size_rai'] = '0'
            else:
                postdata['area'] += str(str(data['land_size_rai'])+'ไร่')
            if data['land_size_ngan'] == '' or data['land_size_ngan'] == None:
                data['land_size_ngan'] = '0'
            else:
                postdata['area'] += str(str(data['land_size_ngan'])+'งาน')
            if data['land_size_wa'] == '' or data['land_size_wa'] == None:
                data['land_size_wa'] = '0'
            else:
                postdata['area'] += str(str(data['land_size_wa'])+'ตรว')
            if data['floor_area'] == '' or data['floor_area'] == None:
                data['floor_area'] = '0'
            else:
                postdata['area'] += str(str(data['floor_area'])+'ตรม')

            #postdata['area'] = str( + str(data['land_size_ngan'])+'งาน' + str(data['land_size_wa'])+'ตรว' + str(data['floor_area'])+'ตรม')
            postdata['layer'] = str(data['floor_total'])
            postdata['room'] = str(data['bed_room'])
            postdata['toilet'] = str(data['bath_room'])
            postdata['detail'] = str(data['post_description_th'])
            postdata['Submit'] = 'Submit'
            
            try:
                url = 'https://www.house4post.com/add_property.php'
                req = self.httprequestObj.http_post(url, data=postdata, headers=headers)
                txt = req.text
                
                if txt.find('.php?id=') == -1:
                    success = 'false'
                    soup = BeautifulSoup(txt, features=self.parser)
                    alert = soup.find(class_='alert-danger')
                    detail = 'Network error'
                    if alert:
                        detail = alert.getText()
                else:
                    ind = txt.find('.php?id=') + 8
                    while txt[ind] != '>':
                        post_id += txt[ind]
                        ind += 1

                    post_url = 'https://www.house4post.com/idasungha-' + str(post_id) + '-' + data['post_title_th']
                    post_url = post_url.replace(' ', '-')
                    imgurl = 'https://www.house4post.com/add_img.php?id={}'.format(post_id)
                    self.httprequestObj.http_get(imgurl)
                    if 'post_images' in data:
                        if len(data['post_images']) > 0:
                            pass
                    else:
                        data['post_images'] = [
                         './imgtmp/default/white.jpg']
                    files = {}
                    temp = 1
                    if len(data['post_images']) <= 6:
                        for i in range(len(data['post_images'])):
                            r = open(os.getcwd() + '/' + data['post_images'][i], 'rb')
                            files['photoimg'] = r
                            response = self.httprequestObj.http_post('https://www.house4post.com/ajax_img.php', data=None, files=files)
                            time.sleep(3)

                    else:
                        for i in range(len(data['post_images'][:6])):
                            r = open(os.getcwd() + '/' + data['post_images'][i], 'rb')
                            files['photoimg'] = r
                            response = self.httprequestObj.http_post('https://www.house4post.com/ajax_img.php', data=None, files=files)
                            time.sleep(3)

                    success = 'true'
                    detail = 'Successful post'
            except:
                success = 'false'
                detail = 'Something went wrong.'

        if to_edit == 1:
            return (success, detail, post_url, post_id)
        else:
            end_time = datetime.datetime.utcnow()
            result = {'success':success,
             'usage_time':str(end_time - start_time),
             'start_time':str(start_time),
             'end_time':str(end_time),
             'post_url':post_url,
             'post_id':post_id,
             'account_type':'null',
             'ds_id':data['ds_id'],
             'detail':detail,
             'websitename':'house4post'}
            return result

    def delete_post(self, postdata):
        test_login = self.test_login(postdata)
        success = test_login['success']
        start_time = datetime.datetime.utcnow()
        end_time = datetime.datetime.utcnow()
        post_id = postdata['post_id']
        detail = test_login['detail']
        
        if success=="true":
            post_found = True
            page_num = 0
            flag = True
            """while flag:
                response = self.httprequestObj.http_get('https://www.house4post.com//maneg_property.php?&page='+str(page_num))
                if response.status_code==200:
                    soup = BeautifulSoup(response.text, features=self.parser)
                    posts_element = soup.find(class_='well')             
                    
                    if posts_element and posts_element.find('tbody'): 
                        posts = posts_element.find('tbody').find_all('tr')
                        if len(posts)<10:
                            flag = False
                        for post in posts:
                            id_link = post.find_all('td')[-1].a
                            id = id_link.get('href').split("id=")[-1]
                            print(post_id, id, post_id==id)
                            if id==post_id:
                                post_found = True
                                flag = False
                                break
                    else:
                        break
                page_num += 1"""

            # headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}
            # url = 'https://www.house4post.com/maneg_property.php'
            # valid_ids = []
            # req = self.httprequestObj.http_get_with_headers(url, headers=headers)
            # soup = BeautifulSoup(req.text, 'html.parser')
            # total_pages = 1
            # if soup.find('ul', {'class': 'pagination'}) != None:
            #     total_pages = len(soup.find('ul', {'class': 'pagination'}).findAll('li'))
            #     if total_pages > 0:
            #         total_pages -= 1
            # for i in range(total_pages):
            #     url = 'https://www.house4post.com/maneg_property.php?&page=' + str(i)
            #     req = self.httprequestObj.http_get_with_headers(url, headers=headers)
            #     soup = BeautifulSoup(req.text, 'html.parser')
            #     posts = soup.find('table', {'class': 'table table-striped'}).find('tbody').findAll('tr')
            #     for post in posts:
            #         id = ''
            #         a = str(post.find('a')['href'])
            #         ind = a.find('-') + 1
            #         while a[ind] != '-':
            #             id += a[ind]
            #             ind += 1

            #         valid_ids.append(id)

            if not post_found:
                success = 'false'
                detail = 'Invalid id'
            else:
                url = 'https://www.house4post.com/maneg_property.php?delete=' + str(post_id)
                req = self.httprequestObj.http_get_with_headers(url)
                txt = req.text
                if txt.find('ลบรายการที่เลือกเรียบร้อยแล้ว') == -1:
                    success = 'false'
                    detail = 'Network error'
                else:
                    success = 'true'
                    detail = 'Successfully deleted'
        end_time = datetime.datetime.utcnow()
        result = {'success':success,
         'usage_time':str(end_time - start_time),
         'start_time':str(start_time),
         'end_time':str(end_time),
         'log_id':postdata['log_id'],
         'ds_id':postdata['ds_id'],
         'detail':detail,
         'post_id':str(post_id),
         'websitename':'house4post'}
        return result


    def search_post(self, postdata):
        start_time = datetime.datetime.utcnow()
        test_login = self.test_login(postdata)
        success = test_login['success']
        end_time = datetime.datetime.utcnow()
        post_id = ''
        post_url = ''
        detail = test_login['detail']

        if success == "true":
            post_found = "false"
            detail = "No post found with given title"
            post_title = " ".join(str(postdata['post_title_th']).strip().split())
            
            page_num = 0
            flag = True
            while flag:
                response = self.httprequestObj.http_get('https://www.house4post.com//maneg_property.php?&page='+str(page_num))
                if response.status_code==200:
                    soup = BeautifulSoup(response.text, features=self.parser)
                    posts_element = soup.find(class_='well')             
                    
                    if posts_element and posts_element.find('tbody'): 
                        posts = posts_element.find('tbody').find_all('tr')
                        if len(posts)<10:
                            flag = False
                        for post in posts:
                            title = post.find_all('td')[1].a
                            title_text = " ".join(title.getText().strip().split())
                            if title_text==post_title:
                                flag = False
                                post_found = "true"
                                detail = "Post found successfully"
                                post_url = title.get('href')
                                post_id = post_url.split('/idasungha-')[-1].split('-')[0]
                                break
                    else:
                        break
                page_num += 1
        else:
            detail = "cannot login"

        end_time = datetime.datetime.utcnow()
        result = {'success':success,
         'usage_time':str(end_time - start_time),
         'start_time':str(start_time),
         'end_time':str(end_time),
         'detail':detail,
         'websitename':'house4post',
         'account_type':None,
         'ds_id':postdata['ds_id'],
         'log_id':postdata['log_id'],
         'post_create_time': '',
         'post_modify_time': '',
         'post_view': '',
         'post_id': post_id,
         'post_url':post_url,
         'post_found':post_found}
        return result

    def edit_post(self, data):
        start_time = datetime.datetime.utcnow()
        result = self.test_login(data)
        success = result['success']
        detail = result['detail']
        post_url = ''
        post_id = data['post_id']

        """if success == 'true':
            post_found = False
            page_num = 0
            flag = True
            while flag:
                response = self.httprequestObj.http_get('https://www.house4post.com//maneg_property.php?&page='+str(page_num))
                if response.status_code==200:
                    soup = BeautifulSoup(response.text, features=self.parser)
                    posts_element = soup.find(class_='well')             
                    
                    if posts_element and posts_element.find('tbody'): 
                        posts = posts_element.find('tbody').find_all('tr')
                        if len(posts)<10:
                            flag = False
                        for post in posts:
                            id_link = post.find_all('td')[-1].a
                            id = id_link.get('href').split("id=")[-1]
                            if id==post_id:
                                post_found = True
                                break
                    else:
                        break
                page_num += 1

            # headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}
            # url = 'https://www.house4post.com/maneg_property.php'
            # valid_ids = []
            # req = self.httprequestObj.http_get_with_headers(url, headers=headers)
            # soup = BeautifulSoup(req.text, 'html.parser')
            # total_pages = 1
            # if soup.find('ul', {'class': 'pagination'}) != None:
            #     total_pages = len(soup.find('ul', {'class': 'pagination'}).findAll('li'))
            #     if total_pages > 0:
            #         total_pages -= 1
            # for i in range(total_pages):
            #     url = 'https://www.house4post.com/maneg_property.php?&page=' + str(i)
            #     req = self.httprequestObj.http_get_with_headers(url, headers=headers)
            #     soup = BeautifulSoup(req.text, 'html.parser')
            #     posts = soup.find('table', {'class': 'table table-striped'}).find('tbody').findAll('tr')
            #     for post in posts:
            #         id = ''
            #         a = str(post.find('a')['href'])
            #         print(a)
            #         ind = a.find('-') + 1
            #         while a[ind] != '-':
            #             id += a[ind]
            #             ind += 1

            #         valid_ids.append(id)

            # print(valid_ids)
            if not post_found:
                success = 'false'
                detail = 'No post found with given id'
            else:
                self.delete_post(data)
                success, detail, post_url, post_id = self.create_post(data, to_edit=1)
                detail = 'Successfully edited'"""
        try:
            self.delete_post(data)
            success, detail, post_url, post_id = self.create_post(data, to_edit=1)
            detail = 'Successfully edited'
        except:
            success = 'false'
            detail = 'No post found with given id'
        end_time = datetime.datetime.utcnow()
        result = {'success':success,
         'usage_time':str(end_time - start_time),
         'start_time':str(start_time),
         'end_time':str(end_time),
         'post_url':post_url,
         'post_id':post_id,
         'account_type':'null',
         'ds_id':data['ds_id'],
         'log_id':data['log_id'],
         'detail':detail,
         'websitename':'house4post'}
        return result


    def boost_post(self, data):
        start_time = datetime.datetime.utcnow()
        post_id = data['post_id']
        log_id = data['log_id']
        result = self.test_login(data)
        success = result['success']
        detail = result['detail']
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}
        url = 'https://www.house4post.com/maneg_property.php'
        valid_ids = []
        req = self.httprequestObj.http_get_with_headers(url, headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        total_pages = 1
        if soup.find('ul', {'class': 'pagination'}) != None:
            total_pages = len(soup.find('ul', {'class': 'pagination'}).findAll('li'))
            if total_pages > 0:
                total_pages -= 1
        for i in range(total_pages):
            url = 'https://www.house4post.com/maneg_property.php?&page=' + str(i)
            req = self.httprequestObj.http_get_with_headers(url, headers=headers)
            soup = BeautifulSoup(req.text, 'html.parser')
            posts = soup.find('table', {'class': 'table table-striped'}).find('tbody').findAll('tr')
            for post in posts:
                id = ''
                a = str(post.find('a')['href'])
                ind = a.find('-') + 1
                while a[ind] != '-':
                    id += a[ind]
                    ind += 1

                valid_ids.append(id)

        if str(post_id) not in valid_ids:
            success = 'false'
            detail = 'Invalid id'
        if success == 'true':
            url = 'https://www.house4post.com/maneg_property.php?refresh=' + str(post_id)
            req = self.httprequestObj.http_get_with_headers(url, headers=headers)
            txt = req.text
            if txt.find(' เลื่อนประกาศเรียบร้อยแล้ว') == -1:
                success = 'false'
                detail = 'Postpone failed'
            else:
                success = 'true'
                detail = 'Successfully postponed'
        end_time = datetime.datetime.utcnow()
        result = {'success':'true',
         'usage_time':str(end_time - start_time),
         'start_time':str(start_time),
         'end_time':str(end_time),
         'detail':detail,
         'ds_id':data['ds_id'],
         'log_id':log_id,
         'post_id':post_id,
         'websitename':'house4post'}
        return result
