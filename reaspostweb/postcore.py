# -*- coding: utf-8 -*-
import logging
import logging.config
import shutil
import datetime
import importlib
import sys
import json
import base64
import os
import string
import random
import concurrent.futures
from webmodule.lib_httprequest import *
httprequestObj = lib_httprequest()
import re
import time
import traceback




try:
    import configs
    import subprocess
    import platform
    time_update = time.strftime("%H%M")
except ImportError:
    configs = {}
if os.path.isdir('log') == False:
    os.mkdir('log')
logging.basicConfig(level=logging.INFO, filename='log/app-' + str(datetime.date.today()) + '.log', filemode='a', format='%(process)d-%(asctime)s-%(levelname)s-%(message)s', datefmt='%d-%b-%y %H:%M:%S')
# logging.config.dictConfig(getattr(configs, 'logging_config', {}))
# log = logging.getLogger()

# # new import using try be safe
# work pip install 04:00:00
if time_update == "0400":
    try:
        logging.info("==============================================================================")
        logging.info("==============================================================================")
        logging.info("==============================================================================")
        logging.info("==============================================================================")
        logging.warning("*/*\**/*\**/*\**/*\**/*\*UPDATE STARTING*/*\**/*\**/*\**/*\**/*\*") 
        logging.info("==============================================================================")
        logging.info("==============================================================================")
        logging.info("==============================================================================")
        logging.info("==============================================================================")
        logging.warning("PULL GIT: IN PROGRESS") 
        process_pull = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
        output_pull = process_pull.communicate()[0]
        logging.warning("PULL GIT: "+output_pull)
        logging.info("==============================================================================")
        logging.info("==============================================================================")

        logging.warning("RESTART SERVER: IN PROGRESS") 
        process_restart = subprocess.run(["pm2", "restart", "pm_config.json"])
        logging.warning("RESTART SERVER: "+process_restart) 
        logging.info("==============================================================================")
        logging.info("==============================================================================")
    except:
        try:
            logging.info("==============================================================================")
            logging.info("==============================================================================")
            if output_pull:
                logging.error("PULL GIT : ERROR")
                logging.warning("CODE: "+output_pull))
            if output_server:
                logging.error("RESTART SERVER : ERROR")
                logging.warning("CODE: "+process_restart) )
            logging.info("==============================================================================")
            logging.info("==============================================================================")
        except:
            pass
        pass


def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons	
        u"\U0001F44C-\U0001F919"  #Hand emoji
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)


class postcore():

    name = 'postcore'

    def __init__(self):
        self.secret_key = getattr(configs, 'secret_key', [])
        self.list_module = getattr(configs, 'list_module', [])
        self.list_action = getattr(configs, 'list_action', [])
        self.encoding = 'utf-8'
        logging.info('load app config success.')


    def coreworker(self, access_token, postdata):

        logging.info("==============================================================================")
        logging.info("==============================================================================")
        logging.info("==============================================================================")
        logging.info("INPUT POST DATA:")
        logging.warning(postdata) 
        logging.info("==============================================================================")
        logging.info("==============================================================================")
        logging.info("==============================================================================")


        # check secret key
        if self.secret_key != access_token:
            logging.error('wrong access token.')
            return {
                "success": "false",
                "detail": "Wrong access token",
            }

        # base64 decode postdata
        postdatajson = '{}'
        try:
            postdatajson = base64.b64decode(postdata)
        except ValueError as e:
            logging.error('base64 decode error.' + str(e))
            return {
                "success": "false",
                "detail": "Wrong data request (" + str(e) + ")",
            }

        # json decode to array
        try:
            datarequest = json.loads(postdatajson.decode('utf-8'))
        except ValueError as e:
            logging.error('json decode error.' + str(e))
            return {
                "success": "false",
                "detail": "Wrong json format (" + str(e) + ")",
            }
        
        if 'property_id' in datarequest:
            logging.warning("PR_ID : "+datarequest['property_id'])
        else:
            logging.warning("PR_ID : request not send.")
        logging.info("==============================================================================")

        # replace string \n to \r\n , \t to ''
        # TODO how to replace all dict by foreach or array walk?
        try:
            datarequest['post_title_th'] = deEmojify(datarequest['post_title_th'].strip().replace("/","-"))
            datarequest['post_title_th'] = deEmojify(re.sub(r'\n','\r\n',datarequest['post_title_th']))
            datarequest['post_title_en'] = deEmojify(re.sub(r'\n','\r\n',datarequest['post_title_en']))
            datarequest['short_post_title_th'] = deEmojify(re.sub(r'\n','\r\n',datarequest['short_post_title_th']))
            datarequest['short_post_title_en'] = deEmojify(re.sub(r'\n','\r\n',datarequest['short_post_title_en']))
            datarequest['post_description_th'] = deEmojify(re.sub(r'\n','\r\n',datarequest['post_description_th']))
            datarequest['post_description_en'] = deEmojify(re.sub(r'\n','\r\n',datarequest['post_description_en']))

            datarequest['post_title_th'] = re.sub(r'\t','',datarequest['post_title_th'])
            datarequest['post_title_en'] = re.sub(r'\t','',datarequest['post_title_en'])
            datarequest['short_post_title_th'] = re.sub(r'\t','',datarequest['short_post_title_th'])
            datarequest['short_post_title_en'] = re.sub(r'\t','',datarequest['short_post_title_en'])
            datarequest['post_description_th'] = re.sub(r'\t','',datarequest['post_description_th'])
            datarequest['post_description_en'] = re.sub(r'\t','',datarequest['post_description_en'])
        except:
            pass

