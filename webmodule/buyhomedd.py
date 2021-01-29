import requests
from bs4 import BeautifulSoup
import json
import datetime

from .lib_httprequest import *

httprequestObj = lib_httprequest()

class buyhomedd():

    def register_user(self,data):

        # extracting all information from json file
        user = data['user']
        password = data['pass']
        company_name = data['company_name']
        name_title = data['name_title']
        name_th = data['name_th']
        surname_th = data['surname_th']
        tel = data['tel']

        # complete register user data
        # using split method to remove the whitespaces around the entry.
        register_data = {
            'username': user.split(),
            'pass': password.split(),
            'conpass': password.split(),
            'email': user.split(),
            'name': name_th.split(),
            'lastname': surname_th.split(),
            'phone': tel.split(),
            'address': 'Phaya Thai, Samsen Nai, Bangkok 10400, Thailand',
            'action': 'register'
        }

        # headers
        headers = {
            'user_agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36'
        }

        success = False
        start_time = datetime.datetime.utcnow()
        end_time = datetime.datetime.utcnow()
        detail = ""

        # some validations
        if register_data['username'] == "":
            detail = "Invalid username"
        elif register_data['pass'] == "":
            detail = "Invalid Password"
        elif register_data['pass'] != register_data['conpass']:
            detail = "Invalid Password Confirmation"
        elif register_data['email'] == "":
            detail = "Invalid email"
        elif register_data['name'] == "":
            detail = "Invalid Name"
        elif register_data['lastname'] == "":
            detail = "Invalid lastname"
        elif register_data['phone'] == "":
            detail = "Invalid Phone Number"
        else:

            # Valid credentials
            url = 'https://www.buyhomedd.com/submitform.php'

            try:
                start_time = datetime.datetime.utcnow()

                # making a POST request to fill and submit the form
                req = httprequestObj.http_post(url,data=register_data,headers=headers)
                end_time = datetime.datetime.utcnow()

                txt = req.text
                if 'มีคนใช้แล้ว' in txt:
                    detail = 'Someone is already using it'
                else:
                    success = True
                    detail = 'Successfully registered'

            except requests.exceptions.RequestException:
                end_time = datetime.datetime.utcnow()
                detail = "Network Problem"

        # creating the final result object
        result = {
            'websitename': 'buyhomedd',
            'success': success,
            'start_time': str(start_time),
            'end_time': str(end_time),
            'usage_time': str(end_time-start_time),
            'detail': detail
        }

        return result

    def test_login(self,data):

        # extracting all information from json file
        user = data['user']
        password = data['pass']

        login_data = {
            'log_u': user,
            'log_p': password,
            'action': 'login'
        }

        # headers
        headers = {
            'user_agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36'
        }

        success = False
        start_time = datetime.datetime.utcnow()
        end_time = datetime.datetime.utcnow()
        detail = ""

        # some validations
        if login_data['log_u'] == "":
            detail = "Invalid username"
        elif login_data['log_p'] == "":
            detail = "Invalid Password"
        else:

            # Valid credentials
            url = 'https://www.buyhomedd.com/submitform.php'

            try:
                start_time = datetime.datetime.utcnow()

                # making a POST request to fill and submit the form
                req = httprequestObj.http_post(url,data=login_data,headers=headers)
                end_time = datetime.datetime.utcnow()

                txt = req.text
                if 'ไม่ถูกต้อง' in txt:
                    detail = 'Login Unsuccessful'
                else:
                    success = True
                    detail = 'Successfully logged in'

            except requests.exceptions.RequestException:
                end_time = datetime.datetime.utcnow()
                detail = "Network Problem"

        # creating the final result object
        result = {
            'websitename': 'buyhomedd',
            'success': success,
            'start_time': str(start_time),
            'end_time': str(end_time),
            'usage_time': str(end_time-start_time),
            'detail': detail
        }

        return result
