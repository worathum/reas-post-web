from selenium import webdriver
from urllib.parse import unquote
import sys
import time
import requests
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from .lib_httprequest import *
from .lib_captcha import *
import os
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
# import lib_httprequest
from bs4 import BeautifulSoup
import os.path
from urllib import parse
import re
import json
import datetime
import shutil

captcha = lib_captcha()
with open("./static/houseforsale,land.json") as f:

    provincedata = json.load(f)
with open("./static/houseforsaleProvincedistrict.json") as f:
    provinceDistrictdata = json.load(f)


class houseforsaleland():

    name = 'houseforsaleland'

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

        return {
            "success": "true",
            "time_usage": time_end - time_start,
            "time_start": time_start,
            "time_end": time_end,
            "detail": ""
        }



    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()

        success = "false"
        detail = "Website does not have Registration"

        end_time = datetime.datetime.utcnow()
        time_usage = end_time - start_time
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(start_time),
            "end_time": str(end_time),
            "detail": detail,
            "ds_id": postdata['ds_id'],
            "websitename": "houseforsaleland",
        }

    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()

        if '@' in postdata['user']:
            success = "true"
            detail = "No Login Option in site"
        else:
            success = "false"
            detail = "Your username need to be an email."


        end_time = datetime.datetime.utcnow()
        time_usage = end_time - start_time
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(start_time),
            "end_time": str(end_time),
            "detail": detail,
            "ds_id": postdata['ds_id'],
            "websitename": "houseforsaleland",
        }

    def boost_post(self, postdata):
        print("in edit")
        # print(postdata)
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        urlpost = "https://www.xn--22c0bihcc9cwhcxj2ui.com"

        editurl = 'https://www.xn--22c0bihcc9cwhcxj2ui.com/process-postfree.php?act=EditPostCheck&pID=' + \
            str(postdata['post_id'])
        with requests.Session() as s:
            r = s.post(editurl, data={'passwordedit': postdata['pass']})
            print(r.text)
        if 'error' in r.text:
            detail = "wrong post id"
            time_end = datetime.datetime.utcnow()
            time_usage = time_end - time_start
            return {
                'websitename': 'houseforsaleland',
                'success': 'False',
                "start_time": str(time_start),
                "end_time": str(time_end),
                "detail": detail,
                "post_view": ""
            }
        url_n = 'https://www.xn--22c0bihcc9cwhcxj2ui.com/process-postfree.php?act=editpostfree&id=' + \
            postdata['post_id']
        with requests.Session() as s:
            r = s.post(url_n)
            detail = r.text
        success = "true"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            'websitename': 'houseforsaleland',
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": "boosted",
            "post_id": postdata['post_id'],
            "post_view": ""
        }


    def edit_post(self, postdata):
        try:
            logid = postdata['log_id']
        except:
            postdata['log_id'] = ""
        print("in edit")
        # print(postdata)
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        urlpost = "https://www.xn--22c0bihcc9cwhcxj2ui.com"

        editurl = 'https://www.xn--22c0bihcc9cwhcxj2ui.com/process-postfree.php?act=EditPostCheck&pID=' + \
            str(postdata['post_id'])
        # postdata['post_description_th']=str(postdata['post_description_th']).replace('\r\n','')
        # postdata['post_description_th']=str(postdata['post_description_th']).replace('\n','')
        with requests.Session() as s:
            r = s.post(editurl, data={'passwordedit': postdata['pass']})
        if 'error' in r.text:
            detail = "wrong post id"
            time_end = datetime.datetime.utcnow()
            time_usage = time_end - time_start
            return {
                'websitename': 'houseforsaleland',
                'success': 'False',
                "start_time": str(time_start),
                "end_time": str(time_end),
                "ds_id": postdata['ds_id'],
                "log_id": postdata['log_id'],
                "post_id": postdata['post_id'],
                "detail": detail
            }
        subcategory = {
            '6': 1,
            '2': 2,
            '3': 2,
            '1': 5,
            '7': 5,
            '5': 4,
            '9': 4,
            '10': 6,
            '4': 3,
            '8': 6,
            '25': 6
        }
        try:
            postdata['cate_id'] = subcategory[str(postdata['property_type'])]
        except:
            return{
                'success': 'false',
                'websitename': 'houseforsaleland',
                'detail': 'wrong propertytype',
                'post_url': '',
                'post_id': '',
                "ds_id": postdata['ds_id'],
                "log_id": postdata['log_id']
            }
        success = "true"
        post_id = ""
        detail = ""
        post_id = ""
        detail = ""
        url_n = ""
        postparams = {
            'acceptBTN': 'Accept all terms and conditions'
        }
        s = requests.Session()
        amphur_id = -1
        finalRegion = ""
        for i in range(1, 7):
            province_id = str(i)
            for (key, value) in provincedata[province_id+"_province"].items():
                if (postdata['addr_province'].strip()).replace(' ', '') in (value.strip()).replace(' ', ''):
                    amphur_id = key
                    finalRegion = str(i)
                    break
            if finalRegion != "":
                break
        if amphur_id == -1 or finalRegion == "":
            return{
                'websitename': 'houseforsaleland',
                'success': 'false',
                'ret': "wrong province",
                "ds_id": postdata['ds_id'],
                "log_id": postdata['log_id'],
                'post_url': "",
                'post_id': ""
            }
        province_id = amphur_id
        postdata['addr_region'] = finalRegion
        amphur_id = ""
        for (key, value) in provinceDistrictdata[province_id+"_province"].items():
            if (postdata['addr_district'].strip()).replace(' ', '') in (value.strip()).replace(' ', ''):
                amphur_id = key
                break

        if amphur_id == "":
            return{
                'websitename': 'houseforsaleland',
                'success': 'false',
                'ret': "wrong amphur id"+str(postdata['addr_district']),
                "ds_id": postdata['ds_id'],
                "log_id": postdata['log_id'],
                'post_url': "",
                'post_id': ""
            }

        prod_address = ""
        for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
            if add is not None and add != "" and add != " ":
                prod_address += add + ","
        prod_address = prod_address[:-1]
        postdata['address'] = prod_address
        s = requests.Session()
        if len(postdata['post_images']) == 0:
            postdata['post_images'] = ['./imgtmp/default/white.jpg']
        if postdata['listing_type'] == '????????????':
            postdata['listing_type'] = '3'
        else:
            postdata['listing_type'] = '2'
        datapost = {
            'type': postdata['listing_type'],
            'category': subcategory[str(postdata['property_type'])],
            'geography': finalRegion,
            'province': province_id,
            'amphur': amphur_id,
            'subject': str(postdata['post_title_th']),
            'detail': str(postdata['post_description_th']),
            'lat': postdata['geo_latitude'],
            'lng': postdata['geo_longitude'],
            'name': postdata['name'],
            'tel': postdata['mobile'],
            'email': postdata['user'],
            'password': postdata['pass'],
            'sendmail': 1
        }
        arr = ["picture"]
        files = {}

        for i in range(len(postdata['post_images'])):
            datapost[arr[i]] = postdata['post_images'][i]
            file =open(postdata['post_images'][i], "rb")
            files[arr[i]] = (postdata['post_images'][i], file, "image/jpeg")
            if i == 0:
                break
        url_n = 'https://www.xn--22c0bihcc9cwhcxj2ui.com/process-postfree.php?act=editpostfree&id=' + \
            str(postdata['post_id'])
        with requests.Session() as s:
            r = s.post(url_n, data=datapost, files=files)
            detail = r.text
        # print(f'detail--->{detail}')
        success = "true"
        url_n = 'https://www.xn--22c0bihcc9cwhcxj2ui.com/process-postfree.php?act=editpostfree&id=' + \
            postdata['post_id']

        options = Options()
        options.headless = True
        options.add_argument('--no-sandbox')
        try:
            driver = webdriver.Chrome("./static/chromedriver", chrome_options=options)

            post_url = urlpost+'/page-postfree-detail.php?pID='+postdata['post_id']
            driver.get(post_url)
            driver.maximize_window()
            # driver.find_element_by_id('btnShowEdit').click()
            jsscript='document.getElementById("btnShowEdit").click()'
            driver.execute_script(jsscript)
            # time.sleep(1)
            jsscript='document.getElementById("passwordedit")["value"]="'+postdata['pass']+'";document.getElementById("submit").click();'
            driver.execute_script(jsscript)
            # time.sleep(1)
            try:
                WebDriverWait(driver, 5).until(EC.alert_is_present(),
                                               'Timed out waiting for PA creation ' +
                                               'confirmation popup to appear.')


            except:
                print('alert not accepted within time')
                time.sleep(3)

            try:
                driver.switch_to.alert.accept()
            except:
                time.sleep(2)
                driver.switch_to.alert.accept()
            time.sleep(5)


            # jsscript='function getElementByXpath(path) {return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;}'
            # jsscript="document.getElementById('type"+postdata['listing_type']+"')['checked']=true;"
            # jsscript+="document.getElementById('sendmail1')['checked']=true;document.querySelectorAll('#category1')["+str(postdata['cate_id'])+"]['checked']=true;"
            # jsscript+="document.getElementById('subject')['value']='"+postdata['post_title_th']+"';"
            # jsscript+="document.getElementById('detail')['value']='';"
            # jsscript+="document.getElementById('name')['value']='"+postdata['name']+"';"
            # jsscript+="document.getElementById('address')['value']='"+prod_address+"';"
            # jsscript+="document.getElementById('tel')['value']='"+postdata['mobile']+"';"
            # jsscript+="document.getElementById('email')['value']='"+postdata['email']+"';"
            # jsscript+="document.getElementById('password')['value']='"+postdata['pass']+"';"
            # # time.sleep(5000)
            # # driver.execute_script(jsscript)
            # driver.find_element_by_id('detail').send_keys(str(postdata['post_description_th']));
            # time.sleep(5000)

            # jsscript = "document.getElementById('detail')['value']='';"
            # jsscript += "document.getElementById('subject')['value']='';"
            # jsscript += "document.getElementById('password')['value']='';"
            # jsscript += "document.getElementById('email')['value']='';"
            # jsscript += "document.getElementById('address')['value']='';"
            # jsscript += "document.getElementById('name')['value']='';"
            # print(f'prod_address--->{prod_address}')
            # driver.execute_script(jsscript)
            # file.close()
            try:
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="detail"]'))
                )
            except:
                print('increase wait time for detail')
            time.sleep(1)
            driver.find_element_by_id('detail').clear()
            driver.find_element_by_id('detail').send_keys(
                str(postdata['post_description_th']))
            driver.find_element_by_id('subject').clear()
            driver.find_element_by_id('subject').send_keys(
                str(postdata['post_title_th']))
            driver.find_element_by_id('password').clear()
            driver.find_element_by_id('password').send_keys(str(postdata['pass']))
            driver.find_element_by_id('email').clear()
            driver.find_element_by_id('email').send_keys(str(postdata['email']))
            driver.find_element_by_id('address').clear()
            driver.find_element_by_id('address').send_keys(str(prod_address))
            driver.find_element_by_id('name').clear()
            driver.find_element_by_id('name').send_keys(str(postdata['name']))
            time.sleep(2)
            driver.find_element_by_id('submit').click()
            time.sleep(5)
            # driver.close()
            # driver.quit()
            # driver.close()

            # driver.quit()
        finally:
            try:
                time.sleep(2)
                alert = driver.switch_to.alert
                alert.accept()
                driver.close()
                driver.quit()
            except:
                try:
                    alert = driver.switch_to.alert
                    alert.accept()
                    driver.close()
                    driver.quit()
                except:
                    pass

        success = "true"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            'websitename': 'houseforsaleland',
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": "Edited ",
            "post_id": postdata['post_id']
        }



    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        tempotempo=postdata
        subcategory = {
            '6': 1,
            '2': 2,
            '3': 2,
            '1': 5,
            '7': 5,
            '5': 4,
            '9': 4,
            '10': 6,
            '4': 3,
            '8': 6,
            '25': 6
        }
        try:
            postdata['cate_id'] = subcategory[str(postdata['property_type'])]
        except:
            return{
                'success': 'false',
                'websitename': 'houseforsaleland',
                'detail': 'wrong propertytype',
                'post_url': '',
                'post_id': '',
                'ds_id': postdata['ds_id']
            }
        success = "true"
        post_id = ""
        detail = ""
        post_id = ""
        detail = ""
        url_n = ""
        postparams = {
            'acceptBTN': 'Accept all terms and conditions'
        }
        # s = requests.Session()
        amphur_id = -1
        finalRegion = ""
        for i in range(1, 7):
            province_id = str(i)
            for (key, value) in provincedata[province_id+"_province"].items():
                if (postdata['addr_province'].strip()).replace(' ', '') in (value.strip()).replace(' ', ''):
                    amphur_id = key
                    finalRegion = str(i)
                    break
            if finalRegion != "":
                break
        if amphur_id == -1 or finalRegion == "":
            return{
                'websitename': 'houseforsaleland',
                'success': 'false',
                'ret': "wrong province",
                'ds_id': postdata['ds_id'],
                'post_url': "",
                'post_id': ""
            }
        province_id = amphur_id
        # postdata['addr_province'] = province_id
        # postdata['addr_region'] = finalRegion
        amphur_id = ""
        for (key, value) in provinceDistrictdata[province_id+"_province"].items():
            if (postdata['addr_district'].strip()).replace(' ', '') in (value.strip()).replace(' ', ''):
                amphur_id = key
                break

        if amphur_id == "":
            return{
                'websitename': 'houseforsaleland',
                'success': 'false',
                'detail': "wrong amphur id"+str(postdata['addr_district']),
                'ds_id': postdata['ds_id'],
                'post_url': "",
                'post_id': ""
            }

        prod_address = ""
        for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
            if add is not None and add != "" and add != " ":
                prod_address += add + ","
        prod_address = prod_address[:-1]
        postdata['address'] = prod_address
        # s = requests.Session()
        if len(postdata['post_images']) == 0:
            postdata['post_images'] = ['./imgtmp/default/white.jpg']
        if postdata['listing_type'] == '????????????':
            postdata['listing'] = '3'
        else:
            postdata['listing'] = '2'
        datapost = {
            'type': postdata['listing'],
            'category': subcategory[str(postdata['property_type'])],
            'geography': finalRegion,
            'province': province_id,
            'amphur': amphur_id,
            'subject': str(postdata['post_title_th'])+'?????????',
            'detail': str(postdata['post_description_th']),
            'lat': postdata['geo_latitude'],
            'lng': postdata['geo_longitude'],
            'name': postdata['name'],
            'tel': postdata['mobile'],
            'email': postdata['user'],
            'password': postdata['pass'],
            'sendmail': 1
        }
        arr = ["picture"]
        files = {}
        for i in range(len(postdata['post_images'])):

            datapost[arr[i]] = postdata['post_images'][i]
            file = open(postdata['post_images'][i], "rb")
            files[arr[i]] = (postdata['post_images'][i],  file, "image/jpeg")

            if i == 0:
                break
        # print(f"files ---> {files}\n"
        #       f"datapost ---> {datapost}\n")
        # captcha!!!
        detail = ""
        s = requests.Session()
        urlpost = "https://www.xn--22c0bihcc9cwhcxj2ui.com"
        r = s.get("https://www.xn--22c0bihcc9cwhcxj2ui.com/post")
        soup = BeautifulSoup(r.content, features = self.parser)
        captchaurl = soup.find('img', attrs={'alt': 'Captcha image'})['src']
        finalurl = urlpost+"/"+captchaurl
        r = s.get(finalurl, stream=True)
        filename = "captcha.png"
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True
            # Open a local file with wb ( write binary ) permission.
            with open(filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
            print('Image sucessfully Downloaded: ', filename)
            time_end = datetime.datetime.utcnow()
        else:
            time_end = datetime.datetime.utcnow()
            print('Image Couldn\'t be retreived')
            return {
                'websitename': 'houseforsaleland',
                "success": 'false',
                'post_url': '',
                'ds_id': postdata['ds_id'],
                "start_time": str(time_start),
                "end_time": str(time_end),
                "detail": "Captcha Image Retrieval failed"
            }
        rc = captcha.imageCaptcha(filename)
        print(rc)
        if rc[0] != -1:
            datapost['code'] = str(rc[1]).upper()
        else:
            time_end = datetime.datetime.utcnow()
            return {
                'websitename': 'houseforsaleland',
                "success": 'false',
                'post_url': '',
                "start_time": str(time_start),
                'ds_id': postdata['ds_id'],
                "end_time": str(time_end),
                "detail": "Captcha fail"
            }

        # post
        url_n = "https://www.xn--22c0bihcc9cwhcxj2ui.com/process-postfree.php?act=addpostfree"
        r = s.post(url_n, data=datapost, files=files)
        content = r.content
        detail = r.text

        data = detail
        success = "true"
        # print(r.content)
        if 'error' in r.text:
            s = requests.Session()
            urlpost = "https://www.xn--22c0bihcc9cwhcxj2ui.com"
            r = s.get("https://www.xn--22c0bihcc9cwhcxj2ui.com/post")
            soup = BeautifulSoup(r.content, features = self.parser)
            captchaurl = soup.find(
                'img', attrs={'alt': 'Captcha image'})['src']
            finalurl = urlpost+"/"+captchaurl
            r = s.get(finalurl, stream=True)
            filename = "captcha.png"
            if r.status_code == 200:
                # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                r.raw.decode_content = True
                # Open a local file with wb ( write binary ) permission.
                with open(filename, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
                print('Image sucessfully Downloaded: ', filename)
                time_end = datetime.datetime.utcnow()
            else:
                time_end = datetime.datetime.utcnow()
                print('Image Couldn\'t be retreived')
                return {
                    'websitename': 'houseforsaleland',
                    "success": "false",
                    'post_url': '',
                    "start_time": str(time_start),
                    "end_time": str(time_end),
                    'ds_id': postdata['ds_id'],
                    "detail": "Captcha Image Retrieval failed"
                }
            r = captcha.imageCaptcha(filename)
            print(r)
            if r[0] != -1:
                datapost['code'] = str(r[1]).upper()
            else:
                time_end = datetime.datetime.utcnow()
                return {
                    'websitename': 'houseforsaleland',
                    "success": 'false',
                    'post_url': '',
                    'ds_id': postdata['ds_id'],
                    "start_time": str(time_start),
                    "end_time": str(time_end),
                    "detail": "Captcha fail"
                }
            # #################################### The part below this is repeated and is same as above ##################################################################################################
            url_n = "https://www.xn--22c0bihcc9cwhcxj2ui.com/process-postfree.php?act=addpostfree"
            r = s.post(url_n, data=datapost, files=files)
            content = r.content
            detail = r.text
            data = detail
            success = "true"
            if 'error' in detail:
                success = "False"
                detail = r.text
                time_end = datetime.datetime.utcnow()
                time_usage = time_end - time_start
                return {
                    'websitename': 'houseforsaleland',
                    "success": success,
                    "start_time": str(time_start),
                    "end_time": str(time_end),
                    'post_url': '',
                    "detail": detail,
                    'ds_id': postdata['ds_id']
                }
            else:
                if 'msg_complete' in r.text:
                    soup = BeautifulSoup(r.content, features = self.parser)
                    var = soup.find('script')
                    i = len("<script>window.parent.msg_complete(1,")
                    post_id = ''
                    var = str(var)
                    # print(var)
                    while var[i] != ')':
                        post_id += var[i]
                        i += 1
                    post_url = urlpost+'/page-postfree-detail.php?pID='+post_id
                    tempotempo['post_id']=post_id
                    r=self.edit_post(tempotempo)
                    time_end = datetime.datetime.utcnow()
                    time_usage = time_end - time_start

                    return {
                        'websitename': 'houseforsaleland',
                        'success': 'true',
                        "start_time": str(time_start),
                        "end_time": str(time_end),
                        'detail': "Post created successfully",
                        'post_url': post_url,
                        'post_id': str(int(post_id)),
                        'ds_id': postdata['ds_id']
                    }
                else:
                    success = "False"
        else:
            if 'msg_complete' in r.text:
                soup = BeautifulSoup(r.content, features = self.parser)
                var = soup.find('script')
                i = len("<script>window.parent.msg_complete(1,")
                post_id = ''
                var = str(var)

                while var[i] != ')':
                    post_id += var[i]
                    i += 1
                post_url = urlpost+'/page-postfree-detail.php?pID='+post_id
                tempotempo['post_id']=post_id

                r=self.edit_post(tempotempo)


                time_end = datetime.datetime.utcnow()
                time_usage = time_end - time_start
                return {
                    'websitename': 'houseforsaleland',
                    'success': 'true',
                    'detail': "Post created successfully",
                    "start_time": str(time_start),
                    "end_time": str(time_end),
                    'post_url': post_url,
                    'post_id': str(int(post_id)),
                    'ds_id': postdata['ds_id']
                }
            else:
                success = "False"
                time_end = datetime.datetime.utcnow()
                time_usage = time_end - time_start

        return {
            'websitename': 'houseforsaleland',
            "success": success,
            "start_time": str(time_start),
            "end_time": str(time_end),
            'post_url': '',
            "detail": "Failed to Create Post",
            'ds_id': postdata['ds_id']
        }



    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        success = "true"
        detail = ""
        editurl = 'https://www.xn--22c0bihcc9cwhcxj2ui.com/process-postfree.php?act=EditPostCheck&pID=' + \
            str(postdata['post_id'])
        with requests.Session() as s:
            r = s.post(editurl, data={'passwordedit': postdata['pass']})
        if 'error' in r.text:
            detail = "wrong post id"
            time_end = datetime.datetime.utcnow()
            time_usage = time_end - time_start
            return {
                'websitename': 'houseforsaleland',
                'success': 'False',
                "start_time": str(time_start),
                "end_time": str(time_end),
                "detail": detail,
                "ds_id": postdata['ds_id'],
                "log_id": postdata['log_id'],
                "post_id": postdata['post_id']
            }
        if success == "true":
            urlpost = "https://www.xn--22c0bihcc9cwhcxj2ui.com/process-postfree.php"
            params = (
                ('act', 'deletepost'),
                ('pID', str(postdata['post_id'])),
            )

            data = {
                'passwordinput': postdata['pass'],
                'submit': '%B5%A1%C5%A7'
            }
            with requests.Session() as s:
                r = s.post(urlpost, data=data, params=params)
            data = r.text
            if 'error' in r.text:
                success = "false"
                detail = "Failed to deleted"
            else:
                detail = "Successfully deleted"
        else:
            success = "false"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            'websitename': 'houseforsaleland',
            "success": success,
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": postdata['post_id']
        }

    def search_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        log_id = postdata['log_id']

        #
        #
        #

        time_end = datetime.datetime.utcnow()
        return {
            "websitename": "houseforsaleland",
            "success": "false",
            "post_found": "false",
            "time_usage": time_end - time_start,
            "start_time": time_start,
            "end_time": time_end,
            "detail": "Search Post is not possible, since no registration",
            'ds_id': postdata['ds_id'],
            "log_id": log_id,
        }



# obj = houseforsaleland()

# postdata=dict(
#     post_id='377743435234',
#     password='12345678'
# )

# postdata = {
#     'post_id': '200833',
#     'property_type': '3',
#     'post_title_th': 'DDDhgfdj',
#     'post_description_th': 'f????????? ??????????????? watermark ???????????????????????????????????????????????? 105 ?????????. 2 ????????? 2 ????????? ???????????? 33 ????????? ??????????????? ????????? ??????????????? Fully furnished :: ?????????????????????????????????????????? :: - ???????????? 105 ?????????. - ???????????? 2 ????????????????????? 2 ????????????????????? - ??????????????? 1 ???????????? 33 - ???????????????????????????????????????????????? ??????????????? ????????? ??????????????? :: ??????????????????????????????????????????????????? :: - ?????????????????????????????????: watermark ???????????????????????????????????????????????? Project Owner: Major Development Project Area: 11 Rai Number of building: 2 52 floors 486 units :: ???????????????????????????????????????????????? :: - Senan fest: 1.2 km - icon SIAM : 2km ???????????????: http://maps.google.com/maps?q=13.710968,100.498459 ????????????: 13,900,000 ????????? ??????????????????????????????: NADECHAuto 0852546523 Line: Pokajg #??????????????????????????????????????????????????? ',
#     "addr_province": "???????????????????????????????????????",
#     "addr_district": "?????????????????????",
#     "addr_sub_district": "?????????????????????",
#     "addr_soi": "",
#     "addr_nearby": "",
#     "addr_road": "",
#     "geo_latitude": "12",
#     "geo_longitude": "12",
#     'listing_type': '',
#     'land_size_rai': '5234',
#     'land_size_wa': '5234',
#     'land_size_ngan': '5234',
#     'name': 'temptemp',
#     'pass': '12345678',
#     'mobile': '523452',
#     'email':'temp@gmail.com',
#     'price_baht': '234523',
#     'user': 'temp@gmail.com',
#     'post_images': ['../Desktop/download.jpeg']
# }
# r = obj.create_post(postdata)
# r = obj.edit_post(postdata)
# r = obj.delete_post(postdata)
# print(r)