# ===========================================================================
# correcting input
# ===========================================================================

        for key in datarequest.keys():
            if datarequest[key] == "\n":
                datarequest[key] = ""
        if 'project_name' in datarequest and datarequest['project_name'] == "":
            del datarequest['project_name']
 
        check_int = ['land_size_rai', 'land_size_ngan', 'land_size_wa', 'floor_area']
        for item in check_int:
            try:
                a = float(datarequest[item])
                datarequest[item] = str(int(a))
            except:
                datarequest[item] = '0'
        try:
            if int(datarequest['property_type'])  == 1:
                datarequest['land_size_wa'] = '0'
                datarequest['land_size_rai'] = '0'
                datarequest['land_size_ngan'] = '0'
        except:
            pass
# ===========================================================================
# ===========================================================================

        
# ===========================================================================
# check action in list
# ===========================================================================
        action = datarequest['action']
        if (action not in self.list_action):
            logging.error('action %s not allow', datarequest['action'])
            return {
                "success": "false",
                "detail": "Action not allow",
            }
# ===========================================================================
# ===========================================================================

        # default response
        response = {
            "success": "true",
            "action": action,
            "web": {},
        }

# ===========================================================================
# store image in img tmp
# ===========================================================================
        try:
            allimages = datarequest["post_img_url_lists"]
        except KeyError as e:
            allimages = {}
            # logging.warning(str(e))

        for i in range(6):
            dirtmp = 'imgupload_' + ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(16))
            uuni = dirtmp.split('_')[1]
            if os.path.isdir('imgtmp/' + dirtmp) == False:
                try:
                    os.mkdir("imgtmp/" + dirtmp)
                    logging.info('image directory imgtmp/%s is created', dirtmp)
                    time.sleep(0.2)
                except:
                    pass
                break
