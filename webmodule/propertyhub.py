from selenium import webdriver
from selenium.webdriver.common import action_chains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from time import sleep
import os
from selenium.webdriver.common.action_chains import ActionChains

class propertyhub():


    def __init__ (self):
        self.websitename = 'propertyhub'


    def test_login(self, postdata):
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('start-maximized')
        options.add_argument('disable-infobars')
        options.add_argument('--disable-extensions')
        options.add_argument('disable-gpu')
        options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome('./static/chromedriver', chrome_options=options)

        time_start = datetime.utcnow()

        url = 'https://dashboard.propertyhub.in.th/login'

        self.driver.get(url)
        success = 'true'
        detail = 'Can reach url'

        try:
            user = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'email'))).send_keys(postdata['user'])
            pasword = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'password'))).send_keys(postdata['pass'])
            btn = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'gagEqT'))).click()

            sleep(1.5)

            new_url = self.driver.current_url
            if new_url != url:
                success = 'true'
                detail = 'Log in success'
            else:
                success = 'false'
                detail = 'Your email or password are wrong'
        except:
            success = 'false'
            detail = 'Error when tring to login or can not reach the elements.'

        if postdata['action'] == 'test_login':
            self.driver.close()
            self.driver.quit()

        time_end = datetime.utcnow()
        time_usage = time_end-time_start
        
        return {
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
            datahandled['post_title_th'] = postdata['post_title_th'].replace('\n', ' ')
        except KeyError as e:
            datahandled['post_title_th'] = ''

        try:
            datahandled['post_title_en'] = postdata['post_title_en'].replace('\n', ' ')
        except KeyError as e:
            datahandled['post_title_en'] = ''

        try:
            if postdata['web_project_name'] == '':
                datahandled['project_name'] = postdata['project_name']
            else:
                datahandled['project_name'] = postdata['web_project_name']
        except KeyError as e:
            datahandled['project_name'] = ''

        try:
            datahandled['building'] = postdata['building']
        except KeyError as e:
            datahandled['building'] = ''

        try:
            datahandled['type_room'] = postdata['bed_room']
            if int(datahandled['type_room']) > 5:
                datahandled['type_room'] = '5'
        except KeyError as e:
            datahandled['type_room'] = 'สตูดิโอ'

        try:
            datahandled['floor_level'] = postdata['floor_level']
        except KeyError as e:
            datahandled['floor_level'] = ''

        try:
            datahandled['bed_room'] = postdata['bed_room']
        except KeyError as e:
            datahandled['bed_room'] = ''

        try:
            datahandled['bath_room'] = postdata['bath_room']
        except KeyError as e:
            datahandled['bath_room'] = ''
        
        try:
            datahandled['floor_area'] = postdata['floor_area']
        except KeyError as e:
            datahandled['floor_area'] = ''

        try:
            datahandled['price_baht'] = postdata['price_baht']
        except KeyError as e:
            datahandled['price_baht'] = ''

        try:
            datahandled['post_description_th'] = postdata['post_description_th']
        except KeyError as e:
            datahandled['post_description_th'] = ''

        try:
            datahandled['post_description_en'] = postdata['post_description_en']
        except KeyError as e:
            datahandled['post_description_en'] = ''

        return datahandled

    
    def create_post(self, postdata):
        time_start = datetime.utcnow()

        datahandled = self.postdata_handle(postdata)
        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]

        slt_project = datahandled['project_name'].split(' ')
        try:
            if success == 'true':
                clear_pop = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body'))).send_keys(Keys.ESCAPE)
                sleep(1)
                if postdata['listing_type'] == 'เช่า':
                    check_limit_rent = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sc-1rsvu2b-3')))
                    if int(check_limit_rent[0].text.split('/')[0].replace(',', '')) < int(check_limit_rent[0].text.split('/')[1].replace(',', '')):
                        success = 'true'
                    else:
                        success = 'false'
                        detail = 'You can not post any more cause reaching the limit.'
                if postdata['listing_type'] == 'ขาย':
                    check_limit_sell = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sc-1rsvu2b-3')))
                    if int(check_limit_sell[1].text.split('/')[0].replace(',', '')) < int(check_limit_sell[1].text.split('/')[1].replace(',', '')):
                        success = 'true'
                    else:
                        success = 'false'
                        detail = 'You can not post any more cause reaching the limit.'

            if success == 'true':
                self.driver.get('https://dashboard.propertyhub.in.th/members/listings/new')

                sleep(1)
                clear_pop = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body'))).send_keys(Keys.ESCAPE)
                title_th = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'title.th'))).send_keys(datahandled['post_title_th'])
                title_en = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'title.en'))).send_keys(datahandled['post_title_en'])
                project = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div/div/form/div/div/div[1]/div[4]/div[2]/div/div/input')))
                for word in slt_project:
                    project.send_keys(word+' ')
                    sleep(0.4)
                project.send_keys(Keys.BACKSPACE)
                sleep(0.6)

                try:
                    all_sel_pro = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'i8hizn-0')))
                    all_sel_pro[0].click()
                    """ match = 0
                    for project_sel in all_sel_pro:
                        #print(project_sel.text)
                        print(slt_project)
                        for word in slt_project:
                            #print(word.replace('(', '').replace(')', ''))
                            if word.replace('(', '').replace(')', '') in project_sel.text.split('\n')[0].replace('(', '').replace(')', '').split(' '):
                                print(project_sel.text.split('\n')[0].replace('(', '').replace(')', '').split(' '))
                                print(word.replace('(', '').replace(')', ''))
                                print('Match')
                                match += 1
                        #print(match)
                        if match >= len(project_sel.text.split('\n')[0].replace('(', '').replace(')', '').split(' '))-1:
                            project_sel.click()
                            success = 'true'
                            break
                        else:
                            success = 'false'
                            detail = 'Your project name does not match.' """
                except:
                    success = 'false'
                    detail = 'ไม่สามารถโพสต์ประกาศได้ เนื่องจากไม่เจอโครงการของคุณ'
                    
                """ try:
                    project_sel = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div/form/div/div/div[1]/div[4]/div[2]/div/div/div[2]/div/div/div'))).click()
                    success = 'true'
                    detail = 'Found project'
                except:
                    success = 'false'
                    detail = 'Your project name does not match.' """

                if success == 'true':
                    building = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'roomInformation.building'))).send_keys(datahandled['building'])
                    sel_roomtype =  WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.NAME, 'roomInformation.roomType')))[1].click()
                    sel_type1 = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'item')))
                    for count, value in enumerate(sel_type1):
                        if datahandled['type_room'] in value.text:
                            value.click()
                            break
                    on_floor = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'roomInformation.onFloor'))).send_keys(datahandled['floor_level'])
                    bed_room = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'roomInformation.numberOfBed'))).send_keys(datahandled['bed_room'])
                    bath_room = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'roomInformation.numberOfBath'))).send_keys(datahandled['bath_room'])
                    floor_area = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'roomInformation.roomArea'))).send_keys(datahandled['floor_area'])
                    sel_posttype = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.NAME, 'postType')))[1].click()
                    sel_type2 = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@class="visible menu transition"]')))
                    child_sel_type2 = sel_type2.find_elements_by_tag_name('div')
                    if postdata['listing_type'] == 'ขาย':
                        #print(sel_type2[25].text)
                        child_sel_type2[1].click()
                        sale_price = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'price.forSale.price'))).send_keys(datahandled['price_baht'])
                    elif postdata['listing_type'] == 'เช่า':
                        #print(sel_type2[26].text)
                        child_sel_type2[0].click()
                        rent_price = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'price.forRent.monthly.price'))).send_keys(datahandled['price_baht'])
                        daily_price = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.NAME, 'price.forRent.daily.type')))[2].click()
                        deposit = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.NAME, 'price.forRent.deposit.type')))[2].click()
                        advance = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.NAME, 'price.forRent.advancePayment.type')))[2].click()
                    else:
                        success = 'false'
                        detail = 'Your post type does not match'

                    #if 'เฟอร์นิเจอร์' in datahandled['post_description_th']:
                    sel_funiture = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'amenities.hasFurniture'))).click()
                    if 'เครื่องปรับอากาศ' in datahandled['post_description_th'] or 'แอร์' in datahandled['post_description_th']:
                        sel_funiture = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'amenities.hasAir'))).click()
                    if 'digital lock' in datahandled['post_description_th'].lower() or 'key card' in datahandled['post_description_th'].lower():
                        sel_funiture = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'amenities.hasDigitalDoorLock'))).click()
                    if 'tv' in datahandled['post_description_th'].lower() or 'ทีวี' in datahandled['post_description_th']:
                        sel_funiture = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'amenities.hasTV'))).click()
                    if 'ตู้เย็น' in datahandled['post_description_th']:
                        sel_funiture = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'amenities.hasRefrigerator'))).click()
                    if 'อินเตอร์เน็ต' in datahandled['post_description_th'] or 'wifi' in datahandled['post_description_th']:
                        sel_funiture = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'amenities.hasInternet'))).click()
                    if 'เครื่องทำน้ำอุ่น' in datahandled['post_description_th'] or 'เครื่องทำน้ำร้อน' in datahandled['post_description_th']:
                        sel_funiture = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'amenities.hasWaterHeater'))).click()
                    if 'อ่างอาบน้ำ' in datahandled['post_description_th']:
                        sel_funiture = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'amenities.hasHotTub'))).click()
                    if 'เตาไฟฟ้า' in datahandled['post_description_th'] or 'เตาแก๊ส' in datahandled['post_description_th'] or 'เตาทำอาหาร' in datahandled['post_description_th']:
                        sel_funiture = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'amenities.hasKitchenStove'))).click()
                    if 'ที่ดูดควัน' in datahandled['post_description_th'] or 'เครื่องดูดควัน' in datahandled['post_description_th']:
                        sel_funiture = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'amenities.hasKitchenHood'))).click()
                    if 'เครื่องซักผ้า' in datahandled['post_description_th']:
                        sel_funiture = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'amenities.hasWasher'))).click()

                    body = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body'))).send_keys(Keys.PAGE_DOWN)

                    upload = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div/form/div/div/div[3]/div[2]/input')))
                    #all_images = ""

                    all_images = ""
                    for count, pic in enumerate(postdata['post_images']):
                        if count < len(postdata['post_images'])-1:
                            all_images += os.path.abspath(pic) + '\n'
                        else:
                            all_images += os.path.abspath(pic)
                    upload = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div/form/div/div/div[3]/div[2]/input')))
                    upload.send_keys(all_images)
                    last_img = '//*[@id="__next"]/div[1]/div/div/form/div/div/div[3]/div[2]/div/div/div[' + str(len(postdata['post_images'])) + ']/div[3]/div[2]'
                    wait_upload = WebDriverWait(self.driver, 60).until(EC.text_to_be_present_in_element((By.XPATH, last_img), "100%"))

                    for i in range(len(postdata['post_images'])-1):
                        drag = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[1]/div/div/form/div/div/div[3]/div[2]/div/div/div[' + str(i+1) + ']')))
                        drop = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[1]/div/div/form/div/div/div[3]/div[2]/div/div/div[' + str(len(postdata['post_images'])) + ']')))
                        ActionChains(self.driver).drag_and_drop(drag, drop).perform()
                        ActionChains(self.driver).drag_and_drop(drop, drag).perform()

                    detail_post = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ql-editor')))
                    detail_post[1].click()
                    detail_post[1].send_keys(datahandled['post_description_th'])
                    detail_post[2].click()
                    detail_post[2].send_keys(datahandled['post_description_en'])

                    try:
                        last_img = '//*[@id="__next"]/div[1]/div/div/form/div/div/div[3]/div[2]/div/div/div[' + str(len(postdata['post_images'])) + ']/div[3]/div[2]'
                        wait_upload = WebDriverWait(self.driver, 60).until(EC.text_to_be_present_in_element((By.XPATH, last_img), "100%"))
                        success = 'true'
                    except:
                        success = 'false'
                        detail = 'Image are not uploaded successfully.'
                        post_url = ''
                        post_id = ''
                    
                    if success == 'true':
                        try:
                            agreement = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'agreement'))).click()
                            cfm_post = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'btnSaveListing'))).click()
                            sleep(5)
                            try:
                                check_eng = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'diLcnC'))).click()
                                cfm_post = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'btnSaveListing'))).click()
                                sleep(5)
                            except:
                                pass
                            
                            get_all_link = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'listing-list-view')))
                            title_check = ''
                            a_link = []
                            for link in get_all_link.find_elements_by_tag_name('a'):
                                if link.get_attribute('href') != None:
                                    if 'https://propertyhub.in.th/listings/' in link.get_attribute('href'):
                                        title_check = link.find_element_by_tag_name('span').get_attribute("innerHTML").split('<i')[0].replace('&nbsp;', ' ')
                                        if postdata['post_title_th'].replace(' ', '').replace('\xa0', '').strip() == title_check.replace(' ', '').strip():
                                            a_link.append(link.get_attribute('href'))               
                            if not a_link:
                                success = 'false'
                                detail = 'Your post already created but can not get the link. Please check your acount again'
                                post_url = ''
                                post_id = ''
                            else:
                                post_url = a_link[0]
                                post_id = post_url.split('---')[-1]
                                success = 'true'
                                detail = 'Post was created.'
                        except:
                            success = 'false'
                            detail =  'ไม่สามารถโพสประกาศได้ กรุณาตรวจสอบว่าท่านได้ยืนยันเบอร์มือถือหรือไม่ หากยืนยันแล้วโปรดตรวจสอบว่าข้อมูลครบถ้วนหรือไม่' #'Your post can not create. Please make sure your data is completed or make sure that you already verify you phone number via OTP.'
                            post_url = ''
                            post_id = ''
                else:
                    post_url = ''
                    post_id = ''
            else:
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

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]

        datahandled = self.postdata_handle(postdata)

        slt_project = datahandled['project_name'].split(' ')

        try:
            if success == 'true':
                self.driver.get('https://dashboard.propertyhub.in.th/members/listings/edit/' + postdata['post_id'])

                clear_pop = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body'))).send_keys(Keys.ESCAPE)
                title_th = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'title.th')))
                title_th.send_keys(Keys.CONTROL + 'a')
                title_th.send_keys(datahandled['post_title_th'])
                title_en = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'title.en')))
                title_en.send_keys(Keys.CONTROL + 'a')
                title_en.send_keys(datahandled['post_title_en'])
                project = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div/div/form/div/div/div[1]/div[4]/div[2]/div/div/input')))
                for word in slt_project:
                    project.send_keys(word+' ')
                    sleep(0.4)
                project.send_keys(Keys.BACKSPACE)
                sleep(0.6)

                try:
                    all_sel_pro = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'i8hizn-0')))
                    all_sel_pro[0].click()
                    """ match = 0
                    for project_sel in all_sel_pro:
                        #print(project_sel.text)
                        print(slt_project)
                        for word in slt_project:
                            #print(word.replace('(', '').replace(')', ''))
                            if word.replace('(', '').replace(')', '') in project_sel.text.split('\n')[0].replace('(', '').replace(')', '').split(' '):
                                print(project_sel.text.split('\n')[0].replace('(', '').replace(')', '').split(' '))
                                print(word.replace('(', '').replace(')', ''))
                                print('Match')
                                match += 1
                        #print(match)
                        if match >= len(project_sel.text.split('\n')[0].replace('(', '').replace(')', '').split(' '))-1:
                            project_sel.click()
                            success = 'true'
                            break
                        else:
                            success = 'false'
                            detail = 'Your project name does not match.' """
                except:
                    success = 'false'
                    detail = 'ไม่สามารถโพสต์ประกาศได้ เนื่องจากไม่เจอโครงการของคุณ'
                    
                """ try:
                    project_sel = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div/form/div/div/div[1]/div[4]/div[2]/div/div/div[2]/div/div/div'))).click()
                    success = 'true'
                    detail = 'Found project'
                except:
                    success = 'false'
                    detail = 'Your project name does not match.' """

                if success == 'true':
                    building = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'roomInformation.building')))
                    building.send_keys(Keys.CONTROL + 'a')
                    building.send_keys(datahandled['building'])
                    sel_roomtype =  WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.NAME, 'roomInformation.roomType')))[1].click()
                    sel_type1 = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'item')))
                    for count, value in enumerate(sel_type1):
                        if datahandled['type_room'] in value.text:
                            value.click()
                            break
                    on_floor = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'roomInformation.onFloor')))
                    on_floor.send_keys(Keys.CONTROL + 'a')
                    on_floor.send_keys(datahandled['floor_level'])
                    bed_room = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'roomInformation.numberOfBed')))
                    bed_room.send_keys(Keys.CONTROL + 'a')
                    bed_room.send_keys(datahandled['bed_room'])
                    bath_room = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'roomInformation.numberOfBath')))
                    bath_room.send_keys(Keys.CONTROL + 'a')
                    bath_room.send_keys(datahandled['bath_room'])
                    floor_area = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'roomInformation.roomArea')))
                    floor_area.send_keys(Keys.CONTROL + 'a')
                    floor_area.send_keys(datahandled['floor_area'])

                    sel_posttype = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'postType')))
                    #print(sel_posttype.get_attribute('value'))
                    try:
                        sel_posttype = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.NAME, 'postType')))[1].click()
                        sel_type2 = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@class="visible menu transition"]')))
                        child_sel_type2 = sel_type2.find_elements_by_tag_name('div')
                        if postdata['listing_type'] == 'ขาย':
                            #print(sel_type2[25].text)
                            child_sel_type2[1].click()
                            sale_price = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'price.forSale.price')))
                            sale_price.send_keys(Keys.CONTROL + 'a')
                            sale_price.send_keys(datahandled['price_baht'])
                        elif postdata['listing_type'] == 'เช่า':
                            #print(sel_type2[26].text)
                            child_sel_type2[0].click()
                            rent_price = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'price.forRent.monthly.price')))
                            rent_price.send_keys(Keys.CONTROL + 'a')
                            rent_price.send_keys(datahandled['price_baht'])
                            daily_price = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.NAME, 'price.forRent.daily.type')))[2].click()
                            deposit = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.NAME, 'price.forRent.deposit.type')))[2].click()
                            advance = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.NAME, 'price.forRent.advancePayment.type')))[2].click()
                    except:
                        if sel_posttype.get_attribute('value') == 'FOR_SALE_TRIAL':
                            sale_price = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'price.forSale.price')))
                            sale_price.send_keys(Keys.CONTROL + 'a')
                            sale_price.send_keys(datahandled['price_baht'])
                        elif sel_posttype.get_attribute('value') == 'FOR_RENT':
                            rent_price = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'price.forRent.monthly.price')))
                            rent_price.send_keys(Keys.CONTROL + 'a')
                            rent_price.send_keys(datahandled['price_baht'])
                            daily_price = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.NAME, 'price.forRent.daily.type')))[2].click()
                            deposit = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.NAME, 'price.forRent.deposit.type')))[2].click()
                            advance = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.NAME, 'price.forRent.advancePayment.type')))[2].click()
                        pass

                    images = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'dragablePreview')))
                    sel_img = images[0]
                    for image in images:
                        action_chain = ActionChains(self.driver)
                        action_chain.move_to_element(sel_img)
                        sleep(1.5)
                        del_img = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'trceoc-0')))
                        action_chain.move_to_element(del_img)
                        sleep(1.5)
                        action_chain.click().perform()
                        
                    all_images = ""
                    for count, pic in enumerate(postdata['post_images']):
                        if count < len(postdata['post_images'])-1:
                            all_images += os.path.abspath(pic) + '\n'
                        else:
                            all_images += os.path.abspath(pic)
                    
                    upload = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div/form/div/div/div[3]/div[2]/input')))
                    upload.send_keys(all_images)
                    last_img = '//*[@id="__next"]/div[1]/div/div/form/div/div/div[3]/div[2]/div/div/div[' + str(len(postdata['post_images'])) + ']/div[3]/div[2]'
                    wait_upload = WebDriverWait(self.driver, 60).until(EC.text_to_be_present_in_element((By.XPATH, last_img), "100%"))

                    for i in range(len(postdata['post_images'])-1):
                        drag = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[1]/div/div/form/div/div/div[3]/div[2]/div/div/div[' + str(i+1) + ']')))
                        drop = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[1]/div/div/form/div/div/div[3]/div[2]/div/div/div[' + str(len(postdata['post_images'])) + ']')))
                        ActionChains(self.driver).drag_and_drop(drag, drop).perform()
                        ActionChains(self.driver).drag_and_drop(drop, drag).perform()

                    detail_post = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ql-editor')))
                    detail_post[1].click()
                    detail_post[1].send_keys(Keys.CONTROL + 'a')
                    detail_post[1].send_keys(datahandled['post_description_th'])
                    detail_post[2].click()
                    detail_post[2].send_keys(Keys.CONTROL + 'a')
                    detail_post[2].send_keys(datahandled['post_description_en'])

                    try:
                        last_img = '//*[@id="__next"]/div[1]/div/div/form/div/div/div[3]/div[2]/div/div/div[' + str(len(postdata['post_images'])) + ']/div[3]/div[2]'
                        wait_upload = WebDriverWait(self.driver, 60).until(EC.text_to_be_present_in_element((By.XPATH, last_img), "100%"))
                        success = 'true'
                    except:
                        success = 'false'
                        detail = 'Image are not uploaded successfully.'
                    
                    if success == 'true':
                        agreement = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'agreement'))).click()
                        cfm_post = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'btnSaveListing'))).click()
                        sleep(5)
                        try:
                            check_eng = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'diLcnC'))).click()
                            cfm_post = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'btnSaveListing'))).click()
                            sleep(5)
                        except:
                            pass

                        postcheck = True
                        while postcheck:
                            get_all_link = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'listing-list-view')))
                            title_check = ''
                            a_link = []
                            for link in get_all_link.find_elements_by_tag_name('a'):
                                if link.get_attribute('href') != None:
                                    if 'https://propertyhub.in.th/listings/' in link.get_attribute('href'):
                                        title_check = link.find_element_by_tag_name('span').get_attribute("innerHTML").split('<i')[0].replace('&nbsp;', ' ')
                                        if postdata['post_title_th'].replace(' ', '').replace('\xa0', '').strip() == title_check.replace(' ', '').strip():
                                            a_link.append(link.get_attribute('href'))
                            if a_link:
                                post_url = a_link[0]
                                postcheck = False
                                success = 'true'
                                detail = 'Post was edited.'
                            if postcheck:
                                #Pagination
                                try:
                                    pagi = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'sc-1p20b44-0')))
                                    pagechk = pagi.find_elements_by_tag_name('li')[-1].click()
                                except:
                                    postcheck = False
                                    success = 'false'
                                    detail = 'Your post already edited but can not get the link. Please check your acount again'
                                    post_url = ''
                                    pass     
                        
                else:
                    post_url = ''
            else:
                post_url = ''

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
            "ds_id": postdata['ds_id'],
            "post_url" : post_url,
            "post_id" : postdata['post_id'],
            "account_type": "null",
            "detail": detail,
            "websitename": self.websitename
        }


    def boost_post(self, postdata):

        time_start = datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]

        try:
            if success == 'true':
                self.driver.get('https://dashboard.propertyhub.in.th/members/listings/online')
                sleep(1)
                clear_pop = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body'))).send_keys(Keys.ESCAPE)
                sleep(1)
                check_limit_rent = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sc-1rsvu2b-3')))
                if int(check_limit_rent[1].text.split('/')[0].replace(',', '')) < int(check_limit_rent[1].text.split('/')[1].replace(',', '')):
                    success = 'true'
                else:
                    success = 'false'
                    detail = 'You can not boost your post any more cause reaching the limit.'

                if success == 'true':
                    search = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="sc-1r06t7h-0 cxhLHS hp6yc9-0 hMAYxM"]'))).click()
                    sleep(1)
                    iden = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'listingId'))).send_keys(postdata['post_id'])
                    apply = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'kLYpXZ'))).click()
                    sleep(1)
                    try:
                        refresh = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'btnRefreshListing'))).click()
                        success = 'true'
                        detail = 'Your post has been boosted.'
                    except:
                        try:
                            refresh = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'btnRefreshTrialListing'))).click()
                            sleep(5)
                            try:
                                elements = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "bp3-popover")))
                                success = 'false'
                                detail = 'Sales announcements can be boot one time per day.'
                            except:
                                success = 'true'
                                detail = 'Your post has been boosted.'
                        except:
                            success = 'false'
                            detail = 'Your post does not exist. Please check the post id.'
        finally:
            self.driver.close()
            self.driver.quit()

        time_end = datetime.utcnow()
        time_usage = time_end-time_start

        return {
            "success": success, 
            "usage_time": str(time_usage), 
            "start_time": str(time_start), "end_time": str(time_end), 
            "detail": detail, 
            "log_id": postdata['log_id'], 
            "websitename": self.websitename
        }


    def search_post(self, postdata):

        time_start = datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]

        datahandled = self.postdata_handle(postdata)

        slt_project = datahandled['project_name'].split(' ')

        try:
            if success == 'true':
                self.driver.get('https://dashboard.propertyhub.in.th/members/listings/online')
                sleep(1)
                clear_pop = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body'))).send_keys(Keys.ESCAPE)
                sleep(1)
                search_pro = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='__next']/div[1]/div[2]/div[1]/div[1]/input"))).send_keys(datahandled['project_name'])
                sleep(1)
                try:
                    results = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'kJrNeq')))
                    success = 'true'
                except:
                    success = 'false'
                    detail = 'Your post has not been created yet.'
                    post_found = 'false'
                    post_id = ''
                    post_url = ''
                
                if success == 'true':
                    match = 0
                    for result in results:
                        for word in slt_project:
                            if word in result.text.split('\n')[0].split(' '):
                                match += 1
                        """ print(result.text.split('\n')[0].split(' '))
                        print(match) """
                        if match >= len(result.text.split('\n')[0].split(' '))/2:
                            result.click()
                            success = 'true'
                            break
                        else:
                            success = 'false'
                            detail = 'Your project name is not contain in your list.'

                    if success == 'true':
                        all_list = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'gjWKCz')))
                        for li in all_list:
                            if datahandled['post_title_th'].lower() in li.text.lower():
                                url = li.get_attribute('href')
                                success = 'true'
                                post_found = 'true'
                                detail = 'Your post has already been created.'
                                post_id = url.split('---')[-1]
                                post_url = url
                                break
                            else:
                                success = 'false'
                                detail = 'Your post has not been created yet.'
                                post_found = 'false'
                                post_id = ''
                                post_url = ''
        finally:
            self.driver.close()
            self.driver.quit()
        
        time_end = datetime.utcnow()
        time_usage = time_end-time_start

        return {
            "success": "true",
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_found": post_found,
            "post_id": post_id,
            'post_url': post_url,
            "post_create_time": '',
            "post_modify_time": '',
            "post_view": '',
            'websitename': self.websitename
        }


    def delete_post(self, postdata):

        time_start = datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]

        try:
            if success == 'true':
                self.driver.get('https://dashboard.propertyhub.in.th/members/listings/online')
                sleep(1)
                clear_pop = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body'))).send_keys(Keys.ESCAPE)
                sleep(1)

                search = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div[1]/div/div[2]/div[5]/div/div[1]/button'))).click()
                iden = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'listingId'))).send_keys(postdata['post_id'])
                apply = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'kQuBJO'))).click()

                try:
                    delete = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'btnTakeOfflineListing'))).click()
                    success = 'true'
                    detail = 'Your post has been deleted.'
                except:
                    success = 'false'
                    detail = 'Your post does not exist. Please check the post id.'
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
            "log_id": postdata['log_id'],
            "ds_id": postdata['ds_id'],
            "post_id": postdata['post_id'],
            "websitename": self.websitename
        }