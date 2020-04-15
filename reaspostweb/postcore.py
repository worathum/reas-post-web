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

try:
    import configs
except ImportError:
    configs = {}
if os.path.isdir('log') == False:
    os.mkdir('log')
logging.config.dictConfig(getattr(configs, 'logging_config', {}))
log = logging.getLogger()

class postcore():


    name = 'postcore'

    def __init__(self):
        self.secret_key = getattr(configs, 'secret_key', [])
        self.list_module = getattr(configs, 'list_module', [])
        self.list_action = getattr(configs, 'list_action', [])
        self.encoding = 'utf-8'
        log.debug('load app config success.')


    def coreworker(self, access_token, postdata):

        # check secret key
        if self.secret_key != access_token:
            log.error('wrong access token.')
            return {
                "success": "false",
                "detail": "Wrong access token",
            }

        # base64 decode postdata
        postdatajson = '{}'
        try:
            postdatajson = base64.b64decode(postdata)
        except ValueError as e:
            log.error('base64 decode error.'+str(e))
            return {
                "success": "false",
                "detail": "Wrong data request (" + str(e) + ")",
            }

        # json decode
        try:
            datarequest = json.loads(postdatajson.decode('utf-8'))
        except ValueError as e:
            log.error('json decode error.'+str(e))
            return {
                "success": "false",
                "detail": "Wrong json format (" + str(e) + ")",
            }

        # check action in list
        action = datarequest['action']
        if(action not in self.list_action):
            log.error('action %s not allow',datarequest['action'])
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

        # store image in img tmp
        try:
            allimages = datarequest["post_img_url_lists"]
        except KeyError:
            allimages = {}
        #dirtmp = str(os.getpid())+'_'+str(datetime.datetime.utcnow().strftime("%Y%m%d%H:%M:%S"))
        for i in range(6):
            dirtmp = 'imgupload_'+''.join(random.SystemRandom().choice(string.ascii_lowercase + string.ascii_uppercase  + string.digits) for _ in range(16))
            if os.path.isdir('imgtmp/'+dirtmp) == False:
                os.mkdir("imgtmp/"+dirtmp)
                log.debug('image directory imgtmp/%s is created',dirtmp)
                break
        
        datarequest['post_images'] = []
        imgcount = 1
        for imgurl in allimages:
            try:
                res = httprequestObj.http_get(imgurl, verify=False)
            except:
                log.warning('http connection error %s',imgurl)
                continue
            if res.status_code == 200:
                if res.headers['Content-Type'] == 'image/jpeg' or res.headers['Content-Type'] == 'image/png':
                    extension = res.headers['Content-Type'].split("/")[-1]
                    with open("imgtmp/"+dirtmp+"/"+str(imgcount)+"."+extension, 'wb') as f:
                        f.write(res.content)
                    datarequest['post_images'].append("imgtmp/"+dirtmp+"/"+str(imgcount)+"."+extension)
                    imgcount = imgcount+1
                else:
                    log.warning('url %s is not image content-type %s',imgurl,res.headers['Content-Type'])
            else:
                log.warning('image url response error %s',res.status_code)
        
        # define all website list
        weblists = datarequest['web']
        del(datarequest['web'])
        futures = []
        with concurrent.futures.ProcessPoolExecutor() as pool:
            for webitem in weblists:
                websitename = webitem['ds_name']
                # # if not defind in configs['list_module']
                # if websitename not in self.list_module:
                #     response["web"][websitename] = {}
                #     response["web"][websitename]["success"] = "false"
                #     response["web"][websitename]["detail"] = "not found website class"
                #     response["web"][websitename]["ds_id"] = webitem['ds_id']
                #     response["web"][websitename]["usage_time"] = datetime.datetime.utcnow()
                #     response["web"][websitename]["start_time"] = datetime.datetime.utcnow()
                #     response["web"][websitename]["end_time"] = datetime.datetime.utcnow()
                #     response["web"][websitename]["post_url"] = ''
                #     response["web"][websitename]["post_id"] = ''
                #     log.error('websitename %s is not in allow list module',websitename)
                #     continue
                # if file not exists websitename.py to next
                if os.path.isfile('webmodule/'+websitename+'.py') == False:
                    response["web"][websitename] = {}
                    response["web"][websitename]["success"] = "false"
                    response["web"][websitename]["detail"] = "not found website class"
                    response["web"][websitename]["ds_id"] = webitem['ds_id']
                    response["web"][websitename]["usage_time"] = datetime.datetime.utcnow()
                    response["web"][websitename]["start_time"] = datetime.datetime.utcnow()
                    response["web"][websitename]["end_time"] = datetime.datetime.utcnow()
                    response["web"][websitename]["post_url"] = ''
                    response["web"][websitename]["post_id"] = ''
                    log.error('not found websitename %s module',websitename)
                    continue
                try:  # removed for debug
                    module = importlib.import_module('webmodule.'+websitename)
                    classname = getattr(module, websitename)
                    module_instance = classname()
                    actioncall = getattr(module_instance, action)
                    webdata = webitem
                    webdata.update(datarequest)
                    futures.append(pool.submit(actioncall, webdata))
                    response["web"][websitename] = getattr(module_instance, action)(webdata)
                except Exception as e:  # removed for debug
                    response["web"][websitename] = {}
                    response["web"][websitename]["success"] = "false"
                    response["web"][websitename]["detail"] = str(e)
                    response["web"][websitename]["ds_id"] = webitem['ds_id']
                    response["web"][websitename]["usage_time"] = datetime.datetime.utcnow()
                    response["web"][websitename]["start_time"] = datetime.datetime.utcnow()
                    response["web"][websitename]["end_time"] = datetime.datetime.utcnow()
                    log.error('import error %s',e)
                    continue
            for poolresult in concurrent.futures.as_completed(futures):
                webresult = poolresult.result()
                websitename = webresult["websitename"]
                response["web"][websitename] = webresult

        # remove image tmp
        if os.path.isdir('imgtmp/'+dirtmp) == True:
            shutil.rmtree(os.path.abspath('imgtmp/'+dirtmp))
            log.debug('removed image temp imgtmp/%s',dirtmp)

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
        if(action not in self.list_action):
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
        del(datarequest['web'])

        for webitem in weblists:
            websitename = webitem['ds_name']
            # if file not exists websitename.py to next
            if os.path.isfile('webmodule/'+websitename+'.py') == False:
                response["web"][websitename] = {}
                response["web"][websitename]["success"] = "false"
                response["web"][websitename]["detail"] = "not found website class"
                continue

            module = importlib.import_module('webmodule.'+websitename)
            classname = getattr(module, websitename)
            module_instance = classname()
            webdata = webitem
            webdata.update(datarequest)
            response["web"][websitename] = getattr(module_instance, action)(webdata)

        return response
