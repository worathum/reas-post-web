# -*- coding: utf-8 -*-

import importlib
import sys
import json
import configs

def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

jsonstring = '''
{
    "action": "create_post",
    "timeout": "5",
    "post_img_url_lists": [
        "http://imagestore.com/pic1.jpg",
        "http://imagestore.com/pic2.jpg"
    ],
    "geo_latitude": "13.786862",
    "geo_longitude": "100.757815",    
    "property_id" : "",
    "post_title_th": "xxx",
    "short_post_title_th": "xxx",
    "post_description_th": "xxx",
    "post_title_en": "",
    "short_post_title_en": "xxx",
    "post_description_en": "",
    "price_baht": "3000",
    
    "listing_type": "ขาย",    
    "property_type": "คอนโด",    
    "floor_level  " : "11",
    "floor_total  " : "11",
    "floor_area  " : "11",
    "bath_room  " : "11",
    "bed_room  " : "11",
    "prominent_point  " : "จุดเด่น",    
    "view_type " : "11",
    "direction_type" : "11",
    "addr_province": "จังหวัด",
    "addr_district": "เขต",
    "addr_sub_district": "ตำบล แขวง",
    "addr_road": "ถนน",
    "addr_soi": "ซอย",
    "addr_near_by": "สถานที่ใกล้เคียง",
    "floorarea_sqm": "พื้นที่",
    
    "land_size_rai": "ขนาดที่ดินเป็นไร่",
    "land_size_ngan": "ขนาดที่ดินเป็นงาน",
    "land_size_wa": "ขนาดที่ดินเป็นวา",
    
    "name": "xxx",
    "mobile": "xxx",
    "email": "xxx",
    "line": "xxx",
    "web": [
        {
            "ds_name": "thaihometown",
            "ds_id": "4",              
            "user": "amarin.ta@gmail.com",
            "pass": "5k4kk3253434"
        },
        {
            "ds_name": "ddproperty",
            "ds_id": "5",     
            "user": "amarin.ta@gmail.com",
            "pass": "5k4kk3253434"         
        }
    ]
}
'''

response = {
    "success": "true",
    "action": "create_post",
    "start_time": "0:00:00.771743",
    "end_time": "0:00:00.771743",
    "web": {
        "thaihometown": {
            "success": "true",            
            "start_time": "0:00:00.771743",
            "end_time": "0:00:00.771743",
            "ds_id": "4",
            "post_url": "http://xxxxx/post/232323",
            "post_id": "33333",
            "account_type" : "",
        },
        "ddproperty": {
            "success": "false",
            "start_time": "0:00:00.771743",
            "end_time": "0:00:00.771743",
            "ds_id": "5",
            "post_url": "",
            "post_id": "",
            "account_type" : "normal",            
            "detail": ""
        }
    }
}


datarequest = json.loads(jsonstring)
action = datarequest['action']
listmodule = getattr(configs, 'web_module', [])
datarequest = json.loads(jsonstring)
weblistdata = datarequest['web']
del(datarequest['web']) 

for webitems in weblistdata:
    websitename = webitems['ds_name']    
    if websitename not in listmodule:
        continue    
    module = importlib.import_module('webmodule.'+websitename)
    classname = getattr(module, websitename)
    module_instance = classname()
    webdatas = webitems
    webdatas.update(datarequest)
    response["web"][websitename] = getattr(module_instance, action)(webdatas)
    
print(response)



