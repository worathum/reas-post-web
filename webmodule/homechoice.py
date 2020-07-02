# -*- coding: utf-8 -*-

from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
import re
import json
import datetime
import sys
import requests

livingarea_options = {'บางซื่อ กรุงเทพนนท์ วงศ์สว่าง เตาปูน ประชาชื่น บางโพ ประชาราษฏร์': '1', 'รัตนาธิเบศร์ สนามบินน้ำ เลียบคลองประปา สามัคคี เรวดี': '2', 'บางกรวย ราชพฤกษ์ ติวานนท์ นครอินทร์ พระราม 5 พิบูลสงคราม ชัยพฤกษ์': '3', 'เมืองทอง ปากเกร็ด งามวงศ์วาน แคราย แจ้งวัฒนะ': '6', 'พระราม 8 สามเสน ราชวัตร ศรีย่าน ดุสิต': '7', 'สยาม จุฬาลงกรณ์ สามย่าน สนามกีฬาแห่งชาติ หัวลำโพง ปทุมวัน': '8', 'บางรัก สีลม สุรวงศ์ ศาลาแดง สี่พระยา': '9', 'ลุมพินี ร่วมฤดี วิทยุ เพลินจิต หลังสวน ชิดลม  สารสิน ราชดำริ': '10', 'พญาไท ราชปรารภ ราชเทวี รางน้ำ ประตูน้ำ': '11', 'ราชครู อารีย์ สนามเป้า อนุสาวรีย์': '12', 'หมอชิต สะพานควาย จตุจักร ประดิพัทธ์ อินทามะระ': '13', 'สุทธิสาร รัชดาภิเษก ห้วยขวาง ดินแดง ศูนย์วัฒนธรรม เหม่งจ๋าย': '14', 'พระราม 9 คลองตัน RCA เพชรบุรีตัดใหม่ ศูนย์วิจัย': '15', 'นานาฝั่งเหนือ นานาฝั่งใต้': '16', 'สุขุมวิท ทองหล่อ อโศก พร้อมพงศ์ เอกมัย ประสานมิตร': '17', 'พระโขนง อ่อนนุช ปุณณวิถี อุดมสุข บางจาก': '18', 'พระราม 4 คลองเตย กล้วยน้ำไท ท่าเรือ': '19', 'เจริญกรุง สาทร นราธิวาส ช่องนนทรี สุรศักดิ์ เซ้นต์หลุย เจริญราษฎร์': '20', 'พระราม 3 นางลิ้นจี่ ยานนาวา สาธุประดิษฐ์ เย็นอากาศ': '21', 'เยาวราช บางลำพู พระนคร ป้อมปราบ สัมพันธวงศ์': '22', 'รัชโยธิน เสือใหญ่ เกษตรศาสตร์ เสนานิคม วังหิน รัชวิภา': '23', 'สุคนธสวัสดิ์ เกษตร-นวมินทร์ (ประเสริฐมนูกิจ) ลาดปลาเค้า นวลจันทร์ มัยลาภ ': '24', 'เลียบทางด่วนรามอินทรา (ประดิษฐ์มนูธรรม) โยธินพัฒนา CDC ศรีวรา': '25', 'รามอินทรา  วัชรพล สายไหม นวมินทร์ แฟชั่นไอส์แลนด์ สุขาภิบาล 5 หทัยราษฏร์': '26', 'เซ็นทรัลลาดพร้าว ลาดพร้าวตอนต้น ห้าแยกลาดพร้าว โชคชัยร่วมมิตร': '27', 'ลาดพร้าวตอนกลาง โชคชัย 4 ลาดพร้าว 71 นาคนิวาส': '28', 'เดอะมอลล์บางกะปิ ลาดพร้าวตอนปลาย มหาดไทย แฮปปี้แลนด์ ลาดพร้าว 101': '29', 'พัฒนาการ กรุงเทพกรีฑา ศรีนครินทร์ สวนหลวง อ่อนนุช (ตอนปลาย)': '30', 'ม.รามคำแหง บางนา สรรพวุธ ลาซาล แบริ่ง สันติคาม 2 เมกะบางนา': '31', 'รามคำแหงตอนต้น มหาวิทยาลัยรามคำแหง หัวหมาก เอแบค บดินทรเดชา ทาวน์อินทาวน์': '32', 'รามคำแหงตอนกลาง เสรีไทย นิด้า สุขาภิบาล 2': '33', 'ร่มเกล้า รามคำแหงตอนปลาย ซอยมิสทีน มีนบุรี หนองจอก สุวินทวงศ์': '34', 'บางปู สมุทรปราการ สำโรง เทพารักษ์ แพรกษา ปู่เจ้าสมิงพราย ศรีด่าน ปากน้ำ': '35', 'สุวรรณภูมิ มอเตอร์เวย์ ลาดกระบัง เฉลิมพระเกียรติ ประเวศ': '36', 'วงเวียนใหญ่ อิสรภาพ เจริญนคร ตากสิน กรุงธนบุรี': '37', 'เทอดไท กัลปพฤกษ์ ท่าพระ ตลาดพลู โพธิ์นิมิตร วุฒากาศ บางหว้า': '38', 'ปิ่นเกล้า บรมราชชนนี อรุณอัมรินทร์ ราชพฤกษ์ จรัญสนิทวงศ์ บางอ้อ บางพลัด ตลิ่งชัน': '39', 'บางบอน กัลปพฤกษ์ ดาวคะนอง จอมทอง เอกชัย': '40', 'ประชาอุทิศ ราษฎร์บูรณะ พุทธบูชา สุขสวัสดิ์ ทุ่งครุ': '41', 'พระราม 2 ท่าข้าม บางขุนเทียน เทียนทะเล': '42', 'บางแค ภาษีเจริญ หนองแขม เพชรเกษม': '43', 'บางบัวทอง บางใหญ่ ไทรน้อย ไทรม้า ท่าอิฐ นนทบุรี': '44', 'รังสิต ธรรมศาสตร์ คลองหลวง ปทุมธานี': '45', 'สรงประภา หลักสี่  วิภาวดี ดอนเมือง สะพานใหม่ ลำลูกกา': '46', 'นครปฐม พุทธมณฑล ศาลายา ศาลาธรรมสพน์ เลียบคลองทวีวัฒนา': '47', 'พระนครศรีอยุธยา สุพรรณบุรี': '48', 'กำแพงเพชร': '49', 'ชัยนาท': '50', 'นครนายก': '51', 'นครสวรรค์': '52', 'พิจิตร': '53', 'พิษณุโลก': '54', 'เพชรบูรณ์': '55', 'ลพบุรี': '56', 'สมุทรสงคราม': '57', 'มหาชัย สมุทรสาคร': '58', 'สิงห์บุรี': '59', 'สุโขทัย': '60', 'สระบุรี': '61', 'อ่างทอง': '62', 'อุทัยธานี': '63', 'เชียงใหม่': '64', 'เชียงราย': '65', 'น่าน': '66', 'พะเยา': '67', 'แพร่': '68', 'แม่ฮ่องสอน': '69', 'ลำปาง': '70', 'ลำพูน': '71', 'อุตรดิตถ์': '72', 'หัวหิน ปราณบุรี ประจวบคีรีขันธ์': '73', 'กาญจนบุรี': '74', 'ตาก': '75', 'ชะอำ เพชรบุรี': '76', 'ราชบุรี': '77', 'พัทยา บางแสน ศรีราชา ชลบุรี': '78', 'จันทบุรี': '79', 'ฉะเชิงเทรา': '80', 'ตราด': '81', 'ปราจีนบุรี': '82', 'ระยอง': '83', 'สระแก้ว': '84', 'นครราชสีมา เขาใหญ่': '85', 'ขอนแก่น': '86', 'กาฬสินธุ์': '87', 'ชัยภูมิ': '88', 'นครพนม': '89', 'บึงกาฬ': '90', 'บุรีรัมย์': '91', 'มหาสารคาม': '92', 'มุกดาหาร': '93', 'ยโสธร': '94', 'ร้อยเอ็ด': '95', 'เลย': '96', 'ศรีสะเกษ': '97', 'สกลนคร': '98', 'สุรินทร์': '99', 'หนองคาย': '100', 'หนองบัวลำภู': '101', 'อำนาจเจริญ': '102', 'อุดรธานี': '103', 'อุบลราชธานี': '104', 'ภูเก็ต ป่าตอง': '105', 'กระบี่': '106', 'ชุมพร': '107', 'ตรัง': '108', 'นครศรีธรรมราช': '109', 'นราธิวาส': '110', 'ปัตตานี': '111', 'พังงา': '112', 'พัทลุง': '113', 'ยะลา': '114', 'ระนอง': '115', 'หาดใหญ่ สงขลา': '116', 'สตูล': '117', 'สมุย สุราษฎร์ธานี': '118'}
property_types = {
    '1': 'คอนโด',
    '2': 'บ้านเดี่ยว',
    '3': 'บ้านแฝด',
    '4': 'ทาวน์เฮ้าส์',
    '5': 'ตึกแถว-อาคารพาณิชย์',
    '6': 'ที่ดิน',
    '7': 'อพาร์ทเมนท์',
    '8': 'โรงแรม',
    '9': 'ออฟฟิศสำนักงาน',
    '10': 'โกดัง-โรงงาน',
    '25': 'โรงงาน'
}
httprequestObj = lib_httprequest()


