from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from time import sleep
import os
import json

class facebook():

    def __init__(self): #For constructor when make an instance
        self.websitename = 'facebook' #Fix websitename for retruning value

    def test_login(self, postdata): #Main log in method

        #Set up web browser
        options = Options() #Create and options for chromedriver
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('start-maximized')
        options.add_argument('disable-infobars')
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

            """ if success == 'true':
                try:
                    self.driver.get('https://www.facebook.com/profile.php') #Try to redirect to profile page and facebook will bring to the profile page atomatically
                    #Get the username of facebook for comparingwhen the post is posted succesfully
                    self.username = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[2]/div/div/div[1]/div/div/div/div/span/h1'))).text
                    curr = self.driver.current_url  #Recieve current url for get the user id
                    try:
                        user_id = curr.split('/')[-1]   #
                    except:
                        pass
                    success = 'true'
                except:
                    success = 'false'
                    detail = 'Cannot login due to the wrong email or password.'
                    user_id = None

                #Check the username
                if user_id is not None:
                    success = 'true'
                    detail = 'Log in success. '
                else:
                    success = 'false'
                    detail = 'Log in fail. ' """

        if postdata['action'] == 'test_login':
            self.driver.close()

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
            datahandled['addr_province'] = 'กรุงเทพ'

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

        #Store the marketplace group id
        market_place = [ '949011775144962', '489057711426782', 'baandproperty', '225560867776412', '1519858448244276', '235671627109277', '191813887602870',
                         '465883490928070', '127202081207160', 'propertysinthailand', '197875780952405', '344667419323230', 'landandhouseforsale' ]

        if len(datahandled['post_title_th']) >= 99:
            datahandled['post_title_th'] = datahandled['post_title_th'][:99]
        
        if '\t' in datahandled['post_description_th']:
            datahandled['post_description_th'] = datahandled['post_description_th'].replace('\t', '\n')

        post_url = {}
        posted_g = []

        if success == 'true':
            for key, group in list_group.items():
                try:
                    self.driver.get('https://www.facebook.com/groups/' + group)
                    success = 'true'
                except:
                    success = 'false'
                    detail += 'Can not reach group page or not found the group by id. '
                    pass
                
                if success == 'true':
                    if group in market_place:
                        try:
                            sale_btn = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['sale_btn']))).click()
                            sale_photo = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['sale_photo'])))

                            all_images = ""
                            for count, pic in enumerate(postdata['post_images']):
                                if count < len(postdata['post_images'])-1:
                                    all_images += os.path.abspath(pic) + '\n'
                                else:
                                    all_images += os.path.abspath(pic)
                            sale_photo.send_keys(all_images)
                            """ if len(postdata['post_images']) < 8:
                                for pic in postdata['post_images']:
                                    pic_path = os.path.abspath(pic)
                                    sale_photo.send_keys(pic_path)
                            else:
                                for pic in postdata['post_images'][:9]:
                                    pic_path = os.path.abspath(pic)
                                    sale_photo.send_keys(pic_path) """
                            sale_title = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['sale_title'])))
                            sale_title.send_keys(datahandled['post_title_th'])
                            sale_price = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['sale_price'])))
                            sale_price.send_keys(datahandled['price_baht'])
                            try:
                                sale_detail1 = WebDriverWait(self.driver, 2.5).until(EC.presence_of_element_located((By.XPATH, element['sale_detail1'])))
                                sale_detail1.send_keys(datahandled['post_description_th'])
                            except:
                                sale_detail2 = WebDriverWait(self.driver, 2.5).until(EC.presence_of_element_located((By.XPATH, element['sale_detail2'])))
                                sale_detail2.send_keys(datahandled['post_description_th'])
                                pass
                            """ if len(postdata['post_images']) < 8:
                                num = len(postdata['post_images'])
                                limit = int((num/2)*(num+1)-num)
                                for i in range(limit):                                                                                                                                                                                   
                                    delete = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/div[3]/div[1]/div/div/div/div[1]/div/div/div[2]/div/div'))).click()
                            else:
                                num = len(postdata['post_images'][:9])
                                limit = int((num/2)*(num+1)-num)
                                for i in range(limit):                                                                                                                                                                                   
                                    delete = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/div[3]/div[1]/div/div/div/div[1]/div/div/div[2]/div/div'))).click()
                            sleep(1) """
                            sleep(5)
                            try:
                                sale_next2 = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, element['sale_next2']))).click()
                            except:
                                pass
                            try:
                                sale_next = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, element['sale_next1']))).click()
                            except:
                                pass
                            mp_check = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[4]/div[1]/div[4]/div'))).click()
                            #check_list = WebDriverWait(self.driver, 15).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[4]/div[1]/div[8]')))
                            """ for i in range(1, 46): #46
                                try:
                                    check_other = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[4]/div[1]/div[6]/div[3]/div[{i}]/div/div[1]/div[2]/div[1]/div/div/div[1]/span/span/span'))).text
                                except:
                                    check_other = ''
                                    pass
                                if check_other in list_group.keys():
                                    ch_group = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[4]/div[1]/div[6]/div[3]/div[{i}]/div'))).click()
                                    posted_g.append(check_other) """
                            post = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, element['sale_post']))).click()
                            #For testing
                            #cancel = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div'))).click()
                            success = 'true'
                            sleep(1)
                        except:
                            success = 'false'
                            detail = f'Can not post in {key} marketplace maybe you did not join the group yet. '
                            pass
                        
                        if success == 'true':
                            try:
                                user_name = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[1]/span/h2/span/div/a'))).text
                                if user_name:
                                    url = self.driver.current_url
                                    #posted_id = url.split('/')[-1]
                                    #post_url[key] = 'https://www.facebook.com/groups/' + group + '/permalink/' + posted_id
                                    post_url = url
                                    post_id = url.split('/')[-1]
                                    success = 'true'
                                    detail = 'Post successfully.'
                                    break
                            except:
                                post_url = ''
                                post_id = ''
                                success = 'false'
                                detail = 'Post success. But can not get the post id.'
                                break

                        """ if success == 'true':
                            try:
                                sleep(3)
                                self.driver.get('https://www.facebook.com/groups/' + group + '/yourposts')
                                share_btn = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div/div/div[1]/span/span/div/div[2]/div[2]/div'))).click()
                                for i in range(1, 46):
                                    try:
                                        check_other = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div[1]/div[2]/div[2]/div[{i}]/div/div[1]/div[2]/div[1]/div/div/div[1]/span/span/span'))).text
                                    except:
                                        check_other = ''
                                        pass
                                    if check_other in list_group.keys():
                                        #ch_group = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div[1]/div[2]/div[2]/div[{i}]/div/div[1]/div[2]/div[2]/div/div'))).click()
                                        ch_group = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div[1]/div[2]/div[3]/div[{i}]/div'))).click()
                                        posted_g.append(check_other)
                                    if len(posted_g) > 1:
                                        for item in posted_g:
                                            post_url[item] = 'https://www.facebook.com/groups/' + list_group[item] + '/permalink/' + post_id
                                submit_post = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div[2]/div/div/div[2]/div[2]'))).click()                                                                                        
                                sleep(3)
                                success = 'true'
                                detail = 'Post and share successfully.'
                                break
                            except:
                                success = 'true'
                                detail = 'Post success but can not share.'
                                break """

                    else:
                        try:
                            post_popup = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, element['post_popup']))).click()
                            pic_post = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/form/div/div/div/div/div/div[1]/div/div/div[1]/div[3]/div[1]/div[2]/div[1]/input')))
                            for pic in postdata["post_images"]:
                                pic_path = os.path.abspath(pic)
                                pic_post.send_keys(pic_path)
                            else:
                                datahandled['post_description_th'] = datahandled['post_description_th']
                            post = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['post'])))
                            post.send_keys(datahandled['post_description_th'])
                            try:
                                del_maps = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="facebook"]/body/div[5]/div[1]/div/div[2]/div/div/div/div[1]/div'))).click()
                            except:
                                pass
                            try:
                                submit = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['submit']))).click()
                            except:
                                sleep(1)
                                submit = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['submit']))).click()
                                pass
                            #For testing
                            #cancel = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/form/div/div/div/div/div/div[1]/div/div/div[1]/div[1]/div[1]/div[2]/div'))).click()
                            success = 'true'
                            detail = 'Group Post success. '
                        except:
                            success = 'false'
                            detail = f'Can not post in {key} group maybe you did not join the group yet. '
                            pass

                        try:
                            check_user = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['check_user']))).text
                            if check_user == self.username:
                                self.driver.get('https://www.facebook.com/groups/'+ group +'/search?q=' + self.username + '&filters=eyJycF9jaHJvbm9fc29ydCI6IntcIm5hbWVcIjpcImNocm9ub3NvcnRcIixcImFyZ3NcIjpcIlwifSJ9/')
                            select = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div/div[3]/a'))).click()
                            url = self.driver.current_url
                            posted_id = url.split('/')[-1]
                            post_url[key] = url
                            post_id = posted_id
                            success = 'true'
                            detail = 'Group post success but can not get the ID. '
                        except:
                            post_url[key] = ''
                            post_id = ''
                            success = 'false'
                            detail += 'Can not get post_id from group post. '
                            pass
    
        self.driver.close()
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

        #Store market place id
        market_place = [ '949011775144962', '489057711426782', 'baandproperty', '225560867776412', '1519858448244276', '235671627109277', '191813887602870',
                         '465883490928070', '127202081207160', 'propertysinthailand', '197875780952405', '344667419323230', 'landandhouseforsale' ]

        for key, group in list_group.items():  #key is the group name / value is the post id  
            if success == 'true':
                post_link = 'https://www.facebook.com/groups/'+ group +'/permalink/'+ postdata['post_id'] + '/'
                try:
                    self.driver.get(post_link)
                    success = 'true'
                except:
                    success = 'false'
                    detail = 'The page can not reach.'
                    pass

                if success == 'true':
                    if list_group[key] in market_place:
                        try:
                            menu_btn = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['menu_btn']))).click()
                            edit_f = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['edit_f'])))
                            if edit_f.text == 'แก้ไขโพสต์':
                                edit_f.click()
                                old_pic = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/div[3]/div[1]/span')))
                                pic_no = int(old_pic.text.split(' ')[3])
                                for i in range(pic_no):
                                    try:                                                                                                                                                                         
                                        delete = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/div[3]/div[1]/div[1]/div/div/div[1]/div/div/div[2]'))).click()                                              
                                    except:
                                        pass
                                sleep(2)
                                sale_photo = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['sale_photo'])))
                            
                                all_images = ""
                                for count, pic in enumerate(postdata['post_images']):
                                    if count < len(postdata['post_images'])-1:
                                        all_images += os.path.abspath(pic) + '\n'
                                    else:
                                        all_images += os.path.abspath(pic)
                                sale_photo.send_keys(all_images)
                                
                                """ for pic in postdata['post_images']:
                                    pic_path = os.path.abspath(pic)
                                    sale_photo.send_keys(pic_path) """

                                old_sale_title = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['sale_title'])))
                                old_sale_title.send_keys(Keys.CONTROL, 'a')
                                sale_title = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['sale_title'])))
                                sale_title.send_keys(datahandled['post_title_th'])

                                old_sale_price = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['sale_price'])))
                                old_sale_price.send_keys(Keys.CONTROL, 'a')
                                sale_price = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['sale_price'])))
                                sale_price.send_keys(datahandled['price_baht'])

                                try:
                                    old_sale_detail1 = WebDriverWait(self.driver, 2.5).until(EC.presence_of_element_located((By.XPATH, element['sale_detail1'])))
                                    old_sale_detail1.send_keys(Keys.CONTROL, 'a')
                                    sale_detail1 = WebDriverWait(self.driver, 2.5).until(EC.presence_of_element_located((By.XPATH, element['sale_detail1'])))
                                    sale_detail1.send_keys(datahandled['post_description_th'])
                                except:
                                    old_sale_detail2 = WebDriverWait(self.driver, 2.5).until(EC.presence_of_element_located((By.XPATH, element['sale_detail2'])))
                                    old_sale_detail2.send_keys(Keys.CONTROL, 'a')
                                    sale_detail2 = WebDriverWait(self.driver, 2.5).until(EC.presence_of_element_located((By.XPATH, element['sale_detail2'])))
                                    sale_detail2.send_keys(datahandled['post_description_th'])
                                pass

                                """ num = len(postdata['post_images'])
                                limit = int((num/2)*(num+1)-num)
                                for i in range(limit):                                                                                                                                                                                  
                                    delete = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/div[3]/div[1]/div/div/div/div[1]/div/div/div[2]/div/div'))).click()
                                sleep(4) """
                                sleep(5)
                                try:
                                    edit_submit1 = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, element['edit_post1']))).click()
                                except:
                                    edit_submit2 = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, element['edit_post2']))).click()
                                    pass
                                sleep(5)
                                success = 'true'
                                detail = 'Success for editing post.'
                                break
                            else:
                                edit_s = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['edit_s']))).click()
                                old_pic = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/div[3]/div[1]/span')))
                                pic_no = int(old_pic.text.split(' ')[3])
                                for i in range(pic_no):
                                    try:                                                                                                                                                                         
                                        delete = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/div[3]/div[1]/div[1]/div/div/div[1]/div/div/div[2]'))).click()                                              
                                    except:
                                        pass
                                sleep(2)
                                sale_photo = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['sale_photo'])))
                            
                                all_images = ""
                                for count, pic in enumerate(postdata['post_images']):
                                    if count < len(postdata['post_images'])-1:
                                        all_images += os.path.abspath(pic) + '\n'
                                    else:
                                        all_images += os.path.abspath(pic)
                                sale_photo.send_keys(all_images)

                                old_sale_title = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['sale_title'])))
                                old_sale_title.send_keys(Keys.CONTROL, 'a')
                                sale_title = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['sale_title'])))
                                sale_title.send_keys(datahandled['post_title_th'])

                                old_sale_price = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['sale_price'])))
                                old_sale_price.send_keys(Keys.CONTROL, 'a')
                                sale_price = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['sale_price'])))
                                sale_price.send_keys(datahandled['price_baht'])

                                try:
                                    old_sale_detail1 = WebDriverWait(self.driver, 2.5).until(EC.presence_of_element_located((By.XPATH, element['sale_detail1'])))
                                    old_sale_detail1.send_keys(Keys.CONTROL, 'a')
                                    sale_detail1 = WebDriverWait(self.driver, 2.5).until(EC.presence_of_element_located((By.XPATH, element['sale_detail1'])))
                                    sale_detail1.send_keys(datahandled['post_description_th'])
                                except:
                                    old_sale_detail2 = WebDriverWait(self.driver, 2.5).until(EC.presence_of_element_located((By.XPATH, element['sale_detail2'])))
                                    old_sale_detail2.send_keys(Keys.CONTROL, 'a')
                                    sale_detail2 = WebDriverWait(self.driver, 2.5).until(EC.presence_of_element_located((By.XPATH, element['sale_detail2'])))
                                    sale_detail2.send_keys(datahandled['post_description_th'])
                                pass

                                try:
                                    edit_submit1 = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, element['edit_post1']))).click()
                                except:
                                    edit_submit2 = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, element['edit_post2']))).click()
                                    pass
                                sleep(3)
                                success = 'true'
                                detail = 'Success for editing post.'
                                break

                        except:
                            success = 'false'
                            detail = 'Cannot edit post'

                    else:
                        try:
                            menu_btn = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['menu_btn']))).click()
                            edit_f = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['edit_f'])))
                            if edit_f.text == 'แก้ไขโพสต์':
                                edit_f.click()
                                clear_post = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['clear_post'])))
                                clear_post.send_keys(Keys.CONTROL, 'a', Keys.DELETE)
                                delete_pic = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['delete_pic']))).click()
                                success = 'true'
                            else:
                                edit_s = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['edit_s']))).click()
                                clear_post = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['clear_post'])))
                                clear_post.send_keys(Keys.CONTROL, 'a', Keys.DELETE)
                                delete_pic = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['delete_pic']))).click()
                                success = 'true'
                        except:
                            success = 'false'
                            detail = 'Can not clear the old data'

                        if success == 'true':
                            try:                                                                                               
                                post = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['post'])))
                                post.send_keys(datahandled['post_description_th'])
                                try:
                                    del_maps = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="facebook"]/body/div[5]/div[1]/div/div[2]/div/div/div/div[1]/div'))).click()
                                except:
                                    pass
                                pic_post = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['pic_post'])))
                                for pic in postdata["post_images"]:
                                    pic_path = os.path.abspath(pic)
                                    pic_post.send_keys(pic_path)
                                sleep(1)
                                submit = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element['submit'])))
                                success = 'true'
                                detail = 'Can edit post'
                            except:
                                success = 'false'
                                detail += 'Can not post. '
                                pass
        sleep(5)
        self.driver.close()

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
        group_dict = {
            "นายทุน นายหน้า อสังหาริมทรัพย์ทัวไทย": "949011775144962",
            "ขายฝาก ซื้อขาย จำนอง บ้าน ที่ดิน อสังหาฯ ราคาถูก ทั่วเมืองไทย": "489057711426782",
            "ขายบ้าน ซื้อบ้าน ที่ดิน อสังหา ทั่วประเทศ": "baandproperty",
            "ซื้อ-ขาย บ้าน ที่ดิน และอสังหาริมทรัพย์ อื่นๆ ทั่วไทย": "landandhouseforsale",
            "กลุ่มซื้อขาย ที่ดิน บ้าน และอสังหาริมทรัพย์ทุกชนิด": "225560867776412",
            "กลุ่มนายหน้าซื้อขายที่ดิน อสังหาริมทรัพย์ ทั่วประเทศ": "1519858448244276",
            "ซื้อขายบ้าน และคอนโดกรุงเทพ": "235671627109277",
            "ตลาดซื้อ-ขายที่ดิน อสังหาริมทรัพย์": "191813887602870",
            "ขาย ปล่อยเช่า คอนโดมิเนียม ในเขตกรุงเทพและปริมณฑล": "465883490928070",
            "บ้าน ห้องพัก คอนโด Apartment อพาร์ทเมนท์ ที่ดิน ขาย ให้เช่า กรุงเทพ": "127202081207160",
            "อสังหาริมทรัพย์ Asian RealEstate": "thaibestproperty",
            "แหล่งรวมห้องเช่าคอนโด": "1533334003579866",
            "ซื้อ/ขาย/เช่า บ้าน คอนโด ที่ดิน โดยเจ้าของขายเอง": "728861290645180",
            "Condolodge ซื้อ ขาย เช่า คอนโดทุกโครงการ ใกล้ BTS MRT ราคาถูกสุด": "1986622261663799",
            "CONDO EXCHANGE CENTERER": "918513708275659",
            "CONDO EXCHANGE CENTER OWNER POST": "951105918609202",
            "CONDO EXCHANGE CENTER 1,000,000 ผู้ใช้งาน ขายเช่า คอนโด บ้าน - Adviser": "property.exchange.center",
            "กล่มปล่อยเช่าคอนโด อพาร์ทเม้นท์": "995615727143180",
            "Bangkok Luxury Condo Exchange": "323050574855859",
            "Bangkok Condo for Rent and Sale ซื้อ ขาย เช่า คอนโดติดรถไฟฟ้า": "133594553855013",
            "กลุ่มซื้อขายคอนโดและปล่อยเช่า": "1809918985887417",
            "Rent Sale condo BTS MRT ปล่อยเช่าคอนโด ซื้อ-ขาย หาห้องพัก": "454134418690334",
            "Condo-Market คอนโด ซื้อ ขาย ให้เช่า ขายใบจอง": "condomarket",
            "คอนโด ห้องเช่า ที่พัก บ้านเช่า เช่า - ขาย กรุงเทพ กทม Bangkok": "1508927629253734",
            "ขาย เช่า คอนโด กรุงเทพ": "770357389784713",
            "曼谷公寓大樓~ Bangkok condo apartment for rent ~長租~短租": "1547652135557140",
            "Condo Only ซื้อขายเช่า “คอนโด” เท่านั้น": "828001787348618",
            "Property Thailand Sale-Rent": "373266569543816",
            "ประกาศ ขาย & ให้เช่า คอนโด บ้าน ที่ดิน ในกรุงเทพและปริมณฑล": "630201357077874",
            "ขาย เช่า คอนโด บ้าน ที่ดิน ทั่วประเทศ": "971888629619654",
            "เช่า ซื้อ หอพัก อพาร์ทเม้นท์ คอนโด กทม.และ ปริมณฑล": "237859323573408",
            "ฝากขายคอนโด/ขายดาวน์/ให้เช่า": "1604160379797295",
            "ซื้อ ขาย ให้เช่า บ้าน คอนโด ลาดพร้าว รามคำแหง": "doomyhome",
            "Condo ใกล้ BTS MRT ลงประกาศเช่าฟรี คอนโด รถไฟฟ้า": "1626040321016300",
            "CONDO EXCHANGE CENTER": "prakard",
            "CONDO & PROPERTY POST BY OWNER": "299716057099018",
            "ตลาดซื้อ-ขายบ้านและที่ดินเมืองไทย": "propertysinthailand",
            "กลุ่มซื้อขาย-เช่า บ้านและที่ดินทั่วประเทศไทย": "197875780952405",
            "ซื้อ-ขายที่ดิน และบ้านทั่วประเทศ": "1793532070937320",
            "ซื้อ-ขายที่ดินทั่วไทย": "344667419323"
        }

        with open('./static/facebook_element.json', 'r', encoding='utf-8') as e:
            element = json.load(e)

        for key, value in group_dict.items():
            try:
                url = 'https://www.facebook.com/groups/' + value + '/permalink/' + postdata['post_id'] + '/'
                self.driver.get(url)
                success = 'true'
            except:
                success = 'false'
                detail = 'The post does not exist.'

            try:
                menu_btn = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, element['menu_btn']))).click()
                delete_f = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/div/div[3]')))                                                                          
                if delete_f.text == 'ลบโพสต์':
                    delete_f.click()
                    cfm_btn = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div[2]/div/div[1]/div[1]'))).click()       
                                                                                                                                                                                                 
                else:
                    delete_s = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/div/div[4]'))).click()
                    cfm_btn = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div[2]/div/div[1]/div[1]'))).click()
                success = 'true'
                detail = 'Delete the post successfully'
                break
            except:
                success = 'false'
                detail = 'Can not delete post'

        self.driver.close()
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

        """ test_login = self.test_login(postdata)
        success = test_login['success']
        detail = test_login['detail']

        time_start = datetime.utcnow()
        group_dict = {
            "นายทุน นายหน้า อสังหาริมทรัพย์ทัวไทย": "949011775144962",
            "ขายฝาก ซื้อขาย จำนอง บ้าน ที่ดิน อสังหาฯ ราคาถูก ทั่วเมืองไทย": "489057711426782",
            "ขายบ้าน ซื้อบ้าน ที่ดิน อสังหา ทั่วประเทศ": "baandproperty",
            "ซื้อ-ขาย บ้าน ที่ดิน และอสังหาริมทรัพย์ อื่นๆ ทั่วไทย": "landandhouseforsale",
            "กลุ่มซื้อขาย ที่ดิน บ้าน และอสังหาริมทรัพย์ทุกชนิด": "225560867776412",
            "กลุ่มนายหน้าซื้อขายที่ดิน อสังหาริมทรัพย์ ทั่วประเทศ": "1519858448244276",
            "ซื้อขายบ้าน และคอนโดกรุงเทพ": "235671627109277",
            "ตลาดซื้อ-ขายที่ดิน อสังหาริมทรัพย์": "191813887602870",
            "ขาย ปล่อยเช่า คอนโดมิเนียม ในเขตกรุงเทพและปริมณฑล": "465883490928070",
            "บ้าน ห้องพัก คอนโด Apartment อพาร์ทเมนท์ ที่ดิน ขาย ให้เช่า กรุงเทพ": "127202081207160",
            "อสังหาริมทรัพย์ Asian RealEstate": "thaibestproperty",
            "แหล่งรวมห้องเช่าคอนโด": "1533334003579866",
            "ซื้อ/ขาย/เช่า บ้าน คอนโด ที่ดิน โดยเจ้าของขายเอง": "728861290645180",
            "Condolodge ซื้อ ขาย เช่า คอนโดทุกโครงการ ใกล้ BTS MRT ราคาถูกสุด": "1986622261663799",
            "CONDO EXCHANGE CENTERER": "918513708275659",
            "CONDO EXCHANGE CENTER OWNER POST": "951105918609202",
            "CONDO EXCHANGE CENTER 1,000,000 ผู้ใช้งาน ขายเช่า คอนโด บ้าน - Adviser": "property.exchange.center",
            "กล่มปล่อยเช่าคอนโด อพาร์ทเม้นท์": "995615727143180",
            "Bangkok Luxury Condo Exchange": "323050574855859",
            "Bangkok Condo for Rent and Sale ซื้อ ขาย เช่า คอนโดติดรถไฟฟ้า": "133594553855013",
            "กลุ่มซื้อขายคอนโดและปล่อยเช่า": "1809918985887417",
            "Rent Sale condo BTS MRT ปล่อยเช่าคอนโด ซื้อ-ขาย หาห้องพัก": "454134418690334",
            "Condo-Market คอนโด ซื้อ ขาย ให้เช่า ขายใบจอง": "condomarket",
            "คอนโด ห้องเช่า ที่พัก บ้านเช่า เช่า - ขาย กรุงเทพ กทม Bangkok": "1508927629253734",
            "ขาย เช่า คอนโด กรุงเทพ": "770357389784713",
            "曼谷公寓大樓~ Bangkok condo apartment for rent ~長租~短租": "1547652135557140",
            "Condo Only ซื้อขายเช่า “คอนโด” เท่านั้น": "828001787348618",
            "Property Thailand Sale-Rent": "373266569543816",
            "ประกาศ ขาย & ให้เช่า คอนโด บ้าน ที่ดิน ในกรุงเทพและปริมณฑล": "630201357077874",
            "ขาย เช่า คอนโด บ้าน ที่ดิน ทั่วประเทศ": "971888629619654",
            "เช่า ซื้อ หอพัก อพาร์ทเม้นท์ คอนโด กทม.และ ปริมณฑล": "237859323573408",
            "ฝากขายคอนโด/ขายดาวน์/ให้เช่า": "1604160379797295",
            "ซื้อ ขาย ให้เช่า บ้าน คอนโด ลาดพร้าว รามคำแหง": "doomyhome",
            "Condo ใกล้ BTS MRT ลงประกาศเช่าฟรี คอนโด รถไฟฟ้า": "1626040321016300",
            "CONDO EXCHANGE CENTER": "prakard",
            "CONDO & PROPERTY POST BY OWNER": "299716057099018",
            "ตลาดซื้อ-ขายบ้านและที่ดินเมืองไทย": "propertysinthailand",
            "กลุ่มซื้อขาย-เช่า บ้านและที่ดินทั่วประเทศไทย": "197875780952405",
            "ซื้อ-ขายที่ดิน และบ้านทั่วประเทศ": "1793532070937320",
            "ซื้อ-ขายที่ดินทั่วไทย": "344667419323"
        }

        with open('./static/facebook_element.json', 'r', encoding='utf-8') as e:
            element = json.load(e)

        #Store market place id
        market_place = [ '949011775144962', '489057711426782', 'baandproperty', '225560867776412', '1519858448244276', '235671627109277', '191813887602870',
                         '465883490928070', '127202081207160', 'propertysinthailand', '197875780952405', '344667419323230', 'landandhouseforsale' ]

        if success == 'true':
            for key, value in postdata['post_id'].items():
                try:
                    url = 'https://www.facebook.com/groups/' + group_dict[key] + '/permalink/' + value + '/'
                    self.driver.get(url)
                    success = 'true'
                except:
                    success = 'false'
                    detail = 'The post does not exist.'

                if success == 'true':
                    if group_dict[key] in market_place:
                        try:
                            menu_btn = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, element['menu_btn']))).click()
                            edit_f = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, element['edit_f'])))
                            if edit_f.text == 'แก้ไขโพสต์':
                                edit_f.click()
                                old_sale_detail = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, element['old_sale_detail'])))
                                old_sale_detail.send_keys(' ')
                                success = 'true'
                            else:
                                edit_s = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, element['edit_s']))).click()
                                old_sale_detail = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, element['old_sale_detail'])))
                                old_sale_detail.send_keys(' ')
                                try:
                                    edit_submit = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, element['edit_post']))).click()
                                    break
                                except:
                                    sleep(5)
                                    edit_submit = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, element['edit_post']))).click()
                                success = 'true'
                        except:
                            success = 'false'
                            detail = 'Cannot boostpost'

                    else:
                        try:
                            menu_btn = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, element['menu_btn']))).click()
                            edit_f = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, element['edit_f'])))
                            if edit_f.text == 'แก้ไขโพสต์':
                                edit_f.click()
                                post = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, element['post'])))
                                post.send_keys(' ')
                                submit = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, element['submit'])))
                                success = 'true'
                            else:
                                edit_s = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, element['edit_s']))).click()
                                post = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, element['post'])))
                                post.send_keys(' ')
                                submit = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, element['submit'])))
                                success = 'true'
                        except:
                            success = 'false'
                            detail = 'Can not clear the old data'
        self.driver.close() """
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

        self.driver.close()
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