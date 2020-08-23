# -*- coding: utf-8 -*-

# from .lib_httprequest import *
from .lib_httprequest import *

from bs4 import BeautifulSoup
import os.path
# from urlparse import urlparse
import re
import sys
import json
# import datetime
import time 
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
# httprequestObj = lib_httprequest()
# httprequestObj = lib_httprequest()
httprequestObj = lib_httprequest()



# sess = requests.session()

class pantipmarket():

    name = 'pantipmarket'

    def __init__(self):

        try:
            import configs
        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.primarydomain = 'https://www.pantipmarket.com/'
        self.debug = 0
        self.debugresdata = 0


    def register_user(self, userdata):
        # print('hello')
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.utcnow()

        httprequestObj.http_get('https://www.pantipmarket.com/member/logout.php')

        for x in ['user','pass','name_th','surname_th','tel','company_name']:
            # print(x)
            if x not in userdata:
                time_end = datetime.utcnow()
                return {
                    "websitename":"pantipmarket",
                    "success": "false",
                    "time_usage": time_end - time_start,
                    "start_time": time_start,
                    "end_time": time_end,
                    "detail": "Field {} not provided." .format(x) 
                }


        datapost = {
            'username': userdata['user'],
            'password': userdata['pass'],
            'confirm_password': userdata['pass'],
            'name': userdata['name_th'],
            'sname': userdata['surname_th'],
            'email': userdata['user'],
            'phone': userdata['tel'],
            'display_name': userdata['company_name'],
            'except_privacy_policy' : '1',
            'btn_register_submit': 'Submit',
            'act': 'register',
            'new': '1',
            'member_social_id': '',
            'member_social_type': '',
            'access_token': '',
            'username_code': '0',
            'display_name_code': '0',
            'customerID': '',
            'do_order': 'no',
            'orderid': '',
            'step': ''
        }

        # headers = {
        #     'authority': 'www.pantipmarket.com',
        #     'cache-control': 'max-age=0',
        #     'origin': 'https://www.pantipmarket.com',
        #     'upgrade-insecure-requests': '1',
        #     'dnt': '1',
        #     'content-type': 'application/x-www-form-urlencoded',
        #     'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        #     'sec-fetch-dest': 'document',
        #     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        #     'sec-fetch-site': 'same-origin',
        #     'sec-fetch-mode': 'navigate',
        #     'sec-fetch-user': '?1',
        #     'referer': 'https://www.pantipmarket.com/member/register_2012.php?new=1',
        #     'accept-language': 'en-IN,en-US;q=0.9,en-GB;q=0.8,en;q=0.7',
        #     'cookie': '_ga=GA1.2.151159769.1589130796; _gid=GA1.2.1042363384.1589130796; pmk_ipage_id[528170]=0; pmk_ipage_id[528171]=0; pmk_ipage_id[528169]=0; pmk_ipage_id[528213]=0; SS_PANTIPMARKET_COM=g0b28h60ah1hkfj9fs04nf7np3; pmk_user_screen=1920|1080',
        # }
        success = True
        r = httprequestObj.http_post('https://www.pantipmarket.com/member/register_2012.php',data=datapost)
        print(r.text)        
        registered = "คุณเป็นสมาชิก" in r.content.decode('utf-8')
        if registered == False:
            success = False
        time_end = datetime.utcnow()

        return {
            "websitename":"pantipmarket",
            "success": success,
            "time_usage": time_end - time_start,
            'ds_id': userdata['ds_id'],
            "start_time": time_start,
            "end_time": time_end,
            "detail": "Registered Successfully " if registered else "Registration Failed. Either email is already registered or company name has 2 letters occurring consecutively which is not allowed by this site. "
        }

    def test_login(self, logindata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.utcnow()
        httprequestObj.http_get('https://www.pantipmarket.com/member/logout.php')
        success = True
        headers = {
            'authority': 'www.pantipmarket.com',
            'cache-control': 'max-age=0',
            'origin': 'https://www.pantipmarket.com',
            'upgrade-insecure-requests': '1',
            'dnt': '1',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'sec-fetch-dest': 'document',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'referer': 'https://www.pantipmarket.com/member/login.php?step=&sCode=',
            'accept-language': 'en-IN,en-US;q=0.9,en-GB;q=0.8,en;q=0.7',
            'cookie': '_ga=GA1.2.151159769.1589130796; _gid=GA1.2.1042363384.1589130796; pmk_ipage_id[528170]=0; pmk_ipage_id[528171]=0; pmk_ipage_id[528169]=0; pmk_ipage_id[528213]=0; SS_PANTIPMARKET_COM=g0b28h60ah1hkfj9fs04nf7np3; pmk_user_screen=1920|1080; pmk_ipage_id[528239]=0; _gat=1',
        }

        datapost = {
            'username': logindata['user'],
            'password': logindata['pass'],
            'btn_login_submit': ' Login ',
            'act': 'login',
            'url': 'https://www.pantipmarket.com/member/my/',
            'pop': ''
        }
        r = httprequestObj.http_post('https://www.pantipmarket.com/member/login.php?step=&sCode=', headers=headers, data=datapost)

        time_end = datetime.utcnow()
        logged_in = '4264545' in r.text
        if logged_in == False:
            success = False

        return {
            "websitename":"pantipmarket",
            "success": success,
            "ds_id": logindata['ds_id'],
            "time_usage": time_end - time_start,
            "start_time": time_start,
            "end_time": time_end,
            "detail": "Log in Successfully " if logged_in else "Log in Failed"
        }

    def create_post(self, postdata):
        
        # print(json.dumps(postdata, indent=4, sort_keys=True,default=str)) 
        start_time = datetime.utcnow()

        listing_type = postdata['listing_type']
        property_type = postdata['property_type']
        post_img_url_lists = postdata['post_img_url_lists']
        price_baht = postdata['price_baht']
        addr_province = postdata['addr_province']
        addr_district = postdata['addr_district']
        addr_sub_district = postdata['addr_sub_district']
        addr_road = postdata['addr_road']
        addr_near_by = postdata['addr_near_by']
        floorarea_sqm = postdata['floor_area']
        geo_latitude = postdata['geo_latitude']
        geo_longitude = postdata['geo_longitude']
        property_id = postdata['property_id']
        post_title_th = postdata['post_title_th']
        post_description_th = postdata['post_description_th']
        name = postdata['name']
        mobile = postdata['mobile']
        email = postdata['email']
        line = postdata['line']
        ds_id = postdata["ds_id"]
        user = postdata["user"]
        password = postdata["pass"]

        if user == "" or password == "":

            return {
                "websitename":"pantipmarket",
                "success": "false",
                "post_url": "",
                "start_time": start_time,
                "end_time" : datetime.utcnow(),
                "time_usage": datetime.utcnow() - start_time,
                "ds_id": postdata['ds_id'],
                "post_id": "",
                "account_type": "null",
                "detail": "User/Pass Missing"
            }
        # project_name = postdata["project_name"]

        select_group = ""
        old_group = "6_37"
        group = ""
        post_url = ""
        post_id = ""


        send_property = '//*[@id="lv"]/li['

        if postdata['property_type'] == "1": #condo
            select_group = "อสังหาริมทรัพย์ » คอนโด ห้องพัก"
            send_property += '6]'
            group = "6_122"

        elif postdata['property_type'] == "2": #single house
            select_group = "อสังหาริมทรัพย์ » บ้านเดี่ยว"
            send_property += '1]'
            group = "6_37"
        
        elif postdata['property_type'] == "3": #twin house
            select_group = "อสังหาริมทรัพย์ » บ้านแฝด"
            send_property += '2]'

            group = "6_865"
        
        elif postdata['property_type'] == "4": #townhouse
            select_group = "อสังหาริมทรัพย์ » ทาวน์เฮ้าส์"
            send_property +='4]'

            group = "6_64"
        
        elif postdata['property_type'] == "5": #comm building
            select_group = "อสังหาริมทรัพย์ » อาคารพาณิชย์"
            send_property += '5]'

            group = "6_93"
        
        elif postdata['property_type'] == "6": #land
            select_group = "อสังหาริมทรัพย์ » ที่ดิน"
            send_property += '7]'

            group = "6_168"

        elif postdata['property_type'] == "7":  #apartment
            select_group = "อสังหาริมทรัพย์ » อพาร์ทเม้นท์/ หอพัก ทั้งหลัง"
            send_property += '9]'

            group = "6_148"
        
        elif postdata['property_type'] == "8":  #hotels
            select_group = "อสังหาริมทรัพย์ » รีสอร์ท โรงแรม ทั้งกิจการ"
            send_property += '10]'

            group = "6_212"

        elif postdata['property_type'] == "9":  #office
            select_group = "อสังหาริมทรัพย์ » พื้นที่สำนักงาน"
            send_property += '8]'

            group = "6_199"

        elif postdata['property_type'] == "10": #warehouse/factory
            select_group = "อสังหาริมทรัพย์ » โกดัง/ โรงงาน"
            send_property += '12]'

            group = "6_1096"

        elif postdata['property_type'] == "25": #warehouse/factory
            select_group = "อสังหาริมทรัพย์ » โกดัง/ โรงงาน"
            send_property += '12]'

            group = "6_1096"

        options = Options()
        options.headless = True
        options.add_argument('--no-sandbox')

        driver = webdriver.Chrome("./static/chromedriver", chrome_options=options)

        driver.implicitly_wait(4)


        # driver = webdriver.Chrome()
        driver.get("https://www.pantipmarket.com/member/login.php?step=&sCode=")

        driver.find_element_by_xpath('//*[@id="login_box2"]/div[1]/a').click()
        driver.find_element_by_name("username").send_keys(postdata['user'])
        driver.find_element_by_name("password").send_keys(postdata['pass'])
        driver.find_element_by_name("btn_login_submit").click()

        success = True
        end_time = datetime.utcnow()
        # if 'web_project_name' not in postdata or postdata['web_project_name']!=None:
        #     if 'project_name' in postdata and postdata['project_name']!=None:
        #         postdata['web_project_name'] = postdata['project_name']
        #     else:
        #         postdata['web_project_name'] = postdata['post_title_th']

        driver.get("https://www.pantipmarket.com/post/")

        detail = ""
        
        # post_title_th += " -ทรัพย์สินไทย"
        driver.find_element_by_name("topic_th").send_keys(post_title_th)
        time.sleep(4)
        try:
            if driver.page_source.find('หัวข้อประกาศนี้ ต้องไม่ซ้ำกับหัวข้อประกาศอื่นๆ') == None:
                driver.find_element_by_xpath('//*[@id="select_group"]').click()
                driver.find_element_by_xpath('//*[@id="lv"]/li[6]').click()
                driver.find_element_by_xpath(send_property).click()

        except ElementNotInteractableException:
            detail = "A post with the same title already exists"
            success = False
        
        if success == True:    
            try:
                element = WebDriverWait(driver,5).until(
                    EC.presence_of_element_located((By.NAME,"jqi_state0_buttonOk"))
                )
                driver.find_element_by_name('jqi_state0_buttonOk').click()
                print("Page is ready")
            except:
                print('Loading took too much time!')

            new_title = post_title_th.replace(" ","%20")

            url = "https://www.pantipmarket.com/post/?lang=th&group=" + str(group) + "&topic=" + new_title

            driver.get(url)
            time.sleep(3)
            
            driver.find_element_by_name("message_th").send_keys(post_description_th)

            # time.sleep(10)
            driver.find_element_by_xpath('//*[@id="action_type"]/option[2]').click()

            if postdata['listing_type'] == 'ขาย':
                driver.find_element_by_xpath('//*[@id="action_list_S1"]').click()

            else:
                driver.find_element_by_xpath('//*[@id="action_list_S2"]').click()
            
            for i in range(len(postdata['post_images'])):
                if i < 15:
                    filepath = os.getcwd() + "/"+ postdata['post_images'][i]
                    driver.find_element_by_xpath('//*[@id="PMKuploadfile-btn"]').send_keys(filepath)
                else:
                    break


            driver.find_element_by_name("price_text_th").send_keys(price_baht)

            provinces = {}

            select_box = driver.find_element_by_id('located_in_select_2')
            options = [x for x in select_box.find_elements_by_tag_name("option")]
            for i in options[1:]:
                provinces[i.get_attribute("value")] = i.text


            for key,value in provinces.items():
                if addr_province.find(value) != -1 or value.find(addr_province) != -1:
                    addr_province = key
                    break


            element = driver.find_element_by_id('located_in_select_2')
            dropdown = Select(element)
            dropdown.select_by_value(addr_province)


            time.sleep(10)
            districts = {}
            district_located = ""
            try:
                select_box = driver.find_element_by_id('located_in_select_3')
                district_located = 'located_in_select_3'
            except:
                select_box = driver.find_element_by_id('located_in_select_4')
                district_located = 'located_in_select_4'

            options = [x for x in select_box.find_elements_by_tag_name("option")]
            for i in options[1:]:
                districts[i.get_attribute("value")] = i.text
            
            for key,value in districts.items():
                # print(key)
                if addr_district.find(value) != -1 or value.find(addr_district) != -1:
                    addr_district = key
                    break

            element = driver.find_element_by_id(district_located)
            dropdown = Select(element)
            dropdown.select_by_value(addr_district)


            driver.find_element_by_name('name_th').clear()
            if name!= None:
                driver.find_element_by_name("name_th").send_keys(name)
            driver.find_element_by_name('contact[telephone]').clear()
            if mobile != None:
                driver.find_element_by_name("contact[telephone]").send_keys(mobile)
            driver.find_element_by_name('contact[email]').clear()
            if email != None:
                driver.find_element_by_name("contact[email]").send_keys(email)
            driver.find_element_by_name('contact[line]').clear()
            if line != None and len(line) >=4:
                driver.find_element_by_name("contact[line]").send_keys(line)

            # new_post_description = ""
            # for i in post_description_th:
            #     if(len(new_post_description)<385):
            #         new_post_description+=i


            # print(new_post_description)
            # driver.find_element_by_name("message_th").send_keys(new_post_description)
            # driver.find_element_by_name("message_th").send_keys(post_description_th)

            html = driver.find_element_by_tag_name('html')
            html.send_keys(Keys.END)
            time.sleep(2)
            slider = driver.find_element_by_xpath('//*[@id="data_post"]/div[5]/fieldset/div/div/div[2]/div/div/div[1]/div')
            move = ActionChains(driver)
            move.click_and_hold(slider).move_by_offset(379.005, 0).release().perform()
            try:
                element = WebDriverWait(driver,10).until(
                    EC.presence_of_element_located((By.NAME,"jqi_state0_buttonOk"))
                )
                driver.find_element_by_name('jqi_state0_buttonOk').click()
            except:
                print('loading took too much time!')

            success = True
            detail = 'Created the post successfully'
            end_time = datetime.utcnow()

            time.sleep(4)
            test_login = self.test_login(postdata)

            success2 = test_login["success"]
            if success2 == True:

                next_url = 'https://www.pantipmarket.com/member/my/?view=ads&adsmode=ads&p='
                page = 1
                found = 1
                idn = []
                while found > 0:
                    request = httprequestObj.http_get(next_url + str(page))

                    regex = 'id=\"tr[0-9]+\"'
                    found = re.findall(regex,str(request.text))

                    page += 1

                    if len(found) > 0:
                        idn = found.copy()
                    else:
                        break

                try:
                    idnn = idn[len(idn)-1]
                    post_id = idnn[6:len(idnn)-1]
                    print(post_id)

                    post_url = 'https://www.pantipmarket.com/items/' + post_id
                except:
                    detail = "couldn't create post"
                    post_id = ""
                    post_url = ""
                # print(post_url)
        else:
            end_time = datetime.utcnow()

        try:
            driver.quit()
        except:
            pass

        return {
            "websitename":"pantipmarket",
            "success": success,
            "post_url": post_url,
            "start_time":start_time,
            "end_time" : end_time,
            "time_usage": end_time - start_time,
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
            "account_type": "null",
            "detail": detail
        }



    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        post_id = postdata["post_id"]

        test_login = self.test_login(postdata)

        success = test_login["success"]
        start_time = datetime.utcnow()
        end_time = datetime.utcnow()
        post_url = ""

        if success == True:
            post_url = "https://www.pantipmarket.com/items/" + post_id


            request = httprequestObj.http_get("https://www.pantipmarket.com/form.php?mode=board_delete&id=" + post_id + "&v12.0")
            response_result = str(request.text)
            regex = '<div class="blue_box">ไม่พบข้อมูลของประกาศ</div>'
            result = re.findall(regex,response_result)
            if(len(result)>=1):
                success = False
                detail = "The post doesn't exist"
                post_url = ""
                post_id = ""

            # print(success)
            if success == True:
                url = "https://www.pantipmarket.com/member/my/"
                request = httprequestObj.http_get(url)
                soup = BeautifulSoup(request.text,'lxml')
                date = soup.find('input',attrs = {'id': 'date'+post_id, 'name' : 'date'})['value']
                datapost = {
                'board_shift[]' : post_id,
                'board_delete_chk' : '',
                'board_shift_check' : '',
                'package_shift_chk' : '',
                'act' : 'board_shift',
                'allow_delete' : '1',
                'allow_shift' : '1',
                'allow_package' : '1',
                'url' : 'https://www.pantipmarket.com/member/my/?view=ads',
                'ipid' : '1',
                'date' : date
                }
                # f = open("pantip.txt","w+")
                # f.write(str(request.text))
                # f.close()
                
                newurl = 'https://www.pantipmarket.com/member/my/action.php'

                request = httprequestObj.http_post(newurl, data=datapost)
                end_time = datetime.utcnow()
                detail = "Successful boost"
        else:
            success = False
            end_time = datetime.utcnow()
            detail = "Unsuccessful login"


        return {
            "websitename":"pantipmarket",
            "success": success,
            "time_usage": end_time - start_time,
            "start_time": start_time,
            "end_time": end_time,
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "detail": detail,
            "post_id": post_id,
            "post_url" : post_url
        }


    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        # time_start = datetime.datetime.utcnow()

        # log_id = postdata['post_id']
        # email_user = postdata['email_user']
        # email_pass = postdata['email_pass']
        post_id = postdata["post_id"]
        # print(post_id)
        test_login = self.test_login(postdata)
        print("lol")
        start_time = datetime.utcnow()
        end_time = datetime.utcnow()

        success = test_login["success"]
        # print(success)
        post_url = ""
        # post_id = ""

        if success == True:
            # print(json.dumps(postdata, indent=4, sort_keys=True,default=str))
            post_url = "https://www.pantipmarket.com/items/" + post_id
            # print(post_id)
            # print(post_url)

            url = 'https://www.pantipmarket.com/member/my/action.php'

            datapost = {
                'board_delete[]' : post_id,
                'act' : 'board_delete',
                'url' : 'https://www.pantipmarket.com/member/my/?view=ads&adsmode=delads'
            }

            request = httprequestObj.http_get("https://www.pantipmarket.com/form.php?mode=board_delete&id=" + post_id + "&v12.0")
            response_result = str(request.text)


            regex = '<div class="blue_box">ไม่พบข้อมูลของประกาศ</div>'
            result = re.findall(regex,response_result)
            if(len(result)>=1):
                success = False
                detail = "The post doesn't exist"
                post_url = ""
                post_id = ""

            # time_start = datetime.datetime.utcnow()            

            # print(success)
            if success == True:
                request = httprequestObj.http_post(url, data=datapost)
                end_time = datetime.utcnow()
                detail = "Successfully deleted the post"
                # post_url = ""
                # time_end = datetime.datetime.utcnow()

                # print(post_url)
        
        else:
            success = False
            end_time = datetime.utcnow()
            detail = "Unsuccessful login"
        return {
            "websitename":"pantipmarket",
            "success": success,
            "time_usage": end_time - start_time,
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "start_time": start_time,
            "end_time": end_time,
            "detail": detail,
            "post_id": post_id,
            "post_url" : post_url
        }

    def edit_post(self, postdata):
        listing_type = postdata['listing_type']
        property_type = postdata['property_type']
        post_img_url_lists = postdata['post_img_url_lists']
        price_baht = postdata['price_baht']
        addr_province = postdata['addr_province']
        addr_district = postdata['addr_district']
        addr_sub_district = postdata['addr_sub_district']
        addr_road = postdata['addr_road']
        addr_near_by = postdata['addr_near_by']
        floorarea_sqm = postdata['floor_area']
        geo_latitude = postdata['geo_latitude']
        geo_longitude = postdata['geo_longitude']
        property_id = postdata['property_id']
        post_title_th = postdata['post_title_th']
        post_description_th = postdata['post_description_th']
        name = postdata['name']
        mobile = postdata['mobile']
        email = postdata['email']
        line = postdata['line']
        ds_id = postdata["ds_id"]
        user = postdata["user"]
        password = postdata["pass"]
        project_name = postdata["project_name"]
        post_id = postdata['post_id']


        post_url = ""

        # if 'web_project_name' not in postdata or postdata['web_project_name']!=None:
        #     if 'project_name' in postdata and postdata['project_name']!=None:
        #         postdata['web_project_name'] = postdata['project_name']
        #     else:
        #         postdata['web_project_name'] = postdata['post_title_th']

        select_group = ""
        old_group = "6_37"
        group = ""

        send_property = '//*[@id="lv"]/li['

        if postdata['property_type'] == "1": #condo
            select_group = "อสังหาริมทรัพย์ » คอนโด ห้องพัก"
            send_property += '6]'
            group = "6_122"

        elif postdata['property_type'] == "2": #single house
            select_group = "อสังหาริมทรัพย์ » บ้านเดี่ยว"
            send_property += '1]'
            group = "6_37"
        
        elif postdata['property_type'] == "3": #twin house
            select_group = "อสังหาริมทรัพย์ » บ้านแฝด"
            send_property += '2]'

            group = "6_865"
        
        elif postdata['property_type'] == "4": #townhouse
            select_group = "อสังหาริมทรัพย์ » ทาวน์เฮ้าส์"
            send_property +='4]'

            group = "6_64"
        
        elif postdata['property_type'] == "5": #comm building
            select_group = "อสังหาริมทรัพย์ » อาคารพาณิชย์"
            send_property += '5]'

            group = "6_93"
        
        elif postdata['property_type'] == "6": #land
            select_group = "อสังหาริมทรัพย์ » ที่ดิน"
            send_property += '7]'

            group = "6_168"

        elif postdata['property_type'] == "7":  #apartment
            select_group = "อสังหาริมทรัพย์ » อพาร์ทเม้นท์/ หอพัก ทั้งหลัง"
            send_property += '9]'

            group = "6_148"
        
        elif postdata['property_type'] == "8":  #hotels
            select_group = "อสังหาริมทรัพย์ » รีสอร์ท โรงแรม ทั้งกิจการ"
            send_property += '10]'

            group = "6_212"

        elif postdata['property_type'] == "9":  #office
            select_group = "อสังหาริมทรัพย์ » พื้นที่สำนักงาน"
            send_property += '8]'

            group = "6_199"

        elif postdata['property_type'] == "10": #warehouse/factory
            select_group = "อสังหาริมทรัพย์ » โกดัง/ โรงงาน"
            send_property += '12]'

            group = "6_1096"

        elif postdata['property_type'] == "25": #warehouse/factory
            select_group = "อสังหาริมทรัพย์ » โกดัง/ โรงงาน"
            send_property += '12]'

            group = "6_1096"
    
        success = True
        start_time = datetime.utcnow()
        end_time = datetime.utcnow()
        options = Options()
        options.headless = True
        options.add_argument('--no-sandbox')
        
        driver = webdriver.Chrome("./static/chromedriver", chrome_options=options)
        
        driver.implicitly_wait(4)
        driver.get("https://www.pantipmarket.com/member/login.php?step=&sCode=")
        driver.find_element_by_xpath('//*[@id="login_box2"]/div[1]/a').click()
        driver.find_element_by_name("username").send_keys(postdata['user'])
        driver.find_element_by_name("password").send_keys(postdata['pass'])
        driver.find_element_by_name("btn_login_submit").click()
        request = httprequestObj.http_get("https://www.pantipmarket.com/form.php?mode=board_delete&id=" + post_id + "&v12.0")
        response_result = str(request.text)
        
        regex = '<div class="blue_box">ไม่พบข้อมูลของประกาศ</div>'
        result = re.findall(regex,response_result)


        if(len(result)>=1):
            success = False
            detail = "The post doesn't exist"
            end_time = datetime.utcnow()
        else:
            success = True

        if success == True:

            driver.get("https://www.pantipmarket.com/post/edit.php?board_id=" + post_id)

            if post_title_th != None:
                driver.find_element_by_name('topic_th').clear()
            print(post_title_th)
            driver.find_element_by_name("topic_th").send_keys(post_title_th)

            if post_description_th != None:
                driver.find_element_by_name('message_th').clear()        
                driver.find_element_by_name("message_th").send_keys(post_description_th)

            driver.find_element_by_xpath('//*[@id="action_type"]/option[2]').click()

            if postdata['listing_type'] != None:
                if postdata['listing_type'] == 'ขาย':
                    driver.find_element_by_xpath('//*[@id="action_list_S1"]').click()

                else:
                    driver.find_element_by_xpath('//*[@id="action_list_S2"]').click()

            if postdata['post_images'] != None:
                driver.find_element_by_xpath('//*[@id="PMKuploadfile-btn"]').clear()
                for i in range(len(postdata['post_images'])):
                    if i < 15:
                        filepath = os.getcwd() + "/"+ postdata['post_images'][i]
                        driver.find_element_by_xpath('//*[@id="PMKuploadfile-btn"]').send_keys(filepath)
                    else:
                        break

            if price_baht != None:
                driver.find_element_by_name('price_text_th').clear()
                driver.find_element_by_name("price_text_th").send_keys(price_baht)


            if addr_province != None:
                provinces = {}

                select_box = driver.find_element_by_id('located_in_select_2')
                options = [x for x in select_box.find_elements_by_tag_name("option")]
                for i in options[1:]:
                    provinces[i.get_attribute("value")] = i.text


                for key,value in provinces.items():
                    if addr_province.find(value) != -1:
                        addr_province = key
                        break


                element = driver.find_element_by_id('located_in_select_2')
                dropdown = Select(element)
                dropdown.select_by_value(addr_province)


            time.sleep(10)
            if addr_district != None:
                districts = {}
                district_located = ""
                try:
                    select_box = driver.find_element_by_id('located_in_select_3')
                    district_located = 'located_in_select_3'
                except:
                    select_box = driver.find_element_by_id('located_in_select_4')
                    district_located = 'located_in_select_4'

                options = [x for x in select_box.find_elements_by_tag_name("option")]
                for i in options[1:]:
                    districts[i.get_attribute("value")] = i.text
                
                for key,value in districts.items():
                    # print(key)
                    if addr_district.find(value) != -1:
                        addr_district = key
                        break

                element = driver.find_element_by_id(district_located)
                dropdown = Select(element)
                dropdown.select_by_value(addr_district)

            
            if name != None:
                driver.find_element_by_name('name_th').clear()
                driver.find_element_by_name("name_th").send_keys(name)
            if mobile != None:
                driver.find_element_by_name('contact[telephone]').clear()
                driver.find_element_by_name("contact[telephone]").send_keys(mobile)
            if email != None:
                driver.find_element_by_name('contact[email]').clear()
                driver.find_element_by_name("contact[email]").send_keys(email)
            if line !=None and len(line)>=4:
                driver.find_element_by_name('contact[line]').clear()
                driver.find_element_by_name("contact[line]").send_keys(line)




            html = driver.find_element_by_tag_name('html')
            html.send_keys(Keys.END)
            time.sleep(2)

            slider = driver.find_element_by_xpath('//*[@id="data_post"]/div[5]/fieldset/div/div/div[2]/div/div/div[1]/div')
            move = ActionChains(driver)
            move.click_and_hold(slider).move_by_offset(379.005, 0).release().perform()
            try:
                element = WebDriverWait(driver,20).until(
                    EC.presence_of_element_located((By.NAME,"jqi_state0_buttonOk"))
                )
                driver.find_element_by_name('jqi_state0_buttonOk').click()
            except:
                print('loading took too much time!')


            post_url = "https://www.pantipmarket.com/items/" + post_id
            detail = "Successfully edited the post"
            success = True
            end_time = datetime.utcnow()

        try:
            driver.quit()
        except:
            pass

        return {
            "websitename":"pantipmarket",
            "success": success,
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "time_usage": end_time - start_time,
            "start_time": start_time,
            "end_time": end_time,
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
        }
        

    def search_post(self, postdata):

        time_start = datetime.utcnow()
        search_title = postdata['post_title_th']
        resp = self.test_login(postdata)
        detail = resp['detail']

        success = False
        post_url = ''
        post_id = ''

        if resp['success'] is True:

            resp = httprequestObj.http_get("https://www.pantipmarket.com/member/my/?view=ads")
            with open ("temp-5", "w") as f:
                f.write(resp.text)

            soup = BeautifulSoup(resp.text, 'html.parser')
            posts = soup.findAll("div", {"class": "topic_box"})
            titles = []

            for i in posts:
                try:
                    titles += [[i.find(text=True).strip(), i.find('a')["href"].strip()]]
                except:
                    pass
            print(titles)
            detail = 'Not found'

            for title in titles:
                if title[0] == search_title:
                    success = True
                    detail = "Post found"
                    post_url = title[1]
                    post_id = ''.join(filter(str.isdigit,title[1]))

        time_end = datetime.utcnow()
        time_usage = time_end - time_start

        ret = {
                "websitename": "pantipmarket",
                "success": "true",
                "ds_id": postdata['ds_id'],
                "log_id": postdata['log_id'],
                "post_found": success,
                "post_url": post_url,
                "post_id": post_id, 
                "post_create_time": '',
                "post_modify_time": '',
                "post_view": '',
                "account_type": "null",
                "detail": detail,
                "start_time": str(time_start),
                "end_time": str(time_end),
                "time_usage": str(time_usage),
                }

        return ret

    def print_debug(self, msg):
        if(self.debug == 1):
            print(msg)
        return True

    def print_debug_data(self, data):
        if(self.debugdata == 1):
            print(data)
        return True
