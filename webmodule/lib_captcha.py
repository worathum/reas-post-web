from anticaptchaofficial.recaptchav2proxyless import *
from anticaptchaofficial.imagecaptcha import *
from anticaptchaofficial.hcaptchaproxyless import *
import requests
import os
import shutil
import time

class lib_captcha():
    def __init__(self):
        self.set_key = "b6cba1a55625222104231e2e3eeed069"
        
    def reCaptcha(self,sitekey, url):
        solver = recaptchaV2Proxyless()
        solver.set_verbose(1)
        solver.set_key(self.set_key)
        solver.set_website_url(url)
        solver.set_website_key(sitekey)

        g_response = solver.solve_and_return_solution()
        return g_response
    
    def HCaptcha(self,sitekey, url):
        solver = hCaptchaProxyless()
        solver.set_verbose(1)
        solver.set_key(self.set_key)
        solver.set_website_url(url)
        solver.set_website_key(sitekey)

        g_response = solver.solve_and_return_solution()
        return g_response

    def image_captcha(self,img_url):
        with open(os.getcwd() + '/imgtmp/Img_Captcha/imagecaptcha.jpg','wb') as local_file :
            response = requests.get(img_url,stream=True)
            if not response.ok:
                print (response)

            for block in response.iter_content(1024):
                if not block:
                    break

                local_file.write(block)
        print(os.stat(os.getcwd() + '/imgtmp/Img_Captcha/imagecaptcha.jpg').st_size)
        solver = imagecaptcha()
        solver.set_verbose(1)
        solver.set_key(self.set_key)
        captcha_text = solver.solve_and_return_solution(os.getcwd() + '/imgtmp/Img_Captcha/imagecaptcha.jpg')
        if captcha_text != 0:
            print ("captcha text "+captcha_text)
        else:
            print ("task finished with error "+solver.error_code)
        return captcha_text


    def imageCaptcha(self,image):
        solver = imagecaptcha()
        solver.set_verbose(1)
        solver.set_key(self.set_key)
        captcha_text = solver.solve_and_return_solution(image)
        if captcha_text != 0:
           return [1,captcha_text]
        else:
            return [-1,solver.error_code]
        
