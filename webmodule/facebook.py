from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
from time import sleep
import os
import json
from bs4 import BeautifulSoup

class facebook():

    def __init__(self): #For constructor when make an instance
        self.websitename = 'facebook' #Fix websitename for retruning value

    def test_login(self, postdata): #Main log in method

        #Set up web browser
        options = Options() #Create and options for chromedriver
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-infobars')
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1024,768")
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome('./static/chromedriver', chrome_options=options) #Start chrome driver

        time_start = datetime.utcnow()  #Set start time

        try:
            self.driver.get('https://www.facebook.com/login')   #Get facebook nlogin url
            success = 'true'    #If url is valid, return true
        except:
            success = 'false'   #If url is invalid, return false
            detail = 'Can not reach the page. ' #Make a detail
            pass

        #Start log in method
        if success == 'true':   #If url is valid, continue to check element and send key
            try:
                email = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, 'email')))    #Check email element and send key
                email.send_keys('pum705@gmail.com') #pum705@gmail.com
                password = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, 'pass')))  #Check password element and send key
                password.send_keys('PumPum456@2020') #PumPum456@2020
                login = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login'))).click() #Check log in button and click
                success = 'true'    #If all done then return success
                detail = 'Log in success'
            except WebDriverException as e:
                success = 'false'   #If error return flase
                detail = 'Can not find element.'
                pass

            sleep(1)

        if postdata['action'] == 'test_login':
            self.driver.close()
            self.driver.quit()

        time_end = datetime.utcnow()
        time_usage = time_end-time_start

        return{
            "success": success,
            "usage_time": str(time_usage),
            'ds_id': postdata['ds_id'],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": postdata['ds_name'],
            "ds_id": postdata['ds_id']
        }

    def postdata_handle(self, postdata):
        
        datahandled = {}
        try:
            datahandled['post_title_th'] = postdata['post_title_th']
        except KeyError as e:
            datahandled['post_title_th'] = ''

        try:
            datahandled['property_type'] = postdata['property_type']
        except KeyError as e:
            datahandled['property_type'] = '30'
        prop_type = {
            '1' : 'คอนโด',
            '2' : 'บ้านเดี่ยว',
            '3' : 'บ้านแฝด',
            '4' : 'ทาวน์เฮ้าส์',
            '5' : 'ตึกแถว-อาคารพาณิชย์',
            '6' : 'ที่ดิน',
            '7' : 'อพาร์ทเมนท์',
            '8' : 'โรงแรม',
            '9' : 'ออฟฟิศสำนักงาน',
            '10' : 'โกดัง',
            '25' : 'โรงงาน',
            '30' : 'อสังหาริมทรัพย์'
        }
        datahandled['property_type'] = prop_type[str(datahandled['property_type'])]

        try:
            datahandled['listing_type'] = postdata['listing_type']
        except KeyError as e:
            datahandled['listing_type'] = ''

        try:
            datahandled['price_baht'] = postdata['price_baht']
        except KeyError as e:
            datahandled['price_baht'] = ''
        
        try:
            datahandled['floor_level'] = postdata['floor_level']
        except KeyError as e:
            datahandled['floor_level'] = ''

        try:
            datahandled['floor_area'] = postdata['floor_area']
        except KeyError as e:
            datahandled['floor_area'] = ''

        try:
            datahandled['bed_room'] = postdata['bed_room']
        except KeyError as e:
            datahandled['bed_room'] = ''

        try:
            datahandled['bath_room'] = postdata['bath_room']
        except KeyError as e:
            datahandled['bath_room'] = ''

        try:
            datahandled['project_name'] = postdata['project_name']
        except KeyError as e:
            datahandled['project_name'] = ''

        try:
            datahandled['post_description_th'] = postdata['post_description_th']
        except KeyError as e:
            datahandled['post_description_th'] = ''

        try:
            datahandled['addr_province'] = postdata['addr_province']
        except KeyError as e:
            datahandled['addr_province'] = 'กรุงเทพมหานคร'

        try:
            datahandled['name'] = postdata['name']
        except KeyError as e:
            datahandled['name'] = ''

        try:
            datahandled['mobile'] = postdata['mobile']
        except KeyError as e:
            datahandled['mobile'] = ''

        try:
            datahandled['line'] = postdata['line']
        except KeyError as e:
            datahandled['line'] = ''

        return datahandled
    
    def create_post(self, postdata):
        
        time_start = datetime.utcnow()

        datahandled = self.postdata_handle(postdata)
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]

        with open('./static/facebook_element.json', encoding="utf8") as e:
            element = json.load(e)

        with open('./static/facebook_group.json', 'r', encoding="utf8") as g:
            group = json.load(g)

        prop_type = {
            'คอนโด' : '0',
            'บ้าน' : '1',
            'ที่ดิน'  : '2'   
        }
        list_type = {
            'ขาย' : '0',
            'เช่า' : '1'
        }
        prov = {
            'ทั่วไทย' : '0',
            'กรุงเทพ' : '1'
        }

        #Data arragement
        if datahandled['property_type'] == 'บ้านเดี่ยว' or datahandled['property_type'] == 'บ้านแฝด' or datahandled['property_type'] == 'ทาวน์เฮ้าส์' or datahandled['property_type'] == 'ตึกแถว-อาคารพาณิชย์' or datahandled['property_type'] == 'ออฟฟิศสำนักงาน':
            datahandled['property_type'] = 'บ้าน'
        elif datahandled['property_type'] == 'ที่ดิน' or datahandled['property_type'] == 'โกดัง' or datahandled['property_type'] == 'โรงงาน':
            datahandled['property_type'] = 'ที่ดิน'
        else:
            datahandled['property_type'] = 'คอนโด'

        if datahandled['addr_province'] not in  prov.keys():
            datahandled['addr_province'] = 'ทั่วไทย'


        list_group = group['group'][int(prop_type[datahandled['property_type']])][datahandled['property_type']][int(list_type[datahandled['listing_type']])][datahandled['listing_type']] \
                        [int(prov[datahandled['addr_province']])][datahandled['addr_province']]


        if len(datahandled['post_title_th']) >= 99:
            datahandled['post_title_th'] = datahandled['post_title_th'][:99]
        
        if '\t' in datahandled['post_description_th']:
            datahandled['post_description_th'] = datahandled['post_description_th'].replace('\t', '\n')

        try:
            if success == 'true':
                self.driver.get('https://www.facebook.com/marketplace/create/item')
                sleep(3)
                pic_post = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, element['pic_post_input'])))

                all_images = ""
                for count, pic in enumerate(postdata['post_images'][:10]):
                    if count < len(postdata['post_images'])-1:
                        all_images += os.path.abspath(pic) + '\n'
                    else:
                        all_images += os.path.abspath(pic)
                pic_post.send_keys(all_images)

                owner_name = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, element['owner_name'])))                                                                                
                ActionChains(self.driver).move_to_element(owner_name).click().send_keys(Keys.DOWN).send_keys(Keys.DOWN).send_keys(Keys.DOWN).send_keys(Keys.DOWN).send_keys(Keys.DOWN).send_keys(Keys.DOWN).send_keys(Keys.DOWN).perform()

                title = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['title'])))
                title.send_keys(datahandled['post_title_th'])

                price = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['price'])))
                price.send_keys(datahandled['price_baht'])

                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['type_btn']))).click()
                sleep(1)
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['sel_type']))).click()

                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div/div/div[6]/div/div/div/label'))).click()
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]'))).click()

                detail = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['detail']))).send_keys(datahandled['post_description_th'])

                location = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['location'])))
                location.send_keys(Keys.CONTROL + 'a')
                if datahandled['addr_province'] == 'ทั่วไทย':
                    location.send_keys('กรุงเทพมหานคร')
                else:
                    location.send_keys('กรุงเทพมหานคร')
                sleep(1)
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['sel_location']))).click()

                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['next']))).click()

                try:
                    for i in range(1, 46):
                        try:
                            check_other = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div/div/div[4]/div[3]/div[{i}]/div/div[1]/div[2]/div[1]/div/div/div[1]/span/span/span'))).text
                        except:
                            check_other = ''
                            pass
                        if check_other in list_group.keys():
                            ch_group = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div/div/div[4]/div[3]/div[{i}]/div'))).click()
                except:
                    pass

                self.driver.save_screenshot('debug_response/save_screen.png')

                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[1]/div/div[5]/div/div'))).click()
                
                sleep(3)

                post = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div[3]/div[2]/div[2]/div/div[2]/div/div[1]/div/div[2]/div/div[1]/span/span'))).click()
                
                sleep(3)

                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                anchor = soup.find_all('a')
                for item in anchor:
                    if item.get('aria-label') == 'แก้ไขรายการสินค้า':
                        item_url = item['href']
                
                url = item_url.split('=')[-1]

                post_url = 'https://www.facebook.com/marketplace/item/' + url
                post_id = url
                succcess = 'true'
                detail = 'Success create item in marketplace'

        except Exception as e:
            success = 'false'
            detail = 'Can not create post in market place.' + str(e)
            post_url = ''
            post_id = ''    

        finally:
            self.driver.close()
            self.driver.quit()
        
        time_end = datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": postdata['ds_id'],
            "post_url" : post_url,
            "post_id" : post_id,
            "account_type": "null",
            "detail": detail,
            "websitename": self.websitename
        }

    def edit_post(self, postdata):

        time_start = datetime.utcnow()

        datahandled = self.postdata_handle(postdata)
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]

        with open('./static/facebook_element.json', 'r', encoding="utf8") as e:
            element = json.load(e)

        with open('./static/facebook_group.json', 'r', encoding="utf8") as g:
            group = json.load(g)

        prop_type = {
            'คอนโด' : '0',
            'บ้าน' : '1',
            'ที่ดิน'  : '2'   
        }
        list_type = {
            'ขาย' : '0',
            'เช่า' : '1'
        }
        prov = {
            'ทั่วไทย' : '0',
            'กรุงเทพ' : '1'
        }

        #Data arragement
        if datahandled['property_type'] == 'บ้านเดี่ยว' or datahandled['property_type'] == 'บ้านแฝด' or datahandled['property_type'] == 'ทาวน์เฮ้าส์' or datahandled['property_type'] == 'ตึกแถว-อาคารพาณิชย์' or datahandled['property_type'] == 'ออฟฟิศสำนักงาน':
            datahandled['property_type'] = 'บ้าน'
        elif datahandled['property_type'] == 'ที่ดิน' or datahandled['property_type'] == 'โกดัง' or datahandled['property_type'] == 'โรงงาน':
            datahandled['property_type'] = 'ที่ดิน'
        else:
            datahandled['property_type'] = 'คอนโด'

        if datahandled['addr_province'] not in  prov.keys():
            datahandled['addr_province'] = 'ทั่วไทย'
        
        list_group = group['group'][int(prop_type[datahandled['property_type']])][datahandled['property_type']][int(list_type[datahandled['listing_type']])][datahandled['listing_type']] \
                        [int(prov[datahandled['addr_province']])][datahandled['addr_province']]

        if len(datahandled['post_title_th']) >= 99:
            datahandled['post_title_th'] = datahandled['post_title_th'][:99]

        if '\t' in datahandled['post_description_th']:
            datahandled['post_description_th'] = datahandled['post_description_th'].replace('\t', '\n')

        try:
            if success == 'true':
                self.driver.get('https://www.facebook.com/marketplace/edit/?listing_id=' + postdata['post_id'])
                count_img = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['count_img']))).text
                images = count_img.split('/')[0]
                print(repr(images.strip()[-1]))
                for img in range(0, int(images.strip()[-1])):
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['del_img']))).click()
                    sleep(0.5)

                pic_post = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, element['pic_post_input'])))

                all_images = ""
                for count, pic in enumerate(postdata['post_images'][:10]):
                    if count < len(postdata['post_images'])-1:
                        all_images += os.path.abspath(pic) + '\n'
                    else:
                        all_images += os.path.abspath(pic)
                pic_post.send_keys(all_images)

                owner_name = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, element['owner_name'])))                                                                                
                ActionChains(self.driver).move_to_element(owner_name).click().send_keys(Keys.DOWN).send_keys(Keys.DOWN).send_keys(Keys.DOWN).send_keys(Keys.DOWN).send_keys(Keys.DOWN).perform()

                title = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['title'])))
                title.send_keys(Keys.CONTROL + 'a')
                title.send_keys(datahandled['post_title_th'])

                price = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['price'])))
                price.send_keys(Keys.CONTROL + 'a')
                price.send_keys(datahandled['price_baht'])

                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['type_btn']))).click()
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['sel_type']))).click()

                detail = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['detail'])))
                detail.send_keys(Keys.CONTROL + 'a')
                detail.send_keys(datahandled['post_description_th'])

                location = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['location'])))
                location.send_keys(Keys.CONTROL + 'a')
                if datahandled['addr_province'] == 'ทั่วไทย':
                    location.send_keys(postdata['addr_province'])
                else:
                    location.send_keys('กรุงเทพมหานคร')
                sleep(1)
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['sel_location']))).click()

                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['next']))).click()
        
        except:
            success = 'false'
            detail = 'Can not edit post. You can edit post after your post are approved.'

        finally:
            self.driver.close()
            self.driver.quit()

        time_end = datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_id": postdata['post_id'],
            "log_id": postdata['log_id'],
            "account_type": "null",
            "detail": detail,
            "websitename": self.websitename,
            "ds_id": postdata['ds_id']
        }

    def delete_post(self, postdata):

        test_login = self.test_login(postdata)
        success = test_login['success']
        detail = test_login['detail']

        time_start = datetime.utcnow()
        try:
            if success == 'true':
                self.driver.get('https://www.facebook.com/marketplace/item/' + postdata['post_id'])

                body = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                ActionChains(self.driver).move_to_element(body).send_keys(Keys.DOWN).send_keys(Keys.DOWN).send_keys(Keys.DOWN).send_keys(Keys.DOWN).send_keys(Keys.DOWN).perform()
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, element['del_item']))).click()
                sleep(2)
                success = 'true'
                detail = 'Delete post successfully'

        except:
            success = 'false'
            detail = 'Can not delete post'

        finally:
            self.driver.close()
            self.driver.quit()

        time_end = datetime.utcnow()
        time_usage = time_end-time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": postdata['post_id'],
            "websitename": self.websitename,
        }


    def boost_post(self, postdata):

        time_start = datetime.utcnow()
        success = 'false'
        detail = 'Facebook can not boost post.'
        time_end = datetime.utcnow()
        time_usage = time_end-time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": postdata['post_id'],
            "websitename": self.websitename,
        }

    
    def search_post(self, postdata):

        time_start = datetime.utcnow()

        datahandled = self.postdata_handle(postdata)
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]

        try:
            if success == 'true':
                try:
                    self.driver.get('https://www.facebook.com/search/posts/?q=' + datahandled['post_title_th'])
                    try:          
                        post_ele = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div/div[1]/div/div/div/div/div/div[3]/a'))).click()
                    except:
                        pass
                    try:
                        text_all = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[2]/div[1]/div[4]/div/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div[3]/div[1]/div/div/div'))).text
                    except:
                        text_all = ' '
                        pass
                    if datahandled['post_title_th'] in text_all:
                        post_url = self.driver.current_url
                        post_id = post_url.split('/')[-1]
                        success = 'true'
                        detail = 'Your post has already been created.'
                        post_found = 'true'
                    else:
                        post_url = 'null'
                        post_id = 'null'
                        success = 'true'
                        detail = "Your post hasn't been create yet."
                        post_found = 'false'
                except:
                    success = 'false'
                    detail = 'Can not search'
                    post_url = 'null'
                    post_id = 'null'
                    post_found = 'false'

        finally:
            self.driver.close()
            self.driver.quit()
        time_end = datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "websitename" : "facebook",
            "success" : success,
            "start_time" : str(time_start),
            "end_time" : str(time_end),
            "usage_time" : str(time_usage),
            "detail" : detail,
            "account_type" : 'null',
            "ds_id" : postdata['ds_id'],
            "log_id" : postdata['log_id'],
            "post_id" : post_id,
            "post_url" : post_url,
            "post_modify_time" : '',
            "post_create_time" : '',
            "post_view" : '',
            "post_found" : post_found
        }