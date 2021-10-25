# -*- coding: utf-8 -*-

from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
import re
import json
import datetime
import sys
import requests
import shutil
from urllib.parse import unquote


with open("./static/home2all_province.json",encoding = 'utf-8') as f:
    provincedata = json.load(f)


class home2all():

    name = 'home2all'

    def __init__(self):

        try:
            import configs

        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.debug = False
        self.debugresdata = 0
        self.parser = 'html.parser'
        self.httprequestObj = lib_httprequest()

    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user']
        passwd = postdata['pass']

        # start process
        #
        success = "true"
        detail = ""

        datapost = {
            "ScriptManager": "dnn$ctr$dnn$ctr$Register_UPPanel|dnn$ctr$Register$registerButton",
            "StylesheetManager_TSSM": ";Telerik.Web.UI, Version=2013.2.717.40, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en-US:dae8717e-3810-4050-96d3-31018e70c6e4:45085116:27c5704c",
            "ScriptManager_TSM": ";;AjaxControlToolkit, Version=4.1.51116.0, Culture=neutral, PublicKeyToken=28f01b0e84b6d53e:en:fd384f95-1b49-47cf-9b47-2fa2a921a36a:ea597d4b:b25378d2;Telerik.Web.UI, Version=2013.2.717.40, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en:dae8717e-3810-4050-96d3-31018e70c6e4:16e4e7cd:f7645509:ed16cbdc;",
            "dnn$ctr$Register$userForm$Password$Password_TextBox": passwd,
            "dnn$ctr$Register$userForm$PasswordConfirm$PasswordConfirm_TextBox": passwd,
            "dnn$ctr$Register$userForm$DisplayName$DisplayName_TextBox": postdata['name_th']+' '+postdata['surname_th'],
            "dnn$ctr$Register$userForm$Email$Email_TextBox": user,
            "dnn$ctr$Register$userForm$Telephone$Telephone_Control": postdata['tel'],
            "dnn$ctr$Register$ctlCaptcha": "iHkFN6",
            "ScrollTop": "132",
            "__dnnVariable": "`{`__scdoff`:`1`,`sf_siteRoot`:`/`,`sf_tabId`:`56`}",
            "__EVENTTARGET": "dnn$ctr$Register$registerButton",
            "__EVENTARGUMENT": '',
            "__VIEWSTATE": "/wEPDwULLTEwNjk5NzcxNzgPZBYIZg8WAh4EVGV4dAU+PCFET0NUWVBFIEhUTUwgUFVCTElDICItLy9XM0MvL0RURCBIVE1MIDQuMCBUcmFuc2l0aW9uYWwvL0VOIj5kAgIPFgIfAAUNIGxhbmc9ImVuLVVTImQCBA9kFg4CBg8WAh4HVmlzaWJsZWhkAgcPFgIeB2NvbnRlbnQFyANob21lMmFsbC5jb20gLSDguJXguKXguLLguJTguIvguLfguYnguK0t4LiC4Liy4Lii4Lit4Liq4Lix4LiH4Lir4Liy4Lij4Li04Lih4LiX4Lij4Lix4Lie4Lii4LmM4LiX4Li44LiB4LiK4LiZ4Li04LiU4LiX4Li14LmI4LmD4Lir4LiN4LmI4LiX4Li14LmI4Liq4Li44LiU4LmD4LiZ4Lib4Lij4Liw4LmA4LiX4Lio4LmE4LiX4LiiIOC4muC5ieC4suC4meC5gOC4lOC4teC5iOC4ouC4pyDguITguK3guJnguYLguJQg4LiX4Liy4Lin4LiZ4LmM4LmA4Liu4LmJ4Liy4Liq4LmMIOC4guC4suC4ouC4muC5ieC4suC4mSDguYDguIrguYjguLLguJrguYnguLLguJkg4Lia4LmJ4Liy4LiZ4Lih4Li34Lit4Liq4Lit4LiHIOC4hOC4o+C4muC4luC5ieC4p+C4meC5geC4peC4sOC4reC4seC4nuC5gOC4lOC4l+C4l+C4teC5iOC4quC4uOC4lCDguJfguLjguIHguJfguLPguYDguKXguJfguLHguYjguKfguYTguJfguKJkAggPFgIfAgW+CuC4guC4suC4ouC4l+C4teC5iOC4lOC4tOC4mSzguILguLLguKIg4LiX4Li14LmI4LiU4Li04LiZLOC4guC4suC4oiDguJrguYnguLLguJks4LiC4Liy4LiiIOC4muC5ieC4suC4mSDguYDguIrguLXguKLguIfguYPguKvguKHguYgs4LiC4Liy4Lii4Lir4Lit4Lie4Lix4LiBLOC4guC4suC4oiDguKvguK3guJ7guLHguIEs4LmA4LiK4LmI4Liy4Lia4LmJ4Liy4LiZLOC4hOC4reC4meC5guC4lCzguJrguYnguLLguJnguYDguJTguLXguYjguKLguKcs4LiX4Liy4Lin4LiZ4LmM4LmA4Liu4LmJ4Liy4Liq4LmMLOC4guC4suC4ouC4muC5ieC4suC4mSzguJrguYnguLLguJnguKHguLfguK3guKrguK3guIcs4Lia4LmJ4Liy4LiZ4LmD4Lir4Lih4LmILOC5guC4hOC4o+C4h+C4geC4suC4o+C5g+C4q+C4oeC5iCzguJfguLLguKfguJnguYzguYDguK7guYnguLLguKrguYzguYPguKvguKHguYgsCuC4guC4suC4ouC4hOC4reC4meC5guC4lCAsIOC5gOC4iuC5iOC4suC4hOC4reC4meC5guC4lCAsIOC4muC5ieC4suC4meC5gOC4iuC5iOC4siAsIOC5gOC4iuC5iOC4suC4muC5ieC4suC4mSAsIOC4hOC4reC4meC5guC4lOC4oeC4tOC5gOC4meC4teC4ouC4oSAsIOC4m+C4o+C4sOC4geC4suC4qOC4guC4suC4ouC4muC5ieC4suC4mSAsIOC4m+C4o+C4sOC4geC4suC4qOC4guC4suC4ouC4hOC4reC4meC5guC4lCAsIOC4m+C4o+C4sOC4geC4suC4qOC5g+C4q+C5ieC5gOC4iuC5iOC4suC4hOC4reC4meC5guC4lCAsIOC4m+C4o+C4sOC4geC4suC4qOC4guC4suC4ouC4hOC4reC4meC5guC4lCAsIOC4m+C4o+C4sOC4geC4suC4qOC4guC4suC4ouC4reC4quC4seC4h+C4q+C4suC4o+C4tOC4oeC4l+C4o+C4seC4nuC4ouC5jCDguIHguKPguLjguIfguYDguJfguJ7guK8g4LiX4Lix4LmI4Lin4LmE4LiX4LiiICwg4Lia4LmJ4Liy4LiZ4Lih4Li34Lit4Liq4Lit4LiHIOC4l+C4teC5iOC4lOC4tOC4mSDguJvguKPguLDguIHguLLguKgg4LiC4Liy4Lii4Lia4LmJ4Liy4LiZIOC4i+C4t+C5ieC4reC4muC5ieC4suC4mSAsIOC4neC4suC4geC4guC4suC4ouC4muC5ieC4suC4mSDguJ/guKPguLUgLCDguITguYnguJnguKvguLLguJrguYnguLLguJkgLCDguYPguKvguYnguYDguIrguYjguLLguJrguYnguLLguJnguYDguJTguLXguYjguKLguKcgLCDguYPguKvguYnguYDguIrguYjguLLg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cHQgYXN5bmMgc3JjPSIvL3BhZ2VhZDIuZ29vZ2xlc3luZGljYXRpb24uY29tL3BhZ2VhZC9qcy9hZHNieWdvb2dsZS5qcyI+PC9zY3JpcHQ+PCEtLSB0aGFpLWhlYWQgLSA5NTB4OTAgLS0+PGlucyBjbGFzcz0iYWRzYnlnb29nbGUiICAgICBzdHlsZT0iZGlzcGxheTppbmxpbmUtYmxvY2s7d2lkdGg6OTcwcHg7aGVpZ2h0OjI1MHB4IiAgICAgZGF0YS1hZC1jbGllbnQ9ImNhLXB1Yi0wODY2NDU4MDY4NDQyMzIwIiAgICAgZGF0YS1hZC1zbG90PSIxMDgyNTI1MTI1Ij48L2lucz48c2NyaXB0PihhZHNieWdvb2dsZSA9IHdpbmRvdy5hZHNieWdvb2dsZSB8fCBbXSkucHVzaCh7fSk7PC9zY3JpcHQ+HwFoZAIYDxYCHwMFFmNvbC1tZC0xMiBETk5FbXB0eVBhbmVkAhoPZBYCZg8WAh8DBSFEbm5Nb2R1bGUgRG5uTW9kdWxlLSBEbm5Nb2R1bGUtLTEWAmYPZBYGZg8PFgIfAWdkZAIBD2QWAgICDxYCHwFoZAICD2QWAmYPD2QWAh8DBRVETk5Nb2R1bGVDb250ZW50IE1vZEMWAgIBD2QWBGYPFgIfAWdkAgEPZBYGAgEPDxYCHwAFkgM8c3Ryb25nPipOb3RlOjwvc3Ryb25nPiBNZW1iZXJzaGlwIHRvIHRoaXMgd2Vic2l0ZSBpcyBWZXJpZmllZC4gT25jZSB5b3VyIGFjY291bnQgaW5mb3JtYXRpb24gaGFzIGJlZW4gc3VibWl0dGVkLCB5b3Ugd2lsbCByZWNlaXZlIGFuIGVtYWlsIGNvbnRhaW5pbmcgYSBsaW5rIHRoYXQgeW91IGNhbiB1c2UgdG8gdmVyaWZ5IHlvdXIgYWNjb3VudC4gQWxsIGZpZWxkcyBtYXJrZWQgd2l0aCBhIHJlZCBhc3RlcmlzayBhcmUgcmVxdWlyZWQuIC0gPGVtPig8c3Ryb25nPk5vdGU6PC9zdHJvbmc+IC0gUmVnaXN0cmF0aW9uIG1heSB0YWtlIHNldmVyYWwgc2Vjb25kcy4gIE9uY2UgeW91IGNsaWNrIHRoZSBSZWdpc3RlciBidXR0b24gcGxlYXNlIHdhaXQgdW50aWwgdGhlIHN5c3RlbSByZXNwb25kcy4pPC9lbT5kZAIDDw8WBB8GBQdkbm5Gb3JtHwcCAmQWCmYPDxYEHwYFGGRubkZvcm1JdGVtIGRubkZvcm1TaG9ydB8HAgJkFgRmDw8WBB8GBQhkbm5MYWJlbB8HAgJkZAIBDw9kFgIeBXZhbHVlBQgxMjM0NTZhYWQCAQ8PFgQfBgUYZG5uRm9ybUl0ZW0gZG5uRm9ybVNob3J0HwcCAmQWBGYPDxYEHwYFCGRubkxhYmVsHwcCAmRkAgEPD2QWAh8IBQgxMjM0NTZhYWQCAg8PFgQfBgUYZG5uRm9ybUl0ZW0gZG5uRm9ybVNob3J0HwcCAmQWBGYPDxYEHwYFCGRubkxhYmVsHwcCAmRkAgEPDxYCHwAFC0FsZXggU2F4YWxlZGQCAw8PFgQfBgUYZG5uRm9ybUl0ZW0gZG5uRm9ybVNob3J0HwcCAmQWBGYPDxYEHwYFCGRubkxhYmVsHwcCAmRkAgEPDxYCHwAFG3NheGFsZXMxNDRAb2ZmaWNlbWFsYWdhLmNvbWRkAgQPDxYEHwYFGGRubkZvcm1JdGVtIGRubkZvcm1TaG9ydB8HAgJkFgJmDw8WBB8GBQhkbm5MYWJlbB8HAgJkZAIHDxYCHwFnFgICAw8UKwACZAUGaUhrRk42ZAIcDxYCHwMFFWNvbC1tZC0zIEROTkVtcHR5UGFuZWQCHg8WAh8DBRVjb2wtbWQtNCBETk5FbXB0eVBhbmVkAiAPFgIfAwUVY29sLW1kLTQgRE5ORW1wdHlQYW5lZAIiDxYCHwMFFWNvbC1tZC00IEROTkVtcHR5UGFuZWQCJA8WAh8DBRVjb2wtbWQtMyBETk5FbXB0eVBhbmVkAiYPFgIfAwUVY29sLW1kLTkgRE5ORW1wdHlQYW5lZAIoDxYCHwMFFWNvbC1tZC0yIEROTkVtcHR5UGFuZWQCKg8WAh8DBRZjb2wtbWQtMTAgRE5ORW1wdHlQYW5lZAIsDxYCHwMFFmNvbC1tZC0xMiBETk5FbXB0eVBhbmVkAi4PFgIfAwUVY29sLW1kLTQgRE5ORW1wdHlQYW5lZAIwDxYCHwMFFWNvbC1tZC00IEROTkVtcHR5UGFuZWQCMg8WAh8DBRVjb2wtbWQtNCBETk5FbXB0eVBhbmVkAjQPFgIfAwUWY29sLW1kLTEyIEROTkVtcHR5UGFuZWQCOg8WAh8ABaYDPHNjcmlwdD4gIChmdW5jdGlvbihpLHMsbyxnLHIsYSxtKXtpWydHb29nbGVBbmFseXRpY3NPYmplY3QnXT1yO2lbcl09aVtyXXx8ZnVuY3Rpb24oKXsgIChpW3JdLnE9aVtyXS5xfHxbXSkucHVzaChhcmd1bWVudHMpfSxpW3JdLmw9MSpuZXcgRGF0ZSgpO2E9cy5jcmVhdGVFbGVtZW50KG8pLCAgbT1zLmdldEVsZW1lbnRzQnlUYWdOYW1lKG8pWzBdO2EuYXN5bmM9MTthLnNyYz1nO20ucGFyZW50Tm9kZS5pbnNlcnRCZWZvcmUoYSxtKSAgfSkod2luZG93LGRvY3VtZW50LCdzY3JpcHQnLCcvL3d3dy5nb29nbGUtYW5hbHl0aWNzLmNvbS9hbmFseXRpY3MuanMnLCdnYScpOyAgZ2EoJ2NyZWF0ZScsICdVQS0xMDU2MTMyOS0yJywgJ2F1dG8nKTsgIGdhKCdzZW5kJywgJ3BhZ2V2aWV3Jyk7Z2EoJ3NldCcsICcmdWlkJywgLTEpOyA8L3NjcmlwdD5kGAYFGWRubiRjdHIkUmVnaXN0ZXIkdXNlckZvcm0PAgVkBSVkbm4kY3RyJFJlZ2lzdGVyJHVzZXJGb3JtJERpc3BsYXlOYW1lDwULQWxleCBTYXhhbGVkBR9kbm4kY3RyJFJlZ2lzdGVyJHVzZXJGb3JtJEVtYWlsDwUbc2F4YWxlczE0NEBvZmZpY2VtYWxhZ2EuY29tZAUjZG5uJGN0ciRSZWdpc3RlciR1c2VyRm9ybSRUZWxlcGhvbmUPBQkxMjM0NTY3ODlkBSJkbm4kY3RyJFJlZ2lzdGVyJHVzZXJGb3JtJFBhc3N3b3JkDwUIMTIzNDU2YWFkBSlkbm4kY3RyJFJlZ2lzdGVyJHVzZXJGb3JtJFBhc3N3b3JkQ29uZmlybQ8FCDEyMzQ1NmFhZL9MyMteiPTQZuJ6GD6ZMF1rW0l9",
            "__VIEWSTATEGENERATOR": "CA0B0334",
            "__ASYNCPOST": "true",
            "RadAJAXControlID": "dnn_ctr_Register_UP"
        }
        r = self.httprequestObj.http_post(
            'https://home2all.com/Register?returnurl=https%3a%2f%2fhome2all.com%2f', data=datapost)
        
        # with open('b.html','w') as f:
        #     print(r.text,file=f)  
        # data = r.text
        # print(data)
        if r.text.find("A user is already using this email address.") != -1:
            success = "False"
            detail = "Email Already registered"
        elif r.text.find("The Display Name is already in use.") != -1:
            success = "False"
            detail = "Same Display name"
        elif r.text.find("The password specified is invalid") != -1:
            success = "False"
            detail = "The password specified is invalid"
        elif r.text.find("The requested password is invalid") != -1:
            detail = "The requested password is invalid"
            success = "False"
        elif r.text.find("You must enter a valid email address") != -1:
            detail = "Invalid Email Address"
            success = "False"
        # else:
        #     detail = "Registered"
        # #
        # # end process

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "home2all",
            "success": success,
            "usage_time": str(time_usage),
            'ds_id': postdata['ds_id'],
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "ds_id": postdata['ds_id']
        }



    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        user = postdata['user'].rstrip("\u200b")
        passwd = postdata['pass']
        # start process
        #
        success = "true"
        detail = "logged in"
        # print(postdata['user'], len(postdata['user']), len(postdata['user'].rstrip("\u200b")))
        res = self.httprequestObj.http_get("https://home2all.com/home/ctl/Logoff")
        print(res.status_code)
        datapost = {
            "StylesheetManager_TSSM": '',
            "ScriptManager_TSM": ";;AjaxControlToolkit, Version=4.1.51116.0, Culture=neutral, PublicKeyToken=28f01b0e84b6d53e:en:fd384f95-1b49-47cf-9b47-2fa2a921a36a:ea597d4b:b25378d2",
            "__EVENTTARGET": "dnn$ctr$Login$Login_DNN$cmdLogin",
            "__EVENTARGUMENT": '',
            "__VIEWSTATE": "/wEPDwULLTEwNjk5NzcxNzgPZBYIZg8WAh4EVGV4dAU+PCFET0NUWVBFIEhUTUwgUFVCTElDICItLy9XM0MvL0RURCBIVE1MIDQuMCBUcmFuc2l0aW9uYWwvL0VOIj5kAgIPFgIfAAUNIGxhbmc9ImVuLVVTImQCBA9kFg4CBg8WAh4HVmlzaWJsZWhkAgcPFgIeB2NvbnRlbnQFyANob21lMmFsbC5jb20gLSDguJXguKXguLLguJTguIvguLfguYnguK0t4LiC4Liy4Lii4Lit4Liq4Lix4LiH4Lir4Liy4Lij4Li04Lih4LiX4Lij4Lix4Lie4Lii4LmM4LiX4Li44LiB4LiK4LiZ4Li04LiU4LiX4Li14LmI4LmD4Lir4LiN4LmI4LiX4Li14LmI4Liq4Li44LiU4LmD4LiZ4Lib4Lij4Liw4LmA4LiX4Lio4LmE4LiX4LiiIOC4muC5ieC4suC4meC5gOC4lOC4teC5iOC4ouC4pyDguITguK3guJnguYLguJQg4LiX4Liy4Lin4LiZ4LmM4LmA4Liu4LmJ4Liy4Liq4LmMIOC4guC4suC4ouC4muC5ieC4suC4mSDguYDguIrguYjguLLguJrguYnguLLguJkg4Lia4LmJ4Liy4LiZ4Lih4Li34Lit4Liq4Lit4LiHIOC4hOC4o+C4muC4luC5ieC4p+C4meC5geC4peC4sOC4reC4seC4nuC5gOC4lOC4l+C4l+C4teC5iOC4quC4uOC4lCDguJfguLjguIHguJfguLPguYDguKXguJfguLHguYjguKfguYTguJfguKJkAggPFgIfAgW+CuC4guC4suC4ouC4l+C4teC5iOC4lOC4tOC4mSzguILguLLguKIg4LiX4Li14LmI4LiU4Li04LiZLOC4guC4suC4oiDguJrguYnguLLguJks4LiC4Liy4LiiIOC4muC5ieC4suC4mSDguYDguIrguLXguKLguIfguYPguKvguKHguYgs4LiC4Liy4Lii4Lir4Lit4Lie4Lix4LiBLOC4guC4suC4oiDguKvguK3guJ7guLHguIEs4LmA4LiK4LmI4Liy4Lia4LmJ4Liy4LiZLOC4hOC4reC4meC5guC4lCzguJrguYnguLLguJnguYDguJTguLXguYjguKLguKcs4LiX4Liy4Lin4LiZ4LmM4LmA4Liu4LmJ4Liy4Liq4LmMLOC4guC4suC4ouC4muC5ieC4suC4mSzguJrguYnguLLguJnguKHguLfguK3guKrguK3guIcs4Lia4LmJ4Liy4LiZ4LmD4Lir4Lih4LmILOC5guC4hOC4o+C4h+C4geC4suC4o+C5g+C4q+C4oeC5iCzguJfguLLguKfguJnguYzguYDguK7guYnguLLguKrguYzguYPguKvguKHguYgsCuC4guC4suC4ouC4hOC4reC4meC5guC4lCAsIOC5gOC4iuC5iOC4suC4hOC4reC4meC5guC4lCAsIOC4muC5ieC4suC4meC5gOC4iuC5iOC4siAsIOC5gOC4iuC5iOC4suC4muC5ieC4suC4mSAsIOC4hOC4reC4meC5guC4lOC4oeC4tOC5gOC4meC4teC4ouC4oSAsIOC4m+C4o+C4sOC4geC4suC4qOC4guC4suC4ouC4muC5ieC4suC4mSAsIOC4m+C4o+C4sOC4geC4suC4qOC4guC4suC4ouC4hOC4reC4meC5guC4lCAsIOC4m+C4o+C4sOC4geC4suC4qOC5g+C4q+C5ieC5gOC4iuC5iOC4suC4hOC4reC4meC5guC4lCAsIOC4m+C4o+C4sOC4geC4suC4qOC4guC4suC4ouC4hOC4reC4meC5guC4lCAsIOC4m+C4o+C4sOC4geC4suC4qOC4guC4suC4ouC4reC4quC4seC4h+C4q+C4suC4o+C4tOC4oeC4l+C4o+C4seC4nuC4ouC5jCDguIHguKPguLjguIfguYDguJfguJ7guK8g4LiX4Lix4LmI4Lin4LmE4LiX4LiiICwg4Lia4LmJ4Liy4LiZ4Lih4Li34Lit4Liq4Lit4LiHIOC4l+C4teC5iOC4lOC4tOC4mSDguJvguKPguLDguIHguLLguKgg4LiC4Liy4Lii4Lia4LmJ4Liy4LiZIOC4i+C4t+C5ieC4reC4muC5ieC4suC4mSAsIOC4neC4suC4geC4guC4suC4ouC4muC5ieC4suC4mSDguJ/guKPguLUgLCDguITguYnguJnguKvguLLguJrguYnguLLguJkgLCDguYPguKvguYnguYDguIrguYjguLLguJrguYnguLLguJnguYDguJTguLXguYjguKLguKcgLCDguYPguKvguYnguYDguIrguYjguLLg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bmMgc3JjPSIvL3BhZ2VhZDIuZ29vZ2xlc3luZGljYXRpb24uY29tL3BhZ2VhZC9qcy9hZHNieWdvb2dsZS5qcyI+PC9zY3JpcHQ+PCEtLSB0aGFpLWhlYWQgLSA5NTB4OTAgLS0+PGlucyBjbGFzcz0iYWRzYnlnb29nbGUiICAgICBzdHlsZT0iZGlzcGxheTppbmxpbmUtYmxvY2s7d2lkdGg6OTcwcHg7aGVpZ2h0OjI1MHB4IiAgICAgZGF0YS1hZC1jbGllbnQ9ImNhLXB1Yi0wODY2NDU4MDY4NDQyMzIwIiAgICAgZGF0YS1hZC1zbG90PSIxMDgyNTI1MTI1Ij48L2lucz48c2NyaXB0PihhZHNieWdvb2dsZSA9IHdpbmRvdy5hZHNieWdvb2dsZSB8fCBbXSkucHVzaCh7fSk7PC9zY3JpcHQ+HwFoZAIYDxYCHwMFFmNvbC1tZC0xMiBETk5FbXB0eVBhbmVkAhoPZBYCZg8WAh8DBSFEbm5Nb2R1bGUgRG5uTW9kdWxlLSBEbm5Nb2R1bGUtLTEWAmYPZBYGZg8PFgIfAWdkZAIBD2QWAgICDxYCHwFoZAICD2QWAmYPD2QWAh8DBRVETk5Nb2R1bGVDb250ZW50IE1vZEMWBGYPFgIfAWcWAmYPZBYCZg8PFgQfBgUnZG5uRm9ybU1lc3NhZ2UgZG5uRm9ybVZhbGlkYXRpb25TdW1tYXJ5HwcCAmRkAgEPDxYEHgZQYWdlTm9mHgtMb2dpblN0YXR1cwspc0RvdE5ldE51a2UuU2VjdXJpdHkuTWVtYmVyc2hpcC5Vc2VyTG9naW5TdGF0dXMsIERvdE5ldE51a2UsIFZlcnNpb249Ny4yLjIuMzAzLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPW51bGwEZBYIAgEPDxYCHwFnZBYEAgMPDxYCHwFnZBYCZg8WAh4Jb25rZXlkb3duBZwEcmV0dXJuIF9fZG5uX0tleURvd24oJzEzJywgJ2phdmFzY3JpcHQ6X19kb1Bvc3RCYWNrKCUyN2RubiRjdHIkTG9naW4kTG9naW5fRE5OJGNtZExvZ2luJTI3LCUyNyUyNyknLCBldmVudCk7cmV0dXJuIF9fZG5uX0tleURvd24oJzEzJywgJ2phdmFzY3JpcHQ6X19kb1Bvc3RCYWNrKCUyN2RubiRjdHIkTG9naW4kTG9naW5fRE5OJGNtZExvZ2luJTI3LCUyNyUyNyknLCBldmVudCk7cmV0dXJuIF9fZG5uX0tleURvd24oJzEzJywgJ2phdmFzY3JpcHQ6X19kb1Bvc3RCYWNrKCUyN2RubiRjdHIkTG9naW4kTG9naW5fRE5OJGNtZExvZ2luJTI3LCUyNyUyNyknLCBldmVudCk7cmV0dXJuIF9fZG5uX0tleURvd24oJzEzJywgJ2phdmFzY3JpcHQ6X19kb1Bvc3RCYWNrKCUyN2RubiRjdHIkTG9naW4kTG9naW5fRE5OJGNtZExvZ2luJTI3LCUyNyUyNyknLCBldmVudCk7cmV0dXJuIF9fZG5uX0tleURvd24oJzEzJywgJ2phdmFzY3JpcHQ6X19kb1Bvc3RCYWNrKCUyN2RubiRjdHIkTG9naW4kTG9naW5fRE5OJGNtZExvZ2luJTI3LCUyNyUyNyknLCBldmVudCk7FgJmD2QWCgIBDw8WAh8ABQ5FbWFpbCBBZGRyZXNzOmRkAgsPZBYCAgEPFCsAAmQFBk1DZnFocWQCDQ8PFgIfAGVkZAITD2QWAmYPDxYCHwUFK2h0dHBzOi8vaG9tZTJhbGwuY29tL1JlZ2lzdGVyP3JldHVybnVybD0lMmZkZAIVD2QWAmYPDxYCHwUFOGh0dHBzOi8vaG9tZTJhbGwuY29tL2hvbWUvY3RsL1NlbmRQYXNzd29yZD9yZXR1cm51cmw9JTJmZGQCBQ9kFgJmD2QWAgICDxYCHwFoZAIDD2QWAgIVDxYCHwFoFgICAw8UKwACZAUGTUNmcWhxZAIFD2QWAgIFD2QWAgICD2QWAgIDDxQrAAIPFgIfAGVkZBYEZg8PFgQfBgUJcmNiSGVhZGVyHwcCAmRkAgEPDxYEHwYFCXJjYkZvb3Rlch8HAgJkZAIHD2QWAgIBD2QWAgIDD2QWAgIPD2QWAgIDDxQrAAJkBQZNQ2ZxaHFkAhwPFgIfAwUVY29sLW1kLTMgRE5ORW1wdHlQYW5lZAIeDxYCHwMFFWNvbC1tZC00IEROTkVtcHR5UGFuZWQCIA8WAh8DBRVjb2wtbWQtNCBETk5FbXB0eVBhbmVkAiIPFgIfAwUVY29sLW1kLTQgRE5ORW1wdHlQYW5lZAIkDxYCHwMFFWNvbC1tZC0zIEROTkVtcHR5UGFuZWQCJg8WAh8DBRVjb2wtbWQtOSBETk5FbXB0eVBhbmVkAigPFgIfAwUVY29sLW1kLTIgRE5ORW1wdHlQYW5lZAIqDxYCHwMFFmNvbC1tZC0xMCBETk5FbXB0eVBhbmVkAiwPFgIfAwUWY29sLW1kLTEyIEROTkVtcHR5UGFuZWQCLg8WAh8DBRVjb2wtbWQtNCBETk5FbXB0eVBhbmVkAjAPFgIfAwUVY29sLW1kLTQgRE5ORW1wdHlQYW5lZAIyDxYCHwMFFWNvbC1tZC00IEROTkVtcHR5UGFuZWQCNA8WAh8DBRZjb2wtbWQtMTIgRE5ORW1wdHlQYW5lZAI6DxYCHwAFpgM8c2NyaXB0PiAgKGZ1bmN0aW9uKGkscyxvLGcscixhLG0pe2lbJ0dvb2dsZUFuYWx5dGljc09iamVjdCddPXI7aVtyXT1pW3JdfHxmdW5jdGlvbigpeyAgKGlbcl0ucT1pW3JdLnF8fFtdKS5wdXNoKGFyZ3VtZW50cyl9LGlbcl0ubD0xKm5ldyBEYXRlKCk7YT1zLmNyZWF0ZUVsZW1lbnQobyksICBtPXMuZ2V0RWxlbWVudHNCeVRhZ05hbWUobylbMF07YS5hc3luYz0xO2Euc3JjPWc7bS5wYXJlbnROb2RlLmluc2VydEJlZm9yZShhLG0pICB9KSh3aW5kb3csZG9jdW1lbnQsJ3NjcmlwdCcsJy8vd3d3Lmdvb2dsZS1hbmFseXRpY3MuY29tL2FuYWx5dGljcy5qcycsJ2dhJyk7ICBnYSgnY3JlYXRlJywgJ1VBLTEwNTYxMzI5LTInLCAnYXV0bycpOyAgZ2EoJ3NlbmQnLCAncGFnZXZpZXcnKTtnYSgnc2V0JywgJyZ1aWQnLCAtMSk7IDwvc2NyaXB0PmQYAgUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFIWRubiRjdHIkTG9naW4kTG9naW5fRE5OJGNoa0Nvb2tpZQUbZG5uJGN0ciRMb2dpbiRVc2VyJGNib1NpdGVzDxQrAAJlZWRx55Zk3eVIUK7aYCsTKRuAxkPv3w==",
            "__VIEWSTATEGENERATOR": "CA0B0334",
            "dnn$ctr$Login$Login_DNN$txtUsername": user,
            "dnn$ctr$Login$Login_DNN$txtPassword": passwd,
            "ScrollTop": "",
            "__dnnVariable": "`{`__scdoff`:`1`,`sf_siteRoot`:`/`,`sf_tabId`:`56`}"
        }
        r = self.httprequestObj.http_post(
            'https://home2all.com/Login?returnurl=%2f', data=datapost)
    
        soup = BeautifulSoup(r.text, features='html.parser')
        if soup.find(id='dnn_ctr_Login_pnlLoginContainer'):
            detail = "cannot login"
            success = "False"

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "home2all",
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "ds_id": postdata['ds_id'],
            "end_time": str(time_end),
            "detail": detail,
        }


    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()
        
        # start process
        # login
        success = "True"
        if 'name' not in postdata:
            success = "False"
            detail  = "Please fill name"
        elif 'mobile' not in postdata:
            success = "False"
            detail  = "Please fill mobile number"
        elif 'email' not in postdata:
            success = "False"
            detail  = "Please fill email"
        if success=="False":
            time_end = datetime.datetime.utcnow()
            time_usage = time_end-time_start
            return {
                "websitename": "home2all",
                "success": success,
                "ds_id": postdata['ds_id'],
                "usage_time": str(time_usage),
                "start_time": str(time_start),
                "end_time": str(time_end),
                "post_url": "",
                "post_id": "",
                "account_type": "null",
                "detail": detail
            }

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        post_id = ""
        post_url = ""

        proid = {
            'คอนโด': '1',
            'บ้านเดี่ยว': '2',
            'บ้านแฝด': '3',
            'ทาวน์เฮ้าส์': '4',
            'ตึกแถว-อาคารพาณิชย์': '5',
            'ที่ดิน': '6',
            'อพาร์ทเมนท์': '7',
            'โรงแรม': '8',
            'ออฟฟิศสำนักงาน': '9',
            'โกดัง': '10',
            'โรงงาน':'25'
        }
        getProdId = {'1': 3, '2': 1, '3': 9, '4': 2,
                     '5': 7, '6': 5, '7': 4, '8': 9, '9': 9, '10': 9, '25': 11}

        try:
            theprodid = getProdId[proid[str(postdata['property_type'])]]
        except:
            theprodid = getProdId[str(postdata['property_type'])]

        # print(theprodid)
        
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
        
        # print(province_id)
        # print(amphur_id)
        # print(postdata['addr_district'])
        
        prod_address = ""
        
        for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
            if add is not None:
                prod_address += add+" "

        if postdata['land_size_rai'] == None or postdata['land_size_rai'] == '':
            postdata['land_size_rai'] = 0

        if postdata['land_size_ngan'] == None or postdata['land_size_ngan'] == '':
            postdata['land_size_ngan'] = 0

        if postdata['land_size_wa'] == None or postdata['land_size_wa'] == '':
            postdata['land_size_wa'] = 0


        print(postdata['land_size_wa'])

        area = str(400*int(postdata['land_size_rai']) + 100 *int(postdata['land_size_ngan']) + int(postdata['land_size_wa']))
        typ = '2'

        if theprodid != 5:
            if 'floor_area' not in postdata or postdata['floor_area'] == None:
                if 'floorarea_sqm' not in postdata or postdata['floorarea_sqm'] == None:
                    area ='0'
                else:
                    area = str(postdata['floorarea_sqm'])
                    typ = '3'
            else:
                area = str(postdata['floor_area'])
                typ = '3' 

        if int(area) > 999:
            if typ == '2':
                area = str(int(area)//400)
                typ='1'
            else:
                area = str(int(area)//4)
                typ='2'
                if int(area) > 999:
                    area = str(int(area)//400)
                    typ='1'

        prod_address = prod_address[:-1]

        postdata['price_baht'] = str(postdata['price_baht'])

        if 'floor_total' not in postdata:
                postdata['floor_total']=""
        else:
                postdata['floor_total']=str(postdata['floor_total'])

        
        if 'floor_level' not in postdata:
                postdata['floor_level']=""
        else:
                postdata['floor_level']=str(postdata['floor_level'])

        if 'project_name' not in postdata:
                postdata['project_name']=""
        
        if 'bath_room' not in postdata:
                postdata['bath_room']=""
        else:
                postdata['bath_room']=str(postdata['bath_room'])
        
        if 'bed_room' not in postdata:
                postdata['bed_room']=""
        else:
                postdata['bed_room']=str(postdata['bed_room'])
        
        listing = 0 
        
        if postdata['listing_type'] != 'ขาย':
            listing = 3
        else:
            listing = 1

        r = self.httprequestObj.http_get(
            'https://home2all.com/%E0%B8%A5%E0%B8%87%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B8%81%E0%B8%B2%E0%B8%A8%E0%B8%9F%E0%B8%A3%E0%B8%B5')
        soup = BeautifulSoup(r.text, 'lxml')
        viewstate = soup.select_one("#__VIEWSTATE")['value']

        if success == "true":
            datapost = {
                'StylesheetManager_TSSM': ';Telerik.Web.UI, Version=2013.2.717.40, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en-US:dae8717e-3810-4050-96d3-31018e70c6e4:1c2121e:e24b8e95:aac1aeb7:c73cf106',
                'ScriptManager_TSM': ';;AjaxControlToolkit, Version=4.1.51116.0, Culture=neutral, PublicKeyToken=28f01b0e84b6d53e:en:fd384f95-1b49-47cf-9b47-2fa2a921a36a:ea597d4b:b25378d2;Telerik.Web.UI, Version=2013.2.717.40, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en:dae8717e-3810-4050-96d3-31018e70c6e4:16e4e7cd:f7645509:24ee1bba:f46195d3:2003d0b8:1e771326:aa288e2d:b7778d6c:e085fe68',
                '__EVENTTARGET': 'dnn$ctr438$AddTopic$btnSubmit',
                '__EVENTARGUMENT': '',
                '__LASTFOCUS': '',
                "__VIEWSTATE": viewstate,
                "__VIEWSTATEGENERATOR": "CA0B0334",
                "sid": "20090729-GP-be8e7bbb9f842760f6cab9b4f40e5787",
                "dnn$ctr438$AddTopic$ddlNewProject": "โปรดกรอกชื่อโครงการที่เกี่ยวข้องกับประกาศของท่าน",
                "dnn_ctr438_AddTopic_ddlNewProject_ClientState": "",
                "dnn$ctr438$AddTopic$ddlType": listing,
                "dnn$ctr438$AddTopic$ddlPropertyType": theprodid,
                "dnn$ctr438$AddTopic$txtTopic": postdata["post_title_th"],
                "dnn$ctr438$AddTopic$txtDescription": postdata["post_description_th"].replace('\n','\r\n'),
                "dnn$ctr438$AddTopic$txtLocation": prod_address,
                "dnn$ctr438$AddTopic$ddlProvince": province_id,
                "dnn$ctr438$AddTopic$ddlAumphur": amphur_id,
                "dnn$ctr438$AddTopic$txtNumAllFloor": postdata['floor_total'],
                "dnn_ctr438_AddTopic_txtNumAllFloor_ClientState": '{"enabled":true,"emptyMessage":"","validationText":"'+postdata['floor_total']+'","valueAsString":"'+postdata['floor_total']+'","minValue":0,"maxValue":99,"lastSetTextBoxValue":"'+postdata['floor_total']+'"}',
                "dnn$ctr438$AddTopic$txtNumFloor": postdata['floor_level'],
                "dnn_ctr438_AddTopic_txtNumFloor_ClientState": '{"enabled":true,"emptyMessage":"","validationText":"'+postdata['floor_level']+'","valueAsString":"'+postdata['floor_level']+'","minValue":0,"maxValue":99,"lastSetTextBoxValue":"'+postdata['floor_level']+'"}',
                "dnn$ctr438$AddTopic$txtRoom": postdata['bed_room'],
                "dnn_ctr438_AddTopic_txtRoom_ClientState": '{"enabled":true,"emptyMessage":"","validationText":"'+postdata['bed_room']+'","valueAsString":"'+postdata['bed_room']+'","minValue":0,"maxValue":99,"lastSetTextBoxValue":"'+postdata['bed_room']+'"}',
                "dnn$ctr438$AddTopic$txtBath": postdata['bath_room'],
                "dnn_ctr438_AddTopic_txtBath_ClientState": '{"enabled":true,"emptyMessage":"","validationText":"'+postdata['bath_room']+'","valueAsString":"'+postdata['bath_room']+'","minValue":0,"maxValue":99,"lastSetTextBoxValue":"'+postdata['bath_room']+'"}',
                "dnn$ctr438$AddTopic$txtArea": area,
                "dnn_ctr438_AddTopic_txtArea_ClientState": '{"enabled":true,"emptyMessage":"","validationText":"'+area+'","valueAsString":"'+area+'","minValue":0,"maxValue":999,"lastSetTextBoxValue":"'+area+'"}',
                "dnn$ctr438$AddTopic$ddlArea": typ,
                "dnn$ctr438$AddTopic$txtPrice": postdata['price_baht'],
                "dnn_ctr438_AddTopic_txtPrice_ClientState": '{"enabled":true,"emptyMessage":"","validationText":"'+postdata['price_baht']+'","valueAsString":"'+postdata['price_baht']+'","minValue":0,"maxValue":999999999,"lastSetTextBoxValue":"'+postdata['price_baht']+'"}',
                "dnn$ctr438$AddTopic$ddlBTS": 'เลือกสถานีไฟฟ้า',
                "dnn$ctr438$AddTopic$txtBTS": '',
                "dnn_ctr438_AddTopic_txtBTS_ClientState": '{"enabled":true,"emptyMessage":"","validationText":"","valueAsString":"","minValue":0,"maxValue":9999,"lastSetTextBoxValue":""}',
                "dnn$ctr438$AddTopic$ddlMRT": 'เลือกสถานีใต้ดิน',
                "dnn$ctr438$AddTopic$txtMRT": "",
                "dnn_ctr438_AddTopic_txtMRT_ClientState": '{"enabled":true,"emptyMessage":"","validationText":"","valueAsString":"","minValue":0,"maxValue":9999,"lastSetTextBoxValue":""}',
                "dnn$ctr438$AddTopic$ddlARL": 'เลือกสถานีแอร์พอร์ตลิงค์',
                "dnn$ctr438$AddTopic$txtARL": "",
                "dnn_ctr438_AddTopic_txtARL_ClientState": '{"enabled":true,"emptyMessage":"","validationText":"","valueAsString":"","minValue":0,"maxValue":9999,"lastSetTextBoxValue":""}',
                "dnn$ctr438$AddTopic$ddlBRT": 'เลือกสถานีรถเมล์ BRT',
                "dnn$ctr438$AddTopic$txtBRT": "",
                "dnn_ctr438_AddTopic_txtBRT_ClientState": '{"enabled":true,"emptyMessage":"","validationText":"","valueAsString":"","minValue":0,"maxValue":9999,"lastSetTextBoxValue":""}',
                "dnn$ctr438$AddTopic$ddlExtension": 'เลือกสถานีรถไฟฟ้าส่วนต่อขยาย',
                "dnn$ctr438$AddTopic$txtExtension": '',
                "dnn_ctr438_AddTopic_txtExtension_ClientState": '{"enabled":true,"emptyMessage":"","validationText":"","valueAsString":"","minValue":0,"maxValue":9999,"lastSetTextBoxValue":""}',
                "dnn$ctr438$AddTopic$ddlKeyword": 'พิมพ์คำสำคัญที่ต้องการให้ Google ค้นเจอ­',
                "dnn_ctr438_AddTopic_ddlKeyword_ClientState": '',
                "dnn$ctr438$AddTopic$txtName": postdata['name'],
                "dnn$ctr438$AddTopic$txtTelephone": postdata['mobile'],
                "dnn$ctr438$AddTopic$txtFax": '',
                "dnn$ctr438$AddTopic$txtEmail": postdata['email'],
                "dnn$ctr438$AddTopic$txtWebsite": '',
                "dnn$ctr438$AddTopic$lat_text": postdata['geo_latitude'],
                "dnn$ctr438$AddTopic$lng_text": postdata['geo_longitude'],
                "zoom_level": '7',
                "dnn$ctr438$AddTopic$topicHitNearSubway$ddlBTS": 'เลือกสถานีไฟฟ้า',
                "dnn$ctr438$AddTopic$topicHitNearSubway$ddlMRT": 'เลือกสถานีใต้ดิน',
                "ScrollTop": '2739',
                "__dnnVariable": '`{`__scdoff`:`1`,`sf_siteRoot`:`/`,`sf_tabId`:`91`}'
            }

            files = {}
            allimages = postdata["post_images"][:5]
            for i in range(1, len(allimages)+1):
                print(os.path.getsize(os.getcwd()+"/"+allimages[i-1]))
                r = open(os.getcwd()+"/"+allimages[i-1], 'rb')
                files["dnn$ctr438$AddTopic$FileUpload"+str(i)] = r

            r = self.httprequestObj.http_post(
                'https://home2all.com/%E0%B8%A5%E0%B8%87%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B8%81%E0%B8%B2%E0%B8%A8%E0%B8%9F%E0%B8%A3%E0%B8%B5', data=datapost, files=files)
            data = r.text
           
            soup=BeautifulSoup(r.text,'lxml')
            if soup.select("#dnn_ctr440_Thankyou_hplTopicId"):
                detail = "Post created successfully"
                post_url = soup.select("#dnn_ctr440_Thankyou_hplTopicId")[0]['href']
                post_id  = soup.select("#dnn_ctr440_Thankyou_hplTopicId")[0].text.strip()
            else:
                success = 'false'
                detail  = "Please check parameters"
        else:
            detail = "cannot login"
            # print(test_login)
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "websitename": "home2all",
            "success": success,
            "ds_id": postdata['ds_id'],
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
        }

    def edit_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        # start process
        # https://home2all.com/post/topicid/78776

        # login
        success = "True"
        if 'name' not in postdata:
            success = "False"
            detail  = "Please fill name"
        elif 'mobile' not in postdata:
            success = "False"
            detail  = "Please fill mobile number"
        elif 'email' not in postdata:
            success = "False"
            detail  = "Please fill email"
        if success=="False":
            time_end = datetime.datetime.utcnow()
            time_usage = time_end-time_start
            return {
                "websitename": "home2all",
                "success": success,
                "ds_id": postdata['ds_id'],
                "usage_time": str(time_usage),
                "start_time": str(time_start),
                "end_time": str(time_end),
                "post_url": "",
                "post_id": postdata['post_id'],
                "account_type": "null",
                "detail": detail
            }


        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]
        

        post_id = ""
        post_url = ""

        proid = {
            'คอนโด': '1',
            'บ้านเดี่ยว': '2',
            'บ้านแฝด': '3',
            'ทาวน์เฮ้าส์': '4',
            'ตึกแถว-อาคารพาณิชย์': '5',
            'ที่ดิน': '6',
            'อพาร์ทเมนท์': '7',
            'โรงแรม': '8',
            'ออฟฟิศสำนักงาน': '9',
            'โกดัง': '10',
            'โรงงาน':'25'
        }
        getProdId = {'1': 3, '2': 1, '3': 9, '4': 2,
                     '5': 7, '6': 5, '7': 4, '8': 9, '9': 9, '10': 9, '25': 11}

        try:
            theprodid = getProdId[proid[str(postdata['property_type'])]]
        except:
            theprodid = getProdId[str(postdata['property_type'])]

        # print(theprodid)
        
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
        
        # print(province_id)
        # print(amphur_id)
        # print(postdata['addr_district'])
        
        prod_address = ""
        
        for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
            if add is not None:
                prod_address += add+" "

        if postdata['land_size_rai'] == None or postdata['land_size_rai'] == '':
            postdata['land_size_rai'] = 0

        if postdata['land_size_ngan'] == None or postdata['land_size_ngan'] == '':
            postdata['land_size_ngan'] = 0

        if postdata['land_size_wa'] == None or postdata['land_size_wa'] == '':
            postdata['land_size_wa'] = 0

        print(postdata['land_size_wa'])

        area = str(400*int(postdata['land_size_rai']) + 100 *int(postdata['land_size_ngan']) + int(postdata['land_size_wa']))
        typ = '2'

        if theprodid != 5:
            if 'floor_area' not in postdata or postdata['floor_area'] == None:
                if 'floorarea_sqm' not in postdata or postdata['floorarea_sqm'] == None:
                    area ='0'
                else:
                    area = str(postdata['floorarea_sqm'])
                    typ = '3'
            else:
                area = str(postdata['floor_area'])
                typ = '3' 

        if int(area) > 999:
            if typ == '2':
                area = str(int(area)//400)
                typ='1'
            else:
                area = str(int(area)//4)
                typ='2'
                if int(area) > 999:
                    area = str(int(area)//400)
                    typ='1'

        prod_address = prod_address[:-1]

        postdata['price_baht'] = str(postdata['price_baht'])

        if 'floor_total' not in postdata:
                postdata['floor_total']=""
        else:
                postdata['floor_total']=str(postdata['floor_total'])

        
        if 'floor_level' not in postdata:
                postdata['floor_level']=""
        else:
                postdata['floor_level']=str(postdata['floor_level'])

        if 'project_name' not in postdata:
                postdata['project_name']=""
        
        if 'bath_room' not in postdata:
                postdata['bath_room']=""
        else:
                postdata['bath_room']=str(postdata['bath_room'])
        
        if 'bed_room' not in postdata:
                postdata['bed_room']=""
        else:
                postdata['bed_room']=str(postdata['bed_room'])
        
        listing = 0 
        
        if postdata['listing_type'] != 'ขาย':
            listing = 3
        else:
            listing = 1






        if success == "true":
            r = self.httprequestObj.http_get(
                'https://home2all.com/post/topicid/'+str(postdata['post_id']))

            print(r.text)
            
            if r.text.find('ไม่พบประกาศที่ต้องการ') == -1:
                soup = BeautifulSoup(r.text, features=self.parser) 
                topic = soup.find(attrs={"id": "dnn_ctr441_ViewTopic_topicDetailInLine_hplTopicId"})
                # topic = soup.find(attrs={"name": "dnn$ctr438$AddTopic$txtTopic"})
                if topic.text.strip() == str(postdata['post_id']):
                # if topic and topic.get('value'):
                    # print(topic.get('value'), len(topic.get('value')))
                    r = self.httprequestObj.http_get(
                        'https://home2all.com/%E0%B8%A5%E0%B8%87%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B8%81%E0%B8%B2%E0%B8%A8%E0%B8%9F%E0%B8%A3%E0%B8%B5/topicid/'+postdata['post_id']+'/trk/-1')
                    soup = BeautifulSoup(r.text, features=self.parser)
                    viewstate = soup.select_one("#__VIEWSTATE")['value']
                    datapost = {
                        'StylesheetManager_TSSM': ';Telerik.Web.UI, Version=2013.2.717.40, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en-US:dae8717e-3810-4050-96d3-31018e70c6e4:1c2121e:e24b8e95:aac1aeb7:c73cf106',
                        'ScriptManager_TSM': ';;AjaxControlToolkit, Version=4.1.51116.0, Culture=neutral, PublicKeyToken=28f01b0e84b6d53e:en:fd384f95-1b49-47cf-9b47-2fa2a921a36a:ea597d4b:b25378d2;Telerik.Web.UI, Version=2013.2.717.40, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en:dae8717e-3810-4050-96d3-31018e70c6e4:16e4e7cd:f7645509:24ee1bba:f46195d3:2003d0b8:1e771326:aa288e2d:b7778d6c:e085fe68',
                        '__EVENTTARGET': 'dnn$ctr438$AddTopic$btnSubmit',
                        '__EVENTARGUMENT': '',
                        '__LASTFOCUS': '',
                        "__VIEWSTATE": viewstate,
                        "__VIEWSTATEGENERATOR": "CA0B0334",
                        "sid": "20090729-GP-be8e7bbb9f842760f6cab9b4f40e5787",
                        "dnn$ctr438$AddTopic$ddlNewProject": "โปรดกรอกชื่อโครงการที่เกี่ยวข้องกับประกาศของท่าน",
                        "dnn_ctr438_AddTopic_ddlNewProject_ClientState": "",
                        "dnn$ctr438$AddTopic$ddlType": listing,
                        "dnn$ctr438$AddTopic$ddlPropertyType": theprodid,
                        "dnn$ctr438$AddTopic$txtTopic": postdata["post_title_th"],
                        "dnn$ctr438$AddTopic$txtDescription": postdata["post_description_th"],
                        "dnn$ctr438$AddTopic$txtLocation": prod_address,
                        "dnn$ctr438$AddTopic$ddlProvince": province_id,
                        "dnn$ctr438$AddTopic$ddlAumphur": amphur_id,
                        "dnn$ctr438$AddTopic$txtNumAllFloor": postdata['floor_total'],
                        "dnn_ctr438_AddTopic_txtNumAllFloor_ClientState": '{"enabled":true,"emptyMessage":"","validationText":"'+postdata['floor_total']+'","valueAsString":"'+postdata['floor_total']+'","minValue":0,"maxValue":99,"lastSetTextBoxValue":"'+postdata['floor_total']+'"}',
                        "dnn$ctr438$AddTopic$txtNumFloor": postdata['floor_level'],
                        "dnn_ctr438_AddTopic_txtNumFloor_ClientState": '{"enabled":true,"emptyMessage":"","validationText":"'+postdata['floor_level']+'","valueAsString":"'+postdata['floor_level']+'","minValue":0,"maxValue":99,"lastSetTextBoxValue":"'+postdata['floor_level']+'"}',
                        "dnn$ctr438$AddTopic$txtRoom": postdata['bed_room'],
                        "dnn_ctr438_AddTopic_txtRoom_ClientState": '{"enabled":true,"emptyMessage":"","validationText":"'+postdata['bed_room']+'","valueAsString":"'+postdata['bed_room']+'","minValue":0,"maxValue":99,"lastSetTextBoxValue":"'+postdata['bed_room']+'"}',
                        "dnn$ctr438$AddTopic$txtBath": postdata['bath_room'],
                        "dnn_ctr438_AddTopic_txtBath_ClientState": '{"enabled":true,"emptyMessage":"","validationText":"'+postdata['bath_room']+'","valueAsString":"'+postdata['bath_room']+'","minValue":0,"maxValue":99,"lastSetTextBoxValue":"'+postdata['bath_room']+'"}',
                        "dnn$ctr438$AddTopic$txtArea": area,
                        "dnn_ctr438_AddTopic_txtArea_ClientState": '{"enabled":true,"emptyMessage":"","validationText":"'+area+'","valueAsString":"'+area+'","minValue":0,"maxValue":999999999,"lastSetTextBoxValue":"'+area+'"}',
                        "dnn$ctr438$AddTopic$ddlArea": '3',
                        "dnn$ctr438$AddTopic$txtPrice": postdata['price_baht'],
                        "dnn_ctr438_AddTopic_txtPrice_ClientState": '{"enabled":true,"emptyMessage":"","validationText":"'+postdata['price_baht']+'","valueAsString":"'+postdata['price_baht']+'","minValue":0,"maxValue":999999999,"lastSetTextBoxValue":"'+postdata['price_baht']+'"}',
                        "dnn$ctr438$AddTopic$ddlBTS": 'เลือกสถานีไฟฟ้า',
                        "dnn$ctr438$AddTopic$txtBTS": '',
                        "dnn_ctr438_AddTopic_txtBTS_ClientState": '{"enabled":true,"emptyMessage":"","validationText":"","valueAsString":"","minValue":0,"maxValue":9999,"lastSetTextBoxValue":""}',
                        "dnn$ctr438$AddTopic$ddlMRT": 'เลือกสถานีใต้ดิน',
                        "dnn$ctr438$AddTopic$txtMRT": "",
                        "dnn_ctr438_AddTopic_txtMRT_ClientState": '{"enabled":true,"emptyMessage":"","validationText":"","valueAsString":"","minValue":0,"maxValue":9999,"lastSetTextBoxValue":""}',
                        "dnn$ctr438$AddTopic$ddlARL": 'เลือกสถานีแอร์พอร์ตลิงค์',
                        "dnn$ctr438$AddTopic$txtARL": "",
                        "dnn_ctr438_AddTopic_txtARL_ClientState": '{"enabled":true,"emptyMessage":"","validationText":"","valueAsString":"","minValue":0,"maxValue":9999,"lastSetTextBoxValue":""}',
                        "dnn$ctr438$AddTopic$ddlBRT": 'เลือกสถานีรถเมล์ BRT',
                        "dnn$ctr438$AddTopic$txtBRT": "",
                        "dnn_ctr438_AddTopic_txtBRT_ClientState": '{"enabled":true,"emptyMessage":"","validationText":"","valueAsString":"","minValue":0,"maxValue":9999,"lastSetTextBoxValue":""}',
                        "dnn$ctr438$AddTopic$ddlExtension": 'เลือกสถานีรถไฟฟ้าส่วนต่อขยาย',
                        "dnn$ctr438$AddTopic$txtExtension": '',
                        "dnn_ctr438_AddTopic_txtExtension_ClientState": '{"enabled":true,"emptyMessage":"","validationText":"","valueAsString":"","minValue":0,"maxValue":9999,"lastSetTextBoxValue":""}',
                        "dnn$ctr438$AddTopic$ddlKeyword": 'พิมพ์คำสำคัญที่ต้องการให้ Google ค้นเจอ­',
                        "dnn_ctr438_AddTopic_ddlKeyword_ClientState": '',
                        "dnn$ctr438$AddTopic$txtName": postdata['name'],
                        "dnn$ctr438$AddTopic$txtTelephone": postdata['mobile'],
                        "dnn$ctr438$AddTopic$txtFax": '',
                        "dnn$ctr438$AddTopic$txtEmail": postdata['email'],
                        "dnn$ctr438$AddTopic$txtWebsite": '',
                        "dnn$ctr438$AddTopic$lat_text": postdata['geo_latitude'],
                        "dnn$ctr438$AddTopic$lng_text": postdata['geo_longitude'],
                        "zoom_level": '7',
                        "dnn$ctr438$AddTopic$topicHitNearSubway$ddlBTS": 'เลือกสถานีไฟฟ้า',
                        "dnn$ctr438$AddTopic$topicHitNearSubway$ddlMRT": 'เลือกสถานีใต้ดิน',
                        "ScrollTop": '2739',
                        "__dnnVariable": '`{`__scdoff`:`1`,`sf_siteRoot`:`/`,`sf_tabId`:`91`}'
                    }

                    files = {}
                    allimages = postdata["post_images"][:5]
                    for i in range(1, len(allimages)+1):
                        r = open(os.getcwd()+"/"+allimages[i-1], 'rb')
                        files["dnn$ctr438$AddTopic$FileUpload"+str(i)] = r

                    r = self.httprequestObj.http_post(
                        'https://home2all.com/%E0%B8%A5%E0%B8%87%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B8%81%E0%B8%B2%E0%B8%A8%E0%B8%9F%E0%B8%A3%E0%B8%B5/topicid/'+postdata['post_id']+'/trk/-1', data=datapost, files=files)
                    data = r.text
                    soup = BeautifulSoup(r.text,'lxml')
                    if soup.select("#dnn_ctr440_Thankyou_hplTopicId"):
                        detail = "Post edited successfully!"
                        post_url = soup.select("#dnn_ctr440_Thankyou_hplTopicId")[0]['href']
                        post_id  = post_url.split('/')[-1]
                    else:
                        success = 'False'
                        detail  = "Please check parameters"
                    # print(post_id)
                    # print(postdata['post_id'])
                    if post_id != postdata['post_id']:
                        success = 'False'
                        detail = 'Wrong post id'
                    # with open('b.html','w') as f:
                    #     print(data,file=f)
                else:
                    success = "False"
                    detail = "Incorrect Post Id"
            else:
                    success = "False"
                    detail = "Incorrect Post Id"
        else:
            detail = "cannot login"
        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        log_id = ""
        if 'log_id' in postdata:
            log_id = postdata['log_id']
        return {
            "websitename": "home2all",
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": post_url,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": postdata['post_id'],
            "account_type": "null",
            "detail": detail,
        }

    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        success = test_login["success"]
        detail = test_login["detail"]

        if success == "true":
            r = self.httprequestObj.http_get(
                'https://home2all.com/post/topicid/'+postdata['post_id'])
            if r.text.find('ไม่พบประกาศที่ต้องการ') == -1:
                soup = BeautifulSoup(r.text, 'lxml')
                viewstate = soup.select_one("#__VIEWSTATE")['value']
                # print(viewstate)
                datapost = {
                    'StylesheetManager_TSSM': ';Telerik.Web.UI, Version=2013.2.717.40, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en-US:dae8717e-3810-4050-96d3-31018e70c6e4:92753c09:91f742eb',
                    'ScriptManager_TSM': ';;AjaxControlToolkit, Version=4.1.51116.0, Culture=neutral, PublicKeyToken=28f01b0e84b6d53e:en:fd384f95-1b49-47cf-9b47-2fa2a921a36a:ea597d4b:b25378d2;Telerik.Web.UI, Version=2013.2.717.40, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en:dae8717e-3810-4050-96d3-31018e70c6e4:16e4e7cd:f7645509:24ee1bba:92fe8ea0:f46195d3:fa31b949:874f8ea2:19620875:490a9d4e',
                    '__EVENTTARGET': 'dnn$ctr441$ViewTopic$topicDetail$btnDelete',
                    '__VIEWSTATE': viewstate,
                    "__VIEWSTATEGENERATOR": "CA0B0334"
                }
                r = self.httprequestObj.http_post(
                    'https://home2all.com/post/topicid/'+postdata['post_id'], data=datapost)
                # with open('b.html','w') as f:
                #     print(r.text,file=f)
                if r.text.find("You are using an unverified account") != -1:
                    success = "False"
                    detail = "Account Unverified"  
                else:
                    success = 'true'
                    detail = 'Delete post successful'
            else:
                success = "False"
                detail = "Incorrect Post Id"

        time_end = datetime.datetime.utcnow()
        return {
            "success": success,
            "time_usage": str(time_end - time_start),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": postdata['post_id'],
            "websitename": "home2all"

        }

    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        post_id = postdata['post_id']
        log_id = postdata['log_id']

        #
        #

        time_end = datetime.datetime.utcnow()
        return {
            "websitename": "home2all",
            "success": "false",
            "time_usage": time_end - time_start,
            "start_time": time_start,
            "end_time": time_end,
            "detail": "Cannot Edit & Save the post",
            'ds_id': postdata['ds_id'],
            "log_id": log_id,
            "post_id": post_id,
            "ds_id": postdata['ds_id'],
            "post_view": ""
        }

    def search_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()
        test_login = self.test_login(postdata)
        #https://home2all.com/post/topicid/832359
        success = test_login['success']
        detail = test_login['detail']

        post_url = ''
        post_id = ''
        post_found = 'false'
        post_create_time = ''
        post_modify_time = ''
        post_view = ''

        if test_login['success'] == "true":
            post_title = postdata['post_title_th'].replace('.  ','. ').replace('.', '')
            tURL = dict()
            date = []
            url = "https://home2all.com/my-post/txt/" + post_title.replace(' ', '%20')
            r = self.httprequestObj.http_get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            # print(soup.prettify())
            div1 = soup.find_all('div', attrs={'class': 'tb-topic_tr_alt'})
            div2 = soup.find_all('div', attrs={'class': 'tb-topic_tr'})
            posts = div1 + div2
            flag=0
            ind=0
            for i in posts:
                try:
                    title = i.find('h5').text
                    title = str(title).replace('\n','')
                except:
                    continue

                if title == post_title:
                    
                    success = 'true'
                    post_found = 'true'
                    post_url = str(i.find('div', {'class':'row'})['onclick']).replace('window.open(\'','').replace("', '_blank');  return false;",'')
                    post_id = post_url.split('/')[-1]
                    detail = 'Post Successfully Found'
                    for j in range(1,12):
                        """ num = str(j)
                        if len(num) == 1:
                            num = '0'+num
                        print(num) """
                        if i.find('span',attrs={'id':'dnn_ctr451_ShowTopic_tbTopic_ctl%02d_lblUpdateDate' % j}):
                           # post_modify_time = i.find('span',attrs={'id':'dnn_ctr451_ShowTopic_tbTopic_ctl{num}_lblUpdateDate'}).text
                           post_modify_time = i.find('span',attrs={'id':'dnn_ctr451_ShowTopic_tbTopic_ctl%02d_lblUpdateDate' % j}).text

                    flag=1
                    break
                ind+=1
            if flag != 1:
                detail = 'Post Not Found'
                

        return {
            "websitename": "home2all",
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "start_time": str(start_time),
            "end_time": str(datetime.datetime.utcnow()),
            "usage_time": str(datetime.datetime.utcnow() - start_time),
            "account_type":'null',
            "success": success,
            "detail": detail,
            "post_id": post_id,
            "post_url": post_url,
            "post_modify_time": post_modify_time,
            "post_create_time": post_create_time,
            "post_view": post_view,
            "post_found": post_found
        }
    def print_debug(self, msg):
        if(self.debug):
            print(msg)
        return "true"


# tri = home2all()
# dic = {
#     "geo_latitude": 13.710968,
#     "geo_longitude": 100.498459,
#     "property_id": None,
#     "post_title_th": "ขาย คอนโด watermark เจ้าพระยาริเวอร์ 105 ตรม. 2 นอน 2 น้ำ ชั้น 33 ทิศ เหนือ วิว เมือง Fully furnished",
#     "short_post_title_th": "ขาย  watermark เจ้าพระยาริเวอร์ 105 ตรม 2 ห้องนอน ชั้น 33",
#     "post_description_th": "ขาย คอนโด watermark เจ้าพระยาริเวอร์ 105 ตรม. 2 นอน 2 น้ำ ชั้น 33 ทิศ เหนือ วิว เมือง Fully furnished\n\n:: รายละเอียดห้อง ::\n - ขนาด 105 ตรม.\n - ชนิด 2 ห้องนอน 2 ห้องน้ำ \n - อาคาร 1 ชั้น 33\n - ระเบียงหันทางทิศ เหนือ วิว เมือง\n\n\n:: รายละเอียดโครงการ ::\n - ชื่อโครงการ: watermark เจ้าพระยาริเวอร์\n\n\n\nProject Owner: Major Development\nProject Area: 11 Rai\nNumber of building: 2\n52 floors 486 units\n\n:: สถานที่ใกล้เตียง ::\n- Senan fest: 1.2 km\n- icon SIAM : 2km\nพิกัด: http://maps.google.com/maps?q=13.710968,100.498459\n\nราคา: 13,900,000 บาท\n\nสนใจติดต่อ: NADECHAuto 0852546523\nLine: Pokajg\n#ณเดชพร็อพดพอร์ตี้",
#     "post_title_en": "Condo for sale at watermark ChaoPhraya River, 105 Sqm, 33th floor, fully furnished",
#     "short_post_title_en": None,
#     "post_description_en": ":: Room Details ::\n- Size 105 sqm.\n- Type 2 bed 2 bath\n- Fully furnished and electric appliances\n- Building 1, Floor 33\n- Balcony facing the city view\n\n:: Project Details ::\nProject Name: WaterMark Chaopraya River\nProject Owner: Major Development\nProject Area: 11 Rai\nNumber of building: 2\n52 floors 486 units",
#     "price_baht": 13900000,
#     "listing_type": "ขาย",
#     "property_type": "1",
#     "floor_level": 33,
#     "floor_total": 52,
#     "floor_area": 105,
#     "bath_room": 2,
#     "bed_room": 2,
#     "prominent_point": None,
#     "view_type": 17,
#     "direction_type": 11,
#     "addr_province": "กรุงเทพมหานคร",
#     "addr_district": "เขต คลองสาน",
#     "addr_sub_district": "บางลำภูล่าง",
#     "addr_road": None,
#     "addr_soi": None,
#     "addr_near_by": "- Senan fest: 1.2 km\n- icon SIAM : 2km",
#     "floorarea_sqm": 105,
#     "land_size_rai": None,
#     "land_size_ngan": None,
#     "land_size_wa": None,
#     "name": "NADECHAuto",
#     "mobile": "0852546523",
#     "email": "Puautopost@gmail.com",
#     "user": "parzodupso@yevme.com",
#     "pass": "123456aa9",
#     "line": "Pokajg",
#     "post_images": [
#         # "imgtmp/13964_2020042021:58:45/1.jpeg",
#         # "imgtmp/13964_2020042021:58:45/2.jpeg",
#         # "imgtmp/13964_2020042021:58:45/3.jpeg",
#         # "imgtmp/13964_2020042021:58:45/4.jpeg",
#         # "imgtmp/13964_2020042021:58:45/5.jpeg",
#         # "imgtmp/13964_2020042021:58:45/6.jpeg",
#         # "imgtmp/13964_2020042021:58:45/7.jpeg",
#         # "imgtmp/13964_2020042021:58:45/8.jpeg",
#         # "imgtmp/13964_2020042021:58:45/9.jpeg",
#         # "imgtmp/13964_2020042021:58:45/10.jpeg"
#     ]
# }
# dic = {"user": "sobif61866@homedepinst.com", "email": "sobif61866@homedepinst.com", "post_id": "82860", "pass": '123456aa', "addr_soi": "xyz", 'post_images': [],
#        "addr_road": "123", "addr_sub_district": "abc", "addr_district": "bbc", 'addr_province': "กระบี่", 'property_type': 'ที่ดิน',
#        "post_title_th": "ppppppppp", "post_description_th": "ahhahahaha", "price_baht": "128", 'name': 'shikhar',
#        'mobile': '', "tel": "0891999450", "name_th": "อัมรินทร์", "surname_th": "บุญเกิด", }
# print(tri.create_post(dic))
# {"user":"shikhar100mit@gmail.com","email": "rohibe8488@gotkmail.com", "id": "823", "pass": 12345678, "addr_soi": "xyz", "post_img_url_lists": ["http://pngimg.com/uploads/birds/birds_PNG115.png","http://pngimg.com/uploads/birds/birds_PNG111.png"],
# "addr_road": "123", "addr_sub_district": "abc", "addr_district": "bbc","addr_province": "กระบี่", "property_type": "1","post_title_th": "ppppppppp", "post_description_th": "ahhahahaha", "price_baht": "128", "name": "shikhar",        "mobile": ""}