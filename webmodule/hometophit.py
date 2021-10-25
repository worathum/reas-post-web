

from .lib_httprequest import *
import random
from bs4 import BeautifulSoup
import os.path
# from urlparse import urlparse
import re
import json,time
import datetime
import sys
import requests
import shutil
from urllib.parse import unquote
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
# from googletrans import Translator
# translator = Translator()

def set_end_time(start_time):
    time_end = datetime.datetime.utcnow()
    time_usage = time_end - start_time
    return time_end, time_usage

class hometophit():

    name = 'hometophit'

    def __init__(self):

        try:
            import configs

        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.debug = 1
        self.debugresdata = 0
        self.parser = 'html.parser'
        self.httprequestObj = lib_httprequest()

    def logout_user(self):
        url = 'http://hometophit.com/hometh/logout.php'
        self.httprequestObj.http_get(url)

    def register_user(self, postdata):
        self.logout_user()
        start_time=datetime.datetime.utcnow()

        res = {
            'websitename':'hometophit', 
            'success':"false", 
            'start_time': str(start_time), 
            'end_time': '0', 
            'ds_id': postdata['ds_id'], 
            'usage_time': '0', 
            'detail': ''
        }

        register_data1={}
        register_data2={}

        data=postdata
        try:
            register_data1['mem_user']=data['user'].split("@")[0]
            register_data1['mem_pwd']=data['pass']
            register_data1['conf_pwd']=data['pass']
            register_data1['mem_email']=data['user']
        except:
            res['detail']+='JSON format wrong'
            res['end_time'],res['usage_time']=set_end_time(start_time)
            return res

        posturl='http://hometophit.com/hometh/register_check.php'

        userpass_regex=re.compile(r'^([a-zA-Z0-9_]{4,15})$')
        email_regex=re.compile(r'^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$')

        if(userpass_regex.search(register_data1['mem_user'])==None):
            print(register_data1['mem_user'])
            res['detail']+='User Name must be in az, AZ, 0-9 or _ only and should be 4-15 characters only.'
        if(userpass_regex.search(register_data1['mem_pwd'])==None):
            res['detail']+='Password must be in az, AZ, 0-9 or _ only and should be 4-15 characters only.'
        if(email_regex.search(register_data1['mem_email'])==None):
            res['detail']+='Invalid email. '
        if(res['detail'] != ''):
            res['end_time'],res['usage_time']=set_end_time(start_time)
            return res

        r = self.httprequestObj.http_post(posturl, data = register_data1)
        res['websitename']='hometophit'

        if r.encoding is None or r.encoding == 'ISO-8859-1':
            r.encoding = r.apparent_encoding

        user_dup_regex=re.compile(r'User Name.*มีสมาชิกท่านอื่นใช้แล้ว')
        email_dup_regex=re.compile(r'E-Mail.*มีสมาชิกท่านอื่นใช้แล้ว')

        if(user_dup_regex.search(r.text)!=None):
            res['detail']+='Username already in use.'
        if(email_dup_regex.search(r.text)!=None):
            res['detail']+='E-mail already in use.'
        if(res['detail']!=''):
            res['end_time'],res['usage_time']=set_end_time(start_time)
            return res

        try:
            register_data2['mem_name']=data['name_th']+' '+data['surname_th']
            register_data2['mem_sex']="1"
            register_data2['b_date']='01'
            register_data2['b_month']='01'
            register_data2['b_year']='2000'
            register_data2['mem_maritial']="0"
            register_data2['mem_edu']='01'
            register_data2['mem_occ']='01'
            register_data2['mem_salary']='2500'
            register_data2['mem_add']='house_no,street'
            register_data2['mem_city']='1'
            register_data2['mem_province']='10400'
            register_data2['mem_zip']='50003'
            register_data2['mem_tel']=data['tel']
            register_data2['mem_fax']=''
            register_data2['mem_mobile']=data['tel']
            register_data2['mem_news']='1'
            register_data2['mem_user']=data['user'].split("@")[0]
            register_data2['mem_pwd']=data['pass']
            register_data2['mem_email']=data['user']
        except:
            res['detail']+='JSON format wrong'
            res['end_time'],res['usage_time']=set_end_time(start_time)
            return res

        phone_regex=re.compile(r'^([0-9]{8,10})$')

        if(len(data['name_th'])<1 or len(data['surname_th'])<1):
            res['detail']+='First name and surname must be at least 1 character long.'
        if(phone_regex.search(register_data2['mem_tel'])==None):
            res['detail']+='Invalid phone number.'
        if(res['detail']!=''):
            res['end_time'],res['usage_time']=set_end_time(start_time)
            return res

        posturl='http://hometophit.com/hometh/submit_msn.php'

        r = self.httprequestObj.http_post(posturl, data = register_data2)
        res['websitename']="hometophit"

        if r.encoding is None or r.encoding == 'ISO-8859-1':
            r.encoding = r.apparent_encoding

        if(r.text==''):
            res['detail']+='Something went wrong.'
        else:
            res['success']="true"
            res['detail']+='User successfully registered'

        res['end_time'],res['usage_time']=set_end_time(start_time)
        
        return res

    def test_login(self, postdata):
        self.logout_user()
        start_time=datetime.datetime.utcnow()

        res = {
            'websitename':'hometophit', 
            'success':"false", 
            'start_time': str(start_time), 
            "ds_id": postdata['ds_id'], 
            'end_time': '0', 
            'usage_time': '0', 
            'detail': ''
        }

        posturl='http://hometophit.com/hometh/secure.php'

        login_data={}
        
        try:
            login_data['mem_user']=postdata['user'].split("@")[0]
            login_data['mem_pwd']=postdata['pass']
        except:
            res['detail']+='JSON format wrong'
            res['end_time'],res['usage_time']=set_end_time(start_time)
            return res

        r = self.httprequestObj.http_post(posturl, data = login_data)

        if r.encoding is None or r.encoding == 'ISO-8859-1':
            r.encoding = r.apparent_encoding

        res['websitename']="hometophit"

        if(r.url=='http://hometophit.com/hometh/mem_panel.php'):
            res['success']="true"
            res['detail']='user logged in'
        else:
            res['success']="false"
            print(r.text)
            if('<SCRIPT LANGUAGE="JavaScript">window.location = "login.php";alert' in r.text):
                res['detail']='username or pass wrong. Please try again'
            else:
                res['detail']='some problem happened. Please try later'

        res['end_time'],res['usage_time']=set_end_time(start_time)
        
        return res

    '''def edit_post(self, postdata):
        # self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()
        data = postdata
        res_login = self.test_login(postdata)
        if (res_login['success'] == "false"):
            return res_login
        res = {'websitename': 'hometophit', 'success': "false", 'start_time': str(start_time), 'end_time': '0',
               'usage_time': '0', 'detail': '', 'account_type': "null", }
        create = {}
        driver = webdriver.Chrome()
        driver.get("http://www.hometophit.com/hometh/home_edit.php?home_id=1024545")
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
        property_tp = {
            "1": "03",
            "2": "11",
            "3": "13",
            "4": "06",
            "5": "05",
            "6": "07",
            "7": "25",
            "8": "20",
            "9": "26",
            "10": "02",
            "25": "19"
        }
        if data['property_type'] not in property_tp:
            data['property_type'] = ids[data['property_type']]
        try:
            create['home_name'] = data['post_title_th']
            create['home_type'] = property_tp[data['property_type']]
            create['home_for'] = 2 if data['listing_type'] == "ขาย" else 4
            create['home_timeshow'] = 4
            create['area'] = data['land_size_wa']
            create['areatype'] = 2 if data['property_type'] == "1" else 1
            create['home_floor'] = data['floor_level']
            create['home_detail'] = data['post_description_th']
            if data['listing_type'] == "ขาย":
                create['home_price'] = data['price_baht']
            else:
                create['home_rent'] = data['price_baht']
            create['home_project'] = data['project_name']
            create['home_address'] = data['addr_soi'] + ', ' + data['addr_road'] + ', ' + data['addr_sub_district']
            create['mem_city'] = '1'
            create['mem_province'] = '10400'
            create['home_id'] = data['post_id']
        #         print(create)
        except:
            res['detail'] += 'Error in json input2'
            #         print(create)
            res['end_time'], res['usage_time'] = set_end_time(start_time)
            return res
        post_id = data['post_id']
        posturl = 'http://hometophit.com/hometh/mem_panel.php'
        r = self.httprequestObj.http_get(posturl)
        listed_reg = r'\"home_view\.php\?home_id=' + post_id + '\"'
        if re.search(listed_reg, r.text, re.DOTALL) is None:
            res['detail'] = 'Post not found.'
            # res['websitename']=r.url
            res['end_time'], res['usage_time'] = set_end_time(start_time)
            return res
        posturl = 'http://hometophit.com/hometh/update_homepost.php'
        r = self.httprequestObj.http_post(posturl, data=create)

        #     print(r.cookies,r.history[0].cookies)
        # res['websitename']=r.url
        if r.encoding is None or r.encoding == 'ISO-8859-1':
            r.encoding = r.apparent_encoding
        #     print(r.text)
        webpage_text = r.text
        page_reg = r"home_view.*?&"
        id_reg = r"home_id.*?&"
        res['post_id'] = post_id
        res['post_url'] = "http://hometophit.com/hometh/update_home_uptime.php?home_id=" + post_id
        if (r.text == ''):
            res['detail'] += 'Something went wrong. '
        else:
            res['success'] = "true"
            res['detail'] += 'Edited'
        res['end_time'], res['usage_time'] = set_end_time(start_time)
        return res'''

    def edit_post(self,postdata):
        data = postdata
        start_time = datetime.datetime.utcnow()

        res_login = self.test_login(postdata)
        if (res_login['success'] == "false"):
            return res_login
        res = {'websitename': 'hometophit', 'success': "false", 'start_time': str(start_time), 'end_time': '0',
               'usage_time': '0', 'detail': '', 'account_type': "null", "ds_id": postdata['ds_id'], "post_id": postdata['post_id']}
        create = {}
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
        property_tp = {
            "1": "03",
            "2": "11",
            "3": "13",
            "4": "06",
            "5": "05",
            "6": "07",
            "7": "25",
            "8": "20",
            "9": "26",
            "10": "19",
            "25": "19"
        }
        # print('here')
        data['property_type'] = str(data['property_type'])
        if data['property_type'] not in property_tp:
            data['property_type'] = ids[data['property_type']]
        try:
            print('here1')
            create['home_name'] = str(data['post_title_th'])
            # create['home_name']=(data['post_title_th'])
            # print('here2')
            create['home_type'] = property_tp[data['property_type']]
            # print('here3')
            create['home_for'] = 2 if data['listing_type'] == "ขาย" else 4
            # print('here4')
            create['home_timeshow'] = 4
            # print('here5')
            if data['floor_area'] is not None and data['floor_area'] != '':
                create['home_area'] = data['floor_area']
            #print('area',data['land_size_wa'])
            # print('here6')
            create['home_areatype'] = 2
            # print('here7')
            if data['floor_total'] is not None and data['floor_total'] != '':
                if int(data['floor_total'])<=50:
                    create['home_floor'] = data['floor_total']
                else:
                    create['home_floor'] = '99'
            # print('here8')
            create['home_detail'] = str(data['post_description_th'])

            # create['home_detail'] = str(soup)

            if data['listing_type'] == "ขาย":
                create['home_price'] = data['price_baht']
            else:
                create['home_rent'] = data['price_baht']
            if 'web_project_name' not in data or data['web_project_name'] is None or data['web_project_name'] == "":
                if 'project_name' in data and data['project_name'] is not None:
                    data['web_project_name'] = data['project_name']
                else:
                    data['web_project_name'] = data['post_title_th']

            create['home_project'] = data['web_project_name']
            print('here9')
            # print(data['addr_soi'],data['addr_road'],data['addr_sub_district'])
            if data['addr_soi'] == None:
                data['addr_soi'] = ''
            if data['addr_road'] == None:
                data['addr_road'] = ''
            if data['addr_sub_district'] == None:
                data['addr_sub_district'] = ''

            create['home_address'] = data['addr_soi'] + ', ' + data['addr_road'] + ', ' + data['addr_sub_district']
            print(create['home_address'])
            create['home_address'] = str(create['home_address'])
            print(create['home_address'])
            print('here10')
            if data['bed_room'] is not None and data['bed_room']!='':
                if int(data['bed_room'])<=10:
                    create['home_bedr'] = data['bed_room']
                else:
                    create['home_bedr'] = '99'
            if data['bath_room'] is not None and data['bath_room']!='':
                if int(data['bath_room'])<=10:
                    create['home_bathr'] = data['bath_room']
                else:
                    create['home_bathr'] = '99'
            print('debug')
            create['mem_city'] = '1'
            create['mem_province'] = '10400'
            if 'post_images' in data and len(data['post_images']) > 0:
                pass
            else:
                data['post_images'] = ['./imgtmp/default/white.jpg']
            file = []
            temp = 1

            if len(data['post_images']) <= 4:
                for i in data['post_images']:
                    y = str(random.randint(0, 100000000000000000)) + ".jpg"
                    # print(y)
                    if temp != 1:
                        file.append((str('home_pic' + str(temp)), (y, open(i, "rb"), "image/jpg")))
                    else:
                        file.append((str('home_pic'), (y, open(i, "rb"), "image/jpg")))
                    temp = temp + 1

            else:
                for i in data['post_images'][:4]:
                    y = str(random.randint(0, 100000000000000000)) + ".jpg"
                    # print(y)
                    if temp != 1:
                        file.append((str('home_pic' + str(temp)), (y, open(i, "rb"), "image/jpg")))
                    else:
                        file.append((str('home_pic'), (y, open(i, "rb"), "image/jpg")))
                    temp = temp + 1
        #         print(create)
        except Exception as e:
            # print(e)
            res['detail'] += 'Error in json input2'
            #         print(create)
            res['end_time'], res['usage_time'] = set_end_time(start_time)
            return res

        print('fin')
        post_id = data['post_id']
        posturl = 'http://hometophit.com/hometh/mem_panel.php'
        r = self.httprequestObj.http_get(posturl)
        listed_reg = r'\"home_view\.php\?home_id=' + post_id + '\"'
        if re.search(listed_reg, r.text, re.DOTALL) is None:
            res['detail'] = 'Post not found.'
            # res['websitename']=r.url
            res['end_time'], res['usage_time'] = set_end_time(start_time)
            return res
        posturl = 'http://hometophit.com/hometh/update_homepost.php'
        create['Submit'] = '   record'
        create['home_id'] = post_id
        r = self.httprequestObj.http_post(posturl, data=create)
        #print(str(r.text).find('คลิ๊กที่นี่ เพื่อดูประกาศของท่าน.!'))

        #     print(r.cookies,r.history[0].cookies)
        # res['websitename']=r.url
        if r.encoding is None or r.encoding == 'ISO-8859-1':
            r.encoding = r.apparent_encoding
        #     print(r.text)
        webpage_text = r.text
        page_reg = r"home_view.*?&"
        id_reg = r"home_id.*?&"
        res['post_id'] = post_id
        res['post_url'] = "http://hometophit.com/hometh/home_view.php?home_id=" + post_id
        if (r.text == ''):
            res['detail'] += 'Something went wrong. '
        else:
            res['success'] = "true"
            res['detail'] += 'Edited'

        print('start')
        options = Options()
        options.set_headless(True)
        options.add_argument('--no-sandbox')
        success = ''
        detail = ''

        driver = webdriver.Chrome("./static/chromedriver",chrome_options=options)
        url = 'http://www.hometophit.com/hometh/login.php'
        driver.get(url)
        print('done')
        element = driver.find_element_by_name("mem_user")
        element.send_keys(data['user'].split("@")[0])
        print('done')
        element = driver.find_element_by_name("mem_pwd")
        element.send_keys(data['pass'])
        print('done')
        submit = driver.find_element_by_name("Submit")
        submit.click()
        print('done')
        success = 'true'
        detail = 'Login successful'
        try:
            ind = (driver.page_source)
        except:
            success = 'false'
            detail = 'Cannot Login'

        print(success,detail)
        if success == 'true':
            url = 'http://www.hometophit.com/hometh/home_edit.php?home_id='+str(data['post_id'])
            print('in')
            driver.get(url)




            elem = driver.find_element_by_name("home_name")
            elem.clear()
            elem.send_keys(str(data['post_title_th']),Keys.ARROW_DOWN)
            time.sleep(5)






            print('2')
            elem = driver.find_element_by_name("home_detail")
            # print('8')
            elem.clear()
            elem.send_keys(str(data['post_description_th']),Keys.ARROW_DOWN)
            time.sleep(5)
            print('3')



            print('4')
            try:
                driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)

                if 'web_project_name' not in data or data['web_project_name'] is None or data['web_project_name'] == "":
                    if 'project_name' in data and data['project_name'] is not None:
                        data['web_project_name'] = data['project_name']
                    else:
                        data['web_project_name'] = data['post_title_th']

                elem = driver.find_element_by_name("home_project")
                elem.clear()
                elem.send_keys(data['web_project_name'][:49],Keys.ARROW_DOWN)
                time.sleep(5)


                if data['addr_road'] == None:
                    data['addr_road'] = ''
                if data['addr_sub_district'] == None:
                    data['addr_sub_district'] = ''
                adrs = []
                if data['addr_road'] != '':
                    adrs.append(data['addr_road'])
                if data['addr_sub_district'] != '':
                    adrs.append(data['addr_sub_district'])
                if data['addr_district'] != '':
                    adrs.append(data['addr_district'])
                if data['addr_province'] != '':
                    adrs.append(data['addr_province'])

                print('5')
                elem = driver.find_element_by_name("home_address")
                elem.clear()
                adr = ''
                for i in range(len(adrs)):
                    if i!=len(adrs)-1:
                        adr+=adrs[i]
                        adr+=' , '
                    else:
                        adr+=adrs[i]

                elem.send_keys(adr,Keys.ARROW_DOWN)
                time.sleep(5)
                print('6')

                print('7')


                print('9')
                driver.find_element_by_css_selector("input[name='Submit'][value='   บันทึก    ']").click()


                print('done')
            except:
                res['success'] = 'false'
                res['detail'] = 'Something wrong happened'
                res['post_url'] = 'aaa'
                res['end_time'], res['usage_time'] = set_end_time(start_time)
                return res
        driver.close()
        driver.quit()
        res['end_time'], res['usage_time'] = set_end_time(start_time)
        return res


    def create_post(self, postdata):
        # self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time=datetime.datetime.utcnow()
        data = postdata
        res_login=self.test_login(postdata)
        if(res_login['success']=="false"):
            return res_login
        res={'websitename':'hometophit', 'success':"false", 'start_time': str(start_time), 'end_time': '0', 'usage_time': '0', 'detail': '', 'account_type':"null", "ds_id": postdata['ds_id']}
        create={}
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
        property_tp = {
            "1": "03",
            "2": "11",
            "3": "13",
            "4": "06",
            "5": "05",
            "6": "07",
            "7": "25",
            "8": "20",
            "9": "26",
            "10": "02",
            "25": "19"
        }
        #print('here')
        data['property_type'] = str(data['property_type'])
        if data['property_type'] not in property_tp:
            data['property_type'] = ids[data['property_type']]
        try:
            #print('here1')
            create['home_name'] = str(data['post_title_th'])
            #create['home_name']=(data['post_title_th'])
            #print('here2')
            create['home_type']=property_tp[data['property_type']]
            #print('here3')
            create['home_for']=2 if data['listing_type']=="ขาย" else 4
            #print('here4')
            create['home_timeshow']=4
            #print('here5')
            create['home_area']=data['land_size_wa']
            #print('here6')
            create['home_areatype']=2 if data['property_type']=="1" else 1
            #print('here7')
            create['home_floor']=data['floor_level']
            #print('here8')
            create['home_detail'] =str(data['post_description_th'])

            #create['home_detail'] = str(soup)

            if data['listing_type']=="ขาย":
                create['home_price']=data['price_baht']
            else:
                create['home_rent']=data['price_baht']
            if 'web_project_name' not in data or data['web_project_name'] is None or data['web_project_name'] == "":
                if 'project_name' in data and data['project_name'] is not None:
                    data['web_project_name'] = data['project_name']
                else:
                    data['web_project_name'] = data['post_title_th']

            create['home_project']=data['web_project_name']
            #print('here9')
            #print(data['addr_soi'],data['addr_road'],data['addr_sub_district'])
            if data['addr_soi'] == None:
                data['addr_soi'] = ''
            if data['addr_road'] == None:
                data['addr_road'] = ''
            if data['addr_sub_district'] == None:
                data['addr_sub_district'] = ''


            create['home_address']=data['addr_soi']+', '+data['addr_road']+', '+data['addr_sub_district']
            #print(create['home_address'])
            create['home_address'] = str(create['home_address'])
            #print(create['home_address'])
            #print('here10')
            #create['home_bedr'] = data['bed_room']
            #create['home_bathr'] = data['bath_room']
            create['mem_city']='1'
            create['mem_province']='10400'
            if 'post_images' in data and len(data['post_images']) > 0:
                pass
            else:
                data['post_images'] = ['./imgtmp/default/white.jpg']
            file = []
            temp = 1

            if len(data['post_images']) <= 4:
                for i in data['post_images']:
                    y = str(random.randint(0, 100000000000000000)) + ".jpg"
                    # print(y)
                    if temp!=1:
                        file.append((str('home_pic' + str(temp)), (y, open(i, "rb"), "image/jpg")))
                    else:
                        file.append((str('home_pic'), (y, open(i, "rb"), "image/jpg")))
                    temp = temp + 1

            else:
                for i in data['post_images'][:4]:
                    y = str(random.randint(0, 100000000000000000)) + ".jpg"
                    # print(y)
                    if temp!=1:
                        file.append((str('home_pic' + str(temp)), (y, open(i, "rb"), "image/jpg")))
                    else:
                        file.append((str('home_pic'), (y, open(i, "rb"), "image/jpg")))
                    temp = temp + 1
    #         print(create)
        except Exception as e:
            #print(e)
            res['detail']+='Error in json input2'
    #         print(create)
            res['end_time'],res['usage_time']=set_end_time(start_time)
            return res
        posturl='http://hometophit.com/hometh/submit_homepost.php'
        r = self.httprequestObj.http_post(posturl, data = create, files = file)
        
    #     print(r.cookies,r.history[0].cookies)
        #res['websitename']=r.url
        if r.encoding is None or r.encoding == 'ISO-8859-1':
            r.encoding = r.apparent_encoding
    #     print(r.text)
        webpage_text = r.text
        page_reg = r"home_view.*?&"
        id_reg = r"home_id.*?&"
        res['post_id']=re.search(id_reg, webpage_text, re.DOTALL).group()[8:-1]
        res['post_url']=''
        if(r.text==''):
            res['detail']+='Something went wrong. '
        else:
            res['success']="true"
            res['detail']+='Posted'
            data['post_id'] = res['post_id']
            ans = self.edit_post(data)
            res['post_url'] = ans['post_url']
        res['end_time'],res['usage_time']=set_end_time(start_time)
        return res

    def delete_post(self, postdata):
        # self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        data = postdata
        start_time=datetime.datetime.utcnow()
        res_login=self.test_login(postdata)
        if(res_login['success']=="false"):
            return res_login
        res={'websitename':'hometophit', 'success':"false", 'start_time': str(start_time), 'end_time': '0', 'usage_time': '0', 'detail': '', 'account_type':"null", "post_id": postdata['post_id']}
        delete={
            'home_id[]': data['post_id'],
            'Submit': 'Delete data'
        }
        posturl='http://hometophit.com/hometh/mem_panel.php'
        r=self.httprequestObj.http_get(posturl)
        listed_reg=r'\"home_view\.php\?home_id='+delete['home_id[]']+'\"'
        if re.search(listed_reg, r.text, re.DOTALL) is None:
            res['detail']='Post not found.'
            #res['websitename']=r.url
            res['end_time'],res['usage_time']=set_end_time(start_time)
            return res
        posturl='http://hometophit.com/hometh/delete_homepost.php'
        r = self.httprequestObj.http_post(posturl, data = delete)
    #     print(r.text, r.status_code, r.url)
        if(r.text==''):
            res['detail']+='Something went wrong. '
        else:
            res['success']="true"
            res['detail']+='Deleted'
        #res['websitename']=r.url
        res['end_time'],res['usage_time']=set_end_time(start_time)
        return res

    def search_post(self,postdata):
        start_time = datetime.datetime.utcnow()
        post_found=False
        post_id=""
        post_url=""
        options = Options()
        options.set_headless(True)
        options.add_argument('--no-sandbox')
        try:
            driver = webdriver.Chrome("./static/chromedriver",chrome_options=options)
            url = 'http://www.hometophit.com/hometh/login.php'
            driver.get(url)
            element = driver.find_element_by_name("mem_user")
            element.send_keys(postdata['user'].split("@")[0])
            element = driver.find_element_by_name("mem_pwd")
            element.send_keys(postdata["pass"])
            time.sleep(2)
            submit = driver.find_element_by_name("Submit")
            submit.click()
            time.sleep(2)
            try:
                if driver.current_url == "http://www.hometophit.com/hometh/mem_panel.php":
                    success = True
                else:
                    success = False
                    detail = "Username or Password Incorrect."
            except:
                success = False
                detail = "Username or Password Incorrect."

            if success == True:
                all_posts=driver.find_elements_by_css_selector("td:nth-child(3) a:nth-child(1)")
                for post in all_posts:
                    if post.get_attribute("title") in postdata['post_title_th'] or postdata['post_title_th'] in post.get_attribute("title"):
                        post_found=True
                        success=True
                        detail="Post Found."
                        post_url=post.get_attribute("href")
                        post_id=post_url.split("=")[1]
                        break
                else:
                    post_found = False
                    success = False
                    detail = "Post Not Found."
                    post_url = ""
                    post_id = ""

        except:
            success=False
            detail="Selenium Web browser Problem."
        finally:
            driver.close()
            driver.quit()
        end_time,usage_time=set_end_time(start_time)


        return {'websitename':'hometophit',
         'success':success,
         'post_found':post_found,
        'post_id':post_id,
        'post_url':post_url,
         'start_time': str(start_time),
         'end_time': end_time,
        'usage_time': usage_time,
         'detail': detail,
        'account_type':"null",
         "post_create_time": '',
         "post_modify_time": '',
         "post_view": ''}

    """
    def search_post(self, postdata):
        # self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time=datetime.datetime.utcnow()
        data = postdata
        res_login=self.test_login(postdata)
        if(res_login['success']=="false"):
            return res_login
        res={'websitename':'hometophit', 'success':"false", 'start_time': str(start_time), 'end_time': '0', 'usage_time': '0', 'detail': '', 'account_type':"null", "post_create_time": '', "post_modify_time": '', "post_view": ''}
        post_title = data['post_title_th']
        posturl='http://hometophit.com/hometh/mem_panel.php'
        r=self.httprequestObj.http_get(posturl)

        listed_reg=r'title="'+post_title+'\"'
        #print(r.text)
        #print('here1')
        if re.search(listed_reg, r.text, re.DOTALL) is None:
            res['detail']='Post not found.'
            res['post_found']="false"
            #res['websitename']=r.url
            res['end_time'],res['usage_time']=set_end_time(start_time)
            return res
        else:
            res['detail']='Post found.'
            res['post_found']="false"
            #res['websitename']=r.url
            res['success']="true"
            anchor_reg = r'<a href=\"home_view\.php\?home_id=[0-9]+\"  target=\"_blank\" title=\"'+post_title+'\"'
            try:
                temp=re.search(anchor_reg, r.text, re.DOTALL).group()
                #print(temp)
            except:
                res['detail']='Post not found.'
                res['post_found']="false"
                #res['websitename']=r.url
                res['end_time'],res['usage_time']=set_end_time(start_time)
                #print(temp)
                #print('here2')
                return res
            #print('here3')
            page_reg = r'home_view.*?\"'
            id_reg = r"home_id.*?\""
            res['post_id']=re.search(id_reg, temp, re.DOTALL).group()[8:-1]
            res['post_url']="http://hometophit.com/hometh/"+re.search(page_reg, temp, re.DOTALL).group()[:-1]
            res['end_time'],res['usage_time']=set_end_time(start_time)
            #print('here4')
            if 'post_url' not in res or res['post_url'] == "":
                res['post_url'] = ''
                res['post_id'] = ''
                res['post_found'] = "false"
                res['detail'] = 'Post not found'
            return res
    """
    def boost_post(self, postdata):
        # self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time=datetime.datetime.utcnow()
        post_id = postdata['post_id']
        data = postdata
        res_login=self.test_login(postdata)
        if(res_login['success']=="false"):
            return res_login
        res={'websitename':'hometophit', 'success':"false", 'start_time': str(start_time), 'end_time': '0', 'usage_time': '0', 'detail': '', 'account_type':"null", "post_id": postdata['post_id']}
        posturl='http://hometophit.com/hometh/mem_panel.php'
        r=self.httprequestObj.http_get(posturl)
        listed_reg=r'\"home_view\.php\?home_id='+post_id+'\"'
        if re.search(listed_reg, r.text, re.DOTALL) is None:
            res['detail']='Post not found.'
            res['websitename']='hometophit'
            res['end_time'],res['usage_time']=set_end_time(start_time)
            return res
        r=self.httprequestObj.http_get("http://hometophit.com/hometh/update_home_uptime.php?home_id="+post_id)
        if(r.text==''):
            res['detail']+='Something went wrong. '
        else:
            print('Here')
            res['success']="true"
            res['detail']+='Post edited and saved'
            res['post_id'] = postdata['post_id']
        #res['websitename']=r.url
        res['post_id'] = postdata['post_id']
        res['end_time'],res['usage_time']=set_end_time(start_time)
        return res


    