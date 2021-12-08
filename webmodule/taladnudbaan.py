from .lib_httprequest import *
import datetime
import sys


class taladnudbaan():

    name = 'taladnudbaan'

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
        self.webname = 'taladnudbaan'

    def print_debug(self, msg):
        if self.debug == 1:
            print(msg)
        return True

    def logout_user(self):
        url = "https://th.taladnudbaan.com/baan/index.php/cod.logout"
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


        res = self.httprequestObj.http_post('https://accounts.taladnudbaan.com/?cod=create_user&url=https%3A%2F%2Fth.taladnudbaan.com%2Fbaan%2Findex.php%2Fcod.mail_preferences&language=th_TH&', data=data_register)

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
            "websitename": "taladnudbaan",
            "success": register_success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
        }

    def test_login(self, postdata):
        self.logout_user()
        self.print_debug('function [' + sys._getframe().f_code.co_name + ']')
        url = "https://accounts.taladnudbaan.com/?cod=check_login&url=https%3A%2F%2Fth.taladnudbaan.com%2Fbaan%2Findex.php%2Fcod.mail_preferences&language=th_TH&"

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

