# -*- coding: utf-8 -*-

from .lib_httprequest import *
from .lib_captcha import *
from bs4 import BeautifulSoup
import os.path
from shutil import copyfile
# from urlparse import urlparse
import re
import json
import datetime
import sys
from urllib.parse import unquote
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import random
import selenium.webdriver.support.ui as ui
import time
httprequestObj = lib_httprequest()
Captcha = lib_captcha()


class thaihomeonline():

    name = 'thaihomeonline'

    def __init__(self):

        try:
            import configs
        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.primarydomain = 'http://www.thaihomeonline.com/'
        self.debug = 0
        self.debugresdata = 0
        self.parser = 'html.parser'
        self.max_image = 6

    def logout_user(self):
        url = 'https://www.thaihomeonline.com/logout/'
        httprequestObj.http_get(url)

    def register_user(self, userdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        # print("here in register")

        email = userdata['user']
        passwd = userdata['pass']
        full_name_th = userdata['name_th'] + " "+ userdata['surname_th']
        mobile = userdata['tel']

        options = Options()
        options.headless = True
        options.add_argument('--no-sandbox')

        driver = webdriver.Chrome("./static/chromedriver",options=options)
        driver.implicitly_wait(10)

        driver.get("https://www.thaihomeonline.com/register/")

        val = re.findall(r'https://www.thaihomeonline.com/files/captcha/[\w.]+',driver.page_source)
        # httpobj2 = lib_httprequest()
        print(val[0])

        response = requests.get(val[0],stream=True)
        # os.system('mkdir '+os.getcwd() + '/imgtmp/Img_Captcha')
        if response.status_code == 200:
            imgname = "/imgtmp/" + str(random.randint(1, 999999999)) + '.png'
            with open(os.getcwd()+imgname, 'wb') as f:
                f.write(response.content)
        else:
            print(response)

        img_text = Captcha.imageCaptcha(os.getcwd() + imgname)

        print(img_text[1])

        try:
            driver.find_element_by_name('regisEmail1').send_keys(email)
            driver.find_element_by_name('regisEmail2').send_keys(email)
            driver.find_element_by_name('regisPass1').send_keys(passwd)
            driver.find_element_by_name('regisPass2').send_keys(passwd)
            driver.find_element_by_name('regisFullnameTH').send_keys(full_name_th)
            driver.find_element_by_name('regisMobile').send_keys(mobile)
            driver.find_element_by_name('regisCaptcha').send_keys(img_text[1])
            driver.find_element_by_name('agreeChk').click()
            time.sleep(1)
            driver.find_element_by_name('btnSubmit').click()
        except:
            driver.close()
            driver.quit()
            time_end = datetime.datetime.utcnow()
            time_usage = time_end - time_start
            return {
                "websitename": "thaihomeonline",
                "success": "false",
                "start_time": str(time_start),
                "end_time": str(time_end),
                'ds_id': userdata['ds_id'],
                "detail": "Selenium Issue",
            }


        if(re.search('การสมัครสมาชิกของท่านเสร็จสมบูรณ์',driver.page_source)):
            driver.close()
            driver.quit()
            success = "True"
            detail = "Registered"
        else:
            driver.close()
            driver.quit()
            success = "False"
            detail = 'not registered'

        if os.path.exists(os.getcwd()+imgname):
            os.remove(os.getcwd()+imgname)     

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "thaihomeonline",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            'ds_id': userdata['ds_id'],
            "detail": detail,
        }

    def test_login(self, logindata):
        self.logout_user()
        # print("Here in test_login")
        r = httprequestObj.http_get('https://www.thaihomeonline.com/logout/')
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        email_user = logindata['user']
        email_pass = logindata['pass']            
        
        datapost = {
            'username' : email_user,
            'password' : email_pass,
            'hidMode':'login'
        }
        # print(datapost)
        r = httprequestObj.http_post('https://www.thaihomeonline.com/login/', data=datapost)
        data = r.text
        # print(data)
        # print("Data Printed")
        matchObj = re.search(r'logout/', data)
        # print(matchObj)
        if matchObj:
            success = "True"
            detail = "Sucessful Login"
        else:
            success = "False"
            detail = "Login Unsucessful"
        
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        
        return {
            "websitename": "thaihomeonline",
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            "usage_time": str(time_usage),
            "ds_id": logindata['ds_id'],
            "detail": detail,
        }
        #
        #
        #
    
    def create_post(self, postdata):
        # https://www.thaihomeonline.com/post/get_json_district?province_id=13   ->     for district
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        # print(postdata)
        # postdata = postdata
        # print(self.max_image)
        listing_type = postdata['listing_type']
        property_type = postdata['property_type']
        post_img_url_lists = postdata['post_img_url_lists']
        price_baht = postdata['price_baht']
        addr_province = postdata['addr_province']
        addr_district = postdata['addr_district']
        addr_sub_district = postdata['addr_sub_district']
        addr_road, addr_near_by, floorarea_sqm = ['','','']
        addr_number = '1'
        if 'addr_road' in postdata:
            addr_road = postdata['addr_road']
        if 'addr_near_by' in postdata:
            addr_near_by = postdata['addr_near_by']
        if 'floorarea_sqm' in postdata:
            floorarea_sqm = postdata['floorarea_sqm']
        if 'addr_number' in postdata:
            addr_number = postdata['addr_number']
            
            
        
        geo_latitude = postdata['geo_latitude']
        geo_longitude = postdata['geo_longitude']
        property_id = postdata['property_id']
        post_title_th = postdata['post_title_th']
        post_description_th = postdata['post_description_th']
        # post_title_en = postdata['post_title_en']
        # post_description_en = postdata['post_description_en']
        # floor_no = postdata['floor_level']
        # bedroom = postdata['bed_room']
        # bathroom = postdata['bath_room']
        # ds_id = postdata["ds_id"]
        name = postdata["name"]
        mobile = postdata["mobile"]
        email = postdata["email"]
        # account_type = postdata["account_type"]
        user = postdata["user"]
        password = postdata["pass"]
        # project_name = postdata["project_name"]
        land_size_rai = postdata['land_size_rai']
        land_size_ngan = postdata['land_size_ngan']
        land_size_wah = postdata['land_size_wa']
        # post_description_en =  post_description_en.replace("\r\n","<br>")
        try:
            a = int(land_size_rai)
        except:
            land_size_rai = '0'
        try:
            a = int(land_size_ngan)
        except:
            land_size_ngan = '0'
        try:
            a = int(land_size_wah)
        except:
            land_size_wah = '0'
        project_name = ""
        try:
            project_name = postdata['web_project_name']
        except:
            try:
                project_name = postdata['project_name']
            except:
                project_name = post_title_th
        
        # print(post_description_th)
        list_dict = {'ขาย' : 1, 'ซื้อ':2,'แจกฟรี':6,'เช่า':9,'บริการ':16}
        province = {}
        with open('./static/thaihomeonline_province.json') as f:
            province = json.load(f)
        # print(addr_province)
        # print(province[addr_province])
        datapost = {
           'proptWant': "",
'proptType': property_type,
'proptSubjectTH': post_title_th,
'proptSubjectEN':"", 
'proptDetailTH': post_description_th,
'proptDetailEN':"", 
'proptProvince': "",
'proptDistrict': "",
'proptArea': "",
'proptProject': project_name,
'proptAddrNo':"", #addr_number
"proptRoad": addr_road,
"proptZipcode": "12345",
"gMapSearchTxt": "", 
'proptLatitude': geo_latitude,
'proptLongitude': geo_longitude,
'proptPrice': price_baht,
'proptPriceUnit': 'บาท',
'proptSpaceAll': "", #area
'proptSpaceWidth':"", 
'proptSpaceHeight':"", 
'proptSpaceRai': land_size_rai,
'proptSpaceNgaan': land_size_ngan, 
'proptSpaceSqw': land_size_wah, 
'proptSpaceLandW':"", 
'proptSpaceLandH':"", 
'hidStepCurrent': "postStep1",
        }    
        
        if listing_type == 'เช่า' :
            datapost['proptWant'] = 'rent'
        else :
            datapost['proptWant'] = 'sale'
        
        
        second_step = {}
        if str(property_type) == "1" :  #condo
            datapost['proptType'] = "condo"
            datapost['proptSpaceAll'] = postdata['floor_area']
           
        elif str(property_type) == "2" or str(property_type) == "3": #detached houses /home / house / Single House 
            datapost['proptType'] = "detached-house"
            datapost['proptSpaceAll'] = postdata['floor_area']
        # elif str(property_type) == "3" : # twin houses 
            
        elif str(property_type) == "4": # townhouses / town home / home office
            datapost['proptType'] = "townhouse"
            datapost['proptSpaceAll'] = postdata['floor_area']
                                      
        elif str(property_type) == "5": #commercial buildings  
            datapost['proptType'] = "shophouse"
            datapost['proptSpaceAll'] = postdata['floor_area']
            
             
            
        elif str(property_type) == "6": #land 
            datapost['proptType'] = "land" 
            datapost['proptSpaceAll'] = str(400*int(land_size_rai) + 100*int(land_size_ngan) + int(land_size_wah))
            
        elif str(property_type) == "7": #apartments 
            datapost['proptType'] = "apartment" 
            datapost['proptSpaceAll'] = postdata['floor_area']
            
        elif str(property_type) == "8": #hotels, Real Estate Residencial
            datapost['proptType'] = "business" 
            datapost['proptSpaceAll'] = postdata['floor_area']
            
        elif str(property_type) == "9": #Office 
            datapost['proptType'] = "office-space" 
            datapost['proptSpaceAll'] = postdata['floor_area']
            
            
            
        elif str(property_type) == "10": #warehouses
            datapost['proptType'] = "warehouse-factory"
            datapost['proptSpaceAll'] = postdata['floor_area']
             
            
        elif str(property_type) == "25": #Factory
            datapost['proptType'] = "warehouse-factory" 
            datapost['proptSpaceAll'] = postdata['floor_area']
            
        try :
            second_step = {
                'proptBedroom': "10 more" if int(postdata['bed_room']) >= 10 else postdata['bed_room'],
'proptBathroom': "10 more" if int(postdata['bath_room']) >= 10 else postdata['bath_room'],
'proptFloor': "50 more" if int(postdata['floor_total']) >= 50 else postdata['floor_total'],
'proptFloorIs': "50 above" if int(postdata['floor_level']) >= 50 else postdata['floor_level'],
'proptFurniture': "",
'hidStepCurrent': "postStep2"
            }
        except :
            second_step = {
                'proptBedroom': "",
'proptBathroom': "",
'proptFloor': "",
'proptFloorIs': "",
'proptFurniture': "",
'hidStepCurrent': "postStep2"
            } 
        
        # login
        login = self.test_login(postdata)
        success = login["success"]
        detail = login["detail"]
        post_id = ""
        post_url = ""
        filestoup = {}
        if(success == "True"):
            # print(addr_province,addr_district,addr_sub_district)
            addr_district = addr_district.replace(" ","")
            addr_province = addr_province.replace(" ","")
            addr_sub_district = addr_sub_district.replace(" ","")
            for key in province:
                if 'province' not in key:
                    if(addr_province.find(str(province[key]).strip()) != -1 or str(province[key]).find(addr_province.strip()) != -1):
                        datapost['proptProvince'] = key
                        break
            # district = province[datapost['proptProvince']+"_province"]
            # headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
            # }
            # r = httprequestObj.http_post('https://www.thaihomeonline.com/location/get-district/',data={'provinceID': datapost['proptProvince'],'elemName': 'proptDistrict','css': 'class="input1"'},headers=headers)
            # soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
            district = province[datapost['proptProvince']+'_province']
            # print("District\n",r.text)
            # print(district)
            for i in district:
                # datapost['proptArea'] = i['value']
                if(addr_sub_district.find(str(district[i]).strip()) != -1 or str(district[i]).strip().find(addr_district) != -1):
                    datapost['proptDistrict'] = i
                    break
            # for key in district:
            #     if(addr_district.find(str(district[key]).strip()) != -1):
            #         datapost['proptDistrict'] = key
            #         break
            # print(datapost['proptProvince'])