# ===========================================================================
# ===========================================================================

        datarequest['post_images'] = []
        imgcount = 1
        for imgurl in allimages:
            try:
                res = httprequestObj.http_get(imgurl, verify=False)
                # logging.info('get image from url %s', imgurl)
            except:
                # logging.warning('http connection error %s', imgurl)
                continue
            if res.status_code == 200:
                if int(res.headers['Content-Length']) > 0:
                    if res.headers['Content-Type'] == 'image/jpeg' or res.headers['Content-Type'] == 'image/png': # Please make the condition if there is no image, please send success false directly
                        try:
                            extension = res.headers['Content-Type'].split("/")[-1]
                            with open("imgtmp/" + dirtmp + "/" + str(imgcount) + "_" + uuni + "." + extension, 'wb') as f:
                                f.write(res.content)
                                f.close()
                            datarequest['post_images'].append("imgtmp/" + dirtmp + "/" + str(imgcount) + "_" + uuni + "." + extension)
                            imgcount = imgcount + 1
                        except:
                            pass
                    elif res.headers['Content-Type'] == 'application/octet-stream':
                        try:
                            extension = 'jpeg'
                            with open("imgtmp/" + dirtmp + "/" + str(imgcount) + "_" + uuni + "." + extension, 'wb') as f:
                                f.write(res.content)
                                f.close()
                            datarequest['post_images'].append("imgtmp/" + dirtmp + "/" + str(imgcount) + "_" + uuni + "." + extension)
                            imgcount = imgcount + 1
                        except:
                            pass
                    else:
                        logging.error('Issue with image urls')
                        weblists = datarequest['web']
                        web = {}
                        for webitem in weblists:
                            web[webitem['ds_name']] = {
                                "websitename": webitem['ds_name'],
                                "success": "false",
                                "detail": "ข้อมูลจากลิงค์รูปภาพของท่านมีประเภทที่ไม่สามารถดำเนินการในระบบได้ กรุณาตรวจสอบรูปภาพใหม่อีกครั้ง", #Your image url is not a proper content type.
                                "start_time": datetime.datetime.utcnow(),
                                "end_time": datetime.datetime.utcnow(),
                                "usage_time": datetime.datetime.utcnow(),
                                "ds_name": webitem['ds_name'],
                                "ds_id": webitem['ds_id'],
                                "account_type": "",
                                "post_url": "",
                                "post_id": "",
                            }
                            if 'log_id' in webitem:
                                web[webitem['ds_name']]['log_id'] = webitem['log_id']
                        return {
                            "success": "true",
                            "action": action,
                            "web": web
                        }
                else:
                    logging.error('Issue with image urls')
                    weblists = datarequest['web']
                    web = {}
                    for webitem in weblists:
                        web[webitem['ds_name']] = {
                            "websitename": webitem['ds_name'],
                            "success": "false",
                            "detail": "ลิงค์รูปภาพของท่านไม่มีข้อมูลรูปภาพ กรุณาตรวจสอบรูปภาพอีกครั้ง", #There is no image in your data. Please kindly recheck.
                            "start_time": datetime.datetime.utcnow(),
                            "end_time": datetime.datetime.utcnow(),
                            "usage_time": datetime.datetime.utcnow(),
                            "ds_name": webitem['ds_name'],
                            "ds_id": webitem['ds_id'],
                            "account_type": "",
                            "post_url": "",
                            "post_id": "",
                        }
                        if 'log_id' in webitem:
                            web[webitem['ds_name']]['log_id'] = webitem['log_id']
                    return {
                        "success": "true",
                        "action": action,
                        "web": web
                    }  
            else:
                logging.error('Issue with image urls')
                weblists = datarequest['web']
                web = {}
                for webitem in weblists:
                    web[webitem['ds_name']] = {
                        "websitename": webitem['ds_name'],
                        "success": "false",
                        "detail": "ไม่สามารถเชื่อมต่อลิงค์รูปภาพของท่านได้ กรุณาตรวจสอบรูปภาพใหม่อีกครั้ง", #Found 404 on your image link.
                        "start_time": datetime.datetime.utcnow(),
                        "end_time": datetime.datetime.utcnow(),
                        "usage_time": datetime.datetime.utcnow(),
                        "ds_name": webitem['ds_name'],
                        "ds_id": webitem['ds_id'],
                        "account_type": "",
                        "post_url": "",
                        "post_id": "",
                    }
                    if 'log_id' in webitem:
                        web[webitem['ds_name']]['log_id'] = webitem['log_id']
                return {
                    "success": "true",
                    "action": action,
                    "web": web
                }

                # else:
                    # logging.warning('url %s is not image content-type %s', imgurl, res.headers['Content-Type'])
            # else:
                # logging.warning('image url response error %s', res.status_code)


