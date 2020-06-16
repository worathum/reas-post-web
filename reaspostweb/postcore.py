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
            log.error('base64 decode error.' + str(e))
            return {
                "success": "false",
                "detail": "Wrong data request (" + str(e) + ")",
            }

        # json decode to array
        try:
            datarequest = json.loads(postdatajson.decode('utf-8'))
        except ValueError as e:
            log.error('json decode error.' + str(e))
            return {
                "success": "false",
                "detail": "Wrong json format (" + str(e) + ")",
            }
        

        # replace string \n to \r\n , \t to ''
        # TODO how to replace all dict by foreach or array walk?
        try:
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

        
        # check action in list
        action = datarequest['action']
        if (action not in self.list_action):
            log.error('action %s not allow', datarequest['action'])
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
        except KeyError as e:
            allimages = {}
            log.warning(str(e))
        #dirtmp = str(os.getpid())+'_'+str(datetime.datetime.utcnow().strftime("%Y%m%d%H:%M:%S"))
        for i in range(6):
            dirtmp = 'imgupload_' + ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(16))
            if os.path.isdir('imgtmp/' + dirtmp) == False:
                try:
                    os.mkdir("imgtmp/" + dirtmp)
                    log.debug('image directory imgtmp/%s is created', dirtmp)
                    time.sleep(0.2)
                except:
                    pass
                break

        datarequest['post_images'] = []
        imgcount = 1
        for imgurl in allimages:
            try:
                res = httprequestObj.http_get(imgurl, verify=False)
                log.debug('get image from url %s', imgurl)
            except:
                log.warning('http connection error %s', imgurl)
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
                    log.warning('url %s is not image content-type %s', imgurl, res.headers['Content-Type'])
            else:
                log.warning('image url response error %s', res.status_code)

        # define all website list
        weblists = datarequest['web']
        del (datarequest['web'])
        futures = []

        #with concurrent.futures.ProcessPoolExecutor() as pool:
        #with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        with concurrent.futures.ThreadPoolExecutor() as pool:
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
                    log.error('not found websitename %s module', websitename)
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
                    log.error('import error %s',str(e))
                    continue

            errors = []
            for poolresult in concurrent.futures.as_completed(futures):
                try:
                    webresult = poolresult.result()
                    websitename = webresult["websitename"]
                    response["web"][websitename] = webresult
                except Exception as e:
                    errors.append([str(traceback.format_exc()),str(e)])

            for webitem in weblists:
                if webitem['ds_name'] not in response:
                    for i, error in enumerate(errors):
                        if webitem['ds_name'] in error[0]:
                            response["web"][webitem['ds_name']] = {'success':'false','detail': error[1], 'websitename':webitem['ds_name'], 'start_time':datetime.datetime.utcnow(), 'end_time':datetime.datetime.utcnow()}
                            if 'ds_id' in webitem:
                                response["web"][webitem['ds_name']]['ds_id'] = webitem['ds_id']
                            if 'log_id' in webitem:
                                response["web"][webitem['ds_name']]['log_id'] = webitem['ds_id']                        
                            del errors[i]
                            break


        # remove image tmp
        if os.path.isdir('imgtmp/' + dirtmp) == True:
            shutil.rmtree(os.path.abspath('imgtmp/' + dirtmp))
            log.debug('removed image temp imgtmp/%s', dirtmp)

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
