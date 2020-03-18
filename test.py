# -*- coding: utf-8 -*-

import importlib
import sys
import json
import configs
from sample import sample
from reaspostweb.postcore import postcore

params = {}
#common
params["web_name"] = 'dotproperty'
params["login_user"] = 'amarin_ta@hotmail.com'  # amarin_ta@hotmail.com amarin.ta@gmail.com
params["login_pass"] = '5k4kk3253434'
params["email"] = 'amarin.ta@gmail.com'
params["tel"] = '891999450'

#post_info
params["post_title_th"] =  "xxx"
params["short_post_title_th"] =  "xxx"
params["post_description_th"] =  "xxx"
params["post_title_en"] =  ""
params["short_post_title_en"] =  "xxx"
params["post_description_en"] =  ""
params["price_baht"] =  "3000"

#edit boost delet post
params["post_id"] = "5"

get_action_json_function = 'get_test_login_json_string' # get_register_json_string 

sampleObj = sample(params)
post_data = getattr(sampleObj, get_action_json_function)()

postcore = postcore()
response = postcore.coreworker_test(post_data)

print(response)