from .lib_httprequest import *
from .lib_captcha import *
from bs4 import BeautifulSoup, Tag
import datetime
import sys
import json
import requests
import urllib.request
import re
import shutil



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
        detail = ""
        device_id = ""
        mem_id = ""
        mem_status = False
        success = False
        
        r = self.httprequestObj.http_post(url, data=data_login)
        if r.text == 'ไม่พบข้อมูลสมาชิกค่ะ':
            detail = 'ไม่พบข้อมูลสมาชิกค่ะ'
        else:
            r = self.httprequestObj.http_get("http://www.bkkland.com/member")
            print(r.status_code)
            soup_web = BeautifulSoup(r.content,'lxml')
            if soup_web:
                try:
                    verify = soup_web.find("div", attrs={"class":"personal_info"}).text
                except:
                    pass
                if postdata['user'] in verify.split():
                    success = True
                    mem_status = True
                    detail = "เข้าสู่ระบบสำเร็จ"
                else:
                    detail = "เข้าสู่ระบบล้มเหลว"

                

        # 
        # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
        "websitename": self.webname,
        "usage_time": str(time_usage),
        "start_time": str(time_start),
        "end_time": str(time_end),
        "success": success,
        "detail": detail,
        'device_id': device_id,
        'mem_id': mem_id,
        'mem_status': mem_status,
        "ds_id": postdata['ds_id']
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


        detail = ""
        success = False
        if res.status_code == 200:
            soup = BeautifulSoup(res.content,'lxml')
            for hit in soup.find_all("p", attrs={"class":"comment"}):
                soup_ele = BeautifulSoup(str(hit), self.parser)
                detail = soup_ele.find("p", attrs={"class":"comment"}).text
                if detail == "อีเมล์ นี้มีคนใช้แล้วค่ะ":
                    success = False
                elif detail == "ชื่อสมาชิก นี้มีคนใช้แล้วค่ะ":
                    success = False

        self.test_login(postdata)
        r = self.httprequestObj.http_get("http://www.bkkland.com/member")
        print(r.status_code)
        soup = BeautifulSoup(r.content,'lxml')
        find_member = soup.find("div", attrs={"class":"personal_info"}).text
        if find_member != []:
            if postdata['user'] in find_member.split():
                success = True
        

        # 
        # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": self.webname,
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            'ds_id': postdata['ds_id'],
            "detail": detail,
    }



    def datapost_details(self, postdata, url_capcha):


        pd_condition = {
            'ขาย':'1', 
            'เช่า':'2', 
            'ซื้อ':'3', 
        }

        pd_properties = {
                '1' : '5', # condo
                '2' : '2', # house
                '3' : '3', # townhouse
                '4' : '3', # townhome
                '5' : '4', # building
                '6' : '1', # land
                '7' : '5', # apartment
                '8' : '5', # hotel
                '9' : '6', # office
                '10' : '6', # warehouse
                '25' : '6' # factory
                # '8' : '6', # hotel
            }


        land_area = ""

        rai = "{}ไร่".format(postdata['land_size_rai'])
        ngan = "{}งาน".format(postdata['land_size_ngan'])
        wa = "{}วา".format(postdata['land_size_wa'])
        sqm = "{}ตรม.".format(postdata['floorarea_sqm'])

        if postdata['property_type'] == '1' or postdata['property_type'] == '7':
            land_area = "{}".format(sqm)
        else:
            if postdata['floorarea_sqm'] != "":
                land_area += " "+sqm
            
            if postdata['land_size_wa'] != "":
                land_area += " "+wa

            if postdata['floorarea_sqm'] == "" and postdata['land_size_wa'] == "":
                if postdata['land_size_rai'] != "":
                    land_area += " "+rai

                if postdata['land_size_ngan'] != "":
                    land_area += " "+ngan
            
            else:
                land_area = "0"

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

        postdata['captcha'] = ""  
        if url_capcha == "http://www.bkkland.com/post/form":
            r = self.httprequestObj.http_get(url_capcha)
            if r.status_code==200:
                soup = BeautifulSoup(r.text, features=self.parser)
                img_url = soup.find_all('img')
                for link in img_url:
                    link_cap = link.get("src")
                    # if web is captcha get img and process
                    if link_cap == "http://www.bkkland.com/post/captcha":
                        captcha_img = self.httprequestObj.http_get(link_cap, stream=True)
                
                path_img = os.getcwd() + '/imgtmp/imagecaptcha.jpg'
                with open(path_img,'wb') as local_file :
                    for block in captcha_img.iter_content(1024):
                        if not block:
                            break
                        local_file.write(block)
                
                g_response = captcha.imageCaptcha(path_img)
                if g_response[0]==1:
                    postdata['captcha'] = g_response[1]
                else:
                    postdata['captcha'] = g_response

            os.remove(path_img)

        # replace : space and break the line
        post_title_th = ' '.join(postdata['post_title_th'].split())
        des_re = postdata['post_description_th'].replace("\r\n", "<p>&nbsp;</p>")

        datapost = {
            'f_topic' : (None, post_title_th),
            'f_condition' : (None, int(pd_condition[str(postdata['listing_type'])])),
            'f_typepost' : (None, int(pd_properties[str(postdata['property_type'])])),
            'f_province' : (None, province_id),
            'f_amphur' : (None, amphur_id),
            'f_district' : (None, ""),
            'f_land_area' : (None, land_area),
            'f_price_accept' : (None, "Y"),
            'f_price' : (None, postdata['price_baht']),
            'f_pricetype' : (None, "1"),
            'f_journey' : (None, postdata['addr_soi']+postdata['addr_road']+postdata['addr_near_by']),
            'f_mhtml' : (None, des_re),
            'f_picfake1' : (None, "fakepath"),
            'picfile1' : (None, ""),
            'f_captcha' : (None, postdata['captcha']),
            'process' : (None, ""),
            'lat_value' : (None, postdata['geo_latitude']),
            'lon_value' : (None, postdata['geo_longitude']),
            'f_name' : (None, postdata['name']),
            'f_phone' : (None, postdata['mobile']),
            'f_email' : (None, postdata['email']),
        }

        return datapost

    def re_lastname_imgs(self, postdata):
        for img in postdata['post_images']:
            shutil.move(img, img+".jpg")

    def pull_imgs(self, postdata):
        files = {}
        allimages = []
        # try:
        for count in range(len(postdata["post_img_url_lists"])):
            link = postdata["post_img_url_lists"][count]
            path = os.getcwd()+"/imgtmp/"+"photo_{}.jpg".format(count+1)
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

        if test_login['success'] != True:
            return test_login

        url = "http://www.bkkland.com/post/add"
        payload = self.datapost_details(postdata, 'http://www.bkkland.com/post/form')
        payload['process'] = "post_add"

        files = {}
        
        try:
            # on web upload .jpg only
            self.re_lastname_imgs(postdata)
            for i in range(len(postdata['post_images'])):
                path_img = os.getcwd()+"/"+postdata['post_images'][i]+".jpg"
                r = open(path_img, 'rb')
                name = "photo{}".format(i+1)
                files[name] = ("{}".format(path_img),r,"image/jpeg")

            r = self.httprequestObj.http_post(url, data=payload, files=files)
            for f in postdata['post_images']:
                os.remove(f+".jpg")
        except:
            files, path_imgs = self.pull_imgs(postdata)
            r = self.httprequestObj.http_post(url, data=payload, files=files)
            for f in path_imgs:
                os.remove(f)
    
        success = False
        post_id = ""
        post_url = ""
        detail = "post fail"
        res_complete = self.httprequestObj.http_get("http://www.bkkland.com/post/your_list")
        soup = BeautifulSoup(res_complete.text, self.parser)
        # loop find all title post (first page)
        for hit in soup.find_all("a", attrs={"class":"link_blue14_bu"}):
            soup_ele = BeautifulSoup(str(hit), self.parser)
            title = soup_ele.find("a", attrs={"class":"link_blue14_bu"})

            post_title = ' '.join(postdata['post_title_th'].split())
            name = title.text.replace(" ", "")
            title_post = post_title.replace(" ", "")

            if name == title_post:
                post_url = soup_ele.find("a", attrs={"class":"link_blue14_bu"})['href']
                post_id = re.findall("\d+", post_url)[0]
                detail = "post complete."
                success = True
                break
            else:
                post_url = soup_ele.find("a", attrs={"class":"link_blue14_bu"})['href']
                post_id = re.findall("\d+", post_url)[0]
                res = self.httprequestObj.http_get(post_url)
                if res.status_code == 200:
                    detail = "Post Found"
                    success = True
                    break

        
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
        "success": success,
        "websitename": self.webname,
        "usage_time": str(time_usage),
        "start_time": str(time_start),
        "end_time": str(time_end),
        "post_url": post_url,
        "post_id": post_id,
        "account_type": "null",
        "detail": detail,
    }


    def delete_post(self, postdata):
        self.logout_user()
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)

        if test_login['success'] == True:
            url = 'http://www.bkkland.com/post/update'
            payload = {
                'f_checked[]' : postdata["post_id"],
                'process' : "table_form",
                'edittype' : "ลบ"
            }
            r = self.httprequestObj.http_post(url, data=payload)

        success = False
        url_post = ""
        detail = ""
        res_post = self.httprequestObj.http_get("http://www.bkkland.com/post/your_list")
        soup = BeautifulSoup(res_post.text, self.parser)
        # loop find all title post (first page)
        search_post = None
        for hit in soup.find_all("a", attrs={"class":"link_blue14_bu"}):
            search_post = "found"
            soup_ele = BeautifulSoup(str(hit), self.parser)
            try:
                url_post = soup_ele.find("a", attrs={"class":"link_blue14_bu"})['href']
                postdata = re.findall("\d+", url_post)[0]
                if postdata:
                    detail = "delete False"
                    success = False
            except:
                url_post = soup_ele.find("a", attrs={"class":"link_blue14_bu"})['href']
                postdata = re.findall("\d+", url_post)[0]
                print(type(postdata), type(postdata['post_id']))
                if postdata == postdata['post_id']:
                    detail = "delete complete - post_id : {}".format(postdata)
                    success = True
        
        if search_post == None:
            for hit in soup.find_all("td", attrs={"colspan":"6"}):
                soup_ele = BeautifulSoup(str(hit), self.parser)
                detail = soup_ele.text
                success = True
        else:
            if url_post:
                detail = "post_id wrong!"
            else:
                detail = "error"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            'ds_id': "",
            'url' : url_post,
            "detail": detail,
            "websitename": self.webname,
        }

    def edit_post(self,postdata):
        self.logout_user()
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)

        success = False
        post_id = ""
        post_url = ""
        detail = ""
        if test_login['success'] == True:
            count_page = 1
            post_id = ""
            while count_page < 35:
                url_check_title = "http://www.bkkland.com/post/your_list?page={}".format(str(count_page))
                print(url_check_title)
                res_complete = self.httprequestObj.http_get(url_check_title)
                soup = BeautifulSoup(res_complete.text, self.parser)
                # loop find all title post (first page)
                for hit in soup.find_all("a", attrs={"class":"link_blue14_bu"}):
                    soup_ele = BeautifulSoup(str(hit), self.parser)
                    title = soup_ele.find("a", attrs={"class":"link_blue14_bu"})

                    post_title = ' '.join(postdata['post_title_th'].split())
                    name = title.text.replace(" ", "")
                    title_post = post_title.replace(" ", "")


                    if name == title_post:
                        post_url = soup_ele.find("a", attrs={"class":"link_blue14_bu"})['href']
                        post_id = re.findall("\d+", post_url)[0]
                        detail = "Post Found"
                        success = True
                        break
                    else:
                        post_url = soup_ele.find("a", attrs={"class":"link_blue14_bu"})['href']
                        post_id = re.findall("\d+", post_url)[0]
                        res = self.httprequestObj.http_get(post_url)
                        if res.status_code == 200:
                            detail = "Post Found"
                            success = True
                            break
                    
                count_page += 1
                if success == True:
                    break

            

            # start edit_post            
            url_edit = 'http://www.bkkland.com/post/form/edit?id={}'.format(post_id)
            url_api = 'http://www.bkkland.com/post/update'
            payload = self.datapost_details(postdata, url_edit)
            payload['process'] = "edit_post"
            payload["post_id"] = post_id
            payload["f_activated"] = (None, "Y")
            payload["go"] = (None, "แก้ไขประกาศ")

            r = self.httprequestObj.http_post_with_headers(url_api, data=payload)
            print(r.status_code)

            success = False
            detail = ""
            url_update = 'http://www.bkkland.com/post/form/edit?id={}&status=update_complete'.format(post_id)
            res_complete = self.httprequestObj.http_get(url_update)
            soup = BeautifulSoup(res_complete.text, self.parser)
            for hit in soup.find_all("script", attrs={"type":"text/javascript"}):
                soup_ele = BeautifulSoup(str(hit), self.parser)
                try:
                    text_update = soup_ele.find("script", attrs={"type":"text/javascript"})
                    mystr = str(text_update)
                    # if != -1 is finded
                    if mystr.find("อัพเดทประกาศเรียบร้อยค่ะ") != -1:
                        detail = "update complete - post_id : {}".format(post_id)
                        success = True

                except:
                    detail = "update False"
                    success = False

    

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "websitename": self.webname,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
        }

    def boost_post(self, postdata):
        self.logout_user()
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)


        if test_login['success'] == True:
            url_form = 'http://www.bkkland.com/post/form/edit?id={}'.format(postdata['post_id'])
            url_api = 'http://www.bkkland.com/post/update'
            payload = self.datapost_details(postdata, url_form)
            payload['process'] = "edit_post"
            payload["post_id"] = postdata['post_id']
            payload["f_activated"] = (None, "Y")
            payload["go"] = (None, "แก้ไขประกาศ")

            r = self.httprequestObj.http_post_with_headers(url_api, data=payload)
            print(r.status_code)

            success = False
            detail = ""
            url_update = 'http://www.bkkland.com/post/form/edit?id={}&status=update_complete'.format(postdata['post_id'])
            res_complete = self.httprequestObj.http_get(url_update)
            soup = BeautifulSoup(res_complete.text, self.parser)
            for hit in soup.find_all("script", attrs={"type":"text/javascript"}):
                soup_ele = BeautifulSoup(str(hit), self.parser)
                try:
                    text_update = soup_ele.find("script", attrs={"type":"text/javascript"})
                    mystr = str(text_update)
                    # if != -1 is finded
                    if mystr.find("อัพเดทประกาศเรียบร้อยค่ะ") != -1:
                        detail = "update complete"
                        success = True

                except:
                    detail = "update False"
                    success = False

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": time_usage,
            "start_time": time_start,
            "end_time": time_end,
            "detail": detail,
            "log_id": postdata['log_id'],
            "ds_id": postdata['ds_id'],
            "post_id": postdata['post_id'],
            "websitename": self.webname,
            "post_view": ''
        }

    def search_post(self, postdata):
        self.logout_user()
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)

        success = False
        detail = "post not found"
        post_url = ""
        ds_id = ""
        log_id = ""
        if test_login['success'] == True:
            count_page = 1
            post_id = ""
            while count_page < 35:
                url_check_title = "http://www.bkkland.com/post/your_list?page={}".format(str(count_page))
                res_complete = self.httprequestObj.http_get(url_check_title)
                soup = BeautifulSoup(res_complete.text, self.parser)
                # loop find all title post (first page)
                for hit in soup.find_all("a", attrs={"class":"link_blue14_bu"}):
                    soup_ele = BeautifulSoup(str(hit), self.parser)
                    title = soup_ele.find("a", attrs={"class":"link_blue14_bu"})

                    post_title = ' '.join(postdata['post_title_th'].split())
                    name = title.text.replace(" ", "")
                    title_post = post_title.replace(" ", "")

                    if name == title_post:
                        post_url = soup_ele.find("a", attrs={"class":"link_blue14_bu"})['href']
                        post_id = re.findall("\d+", post_url)[0]
                        detail = "Post Found"
                        success = True
                        try:
                            ds_id = postdata['ds_id']
                            log_id = postdata['log_id']
                        except:
                            pass
                        break
                    else:
                        post_url = soup_ele.find("a", attrs={"class":"link_blue14_bu"})['href']
                        post_id = re.findall("\d+", post_url)[0]
                        res = self.httprequestObj.http_get(post_url)
                        if res.status_code == 200:
                            detail = "Post Found"
                            success = True
                            break
                count_page += 1
                if success == True:
                    break

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": self.webname,
            "account_type": None,
            "ds_id": ds_id,
            "log_id": log_id,
            "post_id": post_id,
            "post_created": '',
            "post_modified": time_end,
            "post_view": "",
            "post_url": post_url
        }
