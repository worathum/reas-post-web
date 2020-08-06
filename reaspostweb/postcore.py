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
except ImportError:
    configs = {}
if os.path.isdir('log') == False:
    os.mkdir('log')
logging.basicConfig(level=logging.DEBUG, filename='log/app.log', filemode='a', format='%(process)d-%(asctime)s-%(levelname)s-%(message)s', datefmt='%d-%b-%y %H:%M:%S')
# logging.config.dictConfig(getattr(configs, 'logging_config', {}))
# log = logging.getLogger()


class postcore():

    name = 'postcore'

    def __init__(self):
        self.secret_key = getattr(configs, 'secret_key', [])
        self.list_module = getattr(configs, 'list_module', [])
        self.list_action = getattr(configs, 'list_action', [])
        self.encoding = 'utf-8'
        logging.debug('load app config success.')

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
        

        # replace string \n to \r\n , \t to ''
        # TODO how to replace all dict by foreach or array walk?
        try:
            datarequest['post_title_th'] = datarequest['post_title_th'].strip()
            datarequest['post_title_th'] = re.sub(r'\n','\r\n',datarequest['post_title_th'])
            datarequest['post_title_en'] = re.sub(r'\n','\r\n',datarequest['post_title_en'])
            datarequest['short_post_title_th'] = re.sub(r'\n','\r\n',datarequest['short_post_title_th'])
            datarequest['short_post_title_en'] = re.sub(r'\n','\r\n',datarequest['short_post_title_en'])
            datarequest['post_description_th'] = re.sub(r'\n','\r\n',datarequest['post_description_th'])
            datarequest['post_description_en'] = re.sub(r'\n','\r\n',datarequest['post_description_en'])
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
            datarequest['project_name'] = None
 
        check_int = ['land_size_rai', 'land_size_ngan', 'land_size_wa', 'floor_area']
        for item in check_int:
            try:
                a = int(datarequest[item])
            except:
                datarequest[item] = '0'
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
            logging.warning(str(e))

        for i in range(6):
            dirtmp = 'imgupload_' + ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(16))
            if os.path.isdir('imgtmp/' + dirtmp) == False:
                try:
                    os.mkdir("imgtmp/" + dirtmp)
                    logging.debug('image directory imgtmp/%s is created', dirtmp)
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
                logging.debug('get image from url %s', imgurl)
            except:
                logging.warning('http connection error %s', imgurl)
                continue
            if res.status_code == 200:
                if res.headers['Content-Type'] == 'image/jpeg' or res.headers['Content-Type'] == 'image/png':
                    try:
                        extension = res.headers['Content-Type'].split("/")[-1]
                        with open("imgtmp/" + dirtmp + "/" + str(imgcount) + "." + extension, 'wb') as f:
                            f.write(res.content)
                            f.close()
                        datarequest['post_images'].append("imgtmp/" + dirtmp + "/" + str(imgcount) + "." + extension)
                        imgcount = imgcount + 1
                    except:
                        pass
                else:
                    logging.warning('url %s is not image content-type %s', imgurl, res.headers['Content-Type'])
            else:
                logging.warning('image url response error %s', res.status_code)



# ===========================================================================
# define & call all website list
# ===========================================================================

        weblists = datarequest['web']
        del (datarequest['web'])
        futures = []


        with concurrent.futures.ThreadPoolExecutor() as pool:
            for webitem in weblists:

                # correcting input
                check_ids = ['log_id', 'ds_id', 'post_id']
                for anid in check_ids:
                    if anid not in webitem:
                        webitem[anid] = ""
                if 'web_project_name' in webitem and webitem['web_project_name'] == "": 
                    webitem['web_project_name'] = None

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
                    logging.error('not found websitename %s module', websitename)
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
                    logging.error('import error %s',str(e))
                    continue

            errors = []
            for poolresult in concurrent.futures.as_completed(futures):
                try:
                    webresult = poolresult.result()
                    websitename = webresult["websitename"]
                    response["web"][websitename] = webresult
                    try:
                        if response["web"][websitename]['success'] == "True" or response["web"][websitename]['success'] is True:
                            response["web"][websitename]['success'] = "true"
                        if response["web"][websitename]['success'] == "False" or response["web"][websitename]['success'] is False:
                            response["web"][websitename]['success'] = "false"
                        
                        if 'detail' not in response["web"][websitename]:
                            response["web"][websitename]['detail'] = ""
                        if 'ret' in response["web"][websitename]:
                            response["web"][websitename]['detail'] += str(ret)
                        if 'time_start' in response["web"][websitename]:
                            response["web"][websitename]['start_time'] = response["web"][websitename]['time_start']
                        if 'time_end' in response["web"][websitename]:
                            response["web"][websitename]['end_time'] = response["web"][websitename]['time_end']
                        if 'account_type' not in response["web"][websitename]:
                            response["web"][websitename]['account_type'] = ""
                        if 'post_url' not in response["web"][websitename] and (action == "create_post" or action == "search_post"):
                            response["web"][websitename]['post_url'] = ""
                        if 'post_create_time' not in response["web"][websitename] and action == "search_post":
                            response["web"][websitename]['post_create_time'] = ""
                        if 'post_modify_time' not in response["web"][websitename] and action == "search_post":
                            response["web"][websitename]['post_modify_time'] = ""
                        if 'post_view' not in response["web"][websitename] and action == "search_post":
                            response["web"][websitename]['post_view'] = ""
                        if 'post_found' not in response["web"][websitename] and action == "search_post":
                            response["web"][websitename]['post_found'] = "true" if response["web"][websitename]['post_url'] != "" else "false"
                        if 'ds_name' not in response["web"][websitename]:
                            response["web"][websitename]['ds_name'] = str(websitename)

                    except:
                        pass


                except Exception as e:
                    errors.append([str(traceback.format_exc()),str(e)])


            for webitem in weblists:

                if webitem['ds_name'] not in response:
                    for i, error in enumerate(errors):
                        if webitem['ds_name'] in error[0]:
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

                            response["web"][webitem['ds_name']] = {'success':'false','detail': error[0], 'websitename':webitem['ds_name'], 'start_time':datetime.datetime.utcnow(), 'end_time':datetime.datetime.utcnow()}
                            break


                response["web"][webitem['ds_name']]['ds_id'] = webitem['ds_id']      
                response["web"][webitem['ds_name']]['log_id'] = webitem['log_id']    
                if 'post_id' not in response["web"][webitem['ds_name']]:  
                    response["web"][webitem['ds_name']]['post_id'] = webitem['post_id']      
                if 'post_url' not in response["web"][webitem['ds_name']] and action == 'create_post':  
                    response["web"][webitem['ds_name']]['post_url'] = ''      

                logging.info("")
                logging.info("")
                logging.info("==============================================================================")
                logging.info("=^=^=^=^=^=^=S-T-A-R-T---O-U-T-P-U-T=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^")
                logging.info("==============================================================================")
                logging.info("")
                logging.error(json.dumps(json.loads(response), indent=4, sort_keys=True)) 
                logging.info("")
                logging.info("==============================================================================")
                logging.info("=^=^=^=^=^=^=^=E-N-D---O-U-T-P-U-T=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^")
                logging.info("==============================================================================")
                logging.info("")
                logging.info("")


        # remove image tmp
        if os.path.isdir('imgtmp/' + dirtmp) == True:
            shutil.rmtree(os.path.abspath('imgtmp/' + dirtmp))
            logging.debug('removed image temp imgtmp/%s', dirtmp)

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
            datarequest = json.loads(postdatajson)
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

        return response
