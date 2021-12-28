# -*- coding: utf-8 -*-

import facebook as fb
from .lib_httprequest import *
import datetime
import sys
import requests

class facebook_page():
    name = 'aecmarketing'

    def __init__(self):

        try:
            import configs

        except ImportError:
            configs = {}

        self.debug = 0
        self.httprequestObj = lib_httprequest()
        self.webname = 'facebook_page'
        self.access_token = 'EAAPUQnySNZA4BALQ4k8mes2Jwpr5ShZBPuSoAgzIDUsJOwZCoYZAgTFv46cljRuwNjEGNDKkNvN0lebEF9fv4jNf6ZBUqpsHNXYcL8Eom42kyRFL8jkmwYaBVQFdBMXteob3wZAtbNLiX2uHlfanauzzDtxzOIJDDodYd8AZCHiEf1C9jBaFEPj4j6ra5ANODMZD'
        self.page_id ='109985104886077'
        self.graphapi = fb.GraphAPI(self.access_token)

    def test_login(self, postdata):
        time_start = datetime.datetime.utcnow()

        success = True
        detail = ''

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": self.webname,
            "ds_id": postdata['ds_id'],
        }

    def create_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        success = False
        detail = 'Something wrong'
        post_url = ''
        post_id = ''

        message_post = 'รหัสทรัพย์ : {}\n\n{}\n\n{}'.format(postdata['property_id'],postdata['post_description_th'],postdata['post_description_en'])
        
        imgs_id = []
        for img in postdata['post_images']:
            photo = open(img, "rb")
            imgs_id.append(self.graphapi.put_photo(photo, album_id='me/photos',published=False)['id'])
            photo.close()

        args={}
        args["message"]= message_post
        for img_id in imgs_id:
            key="attached_media["+str(imgs_id.index(img_id))+"]"
            args[key]="{'media_fbid': '"+img_id+"'}"
        
        post = self.graphapi.request(path='/me/feed', args=None, post_args=args, method='POST')

        try:
            post_id = post['id'].split('_')[1]
            post_url = 'https://www.facebook.com/permalink.php?story_fbid={}&id={}'.format(post_id,self.page_id)
            success = True
            detail = 'Post successful'
        except:
            pass

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "post_url": post_url,
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
            "account_type": "null",
            "detail": detail,
            "websitename": self.webname,
        }

    def edit_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        success = False
        detail = 'Something wrong'
        post_id = ''
        post_url = ''
        delete = self.delete_post(postdata)
        success = delete['success']
        if success or (not success and delete['detail'] == 'Post id not found'):
            success = False
            post = self.create_post(postdata)
            success = post['success']
            if success:
                post_id = post['post_id']
                post_url = post['post_url']
                detail = 'Edit successful'

        """try:
            post = self.graphapi.request(path='/{}_{}'.format(self.page_id,postdata['post_id]), args=None, post_args=args, method='POST')
        except:
            pass"""

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start

        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "ds_id": postdata['ds_id'],
            "post_id": post_id,
            "post_url": post_url,
            "account_type": "null",
            "detail": detail,
            "websitename": self.webname,
        }
    
    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        success = False
        detail = 'Something wrong'
        try:
            delete = self.graphapi.delete_object('{}_{}'.format(self.page_id,postdata['post_id']))
            success = delete['success']
            if success:
                detail = 'Delete successful'
        except:
            detail = 'Post id not found'
        

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": self.webname,
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": postdata['post_id']
        }

    def boost_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        success = False
        detail = 'No option boost in this website'

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            'ds_id': postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": postdata['post_id'],
            "websitename": self.webname,
            "post_view": ""
        }


    def search_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        time_start = datetime.datetime.utcnow()

        success = False
        post_found = False
        detail = 'Something wrong'
        post_id = ''
        post_url = ''
        
        query_string = 'posts?limit={0}'.format(6)
        posts = self.graphapi.get_all_connections(self.page_id, query_string)
        for i in posts:
            if postdata['post_title_th'] in i['message']:
                post_id = i['id'].split('_')[1]
                post_url = 'https://www.facebook.com/permalink.php?story_fbid={}&id={}'.format(post_id,self.page_id)
                post_found = True
                detail = 'Post found'
                break
        if not post_found:
            detail = 'Not found this post'

        time_end = datetime.datetime.utcnow()
        time_usage = time_end - time_start
        return {
            "success": success,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "detail": detail,
            "websitename": self.webname,
            "account_type":None,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": post_id,
            "post_modify_time": '',
            "post_view": '',
            "post_url": post_url,
            "post_found": post_found
        }

    def print_debug(self, msg):
        if(self.debug == 1):
            print(msg)
        return True