class homechoice():
    name = 'homechoice'
    site_name = "https://www.xn--22ce1cbmnb1e9exbzak9o1c.com"
    to_web = "https://\u0E02\u0E32\u0E22\u0E17\u0E35\u0E48\u0E14\u0E34\u0E19\u0E04\u0E2D\u0E19\u0E42\u0E14.com"

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



    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        success = "false"
        detail = 'An Error has Occurred'

        datapost = {
            "to_web": self.to_web,
            "first_name": postdata['name_th'], 
            "last_name": postdata['surname_th'],
            "email": postdata['user'],
            "password": postdata['pass'],
            "link": "-",
            "tel": postdata['tel'],
            "line": postdata['line']
        }
        
        response = httprequestObj.http_post(self.site_name+'/insert/insert_user.php', data=datapost)

        popup_responses = {
            '1':"Membership is successful!. You can log in immediately!", 
            '2':"An error has occurred. Unable to apply for membership" ,
            '3':"An error has occurred. This email is already in use. Please check again."
        }
        
        if response.status_code==200:
            # get response code i.e. 1,2 or 3 from javascript
            parsed_response = re.split("showResult_user\('",response.text)
            
            if len(parsed_response)>1:
                if parsed_response[1][0]=='1':
                    success = "true"
                detail = popup_responses[parsed_response[1][0]] 
        else:
            detail = 'An Error has occurred with response_code '+str(response.status_code) 
            # # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            'ds_id': postdata['ds_id'],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": self.name
        }



    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        
        # start process
        success = "false"
        detail = 'An Error has Occurred'

        datapost = {
            "to_web": self.to_web,
            "email": postdata['user'],
            "password": postdata['pass']
        }
        response = httprequestObj.http_post(self.site_name+'/chk_login.php', data=datapost)

        popup_responses = {
            '1':"Login successful!. Happy to receive your return again!",
            '2':"An error has occurred. This user cannot be found. Please check again." ,
            '3':"An error has occurred. Incorrect password. Please check again.", 
            '4':"An error has occurred. Your email has been blocked. In order to Login, Please contact staff"
        }

        if response.status_code==200:
            # get response code i.e. 1,2, 3 or 4 from javascript
            parsed_response = re.split("showResult_login\('",response.text)
            
            if len(parsed_response)>1:
                if parsed_response[1][0]=='1':
                    success = "true"
                detail = popup_responses[parsed_response[1][0]] 
        else:
            detail = 'An Error has occurred with response_code '+str(response.status_code) 
        
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": self.name,
            "ds_id": postdata['ds_id'],
        }
    

    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        # login

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""

        if 'web_project_name' not in postdata or postdata['web_project_name'] is None:
            if 'project_name' in postdata and postdata['project_name'] is not None:
                postdata['web_project_name'] = postdata['project_name']
            else:
                postdata['web_project_name'] = postdata['post_title_th']
        
        if success=="true":
            r = httprequestObj.http_get(self.site_name+'/create_post.html')
            soup = BeautifulSoup(r.text, features=self.parser)
            teedin_target = soup.find(attrs={"name":"at_target"}).get('value')
           
            teedin_type = 2
            if postdata['listing_type']=='ขาย':
                teedin_type = 1
            
            teedin_livingarea = '1'
            for i in livingarea_options.keys():
                if postdata['addr_sub_district'] in i:
                    teedin_livingarea = livingarea_options[i]
                    break
                elif postdata['addr_district'] in i:
                    teedin_livingarea = livingarea_options[i]
                    break
                elif postdata['addr_province'] in i:
                    teedin_livingarea = livingarea_options[i]
                    break
            
            postimage_url = self.site_name+'/dropzonejs_upimg/uploadp.php?at_target='+teedin_target+'&url=https://xn--22ce1cbmnb1e9exbzak9o1c.com'
            for each_img in postdata['post_images'][:21]:
                r = httprequestObj.http_post(postimage_url, data={}, files={"file":open(os.getcwd()+"/"+each_img, 'rb')})
                if r.status_code>=400:
                    status = "false"
                    detail = "unable to upload image(s)"
            
            if success=="true":
                if 'land_size_ngan' not in postdata or postdata['land_size_ngan'] == None:
                    postdata['land_size_ngan'] = 0
                if 'land_size_rai' not in postdata or postdata['land_size_rai'] == None:
                    postdata['land_size_rai'] = 0
                if 'land_size_wa' not in postdata or postdata['land_size_wa'] == None:
                    postdata['land_size_wa'] = 0
                try:
                    postdata['land_size_ngan'] = int(postdata['land_size_ngan'])
                except ValueError:
                    postdata['land_size_ngan'] = 0
                try:
                    postdata['land_size_rai'] = int(postdata['land_size_rai'])
                except ValueError:
                    postdata['land_size_rai'] = 0
                try:
                    postdata['land_size_wa'] = int(postdata['land_size_wa'])
                except ValueError:
                    postdata['land_size_wa'] = 0

                description = '<p>'+postdata['post_description_th']
                description = description.replace('\n','</p><p>')
                if description[-3:]=='<p>':
                    description = description[:-3]
                
                datapost= {
                    "teedin_target": teedin_target,
                    "teedin_to_web": self.to_web,
                    "teedin_title": postdata['post_title_th'],
                    "teedin_type": teedin_type,
                    "teedin_livingarea": teedin_livingarea,
                    "teedin_price": postdata['price_baht'],
                    "teedin_area": 400*postdata['land_size_rai'] + 100*postdata['land_size_ngan'] + postdata['land_size_wa'],
                    "teedin_youtube": "-",
                    "teedin_key": property_types[str(postdata['property_type'])],
                    "teedin_des": postdata['post_title_th'],
                    "teedin_ggmap":"",
                    "teedin_detail": description,
                    "teedin_latitude": postdata['geo_latitude'],
                    "teedin_longitude": postdata['geo_longitude'],       
                    "at_target": teedin_target
                }

                response = httprequestObj.http_post(self.site_name+'/insert/insert_post.php', data=datapost)
                popup_responses = {'1': 'Success announcement! We have received your announcement!', '2':'An error has occurred. Cannot announce at this time. The system is editing'}
                success = "false"
                if response.status_code==200:
                    detail = "Post created successfully"
                    parsed_response = re.split("showResult_post\('",response.text)
            
                    if len(parsed_response)>1:
                        if parsed_response[1][0]=='1':
                            success = "true"
                            r = httprequestObj.http_get(self.site_name+'/my_property.html')
                            soup = BeautifulSoup(r.text, features=self.parser)
                            all_posts = soup.find_all(class_="utf_list_box_listing_item")
                            for post in all_posts[::-1]:
                                if post.find('h3').getText()==postdata['post_title_th']:
                                    post_link = post.find('a').get('href')
                                    post_id = post_link.replace('/post/', '').replace('html','')
                                    post_url = self.site_name + post_link
                                    break
                        detail = popup_responses[parsed_response[1][0]] 
                else:
                    detail = 'Unable to create post. An Error has occurred with response_code '+str(response.status_code) 
        else:
            detail = "cannot login"
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
            "websitename": self.name
        }



    def edit_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        # login

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = "Unable to update post."
        post_id = ""
        post_url = ""

        if 'web_project_name' not in postdata or postdata['web_project_name'] is None:
            if 'project_name' in postdata and postdata['project_name'] is not None:
                postdata['web_project_name'] = postdata['project_name']
            else:
                postdata['web_project_name'] = postdata['post_title_th']
        
        if success=="true":
            r = httprequestObj.http_get(self.site_name+'/my_property.html')
            soup = BeautifulSoup(r.text, features=self.parser)
            all_posts = soup.find_all(class_="utf_list_box_listing_item")
            post_url = '/post/'+postdata['post_id']+'.html'

            flag = 0
            for post in all_posts:
                if post.find('a').get('href')==post_url:    
                    flag = 1
                    break
            if flag==1:
                r = httprequestObj.http_get(self.site_name+'/edit_post/'+postdata['post_id']+'.html')
                soup = BeautifulSoup(r.text, features=self.parser)
                teedin_target = soup.find(attrs={"name":"at_target"}).get('value')
            
                teedin_type = 2
                if postdata['listing_type']=='ขาย':
                    teedin_type = 1
                
                teedin_livingarea = '1'
                for i in livingarea_options.keys():
                    if postdata['addr_sub_district'] in i:
                        teedin_livingarea = livingarea_options[i]
                    elif postdata['addr_district'] in i:
                        teedin_livingarea = livingarea_options[i]
                    elif postdata['addr_province'] in i:
                        teedin_livingarea = livingarea_options[i]
                
                postimage_url = self.site_name+'/dropzonejs_upimg/uploadp.php?at_target='+teedin_target+'&url=https://xn--22ce1cbmnb1e9exbzak9o1c.com'
                for each_img in postdata['post_images'][:21]:
                    r = httprequestObj.http_post(postimage_url, data={}, files={"file":open(os.getcwd()+"/"+each_img, 'rb')})
                    if r.status_code>=400:
                        status = "false"
                        detail = "unable to upload image(s)"
                
                if success=="true":
                    if 'land_size_ngan' not in postdata or postdata['land_size_ngan'] == None:
                        postdata['land_size_ngan'] = 0
                    if 'land_size_rai' not in postdata or postdata['land_size_rai'] == None:
                        postdata['land_size_rai'] = 0
                    if 'land_size_wa' not in postdata or postdata['land_size_wa'] == None:
                        postdata['land_size_wa'] = 0
                    try:
                        postdata['land_size_ngan'] = int(postdata['land_size_ngan'])
                    except ValueError:
                        postdata['land_size_ngan'] = 0
                    try:
                        postdata['land_size_rai'] = int(postdata['land_size_rai'])
                    except ValueError:
                        postdata['land_size_rai'] = 0
                    try:
                        postdata['land_size_wa'] = int(postdata['land_size_wa'])
                    except ValueError:
                        postdata['land_size_wa'] = 0

                    description = '<p>'+postdata['post_description_th']
                    description = description.replace('\n','</p><p>')
                    if description[-3:]=='<p>':
                        description = description[:-3]
                    
                    datapost= {
                        "edit": postdata['post_id'],
                        "teedin_title": postdata['post_title_th'],
                        "teedin_type": teedin_type,
                        "teedin_livingarea": teedin_livingarea,
                        "teedin_price": postdata['price_baht'],
                        "teedin_area": 400*postdata['land_size_rai'] + 100*postdata['land_size_ngan'] + postdata['land_size_wa'],
                        "teedin_youtube": "-",
                        "teedin_key": property_types[str(postdata['property_type'])],
                        "teedin_des": postdata['post_title_th'],
                        "teedin_ggmap":"",
                        "teedin_detail": description,
                        "teedin_latitude": postdata['geo_latitude'],
                        "teedin_longitude": postdata['geo_longitude'],       
                        "at_target": teedin_target
                    }

                    response = httprequestObj.http_post(self.site_name+'/insert/update_post.php', data=datapost)
                    popup_responses = {'1': 'Successful update announcement! We have received information to update your announcement!', '2':'An error has occurred. Cannot announce at this time. The system is editing'}
                    success = "false"
                    if response.status_code==200:
                        parsed_response = re.split("showResult_post\('",response.text)
                
                        if len(parsed_response)>1:
                            if parsed_response[1][0]=='1':
                                success = "true"
                            detail = popup_responses[parsed_response[1][0]] 
                    else:
                        detail = 'Unable to update post. An Error has occurred with response_code '+str(response.status_code) 
            else:
                success = "false"
                detail  = "No post found with given id"
        else:
            detail = "cannot login"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "log_id": postdata['log_id'],
            "account_type": "null",
            "detail": detail,
            "websitename": self.name
        }



    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]

        if success=="true":
            r = httprequestObj.http_get(self.site_name+'/my_property.html')
            soup = BeautifulSoup(r.text, features=self.parser)
            all_posts = soup.find_all(class_="utf_list_box_listing_item")
            post_url = '/post/'+postdata['post_id']+'.html'

            flag = 0
            for post in all_posts:
                if post.find('a').get('href')==post_url:    
                    response = httprequestObj.http_get(self.site_name+'/my_property/'+postdata['post_id']+'.html')
                    if response.status_code==200:
                        detail = "Post deleted successfully!"
                    else:
                        success = "false"
                        detail = "Unable to delete post. An Error has occurred with response_code "+str(response.status_code) 
                    flag = 1
                    break
            if flag==0:
                success = "false"
                detail = "No post found with given id"
        else:
            detail = "Unable to login"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": self.name,
            "log_id": postdata['log_id'],
        }
    

    def search_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        post_url = ""
        post_id = ""
        post_found = ""
        post_modify_time = ""
        post_create_time = ""
        post_view = ""

        if success == "true":
            post_found = "false"
            detail = "No post found with given title"
            post_title = postdata['post_title_th']

            response = httprequestObj.http_get(self.site_name+'/my_property.html')
            if response.status_code==200:
                soup = BeautifulSoup(response.text, features=self.parser)
                all_posts = soup.find_all(class_="utf_list_box_listing_item")

                flag = 0
                for post in all_posts:
                    if post.find('h3').getText()==post_title:    
                        post_found = "true"
                        detail = "Post found successfully"
                        post_url = self.site_name + post.find('a').get('href')
                        post_id = post.find('a').get('href').replace('/post/','').replace('.html','')
                        break
            else:
                success = "false"
                detail = "Unable to search. An Error has occurred with response_code "+str(response.status_code)     
        else:
            detail = "Unable to login"
            
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": self.name,
            "account_type": None,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "post_create_time": post_create_time,
            "post_modify_time": post_modify_time,
            "post_view": post_view,
            "post_url": post_url,
            "post_found": post_found
        }



    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        
        if success=="true":
            r = httprequestObj.http_get(self.site_name+'/my_property.html')
            soup = BeautifulSoup(r.text, features=self.parser)
            all_posts = soup.find_all(class_="utf_list_box_listing_item")
            post_url = '/post/'+postdata['post_id']+'.html'

            flag = 0
            for post in all_posts:
                if post.find('a').get('href')==post_url:    
                    flag = 1
                    r = httprequestObj.http_get(self.site_name+'/edit_post/'+postdata['post_id']+'.html')
                    soup = BeautifulSoup(r.text, features=self.parser)
                    form = soup.find(attrs={'name':'frm', 'action':'../insert/update_post.php'})
                    teedin_type = form.find(attrs={'name':'teedin_type'}).find('option', selected=True).get('value')
                    teedin_livingarea = form.find(attrs={'name':'teedin_livingarea'}).find('option', selected=True).get('value')
                    teedin_latitude, teedin_longitude = '0', '0'
                    for script in soup.find_all('script', {"src":False, "type":False, "language":False}):
                        if 'function init() {' in script.string:
                            lat = re.split("var a1 = '",script.string)[1]
                            lng = re.split("var a2 = '",script.string)[1]
                            teedin_latitude = lat[:lat.index("'")]
                            teedin_longitude = lng[:lng.index("'")]
                            break
                        
                    datapost= {
                            "edit": postdata['post_id'],
                            "teedin_title": form.find(attrs={'name':'teedin_title'}).get('value'),
                            "teedin_type": teedin_type,
                            "teedin_livingarea": teedin_livingarea,
                            "teedin_price": form.find(attrs={'name':'teedin_price'}).get('value'),
                            "teedin_area": form.find(attrs={'name':'teedin_area'}).get('value'),
                            "teedin_youtube": "-",
                            "teedin_key": form.find(attrs={'name':'teedin_key'}).get('value'),
                            "teedin_des": form.find(attrs={'name':'teedin_des'}).get('value'),
                            "teedin_ggmap": "",
                            "teedin_detail": form.find(attrs={'name':'teedin_detail'}).get('value'),
                            "teedin_latitude": teedin_latitude,
                            "teedin_longitude": teedin_longitude,       
                            "at_target": form.find(attrs={'name':'at_target'}).get('value')
                        }
                    response = httprequestObj.http_post(self.site_name+'/insert/update_post.php', data=datapost)
                    
                    popup_responses = {'1': 'Post boosted!', '2':'An error has occurred. Cannot announce at this time. The system is editing'}
                    success = "false"
                    if response.status_code==200:
                        detail = "Unable to boost post"
                        parsed_response = re.split("showResult_post\('",response.text)
            
                        if len(parsed_response)>1:
                            if parsed_response[1][0]=='1':
                                success = "true"
                            detail = popup_responses[parsed_response[1][0]] 
                    else:
                        detail = 'Unable to boost post. An Error has occurred with response_code '+str(response.status_code) 
                    break
            if flag==0:
                success = "false"
                detail  = "No post found with given id"
        else:
            detail = "Unable to login"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "log_id": postdata['log_id'],
            "websitename": self.name,
        }



    def print_debug(self, msg):
        if(self.debug == 1):
            print(msg)
        return True

    def print_debug_data(self, data):
        if(self.debugdata == 1):
            print(data)
        return True

        if(self.debugdata == 1):
            print(data)
        return True
