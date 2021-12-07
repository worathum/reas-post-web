from .lib_httprequest import *
import datetime
import sys


class trovit():

    name = 'trovit'

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
        self.webname = 'trovit'

    def print_debug(self, msg):
        if self.debug == 1:
            print(msg)
        return True

    def logout_user(self):
        url = "https://th.trovit.com/baan/index.php/cod.logout"
        self.httprequestObj.http_get(url)

    def register_details(self, postdata):
        register_data = {}

        register_data["email"] = postdata["user"]
        register_data["password"] = postdata["pass"]
        register_data["password2"] = postdata["pass"]
        register_data["terms"] = "on"

        return register_data

    def register_user(self, postdata):
        self.logout_user()
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        # start process
        #
        data_register = self.register_details(postdata)


        res = self.httprequestObj.http_post('https://accounts.trovit.com/?cod=create_user&url=https%3A%2F%2Fth.trovit.com%2Fbaan%2Findex.php%2Fcod.mail_preferences&language=th_TH&', data=data_register)

        detail = ""
        register_success = False
        soup_web = BeautifulSoup(res.text, "html5lib")
        if soup_web:
            verify_register = soup_web.find("p", attrs={"class":"before_form"}).text
            if verify_register == "อีเมลนี้ใช้ในการสมัครแล้ว คุณสามารลงชื่อเข้าใช้ได้ที่นี่":
                register_success = True

        # 
        # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "trovit",
            "success": register_success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
        }

    def test_login(self, postdata):
        self.logout_user()
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        url = "https://accounts.trovit.com/?cod=check_login&url=https%3A%2F%2Fth.trovit.com%2Fbaan%2Findex.php%2Fcod.mail_preferences&language=th_TH&"

        time_start = datetime.datetime.utcnow()

        data_login = {
            'email' : postdata['user'],
            'password' : postdata['pass']
        }

        r = self.httprequestObj.http_post(url, data=data_login)
        print(r.status_code)

        detail = ""
        success = False
        soup = BeautifulSoup(r.text, self.parser)
        verify_login = soup.find("span", attrs={"class":"account-button-text header-option-button-text"}).text
        if verify_login == "บัญชี":
            success = True

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            'ds_id': postdata['ds_id'],
            "detail": detail,
            "websitename": self.webname,
        }


    def postdata_handle(self, postdata):
        #log.debug('')
        if self.handled == True:
            return postdata

        datahandled = {}

        # "SALE", "RENT", "OPT" ขาย ให้เช่า ขายดาวน์
        try:
            datahandled['listing_type'] = postdata['listing_type']
        except KeyError as e:
            datahandled['listing_type'] = "SALE"
            #log.warning(str(e))
        if datahandled['listing_type'] == "เช่า":
            datahandled['listing_type'] = "RENT"
        elif datahandled['listing_type'] == "ขายดาวน์":
            datahandled['listing_type'] = "OPT"
        else:
            datahandled['listing_type'] = "SALE"

        # "CONDO","BUNG","TOWN","LAND","APT","RET","OFF","WAR","BIZ","SHOP"]
        try:
            datahandled['property_type'] = postdata['property_type']
        except KeyError as e:
            datahandled['property_type'] = "CONDO"
            #log.warning(str(e))
        if datahandled['property_type'] == '2' or datahandled['property_type'] == 2 or datahandled['property_type'] == "บ้านเดี่ยว":
            datahandled['property_type'] = "BUNG"
        elif datahandled['property_type'] == '3' or datahandled['property_type'] == 3 or datahandled['property_type'] == "บ้านแฝด":
            datahandled['property_type'] = "BUNG"
        elif datahandled['property_type'] == '4' or datahandled['property_type'] == 4 or datahandled['property_type'] == "ทาวน์เฮ้าส์":
            datahandled['property_type'] = "TOWN"
        elif datahandled['property_type'] == '5' or datahandled['property_type'] == 5 or datahandled['property_type'] == "ตึกแถว-อาคารพาณิชย์":
            datahandled['property_type'] = "SHOP"
        elif datahandled['property_type'] == '6' or datahandled['property_type'] == 6 or datahandled['property_type'] == "ที่ดิน":
            datahandled['property_type'] = "LAND"
        elif datahandled['property_type'] == '7' or datahandled['property_type'] == 7 or datahandled['property_type'] == "อพาร์ทเมนท์":
            datahandled['property_type'] = "APT"
        elif datahandled['property_type'] == '8' or datahandled['property_type'] == 8 or datahandled['property_type'] == "โรงแรม":
            datahandled['property_type'] = "BIZ"
        elif datahandled['property_type'] == '9' or datahandled['property_type'] == 9 or datahandled['property_type'] == "ออฟฟิศสำนักงาน":
            datahandled['property_type'] = "OFF"
        elif datahandled['property_type'] == '10' or datahandled['property_type'] == 10 or datahandled['property_type'] == "โกดัง":
            datahandled['property_type'] = "WAR"
        elif datahandled['property_type'] == '25' or datahandled['property_type'] == 25 or datahandled['property_type'] == "โรงงาน":
            datahandled['property_type'] = "WAR"
        else:
            datahandled['property_type'] = "CONDO"

        try:
            datahandled['post_img_url_lists'] = postdata['post_img_url_lists']
        except KeyError as e:
            datahandled['post_img_url_lists'] = {}
            #log.warning(str(e))

        try:
            datahandled['price_baht'] = postdata['price_baht']
        except KeyError as e:
            datahandled['price_baht'] = 0
            #log.warning(str(e))

        try:
            datahandled['addr_province'] = postdata['addr_province']
        except KeyError as e:
            datahandled['addr_province'] = ''
            #log.warning(str(e))

        try:
            datahandled['addr_district'] = postdata['addr_district']
        except KeyError as e:
            datahandled['addr_district'] = ''
            #log.warning(str(e))

        try:
            datahandled['addr_sub_district'] = postdata['addr_sub_district']
        except KeyError as e:
            datahandled['addr_sub_district'] = ''
            #log.warning(str(e))

        try:
            datahandled['addr_road'] = postdata['addr_road']
            if datahandled['addr_road'] == None:
                datahandled['addr_road'] = ""
        except KeyError as e:
            datahandled['addr_road'] = ''
            #log.warning(str(e))

        try:
            datahandled['addr_near_by'] = postdata['addr_near_by']
        except KeyError as e:
            datahandled['addr_near_by'] = ''
            #log.warning(str(e))

        try:
            datahandled['addr_postcode'] = postdata['addr_postcode']
        except KeyError as e:
            datahandled['addr_postcode'] = ''
            #log.warning(str(e))

        try:
            datahandled['floor_area'] = postdata['floor_area']
        except KeyError as e:
            datahandled['floor_area'] = '0'
            #log.warning(str(e))

        try:
            datahandled['geo_latitude'] = str(postdata['geo_latitude'])
        except KeyError as e:
            datahandled['geo_latitude'] = ''
            #log.warning(str(e))

        try:
            datahandled['geo_longitude'] = str(postdata['geo_longitude'])
        except KeyError as e:
            datahandled['geo_longitude'] = ''
            #log.warning(str(e))

        try:
            datahandled['property_id'] = postdata['property_id']
        except KeyError as e:
            datahandled['property_id'] = ''
            #log.warning(str(e))

        try:
            datahandled['post_title_th'] = str(postdata['post_title_th'])
        except KeyError as e:
            datahandled['post_title_th'] = ''
            #log.warning(str(e))

        try:
            datahandled['post_description_th'] = str(postdata['post_description_th'])
        except KeyError as e:
            datahandled['post_description_th'] = ''
            #log.warning(str(e))

        try:
            datahandled['post_title_en'] = postdata['post_title_en']
        except KeyError as e:
            datahandled['post_title_en'] = ''
            #log.warning(str(e))

        try:
            datahandled['post_description_en'] = postdata['post_description_en']
        except KeyError as e:
            datahandled['post_description_en'] = ''
            #log.warning(str(e))

        try:
            datahandled['ds_id'] = postdata["ds_id"]
        except KeyError as e:
            datahandled['ds_id'] = ''
            #log.warning(str(e))

        try:
            datahandled['ds_name'] = postdata["ds_name"]
        except KeyError as e:
            datahandled['ds_name'] = ''
            #log.warning(str(e))

        try:
            datahandled['user'] = postdata['user']
        except KeyError as e:
            datahandled['user'] = ''
            #log.warning(str(e))

        try:
            datahandled['pass'] = postdata['pass']
        except KeyError as e:
            datahandled['pass'] = ''
            #log.warning(str(e))

        try:
            datahandled['project_name'] = postdata["project_name"]
        except KeyError as e:
            datahandled['project_name'] = ''
            #log.warning(str(e))

        try:
            datahandled['name'] = postdata["name"]
        except KeyError as e:
            datahandled['name'] = ''
            #log.warning(str(e))

        try:
            datahandled['mobile'] = postdata["mobile"]
        except KeyError as e:
            datahandled['mobile'] = ''
            #log.warning(str(e))

        try:
            datahandled['email'] = postdata["email"]
        except KeyError as e:
            datahandled['email'] = ''
            #log.warning(str(e))

        try:
            datahandled['web_project_name'] = postdata["web_project_name"]
        except KeyError as e:
            datahandled['web_project_name'] = ''
            #log.warning(str(e))

        try:
            datahandled['action'] = postdata["action"]
        except KeyError as e:
            datahandled['action'] = ''
            #log.warning(str(e))

        try:
            datahandled['bath_room'] = postdata["bath_room"]
        except KeyError as e:
            datahandled['bath_room'] = 0
            #log.warning(str(e))

        try:
            datahandled['bed_room'] = postdata["bed_room"]
        except KeyError as e:
            datahandled['bed_room'] = 0
            #log.warning(str(e))

        try:
            datahandled['floor_total'] = postdata["floor_total"]
        except KeyError as e:
            datahandled['floor_total'] = 0
            #log.warning(str(e))

        try:
            datahandled['floor_level'] = postdata["floor_level"]
        except KeyError as e:
            datahandled['floor_level'] = 0
            #log.warning(str(e))

        try:
            datahandled['direction_type'] = postdata["direction_type"]
        except KeyError as e:
            datahandled['direction_type'] = "ทิศเหนือ"
            #log.warning(str(e))
        if datahandled['direction_type'] == '11' or datahandled['direction_type'] == 11:
            datahandled['direction_type'] = "ทิศเหนือ"
        elif datahandled['direction_type'] == '12' or datahandled['direction_type'] == 12:
            datahandled['direction_type'] = "ทิศใต้"
        elif datahandled['direction_type'] == '13' or datahandled['direction_type'] == 13:
            datahandled['direction_type'] = "ทิศตะวันออก"
        elif datahandled['direction_type'] == '14' or datahandled['direction_type'] == 14:
            datahandled['direction_type'] = "ทิศตะวันตก"
        elif datahandled['direction_type'] == '21' or datahandled['direction_type'] == 21:
            datahandled['direction_type'] = "ทิศตะวันออกเฉียงเหนือ"
        elif datahandled['direction_type'] == '22' or datahandled['direction_type'] == 22:
            datahandled['direction_type'] = "ทิศตะวันออก"
        elif datahandled['direction_type'] == '23' or datahandled['direction_type'] == 23:
            datahandled['direction_type'] = "ทิศตะวันตกเฉียงเหนือ"
        elif datahandled['direction_type'] == '24' or datahandled['direction_type'] == 24:
            datahandled['direction_type'] = "ทิศตะวันตกเฉียงใต้"

        # add on trovit 12/03/2021
        try:
            datahandled['post_images'] = postdata["post_images"]
        except KeyError as e:
            datahandled['post_images'] = ''

        try:
            datahandled['post_id'] = postdata["post_id"]
        except KeyError as e:
            datahandled['post_id'] = ''
            #log.warning(str(e))

        try:
            datahandled['log_id'] = postdata["log_id"]
        except KeyError as e:
            datahandled['log_id'] = ''
            #log.warning(str(e))

        try:
            datahandled['land_size_rai'] = str(postdata["land_size_rai"])
            if(postdata["land_size_rai"]) == None:
                postdata["land_size_rai"] = '0'
        except KeyError as e:
            datahandled['land_size_rai'] = '0'
            #log.warning(str(e))

        try:
            datahandled['land_size_ngan'] = str(postdata["land_size_ngan"])
            if(postdata["land_size_ngan"]) == None:
                postdata["land_size_ngan"] = '0'
        except KeyError as e:
            datahandled['land_size_ngan'] = '0'
            #log.warning(str(e))

        try:
            datahandled['land_size_wa'] = str(postdata["land_size_wa"])
            if(postdata["land_size_wa"]) == None:
                postdata["land_size_wa"] = '0'
        except KeyError as e:
            datahandled['land_size_wa'] = '0'
            #log.warning(str(e))

        self.handled = True
        return datahandled