from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
import re
import json
import datetime
import sys
import requests
import random
import urllib.parse as urlparse
from urllib.parse import parse_qs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.common.by import By
import cloudscraper
import undetected_chromedriver.v2 as uc


with open("./static/hipflat_province.json", encoding='utf-8') as f:
    provincedata = json.load(f)

class hipflat():
   
    name = 'hipflat'

    def __init__(self):
   
        try:
            import configs

        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.primarydomain = ''
        self.debug = 0
        self.debugresdata = 0
        self.baseurl = 'https://www.hipflat.co.th'
        self.parser = 'html.parser'
        self.session = lib_httprequest()



    def upload_file(self,postdata,post_id):

        options = uc.ChromeOptions()
        options.headless = True
        browser = uc.Chrome('./static/chromedriver', options=options)

        try:
            browser.implicitly_wait(10)

            browser.get('https://www.hipflat.co.th/login')
            #browser.save_screenshot('./log/hipflat.png')
            time.sleep(1)
            email = browser.find_element_by_id('user_email')
            email.send_keys(postdata['user'])
            password = browser.find_element_by_id('user_password')
            password.send_keys(postdata['pass'])
            browser.find_element_by_name('commit').click()
            browser.get('https://www.hipflat.co.th/listings/'+post_id+'/edit')


            allimages = postdata['post_images']

            dropzone = browser.find_element_by_id("dropzone-upload-link")

            files = [os.getcwd() + "/" + img for img in allimages]

            isLocal = not browser._is_remote or '127.0.0.1' in browser.command_executor._url

            JS_DROP_FILES = "var c=arguments,b=c[0],k=c[1];c=c[2];for(var d=b.ownerDocument||document,l=0;;){var e=b.getBoundingClientRect(),g=e.left+(k||e.width/2),h=e.top+(c||e.height/2),f=d.elementFromPoint(g,h);if(f&&b.contains(f))break;if(1<++l)throw b=Error('Element not interactable'),b.code=15,b;b.scrollIntoView({behavior:'instant',block:'center',inline:'center'})}var a=d.createElement('INPUT');a.setAttribute('type','file');a.setAttribute('multiple','');a.setAttribute('style','position:fixed;z-index:2147483647;left:0;top:0;');a.onchange=function(b){a.parentElement.removeChild(a);b.stopPropagation();var c={constructor:DataTransfer,effectAllowed:'all',dropEffect:'none',types:['Files'],files:a.files,setData:function(){},getData:function(){},clearData:function(){},setDragImage:function(){}};window.DataTransferItemList&&(c.items=Object.setPrototypeOf(Array.prototype.map.call(a.files,function(a){return{constructor:DataTransferItem,kind:'file',type:a.type,getAsFile:function(){return a},getAsString:function(b){var c=new FileReader;c.onload=function(a){b(a.target.result)};c.readAsText(a)}}}),{constructor:DataTransferItemList,add:function(){},clear:function(){},remove:function(){}}));['dragenter','dragover','drop'].forEach(function(a){var b=d.createEvent('DragEvent');b.initMouseEvent(a,!0,!0,d.defaultView,0,0,0,g,h,!1,!1,!1,!1,0,null);Object.setPrototypeOf(b,null);b.dataTransfer=c;Object.setPrototypeOf(b,DragEvent.prototype);f.dispatchEvent(b)})};d.documentElement.appendChild(a);a.getBoundingClientRect();return a;"

            elm_input = browser.execute_script(JS_DROP_FILES, dropzone, 0, 0)
            value = '\n'.join(files)
            elm_input._execute('sendKeysToElement', {'value': [value], 'text': value})
            

            time.sleep(10)

            browser.find_element_by_name('commit').click()
            browser.get('https://www.hipflat.co.th/logout')
        finally:
            #browser.close()
            browser.quit()
            try:
                alert = browser.switch_to.alert
                alert.accept()
                #browser.close()
                browser.quit()
            except:
                pass






    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        
        start_time = datetime.datetime.utcnow()
        self.session.http_get_with_headers('https://www.hipflat.co.th/logout')

        headers = {
            'user_agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36'
        }

        response = self.session.http_get('https://www.hipflat.co.th/login', headers = headers)
        soup = BeautifulSoup(response.content, features = self.parser)

        post_data = {
        '_method':'delete',
        'authenticity_token': soup.find("meta",{"name":"csrf-token"})['content']
        }

        self.session.http_post_with_headers('https://www.hipflat.co.th/logout', data=post_data)


        success = "false"
        detail = ""

        data = {
            "utf8": '',
            "authenticity_token": '',
            "user[session_id]": '',
            "user[old_session_id]": '',
            "user[locale]": '',
            "user[email]": str(postdata['user']),
            "user[first_name]": str(postdata['name_th']),
            "user[last_name]": str(postdata['surname_th']),
            "commit": "ลงทะเบียน"
        }


        if data['user[email]'] == "":
            detail = "Invalid email"
        elif data['user[first_name]'] == "":
            detail = "Please enter your name"
        else:
            try:
                response = self.session.http_get('https://www.hipflat.co.th/signup', headers = headers)

                soup = BeautifulSoup(response.content, features = "html.parser")

                data['utf8'] = str(soup.find('input', attrs = {'name': 'utf8'})['value'])

                data['authenticity_token'] = str(soup.find('input', attrs = {'name': 'authenticity_token'})['value'])

                data['user[locale]'] = str(soup.find('input', attrs = {'name': 'user[locale]'})['value'])

                res = self.session.http_post('https://www.hipflat.co.th/signup', data = data, headers = headers)


                if 'มีผู้ลงทะเบียนใช้อีเมล' in res.text:
                    success = "false"
                    detail = 'Email already registered'

                else:
                    success = "true"
                    detail = "Registration successful, please confirm your email and set your password there"


            except requests.exceptions.RequestException:
                detail = "Network Problem occured"

        

        end_time = datetime.datetime.utcnow()


        return {
            "websitename": "hipflat",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(end_time - start_time),
            "ds_id" : str(postdata['ds_id']),
            "detail": detail
        }





    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        print('0')
        start_time = datetime.datetime.utcnow()
        print('1')

        scraper = cloudscraper.create_scraper()

        data = {
            'utf8': '',
            'authenticity_token': '',
            'user[email]': str(postdata['user']),
            'user[password]': str(postdata['pass']),
            'user[remember_me]': '0',
            'commit': 'ลงชื่อเข้าใช้'
        }

        headers = {
            'user_agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36'
        }

        response = scraper.get('https://www.hipflat.co.th/login', headers = headers)
        soup = BeautifulSoup(response.content, features = self.parser)

        
        post_data = {
        '_method':'delete',
        'authenticity_token': soup.find("meta",{"name":"csrf-token"})['content']
        }
        

        scraper.post('https://www.hipflat.co.th/logout', data=post_data)

        success = "false"
        detail = ""
        
        if data['user[email]'] == "":
            detail = "Invalid username"
        elif data['user[password]'] == "":
            detail = "Invalid Password"
        else:
            try:

                response = scraper.get('https://www.hipflat.co.th/login', headers = headers)
                soup = BeautifulSoup(response.content, features = "html.parser")
                try:
                    data['utf8'] = str(soup.find('input', attrs = {'name': 'utf8'})['value'])
                except:
                    post_data = {
                    '_method':'delete',
                    'authenticity_token': soup.find("meta",{"name":"csrf-token"})['content']
                    }

                    scraper.post('https://www.hipflat.co.th/logout', data=post_data)
                    response = scraper.get('https://www.hipflat.co.th/login', headers = headers)
                    soup = BeautifulSoup(response.content, features = "html.parser")
                    data['utf8'] = str(soup.find('input', attrs = {'name': 'utf8'})['value'])


                data['authenticity_token'] = str(soup.find('input', attrs = {'name': 'authenticity_token'})['value'])

                
                response = scraper.post('https://www.hipflat.co.th/login', data = data, headers = headers)
                #print(response.status_code)
                #print(response.url)
                #
                """ print('=======rest')
                print(response.text) """
                
                #if 'อีเมลล์หรือรหัสผ่าน ไม่ถูกต้อง' in response.text:
                if response.url == 'https://www.hipflat.co.th/login':
                    success = "false"
                    detail = 'Incorrect Username or Password !!'
                else:
                    success = "true"
                    detail = 'Logged in successfully'
                    #res = self.session.http_get('http://www.estate.in.th/member/index.php')
                    #print(res.text)
            
            except:
                detail = "Network Problem occured"

        end_time = datetime.datetime.utcnow()

        return {
            "websitename": 'hipflat',
            "success": success,
            "ds_id" : str(postdata['ds_id']),
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(end_time - start_time),
            "detail": detail
        }






    def create_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()

        scraper = cloudscraper.create_scraper()
        success = 'false'
        detail = ''
        data = {
            'utf8': '',
            'authenticity_token': '',
            'user[email]': str(postdata['user']),
            'user[password]': str(postdata['pass']),
            'user[remember_me]': '0',
            'commit': 'ลงชื่อเข้าใช้'
        }
        headers = {
            'user_agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36'
        }
        try:
            response = scraper.get('https://www.hipflat.co.th/login', headers = headers)
            soup = BeautifulSoup(response.content, features = "html.parser")
            try:
                data['utf8'] = str(soup.find('input', attrs = {'name': 'utf8'})['value'])
            except:
                post_data = {
                    '_method':'delete',
                    'authenticity_token': soup.find("meta",{"name":"csrf-token"})['content']
                }
                scraper.post('https://www.hipflat.co.th/logout', data=post_data)
                response = scraper.get('https://www.hipflat.co.th/login', headers = headers)
                soup = BeautifulSoup(response.content, features = "html.parser")
                data['utf8'] = str(soup.find('input', attrs = {'name': 'utf8'})['value'])
            data['authenticity_token'] = str(soup.find('input', attrs = {'name': 'authenticity_token'})['value'])
            print(data['authenticity_token'])
            response = scraper.post('https://www.hipflat.co.th/login', data = data, headers = headers)
            if response.url == 'https://www.hipflat.co.th/login':
                success = "false"
                detail = 'Incorrect Username or Password !!'
            else:
                success = "true"
                detail = 'Logged in successfully'
        except:
            detail = "Network Problem occured"

        post_id = ''
        post_url = ''

        if success == 'true':

            if 'web_project_name' not in postdata or postdata['web_project_name'] == "":
                if 'project_name' in postdata and postdata['project_name'] != "":
                    postdata['web_project_name'] = postdata['project_name']
                else:
                    postdata['web_project_name'] = postdata['post_title_th']

            #print(postdata['web_project_name'])


            getProdId = {
                '1': 'condo',
                '2': 'house',
                '3': 'house',
                '4': 'townhouse',
                '5': 'shophouse',
                '6': 'land',
                '7': 'multifamily',
                '8': 'hotel',
                '9': 'office',
                '10': 'warehouse',
                '25': 'warehouse'
            }



            province_id = '0'
            amphur_id = '0'
            tumbon_id = '0'
            #print(postdata['addr_province'])
            for (key, value) in provincedata.items():
                # print(value.strip(),postdata['addr_province'])
                #if type(value) is str and (postdata['addr_province'].strip().find(value.strip()) != -1 or value.strip().find(postdata['addr_province'].strip()) != -1):
                if '_amphur' not in str(key) and '_province' not in str(key) and (str(postdata['addr_province']) in str(value) or str(value) in str(postdata['addr_province'])):
                #if str(postdata['addr_province']) == str(value)
                    province_id = str(key)
                    break
            #print(province_id)
            #print(postdata['addr_district'])
            if province_id != '0':
                for (key, value) in provincedata[province_id+"_province"].items():
                    # print(value.strip())
                    #if postdata['addr_district'].strip().find(value.strip()) != -1 or value.strip().find(postdata['addr_district'].strip()) != -1:
                    if str(postdata['addr_district']) == "วัฒนา" and str(value) == "วัฒนา":
                    #if str(postdata['addr_district']) == str(value):
                        # if value.strip().find(postdata['addr_district'].replace(" ","")) == -1:
                            # continue
                        amphur_id = str(key)
                        break
                    elif (str(postdata['addr_district']) in str(value) or str(value) in str(postdata['addr_district'])) and str(postdata['addr_district']) != "วัฒนา":
                        amphur_id = str(key)
                        break
                    '''elif value.strip().find(postdata['addr_district'].replace(" ", "")) != -1 or postdata['addr_district'].replace(" ", "").find(value.strip()) != -1:
                        amphur_id = key
                        break'''

            if amphur_id != '0':
                for (key, value) in provincedata[amphur_id+"_amphur"].items():
                    #if postdata['addr_sub_district'].strip().find(value.strip()) != -1:
                    if str(postdata['addr_sub_district']) in str(value) or str(value) in str(postdata['addr_sub_district']):
                        tumbon_id = str(key)
                        break
            if province_id == '0':
                province_id = '5599801770726f1f36000019'

            if amphur_id == '0':
                amphur_id = '5599801870726f1f36000058'

            if tumbon_id == '0':
                tumbon_id = '5599801f70726f1f36000b5e'

            #print(provincedata['5599801970726f1f3600017e_amphur'])

            
            #'listing[project_name]': 'วอร์เตอร์มาร์ค เจ้าพระยา',
            #'listing[project_name]': str(postdata['web_project_name']),
            #print(province_id)
            #print(amphur_id)
            #print(tumbon_id)
            #'listing[bedrooms]': str(postdata['bed_room']),
            #    'listing[bathrooms]': str(postdata['bath_room']),

            

            dataque = {
                "params": "query="+ str(postdata['web_project_name']) +"&hitsPerPage=1"
            }
            

            if postdata['property_type'] == "1":
                res = scraper.post(f'https://tom76npq59-dsn.algolia.net/1/indexes/PROD_Projects/query?x-algolia-api-key=318055435c6b9c9bdb6fefe330216299&x-algolia-application-id=TOM76NPQ59&x-algolia-agent=Algolia%20for%20jQuery%203.10.2', data=json.dumps(dataque))
                project = res.json()
                if len(project['hits']) > 0:
                    condo_id = str(project['hits'][0]['objectID'])
                    pro_name = ''
                    lat = str(project['hits'][0]['lat'])
                    lng = str(project['hits'][0]['lng'])
                else:
                    condo_id = ''
                    pro_name = str(postdata['web_project_name'])
                    lat = str(postdata['geo_latitude'])
                    lng = str(postdata['geo_longitude'])
            else:
                condo_id = ''
                pro_name = str(postdata['web_project_name'])
                lat = str(postdata['geo_latitude'])
                lng = str(postdata['geo_longitude'])

            data = {
                'utf8': '',
                'authenticity_token': '',
                'ga_client_id': '',
                'listing[added_manually]': 'false',
                'listing[token]': '',
                'listing[rank]': '',
                'listing[is_active]': 'true',
                'listing[never_expires]': 'true',
                'listing[property_type]': str(getProdId[str(postdata['property_type'])]),
                'listing[reference_number]': '',
                'listing[title_deed]': 'free',
                'listing[major_region_id]': province_id,
                'listing[region_id]': amphur_id,
                'listing[place_id]': tumbon_id,
                'listing[project_name]': pro_name,
                'listing[condo_id]': condo_id,
                'listing[street_number]': '-',
                'listing[street_name]': str(postdata['addr_road']),
                'listing[street_postcode]': '-',
                'listing[location_string]': lat + ',' + lng,
                'listing[rooms_number]': '',
                'listing[internal_area_sqm]': str(postdata['floor_area']),
                'listing[plot_area][units]': 'thai',
                'listing[plot_area][value]': str(postdata['floor_area']),
                'listing[plot_area][rai]': str(postdata['land_size_rai']),
                'listing[plot_area][ngaan]': str(postdata['land_size_ngan']),
                'listing[plot_area][sqwa]': str(postdata['land_size_wa']),
                'listing[bedrooms]': str(postdata['bed_room']),
                'listing[bathrooms]': str(postdata['bath_room']),
                'listing[floor]': str(postdata['floor_level']),
                'listing[building_floors]': str(postdata['floor_total']),
                'listing[furnishing]': 'partial',
                'listing[facing_direction]': str(postdata['direction_type']),
                'listing[parking_spaces]': '1',
                'listing[special_features][duplex]': 0,
                'listing[special_features][penthouse]': 0,
                'listing[special_features][renovated]': 0,
                'listing[special_features][original_condition]': 0,
                'listing[special_features][corner_unit]': 0,
                'listing[special_features][ground_floor]': 0,
                'listing[special_features][green_view]': 0,
                'listing[special_features][city_view]': 0,
                'listing[special_features][sea_view]': 0,
                'listing[special_features][pool_view]': 0,
                'listing[special_features][mountain_view]': 0,
                'listing[special_features][river_view]': 0,
                'listing[special_features][lake_view]': 0,
                'listing[special_features][pets_allowed]': 0,
                'listing[special_features][small_pets_allowed]': 0,
                'listing[private_amenities][air_con]': 0,
                'listing[private_amenities][bathtub]': 0,
                'listing[private_amenities][jacuzzi]': 0,
                'listing[private_amenities][private_pool]': 0,
                'listing[private_amenities][private_garden]': 0,
                'listing[private_amenities][intercom]': 0,
                'listing[private_amenities][water_heater]': 0,
                'listing[private_amenities][builtin_kitchen]': 0,
                'listing[private_amenities][cooker_hob]': 0,
                'listing[private_amenities][builtin_wardrobe]': 0,
                'listing[private_amenities][walkin_wardrobe]': 0,
                'listing[private_amenities][maids_room]': 0,
                'listing[private_amenities][study_room]': 0,
                'listing[private_amenities][balcony]': 0,
                'listing[private_amenities][patio]': 0,
                'listing[private_amenities][terrace]': 0,
                'listing[private_amenities][roof_terrace]': 0,
                'listing[private_amenities][garage]': 0,
                'listing[common_facilities][elevator]': 0,
                'listing[common_facilities][security]': 0,
                'listing[common_facilities][cctv]': 0,
                'listing[common_facilities][parking]': 0,
                'listing[common_facilities][open_parking]': 0,
                'listing[common_facilities][basement_parking]': 0,
                'listing[common_facilities][covered_parking]': 0,
                'listing[common_facilities][pool]': 0,
                'listing[common_facilities][sauna]': 0,
                'listing[common_facilities][jacuzzi]': 0,
                'listing[common_facilities][gym]': 0,
                'listing[common_facilities][garden]': 0,
                'listing[common_facilities][playground]': 0,
                'listing[common_facilities][shop]': 0,
                'listing[common_facilities][restaurant]': 0,
                'listing[common_facilities][wifi]': 0,
                'listing[common_facilities][clubhouse]': 0,
                'listing[common_facilities][lounge]': 0,
                'listing[common_facilities][basketball]': 0,
                'listing[common_facilities][billiard]': 0,
                'listing[common_facilities][mini_golf]': 0,
                'listing[common_facilities][putting_green]': 0,
                'listing[common_facilities][driving_range]': 0,
                'listing[common_facilities][tennis]': 0,
                'listing[common_facilities][squash]': 0,
                'listing[common_facilities][badminton]': 0,
                'listing[common_facilities][laundry]': 0,
                'listing[common_facilities][library]': 0,
                'listing[common_facilities][function_room]': 0,
                'listing[common_facilities][karaoke]': 0,
                'listing[description]': str(postdata['post_description_th']),
                'listing[name]': str(postdata['name']),
                'listing[phone]': str(postdata['mobile']),
                'listing[email]': str(postdata['user']),
                'commit': 'record'
            }

            if(str(postdata['bed_room']) == "" or str(postdata['bed_room']) == "null" or 'bed_room' not in postdata or str(postdata['bed_room']) == None):
                data['listing[bedrooms]'] == '0'

            else:
                data['listing[bedrooms]'] == str(postdata['bed_room'])

            if(str(postdata['bath_room']) == "" or str(postdata['bath_room']) == "null" or 'bath_room' not in postdata or str(postdata['bath_room']) == None):
                data['listing[bathrooms]'] == '1'

            else:
                data['listing[bathrooms]'] == str(postdata['bath_room'])

            if 'watermark เจ้าพระยา' in str(postdata['web_project_name']):
            
                data['listing[project_name]'] = 'วอร์เตอร์มาร์ค เจ้าพระยา'
                data['listing[condo_id]'] = '5119af8eef23779a61000713'
            
          
            response = scraper.get('https://www.hipflat.co.th/listings/add?rank=100', headers = headers)
            soup = BeautifulSoup(response.content,'html.parser')
            alert = soup.find('div',{'class' : 'alert-backdrop'})

            if alert != None:
                response_free = scraper.get('https://www.hipflat.co.th/account/listings/free', headers = headers)
                soup_free = BeautifulSoup(response_free.content,'html.parser')
                company_account = str(soup_free.find('div',{'class' : 'col-md-7 col-md-offset-3 col-sm-8'}).find('h1').find('small').text).split('\n')[1]
                soup_free_count = 0
                list_post = soup_free.find('div',{'class' : 'user-listings__collection'}).find_all('div')
                for list_post_t in list_post:
                    try:
                        for list_post_t_2 in list_post_t['class']:
                            if ("user-listing__state--live" in list_post_t_2) or ("user-listing__state--publishing" in list_post_t_2):
                                soup_free_count += 1
                    except:
                        pass

                if soup_free_count < 3 and company_account!='คุณใช้สิทธิ์การลงประกาศฟรีครบ 3 ประกาศแล้ว':
                    response = scraper.get('https://www.hipflat.co.th/listings/add?rank=1', headers = headers)
                else:
                    return{
                        "websitename": "hipflat",
                        "success": 'false',
                        "start_time": str(start_time),
                        "end_time": str(datetime.datetime.utcnow()),
                        "usage_time": str(datetime.datetime.utcnow() - start_time),
                        "post_url": post_url,
                        "ds_id": postdata['ds_id'],
                        "post_id": post_id,
                        "detail": 'บัญชีฟรีของท่านมีครบทั้ง 3 ประกาศแล้ว',
                        "account_type": "null"
                    }
            
            soup = BeautifulSoup(response.content, features = "html.parser")

            data['utf8'] = str(soup.find('input', attrs = {'name': 'utf8'})['value'])

            data['authenticity_token'] = str(soup.find('input', attrs = {'name': 'authenticity_token'})['value'])
            data['listing[rank]'] = str(soup.find('input', attrs = {'name': 'listing[rank]'})['value'])

            if postdata['listing_type'] == 'เช่า':
                data['listing[rent_availability_status]'] = 'true'
                data['listing[rent_price]'] = str(postdata['price_baht'])
            else:
                data['listing[sale_availability_status]'] = 'true'
                data['listing[sale_price]'] = str(postdata['price_baht'])

            r = scraper.post('https://www.hipflat.co.th/listings/add', data = data, headers = headers)

            success = "true"
            detail = "Post created successfully"

            data = r.text

            link = ''
            aaas = []
            self.test_login(postdata)
            r = scraper.get('https://www.hipflat.co.th/account/listings/pro')
            data=r.text

            soup = BeautifulSoup(data, features = "html.parser")

            for i in soup.find_all('a'):
                try:
                    if i.get('href').find('/edit') != -1:

                        aaas.append(i['href'])
                except:
                    continue

            link = str(aaas[0])
            link = link.replace('/listings/','')
            post_id = str(link.replace('/edit',''))

            post_url = str('https://www.hipflat.co.th/listing-preview/'+str(post_id))

            if 'post_images' in postdata and len(postdata['post_images']) > 0:
                self.upload_file(postdata,post_id)

        else:
            success = "false"
            detail = "Can not log in"
            
        end_time = datetime.datetime.utcnow()
        
        return {
            "websitename": "hipflat",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(end_time - start_time),
            "post_url": post_url,
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
            "detail": detail,
            "account_type": "null"
        }

    def edit_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()
        print('start')
        scraper = cloudscraper.create_scraper()
        success = 'false'
        detail = ''
        data = {
            'utf8': '',
            'authenticity_token': '',
            'user[email]': str(postdata['user']),
            'user[password]': str(postdata['pass']),
            'user[remember_me]': '0',
            'commit': 'ลงชื่อเข้าใช้'
        }
        headers = {
            'user_agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36'
        }
        try:
            response = scraper.get('https://www.hipflat.co.th/login', headers = headers)
            soup = BeautifulSoup(response.content, features = "html.parser")
            try:
                data['utf8'] = str(soup.find('input', attrs = {'name': 'utf8'})['value'])
            except:
                post_data = {
                    '_method':'delete',
                    'authenticity_token': soup.find("meta",{"name":"csrf-token"})['content']
                }
                scraper.post('https://www.hipflat.co.th/logout', data=post_data)
                response = scraper.get('https://www.hipflat.co.th/login', headers = headers)
                soup = BeautifulSoup(response.content, features = "html.parser")
                data['utf8'] = str(soup.find('input', attrs = {'name': 'utf8'})['value'])
            data['authenticity_token'] = str(soup.find('input', attrs = {'name': 'authenticity_token'})['value'])
            response = scraper.post('https://www.hipflat.co.th/login', data = data, headers = headers)
            if response.url == 'https://www.hipflat.co.th/login':
                success = "false"
                detail = 'Incorrect Username or Password !!'
            else:
                success = "true"
                detail = 'Logged in successfully'
        except:
            detail = "Network Problem occured"
        
        if success == "true":
            req_post_id = str(postdata['post_id'])
            found = True
            page = 1
            """while True:
                res = scraper.get("https://www.hipflat.co.th/account/listings/pro/page/"+str(page), headers = headers).text
                soup = BeautifulSoup(res, features = self.parser)
                count = 0
                for i in soup.find_all('a'):
                    if i.get('href') and i.get('href').find('/edit') != -1:
                        link = i.get('href').split('/')
                        count += 1
                        # print(link)
                        if len(link)>2 and link[2]==req_post_id:
                            found = True
                            break
                page += 1
                if found or count==0:
                    break"""

            if found:
                if 'web_project_name' not in postdata or postdata['web_project_name'] == "":
                    if 'project_name' in postdata and postdata['project_name'] != "":
                        postdata['web_project_name'] = postdata['project_name']
                    else:
                        postdata['web_project_name'] = postdata['post_title_th']

                getProdId = {
                    '1': 'condo',
                    '2': 'house',
                    '3': 'house',
                    '4': 'townhouse',
                    '5': 'shophouse',
                    '6': 'land',
                    '7': 'multifamily',
                    '8': 'hotel',
                    '9': 'office',
                    '10': 'warehouse',
                    '25': 'warehouse'
                }
                #print('1')



                province_id = '0'
                amphur_id = '0'
                tumbon_id = '0'
                #print(postdata['addr_province'])
                for (key, value) in provincedata.items():
                    # print(value.strip(),postdata['addr_province'])
                    #if type(value) is str and (postdata['addr_province'].strip().find(value.strip()) != -1 or value.strip().find(postdata['addr_province'].strip()) != -1):
                    if '_amphur' not in str(key) and '_province' not in str(key) and (str(postdata['addr_province']) in str(value) or str(value) in str(postdata['addr_province'])):

                        province_id = str(key)
                        break
                #print(province_id)
                #print(postdata['addr_district'])
                if province_id != '0':
                    for (key, value) in provincedata[province_id+"_province"].items():
                        # print(value.strip())
                        #if postdata['addr_district'].strip().find(value.strip()) != -1 or value.strip().find(postdata['addr_district'].strip()) != -1:
                        if str(postdata['addr_district']) == "วัฒนา" and str(value) == "วัฒนา":
                            amphur_id = str(key)
                            break
                        elif (str(postdata['addr_district']) in str(value) or str(value) in str(postdata['addr_district'])) and str(postdata['addr_district']) != "วัฒนา":
                            amphur_id = str(key)
                            break
                        '''elif value.strip().find(postdata['addr_district'].replace(" ", "")) != -1 or postdata['addr_district'].replace(" ", "").find(value.strip()) != -1:
                            amphur_id = key
                            break'''

                if amphur_id != '0':
                    for (key, value) in provincedata[amphur_id+"_amphur"].items():
                        #if postdata['addr_sub_district'].strip().find(value.strip()) != -1:
                        if str(postdata['addr_sub_district']) in str(value) or str(value) in str(postdata['addr_sub_district']):
                            tumbon_id = str(key)
                            break
                if province_id == '0':
                    province_id = '5599801770726f1f36000019'

                if amphur_id == '0':
                    amphur_id = '5599801870726f1f36000058'

                if tumbon_id == '0':
                    tumbon_id = '5599801f70726f1f36000b5e'


                dataque = {
                    "params": "query="+ str(postdata['web_project_name']) +"&hitsPerPage=1"
                }
                
                #print(postdata['property_type'])

                if postdata['property_type'] == "1":
                    res = scraper.post(f'https://tom76npq59-dsn.algolia.net/1/indexes/PROD_Projects/query?x-algolia-api-key=318055435c6b9c9bdb6fefe330216299&x-algolia-application-id=TOM76NPQ59&x-algolia-agent=Algolia%20for%20jQuery%203.10.2', data=json.dumps(dataque))
                    project = res.json()
                    if len(project['hits']) > 0:
                        condo_id = str(project['hits'][0]['objectID'])
                        pro_name = ''
                        lat = str(project['hits'][0]['lat'])
                        lng = str(project['hits'][0]['lng'])
                    else:
                        condo_id = ''
                        pro_name = str(postdata['web_project_name'])
                        lat = str(postdata['geo_latitude'])
                        lng = str(postdata['geo_longitude'])
                else:
                    condo_id = ''
                    pro_name = str(postdata['web_project_name'])
                    lat = str(postdata['geo_latitude'])
                    lng = str(postdata['geo_longitude']) 

                #print('abcde')
                data = {
                    'utf8': '',
                    '_method': 'put',
                    'authenticity_token': '',
                    'ga_client_id': '',
                    'listing[added_manually]': 'false',
                    'listing[token]': req_post_id,
                    'listing[rank]': '',
                    'listing[is_active]': 'true',
                    'listing[never_expires]': 'true',
                    'listing[property_type]': str(getProdId[str(postdata['property_type'])]),
                    'listing[reference_number]': '',
                    'listing[title_deed]': 'free',
                    'listing[major_region_id]': province_id,
                    'listing[region_id]': amphur_id,
                    'listing[place_id]': tumbon_id,
                    'listing[project_name]': pro_name,
                    'listing[condo_id]': condo_id,
                    'listing[street_number]': '-',
                    'listing[street_name]': str(postdata['addr_road']),
                    'listing[street_postcode]': '-',
                    'listing[location_string]': lat +','+lng,
                    'listing[rooms_number]': '',
                    'listing[internal_area_sqm]': str(postdata['floor_area']),
                    'listing[plot_area][units]': 'thai',
                    'listing[plot_area][value]': '',
                    'listing[plot_area][rai]': str(postdata['land_size_rai']),
                    'listing[plot_area][ngaan]': str(postdata['land_size_ngan']),
                    'listing[plot_area][sqwa]': str(postdata['land_size_wa']),
                    'listing[bedrooms]': str(postdata['bed_room']),
                    'listing[bathrooms]': str(postdata['bath_room']),
                    'listing[floor]': str(postdata['floor_total']),
                    'listing[building_floors]': str(postdata['floor_level']),
                    'listing[furnishing]': 'partial',
                    'listing[facing_direction]': str(postdata['direction_type']),
                    'listing[parking_spaces]': '1',
                    'listing[special_features][duplex]': '0',
                    'listing[special_features][penthouse]': '0',
                    'listing[special_features][renovated]': '0',
                    'listing[special_features][original_condition]': '0',
                    'listing[special_features][corner_unit]': '0',
                    'listing[special_features][ground_floor]': '0',
                    'listing[special_features][green_view]': '0',
                    'listing[special_features][city_view]': '0',
                    'listing[special_features][sea_view]': '0',
                    'listing[special_features][pool_view]': '0',
                    'listing[special_features][mountain_view]': '0',
                    'listing[special_features][river_view]': '0',
                    'listing[special_features][lake_view]': '0',
                    'listing[special_features][pets_allowed]': '0',
                    'listing[special_features][small_pets_allowed]': '0',
                    'listing[private_amenities][air_con]': '0',
                    'listing[private_amenities][bathtub]': '0',
                    'listing[private_amenities][jacuzzi]': '0',
                    'listing[private_amenities][private_pool]': '0',
                    'listing[private_amenities][private_garden]': '0',
                    'listing[private_amenities][intercom]': '0',
                    'listing[private_amenities][water_heater]': '0',
                    'listing[private_amenities][builtin_kitchen]': '0',
                    'listing[private_amenities][cooker_hob]': '0',
                    'listing[private_amenities][builtin_wardrobe]': '0',
                    'listing[private_amenities][walkin_wardrobe]': '0',
                    'listing[private_amenities][maids_room]': '0',
                    'listing[private_amenities][study_room]': '0',
                    'listing[private_amenities][balcony]': '0',
                    'listing[private_amenities][patio]': '0',
                    'listing[private_amenities][terrace]': '0',
                    'listing[private_amenities][roof_terrace]': '0',
                    'listing[private_amenities][garage]': '0',
                    'listing[common_facilities][elevator]': '0',
                    'listing[common_facilities][security]': '0',
                    'listing[common_facilities][cctv]': '0',
                    'listing[common_facilities][parking]': '0',
                    'listing[common_facilities][open_parking]': '0',
                    'listing[common_facilities][basement_parking]': '0',
                    'listing[common_facilities][covered_parking]': '0',
                    'listing[common_facilities][pool]': '0',
                    'listing[common_facilities][sauna]': '0',
                    'listing[common_facilities][jacuzzi]': '0',
                    'listing[common_facilities][gym]': '0',
                    'listing[common_facilities][garden]': '0',
                    'listing[common_facilities][playground]': '0',
                    'listing[common_facilities][shop]': '0',
                    'listing[common_facilities][restaurant]': '0',
                    'listing[common_facilities][wifi]': '0',
                    'listing[common_facilities][clubhouse]': '0',
                    'listing[common_facilities][lounge]': '0',
                    'listing[common_facilities][basketball]': '0',
                    'listing[common_facilities][billiard]': '0',
                    'listing[common_facilities][mini_golf]': '0',
                    'listing[common_facilities][putting_green]': '0',
                    'listing[common_facilities][driving_range]': '0',
                    'listing[common_facilities][tennis]': '0',
                    'listing[common_facilities][squash]': '0',
                    'listing[common_facilities][badminton]': '0',
                    'listing[common_facilities][laundry]': '0',
                    'listing[common_facilities][library]': '0',
                    'listing[common_facilities][function_room]': '0',
                    'listing[common_facilities][karaoke]': '0',
                    'listing[description]': str(postdata['post_description_th']),
                    'listing[name]': str(postdata['name']),
                    'listing[phone]': str(postdata['mobile']),
                    'listing[email]': str(postdata['user']),
                    'commit': 'record'
                }


                if(str(postdata['bed_room']) == "" or str(postdata['bed_room']) == "null" or 'bed_room' not in postdata or str(postdata['bed_room']) == None):
                    data['listing[bedrooms]'] == '0'

                else:
                    data['listing[bedrooms]'] == str(postdata['bed_room'])

                if(str(postdata['bath_room']) == "" or str(postdata['bath_room']) == "null" or 'bath_room' not in postdata or str(postdata['bath_room']) == None):
                    data['listing[bathrooms]'] == '1'

                else:
                    data['listing[bathrooms]'] == str(postdata['bath_room'])

                if 'watermark เจ้าพระยา' in str(postdata['web_project_name']):
                
                    data['listing[project_name]'] = 'วอร์เตอร์มาร์ค เจ้าพระยา'
                    data['listing[condo_id]'] = '5119af8eef23779a61000713'

                ''''listing[photos_attributes][0][id]': '5f060bfaa12eda320d00eae5',
                    'listing[photos_attributes][0][order]': '1',
                    'listing[photos_attributes][0][_destroy]': '1',
                    'listing[photos_attributes][1][id]': '5f060bfaa12eda320d00eae7',
                    'listing[photos_attributes][1][order]': '2',
                    'listing[photos_attributes][1][_destroy]': '1',
                    'listing[photos_attributes][2][id]': '5f060bfaa12eda320d00eae8',
                    'listing[photos_attributes][2][order]': '3',
                    'listing[photos_attributes][2][_destroy]': '1',
                    'listing[photos_attributes][3][id]': '5f0db827a12eda389d0061a2',
                    'listing[photos_attributes][3][order]': '4',
                    'listing[photos_attributes][3][_destroy]': '1',
                    'listing[photos_attributes][4][id]': '5f0de90ba12eda37d3007800',
                    'listing[photos_attributes][4][order]': '5',
                    'listing[photos_attributes][4][_destroy]': '1',
                    'listing[photos_attributes][5][id]': '5f0dea28a12eda38fa005364',
                    'listing[photos_attributes][5][order]': '6',
                    'listing[photos_attributes][5][_destroy]': '1','''


                response = scraper.get(str('https://www.hipflat.co.th/listings/'+req_post_id+'/edit'), headers = headers)

                soup = BeautifulSoup(response.content, features = "html.parser")

                data['utf8'] = str(soup.find('input', attrs = {'name': 'utf8'})['value'])

                data['authenticity_token'] = str(soup.find('input', attrs = {'name': 'authenticity_token'})['value'])

                data['listing[rank]'] = str(soup.find('input', attrs = {'name': 'listing[rank]'})['value'])

                pho = soup.find('div', attrs = {'class': 'photo-upload__photos'})
                #print('prev')

                for pqr in pho.find_all('input'):
                    if('_destroy' in str(pqr['name'])):
                        data[str(pqr['name'])] = '1'

                    else:
                        data[str(pqr['name'])] = str(pqr['value'])

                if postdata['listing_type'] == 'เช่า':
                    data['listing[rent_availability_status]'] = 'true'
                    data['listing[rent_price]'] = str(postdata['price_baht'])
                else:
                    data['listing[sale_availability_status]'] = 'true'
                    data['listing[sale_price]'] = str(postdata['price_baht'])

                r = scraper.post(str('https://www.hipflat.co.th/listings/'+req_post_id+'/update'), data = data, headers = headers)

                success = "true"
                detail = "Post edited successfully"

                if 'post_images' in postdata and len(postdata['post_images']) > 0:
                    self.upload_file(postdata,req_post_id)
            else:
                success = "false"
                detail = "post_id is incorrect"
        else :
            success = "false"
            detail = "Login failed"
        print('complete hipflat')
        end_time = datetime.datetime.utcnow()
        
        return {
            "websitename": "hipflat",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(end_time - start_time),
            "detail": detail,
            "ds_id" : str(postdata['ds_id']),
            "post_id": str(postdata['post_id']),
            "log_id": postdata['log_id']
        }

    def delete_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()
        
        scraper = cloudscraper.create_scraper()
        success = 'false'
        detail = ''
        data = {
            'utf8': '',
            'authenticity_token': '',
            'user[email]': str(postdata['user']),
            'user[password]': str(postdata['pass']),
            'user[remember_me]': '0',
            'commit': 'ลงชื่อเข้าใช้'
        }
        headers = {
            'user_agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36'
        }
        try:
            response = scraper.get('https://www.hipflat.co.th/login', headers = headers)
            soup = BeautifulSoup(response.content, features = "html.parser")
            try:
                data['utf8'] = str(soup.find('input', attrs = {'name': 'utf8'})['value'])
            except:
                post_data = {
                    '_method':'delete',
                    'authenticity_token': soup.find("meta",{"name":"csrf-token"})['content']
                }
                scraper.post('https://www.hipflat.co.th/logout', data=post_data)
                response = scraper.get('https://www.hipflat.co.th/login', headers = headers)
                soup = BeautifulSoup(response.content, features = "html.parser")
                data['utf8'] = str(soup.find('input', attrs = {'name': 'utf8'})['value'])
            data['authenticity_token'] = str(soup.find('input', attrs = {'name': 'authenticity_token'})['value'])
            response = scraper.post('https://www.hipflat.co.th/login', data = data, headers = headers)
            if response.url == 'https://www.hipflat.co.th/login':
                success = "false"
                detail = 'Incorrect Username or Password !!'
            else:
                success = "true"
                detail = 'Logged in successfully'
        except:
            detail = "Network Problem occured"
        
        headers = {
            'user_agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36'
        }
        
        if success == "true":
            req_post_id = str(postdata['post_id'])
            """found = False
            page = 1
            while True:
                res = scraper.get("https://www.hipflat.co.th/account/listings/pro/page/"+str(page), headers = headers).text
                soup = BeautifulSoup(res, features = self.parser)
                count = 0
                for i in soup.find_all('a'):
                    if i.get('href') and i.get('href').find('/edit') != -1:
                        link = i.get('href').split('/')
                        count += 1
                        # print(link)
                        if len(link)>2 and link[2]==req_post_id:
                            found = True
                            break
                page += 1
                if found or count==0:
                    break"""

            try:

                '''if province_id == '0':
                    province_id = '5599801770726f1f36000019'

                if amphur_id == '0':
                    amphur_id = '5599801870726f1f36000058'

                if tumbon_id == '0':
                    tumbon_id = '5599801f70726f1f36000b5e'''

                data = {
                    'utf8': '',
                    '_method': 'put',
                    'authenticity_token': '',
                    'ga_client_id': '',
                    'listing[added_manually]': 'false',
                    'listing[token]': req_post_id,
                    'listing[rank]': '',
                    'listing[is_active]': 'true',
                    'listing[never_expires]': 'true',
                    'listing[property_type]': 'condo',
                    'listing[reference_number]': '',
                    'listing[title_deed]': 'free',
                    'listing[major_region_id]': '0',
                    'listing[region_id]': '0',
                    'listing[place_id]': '0',
                    'listing[project_name]': '-',
                    'listing[condo_id]': '',
                    'listing[street_number]': '-',
                    'listing[street_name]': '-',
                    'listing[street_postcode]': '-',
                    'listing[location_string]': '',
                    'listing[rooms_number]': '',
                    'listing[internal_area_sqm]': '0.0',
                    'listing[plot_area][units]': 'thai',
                    'listing[plot_area][value]': '0.0',
                    'listing[plot_area][rai]': '0.0',
                    'listing[plot_area][ngaan]': '0.0',
                    'listing[plot_area][sqwa]': '0.0',
                    'listing[bedrooms]': '1',
                    'listing[bathrooms]': '1',
                    'listing[floor]': '1',
                    'listing[building_floors]': '1',
                    'listing[furnishing]': 'none',
                    'listing[facing_direction]': 'e',
                    'listing[parking_spaces]': '0',
                    'listing[special_features][duplex]': '0',
                    'listing[special_features][penthouse]': '0',
                    'listing[special_features][renovated]': '0',
                    'listing[special_features][original_condition]': '0',
                    'listing[special_features][corner_unit]': '0',
                    'listing[special_features][ground_floor]': '0',
                    'listing[special_features][green_view]': '0',
                    'listing[special_features][city_view]': '0',
                    'listing[special_features][sea_view]': '0',
                    'listing[special_features][pool_view]': '0',
                    'listing[special_features][mountain_view]': '0',
                    'listing[special_features][river_view]': '0',
                    'listing[special_features][lake_view]': '0',
                    'listing[special_features][pets_allowed]': '0',
                    'listing[special_features][small_pets_allowed]': '0',
                    'listing[private_amenities][air_con]': '0',
                    'listing[private_amenities][bathtub]': '0',
                    'listing[private_amenities][jacuzzi]': '0',
                    'listing[private_amenities][private_pool]': '0',
                    'listing[private_amenities][private_garden]': '0',
                    'listing[private_amenities][intercom]': '0',
                    'listing[private_amenities][water_heater]': '0',
                    'listing[private_amenities][builtin_kitchen]': '0',
                    'listing[private_amenities][cooker_hob]': '0',
                    'listing[private_amenities][builtin_wardrobe]': '0',
                    'listing[private_amenities][walkin_wardrobe]': '0',
                    'listing[private_amenities][maids_room]': '0',
                    'listing[private_amenities][study_room]': '0',
                    'listing[private_amenities][balcony]': '0',
                    'listing[private_amenities][patio]': '0',
                    'listing[private_amenities][terrace]': '0',
                    'listing[private_amenities][roof_terrace]': '0',
                    'listing[private_amenities][garage]': '0',
                    'listing[common_facilities][elevator]': '0',
                    'listing[common_facilities][security]': '0',
                    'listing[common_facilities][cctv]': '0',
                    'listing[common_facilities][parking]': '0',
                    'listing[common_facilities][open_parking]': '0',
                    'listing[common_facilities][basement_parking]': '0',
                    'listing[common_facilities][covered_parking]': '0',
                    'listing[common_facilities][pool]': '0',
                    'listing[common_facilities][sauna]': '0',
                    'listing[common_facilities][jacuzzi]': '0',
                    'listing[common_facilities][gym]': '0',
                    'listing[common_facilities][garden]': '0',
                    'listing[common_facilities][playground]': '0',
                    'listing[common_facilities][shop]': '0',
                    'listing[common_facilities][restaurant]': '0',
                    'listing[common_facilities][wifi]': '0',
                    'listing[common_facilities][clubhouse]': '0',
                    'listing[common_facilities][lounge]': '0',
                    'listing[common_facilities][basketball]': '0',
                    'listing[common_facilities][billiard]': '0',
                    'listing[common_facilities][mini_golf]': '0',
                    'listing[common_facilities][putting_green]': '0',
                    'listing[common_facilities][driving_range]': '0',
                    'listing[common_facilities][tennis]': '0',
                    'listing[common_facilities][squash]': '0',
                    'listing[common_facilities][badminton]': '0',
                    'listing[common_facilities][laundry]': '0',
                    'listing[common_facilities][library]': '0',
                    'listing[common_facilities][function_room]': '0',
                    'listing[common_facilities][karaoke]': '0',
                    'listing[description]': '-',
                    'listing[name]': '-',
                    'listing[phone]': '-',
                    'listing[email]': '-',
                    'commit': 'record'
                }

                response = scraper.get(str('https://www.hipflat.co.th/listings/'+req_post_id+'/edit'), headers = headers)

                soup = BeautifulSoup(response.content, features = "html.parser")

                data['utf8'] = str(soup.find('input', attrs = {'name': 'utf8'})['value'])

                data['authenticity_token'] = str(soup.find('input', attrs = {'name': 'authenticity_token'})['value'])

                data['listing[rank]'] = str(soup.find('input', attrs = {'name': 'listing[rank]'})['value'])

                pho = soup.find('div', attrs = {'class': 'photo-upload__photos'})
                #print('prev')

                for pqr in pho.find_all('input'):
                    if('_destroy' in str(pqr['name'])):
                        data[str(pqr['name'])] = '1'

                    else:
                        data[str(pqr['name'])] = str(pqr['value'])

                    #print(data[str(pqr['name'])])


                r = scraper.post(str('https://www.hipflat.co.th/listings/'+req_post_id+'/update'), data = data, headers = headers)

                #print(r.url)
                #print(r.text)

                success = "true"
                detail = "Post deleted successfully"


            except:
                success = "false"
                detail = "post_id is incorrect"


        else :
            success = "false"
            detail = "Login failed"

        end_time = datetime.datetime.utcnow()
        
        return {
            "websitename": "hipflat",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(end_time - start_time),
            "detail": detail,
            "ds_id" : str(postdata['ds_id']),
            "post_id": str(postdata['post_id']),
            "log_id": postdata['log_id']
        }








    def boost_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()
        
        scraper = cloudscraper.create_scraper()
        success = 'false'
        detail = ''
        data = {
            'utf8': '',
            'authenticity_token': '',
            'user[email]': str(postdata['user']),
            'user[password]': str(postdata['pass']),
            'user[remember_me]': '0',
            'commit': 'ลงชื่อเข้าใช้'
        }
        headers = {
            'user_agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36'
        }
        try:
            response = scraper.get('https://www.hipflat.co.th/login', headers = headers)
            soup = BeautifulSoup(response.content, features = "html.parser")
            try:
                data['utf8'] = str(soup.find('input', attrs = {'name': 'utf8'})['value'])
            except:
                post_data = {
                    '_method':'delete',
                    'authenticity_token': soup.find("meta",{"name":"csrf-token"})['content']
                }
                scraper.post('https://www.hipflat.co.th/logout', data=post_data)
                response = scraper.get('https://www.hipflat.co.th/login', headers = headers)
                soup = BeautifulSoup(response.content, features = "html.parser")
                data['utf8'] = str(soup.find('input', attrs = {'name': 'utf8'})['value'])
            data['authenticity_token'] = str(soup.find('input', attrs = {'name': 'authenticity_token'})['value'])
            response = scraper.post('https://www.hipflat.co.th/login', data = data, headers = headers)
            if response.url == 'https://www.hipflat.co.th/login':
                success = "false"
                detail = 'Incorrect Username or Password !!'
            else:
                success = "true"
                detail = 'Logged in successfully'
        except:
            detail = "Network Problem occured"
        
        if success == "true":
            req_post_id = str(postdata['post_id'])
            found = False
            page = 1
            while True:
                res = scraper.get("https://www.hipflat.co.th/account/listings/pro/page/"+str(page), headers = headers).text
                soup = BeautifulSoup(res, features = self.parser)
                count = 0
                for i in soup.find_all('a'):
                    if i.get('href') and i.get('href').find('/edit') != -1:
                        link = i.get('href').split('/')
                        count += 1
                        # print(link)
                        if len(link)>2 and link[2]==req_post_id:
                            found = True
                            break
                page += 1
                if found or count==0:
                    break

            print(found)
            try:
                data = {
                    'utf8': '',
                    '_method': 'put',
                    'authenticity_token': '',
                    'ga_client_id': '',
                    'listing[added_manually]': 'false',
                    'listing[token]': req_post_id,
                    'listing[rank]': '',
                    'listing[is_active]': 'true',
                    'listing[never_expires]': 'true',
                    'commit': 'Save'
                }


                response = scraper.get(str('https://www.hipflat.co.th/listings/'+req_post_id+'/edit'), headers = headers)

                soup = BeautifulSoup(response.content, features = "html.parser")

                data['utf8'] = str(soup.find('input', attrs = {'name': 'utf8'})['value'])

                data['authenticity_token'] = str(soup.find('input', attrs = {'name': 'authenticity_token'})['value'])

                data['listing[rank]'] = str(soup.find('input', attrs = {'name': 'listing[rank]'})['value'])

                r = scraper.post(str('https://www.hipflat.co.th/listings/'+req_post_id+'/update'), data = data, headers = headers)

                #print(r.url)
                #print(r.text)

                success = "true"
                detail = "Post boosted successfully"

            except:
                success = "false"
                detail = "post_id is incorrect"



        else :
            success = "false"
            detail = "Login failed"

        end_time = datetime.datetime.utcnow()
        
        return {
            "websitename": "hipflat",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(end_time - start_time),
            "detail": detail,
            "ds_id" : str(postdata['ds_id']),
            "post_id": str(postdata['post_id']),
            "log_id": postdata['log_id'],
            "post_view": ""
        }







    def search_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        
        start_time = datetime.datetime.utcnow()
        scraper = cloudscraper.create_scraper()
        headers = {
            'user_agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36'
        }

        login = self.test_login(postdata)
        
        if (login['success'] == 'true'):

            post_found = "false"
            post_id = ''
            post_url = ''
            post_view = ''
            post_create_time = ''
            post_modify_time = ''
            detail = 'No post with this title'

            url = 'https://www.hipflat.co.th/account/listings/pro'
            posts = scraper.get('https://www.hipflat.co.th/account/listings/free', headers = headers).text
            soup = BeautifulSoup(posts, features = "html.parser")
            pages = [p['href'] for p in soup.find_all('a', attrs={'data-remote': 'true'})]
            try:
                max_pages = int(pages[-1].split('/')[-1])
            except:
                max_pages = 1

            #  single page start
            for i in range(1,max_pages+1):
                if detail == 'Post found':
                    break
                # print(f'page--{i}')
                all_posts_url = 'https://www.hipflat.co.th/account/listings/free/page/' + str(i)
                all_posts = scraper.get(all_posts_url, headers = headers).text
                soup = BeautifulSoup(all_posts, features = "html.parser")
                req_post_title = str(postdata['post_title_th'])
                aaas = []
                for i in soup.find_all('a'):
                    try:
                        if i['href'].find('/edit') != -1:

                            #print(link)
                            link = i['href'].replace('/listings/','')
                            post_ids = str(link.replace('/edit',''))
                            aaas.append(post_ids)
                    except:
                        continue



                temp = 0

                for qwe in soup.find_all('div', attrs = {'class': 'user-listing__title'}):
                    t = str(qwe.text.replace('\n',' ')).strip()
                    # print(f"w_title---{t}\np_title---{req_post_title}\n\n\n")
                    if t == req_post_title :
                        #print(temp)
                        print("true")
                        post_id = str(aaas[temp])

                        post_url = str('https://www.hipflat.co.th/listing-preview/'+str(post_id))

                        post_found = "true"
                        post_view = 'Post views not on site'
                        post_create_time = 'Post create time not on site'
                        post_modify_time = 'Post modify time not on site'
                        detail = 'Post found'

                        break

                    temp = temp + 1

            #  single page ends



        else :
            detail = 'Can not log in'
        
        end_time = datetime.datetime.utcnow()
        
        return {
            "websitename": "hipflat",
            "success": login['success'],
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(end_time - start_time),
            "detail": detail,
            "account_type":'null',
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "post_url": post_url,
            "post_modify_time": post_modify_time,
            "post_create_time": post_create_time,
            "post_view": post_view,
            "post_found": post_found
        }





    def print_debug(self, msg):
        if(self.debug == 1):
            print(msg)
        return True

    def print_debug_data(self, data):
        if(self.debugdata == 1):
            print(data)
        return True