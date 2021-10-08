import requests

import os
from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
# from urlparse import urlparse
import re
import json
import datetime
import time
import sys
import urllib.request
from urllib.parse import unquote

province_arr = ['เลือกหมวดหมู่', 'เครื่องสำอางค์', 'น้ำหอม', 'ครีม โลชั่น', 'เกี่ยวกับผิวหน้า', 'เกี่ยวกับผม', 'เกี่ยวกับมือและเล็บ', 'เกี่ยวกับความสะอาดร่างกาย', 'เสริมความงาม', 'อื่นๆ', 'อื่นๆ', 'Resume', 'คนหางาน', 'Part Time', 'รายได้เสริม', 'งานพิเศษ', 'งานราชการ', 'งานประจำ', 'อื่นๆ', 'สินเชื่อและไฟแนนซ์', 'ประกันภัยและพรบ', 'ศูนย์บริการ', 'จักรยาน', 'ประดับยนต์', 'เครื่องเสียง', 'อะไหล่', 'มอเตอร์ไซค์', 'รถยนต์', 'อื่นๆ', 'งานวิจัย', 'พิมพ์งาน เข้าเล่ม', 'งานแปล', 'บัญชี', 'รับเหมา', 'รับจ้าง', 'ขายตรง', 'งานพิมพ์', 'กฎหมาย', 'ก่อสร้าง', 'อื่นๆ', 'โรงแรม', 'โรงงาน โกดัง', 'ทาวน์เฮาส์', 'ตึกแถว', 'ร้านค้า พื้นที่ขายของ', 'สำนักงาน', 'หอพัก', 'คอนโดมิเนียม', 'ที่ดิน', 'บ้านเดี่ยว', 'การสักบนร่างกาย', 'ศัลยกรรม', 'อื่นๆ', 'เครื่องสำอางค์', 'อาหารเสริม', 'การแพทย์', 'เสริมความงาม', 'การรักษาโรค', 'การนวด', 'สปา', 'อื่นๆ', 'น้ำหอม', 'เครื่องสำอาง', 'เด็กหญิง', 'เด็กชาย', 'เนคไท ผ้าพันคอ', 'รองเท้า ถุงเท้า', 'ชุดนอน', 'ชุดชั้นใน', 'เสื้อผ้าสตรี', 'เสื้อผ้าบุรุษ', 'กระเป๋า', 'อื่นๆ', 'วัสดุอุปกรณ์', 'ตกแต่งภายใน', 'ห้องน้ำ', 'ห้องรับแขก', 'ห้องนอน', 'ห้องครัว', 'อื่นๆ', 'บริการไอที', 'โฮสติ้ง', 'เว็บไซต์', 'Server', 'Hardware', 'Software', 'Printer Scaner', 'PDA', 'Notebook', 'PC', 'อื่นๆ', 'บริการ ซ่อม', 'อุปกรณ์เสริม', 'ซิมการ์ด บัตรเติมเงิน', 'PABX', 'โทรศัพท์บ้าน', 'วิทยุสื่อสาร', 'PCT', 'มือถือ', 'อื่นๆ', 'บริการถ่ายภาพ', 'อุปกรณ์เสริม', 'เมมโมรี่การ์ด', 'กล้องส่องทางไกล', 'กล้องวงจรปิด', 'กล้องวีดีโอ', 'กล้องดิจิตอล', 'กล้องใช้ฟิล์ม', 'อื่นๆ', 'ต่างหู ตุ้มหู', 'สร้อย จี้', 'เพชร', 'แหวน', 'เพชร', 'ทอง', 'จิวเวลลี่', 'อื่นๆ', 'บริการซ่อม', 'เคเบิ้ล จานดาวเทียม', 'หลอดไฟ โคมไฟ', 'เครื่องครัว', 'เครื่องซักผ้า', 'เครื่องทำความเย็น', 'เครื่องปรับอากาศ', 'เครื่องเล่นเพลง หนัง', 'เครื่องเสียง', 'วิทยุ เทป', 'ทีวี', 'อื่นๆ', 'ทำผม', 'ตกแต่งเล็บ', 'สายรัดข้อมือ ข้อเท้า', 'เข็มขัด', 'หมวก', 'ที่ดัดฟัน', 'คอนแท็คเลนส์', 'แว่นตา', 'นาฬิกา', 'อื่นๆ', 'ตกแต่งขน', 'กรง ที่อยู่สัตว์', 'รักษาสัตว์', 'อาหารสัตว์', 'สัตว์เลี้ยง', 'อื่นๆ', 'คู่มือ บทสรุป', 'เกมส์คอมพิวเตอร์', 'เกมส์ออนไลน์', 'XBox', 'Nintendo', 'PlayStation', 'อื่นๆ', 'วัสดุอุปกรณ์ วัตถุดิบ', 'เครื่องมือ', 'เครื่องจักรกล', 'โรงงาน', 'ส่งออก', 'นำเข้า', 'อุตสาหกรรม', 'อื่นๆ', 'โปสการ์ด', 'เหรียญ', 'แสตมป์', 'โมเดล', 'การ์ด', 'รถบังคับ', 'ของเก่า', 'ตุ๊กตา', 'พระเครื่อง', 'อื่นๆ', 'ละครเวที', 'แสดงสินค้า', 'แต่งงาน', 'คอนเสิร์ต', 'ไนท์คลับ', 'คาราโอเกะ', 'ร้านอาหาร', 'ผับ บาร์', 'อื่นๆ', 'สารคดี', 'รายการทีวี', 'คอนเสิร์ต',
                'ละคร VCD', 'CD เพลง', 'เทป', 'หนัง DVD', 'หนัง VCD', 'อื่นๆ', 'ห้องซ้อม', 'วงดนตรี', 'เครื่องตี', 'เครื่องสาย', 'เครื่องเป่า', 'อิเล็กโทน', 'กลอง', 'เบส', 'กีตาร์', 'อื่นๆ', 'เสื้อผ้า', 'รับเลี้ยงเด็ก', 'เฟอร์นิเจอร์เด็ก', 'อาบน้ำเด็ก', 'ที่นอน', 'ของเล่น', 'อื่นๆ', 'สถาบัน', 'อบรม สัมนา', 'สอนภาษา', 'สอนพิเศษ', 'กวดวิชา', 'เตรียมสอบ', 'เรียนต่อ', 'นิตยสาร', 'นวนิยาย', 'การ์ตูน', 'Textbook', 'ตำราเรียน', 'หนังสือ', 'อื่นๆ', 'โต๊ะ เก้าอี้', 'แฟกซ์', 'โปรเจ็กเตอร์', 'เครื่องถ่ายเอกสาร', 'เครื่องเขียน', 'อื่นๆ', 'เย็บปักถักร้อย', 'รูปปั้น', 'ภาพถ่าย', 'ภาพวาด', 'เทียน', 'ดินเผา', 'ผ้า', 'ไม้', 'โลหะ', 'แก้ว', 'เครื่องสาน', 'อื่นๆ', 'กรอบรูป', 'ของพรีเมี่ยม', 'ของกิ๊ฟชอป', 'ผ้าไหม', 'สินค้าท้องถิ่น', 'ของชำร่วย', 'ของฝาก', 'ของที่ระลึก', 'อื่นๆ', 'ปุ๋ย เคมี', 'กระถาง', 'หญ้า', 'ไม้ประดับ', 'ร้านดอกไม้', 'ดอกไม้', 'ร้านต้นไม้', 'ต้นไม้', 'อื่นๆ', 'ฟิตเนส โยคะ', 'เครื่องออกกำลังกาย', 'อุปกรณ์', 'งานเลี้ยง', 'นันทนาการ', 'กิจกรรม', 'กีฬา', 'อื่นๆ', 'อุปกรณ์ท่องเที่ยว', 'จองตั๋วเครื่องบินรถเรือ', 'บริการเช่า', 'โปรแกรมทัวร์', 'บริษัททัวร์', 'ที่พัก', 'จองโรงแรมต่างประเทศ', 'จองโรงแรมในประเทศ', 'อื่นๆ', 'อุปกรณ์', 'เครื่องจักร', 'ทำสวน ทำไร่', 'ปลูกพืช', 'การเกษตร', 'อื่นๆ', 'คู่มือทำอาหาร', 'ภัตราคาร', 'ร้านอาหาร', 'เครื่องดื่ม', 'อาหาร', 'อื่นๆ', 'ใบปลิว', 'การ์ด', 'คูปอง', 'บัตร', 'ตั๋ว', 'อื่นๆ', 'ไม่มีหมวด', 'กินไม่ได้', 'กินได้', 'กรุณาเลือก', 'อยากขาย', 'อยากซื้อ', 'อยากเช่า', 'ให้เช่า', 'แนะนำ', 'รับจ้าง', 'บริการ', 'หาคน', 'กรุณาเลือก', 'สินค้าใหม่', 'สินค้ามือสอง', 'กรุณาเลือก', 'กรุงเทพมหานคร', 'กระบี่', 'กาญจนบุรี', 'กาฬสินธุ์', 'กำแพงเพชร', 'ขอนแก่น', 'จันทบุรี', 'ฉะเชิงเทรา', 'ชลบุรี', 'ชัยนาท', 'ชัยภูมิ', 'ชุมพร', 'เชียงราย', 'เชียงใหม่', 'ตรัง', 'ตราด', 'ตาก', 'นครนายก', 'นครปฐม', 'นครพนม', 'นครราชสีมา', 'นครศรีธรรมราช', 'นครสวรรค์', 'นนทบุรี', 'นราธิวาส', 'น่าน', 'บุรีรัมย์', 'ปทุมธานี', 'ประจวบคีรีขันธ์', 'ปราจีนบุรี', 'ปัตตานี', 'พระนครศรีอยุธยา', 'พะเยา', 'พังงา', 'พัทลุง', 'พิจิตร', 'พิษณุโลก', 'เพชรบุรี', 'เพชรบูรณ์', 'แพร่', 'ภูเก็ต', 'มหาสารคาม', 'มุกดาหาร', 'แม่ฮ่องสอน', 'ยโสธร', 'ยะลา', 'ร้อยเอ็ด', 'ระนอง', 'ระยอง', 'ราชบุรี', 'ลพบุรี', 'ลำปาง', 'ลำพูน', 'เลย', 'ศรีสะเกษ', 'สกลนคร', 'สงขลา', 'สตูล', 'สมุทรปราการ', 'สมุทรสงคราม', 'สมุทรสาคร', 'สระแก้ว', 'สระบุรี', 'สิงห์บุรี', 'สุโขทัย', 'สุพรรณบุรี', 'สุราษฎร์ธานี', 'สุรินทร์', 'หนองคาย', 'หนองบัวลำภู', 'อ่างทอง', 'อำนาจเจริญ', 'อุดรธานี', 'อุตรดิตถ์', 'อุทัยธานี', 'อุบลราชธานี', '7', '15', '30', '45', '60', '90']