# ===========================================================================
# define & call all website list
# ===========================================================================

        weblists = datarequest['web']
        del (datarequest['web'])
        futures = []


        with concurrent.futures.ThreadPoolExecutor() as pool:
            for webitem in weblists:
                webitem['user'] = webitem['user'].rstrip('\u200b')
                webitem['pass'] = webitem['pass'].rstrip('\u200b')
                # correcting input
                check_ids = ['log_id', 'ds_id', 'post_id']
                for anid in check_ids:
                    if anid not in webitem:
                        webitem[anid] = ""
                if 'web_project_name' in webitem and webitem['web_project_name'] == "": 
                    del webitem['web_project_name']

                websitename = webitem['ds_name']
         
                if os.path.isfile('webmodule/' + websitename + '.py') == False:
                    response["web"][websitename] = {}
                    response["web"][websitename]["success"] = "false"
                    response["web"][websitename]["detail"] = "not found website class"
                    response["web"][websitename]["ds_id"] = webitem['ds_id']
                    response["web"][websitename]["usage_time"] = datetime.datetime.utcnow()
                    response["web"][websitename]["start_time"] = datetime.datetime.utcnow()
                    response["web"][websitename]["end_time"] = datetime.datetime.utcnow()
                    response["web"][websitename]["post_url"] = ''
                    response["web"][websitename]["post_id"] = ''
                    logging.error('NOT found websitename %s module', websitename)
                    continue

                if webitem['user'].strip() == "" or webitem['pass'].strip() == "":
                    response["web"][websitename] = {}
                    response["web"][websitename]["success"] = "false"
                    response["web"][websitename]["detail"] = "User/Pass missing"
                    response["web"][websitename]["ds_id"] = webitem['ds_id']
                    response["web"][websitename]["usage_time"] = datetime.datetime.utcnow()
                    response["web"][websitename]["start_time"] = datetime.datetime.utcnow()
                    response["web"][websitename]["end_time"] = datetime.datetime.utcnow()
                    response["web"][websitename]["post_url"] = ''
                    response["web"][websitename]["post_id"] = ''
                    logging.error('NOT found websitename %s module', websitename)
                    continue
                try:  # removed for debug
                    module = importlib.import_module('webmodule.' + websitename)
                    classname = getattr(module, websitename)
                    module_instance = classname()
                    actioncall = getattr(module_instance, action)
                    webdata = webitem
                    webdata.update(datarequest)
                    futures.append(pool.submit(actioncall, webdata))
                    #response["web"][websitename] = getattr(module_instance, action)(webdata)
                except Exception as e:  # removed for debug
                    response["web"][websitename] = {}
                    response["web"][websitename]["success"] = "false"
                    response["web"][websitename]["detail"] = str(e)
                    response["web"][websitename]["ds_id"] = webitem['ds_id']
                    response["web"][websitename]["usage_time"] = datetime.datetime.utcnow()
                    response["web"][websitename]["start_time"] = datetime.datetime.utcnow()
                    response["web"][websitename]["end_time"] = datetime.datetime.utcnow()
                    import_error = 'IMPORT ERROR %s',str(e)
                    logging.error(import_error)
                    if import_error:
                        try:
                            logging.info("==============================================================================")
                            logging.info("==============================================================================")

                            logging.warning("RESTART SERVER: IN PROGRESS") 
                            process_restart = subprocess.run(["pm2", "restart", "pm_config.json"])
                            logging.warning("RESTART SERVER: "+process_restart) 
                            logging.info("==============================================================================")
                            logging.info("==============================================================================")
                        except:
                            if output_server:
                                logging.error("RESTART SERVER : ERROR")
                                logging.warning("CODE: "+process_restart)
                                logging.info("==============================================================================")
                                logging.info("==============================================================================")
                    continue
            all_start_time = datetime.datetime.utcnow()

            errors = []
            for poolresult in concurrent.futures.as_completed(futures):
                try:
                    webresult = poolresult.result()
                    websitename = webresult["websitename"]
                    response["web"][websitename] = webresult
                    try:

                        if 'success' not in response["web"][websitename] or response["web"][websitename]['success'] == "False" or response["web"][websitename]['success'] is False:
                            response["web"][websitename]['success'] = "false"
                        elif response["web"][websitename]['success'] == "True" or response["web"][websitename]['success'] is True:
                            response["web"][websitename]['success'] = "true"

                        
                        if 'detail' not in response["web"][websitename]:
                            response["web"][websitename]['detail'] = ""

                        if 'ret' in response["web"][websitename]:
                            response["web"][websitename]['detail'] += str(response["web"][websitename]['ret'])
                        
                        if 'time_start' in response["web"][websitename]:
                            response["web"][websitename]['start_time'] = response["web"][websitename]['time_start']
                        if 'time_end' in response["web"][websitename]:
                            response["web"][websitename]['end_time'] = response["web"][websitename]['time_end']
                        
                        if 'account_type' not in response["web"][websitename]:
                            response["web"][websitename]['account_type'] = ""
                        
                        if 'post_url' not in response["web"][websitename] and (action == "create_post" or action == "search_post" or action == 'edit_post'):
                            response["web"][websitename]['post_url'] = ""

                        if action == "search_post":

                            if 'post_create_time' not in response["web"][websitename]:
                                response["web"][websitename]['post_create_time'] = ""
                            if 'post_modify_time' not in response["web"][websitename]:
                                response["web"][websitename]['post_modify_time'] = ""
                            if 'post_view' not in response["web"][websitename]:
                                response["web"][websitename]['post_view'] = ""
                            if 'post_found' not in response["web"][websitename]:
                                response["web"][websitename]['post_found'] = "true" if response["web"][websitename]['post_url'] != "" else "false"

                            if response["web"][websitename]['post_found'] == "False" or response["web"][websitename]['post_found'] is False:
                                response["web"][websitename]['post_found'] = "false"
                            elif response["web"][websitename]['post_found'] == "True" or response["web"][websitename]['post_found'] is True:
                                response["web"][websitename]['post_found'] = "true"


                        if 'ds_name' not in response["web"][websitename]:
                            response["web"][websitename]['ds_name'] = str(websitename)

                        if 'start_time' not in response["web"][websitename]:
                            response["web"][websitename]['start_time'] = all_start_time
                        if 'end_time' not in response["web"][websitename]:
                            response["web"][websitename]['end_time'] = datetime.datetime.utcnow()
                        
                        if 'post_url' in response["web"][websitename] and 'http' not in response["web"][websitename]['post_url'] and response["web"][websitename]['post_url'] != '':
                            response["web"][websitename]['post_url'] = "http://" + response["web"][websitename]['post_url']

                    except:
                        pass

                except Exception as e:
                    errors.append([str(traceback.format_exc()),str(e)])


            for webitem in weblists:

                if webitem['ds_name'] not in response:
                    for i, error in enumerate(errors):
                        print(webitem['ds_name'])
                        if webitem['ds_name'] + ".py" in error[0]:

                            logging.info("")
                            logging.info("")
                            logging.info("==============================================================================")
                            logging.info("=^=^=^=^=^=^=^=E-R-R-O-R=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^")
                            logging.info("==============================================================================")
                            logging.info("")
                            logging.info("WEBSITE NAME:")
                            logging.info(webitem['ds_name'])
                            logging.info("ERROR REPORTED:")
                            logging.error(error[0]) 
                            logging.info("")
                            logging.info("==============================================================================")
                            logging.info("==============================================================================")
                            logging.info("")
                            logging.info("")

                            if 'ConnectionError' in str(error[0]) or 'ReadTimeout' in str(error[0]):
                                error[0] = "Connection Error!"
                            if 'ProxyError' in str(error[0]):
                                error[0] = "Proxy Error!"    
                            if 'cloudflare' in str(error[0]).lower():                            
                                error[0] = "Website has security by Cloud Flare! Couldn't complete the action."    

                            response["web"][webitem['ds_name']] = {'success':'false','detail': error[1], 'websitename':webitem['ds_name'], 'ds_name':webitem['ds_name'], 'start_time':datetime.datetime.utcnow(), 'end_time':datetime.datetime.utcnow(), 'account_type': ''}
                            if action == "create_post" or action == "edit_post":
                                response["web"][webitem['ds_name']]['post_url'] = ""
                            if action == "search_post":
                                response["web"][webitem['ds_name']]['post_url'] = ""
                                response["web"][webitem['ds_name']]['post_create_time'] = ""
                                response["web"][webitem['ds_name']]['post_modify_time'] = ""
                                response["web"][webitem['ds_name']]['post_view'] = ""
                                response["web"][webitem['ds_name']]['post_found'] = "false"
    
                            break


                response["web"][webitem['ds_name']]['ds_id'] = webitem['ds_id']      
                response["web"][webitem['ds_name']]['log_id'] = webitem['log_id']    
                if 'post_id' not in response["web"][webitem['ds_name']]:  
                    response["web"][webitem['ds_name']]['post_id'] = webitem['post_id']




            logging.info("")
            logging.info("")
            logging.info("==============================================================================")
            logging.info("=^=^=^=^=^=^=S-T-A-R-T---O-U-T-P-U-T=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^")
            logging.info("==============================================================================")
            logging.info("")
            logging.error(response)
            logging.info("")
            logging.info("==============================================================================")
            logging.info("=^=^=^=^=^=^=^=E-N-D---O-U-T-P-U-T=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^")
            logging.info("==============================================================================")
            logging.info("")
            logging.info("")


        # remove image tmp
        if os.path.isdir('imgtmp/' + dirtmp) == True:
            shutil.rmtree(os.path.abspath('imgtmp/' + dirtmp))
            # logging.info('removed image temp imgtmp/%s', dirtmp)

    #    if action == 'register_user':
    #         re    sponse["action"] = action
    #         allweb = datarequest['web']
    #         for datareq in allweb:
    #             websitename = datareq['ds_name']
    #             # if file not exists websitename.py to next
    #             if os.path.isfile('webmodule/'+websitename+'.py') == False:
    #                 response["web"][websitename]["success"] = "false"
    #                 response["web"][websitename]["detail"] = "not found website class"
    #                 continue
    #             module = importlib.import_module('webmodule.'+websitename)
    #             classname = getattr(module, websitename)
    #             module_instance = classname()
    #             response["web"][websitename] = module_instance.register_user(
    #                 datareq)

    #     if action == 'boost_post':
    #         response["action"] = action
    #         allweb = datarequest['web']
    #         for datareq in allweb:
    #             websitename = datareq['ds_name']
    #             # if file not exists websitename.py to next
    #             if os.path.isfile('webmodule/'+websitename+'.py') == False:
    #                 response["web"][websitename]["success"] = "false"
    #                 response["web"][websitename]["detail"] = "not found website class"
    #                 continue
    #             module = importlib.import_module('webmodule.'+websitename)
    #             classname = getattr(module, websitename)
    #             module_instance = classname()
    #             response["web"][websitename] = module_instance.boost_post(
    #                 datareq)

    #     if action == 'create_post':
    #         response["action"] = action
    #         allweb = datarequest['web']
    #         for datareq in allweb:
    #             websitename = datareq['ds_name']
    #             # if file not exists websitename.py to next
    #             if os.path.isfile('webmodule/'+websitename+'.py') == False:
    #                 response["web"][websitename]["success"] = "false"
    #                 response["web"][websitename]["detail"] = "not found website class"
    #                 continue
    #             module = importlib.import_module('webmodule.'+websitename)
    #             classname = getattr(module, websitename)
    #             module_instance = classname()
    #             response["web"][websitename] = module_instance.create_post(
    #                 datareq, {})

    #     if action == 'delete_post':
    #         response["action"] = action
    #         allweb = datarequest['web']
    #         for datareq in allweb:
    #             websitename = datareq['ds_name']
    #             # if file not exists websitename.py to next
    #             if os.path.isfile('webmodule/'+websitename+'.py') == False:
    #                 response["web"][websitename]["success"] = "false"
    #                 response["web"][websitename]["detail"] = "not found website class"
    #                 continue
    #             module = importlib.import_module('webmodule.'+websitename)
    #             classname = getattr(module, websitename)
    #             module_instance = classname()
    #             response["web"][websitename] = module_instance.delete_post(
    #                 datareq)

    #     if action == 'edit_post':
    #         response["action"] = action
    #         allweb = datarequest['web']
    #         for datareq in allweb:
    #             websitename = datareq['ds_name']
    #             # if file not exists websitename.py to next
    #             if os.path.isfile('webmodule/'+websitename+'.py') == False:
    #                 response["web"][websitename]["success"] = "false"
    #                 response["web"][websitename]["detail"] = "not found website class"
    #                 continue
    #             module = importlib.import_module('webmodule.'+websitename)
    #             classname = getattr(module, websitename)
    #             module_instance = classname()
    #             response["web"][websitename] = module_instance.edit_post(
    #                 datareq, {})

    #     if action == 'test_login':
    #         response["action"] = action
    #         allweb = datarequest['web']
    #         for datareq in allweb:
    #             websitename = datareq['ds_name']
    #             # if file not exists websitename.py to next
    #             if os.path.isfile('webmodule/'+websitename+'.py') == False:
    #                 response["web"][websitename]["success"] = "false"
    #                 response["web"][websitename]["detail"] = "not found website class"
    #                 continue
    #             module = importlib.import_module('webmodule.'+websitename)
    #             classname = getattr(module, websitename)
    #             module_instance = classname()
    #             response["web"][websitename] = module_instance.test_login(
    #                 datareq)



        return response

    def coreworker_test(self, postdatajson):
        # json decode
        try:
            datarequest = json.loads(postdatajson, strict=False)
        except ValueError as e:
            return {
                "success": "false",
                "detail": "Wrong json format (" + str(e) + ")",
            }

        # check action in list
        action = datarequest['action']
        if (action not in self.list_action):
            return {
                "success": "false",
                "detail": "Action not allow",
            }

        # default response
        response = {
            "success": "true",
            "action": action,
            "web": {},
        }

        # ===========================================================================
        # store image in img tmp
        # ===========================================================================
        try:
            allimages = datarequest["post_img_url_lists"]
        except KeyError as e:
            allimages = {}
            # logging.warning(str(e))

        for i in range(6):
            dirtmp = 'imgupload_' + ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(16))
            uuni = dirtmp.split('_')[1]
            if os.path.isdir('imgtmp/' + dirtmp) == False:
                try:
                    os.mkdir("imgtmp/" + dirtmp)
                    logging.info('image directory imgtmp/%s is created', dirtmp)
                    time.sleep(0.2)
                except:
                    pass
                break
        # ===========================================================================
        # ===========================================================================

        datarequest['post_images'] = []
        imgcount = 1
        for imgurl in allimages:
            try:
                res = httprequestObj.http_get(imgurl, verify=False)
                # logging.info('get image from url %s', imgurl)
            except:
                # logging.warning('http connection error %s', imgurl)
                continue
            if res.status_code == 200:
                if int(res.headers['Content-Length']) > 0:
                    if res.headers['Content-Type'] == 'image/jpeg' or res.headers['Content-Type'] == 'image/png': # Please make the condition if there is no image, please send success false directly
                        try:
                            extension = res.headers['Content-Type'].split("/")[-1]
                            with open("imgtmp/" + dirtmp + "/" + str(imgcount) + "_" + uuni + "." + extension, 'wb') as f:
                                f.write(res.content)
                                f.close()
                            datarequest['post_images'].append("imgtmp/" + dirtmp + "/" + str(imgcount) + "_" + uuni + "." + extension)
                            imgcount = imgcount + 1
                        except:
                            pass
                    elif res.headers['Content-Type'] == 'application/octet-stream':
                        try:
                            extension = 'jpeg'
                            with open("imgtmp/" + dirtmp + "/" + str(imgcount) + "_" + uuni + "." + extension, 'wb') as f:
                                f.write(res.content)
                                f.close()
                            datarequest['post_images'].append("imgtmp/" + dirtmp + "/" + str(imgcount) + "_" + uuni + "." + extension)
                            imgcount = imgcount + 1
                        except:
                            pass
                    else:
                        logging.error('Issue with image urls')
                        weblists = datarequest['web']
                        web = {}
                        for webitem in weblists:
                            web[webitem['ds_name']] = {
                                "websitename": webitem['ds_name'],
                                "success": "false",
                                "detail": "ข้อมูลจากลิงค์รูปภาพของท่านมีประเภทที่ไม่สามารถดำเนินการในระบบได้ กรุณาตรวจสอบรูปภาพใหม่อีกครั้ง", #Your image url is not a proper content type.
                                "start_time": datetime.datetime.utcnow(),
                                "end_time": datetime.datetime.utcnow(),
                                "usage_time": datetime.datetime.utcnow(),
                                "ds_name": webitem['ds_name'],
                                "ds_id": webitem['ds_id'],
                                "account_type": "",
                                "post_url": "",
                                "post_id": "",
                            }
                            if 'log_id' in webitem:
                                web[webitem['ds_name']]['log_id'] = webitem['log_id']
                        return {
                            "success": "true",
                            "action": action,
                            "web": web
                        }
                else:
                    logging.error('Issue with image urls')
                    weblists = datarequest['web']
                    web = {}
                    for webitem in weblists:
                        web[webitem['ds_name']] = {
                            "websitename": webitem['ds_name'],
                            "success": "false",
                            "detail": "ลิงค์รูปภาพของท่านไม่มีข้อมูลรูปภาพ กรุณาตรวจสอบรูปภาพอีกครั้ง", #There is no image in your data. Please kindly recheck.
                            "start_time": datetime.datetime.utcnow(),
                            "end_time": datetime.datetime.utcnow(),
                            "usage_time": datetime.datetime.utcnow(),
                            "ds_name": webitem['ds_name'],
                            "ds_id": webitem['ds_id'],
                            "account_type": "",
                            "post_url": "",
                            "post_id": "",
                        }
                        if 'log_id' in webitem:
                            web[webitem['ds_name']]['log_id'] = webitem['log_id']
                    return {
                        "success": "true",
                        "action": action,
                        "web": web
                    }  
            else:
                logging.error('Issue with image urls')
                weblists = datarequest['web']
                web = {}
                for webitem in weblists:
                    web[webitem['ds_name']] = {
                        "websitename": webitem['ds_name'],
                        "success": "false",
                        "detail": "ไม่สามารถเชื่อมต่อลิงค์รูปภาพของท่านได้ กรุณาตรวจสอบรูปภาพใหม่อีกครั้ง", #Found 404 on your image link.
                        "start_time": datetime.datetime.utcnow(),
                        "end_time": datetime.datetime.utcnow(),
                        "usage_time": datetime.datetime.utcnow(),
                        "ds_name": webitem['ds_name'],
                        "ds_id": webitem['ds_id'],
                        "account_type": "",
                        "post_url": "",
                        "post_id": "",
                    }
                    if 'log_id' in webitem:
                        web[webitem['ds_name']]['log_id'] = webitem['log_id']
                return {
                    "success": "true",
                    "action": action,
                    "web": web
                }

                # else:
                    # logging.warning('url %s is not image content-type %s', imgurl, res.headers['Content-Type'])
            # else:
                # logging.warning('image url response error %s', res.status_code)

        weblists = datarequest['web']
        del (datarequest['web'])

        for webitem in weblists:
            websitename = webitem['ds_name']
            # if file not exists websitename.py to next
            if os.path.isfile('webmodule/' + websitename + '.py') == False:
                response["web"][websitename] = {}
                response["web"][websitename]["success"] = "false"
                response["web"][websitename]["detail"] = "not found website class"
                continue

            module = importlib.import_module('webmodule.' + websitename)
            classname = getattr(module, websitename)
            module_instance = classname()
            webdata = webitem
            webdata.update(datarequest)
            response["web"][websitename] = getattr(module_instance, action)(webdata)

        # remove image tmp
        if os.path.isdir('imgtmp/' + dirtmp) == True:
            shutil.rmtree(os.path.abspath('imgtmp/' + dirtmp))
            
        return response
