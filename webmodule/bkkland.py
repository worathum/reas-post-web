from .lib_httprequest import *
from .lib_captcha import *
from bs4 import BeautifulSoup
import datetime
import sys
import json
import requests
import urllib.request



captcha = lib_captcha()

with open("./static/bkkland_province.json",encoding = 'utf-8') as f:
    provincedata = json.load(f)

class bkkland():

    name = 'bkkland'

    def __init__(self):

        try:
            import configs

        except ImportError:
            configs = {}

        self.httprequestObj = lib_httprequest()
        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.debug = 1
        self.debugresdata = 0
        self.parser = 'html.parser'
        self.webname = 'bkkland'

    def print_debug(self, msg):
        if self.debug == 1:
            print(msg)
        return True


    def logout_user(self):
        url = "http://www.bkkland.com/auth/logout"
        self.httprequestObj.http_get(url)


    def test_login(self, postdata):

        self.logout_user()
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        url = "http://www.bkkland.com/auth/login"
        data_login = {
            'f_login_email' : postdata['user'],
            'f_login_pass' : postdata['pass'],
            'process' : 'login'
        }

        # start process
        #
        
        r = self.httprequestObj.http_post(url, data=data_login)
        print(r.status_code)

        r = self.httprequestObj.http_get("http://www.bkkland.com/member")
        print(r.status_code)

        detail = ""
        login_success = False
        soup_web = BeautifulSoup(r.content,'lxml')
        if soup_web:
            try:
                verify = soup_web.find("div", attrs={"class":"personal_info"}).text
            except:
                pass
            if postdata['user'] in verify.split():
                login_success = True
                

        # 
        # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": self.webname,
            "success": login_success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
        }

    def register_details(self, postdata):
        register_data = {}

        register_data["f_email"] = postdata["user"]
        register_data["f_pass"] = postdata["pass"]
        register_data["f_phone"] = postdata["tel"]
        register_data["f_name"] = postdata['name_en']
        register_data["process"] = "register"
        register_data["go"] = 'สมัครโลด !'

        return register_data

    def register_user(self, postdata):
        self.logout_user()
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        data_register = self.register_details(postdata)

        res = self.httprequestObj.http_post_with_headers('http://www.bkkland.com/auth/register/add', data=data_register)
        print(res.status_code)


        comment = ""
        register_success = False
        if res.status_code == 200:
            soup = BeautifulSoup(res.content,'lxml')
            for hit in soup.find_all("p", attrs={"class":"comment"}):
                soup_ele = BeautifulSoup(str(hit), self.parser)
                comment = soup_ele.find("p", attrs={"class":"comment"}).text
                if comment == "อีเมล์ นี้มีคนใช้แล้วค่ะ":
                    register_success = False
                elif comment == "ชื่อสมาชิก นี้มีคนใช้แล้วค่ะ":
                    register_success = False

        try:
            self.test_login(postdata)
            r = self.httprequestObj.http_get("http://www.bkkland.com/member")
            print(r.status_code)
            soup = BeautifulSoup(r.content,'lxml')
            verify = soup.find("div", attrs={"class":"personal_info"}).text
            if verify != []:
                if postdata['user'] in verify.split():
                    register_success = True
                    comment = "สมัครสมาชิกสำเร็จแล้วค่ะ"
        except:
            comment = "Error"



        # 
        # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": self.webname,
            "success": register_success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": comment,
        }

    def datapost_details(self, postdata):


        pd_condition = {
            'ขาย':'1', 
            'เช่า':'2', 
            'ซื้อ':'3', 
        }

        pd_properties = {
                'land':'1', 
                'house':'2', 
                'townhouse':'3', 
                'building':'4', 
                'condo':'5', 
                'office':'6', 
            }

        province_id = ''
        amphur_id = ''

        for (key, value) in provincedata.items():
            if type(value) is str and postdata['addr_province'].strip() in value.strip():
                province_id = key
                break

        for (key, value) in provincedata[province_id+"_province"].items():
                if postdata['addr_district'].strip() in value.strip() or value.strip() in postdata['addr_district'].strip():
                    amphur_id = key
                    break

        r = self.httprequestObj.http_get('http://www.bkkland.com/post/form')
        if r.status_code==200:
            soup = BeautifulSoup(r.text, features=self.parser)
            img_url = soup.find_all('img')
            for link in img_url:
                # if web is captcha get img and process
                if str(link) == '''<img src="http://www.bkkland.com/post/captcha"/>''':
                    captcha_img = self.httprequestObj.http_get("http://www.bkkland.com/post/captcha", stream=True)
            
            path_img = os.getcwd() + '/imgtmp/Img_Captcha/imagecaptcha.jpg'
            with open(path_img,'wb') as local_file :
                for block in captcha_img.iter_content(1024):
                    if not block:
                        break
                    local_file.write(block)
            
            g_response = captcha.imageCaptcha(path_img)
            if g_response[0]==1:
                postdata['captcha'] = g_response[1]
                os.remove(path_img)

        datapost = {
            'f_topic' : (None, postdata['post_title_th']),
            'f_condition' : (None, int(pd_condition[str(postdata['listing_type'])])),
            'f_typepost' : (None, int(pd_properties[str(postdata['property_type'])])),
            'f_province' : (None, province_id),
            'f_amphur' : (None, amphur_id),
            'f_district' : (None, ""),
            'f_land_area' : (None, postdata['land_size_wa']),
            'f_price_accept' : (None, "Y"),
            'f_price' : (None, postdata['price_baht']),
            'f_pricetype' : (None, "1"),
            'f_journey' : (None, postdata['addr_soi']+postdata['addr_road']+postdata['addr_near_by']),
            'f_mhtml' : (None, postdata['post_description_th']),
            'f_picfake1' : (None, "fakepath"),
            'picfile1' : (None, ""),
            'f_captcha' : (None, postdata['captcha']),
            'process' : (None, "post_add"),
            'lat_value' : (None, postdata['geo_latitude']),
            'lon_value' : (None, postdata['geo_longitude']),
            'f_name' : (None, postdata['name']),
            'f_phone' : (None, postdata['tel']),
            'f_email' : (None, postdata['email']),

        }

        return datapost


    def pull_imgs(self, postdata):
        files = {}
        allimages = []
        # try:
        for count in range(len(postdata["post_img_url_lists"])):
            link = postdata["post_img_url_lists"][count]
            path = os.getcwd()+"/imgtmp/img_upload/"+"photo_{}.jpg".format(count+1)
            img_data = requests.get(link).content
            with open(path, 'wb') as handler:
                handler.write(img_data)
            allimages.append(path)

        # except:
        #     allimages = os.getcwd()+postdata["post_images"]

        for i in range(len(allimages)):
            r = open(allimages[i], 'rb')
            name = 'photo{}'.format(i+1)
            files[name] = ("{}".format(allimages[i]),r,"image/jpeg")
        
        return files, allimages
        

    def create_post(self, postdata):
        self.logout_user()
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)

        if test_login['success'] == True:
            url = "http://www.bkkland.com/post/add"
            payload = self.datapost_details(postdata)
            files, path_imgs = self.pull_imgs(postdata)
            print(files)
            r = self.httprequestObj.http_post(url, data=payload, files=files)
            for f in path_imgs:
                os.remove(f)
            print(r.status_code)

        success = False
        url_post = ""
        res_complete = self.httprequestObj.http_get("http://www.bkkland.com/post/your_list?status=add_complete")
        soup = BeautifulSoup(res_complete.text, self.parser)
        # loop find all title post (first page)
        for hit in soup.find_all("a", attrs={"class":"link_blue14_bu"}):
            soup_ele = BeautifulSoup(str(hit), self.parser)
            title = soup_ele.find("a", attrs={"class":"link_blue14_bu"}).text

            if title == postdata['post_title_th']:
                url_post = soup_ele.find("a", attrs={"class":"link_blue14_bu"})['href']
                success = True

        detail = ""
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            'ds_id': postdata['ds_id'],
            'url' : url_post,
            "detail": detail,
            "websitename": self.webname,
        }

    def edit_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)

        if test_login['success'] == True:
            url = '''http://www.bkkland.com/post/form/edit?id={}'''.format(postdata['post_id'])
            payload = self.datapost_details(postdata)

