# -*- coding: utf-8 -*-

from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
import re
import json
import datetime
import sys
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys



category_types = {
    '1': '19',
    '2': '20',
    '3': '22',
    '4': '18',
    '5': '21',
    '6': '17',
    '7': '23',
    '8': '22',
    '9': '22',
    '10': '22',
    '25': '22'
} 
httprequestObj = lib_httprequest()

class baandd():
    name = 'baandd'
    site_name = "http://www.baan-dd.com"

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



        self.options = Options()
        self.options.headless = True
        # self.options.add_argument("--headless")  # Runs Chrome in headless mode.
        # self.options.add_argument('--no-sandbox')  # Bypass OS security model
        self.options.add_argument('start-maximized')
        self.options.add_argument('disable-infobars')
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("window-size=1024,768")
        # self.chromedriver_binary = "/usr/bin/chromedriver"

    def logout_user(self):
        url = 'http://www.baan-dd.com/index.php?option=logout'
        httprequestObj.http_get(url)


    def register_user(self, postdata):
        self.logout_user()
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        success = "false"
        detail = 'An Error has Occurred'

        datapost = {
            "name": postdata['name_th'] + ' ' + postdata['surname_th'],
            "username": postdata['user'],
            "email": postdata['user'],
            "password": postdata['pass'],
            "password2": postdata['pass']
        }

        r = httprequestObj.http_get(self.site_name+'/index.php?option=com_registration&task=register')
        soup = BeautifulSoup(r.text, features=self.parser)
        form = soup.find(attrs={'name':'mosForm'})
        inputs = form.find_all('input', {'type':'hidden'})
        for inp in inputs:
            datapost[inp.get('name')] = inp.get('value')

        response = httprequestObj.http_post(self.site_name+'/index.php', data=datapost)
        if response.status_code==200:
            soup = BeautifulSoup(response.content, features=self.parser)
            res_div = soup.find(class_='componentheading')
            if res_div:
                if res_div.getText()=='การลงทะเบียนเสร็จสมบูรณ์!':
                    success = "true"
                    detail = "Registration Successfull"   
            elif 'window.history.go(-1)' in response.text:
                detail  = "This email is already in use"            
        else:
            detail = 'An Error has occurred with response_code '+str(response.status_code)

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            'ds_id': postdata['ds_id'],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": self.name,
            "ds_id": postdata['ds_id']
        }



    def test_login(self, postdata):
        self.logout_user()
        r = httprequestObj.http_get('http://www.baan-dd.com/index.php?option=logout')
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        
        # start process
        success = "false"
        detail = 'An Error has Occurred'

        datapost = {
            "username": postdata['user'],
            "passwd": postdata['pass'],
            "Submit":  "Sign in"
        }

        r = httprequestObj.http_get(self.site_name+'/index.php')
        soup = BeautifulSoup(r.text, features=self.parser)
        form = soup.find(attrs={'name':'login'})
        
        try:
            inputs = form.find_all('input', {'type':'hidden'})
            for inp in inputs:
                datapost[inp.get('name')] = inp.get('value')    
        except AttributeError:
            pass

        response = httprequestObj.http_post(self.site_name+'/index.php', data=datapost)

        if response.status_code == 200:
            if b'alert(\'\xaa\xd7\xe8\xcd\xbc\xd9\xe9\xe3\xaa\xe9\xcb\xc3\xd7\xcd\xc3\xcb\xd1\xca\xbc\xe8\xd2\xb9 \xe4\xc1\xe8\xb6\xd9\xa1\xb5\xe9\xcd\xa7  \xa1\xc3\xd8\xb3\xd2\xc5\xcd\xa7\xe3\xcb\xc1\xe8\')' in response.content:
                detail = "Invalid username or password"
            else:
                soup = BeautifulSoup(response.text, features=self.parser)
                if soup.find(attrs={'name':'logout'}):
                    success = "true"
                    detail = "Logged in successfully" 
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
            "ds_id": postdata['ds_id']
        }



    def edit_title_selenium(self, username, password, post_id, post_title, post_description, name):
        print('Here')
        options = Options()
        options.set_headless(True)
        options.add_argument('--no-sandbox')

        chrome = webdriver.Chrome("./static/chromedriver", chrome_options=options)
        chrome.implicitly_wait(4)
        print('Now here')
        #chrome = webdriver.Chrome(self.chromedriver_binary, options=self.options)
        delay = 3
        timeout = 10
        while timeout>0:
            print(timeout)
            chrome.get(self.site_name+'/index.php')
            form = WebDriverWait(chrome, delay).until(EC.presence_of_element_located((By.NAME, 'login')))

            username_in = form.find_element_by_name('username')
            username_in.send_keys(username)
            password_in = form.find_element_by_name('passwd')
            password_in.send_keys(password)
            submit_btn = WebDriverWait(form, delay).until(EC.element_to_be_clickable((By.NAME, "Submit")))
            submit_btn.click()
            
            timeout -= 1
            try:
                WebDriverWait(chrome, delay).until(EC.presence_of_element_located((By.NAME, 'logout')))
                break
            except TimeoutException:
                print('Timeout 1')
                if timeout==0:
                    return False
                pass
        
        # edit post details
        timeout = 5
        while timeout>0:
            try:
                url=self.site_name+'/index.php?option=com_marketplace&page=write_ad&adid='+post_id+'&Itemid=56'
                print(url)
                chrome.get(url)
                ad_form = WebDriverWait(chrome, delay).until(EC.presence_of_element_located((By.NAME, 'write_ad')))
                post_title_in = ad_form.find_element_by_name('ad_headline')
                post_title_in.clear()
                post_title_in.send_keys(post_title)
                script = 'document.getElementsByName("ad_text")[0].value='+json.dumps(r'{}'.format(post_description))+';'
                chrome.execute_script(script)

                name_in = ad_form.find_element_by_name('name')
                name_in.clear()
                name_in.send_keys(name)
                
                timeout -= 1
    
                post_submit_btn = WebDriverWait(ad_form, delay).until(EC.element_to_be_clickable((By.NAME, 'submit')))
                post_submit_btn.click()
                if chrome.current_url=="http://www.baan-dd.com/index.php?option=com_marketplace&page=write_ad&Itemid=56":
                    break
                elif timeout==0:
                    print('Timeout 2')
                    chrome.quit()
                    return False
            except (StaleElementReferenceException, TimeoutException):
                if timeout==0:
                    print('Timeout 3')
                    return False
                continue
        
        chrome.quit()
        return True
        


    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        # login

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = "Unable to create post"
        post_id = ""
        post_url = ""
        
        if 'web_project_name' not in postdata or postdata['web_project_name'] is None:
            if 'project_name' in postdata and postdata['project_name'] is not None:
                postdata['web_project_name'] = postdata['project_name']
            else:
                postdata['web_project_name'] = postdata['post_title_th']
        
        if success=="true":            
            success = "false" 
            if len(str(postdata['post_description_th']).replace('\n', '<br>'))>=5:
                try:
                    category = category_types[str(postdata['property_type'])]
                except:
                    category = '22'
                datapost = {
                    "name": postdata['name'],
                    "email": postdata['email'],
                    "web": "-",
                    "phone1": postdata['mobile'],
                    "ad_type": "2",
                    "category": category,
                    "ad_headline": str(postdata['post_title_th']),
                    "ad_text": str(postdata['post_description_th']),
                    "ad_price": postdata['price_baht'],
                    "submit": "ส่งประกาศ"
                }

                r = httprequestObj.http_get(self.site_name+ '/index.php?option=com_marketplace&page=write_ad&Itemid=56')
                soup = BeautifulSoup(r.text, features=self.parser)
                form  = soup.find(attrs={'name': 'write_ad'})
                
                if form:
                    for hidden_input in form.find_all('input',{'type': 'hidden'}):
                        datapost[hidden_input.get('name')] = hidden_input.get('value')          
                    files = {}
                    for i, image in enumerate(postdata["post_images"][:3]):
                        files["ad_picture"+str(i+1)] = open(os.getcwd()+"/"+image, 'rb')
                    
                    #print(json.dumps(datapost))
                    response = httprequestObj.http_post(self.site_name+'/index.php?option=com_marketplace&page=write_ad&Itemid=56', data=datapost, files=files)
                    with open('temp.html', 'w') as f:
                        f.write(str(response.text))
                    if response.status_code==200:
                        try:
                            table = BeautifulSoup(response.text, features=self.parser).find(class_='contentpadding').find('table')
                        
                            if table.find_all('table')[-1].find('img').get('src')=='http://www.baan-dd.com/components/com_marketplace/images/system/success.gif':
                                success = "true"
                                detail = "Post created successfully"

                                r = httprequestObj.http_get(self.site_name+'/index.php?option=com_marketplace&page=show_category&catid=0&Itemid=56')
                                print(r.url)
                                print(r.status_code)
                                if r.status_code==200:
                                    soup = BeautifulSoup(r.text, features=self.parser)
                                    posts = soup.find_all(class_='jooNormal')
                                    if posts:
                                        print('INSIDE')
                                        links = posts[0].find('table').find_all('a')
                                        post_url = links[-1].get('href')
                                        post_id = post_url.split('adid=')[1].split('&')[0]
                                        print('Checked')
                                        if not self.edit_title_selenium(postdata['user'], postdata['pass'], post_id, str(postdata['post_title_th']), str(postdata['post_description_th']), str(postdata['name'])):
                                            success = "false"
                                            detail = "Post created. But an error occurred while updating title"
                        except (AttributeError, IndexError):
                            pass
                    else:
                        detail = 'Unable to create post. An Error has occurred with response_code '+str(response.status_code) 
            else:
                success = "false"
                detail = "Description is too short"
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
        detail = "Unable to update post"
        post_id = ""
        post_url = ""

        if 'web_project_name' not in postdata or postdata['web_project_name'] is None:
            if 'project_name' in postdata and postdata['project_name'] is not None:
                postdata['web_project_name'] = postdata['project_name']
            else:
                postdata['web_project_name'] = postdata['post_title_th']
        
        if success=="true":
            success = "false" 
            if len(str(postdata['post_description_th']).replace('\n', '<br>'))>=5:
                try:
                    category = category_types[str(postdata['property_type'])]
                except:
                    category = '22'
                datapost = {
                    "name": postdata['name'],
                    "email": postdata['email'],
                    "web": "-",
                    "phone1": postdata['mobile'],
                    "ad_type": "2",
                    "category": category,
                    "ad_headline": postdata['post_title_th'],
                    "ad_text": postdata['post_description_th'],
                    "ad_price": postdata['price_baht'],
                    "submit": "ส่งประกาศ"
                }
                r = httprequestObj.http_get(self.site_name+'/index.php?option=com_marketplace&page=write_ad&adid='+postdata['post_id']+'&Itemid=56')
                soup = BeautifulSoup(r.text, features=self.parser)
                form  = soup.find(attrs={'name': 'write_ad'})
                
                if form and form.find(attrs={'name':'ad_headline'}).get('value'):
                    for hidden_input in form.find_all('input',{'type': 'hidden'}):
                        datapost[hidden_input.get('name')] = hidden_input.get('value') 
                    
                    files = {}
                    for i, image in enumerate(postdata["post_images"][:3]):
                        files["ad_picture"+str(i+1)] = open(os.getcwd()+"/"+image, 'rb')

                    response = httprequestObj.http_post(self.site_name+'/index.php?option=com_marketplace&page=write_ad&Itemid=56', data=datapost, files = files)
                    if response.status_code==200:
                        table = BeautifulSoup(response.text, features=self.parser).find(class_='contentpadding').find('table')
                        try:
                            if str(table.find_all('table')[-1].find('img').get('src'))=='http://www.baan-dd.com/components/com_marketplace/images/system/success.gif':
                                success = "true"
                                detail = "Post updated successfully"
                                if not self.edit_title_selenium(postdata['user'], postdata['pass'], postdata['post_id'],str(postdata['post_title_th']),str(postdata['post_description_th']),str(postdata['name'])):
                                    success = "false"
                                    detail = "Post created. But an error occurred while updating title"
                        except:
                                success = 'false'
                                detail = 'not updated'
                    else:
                        detail = 'Unable to update post. An Error has occurred with response_code '+str(response.status_code) 
                else:
                    detail = "No post found with given id"
            else:
                success = "true"
                detail = "Description is too short"
        else:
            detail = "cannot login"
        
        time_end = datetime.datetime.utcnow()
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
            "websitename": self.name,
            "ds_id": postdata['ds_id']
        }



    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = "Unable to delete post"

        if success=="true":
            success = "false"
            post_id = str(postdata['post_id'])
            flag = True
            i = 0
            post_found = False
            detail = "No post found with given id"
            while flag:
                r = httprequestObj.http_get(self.site_name+'/index.php?option=com_marketplace&page=show_category&catid=0&Itemid=56&ad_type=0&limit=20&limitstart='+str(i*20))
                if r.status_code==200:
                    soup = BeautifulSoup(r.content, features=self.parser)
                    posts = soup.find_all(class_='jooNormal')
                    for post in posts:
                        links = post.find('table').find_all('a')
                        if str(links[-1].get('href').split('adid=')[1].split('&')[0])==post_id:
                            post_found = True
                            break
                    if len(posts)<20:
                        flag = False
                    i += 1
                else:
                    flag = False
                    detail = "Unable to search. An Error has occurred with response_code "+str(r.status_code)        
            
            if post_found:
                response = httprequestObj.http_get(self.site_name+"/index.php?option=com_marketplace&page=delete_ad&adid="+postdata['post_id']+"&mode=db&Itemid=56")
                if response.status_code==200:
                    soup = BeautifulSoup(response.text, features=self.parser)
                    tables = soup.find_all('table')
                    for table in tables:
                        try:
                            if table.find('img').get('src')=='http://www.baan-dd.com/components/com_marketplace/images/system/success.gif':
                                success = "true"
                                detail = "Post deleted successfully!"
                                break
                            elif table.find('img').get('src')=='http://www.baan-dd.com/components/com_marketplace/images/system/warning.gif':
                                detail = "No post found with given id"
                                break
                        except AttributeError:
                            pass
                else:
                    detail = "Unable to delete post. An Error has occurred with response_code "+str(response.status_code) 
        else:
            detail = "cannot login"
        
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": self.name,
            "post_id": postdata['post_id'],
            "log_id": postdata['log_id'],
            "ds_id": postdata['ds_id']
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
            post_title = str(postdata['post_title_th']).strip()
            flag = True
            i = 0
            while flag:
                response = httprequestObj.http_get(self.site_name+'/index.php?option=com_marketplace&page=show_category&catid=0&Itemid=56&ad_type=0&limit=20&limitstart='+str(i*20))
                if response.status_code==200:
                    soup = BeautifulSoup(response.content, features=self.parser)
                    posts = soup.find_all(class_='jooNormal')
                    for post in posts:
                        links = post.find('table').find_all('a')
                        titl=str(links[-1].getText().strip())
                        if titl in post_title or post_title in titl :
                            post_found = "true"
                            detail = "Post found successfully"
                            post_url = links[-1].get('href')
                            post_id = post_url.split('adid=')[1].split('&')[0]
                            post_view = post.find('table').find('tr').find_all(recursive=False)[1].getText()
                            break
                    if len(posts)<20:
                        flag = False
                    i += 1
                else:
                    flag = False
                    success = "false"
                    detail = "Unable to search. An Error has occurred with response_code "+str(response.status_code)     
        else:
            detail = "cannot login"
        if post_found == 'false':
            post_title = ''
            success = 'false'
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
            "post_found": post_found,
            "post_title_th": post_title
        }



    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        
        if success=="true":
            success = "false"
            detail = "Unable to boost post"
            r = httprequestObj.http_get(self.site_name+'/index.php?option=com_marketplace&page=write_ad&adid='+postdata['post_id']+'&Itemid=56')
            soup = BeautifulSoup(r.text, features=self.parser)
            form  = soup.find(attrs={'name': 'write_ad'})
            datapost = {}
            files = {}
            if form:
                for inp in form.find_all('input'):
                    if inp.get('type') not in ['file', 'checkbox']:
                        datapost[inp.get('name')] = inp.get('value')
                
                datapost['ad_type'] = "2"
                datapost['category'] = "22"
                ad_type = form.find(attrs={'name': 'ad_type'}).find_all('option', selected=True)
                if ad_type:

                    datapost['ad_type'] = ad_type[-1].get('value')
                    category = form.find(attrs={'name': 'category'}).find_all('option', selected=True)
                    if category:
                        datapost['category']  = category[-1].get('value')
                    datapost['ad_text'] = form.find(attrs={'name': 'ad_text'}).getText()
                    
                    response = httprequestObj.http_post(self.site_name+'/index.php?option=com_marketplace&page=write_ad&Itemid=56', data=datapost, files=files)
                    
                    if response.status_code==200:
                        try:
                            table = BeautifulSoup(response.text, features=self.parser).find(class_='contentpadding').find('table')
                            if table.find_all('table')[-1].find('img').get('src')=='http://www.baan-dd.com/components/com_marketplace/images/system/success.gif':
                                success = "true"
                                detail = "Post boosted successfully"
                        except: 
                            pass
                    else:
                        detail = 'Unable to boost post. An Error has occurred with response_code '+str(response.status_code) 
                else:
                    detail = "No post found with given id"
        else:
            detail = "Cannot login"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "post_id": postdata['post_id'],
            "log_id": postdata['log_id'],
            "websitename": self.name,
            "ds_id": postdata['ds_id']
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
