import requests, re, random
from bs4 import BeautifulSoup
import json, datetime
from .lib_httprequest import *
from .lib_captcha import  *
httprequestObj = lib_httprequest()
import datetime
import time,math

def decodeEmail(e):
        de = ""
        k = int(e[:2], 16)
        for i in range(2, len(e)-1, 2):
            de += chr(int(e[i:i+2], 16)^k)
        return de

class ilovecondo:

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

    def register_user(self, data):
        start_time = datetime.datetime.utcnow()

        success = ''
        detail = ''
        postdata = {
            'ScriptManager': 'dnn$ctr$dnn$ctr$Register_UPPanel|dnn$ctr$Register$registerButton',
            '__EVENTTARGET': 'dnn$ctr$Register$registerButton',
            '__ASYNCPOST': 'true',
            'RadAJAXControlID': 'dnn_ctr_Register_UP',
            'dnn$ctr$Register$userForm$Username$Username_TextBox':str(data['user']),
            'dnn$ctr$Register$userForm$Password$Password_TextBox':str(data['pass']),
            'dnn$ctr$Register$userForm$PasswordConfirm$PasswordConfirm_TextBox':str(data['pass']),
            'dnn$ctr$Register$userForm$DisplayName$DisplayName_TextBox':str(data['name_th']),
            'dnn$ctr$Register$userForm$Email$Email_TextBox':str(data['user']),
            'dnn$ctr$Register$userForm$Telephone$Telephone_Control':str(data['tel']),
            'dnn$ctr$Register$ctlCaptcha':'',
            'StylesheetManager_TSSM':'',
            'ScriptManager_TSM':'',
            '__EVENTARGUMENT':'',
            '__VIEWSTATE':'',
            '__VIEWSTATEGENERATOR':'',
            '__dnnVariable':'',
            'ScrollTop':''

        }
        regex = '^\\w+([\\.-]?\\w+)*@\\w+([\\.-]?\\w+)*$'
        f1 = True
        regex = '^\\w+([\\.-]?\\w+)*@\\w+([\\.-]?\\w+)*$'
        if re.search(regex, postdata['dnn$ctr$Register$userForm$Email$Email_TextBox']):
            f1 = True
        else:
            f1 = False
        url = 'https://ilovecondo.net/Register?returnurl=https%3a%2f%2filovecondo.net%2f'
        req = httprequestObj.http_get(url)
        soup = BeautifulSoup(req.text,'html.parser')

        postdata['StylesheetManager_TSSM'] = soup.find('input',{'name':'StylesheetManager_TSSM'})['value']
        postdata['ScriptManager_TSM'] = soup.find('input',{'name':'ScriptManager_TSM'})['value']
        postdata['__VIEWSTATE'] = soup.find('input',{'name':'__VIEWSTATE'})['value']
        postdata['__VIEWSTATEGENERATOR'] = soup.find('input',{'name':'__VIEWSTATEGENERATOR'})['value']
        postdata['__dnnVariable'] = soup.find('input',{'name':'__dnnVariable'})['value']



        div = soup.find('div',{'class':'dnnLeft'})
        src = div.find('img')['src']
        ##print(src)
        url = 'https://www.ilovecondo.net'+str(src)
        response = httprequestObj.http_get(url)
        file = open('tmp.jpeg', 'wb')
        file.write(response.content)
        file.close()

        captcha_solver = lib_captcha()

        result = captcha_solver.imageCaptcha('tmp.jpeg')

        if (result[0] == 1):
            captcha_code = result[1]
            ##print(captcha_code)
            postdata['dnn$ctr$Register$ctlCaptcha'] = captcha_code
            headers = {
                'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
            }
            url = 'https://ilovecondo.net/Register?returnurl=https%3a%2f%2filovecondo.net%2f'
            req = httprequestObj.http_post(url,data=postdata,headers = headers)
            txt = str(req.text)


            if txt.find('A User Already Exists For the Username Specified. Please Register Again Using A Different Username') != -1:
                success = 'false'
                detail = 'Username already exists'
            elif txt.find('The requested password is invalid as it is either the same as the username or uses a term that is on the banned list of passwords') != -1:
                success = 'false'
                detail = 'Invalid Password'
            elif f1==False:
                success = 'false'
                detail = 'Invalid email'
            elif txt.find('The Display Name is already in use') != -1:
                success = 'false'
                detail = 'Invalid name(already in use)'
            else:
                success = 'true'
                detail = 'Successfully Registered'


        else:
            success = 'false'
            detail = 'Problem with captcha'


        end_time = datetime.datetime.utcnow()
        result = {'websitename':'ilovecondo',
         'success':success,
         'start_time':str(start_time),
         'end_time':str(end_time),
         'usage_time':str(end_time - start_time),
         'detail':detail,
         'ds_id':data['ds_id']}
        return result

    def test_login(self, data):
        req = httprequestObj.http_get('https://ilovecondo.net/%e0%b8%ab%e0%b8%99%e0%b9%89%e0%b8%b2%e0%b9%81%e0%b8%a3%e0%b8%81/ctl/Logoff')
        start_time = datetime.datetime.utcnow()

        success = ''
        detail = ''
        postdata = {

            '__EVENTTARGET': 'dnn$ctr$Login$Login_DNN$cmdLogin',
            'dnn$ctr$Login$Login_DNN$txtUsername': data['user'],
            'dnn$ctr$Login$Login_DNN$txtPassword': data['pass'],
            'StylesheetManager_TSSM': '',
            'ScriptManager_TSM': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '',
            '__VIEWSTATEGENERATOR': '',
            '__dnnVariable': '',
            'ScrollTop': ''

        }

        url = 'https://ilovecondo.net/Login?returnurl=%2f'
        req = httprequestObj.http_get(url)
        #time.sleep(5)
        soup = BeautifulSoup(req.text, 'html.parser')

        #postdata['StylesheetManager_TSSM'] = soup.find('input', {'name': 'StylesheetManager_TSSM'})['value']
        postdata['ScriptManager_TSM'] = soup.find('input', {'name': 'ScriptManager_TSM'})['value']
        postdata['__VIEWSTATE'] = soup.find('input', {'name': '__VIEWSTATE'})['value']
        postdata['__VIEWSTATEGENERATOR'] = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']
        postdata['__dnnVariable'] = soup.find('input', {'name': '__dnnVariable'})['value']


        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        }
        url = 'https://ilovecondo.net/Login?returnurl=%2f'
        req = httprequestObj.http_post(url, data=postdata, headers=headers)
        #time.sleep(5)
        txt = str(req.text)

        if txt.find('You are using an unverified account.') != -1:
                success = 'false'
                detail = 'Unverified account'
        elif txt.find('Logout') == -1:
            success = 'false'
            detail = 'Invalid credentials'

        else:
            success = 'true'
            detail = 'Successfully Login'



        end_time = datetime.datetime.utcnow()
        result = {'websitename':'ilovecondo',
         'success':success,
         'start_time':str(start_time),
         'end_time':str(end_time),
         'usage_time':str(end_time - start_time),
         'ds_id':data['ds_id'],
         'detail':detail}
        return result


    def create_post(self,data):
        start_time = datetime.datetime.utcnow()

        result = self.test_login(data)
        success = result['success']
        detail = result['detail']
        post_url = ''
        post_id = ''
        if success == 'true':
            postdata = {
                'StylesheetManager_TSSM':'',
                'ScriptManager_TSM':'',
                '__EVENTTARGET': 'dnn$ctr370$AddTopic$btnSubmit',
                '__EVENTARGUMENT':'',
                '__LASTFOCUS':'',
                '__VIEWSTATE':'',
                '__VIEWSTATEGENERATOR':'',
                'sid':'',
                'dnn$ctr370$AddTopic$ddlNewProject':'',

            }
            url = 'https://ilovecondo.net/new-post'
            req = httprequestObj.http_get(url)

            soup = BeautifulSoup(req.text,'html.parser')
            try:
                ##print('here')
                postdata['StylesheetManager_TSSM'] = soup.find('input',{'name':'StylesheetManager_TSSM'})['value']
                ##print('here1')
                postdata['ScriptManager_TSM'] = soup.find('input',{'name':'ScriptManager_TSM'})['value']
                ##print('here2')
                postdata['__VIEWSTATE'] = soup.find('input',{'name':'__VIEWSTATE'})['value']
                ##print('here3')
                postdata['__VIEWSTATEGENERATOR'] = soup.find('input',{'name':'__VIEWSTATEGENERATOR'})['value']
                ##print('here4')
                postdata['sid'] = soup.find('input',{'name':'sid'})['value']
                ##print('here5')
                ##print(data['web_project_name'],data['project_name'],data['post-title_th'])
                if 'web_project_name' not in data or data['web_project_name'] is None or str(data['web_project_name']).strip() == "":
                    if 'project_name' not in data or data['project_name'] is None or str(data['project_name']).strip() == '':
                        data['web_project_name'] = data['post_title_th']
                    else:
                        data['web_project_name'] = data['project_name']
                ##print('here6')
                url = 'https://ilovecondo.net/new-post'
                names = []
                req = httprequestObj.http_get(url)
                soup = BeautifulSoup(req.text,'html.parser')
                postdata['dnn_ctr370_AddTopic_ddlNewProject_ClientState'] = ''
                options = soup.find('ul',{'class':'rcbList'}).findAll('li',{'class':'rcbItem'})
                for opt in options:
                    names.append(opt.text)
                ind = -1
                for name in names:
                    ind+=1
                    if name == data['web_project_name']:
                        postdata['dnn$ctr370$AddTopic$ddlNewProject'] = data['web_project_name']
                        break
                if postdata['dnn$ctr370$AddTopic$ddlNewProject'] == "":
                    ind = -1
                    for name in names:
                        ind+=1
                        if name.find(data['web_project_name'])!=-1:
                            postdata['dnn$ctr370$AddTopic$ddlNewProject'] = data['web_project_name']
                            break
                if postdata['dnn$ctr370$AddTopic$ddlNewProject'] == "":
                    postdata['dnn$ctr370$AddTopic$ddlNewProject'] = data['web_project_name']
                    postdata['dnn_ctr370_AddTopic_ddlNewProject_ClientState'] = '{"logEntries":[],"value":"","text":"'+str(data['web_project_name'])+'","enabled":true,"checkedIndices":[],"checkedItemsTextOverflows":false}'
                else:
                    ##print('load')
                    with open('./static/ilovecondo_project_names.json') as data_file:
                        projects = json.load(data_file)
                    postdata['dnn_ctr370_AddTopic_ddlNewProject_ClientState'] = '{"logEntries":[],"value":"'+str(projects["project_names"][ind]['value'])+'","text":"' + str(postdata['dnn$ctr370$AddTopic$ddlNewProject']) + '","enabled":true,"checkedIndices":[],"checkedItemsTextOverflows":false}'
                    ##print('here')

                ##print(postdata['dnn$ctr370$AddTopic$ddlNewProject'],postdata['dnn_ctr370_AddTopic_ddlNewProject_ClientState'])

                if data['listing_type'] == 'ขาย':
                    postdata['dnn$ctr370$AddTopic$ddlType'] = '1'
                else:
                    postdata['dnn$ctr370$AddTopic$ddlType'] = '3'

                postdata['dnn$ctr370$AddTopic$ddlPropertyType'] = ''
                ids = {'คอนโด': '1',
                       'บ้านเดี่ยว': '2',
                       'บ้านแฝด': '3',
                       'ทาวน์เฮ้าส์': '4',
                       'ตึกแถว-อาคารพาณิชย์': '5',
                       'ที่ดิน': '6',
                       'อพาร์ทเมนท์': '7',
                       'โรงแรม': '8',
                       'ออฟฟิศสำนักงาน': '9',
                       'โกดัง-โรงงาน': '10',
                       'โรงงาน': '25'}
                property_tp = {'1': '3',
                               '2': '1',
                               '3': '1',
                               '4': '2',
                               '5': '9',
                               '6': '5',
                               '7': '4',
                               '8': '4',
                               '9': '9',
                               '10': '9',
                               '25': '9'}

                if str(data['property_type']) in property_tp:
                    postdata['dnn$ctr370$AddTopic$ddlPropertyType'] = property_tp[str(data['property_type'])]
                else:
                    postdata['dnn$ctr370$AddTopic$ddlPropertyType'] = property_tp[ids[str(data['property_type'])]]

                data['post_title_th'] = str(data['post_title_th']).replace('\n', '\r\n')
                postdata['dnn$ctr370$AddTopic$txtTopic'] = str(data['post_title_th'])
                data['post_description_th'] = str(data['post_description_th']).replace('\n','\r\n')
                #print(data['post_description_th'])

                postdata['dnn$ctr370$AddTopic$txtDescription'] = str(data['post_description_th'])
                ##print('address')
                postdata['dnn$ctr370$AddTopic$txtLocation'] = str(data['addr_road'])+','+str(data['addr_soi'])+','+str(data['addr_near_by'])
                ##print('address')
                postdata['dnn$ctr370$AddTopic$ddlProvince'] = ''
                provinces = []
                provinces_id = []
                options = soup.find('select',{'name':'dnn$ctr370$AddTopic$ddlProvince'}).findAll('option')
                for opt in options:
                    provinces.append(opt.text)
                    provinces_id.append(opt['value'])
                for i in range(len(provinces)):
                    if provinces[i].find(str(data['addr_province'])) !=-1:
                        postdata['dnn$ctr370$AddTopic$ddlProvince'] = str(provinces_id[i])
                        break
                if postdata['dnn$ctr370$AddTopic$ddlProvince'] == '':
                    postdata['dnn$ctr370$AddTopic$ddlProvince'] = provinces_id[0]

                ##print('done provinces',postdata['dnn$ctr370$AddTopic$ddlProvince'])
                postdata['dnn$ctr370$AddTopic$ddlAumphur'] = ''
                with open('./static/ilovecondo_province.json') as data1_file:
                    prov_data = json.load(data1_file)
                ##print('loaded')
                aumphurs = prov_data[postdata['dnn$ctr370$AddTopic$ddlProvince']]
                ##print(aumphurs)
                for i in range(len(aumphurs)):
                    for key in aumphurs[i]:
                        if str(key).find(data['addr_district'])!=-1:
                            postdata['dnn$ctr370$AddTopic$ddlAumphur'] = aumphurs[i][key]
                            break
                if postdata['dnn$ctr370$AddTopic$ddlAumphur'] == "":
                    for key in aumphurs[0]:
                        postdata['dnn$ctr370$AddTopic$ddlAumphur'] = aumphurs[0][key]
                        break

                ##print(postdata['dnn$ctr370$AddTopic$ddlProvince'],postdata['dnn$ctr370$AddTopic$ddlAumphur'])
                postdata['dnn$ctr370$AddTopic$txtNumAllFloor'] = str(data['floor_total'])

                postdata['dnn_ctr370_AddTopic_txtNumAllFloor_ClientState'] = '{"enabled": true, "emptyMessage": "","validationText": "'+str(data['floor_total'])+'", "valueAsString": "'+str(data['floor_total'])+'","minValue": 0, "maxValue": 99,"lastSetTextBoxValue": "'+str(data['floor_total'])+'"}'
                postdata['dnn$ctr370$AddTopic$txtNumFloor'] = str(data['floor_level'])
                postdata['dnn_ctr370_AddTopic_txtNumFloor_ClientState'] = '{"enabled": true, "emptyMessage": "","validationText": "'+str(data['floor_level'])+'", "valueAsString": "'+str(data['floor_level'])+'","minValue": 0, "maxValue": 99, "lastSetTextBoxValue": "'+str(data['floor_level'])+'"}'

                postdata['dnn$ctr370$AddTopic$txtRoom'] = str(data['bed_room'])
                postdata['dnn_ctr370_AddTopic_txtRoom_ClientState'] = '{"enabled": true, "emptyMessage": "", "validationText": "'+str(data['bed_room'])+'","valueAsString": "'+str(data['bed_room'])+'", "minValue": 0, "maxValue": 99,"lastSetTextBoxValue": "'+str(data['bed_room'])+'"}'

                postdata['dnn$ctr370$AddTopic$txtBath'] = str(data['bath_room'])
                postdata['dnn_ctr370_AddTopic_txtBath_ClientState'] = '{"enabled": true, "emptyMessage": "", "validationText": "'+str(data['bath_room'])+'","valueAsString": "'+str(data['bath_room'])+'", "minValue": 0, "maxValue": 99,"lastSetTextBoxValue": "'+str(data['bath_room'])+'"}'

                if str(data['property_type']) == '1' or str(data['property_type']) == '9':
                    postdata['dnn$ctr370$AddTopic$txtArea'] = str(data['floor_area'])
                    postdata['dnn_ctr370_AddTopic_txtArea_ClientState'] = '{"enabled": true, "emptyMessage": "", "validationText": "'+str(data['floor_area'])+'","valueAsString": "'+str(data['floor_area'])+'", "minValue": 0, "maxValue": 999,"lastSetTextBoxValue": "'+str(data['floor_area'])+'"}'

                    postdata['dnn$ctr370$AddTopic$ddlArea'] = '3'
                else:
                    #print('herein')
                    if data['land_size_rai'] is None or data['land_size_rai'] == '':
                        data['land_size_rai'] = '0'
                    if data['land_size_ngan'] is None or data['land_size_ngan'] == '':
                        data['land_size_ngan'] = '0'
                    if data['land_size_wa'] is None or data['land_size_wa'] == '':
                        data['land_size_wa'] = '0'
                    #print('hereout')
                    data['floor_area'] = 400*float(data['land_size_rai']) + 100 * float(data['land_size_ngan']) + float(data['land_size_wa'])
                    if data['floor_area']<=999:
                        postdata['dnn$ctr370$AddTopic$txtArea'] = str(int(round(data['floor_area'],0)))

                        data['floor_area'] = postdata['dnn$ctr370$AddTopic$txtArea']

                        #print(postdata['dnn$ctr370$AddTopic$txtArea'])
                        postdata[
                            'dnn_ctr370_AddTopic_txtArea_ClientState'] = '{"enabled": true, "emptyMessage": "", "validationText": "' + str(
                            data['floor_area']) + '","valueAsString": "' + str(
                            data['floor_area']) + '", "minValue": 0, "maxValue": 999,"lastSetTextBoxValue": "' + str(
                            data['floor_area']) + '"}'

                        postdata['dnn$ctr370$AddTopic$ddlArea'] = '2'

                postdata['dnn$ctr370$AddTopic$txtPrice'] = str(data['price_baht'])
                postdata['dnn_ctr370_AddTopic_txtPrice_ClientState'] = '{"enabled":true,"emptyMessage":"","validationText":"'+str(data['price_baht'])+'","valueAsString":"'+str(data['price_baht'])+'","minValue":0,"maxValue":999999999,"lastSetTextBoxValue":"'+str(data['price_baht'])+'"}'
                postdata['dnn$ctr370$AddTopic$ddlBTS'] = 'เลือกสถานีไฟฟ้า'
                postdata['dnn$ctr370$AddTopic$txtBTS'] = ''
                postdata['dnn_ctr370_AddTopic_txtBTS_ClientState'] = '{"enabled":true,"emptyMessage":"","validationText":"","valueAsString":"","minValue":0,"maxValue":9999,"lastSetTextBoxValue":""}'
                postdata['dnn$ctr370$AddTopic$ddlMRT'] = 'เลือกสถานีใต้ดิน'
                postdata['dnn$ctr370$AddTopic$txtMRT'] = ''
                postdata['dnn_ctr370_AddTopic_txtMRT_ClientState'] = '{"enabled":true,"emptyMessage":"","validationText":"","valueAsString":"","minValue":0,"maxValue":9999,"lastSetTextBoxValue":""}'
                postdata['dnn$ctr370$AddTopic$ddlARL'] = 'เลือกสถานีแอร์พอร์ตลิงค์'
                postdata['dnn$ctr370$AddTopic$txtARL'] = ''
                postdata['dnn_ctr370_AddTopic_txtARL_ClientState'] = '{"enabled":true,"emptyMessage":"","validationText":"","valueAsString":"","minValue":0,"maxValue":9999,"lastSetTextBoxValue":""}'
                postdata['dnn$ctr370$AddTopic$ddlBRT'] = 'เลือกสถานีรถเมล์ BRT'
                postdata['dnn$ctr370$AddTopic$txtBRT'] = ''
                postdata['dnn_ctr370_AddTopic_txtBRT_ClientState'] = '{"enabled":true,"emptyMessage":"","validationText":"","valueAsString":"","minValue":0,"maxValue":9999,"lastSetTextBoxValue":""}'
                postdata['dnn$ctr370$AddTopic$ddlExtension'] = 'เลือกสถานีรถไฟฟ้าส่วนต่อขยาย'
                postdata['dnn$ctr370$AddTopic$txtExtension'] = ''
                postdata['dnn_ctr370_AddTopic_txtExtension_ClientState'] = '{"enabled":true,"emptyMessage":"","validationText":"","valueAsString":"","minValue":0,"maxValue":9999,"lastSetTextBoxValue":""}'
                postdata['dnn$ctr370$AddTopic$ddlKeyword'] = ''
                postdata['dnn_ctr370_AddTopic_ddlKeyword_ClientState'] = ''
                postdata['dnn$ctr370$AddTopic$txtName'] = str(data['name'])
                postdata['dnn$ctr370$AddTopic$txtTelephone'] = str(data['mobile'])
                postdata['dnn$ctr370$AddTopic$txtFax'] = ''
                postdata['dnn$ctr370$AddTopic$txtEmail'] = str(data['email'])
                postdata['dnn$ctr370$AddTopic$txtWebsite'] = ''

                if 'post_images' in data and len(data['post_images']) > 0:
                    pass
                else:
                    data['post_images'] = ['./imgtmp/default/white.jpg']

                file = []
                temp = 1

                if len(data['post_images']) <= 5:
                    for i in data['post_images']:
                        y = str(random.randint(0, 100000000000000000)) + ".jpg"
                        # ##print(y)
                        file.append((str('dnn$ctr370$AddTopic$FileUpload' + str(temp)), (y, open(i, "rb"), "image/jpg")))
                        temp = temp + 1

                else:
                    for i in data['post_images'][:5]:
                        y = str(random.randint(0, 100000000000000000)) + ".jpg"
                        # ##print(y)
                        file.append((str('dnn$ctr370$AddTopic$FileUpload' + str(temp)), (y, open(i, "rb"), "image/jpg")))
                        temp = temp + 1

                postdata['dnn$ctr370$AddTopic$lat_text'] = str(data['geo_latitude'])
                postdata['dnn$ctr370$AddTopic$lng_text'] = str(data['geo_longitude'])
                postdata['zoom_level'] = '15'
                postdata['dnn$ctr370$AddTopic$topicHitNearSubway$ddlBTS'] = 'เลือกสถานีไฟฟ้า'
                postdata['dnn$ctr370$AddTopic$topicHitNearSubway$ddlMRT'] = 'เลือกสถานีใต้ดิน'
                postdata['ScrollTop'] = '2299'
                url = 'https://ilovecondo.net/new-post'
                req = httprequestObj.http_get(url)

                soup = BeautifulSoup(req.text, 'html.parser')
                postdata['__dnnVariable'] = soup.find('input',{'name':'__dnnVariable'})['value']



                url = 'https://ilovecondo.net/new-post'
                headers = {
                    'User-Agnet':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
                }
                req = httprequestObj.http_post(url,data=postdata,files=file,headers=headers)
                txt = req.text
                if txt.find('ประกาศของคุณเป็นหมายเลขที่') == -1:
                    success = 'false'
                    detail = 'Something wrong happened'
                else:
                    success = 'true'
                    detail = 'Post created'
                    post_id = ''
                    post_url = ''
                    soup = BeautifulSoup(req.text,'html.parser')
                    post_url = soup.find('a',{'id':'dnn_ctr509_Thankyou_hplTopicId'})['href']
                    post_id = soup.find('a',{'id':'dnn_ctr509_Thankyou_hplTopicId'}).text
                    ##print(post_id,post_url)

            except Exception as e:
                print(e)
                success = 'false'
                detail = 'Network error'

        end_time = datetime.datetime.utcnow()
        result = {'success': success,
                  'usage_time': str(end_time - start_time),
                  'start_time': str(start_time),
                  'end_time': str(end_time),
                  'post_url': post_url,
                  'post_id': post_id,
                  'account_type': 'null',
                  'ds_id': data['ds_id'],
                  'detail': detail,
                  'websitename': 'ilovecondo'}
        return result

    def delete_post(self, data):
        ##print('in')
        test_login = self.test_login(data)
        success = test_login["success"]
        start_time = datetime.datetime.utcnow()
        end_time = datetime.datetime.utcnow()
        post_id = int(data["post_id"])
        detail = test_login["detail"]

        if success == "true":
            ##print('debug')
            valid_ids = []
            valid_info = []
            page_no = []
            # #print('debug')
            postdata = {}
            url = 'https://ilovecondo.net/my-post'
            req = httprequestObj.http_get(url)
            soup = BeautifulSoup(req.text, 'html.parser')
            total_pages = soup.find('input', {'name': 'dnn$ctr498$ShowTopic$lblTotalRows'})['value']
            total_pages = math.ceil(int(total_pages) / 15)
            ##print(total_pages)
            for i in range(total_pages):
                url = 'https://ilovecondo.net/my-post/pg/' + str(i + 1)
                req = httprequestObj.http_get(url)
                soup = BeautifulSoup(req.text, 'html.parser')
                supermarket = soup.find('div',{'class':'col-md-12 tb-topic supermarket'})

                posts = supermarket.findAll('div',{'class':'row tb-topic_tr_alt'})


                for post in posts:
                    id = ''
                    a_s = post.findAll('a')
                    url = str(a_s[1])
                    ind = url.find('topicid')+8
                    while url[ind]!="/":
                        id+=url[ind]
                        ind+=1
                    valid_ids.append(id)
                    ##print(a_s)
                    valid_info.append(a_s[2]['id'])
                    page_no.append(str(i+1))
                    ##print(valid_ids)
                    ##print(valid_info)
                posts = supermarket.findAll('div', {'class': 'row tb-topic_tr'})

                ##print(len(posts))

                for post in posts:
                    id = ''
                    a_s = post.findAll('a')
                    url = str(a_s[1])
                    ind = url.find('topicid') + 8
                    while url[ind] != "/":
                        id += url[ind]
                        ind += 1
                    valid_ids.append(id)
                    # #print(a_s)
                    valid_info.append(a_s[2]['id'])
                    page_no.append(str(i + 1))
                    ##print(valid_ids)
                    ##print(valid_info)

            if str(post_id) in valid_ids:
                save_page = ''
                for i in range(len(valid_ids)):
                    if valid_ids[i] == str(post_id):
                        postdata['__EVENTTARGET'] = str(valid_info[i]).replace('_', '$')
                        save_page = page_no[i]
                        ##print('here',postdata['__EVENTTARGET'])
                        break

                url = 'https://ilovecondo.net/my-post/pg/'+str(save_page)
                req = httprequestObj.http_get(url)
                soup = BeautifulSoup(req.text, 'html.parser')

                postdata['StylesheetManager_TSSM'] = soup.find('input',{'name':'StylesheetManager_TSSM'})['value']
                ##print('here1',postdata['StylesheetManager_TSSM'])
                postdata['ScriptManager_TSM'] = soup.find('input',{'name':'ScriptManager_TSM'})['value']
                ##print('here2',postdata['ScriptManager_TSM'])
                postdata['__EVENTARGUMENT'] = ''
                postdata['__LASTFOCUS'] = ''
                postdata['__VIEWSTATE'] = soup.find('input', {'name': '__VIEWSTATE'})['value']
                postdata['__VIEWSTATEGENERATOR'] = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']

                postdata['dnn$ctr498$ShowTopic$ddlType'] = '0'
                postdata['dnn$ctr498$ShowTopic$ddlPropertyType'] = '0'
                postdata['dnn$ctr498$ShowTopic$ddlProvince'] = '0'
                postdata['dnn$ctr498$ShowTopic$ddlAumphur'] = '0'
                postdata['dnn$ctr498$ShowTopic$txtMinPrice'] = 'ราคาเริ่มต้น'
                postdata['dnn_ctr498_ShowTopic_txtMinPrice_ClientState'] = '{"enabled": true, "emptyMessage": "ราคาเริ่มต้น","validationText": "", "valueAsString": "", "minValue": 0,"maxValue": 999999999, "lastSetTextBoxValue": "ราคาเริ่มต้น"}'
                postdata['dnn$ctr498$ShowTopic$txtMaxPrice'] = 'ราคาสูงสุด'
                postdata['dnn_ctr498_ShowTopic_txtMaxPrice_ClientState'] = '{"enabled": true, "emptyMessage": "ราคาสูงสุด","validationText": "", "valueAsString": "", "minValue": 0,"maxValue": 999999999, "lastSetTextBoxValue": "ราคาสูงสุด"}'
                postdata['dnn$ctr498$ShowTopic$ddlBTS'] = 'เลือกสถานีไฟฟ้าทั้งหมด'
                postdata['dnn$ctr498$ShowTopic$ddlMRT'] = 'เลือกสถานีใต้ดินทั้งหมด'
                postdata['dnn$ctr498$ShowTopic$ddlARL'] = 'เลือกสถานีแอร์พอร์ตลิงค์ทั้งหมด'
                postdata['dnn$ctr498$ShowTopic$ddlBRT'] = 'เลือกสถานีรถเมล์ BRT ทั้งหมด'
                postdata['dnn$ctr498$ShowTopic$ddlExtension'] = 'เลือกสถานีรถไฟฟ้าส่วนต่อขยายทั้งหมด'
                postdata['dnn$ctr498$ShowTopic$txtSearch'] = 'คำที่ต้องการค้นหา'
                postdata['dnn_ctr498_ShowTopic_txtSearch_ClientState'] = '{"enabled": true, "emptyMessage": "คำที่ต้องการค้นหา","validationText": "", "valueAsString": "","lastSetTextBoxValue": "คำที่ต้องการค้นหา"}'

                postdata['dnn$ctr498$ShowTopic$lblTotalRows'] = soup.find('input', {'name': 'dnn$ctr498$ShowTopic$lblTotalRows'})['value']
                postdata['dnn$ctr498$ShowTopic$topicHitNearSubway$ddlBTS'] = 'เลือกสถานีไฟฟ้า'
                postdata['dnn$ctr498$ShowTopic$topicHitNearSubway$ddlMRT'] = 'เลือกสถานีใต้ดิน'
                postdata['dnn$ctr498$ShowTopic$txtddlAumphur'] = soup.find('input', {'name': 'dnn$ctr498$ShowTopic$txtddlAumphur'})['value']
                postdata['dnn$ctr498$ShowTopic$RadWindow_ContentTemplate$C$rblOccurrence'] = soup.find('input', {'name': 'dnn$ctr498$ShowTopic$RadWindow_ContentTemplate$C$rblOccurrence'})['value']
                postdata['dnn$ctr498$ShowTopic$RadWindow_ContentTemplate$C$txtEmail'] = soup.find('input', {'name': 'dnn$ctr498$ShowTopic$RadWindow_ContentTemplate$C$txtEmail'})['value']
                postdata['dnn_ctr498_ShowTopic_RadWindow_ContentTemplate_ClientState'] = ''
                postdata['ScrollTop'] = '1844'
                postdata['__dnnVariable'] = soup.find('input', {'name': '__dnnVariable'})['value']

                url = 'https://ilovecondo.net/my-post/pg/'+str(save_page)
                #print(url)
                headers = {
                    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
                }
                req = httprequestObj.http_post(url,data=postdata,headers=headers)

                success = 'true'
                detail = 'Post deleted'
            else:
                success = 'false'
                detail = 'Invalid id'



        end_time = datetime.datetime.utcnow()
        result = {
            "success": success,
            "usage_time": str(end_time - start_time),
            "start_time": str(start_time),
            "end_time": str(end_time),
            "log_id": data['log_id'],
            'ds_id': data['ds_id'],
            "post_id": data['post_id'],
            "detail": detail,
            "websitename": "ilovecondo"
        }
        return result

    def boost_post(self, data):
        start_time = datetime.datetime.utcnow()
        # #print('start')
        post_id = str(data['post_id'])
        log_id = str(data['log_id'])
        result = self.test_login(data)
        success = result['success']
        detail = result['detail']

        if success == 'true':
            valid_ids = []
            valid_info = []
            page_no = []
            ##print('debug')
            postdata = {}
            url = 'https://ilovecondo.net/my-post'
            req = httprequestObj.http_get(url)
            soup = BeautifulSoup(req.text,'html.parser')
            total_pages = soup.find('input',{'name':'dnn$ctr498$ShowTopic$lblTotalRows'})['value']
            total_pages = math.ceil(int(total_pages)/15)
            ##print(total_pages)
            for i in range(total_pages):
                url = 'https://ilovecondo.net/my-post/pg/'+str(i+1)
                req = httprequestObj.http_get(url)
                soup = BeautifulSoup(req.text, 'html.parser')
                supermarket = soup.find('div', {'class': 'col-md-12 tb-topic supermarket'})

                posts = supermarket.findAll('div', {'class': 'row tb-topic_tr_alt'})

                ##print(len(posts))

                for post in posts:
                    id = ''
                    a_s = post.findAll('a')
                    url = str(a_s[1])
                    ind = url.find('topicid') + 8
                    while url[ind] != "/":
                        id += url[ind]
                        ind += 1
                    valid_ids.append(id)
                    # #print(a_s)
                    valid_info.append(a_s[0]['id'])
                    page_no.append(str(i+1))
                    ##print(valid_ids)
                    ##print(valid_info)
                posts = supermarket.findAll('div', {'class': 'row tb-topic_tr'})

                ##print(len(posts))

                for post in posts:
                    id = ''
                    a_s = post.findAll('a')
                    url = str(a_s[1])
                    ind = url.find('topicid') + 8
                    while url[ind] != "/":
                        id += url[ind]
                        ind += 1
                    valid_ids.append(id)
                    # #print(a_s)
                    valid_info.append(a_s[0]['id'])
                    page_no.append(str(i + 1))
                    ##print(valid_ids)
                    ##print(valid_info)

            if str(post_id) in valid_ids:
                save_page = ''
                for i in range(len(valid_ids)):
                    if valid_ids[i] == str(post_id):
                        postdata['__EVENTTARGET'] = str(valid_info[i]).replace('_', '$')
                        save_page = page_no[i]
                        ##print('here', postdata['__EVENTTARGET'])
                        break

                url = 'https://ilovecondo.net/my-post/pg/'+str(save_page)
                req = httprequestObj.http_get(url)
                soup = BeautifulSoup(req.text, 'html.parser')

                postdata['StylesheetManager_TSSM'] = soup.find('input', {'name': 'StylesheetManager_TSSM'})['value']
                ##print('here1', postdata['StylesheetManager_TSSM'])
                postdata['ScriptManager_TSM'] = soup.find('input', {'name': 'ScriptManager_TSM'})['value']
                ##print('here2', postdata['ScriptManager_TSM'])
                postdata['__EVENTARGUMENT'] = ''
                postdata['__LASTFOCUS'] = ''
                postdata['__VIEWSTATE'] = soup.find('input', {'name': '__VIEWSTATE'})['value']
                postdata['__VIEWSTATEGENERATOR'] = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']

                postdata['dnn$ctr498$ShowTopic$ddlType'] = '0'
                postdata['dnn$ctr498$ShowTopic$ddlPropertyType'] = '0'
                postdata['dnn$ctr498$ShowTopic$ddlProvince'] = '0'
                postdata['dnn$ctr498$ShowTopic$ddlAumphur'] = '0'
                postdata['dnn$ctr498$ShowTopic$txtMinPrice'] = 'ราคาเริ่มต้น'
                postdata[
                    'dnn_ctr498_ShowTopic_txtMinPrice_ClientState'] = '{"enabled": true, "emptyMessage": "ราคาเริ่มต้น","validationText": "", "valueAsString": "", "minValue": 0,"maxValue": 999999999, "lastSetTextBoxValue": "ราคาเริ่มต้น"}'
                postdata['dnn$ctr498$ShowTopic$txtMaxPrice'] = 'ราคาสูงสุด'
                postdata[
                    'dnn_ctr498_ShowTopic_txtMaxPrice_ClientState'] = '{"enabled": true, "emptyMessage": "ราคาสูงสุด","validationText": "", "valueAsString": "", "minValue": 0,"maxValue": 999999999, "lastSetTextBoxValue": "ราคาสูงสุด"}'
                postdata['dnn$ctr498$ShowTopic$ddlBTS'] = 'เลือกสถานีไฟฟ้าทั้งหมด'
                postdata['dnn$ctr498$ShowTopic$ddlMRT'] = 'เลือกสถานีใต้ดินทั้งหมด'
                postdata['dnn$ctr498$ShowTopic$ddlARL'] = 'เลือกสถานีแอร์พอร์ตลิงค์ทั้งหมด'
                postdata['dnn$ctr498$ShowTopic$ddlBRT'] = 'เลือกสถานีรถเมล์ BRT ทั้งหมด'
                postdata['dnn$ctr498$ShowTopic$ddlExtension'] = 'เลือกสถานีรถไฟฟ้าส่วนต่อขยายทั้งหมด'
                postdata['dnn$ctr498$ShowTopic$txtSearch'] = 'คำที่ต้องการค้นหา'
                postdata[
                    'dnn_ctr498_ShowTopic_txtSearch_ClientState'] = '{"enabled": true, "emptyMessage": "คำที่ต้องการค้นหา","validationText": "", "valueAsString": "","lastSetTextBoxValue": "คำที่ต้องการค้นหา"}'

                postdata['dnn$ctr498$ShowTopic$lblTotalRows'] = \
                soup.find('input', {'name': 'dnn$ctr498$ShowTopic$lblTotalRows'})['value']
                postdata['dnn$ctr498$ShowTopic$topicHitNearSubway$ddlBTS'] = 'เลือกสถานีไฟฟ้า'
                postdata['dnn$ctr498$ShowTopic$topicHitNearSubway$ddlMRT'] = 'เลือกสถานีใต้ดิน'
                postdata['dnn$ctr498$ShowTopic$txtddlAumphur'] = \
                soup.find('input', {'name': 'dnn$ctr498$ShowTopic$txtddlAumphur'})['value']
                postdata['dnn$ctr498$ShowTopic$RadWindow_ContentTemplate$C$rblOccurrence'] = \
                soup.find('input', {'name': 'dnn$ctr498$ShowTopic$RadWindow_ContentTemplate$C$rblOccurrence'})['value']
                postdata['dnn$ctr498$ShowTopic$RadWindow_ContentTemplate$C$txtEmail'] = \
                soup.find('input', {'name': 'dnn$ctr498$ShowTopic$RadWindow_ContentTemplate$C$txtEmail'})['value']
                postdata['dnn_ctr498_ShowTopic_RadWindow_ContentTemplate_ClientState'] = ''
                postdata['ScrollTop'] = '1844'
                postdata['__dnnVariable'] = soup.find('input', {'name': '__dnnVariable'})['value']

                url = 'https://ilovecondo.net/my-post/pg/'+str(save_page)
                #print(url)
                headers = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
                }
                req = httprequestObj.http_post(url, data=postdata, headers=headers)

                success = 'true'
                detail = 'Post Boosted'
            else:
                success = 'false'
                detail = 'Invalid id'

        end_time = datetime.datetime.utcnow()
        result = {
            "success": "true",
            "usage_time": str(end_time - start_time),
            "start_time": str(start_time),
            "end_time": str(end_time),
            "detail": detail,
            'ds_id': data['ds_id'],
            "log_id": log_id,
            "post_id": post_id,
            'websitename': 'ilovecondo'
        }
        # https://ilovecondo.net/new-post/topicid/910653/trk/78
        return result

    def edit_post(self,data):
        start_time = datetime.datetime.utcnow()

        result = self.test_login(data)
        success = result['success']
        detail = result['detail']
        post_url = ''
        post_id = data['post_id']
        if success == 'true':
            '''valid_ids = []
            valid_info = []
            # #print('debug')
            postdata = {}
            url = 'https://ilovecondo.net/my-post'
            req = httprequestObj.http_get(url)
            print(req.url)
            print(req.status_code)

            with open('b.html', 'w') as f:
                f.write(req.text)
            
            soup = BeautifulSoup(req.text, 'html.parser')
            total_pages = soup.find('input', {'name': 'dnn$ctr498$ShowTopic$lblTotalRows'})['value']
            total_pages = math.ceil(int(total_pages) / 15)
            ##print(total_pages)
            for i in range(total_pages):
                url = 'https://ilovecondo.net/my-post/pg/' + str(i + 1)
                req = httprequestObj.http_get(url)
                soup = BeautifulSoup(req.text, 'html.parser')
                supermarket = soup.find('div', {'class': 'col-md-12 tb-topic supermarket'})

                posts = supermarket.findAll('div', {'class': 'row tb-topic_tr_alt'})

                # #print(len(posts))

                for post in posts:
                    id = ''
                    a_s = post.findAll('a')
                    url = str(a_s[1])
                    ind = url.find('topicid') + 8
                    while url[ind] != "/":
                        id += url[ind]
                        ind += 1
                    valid_ids.append(id)
                    # #print(a_s)
                    valid_info.append(a_s[0]['id'])
                    # #print(valid_ids)
                    # #print(valid_info)
                posts = supermarket.findAll('div', {'class': 'row tb-topic_tr'})

                # #print(len(posts))

                for post in posts:
                    id = ''
                    a_s = post.findAll('a')
                    url = str(a_s[1])
                    ind = url.find('topicid') + 8
                    while url[ind] != "/":
                        id += url[ind]
                        ind += 1
                    valid_ids.append(id)
                    # #print(a_s)
                    valid_info.append(a_s[0]['id'])
                    # #print(valid_ids)
                    # #print(valid_info)

            if str(post_id) in valid_ids:'''
                
            url = 'https://ilovecondo.net/post/topicid/'+str(post_id)
            req = httprequestObj.http_get(url)
            soup = BeautifulSoup(req.text,'html.parser')
            post_mail = decodeEmail(str(soup.find('a',{'id':'dnn_ctr374_ViewTopic_topicDetail_hplEmail'})['href'])[28:])
            if req.text.find('ไม่พบประกาศที่ต้องการ') == -1 and post_mail == data['email']:
                

                postdata = {
                    'StylesheetManager_TSSM':'',
                    'ScriptManager_TSM':'',
                    '__EVENTTARGET': 'dnn$ctr370$AddTopic$btnSubmit',
                    '__EVENTARGUMENT':'',
                    '__LASTFOCUS':'',
                    '__VIEWSTATE':'',
                    '__VIEWSTATEGENERATOR':'',
                    'sid':'',
                    'dnn$ctr370$AddTopic$ddlNewProject':'',

                }
                url = 'https://ilovecondo.net/new-post/topicid/'+str(post_id)+'/trk/78'
                req = httprequestObj.http_get(url)

                soup = BeautifulSoup(req.text,'html.parser')
                x=1
                if x==1:
                    ##print('here')
                    postdata['StylesheetManager_TSSM'] = soup.find('input',{'name':'StylesheetManager_TSSM'})['value']
                    ##print('here1')
                    postdata['ScriptManager_TSM'] = soup.find('input',{'name':'ScriptManager_TSM'})['value']
                    ##print('here2')
                    postdata['__VIEWSTATE'] = soup.find('input',{'name':'__VIEWSTATE'})['value']
                    ##print('here3')
                    postdata['__VIEWSTATEGENERATOR'] = soup.find('input',{'name':'__VIEWSTATEGENERATOR'})['value']
                    ##print('here4')
                    postdata['sid'] = soup.find('input',{'name':'sid'})['value']
                    ##print('here5')
                    ###print(data['web_project_name'],data['project_name'],data['post-title_th'])
                    if 'web_project_name' not in data or data['web_project_name'] is None or str(data['web_project_name']).strip() == "":
                        if 'project_name' not in data or data['project_name'] is None or str(data['project_name']).strip() == '':
                            data['web_project_name'] = data['post_title_th']
                        else:
                            data['web_project_name'] = data['project_name']
                    ##print('here6')
                    url = 'https://ilovecondo.net/new-post/topicid/'+str(post_id)+'/trk/78'
                    names = []
                    req = httprequestObj.http_get(url)
                    soup = BeautifulSoup(req.text,'html.parser')
                    postdata['dnn_ctr370_AddTopic_ddlNewProject_ClientState'] = ''
                    options = soup.find('ul',{'class':'rcbList'}).findAll('li',{'class':'rcbItem'})
                    for opt in options:
                        names.append(opt.text)
                    ind = -1
                    for name in names:
                        ind+=1
                        if name == data['web_project_name']:
                            postdata['dnn$ctr370$AddTopic$ddlNewProject'] = data['web_project_name']
                            break
                    if postdata['dnn$ctr370$AddTopic$ddlNewProject'] == "":
                        ind = -1
                        for name in names:
                            ind+=1
                            if name.find(data['web_project_name'])!=-1:
                                postdata['dnn$ctr370$AddTopic$ddlNewProject'] = data['web_project_name']
                                break
                    if postdata['dnn$ctr370$AddTopic$ddlNewProject'] == "":
                        postdata['dnn$ctr370$AddTopic$ddlNewProject'] = data['web_project_name']
                        postdata['dnn_ctr370_AddTopic_ddlNewProject_ClientState'] = '{"logEntries":[],"value":"","text":"'+str(data['web_project_name'])+'","enabled":true,"checkedIndices":[],"checkedItemsTextOverflows":false}'
                    else:
                        ##print('load')
                        with open('./static/ilovecondo_project_names.json') as data_file:
                            projects = json.load(data_file)
                        postdata['dnn_ctr370_AddTopic_ddlNewProject_ClientState'] = '{"logEntries":[],"value":"'+str(projects["project_names"][ind]['value'])+'","text":"' + str(postdata['dnn$ctr370$AddTopic$ddlNewProject']) + '","enabled":true,"checkedIndices":[],"checkedItemsTextOverflows":false}'
                        ##print('here')

                    ##print(postdata['dnn$ctr370$AddTopic$ddlNewProject'],postdata['dnn_ctr370_AddTopic_ddlNewProject_ClientState'])

                    if data['listing_type'] == 'ขาย':
                        postdata['dnn$ctr370$AddTopic$ddlType'] = '1'
                    else:
                        postdata['dnn$ctr370$AddTopic$ddlType'] = '3'

                    postdata['dnn$ctr370$AddTopic$ddlPropertyType'] = ''
                    ids = {'คอนโด': '1',
                           'บ้านเดี่ยว': '2',
                           'บ้านแฝด': '3',
                           'ทาวน์เฮ้าส์': '4',
                           'ตึกแถว-อาคารพาณิชย์': '5',
                           'ที่ดิน': '6',
                           'อพาร์ทเมนท์': '7',
                           'โรงแรม': '8',
                           'ออฟฟิศสำนักงาน': '9',
                           'โกดัง-โรงงาน': '10',
                           'โรงงาน': '25'}
                    property_tp = {'1': '3',
                                   '2': '1',
                                   '3': '1',
                                   '4': '2',
                                   '5': '9',
                                   '6': '5',
                                   '7': '4',
                                   '8': '4',
                                   '9': '9',
                                   '10': '9',
                                   '25': '9'}

                    if str(data['property_type']) in property_tp:
                        postdata['dnn$ctr370$AddTopic$ddlPropertyType'] = property_tp[str(data['property_type'])]
                    else:
                        postdata['dnn$ctr370$AddTopic$ddlPropertyType'] = property_tp[ids[str(data['property_type'])]]

                    data['post_title_th'] = str(data['post_title_th']).replace('\n', '\r\n')
                    postdata['dnn$ctr370$AddTopic$txtTopic'] = str(data['post_title_th'])
                    data['post_description_th'] = str(data['post_description_th']).replace('\n', '\r\n')
                    postdata['dnn$ctr370$AddTopic$txtDescription'] = str(data['post_description_th'])
                    ##print('address')
                    postdata['dnn$ctr370$AddTopic$txtLocation'] = str(data['addr_road'])+','+str(data['addr_soi'])+','+str(data['addr_near_by'])
                    ##print('address')
                    postdata['dnn$ctr370$AddTopic$ddlProvince'] = ''
                    provinces = []
                    provinces_id = []
                    options = soup.find('select',{'name':'dnn$ctr370$AddTopic$ddlProvince'}).findAll('option')
                    for opt in options:
                        provinces.append(opt.text)
                        provinces_id.append(opt['value'])
                    for i in range(len(provinces)):
                        if provinces[i].find(str(data['addr_province'])) !=-1:
                            postdata['dnn$ctr370$AddTopic$ddlProvince'] = str(provinces_id[i])
                            break
                    if postdata['dnn$ctr370$AddTopic$ddlProvince'] == '':
                        postdata['dnn$ctr370$AddTopic$ddlProvince'] = provinces_id[0]

                    ##print('done provinces',postdata['dnn$ctr370$AddTopic$ddlProvince'])
                    postdata['dnn$ctr370$AddTopic$ddlAumphur'] = ''
                    with open('./static/ilovecondo_province.json') as data1_file:
                        prov_data = json.load(data1_file)
                    ##print('loaded')
                    aumphurs = prov_data[postdata['dnn$ctr370$AddTopic$ddlProvince']]
                    ##print(aumphurs)
                    for i in range(len(aumphurs)):
                        for key in aumphurs[i]:
                            if str(key).find(data['addr_district'])!=-1:
                                postdata['dnn$ctr370$AddTopic$ddlAumphur'] = aumphurs[i][key]
                                break
                    if postdata['dnn$ctr370$AddTopic$ddlAumphur'] == "":
                        for key in aumphurs[0]:
                            postdata['dnn$ctr370$AddTopic$ddlAumphur'] = aumphurs[0][key]
                            break

                    ##print(postdata['dnn$ctr370$AddTopic$ddlProvince'],postdata['dnn$ctr370$AddTopic$ddlAumphur'])

                    if 'floor_total' not in data or data['floor_total'] is None or data['floor_total'] == '':
                        data['floor_total'] = '0'
                    if 'floor_level' not in data or data['floor_level'] is None or data['floor_level'] == '':
                        data['floor_level'] = '0'
                    if 'bed_room' not in data or data['bed_room'] is None or data['bed_room'] == '':
                        data['bed_room'] = '0'
                    if 'bath_room' not in data or data['bath_room'] is None or data['bath_room'] == '':
                        data['bath_room'] = '0'

                    postdata['dnn$ctr370$AddTopic$txtNumAllFloor'] = str(data['floor_total'])

                    postdata['dnn_ctr370_AddTopic_txtNumAllFloor_ClientState'] = '{"enabled": true, "emptyMessage": "","validationText": "'+str(data['floor_total'])+'", "valueAsString": "'+str(data['floor_total'])+'","minValue": 0, "maxValue": 99,"lastSetTextBoxValue": "'+str(data['floor_total'])+'"}'
                    postdata['dnn$ctr370$AddTopic$txtNumFloor'] = str(data['floor_level'])
                    postdata['dnn_ctr370_AddTopic_txtNumFloor_ClientState'] = '{"enabled": true, "emptyMessage": "","validationText": "'+str(data['floor_level'])+'", "valueAsString": "'+str(data['floor_level'])+'","minValue": 0, "maxValue": 99, "lastSetTextBoxValue": "'+str(data['floor_level'])+'"}'

                    postdata['dnn$ctr370$AddTopic$txtRoom'] = str(data['bed_room'])
                    postdata['dnn_ctr370_AddTopic_txtRoom_ClientState'] = '{"enabled": true, "emptyMessage": "", "validationText": "'+str(data['bed_room'])+'","valueAsString": "'+str(data['bed_room'])+'", "minValue": 0, "maxValue": 99,"lastSetTextBoxValue": "'+str(data['bed_room'])+'"}'

                    postdata['dnn$ctr370$AddTopic$txtBath'] = str(data['bath_room'])
                    postdata['dnn_ctr370_AddTopic_txtBath_ClientState'] = '{"enabled": true, "emptyMessage": "", "validationText": "'+str(data['bath_room'])+'","valueAsString": "'+str(data['bath_room'])+'", "minValue": 0, "maxValue": 99,"lastSetTextBoxValue": "'+str(data['bath_room'])+'"}'

                    if str(data['property_type']) == '1' or str(data['property_type']) == '9':
                        postdata['dnn$ctr370$AddTopic$txtArea'] = str(data['floor_area'])
                        postdata[
                            'dnn_ctr370_AddTopic_txtArea_ClientState'] = '{"enabled": true, "emptyMessage": "", "validationText": "' + str(
                            data['floor_area']) + '","valueAsString": "' + str(
                            data['floor_area']) + '", "minValue": 0, "maxValue": 999,"lastSetTextBoxValue": "' + str(
                            data['floor_area']) + '"}'

                        postdata['dnn$ctr370$AddTopic$ddlArea'] = '3'
                    else:
                        # print('herein')
                        if data['land_size_rai'] is None or data['land_size_rai'] == '':
                            data['land_size_rai'] = '0'
                        if data['land_size_ngan'] is None or data['land_size_ngan'] == '':
                            data['land_size_ngan'] = '0'
                        if data['land_size_wa'] is None or data['land_size_wa'] == '':
                            data['land_size_wa'] = '0'
                        # print('hereout')
                        data['floor_area'] = 400 * float(data['land_size_rai']) + 100 * float(
                            data['land_size_ngan']) + float(data['land_size_wa'])
                        if data['floor_area']<=999:
                            postdata['dnn$ctr370$AddTopic$txtArea'] = str(int(round(data['floor_area'], 0)))
                            data['floor_area'] = postdata['dnn$ctr370$AddTopic$txtArea']

                            # print(postdata['dnn$ctr370$AddTopic$txtArea'])
                            postdata[
                                'dnn_ctr370_AddTopic_txtArea_ClientState'] = '{"enabled": true, "emptyMessage": "", "validationText": "' + str(
                                data['floor_area']) + '","valueAsString": "' + str(
                                data['floor_area']) + '", "minValue": 0, "maxValue": 999,"lastSetTextBoxValue": "' + str(
                                data['floor_area']) + '"}'

                            postdata['dnn$ctr370$AddTopic$ddlArea'] = '2'
                    postdata['dnn$ctr370$AddTopic$txtPrice'] = str(data['price_baht'])
                    postdata['dnn_ctr370_AddTopic_txtPrice_ClientState'] = '{"enabled":true,"emptyMessage":"","validationText":"'+str(data['price_baht'])+'","valueAsString":"'+str(data['price_baht'])+'","minValue":0,"maxValue":999999999,"lastSetTextBoxValue":"'+str(data['price_baht'])+'"}'
                    postdata['dnn$ctr370$AddTopic$ddlBTS'] = 'เลือกสถานีไฟฟ้า'
                    postdata['dnn$ctr370$AddTopic$txtBTS'] = ''
                    postdata['dnn_ctr370_AddTopic_txtBTS_ClientState'] = '{"enabled":true,"emptyMessage":"","validationText":"","valueAsString":"","minValue":0,"maxValue":9999,"lastSetTextBoxValue":""}'
                    postdata['dnn$ctr370$AddTopic$ddlMRT'] = 'เลือกสถานีใต้ดิน'
                    postdata['dnn$ctr370$AddTopic$txtMRT'] = ''
                    postdata['dnn_ctr370_AddTopic_txtMRT_ClientState'] = '{"enabled":true,"emptyMessage":"","validationText":"","valueAsString":"","minValue":0,"maxValue":9999,"lastSetTextBoxValue":""}'
                    postdata['dnn$ctr370$AddTopic$ddlARL'] = 'เลือกสถานีแอร์พอร์ตลิงค์'
                    postdata['dnn$ctr370$AddTopic$txtARL'] = ''
                    postdata['dnn_ctr370_AddTopic_txtARL_ClientState'] = '{"enabled":true,"emptyMessage":"","validationText":"","valueAsString":"","minValue":0,"maxValue":9999,"lastSetTextBoxValue":""}'
                    postdata['dnn$ctr370$AddTopic$ddlBRT'] = 'เลือกสถานีรถเมล์ BRT'
                    postdata['dnn$ctr370$AddTopic$txtBRT'] = ''
                    postdata['dnn_ctr370_AddTopic_txtBRT_ClientState'] = '{"enabled":true,"emptyMessage":"","validationText":"","valueAsString":"","minValue":0,"maxValue":9999,"lastSetTextBoxValue":""}'
                    postdata['dnn$ctr370$AddTopic$ddlExtension'] = 'เลือกสถานีรถไฟฟ้าส่วนต่อขยาย'
                    postdata['dnn$ctr370$AddTopic$txtExtension'] = ''
                    postdata['dnn_ctr370_AddTopic_txtExtension_ClientState'] = '{"enabled":true,"emptyMessage":"","validationText":"","valueAsString":"","minValue":0,"maxValue":9999,"lastSetTextBoxValue":""}'
                    postdata['dnn$ctr370$AddTopic$ddlKeyword'] = ''
                    postdata['dnn_ctr370_AddTopic_ddlKeyword_ClientState'] = ''
                    postdata['dnn$ctr370$AddTopic$txtName'] = str(data['name'])
                    postdata['dnn$ctr370$AddTopic$txtTelephone'] = str(data['mobile'])
                    postdata['dnn$ctr370$AddTopic$txtFax'] = ''
                    postdata['dnn$ctr370$AddTopic$txtEmail'] = str(data['email'])
                    postdata['dnn$ctr370$AddTopic$txtWebsite'] = ''



                    postdata['dnn$ctr370$AddTopic$lat_text'] = str(data['geo_latitude'])
                    postdata['dnn$ctr370$AddTopic$lng_text'] = str(data['geo_longitude'])
                    postdata['zoom_level'] = '15'
                    postdata['dnn$ctr370$AddTopic$topicHitNearSubway$ddlBTS'] = 'เลือกสถานีไฟฟ้า'
                    postdata['dnn$ctr370$AddTopic$topicHitNearSubway$ddlMRT'] = 'เลือกสถานีใต้ดิน'
                    postdata['ScrollTop'] = '2299'
                    url = 'https://ilovecondo.net/new-post/topicid/' + str(post_id) + '/trk/78'
                    req = httprequestObj.http_get(url)

                    soup = BeautifulSoup(req.text, 'html.parser')
                    postdata['__dnnVariable'] = soup.find('input',{'name':'__dnnVariable'})['value']



                    url = 'https://ilovecondo.net/new-post/topicid/'+str(post_id)+'/trk/78'
                    headers = {
                        'User-Agnet':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
                    }
                    req = httprequestObj.http_post(url,data=postdata,headers=headers)
                    txt = req.text
                    if txt.find('ประกาศของคุณเป็นหมายเลขที่') == -1:
                        success = 'false'
                        detail = 'Something wrong happened'
                    else:
                        success = 'true'
                        detail = 'Post edited'
                        post_id = ''
                        post_url = ''
                        soup = BeautifulSoup(req.text,'html.parser')
                        post_url = soup.find('a',{'id':'dnn_ctr509_Thankyou_hplTopicId'})['href']
                        post_id = soup.find('a',{'id':'dnn_ctr509_Thankyou_hplTopicId'}).text
                        ##print(post_id,post_url)

                #except Exception as e:
                    #print(e)
                    #success = 'false'
                    #detail = str(e)
            else:
                success = 'false'
                detail = 'invalid post id'

        end_time = datetime.datetime.utcnow()
        result = {'success': success,
                  'usage_time': str(end_time - start_time),
                  'start_time': str(start_time),
                  'end_time': str(end_time),
                  'post_url': post_url,
                  'post_id': post_id,
                  'account_type': 'null',
                  'ds_id': data['ds_id'],
                  'log_id':data['log_id'],
                  'detail': detail,
                  'websitename': 'ilovecondo'}
        return result

    def search_post(self, data):
        start_time = datetime.datetime.utcnow()
        # #print('start')
        post_id = ''
        post_url = ''
        post_found = ''
        log_id = str(data['log_id'])
        result = self.test_login(data)
        success = result['success']
        detail = result['detail']

        if success == 'true':
            ##print('debug')
            postdata = {}
            valid_ids = []
            valid_info = []
            valid_titles = []
            page_no = []
            url = 'https://ilovecondo.net/my-post'
            req = httprequestObj.http_get(url)
            soup = BeautifulSoup(req.text, 'html.parser')
            total_pages = soup.find('input', {'name': 'dnn$ctr498$ShowTopic$lblTotalRows'})['value']
            total_pages = math.ceil(int(total_pages) / 15)
            ##print(total_pages)
            for i in range(total_pages):
                url = 'https://ilovecondo.net/my-post/pg/' + str(i + 1)
                req = httprequestObj.http_get(url)
                soup = BeautifulSoup(req.text, 'html.parser')
                supermarket = soup.find('div', {'class': 'col-md-12 tb-topic supermarket'})

                posts = supermarket.findAll('div', {'class': 'row tb-topic_tr_alt'})

                ##print(len(posts))

                for post in posts:
                    valid_titles.append(post.find('h5').text)
                    id = ''
                    a_s = post.findAll('a')
                    url = str(a_s[1])
                    ind = url.find('topicid') + 8
                    while url[ind] != "/":
                        id += url[ind]
                        ind += 1
                    valid_ids.append(id)
                    # #print(a_s)
                    valid_info.append(a_s[0]['id'])
                    page_no.append(str(i+1))
                    ##print(valid_ids)
                    ##print(valid_titles)
                posts = supermarket.findAll('div', {'class': 'row tb-topic_tr'})

                ##print(len(posts))

                for post in posts:
                    valid_titles.append(post.find('h5').text)
                    id = ''
                    a_s = post.findAll('a')
                    url = str(a_s[1])
                    ind = url.find('topicid') + 8
                    while url[ind] != "/":
                        id += url[ind]
                        ind += 1
                    valid_ids.append(id)
                    # #print(a_s)
                    valid_info.append(a_s[0]['id'])
                    page_no.append(str(i + 1))
                    ##print(valid_ids)
                    ##print(valid_titles)


            for i in range(len(valid_titles)):
                if valid_titles[i].strip() == str(data['post_title_th']).strip():
                    post_id = valid_ids[i]
                    post_url = 'https://ilovecondo.net/post/topicid/'+str(post_id)

                    break


            if post_url != '':
                post_found = 'true'
                detail = 'Post found'
            else:
                post_found = 'false'
                detail = 'Post not found'

        end_time = datetime.datetime.utcnow()
        result = {
            "success": "true",
            "usage_time": str(end_time - start_time),
            "start_time": str(start_time),
            "end_time": str(end_time),
            "detail": detail,
            'ds_id': data['ds_id'],
            "log_id": log_id,
            "post_found":post_found,
            "post_id": post_id,
            'post_url':post_url,
            "post_create_time": "",
            "post_modify_time": "",
            "post_view": "",
            'websitename': 'ilovecondo'
        }
        # https://ilovecondo.net/new-post/topicid/910653/trk/78
        return result
