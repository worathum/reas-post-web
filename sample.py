# -*- coding: utf-8 -*-

class sample():

    name = 'sample'

    def __init__(self, params):        
        self.web_name = params["web_name"]
        self.login_user = params["login_user"]
        self.login_pass = params["login_pass"]      
        self.email = params["email"] 

    def get_test_login_json_string(self):
        json_string = '''
{
    "action": "test_login",
    "timeout": "7",
    "web": [
        {
            "ds_name": "''' + self.web_name + '''",
            "ds_id": "4",
            "user": "''' + self.login_user + '''",
            "pass": "''' + self.login_pass + '''"                        
        }
    ]
}
'''
        return json_string

    def get_register_json_string(self):
        json_string = '''
{
    "action": "register_user",
    "timeout": "7",
    "web": [
        {
            "ds_name": "''' + self.web_name + '''",
            "ds_id": "4",
            "user": "''' + self.login_user + '''",
            "pass": "''' + self.login_pass + '''",
            "email": "''' + self.email + '''",
            "company_name": "amarin inc",
            "name_title": "mr",
            "name_th": "อัมรินทร์",
            "surname_th": "บุญเกิด",
            "name_en": "Amarinxyz",
            "surname_en": "Boonkirt",
            "tel": "0891999450",
            "line": "amarin.ta",
            "addr_province" : "nonthaburi"            
        }
    ]
}
'''
        return json_string
        
    def get_create_post_json_string(self):
        json_string = '''
{
    "action": "create_post",
    "timeout": "5",
    "post_img_url_lists": [
        "https://www.img.in.th/images/2ddca76d033d31c21b33008d526e99bb.jpg",
        "https://www.img.in.th/images/a2eadbaab37379317a4d5bc5b14a9d06.jpg",
        "https://www.img.in.th/images/eebbe912a6e023b76e419ffdb77985e8.jpg"
    ],
    "post_images" : "imgtmp/img_upload/photo_1.jpg",
    "geo_latitude": "13.786862",
    "geo_longitude": "100.757815",    
    "property_id" : "A01",
    "post_title_th": "ขายบ้านเดี่ยว 2 ชั้น",
    "short_post_title_th": "test",
    "post_description_th": "test",
    "post_title_en": "testtest",
    "short_post_title_en": "testtest",
    "post_description_en": "testtest",
    "price_baht": "30000000",
    
    "listing_type": "ขาย",    
    "property_type": "house",    
    "floor_level" : "11",
    "floor_total" : "11",
    "floor_area" : "11",
    "bath_room" : "11",
    "bed_room" : "11",
    "prominent_point" : "จุดเด่น",    
    "view_type" : "11",
    "direction_type" : "11",
    "addr_province": "กรุงเทพมหานคร",
    "addr_district": "สายไหม",
    "addr_sub_district": "สายไหม",
    "addr_road": "ถนน",
    "addr_soi": "ซอย",
    "addr_near_by": "สถานที่ใกล้เคียง",
    "floorarea_sqm": "พื้นที่",
    
    "land_size_rai": "ขนาดที่ดินเป็นไร่",
    "land_size_ngan": "ขนาดที่ดินเป็นงาน",
    "land_size_wa": "50",
    
    "name": "amarin",
    "tel": "test",
    "email": "test",
    "line": "test",
    "web": [
        {
            "ds_name": "''' + self.web_name + '''",
            "ds_id": "4",              
            "user": "''' + self.login_user + '''",
            "pass": "''' + self.login_pass + '''"
        }
    ]
}
'''
        return json_string

    def get_edit_post_json_string(self):
        json_string = '''
{
    "action": "create_post",
    "timeout": "5",
    "post_img_url_lists": [
        "http://imagestore.com/pic1.jpg",
        "http://imagestore.com/pic2.jpg"
    ],
    "geo_latitude": "13.786862",
    "geo_longitude": "100.757815",    
    "property_id" : "A01",
    "post_title_th": "ขายบ้านเดี่ยว 2 ชั้น",
    "short_post_title_th": "test",
    "post_description_th": "test",
    "post_title_en": "testtest",
    "short_post_title_en": "testtest",
    "post_description_en": "testtest",
    "price_baht": "30000000",
    
    "listing_type": "ขาย",    
    "property_type": "house",    
    "floor_level" : "11",
    "floor_total" : "11",
    "floor_area" : "11",
    "bath_room" : "11",
    "bed_room" : "11",
    "prominent_point" : "จุดเด่น",    
    "view_type" : "11",
    "direction_type" : "11",
    "addr_province": "กรุงเทพมหานคร",
    "addr_district": "สายไหม",
    "addr_sub_district": "สายไหม",
    "addr_road": "ถนน",
    "addr_soi": "ซอย",
    "addr_near_by": "สถานที่ใกล้เคียง",
    "floorarea_sqm": "พื้นที่",
    
    "land_size_rai": "ขนาดที่ดินเป็นไร่",
    "land_size_ngan": "ขนาดที่ดินเป็นงาน",
    "land_size_wa": "50",
    
    "name": "amarin",
    "tel": "test",
    "email": "test",
    "line": "test",
    "web": [
        {
            "ds_name": "''' + self.web_name + '''",
            "ds_id": "4",              
            "user": "''' + self.login_user + '''",
            "pass": "''' + self.login_pass + '''"
        }
    ]
}
'''
        return json_string