from .lib_httprequest import *
import datetime
import sys


class genie_property():

    name = 'genie_property'

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
        self.webname = 'genie_property'

    def print_debug(self, msg):
        if self.debug == 1:
            print(msg)
        return True


    # Error 401
    # def logout_user(self, postdata):

    #     url = "https://www.genie-property.com/api/logout?mode=production"
    #     r = self.httprequestObj.http_post(url, data=postdata)
    #     print("function [logout_user]")
    #     print(r.status_code)

    def register_details(self, postdata):
        register_data = {}

        
        register_data["first_name"] = postdata["name_en"]
        register_data["last_name"] = postdata["surname_en"]
        register_data["phone"] = postdata["tel"]
        register_data["email"] = postdata["user"]
        register_data["password"] = postdata["pass"]
        register_data["role"] = "seller"
        register_data["company"] = postdata["company_name"]

        return register_data

    def register_user(self, postdata):

        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()

        # start process
        #
        data_register = self.register_details(postdata)


        res = self.httprequestObj.http_post_with_headers('https://www.genie-property.com/api/signup?mode=production', data=data_register)
        print(res.status_code)
        # print(res.text)
        # with open("debug_response/genie_property.txt", "w") as file:
        #     file.write(res.text)


        detail = ""
        register_success = False
        soup_web = BeautifulSoup(res.text, "html5lib")
        if soup_web:
            verify_register = soup_web.find("span", attrs={"class":"mr-2"}).text
            if verify_register != "สำหรับผู้ขาย":
                register_success = True

        # 
        # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "genie_property",
            "success": register_success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
        }

    def test_login(self, postdata):
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        time_start = datetime.datetime.utcnow()


        url = "https://www.genie-property.com/api/signin?mode=production"
        data_login = {
            'email' : postdata['user'],
            'password' : postdata['pass']
        }


        r = self.httprequestObj.http_post(url, data=data_login)
        print(r.status_code)
        res = r.json()

        detail = ""
        success = False
        if res['success'] == True:
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