class thisads():

    name = 'thisads'

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
        time_start = datetime.datetime.utcnow()
        user = postdata['user']
        passwd = postdata['pass']
        if 'name_th' in postdata:
            name_th = postdata["name_th"]
        else:
            name_th = 'temp'
        if 'surname_th' in postdata:
            surname_th = postdata["surname_th"]
        else:
            surname_th = ''
        success = "true"
        detail = ""
        data = {

            'fullname': name_th + surname_th,
            'email': user,
            'password': passwd,
            'repassword': passwd,
            'code': '8758'
        }

        headers = {
            'Pragma': 'no-cache',
            'Origin': 'http://thisads.com',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Cache-Control': 'no-cache',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Referer': 'http://thisads.com/register.php',
        }
        r = self.session.http_post(
            'http://thisads.com/ajax_register.php', headers=headers, data=data)

        data = r.text
        #print(data,r.content)
        if data != '\ufeff1':
            success = 'false'
            detail = 'unable to register'
        else:
            success = 'true'
            detail = 'successfully registered'
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "thisads",
            "success": success,
                'ds_id': postdata['ds_id'],
            "start_time": str(time_start),
            "usage_time": str(time_usage),
            "end_time": str(time_end),
            "detail": detail,
        }

    def test_login(self, postdata):
        time_start = datetime.datetime.utcnow()
        user = postdata['user']
        passwd = postdata['pass']

        headers = {
            'Pragma': 'no-cache',
            'Origin': 'http://thisads.com',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Cache-Control': 'no-cache',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Referer': 'http://thisads.com/',
        }
        data = {
            'url2': 'http://thisads.com/',
            'memail': user,
            'mpassword': passwd,
            'login': ' Login '
        }
        r = self.session.http_post('http://thisads.com/ajax_login.php',
                                     headers=headers, data=data)
        data = r.text
        if data != '\ufeff1':
            success = 'false'
            detail = 'unable to login'
        else:
            success = 'true'
            detail = 'successfully logged in'
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "ds_id": postdata['ds_id'],
            "websitename": "thisads",
            "success": success,
            "start_time": str(time_start),
            "usage_time": str(time_usage),
            "end_time": str(time_end),
            "detail": detail,
        }

    def create_post(self, postdata):
        time_start = datetime.datetime.utcnow()
        test_login = self.test_login(postdata)
        success = test_login['success']
        detail = test_login['detail']
        # done
        if postdata['property_type'] == 'คอนโด' or int(postdata['property_type']) == 1:
            prop = 149
        elif int(postdata['property_type']) == 4 or postdata['property_type'] == 'ทาวน์โฮม ทาวน์เฮ้าส์':  # done
            prop = 154
        elif int(postdata['property_type']) == 2 or postdata['property_type'] == 'บ้านเดี่ยว':  # done
            prop = 147
        elif int(postdata['property_type']) == 3:  # done
            prop = 147
        elif postdata['property_type'] == 'อพาร์ทเมนท์' or int(postdata['property_type']) == 7:
            prop = 32
        # done
        elif postdata['property_type'] == 'ที่ดินเปล่า' or int(postdata['property_type']) == 6:
            prop = 148
        # done
        elif postdata['property_type'] == 'อาคาร พื้นที่สำนักงาน' or int(postdata['property_type']) == 9:
            prop = 151
        # done
        elif postdata['property_type'] == 'อาคารพาณิชย์' or int(postdata['property_type']) == 5:
            prop = 153
        elif int(postdata['property_type']) == 10:  # done
            area = str(postdata['floor_area'])
            prop = 155
        elif int(postdata['property_type']) == 25:  # done
            prop = 155
        elif int(postdata['property_type']) == 8:  # done
            prop = 156

        province = -1
        for i in province_arr:
            if str(i) == postdata['addr_province'] or postdata['addr_province'] in str(i) or str(i) in postdata['addr_province']:
                province = str(i)
        if province == -1:
            success = 'false'
            detail = 'province not found'
        if postdata['listing_type'] == 'ขาย':  # sell
            forid = 1
        else:
            forid = 4
        headers = {
            'Connection': 'keep-alive',
            'Content-Length': '178895',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Origin': 'http://thisads.com',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryBoBuKlPeNF95A6fN',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Referer': 'http://thisads.com/%E0%B8%A5%E0%B8%87%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B8%81%E0%B8%B2%E0%B8%A8%E0%B8%9F%E0%B8%A3%E0%B8%B5.html',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        files = {}
        if len(postdata['post_images']) > 0:
            filename, file_extension = os.path.splitext(postdata['post_images'][0])
            files = {'photo[]': (postdata['post_images'][0], open(
                postdata['post_images'][0], 'rb'), 'image/'+file_extension)}

        # files={}
        n = len(str(postdata['post_title_th']))
        if 'short_post_title_th' in postdata and postdata['short_post_title_th'] != None:
            postdata['post_title_th'] = (str(postdata['short_post_title_th'])[
                                         0:min(n, 100)]).strip()
        else:
            postdata['post_title_th'] = (str(postdata['post_title_th'])[
                                         0:min(n, 100)]).strip()
        postdata['post_description_th'] = str(
            postdata['post_description_th']).replace('\r\n', '<br>')
        postdata['post_description_th'] = str(
            postdata['post_description_th']).replace('\n', '<br>')

        data = {
            'url': 'http://thisads.com/',
            'category': prop,
            'name': str(postdata['post_title_th']),
            'detail': postdata['post_description_th'],
            'price': postdata['price_baht'],
            'forid': forid,
            'conid': '2',
            'province': province,
            'day': 90,
            'send1': 'true',
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0',
        }
        r = self.session.http_post('http://thisads.com/ajax_fullpost.php', headers=headers, data=data, files=files)
        print(r.text)
        if str(r.text) != '\ufeff1':
            success = 'false'
            detail = 'duplicate name or error while posting 1'

            time_end = datetime.datetime.utcnow()
            time_usage = time_end - time_start

            return {

                "websitename": "thisads",
                "success": success,
                "start_time": str(time_start),
                "end_time": str(time_end),
                "post_url": '',
                "post_id": '',
                "account_type": "null",
                "detail": detail,
            }

        # getting post id and url
        r = self.session.http_get(
            'http://www.thisads.com/ajax_showproduct.php', headers=headers, verify=False)
        soup = BeautifulSoup(r.content, 'html5lib')
        # with open('temp.html', 'w') as f:
        #     f.write(r.text)
        flag = 0
        edit_url = ''
        post_url = ''
        for value in soup.findAll('a'):

            if 'edit' in str(value['href']):
                edit_url = value['href']
                if flag==1:
                    break
                else :
                    flag=1
            if str(value.text) == str(postdata['post_title_th']) or (str(value.txt) in str(postdata['post_title_th']) and str(value.txt) != ''):
                post_url = value['href']
                if flag==1:
                    break
                else :
                    flag=1
        #print(edit_url,post_url)
        detail = test_login['detail']
        if edit_url == '' or post_url == '':
            success = 'false'
            detail = 'duplicate name or error while posting'
        if success == 'false':
            post_id = ''
        else:
            n = len(edit_url)
            post_id = edit_url[n-6:n]

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {

            "websitename": "thisads",
            "success": success,
            "ds_id": postdata['ds_id'],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
        }

    def edit_post(self, postdata):
        time_start = datetime.datetime.utcnow()
        test_login = self.test_login(postdata)
        success = test_login['success']
        # done
        if postdata['property_type'] == 'คอนโด' or int(postdata['property_type']) == 1:
            prop = 149
        elif int(postdata['property_type']) == 4 or postdata['property_type'] == 'ทาวน์โฮม ทาวน์เฮ้าส์':  # done
            prop = 154
        elif int(postdata['property_type']) == 2 or postdata['property_type'] == 'บ้านเดี่ยว':  # done
            prop = 147
        elif int(postdata['property_type']) == 3:  # done
            prop = 147
        elif postdata['property_type'] == 'อพาร์ทเมนท์' or int(postdata['property_type']) == 7:
            prop = 32
        # done
        elif postdata['property_type'] == 'ที่ดินเปล่า' or int(postdata['property_type']) == 6:
            prop = 148
        # done
        elif postdata['property_type'] == 'อาคาร พื้นที่สำนักงาน' or int(postdata['property_type']) == 9:
            prop = 151
        # done
        elif postdata['property_type'] == 'อาคารพาณิชย์' or int(postdata['property_type']) == 5:
            prop = 153
        elif int(postdata['property_type']) == 10:  # done
            area = str(postdata['floor_area'])
            prop = 155
        elif int(postdata['property_type']) == 25:  # done
            prop = 155
        elif int(postdata['property_type']) == 8:  # done
            prop = 156

        province = -1
        for i in province_arr:
            if str(i) == postdata['addr_province'] or postdata['addr_province'] in str(i) or str(i) in postdata['addr_province']:
                province = str(i)
        if province == -1:
            success = 'false'
            detail = 'province not found'
        if postdata['listing_type'] == 'ขาย':  # sell
            forid = 1
        else:
            forid = 4

        headers = {
            'Pragma': 'no-cache',
            'Origin': 'http://www.thisads.com',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Cache-Control': 'no-cache',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Referer': 'http://www.thisads.com/edit.php?id=103072',
        }
        files = {}
        if len(postdata['post_images']) > 0:

            filename, file_extension = os.path.splitext(postdata['post_images'][0])
            files = {'photo[]': (postdata['post_images'][0], open(
                postdata['post_images'][0], 'rb'), 'image/'+file_extension)}
        # files={}
        n = len(str(postdata['post_title_th']))
        if 'short_post_title_th' in postdata and postdata['short_post_title_th'] != None:
            postdata['post_title_th'] = (str(postdata['short_post_title_th'])[
                                         0:min(n, 100)]).strip()
        else:
            postdata['post_title_th'] = (str(postdata['post_title_th'])[
                                         0:min(n, 100)]).strip()
        postdata['post_description_th'] = str(
            postdata['post_description_th']).replace('\r\n', '<br>')
        postdata['post_description_th'] = str(
            postdata['post_description_th']).replace('\n', '<br>')
        pid = postdata['post_id']
        data = {
            'pid': pid,
            'url': 'http://www.thisads.com/',
            'maxsize': '100000',
            'category': prop,
            'name': str(postdata['post_title_th']),
            'detail': postdata['post_description_th'],
            'intro': '',
            'price': postdata['price_baht'], #changed here
            'forid': forid,
            'conid': '2',
            'province': province,
            'day': '90',
            'send1': ' record '
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0',
        }
        r = self.session.http_post(
            'http://www.thisads.com/ajax_fulledit.php', headers=headers, data=data, files=files)
        #print(str(r.text),str(r.content))
        if str(r.text) != '\ufeff1':
            success = 'false'
            detail = 'Unable to edit post'
        else:
            detail='Post edited successfully'
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "thisads",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": postdata['ds_id'],
            "post_id": postdata['post_id'],
            "log_id": postdata['log_id'],
            "account_type": "null",
            "detail": detail
        }

    def delete_post(self, postdata):
        time_start = datetime.datetime.utcnow()
        test_login = self.test_login(postdata)
        success = test_login['success']

        pid = postdata['post_id']
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0',
        }
        params = (
            ('id', pid),
        )
        # getting post id and url
        r = self.session.http_get(
            'http://www.thisads.com/ajax_showproduct.php', headers=headers, verify=False)
        soup = BeautifulSoup(r.content, 'html5lib')
        # with open('temp.html', 'w') as f:
        #     f.write(r.text)
        flag = 0
        edit_url = ''
        post_url = ''
        for value in soup.findAll('a'):
            if str(pid) in str(value['href']):
                flag = 1
        detail = test_login['detail']
        if flag == 0:
            success = 'false'
            detail = 'Error while deleting or post id dont exist'
        else:
            detail = 'Success fully deleted'
        r = self.session.http_get(
            'http://www.thisads.com/ajax_deleteproduct.php', headers=headers, params=params, verify=False)

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "websitename": "thisads",
                'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "account_type": "null",
            "detail": detail,
        }

    def boost_post(self, postdata):
        time_start = datetime.datetime.utcnow()
        test_login = self.test_login(postdata)
        success = test_login['success']
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0',
        }
        params = (
            ('id', '0'),
        )
        response = self.session.http_get('http://www.thisads.com/ajax_moveproduct.php', headers=headers, params=params, verify=False)
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        if success=='true':
            detail = 'all posts boosted'
        else :
            detail= 'error while boosting / can only boost once a day'
        return {
            "websitename": "thisads",
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id":postdata['post_id'],
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "account_type": "null",
            "detail": detail,
        }


    def func_get_mapping(self, postdata):
        success = self.test_login(postdata)
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0',
        }
        r = self.session.http_get(
            'http://www.thisads.com/ajax_showproduct.php', headers=headers, verify=False)
        soup = BeautifulSoup(r.content, 'html5lib')
        # with open('temp.html', 'w') as f:
        #     f.write(r.text)
        flag = 0
        edit_url = ''
        for value in soup.findAll('a'):

            if 'edit' in str(value['href']):
                edit_url = value['href']
                flag = 1

            if str(value.text) == str(postdata['post_title_th']) or (str(value.txt) in str(postdata['post_title_th']) and str(value.txt) != ''):
                #  or str(postdata['post_title_th']) in str(value.text) or str(value.text) in str(postdata['post_title_th'])
                post_url = value['href']
                break

    def func_delete_all(self, postdata):
        success = self.test_login(postdata)
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0',
        }
        r = self.session.http_get(
            'http://www.thisads.com/ajax_showproduct.php', headers=headers, verify=False)
        soup = BeautifulSoup(r.content, 'html5lib')
        for value in soup.findAll('a'):
            if 'edit' in str(value['href']):
                edit_url = value['href']
                n = len(edit_url)
                post_id = edit_url[n-6:n]
                params = (
                    ('id', post_id),
                )

                r = self.session.http_get(
                    'http://www.thisads.com/ajax_deleteproduct.php', headers=headers, params=params)

    def search_post(self,postdata):
        start_time = datetime.datetime.utcnow()

        login = self.test_login(postdata)
        post_found = "false"
        post_id = ''
        post_url = ''
        post_view = ''
        post_modify_time = ''
        post_create_time = ''
        detail = 'No post with this title'
        title = ''
        if (login['success'] == 'true'):

            
            #'http://thisads.com/%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B8%81%E0%B8%B2%E0%B8%A8%E0%B8%82%E0%B8%AD%E0%B8%87%E0%B8%84%E0%B8%B8%E0%B8%93.html'

            all_posts_url = 'http://thisads.com/ajax_showproduct.php'
            cookies = {
                'PHPSESSID': 'd6594er797ku4k8j9k13r92kl1',
                'fcspersistslider1': '1',
                'producttabs2': '0',
                'producttabs': '0',
                'HstCfa1057552': '1594641567283',
                'HstCmu1057552': '1594641567283',
                'HstCnv1057552': '1',
                '__dtsu': '6D0015943150553C303F1543554130A6',
                'HstCns1057552': '2',
                'HstCla1057552': '1594642569220',
                'HstPn1057552': '9',
                'HstPt1057552': '9',
            }

            headers = {
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
            }
            pi_url  = 'http://thisads.com/member.php'
            pi = self.session.http_get(pi_url)
            #print(pi.text)
            all_posts = self.session.http_get(all_posts_url)

            page = BeautifulSoup(all_posts.text, features = "html5lib")
            
            #print(page)
            divi = page.find('div', attrs = {'id':'productlist'})
            #print(divi)
            prodList = divi.findAll('li')
            #print(xyz,len(xyz))
            
            if prodList == None:
                detail = "Post Not Found"
            else:
                flag= 0
                for prd in prodList:
                    on = prd.findAll('a')
                    for one in on:
                        if one.has_attr('target'):
                            print(one.text)
                        if one.has_attr('target') and one.text==postdata['post_title_th']:
                            post_url = one['href']
                            print("yha Phunch gya",post_url)
                            pid = post_url.split('/')[-2]
                            sz = len(pid)-1
                            while sz>=0:
                                if '0'<=pid[sz]<='9' :
                                    sz-=1
                                else:
                                    break
                            pid = pid[sz+1:]
                        
                            #print(post_url,end = '\n')
                            post_found = "true"
                            time = prd.find('span',attrs={'class':'date'}).text
                            view = prd.find('span',attrs = {'class':'view'}).find('span',attrs = {'title':'จำนวนคนดู'}).text

                            post_create_time = time
                            post_id = pid

                            post_view = view
                                                
                            detail = "Post Found "
                            flag=1
                            break
                if flag==0:
                    detail = "Post Not Found"
                    post_found = 'false'
                    #print("yha se gya")
                
                    
        else :
            detail = 'Can not log in'
            post_found = 'false'

        end_time = datetime.datetime.utcnow()
        

        return {
            "websitename": "thisads",
            "success": post_found,
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

# temp = {'user': 'amarin.ta@gmail.com', 'pass': '123456',
#         'addr_province': '\u0e01\u0e23\u0e38\u0e07\u0e40\u0e17\u0e1e\u0e21\u0e2b\u0e32\u0e19\u0e04\u0e23', 'property_type': '1', 'post_title_th': 'cdge dsfhjkdfg', 'post_description_th': '\u0e02\u0e32\u0e22 \u0e04\u0e2d\u0e19\u0e42\u0e14 watermark \u0e40\u0e08\u0e49\u0e32\u0e1e\u0e23\u0e30\u0e22\u0e32\u0e23\u0e34\u0e40\u0e27\u0e2d\u0e23\u0e4c 105 \u0e15\u0e23\u0e21. 2 \u0e19\u0e2d\u0e19 2 \u0e19\u0e49\u0e33 \u0e0a\u0e31\u0e49\u0e19 33 \u0e17\u0e34\u0e28 \u0e40\u0e2b\u0e19\u0e37\u0e2d \u0e27\u0e34\u0e27 \u0e40\u0e21\u0e37\u0e2d\u0e07 Fully furnished\r\n\r\n:: \u0e23\u0e32\u0e22\u0e25\u0e30\u0e40\u0e2d\u0e35\u0e22\u0e14\u0e2b\u0e49\u0e2d\u0e07 ::\r\n - \u0e02\u0e19\u0e32\u0e14 105 \u0e15\u0e23\u0e21.\r\n - \u0e0a\u0e19\u0e34\u0e14 2 \u0e2b\u0e49\u0e2d\u0e07\u0e19\u0e2d\u0e19 2 \u0e2b\u0e49\u0e2d\u0e07\u0e19\u0e49\u0e33 \r\n - \u0e2d\u0e32\u0e04\u0e32\u0e23 1 \u0e0a\u0e31\u0e49\u0e19 33\r\n - \u0e23\u0e30\u0e40\u0e1a\u0e35\u0e22\u0e07\u0e2b\u0e31\u0e19\u0e17\u0e32\u0e07\u0e17\u0e34\u0e28 \u0e40\u0e2b\u0e19\u0e37\u0e2d \u0e27\u0e34\u0e27 \u0e40\u0e21\u0e37\u0e2d\u0e07\r\n\r\n\r\n:: \u0e23\u0e32\u0e22\u0e25\u0e30\u0e40\u0e2d\u0e35\u0e22\u0e14\u0e42\u0e04\u0e23\u0e07\u0e01\u0e32\u0e23 ::\r\n - \u0e0a\u0e37\u0e48\u0e2d\u0e42\u0e04\u0e23\u0e07\u0e01\u0e32\u0e23: watermark \u0e40\u0e08\u0e49\u0e32\u0e1e\u0e23\u0e30\u0e22\u0e32\u0e23\u0e34\u0e40\u0e27\u0e2d\u0e23\u0e4c\r\n\r\n\r\n\r\nProject Owner: Major Development\r\nProject Area: 11 Rai\r\nNumber of building: 2\r\n52 floors 486 units\r\n\r\n:: \u0e2a\u0e16\u0e32\u0e19\u0e17\u0e35\u0e48\u0e43\u0e01\u0e25\u0e49\u0e40\u0e15\u0e35\u0e22\u0e07 ::\r\n- Senan fest: 1.2 km\r\n- icon SIAM : 2km\r\n\u0e1e\u0e34\u0e01\u0e31\u0e14: http:\/\/maps.google.com\/maps?q=13.710968,100.498459\r\n\r\n\u0e23\u0e32\u0e04\u0e32: 13,900,000 \u0e1a\u0e32\u0e17\r\n\r\n\u0e2a\u0e19\u0e43\u0e08\u0e15\u0e34\u0e14\u0e15\u0e48\u0e2d: NADECHAuto 0852546523\r\nLine: Pokajg\r\n#\u0e13\u0e40\u0e14\u0e0a\u0e1e\u0e23\u0e47\u0e2d\u0e1e\u0e14\u0e1e\u0e2d\u0e23\u0e4c\u0e15\u0e35\u0e49","post_title_en":"Condo for sale at watermark ChaoPhraya River, 105 Sqm, 33th floor, fully furnished","short_post_title_en":"","post_description_en":":: Room Details ::\r\n- Size 105 sqm.\r\n- Type 2 bed 2 bath\r\n- Fully furnished and electric appliances\r\n- Building 1, Floor 33\r\n- Balcony facing the city view\r\n\r\n:: Project Details ::\r\nProject Name: WaterMark Chaopraya River\r\nProject Owner: Major Development\r\nProject Area: 11 Rai\r\nNumber of building: 2\r\n52 floors 486 units', 'price_baht': '12312321', 'listing_type': 'ขาย', 'post_images': [os.getcwd() + '/download.jpeg']}
# a=thisads()
# a.func_delete_all(temp)
