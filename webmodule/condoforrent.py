import requests, re, random
from bs4 import BeautifulSoup
import json, datetime
from .lib_httprequest import *
httprequestObj = lib_httprequest()

class condoforrent:

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
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}
        success = 'true'
        detail = ''
        postdata = {}
        postdata['username'] = data['user'].split('@')[0]
        postdata['pass'] = postdata['conpass'] = data['pass']
        postdata['line'] = data['line']
        postdata['email'] = data['user']
        postdata['name'] = data['name_th']
        #postdata['lastname'] = data['surname_th']
        postdata['phone'] = data['tel']
        #postdata['address'] = 'พญาไท,กรุงเทพ'
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
        if postdata['username'] == '' or postdata['pass'] == '' or postdata['name'] == '' or postdata['phone'] == '':
            success = 'false'
            detail = 'Empty credentials'
        if success == 'true':
            url = 'http://xn--42cm3at5gj3b0hpal2dj.com/signup_member.php'
            req = httprequestObj.http_post(url, data=postdata, headers=headers)
            txt = str(req.text)
            if txt.find('สมัครสมาชิกเรียบร้อยแล้ว') == -1:
                success = 'false'
                detail = 'Already a user'
            else:
                success = 'true'
                detail = 'Successfully Registered'
        end_time = datetime.datetime.utcnow()
        result = {'websitename':'condoforrent',
         'success':success,
         'start_time':str(start_time),
         'end_time':str(end_time),
         'usage_time':str(end_time - start_time),
         'detail':detail,
         'ds_id':data['ds_id']}
        return result

    def test_login(self, data):
        start_time = datetime.datetime.utcnow()
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}
        postdata = {}
        postdata['log_u'] = data['user']
        postdata['log_p'] = data['pass']
        postdata['submit'] = ''
        success = ''
        detail = ''
        url = 'http://xn--42cm3at5gj3b0hpal2dj.com/login.php'
        req = httprequestObj.http_post(url, data=postdata, headers=headers)
        txt = req.text
        if txt.find('Username หรือ Password ไม่ถูกต้อง') == -1:
            success = 'true'
            detail = 'Successfully login'
        else:
            success = 'false'
            detail = 'User not registered yet'
        end_time = datetime.datetime.utcnow()
        result = {'websitename':'condoforrent',
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
            property_tp = {'1':'2',
                           '2':'3',
                           '3':'3',
                           '4':'3',
                           '5':'3',
                           '6':'3',
                           '7':'3',
                           '8':'3',
                           '9':'3',
                           '10':'3',
                           '25':'3'}
            ##print(str(data['property_type']))
            if str(data['property_type']) in ids:
                postdata['section'] = property_tp[ids[str(data['property_type'])]]
            else:
                postdata['section'] = property_tp[str(data['property_type'])]
            ##print(postdata['section'])
            if postdata['section'] == '3':
                post_url = ''
                success = 'false'
                detail = 'only condo applicable'
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
                          'websitename': 'condoforrent'}
                return result
            postdata['number'] = data['addr_near_by']
            address = []
            postdata['soi'] = data['addr_soi']
            postdata['road'] = data['addr_road']
            if postdata['road'] is not None and postdata['road']!='':
                address.append(postdata['road'])

            data['addr_province'] = ''.join(map(str, str(data['addr_province']).split(' ')))
            data['addr_district'] = ''.join(map(str, str(data['addr_district']).split(' ')))
            data['addr_sub_district'] = ''.join(map(str, str(data['addr_sub_district']).split(' ')))
            postdata['Province'] = ''
            req = httprequestObj.http_get_with_headers('http://xn--42cm3at5gj3b0hpal2dj.com/add_property.php', headers=headers)
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
                    if provinces[i].find(data['addr_province']) != -1 or data['addr_province'].find(provinces[i]) != -1:
                        postdata['Province'] = ids[i]
                        break

            if postdata['Province'] == '':
                postdata['Province'] = ids[0]
            postdata['District'] = ''
            url = 'http://xn--42cm3at5gj3b0hpal2dj.com/getaddress.php?ID=' + str(postdata['Province']) + '&TYPE=District'
            req = httprequestObj.http_get_with_headers(url, headers=headers)
            txt = str(req.text)
            districts = []
            ids = []
            while txt.find('AMPHUR_ID') != -1:
                ind = txt.find('AMPHUR_ID')
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
                ind = txt.find('AMPHUR_NAME')
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
                    if districts[i].find(data['addr_district']) != -1 or data['addr_district'].find(districts[i]) != -1:
                        postdata['District'] = ids[i]
                        break

            if postdata['District'] == '':
                postdata['District'] = ids[0]
            postdata['Subdistrict'] = ''
            url = 'http://xn--42cm3at5gj3b0hpal2dj.com/getaddress.php?ID=' + str(postdata['District']) + '&TYPE=Subdistrict'
            req = httprequestObj.http_get_with_headers(url, headers=headers)
            txt = str(req.text)
            subdistricts = []
            ids = []
            while txt.find('DISTRICT_ID') != -1:
                ind = txt.find('DISTRICT_ID')
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
                ind = txt.find('DISTRICT_NAME')
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
                    if subdistricts[i].find(data['addr_sub_district']) != -1 or data['addr_sub_district'].find(subdistricts[i]) != -1:
                        postdata['Subdistrict'] = ids[i]
                        break

            if postdata['Subdistrict'] == '':
                postdata['Subdistrict'] = ids[0]
            ##print('sub')
            address.append(data['addr_sub_district'])
            address.append(data['addr_district'])
            address.append(data['addr_province'])
            adrs = ''
            for i in range(len(address)):
                if i != len(address)-1:
                    adrs += address[i]
                    adrs += ' , '
                else:
                    adrs += address[i]
            postdata['number'] = adrs
            #print(adrs)
            postdata['price'] = str(data['price_baht'])

            postdata['area'] = data['floor_area']


            #postdata['area'] = str( + str(data['land_size_ngan'])+'งาน' + str(data['land_size_wa'])+'ตรว' + str(data['floor_area'])+'ตรม')
            postdata['layer'] = str(data['floor_level'])
            postdata['room'] = str(data['bed_room'])
            postdata['toilet'] = str(data['bath_room'])
            postdata['detail'] = str(data['post_description_th'])
            postdata['Submit'] = 'Add announcement'
            ##print('done')
            try:
                url = 'http://xn--42cm3at5gj3b0hpal2dj.com/add_property.php'
                req = httprequestObj.http_post(url, data=postdata, headers=headers)
                txt = req.text

                if txt.find('.php?id=') == -1:
                    success = 'false'
                    detail = 'Network error'
                else:
                    ind = txt.find('.php?id=') + 8
                    while txt[ind] != '>':
                        post_id += txt[ind]
                        ind += 1

                    post_url = 'http://xn--42cm3at5gj3b0hpal2dj.com/property-' + str(post_id) + '-' + data['post_title_th']
                    post_url = post_url.replace(' ', '-')

                    # map
                    postdata = {
                        'namePlace':'',
                        'lat_value': data['geo_latitude'],
                        'lon_value': data['geo_longitude'],
                        'zoom_value': '13',
                        'ID': str(post_id),
                        'Submit': 'Add map data'
                    }
                    url = 'http://xn--42cm3at5gj3b0hpal2dj.com/add_map.php?id='+str(post_id)
                    req = httprequestObj.http_post(url,data=postdata,headers=headers)

                    imgurl = 'http://xn--42cm3at5gj3b0hpal2dj.com/add_img.php?id='+str(post_id)
                    httprequestObj.http_get(imgurl)
                    if 'post_images' in data:
                        if len(data['post_images']) > 0:
                            pass
                    else:
                        data['post_images'] = [
                            './imgtmp/default/white.jpg']
                    files = {}
                    temp = 1

                    for i in range(len(data['post_images'])):
                        r = open(os.getcwd() + '/' + data['post_images'][i], 'rb')
                        files['photoimg'] = r
                        response = httprequestObj.http_post('http://xn--42cm3at5gj3b0hpal2dj.com/ajax_img.php', data=None, files=files)

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
             'websitename':'condoforrent'}
            return result

    def delete_post(self, postdata):
        test_login = self.test_login(postdata)
        success = test_login['success']
        start_time = datetime.datetime.utcnow()
        end_time = datetime.datetime.utcnow()
        post_id = str(postdata['post_id'])
        detail = test_login['detail']
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}
        url = 'http://xn--42cm3at5gj3b0hpal2dj.com/maneg_property.php'
        valid_ids = []
        req = httprequestObj.http_get_with_headers(url, headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        total_pages = 1
        if soup.find('ul', {'class': 'pagination'}) != None:
            total_pages = len(soup.find('ul', {'class': 'pagination'}).findAll('li'))
            if total_pages > 1:
                total_pages -= 1
        for i in range(total_pages):
            url = 'http://xn--42cm3at5gj3b0hpal2dj.com/maneg_property.php?&page=' + str(i)
            req = httprequestObj.http_get_with_headers(url, headers=headers)
            soup = BeautifulSoup(req.text, 'html.parser')
            posts = soup.find('table', {'class': 'table table-striped'}).find('tbody').findAll('tr')
            for post in posts:
                id = ''
                a = str(post.find('a')['href'])
                ind = a.find('property-') + 9
                while a[ind] != '-':
                    id += a[ind]
                    ind += 1

                valid_ids.append(id)

        ##print(valid_ids)
        if str(post_id) not in valid_ids:
            success = 'false'
            detail = 'Invalid id'
        if success == 'true':
            url = 'http://xn--42cm3at5gj3b0hpal2dj.com/maneg_property.php?delete=' + str(post_id)
            req = httprequestObj.http_get_with_headers(url, headers=headers)
            txt = req.text
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
         'websitename':'condoforrent'}
        return result

    def search_post(self, postdata):
        start_time = datetime.datetime.utcnow()
        test_login = self.test_login(postdata)
        success = test_login['success']
        end_time = datetime.datetime.utcnow()
        post_id = ''
        post_url = ''
        post_views = ''
        detail = test_login['detail']
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}
        url = 'http://xn--42cm3at5gj3b0hpal2dj.com/maneg_property.php'
        valid_ids = []
        valid_titles = []
        urls = []
        views = []
        req = httprequestObj.http_get_with_headers(url, headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        post_found = 'true'
        total_pages = 1
        if soup.find('ul', {'class': 'pagination'}) != None:
            total_pages = len(soup.find('ul', {'class': 'pagination'}).findAll('li'))
            if total_pages > 1:
                total_pages -= 1
        for i in range(total_pages):
            url = 'http://xn--42cm3at5gj3b0hpal2dj.com/maneg_property.php?&page=' + str(i)
            req = httprequestObj.http_get_with_headers(url, headers=headers)
            soup = BeautifulSoup(req.text, 'html.parser')
            posts = soup.find('table', {'class': 'table table-striped'}).find('tbody').findAll('tr')
            for post in posts:
                id = ''
                a = str(post.find('a')['href'])
                urls.append(a)
                ind = a.find('property-') + 9
                while a[ind] != '-':
                    id += a[ind]
                    ind += 1

                valid_ids.append(id)
                ind += 1
                title = ''
                while ind < len(a):
                    title += a[ind]
                    ind += 1

                valid_titles.append(title.strip().replace('-',' '))
                views.append(str(post.find('p',{'class':'gray'}).text).split(' ')[1])

        print(valid_titles)
        print(postdata['post_title_th'].strip().lower())
        ##print(postdata['post_title_th'])
        if postdata['post_title_th'].strip().lower() not in valid_titles:
            post_found = 'false'
            detail = 'Invalid title'
            post_id = ''
        else:
            print('Here')
            post_found = 'true'
            detail = 'Post found'
            for i in range(len(valid_titles)):
                if valid_titles[i] == postdata['post_title_th'].lower():
                    post_url = urls[i]
                    post_id = valid_ids[i]
                    post_views = views[i]
                    break

        end_time = datetime.datetime.utcnow()
        result = {'success':success,
         'usage_time':str(end_time - start_time),
         'start_time':str(start_time),
         'end_time':str(end_time),
         'detail':detail,
         'websitename':'condoforrent',
         'account_type':None,
         'ds_id':postdata['ds_id'],
         'log_id':postdata['log_id'],
         'post_id':post_id,
         'post_url':post_url,
         "post_create_time": '',
         "post_modify_time": '',
         "post_view": post_views,
         'post_found':post_found}
        return result

    def edit_post(self, data):
        start_time = datetime.datetime.utcnow()
        result = self.test_login(data)
        success = result['success']
        detail = result['detail']
        post_url = ''
        post_id = data['post_id']
        if success == 'true':
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}
            url = 'http://xn--42cm3at5gj3b0hpal2dj.com/maneg_property.php'
            valid_ids = []
            req = httprequestObj.http_get_with_headers(url, headers=headers)
            soup = BeautifulSoup(req.text, 'html.parser')
            total_pages = 1
            if soup.find('ul', {'class': 'pagination'}) != None:
                total_pages = len(soup.find('ul', {'class': 'pagination'}).findAll('li'))
                if total_pages > 1:
                    total_pages -= 1
            for i in range(total_pages):
                url = 'http://xn--42cm3at5gj3b0hpal2dj.com/maneg_property.php?&page=' + str(i)
                req = httprequestObj.http_get_with_headers(url, headers=headers)
                soup = BeautifulSoup(req.text, 'html.parser')
                posts = soup.find('table', {'class': 'table table-striped'}).find('tbody').findAll('tr')
                for post in posts:
                    id = ''
                    a = str(post.find('a')['href'])
                    ind = a.find('property-') + 9
                    while a[ind] != '-':
                        id += a[ind]
                        ind += 1

                    valid_ids.append(id)

            ##print(valid_ids)
            if str(post_id) not in valid_ids:
                success = 'false'
                detail = 'Invalid id'
            else:
                postdata = {}
                postdata['name'] = data['post_title_th']

                postdata['cate'] = '2'
                if data['listing_type'] == 'ขาย':
                    postdata['cate'] = '1'
                headers = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}
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
                property_tp = {'1': '2',
                               '2': '3',
                               '3': '3',
                               '4': '3',
                               '5': '3',
                               '6': '3',
                               '7': '3',
                               '8': '3',
                               '9': '3',
                               '10': '3',
                               '25': '3'}
                ##print(str(data['property_type']))
                if str(data['property_type']) in ids:
                    postdata['section'] = property_tp[ids[str(data['property_type'])]]
                else:
                    postdata['section'] = property_tp[str(data['property_type'])]
                ##print(postdata['section'])
                if postdata['section'] == '3':
                    post_url = 'only condo applicable'
                    success = 'false'
                    detail = 'only condo applicable'
                    end_time = datetime.datetime.utcnow()
                    result = {'success': success,
                              'usage_time': str(end_time - start_time),
                              'start_time': str(start_time),
                              'end_time': str(end_time),
                              'post_url': post_url,
                              'post_id': post_id,
                              'account_type': 'null',
                              'ds_id': data['ds_id'],
                              'log_id': data['log_id'],
                              'detail': detail,
                              'websitename': 'condoforrent'}
                    return result
                
                postdata['number'] = data['addr_near_by']
                address = []
                postdata['soi'] = data['addr_soi']
                postdata['road'] = data['addr_road']
                if postdata['road'] is not None and postdata['road'] != '':
                    address.append(postdata['road'])

                data['addr_province'] = ''.join(map(str, str(data['addr_province']).split(' ')))
                data['addr_district'] = ''.join(map(str, str(data['addr_district']).split(' ')))
                data['addr_sub_district'] = ''.join(map(str, str(data['addr_sub_district']).split(' ')))
                postdata['Province'] = ''
                req = httprequestObj.http_get_with_headers('http://xn--42cm3at5gj3b0hpal2dj.com/edit_property.php?id='+str(post_id),
                                                           headers=headers)
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
                        if provinces[i].find(data['addr_province']) != -1 or data['addr_province'].find(
                                provinces[i]) != -1:
                            postdata['Province'] = ids[i]
                            break

                if postdata['Province'] == '':
                    postdata['Province'] = ids[0]
                postdata['District'] = ''
                url = 'http://xn--42cm3at5gj3b0hpal2dj.com/getaddress.php?ID=' + str(
                    postdata['Province']) + '&TYPE=District'
                req = httprequestObj.http_get_with_headers(url, headers=headers)
                txt = str(req.text)
                districts = []
                ids = []
                while txt.find('AMPHUR_ID') != -1:
                    ind = txt.find('AMPHUR_ID')
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
                    ind = txt.find('AMPHUR_NAME')
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
                        if districts[i].find(data['addr_district']) != -1 or data['addr_district'].find(
                                districts[i]) != -1:
                            postdata['District'] = ids[i]
                            break

                if postdata['District'] == '':
                    postdata['District'] = ids[0]
                postdata['Subdistrict'] = ''
                url = 'http://xn--42cm3at5gj3b0hpal2dj.com/getaddress.php?ID=' + str(
                    postdata['District']) + '&TYPE=Subdistrict'
                req = httprequestObj.http_get_with_headers(url, headers=headers)
                txt = str(req.text)
                subdistricts = []
                ids = []
                while txt.find('DISTRICT_ID') != -1:
                    ind = txt.find('DISTRICT_ID')
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
                    ind = txt.find('DISTRICT_NAME')
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
                        if subdistricts[i].find(data['addr_sub_district']) != -1 or data['addr_sub_district'].find(
                                subdistricts[i]) != -1:
                            postdata['Subdistrict'] = ids[i]
                            break

                if postdata['Subdistrict'] == '':
                    postdata['Subdistrict'] = ids[0]
                # #print('sub')
                address.append(data['addr_sub_district'])
                address.append(data['addr_district'])
                address.append(data['addr_province'])
                adrs = ''
                for i in range(len(address)):
                    if i != len(address) - 1:
                        adrs += address[i]
                        adrs += ' , '
                    else:
                        adrs += address[i]
                postdata['number'] = adrs
                #print(adrs)
                postdata['price'] = str(data['price_baht'])
                
                postdata['area'] = data['floor_area']
                
                # postdata['area'] = str( + str(data['land_size_ngan'])+'งาน' + str(data['land_size_wa'])+'ตรว' + str(data['floor_area'])+'ตรม')
                postdata['layer'] = str(data['floor_level'])
                postdata['room'] = str(data['bed_room'])
                postdata['toilet'] = str(data['bath_room'])
                postdata['detail'] = str(data['post_description_th'])
                postdata['ID'] = str(post_id)
                postdata['Submit'] = 'Edit announcement'
                ##print('done')
                try:
                    url = 'http://xn--42cm3at5gj3b0hpal2dj.com/edit_property.php?id='+str(post_id)
                    req = httprequestObj.http_post(url, data=postdata, headers=headers)
                    txt = req.text

                    if txt.find('บันทึกข้อมูลเรียบร้อยแล้ว') == -1:
                        success = 'false'
                        detail = 'Network error'
                    else:


                        post_url = 'http://xn--42cm3at5gj3b0hpal2dj.com/property-' + str(post_id) + '-' + data[
                            'post_title_th']
                        post_url = post_url.replace(' ', '-')

                        # map
                        postdata = {
                            'namePlace': '',
                            'lat_value': data['geo_latitude'],
                            'lon_value': data['geo_longitude'],
                            'zoom_value': '13',
                            'ID': str(post_id),
                            'Submit': 'Edit map data'
                        }
                        url = 'http://xn--42cm3at5gj3b0hpal2dj.com/edit_map.php?id=' + str(post_id)
                        req = httprequestObj.http_post(url, data=postdata, headers=headers)

                        # deleting previous images
                        url = 'http://xn--42cm3at5gj3b0hpal2dj.com/edit_img.php?id='+str(post_id)
                        req = httprequestObj.http_get(url)
                        soup = BeautifulSoup(req.text,'html.parser')
                        imgs = soup.findAll('div',{'class':'col-xs-12 col-md-4 col-sm-6 col-mm-4'})
                        for img in imgs:
                            url = 'http://xn--42cm3at5gj3b0hpal2dj.com/'+str(img.find('a')['href'])
                            req = httprequestObj.http_get(url)

                        imgurl = 'http://xn--42cm3at5gj3b0hpal2dj.com/add_img.php?id=' + str(post_id)
                        httprequestObj.http_get(imgurl)
                        if 'post_images' in data:
                            if len(data['post_images']) > 0:
                                pass
                        else:
                            data['post_images'] = [
                                './imgtmp/default/white.jpg']
                        files = {}
                        temp = 1

                        for i in range(len(data['post_images'])):
                            r = open(os.getcwd() + '/' + data['post_images'][i], 'rb')
                            files['photoimg'] = r
                            response = httprequestObj.http_post('http://xn--42cm3at5gj3b0hpal2dj.com/ajax_img.php',
                                                                data=None, files=files)

                        success = 'true'
                        detail = 'Successful post'
                except:
                    success = 'false'
                    detail = 'Something went wrong.'
                success = 'true'
                detail = 'Successfully edited'
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
         'websitename':'condoforrent'}
        return result

    def boost_post(self, data):
        start_time = datetime.datetime.utcnow()
        post_id = data['post_id']
        log_id = data['log_id']
        result = self.test_login(data)
        success = result['success']
        detail = result['detail']
        if success=="true":
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}
            url = 'http://xn--42cm3at5gj3b0hpal2dj.com/maneg_property.php'
            valid_ids = []
            req = httprequestObj.http_get_with_headers(url, headers=headers)
            soup = BeautifulSoup(req.text, 'html.parser')
            total_pages = 1
            if soup.find('ul', {'class': 'pagination'}) != None:
                total_pages = len(soup.find('ul', {'class': 'pagination'}).findAll('li'))
                if total_pages > 1:
                    total_pages -= 1
            for i in range(total_pages):
                url = 'http://xn--42cm3at5gj3b0hpal2dj.com/maneg_property.php?&page=' + str(i)
                req = httprequestObj.http_get_with_headers(url, headers=headers)
                soup = BeautifulSoup(req.text, features='html.parser')
                print(soup.find('table', {'class': 'table table-striped'}))
                posts = soup.find('table', {'class': 'table table-striped'}).find('tbody').findAll('tr')
                for post in posts:
                    id = ''
                    a = str(post.find('a')['href'])
                    ind = a.find('property-') + 9
                    while a[ind] != '-':
                        id += a[ind]
                        ind += 1
                    valid_ids.append(id)

            if str(post_id) not in valid_ids:
                success = 'false'
                detail = 'Invalid id'
            if success == 'true':
                success = 'true'
                detail = 'Edited and saved'
        end_time = datetime.datetime.utcnow()
        result = {'success':success,
         'usage_time':str(end_time - start_time),
         'start_time':str(start_time),
         'end_time':str(end_time),
         'detail':detail,
         'ds_id':data['ds_id'],
         'log_id':log_id,
         'post_id':post_id,
         'websitename':'condoforrent'}
        return result
