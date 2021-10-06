import requests, re, random
from bs4 import BeautifulSoup
import json, datetime
from .lib_httprequest import *
from .lib_captcha import  *
import datetime
import time,math
import lxml
from lxml.html.soupparser import fromstring

# Use password in mail

class postproperty:

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
        url = 'https://post-property.com/wp-login.php?action=logout&_wpnonce=cf743bdc66"'
        self.httprequestObj.http_get(url)


    def register_user(self, data):
        self.logout_user()
        start_time = datetime.datetime.utcnow()

        success = ''
        detail = ''
        postdata = {
            'firstname': data['name_th'],
            'lastname': data['surname_th'],
            'username': str(data['user']).split('@')[0],
            'email': data['user'],
            'phone': data['tel'],
            'lineid': data['line'],
            'password': data['pass'],
            'confirm_password': data['pass'],
            'g-recaptcha-response':'',
            'register-submit': 'Apply'
        }
        url = 'https://post-property.com/register'
        headers = {
        	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        }
        regex = '^\\w+([\\.-]?\\w+)*@\\w+([\\.-]?\\w+)*$'
        f1 = True
        regex = '^\\w+([\\.-]?\\w+)*@\\w+([\\.-]?\\w+)*$'
        if re.search(regex, postdata['email']):
            f1 = True
        else:
            f1 = False
        if len(data['tel']) != 10:
            success = 'false'
            detail = 'Telephone length should be 10'
        elif f1 == False:
            success = 'false'
            detail = 'Invalid email id'
        elif len(postdata['username'])<4 or len(postdata['username'])>16:
            success = 'false'
            detail = 'Username length should be between 4 and 16'
        else:

            req = self.httprequestObj.http_get(url,headers=headers)

            soup = BeautifulSoup(req.text,'html5lib')

            key = ''
            #url = ''
            key = str(soup.find('div',{'class':'g-recaptcha'})['data-sitekey'])
            ##print(key)
            #url = str(soup.find('div',{'class':'g-recaptcha'}).find('iframe')['src'])
            ##print(key)
            ##print(url)
            capt = lib_captcha()
            result = capt.reCaptcha(key,url)
            ##print('here',result)

            if result != '' and str(result) != '0':
                captcha_code = result
                ##print(captcha_code)
                postdata['g-recaptcha-response'] = captcha_code

                url = 'https://post-property.com/register'

                req = self.httprequestObj.http_post(url,data=postdata,headers=headers)

                txt = str(req.text)
                ##print(req.status_code)
                print(txt)
                #if txt.find('สม้ครสมาชิกสำเร็จ')!=-1:
                if "สม้ครสมาชิกสำเร็จ กรุณาตรวจสอบข้อมุลผู้ใช้ใน Email" in txt:
                    success = True
                    detail = 'Successfully registered'

                elif "ชื่อ Username นี้มีคนใช้ไปแล้ว" in txt:
                    success=False
                    detail= 'Username already Taken.'

                elif "อีเมลนี้มีคนอื่นใช้ไปแล้ว หรือรูปแบบ email ไม่ถูกต้อง" in txt:
                    success = False
                    detail = 'User already exists'
                else:
                    success='False'
                    detail="Registration Failed."
            else:
                success = 'false'
                detail = 'Problem with captcha'



        end_time = datetime.datetime.utcnow()
        result = {'websitename':'postproperty',
         'success':success,
         'start_time':str(start_time),
         'end_time':str(end_time),
         'usage_time':str(end_time - start_time),
         'detail':detail,
         'ds_id':data['ds_id']}
        return result

    def test_login(self, data):
        # Use password in mail
        self.logout_user()
        # ไม่สามารถเข้าสู่ระบบได้, โปรดตรวจสอบอีเมล์และรหัสผ่านอีกครั้ง

        '''
        hc1@gmail.com  abcd
        hc2@gmail.com  abcd
        hardik@gmail.com  abcdefgh

        '''
        start_time = datetime.datetime.utcnow()

        success = ''
        detail = ''
        postdata = {
            'log': data['user'],
            'pwd': data['pass'],
            'rememberme': 'forever',
            'wp-submit': 'Login',
            'redirect_to': 'https://post-property.com/wp-admin'
        }

        url = 'https://post-property.com/wp-login.php'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        }
        req = self.httprequestObj.http_post(url,data=postdata,headers=headers)
        txt = req.text

        if txt.find('logout') != -1:
            success = 'true'
            detail = 'Login Successful'
        else:
            success = 'false'
            detail = 'Invalid credentials'

        end_time = datetime.datetime.utcnow()
        result = {'websitename':'postproperty',
         'success':success,
         'start_time':str(start_time),
         'end_time':str(end_time),
         'usage_time':str(end_time - start_time),
         'ds_id':data['ds_id'],
         'detail':detail}
        return result

    def create_post(self, data):
        # ลงประกาศเสร็จเรียบร้อยแล้ว
        ##print('in')
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
            ##print('login')
            postdata = {}
            url = 'https://post-property.com/wp-admin/post-new.php'
            req = self.httprequestObj.http_get(url,headers=headers)
            soup = BeautifulSoup(req.text,'html.parser')
            ##print('start1')
            postdata['_wpnonce'] = soup.find('input',{'name':'_wpnonce'})['value']
            ##print(postdata['_wpnonce'])
            txt = str(req.text)
            ind = txt.find('"action":"upload-attachment","_wpnonce":"')+41
            ##print(ind)
            nonce = ''
            ##print(data['addr_province'])
            ##print(data['addr_district'])
            while txt[ind]!='"':
                nonce += txt[ind]
                ind+=1
            ##print(nonce)
            postdata['_wp_http_referer'] = soup.find('input',{'name':'_wp_http_referer'})['value']
            postdata['user_ID'] = soup.find('input',{'name':'user_ID'})['value']
            postdata['action'] = soup.find('input',{'name':'action'})['value']
            postdata['originalaction'] = soup.find('input',{'name':'originalaction'})['value']
            postdata['post_author'] = soup.find('input',{'name':'post_author'})['value']
            postdata['post_type'] = soup.find('input',{'name':'post_type'})['value']
            postdata['original_post_status'] = soup.find('input',{'name':'original_post_status'})['value']
            postdata['referredby'] = soup.find('input',{'name':'referredby'})['value']
            postdata['_wp_original_http_referer'] = soup.find('input',{'name':'_wp_original_http_referer'})['value']
            postdata['auto_draft'] = soup.find('input',{'name':'auto_draft'})['value']
            postdata['post_ID'] = soup.find('input',{'name':'post_ID'})['value']
            post_id = str(postdata['post_ID'])
            postdata['meta-box-order-nonce'] = soup.find('input',{'name':'meta-box-order-nonce'})['value']
            postdata['closedpostboxesnonce'] = soup.find('input',{'name':'closedpostboxesnonce'})['value']
            postdata['post_title'] = data['post_title_th']
            postdata['samplepermalinknonce'] = soup.find('input', {'name': 'samplepermalinknonce'})['value']
            postdata['content'] = str(data['post_description_th'])
            postdata['wp-preview'] = soup.find('input', {'name': 'wp-preview'})['value']
            postdata['hidden_post_status'] = soup.find('input', {'name': 'hidden_post_status'})['value']
            postdata['post_status'] = 'draft'
            postdata['hidden_post_password'] = soup.find('input', {'name': 'hidden_post_password'})['value']
            postdata['hidden_post_visibility'] = soup.find('input', {'name': 'hidden_post_visibility'})['value']
            #postdata['hidden_post_password'] = soup.find('input', {'name': 'hidden_post_password'})['value']
            postdata['visibility'] = 'public'
            postdata['post_password'] = ''
            postdata['jj'] = soup.find('input', {'name': 'jj'})['value']
            options = soup.find('select',{'name':'mm'}).findAll('option')
            ##print('debug1')
            for opt in options:
                if opt.has_attr('selected'):
                    postdata['mm'] = opt['value']
                    break
            postdata['aa'] = soup.find('input', {'name': 'aa'})['value']
            postdata['hh'] = soup.find('input', {'name': 'hh'})['value']
            postdata['mn'] = soup.find('input', {'name': 'mn'})['value']
            postdata['ss'] = soup.find('input', {'name': 'ss'})['value']
            postdata['hidden_mm'] = soup.find('input', {'name': 'hidden_mm'})['value']
            postdata['cur_mm'] = soup.find('input', {'name': 'cur_mm'})['value']
            postdata['hidden_jj'] = soup.find('input', {'name': 'hidden_jj'})['value']
            postdata['cur_jj'] = soup.find('input', {'name': 'cur_jj'})['value']
            postdata['hidden_aa'] = soup.find('input', {'name': 'hidden_aa'})['value']
            postdata['cur_aa'] = soup.find('input', {'name': 'cur_aa'})['value']
            postdata['hidden_hh'] = soup.find('input', {'name': 'hidden_hh'})['value']
            postdata['cur_hh'] = soup.find('input', {'name': 'cur_hh'})['value']
            postdata['hidden_mn'] = soup.find('input', {'name': 'hidden_mn'})['value']
            postdata['cur_mn'] = soup.find('input', {'name': 'cur_mn'})['value']
            postdata['pvc_nonce'] = soup.find('input', {'name': 'pvc_nonce'})['value']
            postdata['amp-status-nonce'] = soup.find('input', {'name': 'amp-status-nonce'})['value']
            postdata['original_publish'] = soup.find('input', {'name': 'original_publish'})['value']
            postdata['publish'] = soup.find('input', {'name': 'publish'})['value']
            postdata['_thumbnail_id'] = soup.find('input', {'name': '_thumbnail_id'})['value']
            postdata['yoast_free_metabox_nonce'] = soup.find('input', {'name': 'yoast_free_metabox_nonce'})['value']
            postdata['yoast_free_metabox_social_nonce'] = '' #soup.find('input', {'name': 'yoast_free_metabox_social_nonce'})['value']
            postdata['yoast_wpseo_focuskw'] = soup.find('input', {'name': 'yoast_wpseo_focuskw'})['value']
            postdata['yoast_wpseo_title'] = soup.find('input', {'name': 'yoast_wpseo_title'})['value']
            postdata['yoast_wpseo_metadesc'] = soup.find('input', {'name': 'yoast_wpseo_metadesc'})['value']
            postdata['yoast_wpseo_linkdex'] = soup.find('input', {'name': 'yoast_wpseo_linkdex'})['value']
            postdata['yoast_wpseo_content_score'] = soup.find('input', {'name': 'yoast_wpseo_content_score'})['value']
            postdata['yoast_wpseo_is_cornerstone'] = soup.find('input', {'name': 'yoast_wpseo_is_cornerstone'})['value']
            postdata['yoast_wpseo_primary_category_term'] = soup.find('input', {'name': 'yoast_wpseo_primary_category_term'})['value']
            postdata['yoast_wpseo_primary_category_nonce'] = soup.find('input', {'name': 'yoast_wpseo_primary_category_nonce'})['value']
            postdata['yoast_wpseo_primary_internal-type_term'] = soup.find('input', {'name': 'yoast_wpseo_primary_internal-type_term'})['value']
            ##print('debug2')
            postdata['yoast_wpseo_primary_internal-type_nonce'] = soup.find('input', {'name': 'yoast_wpseo_primary_internal-type_nonce'})['value']
            postdata['yoast_wpseo_primary_internal-residence_term'] = soup.find('input', {'name': 'yoast_wpseo_primary_internal-residence_term'})['value']
            postdata['yoast_wpseo_primary_internal-residence_nonce'] = soup.find('input', {'name': 'yoast_wpseo_primary_internal-residence_nonce'})['value']
            postdata['yoast_wpseo_primary_internal-location_term'] = soup.find('input', {'name': 'yoast_wpseo_primary_internal-location_term'})['value']
            postdata['yoast_wpseo_primary_internal-location_nonce'] = soup.find('input', {'name': 'yoast_wpseo_primary_internal-location_nonce'})['value']
            ##print('debug3')
            postdata['screen'] = 'mobile'
            postdata['yoast_wpseo_opengraph-title'] = ''
            postdata['yoast_wpseo_opengraph-description'] = ''
            postdata['yoast_wpseo_opengraph-image'] = ''
            postdata['yoast_wpseo_opengraph-image-id'] = ''
            postdata['yoast_wpseo_twitter-title'] = ''
            postdata['yoast_wpseo_twitter-description'] = ''
            postdata['yoast_wpseo_twitter-image'] = ''
            postdata['yoast_wpseo_twitter-image-id'] = ''
            postdata['type'] = 'rent'
            if data['listing_type'] == 'ขาย':
                postdata['type'] = 'sale'
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
            property_tp = {'1': 'condo',
                           '2': 'house',
                           '3': 'townhouse',
                           '4': 'townhouse',
                           '5': 'commercial',
                           '6': 'land',
                           '7': 'apartment',
                           '8': 'hotel',
                           '9': 'commercial',
                           '10': 'condo',
                           '25': 'condo'}
            if str(data['property_type']) in property_tp:
                postdata['residence'] = property_tp[str(data['property_type'])]
            else:
                postdata['residence'] = property_tp[ids[str(data['property_type'])]]

            postdata['rai'] = data['land_size_rai']
            postdata['ngan'] = data['land_size_ngan']
            postdata['sqwa'] = data['land_size_wa']

            postdata['area'] = data['floor_area']
            postdata['bed'] = data['bed_room']
            postdata['bath'] = data['bath_room']
            if postdata['residence'] == 'condo':
                postdata['floor'] = data['floor_level']
            elif postdata['residence'] == 'land':
                postdata['floor'] = ''
            else:
                postdata['floor'] = data['floor_total']
            postdata['price'] = data['price_baht']
            if 'web_project_name' not in data or data['web_project_name'] is None or str(
                    data['web_project_name']).strip() == "":
                if 'project_name' not in data or data['project_name'] is None or str(
                        data['project_name']).strip() == '':
                    data['web_project_name'] = data['post_title_th']
                else:
                    data['web_project_name'] = data['project_name']
            project_name = ''.join(map(str, str(data['web_project_name']).split(' ')))
            ##print('here')
            with open('./static/postproperty_project.json') as data1_file:
                proj_data = json.load(data1_file)

            projects = proj_data['names']
            ##print(len(projects))
            postdata['project_id'] = ''
            postdata['project'] = ''
            for i in range(len(projects)):
                if str(projects[i]["label"]).find(data['web_project_name']) != -1 or data['web_project_name'].find(str(projects[i]["label"])) != -1:
                    postdata['project_id'] = str(projects[i]["ID"])
                    postdata['project'] = projects[i]["label"]
                    break
            if postdata['project_id'] == '':
                postdata['project'] = data['web_project_name']
                postdata['location_id'] = ''
                url = 'https://post-property.com/wp-admin/post-new.php'
                req = self.httprequestObj.http_get(url,headers=headers)
                provinces = []
                prov_id = []
                data['addr_province'] = ''.join(map(str, str(data['addr_province']).split(' ')))
                data['addr_district'] = ''.join(map(str, str(data['addr_district']).split(' ')))
                data['addr_sub_district'] = ''.join(map(str, str(data['addr_sub_district']).split(' ')))
                provs = soup.find('div',{'class':'step-pane province'}).findAll('li')
                for prov in provs:
                    provinces.append(str(prov.find('a').text))
                    prov_id.append(str(prov.find('a')['type']))
                loc_id = ''
                for i in range(len(provinces)):
                    if (provinces[i].replace(' ','')).find(data['addr_province'])!=-1 or data['addr_province'].find(provinces[i].replace(' ',''))!=-1:
                        loc_id = prov_id[i]
                        break
                if loc_id == '':
                    loc_id = prov_id[0]

                url = 'https://post-property.com/wp-admin/admin-ajax.php'
                req = self.httprequestObj.http_post(url,data={'action':'get_district','location_id':loc_id},headers=headers)

                soup = BeautifulSoup(req.text,'html.parser')
                districts = soup.findAll('a')
                dist_id = []
                for dist in districts:
                    dist_id.append(str(dist['type']).replace('"','').replace('\\','').replace("'",""))
                    ##print('dist')
                    txt = str(dist.text).replace(' ','')
                    ind = 0
                    d = ''
                    while txt[ind]!='<':
                        d+=txt[ind]
                        ind+=1
                    d = (d).encode().decode("unicode-escape")
                    ##print(d)
                    if d.find(data['addr_district'])!=-1 or data['addr_district'].find(d)!=-1:
                        postdata['location_id'] = str(dist['type']).replace('"','').replace('\\','').replace("'","")
                        break
                ##print(dist_id)
                if postdata['location_id'] == '':
                    postdata['location_id'] = dist_id[0]
                ##print(postdata['location_id'])




            else:
                postdata['location_id'] = ''

            if 'post_images' in data and len(data['post_images']) > 0:
                pass
            else:
                data['post_images'] = ['./imgtmp/default/white.jpg']

            temp = 1
            files = {}
            postdata['attachment_id[]'] = []
            postdata['media_full_url[]'] = []
            postdata['media_thumbnail_url[]'] = []

            if len(data['post_images']) <= 20:
                ##print('images')
                for i in data['post_images']:
                    y = str(random.randint(0, 100000000000000000)) + ".jpg"
                    # files = []
                    r = open(os.getcwd() + '/' + i, 'rb')
                    # files.append((str('async-upload'), (y, open(i, "rb"), ".jpg")))
                    # files['async-upload'] = r
                    files = {'async-upload': r}
                    imgdata = {
                        'name': y,
                        'action': 'upload-attachment',
                        '_wpnonce': nonce,
                        'post_id': post_id
                    }
                    ##print(imgdata)

                    response = self.httprequestObj.http_post('https://post-property.com/wp-admin/async-upload.php',
                                                        data=imgdata, files=files)

                    txt = str(response.text)
                    id = ''
                    full = ''
                    thumbnail = ''
                    ind = txt.find('"id"') + 5
                    while txt[ind] != ',':
                        id += txt[ind]
                        ind += 1
                    ind = txt.find('thumbnail')
                    txt = txt[ind:]
                    ind = txt.find('url') + 6
                    while txt[ind] != '"':
                        thumbnail += txt[ind]
                        ind += 1
                    ind = txt.find('full')
                    txt = txt[ind:]
                    ind = txt.find('url') + 6
                    while txt[ind] != '"':
                        full += txt[ind]
                        ind += 1
                    full = full.replace("\\", "")
                    thumbnail = thumbnail.replace("\\", "")
                    postdata['attachment_id[]'].append(id)
                    postdata['media_full_url[]'].append(full)
                    postdata['media_thumbnail_url[]'].append(thumbnail)
                    temp = temp + 1
                ##print('done')

            else:
                for i in data['post_images'][:20]:
                    ##print('images')
                    for i in data['post_images']:
                        y = str(random.randint(0, 100000000000000000)) + ".jpg"
                        # files = []
                        r = open(os.getcwd() + '/' + i, 'rb')
                        # files.append((str('async-upload'), (y, open(i, "rb"), ".jpg")))
                        # files['async-upload'] = r
                        files = {'async-upload': r}
                        imgdata = {
                            'name': y,
                            'action': 'upload-attachment',
                            '_wpnonce': nonce,
                            'post_id': post_id
                        }
                        ##print(imgdata)

                        response = self.httprequestObj.http_post('https://post-property.com/wp-admin/async-upload.php',
                                                            data=imgdata, files=files)

                        txt = str(response.text)
                        id = ''
                        full = ''
                        thumbnail = ''
                        ind = txt.find('"id"') + 5
                        while txt[ind] != ',':
                            id += txt[ind]
                            ind += 1
                        ind = txt.find('thumbnail')
                        txt = txt[ind:]
                        ind = txt.find('url') + 6
                        while txt[ind] != '"':
                            thumbnail += txt[ind]
                            ind += 1
                        ind = txt.find('full')
                        txt = txt[ind:]
                        ind = txt.find('url') + 6
                        while txt[ind] != '"':
                            full += txt[ind]
                            ind += 1
                        full = full.replace("\\", "")
                        thumbnail = thumbnail.replace("\\", "")
                        postdata['attachment_id[]'].append(id)
                        postdata['media_full_url[]'].append(full)
                        postdata['media_thumbnail_url[]'].append(thumbnail)
                        temp = temp + 1
                    ##print('done')
            ##print(postdata['attachment_id[]'])
            ##print(postdata['media_full_url[]'])
            ##print(postdata['media_thumbnail_url[]'])

            url = 'https://post-property.com/wp-admin/post.php'
            req = self.httprequestObj.http_post(url,data=postdata,headers=headers)
            txt = str(req.text)
            soup = BeautifulSoup(req.text,'html.parser')
            post_url = str(soup.find('li',{'id':'wp-admin-bar-view'}).find('a')['href'])

            if txt.find('ลงประกาศเสร็จเรียบร้อยแล้ว')!=-1:
                success = 'true'
                detail = 'Post created'
            else:
                success = 'false'
                detail = 'Some error occured'












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
                  'websitename': 'postproperty'}
        return result

    def delete_post(self,data):
        test_login = self.test_login(data)
        success = test_login["success"]
        start_time = datetime.datetime.utcnow()
        end_time = datetime.datetime.utcnow()
        post_id = str(data["post_id"])
        detail = test_login["detail"]

        if success == "true":
            url = 'https://post-property.com/wp-admin/post.php?post='+ post_id +'&action=edit'
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
            }
            req = self.httprequestObj.http_get(url, headers=headers)
            soup = BeautifulSoup(req.text, 'html5lib')
            try:
                owner_id_chk = soup.find('h1', attrs={'class': 'wp-heading-inline'})
                if ("ประกาศ" in str(owner_id_chk.text)):
                    delete_a = soup.find('a', attrs={'class': 'submitdelete deletion'})
                    delete_link = delete_a['href']
                    req = self.httprequestObj.http_get(delete_link, headers=headers)
                    success = 'true'
                    detail = 'Post deleted'
                else:
                    success = 'false'
                    detail = "Post not found"
            except:
                success = 'false'
                detail = "Cannot find post_id"

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
            "websitename": "postproperty"
        }
        return result

    def search_post(self, data):
        ###print('in')
        test_login = self.test_login(data)
        success = test_login["success"]
        start_time = datetime.datetime.utcnow()
        end_time = datetime.datetime.utcnow()
        post_title = str(data["post_title_th"])
        detail = test_login["detail"]
        post_id = ''
        post_url = ''
        post_found = ''

        if success == "true":
            url = 'https://post-property.com/wp-admin/edit.php'

            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
            }
            req = self.httprequestObj.http_get(url, headers=headers)
            soup = BeautifulSoup(req.text,'html.parser')
            valid_ids = []
            valid_titles = []
            valid_urls = []
            total_pages = int(soup.find('span',attrs={'class':'total-pages'}).text)
            ##print(total_pages)


            for page_no in range(total_pages):
                url = 'https://post-property.com/wp-admin/edit.php?paged='+str(page_no+1)
                req = self.httprequestObj.http_get(url,headers=headers)
                soup = BeautifulSoup(req.text, 'html5lib')
                posts = soup.find('tbody', {'id': 'the-list'}).findAll('tr')
                for post in posts:
                    valid_ids.append(str(post['id'])[5:])
                    valid_urls.append(str(post.find('a')['href']))
                    valid_titles.append(str(post.find('a',{'class':'row-title'}).text))
            #print(valid_ids)
            ##print(valid_titles)
            ##print((valid_urls))

            if post_title in valid_titles:
                for i in range(len(valid_titles)):
                    if valid_titles[i] == post_title:
                        post_id = valid_ids[i]
                        post_url = valid_urls[i]
                        break
                success=True
                post_found = 'true'
                detail = 'Post found'
            else:
                success = False
                post_found = 'false'
                detail = 'Post not found'

        end_time = datetime.datetime.utcnow()
        result = {
            "success": success,
            "usage_time": str(end_time - start_time),
            "start_time": str(start_time),
            "end_time": str(end_time),
            "detail": detail,
            'ds_id': data['ds_id'],
            "log_id": data['log_id'],
            "post_found": post_found,
            "post_id": post_id,
            'post_url': post_url,
            "post_create_time": '',
            "post_modify_time": '',
            "post_view": '',
            'websitename': 'postproperty'
        }
        return result

    def boost_post(self, data):
        start_time = datetime.datetime.utcnow()
        # ##print('start')
        post_id = str(data['post_id'])
        log_id = str(data['log_id'])
        result = self.test_login(data)
        success = result['success']
        detail = result['detail']

        if success == 'true':
            url = 'https://post-property.com/wp-admin/edit.php'
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
            }
            req = self.httprequestObj.http_get(url, headers=headers)
            valid_ids = []
            soup = BeautifulSoup(req.text, 'html5lib')
            total_pages = int(soup.find('span', attrs={'class': 'total-pages'}).text)
            # #print(total_pages)

            for page_no in range(total_pages):
                url = 'https://post-property.com/wp-admin/edit.php?paged=' + str(page_no + 1)
                req = self.httprequestObj.http_get(url, headers=headers)
                soup = BeautifulSoup(req.text, 'html5lib')
                posts = soup.find('tbody', {'id': 'the-list'}).findAll('tr')
                for post in posts:
                    valid_ids.append(str(post['id'])[5:])

            #print(valid_ids)

            if post_id in valid_ids:

                success = 'true'
                detail = 'Post edited and saved'
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
            'websitename': 'postproperty'
        }
        # https://ilovecondo.net/new-post/topicid/910653/trk/78
        return result
    def edit_post(self, data):
        # ลงประกาศเสร็จเรียบร้อยแล้ว
        ##print('in')
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
            ##print('login')
            postdata = {}
            url = 'https://post-property.com/wp-admin/post.php?post='+post_id+'&action=edit'
            req = self.httprequestObj.http_get(url,headers=headers)
            txt = str(req.text)
            ##print(txt)
            if txt.find('คุณพยายามแก้ไขสิ่งที่ไม่มีอยู่  บางทีมันอาจถูกลบไปแล้ว?')==-1:
                soup = BeautifulSoup(req.text,'html.parser')
                ##print('start1')
                postdata['_wpnonce'] = soup.find('input',{'name':'_wpnonce'})['value']
                ##print(postdata['_wpnonce'])
                txt = str(req.text)
                ind = txt.find('"action":"upload-attachment","_wpnonce":"')+41
                ##print(ind)
                nonce = ''
                ##print(data['addr_province'])
                ##print(data['addr_district'])
                while txt[ind]!='"':
                    nonce += txt[ind]
                    ind+=1
                ##print(nonce)
                postdata['_wp_http_referer'] = soup.find('input',{'name':'_wp_http_referer'})['value']
                postdata['user_ID'] = soup.find('input',{'name':'user_ID'})['value']
                postdata['action'] = soup.find('input',{'name':'action'})['value']
                postdata['originalaction'] = soup.find('input',{'name':'originalaction'})['value']
                postdata['post_author'] = soup.find('input',{'name':'post_author'})['value']
                postdata['post_type'] = soup.find('input',{'name':'post_type'})['value']
                postdata['original_post_status'] = soup.find('input',{'name':'original_post_status'})['value']
                postdata['referredby'] = soup.find('input',{'name':'referredby'})['value']
                postdata['_wp_original_http_referer'] = soup.find('input',{'name':'_wp_original_http_referer'})['value']
                #postdata['auto_draft'] = soup.find('input',{'name':'auto_draft'})['value']
                postdata['post_ID'] = post_id
                post_id = str(postdata['post_ID'])
                ##print(post_id)
                postdata['meta-box-order-nonce'] = soup.find('input',{'name':'meta-box-order-nonce'})['value']
                postdata['closedpostboxesnonce'] = soup.find('input',{'name':'closedpostboxesnonce'})['value']
                postdata['post_title'] = data['post_title_th']
                postdata['samplepermalinknonce'] = soup.find('input', {'name': 'samplepermalinknonce'})['value']
                postdata['content'] = str(data['post_description_th'])
                postdata['wp-preview'] = soup.find('input', {'name': 'wp-preview'})['value']
                postdata['hidden_post_status'] = soup.find('input', {'name': 'hidden_post_status'})['value']
                postdata['post_status'] = 'draft'
                postdata['hidden_post_password'] = soup.find('input', {'name': 'hidden_post_password'})['value']
                postdata['hidden_post_visibility'] = soup.find('input', {'name': 'hidden_post_visibility'})['value']
                #postdata['hidden_post_password'] = soup.find('input', {'name': 'hidden_post_password'})['value']
                postdata['visibility'] = 'public'
                postdata['post_password'] = ''
                postdata['jj'] = soup.find('input', {'name': 'jj'})['value']
                options = soup.find('select',{'name':'mm'}).findAll('option')
                ##print('debug1')
                for opt in options:
                    if opt.has_attr('selected'):
                        postdata['mm'] = opt['value']
                        break
                postdata['aa'] = soup.find('input', {'name': 'aa'})['value']
                postdata['hh'] = soup.find('input', {'name': 'hh'})['value']
                postdata['mn'] = soup.find('input', {'name': 'mn'})['value']
                postdata['ss'] = soup.find('input', {'name': 'ss'})['value']
                postdata['hidden_mm'] = soup.find('input', {'name': 'hidden_mm'})['value']
                postdata['cur_mm'] = soup.find('input', {'name': 'cur_mm'})['value']
                postdata['hidden_jj'] = soup.find('input', {'name': 'hidden_jj'})['value']
                postdata['cur_jj'] = soup.find('input', {'name': 'cur_jj'})['value']
                postdata['hidden_aa'] = soup.find('input', {'name': 'hidden_aa'})['value']
                postdata['cur_aa'] = soup.find('input', {'name': 'cur_aa'})['value']
                postdata['hidden_hh'] = soup.find('input', {'name': 'hidden_hh'})['value']
                postdata['cur_hh'] = soup.find('input', {'name': 'cur_hh'})['value']
                postdata['hidden_mn'] = soup.find('input', {'name': 'hidden_mn'})['value']
                postdata['cur_mn'] = soup.find('input', {'name': 'cur_mn'})['value']
                postdata['pvc_nonce'] = soup.find('input', {'name': 'pvc_nonce'})['value']
                postdata['amp-status-nonce'] = soup.find('input', {'name': 'amp-status-nonce'})['value']
                postdata['original_publish'] = soup.find('input', {'name': 'original_publish'})['value']
                postdata['publish'] = 'อัปเดต'
                ##print('mid')
                postdata['_thumbnail_id'] = soup.find('input', {'name': '_thumbnail_id'})['value']
                postdata['yoast_free_metabox_nonce'] = soup.find('input', {'name': 'yoast_free_metabox_nonce'})['value']
                postdata['yoast_free_metabox_social_nonce'] = '' #soup.find('input', {'name': 'yoast_free_metabox_social_nonce'})['value']
                postdata['yoast_wpseo_focuskw'] = soup.find('input', {'name': 'yoast_wpseo_focuskw'})['value']
                postdata['yoast_wpseo_title'] = soup.find('input', {'name': 'yoast_wpseo_title'})['value']
                postdata['yoast_wpseo_metadesc'] = soup.find('input', {'name': 'yoast_wpseo_metadesc'})['value']
                postdata['yoast_wpseo_linkdex'] = soup.find('input', {'name': 'yoast_wpseo_linkdex'})['value']
                postdata['yoast_wpseo_content_score'] = soup.find('input', {'name': 'yoast_wpseo_content_score'})['value']
                postdata['yoast_wpseo_is_cornerstone'] = soup.find('input', {'name': 'yoast_wpseo_is_cornerstone'})['value']
                postdata['yoast_wpseo_primary_category_term'] = soup.find('input', {'name': 'yoast_wpseo_primary_category_term'})['value']
                postdata['yoast_wpseo_primary_category_nonce'] = soup.find('input', {'name': 'yoast_wpseo_primary_category_nonce'})['value']
                postdata['yoast_wpseo_primary_internal-type_term'] = soup.find('input', {'name': 'yoast_wpseo_primary_internal-type_term'})['value']
                ##print('debug2')
                postdata['yoast_wpseo_primary_internal-type_nonce'] = soup.find('input', {'name': 'yoast_wpseo_primary_internal-type_nonce'})['value']
                postdata['yoast_wpseo_primary_internal-residence_term'] = soup.find('input', {'name': 'yoast_wpseo_primary_internal-residence_term'})['value']
                postdata['yoast_wpseo_primary_internal-residence_nonce'] = soup.find('input', {'name': 'yoast_wpseo_primary_internal-residence_nonce'})['value']
                postdata['yoast_wpseo_primary_internal-location_term'] = soup.find('input', {'name': 'yoast_wpseo_primary_internal-location_term'})['value']
                postdata['yoast_wpseo_primary_internal-location_nonce'] = soup.find('input', {'name': 'yoast_wpseo_primary_internal-location_nonce'})['value']
                ##print('debug3')
                postdata['screen'] = 'mobile'
                postdata['yoast_wpseo_opengraph-title'] = ''
                postdata['yoast_wpseo_opengraph-description'] = ''
                postdata['yoast_wpseo_opengraph-image'] = ''
                postdata['yoast_wpseo_opengraph-image-id'] = ''
                postdata['yoast_wpseo_twitter-title'] = ''
                postdata['yoast_wpseo_twitter-description'] = ''
                postdata['yoast_wpseo_twitter-image'] = ''
                postdata['yoast_wpseo_twitter-image-id'] = ''
                postdata['type'] = 'rent'
                if data['listing_type'] == 'ขาย':
                    postdata['type'] = 'sale'
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
                property_tp = {'1': 'condo',
                               '2': 'house',
                               '3': 'townhouse',
                               '4': 'townhouse',
                               '5': 'commercial',
                               '6': 'land',
                               '7': 'apartment',
                               '8': 'hotel',
                               '9': 'commercial',
                               '10': 'condo',
                               '25': 'condo'}
                if str(data['property_type']) in property_tp:
                    postdata['residence'] = property_tp[str(data['property_type'])]
                else:
                    postdata['residence'] = property_tp[ids[str(data['property_type'])]]

                postdata['rai'] = data['land_size_rai']
                postdata['ngan'] = data['land_size_ngan']
                postdata['sqwa'] = data['land_size_wa']

                postdata['area'] = data['floor_area']
                postdata['bed'] = data['bed_room']
                postdata['bath'] = data['bath_room']
                if postdata['residence'] == 'condo':
                    postdata['floor'] = data['floor_level']
                elif postdata['residence'] == 'land':
                    postdata['floor'] = ''
                else:
                    postdata['floor'] = data['floor_total']
                postdata['price'] = data['price_baht']
                if 'web_project_name' not in data or data['web_project_name'] is None or str(
                        data['web_project_name']).strip() == "":
                    if 'project_name' not in data or data['project_name'] is None or str(
                            data['project_name']).strip() == '':
                        data['web_project_name'] = data['post_title_th']
                    else:
                        data['web_project_name'] = data['project_name']
                project_name = ''.join(map(str, str(data['web_project_name']).split(' ')))
                ##print('here')
                with open('./static/postproperty_project.json') as data1_file:
                    proj_data = json.load(data1_file)

                projects = proj_data['names']
                ##print(len(projects))
                postdata['project_id'] = ''
                postdata['project'] = ''
                for i in range(len(projects)):
                    if str(projects[i]["label"]).find(data['web_project_name']) != -1 or data['web_project_name'].find(str(projects[i]["label"])) != -1:
                        postdata['project_id'] = str(projects[i]["ID"])
                        postdata['project'] = projects[i]["label"]
                        break
                if postdata['project_id'] == '':
                    postdata['project'] = data['web_project_name']
                    postdata['location_id'] = ''
                    url = 'https://post-property.com/wp-admin/post.php?post=' + post_id + '&action=edit'
                    req = self.httprequestObj.http_get(url,headers=headers)
                    provinces = []
                    prov_id = []
                    data['addr_province'] = ''.join(map(str, str(data['addr_province']).split(' ')))
                    data['addr_district'] = ''.join(map(str, str(data['addr_district']).split(' ')))
                    data['addr_sub_district'] = ''.join(map(str, str(data['addr_sub_district']).split(' ')))
                    provs = soup.find('div',{'class':'step-pane province'}).findAll('li')
                    for prov in provs:
                        provinces.append(str(prov.find('a').text))
                        prov_id.append(str(prov.find('a')['type']))
                    loc_id = ''
                    for i in range(len(provinces)):
                        if (provinces[i].replace(' ','')).find(data['addr_province'])!=-1 or data['addr_province'].find(provinces[i].replace(' ',''))!=-1:
                            loc_id = prov_id[i]
                            break
                    if loc_id == '':
                        loc_id = prov_id[0]

                    url = 'https://post-property.com/wp-admin/admin-ajax.php'
                    req = self.httprequestObj.http_post(url,data={'action':'get_district','location_id':loc_id},headers=headers)

                    soup = BeautifulSoup(req.text,'html.parser')
                    districts = soup.findAll('a')
                    dist_id = []
                    for dist in districts:
                        dist_id.append(str(dist['type']).replace('"','').replace('\\','').replace("'",""))
                        ##print('dist')
                        txt = str(dist.text).replace(' ','')
                        ind = 0
                        d = ''
                        while txt[ind]!='<':
                            d+=txt[ind]
                            ind+=1
                        d = (d).encode().decode("unicode-escape")
                        ##print(d)
                        if d.find(data['addr_district'])!=-1 or data['addr_district'].find(d)!=-1:
                            postdata['location_id'] = str(dist['type']).replace('"','').replace('\\','').replace("'","")
                            break
                    ##print(dist_id)
                    if postdata['location_id'] == '':
                        postdata['location_id'] = dist_id[0]
                    ##print(postdata['location_id'])




                else:
                    postdata['location_id'] = ''

                if 'post_images' in data and len(data['post_images']) > 0:
                    pass
                else:
                    data['post_images'] = ['./imgtmp/default/white.jpg']

                temp = 1
                files = {}
                postdata['attachment_id[]'] = []
                postdata['media_full_url[]'] = []
                postdata['media_thumbnail_url[]'] = []

                if len(data['post_images']) <= 20:
                    ##print('images')
                    for i in data['post_images']:
                        y = str(random.randint(0, 100000000000000000)) + ".jpg"
                        # files = []
                        r = open(os.getcwd() + '/' + i, 'rb')
                        # files.append((str('async-upload'), (y, open(i, "rb"), ".jpg")))
                        # files['async-upload'] = r
                        files = {'async-upload': r}
                        imgdata = {
                            'name': y,
                            'action': 'upload-attachment',
                            '_wpnonce': nonce,
                            'post_id': post_id
                        }
                        ##print(imgdata)

                        response = self.httprequestObj.http_post('https://post-property.com/wp-admin/async-upload.php',
                                                            data=imgdata, files=files)

                        txt = str(response.text)
                        id = ''
                        full = ''
                        thumbnail = ''
                        ind = txt.find('"id"') + 5
                        while txt[ind] != ',':
                            id += txt[ind]
                            ind += 1
                        ind = txt.find('thumbnail')
                        txt = txt[ind:]
                        ind = txt.find('url') + 6
                        while txt[ind] != '"':
                            thumbnail += txt[ind]
                            ind += 1
                        ind = txt.find('full')
                        txt = txt[ind:]
                        ind = txt.find('url') + 6
                        while txt[ind] != '"':
                            full += txt[ind]
                            ind += 1
                        full = full.replace("\\", "")
                        thumbnail = thumbnail.replace("\\", "")
                        postdata['attachment_id[]'].append(id)
                        postdata['media_full_url[]'].append(full)
                        postdata['media_thumbnail_url[]'].append(thumbnail)
                        temp = temp + 1
                    ##print('done')

                else:
                    for i in data['post_images'][:20]:
                        ##print('images')
                        for i in data['post_images']:
                            y = str(random.randint(0, 100000000000000000)) + ".jpg"
                            # files = []
                            r = open(os.getcwd() + '/' + i, 'rb')
                            # files.append((str('async-upload'), (y, open(i, "rb"), ".jpg")))
                            # files['async-upload'] = r
                            files = {'async-upload': r}
                            imgdata = {
                                'name': y,
                                'action': 'upload-attachment',
                                '_wpnonce': nonce,
                                'post_id': post_id
                            }
                            ##print(imgdata)

                            response = self.httprequestObj.http_post('https://post-property.com/wp-admin/async-upload.php',
                                                                data=imgdata, files=files)

                            txt = str(response.text)
                            id = ''
                            full = ''
                            thumbnail = ''
                            ind = txt.find('"id"') + 5
                            while txt[ind] != ',':
                                id += txt[ind]
                                ind += 1
                            ind = txt.find('thumbnail')
                            txt = txt[ind:]
                            ind = txt.find('url') + 6
                            while txt[ind] != '"':
                                thumbnail += txt[ind]
                                ind += 1
                            ind = txt.find('full')
                            txt = txt[ind:]
                            ind = txt.find('url') + 6
                            while txt[ind] != '"':
                                full += txt[ind]
                                ind += 1
                            full = full.replace("\\", "")
                            thumbnail = thumbnail.replace("\\", "")
                            postdata['attachment_id[]'].append(id)
                            postdata['media_full_url[]'].append(full)
                            postdata['media_thumbnail_url[]'].append(thumbnail)
                            temp = temp + 1
                        ##print('done')
                ##print(postdata['attachment_id[]'])
                ##print(postdata['media_full_url[]'])
                ##print(postdata['media_thumbnail_url[]'])

                url = 'https://post-property.com/wp-admin/post.php'
                req = self.httprequestObj.http_post(url,data=postdata,headers=headers)
                txt = str(req.text)
                soup = BeautifulSoup(req.text,'html.parser')
                post_url = str(soup.find('li',{'id':'wp-admin-bar-view'}).find('a')['href'])

                success = 'true'
                detail = 'Post edited'
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
                  'ds_id': data['ds_id'],
                  'log_id':data['log_id'],
                  'detail': detail,
                  'websitename': 'postproperty'}
        return result