#             subdis = {
#                 'districtID': datapost['proptDistrict'],
# 'elemName': 'proptArea',
# 'css': 'class="input1"',
# 'onChange': 'areaChange()'
#             }
#             print('data\n',subdis)
#             r = httprequestObj.http_post('https://www.thaihomeonline.com/location/get-area/',data=subdis,headers=headers)
#             soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
            subdistrict = province[datapost['proptProvince']+'_province'+datapost['proptDistrict']+'_district']
            # print("SubDistrict\n",r.text)
            datapost['proptArea'] = i[0]
            for i in subdistrict:
                if(addr_sub_district.find(str(subdistrict[i]).strip()) != -1 or str(subdistrict[i]).strip().find(addr_sub_district)!= -1):
                    datapost['proptArea']= i
                    break
            
            r = httprequestObj.http_post('https://www.thaihomeonline.com/post-step1/?event=next', data=datapost)
            
            data = r.text
            # with open('/home/maxslide/Real_Estate/temp.html','w') as f:
            #     f.write(data)
            link = re.findall(r'https://www.thaihomeonline.com/post-step1/\?proptID=\d+',data)
            # print("printing link",link)
            if len(link) != 0:
                post_id = re.findall('=\d+',link[0])[0]
                post_id = post_id.replace("=","")
                post_url = 'https://www.thaihomeonline.com/post-step1/?proptID='+post_id
                detail = "Edit post URL"
                # print('post_id',post_id)
                r = httprequestObj.http_post('https://www.thaihomeonline.com/post-step2/?proptID='+post_id+'&event=next',data=second_step)
                
                step3 = {
                    'picOrderInit[]': '1',
'picOrderInit[]': '2',
'picOrderInit[]': '3',
'picOrderInit[]': '4',
'picOrderInit[]': '5',
'picOrderInit[]': '6',
'hidProptID': post_id,
'hidStepCurrent': 'postStep3'
                }
                r = httprequestObj.http_post('https://www.thaihomeonline.com/post-step3/?proptID='+post_id+'&event=next',data=step3)
                
                data = r.text
                soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
                authenticityToken = soup.find("input", {"name": "hidUaddrID"})['value']
                step_four = {
                    'addrFullnameTH': name,
'addrFullnameEN': '',
'addrMobile': mobile,
'addrAddressTH': addr_road,
'addrAddressEN':'', 
'proptProvince': datapost['proptProvince'],
'proptDistrict': datapost['proptDistrict'],
'proptArea': datapost['proptArea'],
'addrZipcode': '00000',
'hidStepCurrent': 'postStep4',
'hidUaddrID': authenticityToken
                }
                r = httprequestObj.http_post('https://www.thaihomeonline.com/post-step4/?proptID='+post_id+'&event=save', data=step_four)
                # with open('/home/maxslide/Real_Estate/temp.html','w') as f:
                #     f.write(r.text)
                if(re.search('ประกาศทั้งหมด', r.text)):
                    success = "True"
                else:
                    success = "False"

                options = Options()
                options.set_headless(True)
                options.add_argument('--no-sandbox')

                driver = webdriver.Chrome("./static/chromedriver", chrome_options=options)

                driver.implicitly_wait(4)

                wait = ui.WebDriverWait(driver,10)     
                driver.get('https://www.thaihomeonline.com/login/')
                log_u = driver.find_element_by_name('username')
                log_p = driver.find_element_by_name('password')
                log_u.send_keys(postdata['user'])
                log_p.send_keys(postdata['pass'])
                login_but = driver.find_element_by_xpath('//input[@value="เข้าสู่ระบบ"]')
                login_but.click()
                driver.get('https://www.thaihomeonline.com/post-step3/?proptID='+post_id)
                for i in range(len(postdata['post_images'][:6])):
                    clickel = driver.find_element_by_xpath('//a[@href="javascript:uploadStart('+str(i+1)+');"]')
                    clickel.click()
                    time.sleep(0.5)
                    filel = driver.find_element_by_name('upload_fileInsertImage')
                    # print(postdata['post_images'][i])
                    copyfile(os.getcwd() + "/"+ postdata['post_images'][i],os.getcwd() + "/"+ postdata['post_images'][i].replace("jpeg","jpg"))
                    filel.send_keys(os.getcwd() + "/"+ postdata['post_images'][i].replace("jpeg","jpg"))
                    driver.find_element_by_name('upload_btnSubmit').click()
                    wait.until(lambda driver: driver.find_element_by_xpath('//div[@id="postPicItem'+str(i+1)+'"]//div[@class="pic"]'))          
                    time.sleep(1)
                driver.find_element_by_name('btnSave').click()
                driver.close()
                driver.quit()
                r = httprequestObj.http_post('https://www.thaihomeonline.com/post-step4/?proptID='+post_id+'&event=next', data=step_four)
                r = httprequestObj.http_post('https://www.thaihomeonline.com/post-step-final/?proptID='+post_id+'&event=next', data={"hidStepCurrent": "postStepFinal"})
                post_url = 'https://www.thaihomeonline.com/property/'+post_id+'/'
            else:
                post_id = "error"
                post_url = "nolink"
        
        time_end = datetime.datetime.utcnow()
        print({
            "websitename": "thaihomeonline",
            "success": success,
            "time_usage": time_end - time_start,
            "time_start": time_start,
            "time_end": time_end,
            # "ds_id": "4",
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "",
            "detail": detail
        }
)
        return {
            "websitename": "thaihomeonline",
            "success": success,
            "usage_time": time_end - time_start,
            "start_time": time_start,
            "end_time": time_end,
            "ds_id": postdata['ds_id'],
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "",
            "detail": detail
        }

    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        try :
            print('0')
            options = Options()
            options.set_headless(True)
            options.add_argument('--no-sandbox')
            driver = webdriver.Chrome("./static/chromedriver", chrome_options=options)
            print('1')
            wait = ui.WebDriverWait(driver,10)     
            driver.get('https://www.thaihomeonline.com/login/')
            log_u = driver.find_element_by_name('username')
            log_p = driver.find_element_by_name('password')
            print('2')
            log_u.send_keys(postdata['user'])
            log_p.send_keys(postdata['pass'])
            login_but = driver.find_element_by_xpath('//input[@value="เข้าสู่ระบบ"]')
            login_but.click()
            print('3')
            driver.get('https://www.thaihomeonline.com/member/property-list/?show=current')

            r = BeautifulSoup(driver.page_source, features="html5lib")

            pages = r.find("div", attrs={"id": "pageBox"}).findAll("a")
            totalpages=1
            for i in pages:
                if i.text == "End":
                    totalpages = int(i["href"].split("=")[1].split("&")[0])
                    break

            for i in range(totalpages):
                driver.get('https://www.thaihomeonline.com/member/property-list/?page={}&show=current'.format(i+1))
                try:
                    a = driver.find_element_by_xpath('//a[@href="javascript:proptPushCheck('+postdata["post_id"]+');"]')
                    a.click()
                    found=True
                    break
                except:
                    found=False

            if found:
                print('4')
                wait.until(lambda driver: driver.find_element_by_xpath('//div[@id="proptPushBoxButton"]'))
                print('5')
                time.sleep(3)
                try:
                    driver.find_element_by_id('proptPushConfirm').click()
                except:
                    time_end = datetime.datetime.utcnow()
                    driver.close()
                    driver.quit()
                    return {
                        "websitename": "thaihomeonline",
                        "success": "false",
                        "usage_time": time_end - time_start,
                        "start_time": time_start,
                        "end_time": time_end,
                        "detail": "Time Remaining to postpone announcement, please try after sometime.",
                        "ds_id": postdata['ds_id'],
                        "log_id": postdata['log_id'],
                        "post_id": postdata['post_id'],
                    }
                print('6')
                driver.switch_to.alert.accept()
                print('7')
                time.sleep(2)
                driver.close()
                driver.quit()
                success = "True"
                detail = "Boost successful"
            else:
                success = "false"
                detail = "Post Not found"
                driver.close()
                driver.quit()

        except Exception as e:
            print(e)
            success = "False"
            detail = "Boost Unsuccessful"
            driver.close()
            driver.quit()
        finally:
            driver.close()
            driver.quit()
        
        time_end = datetime.datetime.utcnow()
        return {
            "websitename": "thaihomeonline",
            "success": success ,
            "usage_time": time_end - time_start,
            "start_time": time_start,
            "end_time": time_end,
            "detail": detail,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": postdata['post_id'],
        }

    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        
        datapost = {}
        login = self.test_login(postdata)
        success = login["success"]
        detail = login["detail"]
        post_id = postdata['post_id']
        post_url = 'https://www.thaihomeonline.com/member/property-delete/?proptID=546416'+post_id+'&mode=current'
        if(success == "True"):
            # print()
            r = httprequestObj.http_get(post_url)
            if r.status_code == 500 :
                success = "False"
                detail = "Cannot delete post with id"+post_id
            else:
                success = "True"
                detail = "Post sucessfully deleted"

        #
        #
        #

        time_end = datetime.datetime.utcnow()
        return {
            "websitename": "thaihomeonline",
            "success": success,
            "usage_time": time_end - time_start,
            "start_time": time_start,
            "end_time": time_end,
            "detail": detail,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": postdata['post_id']
        }

    def edit_post(self, postdata):
        # https://www.thaihomeonline.com/post/get_json_district?province_id=13   ->     for district
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        # print(postdata)
        # postdata = postdata
        # print(self.max_image)
        listing_type = postdata['listing_type']
        property_type = postdata['property_type']
        post_img_url_lists = postdata['post_img_url_lists']
        price_baht = postdata['price_baht']
        addr_province = postdata['addr_province']
        addr_district = postdata['addr_district']
        addr_sub_district = postdata['addr_sub_district']
        addr_road, addr_near_by, floorarea_sqm = ['','','']
        addr_number = '1'
        if 'addr_road' in postdata:
            addr_road = postdata['addr_road']
        if 'addr_near_by' in postdata:
            addr_near_by = postdata['addr_near_by']
        if 'floorarea_sqm' in postdata:
            floorarea_sqm = postdata['floorarea_sqm']
        if 'addr_number' in postdata:
            addr_number = postdata['addr_number']
            
            
        
        geo_latitude = postdata['geo_latitude']
        geo_longitude = postdata['geo_longitude']
        property_id = postdata['property_id']
        post_title_th = postdata['post_title_th']
        post_description_th = postdata['post_description_th']
        # post_title_en = postdata['post_title_en']
        # post_description_en = postdata['post_description_en']
        # floor_no = postdata['floor_level']
        # bedroom = postdata['bed_room']
        # bathroom = postdata['bath_room']
        # ds_id = postdata["ds_id"]
        name = postdata["name"]
        mobile = postdata["mobile"]
        email = postdata["email"]
        # account_type = postdata["account_type"]
        user = postdata["user"]
        password = postdata["pass"]
        # project_name = postdata["project_name"]
        land_size_rai = postdata['land_size_rai']
        land_size_ngan = postdata['land_size_ngan']
        land_size_wah = postdata['land_size_wa']
        # post_description_en =  post_description_en.replace("\r\n","<br>")
        try:
            a = int(land_size_rai)
        except:
            land_size_rai = '0'
        try:
            a = int(land_size_ngan)
        except:
            land_size_ngan = '0'
        try:
            a = int(land_size_wah)
        except:
            land_size_wah = '0'
        project_name = ""
        try:
            project_name = postdata['web_project_name']
        except:
            try:
                project_name = postdata['project_name']
            except:
                project_name = post_title_th
        
        # print(post_description_th)
        list_dict = {'ขาย' : 1, 'ซื้อ':2,'แจกฟรี':6,'เช่า':9,'บริการ':16}
        province = {}
        with open('./static/thaihomeonline_province.json') as f:
            province = json.load(f)
        # print(addr_province)
        # print(province[addr_province])
        datapost = {
           'proptWant': "sale",
'proptType': property_type,
'proptSubjectTH': post_title_th,
'proptSubjectEN':"", 
'proptDetailTH': post_description_th,
'proptDetailEN':"", 
'proptProvince': "",
'proptDistrict': "",
'proptArea': "",
'proptProject': project_name,
'proptAddrNo':"", #addr_number
"proptRoad": addr_road,
"proptZipcode": "12345",
"gMapSearchTxt": "", 
'proptLatitude': geo_latitude,
'proptLongitude': geo_longitude,
'proptPrice': price_baht,
'proptPriceUnit': 'บาท',
'proptSpaceAll': "", #area
'proptSpaceWidth':"", 
'proptSpaceHeight':"", 
'proptSpaceRai': land_size_rai,
'proptSpaceNgaan': land_size_ngan, 
'proptSpaceSqw': land_size_wah, 
'proptSpaceLandW':"", 
'proptSpaceLandH':"", 
'hidStepCurrent': "postStep1",
        }    
        if listing_type == 'เช่า' :
            datapost['proptWant'] = 'rent'
        else :
            datapost['proptWant'] = 'sale'
        
        second_step = {}
        if str(property_type) == "1" :  #condo
            datapost['proptType'] = "condo"
            datapost['proptSpaceAll'] = postdata['floor_area']
           
        elif str(property_type) == "2" or str(property_type) == "3": #detached houses /home / house / Single House 
            datapost['proptType'] = "detached-house"
            datapost['proptSpaceAll'] = postdata['floor_area']
        # elif str(property_type) == "3" : # twin houses 
            
        elif str(property_type) == "4": # townhouses / town home / home office
            datapost['proptType'] = "townhouse"
            datapost['proptSpaceAll'] = postdata['floor_area']
                                      
        elif str(property_type) == "5": #commercial buildings  
            datapost['proptType'] = "shophouse"
            datapost['proptSpaceAll'] = postdata['floor_area']
            
             
            
        elif str(property_type) == "6": #land 
            datapost['proptType'] = "land" 
            datapost['proptSpaceAll'] = str(400*int(land_size_rai) + 100*int(land_size_ngan) + int(land_size_wah))
            
        elif str(property_type) == "7": #apartments 
            datapost['proptType'] = "apartment" 
            datapost['proptSpaceAll'] = postdata['floor_area']
            
        elif str(property_type) == "8": #hotels, Real Estate Residencial
            datapost['proptType'] = "business" 
            datapost['proptSpaceAll'] = postdata['floor_area']
            
        elif str(property_type) == "9": #Office 
            datapost['proptType'] = "office-space" 
            datapost['proptSpaceAll'] = postdata['floor_area']
            
            
            
        elif str(property_type) == "10": #warehouses
            datapost['proptType'] = "warehouse-factory"
            datapost['proptSpaceAll'] = postdata['floor_area']
             
            
        elif str(property_type) == "25": #Factory
            datapost['proptType'] = "warehouse-factory" 
            datapost['proptSpaceAll'] = postdata['floor_area']
            
        try :
            second_step = {
                'proptBedroom': "10 more" if int(postdata['bed_room']) >= 10 else postdata['bed_room'],
'proptBathroom': "10 more" if int(postdata['bath_room']) >= 10 else postdata['bath_room'],
'proptFloor': "50 more" if int(postdata['floor_total']) >= 50 else postdata['floor_total'],
'proptFloorIs': "50 above" if int(postdata['floor_level']) >= 50 else postdata['floor_level'],
'proptFurniture': "",
'hidStepCurrent': "postStep2"
            }
        except :
            second_step = {
                'proptBedroom': "",
'proptBathroom': "",
'proptFloor': "",
'proptFloorIs': "",
'proptFurniture': "",
'hidStepCurrent': "postStep2"
            } 
        
        # login
        login = self.test_login(postdata)
        success = login["success"]
        detail = login["detail"]
        post_id = postdata["post_id"]
        post_url = ""
        filestoup = {}
        if(success == "True"):
            # print(addr_province,addr_district,addr_sub_district)
            addr_district = addr_district.replace(" ","")
            addr_province = addr_province.replace(" ","")
            addr_sub_district = addr_sub_district.replace(" ","")
            for key in province:
                if 'province' not in key:
                    if(addr_province.find(str(province[key]).strip()) != -1 or str(province[key]).find(addr_province.strip()) != -1):
                        datapost['proptProvince'] = key
                        break
            # district = province[datapost['proptProvince']+"_province"]
            # headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
            # }
            # r = httprequestObj.http_post('https://www.thaihomeonline.com/location/get-district/',data={'provinceID': datapost['proptProvince'],'elemName': 'proptDistrict','css': 'class="input1"'},headers=headers)
            # soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
            district = province[datapost['proptProvince']+'_province']
            # print("District\n",r.text)
            # print(district)
            for i in district:
                # datapost['proptArea'] = i['value']
                if(addr_sub_district.find(str(district[i]).strip()) != -1 or str(district[i]).strip().find(addr_district) != -1):
                    datapost['proptDistrict'] = i
                    break
            # for key in district:
            #     if(addr_district.find(str(district[key]).strip()) != -1):
            #         datapost['proptDistrict'] = key
            #         break
            # print(datapost['proptProvince'])
