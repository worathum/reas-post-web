# -*- coding: utf-8 -*-

import shutil
import datetime
import importlib
import sys
import json
import base64
import os
import string
import random
from webmodule.lib_httprequest import *
httprequestObj = lib_httprequest()


class postcore():

    name = 'postcore'

    def __init__(self):
        try:
            import configs
        except ImportError:
            configs = {}
        self.secret_key = getattr(configs, 'secret_key', [])
        self.list_module = getattr(configs, 'list_module', [])
        self.list_action = getattr(configs, 'list_action', [])
        self.encoding = 'utf-8'

    def coreworker(self, access_token, postdata):

        # check secret key
        if self.secret_key != access_token:
            return {
                "success": "false",
                "detail": "Wrong access token",
            }

        # base64 decode postdata
        postdatajson = '{}'
        try:
            postdatajson = base64.b64decode(postdata)
        except ValueError as e:
            return {
                "success": "false",
                "detail": "Wrong data request (" + str(e) + ")",
            }

        # json decode
        try:
            datarequest = json.loads(postdatajson.decode('utf-8'))
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

        # store image in img tmp
        try:
            allimages = datarequest["post_img_url_lists"]
        except KeyError:
            allimages = {}
        datarequest['post_images'] = []
        dirtmp = str(os.getpid())+'_'+str(datetime.datetime.utcnow().strftime("%Y%m%d%H:%M:%S"))
        os.mkdir("imgtmp/"+dirtmp)
        imgcount = 1
        for imgurl in allimages:
            res = httprequestObj.http_get(imgurl, verify=False)
            if res.status_code == 200:
                if res.headers['Content-Type'] == 'image/jpeg' or res.headers['Content-Type'] == 'image/png':
                    extension = res.headers['Content-Type'].split("/")[-1]
                    with open("imgtmp/"+dirtmp+"/"+str(imgcount)+"."+extension, 'wb') as f:
                        f.write(res.content)
                    datarequest['post_images'].append("imgtmp/"+dirtmp+"/"+str(imgcount)+"."+extension)
                    imgcount = imgcount+1

        # define all website list
        weblists = datarequest['web']
        del(datarequest['web'])

        for webitem in weblists:
            websitename = webitem['ds_name']
            # if not defind in configs['list_module']
            if websitename not in self.list_module:
                response["web"][websitename] = {}
                response["web"][websitename]["success"] = "false"
                response["web"][websitename]["detail"] = "not found website class"
                continue
            # if file not exists websitename.py to next
            if os.path.isfile('webmodule/'+websitename+'.py') == False:
                response["web"][websitename] = {}
                response["web"][websitename]["success"] = "false"
                response["web"][websitename]["detail"] = "not found website class"
                continue
            try:  # removed for debug
                module = importlib.import_module('webmodule.'+websitename)
                classname = getattr(module, websitename)
                module_instance = classname()
                webdata = webitem
                webdata.update(datarequest)
                response["web"][websitename] = getattr(module_instance, action)(webdata)
            except BaseException:  # removed for debug
                response["web"][websitename] = {}
                response["web"][websitename]["success"] = "false"
                response["web"][websitename]["detail"] = "test commit Import errors: "
                continue

            # remove image tmp
        if os.path.isdir('imgtmp/'+dirtmp) == True:
            shutil.rmtree(os.path.abspath('imgtmp/'+dirtmp))

        # if action == 'register_user':
        #     response["action"]=action
        #     allweb=datarequest['web']
        #     for datareq in allweb:
        #         websitename=datareq['ds_name']
        #         # if file not exists websitename.py to next
        #         if os.path.isfile('webmodule/'+websitename+'.py') == False:
        #             response["web"][websitename]["success"]="false"
        #             response["web"][websitename]["detail"]="not found website class"
        #             continue
        #         module=importlib.import_module('webmodule.'+websitename)
        #         classname=getattr(module, websitename)
        #         module_instance=classname()
        #         response["web"][websitename]=module_instance.register_user(
        #             datareq)

        # if action == 'boost_post':
        #     response["action"]=action
        #     allweb=datarequest['web']
        #     for datareq in allweb:
        #         websitename=datareq['ds_name']
        #         # if file not exists websitename.py to next
        #         if os.path.isfile('webmodule/'+websitename+'.py') == False:
        #             response["web"][websitename]["success"]="false"
        #             response["web"][websitename]["detail"]="not found website class"
        #             continue
        #         module=importlib.import_module('webmodule.'+websitename)
        #         classname=getattr(module, websitename)
        #         module_instance=classname()
        #         response["web"][websitename]=module_instance.boost_post(
        #             datareq)

        # if action == 'create_post':
        #     response["action"]=action
        #     allweb=datarequest['web']
        #     for datareq in allweb:
        #         websitename=datareq['ds_name']
        #         # if file not exists websitename.py to next
        #         if os.path.isfile('webmodule/'+websitename+'.py') == False:
        #             response["web"][websitename]["success"]="false"
        #             response["web"][websitename]["detail"]="not found website class"
        #             continue
        #         module=importlib.import_module('webmodule.'+websitename)
        #         classname=getattr(module, websitename)
        #         module_instance=classname()
        #         response["web"][websitename]=module_instance.create_post(
        #             datareq, {})

        # if action == 'delete_post':
        #     response["action"]=action
        #     allweb=datarequest['web']
        #     for datareq in allweb:
        #         websitename=datareq['ds_name']
        #         # if file not exists websitename.py to next
        #         if os.path.isfile('webmodule/'+websitename+'.py') == False:
        #             response["web"][websitename]["success"]="false"
        #             response["web"][websitename]["detail"]="not found website class"
        #             continue
        #         module=importlib.import_module('webmodule.'+websitename)
        #         classname=getattr(module, websitename)
        #         module_instance=classname()
        #         response["web"][websitename]=module_instance.delete_post(
        #             datareq)

        # if action == 'edit_post':
        #     response["action"]=action
        #     allweb=datarequest['web']
        #     for datareq in allweb:
        #         websitename=datareq['ds_name']
        #         # if file not exists websitename.py to next
        #         if os.path.isfile('webmodule/'+websitename+'.py') == False:
        #             response["web"][websitename]["success"]="false"
        #             response["web"][websitename]["detail"]="not found website class"
        #             continue
        #         module=importlib.import_module('webmodule.'+websitename)
        #         classname=getattr(module, websitename)
        #         module_instance=classname()
        #         response["web"][websitename]=module_instance.edit_post(
        #             datareq, {})

        # if action == 'test_login':
        #     response["action"]=action
        #     allweb=datarequest['web']
        #     for datareq in allweb:
        #         websitename=datareq['ds_name']
        #         # if file not exists websitename.py to next
        #         if os.path.isfile('webmodule/'+websitename+'.py') == False:
        #             response["web"][websitename]["success"]="false"
        #             response["web"][websitename]["detail"]="not found website class"
        #             continue
        #         module=importlib.import_module('webmodule.'+websitename)
        #         classname=getattr(module, websitename)
        #         module_instance=classname()
        #         response["web"][websitename]=module_instance.test_login(
        #             datareq)

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
