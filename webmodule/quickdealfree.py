# -*- coding: utf-8 -*-

from .lib_httprequest import *
from bs4 import BeautifulSoup
import datetime
import sys

class quickdealfree():

    name = 'quickdealfree'

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
        self.session = lib_httprequest()

    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        
        success = False
        detail = 'Something wrong'
        
        datapost = {
            'action': '7163666772726470',
            'user_username': postdata['user'],
            'user_password': postdata['pass'],
            'user_name': postdata['name_th'],
            'user_tel': postdata['tel'],
            'user_email': postdata['user']
        }
        r = self.session.http_post('https://quickdealfree.com/formaction', data=datapost)
        if 'สมัครสมาชิกเรียบร้อย' in r.text:
            success = True
            detail = "Registered"
        elif 'มีชื่อผู้ใช้งาน {} นี้ในระบบแล้วค่ะ'.format(postdata['user']) in r.text:
            detail = "This email already registered"
        elif 'มีหมายเลขโทรศัพท์  นี้ในระบบแล้วค่ะ' in r.text:
            detail = 'This phone number already registered'

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            'ds_id': postdata['ds_id'],
            "detail": detail,
            "websitename": "quickdealfree",
        }

    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        success = False
        detail = 'Something wrong'

        datapost = {
            'action': '6b6d66676d',
            'login_username': postdata['user'],
            'login_password': postdata['pass']
        }
        r = self.session.http_post('https://quickdealfree.com/formaction', data=datapost)
        if 'successRedirect' in r.text:
            success = True
            detail = 'Login successful'
        elif 'ไม่พบข้อมูล' in r.text:
            detail = 'Wrong username or password'

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": "quickdealfree",
            "ds_id": postdata['ds_id'],
        }

    def post_prop(self, postdata,action):
        success =False
        detail = 'Something wrong'
        post_url = ''
        post_id = ''
        province_id = ''
        district_id = ''
        r = self.session.http_get('https://quickdealfree.com/member/post')
        soup = BeautifulSoup(r.content, features = "html.parser")
        provinces = soup.find('select', {'name': 'province'})
        provinces = provinces.find_all('option')[1:]
        if postdata['addr_province'] == 'กรุงเทพ':
            postdata['addr_province'] = 'กรุงเทพมหานคร'
        for province in provinces:
            if province.text == postdata['addr_province']:
                province_id = province['value']
                break
        get_district = {
            'province': province_id,
            'action': '636772727167627272666e75'
        }
        r = self.session.http_post('https://quickdealfree.com/getdata', data=get_district)
        for i in (r.text).split('option'):
            if postdata['addr_district'] in i:
                district_id = i.split('"')[1]
                break
            elif postdata['addr_sub_district'] in i:
                district_id = i.split('"')[1]
                break
        if province_id == '' or district_id == '':
            detail = 'This subdistrict does not exist on this site.'
        else:
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

            property_type = {
                'ขาย':{
                    '1':'117',
                    '2':'116',
                    '3':'116',
                    '4':'118',
                    '5':'120',
                    '6':'129',
                    '7':'119',
                    '8':'123',
                    '9':'122',
                    '10':'121',
                    '25':'121'
                },
                'เช่า':{
                    '1':'125',
                    '2':'126',
                    '3':'126',
                    '4':'127',
                    '5':'131',
                    '6':'129',
                    '7':'128',
                    '8':'134',
                    '9':'132',
                    '10':'130',
                    '25':'130'
                }
            }
            sub_type = property_type[postdata['listing_type']][postdata['property_type']]
            postdata['property_type'] = property_type_tag[postdata['property_type']]
            tag = ''
            for i in ['addr_province','addr_district','addr_sub_district','listing_type','property_type']:
                if postdata[i] != '':
                    tag += postdata[i] + ','
            tag += 'ราคาถูก'
            data = [
                ('action', '6f6d7272525f7563'),
                ('subject', postdata['post_title_th'][:65]),
                ('categorymain', '7'),
                ('categorysub', sub_type),
                ('price', postdata['price_baht']),
                ('detail', postdata['post_description_th'].replace('\r','')),
                ('province', province_id),
                ('district', district_id),
                ('demandtype', '2'),
                ('itemcondition', '2'),
                ('mobile', postdata['mobile']),
                ('posttag', tag),
            ]
            if action == 'edit':
                r = self.session.http_get("https://quickdealfree.com/member/postedit/?p={}".format(postdata['post_id']))
                soup = BeautifulSoup(r.content, features = "html.parser")
                all_picture = soup.find('div', {'class': 'mb-2'})
                all_picture = all_picture.find_all('div', {'class': 'mb-2'})
                for i in all_picture:
                    del_pic = {
                        'id': i['class'][-1].split('productimagerow')[1],
                        'postid': postdata['post_id'],
                        'action': '686b6065645363636b'
                    }
                    r = self.session.http_post('https://quickdealfree.com/member/formaction', data=del_pic)
                data.append(('id',postdata['post_id']))

            files = []
            for i in postdata['post_images'][:10]:
                files.append(('imageproduct[]',((i, open(i, "rb"), "image/jpeg"))))
            r = self.session.http_post('https://quickdealfree.com/member/formaction', data=data,files=files)
            if action == 'post':
                if 'ลงขายเรียบร้อย' in r.text:
                    r = self.session.http_get("https://quickdealfree.com/member/listing/")
                    soup = BeautifulSoup(r.content, features = "html.parser")
                    for a in soup.find_all('a', href=True):
                        if postdata['post_title_th'][:64] in a.text:
                            post_url = a['href']
                            post_id = post_url.split('=')[1]
                            success = True
                            detail = 'successful'
                            break
                else:
                    detail = r.text
            elif action == 'edit':
                if 'อัพเดทประกาศเรียบร้อย' in r.text:
                    success = True
                    detail = 'successful'
                else:
                    detail = r.text

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
            "websitename": "quickdealfree",
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
            "websitename": "quickdealfree",
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
            data = {
                'id': postdata['post_id'],
                'action': '6f6d727263636b'
            }
            r = self.session.http_post('https://quickdealfree.com/member/formaction', data=data)
            print(r.text)
            if 'ลบข้อมูลเรียบร้อย' in r.text:
                success = True
                detail = 'Delete successful'
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
            "websitename": "quickdealfree",
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": postdata['post_id']
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
                'id': postdata['post_id'],
                'action': '6f6d7272746e73676c63'
            }
            r = self.session.http_post('https://quickdealfree.com/member/formaction', data=data)

            if 'คุณเลื่อนประกาศเรียบร้อย' in r.text:
                success = True
                detail = 'Boost successful'
            elif 'คุณจะเลื่อนประกาศได้อีกครั้งเวลา' in r.text:
                success = False
                detail = 'This announcement was postponed today'
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
            "websitename": "quickdealfree",
            "post_view": ""
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
            r = self.session.http_get("https://quickdealfree.com/member/listing/")
            soup = BeautifulSoup(r.content, features = "html.parser")
            for a in soup.find_all('a', href=True):
                if postdata['post_title_th'][:65] in a.text:
                    post_url = a['href']
                    post_id = post_url.split('=')[1]
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
            "websitename": "quickdealfree",
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