#             subdis = {
#                 'districtID': datapost['proptDistrict'],
# 'elemName': 'proptArea',
# 'css': 'class="input1"',
# 'onChange': 'areaChange()'
#             }
#             print('data\n',subdis)
#             r = httprequestObj.http_post('https://www.thaihomeonline.com/location/get-area/',data=subdis,headers=headers)
#             soup = BeautifulSoup(r.text, self.parser, from_encoding='utf-8')
            subdistrict = province[datapost['proptProvince']+'_province'+datapost['proptDistrict']+'_district']
            # print("SubDistrict\n",r.text)
            datapost['proptArea'] = i[0]
            for i in subdistrict:
                if(addr_sub_district.find(str(subdistrict[i]).strip()) != -1 or str(subdistrict[i]).strip().find(addr_sub_district)!= -1):
                    datapost['proptArea']= i
                    break
            
            r = httprequestObj.http_post('https://www.thaihomeonline.com/post-step1/?proptID='+post_id+'&event=next', data=datapost)
            
            data = r.text
            # with open('/home/maxslide/Real_Estate/temp.html','w') as f:
            #     f.write(data)
            link = re.findall(r'https://www.thaihomeonline.com/post-step1/\?proptID=\d+',data)
            # print("printing link",link)
            if len(link) != 0:
                # post_id = re.findall('=\d+',link[0])[0]
                # post_id = post_id.replace("=","")
                post_url = 'https://www.thaihomeonline.com/post-step1/?proptID='+post_id
                detail = "Edit post URL"
                # print('post_id',post_id)
                r = httprequestObj.http_post('https://www.thaihomeonline.com/post-step2/?proptID='+post_id+'&event=next',data=second_step)
                
                step3 = {
                    'picOrderInit[]': '1',
'picOrderInit[]': '2',
'picOrderInit[]': '3',
'picOrderInit[]': '4',
'picOrderInit[]': '5',
'picOrderInit[]': '6',
'hidProptID': post_id,
'hidStepCurrent': 'postStep3'
                }
                r = httprequestObj.http_post('https://www.thaihomeonline.com/post-step3/?proptID='+post_id+'&event=next',data=step3)
                
                data = r.text
                soup = BeautifulSoup(data, self.parser, from_encoding='utf-8')
                authenticityToken = soup.find("input", {"name": "hidUaddrID"})['value']
                step_four = {
                    'addrFullnameTH': name,
'addrFullnameEN': '',
'addrMobile': mobile,
'addrAddressTH': addr_road,
'addrAddressEN':'', 
'proptProvince': datapost['proptProvince'],
'proptDistrict': datapost['proptDistrict'],
'proptArea': datapost['proptArea'],
'addrZipcode': '00000',
'hidStepCurrent': 'postStep4',
'hidUaddrID': authenticityToken
                }
                r = httprequestObj.http_post('https://www.thaihomeonline.com/post-step4/?proptID='+post_id+'&event=save', data=step_four)
                # with open('/home/maxslide/Real_Estate/temp.html','w') as f:
                #     f.write(r.text)
                if(re.search('ประกาศทั้งหมด', r.text)):
                    success = "True"
                else:
                    success = "False"
                options = Options()
                options.set_headless(True)
                options.add_argument('--no-sandbox')

                driver = webdriver.Chrome("./static/chromedriver", chrome_options=options)

                driver.implicitly_wait(4)

                wait = ui.WebDriverWait(driver,10)     
                driver.get('https://www.thaihomeonline.com/login/')
                log_u = driver.find_element_by_name('username')
                log_p = driver.find_element_by_name('password')
                log_u.send_keys(postdata['user'])
                log_p.send_keys(postdata['pass'])
                login_but = driver.find_element_by_xpath('//input[@value="เข้าสู่ระบบ"]')
                login_but.click()
                driver.get('https://www.thaihomeonline.com/post-step3/?proptID='+post_id)
                for i in range(len(postdata['post_images'][:6])):
                    deletedata={
                        'proptID': post_id,
                        'order': str(i+1),
                        'picOrderInit': '1@2@3@4@5@6'
                    }
                    r=httprequestObj.http_post("https://www.thaihomeonline.com/post-pic-delete/",data=deletedata)
                    driver.get('https://www.thaihomeonline.com/post-step3/?proptID=' + post_id)
                    clickel = driver.find_element_by_xpath('//a[@href="javascript:uploadStart('+str(i+1)+');"]')
                    clickel.click()
                    time.sleep(0.5)
                    filel = driver.find_element_by_name('upload_fileInsertImage')
                    # print(postdata['post_images'][i])
                    copyfile(os.getcwd() + "/"+ postdata['post_images'][i],os.getcwd() + "/"+ postdata['post_images'][i].replace("jpeg","jpg"))
                    filel.send_keys(os.getcwd() + "/"+ postdata['post_images'][i].replace("jpeg","jpg"))
                    driver.find_element_by_name('upload_btnSubmit').click()
                    wait.until(lambda driver: driver.find_element_by_xpath('//div[@id="postPicItem'+str(i+1)+'"]//div[@class="pic"]'))          
                    time.sleep(1)
                driver.find_element_by_name('btnSave').click()
                driver.close()
                driver.quit()
                r = httprequestObj.http_post('https://www.thaihomeonline.com/post-step4/?proptID='+post_id+'&event=next', data=step_four)
                r = httprequestObj.http_post('https://www.thaihomeonline.com/post-step-final/?proptID='+post_id+'&event=next', data={"hidStepCurrent": "postStepFinal"})
                post_url = 'https://www.thaihomeonline.com/property/'+post_id+'/'
            else:
                post_id = "error"
                post_url = "nolink"
        
        time_end = datetime.datetime.utcnow()
        print({
            "websitename": "thaihomeonline",
            "success": success,
            "time_usage": time_end - time_start,
            "time_start": time_start,
            "time_end": time_end,
            # "ds_id": "4",
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "",
            "detail": detail
        }
)
        return {
            "websitename": "thaihomeonline",
            "success": success,
            "time_usage": time_end - time_start,
            "time_start": time_start,
            "time_end": time_end,
            # "ds_id": "4",
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "",
            "detail": detail
        }

    def search_post(self,postdata):
        #self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        #search
        start_time = datetime.datetime.utcnow()

        login = self.test_login(postdata)
        
        post_found = "False"
        post_id = ''
        post_url = ''
        post_view = ''
        post_modify_time = ''
        post_create_time = ''
        detail = 'No post with this title'
        title = ''
        if (login['success'] == 'True'):

            
            all_posts_url = 'https://www.thaihomeonline.com/member/property-list/?show=current'

            all_posts = httprequestObj.http_get(all_posts_url)

            r = BeautifulSoup(all_posts.content, features = "html5lib")

            pages=r.find("div",attrs={"id":"pageBox"}).findAll("a")
            for i in pages:
                if i.text=="End":
                    totalpages=int(i["href"].split("=")[1][0])
                    break

            xyz=[]
            for i in range(totalpages):
                url="https://www.thaihomeonline.com/member/property-list/?page={}&show=current".format(i+1)
                res=httprequestObj.http_get(url)
                page=BeautifulSoup(res.text, features="html5lib")
                a = page.find('div', attrs = {'class':'boxTable'}).findAll('tr')
                xyz.extend(a[1:])

            #print(len(xyz))
            
            if xyz == None:
                detail = "Post Not Found"
            else:
                flag= 0
                for one in xyz:
                    titl = one.find('div',attrs={'class','subject'}).find('a')  
                    if titl['title']==postdata['post_title_th']:
                        post_url = titl['href']

                        #print(post_url,end = '\n')
                        post_found = "true"
                        time = one.findAll('td')
                        post_create_time = time[2].text
                        post_id = post_url.split('/')[-2]

                        #post_view = divi.find('li',attrs={'class':'price'}).findAll('span')[-1].text.split(' ')[1]
                                            
                        detail = "Post Found "
                        flag=1
                        break
                if flag==0:
                    detail = "Post Not Found"
                    post_found = 'False'
                    #print("yha se gya")
                      
                    
        else :
            detail = 'Can not log in'
            post_found = 'False'

        end_time = datetime.datetime.utcnow()
        

        return {
            "websitename": "thaihomeonline",
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
            "post_found": post_found,
            "post_title_th": postdata['post_title_th']
        }



    def print_debug(self, msg):
        if(self.debug == 1):
            print(msg)
        return True

    def print_debug_data(self, data):
        if(self.debugdata == 1):
            print(data)
        return True
