# -*- coding: utf-8 -*-

from .lib_httprequest import *
from bs4 import BeautifulSoup
import datetime
import sys

class livingjoin():

    name = 'livingjoin'

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

    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        
        success = False
        detail = 'Something wrong'

        data = {
            'email': postdata['user'],
            'check_email': postdata['user'],
            'password': postdata['pass'],
            'confirmPassword': postdata['pass'],
            'signup': 'Sign up'
        }

        r = self.httprequestObj.http_post('https://www.livingjoin.com/member/register', data=data)
        r = self.httprequestObj.http_get('https://www.livingjoin.com/member/account')
        
        if r.url == 'https://www.livingjoin.com/member/account':
            success = True
            detail = 'Login successful'

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            'ds_id': postdata['ds_id'],
            "detail": detail,
            "websitename": "livingjoin",
        }

    def test_login(self, postdata):
        time_start = datetime.datetime.utcnow()

        success = False
        detail = 'Something wrong'

        datapost = {
            'refer': '',
            'login_username': postdata['user'],
            'login_password': postdata['pass']
        }
        r = self.httprequestObj.http_post('https://www.livingjoin.com/login', data=datapost)
        r = self.httprequestObj.http_get('https://www.livingjoin.com/member/account')

        if r.url == 'https://www.livingjoin.com/member/account':
            success = True
            detail = 'Login successful'
        else:
            detail = 'Wrong username or password'

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": "livingjoin",
            "ds_id": postdata['ds_id'],
        }

    def post_prop(self, postdata,action):
        success =False
        detail = 'Something wrong'
        post_url = ''
        post_id = ''
        province_id = ''
        district_id = ''
        subdistrict_id = ''

        property_type = {
            '1':'3',
            '2':'1',
            '3':'1',
            '4':'2',
            '5':'5',
            '6':'8',
            '7':'4',
            '8':'4',
            '9':'6',
            '10':'7',
            '25':'7'
        }

        property_type_tag = {
                '1':'คอนโด',
                '2':'บ้านเดี่ยว',
                '3':'บ้านแฝด',
                '4':'ทาวน์เฮ้าส์',
                '5':'ตึกแถว-อาคารพาณิชย์',
                '6':'ที่ดิน',
                '7':'อพาร์ทเมนท์',
                '8':'โรงแรม',
                '9':'ออฟฟิศสำนักงาน',
                '10':'โกดัง',
                '25':'โรงงาน'
            }

        sub_propertytype = {
            '1':'3',
            '2':'1',
            '3':'2',
            '4':'',
            '5':'',
            '6':'7',
            '7':'10',
            '8':'11',
            '9':'18',
            '10':'21',
            '25':'20'
        }

        tag = ''
        for i in ['addr_province','addr_district','addr_sub_district','listing_type']:
            if postdata[i] != '':
                tag += postdata[i] + ','
        tag += '{},ราคาถูก'.format(property_type_tag[postdata['property_type']])

        sub_propertytype = sub_propertytype[postdata['property_type']]
        listing_type = {'ขาย' : '1','เช่า':'2'}
        postdata['property_type'] = property_type[postdata['property_type']]
        postdata['listing_type'] = listing_type[postdata['listing_type']]

        r = self.httprequestObj.http_get('https://www.livingjoin.com/member/post?prop_type_id={}'.format(postdata['property_type']))
        soup = BeautifulSoup(r.content, features = "html.parser")
        provinces = soup.find('select', {'id': 'province_id'})
        provinces = provinces.find_all('option')

        if postdata['addr_province'] == 'กรุงเทพ':
            postdata['addr_province'] = 'กรุงเทพมหานคร'
            postdata['addr_district'] = 'เขต{}'.format(postdata['addr_district'])

        for province in provinces:
            if province.text == postdata['addr_province']:
                province_id = province['value']
                break
        get_district = {
            'province_id': province_id,
            'PH': '../../',
            'andval': '0.94461133400528'
        }
        r = self.httprequestObj.http_post('https://www.livingjoin.com/ajax/misc/set_province?province_id={}&PH=../../&andval=0.94461133400528'.format(province_id), data=get_district)
        for i in (r.text).split('option'):
            if postdata['addr_district'] in i:
                district_id = i.split('"')[1]
                break

        get_subdistrict = {
            'amphur_id': district_id,
            'PH': '../../',
            'andval': '0.33840354397483763'
        }
        r = self.httprequestObj.http_post('https://www.livingjoin.com/ajax/misc/set_district?amphur_id={}&PH=../../&andval=0.33840354397483763'.format(district_id), data=get_subdistrict)
        
        for i in (r.text).split('option'):
            if postdata['addr_sub_district'] in i:
                subdistrict_id = i.split('"')[1]
                break

        if postdata['floor_level'] == '':
            postdata['floor_level'] = postdata['floor_total']

        if 'คุณ' in postdata['post_title_th']:
            postdata['post_title_th'] = postdata['post_title_th'].replace('คุณ','')

        if province_id == '' or district_id == '' or subdistrict_id == '':
            detail = 'This subdistrict does not exist on this site.'
        else:
            data = [
                ('prop_type_id', postdata['property_type']),
                ('small_fb', '1'),
                ('title_x', postdata['post_title_th']),
                ('post_type_id', postdata['listing_type']),
                ('price', postdata['price_baht']),
                ('price_rent', postdata['price_baht']),
                ('price_type_id', '1'),
                ('province_id', province_id),
                ('amphur_id', district_id),
                ('district_id', subdistrict_id),
                ('place_list[]',''),
                ('place_list[]',''),
                ('place_list[]', ''),
                ('unit_type_id', sub_propertytype),
                ('room_class', postdata['floor_level']),
                ('total_class', postdata['floor_total']),
                ('total_bedroom',postdata['bed_room']),
                ('total_bathroom',postdata['bath_room']),
                ('total_kitchenroom', '0'),
                ('total_livingroom','0'),
                ('total_carpark','0'),
                ('size_rai', postdata['land_size_rai']),
                ('size_gan',postdata['land_size_ngan']),
                ('size_va',postdata['land_size_wa']),
                ('unit_size', postdata['floorarea_sqm']),
                ('unit_width',''),
                ('unit_height',''),
                ('living_area', postdata['floorarea_sqm']),
                ('have_detail','yes'),
                ('detail', postdata['post_description_th'].replace('\n', '<br />')),
                ('dir_name', 'classified'),
                ('feature_list_other[]',''),
                ('feature_list_other[]',''),
                ('feature_list_other[]',''),
                ('display_map', 'H'),
                ('lat', postdata['geo_latitude']),
                ('lng', postdata['geo_longitude']),
                ('formatted_address','' ),
                ('tag_list', tag),
                ('fullname', postdata['name']),
                ('phone', postdata['mobile']),
                ('post','')
            ]

            if action == 'edit':
                r = self.httprequestObj.http_get("https://www.livingjoin.com/member/postedit?edit_id={}".format(postdata['post_id']))
                soup = BeautifulSoup(r.content, features = "html.parser")
                all_picture = soup.find('div', {'id': 'msgBox'})
                all_picture = all_picture.find_all('div', {'class': 'list-group-item'})
                old_other_picture = ''
                for count,file in enumerate(all_picture):
                    try:
                        img = file.find('img')['src'].split('/')[-1]
                    except:
                        continue
                    del_pic = {
                        'pic': img,
                        'PH': '../',
                        'andval': '0.8412183517033196'
                    }

                    if count == 0:
                        del_pic['pic_type'] = 'main_pic'
                        r = self.httprequestObj.http_post('https://www.livingjoin.com/ajax/misc/delete_multi_pic_edit?pic_type=main_pic&pic={}&PH=../&andval=0.8412183517033196'.format(img), data= del_pic)
                        data.append(('old_picture',img))
                    else:
                        del_pic['pic_type'] = 'other_pic'
                        r = self.httprequestObj.http_post('https://www.livingjoin.com/ajax/misc/delete_multi_pic_edit?pic_type=other_pic&pic={}&PH=../&andval=0.8412183517033196'.format(img), data= del_pic)
                        if count != len(all_picture)-1:
                            old_other_picture += img+','
                        else:
                            old_other_picture += img

                data.append(('old_other_picture',old_other_picture))
                for count,file in enumerate(postdata['post_images'][:10]):
                    r = self.httprequestObj.http_post('https://www.livingjoin.com/file_upload.php', data={},files={'uploadfile':open(os.getcwd()+"/"+file, 'rb')})
                    if count == 0:
                        data.append(('default_pic','{}.jpg'.format(r.json()['file'])))

                data.append(('picture_digi','H'))
                data.append(('edit_id',postdata['post_id']))

                r = self.httprequestObj.http_post('https://www.livingjoin.com/member/postedit?edit_id={}'.format(postdata['post_id']), data=data)

                if 'แก้ไขประกาศเรียบร้อยค่ะ' in r.text:
                    success = True
                    detail = 'successful'
            else:
                for count,file in enumerate(postdata['post_images'][:10]):
                    r = self.httprequestObj.http_post('https://www.livingjoin.com/file_upload.php', data={},files={'uploadfile':open(os.getcwd()+"/"+file, 'rb')})
                    if count == 0:
                        data.append(('default_pic','{}.jpg'.format(r.json()['file'])))
                
                r = self.httprequestObj.http_post('https://www.livingjoin.com/member/post', data=data)
                if 'โพสต์ประกาศเรียบร้อยค่ะ' in r.text:
                    r = self.httprequestObj.http_get("https://www.livingjoin.com/member/postlist?status=H")
                    soup = BeautifulSoup(r.content, features = "html.parser")
                    for a in soup.find_all('a', href=True):
                        if postdata['post_title_th'] in a.text:
                            post_url = a['href']
                            post_id = post_url.split('item/')[1].replace('.html','')
                            success = True
                            detail = 'successful'
                            break

        return {
            'success': success,
            'detail': detail,
            'post_id': post_id,
            'post_url': post_url
        }

    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        success = False
        detail = 'Something wrong'
        post_url = ''
        post_id = ''
        test_login = self.test_login(postdata)
        success = test_login["success"]
        
        if success:
            success =False
            post = self.post_prop(postdata,'post')
            success = post['success']
            if success:
                detail = 'Post successful'
                post_id = post['post_id']
                post_url = post['post_url']
            else:
                detail = post['detail']
        else:
            detail = test_login["detail"]

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": post_url,
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
            "websitename": "livingjoin",
        }
    
    def edit_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        success = False
        detail = 'Something wrong'
        test_login = self.test_login(postdata)
        success = test_login["success"]
        
        if success:
            success =False
            edit = self.post_prop(postdata,'edit')
            success = edit['success']
            if success:
                detail = 'Edit successful'
            else:
                detail = edit['detail']
        else:
            detail = test_login["detail"]

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": postdata['ds_id'],
            "post_id": postdata['post_id'],
            "account_type": "null",
            "detail": detail,
            "websitename": "livingjoin",
        }

    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        success = False
        detail = 'Something wrong'
        test_login = self.test_login(postdata)
        success = test_login["success"]
        
        if success:
            success =False
            data = {
                'post_id': postdata['post_id'],
                'PH': '../',
                'andval': '0.5898466393952244'
            }
            r = self.httprequestObj.http_post('https://www.livingjoin.com/ajax/member/movepost?post_id={}&PH=../&andval=0.5898466393952244'.format(postdata['post_id']), data=data)

            if 'เลื่อนประกาศล่าสุด' in r.text:
                success = True
                detail = 'Boost successful'
            else:
                detail = r.text
            
        else:
            detail = test_login["detail"]

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": postdata['post_id'],
            "websitename": "livingjoin",
            "post_view": ""
        }

    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        success = False
        detail = 'Something wrong'
        test_login = self.test_login(postdata)
        success = test_login["success"]
        
        if success:
            success =False
            r = self.httprequestObj.http_get("https://www.livingjoin.com/member/postedit?edit_id={}".format(postdata['post_id']))
            soup = BeautifulSoup(r.content, features = "html.parser")
            all_picture = soup.find('div', {'id': 'msgBox'})
            all_picture = all_picture.find_all('div', {'class': 'list-group-item'})
            old_other_picture = ''
            for count,file in enumerate(all_picture):
                try:
                    img = file.find('img')['src'].split('/')[-1]
                except:
                    continue
                if count == 0:
                    default_pic = img
                    old_picture = img
                else:
                    old_other_picture += img+','
            data = [
                ('edit_id',postdata['post_id']),
                ('small_fb', '1'),
                ('status','C'),
                ('title_x', ''),
                ('post_type_id', '1'),
                ('price', ''),
                ('price_type_id', '1'),
                ('province_id', '1'),
                ('amphur_id', '1'),
                ('district_id', '1'),
                ('place_list[]',''),
                ('unit_type_id', ''),
                ('room_class', '0'),
                ('total_class', '0'),
                ('total_bedroom','0'),
                ('total_bathroom','0'),
                ('total_kitchenroom', '0'),
                ('total_livingroom','0'),
                ('total_carpark','0'),
                ('size_rai', '0'),
                ('size_gan','0'),
                ('size_va','0'),
                ('unit_size', '0'),
                ('unit_width',''),
                ('unit_height',''),
                ('living_area', '0'),
                ('have_detail','yes'),
                ('detail', 'ประกาศถูกลบแล้ว ประกาศถูกลบแล้ว ประกาศถูกลบแล้ว ประกาศถูกลบแล้ว ประกาศถูกลบแล้ว ประกาศถูกลบแล้ว ประกาศถูกลบแล้ว'),
                ('dir_name', 'classified'),
                ('feature_list_other[]',''),
                ('display_map', 'H'),
                ('lat', ''),
                ('lng', ''),
                ('formatted_address','' ),
                ('tag_list', ''),
                ('fullname', ''),
                ('phone', ''),
                ('post',''),
                ('default_pic',default_pic),
                ('old_picture',old_picture),
                ('old_other_picture',old_other_picture),
                ('picture_digi','H')
            ]
            r = self.httprequestObj.http_post('https://www.livingjoin.com/member/postedit?edit_id={}'.format(postdata['post_id']), data=data)
            if 'แก้ไขประกาศเรียบร้อยค่ะ' in r.text:
                success = True
                detail = 'Delete success'
        else:
            detail = test_login["detail"]

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": "livingjoin",
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": postdata['post_id']
        }

    def search_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        success = False
        post_found = False
        detail = 'Something wrong'
        post_id = ''
        post_url = ''
        test_login = self.test_login(postdata)
        success = test_login["success"]
        
        if success:
            success =False
            r = self.httprequestObj.http_get("https://www.livingjoin.com/member/postlist/?q={}".format(postdata['post_title_th']))
            soup = BeautifulSoup(r.content, features = "html.parser")
            print(soup)
            for a in soup.find_all('a', href=True):
                if postdata['post_title_th'] in a.text:
                    post_url = a['href']
                    post_id = post_url.split('item/')[1].replace('.html','')
                    success = True
                    detail = 'Post found'
                    post_found = True
                    break
            if not success:
                post_found = False
                detail = 'Not found this post'
        else:
            detail = test_login["detail"]

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": "livingjoin",
            "account_type":None,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "post_modify_time": '',
            "post_view": '',
            "post_url": post_url,
            "post_found": post_found
        }

    def print_debug(self, msg):
        if(self.debug == 1):
            print(msg)
        return True